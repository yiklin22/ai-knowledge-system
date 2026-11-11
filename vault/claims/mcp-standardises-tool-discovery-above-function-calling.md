---
id: clm_9mxxh68s
schema: 2
type: claim
title: "MCP standardises tool discovery above function calling"
aliases: []
domains: [ai]
summary: "MCP does not replace function calling: the model still calls tools through its provider's tool-calling format, while MCP standardises how tools are hosted, discovered and described across models."
tags: [mcp, function-calling]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources:
  - id: src_mkgdl9kp
    locator: "Why Function Calling Breaks Down, Confusion Alert"
    quote: "Your LLM still uses tool calling under the hood."
  - id: src_ixuklw02
    locator: "The Relationship: Function Calling → Tool Use → MCP"
    quote: null
relations:
  - {rel: about, id: cpt_p776cv1f}
  - {rel: about, id: cpt_eripv7vv}
  - {rel: supports, id: cpt_p776cv1f}
verdict: supported
---

# MCP standardises tool discovery above function calling

## Evidence for
- [fact] Both articles by the same author describe MCP as the standardisation layer: function calling is how a model invokes a tool, MCP is how tools are discovered and shared. (src_mkgdl9kp, src_ixuklw02)
- [fact] MCP's roles (host, client, server) and primitives (tools, resources, prompts) are described in src_mkgdl9kp.

## Evidence against
- [inference] Both sources are the same author, so this is one view, not independent corroboration; the MCP specification itself was not read.

## Verdict reasoning
Supported as a description consistent with existing vault knowledge ([[tool-use-and-function-calling]]), but single-author. Confidence kept at medium for an uncontroversial architectural statement.
