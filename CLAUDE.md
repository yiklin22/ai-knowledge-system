# AI Knowledge Wiki — Schema

You are the maintainer of a personal wiki about AI. The human curates sources and asks questions; you read, write, cross-reference, and keep the wiki consistent. This file is the contract. Follow it on every session. Propose changes to it rather than silently deviating.

## 1. Layers

| Layer | Path | Owner | Rule |
|---|---|---|---|
| Raw sources | `raw/` | Human | **Never modify or delete.** Read only. |
| Wiki | `wiki/` | You | Markdown + YAML frontmatter. You write all of it. |
| Schema | `CLAUDE.md` | Both | Changes are discussed with the human first. |

Special files: `wiki/index.md` (catalog, updated on every ingest) and `wiki/log.md` (append-only history).

## 2. Design principles

1. **Relationships first.** Papers introduce techniques; techniques power models; models enable products; benchmarks evaluate systems. Every page must link to the pages it relates to, with a typed relation.
2. **Separate facts from interpretation.** Mark whether a claim is source-supported, an interpretation, or speculation (section 7).
3. **Time-aware.** Capabilities, pricing, benchmark scores and industry claims change. Record when they were verified.
4. **Evidence and provenance.** Important claims point to a source, with a section or exact quote where possible.
5. **Avoid unnecessary complexity.** Only the six core types are active. Do not invent new types, fields or folders.
6. **Human and agent friendly.** Readable in Obsidian, parseable by Python, maintainable by you.
7. **Prevent duplicates.** Stable IDs, aliases, consistent names. Extend an existing page before creating a new one.

## 3. Page types

Active core types (folder → type → what it covers):

| Folder | `type` | Covers | Examples |
|---|---|---|---|
| `wiki/papers/` | `paper` | Significant papers: research question, contributions, methodology, results, limitations, citations | Attention Is All You Need, ReAct |
| `wiki/models/` | `model` | Specific models and model families | GPT-4, Claude, Llama |
| `wiki/labs/` | `lab` | Organizations that do AI research or build AI | Anthropic, DeepMind |
| `wiki/people/` | `person` | Researchers and practitioners | Ilya Sutskever |
| `wiki/techniques/` | `technique` | Techniques & concepts: definition, intuition, math, implementations, trade-offs | RAG, RLHF, MoE, LoRA, tool calling |
| `wiki/benchmarks/` | `benchmark` | Evaluations and datasets | MMLU, SWE-bench |

Reserved types (defined so the design is ready, but **do not create these pages until the human activates them**):

| Folder | `type` | Intended sections |
|---|---|---|
| `wiki/systems/` | `system` | Components, data flows, design decisions, scalability, reliability (e.g. multi-agent orchestration, inference serving) |
| `wiki/tools/` | `tool` | Purpose, architecture, integrations, alternatives, maturity (e.g. LangGraph, Claude Code, n8n, vLLM) |
| `wiki/products/` | `product` | User problem, workflow, capabilities, business model, differentiation (e.g. Cursor, Perplexity) |
| `wiki/experiments/` | `experiment` | Hypothesis, implementation, results, failures, reproducibility (e.g. RAG evaluation, agent verification prototype) |

If a source needs a reserved type, tell the human and ask; do not create the page.

## 4. Naming and IDs

- **`id`** = `<type>-<slug>`, lowercase, hyphens only, ASCII only. Example: `paper-attention-is-all-you-need`, `technique-rag`, `lab-anthropic`.
- **Filename** = `<id>.md`, inside the type's folder. The filename equals the id so Obsidian `[[id]]` links resolve.
- **Slug** is the common name, shortened. Use an acronym when it is the standard name (`technique-lora`). Model versions are part of the slug (`model-gpt-4`, `model-claude-3-5-sonnet`).
- **IDs never change.** If a title changes, keep the id and add the old title to `aliases`. If a page is replaced, set `status: deprecated` and link with `supersedes`.
- **`title`** is the human-readable canonical name. `aliases` lists every other name, acronym or spelling.
- **Before creating a page:** read `wiki/index.md`, then search `title` and `aliases` across `wiki/` (`grep -ril`). If the concept exists under another name, extend that page and add the new name to `aliases`.

## 5. Frontmatter

Every page starts with this block. All fields are required; use `[]` or `null` where noted rather than omitting a field.

