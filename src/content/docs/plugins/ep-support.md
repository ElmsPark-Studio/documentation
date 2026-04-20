---
title: "EP Support"
description: AI-powered support chatbot for PageMotor administrators. Full knowledge base of every EP Suite plugin, answers how-to questions in context.
sidebar:
  order: 54
---

EP Support is an AI chatbot embedded in the PageMotor admin for you, the site owner. Ask it how to do something ("How do I set up Stripe in EP Booking?") and it answers in context, with knowledge of every EP Suite plugin. Distinct from [EP Assistant](/plugins/ep-assistant/) which is the customer-facing AI — this one is just for you.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Admin-only** chat panel.
- **Full EP Suite knowledge base** built in — every plugin, every setting, every common pitfall.
- **Aware of your site's plugins** — it can see what you have installed and tailor answers.
- **Code samples** for customisations.
- **Debugging help** — paste an error message, get a likely cause.

Think of it as: "the documentation you're reading now, but talk-to-able."

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class**
- **An LLM provider API key** (Anthropic, OpenAI, or supported alternatives)

## Installation

1. Download `ep-support.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Support**.
4. Add your LLM API key.

## Using it

The EP Support chat appears in the admin nav. Click to open. Type your question.

Good questions:

- "How do I set up double opt-in on EP Newsletter?"
- "What's the difference between EP Ecommerce and EP Ecommerce Products?"
- "My booking form isn't sending confirmation emails, what should I check?"
- "Show me how to use the LLM prompt extension hook in EP Cards."

The AI has the knowledge base of every EP plugin and can tailor its answer. It can see which plugins you have active; it won't recommend setup in a plugin you don't own.

## Settings

- **LLM provider** and **API key**.
- **Model** — Sonnet is the default balance.
- **Rate limit** — queries per admin per hour.

## Privacy

The plugin sends your questions and relevant context about your plugin setup to the LLM provider. It does NOT send:

- Customer data, order details, or any PII.
- Your database contents.
- Content of pages you're editing.

Just: your question, what plugins you have installed, and relevant excerpts from the EP Suite knowledge base.

## How it differs from EP Assistant

| Feature | EP Support | EP Assistant |
|---|---|---|
| Audience | You (the admin / site owner) | Your customer |
| Purpose | Help you use your plugins | Help customer manage their site |
| Tools | Read-only, answers questions | Read + write tools to take actions |
| Context | Your plugin inventory | Your customer's site setup |
| Typical question | "How do I configure X?" | "Write a blog post about Y" |

## Troubleshooting

### "Chat panel doesn't appear"

Plugin needs to be active and API key set. Check both.

### "Responses are slow"

Depends on LLM provider. Switching from Opus to Sonnet speeds things up noticeably.

### "Answer is outdated compared to a recent plugin update"

The knowledge base updates with plugin releases but there's a lag. Use the most recent plugin documentation as the source of truth; EP Support is a conversation aid.

### "Answer is confidently wrong"

LLMs hallucinate. Never act on an answer from EP Support for anything destructive without verifying in the real docs. Especially for config changes.

### "I want the AI to know my specific custom setup"

Add context in the **Extra system prompt** setting: "This site sells made-to-measure curtains. Prices are in GBP. Orders are handled through EP Booking for consultations, not EP Ecommerce."

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
