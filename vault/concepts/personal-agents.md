---
id: cpt_hjysfcsk
schema: 2
type: concept
title: "Personal agents"
aliases: [Claws, general agents, DIY agents, agent memory files]
domains: [ai]
summary: "Agents that keep your preferences and history in plain-text memory files and, in the packaged consumer version, act proactively; includes the do-it-yourself setup and its trade-offs."
tags: [personal-agents, memory, agents]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_rmfocsxc
    locator: "02:34"
    quote: "personal agents are just the proactive version of DIY agents"
  - id: src_opi2fpk9
    locator: "slide 030"
    quote: "A Claw is really just a coding agent wearing a less threatening hat."
  - id: src_rmfocsxc
    locator: "09:20"
    quote: null
  - id: src_7yi1bz2z
    locator: "p.24, ASI06"
    quote: null
relations:
  - {rel: related, id: cpt_9ug6lxd3}
  - {rel: related, id: cpt_5tf19c1o}
  - {rel: related, id: cpt_f92yye3m}
  - {rel: related, id: qst_2wztspil}
  - {rel: related, id: ent_f21777hn}
  - {rel: related, id: qst_pa20g8j4}
recall:
  - q: What distinguishes a "personal agent" from a DIY agent according to Jeff Su?
    a: "Personal agents are the ready-made, proactive version. They use what they know about you and offer help before you ask, whereas DIY agents wait for tasks and need you to build the folders and rules."
  - q: Name two reasons the presenter still prefers DIY agents.
    a: More control over how the workspace is organised and memory files you can move between tools (less lock-in); personal agents are also newer and less capable.
  - q: Why does memory in plain files create a security question?
    a: Whatever is stored and later re-read can be poisoned; OWASP lists memory and context poisoning as a separate agent risk.
misconceptions:
  - A personal agent works only while your laptop is open.
  - Your agent's memory is private by default whatever the vendor.
---

# Personal agents

## Knowledge
- Three tiers by Su: chatbots for one-off tasks; DIY agents (Claude Code, ChatGPT Work, Codex, Gemini Spark) that read and update plain-text rules and memory files; personal agents (Meta's Muse, ChatGPT dots, Grok bot) that are the packaged, proactive version. [fact] (Su video, 00:29 to 03:36; presenter's taxonomy)
- Memory is files: Su's "Jeff OS" is 100+ text files that the agent writes and maintains, and he says Muse's own files look similar (memory.md, agent.md). [fact] (Su video, 04:07 to 09:20)
- Proactive means the agent watches events and tells you first; Su says personal agents run on dedicated cloud machines so they work when your laptop is closed. [fact] (Su video, 10:23 to 11:57; presenter's description)
- Willison: OpenClaw started a category he calls "Claws", now rebranded "personal agents" or "general agents"; they work like coding agents, writing and running code on your computer; the race is to make a safe one, and he doubts Muse is safe yet. [fact] (Willison 2026, slides 017-030; secondary)

## Evidence
- Su gives three reasons to keep DIY: personal agents are immature, impose one structure and risk ecosystem lock-in; privacy is "a personal preference" and local open-source agents trade privacy for setup effort and weaker models. [fact] (Su video, 11:57 to 13:32; opinion)
- Willison says Mac Mini shortages and install parties in China show real demand for personal agents among non-experts. [fact] (Willison 2026, slides 018 and 030; secondary reporting)
- OWASP ASI06 lists shared-context poisoning, long-term memory drift and cross-agent propagation as ways stored context becomes an attack channel. [fact] (OWASP p.24-25)

## Understanding
- A memory file is just text the agent reads each time; that makes it portable but also an injection surface, because anything written into it is trusted later. [inference] (Su's setup plus OWASP ASI06)
- "Proactive" changes the risk profile: an always-on agent with calendar, email and money access acts without a human in the loop, so least agency and approval gates matter more. [inference]

## Application
- If you build your own: keep memory in portable plain text, keep sensitive categories separate, and review what the agent writes into memory. [inference] (derived)
- If you choose a packaged agent: weigh lock-in and privacy statements by the vendor, which these sources do not verify. [inference]

## Uncertainty
- Products named (Muse, dots, Grok bot, OpenClaw) are changing fast; claims about security and privacy are vendor or presenter statements. [inference]
- Whether proactive agents can be made safe for non-experts is open; see the linked question. [speculation]

## Related
- [[llm-agents]], [[agent-instruction-files]], [[agentic-application-security-risks-owasp-agentic-top-10]], [[how-can-deceptive-behaviour-be-found-if-safety-training-can-hide-it]]
