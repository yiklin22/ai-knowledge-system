---
id: ent_gg0fprgh
schema: 2
type: entity
title: "Beep Locator"
aliases: []
domains: [programming]
summary: Simon Willison's Claude-Code-built tool that triangulates a mysterious beep using several browser-based listener devices coordinated by a Python server.
tags: [web-audio, websockets, triangulation]
status: reviewed
confidence: medium
created: 2026-11-10
updated: 2026-11-10
sources:
  - id: src_iao3w460
    locator: "Locating the source of a mysterious beep with Claude"
    quote: "a software system for triangulating the source of a mysterious beep using multiple devices scattered around the room"
relations:
  - {rel: introduced_in, id: src_iao3w460}
  - {rel: authored_by, id: ent_lh5mezgp}
  - {rel: related, id: ent_8f72s5bf}
  - {rel: about, id: cpt_ckqm2sp9}
kind: tool
---

# Beep Locator

## Who/what
[fact] A Python web server plus browser listeners (WebAudio microphone, WebSockets) built with Claude Code by Simon Willison. Listeners keep a 60 second audio buffer and run an FFT and high-pass-filter beep detector. On a detection the server has one device play a chirp, then collects clips from all listeners and aligns them using that chirp. Features added during the session: rough mode (drag devices on a map), clap test mode, replay, "This is the mystery beep" labelling, repositioning, and suggested listener positions. Source code is on GitHub (simonw/beep-locator); it was not read here.

## Why it matters
[fact] It found the beep to within about 40cm, leading to an old carbon monoxide detector needing batteries. [inference] It is a worked example of [[giving-coding-agents-sensors-and-live-hot-swap-channels]]; one anecdote, so accuracy in other rooms is unknown.
