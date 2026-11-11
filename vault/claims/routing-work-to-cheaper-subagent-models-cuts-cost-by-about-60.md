---
id: clm_3idqb7tq
schema: 2
type: claim
title: "Routing work to cheaper subagent models cuts cost by about 60%"
aliases: []
domains: [ai]
summary: "Moksa claims that sending planning to a large model, coding to a mid-size one and search to a small one cuts token cost about 60%; the figure comes from the author's own illustrative example."
tags: [subagents, cost, volatile]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_c9pkl2fk
    locator: "Example 6"
    quote: "Total: $1.60 vs $4 (60% saving)"
relations:
  - {rel: about, id: cpt_o7t7o69z}
  - {rel: about, id: cpt_zx4myv3t}
  - {rel: related, id: qst_qziu6482}
  - {rel: related, id: clm_g473l8as}
verdict: unverified
volatile: true
last_verified: 2026-11-08
---

# Routing work to cheaper subagent models cuts cost by about 60%

Statement: assigning tasks to subagents on models matched to difficulty (large for architecture, mid-size for implementation, small for search and logs) cuts total cost by about 60% compared with doing everything in one large-model session.

## Evidence for
- The Moksa example estimates $1.60 against $4, a 60% saving, for a typical feature; the same article says Reddit-observed users spend 60-70% fewer tokens. [fact] (Moksa, example 6 and section 1; blog)
- The built-in Explore subagent runs on a small model so large file searches stay out of the main context. [fact] (Moksa, section 2)

## Evidence against
- The $4 and $1.60 figures are the author's illustrative estimates in code comments, with no measurements; the article itself warns cost can go up if models are chosen wrongly. [fact] (Moksa, example 6 and section 5)
- The vault's existing page on subagent decomposition records that sources disagree about when delegation helps, and Anthropic docs warn that models may spawn subagents when a direct search would do. [fact] (existing vault pages; Prompting best practices)
- Model names and prices in the examples are outdated generations. [inference]

## Verdict reasoning
- Unverified: plausible mechanism (cheaper models for easy work, isolated context) but no data; do not cite the 60% figure as evidence. [inference]
