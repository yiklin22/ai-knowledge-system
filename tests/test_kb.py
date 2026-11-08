import datetime
import tempfile
import unittest
from pathlib import Path

from tools.kb import learning
from tools.kb.parse import load_dir, human_blocks
from tools.kb.validate import human_blocks_preserved, validate

TODAY = datetime.date(2026, 11, 8)


def page_text(id, type="concept", title="T", extra="", body="", sources="[]", relations="[]", status="draft"):
    return f"""---
id: {id}
schema: 2
type: {type}
title: "{title}"
aliases: []
domains: [ai]
summary: s
tags: []
status: {status}
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: {sources}
relations: {relations}
{extra}---
{body}
"""


class Vault:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "raw").mkdir()

    def add(self, folder, name, text):
        d = self.root / folder
        d.mkdir(exist_ok=True)
        (d / name).write_text(text, encoding="utf-8")

    def check(self):
        return validate(load_dir(self.root), {"ai"}, root=self.root, today=TODAY)


class ValidateTests(unittest.TestCase):
    def setUp(self):
        self.v = Vault()

    def errs(self):
        return "\n".join(self.v.check()[0])

    def test_valid_stub_passes(self):
        self.v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", status="stub"))
        self.assertEqual(self.v.check()[0], [])

    def test_duplicate_ids(self):
        self.v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", title="A", status="stub"))
        self.v.add("concepts", "b.md", page_text("cpt_aaaaaaaa", title="B", status="stub"))
        self.assertIn("duplicate id", self.errs())

    def test_duplicate_title_detected(self):
        self.v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", title="RAG", status="stub"))
        self.v.add("concepts", "b.md", page_text("cpt_bbbbbbbb", title="rag", status="stub"))
        self.assertIn("possible duplicate", self.errs())

    def test_bad_id_format_and_wrong_folder(self):
        self.v.add("claims", "a.md", page_text("cpt_aaaaaaaa", status="stub"))
        self.assertIn("belongs in folder", self.errs())

    def test_broken_relation_id(self):
        self.v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", status="stub", relations="[{rel: related, id: cpt_zzzzzzzz}]"))
        self.assertIn("unknown id", self.errs())

    def test_unresolved_relation_is_warning_not_error(self):
        self.v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", status="stub", relations='[{rel: related, unresolved: "Thing"}]'))
        errors, warnings = self.v.check()
        self.assertEqual(errors, [])
        self.assertTrue(any("unresolved" in w for w in warnings))

    def test_unknown_rel(self):
        self.v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", status="stub", relations="[{rel: likes, id: cpt_aaaaaaaa}]"))
        self.assertIn("bad relation", self.errs())

    def test_broken_wikilink(self):
        self.v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", status="stub", body="see [[nowhere]]"))
        self.assertIn("broken wikilink", self.errs())

    def test_wikilink_resolves_by_filename(self):
        self.v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", title="A", status="stub", body="see [[b]]"))
        self.v.add("concepts", "b.md", page_text("cpt_bbbbbbbb", title="B", status="stub"))
        self.assertEqual(self.v.check()[0], [])

    def test_non_stub_concept_needs_source(self):
        self.v.add("concepts", "a.md", page_text("cpt_aaaaaaaa"))
        self.assertIn("at least one source", self.errs())

    def test_citation_must_be_source_page(self):
        self.v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", sources="[{id: src_nope0000, locator: p1, quote: null}]"))
        self.assertIn("does not resolve", self.errs())

    def _source(self, text="The quick brown fox."):
        (self.v.root / "raw" / "s.md").write_text(text, encoding="utf-8")
        self.v.add("sources", "s.md", page_text("src_aaaaaaaa", "source", "S", status="stub",
                   extra="kind: web\nreliability: secondary\nraw: raw/s.md\n"))

    def test_real_quote_passes(self):
        self._source("The quick\n brown fox.")
        self.v.add("concepts", "a.md", page_text("cpt_bbbbbbbb", sources='[{id: src_aaaaaaaa, locator: p1, quote: "quick brown fox"}]'))
        self.assertEqual(self.v.check()[0], [])

    def test_fabricated_quote_rejected(self):
        self._source()
        self.v.add("concepts", "a.md", page_text("cpt_bbbbbbbb", sources='[{id: src_aaaaaaaa, locator: p1, quote: "lazy dog"}]'))
        self.assertIn("quote not found", self.errs())

    def test_quote_without_locator_rejected(self):
        self._source()
        self.v.add("concepts", "a.md", page_text("cpt_bbbbbbbb", sources='[{id: src_aaaaaaaa, quote: "quick"}]'))
        self.assertIn("needs a locator", self.errs())

    def test_source_missing_raw_file(self):
        self.v.add("sources", "s.md", page_text("src_aaaaaaaa", "source", "S", status="stub",
                   extra="kind: web\nreliability: secondary\nraw: raw/missing.md\n"))
        self.assertIn("raw file not found", self.errs())

    def test_stale_volatile_warning(self):
        self.v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", status="stub", extra="volatile: true\nlast_verified: 2026-01-01\n"))
        self.assertTrue(any("stale" in w for w in self.v.check()[1]))

    def test_invalid_domain(self):
        self.v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", status="stub").replace("domains: [ai]", "domains: [zzz]"))
        self.assertIn("not in vault/domains.yml", self.errs())


