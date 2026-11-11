---
id: cpt_dhy8mr8e
schema: 2
type: concept
title: "Libghostty"
aliases: [libghostty-vt]
domains: [programming]
summary: A portable, MIT-licensed C library for terminal emulation extracted from Ghostty; 1.0 (2026-11-06) stabilised the library and its C ABI.
tags: [terminal, c-library, embedding]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources:
  - {id: src_y8ptsqp0, locator: "intro", quote: "a portable, high-performance C library for terminal emulation, extracted"}
relations:
  - {rel: derived_from, id: ent_r6iwfis6}
  - {rel: authored_by, id: ent_dy7sielk}
  - {rel: introduced_in, id: src_y8ptsqp0}
  - {rel: prerequisite_for, id: cpt_x0swsenj}
recall:
  - q: "What does libghostty-vt provide, and what does it not?"
    a: "Terminal emulation (parsing protocols/sequences, state, Kitty graphics etc.), not the GUI application; embedders build the UI. Features means protocols understood and performance means parsing throughput and memory."
  - q: "What are libghostty-vt's runtime and licensing constraints?"
    a: "MIT licensed; runtime needs only libc (freestanding if SIMD is off); no copyleft dependencies; creates no threads and allocates via a customisable allocator."
---

# Libghostty

## Knowledge
- [fact] `libghostty-vt` is a C library for terminal emulation extracted from Ghostty's core; 1.0 means library and C ABI are stable, with semantic versioning (src_y8ptsqp0).
- [fact] MIT licensed; dependencies are simdutf, Google Highway, a Unicode table and Wuffs (for Kitty graphics image decoding); no copyleft code and no C++ standard library dependency.
- [fact] Default build links libc; with SIMD off it is freestanding (footnote 3 corrects the earlier "not even libc" claim).
- [fact] Creates no threads, uses a pluggable allocator. CI builds and tests Linux (glibc, musl), macOS 13+, iOS 13+, FreeBSD, Windows x86_64, Android and wasm32; more platforms build without tests.
- [fact] Separate release cycle and tarballs from the Ghostty app, with a signed source tarball and dependencies tarball for offline distro builds.
- [fact] Feature flags can compile out subsystems (input encoding, search, selection, Kitty graphics); functions then return `GHOSTTY_UNSUPPORTED`.

## Evidence
All from the author's post, src_y8ptsqp0. Adoption is in [[libghostty-is-embedded-widely-in-production]].

## Understanding
- [inference] Sharing one emulator core lets bug fixes and protocol support propagate to all embedders, which the author names as the point (section 6); this is the stated rationale, not independently tested.

## Application
- Use when building a terminal, TUI test harness or terminal-rendering feature in any language with C FFI, rather than writing a new emulator.
- [fact] The author says a terminal can be created in about 1,500 lines of C (the "ghostling" example).

## Uncertainty
- [fact] The author claims better features/performance than most terminals; footnote 5 limits this to protocols understood, parsing throughput and memory. Self-reported, no benchmark given.
- [fact] The 10,000-terminal test is a single anecdote by the author.

## Related
[[abi-stability-in-c-libraries]], [[ghostty]]
