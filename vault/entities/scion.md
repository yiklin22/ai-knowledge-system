---
id: ent_xkssuk8m
schema: 2
type: entity
title: "Scion"
aliases: [Scion version control]
domains: [programming]
summary: "Anthropic's internal server-side version control system built for agent-heavy monorepos; not a general Git replacement and not publicly released."
tags: [version-control, anthropic, tool]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_fuuc8606
    locator: "Paragraphs 1-7"
    quote: null
  - id: src_21l5zt28
    locator: "03:49 to 05:55"
    quote: null
relations:
  - {rel: related, id: cpt_boy7hba5}
  - {rel: related, id: clm_uw2nbvpg}
  - {rel: related, id: ent_qwf7zfyu}
kind: tool
---

# Scion

## Who/what
- A version control system that Anthropic reportedly built in about five months with a team of seven using Claude Code agents, then used to migrate its large internal monorepo. [fact] (iThome; Andy Lin video; secondary, primary Anthropic post not ingested)
- Design as summarised by a creator: always-online clients, server does commits, merges and history queries, clients ask rather than copy, no full copy anywhere, commits happen on the server, and you only fetch what you read; a daemon, regional cache nodes and a central server layer. [fact] (Andy Lin video, 03:49 to 05:55; third-hand)
- Anthropic says it is not a suitable replacement for Git for general use, and others would need their own review, search and CI. [fact] (iThome paragraph 7; video 07:27)

## Why it matters
- An example of infrastructure redesigned for agents rather than humans: Git's offline, full-clone design became a cost when nearly all clients are online agents and CI jobs. [fact] (Andy Lin video, 03:18; creator's reading of Anthropic's post)
- Ordinary teams can borrow only small versions (worktrees, sparse checkout). [fact] (Andy Lin video, 07:57)
- Figures are second-hand; see the claim page for the size discrepancy. [inference]
