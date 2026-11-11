# Security model

The app runs next to private documents and feeds untrusted internet text to an LLM, so it is designed around two risks: **a web page attacking the local server**, and **text in a source attacking the model**.

## Assets and trust boundaries

| Asset | Where | Trusted? |
|---|---|---|
| Approved knowledge | `vault/` | Yes: human-reviewed |
| Raw sources | `raw/` | **No.** Untrusted data from the internet, chats, documents |
| AI proposals | `proposals/` | No until a human approves |
| Learning data, clip key | `data/` | Private, never committed |

## Threats and controls

| Threat | Control | Test |
|---|---|---|
| Another website calls the local API (CSRF) | Every state-changing request needs a per-start random token that only the served page knows | `test_post_requires_token` |
| DNS rebinding | `Host` must be `127.0.0.1:<port>` or `localhost:<port>`; server binds to loopback only (Docker publishes to `127.0.0.1` only) | `test_wrong_host_rejected` |
| Malicious page posts to the clipper endpoint | `/api/clip` needs a persistent secret **and** a `chrome-extension://` origin; neither can be sent by ordinary web pages (no CORS headers are served). The page token does not open it and the clip key does not open anything else | `test_clip_needs_key_and_extension_origin` |
| Path traversal | All file access goes through `safe_under`; `/api/raw` serves only `raw/**/*.md` | `test_raw_reader_rejects_non_markdown_and_escapes`, `test_source_path_is_confined_to_raw` |
| **Prompt injection via a source** (e.g. "ignore previous instructions") | (1) Sources are labelled untrusted data in both the digest and Ask prompts, placed after the rules; (2) **least privilege**: Ask calls Claude with an empty tool list, so there is nothing to hijack; the digest agent can only write inside `proposals/` and cannot approve, edit `vault/`/`raw/`, or use the web; (3) a human approves everything before it becomes knowledge; (4) outputs are checked: forged citations and fabricated quotes are flagged | `PromptInjectionTests`, `ToolRestrictionTests`, live canary test (`KB_LIVE=1`) |
| Scope widening (reading vault when only raw was selected) | Client-supplied paths are intersected with indexed files and the kind filter; unknown scope values are dropped | `DataIsolationTests` |
| Secrets leaking | `data/clipper.key` is created with mode 600, git-ignored, and never served by any page | `test_clip_key_is_not_served_by_any_page` |
| Rendering hostile HTML from sources | The Markdown renderer escapes raw HTML; CSP is `default-src 'self'` | `test_index_page_embeds_token_and_headers` |

## Red team

`tools/kb/redteam.py` runs 26 attacks a hostile document could carry (`evals/redteam/attacks.jsonl`) and reports which layer stops each one. Results: [`docs/redteam-results.md`](redteam-results.md).

| Layer | What is checked | Runs |
|---|---|---|
| Tool policy | Would the digest agent's allow/deny list run the action the attack asks for (approve, write to `vault/`, edit `raw/`, shell out, fetch a URL)? | every push |
| Validation gate | If the attack gets a poisoned page into `proposals/`, does approval refuse it (fabricated quote, unknown source, invented domain, silent overwrite, deleted human note, forged raw path, hand-made id)? | every push |
| Prompt placement | Is the hostile text after the rules, inside the untrusted-data block, and absent from the digest prompt? | every push |
| Live model | Does the real Ask call obey? Does the real digest agent, in a throwaway copy, change anything outside `proposals/`? | on demand |

The suite found one real hole, now fixed: a source page could point its `raw` field at a file the agent had written, so an invented quote passed the verbatim check (attack K6, ADR 4).

## Known limits (honest list)

- Defences against prompt injection reduce risk; they do not make a model immune. The strongest controls are structural (no tools in Ask, write confinement, human approval), not the wording of prompts.
- A compromised local user account defeats all of this: the clip key sits in a file readable by that user.
- The extension has broad read access to the pages you clip, by design. Review what you clip.
- There is no multi-user authentication because there is one user on one machine. A hosted version would need real authentication and per-user data isolation before exposure.

## Running the checks

```
.venv/bin/python -m unittest tests.test_security          # deterministic
KB_LIVE=1 .venv/bin/python -m unittest tests.test_security # also calls Claude with injected passages
.venv/bin/python -m tools.kb.redteam                       # 26 attacks, structural layers; exits 1 if any is not blocked
.venv/bin/python -m tools.kb.redteam --live-ask 8 --live-digest 3   # adds live model runs (about a dollar)
```
