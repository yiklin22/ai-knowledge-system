---
id: src_98ddhon2
schema: 2
type: source
title: "What are AI Agent Guardrails?"
aliases: []
domains: [ai]
summary: "Explainer on agent guardrails: six guardrail layers, Willison's lethal trifecta and Meta's Rule of Two, the two-tier cheap-check-then-LLM-judge pattern (Ramp), and why system prompts cannot enforce safety."
tags: [guardrails, security, prompt-injection, agents]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources: []
relations:
  - {rel: authored_by, id: ent_xqueox2g}
  - {rel: about, id: cpt_od52gsyk}
  - {rel: about, id: cpt_2s8cgyu5}
kind: web
reliability: secondary
raw: raw/web/2026-11-10-what-are-ai-agent-guardrails.md
url: "https://theaiengineer.substack.com/p/what-are-ai-agent-guardrails"
author: "Paolo Perrone"
published: "2026-05-13"
volatile: true
last_verified: 2026-11-10
---

# What are AI Agent Guardrails?

## Takeaways
- [fact] Agent guardrails constrain tool calls, credentials and the execution environment, not only text output.
- [fact] Six layers: input, output, tool, sandbox, human-in-the-loop, monitoring; the article says tool and sandbox limits are what actually stop actions.
- [fact] The lethal trifecta (private data + untrusted content + external communication) and Meta's Agents Rule of Two (hold at most two per session).
- [fact] Ramp's Policy Agent two-tier pattern, with vendor-reported results (85% fewer manual reviews, 99%+ accuracy, 10-15% escalated to a human).
- [fact] A January 2026 meta-analysis (second-hand) is cited for adaptive attacks beating state-of-the-art classifiers more than 85% of the time.
- [fact] A Cursor agent deleting a startup's production database on 2026-04-24 is the lead anecdote, cited to The Register.
- The closing reader comment links to an outside post and is unrelated promotion; ignored.

## Locator map
- Intro anecdote; "TL;DR"; "The Lethal Trifecta"; "How guardrails actually work in production" (six layers and an allowlist code sample); "The two-tier pattern"; "What's actually overhyped"; "Who's actually building this" (NeMo Guardrails, Llama Guard, Guardrails AI, OpenAI Guardrails API).

## Reliability
Secondary explainer with vendor-reported numbers (Ramp, Meta). Security statistics and the April 2026 incident are second-hand and volatile.
