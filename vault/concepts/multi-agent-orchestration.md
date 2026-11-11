---
id: cpt_o7t7o69z
schema: 2
type: concept
title: Multi-agent orchestration
aliases:
- agent swarms
- subagents
domains:
- ai
summary: 'Structures for using several agents: fan-out, effort scaling, builder-reviewer-verifier pairs, manager threads and swarms.'
tags:
- agents
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_8s1mxx4c
  locator: 01:38
  quote: the first rung of the ladder is to have one agent with a clear goal and a way for it to check its own work
- id: src_8s1mxx4c
  locator: 03:44
  quote: are actually overusing subagents when a single agent would have done a better job instead
- id: src_kp4s3ioh
  locator: Know what subagents cost
  quote: What they cost you is mostly tokens, since every subagent sends its own requests and they count against the same usage as your main conversation.
- id: src_8tz2b8u3
  locator: Measuring coordination
  quote: the simple independent parallelized method produces 21 vulnerabilities over a 6.5 million token run, while the coordinating agent swarm found 266 vulnerabilities over a 27 million token run.
relations:
- rel: broader
  id: cpt_9ug6lxd3
- rel: prerequisite_for
  id: cpt_5s6mnu9b
- rel: related
  id: cpt_8ga2cohi
recall:
- q: When is fan-out to subagents appropriate?
  a: When the pieces of work are truly independent (e.g. researching five libraries separately); tangled work does worse.
- q: What do subagents cost, according to the Claude Code docs?
  a: Mostly tokens; each subagent sends its own requests, and a fresh one must gather context, so it can even be slower.
probes:
- q: Someone splits a spec into ten tickets and runs ten subagents in parallel. What might go wrong?
  looks_for: Work can be tangled in ways not expected; second-hand claims say this helped older models but not newer ones; coordination conflicts and abandoned PRs appear in Anthropic's swarm tests.
misconceptions:
- 'More subagents always means a smarter answer (docs: you get parallelism or a fresh pair of eyes, not a smarter answer).'
---

# Multi-agent orchestration

## Knowledge
- Rungs described in a creator's recap of an OpenAI talk: one agent with a goal and a check; fan-out; effort scaling; pairs; manager thread; long-lived leads; swarms.
- Subagents help with independent work, keeping long output out of the main conversation, and giving a reviewer that has not seen how the code was written.

## Evidence
- Claude Code docs: subagents pay off for parallel independent work, isolating long output, fresh reviewers and tool-limited reviewers; cost is mostly tokens and can add latency. [fact] (Claude Code docs, Know what subagents cost)
- Amjad: Anthropic finds people overuse subagents when one agent would do better; splitting specs into tickets for subagents is bad advice for newer models. [fact] (Amjad loops video, 03:44; second-hand, the Anthropic article is not in `raw/`)
- Amjad's builder-reviewer-verifier setup caps review rounds at 3 and verification rounds at 2. [fact] (Amjad loops video, 07:47-09:05; his own practice)
- Anthropic's swarm test: 266 vulnerabilities over a 27M-token run versus 21 over 6.5M tokens for independent agents, with only 12 in common. [fact] (Anthropic multiagent, Measuring coordination) See [[claim-coordinating-swarms-found-more-vulnerabilities]].
- Anthropic: agents coordinate well when treated like tool calls with clear inputs and outputs, and stumble as long-lived peers. [fact] (Anthropic multiagent)

## Understanding
- The useful question is whether the work is truly independent; if not, extra agents add coordination cost without extra intelligence. [inference]
- Roles (builder, reviewer, verifier) make sense because a fresh reviewer is not swayed by the builder's reasoning. [inference] (supported by Claude Code docs on fresh reviewers)

## Application
- Use a single agent by default; fan out only for independent work; use cheaper models for self-contained subtasks. [inference] (docs mention Haiku for simple subagents)
- Sending fixes back to the same builder was 38% cheaper in the creator's replay of about 10 PRs; treat that as an anecdote. [fact] (Amjad loops video, 09:39) See [[claim-fixing-findings-with-the-same-builder-is-cheaper]].

## Uncertainty
- Much of this is from one course seller recapping other people's material. [inference]
- Anthropic says true multi-agent systems are in their infancy. [fact] (Anthropic multiagent)

## Related
- [[multi-agent-failure-modes]] — what goes wrong.
- [[workflows-versus-agents]] — the single-agent baseline.
- [[self-verification-loop]] — how pairs check each other.
