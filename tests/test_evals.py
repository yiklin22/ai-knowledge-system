import json
import tempfile
import unittest
from pathlib import Path

from tools.kb import evals

DOCS = {
    "web/cache.md": "Prompt caching reuses earlier tokens so repeated context costs far less. Cached input is cheaper than fresh input.",
    "web/incident.md": "A blameless postmortem lists the timeline, the root cause and action items. Hold a second meeting for the follow-up actions.",
    "web/vector.md": "Approximate nearest neighbour search finds similar items quickly using item embeddings and an index such as HNSW.",
    "web/sre.md": "Service level objectives define reliability targets. An error budget is the allowed amount of failure before releases slow.",
    "videos/talk.md": "**[03:10]** Sandboxes limit what an agent can touch.\n\n**[07:45]** Permissions prompts keep a human approving risky shell commands.",
    "documents/paper.md": "<!-- page 1 -->\nThe Transformer uses self-attention instead of recurrence.\n\n<!-- page 2 -->\nMasking hides future positions in the decoder.",
    "web/cooking.md": "Braise the short ribs slowly with red wine, onion and thyme until the meat is tender.",
    "web/garden.md": "Tomato seedlings need six hours of direct sun and a stake once they pass thirty centimetres.",
}
CASES = [
    {"q": "Why does prompt caching make repeated context cheaper?", "expect": ["raw/web/cache.md"]},
    {"q": "What goes in a blameless postmortem?", "expect": ["raw/web/incident.md"]},
    {"q": "How do item embeddings help find similar items quickly?", "expect": ["raw/web/vector.md"]},
    {"q": "What is an error budget?", "expect": ["raw/web/sre.md"]},
    {"q": "How do sandboxes and permission prompts limit an agent?", "expect": ["raw/videos/talk.md"]},
    {"q": "How does the decoder hide future positions?", "expect": ["raw/documents/paper.md"]},
    {"q": "How long should I braise short ribs?", "expect": ["raw/web/cooking.md"]},
]


class RetrievalEvalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "vault").mkdir()
        for rel, text in DOCS.items():
            f = self.root / "raw" / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(f'---\ntitle: "{f.stem}"\n---\n\n{text}\n')

    def tearDown(self):
        self.tmp.cleanup()

    def test_keyword_retrieval_regression_floor(self):
        """If a change to chunking, ranking or the query builder drops these numbers, this fails."""
        s = evals.summarise(evals.run_retrieval(self.root, CASES, mode="keyword"))
        self.assertGreaterEqual(s["hit@5"], 0.85)
        self.assertGreaterEqual(s["mrr"], 0.7)

    def test_summarise_arithmetic(self):
        s = evals.summarise([1, 2, None, 6])
        self.assertEqual(s["hit@1"], 0.25)
        self.assertEqual(s["hit@5"], 0.5)
        self.assertEqual(s["hit@12"], 0.75)
        self.assertAlmostEqual(s["mrr"], (1 + 0.5 + 1 / 6) / 4)

    def test_groundedness_checks(self):
        ps = [{"n": 1, "text": "Cached input is cheaper than fresh input, and the doc says so plainly."}]
        self.assertEqual(evals.check_answer("Caching is cheaper [1].", ps), [])
        self.assertIn("no citations", evals.check_answer("Caching is cheaper.", ps))
        self.assertTrue(evals.check_answer("Caching is cheaper [2].", ps))

    def test_shipped_case_file_is_well_formed(self):
        cases = evals.load_cases(evals.ROOT / "evals" / "ask_cases.jsonl")
        self.assertGreaterEqual(len(cases), 20)
        for c in cases:
            self.assertTrue(c["q"].strip() and c["expect"] and all(e.endswith(".md") for e in c["expect"]))


if __name__ == "__main__":
    unittest.main()
