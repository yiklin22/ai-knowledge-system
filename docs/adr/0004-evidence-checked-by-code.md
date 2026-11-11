# 4. Evidence rules are enforced by a validator, not by the prompt

**Status:** accepted (2026-11-08), amended 2026-11-11

## Context
"Never fabricate quotes" in a prompt is a request. The system needs a guarantee.

## Decision
`tools/kb/validate.py` re-checks every quote verbatim against the raw file (whitespace and case normalised), requires a locator with every quote, resolves every citation to a source page, and refuses domains that are not in `vault/domains.yml`. The approval gate will not approve a batch with errors.

## Amendment (2026-11-11)
The red-team suite found that a source page could name any file as its raw text, including a file inside `proposals/` that the agent had just written. An invented quote could then pass as verbatim. Validation now accepts a `raw` path only if it resolves to an existing file inside `raw/` (attack K6, `tests/test_quality.py: RawConfinementTests`).

## Consequences
- A quote in the vault is a quote that exists in a source. In the approved vault 160 of 160 quotes verify (`docs/digest-eval.md`).
- Exact matching rejects a quote with one wrong character, so the agent sometimes has to fix and re-validate.
- It checks that the quote exists, not that it supports the claim. That is sampled by an optional model judge and decided by the human reviewer.

## Revisit when
Sources arrive in forms where exact matching is too brittle, such as OCR text.
