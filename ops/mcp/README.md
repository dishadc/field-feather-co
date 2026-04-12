# MCP Integration for Field & Feather Co.

This workspace now includes MCP wiring to accelerate autonomous operations.

## Configured now (working)
1. `fs` MCP server (filesystem)
2. `github` MCP server (GitHub API tools; requires `GITHUB_PERSONAL_ACCESS_TOKEN`)

### Active files
- `config/mcporter.json` (mcporter runtime config)
- `config/mcporter.commerce-template.json` (template for Etsy/Shopify/Gumroad/Pinterest HTTP MCP servers)
- `~/.hermes/config.yaml` updated with `mcp_servers` for native Hermes MCP startup

## Commerce MCP setup (required for direct platform automation)
Populate and use `config/mcporter.commerce-template.json` with real endpoints/tokens:
- ETSY_MCP endpoint + token
- SHOPIFY_MCP endpoint + token
- GUMROAD_MCP endpoint + token
- PINTEREST_MCP endpoint + token

Then run:

`npx -y mcporter list --config config/mcporter.commerce-template.json --output json`

If servers are healthy, we can call tools directly for listing creation, product updates, and marketing post scheduling.

## Native Hermes MCP
Native config is already written to `~/.hermes/config.yaml` under `mcp_servers`.
Restart Hermes process for tool auto-discovery.

## Why this matters
Once commerce MCP endpoints are live, we can automate:
- product publish/update
- price and inventory sync
- order and payout monitoring
- Pinterest posting and analytics pulls
without manual browser actions.
