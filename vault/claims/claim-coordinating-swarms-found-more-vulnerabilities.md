---
id: clm_mpqaei85
schema: 2
type: claim
title: A coordinating agent swarm found more vulnerabilities than independent parallel agents
aliases: []
domains:
- ai
summary: 266 versus 21 vulnerabilities for one model, but about half outside the core directories and little overlap.
tags:
- agents
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_8tz2b8u3
  locator: Measuring coordination
  quote: the simple independent parallelized method produces 21 vulnerabilities over a 6.5 million token run, while the coordinating agent swarm found 266 vulnerabilities over a 27 million token run.
- id: src_8tz2b8u3
  locator: Measuring coordination
  quote: there were only 12 vulnerabilities in common between them
relations:
- rel: about
  id: cpt_o7t7o69z
verdict: supported
---

# A coordinating agent swarm found more vulnerabilities than independent parallel agents

## Evidence for
- Swarm found new vulnerabilities at a roughly constant rate; agents built tools and specialised. [fact] (Anthropic multiagent)

## Evidence against
- Limited to core directories, the two methods look comparable in tokens per vulnerability; the methods are largely complementary. [fact] (Anthropic multiagent)

## Verdict reasoning
Supported as stated, with the caveat that cost-effectiveness in the core directories was comparable; Anthropic's own experiment on its own models. [inference]
