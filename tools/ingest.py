#!/usr/bin/env python3
"""Convert anything into a clean markdown source under raw/.

Usage:
  ingest.py <url|file> [<url|file> ...]   web pages, YouTube, PDF, docx, html, md, txt, chat exports (json)
  ingest.py - --kind chat --title "..."    read pasted text from stdin

raw/ is append-only: this script only ever creates new files, never overwrites.
Prints the paths it created so the LLM can then follow the Ingest workflow in CLAUDE.md.
"""
import argparse, datetime, json, re, shutil, subprocess, sys, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
TODAY = datetime.date.today().isoformat()


def slugify(s, n=60):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return (s[:n].strip("-")) or "untitled"


def write_source(kind, title, body, meta):
    """Write raw/<kind>/<date>-<slug>.md with provenance frontmatter. Never overwrites."""
    folder = RAW / kind
    folder.mkdir(parents=True, exist_ok=True)
    base = f"{TODAY}-{slugify(title)}"
    path, i = folder / f"{base}.md", 2
    while path.exists():
        path, i = folder / f"{base}-{i}.md", i + 1
    fm = ["---", f"title: {json.dumps(title, ensure_ascii=False)}", f"kind: {kind}", f"ingested: {TODAY}"]
    fm += [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in meta.items() if v]
    fm.append("---\n")
    path.write_text("\n".join(fm) + "\n" + body.strip() + "\n", encoding="utf-8")
    return path


def keep_original(src: Path):
    """Copy a binary original into raw/assets/ (never overwrite)."""
    dest = RAW / "assets" / src.name
    i = 2
    while dest.exists():
        dest = RAW / "assets" / f"{src.stem}-{i}{src.suffix}"
        i += 1
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return dest.relative_to(ROOT).as_posix()


# ---------- YouTube ----------
YT_RE = re.compile(r"(?:youtube\.com/(?:watch\?(?:.*&)?v=|shorts/|live/|embed/)|youtu\.be/)([\w-]{11})")


def ingest_youtube(url, vid):
    import yt_dlp
    with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True, "no_warnings": True}) as y:
        info = y.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)
    title = info.get("title", vid)
    segs = []
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        try:
            t = YouTubeTranscriptApi().fetch(vid, languages=["en", "en-US", "en-GB"])
            segs = [(s.start, s.text) for s in t]
        except AttributeError:  # old API
            segs = [(s["start"], s["text"]) for s in YouTubeTranscriptApi.get_transcript(vid)]
    except Exception as e:
        print(f"  ! no transcript via youtube-transcript-api ({type(e).__name__}); description only", file=sys.stderr)
    lines, last = [], -999
    for start, text in segs:  # timestamp roughly every 30s so claims can cite a locator
        text = text.replace("\n", " ").strip()
        if start - last >= 30:
            lines.append(f"\n**[{int(start // 60):02d}:{int(start % 60):02d}]** {text}")
            last = start
        else:
            lines[-1] += " " + text
    body = f"# {title}\n\n## Description\n{info.get('description') or '_none_'}\n\n## Transcript\n"
    body += "\n".join(lines) if lines else "_Transcript unavailable._"
    return [write_source("videos", title, body, {
        "url": f"https://www.youtube.com/watch?v={vid}", "channel": info.get("uploader"),
        "published": info.get("upload_date"), "duration_s": info.get("duration"),
        "transcript": "available" if lines else "missing"})]


# ---------- Web ----------
def ingest_web(url):
    import trafilatura
    html = trafilatura.fetch_url(url)
    if not html:
        raise RuntimeError("could not download page (blocked, paywalled or offline)")
    body = trafilatura.extract(html, output_format="markdown", include_links=True,
                               include_tables=True, with_metadata=False)
    if not body:
        raise RuntimeError("page downloaded but no readable content extracted")
    md = trafilatura.extract_metadata(html)
    title = (md.title if md and md.title else urllib.parse.urlparse(url).path.strip("/").split("/")[-1] or url)
    return [write_source("web", title, f"# {title}\n\n{body}", {
        "url": url, "author": md.author if md else None, "published": md.date if md else None,
        "site": md.sitename if md else None})]


