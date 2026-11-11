import datetime
import tempfile
import unittest
from pathlib import Path

from tools.kb import learnmap, learning
from tools.kb.parse import load_dir
from tests.test_kb import Vault, page_text


def pages_chain():
    v = Vault()
    v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", title="A", status="stub", relations="[{rel: prerequisite_for, id: cpt_bbbbbbbb}]"))
    v.add("concepts", "b.md", page_text("cpt_bbbbbbbb", title="B", status="stub", relations="[{rel: prerequisite_for, id: cpt_cccccccc}]"))
    v.add("concepts", "c.md", page_text("cpt_cccccccc", title="C", status="stub"))
    v.add("concepts", "z.md", page_text("cpt_zzzzzzzz", title="Z", status="stub").replace("domains: [ai]", "domains: [other]"))
    return v, load_dir(v.root)


class MapTests(unittest.TestCase):
    def test_depth_state_and_gaps(self):
        v, pages = pages_chain()
        self.addCleanup(v.tmp.cleanup)
        m = learnmap.compute_map(pages, {"cpt_aaaaaaaa": 0, "cpt_bbbbbbbb": 4}, {}, {}, "ai")
        by = {n["title"]: n for n in m["nodes"]}
        self.assertEqual([by["A"]["depth"], by["B"]["depth"], by["C"]["depth"]], [0, 1, 2])
        self.assertEqual(by["A"]["state"], "ready")
        self.assertEqual(by["B"]["state"], "mastered")
        self.assertTrue(by["B"]["gaps"], "mastered B sits on an unmastered prerequisite A: a foundation gap")
        self.assertEqual(by["C"]["state"], "ready")  # its only prerequisite B is mastered
        self.assertNotIn("Z", by)  # other subject, not an ancestor

    def test_subject_filter_includes_external_ancestors(self):
        v = Vault()
        self.addCleanup(v.tmp.cleanup)
        v.add("concepts", "m.md", page_text("cpt_mmmmmmmm", title="Math", status="stub", relations="[{rel: prerequisite_for, id: cpt_aaaaaaaa}]").replace("domains: [ai]", "domains: [science]"))
        v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", title="A", status="stub"))
        m = learnmap.compute_map(load_dir(v.root), {}, {}, {}, "ai")
        ext = {n["title"]: n["external"] for n in m["nodes"]}
        self.assertEqual(ext, {"Math": True, "A": False})
        self.assertEqual(m["summary"]["total"], 1)

    def test_low_accuracy_and_misconceptions_flagged(self):
        v, pages = pages_chain()
        self.addCleanup(v.tmp.cleanup)
        m = learnmap.compute_map(pages, {}, {"cpt_aaaaaaaa": {"reviews": 5, "accuracy": 0.2}}, {"cpt_aaaaaaaa": 2}, "ai")
        a = next(n for n in m["nodes"] if n["title"] == "A")
        self.assertEqual(len(a["gaps"]), 2)

    def test_cycle_does_not_hang(self):
        v = Vault()
        self.addCleanup(v.tmp.cleanup)
        v.add("concepts", "a.md", page_text("cpt_aaaaaaaa", title="A", status="stub", relations="[{rel: prerequisite_for, id: cpt_bbbbbbbb}]"))
        v.add("concepts", "b.md", page_text("cpt_bbbbbbbb", title="B", status="stub", relations="[{rel: prerequisite_for, id: cpt_aaaaaaaa}]"))
        self.assertEqual(len(learnmap.compute_map(load_dir(v.root), {}, {}, {}, "ai")["nodes"]), 2)


class StreakStatsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.con = learning.connect(Path(self.tmp.name) / "l.db")
        self.today = datetime.date(2026, 11, 8)

    def add_review(self, day, grade=4, card="cpt_aaaaaaaa:x"):
        self.con.execute("INSERT INTO reviews(card_id,day,grade) VALUES (?,?,?)", (card, day.isoformat(), grade))
        self.con.commit()

    def test_streak_counts_consecutive_days(self):
        for n in (0, 1, 2, 4):
            self.add_review(self.today - datetime.timedelta(days=n))
        s = learnmap.streak(self.con, self.today)
        self.assertEqual((s["current"], s["today_done"]), (3, True))

    def test_streak_alive_if_yesterday_dead_if_older(self):
        self.add_review(self.today - datetime.timedelta(days=1))
        self.assertEqual(learnmap.streak(self.con, self.today)["current"], 1)
        self.assertEqual(learnmap.streak(self.con, self.today + datetime.timedelta(days=3))["current"], 0)

    def test_review_stats_accuracy(self):
        for g in (5, 1, 4, 0):
            self.add_review(self.today, g)
        st = learnmap.review_stats(self.con)["cpt_aaaaaaaa"]
        self.assertEqual((st["reviews"], st["accuracy"]), (4, 0.5))


class SubjectsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.vault = Path(self.tmp.name)
        (self.vault / "domains.yml").write_text("ai: Artificial intelligence\nscience: Natural sciences\n")

    def test_old_format_loads_with_defaults(self):
        s = learnmap.load_subjects(self.vault)
        self.assertEqual(s["ai"]["description"], "Artificial intelligence")
        self.assertTrue(s["ai"]["color"].startswith("#"))

    def test_add_subject_persists_and_keeps_existing(self):
        learnmap.add_subject(self.vault, "history", "World History", "Past events", "#aa5500", "🏛")
        s = learnmap.load_subjects(self.vault)
        self.assertEqual(set(s), {"ai", "science", "history"})
        self.assertEqual(s["history"]["name"], "World History")
        from tools.kb.validate import load_domains
        self.assertEqual(load_domains(self.vault), {"ai", "science", "history"})

    def test_add_subject_rejects_bad_input(self):
        for args in (("Bad Key", "x"), ("ai", "Dup"), ("ok-key", ""), ("ok-key", "N", "", "red")):
            with self.assertRaises(ValueError):
                learnmap.add_subject(self.vault, *args)


class ValidationTests(unittest.TestCase):
    def test_conceptmap_normalises_and_drops_bad_edges(self):
        raw = {"nodes": [{"id": "A", "label": "Core", "kind": "core", "vault_slug": "self-attention"}, {"id": "b", "label": "B", "kind": "weird"},
                         {"id": "c", "label": "C"}, {"id": "a", "label": "dup"}],
               "edges": [{"from": "A", "to": "b", "label": "needs"}, {"from": "a", "to": "nope"}, {"from": "c", "to": "c"}]}
        m = learnmap.validate_conceptmap(raw, {"self-attention"})
        self.assertEqual([n["id"] for n in m["nodes"]], ["a", "b", "c"])
        self.assertEqual(m["nodes"][1]["kind"], "related")
        self.assertEqual(m["nodes"][0]["vault_slug"], "self-attention")
        self.assertEqual(len(m["edges"]), 1)

    def test_conceptmap_rejects_unusable(self):
        for bad in ({}, {"nodes": [], "edges": []}, {"nodes": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}], "edges": []}):
            with self.assertRaises(ValueError):
                learnmap.validate_conceptmap(bad, set())

    def test_conceptmap_unknown_slug_is_dropped(self):
        raw = {"nodes": [{"id": "a", "label": "A", "vault_slug": "made-up"}, {"id": "b", "label": "B"}, {"id": "c", "label": "C"}], "edges": [{"from": "a", "to": "b"}]}
        self.assertIsNone(learnmap.validate_conceptmap(raw, set())["nodes"][0]["vault_slug"])

    def test_build_task_validation(self):
        t = learnmap.validate_build_task({"title": "T", "steps": ["s1", "s2"], "hints": ["h"] * 9, "time_minutes": "30"})
        self.assertEqual((len(t["hints"]), t["time_minutes"]), (4, 30))
        with self.assertRaises(ValueError):
            learnmap.validate_build_task({"title": "T", "steps": []})


if __name__ == "__main__":
    unittest.main()


class UserMapTests(unittest.TestCase):
    def good(self):
        return {"title": " My map ", "nodes": [{"id": "n1", "label": "A", "x": 10, "y": 20, "page": "self-attention"}, {"id": "n2", "label": "B", "color": "weird"}],
                "edges": [{"id": "e1", "from": "n1", "to": "n2", "label": "leads to"}]}

    def test_valid_map_is_normalised(self):
        m = learnmap.validate_usermap(self.good())
        self.assertEqual(m["title"], "My map")
        self.assertEqual(m["nodes"][1]["color"], "auto")
        self.assertEqual(m["nodes"][0]["page"], "self-attention")
        self.assertEqual(len(m["edges"]), 1)

    def test_dangling_and_self_links_are_dropped(self):
        d = self.good()
        d["edges"] += [{"id": "e2", "from": "n1", "to": "nope"}, {"id": "e3", "from": "n1", "to": "n1"}]
        self.assertEqual(len(learnmap.validate_usermap(d)["edges"]), 1)

    def test_rejects_bad_ids_duplicates_and_sizes(self):
        for mutate in (lambda d: d["nodes"].append({"id": "n1", "label": "dup"}),
                       lambda d: d["nodes"].append({"id": "BAD ID!", "label": "x"}),
                       lambda d: d["nodes"].__setitem__(0, {"id": "n1", "label": "x", "x": "not a number"}),
                       lambda d: d.__setitem__("nodes", [{"id": f"n{i}", "label": "x"} for i in range(301)])):
            d = self.good()
            mutate(d)
            with self.assertRaises(ValueError):
                learnmap.validate_usermap(d)

    def test_text_is_truncated_and_positions_clamped(self):
        d = self.good()
        d["nodes"][0].update({"label": "x" * 500, "note": "y" * 5000, "x": 1e12})
        n = learnmap.validate_usermap(d)["nodes"][0]
        self.assertEqual((len(n["label"]), len(n["note"]), n["x"]), (120, 1000, 50000.0))

    def test_map_id_pattern_blocks_path_tricks(self):
        for bad in ("../etc", "a/b", "ab", "UPPER", ".hidden"):
            self.assertIsNone(learnmap.MAP_ID.fullmatch(bad))
        self.assertTrue(learnmap.MAP_ID.fullmatch("my-map-1a2b3"))
