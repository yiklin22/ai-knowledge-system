"""Command line UI. Thin: delegates to parse / validate / index / learning."""
import argparse
import datetime
import difflib
import random
import re
import shutil
import string
import sys
from pathlib import Path

from . import graphview, index, learning
from .parse import Page, load_dir, parse_text, slugify
from .schema import ROOT, SCHEMA_VERSION, TYPES, TYPE_ENUMS
from .validate import human_blocks_preserved, load_domains, validate

VAULT, PROPOSALS = ROOT / "vault", ROOT / "proposals"
TODAY = datetime.date.today().isoformat()

EXTRA = {  # type-specific frontmatter lines + body
    "source": ('kind: web                # chat | document | web | video | paper | book | note\n'
               'reliability: secondary    # primary | secondary | vendor | ai-chat | opinion\n'
               'raw: raw/web/CHANGE-ME.md\nurl: null\nauthor: null\npublished: null\n',
               "## Takeaways\n\n## Locator map\n_Where things are (page / section / timestamp)._\n"),
    "concept": ("recall: []   # - {q: \"...\", a: \"...\"}\n",
                "## Knowledge\n\n## Evidence\n\n## Understanding\n\n## Application\n\n## Uncertainty\n\n## Related\n"),
    "claim": ("verdict: unverified\n", "## Evidence for\n\n## Evidence against\n\n## Verdict reasoning\n"),
    "entity": ("kind: person\n", "## Who/what\n\n## Why it matters\n"),
    "question": ("state: open\n", "## Why I'm asking\n\n## What would answer it\n"),
    "insight": ("kind: lesson\n", "<!-- human -->\n_My own words go here._\n<!-- /human -->\n\n## Context\n\n## Applies when\n"),
    "project": ("state: active\n", "## Goal\n\n## Decisions\n\n## Knowledge applied\n"),
    "map": ("", "## Start here\n\n## Learning path\n_Use `prerequisite_for` relations; list in reading order._\n"),
}


def new_id(prefix, taken: set[str]) -> str:
    while True:
        i = f"{prefix}_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        if i not in taken:
            return i


def all_pages(include_proposals=False, batch=None):
    pages = load_dir(VAULT)
    if include_proposals:
        for b in sorted(PROPOSALS.glob("*/")):
            if b.is_dir() and (batch is None or b.name == batch):
                pages += load_dir(b)
    return pages


def report(errors, warnings):
    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("warning", w)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")


def cmd_new(a):
    folder, prefix = TYPES[a.type]
    taken = {p.id for p in all_pages(True)}
    pid = new_id(prefix, taken)
    d = PROPOSALS / a.batch / folder
    d = PROPOSALS / a.batch / folder
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{slugify(a.title)}.md"
    if path.exists():
        sys.exit(f"{path} exists")
    fm_extra, body = EXTRA[a.type]
    path.write_text(f"""---
id: {pid}
schema: {SCHEMA_VERSION}
type: {a.type}
title: "{a.title}"
aliases: []
domains: [{a.domain}]
summary: TODO one or two plain sentences
tags: []
status: draft
confidence: low
created: {TODAY}
updated: {TODAY}
sources: []      # - {{id: src_xxxxxxxx, locator: "p.3", quote: null}}
relations: []    # - {{rel: related, id: cpt_xxxxxxxx}}  or  {{rel: related, unresolved: "Name"}}
{fm_extra}---

# {a.title}

{body}""", encoding="utf-8")
    print(f"{pid}  {path.relative_to(ROOT)}")


def cmd_validate(a):
    pages = all_pages(a.proposals is not None, a.proposals or None)
    errors, warnings = validate(pages, load_domains(VAULT))
    report(errors, warnings)
    sys.exit(1 if errors else 0)


def cmd_build(a=None):
    pages = load_dir(VAULT)
    errors, _ = validate(pages, load_domains(VAULT))
    if errors:
        report(errors, [])
        sys.exit("refusing to build derived indexes from an invalid vault")
    index.build(pages, VAULT)
    con = learning.connect()
    added, gone = learning.sync(con, pages)
    print(f"built {len(pages)} pages -> build/kb.sqlite, build/graph.json, vault/index.md; "
          f"cards +{added} -{gone}")


def cmd_search(a):
    for pid, t, title, snip in index.search(a.query):
        print(f"{pid}  [{t}] {title}\n    {snip}")


