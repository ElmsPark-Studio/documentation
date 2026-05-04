---
title: "EP Provisioning"
description: "Remote provisioning receiver for PageMotor sites. Accepts setup requests from a Discovery AI central server and auto-configures the fresh site."
sidebar:
  order: 43
---

EP Provisioning turns a freshly-installed PageMotor site into a receiver for automated setup. A central Discovery AI server can push configuration (theme, plugins, initial content, assistant memory, API keys) to a brand-new site and the site configures itself from that payload. Designed for hosting companies rolling out AI-managed websites at scale.

Published by [ElmsPark Studio](https://elmspark.com).

## The provisioning model

1. A prospective customer talks to Discovery AI on the hosting company's central server.
2. Discovery AI extracts brand voice, services, audiences, and other context from the conversation.
3. The hosting company's automation spins up a VPS with fresh PageMotor.
4. EP Provisioning is pre-installed with an API key.
5. Discovery AI POSTs the provisioning payload to the new site.
6. EP Provisioning applies it: sets theme colours, activates plugins, writes assistant memory files, configures EP Assistant with its own API key, creates a default contact form.
7. The customer receives a welcome email with a magic-link login, lands in their admin panel, and starts managing their site through conversation.

## What EP Provisioning does

Receives a signed JSON payload and applies the contents:

- **Site metadata.** Business name, address, phone.
- **Theme customisation.** Colours, fonts, logo.
- **Plugin activation.** Activates listed plugins in the correct order.
- **Content seeds.** Creates default pages (home, about, contact).
- **Default contact form.** Creates a "main" form in EP Email.
- **Assistant memory files.** Writes 6 markdown files to `ep-assistant/src/memory/` (brand voice, audiences, services, site inventory, discovery context). The brand-voice file's writing rules can be customised via an optional `writing_rules` array in the `brand_voice` payload (e.g. `["British English always", "Sentence case headings"]`). Without one, a neutral default applies — no regional spelling is forced on the provisioned site.
- **Plugin API keys.** Configures EP Assistant with its own Anthropic key.
- **Webmaster user.** Creates or updates the admin account with a magic-link login token.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**
- **EP Email, EP Assistant** and other plugins mentioned in the payload must also be installed on the target site for their sections to apply.

## Installation

EP Provisioning is typically installed as part of the fresh-site automation rather than manually. If you're setting up a provisioning target by hand:

1. Download `ep-provisioning.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload and activate.
3. Open **Plugin Settings → EP Provisioning**.
4. Click **Generate API key**.
5. Share the key with the central Discovery AI system so it can POST here.

## The provisioning endpoint

POST to: `https://targetsite.com/?ep_provisioning=1`

Headers:

- `Authorization: Bearer YOUR-API-KEY`
- `Content-Type: application/json`

Body: structured JSON with the sections listed above. Full schema is in the plugin's README (it's quite verbose).

Response: `{ "success": true, "applied": [...] }` listing what was applied, or `{ "error": "...", "details": "..." }` on failure.

## Security

- **API key authentication** on every request.
- **IP allowlist** on the settings page — restrict to your Discovery AI server's IP.
- **Audit log** of every provisioning request, successful or failed.
- **Once activated** a provisioning site can be locked: subsequent requests are rejected unless you re-enable. Prevents a stolen key from being used to reconfigure a live site.

## Typical failure modes

- **Missing plugin.** Payload asks to configure EP Booking, but EP Booking isn't installed. Plugin logs the failure and continues with other sections.
- **Schema mismatch.** Payload has unknown keys. Logged as warnings; known keys still process.
- **Bad API key.** Request rejected with 401.
- **Rate limit.** Too many provisioning attempts from the same key in a short window are throttled.

## Troubleshooting

### "Provisioning request fails with 401 Unauthorized"

API key is wrong or disabled. Regenerate and update on the Discovery AI side.

### "Some plugins got configured, others didn't"

The log shows which sections applied and which didn't. Missing plugins are the usual culprit — EP Provisioning can only configure what's installed.

### "The provisioned site's admin login doesn't work"

Check the magic-link token hasn't expired. Tokens have a default 24-hour window. Customer can request a password reset if they miss the window.

### "Site was accidentally re-provisioned and customer's data was overwritten"

This is why the **Lock after provisioning** setting exists. Turn it on after first successful provision. If the damage is done, restore from a backup.

### "I want to manually trigger provisioning from the central side to re-sync"

On the target site, clear the lock, then POST a fresh payload. Audit log tracks the re-sync event.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
