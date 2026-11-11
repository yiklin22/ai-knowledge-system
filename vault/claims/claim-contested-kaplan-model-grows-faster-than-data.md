---
id: clm_f2xbs7e1
schema: 2
type: claim
title: Compute-optimal model size should grow faster than dataset size (Kaplan et al.)
aliases: []
domains:
- ai
summary: 'Kaplan et al.''s conclusion (N_opt about C^0.73): scale models faster than data and stop before convergence.'
tags:
- scaling-laws
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_edl36d2i
  locator: Kaplan et al.'s Scaling Laws
  quote: Kaplan et al. overestimated the optimal model size as their fitted exponent was larger.
relations:
- rel: about
  id: cpt_8cceawd5
verdict: contested
---

# Compute-optimal model size should grow faster than dataset size (Kaplan et al.)

## Evidence for
- Kaplan et al. fitted N_opt proportional to C^0.73 and concluded model size should grow faster than data. [fact] (Weng 2026)

## Evidence against
- Chinchilla found N_opt proportional to C^0.5, i.e. equal scaling, and showed a smaller model trained on more data can beat a larger one. [fact] (Weng 2026)
- Weng reports Kaplan et al. experimented mostly on small models and excluded embedding parameters; Pearce and Song (2024) show the local exponent in Kaplan's size range is close to 0.73 while it converges to Chinchilla's estimate at larger compute. [fact] (as reported by Weng 2026)

## Verdict reasoning
Contested rather than refuted: both results are internally consistent, and the disagreement is attributed to fit range and how parameters are counted. [inference] See [[claim-chinchilla-equal-scaling-of-model-and-tokens]].
