---
id: src_2bnb6lem
schema: 2
type: source
title: Architecture and design decisions (this project)
aliases: []
domains:
- programming
summary: 'The project''s own design document: the problem, the components, and each key decision with its cost and gain.'
tags:
- demo
status: draft
confidence: medium
created: 2026-11-11
updated: 2026-11-11
sources: []
relations: []
kind: document
reliability: primary
raw: raw/documents/2026-11-10-architecture-and-design-decisions.md
url: null
author: project author
published: '2026-11-10'
---

# Architecture and design decisions (this project)

## Takeaways
- Approved Markdown is canonical; every database is a rebuildable cache.
- The digest agent proposes; only a person approves.
- Ask uses hybrid retrieval (BM25 plus embeddings, fused by rank) and one tool-less model call.
- It is a primary source for how this system works, not for whether those choices are right in general.

## Locator map
- Components: the diagram and layer table
- Key decisions and trade-offs: one paragraph per decision
- Failure handling: table of failures and behaviour
- What is deliberately not built: last section
