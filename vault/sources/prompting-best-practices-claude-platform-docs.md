---
id: src_t2ajgzb6
schema: 2
type: source
title: "Prompting best practices (Claude Platform docs)"
aliases: []
domains: [ai]
summary: "Anthropic's reference on prompting current Claude models: clarity, examples, XML tags, long context, formatting, tools, thinking and effort, and agentic prompts for state, autonomy and subagents."
tags: [prompting, documentation, vendor, volatile]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: cpt_be51ajjr}
  - {rel: about, id: cpt_zbtvdo2y}
kind: web
reliability: vendor
raw: raw/web/2026-11-08-prompting-best-practices.md
url: "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices"
author: Anthropic
published: "2025-09-29"
volatile: true
last_verified: 2026-11-08
---

# Prompting best practices (Claude Platform docs)

## Takeaways
- Vendor documentation for Claude models, so advice is about Claude's behaviour; it warns to treat any model-specific technique as measured on that model and re-check with your own evals.
- General: be explicit and treat the model like a capable new colleague with no context; explain why an instruction exists; use diverse examples in tags; structure with XML tags; put long documents at the top and ask for quotes first; say what to do rather than what not to do.
- Thinking: recent models use adaptive thinking controlled by an effort setting; manual token budgets are deprecated or rejected on newer models; general instructions ("think thoroughly") often beat prescriptive steps; prefill on the last assistant turn is no longer supported on newer models.
- Agentic: for tasks across multiple context windows, keep tests in a structured file, progress notes in text, use git for state, and consider a fresh window over compaction; confirm before destructive or hard-to-reverse actions; use subagents only for parallel, isolated or independent work; reduce overeagerness and test-gaming with explicit prompts.
- Capture is partial in my reading: sections 1-240 and 326-595 (of 712 lines) were read; the formatting migration table, frontend design, medication-dosing and migration sections were skimmed only by heading. Model names and API behaviours here are volatile.

## Locator map
- Model-specific guidance table; General principles; Output and formatting; Tool use; Thinking and reasoning (Overthinking, adaptive thinking); Agentic systems (long-horizon state, autonomy and safety, subagent orchestration, overeagerness, hardcoding tests, hallucinations); Capability-specific tips; Migration.
