---
id: clm_tfabt24p
schema: 2
type: claim
title: Agents need a pass/fail check to know whether work is really done
aliases: []
domains:
- ai
summary: Giving an agent something to run that returns pass or fail lets it close the loop itself.
tags:
- agents
status: reviewed
confidence: medium
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_kp4s3ioh
  locator: Give Claude a check to run
  quote: Claude stops when the work looks done.
- id: src_htqxs8h9
  locator: 05:11
  quote: they're usually not having the agent verify its own changes and then make any fixes depending on what it finds
relations:
- rel: about
  id: cpt_8ga2cohi
verdict: supported
---

# Agents need a pass/fail check to know whether work is really done

## Evidence for
- Claude Code docs and Amjad make the same recommendation; Anthropic's agent guide says gaining ground truth from the environment at each step is crucial. [fact]

## Evidence against
- Both main sources are interested parties (a vendor and a course seller); no measured effect size is given. [inference]

## Verdict reasoning
Mechanistically sensible and consistent across sources, but the evidence is guidance rather than measurement. [inference]
