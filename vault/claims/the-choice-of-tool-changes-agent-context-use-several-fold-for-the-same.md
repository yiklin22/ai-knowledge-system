---
id: clm_bbulo1rc
schema: 2
type: claim
title: "The choice of tool changes agent context use several-fold for the same job"
aliases: []
domains: [ai]
summary: "In one sponsored test the same price-lookup job used roughly 36,000 to 155,000 context tokens depending on the scraping tool; the video's numbers are inconsistent and one-off."
tags: [context-window, tools, cost, volatile]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_en5a34og
    locator: "05:09"
    quote: "If we looked at the entire Best Buy page, that's over 280,000 tokens."
  - id: src_en5a34og
    locator: "17:30 to 18:02"
    quote: "What does it return? How big is it? And how much is used?"
relations:
  - {rel: about, id: cpt_bpy1s28v}
  - {rel: about, id: cpt_p776cv1f}
verdict: unverified
volatile: true
last_verified: 2026-11-08
---

# The choice of tool changes agent context use several-fold for the same job

Statement: for an identical task, different tools returning different shapes of data (raw page, markdown, JSON of only the needed fields) cause very different context use, cost and accuracy.

## Evidence for
- Presenter's test: price and stock at seven stores. Built-in fetch was blocked on every site but still used 43,000 tokens; a proxy API run picked a wrong price once; pre-built scrapers needed about 70 tool calls; a field-extraction scraper returned small JSON. [fact] (Tech With Tim context video, 05:56 to 11:27; one test, two runs per tool)
- A single page can be huge: the presenter says the Best Buy page alone is over 280,000 tokens. [fact] (video, 05:09)
- Final summary figures: about 155,000 tokens (pre-built), 63,000 (markdown crawler), 58,000 (proxy API) and 36,000 (Scraper Studio); extrapolated at 500 products a week, about $25 to $150. [fact] (video, 14:56 to 15:58; presenter's calculation)

## Evidence against
- Sponsored by the vendor whose tool wins; the other tools were configured by the presenter and results are two runs each. [fact] (video, 04:37 and description)
- Numbers disagree within the video: mid-video /context readings are about 73,000, 73,000, 158,000 and 50,000 tokens; the summary gives 63,000, 58,000, 155,000 and 36,000. [fact] (video, 07:46 to 10:50 versus 14:56)
- Prices were computed by multiplying tokens by a model price, ignoring prompt caching and tool fees. [inference]

## Verdict reasoning
- Unverified, but the direction (tool output size drives context cost) is consistent with the context window concept and the docs-based advice to watch usage; the magnitudes should not be relied on. [inference]
