---
id: cpt_2s8cgyu5
schema: 2
type: concept
title: "The lethal trifecta and the Agents Rule of Two"
aliases: [lethal trifecta, Agents Rule of Two]
domains: [ai]
summary: "Prompt injection becomes a data breach when an agent has private data, untrusted content and an external communication channel at once; Meta's Rule of Two says hold at most two per session."
tags: [security, prompt-injection, agents]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources:
  - id: src_98ddhon2
    locator: "The Lethal Trifecta"
    quote: "Remove any one leg and the attack path collapses."
relations:
  - {rel: broader, id: cpt_svq1gwub}
  - {rel: related, id: cpt_od52gsyk}
  - {rel: introduced_in, id: ent_lh5mezgp}
recall:
  - q: What are the three legs of the lethal trifecta?
    a: Access to private data, exposure to untrusted content, and the ability to communicate externally.
  - q: What does Meta's Agents Rule of Two say?
    a: Until prompt injection can be reliably refused, an agent should hold at most two of the three trifecta properties in any single session.
probes:
  - q: An email-summarising agent can also send HTTP requests. Which leg do you remove, and why is that enough?
    looks_for: Removes external communication (or untrusted-content exposure); explains the attacker needs an exfiltration channel and the agent already reads private mail.
misconceptions:
  - Prompt injection only matters if the attacker has an account (they only need to leave text where the agent will read it).
---

# The lethal trifecta and the Agents Rule of Two

## Knowledge
- Simon Willison (June 2025) described the trifecta: private data, untrusted content, external communication in one execution path. [fact] (src_98ddhon2)
- The attacker needs no credentials, only text placed where the agent reads. [fact] (src_98ddhon2)
- Slack AI (August 2024, PromptArmor disclosure) is the cited example: a crafted public-channel message led to a rendered link carrying the victim's private data. [fact] (src_98ddhon2)
- Meta's Agents Rule of Two (October 2025): hold at most two of the three in any one session; choose which leg to drop by use case. [fact] (src_98ddhon2)

## Evidence
- Only one secondary source here; the original posts by Willison, PromptArmor and Meta are linked but were not read. [fact] (src_98ddhon2)

## Understanding
- The model is a graph of reachable capabilities: removing one leg breaks the exfiltration path without needing the model to detect the injection. [inference] (follows from the three-leg definition)

## Application
- Audit each agent configuration for the three legs; a coding agent that browses the web should not also hold cloud keys. [fact] (src_98ddhon2, its example)

## Uncertainty
- Rendered links count as external communication per the source; other side channels were not discussed. [inference]
- The source calls Willison's model the simplest explaining "every public" exfiltration breach, which is a strong generalisation. [inference]

## Related
- [[prompt-injection]], [[agent-guardrails-and-defense-in-depth]], [[agentic-application-security-risks-owasp-agentic-top-10]]
