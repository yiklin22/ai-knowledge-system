---
id: src_cjg71ax2
schema: 2
type: source
title: "Uncle Bob on not reading agent-written code (Jim AI Notebook video)"
aliases: []
domains: [ai]
summary: "A Chinese-language creator video summarising two interviews in which Robert C. Martin says he stopped reading agent-written code and relies on machine-checked constraints; only the description was available, not the transcript."
tags: [code-review, verification, agents, creator]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources: []
relations:
  - {rel: about, id: ent_3pp4nerd}
  - {rel: about, id: cpt_hooaxuqi}
  - {rel: about, id: clm_gruqwh4q}
kind: video
reliability: opinion
raw: raw/videos/2026-11-08-clean-code-uncle-bob.md
url: "https://www.youtube.com/watch?v=8Y6ovXMrdVs"
author: Jim AI Notebook (channel)
published: "2026-10-23"
---

# Uncle Bob on not reading agent-written code (Jim AI Notebook video)

## Takeaways
- The transcript is missing ("Transcript unavailable"), so everything here comes from the video description, chapter list and the creator's own fact-check notes. Nothing was heard from the video itself.
- The description lists three constraints Uncle Bob uses instead of reading code: unit tests as double-entry bookkeeping, the CRAP metric (cyclomatic complexity combined with test coverage), and mutation testing with "surviving mutants".
- The creator's check says CRAP is Change Risk Anti-Patterns (Savoia and Evans, 2007) and gives worked values for complexity 10: 110 with no tests, 22.5 at half coverage, 10 at full coverage.
- Uncle Bob moved from a five-station multi-agent pipeline (August) to a single senior-engineer-style agent (September), which he himself called a reversal; the creator says "pipelines are obsolete" is his view, not an industry consensus.
- Conflicts of interest are disclosed in the description: the host's company sells tools that "replace code reviews with verified intent", and Uncle Bob sells agent-development courses and books.
- Counter-evidence listed by the creator: Linus Torvalds, Simon Willison, METR (the 19% slowdown result is marked outdated by METR) and DORA 2025 (correlation, not causation).

## Locator map
- Chapters (description timestamps): 03:36 unit tests as double-entry bookkeeping; 04:32 CRAP metric; 06:29 mutation testing; 08:28 five-station pipeline; 09:25 reversal to one agent; 11:49 bad code traps agents; 14:13 disclosure and responsibility; 16:02 counter-views.
- Fact-check notes and disclosure: description, "利益揭露" and "查證與更正" blocks.
