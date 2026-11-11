---
id: src_wb8vm9mo
schema: 2
type: source
title: "Official Claude Code extension compromise advisory (Phorion)"
aliases: []
domains: [programming]
summary: "A macOS security vendor's technical advisory on a backdoored Claude Code for VS Code extension bundle on the Cursor Marketplace, with infection chain, detection ideas and indicators."
tags: [security, supply-chain, advisory, vendor]
status: reviewed
confidence: medium
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: clm_b3cpoyyb}
  - {rel: about, id: cpt_f92yye3m}
kind: web
reliability: vendor
raw: raw/web/2026-11-08-official-claude-code-extension-compromise-security-advisory.md
url: "https://phorion.io/blog/offical-claude-code-vsx-compromise/"
author: Calum Hall (Phorion)
published: "2026-10-30"
volatile: true
last_verified: 2026-11-08
---

# Official Claude Code extension compromise advisory (Phorion)

## Takeaways
- Finding: Phorion reports a backdoor in the Claude Code for VS Code extension bundle on the Cursor Marketplace, versions 2.1.312 and 2.1.313 (the first version was added after Cursor's own notice, per the revision history), which Cursor removed.
- Mechanism as described: injected code runs when the bundle loads, appends an attacker SSH key to authorized_keys, tries to enable SSH, opens a reverse SSH tunnel to a fixed IP, installs persistence (macOS LaunchAgent disguised as com.apple.sysmond, Linux cron, Windows task) and beacons host reconnaissance including names of environment variables that look like secrets.
- A bug on macOS means enabling SSH usually fails for a standard user, but the advisory warns not to rely on that; uninstalling the extension alone does not remove the backdoor.
- Remediation list: kill tunnels, remove persistence, remove the planted key and temp keys, rotate credentials reachable by the user.
- Single vendor's analysis (the vendor sells EDR and ends with a demo pitch); the report itself says how the extension was compromised is not covered, and Cursor's notice and the sample were not ingested. Treat the incident as reported, not independently confirmed here.
- Indicators (hashes, IP, file paths) are listed in the raw file; they are deliberately not copied into the vault.

## Locator map
- TL;DR; Revision history; Infection Chain stages 1-4; Detection Opportunities; Remediation; Indicators tables.
