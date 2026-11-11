---
id: clm_y5xuvs0n
schema: 2
type: claim
title: "MCP tool poisoning succeeded 84 percent with auto-approval"
aliases: []
domains: [ai]
summary: "Hidden instructions in MCP tool metadata reportedly succeeded 84% of the time in controlled tests where agents auto-approved tool use; reported second-hand and not production data."
tags: [mcp, security, tool-poisoning]
status: reviewed
confidence: low
created: 2026-11-10
updated: 2026-11-10
volatile: true
last_verified: 2026-11-10
sources:
  - id: src_mkgdl9kp
    locator: "What Can Go Wrong, item 1"
    quote: "In controlled testing, tool poisoning attacks achieved 84% success rates when agents had auto-approval enabled"
relations:
  - {rel: about, id: cpt_p776cv1f}
  - {rel: related, id: cpt_f92yye3m}
verdict: unverified
---

# MCP tool poisoning succeeded 84 percent with auto-approval

## Evidence for
- [fact] The source says tool poisoning embeds hidden instructions in tool metadata, that merely loading the tool into context suffices, and that OWASP published an MCP-specific Top 10 (beta). (src_mkgdl9kp)
- [fact] Its footnote credits Invariant Labs' MCPTox benchmark and states the rate comes from controlled testing, not production. (src_mkgdl9kp)

## Evidence against
- [inference] The figure depends on the tested models, prompts and settings; the footnote links were not read, so the 84% cannot be confirmed here.

## Verdict reasoning
Unverified. Treat as an indication that auto-approval with untrusted servers is risky, not as a general rate.
