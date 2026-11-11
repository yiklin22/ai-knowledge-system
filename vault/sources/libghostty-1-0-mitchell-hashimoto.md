---
id: src_y8ptsqp0
schema: 2
type: source
title: "Libghostty 1.0 (Mitchell Hashimoto)"
aliases: []
domains: [programming]
summary: Hashimoto's release post for libghostty-vt 1.0, a portable C terminal-emulation library with a stable, CI-enforced ABI, plus a list of adopters.
tags: [terminal, c-library, abi]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: authored_by, id: ent_dy7sielk}
  - {rel: about, id: cpt_dhy8mr8e}
  - {rel: about, id: cpt_x0swsenj}
kind: web
reliability: primary
raw: raw/web/2026-11-08-libghostty-1-0.md
url: "https://mitchellh.com/writing/libghostty-1-0"
author: "Mitchell Hashimoto"
published: "2026-11-06"
---

# Libghostty 1.0 (Mitchell Hashimoto)

Reliability: primary for what 1.0 contains and how it is built (written by the project's creator), but promotional for adoption and "better than most terminals" claims, which are self-reported. The author states the post was hand-written without AI.

## Takeaways

- libghostty-vt 1.0 (2026-11-06) makes the library and its C ABI stable, under semantic versioning.
- ABI stability comes from design (opaque handles, enum-keyed getters/setters, sized structs) and CI enforcement (libabigail, versioned symbols).
- It is MIT licensed, needs only libc (or nothing with SIMD off), and is built and tested across Linux, macOS, iOS, Windows, Android, FreeBSD and WASM.
- Adopters named include JetBrains IDE terminals, Neovim (approved PR), Turborepo, OrbStack and many bindings.
- Own release cycle and packaging tarballs so distros can package it.

## Locator map
- Adoption list: section 1 ("Since starting the Ghostty project…")
- ABI design and CI: section 2 ("1.0 means…")
- Packaging: section 3
- Licensing and dependencies: section 4
- Platform tables and resource use: section 5
- Closing: section 6
- Footnotes 1-5: end of page (footnote 3 corrects the "not even libc" claim)
