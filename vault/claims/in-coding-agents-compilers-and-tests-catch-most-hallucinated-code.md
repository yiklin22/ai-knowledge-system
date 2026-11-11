---
id: clm_rcwidiyv
schema: 2
type: claim
title: "In coding agents, compilers and tests catch most hallucinated code"
aliases: []
domains: [programming]
summary: "Ptacek argues hallucination is largely a solved problem for coding agents because lint, compile and test failures are fed back to the model; this is an opinion without measurements."
tags: [hallucination, coding-agents]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_03op7psf
    locator: "Hallucination section"
    quote: "If their LLM invents a new function signature, the agent sees the error."
  - id: src_03op7psf
    locator: "Hallucination section"
    quote: "If hallucination matters to you, your programming language has let you down."
  - id: src_21xqrlz9
    locator: "122:12"
    quote: null
relations:
  - {rel: about, id: cpt_a602ati7}
  - {rel: related, id: qst_fwb03lfq}
  - {rel: related, id: clm_tfabt24p}
verdict: unverified
volatile: true
last_verified: 2026-11-08
---

# In coding agents, compilers and tests catch most hallucinated code

Statement: in agentic coding, invented APIs and similar fabrications are mostly caught by the compiler, linter and tests, so hallucination is not a major practical problem there.

## Evidence for
- Ptacek says agents lint, compile and run tests, see an error when the model invents a function signature, and retry; he calls hallucination "more or less" solved in this setting. [fact] (Ptacek, 2025 opinion)
- The existing vault claim that giving an agent a pass/fail check lets it close the loop supports the mechanism. [fact] (see the pass-fail claim page)

## Evidence against
- Ptacek concedes there may still be environments where hallucination matters. [fact] (Ptacek)
- A compiler catches nonexistent names and type errors, not wrong logic that compiles and passes weak tests; the Anthropic docs separately warn about test-gaming and hard-coded values. [inference] (mechanism; Prompting best practices)
- Karpathy's lecture, speaking of chat use without tools, says a model's recollection can be wrong and should be verified, which is about a different setting. [fact] (Karpathy re-upload, 122:12)
- No measurements of how many hallucinations are caught are given. [inference]

## Verdict reasoning
- Unverified: plausible mechanism, but only an experienced practitioner's opinion dated June 2025; models and tools have changed since. [inference]
