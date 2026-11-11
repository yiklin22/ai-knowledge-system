---
id: src_2hzno5ws
schema: 2
type: source
title: Building effective AI agents (Anthropic)
aliases: []
domains:
- ai
summary: 'Anthropic''s guidance: prefer simple composable patterns, separate workflows from agents, design tools carefully. Carries a note that tooling has changed since Dec 2024.'
tags:
- agents
- vendor
status: reviewed
confidence: medium
created: '2026-11-08'
updated: '2026-11-08'
sources: []
relations: []
kind: web
reliability: vendor
raw: raw/web/2026-11-08-building-effective-ai-agents.md
url: https://www.anthropic.com/engineering/building-effective-agents
author: Anthropic
published: '2024-12-19'
---

# Building effective AI agents (Anthropic)

## Takeaways
- Workflows (predefined code paths) versus agents (LLM-directed); start simple, add complexity only when it helps.
- Five workflow patterns: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer.
- Invest in the agent-computer interface; tool design mattered more than the overall prompt for their SWE-bench agent.
- Vendor source; the page itself says much of the tooling landscape has changed.

## Locator map
Headings: What are agents? · When to use agents · Frameworks · Building blocks, workflows, agents · Summary · Appendix 1 (agents in practice) · Appendix 2 (prompt engineering your tools).
