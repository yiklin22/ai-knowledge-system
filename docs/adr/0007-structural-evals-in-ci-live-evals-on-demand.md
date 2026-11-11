# 7. Deterministic evaluations run in CI; evaluations that call a model run on demand

**Status:** accepted (2026-11-11)

## Context
Some quality questions have exact answers (is this quote in the file, does the tool policy allow this command). Others need a model (does the claim follow from the quote, does the model obey an injected instruction) and cost money, take minutes and vary between runs.

## Decision
Two tiers:
- **In CI, on every push:** unit tests, the structural red-team layers (tool policy, validation gate, prompt placement), the digest-quality checks on the sample vault, and the retrieval-evaluation code.
- **On demand, results committed as Markdown:** live red-team runs, the claim-support judge, and retrieval metrics on the private corpus (`docs/redteam-results.md`, `docs/digest-eval.md`, `docs/eval-results.md`). Each report states its sample size and what it does not show.

This replaces the earlier position that no model judge would be built. The judge stays optional and is never a gate.

## Consequences
- CI is free, fast and cannot flake on model behaviour.
- The live numbers are only as fresh as the last manual run, and CI cannot check them because `raw/` is private.

## Revisit when
A public corpus exists that CI can use, or model calls become cheap enough to run a small live sample on a schedule.
