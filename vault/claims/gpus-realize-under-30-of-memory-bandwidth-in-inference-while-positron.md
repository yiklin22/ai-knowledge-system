---
id: clm_vmllc112
schema: 2
type: claim
title: "GPUs realize under 30% of memory bandwidth in inference while Positron claims over 90%"
aliases: []
domains: [ai]
summary: "Positron says most accelerators achieve under 30% of theoretical memory bandwidth on real inference while its Asimov design realises over 90%; these are vendor claims, with Asimov performance from simulation."
tags: [hardware, inference, vendor-claim, volatile]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_ieprcram
    locator: "What We Believe, Memory-First Architecture"
    quote: "over 90% realized memory bandwidth utilization versus under 30% for GPUs"
  - id: src_zd9zmrdf
    locator: "Section on performance data"
    quote: null
relations:
  - {rel: about, id: ent_a0dcmkx0}
verdict: unverified
volatile: true
last_verified: 2026-11-08
---

# GPUs realize under 30% of memory bandwidth in inference while Positron claims over 90%

Statement: on real inference workloads GPUs and most accelerators achieve under 30% of their theoretical memory bandwidth, while Positron's memory-first Asimov design achieves over 90%.

## Evidence for
- Positron's vision page states both figures as part of its principles. [fact] (Positron vision, vendor)

## Evidence against
- The only evidence is the vendor's own marketing; no benchmark, workload or method is given. [fact] (Positron vision)
- The X-AI blog says Asimov performance data come from cycle-accurate simulations rather than measured production silicon and that Asimov is still planned for tape-out, so the over-90% figure is about a design not yet shipped. [fact] (X-AI blog, performance section; secondary summary of vendor material)
- Atlas, the first-generation deployed system, is a different product from Asimov. [fact] (X-AI blog)

## Verdict reasoning
- Unverified vendor claim; the under-30% GPU figure is unsourced and workload-dependent. Do not use as general fact. Check independent benchmarks when silicon ships. [inference]