# ---------- Chats ----------
def _chatgpt(conv):
    msgs = []
    node = conv.get("current_node")
    mapping = conv.get("mapping", {})
    chain = []
    while node:  # walk the active branch leaf -> root
        chain.append(mapping[node]); node = mapping[node].get("parent")
    for n in reversed(chain):
        m = n.get("message")
        if not m or not m.get("content"):
            continue
        role = m["author"]["role"]
        parts = m["content"].get("parts") or []
        text = "\n".join(p for p in parts if isinstance(p, str)).strip()
        if text and role in ("user", "assistant"):
            msgs.append((role, text))
    return conv.get("title") or "ChatGPT conversation", msgs, "chatgpt"


def _claude(conv):
    msgs = []
    for m in conv.get("chat_messages", []):
        text = m.get("text") or "\n".join(c.get("text", "") for c in m.get("content", []) if isinstance(c, dict))
        if text.strip():
            msgs.append(("user" if m.get("sender") == "human" else "assistant", text.strip()))
    return conv.get("name") or "Claude conversation", msgs, "claude"


def ingest_chat_json(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    convs = data if isinstance(data, list) else [data]
    out = []
    for c in convs:
        if "mapping" in c:
            title, msgs, src = _chatgpt(c)
        elif "chat_messages" in c:
            title, msgs, src = _claude(c)
        else:
            raise RuntimeError("unrecognised chat JSON (expected ChatGPT or Claude export)")
        if not msgs:
            continue
        body = f"# {title}\n\n" + "\n\n".join(f"### {'Me' if r == 'user' else 'AI'}\n{t}" for r, t in msgs)
        out.append(write_source("chats", title, body, {"platform": src, "original": keep_original(path)}))
    return out


# ---------- Files ----------
def ingest_file(p: Path, kind_hint=None):
    ext = p.suffix.lower()
    if ext == ".json":
        return ingest_chat_json(p)
    if ext == ".pdf":
        from pypdf import PdfReader
        r = PdfReader(str(p))
        body = "\n\n".join(f"<!-- page {i} -->\n{pg.extract_text() or ''}" for i, pg in enumerate(r.pages, 1))
        if len(body.strip()) < 50 * max(1, len(r.pages)) // 5:
            print("  ! very little text; likely a scanned PDF needing OCR", file=sys.stderr)
        title = (r.metadata.title if r.metadata and r.metadata.title else p.stem)
        return [write_source(kind_hint or "documents", title, f"# {title}\n\n{body}", {"original": keep_original(p)})]
    if ext in (".docx", ".odt", ".epub", ".html", ".htm", ".rtf", ".pptx"):
        body = subprocess.run(["pandoc", str(p), "-t", "gfm", "--wrap=none"], capture_output=True, text=True, check=True).stdout
        return [write_source(kind_hint or "documents", p.stem, f"# {p.stem}\n\n{body}", {"original": keep_original(p)})]
    if ext in (".md", ".txt", ".markdown", ""):
        text = p.read_text(encoding="utf-8", errors="replace")
        return [write_source(kind_hint or "documents", p.stem, text, {})]
    raise RuntimeError(f"unsupported file type {ext}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--kind", choices=["chats", "documents", "web", "videos", "chat", "document"],
                    help="override folder (needed for stdin; e.g. pasted chat logs)")
    ap.add_argument("--title")
    a = ap.parse_args()
    kind = {"chat": "chats", "document": "documents"}.get(a.kind, a.kind)
    created, failed = [], []
    for item in a.inputs:
        try:
            if item == "-":
                text = sys.stdin.read()
                if not text.strip():
                    raise RuntimeError("empty stdin")
                res = [write_source(kind or "documents", a.title or text.strip().splitlines()[0][:60], text, {})]
            elif re.match(r"https?://", item):
                m = YT_RE.search(item)
                res = ingest_youtube(item, m.group(1)) if m else ingest_web(item)
            else:
                p = Path(item).expanduser()
                if not p.exists():
                    raise RuntimeError("file not found")
                res = ingest_file(p, kind if p.suffix.lower() != ".json" else None)
            created += res
            for r in res:
                print(f"created {r.relative_to(ROOT)}")
        except Exception as e:
            failed.append(item)
            print(f"FAILED {item}: {e}", file=sys.stderr)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