class HumanBlockTests(unittest.TestCase):
    def test_preserved(self):
        old = "x <!-- human -->mine<!-- /human --> y"
        self.assertEqual(human_blocks(old), ["mine"])
        self.assertEqual(human_blocks_preserved(old, "z <!-- human -->mine<!-- /human -->"), [])

    def test_removed_or_altered_detected(self):
        old = "<!-- human -->mine<!-- /human -->"
        self.assertEqual(human_blocks_preserved(old, "nothing"), ["mine"])
        self.assertEqual(human_blocks_preserved(old, "<!-- human -->changed<!-- /human -->"), ["mine"])


class LearningTests(unittest.TestCase):
    def test_sync_keeps_progress_and_sm2_schedules(self):
        tmp = tempfile.TemporaryDirectory()
        con = learning.connect(Path(tmp.name) / "l.db")
        d = Vault()
        d.add("concepts", "a.md", page_text("cpt_aaaaaaaa", status="stub", extra='recall:\n  - {q: "Q1", a: "A1"}\n'))
        pages = load_dir(d.root)
        self.assertEqual(learning.sync(con, pages, TODAY), (1, 0))
        cid = learning.due(con, TODAY)[0][0]
        learning.grade(con, cid, 5, TODAY)
        self.assertEqual(learning.due(con, TODAY), [])
        self.assertEqual(learning.sync(con, pages, TODAY), (0, 0))  # idempotent, progress kept
        self.assertEqual(con.execute("SELECT reps FROM cards").fetchone()[0], 1)
        learning.grade(con, cid, 1, TODAY)  # forgot -> interval resets
        self.assertEqual(con.execute("SELECT reps, interval FROM cards").fetchone(), (0, 1))
        self.assertEqual(learning.sync(con, [], TODAY), (0, 1))  # card removed from vault -> deactivated


class TutorTests(unittest.TestCase):
    def _pages(self):
        d = Vault()
        d.add("concepts", "a.md", page_text("cpt_aaaaaaaa", title="A", status="stub", relations="[{rel: prerequisite_for, id: cpt_bbbbbbbb}]"))
        d.add("concepts", "b.md", page_text("cpt_bbbbbbbb", title="B", status="stub", relations="[{rel: prerequisite_for, id: cpt_cccccccc}]"))
        d.add("concepts", "c.md", page_text("cpt_cccccccc", title="C", status="stub"))
        self.d = d
        return load_dir(d.root)

    def test_next_respects_prerequisites(self):
        pages = self._pages()
        topics, _ = learning.next_topics(pages, {})
        self.assertEqual([p.fm["title"] for p, _ in topics], ["A"])
        topics, _ = learning.next_topics(pages, {"cpt_aaaaaaaa": 3})
        self.assertEqual([p.fm["title"] for p, _ in topics], ["B"])
        topics, _ = learning.next_topics(pages, {"cpt_aaaaaaaa": 2})
        self.assertEqual([p.fm["title"] for p, _ in topics], ["A"])  # level 2 is not mastered

    def test_record_session_tracks_mastery_and_misconceptions(self):
        con = learning.connect(Path(tempfile.mkdtemp()) / "l.db")
        learning.record_session(con, "cpt_aaaaaaaa", 2, ["thinks X is Y"], note="n", today=TODAY)
        self.assertEqual(learning.mastery_map(con), {"cpt_aaaaaaaa": 2})
        self.assertEqual(learning.open_misconceptions(con, "cpt_aaaaaaaa"), ["thinks X is Y"])
        learning.record_session(con, "cpt_aaaaaaaa", 4, resolved=["X is Y"], today=TODAY)
        self.assertEqual(learning.mastery_map(con), {"cpt_aaaaaaaa": 4})
        self.assertEqual(learning.open_misconceptions(con, "cpt_aaaaaaaa"), [])


if __name__ == "__main__":
    unittest.main()
