---
id: ent_mhlveeon
schema: 2
type: entity
title: Hoffmann et al. (2022) Chinchilla paper
aliases:
- Chinchilla paper
domains:
- ai
summary: The paper that re-derived compute-optimal training and argued most large models were undertrained.
tags:
- paper
- scaling-laws
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_edl36d2i
  locator: Chinchilla Scaling Laws
  quote: null
relations:
- rel: about
  id: cpt_8cceawd5
kind: paper
---

# Hoffmann et al. (2022) Chinchilla paper

## Who/what
Referred to in Weng (2026) as Hoffmann et al. 2022, arXiv 2203.15556. Not in `raw/`; summary is secondary.

## Why it matters
[fact] Weng reports it scanned over 400 models (70M to over 16B parameters, 5B to 500B tokens) with three fitting methods whose results agree.
[fact] Its headline demonstration: Chinchilla (70B parameters, 1.4T tokens) outperformed Gopher (280B parameters, 300B tokens) at the same compute. See [[compute-optimal-training-chinchilla]].
