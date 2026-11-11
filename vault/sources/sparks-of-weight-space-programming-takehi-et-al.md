---
id: src_jm7s2ac4
schema: 2
type: source
title: "Sparks of Weight-Space Programming (Takehi et al.)"
aliases: []
domains: [ai]
summary: "A November 2026 research blog post reporting that a frontier LLM can read network weights to infer what they do, write small networks from scratch, and edit a small model's weights to fix a failure without training."
tags: [interpretability, weights, research-blog]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: cpt_mp49wsbo}
  - {rel: about, id: clm_1vhrxjud}
  - {rel: about, id: qst_1yx5dqtj}
  - {rel: related, id: cpt_hrzo5jmc}
kind: web
reliability: primary
raw: raw/web/2026-11-08-sparks-of-weight-space-programming-llms-can-natively-read-wr.md
url: "https://rikiyat.github.io/blog/weight-space-programming/"
author: Rikiya Takehi; Jayden Teoh; Alex Zhang; Omar Khattab
published: "2026-11-02"
volatile: true
last_verified: 2026-11-08
---

# Sparks of Weight-Space Programming (Takehi et al.)

## Takeaways
- Defined: "Weight-Space Programming" means a general-purpose LLM reads and writes a network's weights directly (not via an optimizer or gradient descent) around a natural-language spec. The model used is GPT-6 Astra; one experiment uses Gemma 3 270M and Qwen3.5-0.8B as targets.
- Reading results: from raw weights alone it named the right game for four PPO networks, the generated shape for diffusion models, and the training language and every copying (induction) head for three small char-level models with input/output layers removed.
- Writing results: a single edit of 3.5% of weights fixed a stuck PPO car policy in all 1,024 episodes; from-scratch networks beat PPO at 100M steps on three MinAtar games; a 1.5M-parameter Go network written with forward-pass budget beat a PPO network trained on 20 million games at 50 passes.
- Edit result: removing one direction from MLP outputs of Qwen3.5-0.8B (0.016% of weights, 50 forward passes) raised MATH-500 from 7.9% to 48.1%, GSM8K 13.8% to 67.1% and IFEval 21.0% to 62.3%, because the base model looped; the same method did not improve Gemma, which rarely loops.
- Failure: Astra could not tell a sycophantic model from a correct one from weights alone; it could when shown attention patterns on text it wrote.
- Authors' own blog, not peer reviewed; logs and the edited model are released, and a third party reportedly rebuilt it and re-ran evaluation, but this was not checked here. Text from the post's figures and some examples is missing from the capture. The authors state results are early and limited by context length and harnesses.

## Locator map
- Experiments 1-8 in order of appearance: game networks; diffusion; middle-layers-only language models; PPO car fix; MinAtar from scratch; 1.5M-parameter Go network; sycophancy; Qwen3.5-0.8B and Gemma. Discussion on interpretability and limitations near the end.
