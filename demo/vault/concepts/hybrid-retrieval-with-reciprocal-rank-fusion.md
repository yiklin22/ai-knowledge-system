---
id: cpt_xve1awep
schema: 2
type: concept
title: Hybrid retrieval with reciprocal-rank fusion
aliases: []
domains:
- ai
summary: Search the same passages with a keyword index and with embeddings, then merge the two ranked lists by rank position.
tags:
- retrieval
- rag
status: draft
confidence: medium
created: 2026-11-11
updated: 2026-11-11
sources:
- id: src_2bnb6lem
  locator: Key decisions and trade-offs
  quote: The two rankings are merged with reciprocal-rank fusion (k = 60).
relations:
- rel: related
  id: ent_8e08u038
recall:
- q: What two indexes does hybrid retrieval combine here?
  a: BM25 keyword search (SQLite FTS5) and bge-small-en-v1.5 embeddings.
- q: Why fuse by rank and not by score?
  a: BM25 scores and cosine similarities are on different scales; ranks are directly comparable.
---

# Hybrid retrieval with reciprocal-rank fusion

## Knowledge
- [fact] Passages are indexed twice: SQLite FTS5 with BM25 for exact terms, and `bge-small-en-v1.5` embeddings for paraphrases.
- [fact] The rankings are merged with reciprocal-rank fusion, k = 60.
- [fact] Semantic hits below a cosine similarity of 0.68 are dropped so the system can answer "nothing found".

## Evidence
- Design document, Key decisions and trade-offs.
- Measured results are in the evaluation source.

## Understanding
Keyword search finds names and numbers and misses rewordings; embeddings do the reverse. Fusing by rank avoids having to make the two scoring scales comparable.

## Application
A sensible default for question answering over a few thousand to a few hundred thousand passages. Tune the similarity floor on your own corpus; 0.68 was chosen for this one.

## Uncertainty
- [inference] The 0.68 floor and k = 60 were set on one corpus and may not transfer.

## Related
- Evidence for the benefit is tracked in the claim on hybrid versus keyword ranking.
