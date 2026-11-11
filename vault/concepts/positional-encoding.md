---
id: cpt_g0clar9v
schema: 2
type: concept
title: Positional encoding
aliases: []
domains:
- ai
summary: Vectors added to token embeddings so a model with no recurrence or convolution can use word order; the original Transformer used fixed sinusoids.
tags:
- curriculum
- transformer
status: draft
confidence: medium
created: 2026-11-08
updated: '2026-11-08'
sources:
- id: src_jc7zff9n
  locator: §3.5, p.6
  quote: we must inject some information about the relative or absolute position of the tokens in the sequence.
- id: src_9shk661r
  locator: Representing The Order of The Sequence Using Positional Encoding
  quote: null
relations:
- rel: prerequisite_for
  id: cpt_tp1bkybc
- rel: introduced_in
  id: src_jc7zff9n
recall:
- q: Why does the Transformer need positional encodings?
  a: It has no recurrence or convolution, so information about token order must be injected; the encodings are added to the embeddings.
- q: Which positional encoding did the original paper use, and how did it compare with learned ones?
  a: Fixed sine and cosine functions of different frequencies; learned positional embeddings gave nearly identical results.
probes:
- q: If you shuffled the words of a sentence but gave the model no positional information, what would self-attention do differently?
  looks_for: 'Nothing about order: attention treats positions as a set, so the output for each token would be the same up to the shuffle, which is why order must be injected.'
misconceptions:
- Position information is learned by the attention weights without any extra input (it must be supplied).
---

# Positional encoding

## Knowledge
- Self-attention itself does not know token order. Positional encodings of the same dimension as the embeddings are added to the input embeddings at the bottom of the encoder and decoder stacks.
- The original paper used sinusoids: PE(pos, 2i) = sin(pos / 10000^(2i/d_model)) and PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model)).

## Evidence
- The model has no recurrence or convolution, so "we must inject some information about the relative or absolute position of the tokens in the sequence". [fact] (Vaswani 2017, §3.5)
- Wavelengths form a geometric progression from 2 pi to 10000 * 2 pi. [fact] (Vaswani 2017, §3.5)
- Learned positional embeddings gave nearly identical results (Table 3 row E); the sinusoidal version was chosen because it may extrapolate to longer sequences. [fact] (Vaswani 2017, §3.5)
- The authors hypothesised sinusoids would make it easy to attend by relative positions, since PE(pos+k) is a linear function of PE(pos). [fact] (Vaswani 2017, §3.5)
- Alammar describes it as adding a vector to each input embedding that follows a pattern, so meaningful distances exist between embedding vectors once projected into Q/K/V. [fact] (Alammar 2018)

## Understanding
- Adding position to the embedding means attention scores can depend on where tokens are, not only what they are. [inference]
- The Alammar post notes newer models moved to alternatives such as RoPE; this page does not cover them. [fact] (Alammar 2018, update note)

## Application
- Any attention-only sequence model needs some positional scheme; the original choice was fixed sinusoids. [inference]

## Uncertainty
- Whether sinusoids actually extrapolate better than learned encodings is stated as a hope, not shown in the paper. [fact] (Vaswani 2017, §3.5)
- Modern positional schemes are not covered by sources in `raw/`. [inference]

## Related
- [[self-attention]] — the operation that needs this input.
- [[transformer-architecture]] — where it is added.
- [[embeddings]] — what it is added to.
