---
id: src_jj8iamuf
schema: 2
type: source
title: "Self-hosted personal finance dashboard built with Claude Code (Kevin Kinnett)"
aliases: []
domains: [programming]
summary: "A developer's account of building a large self-hosted finance app in 12 days with Claude Code, with lessons about design, early tests and scope."
tags: [case-study, claude-code, personal-software]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: ent_7kkj45y4}
  - {rel: related, id: cpt_24s5izka}
kind: web
reliability: opinion
raw: raw/web/2026-11-08-how-i-built-a-self-hosted-personal-finance-dashboard-with-cl.md
url: "https://www.kevinkinnett.com/posts/self-hosted-personal-finance-dashboard-claude-code/"
author: Kevin Kinnett
published: "2026-04-11"
---

# Self-hosted personal finance dashboard built with Claude Code (Kevin Kinnett)

## Takeaways
- Self-reported scale: first commit 30 March 2026, 132 commits in twelve days, about 45,000 lines of TypeScript, 27 pages, 30 API route files, 40+ tables, every commit co-authored with Claude Code. Not independently verifiable.
- Stack is conventional (React, Node, PostgreSQL, Docker, GitHub Actions, Tailscale); data pipeline (ingestion, rule then LLM categorisation, deduplication) is described as the real heart of the app.
- Workflow: the author keeps architecture, schema and feature choices; Claude writes migrations, routes and scaffolding; he reviews. The claim is that Claude Code changed speed, not responsibility.
- What he would change: design the data model before building many pages, write tests earlier, and be stricter about scope, because cheap implementation makes overbuilding easy.
- A single anecdote from one practitioner; no cost, bug rate or maintenance data. It does show the same human-keeps-judgement pattern that appears in other sources.

## Locator map
- Sections: Why I built it; What shipped in 12 days; The stack; The data pipeline; Claude Code changed the speed, not the responsibility; Self-hosting; What I would do differently.
