import tempfile
import unittest
from pathlib import Path

from tools.kb import ops
from tests.test_kb import page_text


def make_root():
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    for d in ("vault/concepts", "vault/sources", "proposals", "raw", "data"):
        (root / d).mkdir(parents=True, exist_ok=True)
    (root / "vault" / "domains.yml").write_text("ai: x\n")
    (root / "vault" / "log.md").write_text("# Log\n")
    return tmp, root


def put(root, rel, text):
    f = root / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8")


class OpsTests(unittest.TestCase):
    def setUp(self):
        self.tmp, self.root = make_root()
        self.addCleanup(self.tmp.cleanup)

    def test_approve_adds_page_and_marks_reviewed_and_logs(self):
        put(self.root, "proposals/b1/concepts/a.md", page_text("cpt_aaaaaaaa", title="A", status="stub").replace("status: stub", "status: draft"))
        # a draft concept with no sources is invalid, so use a stub-style valid page instead
        put(self.root, "proposals/b1/concepts/a.md", page_text("cpt_aaaaaaaa", title="A", status="stub"))
        res = ops.approve_batch(self.root, "b1")
        self.assertTrue(res["ok"], res)
        self.assertTrue((self.root / "vault/concepts/a.md").exists())
        self.assertFalse((self.root / "proposals/b1").exists())
        self.assertIn("approve | b1", (self.root / "vault/log.md").read_text())

    def test_invalid_batch_is_not_approved_and_stays(self):
        put(self.root, "proposals/b1/concepts/a.md", page_text("cpt_aaaaaaaa", title="A"))  # draft, no source
        res = ops.approve_batch(self.root, "b1")
        self.assertFalse(res["ok"])
        self.assertTrue((self.root / "proposals/b1/concepts/a.md").exists())
        self.assertFalse((self.root / "vault/concepts/a.md").exists())

    def test_amendment_requires_explicit_flag(self):
        put(self.root, "vault/concepts/a.md", page_text("cpt_aaaaaaaa", title="A", status="stub"))
        put(self.root, "proposals/b1/concepts/a.md", page_text("cpt_aaaaaaaa", title="A", status="stub", body="new text"))
        self.assertFalse(ops.approve_batch(self.root, "b1")["ok"])
        self.assertNotIn("new text", (self.root / "vault/concepts/a.md").read_text())
        self.assertTrue(ops.approve_batch(self.root, "b1", amend=True)["ok"])
        self.assertIn("new text", (self.root / "vault/concepts/a.md").read_text())

    def test_amendment_cannot_remove_human_authored_text(self):
        put(self.root, "vault/concepts/a.md", page_text("cpt_aaaaaaaa", title="A", status="stub", body="<!-- human -->mine<!-- /human -->"))
        put(self.root, "proposals/b1/concepts/a.md", page_text("cpt_aaaaaaaa", title="A", status="stub", body="rewritten"))
        res = ops.approve_batch(self.root, "b1", amend=True)
        self.assertFalse(res["ok"])
        self.assertIn("mine", (self.root / "vault/concepts/a.md").read_text())

    def test_filename_collision_with_different_id_blocked(self):
        put(self.root, "vault/concepts/a.md", page_text("cpt_aaaaaaaa", title="A", status="stub"))
        put(self.root, "proposals/b1/concepts/a.md", page_text("cpt_bbbbbbbb", title="B", status="stub"))
        self.assertFalse(ops.approve_batch(self.root, "b1")["ok"])

    def test_discard_only_inside_proposals(self):
        put(self.root, "proposals/b1/concepts/a.md", page_text("cpt_aaaaaaaa", title="A", status="stub"))
        self.assertFalse(ops.discard_batch(self.root, "../vault")["ok"])
        self.assertTrue((self.root / "vault").exists())
        self.assertTrue(ops.discard_batch(self.root, "b1")["ok"])

    def test_diff_shows_amendment(self):
        put(self.root, "vault/concepts/a.md", page_text("cpt_aaaaaaaa", title="A", status="stub", body="old"))
        put(self.root, "proposals/b1/concepts/a.md", page_text("cpt_aaaaaaaa", title="A", status="stub", body="new"))
        d = ops.batch_diff(self.root, "b1", "a.md")
        self.assertEqual(d["action"], "amend")
        self.assertIn("+new", d["diff"])


if __name__ == "__main__":
    unittest.main()
