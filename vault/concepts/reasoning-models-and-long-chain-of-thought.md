---
id: cpt_6spiyzt2
schema: 2
type: concept
title: "Reasoning models and long chain-of-thought"
aliases: [thinking models, reasoning LLMs]
domains: [ai]
summary: "Models trained, mostly with reinforcement learning on checkable tasks, to write a long chain of thought before answering; they help most on hard maths and code and cost more time and tokens."
tags: [reasoning, reinforcement-learning, test-time-compute]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_qpdbwt21
    locator: "p.4, 2.3 Incentivize Reasoning Capability"
    quote: "jumping from an initial 15.6% to 77.9%"
  - id: src_qpdbwt21
    locator: "p.59-60, E.4 test-time scaling"
    quote: null
  - id: src_21xqrlz9
    locator: "22:43"
    quote: "There exist a class of models that we call thinking models."
  - id: src_t2ajgzb6
    locator: "Thinking and reasoning"
    quote: "Prefer general instructions over prescriptive steps."
relations:
  - {rel: introduced_in, id: src_qpdbwt21}
  - {rel: about, id: ent_zrzrdqs7}
  - {rel: related, id: cpt_xdpvfy71}
  - {rel: related, id: cpt_nc6s1zdy}
  - {rel: related, id: cpt_miqp75kg}
  - {rel: related, id: cpt_bpy1s28v}
recall:
  - q: What is a reasoning (thinking) model, in one sentence?
    a: A model trained with reinforcement learning to produce a long chain of thought (trying ideas, backtracking, checking) before its final answer.
  - q: Why did DeepSeek find independent majority voting a weaker way to scale test-time compute than long reasoning?
    a: Samples in majority voting are generated independently and cannot backtrack or self-correct, while one long chain can build on and fix its earlier steps.
  - q: When does Karpathy suggest switching a thinking model on?
    a: For hard maths, code and logic problems when a fast non-thinking answer is not good enough; not for simple queries such as travel ideas.
probes:
  - q: A friend says "reasoning models just sample many answers and vote". Is that right?
    looks_for: Distinguishes sequential long chain-of-thought (can backtrack, builds on earlier steps) from parallel independent sampling plus voting, which the paper says can still complement it (pass@64 90.0%, majority vote 86.7%).
misconceptions:
  - Thinking models are always better, so you should always use them.
  - The visible chain of thought is a faithful transcript of everything the model computed.
---

# Reasoning models and long chain-of-thought

## Knowledge
- A reasoning model writes a long chain of thought (often hundreds to thousands of tokens) before its answer, and is trained mostly with reinforcement learning on tasks whose answers can be checked. [fact] (DeepSeek-R1 paper; Karpathy lecture)
- Typical behaviours that appear in the chain: exploring alternatives, reflecting, backtracking, re-checking. [fact] (DeepSeek-R1 paper, 2.3)
- Providers expose this as a toggle or an effort/thinking setting; higher effort uses more thinking time and tokens. [fact] (Claude prompting docs; Tech With Tim)
- The DeepSeek authors report AIME 2024 pass@1 for R1-Zero rising from 15.6% to 77.9% during RL training, with response length growing steadily. [fact] (DeepSeek-R1 paper, 2.3; authors' own result)

## Evidence
- DeepSeek-R1 paper: pass@1 on AIME 2024 reached 79.8% for DeepSeek-R1; majority voting over 64 samples only moved GPT-4o from 9.3% to 13.4%; for R1, pass@64 was 90.0% and majority voting gave 86.7%. [fact] (paper p.59-60, E.4; authors' report)
- The paper's explanation: in majority voting the samples are independent, and a non-reasoning model cannot backtrack or self-correct. [fact] (paper p.60)
- Karpathy: thinking models were "tuned with reinforcement learning" and help on hard maths and code; he tries non-thinking models first because responses are quick, and switches when the answer seems weak. [fact] (Karpathy re-upload, 16:00 to 23:13)
- Claude docs: recent models use adaptive thinking driven by an effort setting; general instructions such as "think thoroughly" often beat hand-written plans; a prompt that asks for reasoning in tags may be declined on some models. [fact] (Prompting best practices; vendor docs, volatile)
- Zitron argues that token-heavy reasoning pushes inference cost up. [fact] (Zitron, opinion; see the economics claim)

## Understanding
- Reinforcement learning gives the model a reason to spend more tokens when problems are hard, because longer, self-checking chains earn more reward on verifiable answers. [inference] (from the reward design in the DeepSeek paper)
- Long chains trade latency and cost for accuracy; this is why effort levels exist. [inference]

```mermaid
flowchart LR
  A[Base model] --> B[RL with verifiable rewards]
  B --> C[Long chain of thought: reflect, verify, backtrack]
  C --> D[R1 pipeline: rejection sampling + SFT + RL]
  D --> E[Distil into smaller models]
```

## Application
- Use thinking mode for hard maths, code debugging and multi-step logic; skip it for simple lookups and advice. [fact] (Karpathy)
- Set effort deliberately: low for quick prototypes, higher only when correctness matters, because time and usage rise sharply. [fact] (Tech With Tim, presenter's experience)
- Do not hand-write step plans for the model; give the goal and let it plan. [fact] (Claude docs)

## Uncertainty
- Whether RL creates new reasoning ability or surfaces ability already in the base model is not settled in these sources. [speculation]
- The "aha moment" reading of R1-Zero's behaviour is disputed in the literature the paper itself cites; see the claim page. [fact]
- Model names, effort scales and prices here are volatile and dated 2026-11-08. [inference]

## Related
- [[reinforcement-learning-with-verifiable-rewards]] — how the reward is built.
- [[the-r1-zero-aha-moment-shows-reflection-emerging-from-rl]] — contested reading.
- [[reinforcement-learning-on-verifiable-rewards-alone-can-elicit-reasonin]] — the headline claim.
- [[deepseek-r1]], [[reinforcement-learning-basics]], [[supervised-fine-tuning]], [[context-window-and-compaction]]
