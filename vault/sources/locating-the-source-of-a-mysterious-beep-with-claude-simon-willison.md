---
id: src_iao3w460
schema: 2
type: source
title: "Locating the source of a mysterious beep with Claude (Simon Willison)"
aliases: []
domains: [ai]
summary: Willison's first-person account of having Claude Code build Beep Locator, a multi-device acoustic triangulation tool that found a beeping carbon monoxide detector, and of "giving Claude Code ears".
tags: [coding-agents, audio, web-audio, hot-swap, simon-willison]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources: []
relations:
  - {rel: authored_by, id: ent_lh5mezgp}
  - {rel: about, id: cpt_ckqm2sp9}
  - {rel: about, id: ent_gg0fprgh}
  - {rel: about, id: ent_7kkj45y4}
  - {rel: about, id: ent_8f72s5bf}
kind: web
reliability: primary
raw: raw/web/2026-11-10-locating-the-source-of-a-mysterious-beep-with-claude.md
url: "https://simonwillison.net/2026/Nov/9/mysterious-beeps/"
author: "Simon Willison"
published: "2026-11-09"
---

# Locating the source of a mysterious beep with Claude (Simon Willison)

## Takeaways
- Willison had Claude Code build Beep Locator to find an intermittent beep; it located the source to about 40cm and it was an old carbon monoxide detector. [fact, author's report]
- Claude found the 2007 BeepBeep acoustic ranging paper during research, and the design follows it. [fact, author's report]
- Hot-swappable listener modules (code pushed over WebSocket) let the agent keep changing the system without anyone touching each device. [fact, author's report]
- The author frames this as "giving Claude Code ears": the agent has no native audio input but can analyse audio via code. [fact, author's opinion]

## Reliability
Primary for what the author built and observed (a single anecdote, self-reported, not independently verified; the 40cm figure is one trial). Secondary for the BeepBeep paper's content (only its quoted abstract). Willison is a well-known practitioner blogger (see [[simon-willison]]). Mentions of Opus 5.5 and Fable 5.2 are incidental and not evaluated.

## Locator map
- "Locating the source..." intro and result: first sections (box room, 40cm, carbon monoxide detector)
- "How it works": BeepBeep paper, listener 60 second buffer, FFT beep detector, chirp alignment
- "How I built it": prompts, Opus 5.5 then Fable 5.2, `installModule()` hot-swap, feature prompts
- "Giving Claude Code ears": the central framing, GitHub Universe badge webcam anecdote
