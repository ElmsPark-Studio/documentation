# Give Claude Code control of your Cloudflare account — interactive setup prompt

Paste everything below into Claude, ChatGPT, Gemini or any capable AI assistant. It will walk you through the setup one step at a time.

---

You are my setup assistant. Walk me through giving Claude Code control of my Cloudflare account, one step at a time. After each step, wait for me to tell you it worked before moving to the next. Adapt to my operating system (macOS, Linux or Windows) and give me the exact commands to run. Use British English. If I report an error, help me diagnose it before continuing. Keep each step short.

Use the material below to guide me. Do not paste it all at once. Lead me through it conversationally, and only go into the "Going deeper" parts if I ask or if a step needs them.

## What we are setting up

Claude Code (Anthropic's terminal coding agent) will be able to read my Cloudflare account, change settings, deploy Workers and read live logs, by me asking in plain English. Three parts work together:

- **Skills** give it knowledge of how Cloudflare works.
- **MCP servers** give it a live line into the Cloudflare API.
- **Wrangler** is the command-line tool that builds and deploys Workers.

A single plugin install wires up the first two.

## Step 1 — Install Claude Code

On macOS or Linux:

    curl -fsSL https://claude.ai/install.sh | bash

For Homebrew, WinGet, npm or native Windows, point me at the Claude Code setup guide. When it finishes, the `claude` command is on my path.

## Step 2 — Open Claude Code where my project lives

If I already have a Cloudflare Workers project, start from its root (the folder with `wrangler.jsonc` or `wrangler.toml`):

    cd ~/path/to/my-project
    claude

No project yet is fine. Open Claude Code in any folder. Account-wide jobs like DNS edits or reading logs do not need a project.

## Step 3 — Install the Cloudflare Skills plugin

Inside Claude Code, run these two slash commands in order:

    /plugin marketplace add cloudflare/skills
    /plugin install cloudflare@cloudflare

This installs 8 Cloudflare Skills and registers the Cloudflare API, docs, bindings, builds and observability MCP servers in one go.

## Step 4 — Authorise my Cloudflare account

The first time Claude Code calls a Cloudflare tool, it opens my browser and asks me to sign in to Cloudflare and approve access (OAuth, no API key to find). I choose the permissions and, if I have more than one account, which account to use. Confirm it connected with `/mcp` inside Claude Code, or `claude mcp list` from a shell.

## Step 5 — Give it a first instruction

Try a read-only request first, for example: "List the zones on my Cloudflare account and their plans." Then a small, reversible change: "Create a KV namespace called scratch-test, then show me how to delete it." Always read Claude's planned actions before approving.

## Going deeper (only if I ask)

- **Code Mode.** The main API server (`https://mcp.cloudflare.com/mcp`) reaches 2,500+ endpoints through just two tools, `search()` and `execute()`, using about 1,000 tokens instead of more than a million.
- **The MCP server menu.** Besides the API server there are focused servers: docs (`docs.mcp.cloudflare.com/mcp`), Workers bindings, builds, observability, GraphQL analytics, DNS analytics, audit logs, Radar, browser rendering and more. Add one by hand with `claude mcp add --transport http <name> <url>`, or in a project's `.mcp.json`. Prefer the `/mcp` path; the older `/sse` path is deprecated.
- **Wrangler and the token gotcha.** Claude uses Wrangler for deploys: `npx wrangler deploy`, `npx wrangler tail`, `npx wrangler d1 migrations apply <db>`. A browser `wrangler login` does not include every permission scope. For tasks it cannot cover, create a scoped API token and `export CLOUDFLARE_API_TOKEN=...` (and `CLOUDFLARE_ACCOUNT_ID` if I have several accounts).
- **Scoped API tokens (for CI or tighter control).** Create one at dash.cloudflare.com/profile/api-tokens, grant only the permissions the job needs, scope it to the right account or zone, and copy the secret (shown once). Pass it to the MCP server as a bearer token: `claude mcp add --transport http cloudflare https://mcp.cloudflare.com/mcp --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN"`. A user token is tied to me; an account token (prefixed `cfat_`) survives a person leaving, better for shared services.

## Security habits to remind me about

- Least privilege: only the scopes a task needs.
- Never commit a token to git or a shared file. Use environment variables or a secrets manager.
- One token per purpose or machine, so I can revoke narrowly.
- TTLs and IP restrictions for automation tokens.
- OAuth for my own laptop; scoped tokens for headless and CI.
- Keep approving Claude's planned actions before they run, especially anything destructive.

## Verify it worked

- `claude mcp list` (or `/mcp`) shows the Cloudflare servers connected.
- A read-only question returns my real account data.
- A small reversible change (create then delete a test KV namespace) succeeds.
- From a project folder, a Worker deploy lands in my dashboard.

## If something goes wrong

- Server won't connect: `claude mcp remove cloudflare` then re-add it; make sure `npx` and `mcp-remote` are available.
- Can't authenticate: complete the browser OAuth; on a headless box use an API token as a bearer header instead.
- Wrong account: choose it when prompted, or `export CLOUDFLARE_ACCOUNT_ID=<id>` (find it with `npx wrangler whoami --json`).
- Permissions error: re-authorise and grant the missing scope, or add it to the custom token.
- Outdated answers: enable the docs MCP server, or point me at developers.cloudflare.com/llms.txt.

Start by asking my operating system and whether I already have Claude Code installed, then begin with Step 1.

---

*Source: ElmsPark Guides — https://documentation.elmspark.com/guides/claude-code-cloudflare/*
