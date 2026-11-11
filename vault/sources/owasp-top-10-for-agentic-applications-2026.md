---
id: src_7yi1bz2z
schema: 2
type: source
title: "OWASP Top 10 for Agentic Applications 2026"
aliases: []
domains: [ai]
summary: "The OWASP GenAI Security Project's December 2025 community document listing ten highest-impact agentic security risks (ASI01 to ASI10) with examples and mitigations."
tags: [security, agents, standard]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: ent_mcy1o573}
  - {rel: about, id: cpt_f92yye3m}
  - {rel: about, id: cpt_svq1gwub}
kind: document
reliability: primary
raw: raw/documents/2026-11-08-microsoft-word-owasp-top-10-for-agentic-applications-2026-12.md
url: null
author: OWASP GenAI Security Project, Agentic Security Initiative
published: "2025-12-01"
---

# OWASP Top 10 for Agentic Applications 2026

## Takeaways
- Ten risks: ASI01 Agent Goal Hijack; ASI02 Tool Misuse and Exploitation; ASI03 Identity and Privilege Abuse; ASI04 Agentic Supply Chain Vulnerabilities; ASI05 Unexpected Code Execution (RCE); ASI06 Memory and Context Poisoning; ASI07 Insecure Inter-Agent Communication; ASI08 Cascading Failures; ASI09 Human-Agent Trust Exploitation; ASI10 Rogue Agents.
- Core framing: agents amplify existing vulnerabilities; the authors add "least agency" (avoid unnecessary autonomy) to least privilege and say observability becomes non-negotiable.
- Root cause for goal hijack: natural-language inputs mix instructions and content, so agents cannot reliably tell them apart; mitigation 1 is to treat all natural-language inputs as untrusted.
- Each entry has description, examples, attack scenarios, mitigations and references; there is an incident tracker in Appendix D.
- Read in full only up to ASI01, ASI02 (start), ASI06 and ASI10 (descriptions) and the front matter; the remaining entries, appendices and incident table were not read, so details of ASI03 to ASI05, ASI07 to ASI09 are not cited on other pages.
- Published December 2025 (document title says version 2026); date given as the month only, so the day is set to the first for the schema.

## Locator map
- p.6-7 letter from the leaders (least agency); p.8 at a glance; p.9-11 ASI01; p.12-14 ASI02; p.24-26 ASI06; p.36-37 ASI10; Appendix D p.44 incidents tracker (unread).
