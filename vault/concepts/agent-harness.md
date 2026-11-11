---
id: cpt_mta00ls5
schema: 2
type: concept
title: Agent harness
aliases:
- coding agent harness
domains:
- ai
summary: The software around an LLM that supplies the system prompt, tools and loop, turning a model into an agent.
tags:
- agents
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_qu8mtfb9
  locator: How coding agents work
  quote: extending that LLM with additional capabilities that are powered by invisible prompts and implemented as callable tools.
- id: src_qu8mtfb9
  locator: Calling tools
  quote: A tool is a function that the agent harness makes available to the LLM.
- id: src_qu8mtfb9
  locator: Large Language Models
  quote: null
relations:
- rel: part_of
  id: cpt_9ug6lxd3
- rel: prerequisite_for
  id: cpt_24s5izka
- rel: related
  id: ent_7kkj45y4
recall:
- q: What are the three ingredients Willison says make up a coding agent?
  a: An LLM, a system prompt, and tools, run in a loop by the harness.
- q: Why are LLMs described as stateless, and what does the harness do about it?
  a: Each prompt starts from a blank slate, so the harness keeps state and replays the whole conversation each turn.
probes:
- q: Why does a long conversation get more expensive each turn, and how do harnesses soften this?
  looks_for: The whole conversation is resent each turn so input tokens grow; providers charge less for cached input prefixes, so harnesses avoid editing earlier content.
misconceptions:
- The model remembers earlier turns by itself (it is stateless; the harness replays context).
---

# Agent harness

## Knowledge
- A coding agent is software acting as a harness for an LLM, adding capabilities through invisible prompts and callable tools.
- Core mechanics: LLM, system prompt, tools, loop. A simple tool loop is a few dozen lines on top of an LLM API; a good one is much more work.

## Evidence
- A harness extends the LLM with capabilities powered by invisible prompts and implemented as callable tools. [fact] (Willison, How coding agents work)
- LLMs are stateless, so the harness replays the conversation every turn; providers discount cached input tokens, so agents avoid modifying earlier content. [fact] (Willison)
- The harness extracts a requested tool call from the model's response, runs it, and feeds the result back. [fact] (Willison, Calling tools)
- System prompts can be hundreds of lines long; reasoning effort is often adjustable. [fact] (Willison)
- Amjad (quoting Anthropic) says every harness component encodes an assumption about what the model cannot do alone, and these assumptions go stale as models improve. [fact] (Amjad loops video, 11:47; second-hand)

## Understanding
- Because the model only sees text, everything an agent "knows" or "does" is mediated by what the harness puts in the context and which tools it exposes. [inference]
- This is why harness changes (instructions, tools, hooks) can change behaviour without any change to the model. [inference]

## Application
- Building a toy harness is a good way to learn how agents work. [fact] (Willison suggests this)
- Review harness assumptions when a new model ships; some scaffolding may become unnecessary. [inference] (rests on the Amjad/Anthropic quote)

## Uncertainty
- The "assumptions go stale" claim is second-hand (a video quoting an Anthropic article not in `raw/`). [inference] See [[which-agent-harness-components-become-unnecessary-as-models-improve]].

## Related
- [[llm-agents]] — what a harness enables.
- [[context-window-and-compaction]] — what the harness manages.
- [[claude-code]] — an example harness.
