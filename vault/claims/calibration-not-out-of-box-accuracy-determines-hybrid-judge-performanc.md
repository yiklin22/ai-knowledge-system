---
id: clm_6zpsrg7m
schema: 2
type: claim
title: "Calibration, not out-of-box accuracy, determines hybrid judge performance"
aliases: []
domains: [ai]
summary: Hightouch argues that the cheap model with better-calibrated confidence (Jev) makes the better first stage of a hybrid even though Luna is more accurate alone.
tags: [calibration, llm-judge, vendor-claim]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_x1ew5c1z
    locator: "So, what's the conclusion?"
    quote: "Calibration matters! Whereas Luna works better out of the box, its overconfidence prevents success on harder datasets."
relations:
  - {rel: about, id: cpt_rjqiu953}
  - {rel: about, id: cpt_i243o4zy}
verdict: unverified
---

# Calibration, not out-of-box accuracy, determines hybrid judge performance

## Evidence for

- [fact] Easier test alone: Luna 97.3% vs Jev 95.7%; harder test alone: Jev 89.1% vs Luna 88.8%.
- [fact] Hybrid on the harder test: Jev+Opus 95.3% vs Luna+Opus 91.6%, despite Luna's lead on the easier test.
- [fact] Authors report Jev's errors cluster near 50% confidence while Luna's cluster at 90-100%.

## Evidence against

- [inference] Only two cheap models and one task. Other differences (escalation bands: Jev 30-90%, Luna 10-90%; share escalated 22% vs 6%) also differ between arms, so calibration is not isolated as the cause.
- [inference] The calibration plots are not in the raw file, so the calibration description cannot be checked here.

## Verdict reasoning

[inference] A coherent mechanism, consistent with the tables, but confounded by different bands and share escalated. Unverified.
