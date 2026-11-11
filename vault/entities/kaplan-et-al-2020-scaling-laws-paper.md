---
id: ent_burv8ybu
schema: 2
type: entity
title: Kaplan et al. (2020) scaling laws paper
aliases:
- Kaplan scaling laws
domains:
- ai
summary: The paper that popularised LLM scaling laws, fitting power laws of loss in model size, data and compute.
tags:
- paper
- scaling-laws
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_edl36d2i
  locator: Kaplan et al.'s Scaling Laws
  quote: null
relations:
- rel: about
  id: cpt_8cceawd5
kind: paper
---

# Kaplan et al. (2020) scaling laws paper

## Who/what
Referred to in Weng (2026) as Kaplan et al. (2020), arXiv 2001.08361. Not in `raw/`; everything here is from Weng's secondary summary.

## Why it matters
[fact] Weng reports it popularised scaling laws in the language-modeling community, with Transformer models of 768M to 1.5B non-embedding parameters and 22M to 23B tokens.
[fact] Its compute-optimal recommendation (model size grows faster than data) was later challenged by Chinchilla. See [[compute-optimal-training-chinchilla]].
