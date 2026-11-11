---
id: src_x1ew5c1z
schema: 2
type: source
title: "LLM Judges for Identity Resolution at 4x Lower Cost (Hightouch)"
aliases: []
domains: [ai]
summary: Hightouch blog post benchmarking cheap "decision models" (Jev, GPT-6 Luna) and frontier LLMs as judges of over-merged identity profiles, and showing a confidence-gated hybrid with Opus.
tags: [llm-judge, cost, evaluation, identity-resolution]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: authored_by, id: ent_inabsoaz}
  - {rel: about, id: cpt_bjjfgu02}
  - {rel: about, id: cpt_98mq6mw6}
  - {rel: about, id: cpt_i243o4zy}
  - {rel: about, id: cpt_rjqiu953}
  - {rel: about, id: ent_i2k1snkk}
kind: web
reliability: vendor
raw: raw/web/2026-11-08-llm-judges-for-identity-resolution-at-4x-lower-cost-hightouc.md
url: "https://hightouch.com/blog/llm-judges-identity-resolution"
author: "Hightouch"
published: "2026-11-04"
volatile: true
last_verified: 2026-11-08
---

# LLM Judges for Identity Resolution at 4x Lower Cost (Hightouch)

Reliability: vendor. Hightouch sells identity-resolution tooling and reports its own experiment on synthetic data; the post itself says costs and latencies are from its own setup. Methods are described clearly and numbers are tabulated, but there is one benchmark of 1,000 identities, no repeats or error bars, and the harder test set is not sized. Prices, model names and latencies are volatile (as of 2026-11-04).

## Takeaways

- [fact] Task: judge whether a profile (set of records) is an over-merge, i.e. describes more than one real person. Benchmark: 1,000 synthetic identities from pseudopeople, half over-merges.
- [fact] On the easier test, Opus 5.5 scored 99.0% at $3.86 per 1,000 identities; Luna 97.3% at $0.10; Jev 95.7% at $0.05 (tuned thresholds).
- [fact] On the harder test (twins, juniors/seniors, same names, noisy typos) Opus fell to 95.1% and the cheap models to about 89%.
- [fact] Jev's confidence was better calibrated than Luna's, so a Jev-then-Opus hybrid (Opus only on 30-90% confidence) reached 98.8% / 95.3% at $0.88 / $2.94 per 1,000, while a Luna hybrid reached 98.5% / 91.6%.
- [inference] The general lesson, which the authors only suspect ("we suspect it's not just useful in this domain"), is that a cheap scorer's calibration decides whether escalation to an expensive model works.

## Locator map

- "What is identity resolution?" and "Detecting over-merging": problem definition, human sampling ~50 identities/hr.
- "The prompt": three-part prompt; error examples helped most.
- Tables under "Picking a confidence threshold": thresholds 60% Jev, 70% Luna.
- "Jev's confidence is better calibrated than Luna's": calibration plots (images not captured in raw).
- "Hybrid evaluator model": escalation-band tables.
- "So, what's the conclusion?": final comparison table across both tests.
