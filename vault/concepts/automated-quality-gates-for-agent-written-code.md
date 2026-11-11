---
id: cpt_hooaxuqi
schema: 2
type: concept
title: "Automated quality gates for agent-written code"
aliases: [verification over review, test constraints for agents]
domains: [programming]
summary: "Machine-checked constraints (tests, complexity-times-coverage metrics such as CRAP, mutation testing, agent-run verification with evidence) used to trust agent-written code without reading every line."
tags: [verification, testing, code-review, agents]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_cjg71ax2
    locator: "Description: 查證與更正"
    quote: "CRAP 全名 Change Risk Anti-Patterns"
  - id: src_gt6qwx4i
    locator: "Description: question 2"
    quote: "寫的人不能判自己過關"
  - id: src_opi2fpk9
    locator: "slide 022-023"
    quote: "Any code that you write has to have been routed through a coding agent."
  - id: src_03op7psf
    locator: "'Read the code' section"
    quote: "If you build something with an LLM that people will depend on, read the code."
relations:
  - {rel: related, id: cpt_8ga2cohi}
  - {rel: related, id: cpt_24s5izka}
  - {rel: related, id: clm_tfabt24p}
  - {rel: related, id: clm_blkj2ekk}
  - {rel: about, id: ent_gkjlm2x9}
recall:
  - q: What does the CRAP metric combine?
    a: Cyclomatic complexity (number of branches) with test coverage; at complexity 10 the creator's worked values are 110 with no tests, 22.5 at half coverage and 10 at full coverage.
  - q: What does mutation testing tell you that coverage does not?
    a: Whether tests actually fail when the code is deliberately changed; surviving mutants show assertions that do not check behaviour.
  - q: Why should the agent that wrote the code not be the one to declare it verified?
    a: The pstack summary says the author must not judge its own work; independent checks and evidence are what earn trust.
probes:
  - q: A team says "all agent PRs pass CI, so we skip review". What would you ask before agreeing?
    looks_for: What the checks actually test (coverage versus mutation score), who wrote the tests, whether the agent can edit the tests, what evidence is attached, and what is out of scope (design, security, maintainability).
misconceptions:
  - 100% test coverage means the tests would catch a wrong change.
  - If an agent wrote both code and tests, passing tests are independent evidence.
---

# Automated quality gates for agent-written code

## Knowledge
- Instead of reading agent-written code, some practitioners rely on constraints a machine checks: unit tests ("double-entry bookkeeping" in Uncle Bob's phrase), the CRAP metric, and mutation testing with surviving mutants. [fact] (Jim AI Notebook description; summary of interviews, transcript not read)
- CRAP (Change Risk Anti-Patterns, Savoia and Evans 2007) combines cyclomatic complexity with coverage; the creator's worked values at complexity 10 are 110, 22.5 and 10, and 30 is the original warning threshold. [fact] (Jim AI Notebook description, fact-check block)
- pstack (per the AI懶人報 description) rests on verification: the agent runs the program and shows evidence, the author cannot grade its own work, and a repeated mistake becomes a lint rule, type or test. [fact] (EP435 description; creator summary)
- StrongDM's two rules, as reported by Willison, were that humans do not write or review code. [fact] (Willison 2026, slides 022-023)

## Evidence
- Willison calls StrongDM's practice an exploration of how to be confident in quality without reading code; StrongDM is a security company with experienced people. [fact] (Willison 2026, slide 023)
- Counter-position: Ptacek says to read the code for anything people will depend on and notes he edits LLM output himself. [fact] (Ptacek)
- The creator behind the Uncle Bob video lists counter-evidence: Linus Torvalds, Willison, METR (marked outdated by METR) and DORA 2025 (correlation only). [fact] (Jim AI Notebook description)
- Anthropic docs warn that models can focus on making tests pass at the expense of general solutions or hard-code values, and provide a prompt to avoid it. [fact] (Prompting best practices)
- The Scion engineers say their job was often to tell Claude not to break the system's rules, which suggests rule-checking mattered even for strong agents. [fact] (Andy Lin video, 06:56; creator's summary)
- No controlled comparison of reviewed versus unreviewed agent code is in the vault. [inference]

## Understanding
- Tests only constrain what they assert; mutation testing and metrics try to measure test strength, but none of these test design quality or intent. [inference]
- If the same agent writes code and tests, they can agree on the same mistake; independent checks help. [inference] (follows from the pstack principle)
- Whether the checks are enough is the open question linked below. [inference]

## Application
- Make "tests fail on a deliberate change" a standard (mutation testing); keep tests out of the agent's edit scope when possible; require evidence of a run. [inference] (derived from the sources)
- Keep a human review for design, security and scope-critical changes until evidence says otherwise. [inference]

## Uncertainty
- All sources here are opinion or creator summaries; two videos had no transcripts. [fact] (source pages)
- Which gates sufficed for which risk levels is untested here. [speculation]

## Related
- [[self-verification-loop]], [[claim-agents-need-a-pass-fail-check]], [[claim-vibe-coding-versus-agentic-engineering]], [[strong-automated-verification-can-replace-human-review-of-agent-writte]], [[can-automated-verification-replace-human-code-review-for-agent-written]], [[pstack]], [[robert-c-martin-uncle-bob]]
