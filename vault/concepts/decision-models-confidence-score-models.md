---
id: cpt_98mq6mw6
schema: 2
type: concept
title: "Decision models (confidence-score models)"
aliases: [System One models, decision models]
domains: [ai]
summary: A newer class of language models that return a 0-1 confidence that a stated condition is true, much faster and cheaper than frontier models but less accurate on hard cases.
tags: [llm-judge, cost, latency]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_x1ew5c1z
    locator: "Detecting over-merging"
    quote: null
  - id: src_x1ew5c1z
    locator: "Hybrid evaluator model"
    quote: null
relations:
  - {rel: related, id: cpt_rjqiu953}
  - {rel: related, id: cpt_1dk2t19q}
  - {rel: prerequisite_for, id: cpt_i243o4zy}
  - {rel: related, unresolved: "Jev"}
  - {rel: related, unresolved: "GPT-6 Luna"}
volatile: true
last_verified: 2026-11-08
recall:
  - {q: "What does a decision model output, compared with a chat LLM?", a: "A 0-1 confidence that a specific condition is true, rather than free text."}
  - {q: "Trade-off of decision models versus frontier models in the Hightouch test?", a: "Far cheaper and faster (about $0.05-0.10 per 1,000 judgments, ~0.15 s) but about 6 points less accurate on harder cases."}
misconceptions:
  - "Decision models are just smaller chat models with the same behaviour."
---

# Decision models (confidence-score models)

## Knowledge

- [fact] Hightouch describes Jev and GPT-6 Luna (Decisions API) as "members of a new class of language models that return a 0-1 confidence score that a specific condition is true" (src_x1ew5c1z, "Detecting over-merging").
- [fact] Vendor-measured as of 2026-11-04: $0.05-0.10 per 1,000 identities and about 0.15 s each, versus $3.86 and 2.2 s for Opus 5.5 on the same task.
- [fact] Accuracy: 88.8-97.3% out of the box, trailing Opus by about 6 points on harder benchmarks.

## Evidence

- [fact] Authors: "Decision models are up to 90× cheaper and more than 10× faster out of the box." (src_x1ew5c1z, intro; vendor-measured.)
- [fact] Prompt context about data sources helped frontier models by at most a point and did not help decision models; the authors guess these models "don't really reason" (their guess).

## Understanding

- [inference] Because the output is a score, the threshold becomes a tunable error trade-off and a routing signal for escalation.

## Application

- High-volume yes/no judgments where an occasional miss is tolerable, or as the first stage of [[confidence-gated-hybrid-judge-cheap-model-then-frontier]].

## Uncertainty

- [inference] Only two such models tested, one task, one vendor; prices and model versions will change.
- [inference] I could not verify what Jev and Luna are beyond Hightouch's description.

## Related

[[confidence-calibration]], [[evaluating-llms]]
