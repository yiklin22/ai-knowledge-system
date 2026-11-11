"""Tests for the evaluation and operations layer: metrics, digest-quality eval, red team, MCP server, sample vault."""
import io
import json
import tempfile
import unittest
from pathlib import Path

from tools.kb import agent, digest_eval, mcp_server, metrics, ops, redteam, sandbox
from tools.kb.parse import load_dir
from tools.kb.schema import ROOT
from tools.kb.validate import load_domains, raw_file, validate
from tests.test_kb import page_text
from tests.test_ops import make_root, put

DEMO = ROOT / "demo"


class MetricsTests(unittest.TestCase):
    def setUp(self):
        self.tmp, self.root = make_root()
        self.addCleanup(self.tmp.cleanup)

    def test_empty_log_gives_no_data_not_zero_or_a_crash(self):
        s = metrics.summary(metrics.load(self.root))
        self.assertIsNone(s["review"]["batch_approval_rate"])
        self.assertIsNone(s["digest"]["cost_per_source"])
        self.assertIn("no data", metrics.render(s))

    def test_cost_per_source_and_approval_rate(self):
        metrics.record(self.root, "digest", sources=4, pages=10, valid=True, cost_usd=2.0, seconds=100)
        metrics.record(self.root, "digest", sources=1, pages=2, valid=False)          # crashed before a cost was reported
        metrics.record(self.root, "review", decision="approved", pages=9, amended=1)
        metrics.record(self.root, "review", decision="discarded", pages=3)
        s = metrics.summary(metrics.load(self.root))
        self.assertEqual(s["digest"]["cost_per_source"], 0.5)                      # the run without a cost is not counted as free
        self.assertEqual(s["digest"]["first_pass_valid"], 0.5)
        self.assertEqual(s["review"]["batch_approval_rate"], 0.5)
        self.assertEqual(s["review"]["page_approval_rate"], 0.75)

    def test_a_corrupt_line_does_not_hide_the_rest(self):
        metrics.record(self.root, "ask", cost_usd=0.01, seconds=3)
        with open(self.root / metrics.FILE, "a") as f:
            f.write('{"kind": "ask", "cost')
        self.assertEqual(len(metrics.load(self.root)), 1)

    def test_approve_and_discard_are_recorded(self):
        put(self.root, "proposals/b1/concepts/a.md", page_text("cpt_aaaaaaaa", title="A", status="stub"))
        put(self.root, "proposals/b2/concepts/b.md", page_text("cpt_bbbbbbbb", title="B", status="stub"))
        self.assertTrue(ops.approve_batch(self.root, "b1")["ok"])
        self.assertTrue(ops.discard_batch(self.root, "b2")["ok"])
        self.assertEqual([(e["decision"], e["pages"]) for e in metrics.load(self.root)], [("approved", 1), ("discarded", 1)])

    def test_result_event_fields(self):
        u = metrics.from_result_event({"total_cost_usd": 0.42, "duration_ms": 61500, "num_turns": 9, "usage": {"input_tokens": 10, "output_tokens": 20}})
        self.assertEqual((u["cost_usd"], u["seconds"], u["turns"], u["output_tokens"], u["ok"]), (0.42, 61.5, 9, 20, True))


class RawConfinementTests(unittest.TestCase):
    """Found by the red team (K6): evidence may only be verified against files inside raw/."""

    def setUp(self):
        self.tmp, self.root = make_root()
        self.addCleanup(self.tmp.cleanup)
        put(self.root, "raw/web/a.md", "real text")
        put(self.root, "proposals/b/sources/x.md", "invented quote")

    def test_only_files_inside_raw_count(self):
        self.assertIsNotNone(raw_file(self.root, "raw/web/a.md"))
        for bad in ("proposals/b/sources/x.md", "raw/../proposals/b/sources/x.md", "/etc/passwd", "raw/web/missing.md", "raw"):
            self.assertIsNone(raw_file(self.root, bad), bad)


