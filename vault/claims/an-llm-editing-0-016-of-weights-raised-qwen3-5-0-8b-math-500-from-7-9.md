---
id: clm_1vhrxjud
schema: 2
type: claim
title: "An LLM editing 0.016% of weights raised Qwen3.5-0.8B MATH-500 from 7.9% to 48.1%"
aliases: []
domains: [ai]
summary: "Researchers report that GPT-6 Astra, by subtracting one direction from MLP outputs, raised a small model's MATH-500 from 7.9% to 48.1% by stopping reasoning loops, but could not improve a non-looping model."
tags: [weights, reasoning-loops, volatile]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_jm7s2ac4
    locator: "Intro"
    quote: "this weight correction raises MATH-500 from 7.9% to 48.1%"
  - id: src_jm7s2ac4
    locator: "Experiment 8"
    quote: "Editing weights could remove an obstacle that hid an ability, but it could not add an ability the model lacked."
relations:
  - {rel: about, id: cpt_mp49wsbo}
  - {rel: about, id: qst_1yx5dqtj}
  - {rel: answers, id: qst_1yx5dqtj}
verdict: unverified
volatile: true
last_verified: 2026-11-08
---

# An LLM editing 0.016% of weights raised Qwen3.5-0.8B MATH-500 from 7.9% to 48.1%

Statement: a frontier LLM, without training, found and removed a looping direction in Qwen3.5-0.8B's weights (131,072 of 0.8 billion weights), raising MATH-500 from 7.9% to 48.1%, GSM8K from 13.8% to 67.1% and IFEval from 21.0% to 62.3%.

## Evidence for
- The authors report these numbers with 50 forward passes; with 10 or 25 passes the loops barely went away, and the share of MATH-500 answers hitting the token limit fell from 93% to 33% at 50. [fact] (Takehi et al., experiment 8; authors' report)
- Logs of every experiment and the edited model are released; a third party is said to have rebuilt it and re-run the evaluation. [fact] (post acknowledgements; not checked)

## Evidence against
- The authors say the fix lets the model finish answers it could already work out rather than making it better at maths, and that on Gemma 3 270M, which rarely loops, Astra could not improve it. [fact] (experiment 8)
- Unreviewed blog post by the authors; evaluation specifics, sampling variance and whether a simpler non-LLM method (for example steering vector subtraction) matches the result are not discussed in the portions read. [inference]
- Base model scores are extremely low (7.9%), so the jump is relative to a degenerate baseline. [inference]

## Verdict reasoning
- Unverified: striking but single-source and self-reported. The qualification matters: it supports "obstacle removal", not "capability addition", which is the linked open question. [inference]
