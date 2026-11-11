---
id: cpt_od52gsyk
schema: 2
type: concept
title: "Agent guardrails and defense in depth"
aliases: [agent guardrails]
domains: [ai]
summary: "Constraints on an agent's tool calls, credentials and environment, stacked in layers (input, output, tool, sandbox, human approval, monitoring) because no single layer, including the model, can be relied on."
tags: [guardrails, security, agents]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources:
  - id: src_98ddhon2
    locator: "The one thing to remember"
    quote: "Agent safety lives in the system around the model."
  - id: src_ieap5jak
    locator: "Failure Pattern 3, fix"
    quote: null
relations:
  - {rel: broader, id: cpt_9ug6lxd3}
  - {rel: related, id: cpt_svq1gwub}
  - {rel: related, id: cpt_f92yye3m}
  - {rel: related, id: cpt_2s8cgyu5}
  - {rel: related, id: cpt_g1vxdqj6}
recall:
  - q: Name the six guardrail layers for agents.
    a: Input, output, tool, sandbox, human-in-the-loop and monitoring guardrails.
  - q: Why is "do not delete production data" in a system prompt not a guardrail?
    a: It only states a preference the model can override; enforcement must be scoped credentials, sandboxing or an approval gate in the tool dispatcher.
  - q: What is the two-tier guardrail pattern?
    a: A cheap check runs on every request; only unresolved cases escalate to an expensive LLM judge, and the residue to a human.
probes:
  - q: An agent has a delete tool and a prompt rule against destructive actions. What would you add and where?
    looks_for: Allowlist and approval gate in the dispatcher, least-privilege scoped credentials and sandboxing; recognises prompt rules are not enforcement.
misconceptions:
  - A stronger system prompt is a safety control (it is a preference, not an enforcement point).
  - Guardrails replace alignment training (they catch what slips through at runtime; both are needed).
---

# Agent guardrails and defense in depth

## Knowledge
- Agent guardrails constrain tool calls, credentials and the execution environment; chatbot guardrails mainly filter text. [fact] (src_98ddhon2)
- Six categories: input (injection classifiers, PII, topic limits), output (safety classifiers, schema validators, hallucination checks), tool (allowlists, argument validation, rate limits), sandbox (scoped read-only tokens, egress controls, filesystem isolation), human-in-the-loop approvals, and monitoring (audit logs, LLM judges, anomaly detection). [fact] (src_98ddhon2)
- Two-tier pattern: cheap first pass on everything, expensive LLM judge only on flagged traffic; Ramp reports 85% fewer manual reviews at 99%+ accuracy with 10-15% escalated (vendor-reported). [fact] (src_98ddhon2)
- Named tools: NVIDIA NeMo Guardrails, Llama Guard, LlamaFirewall, Guardrails AI, OpenAI's Guardrails API. [fact] (src_98ddhon2)
- A simple tool guardrail is an allowlist with per-tool policy (max calls, approval required) that the dispatcher consults on every call. [fact] (src_98ddhon2, code sample)

## Evidence
- Incidents cited: a Cursor agent deleting a production database via an over-scoped token (April 2026), Replit during a code freeze (July 2025), Amazon Kiro (December 2025). Source states the credentials' scope was the real boundary. [fact] (src_98ddhon2; second-hand via press)
- Adaptive attacks reportedly beat state-of-the-art classifiers more than 85% of the time (a January 2026 meta-analysis cited second-hand). [fact] (src_98ddhon2)
- The three-tier permission idea (read autonomous, write logged, destructive needs approval) appears independently in src_ieap5jak. [fact]

## Understanding
- Because the model decides which tool to call, the only reliable control point is below the model, where actions meet credentials. [inference] (supported by both sources' incident examples; see [[system-prompts-cannot-stop-an-agent-from-calling-a-tool]])
- Defense in depth fits because each classifier layer is bypassable; stacking makes an attack defeat them in series. [inference]

## Application
- Give agents least-privilege, scoped tokens; read-only by default; require approval before delete, send, publish or charge. [inference] (combining src_98ddhon2 and src_ieap5jak)
- Use the two-tier pattern when an LLM judge on every request is too costly or slow. [fact] (src_98ddhon2)

## Uncertainty
- Success rates of classifiers and Ramp's figures are volatile vendor or second-hand numbers. [inference]
- How to define tiers precisely is open: see [[how-should-agent-permission-tiers-be-defined]]. [inference]

## Related
- [[prompt-injection]], [[agentic-application-security-risks-owasp-agentic-top-10]], [[the-lethal-trifecta-and-the-agents-rule-of-two]], [[why-agents-fail-in-production]]
