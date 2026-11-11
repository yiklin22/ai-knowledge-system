---
id: cpt_bpy1s28v
schema: 2
type: concept
title: Context window and compaction
aliases:
- context management
domains:
- ai
summary: What fills an agent's context (instructions, tools, messages, files, results) and how cost, speed and accuracy depend on it; compaction summarises when it fills.
tags:
- agents
status: draft
confidence: low
created: '2026-11-08'
updated: '2026-11-08'
sources:
- id: src_qu8mtfb9
  locator: Chat templated prompts
  quote: 'LLMs are stateless: every time they execute a prompt they start from the same blank slate.'
- id: src_kp4s3ioh
  locator: Keep cost and context down
  quote: null
- id: src_8s1mxx4c
  locator: 04:49
  quote: null
- id: src_en5a34og
  locator: 02:35
  quote: garbage in always gives you garbage out
- id: src_21xqrlz9
  locator: '10:21'
  quote: think of the tokens in the context window as a precious resource
relations:
- rel: related
  id: cpt_mta00ls5
- rel: related
  id: cpt_aj415iv5
- rel: related
  id: cpt_zbtvdo2y
- rel: related
  id: cpt_p776cv1f
- rel: related
  id: clm_bbulo1rc
recall:
- q: Why does a session that has handled three unrelated tasks cost more on the fourth?
  a: Every request sends the whole conversation, so the earlier tasks are re-read each turn; /clear between unrelated tasks avoids this.
- q: What is compaction?
  a: Summarising the conversation when the window fills so the session can continue; the docs say it is triggered automatically before the window fills.
- q: What three questions should you ask before adding a tool to an agent?
  a: What does it return, how big is it, and how much of it is used; compare the /context breakdown before and after calling it.
probes:
- q: Your agent starts at 20,000 tokens before you type anything. What could be in there?
  looks_for: System prompt, tool definitions (including MCP tools), instructions and skills; a context command can show the breakdown.
- q: One tool returns a whole web page and another returns three fields as JSON. How does that change the session?
  looks_for: Large tool results sit in the window and are resent every turn, raising cost and latency and crowding out detail; targeted output keeps the window small.
---

# Context window and compaction

## Knowledge
- Everything the model sees at once: system prompt, tool definitions, messages, files read and tool results.
- LLMs are stateless; the harness replays the conversation each turn, so input grows and caching matters.
- When the window fills, the harness compacts (summarises) the conversation.
- A chat is a growing token stream that the user and model both extend; this stream is the model's working memory. [fact] (Karpathy re-upload, 00:30)

## Evidence
- LLMs are stateless and the conversation is replayed; cached input tokens are cheaper. [fact] (Willison, How coding agents work)
- Every request sends the whole conversation; unrelated tasks in one session are re-read each turn; /clear and /compact with a focus are the usual fixes. [fact] (Claude Code docs, Keep cost and context down)
- The docs say the prompt cache lasts about an hour on a subscription and five minutes on API keys. [fact] (Claude Code docs; volatile, as of the page read on 2026-11-08)
- Amjad says newer models handle larger specs by compacting once rather than splitting work; older advice about a "dumb zone" past about 150k tokens is, in his view, outdated. [fact] (Amjad loops video, 04:49; second-hand creator claim)
- Tech With Tim lists what fills the context (system prompt, tool definitions, messages, files read, every tool result) and names three effects of a fuller window: cost (the whole context is resent), speed and accuracy; his /context view starts at about 20,000 tokens. [fact] (Tech With Tim context video, 00:44 to 02:35; creator, sponsored)
- Karpathy advises a new chat whenever the topic changes: extra tokens can distract the model, lower accuracy and make each next token slightly more expensive. [fact] (Karpathy re-upload, 09:50 to 10:52)
- In Tech With Tim's single test, tool output size drove context use (about 36,000 to 155,000 tokens for the same job); his own numbers are inconsistent, so see the claim page. [fact] (Tech With Tim context video; one test)

## Understanding
- Context is the model's only working memory, so what you put in it (and keep out of it) shapes cost, speed and accuracy. [inference]
- Subagents help partly because long outputs stay out of the main context. [fact] (Claude Code docs, subagents)
- Tools are a main way large text enters the window: choosing tools that return only what is needed is context management. [inference] (Tech With Tim test; one-off)

## Application
- Clear between unrelated tasks; compact with a focus; check usage breakdowns. [fact] (Claude Code docs)
- Before adding a tool or MCP server ask what it returns, how big it is and how much is used, and compare /context before and after. [fact] (Tech With Tim context video, 17:30 to 18:02)
- For long tasks, keep state in files and git, and consider a fresh window over compaction (see the long-horizon concept). [fact] (Claude prompting docs)

## Uncertainty
- Context limits, cache lifetimes and best practice change with each model; dated figures here may be stale. [inference]
- The Tech With Tim figures are sponsored, partly inconsistent and from one test. [fact] (see the tool-context claim)

## Related
- [[agent-harness]] — what manages the context.
- [[kv-cache]] — the underlying caching mechanism for transformers.
- [[long-horizon-agent-state-management]], [[model-context-protocol-mcp]], [[the-choice-of-tool-changes-agent-context-use-several-fold-for-the-same]], [[llm-as-a-lossy-compressed-internet]]
