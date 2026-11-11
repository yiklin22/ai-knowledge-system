---
id: cpt_r0y15j1d
schema: 2
type: concept
title: "The agent loop (think, act, observe)"
aliases: [ReAct loop, think-act-observe]
domains: [ai]
summary: "The core mechanism of an agent: the LLM reasons about the next step, calls a tool, reads the result and repeats until it can answer; the three parts are the model, the tools and the memory/state."
tags: [agents, react, loop]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources:
  - id: src_wlpdy4uq
    locator: "How AI Agents Actually Work"
    quote: "The agent loops between reasoning and executing until it has what it needs."
  - id: src_ixuklw02
    locator: "Where to Next / prerequisite note"
    quote: null
relations:
  - {rel: broader, id: cpt_9ug6lxd3}
  - {rel: prerequisite_for, id: cpt_qlqrjynu}
  - {rel: prerequisite_for, id: cpt_eripv7vv}
  - {rel: related, id: cpt_fzs5i5ha}
  - {rel: related, id: cpt_mta00ls5}
recall:
  - q: What are the three steps of the agent loop and what are its three components?
    a: "Think (reason about the next step), Act (call a tool), Observe (read the result), repeat. Components: the LLM brain, the tools, and the memory/state of what has been done."
  - q: Why does an LLM alone fail at "refund order 4821"?
    a: It has no live data, cannot take actions, and cannot chain multi-step operations; it can only produce text, so it may hallucinate that the refund happened.
  - q: What does function calling have to do with the loop?
    a: "It is the mechanism behind the Act step: the model emits a structured tool call, your code runs it, and the result is observed."
probes:
  - q: A chatbot says it processed your refund but nothing happened. Where in the loop is it missing something?
    looks_for: "Recognises there is no Act/Observe step (no tool), so the model generates a plausible sentence instead of executing and checking a result."
misconceptions:
  - An agent is a smarter model (it is the same LLM given tools and a loop).
  - The loop is complicated code (the loop itself is a few lines; error handling, auth and permissions are the bulk).
---

# The agent loop (think, act, observe)

## Knowledge
- An agent puts an LLM in a loop: think about the goal, act by calling a tool, observe the result, and repeat until it can answer. [fact] (src_wlpdy4uq)
- The loop is named ReAct (Reasoning + Acting) after Yao et al.; the source says LangChain, LlamaIndex, CrewAI and the OpenAI Assistants API all implement a variation. [fact] (src_wlpdy4uq)
- Three components: the LLM (every step is a decision, so weaker models spiral), the tools (the agent only reads their descriptions), and memory/state (what has been looked up so far). [fact] (src_wlpdy4uq)
- Function calling is the "act" mechanism within the loop. [fact] (src_ixuklw02)
- The author says ChatGPT's web browsing and code running are an agent layer over the base LLM. [fact] (src_wlpdy4uq)

## Evidence
- Worked example in the source: two tool calls (order lookup, then refund) complete one task. [fact] (src_wlpdy4uq)
- Coding agents (Copilot, Cursor, Claude Code) are described as the same loop with file, terminal and test tools. [fact] (src_wlpdy4uq; not independently verified)

## Understanding
- The agent adds agency, not intelligence: the reasoning was already in the model; the loop lets it act on and verify against the world. [inference] (resting on the source's framing)
- Because each step is a model decision, per-step reliability matters more for agents than for chatbots; see [[per-step-error-compounds-across-an-agent-workflow]]. [inference]

## Application
- Use a loop when the next action depends on the previous result; for predictable sequences a fixed workflow may be cheaper (see [[workflows-versus-agents]]). [inference]
- Write precise tool descriptions: the source says vague ones lead to hallucinated tool calls. [fact] (src_wlpdy4uq)

## Uncertainty
- The source's "agent" is a broad definition; other sources in the vault distinguish workflows from agents. [inference]
- Adoption and reliability statistics in the source are second-hand. [fact] (src_wlpdy4uq)

## Related
- [[llm-agents]], [[tool-use-and-function-calling]], [[single-agent-reasoning-patterns]], [[agent-harness]]
