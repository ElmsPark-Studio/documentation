---
title: "EP Assistant"
description: "Browser-based AI website management for PageMotor. Your customers manage their site in plain English through a chat interface powered by Claude, GPT, or any of nine LLM providers."
sidebar:
  order: 7
---

EP Assistant puts an AI chat interface in the PageMotor admin panel and wires it up to nine server-side tools so the customer can manage their entire site in plain English. Write a new page. Check today's enquiries. Send a follow-up email. Update the brand colours. All through conversation.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

This is not a chatbot answering support questions. The assistant has real server-side tools that execute actions with safety gates:

- **Read and write files** within the site root, with sandboxing.
- **Run SQL queries** against a whitelisted set of tables, with auto-backup before any write.
- **Recompile CSS** when the customer asks to change styling.
- **Import theme data** the same way EP Provisioning does.
- **Check any page** on the site and return its status and content.
- **Send emails** via EP Email, rate limited per conversation.

Every tool invocation is logged to an audit table. Every destructive operation takes a backup first.

## The hosting model

EP Assistant is designed to be sold through hosting companies as part of an end-to-end AI website product:

1. The **hosting company's central server** runs Discovery AI, which talks to the prospective customer about what they want.
2. Discovery AI extracts brand voice, audiences, services, and site inventory from the conversation.
3. The system provisions a **small VPS from the hosting company's catalogue** and installs PageMotor + EP Assistant + the rest of EP Suite.
4. EP Provisioning writes memory files into the new site and configures EP Assistant with an API key.
5. The customer clicks a welcome-email link, lands in their admin panel, and starts chatting to their site.

The customer never leaves the hosting company's ecosystem. The hosting company gets to sell a differentiated product.

## Supported LLM providers

EP Assistant supports **nine providers** through three adapter formats:

| Provider | Format | Why pick this |
|---|---|---|
| **Anthropic (Claude)** | Native | The reference provider. Best tool-use quality. |
| **OpenAI (GPT)** | OpenAI | Mature API, reliable. |
| **Mistral AI** | OpenAI-compat | European, GDPR-friendly. |
| **DeepSeek** | OpenAI-compat | Lowest cost. |
| **Groq** | OpenAI-compat | Fastest token throughput. |
| **xAI (Grok)** | OpenAI-compat | Alternative to GPT. |
| **Together AI** | OpenAI-compat | Access to open-weight models. |
| **Fireworks AI** | OpenAI-compat | Fast open-weight serving. |
| **Google Gemini** | Native | Google's frontier model. |

Every provider is configured with API key, model, and max tokens. Swap providers in a dropdown without changing anything else.

## Requirements

- **PageMotor 0.8.2b or later**
- **VPS hosting** (not shared). The assistant runs long-polling AJAX and benefits from persistent connections.
- **An API key** from one of the nine providers above.
- **EP Email** (required for the `send_email` tool).

## Installation

Typically installed as part of an automated provisioning flow driven by Discovery AI. If you are installing manually:

