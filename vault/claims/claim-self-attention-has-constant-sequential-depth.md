---
id: clm_yjsp6ql4
schema: 2
type: claim
title: Self-attention connects all positions with a constant number of sequential operations
aliases: []
domains:
- ai
summary: Unlike recurrent layers, which need O(n) sequential operations, a self-attention layer relates any two positions in O(1) steps.
tags:
- transformer
status: reviewed
confidence: medium
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_jc7zff9n
  locator: §4, p.6-7, Table 1
  quote: a self-attention layer connects all positions with a constant number of sequentially executed operations, whereas a recurrent layer requires O(n) sequential operations.
relations:
- rel: about
  id: cpt_0ryfzibo
- rel: derived_from
  id: src_jc7zff9n
verdict: supported
---

# Self-attention connects all positions with a constant number of sequential operations

## Evidence for
- Table 1 of the paper lists self-attention with O(1) sequential operations and O(1) maximum path length, against O(n) for recurrent layers. [fact] (Vaswani 2017, Table 1)
- Self-attention layers are faster than recurrent layers when sequence length n is smaller than representation dimension d. [fact] (Vaswani 2017, §4)

## Evidence against
- Per-layer cost is O(n^2 d), so long sequences get expensive; the paper itself suggests restricted self-attention (O(n/r) path length) as future work. [fact] (Vaswani 2017, §4)

## Verdict reasoning
This is an analytical property from the paper's own complexity analysis, so it is well supported; the trade-off is quadratic cost in n. [inference]
