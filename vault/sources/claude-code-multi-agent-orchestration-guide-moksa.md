---
id: src_c9pkl2fk
schema: 2
type: source
title: "Claude Code multi-agent orchestration guide (Moksa)"
aliases: []
domains: [ai]
summary: "A Chinese-language blog tutorial on Claude Code subagents: built-in subagents, scope priority, seven config examples, worktree isolation, cost tiering and pitfalls, with unsourced performance numbers."
tags: [claude-code, subagents, tutorial, blog]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: cpt_zx4myv3t}
  - {rel: about, id: cpt_o7t7o69z}
  - {rel: about, id: clm_3idqb7tq}
kind: web
reliability: opinion
raw: raw/web/2026-11-08-claude-code-multi-agent-orchestration-5-scope-7-moksa-web.md
url: "https://moksaweb.com/claude-code-multi-agent-orchestration/"
author: Moksa
published: "2026-04-22"
volatile: true
last_verified: 2026-11-08
---

# Claude Code multi-agent orchestration guide (Moksa)

## Takeaways
- Explains subagents as specialised assistants with their own context window, system prompt, tool permissions and model; the main agent delegates, and only a result summary returns, which keeps the main context small.
- Lists built-in subagents (Explore on Haiku, read-only; Plan; General-purpose) and a five-level scope priority for custom ones (managed settings, --agents flag, project .claude/agents, user ~/.claude/agents, plugin).
- Pitfalls: subagents cannot spawn subagents; vague descriptions prevent delegation; giving all tools defeats isolation; worktree isolation still needs a merge plan; persistent memory can go stale; cost can rise if the wrong model is used.
- The author's performance numbers (three times cheaper, 3-5 times faster, 60-70% lower token cost, 4-6 hour sessions) are attributed to personal experience and "Reddit observations" with no data. The model IDs used in examples are older generations and date the article (April 2026).
- Configuration snippets are examples written by the author, not copied from official documentation; verify against Claude Code docs before use.

## Locator map
- §1 definition and context preservation; §2 built-in subagents; §3 five scopes; §4 seven examples (custom definition, --agents flag, planner-coder-reviewer, worktree isolation, hooks, cost tiers, persistent memory); §5 pitfalls; §7 FAQ.
