---
id: clm_gruqwh4q
schema: 2
type: claim
title: "Strong automated verification can replace human review of agent-written code"
aliases: []
domains: [programming]
summary: "Uncle Bob, pstack's author and StrongDM say machine-checked constraints can stand in for reading agent code; Ptacek and others say responsibility still requires reading it."
tags: [code-review, verification, contested]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_cjg71ax2
    locator: "Description: 利益揭露"
    quote: "主持人 Ankit Jain 是 Aviator 創辦人"
  - id: src_gt6qwx4i
    locator: "Description: question 2"
    quote: "讓 agent 自己把程式跑起來、拿證據給你看"
  - id: src_opi2fpk9
    locator: "slide 022"
    quote: "Any code that you write has to have been routed through a coding agent."
  - id: src_03op7psf
    locator: "'Read the code' section"
    quote: "If you build something with an LLM that people will depend on, read the code."
relations:
  - {rel: about, id: cpt_hooaxuqi}
  - {rel: answers, id: qst_mweuaqyt}
  - {rel: related, id: clm_tfabt24p}
  - {rel: related, id: clm_blkj2ekk}
verdict: contested
---

# Strong automated verification can replace human review of agent-written code

Statement: with enough machine-checked constraints and evidence, humans no longer need to read agent-written code before it merges.

## Evidence for
- Uncle Bob, per a creator's summary of two interviews, stopped reading agent-written code and uses tests, the CRAP metric and mutation testing; the host's company sells tools that replace code review with verification. [fact] (Jim AI Notebook description; description only, transcript not read)
- pstack's author lets agents merge about 2,000 PRs a month, on the principle that the agent must run the program and show evidence and that a repeated mistake becomes a lint, type or test. [fact] (EP435 description; creator summary)
- StrongDM, per Willison, adopted the rule that code must not be reviewed by humans, six months ahead of the rest. [fact] (Willison 2026, slides 022-023; secondary)

## Evidence against
- Ptacek: you are responsible for what you merge, so read the code that people will depend on. [fact] (Ptacek; 2025 opinion)
- Uncle Bob reversed an earlier pipeline design within a month and said his position might change again; the creator notes the "pipelines are obsolete" conclusion is not an industry consensus. [fact] (Jim AI Notebook description)
- The creator lists counter-evidence from Linus Torvalds and Willison; METR's slowdown study is marked outdated by METR and DORA 2025 shows correlation only, so neither settles it. [fact] (description)
- Anthropic docs say models can make tests pass without a general solution, so tests alone may not prove correctness. [fact] (Prompting best practices)

## Verdict reasoning
- Contested: advocates are practitioners and vendors with commercial interest, evidence is anecdotal, and no controlled comparison exists in the vault. [inference]
- It sits in tension with the vibe-coding versus agentic engineering claim, which separates unreviewed prototypes from professional work, while this one asks whether professional work can drop review; the pages are linked as related, not contradictory. [inference]
