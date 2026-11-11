---
id: cpt_p776cv1f
schema: 2
type: concept
title: "Model Context Protocol (MCP)"
aliases: [MCP]
domains: [ai]
summary: "An open protocol for connecting AI models to external tools and data through standalone servers; it sits above function calling, adds discoverability and reuse, and brings context-cost and security surfaces."
tags: [tools, protocol, agents]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-10
sources:
  - id: src_sg6yo57l
    locator: "34:55 to 35:37"
    quote: "MCP stands for model context protocol"
  - id: src_03op7psf
    locator: "Agents section"
    quote: "make essentially arbitrary tool calls (that you set up) through MCP"
  - id: src_7yi1bz2z
    locator: "p.12, ASI02 Description"
    quote: "tool definitions increasingly come via MCP servers, creating a natural overlap with ASI04"
  - id: src_136f4it1
    locator: "Lesson table, lesson 11"
    quote: null
  - id: src_mkgdl9kp
    locator: "TL;DR"
    quote: "One MCP server, every AI model. Think USB-C for AI."
  - id: src_mkgdl9kp
    locator: "How MCP Actually Works"
    quote: "The protocol itself uses JSON-RPC 2.0."
  - id: src_ixuklw02
    locator: "The Relationship: Function Calling → Tool Use → MCP"
    quote: null
relations:
  - {rel: related, id: cpt_eripv7vv}
  - {rel: related, id: cpt_f92yye3m}
  - {rel: related, id: cpt_zx4myv3t}
  - {rel: related, id: cpt_bpy1s28v}
  - {rel: related, id: cpt_od52gsyk}
  - {rel: related, id: qst_rp8337kh}
recall:
  - q: What does an MCP server give an agent?
    a: A way to reach external tools and data; its tool definitions are loaded into the agent's context so the model can call them.
  - q: Why can an MCP server be a security risk as well as a convenience?
    a: Tool descriptors and schemas come from the server, so a poisoned or malicious server can steer which tools the agent calls; OWASP flags this overlap between tool misuse and supply chain risk.
  - q: What are MCP's three roles and three server primitives?
    a: Roles are host (the AI app), client (manages connections inside the host) and server (exposes the tool); primitives are tools, resources and prompts.
  - q: What problem does MCP solve, and when is it overkill?
    a: The N-by-M integration explosion between models and tools; it is overkill for one model with a few tools, where plain function calling suffices.
---

# Model Context Protocol (MCP)

## Knowledge
- MCP ("model context protocol") is a way for an agent to communicate with other tools; popular services provide MCP servers, and in Claude you can add one by declaring a server URL and name, or just ask the agent to add it. [fact] (Tech With Tim, 34:55 to 35:37; presenter's description)
- Agents can make tool calls you set up through MCP, alongside Unix tools, Git, linters and test runners. [fact] (Ptacek)
- Tool definitions increasingly come via MCP servers, which creates overlap between tool misuse (ASI02) and supply-chain risk (ASI04). [fact] (OWASP p.12)
- Microsoft's agents course lists "Using Agentic Protocols (MCP, A2A and NLWeb)" as lesson 11; the lesson content was not ingested. [fact] (course README)
- MCP is an open standard intended to remove the N-by-M problem: one MCP server per tool, usable by every model that speaks MCP. [fact] (The AI Engineer, "What is MCP?")
- Architecture: a host (the AI application), a client inside the host that manages connections, and a server exposing three primitives: tools (actions), resources (readable data) and prompts (reusable templates); messages use JSON-RPC 2.0, and the design was inspired by the Language Server Protocol. [fact] (The AI Engineer, "What is MCP?")
- MCP does not replace function calling: the model still uses tool calling, and MCP standardises how tools are defined and discovered across models. [fact] (The AI Engineer, both MCP and function-calling articles; see [[mcp-standardises-tool-discovery-above-function-calling]])
- Adoption as reported in early 2026: adopted by OpenAI, Google and Microsoft; donated by Anthropic to the Linux Foundation's Agentic AI Foundation in December 2025; about 97 million monthly SDK downloads. [fact] (The AI Engineer; volatile, last verified 2026-11-10, second-hand)

## Evidence
- The Claude /context breakdown lists MCP tools and MCP server instructions among the items that fill the context before any message is typed. [fact] (Tech With Tim context video, 00:44 to 01:32)
- OWASP's tool-poisoning scenario: an attacker compromises MCP tool descriptors, schemas or routing metadata so the agent invokes a tool on falsified capabilities. [fact] (OWASP p.13)
- Reported figures (secondary, unverified here): tool poisoning succeeded 84% of the time in controlled tests with auto-approval ([[mcp-tool-poisoning-succeeded-84-percent-with-auto-approval]]); 43% of public MCP servers contained command-injection flaws; CVE-2025-6514 in mcp-remote affected over 558,000 installs. [fact] (The AI Engineer, "What is MCP?")

## Understanding
- Every connected tool adds definitions to the context (cost, distraction) and adds something an attacker can try to influence, so more tools is not automatically better. [inference] (combines the context-window and OWASP sources)
- The context video's audit questions (what does it return, how big, how much is used) apply to MCP tools as much as to scrapers. [inference]
- The author reports Cursor caps tools at 30, and an on-demand tool discovery approach ("Code Mode") claiming 98%+ token savings at some latency cost; the author's own anecdote is that tool selection degraded after about five servers. [fact] (The AI Engineer; anecdote and vendor-reported figure)

## Application
- Connect only the servers a task needs; check /context before and after adding one. [inference]
- Treat third-party servers like dependencies: review who publishes them and what they can reach. [inference] (OWASP supply chain framing)
- With one model and a few tools, plain function calling may be simpler than running MCP servers. [fact] (The AI Engineer's engineering lesson); the threshold is an open question: [[when-is-mcp-worth-its-overhead-compared-with-plain-function-calling]].

## Uncertainty
- The protocol's specification, authentication model and versions are not covered by any source read here beyond one explainer's summary (it mentions specification version 2025-11-25 without our having read it). [inference]
- Adoption and security statistics come from a single newsletter's second-hand citations and change quickly. [inference]

## Related
- [[tool-use-and-function-calling]], [[agentic-application-security-risks-owasp-agentic-top-10]], [[claude-code-customization-layers]], [[context-window-and-compaction]], [[agent-guardrails-and-defense-in-depth]]
