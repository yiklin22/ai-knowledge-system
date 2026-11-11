---
id: ent_8f72s5bf
schema: 2
type: entity
title: "BeepBeep acoustic ranging"
aliases: [BeepBeep]
domains: [science]
summary: A 2007 paper describing a software-only acoustic ranging and localization system for commodity devices, used as the basis for Beep Locator.
tags: [acoustic-ranging, localization]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources:
  - id: src_iao3w460
    locator: "How it works"
    quote: "It is a pure software-based solution and uses only the most basic set of commodity hardware"
relations:
  - {rel: introduced_in, id: src_iao3w460}
  - {rel: related, id: ent_gg0fprgh}
kind: paper
---

# BeepBeep acoustic ranging

## Who/what
[fact] "BeepBeep: A High-Accuracy Acoustic-Based System for Ranging and Localization Using COTS Devices", a 2007 paper by Chunyi Peng, Guobin Shen, Yongguang Zhang, Yanlin Li and Kun Tan (per Willison's post). Its abstract says accuracy comes from three techniques: two-way sensing, self-recording and sample counting. The vault only holds the abstract as quoted in the blog; the paper itself was not read.

## Why it matters
[fact] Willison says Claude found this paper while researching the problem and that it "sounded exactly like what we needed to build". [inference] It shows an agent doing literature lookup to ground a design, but the extent to which Beep Locator implements BeepBeep (versus drawing on its ideas, e.g. the chirp alignment) is not stated in the source.
