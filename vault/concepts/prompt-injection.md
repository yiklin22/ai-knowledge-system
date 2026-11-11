---
id: cpt_svq1gwub
schema: 2
type: concept
title: "Prompt injection"
aliases: [indirect prompt injection]
domains: [ai]
summary: "Untrusted text in a model's context hijacking its instructions; in agents it becomes goal hijack, because instructions and data share one natural-language channel."
tags: [curriculum, security, agents]
status: draft
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_7yi1bz2z
    locator: "p.9, ASI01 Description"
    quote: "agents and the underlying model cannot reliably distinguish instructions from related content"
  - id: src_7yi1bz2z
    locator: "p.10, ASI01 Prevention 1"
    quote: "Treat all natural-language inputs (e.g., user-provided text, uploaded documents, retrieved content) as untrusted."
relations:
  - {rel: related, id: cpt_f92yye3m}
  - {rel: related, id: cpt_9ug6lxd3}
  - {rel: related, id: cpt_p776cv1f}
recall:
  - q: Why is prompt injection worse for agents than for chatbots?
    a: An agent acts on what it reads using real tools, so injected text in a web page, document or email can redirect multi-step behaviour (goal hijack), not just change one reply.
  - q: What is the first mitigation OWASP lists for goal hijack?
    a: Treat all natural-language inputs, including retrieved content and uploaded documents, as untrusted and route them through input-validation and injection safeguards.
---

# Prompt injection

## Knowledge
- Prompt injection is untrusted text in a model's context changing what the model does. [inference] (general definition, from the original stub; carried over)
- OWASP's agentic list treats the agentic version as ASI01 Agent Goal Hijack: agents and the underlying model cannot reliably distinguish instructions from related content, so attackers can redirect goals through prompts, tool outputs, documents or forged agent messages. [fact] (OWASP p.9)
- Indirect injection means the hostile text arrives through content the agent processes (web pages, documents in RAG, emails, calendar invites) rather than from the user. [fact] (OWASP p.9-10 examples)

## Evidence
- OWASP lists EchoLeak (a crafted email silently triggering Microsoft 365 Copilot to exfiltrate data), an Operator agent following instructions planted in web content, and a poisoned Google Doc as scenarios. [fact] (OWASP p.10; the document's descriptions, not independently checked)
- Mitigations in OWASP ASI01: treat all natural-language inputs as untrusted, least privilege for tools, human approval for high-impact or goal-changing actions, locked system prompts, runtime intent checks, logging with a behavioural baseline, red-team tests. [fact] (OWASP p.10-11)

## Understanding
- The root cause is a design property: one untyped text channel carries both instructions and data. Filtering helps but cannot be the only defence, so limiting what a hijacked agent can do (least agency) matters. [inference] (from the ASI01 description and mitigations)

## Application
- Give agents only the tools and scope they need, require approval for consequential actions, and log tool calls. [fact] (OWASP p.10-11)
- Treat web content, third-party documents and tool descriptions as untrusted input. [fact] (OWASP p.10)
- The digest workflow of this knowledge system follows the same rule: raw files are data, not instructions. [inference] (project context)

## Uncertainty
- This amendment draws on one source (the OWASP document); other prompt-injection research is not yet in the vault, so definitions beyond the agentic setting are thin. [inference]
- Prevalence and effectiveness of defences are not covered. [inference]

## Related
- [[agentic-application-security-risks-owasp-agentic-top-10]], [[llm-agents]], [[model-context-protocol-mcp]], [[prompt-engineering]]
