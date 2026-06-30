---
title: "EP Newsletter"
description: "Newsletter management for PageMotor. Subscribers, lists, campaigns with batch sending, open and click tracking, autoresponder sequences, content digests. Delivery via EP Email."
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
- **Delivery extensions.** Swap in Mailgun (the recommended provider) or a custom driver.
- **Webhook handling** for bounces and complaints from delivery services.
- **PM API control** *(new in 1.2.0)* — manage lists, subscribers, campaigns and autoresponders over the PM API and MCP, no direct database access.
- **Unified send log** *(new in 1.2.0)* — every send recorded in one table with a type/source column for deliverability diagnosis.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Email** (required)
- **EP Suite base class**

Optional:

- **EP Newsletter Mailgun** for Mailgun delivery (the recommended provider).
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
- **Rate limiting.** Minutes between subscription attempts from the same IP. Catches lazy bots; does NOT stop attackers who rotate through Tor exits or proxy pools — see Abuse prevention below for that.

### Abuse prevention

Four layers of defence against subscription form abuse, layered to catch different attack shapes:

| Layer | Stops | Blind spot |
|---|---|---|
| Honeypot field | Naive bots that fill every field | Sophisticated bots targeting only visible fields |
| Per-IP rate limit | Lazy bots hammering from one IP | Attackers rotating through Tor exits or proxy pools |
| **Per-domain frequency cap** *(new in 1.1.27)* | Subscription-bombing where one victim email domain is signed up to many newsletters at once | Single-victim, single-mailbox attacks |
| **Disposable email blocklist** *(new in 1.1.27)* | Sign-ups from throwaway inbox providers (mailinator, guerrillamail, 10minutemail, ~130 others) | Custom-domain disposable services not yet on the list |

**Per-domain frequency cap.** When too many sign-ups arrive for the same recipient email domain within a rolling window, further sign-ups to that domain are silently accepted but never stored. Designed to defeat subscription-bombing attacks: per-IP rate limiting does nothing against them because each request comes from a different IP. The cap watches the email **domain** instead. Defaults to 5 sign-ups per domain per 24 hours. Silent success (not visible failure) so attackers cannot probe for the threshold.

**Disposable email blocklist.** Sign-ups from known disposable / throwaway providers are rejected with an honest "please use your regular email address" message. Built-in list covers ~130 providers including the major families (mailinator, guerrillamail, 10minutemail, yopmail, temp-mail, trash). Add your own domains via the **Additional Blocked Domains** textarea (one per line or comma-separated, `#` starts a comment). For developers, the `ep_newsletter_disposable_domains` filter accepts a richer list at runtime.

**Scope.** Both new checks only fire on the public `[newsletter-form]` shortcode. Admin-side **Add Subscriber**, CSV **Import**, and the `subscribe_external()` public API (used by EP Booking and similar plugins for legitimate checkout-time sign-ups) are intentionally unaffected.

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

- **Driver.** EP Email built-in (uses your configured SMTP), Mailgun (via EP Newsletter Mailgun, the recommended provider), or any registered third-party driver.
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

## Background processing (scheduled sending)

Scheduled campaigns, autoresponder sequences, and automated digests are all delivered by a background queue runner. It fires automatically whenever an admin page loads (throttled to once a minute), which is fine for a busy site. On a quiet site where nobody is signed into the admin, that trigger never runs and scheduled email stalls silently.

*(new in 1.1.29)* To drive the queue on a quiet site, EP Newsletter exposes a secret-token cron URL:

```
https://your-site.com/?ep_newsletter_cron=<secret>
```

The ready-made URL, with a crontab example, is under **Settings → Background Processing**. Point a system cron job or uptime monitor at it, for example every five minutes:

```
*/5 * * * * curl -s "https://your-site.com/?ep_newsletter_cron=<secret>" >/dev/null 2>&1
```

The token is generated once and checked with a timing-safe compare; a wrong or missing token returns HTTP 403 and does no work. Keep the URL private (anyone with it can trigger a send, though it exposes no subscriber data). The admin-page-load trigger still works as a fallback, and the `process-queue` API action below does the same job for an authenticated caller.

## Managing EP Newsletter over the PM API

*(new in 1.2.0)* EP Newsletter registers PM API actions under the `EP_Newsletter` class, so an agent or script can drive the whole content-to-email pipeline through the PM API and MCP without writing to the database directly. Browse them with `list-actions`, inspect one with `describe-action`, then invoke with `call-action`. Each handler returns the standard result envelope (`{success, data}` on success, `{success:false, reason}` on a problem).

Access tiers follow the data each action touches: reads are `read-only` so an agent can report without write access, writes are `admin`, and `subscribe` is `producer` (a trusted caller).

*1.2.1 adds autoresponder edit and delete actions, read actions for the queue and the send log, and a `delay_minutes` option on email steps so sequences can run sub-hour.*

