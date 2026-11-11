---
id: clm_crqs8yy6
schema: 2
type: claim
title: Compute-optimal model size and training tokens should scale at roughly equal rates
aliases: []
domains:
- ai
summary: Chinchilla's finding that, for a fixed compute budget, parameters and tokens should grow together.
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
relations:
- rel: about
  id: cpt_pg3p5grc
- rel: contradicts
  id: clm_f2xbs7e1
verdict: supported
---

# Compute-optimal model size and training tokens should scale at roughly equal rates

## Evidence for
- Chinchilla's three fitting methods agree, and Chinchilla beat the larger Gopher at equal compute. [fact] (Weng 2026)

## Evidence against
- Kaplan et al. (2020) concluded the opposite emphasis; Weng argues the difference is explainable but it is documented as a conflict. See [[claim-contested-kaplan-model-grows-faster-than-data]].
- Method 3 of Chinchilla was found slightly off from the other two methods (Besiroglu et al. 2024, as reported by Weng). [fact]

## Verdict reasoning
Marked supported on the strength of the Chinchilla design and Weng's reconciliation, but confidence is low because the source is a single secondary survey and the primary papers are not yet ingested. [inference]
