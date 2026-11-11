"""Learning analytics: personalised learning maps, streaks, subject stats, concept-map validation.

Pure functions over Page objects and the learning DB, so they are testable without the web app.
"""
import datetime
import re
from pathlib import Path

import yaml

from .parse import Page
from .schema import ROOT

MASTERED = 3
NODE_KINDS = {"core", "prerequisite", "part", "example", "misconception", "application", "related"}


# ---------------------------------------------------------------- subjects (domains.yml)
def load_subjects(vault: Path) -> dict[str, dict]:
    """Return {key: {name, description, color, icon}} from vault/domains.yml (supports the old plain-string format)."""
    f = vault / "domains.yml"
    data = yaml.safe_load(f.read_text(encoding="utf-8")) if f.exists() else {}
    palette = ["#7c93ff", "#4cc38a", "#e8a33d", "#e5686a", "#4cb8c4", "#b07cf0", "#e07ab8", "#8aa05a"]
    out = {}
    for i, (k, v) in enumerate((data or {}).items()):
        meta = v if isinstance(v, dict) else {"description": str(v or "")}
        out[k] = {"name": meta.get("name") or k.replace("-", " ").title(), "description": meta.get("description", ""),
                  "color": meta.get("color") or palette[i % len(palette)], "icon": meta.get("icon") or "◆"}
    return out


