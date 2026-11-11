---
id: clm_lbcpiujx
schema: 2
type: claim
title: "Reinforcement learning on verifiable rewards alone can elicit reasoning without human reasoning traces"
aliases: []
domains: [ai]
summary: "DeepSeek reports that RL with only answer-correctness and format rewards, and no SFT stage, produced strong long-chain reasoning in R1-Zero; independent replication is not shown here."
tags: [reasoning, reinforcement-learning]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_qpdbwt21
    locator: "p.2, Introduction"
    quote: "The reward signal is solely based on the correctness of final predictions against ground-truth answers, without imposing constraints on the reasoning process itself."
  - id: src_qpdbwt21
    locator: "p.4, 2.3"
    quote: "jumping from an initial 15.6% to 77.9%"
relations:
  - {rel: about, id: cpt_xdpvfy71}
  - {rel: about, id: cpt_6spiyzt2}
  - {rel: about, id: ent_zrzrdqs7}
  - {rel: related, id: clm_2pmm9nwp}
  - {rel: qualifies, id: cpt_xdpvfy71}
verdict: supported
---

# Reinforcement learning on verifiable rewards alone can elicit reasoning without human reasoning traces

Statement: a base model trained with RL using only rule-based rewards (final-answer correctness and a format reward), with no supervised stage on human reasoning examples, develops long chain-of-thought reasoning.

## Evidence for
- The authors trained DeepSeek-V3-Base with GRPO and bypassed SFT; reward was solely final-answer correctness plus a format reward. [fact] (paper p.2 and 2.2; authors' report)
- AIME 2024 average pass@1 rose from 15.6% to 77.9% and to 86.7% with self-consistency; response length grew over training. [fact] (paper 2.3; authors' report)
- Karpathy describes this paper as the first to publicly discuss the RL stage that produces thinking models. [fact] (Karpathy re-upload, 17:02; secondary)

## Evidence against
- R1-Zero had poor readability and language mixing, and narrow strength on reasoning tasks, so the released R1 used a multi-stage pipeline with SFT and rejection sampling. [fact] (paper Introduction)
- The authors say exclusive reliance on RL can lead to reward hacking in ill-posed tasks and that both RL and SFT are indispensable in their pipeline. [fact] (paper G.1)
- The experiments cover checkable domains (maths, code, logic); they do not show the same works for open-ended tasks. [inference]

## Verdict reasoning
- Supported as a reported result from the primary source with detailed training settings; confidence medium rather than high because no independent replication is in the vault. [inference]
- Scope: reasoning on verifiable tasks, starting from a strong base model; not a claim that RL alone makes a full assistant. [inference]
