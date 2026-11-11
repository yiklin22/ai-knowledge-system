---
id: src_21xqrlz9
schema: 2
type: source
title: "Karpathy: how I use LLMs (re-uploaded lecture)"
aliases: []
domains: [ai]
summary: "A third-party YouTube re-upload, under a clickbait title, of a roughly two-hour Andrej Karpathy practical lecture on using ChatGPT-style apps: context window, model tiers, thinking models, tools, deep research, vibe coding and multimodality."
tags: [karpathy, llm-usage, lecture, re-upload]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: ent_a8uhtyvi}
  - {rel: about, id: cpt_ax286yoy}
  - {rel: about, id: cpt_6spiyzt2}
  - {rel: about, id: cpt_bpy1s28v}
kind: video
reliability: secondary
raw: raw/videos/2026-11-08-andrej-karpathy-99-use-ai-llms-wrong-here-s-how-he-does-it.md
url: "https://www.youtube.com/watch?v=7YEHs2SMaVQ"
author: Andrej Karpathy (speaker); re-uploaded by hyperfixation on AI | beamnxw (channel)
published: "2026-10-15"
volatile: true
last_verified: 2026-11-08
---

# Karpathy: how I use LLMs (re-uploaded lecture)

## Takeaways
- The description is promotional ("99% use AI wrong", "$15K bootcamps"), written by the uploader, not Karpathy. The transcript content looks like an earlier lecture (it discusses GPT-4o, o1 Pro, Grok 3 and deep research as a month-old feature, and refers to "the previous video"), so it dates from before this upload; I did not find the original publication date in the raw file. Model names and prices in it are out of date.
- Mental model: a chat is a growing token stream (the context window, the model's working memory); the model is a lossy, probabilistic "zip file" of the internet from pre-training plus a persona from post-training, with a knowledge cut-off; by itself it has no tools.
- Practical advice: start a new chat when you switch topic (tokens in the window cost accuracy and speed); know which model tier you are on; ask several providers ("LLM council"); use thinking models for hard math and code but not for simple questions; add tools (search, Python, deep research) for fresh or exact information; verify with primary sources for anything important.
- He describes vibe coding with Cursor's composer as his minted term and says you can always fall back to normal programming.
- Read only the first ~130 lines and the last ~25 lines plus keyword matches of the 515-line transcript; the sections on deep research, Python tools, Artifacts, audio, images, video and custom GPTs were not read in full.

## Locator map
- 00:00 context window and token stream; 01:00 pre-training and post-training; 04:40 "zip file" summary; 09:50 start new chats; 10:52 model tiers; 15:30 LLM council; 16:00 thinking models; 24:16 tool use and search; 35:43 deep research; 53:28 no tool used for a simple multiplication; 71:35 vibe coding; 120:38 summary of the ecosystem.