def cmd_approve(a):
    batch = PROPOSALS / a.batch
    if not batch.is_dir():
        sys.exit(f"no such batch: {a.batch}")
    vault_pages = load_dir(VAULT)
    new_pages = load_dir(batch)
    if not new_pages:
        sys.exit("batch is empty")
    by_id = {p.id: p for p in vault_pages if p.id}
    amended = [p for p in new_pages if p.id in by_id]
    merged = [p for p in vault_pages if p.id not in {n.id for n in new_pages}] + new_pages
    errors, warnings = validate(merged, load_domains(VAULT), check_orphans=False)
    if amended and not a.amend:
        errors.append("batch modifies existing pages " + ", ".join(p.path.name for p in amended) + " (re-run with --amend after reviewing)")
    for p in amended:
        old = by_id[p.id]
        lost = human_blocks_preserved(old.body, p.body)
        if lost:
            errors.append(f"{p.path.name}: would remove/alter human-authored text: {lost[0][:60]!r}")
        if a.amend:
            sys.stdout.writelines(difflib.unified_diff(old.path.read_text().splitlines(True), p.path.read_text().splitlines(True),
                                                        f"vault/{old.path.name}", f"proposal/{p.path.name}"))
    for p in new_pages:
        if p.id not in by_id:
            for v in vault_pages:
                if v.path.name == p.path.name:
                    errors.append(f"{p.path.name}: filename already used by {v.id}")
    report(errors, warnings)
    if errors:
        sys.exit("not approved")
    log = []
    for p in new_pages:
        folder = TYPES[p.fm["type"]][0]
        dest = (by_id[p.id].path if p.id in by_id else VAULT / folder / p.path.name)
        text = p.path.read_text(encoding="utf-8")
        if p.id not in by_id and p.fm["status"] == "draft":  # human approval makes it reviewed
            text = re.sub(r"^status: draft", "status: reviewed", text, count=1, flags=re.M)
        dest.write_text(text, encoding="utf-8")
        log.append(f"- {'amended' if p.id in by_id else 'added'} {dest.relative_to(ROOT)} ({p.id})")
    with open(VAULT / "log.md", "a", encoding="utf-8") as f:
        f.write(f"\n## [{TODAY}] approve | {a.batch}\n" + "\n".join(log) + "\n")
    shutil.rmtree(batch)
    print("\n".join(log))
    cmd_build()


def cmd_status(a):
    pages = load_dir(VAULT)
    from collections import Counter
    print("vault:", dict(Counter(p.fm["type"] for p in pages if p.fm)) or "empty")
    print("domains:", dict(Counter(d for p in pages if p.fm for d in p.fm["domains"])))
    print("stubs:", sum(1 for p in pages if p.fm.get("status") == "stub"),
          "| open questions:", sum(1 for p in pages if p.fm.get("state") == "open" and p.fm["type"] == "question"))
    batches = [b.name for b in PROPOSALS.glob("*/") if b.is_dir()]
    print("proposal batches awaiting review:", batches or "none")
    con = learning.connect()
    print("cards due today:", len(learning.due(con, limit=10**6)))


def cmd_quiz(a):
    con = learning.connect()
    cards = learning.due(con, limit=a.n)
    if not cards:
        print("Nothing due."); return
    for cid, q, ans in cards:
        input(f"\nQ: {q}\n(press Enter to reveal) ")
        print(f"A: {ans}")
        g = input("How well did you recall it? 0 (blank) .. 5 (perfect): ").strip()
        learning.grade(con, cid, int(g) if g.isdigit() and 0 <= int(g) <= 5 else 0)


def find_page(pages, key):
    hits = [p for p in pages if p.id == key or p.stem == key or (p.fm and p.fm.get("title", "").lower() == key.lower())]
    if not hits:
        hits = [p for p in pages if p.fm and key.lower() in p.fm.get("title", "").lower()]
    if len(hits) != 1:
        sys.exit(f"{'no page' if not hits else 'ambiguous'} matching '{key}'" + (": " + ", ".join(p.stem for p in hits) if hits else ""))
    return hits[0]


def cmd_next(a):
    pages = load_dir(VAULT)
    con = learning.connect()
    topics, _ = learning.next_topics(pages, learning.mastery_map(con), a.n)
    if not topics:
        print("Nothing ready: no concepts yet, or everything is mastered."); return
    print("Ready to study (prerequisites mastered; most unlocking first):")
    for p, deps in topics:
        print(f"  {p.stem:40} unlocks {deps}  | {p.fm['summary']}")
    print("\nStart a session: ask Claude to tutor you, or run ./kb tutor <name>")


