"""Operations shared by the CLI and the web app. No printing, no sys.exit: return data.

All functions take `root` (the project directory) so they can be tested against a temp directory.
"""
import datetime
import difflib
import re
import shutil
from pathlib import Path

from . import index, learning, metrics
from .parse import load_dir
from .schema import ROOT, TYPES
from .validate import human_blocks_preserved, load_domains, validate


def _p(root: Path):
    return root / "vault", root / "proposals"


def rebuild(root: Path = ROOT) -> dict:
    vault, _ = _p(root)
    pages = load_dir(vault)
    errors, _w = validate(pages, load_domains(vault), root=root)
    if errors:
        return {"ok": False, "errors": errors}
    index.build(pages, vault, build_dir=root / "build")
    con = learning.connect(root / "data" / "learning.db")
    added, gone = learning.sync(con, pages)
    return {"ok": True, "pages": len(pages), "cards_added": added, "cards_removed": gone}


def list_batches(root: Path = ROOT) -> list[str]:
    _, prop = _p(root)
    return sorted(b.name for b in prop.glob("*/") if b.is_dir() and any(b.rglob("*.md")))


def batch_report(root: Path, batch: str) -> dict:
    """Validation + what approving would do, without changing anything."""
    vault, prop = _p(root)
    bdir = prop / batch
    if not bdir.is_dir():
        return {"ok": False, "errors": [f"no such batch: {batch}"], "warnings": [], "files": []}
    vault_pages = load_dir(vault)
    new_pages = load_dir(bdir)
    by_id = {p.id: p for p in vault_pages if p.id}
    new_ids = {n.id for n in new_pages}
    merged = [p for p in vault_pages if p.id not in new_ids] + new_pages
    errors, warnings = validate(merged, load_domains(vault), root=root, check_orphans=False)
    files, amended = [], []
    for p in new_pages:
        old = by_id.get(p.id)
        if old:
            amended.append(p)
            lost = human_blocks_preserved(old.body, p.body)
            if lost:
                errors.append(f"{p.path.name}: would remove/alter human-authored text: {lost[0][:60]!r}")
        else:
            for v in vault_pages:
                if v.path.name == p.path.name:
                    errors.append(f"{p.path.name}: filename already used by {v.id}")
        files.append({"name": p.path.name, "type": p.fm.get("type"), "title": p.fm.get("title"), "id": p.id,
                      "action": "amend" if old else "add", "status": p.fm.get("status")})
    return {"ok": not errors, "errors": errors, "warnings": warnings, "files": files, "has_amendments": bool(amended)}


def batch_diff(root: Path, batch: str, name: str) -> dict:
    """Unified diff of one proposed file against the vault (or full text if new)."""
    vault, prop = _p(root)
    for f in (prop / batch).rglob(name):
        new_text = f.read_text(encoding="utf-8")
        from .parse import parse_text
        pid = parse_text(f, new_text).id
        for v in load_dir(vault):
            if v.id == pid:
                old_text = v.path.read_text(encoding="utf-8")
                d = "".join(difflib.unified_diff(old_text.splitlines(True), new_text.splitlines(True), "vault (current)", "proposal"))
                return {"action": "amend", "diff": d, "text": new_text}
        return {"action": "add", "diff": "", "text": new_text}
    return {"action": "missing", "diff": "", "text": ""}


def approve_batch(root: Path, batch: str, amend: bool = False) -> dict:
    """Move a reviewed batch into the vault. Only call this on an explicit human instruction."""
    vault, prop = _p(root)
    rep = batch_report(root, batch)
    if rep["has_amendments"] and not amend:
        rep["errors"].append("batch modifies existing pages; confirm the amendment diff to proceed")
        rep["ok"] = False
    if rep["errors"]:
        return {"ok": False, "errors": rep["errors"], "warnings": rep["warnings"]}
    bdir = prop / batch
    vault_pages = {p.id: p for p in load_dir(vault) if p.id}
    log, today = [], datetime.date.today().isoformat()
    for p in load_dir(bdir):
        folder = TYPES[p.fm["type"]][0]
        dest = vault_pages[p.id].path if p.id in vault_pages else vault / folder / p.path.name
        text = p.path.read_text(encoding="utf-8")
        if p.id not in vault_pages and p.fm["status"] == "draft":
            text = re.sub(r"^status: draft", "status: reviewed", text, count=1, flags=re.M)
        dest.write_text(text, encoding="utf-8")
        log.append(f"- {'amended' if p.id in vault_pages else 'added'} {dest.relative_to(root)} ({p.id})")
    with open(vault / "log.md", "a", encoding="utf-8") as f:
        f.write(f"\n## [{today}] approve | {batch}\n" + "\n".join(log) + "\n")
    shutil.rmtree(bdir)
    metrics.record(root, "review", decision="approved", batch=batch, pages=len(log), amended=sum(1 for x in log if x.startswith("- amended")))
    return {"ok": True, "log": log, "warnings": rep["warnings"], "rebuild": rebuild(root)}


def discard_batch(root: Path, batch: str) -> dict:
    """Delete an unapproved proposal batch (AI-written; never touches vault/ or raw/)."""
    _, prop = _p(root)
    bdir = (prop / batch).resolve()
    if prop.resolve() not in bdir.parents or not bdir.is_dir():
        return {"ok": False, "errors": ["no such batch"]}
    pages = sum(1 for _ in bdir.rglob("*.md"))
    shutil.rmtree(bdir)
    metrics.record(root, "review", decision="discarded", batch=batch, pages=pages)
    return {"ok": True}
