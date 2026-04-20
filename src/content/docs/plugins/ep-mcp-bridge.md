---
title: "EP MCP Bridge"
description: "JSON-RPC API for remote PageMotor content and plugin management. Lets Claude Desktop, Claude Code, or any MCP-aware client drive your site from outside."
sidebar:
  order: 37
---

EP MCP Bridge exposes your PageMotor site through the Model Context Protocol. With it installed, a remote MCP client (Claude Desktop, Claude Code, or any MCP-aware tool) can read your content, edit it, invoke plugin actions, and run admin tasks without opening a browser.

Published by [ElmsPark Studio](https://elmspark.com).

## What MCP is

The [Model Context Protocol](https://modelcontextprotocol.io) is a standard for giving AI assistants structured access to external systems. An MCP server exposes tools (actions the AI can invoke) and resources (data the AI can read). EP MCP Bridge turns your PageMotor site into an MCP server.

Once configured, you can ask Claude from anywhere: "Look at my site, draft a blog post about X", and it can query your site's content, write the draft, and save it back as a page — without you copying and pasting.

## What it exposes

### Tools (invocable actions)

- `get_page(slug)` — fetch a page's content and metadata.
- `list_pages(filter)` — list pages with filtering.
- `create_page(slug, title, content, ...)` — create a new page.
- `update_page(slug, ...)` — update an existing page.
- `delete_page(slug)` — delete a page.
- `get_plugin_settings(plugin)` — read another plugin's settings.
- `set_plugin_settings(plugin, settings)` — update another plugin's settings.
- `call_plugin_action(plugin, action, params)` — invoke an action on any plugin that exposes MCP-accessible actions.
- `get_site_info()` — PageMotor version, active theme, active plugins.

### Resources (readable data)

- Your site's content database (pages, posts, comments).
- Plugin settings where permitted.
- Recent admin activity.

## Security

Remote access is a real attack surface. EP MCP Bridge gates it carefully:

- **API key authentication.** Every JSON-RPC request carries a long-random API key.
- **Per-key scopes.** Each key has a list of allowed tools. A read-only key cannot write. A "blog-only" key cannot touch ecommerce settings.
- **IP allowlist.** Optionally restrict keys to specific source IPs.
- **Rate limiting** per key.
- **Audit log.** Every request is logged with key, tool, params, result.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**
- **PHP 8.0+** (the JSON-RPC library uses modern PHP features)

## Status

**Version 0.17.2** — functional and in use, but still iterating. Tool list may expand between versions. Check the plugin's own CHANGELOG before integrating.

## Installation

1. Download `ep-mcp-bridge.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP MCP Bridge**.
4. Click **Create API key**. Give it a name, pick scopes, set IP allowlist if needed.
5. Copy the key — it's shown once. Store in a password manager or in your MCP client's config.

## Connecting Claude Desktop

1. In Claude Desktop, open settings.
2. Under MCP servers, add a new server.
3. Server URL: `https://yoursite.com/?ep_mcp_bridge=1`
4. Authentication: Bearer token. Paste your API key.
5. Save. Claude Desktop lists the available tools from your site.

Other MCP clients (Claude Code, third-party tools) follow the same pattern.

## Connecting Claude Code

In your project's `.claude/settings.json`:

```json
{
  "mcp": {
    "servers": {
      "my-site": {
        "url": "https://yoursite.com/?ep_mcp_bridge=1",
        "headers": {
          "Authorization": "Bearer YOUR-API-KEY"
        }
      }
    }
  }
}
```

Restart Claude Code. The tools are now available.

## Scopes

When creating an API key, pick from:

- `read_content` — fetch pages.
- `write_content` — create, update, delete pages.
- `read_settings` — read plugin settings.
- `write_settings` — modify plugin settings.
- `call_actions` — invoke arbitrary plugin actions.
- `admin` — everything.

Principle of least privilege: start with `read_content` only, add scopes as you find you need them.

## Audit log

Every request is logged with timestamp, API key name (not the key itself), tool invoked, parameters, and result. View in the admin settings page. Useful for:

- Debugging AI assistant behaviour.
- Catching unauthorised access (rotate keys immediately if you see anything suspicious).
- Costing exercises ("how much am I leaning on MCP?").

## Troubleshooting

### "My client can't connect"

Check:
- URL is correct, including the `?ep_mcp_bridge=1` query parameter.
- Authorization header uses `Bearer` format.
- The API key matches a key saved in the plugin (keys can be disabled individually).

### "I get 403 Forbidden"

Either the key is invalid, disabled, or your IP isn't in the allowlist for that key.

### "A tool I expected isn't available"

Check the API key's scopes. A key without `write_content` cannot invoke `create_page`, `update_page`, or `delete_page`.

### "Tool invocation succeeds but the result is wrong"

Check the audit log for the full parameters sent. The AI might be passing arguments you don't expect. Refine the AI's prompt or tighten the scope.

### "I want to rotate a key"

Create a new key with the same scopes. Update your client to use it. Delete the old key.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
