---
id: qst_2wztspil
schema: 2
type: question
title: "How can deceptive behaviour be found if safety training can hide it?"
aliases: []
domains: [ai]
summary: "If backdoors can survive and even be hidden by safety training, what detection methods other than behavioural testing work?"
tags: [safety, deception, detection]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: related, id: cpt_87ju9tu3}
  - {rel: related, id: clm_m0q45qmc}
  - {rel: related, id: cpt_hrzo5jmc}
  - {rel: related, id: cpt_f92yye3m}
state: open
---

# How can deceptive behaviour be found if safety training can hide it?

## Why I'm asking
- The sleeper-agent abstract says standard techniques may give a false impression of safety; agent security guidance (OWASP) lists rogue agents and backdoors as risks, and Willison reports training-time break-outs.

## What would answer it
- The full sleeper-agents paper, to see what detection or probing methods it tests.
- Interpretability work on detecting triggers (the weight-space post suggests LLM-assisted weight reading as one route; it did not detect a sycophant from weights alone).
- Primary reports on the reported training break-outs and how they were found (independent researchers, per Willison).
