---
id: ent_zrzrdqs7
schema: 2
type: entity
title: "DeepSeek-R1"
aliases: [DeepSeek-R1-Zero, R1]
domains: [ai]
summary: "DeepSeek-AI's reasoning model family trained with reinforcement learning, released with distilled smaller versions."
tags: [model, reasoning]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_qpdbwt21
    locator: "p.1-2"
    quote: null
relations:
  - {rel: introduced_in, id: src_qpdbwt21}
  - {rel: related, id: cpt_6spiyzt2}
  - {rel: related, id: cpt_xdpvfy71}
kind: model
---

# DeepSeek-R1

## Who/what
- DeepSeek-R1-Zero: DeepSeek-V3-Base trained with GRPO and rule-based rewards, no SFT stage. DeepSeek-R1: the same line with a multi-stage pipeline (rejection sampling, RL, SFT) to fix readability and language mixing and add non-reasoning abilities. Distilled smaller models were released. [fact] (DeepSeek-R1 paper, Introduction)
- Reported benchmark: AIME 2024 pass@1 of 79.8% for DeepSeek-R1, with 90.0% pass@64 and 86.7% by majority voting. [fact] (paper p.59-60; authors' report)
- Released through Hugging Face under the deepseek-ai organisation, per the paper. [fact] (paper Introduction)
- Karpathy notes that Perplexity hosted R1 and that its raw thoughts are visible, unlike OpenAI's summarised thoughts. [fact] (Karpathy re-upload, 21:41 to 22:12)

## Why it matters
- It is the paper Karpathy credits as the first public description of the RL stage behind thinking models, and the source for the verifiable-reward training recipe in this vault. [fact] (Karpathy re-upload, 17:02)
- Note: this entity is the model; the paper is the linked source page. [inference]
