"""Parsing only: read markdown+YAML files into Page objects. No validation here."""
import re
from dataclasses import dataclass, field
from pathlib import Path
import yaml

from .schema import TYPES

FM_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
HUMAN_RE = re.compile(r"<!-- human -->(.*?)<!-- /human -->", re.S)


@dataclass
class Page:
    path: Path
    fm: dict = field(default_factory=dict)
    body: str = ""
    error: str | None = None

    @property
    def id(self):
        return self.fm.get("id")

    @property
    def stem(self):
        return self.path.stem


def slugify(s, n=70):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:n].strip("-") or "untitled"


def parse_text(path: Path, text: str) -> Page:
    m = FM_RE.match(text)
    if not m:
        return Page(path, error="no YAML frontmatter")
    try:
        fm = yaml.safe_load(m.group(1)) or {}
        if not isinstance(fm, dict):
            raise yaml.YAMLError("frontmatter is not a mapping")
    except yaml.YAMLError as e:
        return Page(path, error=f"invalid YAML: {e}")
    return Page(path, fm, m.group(2))


def load_dir(root: Path) -> list[Page]:
    """Load pages from the type folders under root (index.md/log.md at the top level are not pages)."""
    pages = []
    for folder, _ in TYPES.values():
        for f in sorted((root / folder).glob("*.md")):
            pages.append(parse_text(f, f.read_text(encoding="utf-8")))
    return pages


def human_blocks(body: str) -> list[str]:
    return [b.strip() for b in HUMAN_RE.findall(body)]


def wikilinks(body: str) -> list[str]:
    return [m.strip() for m in LINK_RE.findall(body)]
