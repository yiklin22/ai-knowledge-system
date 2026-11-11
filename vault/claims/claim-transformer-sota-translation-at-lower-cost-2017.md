---
id: clm_7lomu1yq
schema: 2
type: claim
title: The Transformer reached state-of-the-art translation quality at lower training cost (2017)
aliases: []
domains:
- ai
summary: The authors report 28.4 BLEU on WMT14 EN-DE and 41.8 on EN-FR with a fraction of prior training cost.
tags:
- transformer
- benchmark
status: reviewed
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_jc7zff9n
  locator: Abstract, p.1
  quote: Our model achieves 28.4 BLEU on the WMT 2014
relations:
- rel: about
  id: cpt_tp1bkybc
- rel: derived_from
  id: src_jc7zff9n
verdict: supported
---

# The Transformer reached state-of-the-art translation quality at lower training cost (2017)

## Evidence for
- The abstract reports 28.4 BLEU on WMT 2014 EN-DE and a single-model state-of-the-art 41.8 BLEU on EN-FR after 3.5 days on eight GPUs. [fact] (Vaswani 2017, Abstract) Self-reported by the authors.
- Table 2 compares training FLOPs against ByteNet, GNMT, ConvS2S and MoE baselines. [fact] (Vaswani 2017, Table 2)

## Evidence against
- Nothing in `raw/` independently reproduces the numbers; this is a 2017 result and says nothing about current models. [inference]

## Verdict reasoning
Treated as supported for 2017 but kept low confidence: the sole source is the authors' own paper and the figures are dated benchmark results. [inference]
