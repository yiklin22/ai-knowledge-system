---
id: cpt_fzs5i5ha
schema: 2
type: concept
title: Workflows versus agents
aliases:
- agentic systems
domains:
- ai
summary: 'Anthropic''s distinction: workflows follow predefined code paths; agents let the LLM direct its own process and tool use.'
tags:
- agents
status: reviewed
confidence: medium
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_2hzno5ws
  locator: What are agents?
  quote: are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.
- id: src_2hzno5ws
  locator: When (and when not) to use agents
  quote: we recommend finding the simplest solution possible, and only increasing complexity when needed.
- id: src_oovo1ykr
  locator: When (and When Not) to Use Agents?
  quote: Always seek the simplest solution first.
relations:
- rel: part_of
  id: cpt_9ug6lxd3
- rel: prerequisite_for
  id: cpt_o7t7o69z
- rel: related
  id: cpt_ezdgksnt
recall:
- q: What is the architectural difference between a workflow and an agent?
  a: Workflows orchestrate LLMs and tools through predefined code paths; in agents the LLM dynamically directs its own process and tool usage.
- q: What do Anthropic and Schmid advise about when to use agents?
  a: Use the simplest solution that works; agents trade latency and cost for flexibility, so add them only when simpler options fall short.
probes:
- q: You know the exact steps for a task. Workflow or agent, and why?
  looks_for: 'A workflow or even a script: predictable, cheaper and easier to debug; agents are for open-ended problems where the number of steps cannot be predicted.'
misconceptions:
- Anything that calls an LLM with tools is an agent (Anthropic reserves 'agent' for LLM-directed control; it calls both agentic systems).
---

# Workflows versus agents

## Knowledge
- Anthropic groups both under "agentic systems" but distinguishes workflows (predefined code paths) from agents (LLM-directed).
- Advice from Anthropic and Schmid: start with the simplest solution, add complexity only when it demonstrably helps.

## Evidence
- Workflows orchestrate LLMs and tools through predefined code paths; agents dynamically direct their own processes and tool use. [fact] (Anthropic, Building effective agents)
- Anthropic recommends the simplest solution possible, increasing complexity only when needed; agentic systems often trade latency and cost for better task performance. [fact] (Anthropic)
- Agents are "typically just LLMs using tools based on environmental feedback in a loop", and suit open-ended problems where steps cannot be predicted. [fact] (Anthropic)
- Schmid: always seek the simplest solution first, and use workflows for predictability, agents for flexibility. [fact] (Schmid)
- Anthropic warns frameworks add abstraction layers that can obscure prompts and responses and recommends starting with direct API calls. [fact] (Anthropic)

## Understanding
- The core trade-off is predictability and cost against flexibility; autonomy brings compounding errors. [fact] (Anthropic notes higher costs and potential for compounding errors)
- The line is a spectrum in practice, since real systems mix fixed steps with model-chosen ones. [inference]

## Application
- Default to a single well-prompted call, then a workflow, then an agent. [inference] (consistent with both sources)
- Anthropic's note says much of the tooling in the post has changed since Dec 2024; check current guidance. [fact] (Anthropic, page note)

## Uncertainty
- The post is vendor guidance, dated Dec 2024, and itself flags that parts are outdated. [fact] (Anthropic note)
- Where the right boundary lies for newer models is unsettled; see [[when-does-a-single-agent-beat-multiple-subagents]]. [inference]

## Related
- [[agentic-workflow-patterns]] — the workflow patterns catalogue.
- [[multi-agent-orchestration]] — when many agents are used.
- [[llm-agents]] — the broader topic.
