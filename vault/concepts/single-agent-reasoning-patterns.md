---
id: cpt_qlqrjynu
schema: 2
type: concept
title: "Single-agent reasoning patterns"
aliases: [ReAct, Plan-and-Execute, ReWOO, Reflexion]
domains: [ai]
summary: "Four ways to structure one LLM agent's reasoning: ReAct (step by step), Plan-and-Execute (plan first), ReWOO (plan with placeholders, run tools in parallel) and Reflexion (retry with a self-critique); chosen by which failure mode you can tolerate."
tags: [agents, react, reflexion, planning]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources:
  - id: src_7eble6ru
    locator: "The Honest Take"
    quote: "start with ReAct and let the failures tell you when to graduate"
relations:
  - {rel: broader, id: cpt_9ug6lxd3}
  - {rel: related, id: cpt_ezdgksnt}
  - {rel: related, id: cpt_8ga2cohi}
  - {rel: related, unresolved: "Agent memory"}
recall:
  - q: What distinguishes ReAct, Plan-and-Execute, ReWOO and Reflexion in one line each?
    a: ReAct reasons and acts one step at a time; Plan-and-Execute plans all steps first then executes; ReWOO plans once with placeholders and runs tools in parallel; Reflexion retries after writing a self-critique.
  - q: When does Reflexion work well and when does it not?
    a: It needs a clear automated success check (tests, schema); with ambiguous success criteria or a single model critiquing itself, reflections get vague and repeat earlier misconceptions.
probes:
  - q: Your task needs 10 sequential steps and each depends on the previous result. Which pattern and why?
    looks_for: Picks ReAct (or Plan-and-Execute with replanning), not ReWOO, because step results must change later steps; notes ReAct's linear token cost.
misconceptions:
  - Agent patterns and agent frameworks are the same thing (patterns are architectures; LangGraph or CrewAI are libraries that can implement them).
  - More sophisticated patterns are always better (the source says most production agents are plain ReAct loops).
---

# Single-agent reasoning patterns

## Knowledge
- Three design choices separate the patterns: when to plan (up front, per step, never), how many LLM calls per task, and how failure is handled. [fact] (src_7eble6ru)
- **ReAct**: Thought, Action, Observation loop, one LLM call per step; adaptive and debuggable, but cost grows with steps and it only sees one step ahead. [fact] (src_7eble6ru)
- **Plan-and-Execute**: a strong model plans, a cheaper one executes, a replanner fires on failure; plan is inspectable before running but rigid when reality surprises it. [fact] (src_7eble6ru)
- **ReWOO**: two LLM calls total with placeholders such as #E1; parallel tools; cannot adapt mid-run. Reported 5x token efficiency and +4% accuracy on HotpotQA versus ReAct (second-hand). [fact] (src_7eble6ru)
- **Reflexion**: an evaluator scores the attempt, a self-critique goes into an episodic memory, the task is retried. Reported GPT-4 HumanEval pass rate 80% to 91%. [fact] (src_7eble6ru)
- Common hybrids: ReAct + Reflexion; Plan-and-Execute with ReAct fallback; ReWOO fast path with Plan-and-Execute fallback. [fact] (src_7eble6ru)

## Evidence
- ReAct from Yao et al., Reflexion from Shinn et al., cited by the source with arXiv links; those papers were not read here. [fact] (src_7eble6ru)
- A 2025 replication study is cited as finding single-agent Reflexion repeats earlier misconceptions. [fact] (src_7eble6ru)

## Understanding
- The patterns trade adaptivity against cost: planning up front saves LLM calls but loses the ability to react to surprises. [inference] (summarising the source's per-pattern pros and cons)
- Reflexion only helps when success can be checked mechanically, which links it to [[self-verification-loop]]. [inference]

## Application
- Start with ReAct; move to another pattern only when a specific failure (cost, planning, correctness) appears. [fact] (src_7eble6ru, author's recommendation)
- Build the eval before choosing the architecture: the source says no pattern helps if success cannot be measured. [fact] (src_7eble6ru)

## Uncertainty
- The numerical results are cited second-hand and depend on benchmark and model; do not treat them as general. [inference]
- The claim that "the majority of agents in production are ReAct loops" is the author's impression, not measured. [inference]

## Related
- [[the-agent-loop-think-act-observe]], [[agentic-workflow-patterns]], [[llm-agents]], [[multi-agent-failure-modes]]
