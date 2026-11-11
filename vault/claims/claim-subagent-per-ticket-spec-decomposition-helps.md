---
id: clm_zj3twix4
schema: 2
type: claim
title: Splitting a spec into tickets run by separate subagents improves results
aliases: []
domains:
- ai
summary: 'Contested: said to help older models but be unnecessary or harmful for newer ones.'
tags:
- agents
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_8s1mxx4c
  locator: 03:44
  quote: are actually overusing subagents when a single agent would have done a better job instead
- id: src_kp4s3ioh
  locator: Know what subagents cost
  quote: What they cost you is mostly tokens, since every subagent sends its own requests and they count against the same usage as your main conversation.
relations:
- rel: about
  id: cpt_o7t7o69z
verdict: contested
---

# Splitting a spec into tickets run by separate subagents improves results

## Evidence for
- Claude Code docs list real benefits of subagents: parallelism, isolating long output and fresh reviewers. [fact] (docs do not endorse ticket-splitting specifically)

## Evidence against
- Amjad says tickets for subagents can be tangled in unexpected ways and cites an Anthropic article saying such decomposition helped older models but not newer ones; that article is not in `raw/`. [fact] (second-hand)
- Docs: subagents cost tokens and can be slower than working in the main session. [fact]

## Verdict reasoning
Marked contested and low confidence: the claim against it is second-hand from a course seller, and no controlled comparison is in `raw/`. [inference]
