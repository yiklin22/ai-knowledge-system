"""Build a throwaway copy of the system around the sample vault in demo/.

Used by `./demo` (try the app without touching your own vault) and by the live red-team runs (let the digest
agent loose on a poisoned source where the only thing it can damage is a temp folder).
"""
import shutil
from pathlib import Path

from .schema import ROOT

CODE = ["app", "tools", "docs", "kb", "web", "CLAUDE.md", ".claude/skills", "playgrounds"]
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc")


def build(dest: Path, src: Path = ROOT) -> Path:
    """Copy the code and the sample data into dest (which must not exist) and return it."""
    dest.mkdir(parents=True)
    for name in CODE:
        s = src / name
        if s.is_dir():
            shutil.copytree(s, dest / name, ignore=IGNORE)
        elif s.is_file():
            (dest / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, dest / name)
    for name in ("vault", "raw", "proposals"):
        shutil.copytree(src / "demo" / name, dest / name)
    for d in ("data", "build", "raw/web", "raw/videos", "raw/chats"):
        (dest / d).mkdir(parents=True, exist_ok=True)
    venv = src / ".venv"
    if venv.is_dir():
        (dest / ".venv").symlink_to(venv, target_is_directory=True)   # so ./kb works inside the copy
    return dest


def tree_hash(folder: Path) -> dict[str, str]:
    """Relative path -> content hash for every file under folder, to prove nothing changed."""
    import hashlib
    return {str(f.relative_to(folder)): hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(folder.rglob("*"))
            if f.is_file() and "__pycache__" not in f.parts}   # bytecode caches appear when ./kb runs; they are not content
