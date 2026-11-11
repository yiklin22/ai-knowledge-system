---
id: cpt_8cceawd5
schema: 2
type: concept
title: Scaling laws
aliases: []
domains:
- ai
summary: Empirical power-law relationships between loss and model size, data and compute, used to decide how to allocate training compute.
tags:
- curriculum
- transformer
status: draft
confidence: low
created: 2026-11-08
updated: '2026-11-08'
sources:
- id: src_edl36d2i
  locator: intro
  quote: the training loss $L$ decreases predictably as we scale up model size $N$, dataset size $D$, and compute $C$, following a power-law curve, which appears as a straight line on a log-log plot.
- id: src_edl36d2i
  locator: intro
  quote: at its core, it is about how to allocate precious compute optimally between $N$ and $D$.
- id: src_edl36d2i
  locator: Trickiness of Fitting Scaling Laws in Reality
  quote: scaling law fitting can be surprisingly sensitive to seemingly trivial procedural choices
relations:
- rel: related
  id: cpt_pg3p5grc
- rel: related
  id: cpt_g762ml74
recall:
- q: What does the approximation C ≈ 6ND mean?
  a: 'Training compute in FLOPs is about 6 times parameters times tokens: 2ND for the forward pass and 4ND for backpropagation.'
- q: What practical workflow do scaling laws support?
  a: Fit them on a handful of small runs, then extrapolate to estimate token and compute requirements for larger models.
probes:
- q: A scaling-law fit looks like a straight line on a log-log plot. What does that tell you about the functional form?
  looks_for: Loss follows a power law in the scaled quantity (possibly plus an irreducible term), so each constant-factor increase gives a predictable reduction.
misconceptions:
- Scaling laws tell you exactly how good a model will be at downstream tasks (they predict pretraining loss; transfer to post-training evaluation needs separate study).
---

# Scaling laws

## Knowledge
- Training loss L decreases predictably as model size N, dataset size D and compute C increase, following a power law (a straight line on a log-log plot).
- A useful approximation is C ≈ 6ND (2ND forward, 4ND backward).
- A core use is allocating compute between N and D; practitioners fit laws on small runs and extrapolate.

## Evidence
- The loss decreases predictably with N, D and C, following a power-law curve. [fact] (Weng 2026, intro)
- Early evidence: Hestness et al. (2017) saw power-law error across four domains; model improvements shifted the curve without changing the exponent. [fact] (as reported by Weng 2026)
- Kaplan et al. (2020) popularised scaling laws for language models; Chinchilla (2022) revised the compute-optimal allocation. [fact] (as reported by Weng 2026) See [[claim-contested-kaplan-model-grows-faster-than-data]] and [[claim-chinchilla-equal-scaling-of-model-and-tokens]].
- Weng notes that train and test loss are strongly correlated, but whether pretraining loss gains transfer to post-training evaluations needs separate studies. [fact] (Weng 2026)
- Fits can be very sensitive to procedure. [fact] (Weng 2026) See [[claim-scaling-law-fits-are-procedure-sensitive]].

## Understanding
- A power law means constant multiplicative gains: each fixed increase in scale buys a predictable fractional reduction in loss. [inference]
- Why the form is a power law is still being explained; see [[why-do-llm-scaling-laws-take-the-form-of-a-power-law]]. [inference]

## Application
- Plan a run by fitting small models and extrapolating, while keeping architecture, optimizer, data mix and tokenizer fixed. [fact] (Weng 2026, Trickiness of Fitting)
- For compute-limited training, read [[compute-optimal-training-chinchilla]]; for limited unique data, read [[data-constrained-scaling]]. [inference]

## Uncertainty
- The Kaplan and Chinchilla results conflict on optimal allocation; Weng gives partial reconciliations. [fact] (Weng 2026)
- Whether the laws keep holding is an open question: [[do-scaling-laws-keep-holding-as-models-and-data-grow]]. [inference]
- All evidence here is from one secondary survey; primary papers are not yet ingested. [inference]

## Related
- [[compute-optimal-training-chinchilla]] — allocation under fixed compute.
- [[data-constrained-scaling]] — limited unique data.
- [[kaplan-et-al-2020-scaling-laws-paper]] and [[hoffmann-et-al-2022-chinchilla-paper]] — the two key papers.
