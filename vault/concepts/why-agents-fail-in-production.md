---
id: cpt_g1vxdqj6
schema: 2
type: concept
title: "Why agents fail in production"
aliases: [agent production failure patterns]
domains: [ai]
summary: "Agents mostly fail from the engineering around the model, not the model: poor retrieval context, brittle connectors (schema drift, expired credentials, polling) and per-step errors that compound without checkpoints."
tags: [agents, production, reliability]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
volatile: true
last_verified: 2026-11-10
sources:
  - id: src_ieap5jak
    locator: "Before We Diagnose"
    quote: "A deterministic system fails loudly. A non-deterministic agent fails quietly, confidently, and often in ways your tests never anticipated."
  - id: src_wlpdy4uq
    locator: "What Can Go Wrong"
    quote: null
relations:
  - {rel: broader, id: cpt_9ug6lxd3}
  - {rel: related, id: cpt_b99cr5t8}
  - {rel: related, id: cpt_5s6mnu9b}
  - {rel: related, id: cpt_od52gsyk}
  - {rel: related, id: cpt_eripv7vv}
recall:
  - q: What are the three production failure patterns named in the source?
    a: Dumb RAG (bad context), brittle connectors (schema drift, credential rot, polling), and compounding error across steps.
  - q: What permission model does the source propose for agents?
    a: Read operations autonomous; write operations autonomous with logging; destructive or irreversible operations require human approval.
misconceptions:
  - A better model fixes agent failures (the source says the failures are in retrieval, connectors, permissions and observability).
---

# Why agents fail in production

## Knowledge
- Gartner is cited as predicting 40%+ of agentic AI projects scrapped by 2027, for cost, unclear value and risk controls rather than model quality; Deloitte as finding about 11% of organisations with agents in production and 38% piloting. [fact] (src_ieap5jak; src_wlpdy4uq; second-hand)
- **Dumb RAG**: retrieval ranks relevance not credibility, floods context, and fails silently (example: Google AI Overviews, May 2024). Fixes: source scoring, freshness filters, confidence thresholds routing to humans. [fact] (src_ieap5jak)
- **Brittle connectors**: schema drift (n8n upgrade producing invalid tool schemas, February 2026), authentication rot (a LangSmith certificate expiring after failed renewal, May 2025), the polling trap. Fixes: circuit breakers, expiry alerts, schema pinning, event-driven design. [fact] (src_ieap5jak)
- **Compounding error**: see [[per-step-error-compounds-across-an-agent-workflow]]; examples a Replit database deletion (July 2025) and Google Antigravity deleting a drive. [fact] (src_ieap5jak)
- What works: bounded scope, observable behaviour (every tool call logged), human gates on irreversible actions. [fact] (src_ieap5jak)

## Evidence
- Incident details are from press and issue trackers linked in the source; none were re-read. [fact] (src_ieap5jak)
- Amazon is cited as finding poorly defined tool schemas a leading cause of agent failures. [fact] (src_ieap5jak, second-hand)

## Understanding
- Handing routing and execution to a non-deterministic model adds quiet, confident failures on top of ordinary distributed-systems failures. [fact] (src_ieap5jak's framing)
- The three patterns map to existing vault topics: retrieval ([[retrieval-augmented-generation]]), tool interfaces ([[tool-use-and-function-calling]], [[model-context-protocol-mcp]]) and guardrails ([[agent-guardrails-and-defense-in-depth]]). [inference]

## Application
- Before production: log every tool call, monitor credential expiry, pin tool schemas, gate irreversible actions, and scope the agent to one domain. [inference] (synthesising the source's fixes)

## Uncertainty
- Adoption and cancellation percentages are volatile, second-hand and dated 2025-2026. [inference]
- The three patterns are one author's taxonomy, not an established classification. [inference]

## Related
- [[llm-agents]], [[multi-agent-failure-modes]], [[the-agent-loop-think-act-observe]], [[klarna-scaled-back-its-customer-service-agent-and-rehired-humans]]
