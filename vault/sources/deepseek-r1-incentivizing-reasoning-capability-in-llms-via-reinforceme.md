---
id: src_qpdbwt21
schema: 2
type: source
title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning (paper)"
aliases: []
domains: [ai]
summary: "The DeepSeek-R1 paper: pure reinforcement learning with rule-based rewards on a base model produces long-chain-of-thought reasoning (R1-Zero), then a multi-stage pipeline gives R1 and distilled smaller models."
tags: [reasoning, reinforcement-learning, paper]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: ent_zrzrdqs7}
  - {rel: about, id: cpt_6spiyzt2}
  - {rel: about, id: cpt_xdpvfy71}
kind: paper
reliability: primary
raw: raw/documents/2026-11-08-deepseek-r1-incentivizing-reasoning-capability-in-llms-via-r.md
url: "https://arxiv.org/abs/2501.12948"
author: DeepSeek-AI
published: "2026-01-04"
---

# DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning (paper)

## Takeaways
- The authors train DeepSeek-V3-Base with GRPO and a reward based only on final-answer correctness plus a format reward, skipping the supervised fine-tuning stage; the resulting model is called DeepSeek-R1-Zero.
- Reported on AIME 2024: average pass@1 rose from 15.6% to 77.9% during RL, and to 86.7% with self-consistency decoding; response length (thinking time) grew steadily.
- R1-Zero had poor readability and language mixing, so DeepSeek-R1 uses a multi-stage pipeline (rejection sampling, RL, SFT) and distillation into smaller models.
- The authors avoided neural reward models for reasoning because of reward hacking, and report that process reward models and Monte Carlo tree search did not work well for them (Supplementary G.2).
- This is the authors' own report (primary source for what they did, not independent verification). The bibliography includes a paper titled "There may not be aha moment in r1-zero-like", so the "aha moment" interpretation has at least one published challenger.
- The version read is arXiv v2 dated 4 Jan 2026. The raw file has NUL bytes near the start, which did not affect the text read; equations are garbled by PDF extraction, so read formulas from the PDF in raw/assets.

## Locator map
- Abstract and Introduction: p.1-2.
- 2.1 Group Relative Policy Optimization: p.2-3.
- 2.2 Reward design (accuracy and format rewards, no neural reward models): p.3-4.
- 2.3 Incentivize reasoning, AIME 15.6% to 77.9%, "aha moment" Table 2: p.4-5.
- E.4 test-time scaling versus majority voting, pass@64: p.59-60.
- G.1 RL versus SFT, G.2 Unsuccessful attempts (PRM, MCTS): p.63-64.
- References: includes the "aha moment" critique title.
