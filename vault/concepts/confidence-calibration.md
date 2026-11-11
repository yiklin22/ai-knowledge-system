---
id: cpt_rjqiu953
schema: 2
type: concept
title: "Confidence calibration"
aliases: [calibrated confidence]
domains: [ai]
summary: A model is calibrated when the confidence it reports matches how often it is right, so low-confidence answers are the likely mistakes and can be routed to review.
tags: [calibration, evaluation]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_x1ew5c1z
    locator: "So, what's the conclusion?"
    quote: "Calibration matters! Whereas Luna works better out of the box, its overconfidence prevents success on harder datasets."
relations:
  - {rel: prerequisite_for, id: cpt_i243o4zy}
  - {rel: related, id: cpt_98mq6mw6}
  - {rel: related, id: cpt_1dk2t19q}
recall:
  - {q: "What does it mean for a classifier to be well calibrated?", a: "Among answers given with confidence p, about a fraction p are correct; its mistakes cluster at low confidence."}
  - {q: "Why does calibration matter more than raw accuracy when escalating to a stronger model?", a: "Escalation picks cases by confidence; if errors are confident, they never get escalated."}
probes:
  - {q: "Model A is 97% accurate but wrong answers come with 95% confidence; model B is 95% accurate and wrong answers sit near 50%. Which do you put in front of an expensive reviewer, and why?", looks_for: "Chooses B: its uncertainty flags its errors so a confidence band catches them; A's errors are invisible."}
misconceptions:
  - "The more accurate model out of the box is always the better first stage of a cascade."
  - "A 50% threshold is a natural, optimal cutoff for any confidence score."
---

# Confidence calibration

## Knowledge

- [fact] In the Hightouch experiment, most of Jev's mistakes had confidence near 50%, "what you'd expect out of a well-calibrated model", while Luna was overconfident in the 90-100% bucket (src_x1ew5c1z, calibration section).
- [fact] The best cutoff differed: 60% for Jev, 70% for Luna; the cutoff mattered a lot for Jev and very little for Luna.
- [inference] Reported confidence is only useful as a routing signal if errors concentrate at low confidence.

## Evidence

- [fact] Single vendor experiment on 1,000 synthetic identities; calibration plots were images not preserved in the raw file, so the bucket claims rest on the authors' prose. See [[calibration-not-out-of-box-accuracy-determines-hybrid-judge-performanc]].

## Understanding

- [inference] A cascade sends uncertain cases to a stronger judge. A confident-but-wrong cheap model removes exactly the cases that most need review.

## Application

- Check a cheap scorer's calibration (error rate per confidence bucket) on your own data before using it as a gate; tune the threshold rather than defaulting to 50%.

## Uncertainty

- [speculation] Calibration may shift with difficulty: the post notes Jev's confidence "incorrectly shifts higher" on harder cases while staying better than Luna's.
- [inference] This page rests on one source; confidence stays low.

## Related

[[confidence-gated-hybrid-judge-cheap-model-then-frontier]], [[decision-models-confidence-score-models]], [[evaluating-llms]]
