---
id: src_fuuc8606
schema: 2
type: source
title: "Anthropic's Scion replaces Git (iThome article)"
aliases: []
domains: [programming]
summary: "A Taiwanese news article summarising Anthropic's engineering post on Scion, a server-side version control system for agent-heavy monorepos, with merge counts and checkout-time claims."
tags: [version-control, anthropic, news]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: ent_xkssuk8m}
  - {rel: about, id: clm_uw2nbvpg}
kind: web
reliability: secondary
raw: raw/web/2026-11-08-anthropic-scion-git-ci.md
url: "https://www.ithome.com.tw/news/179733"
author: 李建興
published: "2026-10-16"
volatile: true
last_verified: 2026-11-08
---

# Anthropic's Scion replaces Git (iThome article)

## Takeaways
- Reported: Anthropic spent five months building Scion and migrated its large internal monorepo; the server handles commits, merges and history queries so clients keep only a limited local cache.
- Reported numbers: average about 2,500 merged changes a day in May 2026 and over 30,000 in September; main-branch history close to 100 GB; working copy over 25 GB compressed; CI checks out code about 25 million times a day.
- Reported result per Anthropic's internal measurements: checkout time for CI and research jobs fell from minutes to seconds and CI saved about 25% CPU capacity.
- Anthropic says Scion targets very large repositories and many agents and is not suited to general use; others would need to supply code review, search and CI integration.
- Secondary news summary of a primary post that was not ingested; compare the video summary, which gives a different history size (almost 800 GB).

## Locator map
- Body paragraphs 2-7 (scale, mirrors and shallow clones, server-side design, changesets, measured results, limits). No numbered sections.
