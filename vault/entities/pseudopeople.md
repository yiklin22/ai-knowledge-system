---
id: ent_i2k1snkk
schema: 2
type: entity
title: "pseudopeople"
aliases: []
domains: [science]
summary: Tool from the Institute for Health Metrics and Evaluation (University of Washington) that simulates a fictional US town and generates realistic noisy records of its residents.
tags: [synthetic-data, benchmark]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_x1ew5c1z
    locator: "Can LLMs measure over-merging in practice?"
    quote: null
relations:
  - {rel: related, id: cpt_bjjfgu02}
kind: dataset
---

# pseudopeople

## Who/what

[fact] Per Hightouch, a tool from the Institute for Health Metrics and Evaluation at the University of Washington that simulates a fictional US town and generates records from multiple sources (census, surveys, WIC, Social Security, tax forms); Hightouch added realistic data errors.

## Why it matters

[inference] Gives a ground-truth-labelled benchmark for identity resolution, which real data lacks. No real people appear in the examples.