1. **Download** `ep-assistant.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**.
3. Activate.
4. Open **Plugin Settings → EP Assistant** and set:
   - **Provider.** Anthropic Claude is the recommended default.
   - **API key.** Paste the key for your chosen provider.
   - **Model.** Leave at the default unless you know what you are doing.
   - **Business name.** Used in the assistant's greeting and system prompt.
5. (Optional) Populate the **memory files** under `src/memory/`. If EP Provisioning installed this plugin, these files are already written for you. Otherwise create:
   - `brand-voice.md` — one page on tone and writing style.
   - `audiences.md` — who visits your site.
   - `services.md` — what you sell.
   - `site-inventory.md` — pages, shortcodes, key content.
   - `discovery-context.md` — free-form background.

## The chat interface

Open the EP Assistant panel from the admin menu. Type into the chat box. The assistant responds with plain English.

Behind the scenes, each message triggers an agentic loop:

1. Your message + conversation history + system prompt + available tools go to the LLM.
2. If the LLM wants to call a tool, the plugin executes it server-side and appends the result.
3. Loop continues until the LLM returns a text-only response.
4. That response is rendered in the chat with markdown formatting.

The loop has a maximum iteration count so a runaway tool-use cascade cannot spin forever.

## The nine server-side tools

| Tool | Purpose | Safety |
|---|---|---|
| `run_query` | SQL against the site database. | Whitelist of 10 allowed tables. Auto-backup before any write. |
| `read_file` | Read any file inside the site root. | `realpath()` sandboxing. Blocked list: `config.php`, `.env`, anything outside `ABSPATH`. |
| `write_file` | Write or create a file inside the site root. | Whitelist of writable directories. Auto-backup of existing content. |
| `recompile_css` | Trigger a CSS recompile after theme changes. | Localhost-only HTTP call with a shared token. |
| `import_theme` | Import partial theme data using EP Provisioning's logic. | Key whitelist. |
| `check_page` | HTTP GET any page on your own site. | Restricted to your own domain. |
| `send_email` | Send an email via EP Email. | Rate limited to 10 per conversation. |

Every successful tool call creates an audit row with input, output, and backup data (if applicable).

## Built-in skills

Type a slash command to load a skill prompt:

| Command | Purpose |
|---|---|
| `/update-page` | Edit the content of an existing page. |
| `/add-page` | Create a new page with a given slug and content. |
| `/write-article` | Draft a blog article. |
| `/write-newsletter` | Compose an EP Newsletter campaign. |
| `/check-enquiries` | Review today's EP Email contact submissions. |
| `/check-bookings` | Review today's EP Booking appointments. |
| `/check-site` | Run the autonomous `site-doctor` agent — page reachability, broken links, spam signals. |
| `/send-email` | Compose and send a one-off email. |
| `/update-styles` | Change theme colours, fonts, spacing. |
| `/update-theme` | Broader theme changes. |
| `/help` | Show every available command. |

Slash commands load a specific skill prompt that primes the assistant for that task.

## System prompt layers

The prompt sent to the LLM is built from five layers:

1. **Core rules** (hardcoded): British English, no jargon, backup before modify, plain text over corporate language.
2. **Operations guide** (hardcoded): How to use each tool correctly.
3. **Plugin knowledge** (from EP Support): Full knowledge base for all 18 EP Suite plugins.
4. **Memory files** (per-site): The five markdown files described above.
5. **Skill instructions** (per-turn): Loaded when the user invokes a slash command.

This layered prompt is why the assistant feels tailored to the customer's site rather than generic. The memory files carry the business context; the plugin knowledge carries the system context.

## Database tables

- `{prefix}ep_assistant_conversations` — conversation history with messages JSON, status, timestamps.
- `{prefix}ep_assistant_audit` — every tool call logged with input, output, backup data.

## Troubleshooting

### "Provider API key is rejected"

Check the key matches the provider selected in the dropdown. Anthropic keys start `sk-ant-`, OpenAI keys start `sk-`, Gemini keys are alphanumeric with no prefix. Paste the full key including the prefix.

### "The assistant hangs forever"

LLM provider is slow or down. Check your provider's status page. Try switching to a different provider temporarily.

### "SQL tool refuses to run my query"

The `run_query` tool has a whitelist of 10 allowed tables. Custom plugin tables are not on it by default. If you need to give the assistant access to more tables, edit the whitelist in `class-ep-assistant-tools.php` carefully.

### "Write tool fails with 'outside writable directory'"

The `write_file` tool only writes inside a specific allowlist of directories (themes, custom CSS, user content). Writing to plugin code or PM core is deliberately blocked.

### "Audit log is huge"

Every tool call creates a row. Over a busy month this can be thousands of rows. Truncate `{prefix}ep_assistant_audit` manually if it grows unmanageable.

### "I changed the memory files but the assistant doesn't seem to know"

Memory files are read once per conversation at start. Open a fresh conversation to pick up changes. Existing conversations keep their original system prompt for consistency.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
