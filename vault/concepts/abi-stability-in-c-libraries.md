---
id: cpt_x0swsenj
schema: 2
type: concept
title: "ABI stability in C libraries"
aliases: [stable C ABI]
domains: [programming]
summary: Keeping a compiled library's binary interface unchanged so programs linked against one version keep working with others; achieved by opaque handles, extensible accessors, sized structs and enforced checks.
tags: [c, abi, api-design]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources:
  - {id: src_y8ptsqp0, locator: "section 2", quote: "Every object is an opaque handle."}
relations:
  - {rel: related, id: cpt_dhy8mr8e}
  - {rel: related, unresolved: "Semantic versioning"}
recall:
  - q: "Name three API design techniques libghostty-vt uses to keep its C ABI stable."
    a: "Opaque handles for every object; enum-keyed getters/setters so new values need no new symbol; non-opaque structs that carry their size or reserved padding (also enums pinned to int)."
  - q: "What happens when a program built with newer headers links against an older libghostty?"
    a: "Unsupported queries return GHOSTTY_UNSUPPORTED instead of crashing or invoking undefined behaviour."
  - q: "Why version every exported symbol on ELF platforms?"
    a: "The dynamic loader then refuses to load a mismatched library by name, instead of failing mysteriously later."
probes:
  - q: "You want to add a new field to a public C struct without breaking existing binaries. What are your options?"
    looks_for: "Understands that struct layout is part of the ABI; fields can only be appended if the struct carries its size or has reserved padding, or the struct is opaque with accessors."
misconceptions:
  - "API compatibility (source level) is the same as ABI compatibility (binary level)."
---

# ABI stability in C libraries

## Knowledge
- [fact] An ABI (application binary interface) promise lets packagers package a library separately and lets programs dynamically link against it (src_y8ptsqp0, section 2).
- [fact] libghostty-vt's design: every object is an opaque handle; values go through a small set of enum-keyed getters and setters; newer headers on older libraries yield `GHOSTTY_UNSUPPORTED`; non-opaque structs carry their size or reserved padding; enums are pinned to `int` as far as the C standard allows (section 2).
- [fact] Enforcement: CI checks each change with libabigail against a committed baseline on Linux, golden type manifests on macOS and WebAssembly, and ELF exported symbols are versioned (section 2).

## Evidence
Single primary source, the library author's release post: src_y8ptsqp0.

## Understanding
- [inference] The enum-keyed accessor pattern turns "add a feature" into "add an enum value", so the symbol table, and hence the ABI, never grows; the cost is runtime dispatch and the need for an "unsupported" result. This follows from the described design, not from a stated rationale in the source.

## Application
- [inference] Useful for any C library intended for distro packaging or dynamic linking; less important for static, single-application builds.

## Uncertainty
- [fact] The author presents the stability goal as his belief about what makes a "high-quality and enduring C library"; that is opinion.
- [speculation] Whether the policy holds up over many releases is untested as of 1.0.

## Related
[[libghostty]]