| Action | Access | Purpose |
|---|---|---|
| `list-lists` | read-only | All mailing lists with subscriber counts. |
| `list-subscribers` | admin | Subscribers, filterable by `list_id` and `status`, paginated. |
| `list-campaigns` | read-only | Campaigns with open and click counts. |
| `list-autoresponders` | read-only | Autoresponder series with their email steps. |
| `get-campaign-stats` | read-only | Open and click stats for one campaign. |
| `subscribe` | producer | Subscribe a contact. Skips double opt-in and the public abuse checks, like the internal sign-up path. |
| `unsubscribe` | admin | Unsubscribe by email and cancel pending autoresponder emails. |
| `create-list` | admin | Create a mailing list. |
| `delete-list` | admin | Delete a list. Subscribers are kept. |
| `create-campaign` | admin | Create a draft campaign. |
| `update-campaign` | admin | Update a campaign's subject, body, list, or template. |
| `send-campaign` | admin | Queue recipients and start sending now. |
| `schedule-campaign` | admin | Schedule a draft to send at a future time. |
| `create-autoresponder` | admin | Create an autoresponder series. |
| `add-email` | admin | Add a timed email step to a series (delay in days, hours, and minutes). |
| `update-autoresponder` | admin | Update a series (name, list binding, or active/paused status). |
| `delete-autoresponder` | admin | Delete a series and all its email steps and pending queue items. |
| `update-email` | admin | Update one email step (subject, body, delays, template). |
| `delete-email` | admin | Delete one email step and its pending queue items. |
| `get-autoresponder-queue` | admin | Read the autoresponder queue (pending, sent, failed, cancelled) with scheduled times, filterable by subscriber or status. |
| `process-queue` | admin | Run the background queue now: due campaign batches, autoresponder emails, scheduled campaigns, and due digests. |
| `list-send-log` | admin | Read the unified send log, newest first, filterable by `send_type`. |

The API `subscribe` deliberately bypasses the per-domain cap and disposable-email blocklist that guard the public `[newsletter-form]`, because an authenticated API caller is trusted. This is the same reasoning as the `subscribe_external()` PHP path that EP Booking uses for checkout-time sign-ups.

## Delivery log

*(new in 1.2.0)* Every newsletter send is recorded in a single table, `ep_newsletter_send_log`, whichever delivery route it took (an external driver, EP Email, EP Email's SMTP class, or the PHP mail fallback). Each row carries a `send_type` column (campaign, autoresponder, welcome, confirmation, transactional), the recipient, status, the driver used, the provider message id, and the related campaign and subscriber ids. One place to diagnose deliverability, instead of piecing it together from the queue tables. Read it over the API with `list-send-log` (new in 1.2.1).

## Troubleshooting

### “Campaign paused partway through sending”

Usually an SMTP error that tripped the driver. Check EP Email's delivery log. If SMTP is the problem, fix it and click Resume on the campaign.

### “Open rates are 0%”

Open tracking uses an invisible pixel. Gmail, Apple Mail's privacy protection, and most modern clients proxy images so tracking pixels don't load per-user. Open rates have become unreliable metrics regardless of plugin.

### “Subscribers complain about not receiving confirmation emails”

EP Email SMTP config is wrong, or emails are going to spam. Check EP Email's delivery log. Test with a Gmail address you control.

### “I'm hitting my SMTP provider's rate limit”

Drop batch size, increase batch delay. If you're regularly sending thousands, consider EP Newsletter Mailgun which handles higher volumes more smoothly.

### “Bounce addresses keep receiving campaigns”

Check the bounce check. Click **Check bounces** manually. If bounces aren't being flagged, the delivery driver's bounce webhook isn't configured.

### “Content digest doesn't include my new page”

Digests only include content matching their query. Check the digest's content type filter. Drafts and scheduled-but-not-yet-published pages don't count until they're actually live.

### “Subscription form being subscription-bombed”

Dozens of pending subscribers with random-alphanumeric names and IPs from Tor exit ranges or commercial proxy pools. Your form is on a publicly-harvested list of newsletter forms and a bot is signing one or more victim addresses up to all of them at once. Per-IP rate limiting does nothing here because each request comes from a different IP. Confirm **Abuse prevention → Per-Domain Frequency Cap** is on (lower the count to 3 or 1 if the attack is concentrated on a single recipient domain) and **Disposable Email Blocklist** is on. Clean up the pending spam in **Subscribers**. The frequency cap is a rolling window so once an attack subsides the cap auto-lifts.

### “Legitimate user with a temp email is being rejected”

The disposable blocklist working as intended. If you want to allow one specific provider, add it as an exception via the `ep_newsletter_disposable_domains` filter in site code. To disable the whole blocklist, untick **Abuse prevention → Disposable Email Blocklist**.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
