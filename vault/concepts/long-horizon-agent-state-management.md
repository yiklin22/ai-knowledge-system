---
id: cpt_zbtvdo2y
schema: 2
type: concept
title: "Long-horizon agent state management"
aliases: [multi-window workflows, agent progress notes]
domains: [ai]
summary: "How to keep an agent oriented across many context windows: tests in a structured file, free-text progress notes, git as a checkpoint log, and a deliberate choice between fresh start and compaction."
tags: [agents, state, context]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_t2ajgzb6
    locator: "Agentic systems, State management best practices"
    quote: "Use git for state tracking"
  - id: src_t2ajgzb6
    locator: "Workflows across multiple context windows"
    quote: null
  - id: src_sg6yo57l
    locator: "40:18 to 43:19"
    quote: null
relations:
  - {rel: related, id: cpt_bpy1s28v}
  - {rel: related, id: cpt_mta00ls5}
  - {rel: related, id: cpt_24s5izka}
  - {rel: related, id: cpt_8ga2cohi}
recall:
  - q: What goes in a structured file and what in free-text notes for a multi-window task?
    a: Structured data such as test status goes in JSON (for example tests.json); general progress and context go in free-text notes (for example progress.txt).
  - q: Why might you start a fresh context window instead of compacting?
    a: Recent models discover state well from the filesystem, git logs and notes, so a clean start with explicit orientation steps can beat a lossy summary.
  - q: Why does the guide tell the model not to remove or edit tests?
    a: Removing tests can hide missing or buggy functionality, so they act as a stable checklist across windows.
---

# Long-horizon agent state management

## Knowledge
- Across several context windows, use the first window to set up a framework (write tests, create setup scripts) and later windows to iterate on a to-do list. [fact] (Claude prompting docs, vendor)
- Keep structured state (test results, task status) in JSON, free-form progress in text notes, and git for a log and restorable checkpoints. [fact] (Claude prompting docs)
- When a window is cleared, consider a brand-new window over compaction, and be prescriptive about how it starts (read progress notes, tests file and git logs; run a basic integration test). [fact] (Claude prompting docs)
- Tell the model that context will be compacted so it does not stop early or rush near the limit; save state before the window refreshes. [fact] (Claude prompting docs)
- Manual management commands in Claude Code include /context, /clear, /compact and /rewind. [fact] (Tech With Tim, 40:18 to 44:40)

## Evidence
- The docs give a sample tests.json and progress.txt and say the models "perform especially well" using git to track state across sessions. [fact] (Prompting best practices; vendor claim, not measured in the page)
- Tech With Tim reports compacting a 154,000-token window to 92,000 with a displayed "saved 137,000" figure that he says he cannot reconcile, a reminder to check numbers. [fact] (video, 42:17 to 42:47)
- The docs' advice about telling the model that compaction exists applies to certain models (context-aware ones); the page says model-specific advice should be re-tested. [fact] (Prompting best practices)

## Understanding
- State kept outside the window (files, git, tests) survives resets; state kept only in conversation does not. [inference]
- Tests double as state and as protection: a stable list of checks tells a fresh window what "done" means. [inference]

## Application
- For multi-hour tasks: write tests first, keep a progress file, commit often, and start new windows with an explicit orientation checklist. [fact] (docs)
- Check /context before long tasks to see what already fills the window. [fact] (Tech With Tim)

## Uncertainty
- Advice is vendor documentation for Claude models and depends on current model behaviour; it may change. [inference]
- No data compares fresh start with compaction. [inference]

## Related
- [[context-window-and-compaction]], [[agent-harness]], [[agentic-engineering]], [[self-verification-loop]]
