"""Derived artifacts only (disposable): SQLite full-text index, graph.json, vault/index.md."""
import json
import sqlite3
from pathlib import Path

from .parse import Page
from .schema import RELS, ROOT, TYPES

BUILD = ROOT / "build"
TYPE_TITLES = {"map": "Maps", "project": "Projects", "concept": "Concepts", "claim": "Claims",
               "question": "Open questions", "insight": "Insights", "entity": "Entities", "source": "Sources"}


def edges(pages: list[Page]):
    out = []
    for p in pages:
        for r in p.fm.get("relations") or []:
            if "id" in r:
                out.append({"from": p.id, "rel": r["rel"], "to": r["id"]})
                out.append({"from": r["id"], "rel": RELS[r["rel"]], "to": p.id, "derived": True})
    return out


def build(pages: list[Page], vault: Path, build_dir: Path = BUILD):
    build_dir.mkdir(exist_ok=True)
    db = build_dir / "kb.sqlite"
    db.unlink(missing_ok=True)
    con = sqlite3.connect(db)
    con.executescript("""
      CREATE TABLE pages(id TEXT PRIMARY KEY, type TEXT, title TEXT, summary TEXT, path TEXT,
                         domains TEXT, status TEXT, confidence TEXT);
      CREATE TABLE links(src TEXT, rel TEXT, dst TEXT, derived INTEGER);
      CREATE VIRTUAL TABLE fts USING fts5(id UNINDEXED, title, aliases, summary, body);
    """)
    es = edges(pages)
    for p in pages:
        f = p.fm
        con.execute("INSERT INTO pages VALUES (?,?,?,?,?,?,?,?)", (f["id"], f["type"], f["title"], f["summary"],
                    str(p.path.relative_to(ROOT)) if p.path.is_relative_to(ROOT) else str(p.path),
                    ",".join(f["domains"]), f["status"], f["confidence"]))
        con.execute("INSERT INTO fts VALUES (?,?,?,?,?)", (f["id"], f["title"], " ".join(f["aliases"]), f["summary"], p.body))
    con.executemany("INSERT INTO links VALUES (?,?,?,?)", [(e["from"], e["rel"], e["to"], int(e.get("derived", False))) for e in es])
    con.commit(); con.close()
    (build_dir / "graph.json").write_text(json.dumps({
        "nodes": [{"id": p.id, "type": p.fm["type"], "title": p.fm["title"], "domains": p.fm["domains"]} for p in pages],
        "edges": es}, indent=1), encoding="utf-8")
    write_index(pages, vault)


def write_index(pages: list[Page], vault: Path):
    lines = ["# Index", "", "_Derived by `./kb build`. Do not edit; edit the pages._", ""]
    for t, title in TYPE_TITLES.items():
        group = sorted((p for p in pages if p.fm["type"] == t and not (t == "question" and p.fm.get("state") == "answered")),
                       key=lambda p: p.fm["title"].lower())
        if not group:
            continue
        lines += [f"## {title}", ""]
        for p in group:
            f = p.fm
            lines.append(f"- [[{p.stem}]] — {f['summary']} ({f['status']}, {f['confidence']}) · {', '.join(f['domains'])}")
        lines.append("")
    (vault / "index.md").write_text("\n".join(lines), encoding="utf-8")


def search(query: str, limit=10, build_dir: Path = BUILD):
    db = build_dir / "kb.sqlite"
    if not db.exists():
        raise SystemExit("no index yet: run ./kb build")
    con = sqlite3.connect(db)
    rows = con.execute("""SELECT p.id, p.type, p.title, snippet(fts, 4, '[', ']', '…', 12)
                          FROM fts JOIN pages p ON p.id = fts.id WHERE fts MATCH ? ORDER BY rank LIMIT ?""",
                       (query, limit)).fetchall()
    con.close()
    return rows
