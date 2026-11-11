---
id: cpt_boy7hba5
schema: 2
type: concept
title: "Git worktrees for parallel agents"
aliases: [worktrees, sparse checkout]
domains: [programming]
summary: "Giving each agent its own working copy (a Git worktree) so parallel agents do not overwrite each other, with the catch that merge conflicts can still arise."
tags: [git, parallelism, agents]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_sg6yo57l
    locator: "44:40 to 45:24"
    quote: null
  - id: src_21l5zt28
    locator: "07:57"
    quote: null
  - id: src_c9pkl2fk
    locator: "Example 4, pitfalls"
    quote: null
  - id: src_rrz50w6n
    locator: "Git essentials"
    quote: null
relations:
  - {rel: related, id: cpt_o7t7o69z}
  - {rel: related, id: cpt_zx4myv3t}
  - {rel: related, id: ent_xkssuk8m}
recall:
  - q: What problem do worktrees solve for parallel agent sessions?
    a: Each session works in its own checkout of the code, so agents do not overwrite each other's files while running at the same time.
  - q: What do worktrees not solve?
    a: Merge conflicts when branches are combined; tasks should be split so they touch different files.
---

# Git worktrees for parallel agents

## Knowledge
- A Git worktree is another working directory attached to the same repository, on its own branch; each parallel agent can have one. [inference] (general Git knowledge not stated in the sources in these words; consistent with the sources below)
- Claude Code's desktop app can run parallel sessions; worktrees are off by default in it, need a Git repo, stop sessions overriding each other's files, but merge conflicts can still appear. [fact] (Tech With Tim, 44:52)
- Sparse checkout keeps only needed folders on disk; the Scion video suggests worktrees (e.g. a claude -w flag) plus sparse checkout as the small-scale version of Scion's ideas. [fact] (Andy Lin video, 07:57; creator summary)
- A subagent can be configured with worktree isolation so each invocation gets a fresh worktree; the author advises splitting tasks by package so they do not touch the same files, or letting the main agent merge serially. [fact] (Moksa, blog example 4 and pitfalls)

## Evidence
- Willison: Git clones include full history, so agents can inspect history without network traffic, and agents can resolve merge conflicts and check tests before finalising. [fact] (Willison, Git essentials; Using Git with coding agents)
- Anthropic's scale problem with full clones for every agent and CI job motivated Scion (see the Scion entity); the creator's cited traffic figure is unverified. [fact] (Andy Lin video)

## Understanding
- Worktrees isolate files, not intent: two agents solving overlapping problems still collide at merge time, so task decomposition matters. [inference]

## Application
- For two or more agents on one repo, give each its own worktree and assign non-overlapping areas; review merge order yourself. [inference] (from the sources above)

## Uncertainty
- No measurement of speed-ups or conflict rates is given in these sources. [inference]

## Related
- [[multi-agent-orchestration]], [[claude-code-customization-layers]], [[scion]], [[using-git-with-coding-agents-simon-willison]]
