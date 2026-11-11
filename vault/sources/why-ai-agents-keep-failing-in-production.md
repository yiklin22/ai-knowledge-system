---
id: src_ieap5jak
schema: 2
type: source
title: "Why AI Agents Keep Failing in Production"
aliases: []
domains: [ai]
summary: "Essay naming three production failure patterns (dumb RAG, brittle connectors, compounding error) with incident examples, the 85%-per-step arithmetic, and a read/write/destructive permission framework."
tags: [agents, production, reliability, failure-modes]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources: []
relations:
  - {rel: authored_by, id: ent_xqueox2g}
  - {rel: about, id: cpt_g1vxdqj6}
kind: web
reliability: secondary
raw: raw/web/2026-11-10-why-ai-agents-keep-failing-in-production.md
url: "https://theaiengineer.substack.com/p/why-ai-agents-keep-failing-in-production"
author: "Paolo Perrone"
published: "2026-03-13"
---

# Why AI Agents Keep Failing in Production

## Takeaways
- [fact] Three failure patterns: Dumb RAG (poor sources, context flooding, silent retrieval failure), Brittle Connectors (schema drift, authentication rot, polling), Compounding Error.
- [fact] Incident examples cited second-hand: Google AI Overviews (May 2024), n8n schema drift (Feb 2026), LangSmith certificate expiry (May 2025), a Replit agent dropping a production database (July 2025), Google Antigravity deleting a drive.
- [fact] Arithmetic: at 85% per-step accuracy, 5 steps gives 44% and 10 steps gives 20% success.
- [fact] Proposed remedies: source-quality scoring, circuit breakers, credential-expiry alerts, schema pinning, and a three-tier permission model (read autonomous; write autonomous with logging; destructive needs human approval).
- Reader comments at the end (one about a £6.95 delivery fee served from a safety instruction, one link drop) are unverified anecdotes and promotion; ignored.

## Locator map
- "TL;DR"; "Failure Pattern 1/2/3"; "What Actually Works"; "The Honest Take".

## Reliability
Secondary essay; incident details rely on linked press and issue-tracker sources not re-read here.
