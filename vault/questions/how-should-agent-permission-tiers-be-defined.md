---
id: qst_k0oghhcy
schema: 2
type: question
title: "How should agent permission tiers be defined?"
aliases: []
domains: [ai]
summary: "Two sources propose read/write/destructive tiers with human approval for destructive actions; how do you classify actions that are write-only but hard to reverse, such as send or publish?"
tags: [agents, permissions, guardrails]
status: reviewed
confidence: low
created: 2026-11-10
updated: 2026-11-10
sources: []
relations:
  - {rel: about, id: cpt_od52gsyk}
  - {rel: about, id: cpt_g1vxdqj6}
state: open
---

# How should agent permission tiers be defined?

## Why I'm asking
src_ieap5jak proposes autonomous reads, logged writes and approved destructive actions, and also lists "send, publish, charge" as needing approval; src_98ddhon2 adds that credential scope is the real boundary. The boundary between tiers is left informal.

## What would answer it
- A source defining reversibility and blast radius criteria per action.
- Examples of tiering applied to real tool sets, including the cost of approval fatigue.
