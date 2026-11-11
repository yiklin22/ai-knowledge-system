---
id: ent_8e08u038
schema: 2
type: entity
title: bge-small-en-v1.5
aliases:
- BAAI/bge-small-en-v1.5
domains:
- ai
summary: A small English text-embedding model from BAAI, used here through ONNX for semantic search.
tags:
- embeddings
status: draft
confidence: medium
created: 2026-11-11
updated: 2026-11-11
sources:
- id: src_2bnb6lem
  locator: Key decisions and trade-offs
  quote: no PyTorch install, CPU-only, ~15 passages/s
relations: []
kind: model
---

# bge-small-en-v1.5

## Who/what
An embedding model: it turns a passage into a vector so that similar meanings land close together.

## Why it matters
It is the semantic half of hybrid retrieval in this system, chosen because it runs on a CPU without PyTorch.
