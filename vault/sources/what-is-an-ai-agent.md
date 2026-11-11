---
id: src_wlpdy4uq
schema: 2
type: source
title: "What is an AI Agent?"
aliases: []
domains: [ai]
summary: "Beginner-to-intermediate explainer (Issue #1 of The AI Engineer): an agent is an LLM in a think-act-observe loop with tools and memory; cites Klarna, Shopify Sidekick and Deloitte/Gartner adoption figures second-hand."
tags: [agents, explainer, react]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources: []
relations:
  - {rel: authored_by, id: ent_xqueox2g}
  - {rel: about, id: cpt_9ug6lxd3}
  - {rel: about, id: cpt_r0y15j1d}
kind: web
reliability: secondary
raw: raw/web/2026-11-10-what-is-an-ai-agent.md
url: "https://theaiengineer.substack.com/p/what-is-an-ai-agent"
author: "Paolo Perrone"
published: "2026-02-18"
---

# What is an AI Agent?

## Takeaways
- [fact] Defines an agent as an LLM-driven system that reasons about a goal, picks tools and acts in a loop (Think, Act, Observe, Repeat); three components: brain (LLM), tools, memory/state.
- [fact] Names the loop ReAct (Yao et al., ICLR 2023) and shows a ~15-line LangChain example; says the other ~10,000 lines of a real system are error handling, auth and guard checks.
- [fact] Reports (second-hand, via Fortune, Deloitte, Gartner, APEX-Agents) Klarna's rollout and partial reversal, ~11% of organisations with agents in production, a Gartner forecast that 40%+ of agentic projects will be scrapped by 2027, and best-model first-attempt success of about 24% on real-world knowledge-work tasks.
- [fact] Failure modes listed: tool-call hallucination, compounding errors, governance gap, hype gap. Pattern that works per the author: constrained domains, clear tool definitions, humans in the loop.

## Locator map
- "The TL;DR" section: summary bullets.
- "How AI Agents Actually Work": the loop and the three components.
- "Who's Actually Building With This": Klarna, coding agents, Shopify Sidekick.
- "What Can Go Wrong (and What's Overhyped)": four failure modes.
- Footnotes 1-4: Deloitte, ReAct paper, APEX-Agents, Gartner.
- The trailing reader comments are advertisements for consulting firms; ignored as noise.

## Reliability
Secondary: a practitioner newsletter explainer. Statistics are quoted from other sources and were not checked against them. The code example uses an outdated model name and is illustrative.
