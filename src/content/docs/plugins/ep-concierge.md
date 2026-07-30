---
title: "EP Concierge"
description: "A public AI chat concierge for a website's visitors. A floating chat bubble powered by OpenAI, DeepSeek, or Anthropic (Claude) that knows the business, answers questions, and captures enquiries."
---

EP Concierge puts a floating AI chat bubble on the public side of a PageMotor site. It knows the business (services, prices, and FAQs from its settings, plus live booking data), answers visitor questions, points people to the booking page, and captures enquiries which are emailed to the owner. It is the only bot in the EP AI line-up that your site's visitors actually talk to.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

A visitor clicks the chat bubble, asks a question, and gets an answer grounded in what you have told the assistant about your business. Behind the scenes:

1. The visitor's message (plus recent conversation history) goes to your configured LLM provider with a system prompt built from your **persona**, your **knowledge** text, and live booking data.
2. If the visitor wants to be contacted or to make a booking enquiry, the assistant collects a name, a way to reach them, and their message, then calls its one tool: **capture enquiry**. The enquiry is emailed to the owner.
3. The reply comes back to the chat bubble. Conversations can be logged for the owner to review, with automatic retention-based deletion.

**Read-only by design.** The assistant has no access to the site or its data beyond what you put in its knowledge. It cannot edit pages, run queries, or touch files. The one exception is live booking data: if [EP Booking](/plugins/ep-booking/) or EP Boarding is installed, current prices, services, and the weekly availability schedule are read into the system prompt automatically, so the assistant quotes real prices and real opening days rather than guessing.

Guardrails are built into the prompt: the assistant is instructed to answer only about this business, never to invent prices, dates, availability, or policies, and to state availability exactly as the live schedule gives it.

## Supported providers

| Provider | Models |
|---|---|
| **OpenAI** | GPT-4o mini (fast, economical), GPT-4o, GPT-4.1 mini |
| **DeepSeek** | DeepSeek Chat |
| **Anthropic (Claude)** | Claude Haiku 4.5 (fast, economical), Claude Sonnet 4.6 |

You bring your own API key, billed per message to your own provider account. The model list in settings narrows to the chosen provider, and the backend validates the pairing too, so a provider/model mismatch can never break the chat. Cheaper, faster models (mini, Haiku) are ideal for a website chat.

## Requirements

- **PageMotor 0.9 or later**
- **An API key** from OpenAI, DeepSeek, or Anthropic
- **[EP Email](/plugins/ep-email/)** (recommended). Enquiries are sent through EP Email when it is active, so they are deliverable and logged; without it the plugin falls back to PHP `mail()`.
- **[EP Booking](/plugins/ep-booking/) / EP Boarding** (optional). When present, live prices and the weekly availability schedule are fed to the assistant automatically.

## Installation

EP Concierge is currently **supplied and updated by ElmsPark directly** — it is not on the ElmsPark update channel yet, so it does not appear in your site's Updates screen. Contact ElmsPark for the zip (see [EP Suite plugins](https://elmspark.com/suite/)); updates arrive the same way.

1. Upload `ep-concierge.zip` via **Plugins → Manage Plugins**.
2. Activate.
3. Open **Plugin Settings → EP Concierge**, set the provider and API key, tick **Enable chat assistant**, and fill in the knowledge box.

The chat bubble only appears once the plugin is enabled **and** an API key is saved.

## Settings

- **Enable chat assistant.** Master switch. Shows or hides the bubble for visitors.
- **AI provider.** OpenAI, DeepSeek, or Anthropic (Claude). The Model list updates to match.
- **API key.** Your key for the chosen provider (OpenAI `sk-...`, DeepSeek, or Anthropic `sk-ant-...`).
- **Model.** Which model answers the chat. Only models for the selected provider are shown.
- **Assistant name.** The name shown in the chat header.
- **Opening greeting.** The first message a visitor sees when they open the chat.
- **Input placeholder.** The hint text in the message box.
- **Accent colour.** Optional hex colour so the bubble matches your brand.
- **Send enquiries to.** Where captured enquiries are emailed. Defaults to your booking admin email.
- **Persona / role.** Who the assistant *is* — its tone and manner. Five presets (friendly, warm and reassuring, professional, knowledgeable specialist, upbeat and playful) plus **Custom**, which uses the box below.
- **Custom persona.** Your own persona text, used only when Persona is set to Custom.
- **Knowledge.** Everything the assistant should know: services, FAQs, policies, prices. This is what it *knows*, as opposed to who it *is*. Live booking prices are added automatically.
- **Privacy note.** An optional short line shown beneath the chat input (for example "Chats may be saved so we can follow up"). Recommended whenever logging is on.
- **Keep conversation logs for (days).** Retention is the single logging control: `0` turns logging off entirely; any other number logs conversations and auto-deletes them after that many days. Default 90.

Below the settings, a **Recent conversations** panel shows the last 25 logged chats — expandable transcripts, each marked when it produced an enquiry, each with a **Delete this conversation** button.

## Privacy and data protection

The plugin is built for data minimisation:

- **No IP addresses are stored** with conversation logs.
- **Retention is automatic.** Logged chats are purged after the configured number of days; setting retention to 0 disables logging entirely.
- **Right to erasure.** Any individual conversation can be deleted from the settings page, which removes it from the database immediately.
- **Privacy note.** The optional line under the chat input tells visitors their conversation may be stored. Mention chat logging in your privacy policy when logging is on.

## Abuse protection

- **Same-origin only.** The chat endpoint rejects requests whose Origin or Referer does not match the site.
- **CSRF protected.** A frontend token is required on every chat request.
- **Rate limited.** 25 messages per 10 minutes per visitor IP, protecting your API key (and your bill) from spam. Rate-limited visitors are asked to wait rather than shown an error.

## Database tables

- `{prefix}ep_concierge_chats` — logged conversations: session id, timestamps, message count, enquiry flag, transcript JSON. Created on first use; only exists when logging is on.

## Troubleshooting

### “The chat bubble doesn't appear”

Check both conditions: **Enable chat assistant** is ticked *and* an API key is saved. The bubble is hidden unless both are true.

### “The assistant says it is not available right now”

Same two conditions checked server-side. If both are set, the API key may be rejected by the provider — check it matches the selected provider (Anthropic keys start `sk-ant-`, OpenAI keys start `sk-`).

### “Visitors get 'Please reload the page and try again'”

The CSRF token has expired or the page was cached without one. A reload fixes it. If it persists behind an aggressive page cache, exclude the page from caching cookies.

### “Enquiries are not arriving”

Check **Send enquiries to** holds a valid address (or that your booking admin email is set). If EP Email is installed, check its delivery log; if not, delivery depends on your host's PHP `mail()`, which is unreliable — install EP Email.

### “The assistant quotes wrong opening days or prices”

Live schedule and prices come from EP Booking / EP Boarding when installed. If those plugins are not present, the assistant only knows what is in the **Knowledge** box — keep it current.

### “No conversations are being logged”

Retention is set to 0, which is the off switch. Set a number of days to start logging.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
