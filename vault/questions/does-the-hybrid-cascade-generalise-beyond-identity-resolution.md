---
id: qst_dcv5gh6i
schema: 2
type: question
title: "Does the hybrid cascade generalise beyond identity resolution?"
aliases: []
domains: [ai]
summary: Does a calibrated cheap scorer gating a frontier model cut cost without losing accuracy on other LLM-judge tasks, and how should one check calibration first?
tags: [llm-judge, cascade]
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
  - {rel: related, id: qst_2wilgfwk}
state: open
---

# Does the hybrid cascade generalise beyond identity resolution?

## Why I'm asking

The authors say they "suspect it's not just useful in this domain" but tested only over-merge detection on synthetic data with two cheap models. Related to the vault's open question on LLM-as-judge reliability.

## What would answer it

Independent replications on other judging tasks (summary grading, code review), with calibration measured per bucket and bands chosen on held-out data. Also open: behaviour with open-weight decision models, which the authors plan to cover.
