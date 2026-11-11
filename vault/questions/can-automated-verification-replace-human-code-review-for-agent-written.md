---
id: qst_mweuaqyt
schema: 2
type: question
title: "Can automated verification replace human code review for agent-written code?"
aliases: []
domains: [programming]
summary: "Practitioners disagree on whether tests, metrics and agent-run evidence can substitute for reading agent-written code; no controlled comparison is in the vault."
tags: [code-review, verification]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: related, id: clm_gruqwh4q}
  - {rel: related, id: cpt_hooaxuqi}
  - {rel: related, id: clm_tfabt24p}
state: open
---

# Can automated verification replace human code review for agent-written code?

## Why I'm asking
- Several sources (Uncle Bob, pstack, StrongDM) say yes; Ptacek says read the code you merge. Whether the vault's own practice of reviewing AI-written proposals should change depends on the answer.

## What would answer it
- A primary talk or paper with outcome data: defect and incident rates for reviewed versus unreviewed agent code at comparable teams.
- The full Uncle Bob interviews (the video had no transcript) and the StrongDM write-up, read directly.
- A definition of which risk classes (security, design, maintainability) tests and mutation scores can and cannot cover.
