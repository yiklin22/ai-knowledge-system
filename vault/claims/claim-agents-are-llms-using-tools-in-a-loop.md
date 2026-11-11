---
id: clm_v5bmbgcx
schema: 2
type: claim
title: Agents are LLMs using tools in a loop
aliases: []
domains:
- ai
summary: Both Willison and Anthropic describe an agent as tools run in a loop toward a goal.
tags:
- agents
status: reviewed
confidence: medium
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_p79zxlba
  locator: What is agentic engineering?
  quote: Agents run tools in a loop to achieve a goal
- id: src_2hzno5ws
  locator: Agents
  quote: They are typically just LLMs using tools based on environmental feedback in a loop.
relations:
- rel: about
  id: cpt_9ug6lxd3
- rel: about
  id: cpt_mta00ls5
verdict: supported
---

# Agents are LLMs using tools in a loop

## Evidence for
- Willison's accepted definition and Anthropic's description agree. [fact]
- OpenAI's SDK docs describe agents with a built-in loop that continues until the task is complete. [fact] (OpenAI Agents SDK docs)

## Evidence against
- Anthropic notes people use 'agent' for several things and separates fixed workflows from agents. [fact]

## Verdict reasoning
Two independent practitioners and a vendor doc agree on the core definition; the boundary with workflows is a matter of degree. [inference]
