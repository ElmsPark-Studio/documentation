---
title: "EP WhatsApp"
description: "Two-way WhatsApp messaging for PageMotor via Meta's WhatsApp Business Cloud API. Send notifications, receive replies through a signed webhook, and read and answer conversations from an admin inbox."
---

EP WhatsApp connects your PageMotor site directly to Meta's WhatsApp Business Cloud API. It sends messages out, receives incoming ones through a signed webhook, and gives you a simple admin inbox to read and reply to customer conversations. There is no middleman service in between: your site talks to Meta directly, using your own credentials.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Use cases:

- **Booking and order notifications.** Other EP plugins, including EP Booking and EP Boarding, can send through EP WhatsApp as a notification channel instead of, or alongside, email.
- **Customer conversations.** A customer replies to a notification and their message lands in the admin inbox, where you can answer it.
- **Reaching people who do not read email.** For some audiences a WhatsApp message is opened in minutes and an email never is.

## How it works

1. You create a WhatsApp app in Meta's developer console and get a phone number ID, an access token and an app secret.
2. You paste those three values into the plugin's settings screen.
3. The plugin generates a verify token and shows you the webhook URL to hand back to Meta.
4. Meta calls that webhook to confirm the verify token, then delivers every inbound message to it.
5. Incoming messages are checked against the app secret signature before they are trusted, then stored as conversation threads.
6. You read and answer those threads in the admin inbox. Replies go back out through the same API.

## Requirements

- **PageMotor 0.9 or later**
- **EP Suite base class** (bundled with the plugin)
- **A Meta WhatsApp Business account**, with a phone number ID, access token and app secret

The Meta side is the fiddly part. WhatsApp Business is Meta's product, with Meta's approval process, message templates and rate limits. This plugin does not change any of that; it connects your site to it.

## Installation

1. `ep-whatsapp.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP WhatsApp**.

## Settings

| Setting | What it does |
| --- | --- |
| **WhatsApp messaging** | Master on/off switch. Leave it off until the Meta credentials are in and the webhook is verified. |
| **Phone number ID** | The sending number's ID from the Meta app dashboard. Not the phone number itself. |
| **Access token** | The token the plugin authenticates to Meta with. |
| **App secret** | Used to verify the signature on every inbound webhook call, so a forged request cannot inject a fake message. |
| **Default country code** | Applied to recipient numbers entered without one, so local-format numbers still reach the right person. |

## The webhook

The plugin answers Meta's webhook at:

```
https://your-site.example/?ep_whatsapp_webhook=1
```

It is handled before any page rendering, so the response Meta receives is the bare acknowledgement it expects rather than a themed page. The verify token is generated for you on first use and shown alongside the URL; paste both into Meta's webhook configuration.

Inbound calls carrying an invalid or missing signature are rejected. Do not disable that check to "make the webhook work" — an unsigned webhook endpoint lets anyone post messages into your inbox as if they were a customer.

## Sending from other plugins

EP WhatsApp exposes two sending methods other EP plugins can call, `send_text()` for a plain message and `send_template()` for one of your approved Meta message templates. Meta only permits free-form text inside an open conversation window; outside it you must use an approved template. That is a Meta rule, not a plugin limitation.

## Troubleshooting

**The webhook never verifies.** Check the URL is reachable from outside your network and returns quickly. A host bot wall or a caching layer in front of the site will break verification; [EP Host Check](/plugins/ep-host-check/) reports both.

**Messages send but replies never arrive.** The webhook is not configured, or its signature check is failing because the app secret does not match the app the messages are going through.

**Nothing sends and the log mentions a token.** Meta access tokens expire. Regenerate in the Meta dashboard and paste the new one in.

## Changelog

### 0.1.4

**The plugin could never deliver its own updates. Fixed.** PageMotor builds its update check from each plugin's `Updates:` header and skips any plugin that has none. This plugin's header block never carried that line, so 0.1.3 was invisible to the Updates screen from the moment it shipped — the plugin was excluded from every update check rather than up to date.

**This fix cannot deliver itself.** An install on 0.1.3 has no `Updates:` header and so cannot be offered this release. Download 0.1.4 and upload it once through **Plugins → Manage Plugins**; from then on the Updates screen works normally.

### 0.1.3

First release on the ElmsPark update channel; earlier 0.1.x builds were internal only.

Fixes "Your session has expired. Please reload to ensure your security." on PageMotor 0.11, which affected the admin settings screen. The CSRF header was being attached twice — once by the plugin, as PageMotor 0.10 required for raw requests, and once by 0.11's new automatic attachment — and because attaching appends rather than overwrites, the token went out doubled and never matched. The plugin now attaches it only when the core has not already done so.
