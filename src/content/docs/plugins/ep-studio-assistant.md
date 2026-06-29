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

1. Download `ep-studio-assistant.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **EP Suite nav → Assistant** and start asking. If a Claude key is already in **AI Setup**, the assistant picks it up automatically.

## Settings

Accessed under the **EP Suite nav → Assistant**.

- **Anthropic API key (override).** Leave blank to use the key from PageMotor's AI Setup. Set one here only if you want this assistant to use a different key.
- **Model.** Claude Sonnet (recommended), Opus, or Haiku.
- **Studio context (optional).** Anything the assistant should always know about your studio, added to every conversation.

## Use it on your own Claude subscription

The same studio data also works from your own Claude Pro or Max plan, with no API key, by connecting your site to Claude as a custom connector. See the guide: [Talk to your studio with Claude](https://documentation.elmspark.com/guides/ask-your-studio-with-claude/).

## Changelog

### 1.0.0

Initial release. The in-Admin Ask box: a server-side Anthropic tool-use loop over the read-only studio tools, with the key read from PageMotor's AI Setup, a fixed read-only allowlist (mutations excluded), and admin and CSRF protection on the same wire as the rest of the EP Suite admin.
