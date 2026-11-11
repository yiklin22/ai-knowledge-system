---
id: cpt_5tf19c1o
schema: 2
type: concept
title: Agent instruction files (CLAUDE.md)
aliases:
- CLAUDE.md
- AGENTS.md
domains:
- ai
summary: Text loaded into every agent session, best kept short and limited to what the agent cannot work out from the code; hard rules belong in hooks.
tags:
- agents
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_kp4s3ioh
  locator: Deterministic and non-deterministic instructions
  quote: you configure the instruction, and Claude Code (the harness) *has* to execute this.
- id: src_kp4s3ioh
  locator: Keep CLAUDE.md short
  quote: 'How to confirm work in this repo: the exact test, typecheck, and lint commands, and how to run a single test file'
- id: src_kp4s3ioh
  locator: Deterministic and non-deterministic instructions
  quote: no matter what the model decided to do.
relations:
- rel: related
  id: cpt_mta00ls5
- rel: related
  id: cpt_8ga2cohi
recall:
- q: What belongs in CLAUDE.md according to the Claude Code docs?
  a: 'What the agent cannot work out from the code: how to confirm work, misleading places in the code, decisions not in the repo, and anything corrected twice.'
- q: When should a rule be a hook instead of a line in CLAUDE.md?
  a: When it can have no exceptions; instructions in text are decided by the model, while hooks are executed by the harness every time.
probes:
- q: Claude keeps ignoring a line in CLAUDE.md. Is adding IMPORTANT the fix?
  looks_for: 'Probably not: either the file is too long so the line gets lost, or the rule is one that cannot have exceptions and belongs in a hook.'
misconceptions:
- The more instructions you write down the better (the docs say every line takes attention on every task).
---

# Agent instruction files (CLAUDE.md)

## Knowledge
- Instructions are non-deterministic (prompt, CLAUDE.md, skills: the model decides) or deterministic (hooks, deny rules, managed settings: the harness executes).
- A good CLAUDE.md stays short and holds what the agent cannot find in the code.

## Evidence
- Deterministic instructions are configured so the harness has to execute them, whatever the model decided. [fact] (Claude Code docs)
- CLAUDE.md should hold how to confirm work, misleading code, decisions not in the repo and repeated corrections; the memory guide suggests staying under 200 lines. [fact] (Claude Code docs, Keep CLAUDE.md short)
- A test before writing something down: could it find this by reading code, and would it actually look? [fact] (Claude Code docs)
- Amjad moves repeated manual steps into CLAUDE.md or a skill ("task lifecycle"). [fact] (Amjad levels video, 15:31; his practice)

## Understanding
- Every line costs attention on every task, so over-long files dilute the lines that matter. [fact] (Claude Code docs, in paraphrase)
- The split between model-decided and harness-enforced instructions mirrors the guidance to reserve hard rules for hooks. [inference]

## Application
- Record the exact verify command; enforce must-pass checks with a Stop hook. [fact] (Claude Code docs)
- Audit instruction files when models change: docs list advice newer models no longer need. [fact] (Claude Code docs, What you can stop doing)

## Uncertainty
- The documentation is vendor guidance for one product and evolves with models. [inference]

## Related
- [[agent-harness]] — where instruction files are loaded.
- [[self-verification-loop]] — why the check command matters.
