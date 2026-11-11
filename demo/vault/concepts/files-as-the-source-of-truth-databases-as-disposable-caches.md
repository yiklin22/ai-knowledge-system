---
id: cpt_8dguiye3
schema: 2
type: concept
title: Files as the source of truth, databases as disposable caches
aliases: []
domains:
- programming
summary: Keep the canonical data in plain files under version control and treat every index or database as something that can be deleted and rebuilt.
tags:
- architecture
- storage
status: draft
confidence: medium
created: 2026-11-11
updated: 2026-11-11
sources:
- id: src_2bnb6lem
  locator: Key decisions and trade-offs
  quote: Everything in `build/` can be deleted and rebuilt.
relations:
- rel: prerequisite_for
  id: cpt_vl2ncl2r
recall:
- q: In this design, which store is canonical and which are disposable?
  a: Approved Markdown + YAML files are canonical; everything in build/ (search index, graph) is derived and can be rebuilt.
- q: What is the stated cost of making files the source of truth?
  a: No concurrent multi-user writes.
---

# Files as the source of truth, databases as disposable caches

## Knowledge
- [fact] In this system approved Markdown with YAML frontmatter is canonical; the search index and graph live in `build/` and are derived.
- [fact] Git supplies history, diffs and rollback.
- [inference] The pattern trades write concurrency for simplicity: there is one writer and no migrations.

## Evidence
- The design document states the rule and its cost directly (source: Key decisions and trade-offs).

## Understanding
A cache you can rebuild cannot hold the only copy of anything, so losing it costs minutes. The canonical files stay readable without the program that wrote them.

## Application
Use it for single-user or low-write systems where human-readable history matters. Reach for a real database when several writers must commit at once.

## Uncertainty
- [inference] The document names the cost (no concurrent multi-user writes) but gives no measurement of rebuild time as the vault grows.

## Related
- Leads to [[Human approval gate]]: an approval is just a reviewed file move plus a rebuild.
