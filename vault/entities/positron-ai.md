---
id: ent_a0dcmkx0
schema: 2
type: entity
title: "Positron AI"
aliases: [Positron]
domains: [business]
summary: "AI inference-silicon startup with memory-first LPDDR designs (Atlas deployed, Asimov planned, Titan 2027), reportedly raising up to $875 million in September 2026."
tags: [hardware, startup, inference, volatile]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_ieprcram
    locator: "Vision page"
    quote: null
  - id: src_zd9zmrdf
    locator: "Table: Titan versus Atlas"
    quote: null
relations:
  - {rel: related, id: clm_vmllc112}
kind: organization
volatile: true
last_verified: 2026-11-08
---

# Positron AI

## Who/what
- Inference-chip company that says it builds memory-first accelerators using commodity LPDDR memory instead of HBM and targets the decode phase of generative inference alongside GPUs. [fact] (Positron vision; vendor)
- Funding (secondary report of the company announcement, 10 September 2026): nominal $875 million at a $5 billion valuation, being a $375 million Series C plus up to $500 million Series C-1 (conditional). [fact] (X-AI blog)
- Products: Atlas first generation, reportedly 50+ racks on Oracle Cloud Infrastructure; Asimov planned for TSMC N3P tape-out at end of 2026 and production in second half of 2027; Titan "Coming in 2027", with 4 or 8 Asimov chips. [fact] (X-AI blog; vendor roadmap)

## Why it matters
- A vendor-sourced example of the argument that inference is memory-bound and needs different hardware from training. [inference]
- Roadmap dates and performance numbers are company statements; Asimov numbers come from simulation. [fact] (X-AI blog)