def add_subject(vault: Path, key: str, name: str, description: str = "", color: str = "", icon: str = "") -> dict:
    if not re.fullmatch(r"[a-z][a-z0-9-]{1,30}", key):
        raise ValueError("key must be lowercase letters, digits and hyphens (2-31 chars)")
    if not name.strip():
        raise ValueError("name is required")
    if color and not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise ValueError("color must look like #aabbcc")
    subjects = load_subjects(vault)
    if key in subjects:
        raise ValueError("that subject already exists")
    subjects[key] = {"name": name.strip()[:60], "description": description.strip()[:200], "color": color or "", "icon": (icon or "◆")[:4]}
    f = vault / "domains.yml"
    clean = {k: {kk: vv for kk, vv in v.items() if vv} for k, v in subjects.items()}
    f.write_text("# Subjects (domains). Every page belongs to at least one. Add new subjects from the app or here.\n"
                 + yaml.safe_dump(clean, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return load_subjects(vault)[key]


# ---------------------------------------------------------------- learning stats
def review_stats(con) -> dict[str, dict]:
    """Per page id: number of reviews and recent accuracy (grade >= 3)."""
    out: dict[str, dict] = {}
    for card_id, grade in con.execute("SELECT card_id, grade FROM reviews ORDER BY id"):
        pid = card_id.split(":")[0]
        s = out.setdefault(pid, {"grades": []})
        s["grades"].append(grade)
    for pid, s in out.items():
        recent = s["grades"][-8:]
        s["reviews"] = len(s["grades"])
        s["accuracy"] = round(sum(1 for g in recent if g >= 3) / len(recent), 2)
        del s["grades"]
    return out


def open_misconception_counts(con) -> dict[str, int]:
    return dict(con.execute("SELECT page_id, COUNT(*) FROM misconceptions WHERE resolved=0 GROUP BY page_id").fetchall())


def streak(con, today: datetime.date | None = None) -> dict:
    """Consecutive days with any review or tutor session; alive if the last active day is today or yesterday."""
    today = today or datetime.date.today()
    days = {r[0] for r in con.execute("SELECT day FROM reviews UNION SELECT day FROM sessions")}
    active = sorted({datetime.date.fromisoformat(d) for d in days if d})
    if not active:
        return {"current": 0, "today_done": False, "total_days": 0}
    last = active[-1]
    cur = 0
    if (today - last).days <= 1:
        d = last
        have = set(active)
        while d in have:
            cur += 1
            d -= datetime.timedelta(days=1)
    return {"current": cur, "today_done": last == today, "total_days": len(active)}


# ---------------------------------------------------------------- the learning map
def compute_map(pages: list[Page], mastery: dict[str, int], stats: dict, miscs: dict, subject: str | None) -> dict:
    """Prerequisite DAG of the concepts in a subject (plus their prerequisites from other subjects), with the
    learner's state on each node: mastered / ready / blocked, and gaps that need attention."""
    concepts = {p.id: p for p in pages if p.fm.get("type") == "concept"}
    prereqs = {i: set() for i in concepts}
    for p in pages:
        for r in p.fm.get("relations") or []:
            if r.get("rel") == "prerequisite_for" and p.id in concepts and r.get("id") in concepts:
                prereqs[r["id"]].add(p.id)
            if r.get("rel") == "requires" and p.id in concepts and r.get("id") in concepts:
                prereqs[p.id].add(r["id"])
    if subject:
        include = {i for i, p in concepts.items() if subject in p.fm.get("domains", [])}
        stack = list(include)
        while stack:  # add all ancestors from other subjects
            for q in prereqs[stack.pop()]:
                if q not in include:
                    include.add(q)
                    stack.append(q)
    else:
        include = set(concepts)
    depth: dict[str, int] = {}

    def d(i, seen=()):
        if i in depth:
            return depth[i]
        if i in seen:
            return 0
        ps = [q for q in prereqs[i] if q in include]
        depth[i] = 0 if not ps else 1 + max(d(q, seen + (i,)) for q in ps)
        return depth[i]

    nodes = []
    for i in include:
        p = concepts[i]
        lvl = mastery.get(i, 0)
        ps = [q for q in prereqs[i] if q in include]
        weak_pre = [concepts[q].fm["title"] for q in ps if mastery.get(q, 0) < MASTERED]
        st = stats.get(i, {})
        if lvl >= MASTERED:
            state = "mastered"
        elif not weak_pre:
            state = "ready"
        else:
            state = "blocked"
        gaps = []
        if lvl > 0 and weak_pre:
            gaps.append("Foundations first: " + ", ".join(weak_pre[:3]))
        if st.get("reviews", 0) >= 3 and st.get("accuracy", 1) < 0.6:
            gaps.append(f"Recall accuracy is {int(st['accuracy'] * 100)}%: revisit it")
        if miscs.get(i):
            gaps.append(f"{miscs[i]} unresolved misconception(s)")
        nodes.append({"id": i, "slug": p.stem, "title": p.fm["title"], "summary": p.fm["summary"], "domains": p.fm["domains"],
                      "level": lvl, "state": state, "depth": d(i), "prereqs": ps, "external": bool(subject and subject not in p.fm["domains"]),
                      "accuracy": st.get("accuracy"), "reviews": st.get("reviews", 0), "misconceptions": miscs.get(i, 0), "gaps": gaps,
                      "status": p.fm["status"], "has_probes": bool(p.fm.get("probes"))})
    nodes.sort(key=lambda n: (n["depth"], n["title"]))
    edges = [{"from": q, "to": n["id"]} for n in nodes for q in n["prereqs"]]
    own = [n for n in nodes if not n["external"]]
    summary = {"total": len(own), "mastered": sum(n["state"] == "mastered" for n in own), "ready": sum(n["state"] == "ready" for n in own),
               "blocked": sum(n["state"] == "blocked" for n in own), "gaps": sum(bool(n["gaps"]) for n in own),
               "avg_level": round(sum(n["level"] for n in own) / len(own), 2) if own else 0}
    return {"nodes": nodes, "edges": edges, "summary": summary, "max_depth": max((n["depth"] for n in nodes), default=0)}


# ---------------------------------------------------------------- concept maps (AI-generated teaching aid)
def validate_conceptmap(data, known_slugs: set[str]) -> dict:
    """Validate and normalise a model-produced concept map. Raises ValueError on unusable output."""
    if not isinstance(data, dict) or not isinstance(data.get("nodes"), list) or not isinstance(data.get("edges"), list):
        raise ValueError("concept map needs nodes and edges lists")
    nodes, ids = [], set()
    for n in data["nodes"][:24]:
        if not isinstance(n, dict) or not n.get("id") or not n.get("label"):
            continue
        nid = re.sub(r"[^a-z0-9_-]", "", str(n["id"]).lower())[:30]
        if not nid or nid in ids:
            continue
        kind = n.get("kind") if n.get("kind") in NODE_KINDS else "related"
        slug = n.get("vault_slug") if n.get("vault_slug") in known_slugs else None
        nodes.append({"id": nid, "label": str(n["label"])[:48], "kind": kind, "note": str(n.get("note", ""))[:400], "vault_slug": slug})
        ids.add(nid)
    if len(nodes) < 3:
        raise ValueError("concept map has too few usable nodes")
    edges = []
    for e in data["edges"][:60]:
        if not isinstance(e, dict):
            continue
        a, b = str(e.get("from", "")).lower(), str(e.get("to", "")).lower()
        a, b = re.sub(r"[^a-z0-9_-]", "", a)[:30], re.sub(r"[^a-z0-9_-]", "", b)[:30]
        if a in ids and b in ids and a != b:
            edges.append({"from": a, "to": b, "label": str(e.get("label", ""))[:32]})
    if not edges:
        raise ValueError("concept map has no usable edges")
    return {"title": str(data.get("title", ""))[:80], "nodes": nodes, "edges": edges, "summary": str(data.get("summary", ""))[:400]}


def validate_build_task(data) -> dict:
    """Validate a model-produced learning-to-build task."""
    if not isinstance(data, dict) or not data.get("title") or not isinstance(data.get("steps"), list) or not data["steps"]:
        raise ValueError("task needs a title and steps")
    lst = lambda v, n: [str(x)[:500] for x in (v if isinstance(v, list) else [])][:n]
    return {"title": str(data["title"])[:120], "kind": str(data.get("kind", "coding"))[:20], "goal": str(data.get("goal", ""))[:600],
            "steps": lst(data["steps"], 12), "starter": str(data.get("starter", ""))[:6000], "language": str(data.get("language", ""))[:20],
            "checks": lst(data.get("checks"), 8), "hints": lst(data.get("hints"), 4), "stretch": str(data.get("stretch", ""))[:400],
            "time_minutes": int(data["time_minutes"]) if str(data.get("time_minutes", "")).isdigit() else None}


# ---------------------------------------------------------------- user-built maps (My maps)
MAP_COLORS = {"auto", "blue", "green", "orange", "red", "violet", "teal", "gray"}
MAP_ID = re.compile(r"[a-z0-9][a-z0-9-]{2,60}")


def validate_usermap(data) -> dict:
    """Validate and normalise a map the learner built in the editor. Raises ValueError on bad input."""
    if not isinstance(data, dict):
        raise ValueError("map must be an object")
    nodes_in, edges_in = data.get("nodes", []), data.get("edges", [])
    if not isinstance(nodes_in, list) or not isinstance(edges_in, list) or len(nodes_in) > 300 or len(edges_in) > 600:
        raise ValueError("too many nodes or edges (max 300 nodes, 600 links)")
    num = lambda v: max(-50000.0, min(50000.0, float(v)))
    nodes, ids = [], set()
    for n in nodes_in:
        if not isinstance(n, dict):
            continue
        nid = str(n.get("id", ""))
        if not re.fullmatch(r"[a-z0-9_-]{1,24}", nid) or nid in ids:
            raise ValueError(f"bad or duplicate node id: {nid!r}")
        try:
            x, y = num(n.get("x", 0)), num(n.get("y", 0))
        except (TypeError, ValueError):
            raise ValueError("node positions must be numbers")
        page = n.get("page")
        nodes.append({"id": nid, "label": str(n.get("label", ""))[:120] or "Untitled", "note": str(n.get("note", ""))[:1000],
                      "color": n.get("color") if n.get("color") in MAP_COLORS else "auto", "x": x, "y": y,
                      "page": str(page)[:80] if page else None})
        ids.add(nid)
    edges, seen = [], set()
    for e in edges_in:
        if not isinstance(e, dict):
            continue
        a, b, eid = str(e.get("from", "")), str(e.get("to", "")), str(e.get("id", ""))
        if a not in ids or b not in ids or a == b:
            continue
        if not re.fullmatch(r"[a-z0-9_-]{1,24}", eid) or eid in seen:
            raise ValueError(f"bad or duplicate link id: {eid!r}")
        seen.add(eid)
        edges.append({"id": eid, "from": a, "to": b, "label": str(e.get("label", ""))[:40]})
    subject = str(data.get("subject", ""))[:30]
    return {"title": str(data.get("title", "")).strip()[:80] or "Untitled map", "subject": subject, "nodes": nodes, "edges": edges}
