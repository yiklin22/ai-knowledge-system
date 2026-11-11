---
id: cpt_h8ptu3ln
schema: 2
type: concept
title: Least privilege for LLM agents
aliases: []
domains:
- ai
summary: Give a model only the tools and write access its task needs, so that a hijacked model has nothing dangerous to do.
tags:
- security
- agents
status: draft
confidence: medium
created: 2026-11-11
updated: 2026-11-11
sources:
- id: src_vs3k1ezx
  locator: Threats and controls
  quote: Ask calls Claude with an empty tool list, so there is nothing to hijack
relations: []
recall:
- q: How many tools does the Ask model call have, and why?
  a: None (an empty tool list), so injected text has nothing to hijack.
- q: Name three things the digest agent cannot do.
  a: Edit vault/ or raw/, run approve, use the web.
---

# Least privilege for LLM agents

## Knowledge
- [fact] Ask calls the model with an empty tool list.
- [fact] The digest agent can write only inside `proposals/`, cannot approve, cannot edit `vault/` or `raw/`, and has no web access.
- [inference] With no web tool there is no channel for sending private text out.

## Evidence
- Security document, Threats and controls, prompt-injection row.

## Understanding
Least privilege changes the question from "will the model resist this text?" to "what can happen if it does not?". The first has a probabilistic answer and the second can be made to have a fixed one.

## Application
For each agent, write the allow-list first and justify every entry. Separate the agent that reads untrusted text from anything that can act on the outside world.

## Uncertainty
- [inference] An allow-list is only as good as the harness that enforces it; that enforcement is not examined in the source.

## Related
- Builds on [[Prompt injection through sources]].
- Works together with [[Human approval gate]].
