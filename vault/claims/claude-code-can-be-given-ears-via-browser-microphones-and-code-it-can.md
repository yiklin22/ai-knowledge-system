---
id: clm_emjwdxss
schema: 2
type: claim
title: "Claude Code can be given ears via browser microphones and code it can analyze"
aliases: []
domains: [ai]
summary: Although Claude has no native audio input, Willison claims a coding agent can "hear" by running code over audio captured by remote microphones; supported by one self-reported working example.
tags: [coding-agents, audio]
status: reviewed
confidence: low
created: 2026-11-10
updated: 2026-11-10
sources:
  - id: src_iao3w460
    locator: "Giving Claude Code ears"
    quote: "Claude doesn’t have native audio input (yet), but it can run JavaScript and Python code that can analyze audio captured by a microphone."
relations:
  - {rel: about, id: cpt_ckqm2sp9}
  - {rel: about, id: ent_7kkj45y4}
  - {rel: derived_from, id: src_iao3w460}
  - {rel: answers, id: qst_22m9h6sx}
verdict: unverified
---

# Claude Code can be given ears via browser microphones and code it can analyze

## Evidence for
[fact] Willison reports that Beep Locator, built and iterated on by Claude Code, located a beep to about 40cm and led him to the source ([[beep-locator]]). [fact] He also cites a similar hack: Martin Woodward pointing a webcam at a badge screen so a coding agent could check whether updates worked (second-hand, "I heard about").

## Evidence against
[inference] None found in the source, but the evidence is a single self-reported success by an enthusiast author. There is no independent replication, no comparison with a human doing the same search, and the human still did setup and chose features. Note the "ears" are signal-processing code, not audio understanding by the model.

## Verdict reasoning
[inference] The narrow claim (an agent can be given an audio feedback channel through code) is plausible and demonstrated once, but I mark it `unverified` because only one self-reported source backs it. Confidence low.
