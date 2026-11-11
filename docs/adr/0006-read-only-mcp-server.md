# 6. The MCP server is read-only and has no dependencies

**Status:** accepted (2026-11-11)

## Context
Other agents (Claude Code in another project, a desktop assistant) are more useful if they can look things up in the vault with citations. The Model Context Protocol is the standard way to offer that.

## Decision
`tools/kb/mcp_server.py` exposes five tools over the stdio transport: `search_vault`, `get_page`, `find_passages`, `list_open_questions`, `vault_status`. None of them writes. Passages from raw sources are labelled as unreviewed, untrusted text. The JSON-RPC handling is about 170 lines of standard library, with `handle` a pure function from request to response.

## Alternatives considered
- **A `propose_page` tool.** It would let any connected agent write proposals. Proposals are still gated, but each new writer is another thing to red-team, and the digest agent already covers the need.
- **The official MCP SDK.** It would add a dependency tree for a server that needs four methods. The cost is that new protocol features have to be added by hand.

## Consequences
- A client that has been prompt-injected can read the vault but cannot change it.
- Only tools are implemented: no resources, prompts or streaming HTTP.

## Revisit when
A second transport or MCP resources are needed; at that point the SDK earns its place.
