---
id: src_ieprcram
schema: 2
type: source
title: "Positron AI vision page"
aliases: []
domains: [ai]
summary: "Positron's own vision statement for memory-first, LPDDR-based inference silicon, with market claims and performance claims that are marketing, not independent measurements."
tags: [hardware, inference, vendor]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: ent_a0dcmkx0}
  - {rel: about, id: clm_vmllc112}
kind: web
reliability: vendor
raw: raw/web/2026-11-08-positron-vision.md
url: "https://www.positron.ai/vision"
author: Positron AI
published: "2026-01-01"
volatile: true
last_verified: 2026-11-08
---

# Positron AI vision page

## Takeaways
- Company view: power availability and memory bandwidth, not compute, are the bottlenecks; training and inference need different silicon; inference splits into subworkloads (prefill versus decode, attention versus feed-forward) so the future is heterogeneous.
- Product stance: Asimov is designed around memory bandwidth and capacity first, using commodity LPDDR rather than HBM; Positron focuses on the generative decode phase and works alongside GPUs.
- Vendor claims (unverified): over 90% realized memory bandwidth utilisation versus under 30% for GPUs; most accelerators achieve under 30% of theoretical bandwidth on real inference; timeline of 8 months to FPGA prototype, 7 months to first product, 7 more to a major cloud provider; Atlas "fully designed, fabricated, assembled and tested in America".
- The page date (2026-01-01) is a placeholder from ingestion; the page is undated. All numbers are marketing claims.

## Locator map
- Sections: Our Vision; How We See the Market; Evolution of Inference; What We Believe (Memory-First Architecture, LPDDR Over HBM, Iteration Speed, Full-Stack Control, TCO and ROI).
