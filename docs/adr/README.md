# Architecture decision records

One page per decision that would be expensive to reverse. Each says what was decided, what it cost, and what would make it worth revisiting.

| # | Decision | Status |
|---|---|---|
| [1](0001-markdown-is-canonical.md) | Markdown files are the source of truth; databases are rebuildable caches | accepted |
| [2](0002-opaque-immutable-ids.md) | Pages are identified by opaque, immutable ids, never by filename | accepted |
| [3](0003-human-approval-gate.md) | AI output reaches the vault only through a human approval gate enforced by permissions | accepted |
| [4](0004-evidence-checked-by-code.md) | Evidence rules are enforced by a validator, not by the prompt | accepted, amended 2026-11-11 |
| [5](0005-learning-state-outside-the-vault.md) | Learning progress lives in SQLite, outside the vault | accepted |
| [6](0006-read-only-mcp-server.md) | The MCP server is read-only and has no dependencies | accepted |
| [7](0007-structural-evals-in-ci-live-evals-on-demand.md) | Deterministic evaluations run in CI; evaluations that call a model run on demand | accepted |
