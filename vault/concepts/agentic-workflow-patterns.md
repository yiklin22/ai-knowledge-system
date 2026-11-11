---
id: cpt_ezdgksnt
schema: 2
type: concept
title: Agentic workflow patterns
aliases:
- agent design patterns
domains:
- ai
summary: 'Reusable designs: prompt chaining, routing, parallelization, orchestrator-workers and evaluator-optimizer (reflection).'
tags:
- agents
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_2hzno5ws
  locator: Building blocks, workflows, and agents
  quote: Prompt chaining decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one.
- id: src_oovo1ykr
  locator: 'Workflow: Routing'
  quote: null
- id: src_oovo1ykr
  locator: Reflection Pattern
  quote: null
relations:
- rel: related
  id: cpt_fzs5i5ha
- rel: part_of
  id: cpt_9ug6lxd3
recall:
- q: Name Anthropic's five workflow patterns.
  a: Prompt chaining, routing, parallelization (sectioning and voting), orchestrator-workers, evaluator-optimizer.
- q: How does orchestrator-workers differ from parallelization?
  a: Same topology, but subtasks are not predefined; a central LLM decides them based on the input.
probes:
- q: A task needs a code change across an unpredictable number of files. Which pattern fits and why?
  looks_for: 'Orchestrator-workers: a central LLM decomposes dynamically and delegates, unlike fixed parallel sectioning.'
---

# Agentic workflow patterns

## Knowledge
- Prompt chaining: fixed sequence of LLM steps, optionally with checks (gates).
- Routing: classify an input and send it to a specialised follow-up.
- Parallelization: sectioning (independent subtasks) or voting (repeated attempts).
- Orchestrator-workers: a central LLM breaks tasks down, delegates and synthesises.
- Evaluator-optimizer: one call generates, another critiques, in a loop (Schmid calls it the reflection pattern).

## Evidence
- Anthropic describes all five patterns with use cases and when to use each. [fact] (Anthropic, Building effective agents)
- Prompt chaining trades latency for accuracy by making each call easier. [fact] (Anthropic)
- Orchestrator-workers suits tasks where the subtasks cannot be predicted, such as multi-file code changes. [fact] (Anthropic)
- Evaluator-optimizer fits when criteria are clear and iterative refinement adds measurable value. [fact] (Anthropic)
- Schmid lists three workflow patterns and four agentic patterns (reflection, tool use, planning/orchestrator-workers and more) built from raw API calls. [fact] (Schmid)

## Understanding
- These are building blocks to combine and customise, and Anthropic says to add complexity only when it improves measured outcomes. [fact] (Anthropic)
- Different sources name the same patterns differently (evaluator-optimizer versus reflection; planning versus orchestrator-workers). [inference]

## Application
- Pick the pattern from the shape of the task: fixed steps (chain), distinct categories (route), independent parts (parallel), unknown parts (orchestrator-workers), clear quality criteria (evaluator-optimizer). [inference]

## Uncertainty
- Newer models may make some patterns unnecessary; see [[which-agent-harness-components-become-unnecessary-as-models-improve]]. [inference]

## Related
- [[workflows-versus-agents]] — when to use patterns versus agents.
- [[multi-agent-orchestration]] — larger structures built from these.
