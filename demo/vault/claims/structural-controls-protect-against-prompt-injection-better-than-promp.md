---
id: clm_migp1fx2
schema: 2
type: claim
title: Structural controls protect against prompt injection better than prompt wording
aliases: []
domains:
- ai
summary: The project's security document holds that removing tools, confining writes and requiring human approval matter more than how the prompt is phrased.
tags:
- security
status: draft
confidence: low
created: 2026-11-11
updated: 2026-11-11
sources:
- id: src_vs3k1ezx
  locator: Known limits (honest list)
  quote: The strongest controls are structural (no tools in Ask, write confinement, human approval), not the wording of prompts.
relations:
- rel: about
  id: cpt_h8ptu3ln
- rel: about
  id: cpt_5wlbt92q
verdict: unverified
---

# Structural controls protect against prompt injection better than prompt wording

## Evidence for
- [fact] The security document states this as its position.
- [inference] A capability that is absent cannot be misused, whatever the model is persuaded of.

## Evidence against
- [inference] The source is the system's own documentation and reports no experiment comparing the two kinds of control.

## Verdict reasoning
A reasoned design position from a single primary source, with no measurement. Left `unverified`.
