---
id: cpt_g7oflf5s
schema: 2
type: concept
title: "Probe-plan-teach AI tutoring loop"
aliases: [adaptive AI tutor, learner-model tutoring]
domains: [learning]
summary: "A pattern for AI-assisted learning: first measure what the learner knows with quizzes, then plan a path as a visible graph, then teach one reasoning step at a time with periodic checks."
tags: [learning, tutoring, agents]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_co7342di
    locator: "04:49"
    quote: "We want to maximize struggle."
  - id: src_co7342di
    locator: "06:26"
    quote: "the actual reason I implemented it is to actually force the AI to reason everything out"
  - id: src_co7342di
    locator: "05:22 to 07:28"
    quote: null
relations:
  - {rel: introduced_in, id: src_co7342di}
  - {rel: related, id: cpt_5tf19c1o}
recall:
  - q: What are the three phases of the loop?
    a: Probe (quiz to map what the learner knows), plan (reason out the path and show it as a graph), teach (one reasoning step at a time with periodic quizzes).
  - q: Why does the presenter want the plan drawn as a diagram?
    a: Partly so the learner sees what is coming, and mainly to force the AI to reason out the whole path rather than improvise.
  - q: Where should "struggle" be, according to the presenter?
    a: In the material itself, not in logistics, planning, finding resources, verifying facts or deciding what to learn next.
probes:
  - q: Why quiz the learner periodically during teaching, if the AI already probed at the start?
    looks_for: Illusion of understanding when learning with AI, calibration of the system's model of the learner, and the learning benefit of applying the material.
---

# Probe-plan-teach AI tutoring loop

## Knowledge
- Phase 1, probe: a quiz tool asks graded multiple-choice questions, starting broad and narrowing like a binary search to map the learner's understanding of each prerequisite strand. [fact] (Alvar video, 05:22 to 05:54; presenter's design)
- Phase 2, plan: the system reasons out how to teach this person this topic, starts verification and fact-checking sub-agents, and shows the plan as a Mermaid graph. [fact] (Alvar video, 05:54 to 06:26)
- Phase 3, teach: one reasoning step at a time, with periodic quizzes; he calls rushing through the whole thing a common failure of ordinary chat. [fact] (Alvar video, 06:56 and 13:43 to 14:13)
- Two principles: optimise the teaching and allocate mental effort to the material, not to logistics. [fact] (Alvar video, 04:18 to 04:49)

## Evidence
- Reasons given for feedback quizzes: self-deception about understanding, calibration of the system, and practice helping the learning lock in. [fact] (Alvar video, 06:56 to 08:00; presenter's reasoning)
- The demo covered differential forms for one learner and did not measure outcomes; the presenter notes a dying diagram sub-agent and AI-sounding style. [fact] (Alvar video, 16:49)
- The claim that one adaptive teacher beats many sources rests on his reasoning and an untested illustration about trust. [fact] (Alvar video, 00:32 to 03:47)

## Understanding
- The design moves the work of finding, ordering and checking material from the learner to the system so effort goes to understanding. [inference] (from the stated principles)
- A learner model built from quiz answers is the key ingredient; without it the tutor reverts to generic explanation. [inference]

## Application
- Start any learning session with a short diagnostic quiz and a visible plan; ask the tutor to teach in small steps and check understanding often. [inference]
- This vault's Socratic tutor skill (grounded in vault pages and mastery records) follows a similar spirit; compare before changing it. [inference] (project context, not from the source)

## Uncertainty
- No evidence of learning gains, only a demo and arguments. [fact] (source page)
- Whether quality depends mostly on model strength or on the teaching style is claimed but untested. [speculation]

## Related
- [[how-i-use-ai-to-learn-things-eero-alvar-video]], [[agent-instruction-files]]
