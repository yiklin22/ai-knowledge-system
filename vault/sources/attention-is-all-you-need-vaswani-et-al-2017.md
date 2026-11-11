---
id: src_jc7zff9n
schema: 2
type: source
title: Attention Is All You Need (Vaswani et al., 2017)
aliases: []
domains:
- ai
summary: 'The original Transformer paper: an encoder-decoder model built only from attention, with machine-translation results.'
tags:
- paper
- transformer
status: reviewed
confidence: medium
created: '2026-11-08'
updated: '2026-11-08'
sources: []
relations: []
kind: paper
reliability: primary
raw: raw/documents/2026-11-08-attention-is-all-you-need.md
url: https://arxiv.org/abs/1706.03762
author: Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin
published: 2017 (NIPS 2017; arXiv v7 2023)
---

# Attention Is All You Need (Vaswani et al., 2017)

## Takeaways
- Proposes the Transformer, based solely on attention, dropping recurrence and convolutions.
- Defines scaled dot-product attention and multi-head attention; adds sinusoidal positional encodings.
- Reports 28.4 BLEU (EN-DE) and 41.8 BLEU (EN-FR) on WMT 2014, with far lower training cost than prior models (authors' own results).

## Locator map
- Abstract, p.1 · Introduction p.2 · Architecture §3, pp.2-5 (attention §3.2, positional encoding §3.5, p.6)
- Why self-attention §4, pp.6-7 (Table 1 complexity comparison) · Training §5, pp.7-8 · Results Table 2, p.8
- PDF pages are marked `<!-- page N -->` in the raw file.
