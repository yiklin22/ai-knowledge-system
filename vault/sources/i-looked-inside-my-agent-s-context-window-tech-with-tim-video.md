---
id: src_en5a34og
schema: 2
type: source
title: "I Looked Inside my Agent's Context Window (Tech With Tim video)"
aliases: []
domains: [ai]
summary: "A sponsored test that gives Claude Code five different web-scraping tools for one price-shopping job and compares how many context tokens each uses, plus a three-question audit for any tool."
tags: [context-window, tools, cost, creator]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: cpt_bpy1s28v}
  - {rel: about, id: clm_bbulo1rc}
kind: video
reliability: opinion
raw: raw/videos/2026-11-08-i-looked-inside-my-agents-context-window.md
url: "https://www.youtube.com/watch?v=Sc_D4o9-vNk"
author: Tech With Tim (channel)
published: "2026-11-03"
volatile: true
last_verified: 2026-11-08
---

# I Looked Inside my Agent's Context Window (Tech With Tim video)

## Takeaways
- Sponsored by Bright Data, whose Scraper Studio wins the comparison; the presenter says the other tools were paid services too, and that each tool has its place.
- Context contents listed: system prompt, tool definitions, messages, files read and every tool result; the /context command shows the breakdown. Starting point in his session: about 20,000 tokens.
- Three effects of a fuller context: cost (the whole context is resent each message), speed, and accuracy (details get lost, and compaction summarises older messages).
- Test: find price and stock for one product at seven stores. Built-in fetch was blocked everywhere (still 43,000 tokens). Proxy API and markdown crawler worked but wrote pages to disk and parsed with scripts; one proxy run picked the wrong Walmart price. Pre-built scrapers took about 70 tool calls and missed two sites. Scraper Studio returned only a small JSON object.
- Numbers are internally inconsistent: mid-video /context readings are about 73,000, 73,000, 158,000 and 50,000 tokens, while the later summary says 63,000, 58,000, 155,000 and 36,000. Cost figures ($25 to about $150 for 500 products a week) are the presenter's token-price multiplication on a model he names Opus 5.5.
- Takeaway: before adding a tool ask what it returns, how big it is and how much of it is used; compare /context before and after.

## Locator map
- 00:44 what is in the context window; 01:52 effects of a larger context; 05:03 task; 05:56-10:33 runs 1-5; 13:05 scoreboard; 15:05 total context usage; 16:06 self-healing scrapers; 17:37 audit your tools.
