---
id: qst_abxsnrqw
schema: 2
type: question
title: "Does libghostty's ABI stability policy hold across releases?"
aliases: []
domains: [programming]
summary: Version 1.0 promises a stable C ABI enforced in CI; it is untested over later releases, so whether the promise holds is open.
tags: [abi]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: cpt_x0swsenj}
  - {rel: about, id: cpt_dhy8mr8e}
state: open
---

# Does libghostty's ABI stability policy hold across releases?

## Why I'm asking
[inference] The source (src_y8ptsqp0) describes the ABI design and CI checks, but 1.0 is the first stable release, so there is no track record yet.

## What would answer it
Checking later libghostty-vt releases for ABI breaks, whether `GHOSTTY_UNSUPPORTED` fallbacks work as described, and how downstream packagers report upgrades.
