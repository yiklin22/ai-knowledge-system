---
id: cpt_be51ajjr
schema: 2
type: concept
title: "Prompt engineering"
aliases: [prompting]
domains: [ai]
summary: "Designing model inputs, including clear instructions, context, examples and structure, to steer outputs; current guidance from Anthropic's docs for Claude models, which is vendor-specific and changes with each model."
tags: [curriculum, prompting, volatile]
status: draft
confidence: low
created: 2026-11-08
updated: 2026-11-08
sources:
  - id: src_t2ajgzb6
    locator: "General principles, Be clear and direct"
    quote: "Think of Claude as a brilliant but new employee who lacks context on your norms and workflows."
  - id: src_t2ajgzb6
    locator: "Output and formatting"
    quote: "Tell Claude what to do instead of what not to do"
  - id: src_t2ajgzb6
    locator: "Long context prompting"
    quote: "Put long-form data at the top"
  - id: src_t2ajgzb6
    locator: "General principles intro"
    quote: "treat it as measured on that model and re-check it against your own evals"
relations:
  - {rel: prerequisite_for, id: cpt_b99cr5t8}
  - {rel: prerequisite_for, id: cpt_eripv7vv}
  - {rel: prerequisite_for, id: cpt_svq1gwub}
  - {rel: related, id: cpt_zbtvdo2y}
  - {rel: related, id: cpt_6spiyzt2}
recall:
  - q: What is the colleague test for a prompt?
    a: Show the prompt to a colleague with minimal context on the task; if they would be confused, the model will be too.
  - q: Why give the reason behind an instruction?
    a: The model can generalise from the explanation (for example text will be read aloud, so avoid ellipses) instead of following a bare rule rigidly.
  - q: Where should long documents go in a prompt, and what should you ask first?
    a: Near the top, above the instructions and query; ask the model to quote the relevant parts before doing the task.
---

# Prompt engineering

## Knowledge
- Be explicit and specific about the output you want; treat the model like a capable new employee without context on your norms. [fact] (Claude prompting docs; vendor)
- Explain why an instruction exists so the model can generalise, and say what to do rather than what not to do. [fact] (Claude prompting docs)
- Use a few relevant, diverse, structured examples (in tags) to steer format, tone and structure; separate instructions, context and inputs with XML-style tags. [fact] (Claude prompting docs)
- For long inputs (about 20k tokens or more) put the documents at the top and ask the model to quote relevant parts first. [fact] (Claude prompting docs)
- For agents, advice extends to thinking effort, tool use, subagent use, state across context windows, confirmation before risky actions, and avoiding overeagerness and test-gaming. [fact] (Claude prompting docs)

## Evidence
- The page is Anthropic's own documentation, describing how its models behave; it says any technique tied to a model should be re-checked with your own evals before applying to another model. [fact] (Claude prompting docs intro)
- Behaviours it documents have changed across model versions (for example prefill on the last assistant turn is no longer supported on newer models; manual thinking budgets are deprecated or rejected on newer ones). [fact] (Claude prompting docs; volatile)
- Only part of the page was read (lines 1-240 and 326-595 of 712). [fact] (reading note)

## Understanding
- Most advice reduces to removing ambiguity (task, audience, format, constraints) and giving the model the context a new colleague would need. [inference] (synthesis of the listed advice)
- Prompts written for one model can over- or under-trigger on another (for example overthorough exploration or subagent overuse), so keep prompts as general instructions and test them. [inference] (from the docs' model-specific warnings)

## Application
- Write the goal, constraints and output format; add the why; test with a person unfamiliar with the task. [fact] (Claude prompting docs)
- For long jobs across windows, keep state in files (see the long-horizon concept). [fact] (Claude prompting docs)
- For retrieved or third-party text, treat it as data, not instructions (see prompt injection). [inference]

## Uncertainty
- Vendor guidance, not independent research; model names and behaviours are volatile and dated 2026-11-08. [inference]
- The original stub drew only on general knowledge; this amendment adds one source only. [fact]

## Related
- [[long-horizon-agent-state-management]], [[reasoning-models-and-long-chain-of-thought]], [[prompt-injection]], [[tool-use-and-function-calling]], [[prompting-best-practices-claude-platform-docs]]
