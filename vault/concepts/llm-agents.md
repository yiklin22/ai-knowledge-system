---
id: cpt_9ug6lxd3
schema: 2
type: concept
title: LLM agents
aliases: []
domains:
- ai
summary: Systems where an LLM uses tools in a loop to pursue a goal, from fixed workflows to autonomous coding agents and swarms.
tags:
- curriculum
status: draft
confidence: medium
created: 2026-11-08
updated: '2026-11-08'
sources:
- id: src_p79zxlba
  locator: What is agentic engineering?
  quote: Agents run tools in a loop to achieve a goal
- id: src_2hzno5ws
  locator: What are agents?
  quote: are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.
- id: src_1urar36y
  locator: intro
  quote: which are LLMs equipped with instructions and tools
relations:
- rel: related
  id: cpt_24s5izka
- rel: related
  id: cpt_mta00ls5
- rel: related
  id: cpt_fzs5i5ha
- rel: related
  id: cpt_o7t7o69z
recall:
- q: Give Willison's one-line definition of an agent.
  a: Agents run tools in a loop to achieve a goal.
- q: Why must an agent get 'ground truth' from the environment at each step?
  a: Tool results and code execution tell it whether it is making progress; Anthropic stresses this for plan-and-act loops.
probes:
- q: What separates an agent from a single LLM call with retrieval?
  looks_for: 'The agent loops: it chooses and calls tools, receives results and continues until a goal or stop condition, with the LLM directing the process.'
misconceptions:
- Agents are a fundamentally different kind of model (they are a loop around an ordinary LLM plus tools).
---

# LLM agents

## Knowledge
- An agent is software that calls an LLM with a prompt and tool definitions, runs the tools the LLM asks for, and feeds results back until a goal is met.
- Anthropic separates workflows (predefined code paths) from agents (LLM-directed). OpenAI's SDK treats agents as LLMs with instructions and tools, plus handoffs and guardrails.
- Coding agents add code execution, which lets them iterate towards software that demonstrably works.

## Evidence
- Agents run tools in a loop to achieve a goal. [fact] (Willison, What is agentic engineering?)
- Agents are systems where LLMs dynamically direct their own processes and tool usage; they are typically just LLMs using tools based on environmental feedback in a loop. [fact] (Anthropic, Building effective agents)
- OpenAI's SDK primitives: agents (LLMs with instructions and tools), agents as tools or handoffs, guardrails, plus tracing. [fact] (OpenAI Agents SDK docs; vendor source)
- Anthropic: agents need ground truth from the environment at each step and stopping conditions for control; autonomy raises costs and the risk of compounding errors. [fact] (Anthropic)
- See [[claim-agents-are-llms-using-tools-in-a-loop]].

## Understanding
- Most of an agent's apparent intelligence comes from the model; the harness decides which tools, instructions and context it gets. [inference] (see [[agent-harness]])
- Tool design is a first-class problem: Anthropic spent more time optimising tools than the overall prompt for its SWE-bench agent. [fact] (Anthropic, Appendix 2)

```mermaid
flowchart LR
  G[Goal + system prompt] --> M[LLM]
  M -->|tool call| T[Harness runs tool]
  T -->|result| M
  M -->|final answer| H[Human review]
```

Follow the loop: the model requests a tool, the harness runs it and returns the result, until a final answer.

## Application
- Use agents for open-ended problems with verifiable feedback (such as coding); prefer workflows when steps are known. [inference] (see [[workflows-versus-agents]])
- Add checks, sandboxes and human review for autonomous runs. [fact] (Anthropic recommends extensive sandbox testing and guardrails)

## Uncertainty
- Definitions vary by author and vendor. [fact] (Anthropic notes several definitions)
- This page uses vendor docs and individual practitioners; no controlled studies are in `raw/`. [inference]

## Related
- [[agentic-engineering]] — doing software engineering with agents.
- [[agent-harness]] — the loop's host software.
- [[workflows-versus-agents]] — when to use agents at all.
- [[multi-agent-orchestration]] — several agents together.
- [[tool-use-and-function-calling]] — the mechanism for acting.
