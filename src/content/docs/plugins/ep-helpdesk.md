---
title: "EP Helpdesk"
description: "AI-first support ticket system for EP Suite plugins. Structured intake, two-pass auto-send pipeline, Pushover admin alerts, 48-hour retract window."
sidebar:
  order: 34
---

EP Helpdesk is a support desk that accepts structured tickets from your customers, asks Claude to draft a reply grounded in your docs, safety-checks the draft with a second model pass, then either sends the reply automatically or flags it for a human. Live demo at [help.elmspark.com](https://help.elmspark.com/).

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Structured intake form** with four primary categories (installing, something broken, a question, billing), each revealing a short subcategory list and category-specific context fields (plugin, version, site URL, hosting, error text).
- **Auto-generated subject line** from category + plugin + site, editable before submit.
- **Two-pass AI pipeline.** A first model drafts the reply from the customer's question and your knowledge base. A second pass checks the draft for accuracy. A clean pass auto-sends; a failed pass regenerates once; two failures flag for a human.
- **Safety net keyword blocklist.** Tickets mentioning billing, refund, cancel, invoice, chargeback, legal, GDPR, complaint, lawyer, or threat never auto-send. They always wait for a human.
- **Rate cap.** Max 20 auto-sends per hour across all tickets. Overflow queues for human review.
- **48-hour retract window.** Admin can one-click retract an auto-sent reply and send an apology within 48 hours. After that, the ticket settles to a normal replied state.
- **Resubmission detection.** Tickets from the same email within four days that match a prior ticket by content flag for human review, so a customer never gets two different AI replies to the same question.
- **Pushover mobile notifications.** Admin gets a push on every flagged ticket, QA failure, resubmission, or auto-send. Deep-links to the specific ticket in admin.
- **Tracking page.** Customers look up their ticket with a reference code, no login.
- **Mobile responsive submission form.** Works one-handed on iPhone and Android.
- **Light / dark mode toggle.** Sun / moon button in the topbar. Follows the visitor's OS preference on first visit, manual override persists in `localStorage`.
- **Docs-link hint.** Once a customer picks a known EP plugin in the intake form, a gold callout offers a direct link to that plugin's docs page. Deflects tickets whose answer is one click away.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Email** for confirmation and reply delivery
- **EP Agent** for the AI proxy and CSRF handling

## Installation

1. Install **EP Email** and **EP Agent** first.
2. Download `ep-helpdesk.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Place the intake form on a page with the `[helpdesk-form]` shortcode.
5. Create a tracking page at `/track/` using the `[helpdesk-status]` shortcode.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[helpdesk-form]` | Structured intake form with category chips, subcategory chips, contextual fields, and auto-subject. |
| `[helpdesk-status]` | Ticket tracking page. Takes a reference code and an email. |

## The intake form

The form has four primary categories, each revealing its own subcategory set:

| Primary | Subcategories |
|---|---|
| Installing or upgrading | New install / Upgrading existing / Activating a licence / Removing a plugin |
| Something isn't working | Site fully down / A feature is broken / Cosmetic / Intermittent |
| I have a question | Plugin configuration / PageMotor core / Hosting / Design / Email / Payment / Other |
| Billing, licence, account | Invoice / Licence key / Subscription / Refund / Change plan / Cancel / Other |

The form collects name, email, subject (auto-filled), and a message. Depending on category, it also asks for plugin slug, plugin version, site URL, hosting, or error text.

When a customer picks a known EP plugin in the plugin-slug field, a gold callout appears below it with a one-click link to that plugin's docs page (`https://documentation.elmspark.com/plugins/<slug>/`). The matcher tolerates variants: `ep-email`, `ep email`, `EP_Email`, `EPEMAIL`, and `email` all resolve to `ep-email`. Free-typed plugin names that do not resolve show no hint (no broken links).

## The auto-send pipeline

When a ticket is submitted, the plugin runs these checks in order:

1. **Resubmission check.** Same email, within four days, similar content -> flag for human.
2. **Keyword blocklist.** Sensitive terms -> flag for human.
3. **Hourly rate cap.** Over 20 auto-sends this hour -> flag for human.
4. **Draft generation.** First model drafts a reply grounded in the knowledge base.
5. **QA pass.** Second model checks the draft against the customer's question.
6. **If QA passes:** reply is sent automatically by email. Status is `auto_sent`.
7. **If QA fails:** the draft is regenerated once with the QA feedback appended. If the second pass still fails, the ticket is flagged for a human.

The whole pipeline typically completes within 15 seconds for auto-sent replies.

## Admin notifications via Pushover

The plugin can push a notification to your phone whenever something interesting happens: a ticket is flagged, an auto-send fires, the rate cap is hit, or a resubmission is detected. Setup takes about five minutes.

### 1. Create a Pushover account

Go to [pushover.net](https://pushover.net) and sign up. Install the Pushover app on your phone (iOS, Android) or desktop (macOS, Windows, Linux) and log in. There is a small one-off fee per device type after a seven-day trial.

### 2. Find your user key

On the Pushover dashboard, your **User Key** is at the top right. It is a 30-character string. Copy it.

### 3. Create an application token

On pushover.net, go to **Create an Application / API Token**. Name it something like "EP Helpdesk". You can leave the description, URL, and icon empty. Submit. Copy the resulting **API Token**, another 30-character string.

### 4. Add the credentials to your site config

Edit the PHP config file that PageMotor loads early (often `config.php` at the site root) and add:

```php
define('EP_HELPDESK_PUSHOVER_TOKEN', 'your-application-api-token');
define('EP_HELPDESK_PUSHOVER_USER', 'your-user-key');
```

Save. The plugin reads these constants on every event, so no reload is needed.

### 5. Test

Submit a ticket with the word `refund` in the subject. The safety-net will catch it and fire a push to your phone. You should see it within a couple of seconds. Tap the notification to jump straight to the ticket in admin.

### What triggers a notification

| Event | Priority | Notes |
|---|---|---|
| Ticket flagged by safety net | Normal | Deep-link opens the ticket in admin |
| Ticket flagged by QA double-fail | High | Needs human review, AI was not confident enough to send |
| Resubmission detected | High | Same email, similar content, within four days |
| Auto-send successful | Normal (warm-up) | Ambient confirmation that auto-sends are firing. Revert to Low in the code once weekly ticket volume makes Normal too noisy. |
| Hourly cap hit | Normal | Investigate if this is sustained |

### Turning it off

Remove the two constants from config.php. The plugin silently skips Pushover when credentials are absent; nothing else is affected.

## Light / dark mode

The helpdesk form and admin both support a theme toggle. A small sun / moon button sits in the topbar.

- **On first visit**, the form follows the visitor's operating-system preference (`prefers-color-scheme`).
- **Clicking the toggle** cycles through auto -> light -> dark -> auto. The choice persists in `localStorage` as `ep-helpdesk-theme` and is applied before the first paint, so dark-mode visitors do not see a flash of light.
- **No server side setting.** Each visitor controls their own theme; no admin configuration needed.

Colours come from a single token set (`--ep-*` variables) with a dark override block, so a future skin change needs one file touched rather than one per surface.

## Retract window

Every auto-sent reply is retractable for 48 hours. From the admin ticket view, click **Retract and apologise**. The plugin:

1. Sends a short apology email to the customer ("Our automatic reply may have missed the mark, a human is taking another look").
2. Sets the ticket status back to `review` and generates a fresh draft for your approval.

After 48 hours, auto-sent tickets transition to `replied` and can no longer be retracted.

## Resubmission detection

The plugin prevents the same customer from getting two different AI replies to the same question. If a customer submits a ticket, then submits another within four days with a similar subject or body, the second is flagged for human review with a reference to the prior ticket.

Matching uses a word-overlap score (Jaccard on tokens) with a threshold. Near-duplicates flag; genuinely different questions do not.

## Troubleshooting

### "Nothing happens after I click Submit"

Check the browser console for JavaScript errors. The chip-based progressive disclosure requires JS. Without JS, the form still submits a ticket, but the category metadata is less complete.

### "The AI draft was wrong"

That is what the 48-hour retract window is for. From admin, open the ticket and hit **Retract and apologise**. Then regenerate the draft or write the reply yourself.

If the same kind of wrongness keeps happening, tune the system prompt in EP Agent to give clearer grounding on the topic that is drifting.

### "I am not getting Pushover notifications"

1. Check `EP_HELPDESK_PUSHOVER_TOKEN` and `EP_HELPDESK_PUSHOVER_USER` are both defined.
2. Check the Pushover app is installed and logged in on your phone.
3. Submit a test ticket with the word `refund` in the subject. It should fire a safety-net ping.
4. Check PHP error log for any Pushover failures.

### "Customer submitted a ticket but didn't get a confirmation email"

EP Email handles delivery. Check EP Email's log. Usually an SMTP credentials or from-address issue.

### "Auto-reply went to spam"

The site's from-address needs SPF, DKIM, and DMARC set up. Ask your hosting provider how to configure DKIM for outgoing mail.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
