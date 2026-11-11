---
id: cpt_z148c3qf
schema: 2
type: concept
title: Software 3.0
aliases:
- Software 3.0 (Karpathy)
domains:
- ai
summary: 'Karpathy''s framing: after explicit code and learned weights, programming becomes prompting the context window of an LLM.'
tags:
- agents
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_i6bjtiga
  locator: 03:12
  quote: your programming now turns to prompting and what's in the context window is your lever over the interpreter that is the LLM
- id: src_i6bjtiga
  locator: 03:44-06:47
  quote: null
relations:
- rel: related
  id: cpt_be51ajjr
- rel: related
  id: cpt_24s5izka
- rel: introduced_in
  id: ent_a8uhtyvi
recall:
- q: How does Karpathy define Software 1.0, 2.0 and 3.0?
  a: '1.0: writing explicit code. 2.0: programming via datasets and trained neural networks. 3.0: programming by prompting, where the context window is the lever over the LLM acting as interpreter.'
probes:
- q: Karpathy says an app he built (MenuGen) 'shouldn't exist'. What does that example illustrate?
  looks_for: Work done in the old paradigm (OCR plus image generation plus an app) can be replaced by giving a photo and a prompt to a model; Software 3.0 enables new things, not just faster old ones.
---

# Software 3.0

## Knowledge
- Software 1.0: write code. 2.0: program by creating datasets and training networks. 3.0: program by prompting; the context window is the lever over the LLM as interpreter.

## Evidence
- Karpathy gives this three-way definition in the Sequoia interview. [fact] (Karpathy talk, 02:40-03:12)
- Example 1: installing an agent tool by pasting text into an agent rather than running a shell script. [fact] (Karpathy talk, 03:42-04:44)
- Example 2: MenuGen; the app was unnecessary once a multimodal model could overlay items directly. [fact] (Karpathy talk, 04:44-06:47)
- He also describes LLM-built knowledge bases as something that could not exist before because no code could create a knowledge base from facts. [fact] (Karpathy talk, 06:47; see [[andrej-karpathy]])

## Understanding
- The point is not faster code but new kinds of tasks: general information processing is now automatable. [fact] (Karpathy's stated view)
- Karpathy's framing is an interpretation by one author; it is not a technical definition. [inference]

## Application
- Ask "what text would I hand an agent?" instead of "what script would I write?". [fact] (paraphrase of Karpathy's example)

## Uncertainty
- Spoken interview; claims are the speaker's opinions and demonstrations, not measurements. [inference]

## Related
- [[agentic-engineering]] — the professional discipline built on it.
- [[prompt-engineering]] — the skill of shaping context.