def cmd_tutor(a):
    """Print the grounding packet the Socratic tutor works from."""
    pages = load_dir(VAULT)
    by_id = {p.id: p for p in pages}
    p = find_page(pages, a.page)
    con = learning.connect()
    mm = learning.mastery_map(con)
    _, prereqs = learning.next_topics(pages, mm)
    print(f"# TUTOR PACKET: {p.fm['title']} ({p.id}, {p.fm['status']}, confidence {p.fm['confidence']})")
    print(f"mastery: {mm.get(p.id, 0)}/5")
    print("prerequisites:", ", ".join(f"{by_id[q].fm['title']} [{mm.get(q, 0)}/5]" for q in sorted(prereqs.get(p.id, ()))) or "none")
    unlocks = [q.fm["title"] for q in pages if p.id in prereqs.get(q.id, ())]
    print("unlocks:", ", ".join(unlocks) or "none")
    for key in ("probes", "misconceptions"):
        if p.fm.get(key):
            print(f"{key} (from the vault):"); [print("  -", x) for x in p.fm[key]]
    mc = learning.open_misconceptions(con, p.id)
    print("misconceptions this learner showed before (unresolved):", mc or "none")
    for r in p.fm.get("relations") or []:
        if "id" in r and r["id"] in by_id and by_id[r["id"]].fm["type"] in ("claim", "question") :
            t = by_id[r["id"]]; print(f"related {t.fm['type']}: {t.fm['title']} ({t.fm.get('verdict') or t.fm.get('state')})")
    for s in p.fm.get("sources") or []:
        if s.get("id") in by_id:
            print(f"source: {by_id[s['id']].fm['title']} [{by_id[s['id']].fm.get('reliability')}] at {s.get('locator')} -> {by_id[s['id']].fm.get('raw') or by_id[s['id']].fm.get('url')}")
    if p.fm["status"] == "stub" or not p.fm["sources"]:
        print("NOTE: this page is a stub / has no sources. Anything you teach beyond the summary is from general knowledge, say so.")
    print("\n--- PAGE BODY ---\n" + p.body.strip())


def cmd_record(a):
    pages = load_dir(VAULT)
    p = find_page(pages, a.page)
    if a.level is not None and not 0 <= a.level <= 5:
        sys.exit("level must be 0..5")
    learning.record_session(learning.connect(), p.id, a.level, a.misconception, a.resolved, a.note or "")
    print(f"recorded for {p.fm['title']}: level={a.level} +{len(a.misconception)} misconception(s), {len(a.resolved)} resolved")


def cmd_graph(a):
    pages = load_dir(VAULT)
    out = ROOT / "build" / "graph.html"
    graphview.write(pages, learning.mastery_map(learning.connect()), out)
    print(f"wrote {out.relative_to(ROOT)}  (open it in a browser)")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="kb", description="Personal knowledge system")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("new", help="create a proposed page skeleton with a fresh id")
    s.add_argument("batch"); s.add_argument("type", choices=list(TYPES)); s.add_argument("title")
    s.add_argument("--domain", default="ai"); s.set_defaults(f=cmd_new)
    s = sub.add_parser("validate", help="validate the vault (or vault + proposals)")
    s.add_argument("--proposals", nargs="?", const="", default=None, metavar="BATCH"); s.set_defaults(f=cmd_validate)
    sub.add_parser("build", help="rebuild derived indexes").set_defaults(f=cmd_build)
    s = sub.add_parser("search"); s.add_argument("query"); s.set_defaults(f=cmd_search)
    s = sub.add_parser("approve", help="HUMAN ONLY: move a reviewed proposal batch into the vault")
    s.add_argument("batch"); s.add_argument("--amend", action="store_true"); s.set_defaults(f=cmd_approve)
    sub.add_parser("status").set_defaults(f=cmd_status)
    s = sub.add_parser("quiz", help="spaced-repetition review"); s.add_argument("-n", type=int, default=10); s.set_defaults(f=cmd_quiz)
    s = sub.add_parser("next", help="what to study next (prerequisite-aware)"); s.add_argument("-n", type=int, default=5); s.set_defaults(f=cmd_next)
    s = sub.add_parser("tutor", help="print the grounding packet for a Socratic session"); s.add_argument("page"); s.set_defaults(f=cmd_tutor)
    s = sub.add_parser("record", help="record a tutoring session's outcome")
    s.add_argument("page"); s.add_argument("--level", type=int); s.add_argument("--note")
    s.add_argument("--misconception", action="append", default=[]); s.add_argument("--resolved", action="append", default=[])
    s.set_defaults(f=cmd_record)
    sub.add_parser("graph", help="write build/graph.html").set_defaults(f=cmd_graph)
    a = ap.parse_args(argv)
    a.f(a)
