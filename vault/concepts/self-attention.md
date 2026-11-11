---
id: cpt_0ryfzibo
schema: 2
type: concept
title: Self-attention
aliases: []
domains:
- ai
summary: Each position of a sequence forms a weighted sum of all positions' value vectors, with weights from a softmax over scaled query-key dot products.
tags:
- curriculum
- transformer
status: draft
confidence: medium
created: 2026-11-08
updated: '2026-11-08'
sources:
- id: src_jc7zff9n
  locator: §3.2.1, p.4
  quote: We compute the dot products of the query with all keys, divide each by √dk, and apply a softmax function to obtain the weights on the values.
- id: src_jc7zff9n
  locator: §3.2, p.3-4
  quote: An attention function can be described as mapping a query and a set of key-value pairs to an output
- id: src_9shk661r
  locator: Self-Attention in Detail
  quote: null
relations:
- rel: prerequisite_for
  id: cpt_g0clar9v
- rel: prerequisite_for
  id: cpt_tp1bkybc
- rel: introduced_in
  id: src_jc7zff9n
- rel: related
  id: cpt_fos9kymw
recall:
- q: In scaled dot-product attention, how are the attention weights computed?
  a: Dot products of the query with all keys, divided by sqrt(d_k), then softmax; the weights multiply the value vectors and are summed.
- q: Where do queries, keys and values come from in encoder self-attention?
  a: 'All three come from the same place: the output of the previous layer.'
probes:
- q: Why divide the query-key dot products by the square root of d_k?
  looks_for: For large d_k the dot products grow in magnitude (variance d_k if components have mean 0 and variance 1), pushing softmax into regions with tiny gradients; scaling counteracts this.
- q: In 'The animal didn't cross the street because it was too tired', how does self-attention help encode 'it'?
  looks_for: The query for 'it' scores highly against the key for 'animal', so the value of 'animal' contributes strongly to the encoding of 'it'.
misconceptions:
- Self-attention processes tokens one after another like an RNN (all positions are computed in parallel).
- The query, key and value vectors are the embedding itself (they are separate learned projections of it).
---

# Self-attention

## Knowledge
- Self-attention relates different positions of a single sequence to compute a representation of that sequence.
- In the Transformer, queries, keys and values all come from the previous layer. Each output is a weighted sum of the values, with weights from a softmax over scaled query-key dot products.
- Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V.

## Evidence
- An attention function maps a query and a set of key-value pairs to an output; the output is a weighted sum of the values, with each weight from a compatibility function of the query with the key. [fact] (Vaswani 2017, §3.2)
- The paper computes dot products of the query with all keys, divides by sqrt(d_k), and applies a softmax to get weights on the values. [fact] (Vaswani 2017, §3.2.1)
- For large d_k, the authors suspect large dot products push softmax into regions with very small gradients, so they scale by 1/sqrt(d_k). [fact] (Vaswani 2017, §3.2.1 and footnote 4)
- A self-attention layer connects all positions with a constant number of sequential operations, versus O(n) for recurrent layers. [fact] (Vaswani 2017, §4, Table 1) See [[claim-self-attention-has-constant-sequential-depth]].
- Alammar's walk-through: create Query, Key and Value vectors from each embedding (64-dimensional against 512-dimensional embeddings), score by dot product, divide by 8, apply softmax, weight the values, and sum. [fact] (Alammar 2018, Self-Attention in Detail)

## Understanding
- Think of it as a soft lookup: the query asks, keys advertise, and softmax turns match scores into how much of each value to blend in. [inference] (an intuition; Alammar calls Q/K/V "abstractions that are useful for calculating and thinking about attention")
- The cost is O(n^2 d) per layer because every position scores against every other. [fact] (Vaswani 2017, Table 1)

```mermaid
flowchart LR
  X[Input vectors X] --> Q[Q = X Wq]
  X --> K[K = X Wk]
  X --> V[V = X Wv]
  Q --> S["scores = Q K^T / sqrt(d_k)"]
  K --> S
  S --> W[softmax]
  W --> O["output = weights x V"]
  V --> O
```

Look at how Q and K only decide the weights, while V is what gets blended into the output.

## Application
- It is the core operation inside every Transformer layer; see [[multi-head-attention]] and [[transformer-architecture]]. [inference]
- Quadratic cost in sequence length is the main practical limit; the paper suggests restricting attention to a neighbourhood of size r as future work. [fact] (Vaswani 2017, §4)

## Uncertainty
- The authors say attention could yield more interpretable models, and that individual heads appear to learn different tasks. [fact] (Vaswani 2017, §4; the authors' own qualitative claim)
- Alammar warns: "If we add all the attention heads to the picture, however, things can be harder to interpret". [fact] (Alammar 2018)
- This page has no source on post-2017 attention variants; Alammar only mentions Multi-Query Attention and RoPE. [inference]

## Related
- [[multi-head-attention]] — several of these in parallel.
- [[positional-encoding]] — how order is supplied, since attention alone ignores order.
- [[embeddings]] — the vectors fed in.
- [[transformer-architecture]] — the full model.
