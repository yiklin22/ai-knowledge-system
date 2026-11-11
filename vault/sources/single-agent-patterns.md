---
id: src_7eble6ru
schema: 2
type: source
title: "Single-Agent Patterns"
aliases: []
domains: [ai]
summary: "Comparison of four single-agent reasoning patterns (ReAct, Plan-and-Execute, ReWOO, Reflexion) with strengths, ceilings, a selection flowchart and common hybrids."
tags: [agents, react, reflexion, rewoo, patterns]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources: []
relations:
  - {rel: authored_by, id: ent_xqueox2g}
  - {rel: about, id: cpt_qlqrjynu}
kind: web
reliability: secondary
raw: raw/web/2026-11-10-single-agent-patterns.md
url: "https://theaiengineer.substack.com/p/the-4-single-agent-patterns"
author: "Paolo Perrone"
published: "2026-04-16"
---

# Single-Agent Patterns

## Takeaways
- [fact] ReAct is the default (one LLM call per step); Plan-and-Execute plans up front with a cheaper executor; ReWOO plans once with placeholders and runs tools in parallel (2 LLM calls); Reflexion retries with a stored self-critique.
- [fact] Figures attributed to papers (second-hand): ReWOO 5x token efficiency and +4% accuracy on HotpotQA; Reflexion lifts GPT-4 HumanEval pass rate from 80% to 91%.
- [fact] A 2025 replication study is cited: single-agent Reflexion tends to repeat earlier misconceptions because the same model writes output and critique.
- [fact] The author's recommendation: start with ReAct; invest first in tools and evals; add other patterns only when a specific failure mode (cost, planning, correctness) appears.

## Locator map
- "TL;DR"; one section per pattern (good / bad / best for / ceiling); "The Decision Flowchart"; "The Hybrid Approach"; "The Honest Take".

## Reliability
Secondary explainer. Paper numbers are cited via a consultancy blog (AgixTech) for ReWOO and via the Reflexion paper for HumanEval; neither was checked against the papers.
