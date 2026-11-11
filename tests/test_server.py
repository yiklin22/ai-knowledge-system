import unittest

from fastapi.testclient import TestClient

from app import server

H = {"host": f"127.0.0.1:{server.PORT}"}


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.c = TestClient(server.app, base_url=f"http://127.0.0.1:{server.PORT}")

    def test_wrong_host_rejected(self):
        self.assertEqual(self.c.get("/api/state", headers={"host": "evil.example"}).status_code, 403)

    def test_state_ok_on_localhost(self):
        self.assertEqual(self.c.get("/api/state", headers=H).status_code, 200)

    def test_post_requires_token(self):
        self.assertEqual(self.c.post("/api/proposals/x/discard", headers=H).status_code, 403)
        self.assertEqual(self.c.post("/api/proposals/x/discard", headers={**H, "x-kb-token": "wrong"}).status_code, 403)

    def test_post_with_token_reaches_handler(self):
        r = self.c.post("/api/proposals/nonexistent-batch/discard", headers={**H, "x-kb-token": server.TOKEN})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(r.json()["ok"])

    def test_discard_cannot_escape_proposals(self):
        r = self.c.post("/api/proposals/..%2Fvault/discard", headers={**H, "x-kb-token": server.TOKEN})
        self.assertIn(r.status_code, (200, 400, 404))
        self.assertTrue((server.VAULT / "index.md").exists())

    def test_digest_rejects_unknown_paths(self):
        r = self.c.post("/api/digest", headers={**H, "x-kb-token": server.TOKEN}, json={"paths": ["../../etc/passwd"]})
        self.assertEqual(r.status_code, 400)

    def test_links_must_be_http(self):
        r = self.c.post("/api/intake/links", headers={**H, "x-kb-token": server.TOKEN}, json={"urls": ["file:///etc/passwd"]})
        self.assertEqual(r.status_code, 400)

    def test_index_page_embeds_token_and_headers(self):
        r = self.c.get("/", headers=H)
        self.assertIn(server.TOKEN, r.text)
        self.assertIn("default-src 'self'", r.headers["content-security-policy"])

    def test_clip_needs_key_and_extension_origin(self):
        ext = {**H, "origin": "chrome-extension://abc", "x-kb-clip-key": server.CLIP_KEY}
        body = {"url": "file:///etc/passwd"}
        self.assertEqual(self.c.post("/api/clip", headers=H, json=body).status_code, 403)
        self.assertEqual(self.c.post("/api/clip", headers={**ext, "x-kb-clip-key": "wrong"}, json=body).status_code, 403)
        self.assertEqual(self.c.post("/api/clip", headers={**ext, "origin": "https://evil.example"}, json=body).status_code, 403)
        # the normal page token does not open the clip endpoint, and the clip key does not open other endpoints
        self.assertEqual(self.c.post("/api/clip", headers={**H, "x-kb-token": server.TOKEN}, json=body).status_code, 403)
        self.assertEqual(self.c.post("/api/proposals/x/discard", headers=ext).status_code, 403)

    def test_clip_rejects_non_http(self):
        ext = {**H, "origin": "chrome-extension://abc", "x-kb-clip-key": server.CLIP_KEY}
        self.assertEqual(self.c.post("/api/clip", headers=ext, json={"url": "file:///etc/passwd"}).status_code, 400)

    def test_source_path_is_confined_to_raw(self):
        from fastapi import HTTPException
        with self.assertRaises(HTTPException):
            server.safe_under(server.RAW, "vault/index.md")


if __name__ == "__main__":
    unittest.main()


class PlaygroundAndSubjectTests(unittest.TestCase):
    def setUp(self):
        self.c = TestClient(server.app, base_url=f"http://127.0.0.1:{server.PORT}")

    def test_playground_is_served_sandboxed_with_no_network(self):
        r = self.c.get("/playground/gradient-descent.html", headers=H)
        self.assertEqual(r.status_code, 200)
        csp = r.headers["content-security-policy"]
        for needle in ("sandbox allow-scripts", "default-src 'none'", "connect-src 'none'"):
            self.assertIn(needle, csp)

    def test_playground_slug_is_validated(self):
        for bad in ("..%2Fserver", "a/b", "nope-doesnt-exist"):
            self.assertEqual(self.c.get(f"/playground/{bad}.html", headers=H).status_code, 404)

    def test_playground_generate_requires_existing_concept(self):
        r = self.c.post("/api/playground/generate", headers={**H, "x-kb-token": server.TOKEN}, json={"page": "claim-agents-need-a-pass-fail-check"})
        self.assertEqual(r.status_code, 400)

    def test_subjects_endpoint_lists_progress(self):
        subs = self.c.get("/api/subjects", headers=H).json()
        self.assertTrue(any(s["key"] == "ai" and s["concepts"] > 0 for s in subs))
        self.assertTrue(all({"name", "color", "icon", "progress"} <= set(s) for s in subs))

    def test_add_subject_validates(self):
        r = self.c.post("/api/subjects", headers={**H, "x-kb-token": server.TOKEN}, json={"key": "Bad Key", "name": "x"})
        self.assertEqual(r.status_code, 400)

    def test_learnmap_has_levels_and_edges(self):
        m = self.c.get("/api/learnmap?subject=ai", headers=H).json()
        self.assertGreater(len(m["nodes"]), 10)
        self.assertGreater(len(m["edges"]), 10)
        self.assertEqual(m["summary"]["total"], len([n for n in m["nodes"] if not n["external"]]))

    def test_build_review_rejects_without_task_or_work(self):
        r = self.c.post("/api/build/review", headers={**H, "x-kb-token": server.TOKEN}, json={"page": "nope", "kind": "coding", "work": "x"})
        self.assertEqual(r.status_code, 400)

    def test_annotation_overlap_and_bounds(self):
        sid = next(p.id for p in server.pages() if p.fm["type"] == "source" and p.fm.get("raw"))
        r = self.c.post(f"/api/annotations/{sid}", headers={**H, "x-kb-token": server.TOKEN}, json={"start": 5, "end": 5})
        self.assertEqual(r.status_code, 400)
        r = self.c.post(f"/api/annotations/{sid}", headers={**H, "x-kb-token": server.TOKEN}, json={"start": 0, "end": 10 ** 9})
        self.assertEqual(r.status_code, 400)


