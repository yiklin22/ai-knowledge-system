---
id: qst_22m9h6sx
schema: 2
type: question
title: "How far can coding agents perceive and act on the physical world?"
aliases: []
domains: [ai]
summary: Beep Locator (microphones) and a webcam-on-a-badge hack suggest agents can be given sensors; how general, reliable and safe is this?
tags: [coding-agents, sensors]
status: reviewed
confidence: low
created: 2026-11-10
updated: 2026-11-10
sources: []
relations:
  - {rel: related, id: cpt_ckqm2sp9}
  - {rel: related, id: clm_emjwdxss}
state: open
---

# How far can coding agents perceive and act on the physical world?

## Why I'm asking
Willison says "Figuring out ways to let coding agents perceive the world around them is a whole lot of fun" (Willison's "Locating the source of a mysterious beep" post, "Giving Claude Code ears"). Two anecdotes (microphones, a webcam) are not a pattern. Which sensor types work, what accuracy is reachable, and how does it compare to a human doing the task?

## What would answer it
- More independent write-ups of agents using physical sensors, with measured results.
- A security view: pushing arbitrary code to remote clients (as with the hot-swap channel) is risky outside a trusted setup; see [[agentic-application-security-risks-owasp-agentic-top-10]].
