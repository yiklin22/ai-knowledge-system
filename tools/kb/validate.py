"""Validation only: pure functions over lists of Page objects. Returns (errors, warnings)."""
import datetime
import re
from pathlib import Path
import yaml

from .parse import Page, human_blocks, wikilinks
from .schema import (COMMON_FIELDS, CONCEPT_SECTIONS, ENUMS, RELS, ROOT, SCHEMA_VERSION, SOURCES_OPTIONAL,
                     STALE_DAYS, TYPE_ENUMS, TYPES)


def load_domains(vault: Path) -> set[str]:
    f = vault / "domains.yml"
    if not f.exists():
        return set()
    data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    return set(data.keys() if isinstance(data, dict) else data)


def _date(v):
    if isinstance(v, datetime.date):
        return v
    try:
        return datetime.date.fromisoformat(str(v))
    except ValueError:
        return None


def raw_file(root: Path, raw) -> Path | None:
    """The file a source page's `raw` field names, or None unless it is an existing file inside raw/.
    Evidence may only be checked against immutable sources: a path into proposals/ (text the agent wrote itself),
    an absolute path or a ../ escape would let an invented quote pass as verbatim."""
    base = (root / "raw").resolve()
    f = (root / str(raw)).resolve()
    return f if base in f.parents and f.is_file() else None


