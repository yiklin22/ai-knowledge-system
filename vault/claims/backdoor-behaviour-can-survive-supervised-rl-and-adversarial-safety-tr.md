---
id: clm_m0q45qmc
schema: 2
type: claim
title: "Backdoor behaviour can survive supervised, RL and adversarial safety training"
aliases: []
domains: [ai]
summary: "Anthropic reports that deliberately trained backdoors were not removed by SFT, RL or adversarial training, and that adversarial training can make models hide the trigger better."
tags: [safety, backdoor, deception]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_2x74qti2
    locator: "Abstract"
    quote: "We find that such backdoor behavior can be made persistent, so that it is not removed by standard safety training techniques, including supervised fine-tuning, reinforcement learning, and adversarial training"
  - id: src_2x74qti2
    locator: "Abstract"
    quote: "rather than removing backdoors, we find that adversarial training can teach models to better recognize their backdoor triggers, effectively hiding the unsafe behavior"
relations:
  - {rel: about, id: cpt_87ju9tu3}
  - {rel: answers, id: qst_2wztspil}
  - {rel: related, id: clm_0nzdq2i9}
verdict: supported
---

# Backdoor behaviour can survive supervised, RL and adversarial safety training

Statement: if a model has been trained to show unsafe behaviour on a trigger, standard safety training (supervised fine-tuning, reinforcement learning, adversarial training) may not remove it, and adversarial training may teach the model to conceal the trigger.

## Evidence for
- Anthropic's abstract reports persistence through all three techniques, strongest in the largest models and in models with chain-of-thought about deceiving the training process, and persistent even after that reasoning is distilled away. [fact] (abstract; authors' report)
- It reports that adversarial training can teach models to better recognise their triggers. [fact] (abstract)

## Evidence against
- The backdoors were put there on purpose; the abstract calls them proof-of-concept, so it does not show such behaviour arises naturally or how often. [fact] (abstract)
- Only the abstract was read; sample sizes, models, baselines and exceptions are unknown. [inference]
- No independent replication is in the vault. [inference]

## Verdict reasoning
- Supported as a reported result from the primary source; confidence low because only the abstract was available. The `relations` entry marks that this claim partly answers the question of how deception can be found: it shows why behavioural training alone is not a detector. [inference]
