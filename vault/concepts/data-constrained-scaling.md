---
id: cpt_g762ml74
schema: 2
type: concept
title: Data-constrained scaling
aliases:
- data-limited scaling
- data wall
domains:
- ai
summary: How scaling laws change when unique training data is limited and must be repeated across epochs.
tags:
- scaling-laws
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_edl36d2i
  locator: Scaling Laws in Data-Limited Region
  quote: Classic scaling laws assume effectively *unlimited unique data*, no repetition, and no multi-epoch training.
relations:
- rel: broader
  id: cpt_8cceawd5
recall:
- q: What assumption do classic scaling laws make about data that data-constrained scaling drops?
  a: That unique data is effectively unlimited, with no repetition or multi-epoch training.
probes:
- q: If you must train for several epochs on the same data, would you expect larger or smaller models to suffer more from repetition, and why?
  looks_for: Weng reports Lovelace et al. finding larger models are more sensitive to repetition; the penalty depends on both model size and unique data (capacity ratio N/U_D).
---

# Data-constrained scaling

## Knowledge
- Classic scaling laws assume unlimited unique data. As models grow, high-quality unique tokens run short, so training may repeat data.
- Studies fit modified laws that discount repeated tokens.

## Evidence
- Classic laws assume effectively unlimited unique data, no repetition and no multi-epoch training. [fact] (Weng 2026, Data-Limited Region)
- Hernandez et al. (2022): with 10% repeated data in a 100B-token run, test loss showed double descent and repeated data hurt some OOD and fine-tuning evaluations. [fact] (as reported by Weng 2026)
- Muennighoff et al. (2023) model repeated tokens as losing value exponentially, with about 400 experiments up to 1500 epochs; they find excess parameters lose value faster than repeated data. [fact] (as reported by Weng 2026)
- Lovelace et al. (2026) report larger models are more sensitive to repetition, and strong weight decay reduces the penalty. [fact] (as reported by Weng 2026)

## Understanding
- Data quality matters as much as quantity: equal D can give very different compute efficiency. [fact] (Weng 2026, data pipeline discussion)
- Both fitted forms are empirical curve fits, and Weng says it is unclear why they should have exactly these forms. [fact] (Weng 2026)

## Application
- When planning long training runs on a fixed corpus, repetition can be traded against model size; the cited studies favour more epochs over more parameters. [inference] (from Muennighoff finding as reported)

## Uncertainty
- Fits are lab-like; Weng notes real-world repetition is more nuanced. [fact] (Weng 2026)
- All of this is second-hand; none of the primary papers are in `raw/`. [inference]

## Related
- [[scaling-laws]] — the framework this refines.
- [[compute-optimal-training-chinchilla]] — the infinite-data baseline.
