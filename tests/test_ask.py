import tempfile
import unittest
from pathlib import Path

from tools.kb import ask


class AskRetrievalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "raw" / "web").mkdir(parents=True)
        (self.root / "raw" / "videos").mkdir(parents=True)
        (self.root / "vault" / "concepts").mkdir(parents=True)
        (self.root / "raw" / "web" / "a.md").write_text('---\ntitle: "Harness post"\n---\n\nThe agent harness is the code around the model.\n')
        (self.root / "raw" / "videos" / "v.md").write_text('---\ntitle: "Talk"\n---\n\n**[00:10]** Intro talk about cooking.\n\n**[12:34]** The agent harness loops over tool calls.\n')
        (self.root / "vault" / "concepts" / "h.md").write_text('---\ntitle: "Agent harness"\n---\n\n# Agent harness\nApproved definition of a harness.\n')

    def tearDown(self):
        self.tmp.cleanup()

    def test_scope_filters(self):
        kinds = lambda **kw: {p["kind"] for p in ask.retrieve(self.root, "what is an agent harness", **kw)}
        self.assertEqual(kinds(), {"web", "videos", "vault"})
        self.assertEqual(kinds(vault=False, kinds=("videos",)), {"videos"})
        self.assertEqual(kinds(vault=True, kinds=()), {"vault"})

    def test_specific_paths_restrict_raw_sources(self):
        r = ask.retrieve(self.root, "agent harness", vault=False, paths=["raw/web/a.md"])
        self.assertEqual({p["path"] for p in r}, {"raw/web/a.md"})
        # paths outside the index are ignored, never read
        self.assertEqual(ask.retrieve(self.root, "agent harness", vault=False, paths=["../../etc/passwd"]), [{**p} for p in ask.retrieve(self.root, "agent harness", vault=False)])

    def test_locator_and_incremental_reindex(self):
        r = ask.retrieve(self.root, "tool calls loop", vault=False, kinds=("videos",))
        self.assertIn("tool calls", r[0]["text"])
        self.assertRegex(r[0]["locator"], r"^\d+:\d{2}$")  # passages merge short lines: locator is the first timestamp in the passage
        (self.root / "raw" / "web" / "b.md").write_text('---\ntitle: "New"\n---\n\nQuantum zebra.\n')
        self.assertTrue(ask.retrieve(self.root, "quantum zebra"))

    def test_stopword_only_question_returns_nothing(self):
        self.assertEqual(ask.retrieve(self.root, "what is the"), [])


if __name__ == "__main__":
    unittest.main()
