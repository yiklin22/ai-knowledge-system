---
id: cpt_fos9kymw
schema: 2
type: concept
title: Multi-head attention
aliases:
- multi-headed attention
domains:
- ai
summary: Running several attention functions in parallel on different learned projections, then concatenating the results.
tags:
- transformer
status: reviewed
confidence: medium
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_jc7zff9n
  locator: §3.2.2, p.4-5
  quote: Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions.
- id: src_9shk661r
  locator: The Beast With Many Heads
  quote: null
relations:
- rel: part_of
  id: cpt_tp1bkybc
- rel: related
  id: cpt_0ryfzibo
- rel: introduced_in
  id: src_jc7zff9n
recall:
- q: What does multi-head attention do with queries, keys and values in the original Transformer?
  a: Projects Q, K, V h=8 times with learned projections to d_k=d_v=64, runs attention in parallel, concatenates the outputs and projects them back with W^O.
- q: Why not just one attention head?
  a: A single head's weighted averaging inhibits attending to information from different representation subspaces at different positions jointly.
probes:
- q: The base model uses 8 heads of size 64 with d_model 512. Why might the total compute stay about the same as one head of size 512?
  looks_for: Each head works in a reduced dimension (d_model/h), so the total computational cost is similar to single-head attention at full dimensionality.
misconceptions:
- More heads always means more parameters or compute (in the original design the per-head dimension shrinks to keep cost similar).
---

# Multi-head attention

## Knowledge
- Instead of one attention function, the model linearly projects queries, keys and values h times and runs attention on each projection in parallel. The outputs are concatenated and projected again.
- The original Transformer uses h = 8 heads with d_k = d_v = d_model/h = 64.

## Evidence
- Multi-head attention lets the model jointly attend to information from different representation subspaces at different positions. [fact] (Vaswani 2017, §3.2.2)
- The paper uses h = 8 heads, each of dimension 64, and says total cost is similar to single-head attention at full dimensionality. [fact] (Vaswani 2017, §3.2.2)
- Alammar describes eight sets of Q/K/V matrices, eight Z matrices, concatenated and multiplied by an extra matrix W^O. [fact] (Alammar 2018, The Beast With Many Heads)
- Alammar notes that with all heads drawn at once, interpretation becomes harder. [fact] (Alammar 2018)

## Understanding
- Each head has its own projections, so different heads can specialise in different relationships between positions. [inference] (rests on the paper's "representation subspaces" claim)
- Concatenation plus W^O is what lets the single feed-forward layer, which expects one vector per position, consume eight heads' output. [inference] (from Alammar's explanation)

## Application
- Any Transformer layer uses it in place of a single attention function. [inference]
- Choosing h trades per-head width against number of heads at roughly constant cost. [inference]

## Uncertainty
- The paper reports individual heads appearing to learn different tasks and syntactic or semantic behaviour; this is the authors' own qualitative observation. [fact] (Vaswani 2017, §4)
- This wiki has no source on how much each head matters in practice or on later variants such as Multi-Query Attention; Alammar only names them. [inference]

## Related
- [[self-attention]] — the mechanism each head runs.
- [[transformer-architecture]] — the model it is part of.
