---
id: src_qu8mtfb9
schema: 2
type: source
title: How coding agents work (Simon Willison)
aliases: []
domains:
- ai
summary: 'Explains a coding agent as an LLM plus system prompt plus tools in a loop: statelessness, replayed context, token caching, tool calls, reasoning.'
tags:
- agents
status: reviewed
confidence: medium
created: '2026-11-08'
updated: '2026-11-08'
sources: []
relations: []
kind: web
reliability: secondary
raw: raw/web/2026-11-08-how-coding-agents-work-agentic-engineering-patterns.md
url: https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/
author: Simon Willison
published: 2026 (page date unclear)
---

# How coding agents work (Simon Willison)

## Takeaways
- LLMs are stateless; the harness replays the whole conversation each turn, so cost grows and caching matters.
- Tools are functions the harness exposes; the harness parses calls and returns results.
- System prompts and reasoning effort are further harness features.

## Locator map
Sections: Large Language Models · Chat templated prompts · Token caching · Calling tools · The system prompt · Reasoning · LLM + system prompt + tools in a loop.
