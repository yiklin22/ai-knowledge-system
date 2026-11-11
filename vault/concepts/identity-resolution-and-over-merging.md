---
id: cpt_bjjfgu02
schema: 2
type: concept
title: "Identity resolution and over-merging"
aliases: [IDR, entity resolution for customers, over-merge]
domains: [business]
summary: Identity resolution maps data records to the real people they describe; over-merging, where one identity mixes several people, is its most common and damaging failure and is hard to measure without ground truth.
tags: [data, customer-data, identity-resolution]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_x1ew5c1z
    locator: "What is identity resolution?"
    quote: null
relations:
  - {rel: related, id: ent_i2k1snkk}
  - {rel: related, id: cpt_i243o4zy}
recall:
  - {q: "What is over-merging in identity resolution?", a: "An identity that incorrectly corresponds to multiple real people."}
  - {q: "Why is it hard to measure IDR accuracy on real data?", a: "There is no answer key; you must sample identities and review them by hand."}
  - {q: "Why do small human samples estimate over-merge rate poorly?", a: "Over-merges are rare, so precision needs many samples (the source says more than 1,000 for +-1%)."}
misconceptions:
  - "A different value in a field (address, age, spelling) means a different person."
---

# Identity resolution and over-merging

## Knowledge

- [fact] Identity resolution (IDR): given records D, produce identities I and a mapping so each record maps to one identity, each identity is exactly one real person, and no two identities are the same person (src_x1ew5c1z).
- [fact] Records differ for one person through typos, misread characters, phonetic spelling, swapped month/day, values copied from relatives, nicknames, placeholder names and blanks; people also move and age.
- [fact] Over-merging is described as the most common and problematic IDR issue.

## Evidence

- [fact] Heuristics (e.g. emails per identity) give statistical signs; confirming requires hand review at roughly 50 identities per hour, and over 1,000 samples to get the over-merge-rate error under +-1% (vendor figures).

## Understanding

- [inference] The difficulty is distinguishing noise within one person from true differences between people (twins, junior/senior, same name), so judgment needs context, which is why LLM judges were tried.

## Application

- Sample and judge output identities to monitor an IDR system, e.g. with [[confidence-gated-hybrid-judge-cheap-model-then-frontier]].

## Uncertainty

- [inference] Under-merging (the opposite error) is deferred to a future post by the source; not covered here.
- [inference] Source is a vendor of IDR tooling.

## Related

[[pseudopeople]], [[evaluating-llms]]