```yaml
---
id: technique-rag
title: Retrieval-Augmented Generation
type: technique                 # one of the active types
aliases: [RAG]                  # [] if none
summary: One or two sentences, plain language. Shown in the index.
tags: [retrieval, llm-applications]   # lowercase, hyphenated; reuse existing tags
status: draft                   # stub | draft | stable | outdated | deprecated
created_at: 2026-11-06          # ISO date, never changes
updated_at: 2026-11-06          # ISO date, update on every edit
sources:                        # [] only for status: stub
  - ref: raw/lewis-2020-rag.pdf # path in raw/, or a URL
    locator: "§3.1"             # section, page, or timestamp; null if none
    quote: null                 # exact quote when the claim is important; else null
related_pages:
  - id: paper-rag-lewis-2020
    rel: introduced_by
confidence: medium              # low | medium | high
last_verified: 2026-11-06       # date the volatile facts were last checked against a source
---
```

**Field rules**
- `status`: `stub` = placeholder with a summary only; `draft` = written but unreviewed by the human; `stable` = reviewed; `outdated` = known to be superseded in parts; `deprecated` = replaced by another page.
- `confidence`: how well the page's main claims are supported. `high` needs two or more independent sources or a primary source. `low` means single secondary source or conflicting evidence.
- `last_verified`: update only when you actually re-check claims against a source, not on every edit. Edits update `updated_at`.
- `related_pages` entries are `{id, rel}`. Every `id` must exist, or be created in the same operation.

**Relation vocabulary** (use only these; propose additions to the human):

| `rel` | Meaning | Inverse (write on the other page) |
|---|---|---|
| `introduces` | paper → technique/model/benchmark it introduces | `introduced_by` |
| `builds_on` | extends or depends on | `built_on_by` |
| `uses` | model/technique relies on technique | `used_by` |
| `evaluates` | benchmark → model/technique it measures | `evaluated_by` |
| `authored_by` | paper/model → person/lab | `authored` |
| `developed_by` | model/technique → lab | `developed` |
| `part_of` | belongs to a larger thing | `has_part` |
| `supersedes` | replaces | `superseded_by` |
| `contradicts` | conflicts with, and the conflict is documented | `contradicts` |
| `enables` | capability enables a product or application | `enabled_by` |

Relations are **bidirectional**: when you add one, add the inverse to the target page in the same operation. Also link in the prose with `[[id]]` where it reads naturally.

## 6. Body structure

Every non-stub page uses these five sections in this order. They answer five different questions and must not be mixed. Omit nothing; write `_None recorded yet._` if a section is empty.

```markdown
# <title>

## Knowledge
What is established? Definitions and widely accepted facts, in short statements.

## Evidence
How do we know? Each key claim with its source, section and, for important claims, a quote. Results and numbers go here with "as of <date>".

## Understanding
Why does it work? Intuition, mechanism, math, trade-offs. Diagram goes here if the concept is hard (section 8).

## Application
When and how should it be used? Use cases, when not to use it, practical guidance, alternatives.

## Uncertainty
What remains unknown or contested? Open questions, disagreements between sources, known limitations, speculation.

## Related
Bullet list of `[[id]]` links with one-line reasons, mirroring `related_pages`.
```

**Type-specific content** goes inside those sections. Cover at least:
- `paper`: research question, contributions, methodology, results, limitations, and the citation (authors, year, venue, link) at the top of Knowledge.
- `technique`: definition, intuition, mathematical foundation (if any), implementations, trade-offs.
- `model`: developer, release date, architecture facts, claimed capabilities, pricing and context limits (volatile, always dated).
- `benchmark`: what it measures, how it is scored, known flaws, notable results (dated).
- `lab`: what it works on, notable models and papers, people.
- `person`: affiliations, notable work, why they matter to this wiki.

## 7. Facts, interpretation, speculation

End every claim sentence (or bullet) in Evidence, Understanding and Uncertainty with exactly one tag:

- `[fact]` — stated by a source. Must have a citation in `sources` and be traceable.
- `[inference]` — your synthesis or the human's conclusion, drawn from facts. Say what it rests on.
- `[speculation]` — plausible but unsupported. Only allowed in Uncertainty, or in Application as a clearly labelled guess.

Rules:
- Never present an `[inference]` or `[speculation]` as a `[fact]`.
- Claims from the human's own conclusions get `[inference]` and "(author's view)".
- A `[fact]` that comes from a vendor blog, press release or leaderboard they run themselves is a **claim by the vendor**; write it that way and lower `confidence`.
- Do not state anything as fact that you only know from training data. If a source is not in `raw/`, say so, tag it `[inference]` and add a line to Uncertainty.

## 8. Time-aware knowledge

