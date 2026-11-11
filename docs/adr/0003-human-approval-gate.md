# 3. AI output reaches the vault only through a human approval gate enforced by permissions

**Status:** accepted (2026-11-08)

## Context
The digest agent reads untrusted text from the internet and writes knowledge. It will sometimes be wrong, and a hostile page will sometimes try to steer it.

## Decision
The agent writes only inside `proposals/<batch>/`. A person approves a batch from the Review page or `./kb approve`; amendments to existing pages need a second confirmation after seeing the diff. The agent's tool allow-list has no way to write to `vault/` or `raw/`, run approve, or reach the web (`tools/kb/agent.py`).

## Alternatives considered
- **Tell the agent not to write to the vault.** A prompt instruction can be overridden by injected text; a missing permission cannot.
- **Auto-approve batches that pass validation.** Validation catches fabricated quotes and broken links. It cannot catch a false statement written in plausible prose.

## Consequences
- Review takes human time, and a backlog of unreviewed batches builds up if intake outruns it.
- A model mistake or a poisoned page cannot enter silently. In the red-team suite all 18 attacks that need a forbidden action or a forged page are stopped by code (`docs/redteam-results.md`).

## Revisit when
The approval rate recorded by `./kb metrics` stays near 100% over many batches for some class of low-risk page; that class could then be approved with a lighter check.
