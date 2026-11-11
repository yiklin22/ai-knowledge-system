---
id: cpt_i243o4zy
schema: 2
type: concept
title: "Confidence-gated hybrid judge (cheap model, then frontier)"
aliases: [LLM cascade, hybrid evaluator, second-opinion routing]
domains: [ai]
summary: Run a cheap confidence-scoring model on every item and escalate only items whose score falls in an uncertain band to an expensive frontier model, trading a little accuracy for much lower cost.
tags: [llm-judge, cascade, cost]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_x1ew5c1z
    locator: "Hybrid evaluator model"
    quote: null
relations:
  - {rel: related, id: cpt_1dk2t19q}
  - {rel: related, id: cpt_98mq6mw6}
  - {rel: related, id: cpt_rjqiu953}
  - {rel: related, unresolved: "Agentic workflow patterns (routing)"}
volatile: true
last_verified: 2026-11-08
recall:
  - {q: "How does a confidence-gated hybrid judge work?", a: "A cheap model scores every item; only items with confidence in an uncertain band go to an expensive model for a second opinion."}
  - {q: "What knob sets the cost/accuracy trade-off in this hybrid?", a: "The width of the escalation band (e.g. 30-90% vs 50-80%)."}
  - {q: "Why did the Jev hybrid hold up on harder data without any change?", a: "Its confidence shifted toward uncertainty, so more cases fell in the band and were escalated automatically."}
probes:
  - {q: "Your cheap judge's error rate is high on a new dataset. What happens to cost and accuracy of the cascade, and why?", looks_for: "Understands that a calibrated gate escalates more, raising cost but protecting accuracy; an overconfident gate does not."}
misconceptions:
  - "A hybrid is only as good as its cheap model's accuracy."
---

# Confidence-gated hybrid judge (cheap model, then frontier)

## Knowledge

- [fact] Hightouch tested "Jev first, then Opus" and "Luna first, then Opus" with different escalation bands (src_x1ew5c1z, "Hybrid evaluator model").
- [fact] Easier test: Jev + Opus on 30-90% confidence sent 22% of cases to Opus and reached 98.8% accuracy at $0.88 per 1,000, versus Opus alone 99.0% at $3.86. Luna + Opus on 10-90% sent 6% and reached 98.5% at $0.33.
- [fact] Harder test: Opus alone 95.1% ($5.39); Jev hybrid 95.3% ($2.94); Luna hybrid 91.6% ($1.15).

## Evidence

- [fact] Table "Harder test results" and the final comparison table in the source. See [[a-jev-then-opus-hybrid-matches-opus-accuracy-at-over-4x-lower-cost]] and [[calibration-not-out-of-box-accuracy-determines-hybrid-judge-performanc]].
- [fact] Vendor-measured, single benchmark; see source reliability.

## Understanding

```mermaid
flowchart LR
  R[Record set] --> C[Cheap decision model: confidence]
  C -->|confident, outside band| D[Accept verdict]
  C -->|uncertain, inside band| F[Frontier model second opinion]
  F --> D
```

- [inference] Cost scales with the share escalated, so spend rises automatically when the data are harder, provided the gate is calibrated ([[confidence-calibration]]).
- [inference] The band is the tuning knob; the authors note thresholds could be narrowed to cut cost at some accuracy loss.

## Application

- Use when a cheap scorer exists, a trustworthy expensive judge exists, and volume makes the expensive one costly (for example auditing samples of 100,000 identities).
- Not worth it if the cheap model's errors are confident, or if the expensive model is itself unreliable on the task.

## Uncertainty

- [speculation] The authors "suspect it's not just useful in this domain"; untested here. See [[does-the-hybrid-cascade-generalise-beyond-identity-resolution]].
- [inference] Band choices were picked after seeing results on the same data (risk of overfitting thresholds).

## Related

[[confidence-calibration]], [[decision-models-confidence-score-models]], [[identity-resolution-and-over-merging]], [[evaluating-llms]]
