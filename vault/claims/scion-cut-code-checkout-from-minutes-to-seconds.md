---
id: clm_uw2nbvpg
schema: 2
type: claim
title: "Scion cut code checkout from minutes to seconds"
aliases: []
domains: [programming]
summary: "Anthropic reportedly says its server-side Scion version control cut CI and agent code checkout from minutes to seconds and saved about 25% of CI CPU; secondary sources also disagree on repository size."
tags: [version-control, performance, volatile]
status: reviewed
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_fuuc8606
    locator: "Paragraph 6"
    quote: "CI及研究工作取出程式碼的時間也從數分鐘縮短至數秒"
  - id: src_fuuc8606
    locator: "Paragraph 6"
    quote: "CI另節省約25%的CPU容量"
  - id: src_21l5zt28
    locator: "02:17"
    quote: "For a developer pulling the latest code, Git took around 87 seconds."
  - id: src_21l5zt28
    locator: "01:14"
    quote: "The history of its main branch alone is almost 800 GB"
  - id: src_fuuc8606
    locator: "Paragraph 3"
    quote: "主分支歷史資料接近100 GB"
relations:
  - {rel: about, id: ent_xkssuk8m}
  - {rel: about, id: cpt_boy7hba5}
verdict: unverified
volatile: true
last_verified: 2026-11-08
---

# Scion cut code checkout from minutes to seconds

Statement: moving to the server-side Scion system reduced the time for CI and agents to get code from minutes to seconds on Anthropic's monorepo.

## Evidence for
- iThome reports Anthropic's internal measurements: checkout time for CI and research jobs fell from minutes to seconds and CI saved about 25% of CPU capacity. [fact] (iThome, secondary summary of Anthropic's post)
- A creator's video narrates a comparison on the same codebase: pulling the latest code 87 s on Git versus 3.5 s on Scion; fresh agent copy over 7 minutes versus 5 s; checking what changed about 4 s versus 19 ms. [fact] (Andy Lin video, 02:17 to 02:48; third-hand)

## Evidence against
- The primary Anthropic post was not ingested, so the figures are unverified secondary reports. [fact] (source pages)
- The two secondary sources disagree on main-branch history size: iThome says close to 100 GB, the video says almost 800 GB. One may be a mistranscription or a different measure; this page cannot tell which. [fact] (iThome paragraph 3; video 01:14)
- Anthropic says Scion is not a suitable general replacement for Git and needs its own review, search and CI tools, so the speedup is specific to its scale. [fact] (iThome; video 07:27 quoting Anthropic)

## Verdict reasoning
- Unverified: the claim is the vendor's own measurement relayed second- and third-hand, with a discrepancy in a related number. Fetch the Anthropic engineering post "Redesigning source control at Anthropic" before trusting figures. [inference]
