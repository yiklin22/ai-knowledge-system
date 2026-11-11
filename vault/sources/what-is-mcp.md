---
id: src_mkgdl9kp
schema: 2
type: source
title: "What is MCP?"
aliases: []
domains: [ai]
summary: "Explainer of the Model Context Protocol: the N-by-M integration problem, the host/client/server architecture with tools, resources and prompts, adoption by major vendors, and security and context-cost drawbacks."
tags: [mcp, protocol, tools, security]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources: []
relations:
  - {rel: authored_by, id: ent_xqueox2g}
  - {rel: about, id: cpt_p776cv1f}
kind: web
reliability: secondary
raw: raw/web/2026-11-10-what-is-mcp.md
url: "https://theaiengineer.substack.com/p/what-is-mcp"
author: "Paolo Perrone"
published: "2026-02-25"
volatile: true
last_verified: 2026-11-10
---

# What is MCP?

## Takeaways
- [fact] MCP is an open standard so a tool is wrapped once as an MCP server and any MCP-speaking model can use it; it still uses function calling underneath.
- [fact] Architecture: Host (the AI app), Client (inside the host, manages connections), Server (exposes Tools, Resources, Prompts) over JSON-RPC 2.0, modelled on the Language Server Protocol.
- [fact] Adoption claims as of early 2026: OpenAI, Google and Microsoft adopted it; Anthropic donated it to the Linux Foundation's Agentic AI Foundation in December 2025; 97 million monthly SDK downloads.
- [fact] Drawbacks: tool poisoning (84% success in controlled tests with auto-approval), 43% of public servers with command-injection flaws, and tool definitions consuming context (the author's own anecdote: tool selection degraded after five servers).
- [fact] The author's stated view: not every project needs MCP; with one model and a few tools plain function calling is enough.

## Locator map
- "TL;DR": three-point summary.
- "How MCP Actually Works": roles and primitives.
- "Who's Using It (Everyone)": adoption figures.
- "What Can Go Wrong (and What's Overhyped)": three risks and "My Take".
- Footnotes 1-4: spec, donation announcement, New Stack analysis, security data sources.

## Reliability
Secondary explainer. Adoption and security figures come from third-party blogs (Invariant Labs, Composio, The New Stack); they are volatile and were not verified here.
