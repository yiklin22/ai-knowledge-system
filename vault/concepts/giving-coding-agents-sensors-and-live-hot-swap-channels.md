---
id: cpt_ckqm2sp9
schema: 2
type: concept
title: "Giving coding agents sensors and live hot-swap channels"
aliases: [giving Claude Code ears]
domains: [ai]
summary: Connect a coding agent to real-world sensors (e.g. microphones) and a channel to push new code to the sensing devices live, so it can observe, experiment and iterate unattended.
tags: [coding-agents, feedback-loop, sensors]
status: reviewed
confidence: low
created: 2026-11-10
updated: 2026-11-10
sources:
  - id: src_iao3w460
    locator: "How I built it"
    quote: "the admin server could execute arbitrary new code on any of its clients"
relations:
  - {rel: broader, id: cpt_9ug6lxd3}
  - {rel: related, id: cpt_8ga2cohi}
  - {rel: related, id: cpt_mta00ls5}
  - {rel: introduced_in, id: src_iao3w460}
  - {rel: related, id: ent_gg0fprgh}
recall:
  - q: "Claude has no native audio input. How did Willison's setup still let Claude Code 'hear'?"
    a: "Browser listeners captured microphone audio over WebAudio and sent it via WebSockets to a Python server; Claude ran JavaScript/Python code that analysed the audio."
  - q: "Why did Beep Locator include a hot-swap module mechanism for listener devices?"
    a: "Some devices ask for microphone permission on every page reload, so pushing new code over the WebSocket avoided manually touching each device and let the agent keep experimenting unattended."
  - q: "What was the chirp for in Beep Locator?"
    a: "One device played a chirp after a detected beep so clips uploaded by all listeners could be time-aligned, a crucial step for locating the beep."
probes:
  - q: "What properties must a sensor channel have for an agent to iterate on it without a human present?"
    looks_for: "Agent can read logs/data, change the sensing code remotely, and judge results against a check, which is a feedback loop."
  - q: "What security risk does a remote code-push channel create?"
    looks_for: "Arbitrary code execution on clients; fine in a trusted local setup, dangerous if exposed."
misconceptions:
  - "Claude Code natively understands audio, so no extra code is needed."
  - "The agent did everything alone; the human only supplied the problem."
---

# Giving coding agents sensors and live hot-swap channels

## Knowledge
[fact] In Willison's project, Claude Code ran a web server connected over WebSockets to several listening devices, each running a WebAudio microphone and able to receive fresh JavaScript to execute (the `installModule()` method). The agent could then query audio logs and reconfigure the listeners. [fact] Opus 5.5 built this hot-swap mechanism in the first session; Fable 5.2 was then used to run and improve the system live.

## Evidence
[fact] Single source: Willison's account (source page "Locating the source of a mysterious beep with Claude", "How I built it", "Giving Claude Code ears"). The outcome was locating a beep to about 40cm. The author describes his role as mostly "chatting" and requesting features. No independent confirmation.

## Understanding
[inference] This extends the [[self-verification-loop]] idea from tests to physical sensing: give the agent an observable signal plus a way to change the instrument, and it can iterate without a human at each step. The hot-swap channel removed a human bottleneck (per-device permission prompts). [inference] The "ears" are analysis code, not model-level audio understanding.

```mermaid
flowchart LR
  A[Agent] -->|push code| S[Server]
  S -->|WebSocket modules| L[Listener devices]
  L -->|audio clips, events| S
  S -->|logs| A
```

## Application
Use when a problem needs sensing the environment from several points and the agent must iterate while the human is away. Avoid exposing a remote-code channel on untrusted networks.

## Uncertainty
[inference] Generality beyond audio is unknown (see [[how-far-can-coding-agents-perceive-and-act-on-the-physical-world]]). [speculation] Similar loops (webcam, USB serial) may work for other debugging, based on one second-hand anecdote in the source.

## Related
[[beep-locator]], [[llm-agents]], [[agent-harness]], [[claude-code-can-be-given-ears-via-browser-microphones-and-code-it-can]]
