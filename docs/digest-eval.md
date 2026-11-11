# Digest quality (approved vault, 2026-11-11)

What the digest agent wrote, measured against the rules it is given. Deterministic unless marked.

| check | result | why it matters |
|---|---|---|
| Quotes found verbatim in the raw source | **160/160 (100%)** | a quote that is not in the source is a fabricated citation |
| Citations that carry a quote | 160/224 (71%) | evidence density: a citation without a quote is harder to check |
| Citations that carry a locator (page, section, timestamp) | 224/224 (100%) | lets a reader jump to the passage |
| Claims backed by at least one quote | 38/39 (97%) | claims are where disagreement lives |
| Claims that tag fact / inference / speculation | 39/39 (100%) | separates what the source says from what the model inferred |
| Concepts with recall cards | 46/46 (100%) | feeds spaced repetition |
| Concepts with all six sections in order | 46/46 (100%) | schema conformance |
| Likely duplicate pages (same type, title similarity ≥ 0.82) | **0 pair(s)** | the agent should amend an existing page, not add a second one |
| Relations pointing at a page that does not exist yet | 5/501 (1%) | written as `unresolved`, never a guessed id |
| Validation | 0 error(s), 1 warning(s) | the approval gate refuses any batch with errors |

Pages: 208 (81 concept, 49 source, 39 claim, 21 entity, 17 question, 1 map). Claim verdicts: {'unverified': 18, 'supported': 16, 'contested': 5}. Source reliability grades: {'secondary': 16, 'vendor': 9, 'primary': 8, 'opinion': 16}. Raw files with a source page: 49 of 538.

## Does the claim follow from its quote? (model judge, 12 sampled claims)

**9 supported, 2 partial, 1 honest counter-evidence on a contested claim, 0 unsupported** (one tool-less call, $0.14).

| claim | recorded as | judge | judge's reason |
|---|---|---|---|
| Given a clear goal, unambiguous constraints and tools, frontier models solve problems by b | unverified | supported | The passage states that Fable class models solve problems through brute force when given a clear goal, unambiguous constraints and tool access. |
| Splitting a spec into tickets run by separate subagents improves results | contested | counter-evidence | The passage argues that splitting specs into tickets for subagents leads to worse results, which fits the recorded 'contested' verdict. |
| Agents need a pass/fail check to know whether work is really done | supported | supported | The passage says that without a check that returns pass or fail, Claude has only 'looks done' to go on, and that such a check lets it close the loop itself. |
| MCP standardises tool discovery above function calling | supported | supported | The passage says MCP standardizes function calling so each tool is defined once and every model can call it the same way, which matches the claim. |
| GPUs realize under 30% of memory bandwidth in inference while Positron claims over 90% | unverified | supported | The passage, from Positron's own text, states over 90% realized memory bandwidth versus under 30% for GPUs, so it supports the claim as a Positron claim. |
| Agents given similar context make similar decisions, so single errors can replicate | supported | supported | The passage says agents with the same or similar context act very similarly, so one agent's bad decision is likely to be replicated across many agents. |
| Reinforcement learning on verifiable rewards alone can elicit reasoning without human reas | supported | supported | The passage describes RL with a reward based only on final-answer correctness and no prior SFT, and says diverse reasoning behaviours emerged. |
| Vibe coding and agentic engineering are different practices | supported | supported | The passage distinguishes vibe coding, meaning unreviewed prototype-quality code, from code brought up to a production-ready standard in agentic engineering. |
| In coding agents, compilers and tests catch most hallucinated code | unverified | partial | The passage says agents see compile, lint and test errors when an LLM invents a function signature, but it does not say these checks catch 'most' hallucinated code. |
| Per-step error compounds across an agent workflow | supported | supported | The passage states that each step introduces a small error and that the errors multiply, which matches the claim. |
| Neural reward models invite reward hacking in large-scale RL | supported | supported | The passage says neural reward models are susceptible to reward hacking during large-scale reinforcement learning. |
| More capable models may be more likely to misreport success, so verification is still need | unverified | partial | The passage says more capable models are more likely to cheat, with an example of Fable 5 lying, and says verification is needed. It does not state that they misreport success more often, and the evid |

## How to read this

- **Scope.** The vault only holds batches that passed the approval gate, and the gate already refuses non-verbatim quotes, so a perfect verbatim score here confirms the gate works; it is not a measure of the agent's first draft. Run with `--batch <name>` on an unreviewed batch for that.
- **Duplicates** are detected from titles only. Two pages can cover the same idea under different names and not be flagged; a flagged pair may be legitimately distinct (for example a claim and its negation).
- **The judge** is a model grading a model's work from a few hundred characters around the quote, on a small seeded sample. Treat it as a smoke test for unsupported claims, not as an accuracy figure. It sees only the claim's title and one cited passage, not the page body, where a claim is often qualified. It is also not stable: an earlier run on the same 12 claims graded 6 supported and 5 partial, before the judge was shown each claim's recorded verdict.
- **Reproduce:** `.venv/bin/python -m tools.kb.digest_eval --judge 12 --write docs/digest-eval.md`
