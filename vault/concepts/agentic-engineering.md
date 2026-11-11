---
id: cpt_24s5izka
schema: 2
type: concept
title: Agentic engineering
aliases:
- agentic coding
domains:
- ai
summary: 'Developing software with coding agents while keeping professional quality: specifying, verifying and iterating, not just prompting.'
tags:
- agents
status: reviewed
confidence: medium
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_p79zxlba
  locator: What is agentic engineering?
  quote: Code execution is the defining capability that makes agentic engineering possible.
- id: src_i6bjtiga
  locator: 15:35-16:06
  quote: vibe coding is about raising the floor for everyone in terms of what they can do in software
- id: src_i6bjtiga
  locator: '16:06'
  quote: agentic engineering is about preserving the quality bar of what existed before in professional software
relations:
- rel: related
  id: cpt_9ug6lxd3
- rel: introduced_in
  id: ent_a8uhtyvi
- rel: related
  id: cpt_8ga2cohi
recall:
- q: How do Willison and Karpathy each distinguish vibe coding from agentic engineering?
  a: 'Willison: vibe coding is unreviewed, prototype-quality LLM code. Karpathy: vibe coding raises the floor for everyone; agentic engineering preserves the professional quality bar while going faster.'
probes:
- q: A teammate ships agent-written code without reading it, saying 'the tests passed'. Is that agentic engineering? What would you check?
  looks_for: Unreviewed output is closer to vibe coding; agentic engineering needs verification evidence, review, and human responsibility for quality and security.
misconceptions:
- Agentic engineering just means using an AI to write code faster (the sources stress verification and responsibility).
---

# Agentic engineering

## Knowledge
- Willison uses the term for developing software with the assistance of coding agents, which are agents that can write and execute code.
- It is contrasted with vibe coding: unreviewed prototype-quality output versus work brought up to a production-ready standard.

## Evidence
- Willison: code execution is the defining capability that makes agentic engineering possible. [fact] (Willison, What is agentic engineering?)
- Willison reserves "vibe coding" for unreviewed, prototype-quality LLM-generated code. [fact] (Willison)
- Karpathy: vibe coding raises the floor for everyone; agentic engineering preserves the quality bar of professional software. [fact] (Karpathy talk, 15:35-16:06)
- Karpathy says people who are very good at it peak a lot more than 10x. [fact] (Karpathy talk, about 17:07; his own estimate)
- Both say humans remain responsible: Willison names specifying problems and verifying results; Karpathy names aesthetics, judgment, taste and oversight. [fact] (Willison; Karpathy 19:42) See [[claim-vibe-coding-versus-agentic-engineering]].

## Understanding
- The shared idea is that agents shift the human's work from typing code to directing and checking it. [inference] (synthesis of two independent sources)
- Verification is what separates the two practices in practice; see [[self-verification-loop]]. [inference]

## Application
- Treat each project as needing: a clear goal, a way for the agent to check its work, and review before merge. [inference] (drawing on [[self-verification-loop]])
- Hiring or training implication Karpathy suggests: judge people on large projects built with agents, not puzzles. [fact] (Karpathy talk, about 18:39; his opinion)

## Uncertainty
- The terminology is young and defined differently by different authors. [inference]
- Both main sources are individual practitioners' views; neither is a controlled study. [inference]

## Related
- [[llm-agents]] — the underlying systems.
- [[self-verification-loop]] — the core practice.
- [[agent-harness]] — what the agent runs inside.
