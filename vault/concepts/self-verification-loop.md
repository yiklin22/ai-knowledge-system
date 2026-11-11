---
id: cpt_8ga2cohi
schema: 2
type: concept
title: Self-verification loop
aliases:
- verification loop
- give the agent a check
domains:
- ai
summary: Giving an agent a pass/fail check, with evidence, so it can test its own work before a human reviews it.
tags:
- agents
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_kp4s3ioh
  locator: Give Claude a check to run
  quote: Claude stops when the work looks done.
- id: src_htqxs8h9
  locator: 03:08
  quote: we still need a self verification loop that we can trust in addition to having some kind of code review
- id: src_htqxs8h9
  locator: 05:11
  quote: they're usually not having the agent verify its own changes and then make any fixes depending on what it finds
- id: src_2hzno5ws
  locator: Appendix 1 B. Coding agents
  quote: null
relations:
- rel: related
  id: cpt_24s5izka
- rel: related
  id: cpt_5tf19c1o
- rel: related
  id: cpt_o7t7o69z
recall:
- q: Why does an agent say 'done' when it is not?
  a: It stops when the work looks done; with no pass/fail check to run, 'looks done' is all it has.
- q: Name options for how strictly a check is enforced.
  a: In the prompt, as a goal checked by another model, as a Stop hook enforced by the harness, or reviewed by a fresh agent that did not write the code.
probes:
- q: An agent reports 'all tests pass'. What evidence do you ask for, and why?
  looks_for: The command it ran and its output (or a screenshot); a bare 'all tests pass' tells you little, especially for unattended runs.
misconceptions:
- If the model is good enough, verification is unnecessary (sources say stronger models can also be more likely to misreport success, per one second-hand source).
---

# Self-verification loop

## Knowledge
- If an agent has nothing that returns pass or fail, you become the test suite. With a check it can run, it makes a change, runs the check, reads failures, fixes and repeats.
- Checks can be tests, build exit codes, linters, fixture diffs, or a screenshot compared to a mockup.

## Evidence
- Claude stops when the work looks done; a check gives it something better. [fact] (Claude Code docs, Give Claude a check to run)
- Options run from in-prompt requests to goals to Stop hooks enforced by the harness, or review by a fresh subagent that never saw the conversation. [fact] (Claude Code docs)
- The docs say to ask for evidence: the command and its output, or a screenshot. [fact] (Claude Code docs)
- Anthropic: coding agents work well because solutions are verifiable by tests, but human review remains crucial for system-level fit. [fact] (Anthropic, Appendix 1)
- Amjad: a trusted self-verification loop plus code review is what distinguishes level 1 from level 2; end-to-end verification needs environments (API keys, browsers, accounts) that must be set up. [fact] (Amjad levels video, 03:08-07:14; creator's view)

## Understanding
- The loop works because it replaces the model's judgement of "done" with external ground truth. [inference] (Anthropic also stresses gaining ground truth from the environment at each step)
- Reviewers who are told to find problems will find something, so scope the review to your spec. [fact] (Claude Code docs, Review against your spec)

## Application
- Put the exact test, typecheck and lint commands in the agent's instructions; enforce non-negotiable checks with a hook. [fact] (Claude Code docs)
- Build verification environments for the surfaces you ship; Amjad says they are worth the up-front time because they let you benefit more as agents improve. [fact] (Amjad levels video, 13:26-13:56)

## Uncertainty
- Amjad (second-hand) says stronger models may cheat more and cites a system card not in `raw/`; see [[claim-more-capable-models-may-misreport-success]]. [inference]
- Both main sources are vendor docs or a course seller; there is no independent measurement of how much verification helps. [inference]

## Related
- [[agentic-engineering]] — the discipline this supports.
- [[agent-instruction-files]] — where to record the check command.
- [[multi-agent-orchestration]] — builder, reviewer and verifier roles.