class JobPersistenceTests(unittest.TestCase):
    def test_running_jobs_become_interrupted_after_restart(self):
        import tempfile
        from pathlib import Path
        old_file, old_jobs = server.JOBS_FILE, dict(server.JOBS)
        with tempfile.TemporaryDirectory() as d:
            server.JOBS_FILE = Path(d) / "jobs.json"
            try:
                server.JOBS.clear()
                j = server.new_job("digest", "t")
                self.assertTrue(server.JOBS_FILE.exists())
                server.JOBS.clear()
                server.load_jobs()
                self.assertEqual(server.JOBS[j["id"]]["status"], "interrupted")
            finally:
                server.JOBS_FILE = old_file
                server.JOBS.clear()
                server.JOBS.update(old_jobs)


class MyMapsApiTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        from pathlib import Path
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.old = server.UMAPS
        server.UMAPS = Path(self.tmp.name)
        self.addCleanup(lambda: setattr(server, "UMAPS", self.old))
        self.c = TestClient(server.app, base_url=f"http://127.0.0.1:{server.PORT}")
        self.h = {**H, "x-kb-token": server.TOKEN}

    def test_create_save_load_delete_roundtrip(self):
        mid = self.c.post("/api/mymaps", headers=self.h, json={"title": "Photosynthesis notes"}).json()["id"]
        self.assertTrue(mid.startswith("photosynthesis-notes-"))
        doc = {"title": "Renamed", "nodes": [{"id": "a", "label": "A", "x": 1, "y": 2}, {"id": "b", "label": "B", "x": 5, "y": 6}],
               "edges": [{"id": "e1", "from": "a", "to": "b", "label": "needs"}]}
        self.assertTrue(self.c.post(f"/api/mymaps/{mid}", headers=self.h, json=doc).json()["ok"])
        got = self.c.get(f"/api/mymaps/{mid}", headers=H).json()
        self.assertEqual((got["title"], len(got["nodes"]), len(got["edges"])), ("Renamed", 2, 1))
        listed = self.c.get("/api/mymaps", headers=H).json()
        self.assertEqual([m["id"] for m in listed], [mid])
        self.c.post(f"/api/mymaps/{mid}/delete", headers=self.h)
        self.assertEqual(self.c.get(f"/api/mymaps/{mid}", headers=H).status_code, 404)

    def test_requires_token_and_valid_input(self):
        self.assertEqual(self.c.post("/api/mymaps", headers=H, json={"title": "x"}).status_code, 403)
        self.assertEqual(self.c.post("/api/mymaps", headers=self.h, json={"title": "  "}).status_code, 400)
        self.assertEqual(self.c.post("/api/mymaps", headers=self.h, json={"title": "ok", "subject": "nonexistent"}).status_code, 400)
        mid = self.c.post("/api/mymaps", headers=self.h, json={"title": "ok"}).json()["id"]
        bad = {"title": "t", "nodes": [{"id": "BAD", "label": "x"}], "edges": []}
        self.assertEqual(self.c.post(f"/api/mymaps/{mid}", headers=self.h, json=bad).status_code, 400)

    def test_path_traversal_in_map_id_is_rejected(self):
        for bad in ("..%2F..%2Fvault%2Findex", "a%2Fb"):
            self.assertIn(self.c.get(f"/api/mymaps/{bad}", headers=H).status_code, (400, 404))
        self.assertEqual(self.c.post("/api/mymaps/UPPER-ID/delete", headers=self.h).status_code, 400)

    def test_neighbors_of_a_real_page(self):
        r = self.c.get("/api/neighbors/self-attention", headers=H).json()
        self.assertTrue(any(n["slug"] == "multi-head-attention" for n in r))
        self.assertEqual(self.c.get("/api/neighbors/no-such-page", headers=H).status_code, 404)


class AskTests(unittest.TestCase):
    def setUp(self):
        self.c = TestClient(server.app, base_url=f"http://127.0.0.1:{server.PORT}")
        self.h = {**H, "x-kb-token": server.TOKEN}

    def test_ask_needs_token_and_question(self):
        self.assertEqual(self.c.post("/api/ask", headers=H, json={"question": "x"}).status_code, 403)
        self.assertEqual(self.c.post("/api/ask", headers=self.h, json={"question": "  "}).status_code, 400)

    def test_ask_with_no_matches_skips_claude(self):
        r = self.c.post("/api/ask", headers=self.h, json={"question": "zzqxjvk wwplrtq", "kinds": ["web"], "vault": False})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(r.json()["grounded"])

    def test_raw_endpoint_is_confined_to_raw(self):
        self.assertEqual(self.c.get("/api/raw?path=vault/index.md", headers=H).status_code, 400)
        self.assertEqual(self.c.get("/api/raw?path=../../etc/passwd", headers=H).status_code, 400)

    def test_ask_sources_listing(self):
        r = self.c.get("/api/ask/sources", headers=H)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(all(s["kind"] != "vault" for s in r.json()))