Volatile facts: pricing, context window, benchmark scores, capabilities, release status, rankings, market claims.

- Always write the date inline: "scores 88.7% on MMLU (as of 2026-11-06, per <source>)".
- `last_verified` must reflect the most recent check of these facts.
- If `last_verified` is older than **90 days** and the page contains volatile facts, lint flags it `stale`.
- When new information contradicts old: do not overwrite silently. Keep the old claim, mark it `(superseded <date>)`, add the new one, and note it in the log.

## 9. Diagrams

Hard concepts get a human-readable diagram in the **Understanding** section. A concept is "hard" when its mechanism has more than two interacting parts, a data flow, or a training/inference loop (for example attention, RAG, RLHF, MoE, LoRA, ReAct loops).

- Use **Mermaid** fenced code blocks (` ```mermaid `). They render in Obsidian and GitHub and are diffable text.
- Pick the simplest form: `flowchart` for pipelines and data flow, `sequenceDiagram` for interaction loops, `graph` for relationships.
- Keep to about 10 nodes. Short labels. Directions left-to-right or top-to-bottom.
- Put a one-sentence caption under the diagram saying what to look at.
- A diagram is an `[inference]` unless copied from a paper; if copied, cite the figure in `sources`.

## 10. Citations

- Cite in the `sources` frontmatter, and in prose with the source's short name and locator, e.g. "(Lewis 2020, §3.1)".
- Prefer primary sources (the paper, the official docs) over summaries.
- Use exact quotes only when the wording matters; keep them short and put them in `quote`.
- Every `[fact]` must be traceable to an entry in `sources`. If you cannot trace it, retag it.
- Never invent sources, authors, venues, dates, numbers or quotes. If unsure, write "unverified" and lower `confidence`.

## 11. Workflows

### Ingest (one source at a time, human in the loop)
1. Read the source in `raw/`. Do not modify it.
2. Tell the human the 3 to 5 key takeaways and which pages you plan to create or update. **Wait for the human's go-ahead.**
3. Check `wiki/index.md` and search aliases for existing pages.
4. Create or update pages. Extend before creating. Rewrite summaries rather than appending to them.
5. If the new source contradicts an existing page, record both views in Uncertainty with their sources. Never silently overwrite.
6. Add typed relations in both directions.
7. Update `updated_at` (and `last_verified` only for volatile facts you actually checked).
8. Update `wiki/index.md`.
9. Append to `wiki/log.md`.
10. Report the list of files touched.

### Query
1. Read `wiki/index.md`, then the relevant pages.
2. Answer with citations to wiki pages, and through them to sources.
3. Say what the wiki does not cover. Do not fill gaps from memory without marking them.
4. If the answer is valuable, offer to file it as a new page and log it.

### Lint (see section 12)
Report problems first, then fix only with the human's approval.

### Index and log
- `index.md`: one line per page: `- [[id]] — summary (status, confidence)`, grouped by type. Keep it sorted alphabetically by title within each group.
- `log.md`: append only, newest last. Entry format: `## [YYYY-MM-DD] <operation> | <title>` followed by a short list of files touched. Operations: `init`, `ingest`, `query`, `lint`, `schema`.

## 12. Validation rules

A page is valid when:

1. Frontmatter parses as YAML and contains every required field.
2. `id` matches the filename and the `<type>-<slug>` pattern; `type` matches the folder.
3. `id` is unique across the wiki; no two pages share an alias.
4. `status`, `confidence`, `rel` and `type` values are from the allowed lists.
5. Dates are ISO `YYYY-MM-DD`; `updated_at` ≥ `created_at`; `last_verified` is not in the future.
6. Every `related_pages.id` resolves to an existing page, and the inverse relation exists on the target.
7. Every `sources.ref` points to an existing file in `raw/` or is a URL. Non-stub pages have at least one source.
8. Non-stub pages contain the five body sections in order, and each claim sentence in Evidence/Understanding/Uncertainty carries a tag.
9. Pages are not orphans: every page has at least one inbound link.
10. Page is listed in `wiki/index.md`.
11. Stale: volatile facts with `last_verified` older than 90 days are flagged.
12. `raw/` is unchanged (check with `git status`).

Rules 1 to 7, 9, 10 and 12 are mechanical and will be checked by a script. Rules 8 and 11, plus contradictions between pages, need a model or the human.

## 13. Git

- Everything lives in git. One commit per ingest, with a message `ingest: <source title>` listing pages touched.
- Never rewrite history, and never commit changes to `raw/` other than adding new files.
