---
title: "EP Newsletter"
description: "Newsletter management for PageMotor. Subscribers, lists, campaigns with batch sending, open and click tracking, autoresponder sequences, content digests. Delivery via EP Email."
sidebar:
  order: 39
---

EP Newsletter is a full newsletter system for PageMotor. Subscribers and lists, campaign composition with draft/test/send, batch delivery with configurable pace, open and click tracking, autoresponder sequences triggered by subscription, and automated content digests. Delivery routes through EP Email so SMTP, from-addresses, and deliverability are managed in one place.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Core features:

- **Subscriber management.** Add, import from CSV, export, track source (which form they came from).
- **Lists.** Named mailing lists with segmentation.
- **Campaigns.** Compose, preview, test-send, schedule, send.
- **Batch delivery** with configurable batch size and delay between batches, so you don't overwhelm SMTP providers.
- **Open tracking** via invisible pixel; **click tracking** via link rewriting.
- **Double opt-in** with confirmation and welcome emails.
- **Autoresponders** — timed sequences of emails triggered when someone subscribes.
- **Automated digests** — daily, weekly, or monthly digests of new content on your site.
- **Delivery extensions.** Swap in SendGrid, Mailgun, or a custom driver.
- **Webhook handling** for bounces and complaints from delivery services.

## Requirements

- **PageMotor 0.6 or later**
- **EP Email** (required)
- **EP Suite base class**

Optional:

- **EP Newsletter SendGrid** for SendGrid delivery.
- **EP GDPR** for consent logging on subscription.
- **EP Affiliate** for affiliate-source tracking on subscription.

## Installation

1. Install EP Email.
2. Download `ep-newsletter.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Work through the settings sections below.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[newsletter-form]` | Subscription form. Attributes: `title`, `button`, `name_field=true/false`, `list=slug`. |
| `[newsletter-unsubscribe]` | Unsubscribe page with optional feedback form. |

## Settings sections

### Subscription

- **Double opt-in.** Toggle. If on, subscribers get a confirmation email; only after clicking do they join the list. Strongly recommended.
- **Confirmation email** subject and body.
- **Welcome email** subject and body (sent after confirmation).
- **Confirmation redirect page.** Where to send users after confirming.
- **Default list** for forms without an explicit list attribute.

### Subscription forms

- **Enable.** Toggle the shortcode.
- **Success and already-subscribed messages.**
- **Rate limiting.** Prevents abuse.

### Campaign settings

- **Default template.** Base HTML wrapper for campaigns.
- **Batch size and delay.** E.g. 100 emails per batch, 30-second delay between. Tune to your SMTP provider's rate limits.
- **Open tracking** and **click tracking** toggles.

### Automated newsletters

- **Frequency.** Daily, weekly, monthly.
- **Send day and time.**
- **Target list.**
- **Subject template.** Supports placeholders for date ranges.
- **Email template.** Structure of the digest.

### Unsubscribe

- **Page URL.** Where `[newsletter-unsubscribe]` lives.
- **Success message.**
- **Feedback collection.** Optional — ask why they unsubscribed to improve future content.

### Email delivery

- **Driver.** EP Email built-in (uses your configured SMTP), SendGrid (via EP Newsletter SendGrid), or any registered third-party driver.
- **Test connection** button.
- **Check bounces** button — polls the driver's bounce API and marks bad addresses.

## Campaign workflow

1. **Compose.** Write the subject and body using the campaign editor. Use merge tags like `{first_name}` for personalisation.
2. **Preview.** Render the campaign as it will appear in common mail clients.
3. **Test send.** Send just to your own address to check.
4. **Choose recipients.** Pick one or more lists, or a segment.
5. **Schedule or send now.**
6. **Monitor.** Open and click rates, bounce count, complaint count all update as the campaign progresses.

## Autoresponders

An autoresponder sequence is a series of timed emails. Example welcome sequence:

- Immediately: "Welcome! Here's what to expect."
- +2 days: "Our 5 most useful articles."
- +5 days: "A case study you might like."
- +10 days: "Ready to go deeper?"

Each email has its own subject, body, and delay after subscription. Created once, runs forever.

## Content digests

Set up an automated weekly digest:

- "Blog posts published this week" gathers the last 7 days of new content.
- "New products in stock" pulls from EP Ecommerce Products.
- Custom query for bespoke content types.

Digests run on the schedule you set and only send if there's new content to include.

## Troubleshooting

### "Campaign paused partway through sending"

Usually an SMTP error that tripped the driver. Check EP Email's delivery log. If SMTP is the problem, fix it and click Resume on the campaign.

### "Open rates are 0%"

Open tracking uses an invisible pixel. Gmail, Apple Mail's privacy protection, and most modern clients proxy images so tracking pixels don't load per-user. Open rates have become unreliable metrics regardless of plugin.

### "Subscribers complain about not receiving confirmation emails"

EP Email SMTP config is wrong, or emails are going to spam. Check EP Email's delivery log. Test with a Gmail address you control.

### "I'm hitting my SMTP provider's rate limit"

Drop batch size, increase batch delay. If you're regularly sending thousands, consider EP Newsletter SendGrid which handles higher volumes more smoothly.

### "Bounce addresses keep receiving campaigns"

Check the bounce check. Click **Check bounces** manually. If bounces aren't being flagged, the delivery driver's bounce webhook isn't configured.

### "Content digest doesn't include my new page"

Digests only include content matching their query. Check the digest's content type filter. Drafts and scheduled-but-not-yet-published pages don't count until they're actually live.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
