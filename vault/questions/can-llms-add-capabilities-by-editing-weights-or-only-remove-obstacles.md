---
id: qst_1yx5dqtj
schema: 2
type: question
title: "Can LLMs add capabilities by editing weights, or only remove obstacles?"
aliases: []
domains: [ai]
summary: "The weight-space programming post fixed a looping failure but could not improve a non-looping model; whether weight editing can add ability is open."
tags: [weights, interpretability]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: related, id: cpt_mp49wsbo}
  - {rel: related, id: clm_1vhrxjud}
state: open
---

# Can LLMs add capabilities by editing weights, or only remove obstacles?

## Why I'm asking
- The Qwen result looks like a large capability jump but the authors say the edit only removed an obstacle; the Gemma result shows no gain. If editing can only unblock, the approach is a debugging tool, not a training replacement.

## What would answer it
- Replication on more models and tasks with failures other than loops.
- Comparisons with simple baselines such as steering-vector subtraction or a few gradient steps.
- Larger models where the LLM needs tools to read the weights, which the authors say they are building a benchmark for.
