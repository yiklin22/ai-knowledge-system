---
id: cpt_tp1bkybc
schema: 2
type: concept
title: Transformer architecture
aliases:
- Transformer
domains:
- ai
summary: An encoder-decoder network built from stacked layers of multi-head attention and position-wise feed-forward networks, with residual connections and layer normalization.
tags:
- curriculum
- transformer
status: draft
confidence: medium
created: 2026-11-08
updated: '2026-11-08'
sources:
- id: src_jc7zff9n
  locator: Abstract, p.1
  quote: We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.
- id: src_jc7zff9n
  locator: §3.1, p.3
  quote: That is, the output of each sub-layer is LayerNorm(x + Sublayer(x))
- id: src_jc7zff9n
  locator: §3.2.2, p.5
  quote: In this work we employ h = 8 parallel attention layers, or heads.
- id: src_9shk661r
  locator: The Residuals
  quote: The exact same feed-forward network is independently applied to each position.
relations:
- rel: prerequisite_for
  id: cpt_fsyf2ys2
- rel: prerequisite_for
  id: cpt_aj415iv5
- rel: prerequisite_for
  id: cpt_3o0xla6w
- rel: prerequisite_for
  id: cpt_hrzo5jmc
- rel: introduced_in
  id: src_jc7zff9n
recall:
- q: What are the two sub-layers of each encoder layer, and what wraps them?
  a: 'Multi-head self-attention and a position-wise feed-forward network, each wrapped in a residual connection followed by layer normalization: LayerNorm(x + Sublayer(x)).'
- q: What does the decoder add compared with an encoder layer?
  a: A third sub-layer doing multi-head attention over the encoder output, and masking in self-attention so positions cannot attend to later positions.
- q: What are the base model's main hyperparameters in the original paper?
  a: N=6 layers, d_model=512, h=8 heads, d_ff=2048.
probes:
- q: Why does the decoder mask its self-attention?
  looks_for: 'To preserve the auto-regressive property: predictions for position i may depend only on known outputs at positions less than i; illegal connections are set to minus infinity before softmax.'
- q: Which part of the Transformer lets positions be processed in parallel, and where do positions still interact?
  looks_for: Each position flows through its own path; dependencies exist only in self-attention, while the feed-forward network is applied to each position separately and identically.
misconceptions:
- Modern LLMs are exactly the 2017 encoder-decoder model (many later models differ; this page covers the original design only).
---

# Transformer architecture

## Knowledge
- The original Transformer is an encoder-decoder model using stacked self-attention and point-wise fully connected layers. It dispenses with recurrence and convolutions entirely.
- Encoder: N = 6 identical layers, each with multi-head self-attention then a position-wise feed-forward network. Decoder: N = 6 layers, adding attention over the encoder output and a masked self-attention.
- All sub-layers use residual connections followed by layer normalization; d_model = 512.

## Evidence
- The paper proposes a network "based solely on attention mechanisms, dispensing with recurrence and convolutions entirely". [fact] (Vaswani 2017, Abstract)
- The output of each sub-layer is LayerNorm(x + Sublayer(x)); the decoder masks self-attention to prevent attending to subsequent positions. [fact] (Vaswani 2017, §3.1)
- The feed-forward network is two linear transformations with a ReLU, d_model = 512, inner dimension 2048. [fact] (Vaswani 2017, §3.3)
- The model uses h = 8 heads. [fact] (Vaswani 2017, §3.2.2)
- Alammar: the encoders are identical in structure but do not share weights, and the same feed-forward network is applied independently to each position. [fact] (Alammar 2018, A High-Level Look; The Residuals)
- Reported results: 28.4 BLEU (EN-DE) and 41.8 BLEU (EN-FR) on WMT 2014, as the authors' own figures. [fact] (Vaswani 2017, Abstract) See [[claim-transformer-sota-translation-at-lower-cost-2017]].
- Alammar's 2025 update says later Transformer models evolved with variants such as Multi-Query Attention and RoPE. [fact] (Alammar 2018, update note)

## Understanding
- Because positions interact only inside attention, the rest of each layer parallelises across positions, which is where the training-speed gain over recurrent models comes from. [inference] (from Alammar's description and the paper's parallelisation argument)
- Residual connections let each sub-layer learn a modification of its input rather than a full transformation. [inference]

```mermaid
flowchart TB
  E[Embeddings + positional encoding] --> A1[Multi-head self-attention]
  A1 --> N1[Add and LayerNorm]
  N1 --> F1[Feed-forward]
  F1 --> N2[Add and LayerNorm]
  N2 --> D[Decoder cross-attention]
  D --> L[Linear + softmax]
```

Follow one position through an encoder layer: attention, add and norm, feed-forward, add and norm.

## Application
- The pattern is the basis for modern language models, though most current LLMs use variants (for example decoder-only). [speculation] (this wiki has no source on current architectures beyond Alammar's note)

## Uncertainty
- This page describes the 2017 design; later changes (positional schemes, attention variants, decoder-only stacks) are not covered by sources in `raw/`. [inference]
- BLEU results are the authors' own and dated. [inference]

## Related
- [[self-attention]] — the central operation.
- [[multi-head-attention]] — how attention is parallelised.
- [[positional-encoding]] — how order enters the model.
