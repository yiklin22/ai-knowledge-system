---
id: clm_n0fhyrah
schema: 2
type: claim
title: "libghostty is embedded widely in production"
aliases: []
domains: [programming]
summary: The author says libghostty runs in production for millions of people across hundreds of products, including JetBrains IDE terminals; evidence is mostly links and self-reported numbers.
tags: [adoption]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - {id: src_y8ptsqp0, locator: "footnote 2", quote: "JetBrains alone reports"}
relations:
  - {rel: about, id: cpt_dhy8mr8e}
verdict: unverified
volatile: true
last_verified: 2026-11-08
---

# libghostty is embedded widely in production

## Evidence for
- [fact] The author states the C API "runs in production for millions of people across hundreds of products" (src_y8ptsqp0, intro) and that JetBrains IDE terminals now run on it, citing 12.5 million recurring active users (footnote 2, as of 2026-11-06).
- [fact] Named adopters: Neovim (approved PR, not yet merged), Turborepo, devenv, OrbStack, plus a list tracking over a hundred projects.

## Evidence against
- [fact] The author concedes numbers are rough because most consumers don't report usage (footnote 2).
- [inference] The JetBrains user count is total IDE users, not necessarily those using the new terminal, so the "millions" figure may overstate; the post gives no breakdown.

## Verdict reasoning
- [inference] Unverified: the source is the project's creator, I did not check the linked JetBrains, Neovim or other pages, and adoption details are volatile (dated 2026-11-08).
