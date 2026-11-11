---
id: clm_e8yl7i47
schema: 2
type: claim
title: Hybrid retrieval ranks the right source first more often than keyword search
aliases: []
domains:
- ai
summary: On this project's 20-question set, hybrid search placed the expected source first in 75% of cases against 50% for keyword search.
tags:
- retrieval
- evaluation
status: draft
confidence: low
created: 2026-11-11
updated: 2026-11-11
sources:
- id: src_9ruu2p7x
  locator: 'How to read this: Limits'
  quote: hybrid placed the right source first more often (75% vs 50% keyword-only) at no cost to recall
relations:
- rel: supports
  id: cpt_xve1awep
verdict: unverified
---

# Hybrid retrieval ranks the right source first more often than keyword search

## Evidence for
- [fact] The evaluation reports hit@1 of 50% (keyword), 65% (semantic) and 75% (hybrid), with hit@5 at 95% for all three.

## Evidence against
- [fact] The same document says 20 cases is a small sample and that a one-question difference is noise.
- [fact] The questions were written by the person who built the retriever.

## Verdict reasoning
The direction is plausible and matches the design rationale, but one small self-written test set does not establish it. Left `unverified`.
