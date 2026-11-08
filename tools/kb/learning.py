"""Learning progress in SQLite (data/learning.db), separate from the vault. SM-2 spaced repetition."""
import datetime
import hashlib
import sqlite3
from pathlib import Path

from .parse import Page
from .schema import ROOT

DB = ROOT / "data" / "learning.db"


def connect(db: Path = DB):
    db.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(db)
    con.executescript("""
      CREATE TABLE IF NOT EXISTS cards(card_id TEXT PRIMARY KEY, page_id TEXT, q TEXT, a TEXT,
          ease REAL DEFAULT 2.5, interval INTEGER DEFAULT 0, reps INTEGER DEFAULT 0,
          due TEXT, active INTEGER DEFAULT 1);
      CREATE TABLE IF NOT EXISTS reviews(id INTEGER PRIMARY KEY, card_id TEXT, day TEXT, grade INTEGER);
      CREATE TABLE IF NOT EXISTS mastery(page_id TEXT PRIMARY KEY, level INTEGER, updated TEXT);
      CREATE TABLE IF NOT EXISTS misconceptions(id INTEGER PRIMARY KEY, page_id TEXT, text TEXT, day TEXT, resolved INTEGER DEFAULT 0);
      CREATE TABLE IF NOT EXISTS sessions(id INTEGER PRIMARY KEY, page_id TEXT, day TEXT, note TEXT);
    """)
    return con


def card_id(page_id: str, q: str) -> str:
    return f"{page_id}:{hashlib.sha1(q.strip().encode()).hexdigest()[:6]}"


def sync(con, pages: list[Page], today=None) -> tuple[int, int]:
    """Add cards from approved concepts' `recall`; deactivate cards no longer in the vault. Progress is kept."""
    today = (today or datetime.date.today()).isoformat()
    live = {}
    for p in pages:
        for r in p.fm.get("recall") or []:
            live[card_id(p.id, r["q"])] = (p.id, r["q"], r["a"])
    added = 0
    for cid, (pid, q, a) in live.items():
        if con.execute("SELECT 1 FROM cards WHERE card_id=?", (cid,)).fetchone():
            con.execute("UPDATE cards SET a=?, active=1 WHERE card_id=?", (a, cid))
        else:
            con.execute("INSERT INTO cards(card_id,page_id,q,a,due) VALUES (?,?,?,?,?)", (cid, pid, q, a, today)); added += 1
    gone = 0
    for (cid,) in con.execute("SELECT card_id FROM cards WHERE active=1").fetchall():
        if cid not in live:
            con.execute("UPDATE cards SET active=0 WHERE card_id=?", (cid,)); gone += 1
    con.commit()
    return added, gone


def due(con, today=None, limit=10):
    today = (today or datetime.date.today()).isoformat()
    return con.execute("SELECT card_id,q,a FROM cards WHERE active=1 AND due<=? ORDER BY due LIMIT ?", (today, limit)).fetchall()


def grade(con, cid: str, g: int, today=None):
    """SM-2. g: 0 (blackout) .. 5 (perfect)."""
    today = today or datetime.date.today()
    ease, interval, reps = con.execute("SELECT ease,interval,reps FROM cards WHERE card_id=?", (cid,)).fetchone()
    if g < 3:
        reps, interval = 0, 1
    else:
        interval = 1 if reps == 0 else 6 if reps == 1 else round(interval * ease)
        reps += 1
    ease = max(1.3, ease + 0.1 - (5 - g) * (0.08 + (5 - g) * 0.02))
    con.execute("UPDATE cards SET ease=?, interval=?, reps=?, due=? WHERE card_id=?",
                (ease, interval, reps, (today + datetime.timedelta(days=interval)).isoformat(), cid))
    con.execute("INSERT INTO reviews(card_id,day,grade) VALUES (?,?,?)", (cid, today.isoformat(), g))
    con.commit()


# ---- tutor state: mastery 0 (unseen) .. 5 (can teach it and apply it to new cases) ----
MASTERED = 3


def record_session(con, page_id, level=None, misconceptions=(), resolved=(), note="", today=None):
    day = (today or datetime.date.today()).isoformat()
    if level is not None:
        con.execute("INSERT INTO mastery VALUES (?,?,?) ON CONFLICT(page_id) DO UPDATE SET level=?, updated=?",
                    (page_id, level, day, level, day))
    for m in misconceptions:
        con.execute("INSERT INTO misconceptions(page_id,text,day) VALUES (?,?,?)", (page_id, m, day))
    for m in resolved:
        con.execute("UPDATE misconceptions SET resolved=1 WHERE page_id=? AND text LIKE ?", (page_id, f"%{m}%"))
    con.execute("INSERT INTO sessions(page_id,day,note) VALUES (?,?,?)", (page_id, day, note))
    con.commit()


def mastery_map(con) -> dict[str, int]:
    return dict(con.execute("SELECT page_id, level FROM mastery").fetchall())


def open_misconceptions(con, page_id):
    return [r[0] for r in con.execute("SELECT text FROM misconceptions WHERE page_id=? AND resolved=0", (page_id,))]


def next_topics(pages: list[Page], mastery: dict[str, int], n=5):
    """Concepts not yet mastered whose prerequisites are all mastered; most unlocking first."""
    concepts = {p.id: p for p in pages if p.fm.get("type") == "concept"}
    prereqs = {i: set() for i in concepts}
    for p in pages:
        for r in p.fm.get("relations") or []:
            if r.get("rel") == "prerequisite_for" and p.id in concepts and r.get("id") in concepts:
                prereqs[r["id"]].add(p.id)
            if r.get("rel") == "requires" and p.id in concepts and r.get("id") in concepts:
                prereqs[p.id].add(r["id"])
    dependents = {i: sum(i in v for v in prereqs.values()) for i in concepts}
    ready = [i for i in concepts if mastery.get(i, 0) < MASTERED and all(mastery.get(q, 0) >= MASTERED for q in prereqs[i])]
    ready.sort(key=lambda i: (-dependents[i], mastery.get(i, 0), concepts[i].fm["title"]))
    return [(concepts[i], dependents[i]) for i in ready[:n]], prereqs
