---
id: clm_pdp2tu9p
schema: 2
type: claim
title: Hooks enforce rules deterministically while CLAUDE.md instructions are followed at the model's discretion
aliases: []
domains:
- ai
summary: Claude Code docs distinguish model-decided instructions from harness-executed ones.
tags:
- agents
status: reviewed
confidence: medium
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_kp4s3ioh
  locator: Deterministic and non-deterministic instructions
  quote: you configure the instruction, and Claude Code (the harness) *has* to execute this.
- id: src_kp4s3ioh
  locator: Deterministic and non-deterministic instructions
  quote: no matter what the model decided to do.
relations:
- rel: about
  id: cpt_5tf19c1o
verdict: supported
---

# Hooks enforce rules deterministically while CLAUDE.md instructions are followed at the model's discretion

## Evidence for
- The docs state it directly and give Stop hooks, deny rules and managed settings as the deterministic forms. [fact]

## Evidence against
- None recorded; this is a vendor's description of its own product. [inference]

## Verdict reasoning
A design fact about one product's documented behaviour; the broader point (hard rules belong in the harness) is an inference. [inference]
