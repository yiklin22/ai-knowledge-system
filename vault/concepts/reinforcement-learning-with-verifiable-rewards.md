---
id: cpt_xdpvfy71
schema: 2
type: concept
title: "Reinforcement learning with verifiable rewards"
aliases: [RLVR, rule-based rewards, GRPO]
domains: [ai]
summary: "Training a model with reinforcement learning where the reward is computed by a rule or checker (a correct answer, passing code) rather than by a learned reward model; DeepSeek used GRPO for this."
tags: [reinforcement-learning, reward, training]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_qpdbwt21
    locator: "p.2-3, 2.1 GRPO"
    quote: null
  - id: src_qpdbwt21
    locator: "p.3-4, 2.2 Reward design"
    quote: "we abstain from applying neural reward models"
  - id: src_qpdbwt21
    locator: "p.63, G.2 Unsuccessful attempts"
    quote: "once a model-based PRM is introduced, it inevitably leads to reward hacking"
  - id: src_opi2fpk9
    locator: "slide 053"
    quote: null
relations:
  - {rel: introduced_in, id: src_qpdbwt21}
  - {rel: prerequisite_for, id: cpt_6spiyzt2}
  - {rel: related, id: cpt_nc6s1zdy}
  - {rel: related, id: cpt_tqbd5i2f}
recall:
  - q: What makes a reward "verifiable"?
    a: It is computed by a rule or checker (final answer matches ground truth, code compiles and passes tests) instead of a learned reward model.
  - q: How does GRPO get an advantage without a separate value model?
    a: It samples a group of outputs for each question and normalises each output's reward by the group's mean and standard deviation.
  - q: Why did DeepSeek avoid neural reward models for reasoning tasks?
    a: They observed that neural reward models are susceptible to reward hacking in large-scale RL, and retraining them adds cost and complexity.
misconceptions:
  - RLVR needs human-written reasoning traces.
  - A verifiable reward guarantees the model's reasoning is correct, not just its final answer.
---

# Reinforcement learning with verifiable rewards

## Knowledge
- In RLVR the reward comes from a program: an accuracy reward checks the final answer against ground truth (or a compiler and tests for code), and a format reward checks that reasoning sits in designated tags. [fact] (DeepSeek-R1 paper, 2.2)
- DeepSeek trained R1-Zero with GRPO (Group Relative Policy Optimization): for each question, sample a group of outputs and compute each advantage as its reward minus the group mean divided by the group standard deviation, with a clipped objective and a KL penalty to a reference policy. [fact] (paper, 2.1; equations are garbled in the raw file, description from the legible text)
- GRPO was proposed to simplify training and reduce resource use compared with PPO. [fact] (paper, 2.1)
- Reported settings for R1-Zero: 16 sampled outputs per question, learning rate 3e-6, KL coefficient 0.001, up to 32,768 tokens then 65,536 after step 8.2k. [fact] (paper, 2.1)

## Evidence
- The reward signal was based only on correctness of the final answer, with no constraint on the reasoning process. [fact] (paper p.2)
- The authors "abstain from applying neural reward models" to reasoning tasks because of reward hacking, and say a process reward model "inevitably leads to reward hacking" once model-based. [fact] (paper p.4 and G.2, authors' report)
- They also report that Monte Carlo tree search did not scale because token generation has an exponentially larger search space and a good value model was hard to train. [fact] (paper G.2)
- Willison says this technique, Reinforcement Learning from Verifiable Rewards, is used by everyone now and explains why models are so good at coding, maths and finding security holes. [fact] (Willison 2026 slide 053, secondary)

## Understanding
- A rule-based reward is hard to fool in ways a learned scorer can be, so the model must actually get answers right to earn reward. [inference] (follows from the paper's reasoning about reward hacking)
- The limit is scope: it only works where an automatic check exists (maths, code, some logic); for writing or open questions the paper still used SFT and other signals. [fact] (paper G.1, authors' view)
- The same property that makes rewards trustworthy can be gamed from inside the checker: Willison's account of agents breaking out of a sandbox during security-exercise training shows the environment itself can be attacked. [inference] (see the reported-break-out claim; unverified)

## Application
- When designing training or agent evaluation, prefer checks a program can run (tests, exact answers) over learned graders. [inference]
- For tasks without a verifier (essays, judgement), RLVR alone is not enough. [fact] (paper G.1)

## Uncertainty
- Whether the 77.9% AIME result and its causes replicate independently is not shown in these sources. [inference]
- Whether verifiable rewards alone suffice for broad capability, as opposed to reasoning on checkable tasks, is open. [speculation]

## Related
- [[reasoning-models-and-long-chain-of-thought]] — what this training produces.
- [[neural-reward-models-invite-reward-hacking-in-large-scale-rl]] — why rule-based rewards were chosen.
- [[reinforcement-learning-on-verifiable-rewards-alone-can-elicit-reasonin]]
- [[reinforcement-learning-basics]], [[reinforcement-learning-from-human-feedback]], [[deepseek-r1]]
