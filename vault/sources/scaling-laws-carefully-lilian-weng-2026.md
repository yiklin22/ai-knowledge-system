---
id: src_edl36d2i
schema: 2
type: source
title: Scaling Laws, Carefully (Lilian Weng, 2026)
aliases: []
domains:
- ai
summary: 'A long survey of LLM scaling laws: Kaplan, Chinchilla, why they disagree, data-limited regimes, and why fitting is fragile.'
tags:
- survey
- scaling-laws
status: reviewed
confidence: medium
created: '2026-11-08'
updated: '2026-11-08'
sources: []
relations: []
kind: web
reliability: secondary
raw: raw/web/2026-11-08-scaling-laws-carefully.md
url: https://lilianweng.github.io/posts/2026-06-24-scaling-laws/
author: Lilian Weng
published: '2026-06-24'
---

# Scaling Laws, Carefully (Lilian Weng, 2026)

## Takeaways
- Loss falls as a power law in model size N, data D and compute C; scaling laws describe how to split compute between N and D.
- Kaplan et al. (2020) and Chinchilla (Hoffmann et al. 2022) disagree on the optimal split; Weng summarises why (fit range, embedding parameters).
- Classic laws assume unlimited unique data; repeated-data regimes need adjusted fits. Fits are sensitive to procedure.
- This is a secondary survey of primary papers (Kaplan, Hoffmann, Muennighoff, Besiroglu and others) that are not in `raw/`.

## Locator map
Headings in the raw file: Early days · Kaplan et al. · Chinchilla (Methods 1-3) · Reconciling Kaplan and Chinchilla · Why power law? · Data-limited region · Trickiness of fitting · Toy simulation.
