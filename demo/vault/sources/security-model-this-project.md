---
id: src_vs3k1ezx
schema: 2
type: source
title: Security model (this project)
aliases: []
domains:
- programming
summary: 'The project''s threat model: a web page attacking the local server and text in a source attacking the model, with a control and a test for each threat.'
tags:
- demo
status: draft
confidence: medium
created: 2026-11-11
updated: 2026-11-11
sources: []
relations: []
kind: document
reliability: primary
raw: raw/documents/2026-11-10-security-model.md
url: null
author: project author
published: '2026-11-10'
---

# Security model (this project)

## Takeaways
- Raw sources are untrusted data; approved vault pages are trusted because a human reviewed them.
- Prompt injection is handled by least privilege and human approval first, prompt wording second.
- The document lists its own known limits.

## Locator map
- Assets and trust boundaries: first table
- Threats and controls: second table
- Known limits (honest list)
