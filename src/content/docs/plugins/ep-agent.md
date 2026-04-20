---
title: "EP Agent"
description: Claude Code CLI embedded in the PageMotor admin panel. Chat with a full AI coding agent that can read files, edit code, run shell commands, and debug your site, all server-side.
sidebar:
  order: 5
---

EP Agent runs the Claude Code CLI on your server and gives you a chat panel in the admin to drive it. This is not a chatbot wrapper. The agent has the same capabilities as Claude Code on your local machine: file read and edit, bash commands, web search, codebase search, all scoped to the server your site lives on.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Drop a prompt into the admin chat panel, hit send, and the agent runs on the server with full tool access. Useful for:

- **Debugging PHP errors** ("why is this page throwing a 500, look at the error log")
- **Explaining your site** ("how does the booking plugin decide whether a slot is free")
- **Editing code** ("add a custom validation rule to the contact form")
- **Running shell tasks** ("what is using the most disk space in user-content")
- **Searching the codebase** ("find every shortcode the active theme uses")
- **Writing guides or READMEs** based on actual server state

## Requirements

- **PageMotor 0.8 or later**
- **VPS or dedicated server.** EP Agent detects shared hosting automatically and refuses to run because shared hosting cannot execute long-running CLI processes.
- **Node.js 18 or later** on the server.
- **Claude Code CLI** installed globally: `npm install -g @anthropic-ai/claude-code`
- **Authentication** via one of:
  - `CLAUDE_CODE_OAUTH_TOKEN` environment variable (Claude Max plan, recommended).
  - `ANTHROPIC_API_KEY` environment variable (pay-as-you-go API billing).

## Installation

1. **Download** `ep-agent.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. **SSH to your server** and install Claude Code globally if you haven't already:

   ```bash
   npm install -g @anthropic-ai/claude-code
   claude --version
   ```

3. **Set the authentication environment variable** in your PHP-FPM pool config (typical path: `/etc/php/8.2/fpm/pool.d/www.conf`):

   For Max plan:
   ```
   env[CLAUDE_CODE_OAUTH_TOKEN] = "sk-ant-oat01-..."
   ```

   Or for API billing:
   ```
   env[ANTHROPIC_API_KEY] = "sk-ant-api03-..."
   ```

4. **Reload PHP-FPM:** `systemctl reload php8.2-fpm`.
5. **Upload the zip** via PageMotor's Plugins → Manage Plugins.
6. **Activate** and open the EP Agent settings page. The prerequisites checklist tells you what is still missing.

## Settings

| Setting | Purpose |
|---|---|
| **Authentication Method** | Choose Max plan or API key. The settings page shows a step-by-step guide for whichever you pick. |
| **Model** | Sonnet (recommended balance), Opus (most capable, slower and pricier), Haiku (fast and cheap, less capable). |
| **Max Budget per Prompt** | USD cap per single prompt. Default $0.50. Set to `0` for no limit. Only relevant on API billing. |
| **Allowed Tools** | Comma-separated whitelist: `Bash, Read, Write, Edit, Glob, Grep` is a common starting set. Leaving it open to all tools gives the agent more power; locking down is safer. |
| **Additional System Prompt** | Text appended to every prompt. Use this to give the agent site-specific context ("This site sells made-to-measure furniture. Prices are in GBP. Stock is managed in EP Ecommerce Products."). |
| **Rate Limit** | Prompts per admin per hour. Default 20. |

## Authentication options explained

### Claude Max Plan (recommended)

Fixed monthly cost (£200/month at time of writing). No surprise bills no matter how much you use it. Best for admins who want to experiment freely without watching the meter.

The OAuth token never expires but CAN be revoked from your Anthropic account settings.

### Anthropic API (pay-as-you-go)

Billed per token on your Anthropic console account. Cheaper if you only use EP Agent occasionally. Use the **Max Budget per Prompt** setting to cap per-invocation spend so a runaway prompt cannot rack up hundreds of pounds.

Typical costs: Sonnet is roughly $3 per million input tokens and $15 per million output. A thoughtful 10,000-token conversation is about £0.10.

## Activity log

Every prompt is logged with admin user ID, cost in USD, duration in seconds, model used, and outcome. Log viewer features:

- **Refresh** to reload.
- **Clear Log** to wipe all entries.
- **Download CSV** for spreadsheet analysis.
- **Download JSON** for pasting into another LLM session for retrospective analysis ("here are my last 50 EP Agent prompts, what was I spending most of my time on?").

Logs auto-purge after **90 days**.

## Security model

- **Admin-only.** No frontend exposure. Non-admins get 403.
- **CSRF tokens** on every AJAX endpoint.
- **Prompt piped via stdin** to `proc_open`, never through the shell. No shell injection risk.
- **Rate limited** per admin user per hour.
- **Budget capped** per prompt on API billing.
- **Allowed-tools whitelist** restricts what the agent can do on the server.
- **No credentials in the database.** Auth is read from environment variables at runtime.

## How the chat flow works

1. Admin types a prompt in the chat panel.
2. PHP validates auth, CSRF token, and rate limit.
3. PHP spawns `claude -p --output-format json --no-session-persistence` via `proc_open()`.
4. Prompt is written to the child process's stdin (the command line never sees the prompt text, so no escaping bugs).
5. CLI flags `--model`, `--max-budget-usd`, `--allowed-tools`, `--append-system-prompt` carry the settings.
6. JSON response comes back from the CLI, gets parsed, logged to the activity log, and returned to the browser.
7. The chat panel renders the response with markdown formatting.

## Troubleshooting

### "Prerequisites checklist shows Claude CLI not found"

SSH to the server and run `which claude`. If empty, `npm install -g @anthropic-ai/claude-code`. If present but the checklist still fails, PHP-FPM may be running with a PATH that doesn't include the Node global bin directory. Either symlink `claude` into `/usr/local/bin/`, or add `env[PATH]` to your PHP-FPM pool config with the Node bin path.

### "Authentication check fails despite setting the env variable"

PHP-FPM needs a reload, not just a restart of the site. Run `systemctl reload php8.2-fpm` (adjust version number) then reload the settings page.

### "The agent times out on long prompts"

Increase `max_execution_time` in PHP to at least 120 seconds. Claude Code can take minutes on complex prompts that use many tools. Also check your PHP-FPM `request_terminate_timeout` is at least as high.

### "Budget exceeded" messages on API billing

Either you set Max Budget too low for what you are asking, or the model you chose is too expensive for this task. Opus on a file-refactor job can burn a dollar a prompt. Drop to Sonnet for cost savings.

### "I want to give the agent access to a specific directory outside the site root"

Use the **Additional System Prompt** to tell it where. The agent already runs as the PHP-FPM user (typically `www-data`), so it can only touch files that user owns. If you want it to read other paths, they need to be readable by `www-data`.

### "I want to stop a runaway prompt mid-flight"

Right now, no in-UI stop button. If the agent is stuck, `ps aux | grep claude` on the server and kill the process. Feature request logged for a stop button in a future version.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
