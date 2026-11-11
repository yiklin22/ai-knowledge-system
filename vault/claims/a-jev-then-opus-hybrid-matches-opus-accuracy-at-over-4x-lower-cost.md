---
id: clm_afjprlw5
schema: 2
type: claim
title: "A Jev-then-Opus hybrid matches Opus accuracy at over 4x lower cost"
aliases: []
domains: [ai]
summary: Hightouch reports that escalating only uncertain Jev cases to Opus gives near-Opus accuracy for about a quarter of the cost on an easier test, but the cost advantage shrinks to under 2x on a harder test.
tags: [llm-judge, cost, vendor-claim]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_x1ew5c1z
    locator: "So, what's the conclusion?"
    quote: null
relations:
  - {rel: about, id: cpt_i243o4zy}
  - {rel: related, id: clm_6zpsrg7m}
volatile: true
last_verified: 2026-11-08
verdict: unverified
---

# A Jev-then-Opus hybrid matches Opus accuracy at over 4x lower cost

## Evidence for

- [fact] Easier test: hybrid Jev 98.8% at $0.88 per 1,000 vs Opus 5.5 99.0% at $3.86 (about 4.4x cheaper, computed from the source's table).
- [fact] Harder test: hybrid Jev 95.3% at $2.94 vs Opus 95.1% at $5.39.

## Evidence against

- [inference] The "over 4x" figure holds only on the easier test; on the harder test the saving computed from the table is about 1.8x (5.39 / 2.94).
- [inference] Differences of 0.2 points on 1,000 identities are about two identities, within plausible noise; no repeats or confidence intervals are given.
- [fact] Vendor-run, own setup, synthetic data; the post says costs and latencies "will vary".

## Verdict reasoning

[inference] Directionally plausible and clearly reported, but a headline of "4x" is selective, and it is a single vendor benchmark. Left unverified pending independent replication.
