---
id: cpt_zx4myv3t
schema: 2
type: concept
title: "Claude Code customization layers"
aliases: [Claude Code extension points, skills subagents hooks plugins]
domains: [ai]
summary: "The ways to shape Claude Code: CLAUDE.md and memory files, settings and permissions, skills, subagents, MCP servers, hooks, plugins and mods, with a rule for which to choose."
tags: [claude-code, harness, configuration]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_sg6yo57l
    locator: "27:03 skills"
    quote: "a skill is just a markdown file, which is a reusable set of instructions that you can give to Claude"
  - id: src_sg6yo57l
    locator: "36:07 hooks"
    quote: "Claude doesn't choose to run it, the harness fires it every time the event occurs."
  - id: src_sg6yo57l
    locator: "38:44 plugins"
    quote: "plugins are basically a bundle of potentially all of these things together"
  - id: src_c9pkl2fk
    locator: "§3 five scopes"
    quote: null
  - id: src_t2ajgzb6
    locator: "Subagent orchestration"
    quote: "Use subagents when tasks can run in parallel, require isolated context, or involve"
relations:
  - {rel: about, id: ent_7kkj45y4}
  - {rel: related, id: cpt_mta00ls5}
  - {rel: related, id: cpt_5tf19c1o}
  - {rel: related, id: cpt_o7t7o69z}
  - {rel: related, id: cpt_p776cv1f}
  - {rel: related, id: clm_pdp2tu9p}
recall:
  - q: What is the difference between an instruction in CLAUDE.md and a hook?
    a: CLAUDE.md is text the model reads and may or may not follow; a hook is a command the harness runs on an event regardless of what the model decides.
  - q: What is a skill, and when should you write one?
    a: A markdown file of reusable instructions; write one when you keep re-explaining the same steps or format.
  - q: What does a subagent protect, and what is the cost of giving it too many tools?
    a: It keeps exploratory output out of the main context window; with every tool granted it no longer isolates anything.
probes:
  - q: You want tests to run every time the agent finishes. Where does that rule belong, and why?
    looks_for: In a hook (event-triggered, enforced by the harness), not only in CLAUDE.md, because model-read instructions are not guaranteed to run.
---

# Claude Code customization layers

## Knowledge
- CLAUDE.md is read at the start of every session; /init generates one; nested files apply to sub-directories. Memory is stored as files, per project, outside the repo unless you ask otherwise. [fact] (Tech With Tim, 16:57 to 23:13)
- settings.json (global or project) holds permissions such as allow, ask and deny lists. [fact] (Tech With Tim, 24:15)
- Skills are reusable markdown instruction files, global or project-level, invoked by slash command; subagents are separate assistants with their own context, prompt, tools and model; hooks fire on events and are run by the harness; plugins bundle skills, MCP servers, subagents and configuration; mods are harness-level customisations shipped inside plugins. [fact] (Tech With Tim)
- A custom subagent can live in five scopes with a priority order: managed settings, --agents flag, project .claude/agents, user ~/.claude/agents, plugin. [fact] (Moksa, blog; the order is not checked against official docs)

## Evidence
- Anthropic's own docs, per the existing vault page, distinguish instructions the model decides to follow from hooks the harness executes. [fact] (see the hooks claim page)
- Anthropic prompting docs: use subagents when work can run in parallel, needs isolated context or is independent; avoid them for simple, sequential or single-file edits. [fact] (Prompting best practices)
- Moksa lists pitfalls: vague subagent descriptions prevent delegation, granting all tools removes the isolation benefit, subagents cannot spawn subagents. [fact] (Moksa §5; blog)
- The Tech With Tim walkthrough is sponsored by Anthropic and recorded at one date; product behaviour changes (for example the presenter says the /agents wizard had been removed). [fact] (video, 32:32)

## Understanding
- Pick the lightest layer that does the job: facts and conventions in CLAUDE.md, repeatable procedures in skills, hard rules in hooks, isolation in subagents, external capabilities in MCP. [inference] (synthesis of the sources above)
- Every layer that loads text adds to the context window, so more configuration has a cost. [inference]

## Application
- Put must-happen rules (formatting, tests, secret protection) in hooks. [fact] (docs, via hooks claim; Tech With Tim examples)
- Write a skill when you notice repeating the same instructions. [fact] (Tech With Tim)
- Give subagents only the tools they need. [fact] (Moksa)

## Uncertainty
- Names, commands and scopes change frequently; treat details as volatile and confirm in current docs. [inference]
- Cost and speed numbers from creators are unverified. [inference]

## Related
- [[claude-code]], [[agent-harness]], [[agent-instruction-files]], [[claim-hooks-enforce-rules-deterministically]], [[multi-agent-orchestration]], [[model-context-protocol-mcp]], [[git-worktrees-for-parallel-agents]]
