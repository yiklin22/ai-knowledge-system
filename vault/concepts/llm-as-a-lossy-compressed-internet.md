---
id: cpt_ax286yoy
schema: 2
type: concept
title: "LLM as a lossy compressed internet"
aliases: [zip file mental model, lossy zip file of the internet]
domains: [ai]
summary: "Karpathy's mental model: a chat is a token stream; the model is a lossy, probabilistic zip file of internet text (pre-training) with an assistant persona (post-training) and a knowledge cut-off, and no tools by default."
tags: [mental-model, karpathy, llm-usage]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_21xqrlz9
    locator: "01:00"
    quote: "The zip file is lossy and probabilistic zip file"
  - id: src_21xqrlz9
    locator: "00:30"
    quote: "So, the context window is kind of like this working memory of tokens"
  - id: src_21xqrlz9
    locator: "04:40"
    quote: "If you stream tokens to it, it will respond with tokens back."
relations:
  - {rel: about, id: ent_a8uhtyvi}
  - {rel: related, id: cpt_fsyf2ys2}
  - {rel: related, id: cpt_miqp75kg}
  - {rel: related, id: cpt_a602ati7}
  - {rel: related, id: cpt_bpy1s28v}
recall:
  - q: In Karpathy's picture, what do pre-training and post-training each contribute?
    a: Pre-training compresses internet text into the network's parameters (the knowledge, lossy and probabilistic); post-training gives it the assistant persona by training on conversations.
  - q: Why can a model be out of date, and what fixes it?
    a: Pre-training is expensive and infrequent, so knowledge stops at a cut-off; tools such as search supply recent information.
  - q: Why does he suggest starting a new chat when you change topic?
    a: Tokens in the window distract the model, can reduce accuracy and make each next token slightly more expensive.
misconceptions:
  - The model looks things up in a stored copy of the internet.
  - A confident answer from the model has been verified.
---

# LLM as a lossy compressed internet

## Knowledge
- A chat is a one-dimensional token stream that the user and the model take turns extending; this stream is the context window, the model's working memory. [fact] (Karpathy re-upload, 00:00 to 00:30)
- Pre-training compresses internet text into the network's parameters, which he likens to a lossy, probabilistic zip file (about 1 TB for about 1 trillion parameters in his example); post-training swaps the data for human-written conversations so the model takes an assistant persona. [fact] (Karpathy re-upload, 01:00 to 04:09)
- Knowledge has a cut-off because pre-training is costly and rare; recent information must come through tools. [fact] (Karpathy re-upload, 02:35 to 03:37)
- By default the model has no calculator, interpreter or browsing: you stream tokens in and tokens come back. [fact] (Karpathy re-upload, 04:40)
- Things said often on the internet are recalled better than rare ones, so verify anything high-stakes or obscure against primary sources. [fact] (Karpathy re-upload, 05:40 to 09:17)

## Evidence
- He tests the model on common, non-recent, low-stakes questions (caffeine in an Americano, cold-medicine ingredients) and still checks a box or a primary source. [fact] (Karpathy re-upload, 06:11 to 09:17; anecdote)
- He advises new chats on topic change because tokens in the window can distract and slow the model slightly. [fact] (Karpathy re-upload, 09:50 to 10:52)

## Understanding
- The metaphor explains hallucination: a lossy reconstruction can be fluent but wrong, especially on rare facts. [inference] (follows from "lossy and probabilistic")
- The metaphor stops fitting once tools, memory and thinking are added; the lecture itself later adds tool use and thinking as extensions. [inference]

## Application
- Ask simple, common, non-recent questions directly; use search or primary sources for fresh or high-stakes ones; keep the context clean. [fact] (Karpathy re-upload)
- Ask several models ("LLM council") for ideas and compare. [fact] (Karpathy re-upload, 15:30)

## Uncertainty
- The 1 TB and 1 trillion figures are his illustration for a particular model, not a general fact. [inference]
- The transcript is from an older lecture (models named are GPT-4o, o1 Pro, Grok 3); model advice is dated. [fact] (source page)

## Related
- [[language-modeling]], [[supervised-fine-tuning]], [[hallucination]], [[context-window-and-compaction]], [[andrej-karpathy]], [[reasoning-models-and-long-chain-of-thought]]
