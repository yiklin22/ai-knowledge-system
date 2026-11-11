---
id: cpt_vl2ncl2r
schema: 2
type: concept
title: Human approval gate
aliases: []
domains:
- ai
- programming
summary: AI-written knowledge lands in a proposals area and becomes part of the knowledge base only when a person approves it.
tags:
- human-in-the-loop
- safety
status: draft
confidence: medium
created: 2026-11-11
updated: 2026-11-11
sources:
- id: src_2bnb6lem
  locator: Key decisions and trade-offs
  quote: The digest agent can write only inside `proposals/`; only a person runs approve
- id: src_vs3k1ezx
  locator: Threats and controls
  quote: a human approves everything before it becomes knowledge
relations:
- rel: related
  id: cpt_h8ptu3ln
recall:
- q: Where may the digest agent write, and who can approve?
  a: Only inside proposals/. Only a person approves (web Review page or ./kb approve).
- q: Why must the gate be enforced by permissions and not by the prompt?
  a: A prompt instruction can be overridden by injected text; a missing write permission cannot.
- q: What does the approval gate cost?
  a: Human review effort.
---

# Human approval gate

## Knowledge
- [fact] The digest agent can write only inside `proposals/`.
- [fact] Approval is a human action, from the Review page or `./kb approve`.
- [fact] The stated cost is review effort; the stated gain is that a model mistake or a poisoned page cannot enter silently.

## Evidence
- Design document, Key decisions and trade-offs.
- The security document lists human approval as one of its controls against prompt injection.

## Understanding
The gate turns an unreliable writer into a reliable pipeline by moving trust from the model to a checkpoint. It only works if the checkpoint is enforced by permissions, since an instruction in a prompt can be argued with and a missing write permission cannot.

## Application
Put a gate wherever model output becomes durable or is acted on: knowledge bases, code merges, outbound messages. Keep the review cheap (diffs, validation run in advance) or people will rubber-stamp it.

## Uncertainty
- [speculation] How well the gate holds up when the reviewer is tired or the batch is large is not measured here.

## Related
- Requires [[Files as the source of truth, databases as disposable caches]].
- One of the structural controls in [[Least privilege for LLM agents]].