def _norm(s):
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def validate(pages: list[Page], domains: set[str], root: Path = ROOT, today=None,
             check_orphans=True) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    today = today or datetime.date.today()
    by_id: dict[str, Page] = {}
    good: list[Page] = []

    def err(p, msg):
        errors.append(f"{p.path.name}: {msg}")

    def warn(p, msg):
        warnings.append(f"{p.path.name}: {msg}")

    # --- structure, identity ---
    for p in pages:
        if p.error:
            err(p, p.error); continue
        fm = p.fm
        missing = [k for k in COMMON_FIELDS if k not in fm]
        if missing:
            err(p, f"missing fields: {', '.join(missing)}"); continue
        t = fm["type"]
        if t not in TYPES:
            err(p, f"unknown type '{t}'"); continue
        folder, prefix = TYPES[t]
        if p.path.parent.name != folder:
            err(p, f"type '{t}' belongs in folder {folder}/")
        if not re.fullmatch(rf"{prefix}_[a-z0-9]{{8}}", str(fm["id"])):
            err(p, f"id '{fm['id']}' must match {prefix}_<8 chars a-z0-9>")
        if fm["id"] in by_id:
            err(p, f"duplicate id {fm['id']} (also {by_id[fm['id']].path.name})"); continue
        if fm["schema"] != SCHEMA_VERSION:
            err(p, f"schema {fm['schema']} != {SCHEMA_VERSION}")
        by_id[fm["id"]] = p
        good.append(p)

    stems: dict[str, Page] = {}
    names: dict[str, Page] = {}
    for p in good:
        fm = p.fm
        for k, allowed in ENUMS.items():
            if fm[k] not in allowed:
                err(p, f"{k} '{fm[k]}' not in {sorted(allowed)}")
        for k, allowed in TYPE_ENUMS.get(fm["type"], {}).items():
            if k not in fm:
                err(p, f"missing {fm['type']} field '{k}'")
            elif fm[k] not in allowed:
                err(p, f"{k} '{fm[k]}' not in {sorted(allowed)}")
        c, u = _date(fm["created"]), _date(fm["updated"])
        if not c or not u:
            err(p, "created/updated must be ISO dates")
        elif u < c:
            err(p, "updated is before created")
        elif u > today:
            err(p, "updated is in the future")
        for k in ("aliases", "domains", "tags", "sources", "relations"):
            if not isinstance(fm[k], list):
                err(p, f"'{k}' must be a list")
        if not fm["domains"]:
            err(p, "needs at least one domain")
        for d in fm["domains"] if isinstance(fm["domains"], list) else []:
            if domains and d not in domains:
                err(p, f"domain '{d}' not in vault/domains.yml")
        # filename uniqueness (needed for [[wikilinks]])
        if p.stem in stems:
            err(p, f"filename also used by {stems[p.stem].path}")
        stems[p.stem] = p
        # duplicate title/alias detection
        for n in [fm["title"]] + (fm["aliases"] if isinstance(fm["aliases"], list) else []):
            key = _norm(n)
            if key in names and names[key] is not p:
                err(p, f"title/alias '{n}' already used by {names[key].path.name} (possible duplicate)")
            names[key] = p
        # type-specific
        if fm["type"] == "source":
            raw, url = fm.get("raw"), fm.get("url")
            if not raw and not url:
                err(p, "source needs 'raw' or 'url'")
            if raw and not raw_file(root, raw):
                err(p, f"raw file not found inside raw/: {raw}")
        if fm["type"] == "concept":
            for r in fm.get("recall") or []:
                if not (isinstance(r, dict) and r.get("q") and r.get("a")):
                    err(p, "each recall card needs q and a")
            for r in fm.get("probes") or []:
                if not (isinstance(r, dict) and r.get("q") and r.get("looks_for")):
                    err(p, "each probe needs q and looks_for")
            if not all(isinstance(m, str) for m in fm.get("misconceptions") or []):
                err(p, "misconceptions must be a list of strings")
            if fm["status"] != "stub":
                heads = re.findall(r"^## (.+)$", p.body, re.M)
                if [h for h in heads if h in CONCEPT_SECTIONS] != CONCEPT_SECTIONS:
                    warn(p, f"sections should be {CONCEPT_SECTIONS} in order")
        if fm.get("volatile"):
            lv = _date(fm.get("last_verified"))
            if not lv:
                err(p, "volatile page needs last_verified date")
            elif (today - lv).days > STALE_DAYS:
                warn(p, f"stale: last_verified {lv} is over {STALE_DAYS} days ago")

    # --- citations ---
    for p in good:
        fm = p.fm
        if not isinstance(fm["sources"], list):
            continue
        if not fm["sources"] and fm["status"] != "stub" and fm["type"] not in SOURCES_OPTIONAL:
            err(p, "non-stub page needs at least one source")
        if fm["confidence"] == "high" and len({s.get("id") for s in fm["sources"] if isinstance(s, dict)}) < 2:
            warn(p, "confidence high but fewer than 2 distinct sources")
        for s in fm["sources"]:
            if not isinstance(s, dict) or s.get("id") not in by_id or by_id[s["id"]].fm["type"] != "source":
                err(p, f"citation {s} does not resolve to a source page"); continue
            q = s.get("quote")
            if q:
                if not s.get("locator"):
                    err(p, f"quote from {s['id']} needs a locator")
                src = by_id[s["id"]].fm
                raw = src.get("raw")
                if not raw or not raw_file(root, raw):
                    err(p, f"cannot verify quote: source {s['id']} has no raw file")
                elif _norm(q) not in _norm(raw_file(root, raw).read_text(encoding="utf-8", errors="replace")):
                    err(p, f"quote not found verbatim in {raw}: {q[:60]!r}")

    # --- relations & links ---
    inbound = {p.id: 0 for p in good}
    resolvable = set(stems) | {_norm(p.fm["title"]) for p in good} | {_norm(a) for p in good for a in p.fm["aliases"] if isinstance(p.fm["aliases"], list)}
    unresolved = 0
    for p in good:
        for r in p.fm["relations"] if isinstance(p.fm["relations"], list) else []:
            if not isinstance(r, dict) or r.get("rel") not in RELS:
                err(p, f"bad relation {r} (rel must be one of {sorted(RELS)})"); continue
            if "id" in r:
                if r["id"] not in by_id:
                    err(p, f"relation {r['rel']} -> unknown id {r['id']}")
                else:
                    inbound[r["id"]] += 1
                    if r["id"] == p.id:
                        err(p, "relation to itself")
            elif r.get("unresolved"):
                unresolved += 1
            else:
                err(p, f"relation {r} needs 'id' or 'unresolved'")
        for l in wikilinks(p.body):
            if l not in stems and _norm(l) not in resolvable:
                err(p, f"broken wikilink [[{l}]]")
            else:
                tgt = stems.get(l) or names.get(_norm(l))
                if tgt and tgt is not p:
                    inbound[tgt.id] += 1
        for s in p.fm["sources"] if isinstance(p.fm["sources"], list) else []:
            if isinstance(s, dict) and s.get("id") in inbound:
                inbound[s["id"]] += 1
    if unresolved:
        warnings.append(f"{unresolved} unresolved relation target(s) (propose pages for them)")
    if check_orphans and len(good) > 1:
        for p in good:
            if inbound[p.id] == 0 and not p.fm["relations"]:
                warn(p, "orphan: no inbound or outgoing links")
    return errors, warnings


def human_blocks_preserved(old_body: str, new_body: str) -> list[str]:
    """Return human-authored blocks present in old but missing from new."""
    new = human_blocks(new_body)
    return [b for b in human_blocks(old_body) if b not in new]