class DigestEvalTests(unittest.TestCase):
    def test_sample_vault_scores(self):
        r = digest_eval.evaluate(DEMO)
        c = r["citations"]
        self.assertEqual(r["errors"], [])
        self.assertGreater(c["with_quote"], 5)
        self.assertEqual(c["verbatim"], c["with_quote"])
        self.assertEqual(c["not_verbatim"], [])
        self.assertIn("Quotes found verbatim", digest_eval.render(r))

    def test_near_duplicate_titles_are_flagged_and_distinct_ones_are_not(self):
        tmp, root = make_root()
        self.addCleanup(tmp.cleanup)
        put(root, "vault/concepts/a.md", page_text("cpt_aaaaaaaa", title="Retrieval-augmented generation", status="stub"))
        put(root, "vault/concepts/b.md", page_text("cpt_bbbbbbbb", title="Retrieval augmented generation (RAG)", status="stub"))
        put(root, "vault/concepts/c.md", page_text("cpt_cccccccc", title="Gradient descent", status="stub"))
        d = digest_eval.near_duplicates(load_dir(root / "vault"))
        self.assertEqual(len(d), 1)
        self.assertNotIn("Gradient descent", d[0][:2])

    def test_judge_reply_is_parsed_strictly(self):
        good = 'Here you go:\n[{"case": 1, "verdict": "supported", "why": "x"}, {"case": 2, "verdict": "maybe"}]'
        self.assertEqual([v["verdict"] for v in digest_eval.parse_judgement(good, 3)], ["supported", "invalid", "invalid"])
        self.assertEqual([v["verdict"] for v in digest_eval.parse_judgement("no json at all", 1)], ["invalid"])

    def test_judge_cases_are_seeded_and_label_passages_untrusted(self):
        pages = load_dir(DEMO / "vault")
        a, b = digest_eval.judge_cases(pages, DEMO, 2), digest_eval.judge_cases(pages, DEMO, 2)
        self.assertEqual([c["id"] for c in a], [c["id"] for c in b])
        self.assertEqual(len(a), 2)
        prompt = digest_eval.judge_prompt(a)
        self.assertLess(prompt.index("untrusted DATA"), prompt.index("### Case 1"))


class PermissionModelTests(unittest.TestCase):
    def test_the_work_the_agent_needs_is_allowed(self):
        for tool, target in (("Read", "raw/web/x.md"), ("Write", "proposals/b/concepts/x.md"), ("Edit", "proposals/b/claims/y.md"),
                             ("Bash", "./kb new b concept \"Title\" --domain ai"), ("Bash", "./kb validate --proposals b")):
            self.assertTrue(agent.is_allowed(tool, target), (tool, target))

    def test_everything_else_is_refused(self):
        for tool, target in (("Write", "vault/concepts/x.md"), ("Write", "proposals/../vault/x.md"), ("Edit", "raw/web/x.md"), ("Edit", "CLAUDE.md"),
                             ("Write", "/etc/cron.d/x"), ("Bash", "./kb approve b"), ("Bash", "./kb validate && ./kb approve b"),
                             ("Bash", "./kb newer"), ("Bash", "rm -rf vault"), ("WebFetch", "https://example.org"), ("Task", "")):
            self.assertFalse(agent.is_allowed(tool, target), (tool, target))


class RedTeamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = redteam.structural(redteam.load_attacks())

    def test_every_attack_that_needs_an_action_or_a_forged_page_is_blocked(self):
        self.assertEqual([r["id"] for r in self.rows if r["verdict"] == "NOT BLOCKED"], [])
        self.assertGreaterEqual(sum(1 for r in self.rows if r["verdict"] == "blocked"), 18)

    def test_hostile_text_is_always_in_the_untrusted_block(self):
        self.assertTrue(all(r["prompt"]["blocked"] for r in self.rows))

    def test_the_suite_can_fail(self):
        """Guard against a suite that passes whatever the policy is: with no deny rules and a shell, attacks get through."""
        loose = [a for a in redteam.load_attacks() if a["attempts"]]
        leaked = [a["id"] for a in loose if any(agent.is_allowed(x["tool"], redteam.fill(x["target"]), allow=["Bash", "Write", "Edit", "WebFetch"], deny=[]) for x in a["attempts"])]
        held = {a["id"] for a in loose} - set(leaked)
        self.assertEqual(held, {"P2"})   # only command chaining is refused regardless of the lists


class McpTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = sandbox.build(Path(self.tmp.name) / "kb")
        ops.rebuild(self.root)

    def call(self, method, params=None, mid=1):
        return mcp_server.handle({"jsonrpc": "2.0", "id": mid, "method": method, "params": params or {}}, self.root)

    def tool(self, name, **args):
        return self.call("tools/call", {"name": name, "arguments": args})["result"]

    def test_handshake_and_tool_list(self):
        init = self.call("initialize", {"protocolVersion": "2025-03-26"})["result"]
        self.assertEqual(init["protocolVersion"], "2025-03-26")
        self.assertEqual(self.call("initialize", {"protocolVersion": "1999-01-01"})["result"]["protocolVersion"], mcp_server.PROTOCOL_VERSIONS[0])
        self.assertIsNone(mcp_server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}, self.root))
        tools = self.call("tools/list")["result"]["tools"]
        self.assertEqual({t["name"] for t in tools}, set(mcp_server.HANDLERS))

    def test_no_tool_can_write(self):
        before = {d: sandbox.tree_hash(self.root / d) for d in ("vault", "raw", "proposals")}
        self.tool("search_vault", query="approval")
        self.tool("get_page", page="Human approval gate")
        self.tool("find_passages", question="how are rankings merged?")
        self.tool("list_open_questions")
        self.tool("vault_status")
        self.assertEqual(before, {d: sandbox.tree_hash(self.root / d) for d in before})
        self.assertFalse(any(w in t["name"] for t in mcp_server.TOOLS for w in ("write", "add", "approve", "propose", "delete")))

    def test_page_comes_back_with_its_evidence(self):
        r = self.tool("get_page", page="Human approval gate")
        self.assertFalse(r["isError"])
        text = r["content"][0]["text"]
        self.assertIn("only a person runs approve", text)      # the verbatim quote
        self.assertIn("Key decisions and trade-offs", text)    # its locator

    def test_retrieval_marks_raw_sources_untrusted(self):
        text = self.tool("find_passages", question="reciprocal-rank fusion", k=8)["content"][0]["text"]
        self.assertIn("approved page", text)
        self.assertIn("UNREVIEWED raw", text)
        only = self.tool("find_passages", question="reciprocal-rank fusion", include_raw_sources=False)["content"][0]["text"]
        self.assertNotIn("UNREVIEWED", only)

    def test_errors_are_reported_not_raised(self):
        self.assertTrue(self.tool("get_page", page="no such page")["isError"])
        self.assertEqual(self.call("tools/call", {"name": "approve_batch", "arguments": {}})["error"]["code"], -32602)
        self.assertEqual(self.call("tools/call", {"name": "get_page", "arguments": {"page": "x", "path": "/etc/passwd"}})["error"]["code"], -32602)
        self.assertEqual(self.call("resources/list")["error"]["code"], -32601)

    def test_stdio_loop_survives_garbage(self):
        out = io.StringIO()
        mcp_server.serve(io.StringIO('not json\n\n{"jsonrpc":"2.0","id":7,"method":"ping"}\n'), out, self.root)
        replies = [json.loads(x) for x in out.getvalue().splitlines()]
        self.assertEqual(replies[0]["error"]["code"], -32700)
        self.assertEqual(replies[1], {"jsonrpc": "2.0", "id": 7, "result": {}})


class SampleVaultTests(unittest.TestCase):
    def test_sample_vault_and_its_pending_batch_are_valid(self):
        errors, _ = validate(load_dir(DEMO / "vault"), load_domains(DEMO / "vault"), root=DEMO)
        self.assertEqual(errors, [])
        self.assertTrue(ops.batch_report(DEMO, "demo-review-me")["ok"])

    def test_sample_ids_do_not_collide_with_the_real_vault(self):
        mine = {p.id for p in load_dir(ROOT / "vault")}
        self.assertFalse(mine & {p.id for p in load_dir(DEMO / "vault")})


if __name__ == "__main__":
    unittest.main()
