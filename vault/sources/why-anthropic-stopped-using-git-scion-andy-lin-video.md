---
id: src_21l5zt28
schema: 2
type: source
title: "Why Anthropic stopped using Git: Scion (Andy Lin video)"
aliases: []
domains: [programming]
summary: "A creator's summary of two other creators' readings of Anthropic's Scion post: why Git strained, Scion's six rules and three cache layers, speed comparisons and what ordinary developers can borrow."
tags: [version-control, anthropic, creator]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: ent_xkssuk8m}
  - {rel: about, id: clm_uw2nbvpg}
  - {rel: about, id: cpt_boy7hba5}
kind: video
reliability: opinion
raw: raw/videos/2026-11-08-anthropic-git-3-scion-amine-ai-milan-jovanovi.md
url: "https://www.youtube.com/watch?v=_D7jkD8tvDw"
author: Andy Lin 林玉堂 (channel)
published: "2026-11-03"
volatile: true
last_verified: 2026-11-08
---

# Why Anthropic stopped using Git: Scion (Andy Lin video)

## Takeaways
- Third-hand: the transcript is the narration of an English-language video (Amine AI) that itself reads Anthropic's blog; the description cites a second creator (Milan Jovanović).
- Figures stated: about 30,401 merges in a day versus about 2,500 in May; main-branch history "almost 800 GB"; about 25 GB working copy; about 25 million CI checkouts a day; Anthropic estimate of around 600 PB of Git traffic a day if every job pulled everything; hundreds of Git mirrors at peak.
- Speed comparisons narrated: pulling the latest code 87 s on Git vs 3.5 s on Scion; checking what changed about 4 s vs 19 ms; fresh agent copy over 7 minutes vs 5 s.
- Design as narrated: six rules (always-online clients, server does the thinking, ask rather than copy, no full copy anywhere, commits happen on the server, you only get what you read) and three layers (Scion daemon, regional cache nodes, central server on Spanner or cloud storage).
- Team: seven people over five months using agents; engineers say Claude writes better code than them but they supply system-level understanding and often must tell it not to break rules. A "Mythos" rewrite is said to use 20 times less memory and run 4 times faster.
- Advice: Scion is not for general use; ordinary teams can copy two ideas, Git worktrees (one copy per agent, e.g. claude -w) and sparse checkout. Keep using Git.
- The 800 GB figure conflicts with the news article's "close to 100 GB"; speech-to-text artefacts ("Sci-on", "Entropic", "cloud-w") are in the transcript.

## Locator map
- 00:11 merges per day; 00:43 repo size; 01:14 600 PB; 02:17 timings; 03:18 offline as a burden; 03:49 six rules; 05:23 three layers; 05:55 team and Mythos rewrite; 07:27 can you use Scion; 07:57 worktrees and sparse checkout; 08:28 stay on Git.
