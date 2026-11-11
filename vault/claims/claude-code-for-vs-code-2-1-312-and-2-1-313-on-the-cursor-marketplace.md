---
id: clm_b3cpoyyb
schema: 2
type: claim
title: "Claude Code for VS Code 2.1.312 and 2.1.313 on the Cursor Marketplace carried an SSH backdoor"
aliases: []
domains: [programming]
summary: "Phorion reports that two versions of the official Claude Code extension on the Cursor Marketplace contained a persistent SSH backdoor and that Cursor removed them; this is one vendor's analysis."
tags: [security, supply-chain, incident, volatile]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_wb8vm9mo
    locator: "TL;DR"
    quote: "Phorion has detected a backdoor in the official Claude Code for VS Code extension bundle on the Cursor Marketplace"
relations:
  - {rel: about, id: cpt_f92yye3m}
verdict: unverified
volatile: true
last_verified: 2026-11-08
---

# Claude Code for VS Code 2.1.312 and 2.1.313 on the Cursor Marketplace carried an SSH backdoor

Statement: versions 2.1.312 and 2.1.313 of the Claude Code for VS Code extension distributed through the Cursor Marketplace contained injected code that planted an SSH key, opened a reverse tunnel and persisted across reboots.

## Evidence for
- Phorion's advisory describes the code path in detail, including macOS, Linux and Windows persistence and a host-reconnaissance beacon, and says Cursor removed the affected versions. [fact] (Phorion advisory; vendor analysis)
- The revision history says the affected marketplace was corrected to Cursor and that version 2.1.312 was added per Cursor's updated notice, which suggests Cursor published its own notice. [fact] (advisory revision history; Cursor notice not read)

## Evidence against
- Single vendor source with a commercial interest (an EDR product) and a demo call to action; no independent confirmation or Anthropic statement is in the vault. [fact] (advisory; source page)
- How the extension was compromised is not explained in the portions read. [inference]
- The advisory notes a bug that stops SSH being enabled on macOS for standard users, so impact may vary; it cautions against relying on this. [fact] (advisory)

## Verdict reasoning
- Unverified: a detailed technical report from one vendor. If you use this extension, check the Cursor notice and your own hosts; the advisory says uninstalling is not enough and lists artefacts to look for. Indicator values are in the raw file only. [inference]
