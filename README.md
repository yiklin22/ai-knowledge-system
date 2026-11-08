# Personal Knowledge System

Throw in AI chats, documents, work files, YouTube links and websites. Claude reads them and **proposes** structured, evidence-linked knowledge; you approve; it lands in an Obsidian vault you can search and study from.

```
raw/        immutable sources (chats/ documents/ web/ videos/ assets/)
proposals/  AI-written pages waiting for your review
vault/      approved knowledge (open this folder in Obsidian)
build/      derived search + graph (disposable)     data/  learning progress (SQLite)
docs/knowledge-schema.md   the contract          CLAUDE.md   instructions for Claude
```

## What the vault holds
`source` (what I read + reliability) · `concept` (ideas, with recall cards) · `claim` (testable statements, contradictions) · `entity` (people, orgs, papers, models, tools) · `question` (what I don't know yet) · `insight` (my own conclusions and decisions) · `project` (where knowledge gets applied) · `map` (domain hubs and learning paths), across domains listed in `vault/domains.yml`.

## Daily use
Open Claude Code here and say "ingest <url>", "ingest ~/Downloads/conversations.json", or paste a chat. Then:

```
./kb validate --proposals <batch>   # check what Claude proposed
./kb approve <batch>                # YOU approve (add --amend to change existing pages)
./kb search "attention"             # full-text search
./kb quiz                           # spaced repetition
./kb status                         # counts, pending batches, cards due
```

Setup: `uv venv && uv pip install -r requirements.txt` (pandoc for docx/html). Tests: `.venv/bin/python -m unittest discover -s tests -t .`
