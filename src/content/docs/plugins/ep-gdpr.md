---
title: "EP GDPR"
description: "GDPR compliance toolkit for PageMotor. Cookie consent banner, data subject request handling, consent logging, and cross-plugin integration with EP Email, EP Newsletter, and EP Booking."
sidebar:
  order: 33
---

EP GDPR is a complete GDPR compliance toolkit for PageMotor. Cookie consent banner, data subject request handling (access, rectification, erasure, portability), consent logging across forms and subscriptions, and integration with every EP Suite plugin that touches personal data.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Three pillars of GDPR that the plugin handles:

### Cookie consent

A customisable banner that asks visitors to accept or reject cookies. Supports granular categories (necessary, analytics, marketing) so visitors can accept some and reject others. Remembers the choice across sessions. Provides a "Revisit consent" link visitors can click at any time to change their mind.

### Form consent

Adds an opt-in consent checkbox above the submit button on every EP Email contact form. The checkbox text and required-or-optional behaviour are configurable. Independent of the cookie banner: a site that has no third-party tracking and therefore needs no banner can still enable form consent for the personal data captured by enquiry forms.

### Data subject requests

Four rights, handled through a single admin dashboard:

- **Access** — "What data do you hold about me?" Generates a JSON or HTML export.
- **Rectification** — "This data is wrong, change it."
- **Erasure** — "Delete all my data." Coordinates with every EP plugin that holds data.
- **Portability** — "Give me my data in a machine-readable format." JSON export.

Each request is logged with timestamps for the full lifecycle (received, under review, completed) so you have an audit trail.

### Consent logging

Every form submission, newsletter signup, and booking that happens while EP GDPR is installed logs the consent state at that moment. If a visitor later requests data, you can show them exactly what they consented to and when.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**

Coordinates with (optional):

- **EP Email** — logs consent on form submissions.
- **EP Newsletter** — logs consent on subscriptions.
- **EP Booking** — logs consent on booking submissions.
- **EP Ecommerce** — logs consent on purchases.
- **EP Bunny Fonts** — reports compliance on font delivery.

## Installation

1. Download `ep-gdpr.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP GDPR** and work through the configuration.

## Cookie consent configuration

- **Banner text.** Shown when the visitor first arrives. The default placeholder ("This website uses cookies to ensure you get the best experience...") is neutral English; replace with your own wording in any language or variant you prefer.
- **Categories.** Necessary (always on, informational), Analytics (EP Analytics doesn't set cookies, but listed for completeness), Marketing. Add custom categories if a plugin needs them.
- **Position.** Bottom banner, top banner, or centre modal.
- **Colours.** Match your site styling.
- **Privacy policy link.** Required — the banner must link to your privacy policy.
- **Revisit link shortcode.** Add `[gdpr-consent-reopen]` to your footer so visitors can change their mind.

## Data subject request form

Drop `[gdpr-request]` on a dedicated page, typically `/privacy-rights/` or similar, linked from your privacy policy.

The form collects:

- Type of request (access, rectification, erasure, portability).
- Name, email.
- Description of the request.
- Verification — email confirmation to prevent fake requests on someone else's data.

Submissions land in the admin dashboard for processing.

## Handling a data subject request

From **Plugin Settings → EP GDPR → Requests**:

1. Click the request to open it.
2. Verify identity (usually email confirmation is enough; for high-risk cases, ask for more).
3. Click **Gather data** — the plugin queries every EP Suite plugin for records matching the email address, assembles them into a single export.
4. Review the export for anything to redact.
5. Send it to the requester (download and email, or use the plugin's built-in send button).
6. Mark the request completed.

For erasure:

1. Click **Gather data** to see what will be deleted.
2. Click **Erase** — every EP Suite plugin deletes or anonymises its records.
3. The consent log entry for this email stays (audit requirement), but is flagged as "subject erased".

## Consent log

Admin view shows:

- Every consent event with timestamp, email, context (which form / plugin), and what they consented to.
- Searchable by email.
- Used as evidence when handling data subject requests.

## Cross-plugin integration

When a plugin hooks into EP GDPR, it:

- Logs consent on opt-in (form submit, subscription, booking).
- Exposes data to the data subject request flow.
- Responds to erasure by deleting or anonymising its records.

EP Email, EP Newsletter, EP Booking, EP Ecommerce, EP Comments, and EP Affiliate all integrate.

## Compliance dashboard

A single page shows your compliance status:

- Cookie consent banner active.
- Privacy policy linked.
- Data subject request form configured.
- Consent logging active on each integrated plugin.
- Font delivery GDPR-compliant (via EP Bunny Fonts).

Red and green indicators. Green means that area is sorted.

## Troubleshooting

### "Banner doesn't appear"

Check **Settings → EP GDPR → Cookie consent → Enabled**. Also check the banner isn't being hidden by an ad-blocker — some aggressive blockers hide consent dialogs.

### "Erasure didn't delete a record in plugin X"

Not every plugin integrates with EP GDPR's erasure flow. The dashboard shows which do. Manual deletion is required for non-integrated plugins. Log the gap in the review queue if you spot one.

### "Data export contains fields that shouldn't be there"

Plugins control what they expose. If a field shouldn't be in the export, it's either sensitive data that's leaking (bug) or metadata the plugin considers user-facing (intentional). Log specifics in the review queue.

### "Consent log is huge"

Retention is configurable. Default retains everything. Consider a 24-month retention for non-erasure consent events and indefinite for consents tied to existing active accounts.

### "Visitors complain about the banner appearing on every page load"

Check cookies are being set correctly. If the visitor's browser blocks all cookies, the banner has no way to remember their choice and shows every time. Nothing to fix — their browser is actively preventing persistence.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
