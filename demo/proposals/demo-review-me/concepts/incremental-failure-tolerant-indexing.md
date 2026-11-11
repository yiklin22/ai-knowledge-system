---
id: cpt_klywfqg2
schema: 2
type: concept
title: Incremental, failure-tolerant indexing
aliases: []
domains:
- programming
summary: Re-index only the files that changed, commit work in batches, and fall back to a simpler mode when a dependency fails.
tags:
- indexing
- reliability
status: draft
confidence: medium
created: 2026-11-11
updated: 2026-11-11
sources:
- id: src_2bnb6lem
  locator: Key decisions and trade-offs
  quote: Files are re-chunked only when their mtime or size changes
relations:
- rel: related
  id: cpt_xve1awep
recall:
- q: When is a file re-chunked?
  a: Only when its modification time or size changes.
- q: What happens to Ask if the embedding library fails?
  a: It falls back to keyword search.
---

# Incremental, failure-tolerant indexing

## Knowledge
- [fact] Files are re-chunked only when their modification time or size changes.
- [fact] Embeddings are committed in batches, so a search can use partial progress.
- [fact] If the embedding library is missing or fails, Ask falls back to keyword search.

## Evidence
- Design document, Key decisions and trade-offs.

## Understanding
Each choice keeps the system answering while background work is unfinished or broken, at the price of results that can be briefly stale.

## Application
Useful for any local tool that indexes a folder the user keeps adding to.

## Uncertainty
- [inference] Modification time and size can miss an edit that preserves both; the source does not discuss this.

## Related
- Supports [[Hybrid retrieval with reciprocal-rank fusion]].
