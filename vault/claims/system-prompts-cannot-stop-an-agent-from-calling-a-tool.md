---
id: clm_lyjzcbus
schema: 2
type: claim
title: "System prompts cannot stop an agent from calling a tool"
aliases: []
domains: [ai]
summary: "A prompt rule such as 'never delete production data' is a preference the model can override; reliable enforcement has to live in scoped credentials, sandboxes and approval gates below the model."
tags: [agents, guardrails, security]
status: reviewed
confidence: low
created: 2026-11-10
updated: 2026-11-10
sources:
  - id: src_98ddhon2
    locator: "What's actually overhyped"
    quote: "Enforcement has to live below the model."
relations:
  - {rel: about, id: cpt_od52gsyk}
  - {rel: related, id: cpt_svq1gwub}
verdict: unverified
---

# System prompts cannot stop an agent from calling a tool

## Evidence for
- [fact] The source describes an April 2026 Cursor agent that had rules against destructive actions in its prompt and quoted them back after deleting a database (second-hand, via The Register). (src_98ddhon2)
- [fact] The source says OpenAI's CISO acknowledged in October 2025 that prompt injection has no model-level fix on the horizon. (src_98ddhon2)
- [fact] Replit's July 2025 database deletion occurred during an explicit code freeze. (src_ieap5jak)

## Evidence against
- [inference] Prompt instructions do reduce unwanted actions in many cases; the claim concerns reliability as a guarantee, not zero effect. No source here measures how often prompt rules hold.

## Verdict reasoning
Plausible and consistent with several incident reports, but all evidence is anecdotal and second-hand from one author. Kept `unverified` until primary incident reports or measurements are ingested.
