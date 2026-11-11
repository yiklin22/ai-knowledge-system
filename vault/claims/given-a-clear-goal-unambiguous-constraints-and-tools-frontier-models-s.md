---
id: clm_5mgqsx7s
schema: 2
type: claim
title: "Given a clear goal, unambiguous constraints and tools, frontier models solve problems by brute force"
aliases: []
domains: [ai]
summary: "Willison describes 'Fable class' models as able to build almost anything you can define with a clear goal, unambiguous constraints and tool access, which makes definition skill the scarce part."
tags: [capability, software-engineering, opinion]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_opi2fpk9
    locator: "slide 042"
    quote: "they will solve your problem effectively through brute force"
relations:
  - {rel: about, id: cpt_24s5izka}
  - {rel: related, id: clm_blkj2ekk}
  - {rel: related, id: clm_tfabt24p}
verdict: unverified
volatile: true
last_verified: 2026-11-08
---

# Given a clear goal, unambiguous constraints and tools, frontier models solve problems by brute force

Statement: for the newest frontier models, if you clearly define the goal, give unambiguous instructions about constraints and provide the necessary tools, the model will solve the problem through brute force; defining these well is the skilled work.

## Evidence for
- Willison states it as his view of the first public Fable-class model and its successors such as GPT-6 Astra. [fact] (Willison 2026, slide 042; opinion)
- His anecdotes: a coding agent built a playable raccoon-heist game from screenshots. [fact] (Willison 2026, slides 056-058)

## Evidence against
- He qualifies it himself: the generated games were fun for about a minute and 15 seconds, and a fun, well-balanced game remains beyond the agents he tried, so "looks like a game" differs from "is a good game". [fact] (Willison 2026, slide 059)
- Scion engineers said their job was often to tell Claude not to break system rules, which suggests that unambiguous constraints are hard to give. [fact] (Andy Lin video, 06:56; third-hand)
- No benchmark or controlled evidence is given. [inference]

## Verdict reasoning
- Unverified opinion from a respected practitioner; it fits the "verification and specification are the human work" theme across sources but is anecdotal. [inference]
