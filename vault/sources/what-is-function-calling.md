---
id: src_ixuklw02
schema: 2
type: source
title: "What is Function Calling?"
aliases: []
domains: [ai]
summary: "Explainer of function calling as the 'act' step of an agent: the five-step JSON-schema flow, how it relates to tool use and MCP, and its production pitfalls (context cost, argument extraction, security, error handling)."
tags: [function-calling, tool-use, agents]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources: []
relations:
  - {rel: authored_by, id: ent_xqueox2g}
  - {rel: about, id: cpt_eripv7vv}
kind: web
reliability: secondary
raw: raw/web/2026-11-10-what-is-function-calling.md
url: "https://theaiengineer.substack.com/p/what-is-function-calling"
author: "Paolo Perrone"
published: "2026-03-11"
---

# What is Function Calling?

## Takeaways
- [fact] Flow: define tools as JSON schemas, send them with the user message, the model returns structured tool calls (possibly several), your code executes them and returns results, the model writes the final answer. The model never touches your APIs itself.
- [fact] Terminology: function calling (OpenAI, June 2023) is provider-specific; tool use is the broader term (Anthropic's); MCP standardises discovery and hosting of tools.
- [fact] Pitfalls: definitions consume context (58 tools about 55,000 tokens, per internal testing cited second-hand), ambiguous arguments, security enforced by your execution layer, under-specified error handling.
- [fact] The article's closing framing: function calling is the model generating JSON that matches a schema.
- Stripe and Shopify Sidekick examples are described without primary citations (footnote links only to blog posts).

## Locator map
- "How Function Calling Actually Works": steps 1-5.
- "The Relationship: Function Calling → Tool Use → MCP".
- "What Can Go Wrong (and What's Overhyped)".

## Reliability
Secondary explainer. Company examples (Stripe, Shopify, Cursor request volume) are unverified second-hand claims.
