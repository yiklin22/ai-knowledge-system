# Personal Knowledge System

[![CI](https://github.com/yiklin22/ai-knowledge-system/actions/workflows/ci.yml/badge.svg)](https://github.com/yiklin22/ai-knowledge-system/actions/workflows/ci.yml)

> **AI you can audit.** Chat-with-your-documents tools answer fluently and invent citations. Here the AI only *proposes*; every claim carries a verbatim quote that is re-checked against the source, and a human approves before anything becomes knowledge.
>
> - **Try it in one command:** `./demo.sh` (sample vault, throwaway folder, your data untouched)
> - **Evidence:** hybrid retrieval hit@1 75% vs 50% keyword ([eval](docs/eval-results.md)), [digest quality](docs/digest-eval.md), [threat model with a test per control](docs/security.md), 96 tests in CI
> - **Read first:** [case study (one page)](docs/case-study.md) · [architecture](docs/architecture.md) · [customer discovery plan](docs/customer-discovery.md)

Throw in AI chats, documents, work files, YouTube links and websites, on **any subject**. Claude reads them and **proposes** structured, evidence-linked knowledge; you approve it in the browser; then you learn it with a personal learning map, concept maps, interactive playgrounds, a Socratic tutor, spaced repetition and build tasks.

## Measured

| Question | Result | Report |
|---|---|---|
| Can a hostile document make the agent approve its own work, write to the vault, tamper with sources or send data out? | **18 of 18** such attacks are stopped by code, whatever the model does. In live runs the agent was contained in 3 of 3 poisoned digests and the Ask call resisted 8 of 8 injected instructions | [red team](docs/redteam-results.md) |
| Are the quotes real? | **160 of 160** quotes in the approved vault are found verbatim in their source; every citation has a locator | [digest quality](docs/digest-eval.md) |
| Do claims follow from the passage they cite? | In a 12-claim sample a model judge graded 9 supported, 2 partial, 1 honest counter-evidence, 0 unsupported | [digest quality](docs/digest-eval.md) |
| Does retrieval find the right source? | Hybrid search ranks it first in **75%** of 20 questions (keyword search: 50%) and in the top 5 in 95% | [retrieval](docs/eval-results.md) |
| What does it cost, and how often is the agent's work accepted? | Logged per call and per review from now on; no history yet | `./kb metrics` |

The live numbers are small samples from one model on one day, and each report says what it does not show. The red team also found a real hole in the quote check, which is now fixed ([ADR 4](docs/adr/0004-evidence-checked-by-code.md)). The reasoning behind the main design choices is in the [decision records](docs/adr/README.md).

## Try it without your own data

```
./demo.sh                                              # http://127.0.0.1:8766, needs the Python setup below
docker compose -f docker-compose.demo.yml up --build   # same, in a container
```

Both run the app on a small sample vault (`demo/`, built from this project's own design documents) in a throwaway copy. Your own vault is not touched and nothing you do in the demo is kept.

## Start it

```
./web            # then open http://127.0.0.1:8765
```

It runs only on your own machine. No command line is needed after this. Press **Ctrl+K** anywhere to jump to any page or action.

| Page | What it does |
|---|---|
| **Home** | Today's plan: cards due, what to learn next, your streak, your subjects |
| **Learn** | Your **personal learning map**: every concept in the order you should learn it, coloured by what you know, with gaps flagged and a **placement check** to find your real level |
| **Concept maps** | AI-generated maps for hard ideas: generate one from any vault concept or any topic you type. Click a node to read it; download as SVG |
| **Library** | Every page with its evidence; clicking a citation opens the **source with the exact quote highlighted**. Select text in a source to **highlight and annotate** it |
| **My maps** | **Build your own knowledge maps.** Drag in vault pages or your own ideas, draw labelled links, add notes and colours, tidy, undo, export as SVG. Start blank or from a vault concept; keep one map per topic. Auto-saved, and it never changes your vault |
| **Study** | Spaced-repetition recall cards (try answering from memory first; keys 1-4 to grade) |
| **Tutor** | A Socratic tutor grounded in your vault and your history; records your level when you finish |
| **Add / Review** | Add files, links or text; Claude proposes pages; you read the diffs and approve |

Also: **Playgrounds** (interactive simulations: change variables, predict first, see what happens) and **Build mode** (turn a concept into a coding exercise, experiment, essay or mini project, with hints that never give the answer and a Socratic reviewer). Open them from any concept page or the Learn page.

## Ask your sources

The **Ask** page answers questions like *what is an agent harness?* from your own material. Choose where to look (approved vault, web pages, videos, documents, AI chats, or specific sources you tick), and Claude answers only from the passages it finds, with clickable citations [1], [2] that open the passage (with its timestamp or page) and the full source. It says what your sources do not cover and labels anything from its own knowledge. Approved vault pages rank above unreviewed raw sources. The search index (`build/ask.db`) is derived and rebuilds itself when sources change.

## Browser clipper (Chrome / Edge)

Clip a page, selection, link or YouTube video from the browser; it is saved as a raw source and **digested automatically** into a proposal batch (you still approve it in Review).

1. Keep `./web` running.
2. `chrome://extensions` > turn on **Developer mode** > **Load unpacked** > choose the `extension/` folder.
3. Click the extension, paste the key from `data/clipper.key` (created on first `./web` start). One time only.
4. Use the popup, the right-click menu, or **Alt+Shift+K** (clips the selection, or the whole page if nothing is selected).

The key and a `chrome-extension://` origin are both required, so ordinary web pages cannot post to your server. Untick "Digest automatically" in the popup to only save sources. If you change `KB_PORT`, edit `host_permissions` in `extension/manifest.json` and `BASE` in `extension/background.js`.

## Use it from other agents (MCP)

A read-only [Model Context Protocol](https://modelcontextprotocol.io) server lets Claude Code, Claude Desktop or any MCP client look things up in your vault with citations. From this folder:

```
claude mcp add knowledge-vault -- .venv/bin/python -m tools.kb.mcp_server
```

Tools: `search_vault`, `get_page` (with every citation's source, locator and quote), `find_passages` (hybrid retrieval; raw-source text is labelled unreviewed), `list_open_questions`, `vault_status`. There is deliberately no tool that writes ([ADR 6](docs/adr/0006-read-only-mcp-server.md)).

## Evaluation and metrics

```
.venv/bin/python -m tools.kb.redteam                         # 26 injection attacks, structural layers (free, in CI)
.venv/bin/python -m tools.kb.redteam --live-ask 8 --live-digest 3 --write docs/redteam-results.md
.venv/bin/python -m tools.kb.digest_eval --judge 12 --write docs/digest-eval.md
.venv/bin/python -m tools.kb.evals --write docs/eval-results.md
./kb metrics                                                 # cost, latency, approval rate from real use
```

The commands with `--live-*` or `--judge` call Claude and cost money: the runs recorded here cost $0.79 and $0.14.

## Subjects, not just AI

Use the subject switcher at the top (or "New subject" in Ctrl+K) to add history, law, biology, anything. Each subject gets its own colour, icon, progress ring, learning map and flashcards. Subjects live in `vault/domains.yml`.

## How it is organised

```
raw/         immutable sources            proposals/   AI drafts waiting for your review
vault/       approved knowledge (also opens in Obsidian)
playgrounds/ interactive simulations      data/        your progress, notes, maps, tasks (private, not committed)
app/         the web app                  tools/kb/    the engine + CLI         docs/knowledge-schema.md  the contract
demo/        sample vault for the demo    evals/       evaluation cases         docs/adr/                 decision records
```

## Safety

- Local only: bound to 127.0.0.1, checks the Host header, every change needs a per-run token (no cross-site requests).
- The digest agent is Claude Code with an allow-list: it can read the repo and write **only inside `proposals/`**. It cannot edit `vault/` or `raw/`, cannot approve, and has no web access. Text in your sources is treated as data, never as instructions.
- Playgrounds are model-written code, so they run in a sandboxed iframe with no network access.
- Concept maps, playgrounds and build tasks are **teaching aids, not evidence**; they never enter the vault. Only the Review page can add knowledge.

## Command line (optional)

`./kb status | validate | search | next | tutor | record | quiz | metrics | approve <batch> --amend`

Setup: `uv venv && uv pip install -r requirements.txt` (pandoc for docx/html). Tests: `.venv/bin/python -m unittest discover -s tests -t .`

## What is (not) in Git

Tracked: code, tests, docs, the approved `vault/`, the sample vault in `demo/`, evaluation cases, playgrounds and the extension. **Ignored (stays on your machine):** `raw/` contents (third-party articles, transcripts, PDFs, personal chats), `data/` (clip key, learning history, tutor chats, maps), `build/`, `.env*`, `*.key`. Because `raw/` is private, run `./kb validate` locally; CI runs the tests, the structural red team and the checks on the sample vault.
