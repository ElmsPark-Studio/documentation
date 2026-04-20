---
title: "EP Connect"
description: "Outbound webhooks for PageMotor. Send JSON payloads to Zapier, Make, Slack, or any URL when events happen on your site. HMAC-signed, sensitive-field-stripped."
sidebar:
  order: 15
---

EP Connect sends webhook notifications from your PageMotor site to external services when things happen. Someone fills out a contact form, a booking is confirmed, a newsletter subscription lands — EP Connect fires a JSON POST to whatever URL you configured.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Use EP Connect to plug PageMotor into the wider automation ecosystem:

- **Zapier** or **Make** to trigger multi-step automations.
- **Slack** or **Discord** to post alerts to a channel.
- **Your own API** for custom workflows.
- **Google Sheets** via Zapier or Apps Script to log every event.

Seven built-in events, with hooks for other plugins to register their own.

## Built-in events

| Event | Source plugin | Fired when |
|---|---|---|
| **Email Form Submitted** | EP Email | Someone submits a contact form. |
| **Booking Confirmed** | EP Booking | A booking moves to Confirmed status. |
| **Newsletter Subscription** | EP Newsletter | Someone opts in to a newsletter list. |
| **Comment Posted** | EP Comments | A comment is submitted (before moderation). |
| **Order Completed** | EP Ecommerce | An order settles payment. |
| **Content Published** | PageMotor core | A page's status changes to Published. |
| **User Registered** | PageMotor core | A new user account is created. |

Five events (Email, Booking, Newsletter, Comments, Ecommerce) fire in **real time** via the `emit()` API. The remaining two (Content Published and User Registered) use **database observation** with a 30-second throttle, because PageMotor core doesn't have an emit hook for them. Events still arrive, just with up to 30 seconds of latency.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class** (bundled)

## Installation

1. Download `ep-connect.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.

## Setting up a webhook

1. Open **Plugin Settings → EP Connect**.
2. Click **Add Webhook**.
3. Fill in:
   - **Name** — internal label, e.g. "Slack alerts".
   - **Event** — pick from the dropdown (the seven built-in events plus any custom ones).
   - **URL** — the endpoint to POST to.
   - **Secret** — a string used to sign the payload via HMAC-SHA256. Your receiving endpoint uses this to verify the payload came from you and wasn't tampered with. Generate a random 32-character string and paste it here and on the receiver.
   - **Enabled** — toggle.
4. Click **Save**.
5. Click **Send Test** on the saved webhook row. A sample payload fires to your URL. Check the receiver got it.

## Payload format

Every webhook POST body is JSON with this shape:

```json
{
  "event": "booking.confirmed",
  "site": "https://yoursite.com",
  "timestamp": "2026-04-20T14:32:11Z",
  "data": {
    "booking_id": 123,
    "service": "60-minute consultation",
    "customer_name": "Alice Smith",
    "customer_email": "alice@example.com",
    "...": "..."
  }
}
```

Headers:

- `Content-Type: application/json`
- `User-Agent: EP-Connect/1.0`
- `X-EP-Signature: sha256=<hex>` — HMAC-SHA256 of the body using your webhook secret. The receiver recomputes and compares.

## Signature verification

On your receiver, verify signatures before trusting the payload. Example in Node.js:

```js
import crypto from 'node:crypto';

const body = rawRequestBody;
const signature = request.headers['x-ep-signature']; // "sha256=<hex>"
const expected = 'sha256=' + crypto
  .createHmac('sha256', process.env.EP_CONNECT_SECRET)
  .update(body)
  .digest('hex');

if (signature !== expected) {
  return response.status(401).send('Invalid signature');
}
```

Without verification, anyone who guesses your webhook URL can fake payloads. Always verify.

## What sensitive fields are stripped

The plugin deliberately excludes these from every payload:

- **Passwords** (duh).
- **API tokens** (session tokens, CSRF tokens, nonces).
- **IP addresses** of end users (GDPR).
- **Any field starting with `_`** (convention for "internal").

If your receiver needs one of these, say so in the review queue — the filter list is configurable but deliberately strict by default.

## Delivery log

The settings page shows the last 200 deliveries across all webhooks:

- Event, webhook name, destination URL (truncated), HTTP status code, duration.
- Green for 2xx, yellow for 3xx, red for 4xx and 5xx.
- Click a row to see the full request and response.

Logs auto-rotate after 200 entries.

## Performance

- Webhook delivery happens via `register_shutdown_function()`, **after** the response has been sent to the user. Zero latency impact on your page loads.
- 30-second observation throttle for DB-observed events so this plugin never becomes the performance bottleneck on a busy site.

## Registering custom events from another plugin

Any plugin can add an event to the dropdown by calling:

```php
EP_Connect::register_event('my_plugin.something_happened', 'My custom event');
```

Then emit it when the thing happens:

```php
EP_Connect::emit('my_plugin.something_happened', [
    'field' => 'value',
    'another' => 42,
]);
```

Your event appears in the webhook dropdown and fires through the same signing and delivery pipeline as built-in events.

## Troubleshooting

### "Send Test succeeds but real events don't fire"

Check the webhook is **Enabled** (toggle in the management UI). Check the event you are expecting actually happened — look at the source plugin's own logs.

### "Receiver gets the payload but signature verification fails"

The secret on your receiver must match the secret saved on the webhook row, byte-for-byte, including any trailing whitespace. Rotate the secret and paste it cleanly on both sides.

### "Delivery log shows HTTP 403 from my receiver"

Your receiver is rejecting the request. Common cause: the receiver expects a specific User-Agent or authentication header. EP Connect sends `User-Agent: EP-Connect/1.0` and the `X-EP-Signature` header. If the receiver needs anything else, it needs to be a proxy or adapter, not a direct EP Connect target.

### "Delivery log shows 'timeout' for every event"

The receiver is slow or unreachable. EP Connect waits up to 10 seconds. If your receiver is legitimately slow, use a faster endpoint (a Zapier webhook that queues, rather than a slow direct integration).

### "Events I expect to fire aren't in the delivery log"

Some events come from plugins that must be active and configured. For example, "Booking Confirmed" only fires if EP Booking is installed and a booking was actually confirmed. Check the source plugin is doing its bit.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
