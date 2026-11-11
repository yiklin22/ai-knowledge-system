---
id: src_rrz50w6n
schema: 2
type: source
title: "Using Git with coding agents (Simon Willison)"
aliases: []
domains: [programming]
summary: "A chapter of Willison's Agentic Engineering Patterns guide: Git as the safety net for agents, plus prompts for merge conflicts, recovering lost work, bisect and history rewriting."
tags: [git, coding-agents, guide]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: authored_by, id: ent_lh5mezgp}
  - {rel: about, id: cpt_boy7hba5}
  - {rel: about, id: cpt_24s5izka}
kind: web
reliability: secondary
raw: raw/web/2026-11-08-using-git-with-coding-agents-agentic-engineering-patterns.md
url: "https://simonwillison.net/guides/agentic-engineering-patterns/using-git-with-coding-agents/"
author: Simon Willison
published: "2024-11-01"
---

# Using Git with coding agents (Simon Willison)

## Takeaways
- Git records how code changes so mistakes can be investigated and reversed; he says coding agents are fluent in Git, so users need to know what is possible rather than memorise commands.
- A clone carries full history, so agents can explore history without network traffic ("history diving effectively free").
- Suggested uses: start a session by telling the agent to look at recent changes so `git log` seeds its context; ask it to resolve merge conflicts (checking tests pass); find lost work via stash and reflog; run git bisect to find the commit that broke a test; extract a library with history into a new repo.
- Treat history as "a deliberately authored story", editable with agents' help; he finds frontier models write good commit messages.
- The raw file has most inline prompt text stripped by conversion (several list items show only their commands), and the listed date (2024-11-01) is likely the guide's first-published date, not this chapter's; read it as a partial capture.

## Locator map
- Sections: Git essentials; Core concepts and prompts; Rewriting history (Undo or rewrite commits; Building a new repository from scraps of an older one). The capture ends at the last section.
