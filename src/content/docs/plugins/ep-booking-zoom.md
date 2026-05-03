---
title: "EP Booking Zoom"
description: "Zoom meeting add-on for EP Booking. Creates a Zoom meeting automatically when a booking is confirmed, deletes it on cancellation. Server-to-Server OAuth."
sidebar:
  order: 10
---

EP Booking Zoom is an add-on for [EP Booking](/plugins/ep-booking/). When a booking is confirmed, this plugin creates a Zoom meeting and puts the join link into the confirmation email. When the booking is cancelled, the Zoom meeting is deleted.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Zero customer friction. Your customer books as normal, gets the confirmation email, and finds a Zoom link embedded. Your staff member gets the host link. Neither side has to create or join anything manually.

Works across all confirmation paths:

- **Free bookings** confirmed on submission.
- **Paid bookings** confirmed after Stripe webhook settles the payment.
- **Manual confirmations** from the admin when a booking starts as Pending.

And on the other side:

- **Cancellations** from the admin dashboard.
- **Self-service cancellations** via the tokenised link in the confirmation email.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**
- **EP Booking** (this plugin is driven by EP Booking's confirmation and cancellation events)
- **A Zoom account** with a Server-to-Server OAuth app configured in the Zoom App Marketplace

## Setting up the Zoom app

Zoom requires a one-time setup in their Marketplace to generate API credentials.

1. Sign in to the [Zoom App Marketplace](https://marketplace.zoom.us/) with the Zoom account that owns the host user.
2. Go to **Develop → Build App** and pick **Server-to-Server OAuth**.
3. Name it (e.g. "PageMotor bookings"), click **Create**.
4. From the **App Credentials** page, copy:
   - **Account ID**
   - **Client ID**
   - **Client Secret**
5. Under **Scopes**, add:
   - `meeting:write:admin` — create and delete meetings
   - `meeting:read:admin` — read meeting details
6. Under **Activation**, click **Activate your app**.

Keep these credentials handy for the next step.

## Installation

1. Download `ep-booking-zoom.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Booking Zoom**.

## Settings

### Zoom API section

- **Enable Zoom integration.** Toggle off if you want to temporarily disable without uninstalling.
- **Account ID, Client ID, Client Secret.** Paste from the Zoom Marketplace.
- **Test Connection** button. Verifies credentials are valid and your scopes are right. Do this before relying on it in production.

The settings page also embeds a step-by-step setup guide for the Marketplace steps above, in case you need a reminder.

### Meeting Settings section

- **Timezone** for meeting creation. Defaults to your server timezone. Pick from the dropdown.
- **Placeholder reference.** A list of the email placeholders this plugin adds to EP Booking's notification templates. Covered below.

## Email placeholders added

This plugin adds two new placeholders to EP Booking's notification templates:

- `{zoom_url}` — the **customer's** join link.
- `{zoom_host_url}` — the **host/staff's** start link.

Edit your EP Booking notification templates to include these. A simple addition to the confirmation template:

```
Hi {customer_name},

Your {service_name} with {staff_name} is confirmed for {booking_date} at {booking_time}.

Join on Zoom: {zoom_url}

Need to cancel? {cancel_link}
```

Send the host URL in a separate admin-alert template so customers don't accidentally start the meeting for the host.

## How the integration runs

1. EP Booking confirms a booking (free flow, Stripe webhook, or admin manual confirm).
2. EP Booking Zoom receives the confirmation event.
3. Calls the Zoom API with service name, booking date/time, duration.
4. Zoom returns a meeting ID, join URL, and start URL.
5. EP Booking Zoom stores these in its own database table, keyed to the booking ID.
6. The confirmation email template substitutes `{zoom_url}` and `{zoom_host_url}` with the stored values.

On cancellation:

1. EP Booking fires the cancellation event.
2. EP Booking Zoom calls Zoom's delete-meeting API.
3. The stored row is marked as cancelled.

## Duplicate protection

If for any reason EP Booking fires a confirmation event twice for the same booking (rare but possible), EP Booking Zoom checks its own table first and does NOT create a second meeting. The existing meeting is reused.

## Troubleshooting

### "Test Connection succeeds but bookings still don't get Zoom links"

The scope you added is read-only. Go back to Zoom Marketplace → Scopes and add `meeting:write:admin` specifically. Read-only scopes are not enough to create meetings.

### "Test Connection fails with invalid_client"

Client ID or Client Secret is wrong. Regenerate the secret in Zoom Marketplace and paste again carefully. Secrets can have leading/trailing whitespace that breaks them.

### "Meeting is created but the link is blank in the email"

The placeholder `{zoom_url}` must be inside the EP Booking template for the relevant notification (confirmation / reminder). Edit the template from EP Booking's settings. Re-sending the email (via EP Email's delivery log) after fixing the template does NOT retroactively fill it — the substitution happens at send time.

### "Cancellation deletes the booking but the Zoom meeting is still active"

Check the Zoom Marketplace app is still activated. If the app was deactivated after the meeting was created, the delete API call will fail silently. Re-activate the app.

### "Customers complain the start time in Zoom doesn't match my site"

The timezone setting in this plugin must match your EP Booking timezone. They are separate settings because Zoom requires its own timezone on the meeting object.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
