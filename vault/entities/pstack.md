---
id: ent_gkjlm2x9
schema: 2
type: entity
title: "pstack"
aliases: [poteto-mode]
domains: [programming]
summary: "An open-source Cursor plugin of agent skills by Cursor engineer Lauren (poteto), built around agent self-verification and agent-driven PR merging."
tags: [tool, cursor, verification]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_gt6qwx4i
    locator: "Description"
    quote: null
relations:
  - {rel: related, id: cpt_hooaxuqi}
  - {rel: related, id: clm_gruqwh4q}
kind: tool
---

# pstack

## Who/what
- An open-source Cursor plugin in the cursor/plugins repository, described as 54 skills with two commands to remember: /setup-pstack and /poteto-mode. [fact] (AI懶人報 EP435 description; creator says contents were checked against the repo, which was not read here)
- Created by Lauren (poteto), who the description says shipped about 2,000 PRs in a month, mostly merged by agents. [fact] (EP435 description; the creator excludes unverified "20 agents" and "85% of engineers" claims)
- Stated core idea: verification. The agent runs the program and shows evidence; the author cannot judge its own work; repeated mistakes become lint rules, types or tests; overnight work runs under a contract with sampling. [fact] (EP435 description)

## Why it matters
- A concrete example of the "verification over review" approach to agent merging. [inference]
- The creator says it is not suitable for small changes, limited token budgets or work that is hard to verify automatically. [fact] (EP435 description)
- Source is a description of a video without transcript; the repo itself was not read. [inference]
