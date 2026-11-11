---
id: clm_uxo31t0x
schema: 2
type: claim
title: "Per-step error compounds across an agent workflow"
aliases: []
domains: [ai]
summary: "If each step succeeds independently with probability p, an n-step workflow succeeds with p^n; at 85% per step that is about 44% over five steps and 20% over ten."
tags: [agents, reliability, compounding-error]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources:
  - id: src_ieap5jak
    locator: "Failure Pattern 3: The Compounding Error Problem"
    quote: "Each step in a multi-step workflow introduces a small error."
relations:
  - {rel: about, id: cpt_g1vxdqj6}
  - {rel: qualifies, id: cpt_r0y15j1d}
verdict: supported
---

# Per-step error compounds across an agent workflow

## Evidence for
- [fact] The source gives 85% per step as 85% for one step, 44% for five and 20% for ten. [fact] (src_ieap5jak)
- [inference] The arithmetic is correct for independent steps: 0.85^5 = 0.44 and 0.85^10 = 0.20.
- [fact] The source also cites the APEX-Agents benchmark (January 2026): best models completed about 24% of real-world tasks on the first attempt. (src_wlpdy4uq, src_ieap5jak; second-hand)

## Evidence against
- [inference] Steps are not independent in practice: tools can fail visibly and be retried, a later step can correct an earlier one, and verification or Reflexion-style retries raise effective per-step reliability, so p^n is a lower-bound illustration rather than a prediction.
- [inference] The 85% figure is an assumption in the source, not a measured per-step accuracy.

## Verdict reasoning
Supported as a mathematical statement under an independence assumption; not established as an empirical rate for real agents. Verdict is `supported` for the principle only.
