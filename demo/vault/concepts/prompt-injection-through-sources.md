---
id: cpt_5wlbt92q
schema: 2
type: concept
title: Prompt injection through sources
aliases: []
domains:
- ai
summary: Text inside a document, web page or transcript that tries to give the model instructions, such as "ignore previous instructions".
tags:
- security
- llm
status: draft
confidence: medium
created: 2026-11-11
updated: 2026-11-11
sources:
- id: src_vs3k1ezx
  locator: Known limits (honest list)
  quote: Defences against prompt injection reduce risk; they do not make a model immune.
relations:
- rel: prerequisite_for
  id: cpt_h8ptu3ln
recall:
- q: What is prompt injection through a source?
  a: Instructions hidden in a document, page or transcript that the model may follow as if they came from the user.
- q: Do prompt-level defences make a model immune to injection?
  a: No. They reduce risk; structural controls (no tools, write confinement, human approval) are the strong ones.
---

# Prompt injection through sources

## Knowledge
- [fact] This system treats everything in `raw/` as untrusted data.
- [fact] Its controls are layered: label sources as data, give the model few or no tools, require human approval, and check outputs for forged citations and invented quotes.
- [fact] The document says these defences reduce risk and do not make a model immune.

## Evidence
- Security document, Threats and controls and Known limits.

## Understanding
The model reads instructions and data through the same channel, so it cannot be relied on to tell them apart. The safe assumption is that injected text will sometimes win, and the design question becomes what the model is able to do when it does.

## Application
Before connecting a model to untrusted text, list what it could do if fully hijacked, then remove every capability the task does not need.

## Uncertainty
- [inference] The document gives no measured block rate; it describes controls and tests.

## Related
- Prerequisite for [[Least privilege for LLM agents]].
