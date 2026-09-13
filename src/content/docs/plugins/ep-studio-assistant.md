---
title: "EP Studio Assistant"
description: "An Ask box inside the PageMotor Admin. The studio owner asks about the business in plain English and Claude answers from live data, over read-only studio tools."
---

EP Studio Assistant puts a chat box inside the PageMotor Admin. The studio owner types a question in plain English ("how is revenue this month", "who is about to churn", "who has not signed a waiver before tomorrow's class") and Claude answers from the studio's live data. It is the conversational front door to the EP Studio Dashboard.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

The assistant runs an Anthropic tool-use loop on the server. When you ask a question, Claude calls the read-only studio tools the EP suite already exposes (the dashboard overview, members at risk, the upcoming schedule, revenue, class passes, waivers, payroll, the instructor roster, and per-member lookups), then answers in plain language.

It is deliberately **read-only**. The model is handed a fixed allowlist of query tools and cannot call anything else, so it shows you what is happening and points you to the right dashboard screen to action it, but it cannot make a booking, grant a pass, run payroll, or change a setting.

Your data never leaves the server except as the model's answer, and your Anthropic key is stored server-side and never sent to the browser.

## Requirements

- **PageMotor 0.8.3b or later**
- An **Anthropic API key** (from [console.anthropic.com](https://console.anthropic.com)), or a Claude key already saved in PageMotor's **AI Setup** page
- The **EP Studio Dashboard** and its sibling plugins for the data the assistant reads

## Installation

1. `ep-studio-assistant.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **EP Suite nav → Assistant** and start asking. If a Claude key is already in **AI Setup**, the assistant picks it up automatically.

## Settings

Accessed under the **EP Suite nav → Assistant**.

- **Anthropic API key (override).** Leave blank to use the key from PageMotor's AI Setup. Set one here only if you want this assistant to use a different key.
- **Model.** Claude Sonnet (recommended), Opus, or Haiku.
- **Studio context (optional).** Anything the assistant should always know about your studio, added to every conversation.

## Use it on your own Claude account

The same studio data also works from your own Claude account, with no API key, by connecting your site to Claude as a custom connector. Any plan can do it, free included, though free accounts may hold only one custom connector. See the guide: [Ask your studio with Claude](https://documentation.elmspark.com/guides/ask-your-studio-with-claude/).

## Changelog

### 1.0.6

- **Your API key is now stored encrypted.** Until this release it sat in plain text in the plugin's settings, where anyone holding an API or MCP connection to your site with permission to configure plugins could read it straight back out. Your site's visitors were never able to see it.
- Existing sites convert themselves the next time the plugin loads, once. There is nothing to re-enter and no key to replace.
- Reading your settings over the API now returns a placeholder rather than the value, and writing that placeholder back leaves the stored secret untouched. Clearing it by submitting an empty value still works as before.
- On hosting without encryption support the previous behaviour is kept and the reason is written to the log, because quietly discarding a working key would be worse than the exposure this closes.

### 1.0.5

- **Fixes "Your session has expired. Please reload to ensure your security." on PageMotor 0.11.** The message appeared on assistant actions taken by a signed-in user even though you were signed in perfectly normally, and whatever you were doing failed to save.
- Nothing was wrong with your session. PageMotor 0.11 started handling part of the security check that this plugin was already handling itself, and the two together made every save look invalid. The plugin now checks whether PageMotor has already done it.
- Visitors who were not signed in were never affected, on any version.
- There is nothing to reconfigure, and nothing else changed.

### 1.0.4

- **The plugin now fails safely if its own bundled shared code is missing or damaged.** Previously that took the whole site down with it. Now the plugin simply does not load, records why, and the rest of the site carries on. The build process also checks the bundle is intact before a release can ship.
- No change when everything is healthy, which is the normal case.

### 1.0.3

- Hardening only. A version mismatch in the shared suite code across your active plugins can no longer cause an error in this plugin's admin screens. No change to what it does.

### 1.0.2

- **Fixes administrators being locked out of this plugin's actions on PageMotor 0.10.** The permission check used an older method that PageMotor 0.10 removed, and it failed closed. It now works on both 0.10 and 0.9.

### 1.0.1

- **Fixes the version number missing from the plugin's admin header.** It now shows correctly.

### 1.0.0

Initial release. The in-Admin Ask box: a server-side Anthropic tool-use loop over the read-only studio tools, with the key read from PageMotor's AI Setup, a fixed read-only allowlist (mutations excluded), and admin and CSRF protection on the same wire as the rest of the EP Suite admin.
