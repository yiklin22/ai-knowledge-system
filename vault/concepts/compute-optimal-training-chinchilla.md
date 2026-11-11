---
id: cpt_pg3p5grc
schema: 2
type: concept
title: Compute-optimal training (Chinchilla scaling)
aliases:
- Chinchilla scaling
- compute-optimal scaling
domains:
- ai
summary: Choosing model size and token count to minimise loss for a fixed compute budget; Chinchilla says scale both at about equal rates.
tags:
- scaling-laws
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_edl36d2i
  locator: Chinchilla Scaling Laws
  quote: When $\alpha \approx \beta$, model size and training tokens should scale at equal rates.
- id: src_edl36d2i
  locator: Chinchilla Scaling Laws
  quote: a model 4x smaller but trained on roughly 4x more tokens and it outperformed Gopher across the board.
relations:
- rel: broader
  id: cpt_8cceawd5
- rel: introduced_in
  id: ent_mhlveeon
- rel: prerequisite_for
  id: cpt_1dk2t19q
recall:
- q: At equal compute, how did Chinchilla compare to Gopher?
  a: Chinchilla had 70B parameters and 1.4T training tokens versus Gopher's 280B and 300B, and outperformed Gopher across the board (per Weng 2026).
- q: What approximation links training compute C, parameters N and tokens D?
  a: C is approximately 6ND (2ND forward plus 4ND backward).
probes:
- q: You double your compute budget. Under Chinchilla-style scaling, what happens to the optimal model size and token count?
  looks_for: Both grow by roughly the same factor (about sqrt(2) each when C is about 6ND), unlike Kaplan's advice of growing the model much faster.
misconceptions:
- Bigger models are always better for a fixed compute budget (Chinchilla says many large models were undertrained).
---

# Compute-optimal training (Chinchilla scaling)

## Knowledge
- Given a fixed compute budget C (approximately 6ND FLOPs), the question is how to split it between parameters N and training tokens D.
- The Chinchilla result: for every doubling of model size, also double the number of training tokens; train a smaller model on more data rather than a big one stopped early.

## Evidence
- The aim of the framework is how to allocate compute optimally between N and D. [fact] (Weng 2026, intro)
- When alpha is approximately beta, model size and training tokens should scale at equal rates. [fact] (Weng 2026, Method 3)
- Chinchilla (70B parameters, 1.4T tokens) outperformed Gopher (280B parameters, 300B tokens) at the same compute. [fact] (Weng 2026; the underlying paper is not in `raw/`)
- Chinchilla used three fitting methods (fixed model sizes, IsoFLOP profiles, parametric fit) whose results agreed. [fact] (Weng 2026)
- Weng reports that independent re-analysis (Besiroglu et al. 2024) found issues with Method 3's optimiser settings and rounding. [fact] (Weng 2026, Trickiness of fitting)

## Understanding
- Under C approximately 6ND, minimising a Rosenfeld-style loss L(N, D) subject to fixed C gives N_opt and D_opt as power laws in C; equal exponents mean equal scaling. [inference] (from Weng's derivation outline)
- The practical shift: models of Kaplan-era recommendations were too large and undertrained for their compute. [inference] (Weng: Chinchilla "would later overturn this recommendation")

## Application
- Use it to plan a training run: estimate N and D from budget before committing compute. [inference]
- Caveat: it optimises training compute only, not later inference cost. [speculation] (not covered by the sources in `raw/`)

## Uncertainty
- The Kaplan and Chinchilla results disagree; Weng offers partial reconciliations, so the exact exponents remain contested. [fact] (Weng 2026) See [[claim-contested-kaplan-model-grows-faster-than-data]].
- Every claim here comes from a secondary survey; the primary papers are not yet ingested, so confidence stays low. [inference]

## Related
- [[scaling-laws]] — the broader framework.
- [[hoffmann-et-al-2022-chinchilla-paper]] — the paper.
- [[data-constrained-scaling]] — what changes when unique data runs out.
