---
id: qst_r3buahv3
schema: 2
type: question
title: At what corpus size does brute-force cosine search stop being enough?
aliases: []
domains:
- ai
- programming
summary: The design uses a NumPy matrix multiply over all passage embeddings and expects that to change at around a million passages; the real threshold is unmeasured.
tags:
- retrieval
- scaling
status: draft
confidence: low
created: 2026-11-11
updated: 2026-11-11
sources:
- id: src_2bnb6lem
  locator: Key decisions and trade-offs
  quote: This would change at roughly 10⁶ passages.
relations:
- rel: about
  id: cpt_xve1awep
state: open
---

# At what corpus size does brute-force cosine search stop being enough?

## Why I'm asking
The design document chose brute-force search over a vector database at about ten thousand passages and names a rough limit without a measurement.

## What would answer it
A latency curve for query time against passage count on this machine, up to the point where a question takes longer than a second.
