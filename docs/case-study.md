# Case study: a trustworthy AI knowledge system

*One page for hiring managers. Every number below is reproducible from this repo; nothing here is a claimed customer result.*

## The customer problem

Teams read a lot (vendor docs, chats, PDFs, videos, tickets) and then cannot answer "where did we learn that, and can we trust it?" Chat-with-your-documents tools answer fluently but invent citations, and nobody can audit what the model "knows". In a business this is the blocker to deploying AI on real work: **trust, not capability**.

## What I built

A system where AI *proposes* and a human *approves*, and every claim carries a verbatim, checkable quote.

| Layer | Decision | Why a customer cares |
|---|---|---|
| Ingest | Web, PDF, video transcripts, chats and clipper extension all become immutable raw markdown | Messy inputs are the real world |
| Digest agent | Claude Code with an allow-list: writes only to `proposals/`, no web, cannot approve | Least privilege: a poisoned document cannot do damage |
| Validation | Quotes re-checked verbatim against the source; forged citations flagged | Auditability; "show me the evidence" always works |
| Review | Human reads diffs and approves; one commit per batch | Accountability and rollback |
| Ask | Hybrid retrieval (BM25 + embeddings, rank fusion), cited answers, says what sources do not cover | Honest "I don't know" |
| Ops | Docker, CI, metrics log, one-command sandboxed demo (`./demo.sh`) | Someone else can run it in minutes |

## Evidence (measured, with limits stated)

- **Retrieval, 20 hand-written cases over ~7,700 passages:** hit@1 keyword 50% → semantic 65% → hybrid **75%**; hit@5 95% across all modes. Small sample (one question = 5 points), author-written questions: see `docs/eval-results.md`.
- **Digest quality:** deterministic checks of quote validity, locator coverage and duplicate titles: `docs/digest-eval.md`.
- **Security:** threat table with a test per control, including a prompt-injection canary: `docs/security.md`.
- **Tests:** 96 passing, run in CI on two Python versions.

## What went wrong / what I would do differently (the part interviewers probe)

- Retrieval eval was written by the same person who built the retriever, so it is optimistic. Next: questions from real users.
- Prompt-injection defences reduce risk but do not remove it; the strong controls are structural, not wording.
- Single-user, local only. A hosted version needs auth and per-tenant isolation first.

## How this maps to the roles

- **AI engineer:** evals before and after, hybrid retrieval, groundedness and citation checks, agent permissions, cost/latency metrics.
- **Forward-deployed engineer:** messy multi-format ingestion, a threat model a customer's security team can read, a demo that runs in one command, and honest limits stated up front.

## Where it goes next: ask a real customer

The next step is not another feature. It is a design-partner pilot: see `docs/customer-discovery.md`.
