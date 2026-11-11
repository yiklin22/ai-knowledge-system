# 1. Markdown files are the source of truth; databases are rebuildable caches

**Status:** accepted (2026-11-08)

## Context
The knowledge has to outlive this program, be readable in Obsidian, and have a history that shows who changed what. There is one user and one writer.

## Decision
Approved pages are Markdown with YAML frontmatter under `vault/`. Everything in `build/` (full-text index, graph, passage index, embeddings) is derived and can be deleted and rebuilt with `./kb build`.

## Consequences
- Git gives history, diffs and rollback with no extra code. A page stays readable without the tool that wrote it.
- No migrations: a schema change is a text edit plus a version bump.
- No concurrent writers, and every query that is not a file read needs a derived index.
- A rebuild reads every page. At 208 pages that is well under a second.

## Revisit when
More than one person writes at the same time, or a rebuild takes long enough to notice.
