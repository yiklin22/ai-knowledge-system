---
id: clm_f1puv7l8
schema: 2
type: claim
title: Agents given similar context make similar decisions, so single errors can replicate
aliases: []
domains:
- ai
summary: Anthropic's experiments show many agents making the same choices, including bad ones.
tags:
- agents
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_8tz2b8u3
  locator: Failures from conformity
  quote: when one agent makes a bad decision, it is likely that many agents will make that same bad decision
- id: src_8tz2b8u3
  locator: Failures from conformity
  quote: 18 out of 30 agents decided to create a git branch with the exact same branch name
relations:
- rel: about
  id: cpt_5s6mnu9b
verdict: supported
---

# Agents given similar context make similar decisions, so single errors can replicate

## Evidence for
- Examples: same branch names, same story titles, same strategy defections, job-queue flooding (2.4 million requests, 117 accepted). [fact]

## Evidence against
- Anthropic expects real-world agents to be higher variance because they will have different contexts and not all be Claude. [fact]

## Verdict reasoning
Well illustrated by the authors' own experiments, but all on Anthropic's models and not independently replicated. [inference]
