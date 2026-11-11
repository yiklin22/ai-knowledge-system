---
id: cpt_eripv7vv
schema: 2
type: concept
title: Tool use and function calling
aliases: []
domains:
- ai
summary: A model emitting structured tool calls that the harness executes, with results fed back to the model.
tags:
- curriculum
status: draft
confidence: medium
created: 2026-11-08
updated: '2026-11-08'
sources:
- id: src_qu8mtfb9
  locator: Calling tools
  quote: A tool is a function that the agent harness makes available to the LLM.
- id: src_2hzno5ws
  locator: Appendix 2
  quote: we actually spent more time optimizing our tools than the overall prompt.
relations:
- rel: prerequisite_for
  id: cpt_9ug6lxd3
- rel: prerequisite_for
  id: cpt_svq1gwub
recall:
- q: How does a harness execute a tool call?
  a: It extracts the call from the model's response (for example with a regular expression), runs the function, and returns the result to the model in the next prompt.
- q: What did Anthropic change in its SWE-bench tools to stop path errors?
  a: It required absolute file paths, after finding the model erred with relative paths once it had moved out of the root directory.
probes:
- q: Why might a tool format that requires counting lines or escaping code be hard for a model?
  looks_for: Formats with overhead (accurate line counts in diffs, string escaping in JSON) are harder to write; prefer formats close to natural text and give the model room to think.
---

# Tool use and function calling

## Knowledge
- A tool is a function the harness makes available to the LLM. The model emits a tool call, the harness runs it, and the result goes back into the prompt.
- Tool definitions deserve as much prompt engineering as the main prompt.

## Evidence
- At the prompt level, the system message describes the tool and its call format; the harness parses the call with something like a regular expression and returns a constructed result prompt. [fact] (Willison, Calling tools)
- The most powerful tools allow code execution, such as Bash() or Python(). [fact] (Willison)
- Anthropic: design tools like human-computer interfaces; include examples, edge cases and boundaries; poka-yoke the arguments; test how the model uses them. [fact] (Anthropic, Appendix 2)
- Anthropic found requiring absolute file paths removed a class of mistakes in its SWE-bench agent. [fact] (Anthropic, Appendix 2)

## Understanding
- The model never executes anything; it only produces text that the harness interprets. [inference] (from Willison's description)
- Tool ergonomics for models resemble API design for junior developers: obvious names, clear parameters, hard-to-misuse inputs. [inference] (Anthropic's docstring analogy)

## Application
- Give models formats close to what appears naturally in text, with no counting or escaping overhead. [fact] (Anthropic, Appendix 2)

## Uncertainty
- Anthropic's post notes tooling has changed since December 2024 (for example MCP and managed agents). [fact] (Anthropic page note)
- This page does not yet cover MCP or protocol standards in depth. [inference]

## Related
- [[llm-agents]] — what uses tools in a loop.
- [[agent-harness]] — what executes them.
