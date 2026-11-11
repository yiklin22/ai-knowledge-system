---
id: qst_rp8337kh
schema: 2
type: question
title: "When is MCP worth its overhead compared with plain function calling?"
aliases: []
domains: [ai]
summary: "The source says MCP is overengineering for one model and a few tools; where is the threshold, given context cost and security surface?"
tags: [mcp, architecture]
status: reviewed
confidence: low
created: 2026-11-10
updated: 2026-11-10
sources: []
relations:
  - {rel: about, id: cpt_p776cv1f}
  - {rel: about, id: cpt_eripv7vv}
state: open
---

# When is MCP worth its overhead compared with plain function calling?

## Why I'm asking
src_mkgdl9kp says the N-by-M integration problem only hurts when both N and M exceed one, and that each server adds a process, a security surface and context tokens (it also reports tool selection degrading after about five servers, as an anecdote).

## What would answer it
- Measurements of tool-selection accuracy versus number of tools, with and without tool search.
- A worked cost comparison for a team with several tools and several models.
