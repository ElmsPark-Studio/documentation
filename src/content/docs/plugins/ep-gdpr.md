---
title: "EP GDPR"
description: GDPR compliance toolkit for PageMotor. Cookie consent banner, data subject request handling, consent logging, and cross-plugin integration with EP Email, EP Newsletter, and EP Booking.
sidebar:
  order: 33
---

EP GDPR is a complete GDPR compliance toolkit for PageMotor. Cookie consent banner, data subject request handling (access, rectification, erasure, portability), consent logging across forms and subscriptions, and integration with every EP Suite plugin that touches personal data.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Three pillars of GDPR that the plugin handles:

### Cookie consent

A customisable banner that asks visitors to accept or reject cookies. Supports granular categories (necessary, analytics, marketing) so visitors can accept some and reject others. Remembers the choice across sessions. Provides a "Revisit consent" link visitors can click at any time to change their mind.

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

- **PageMotor 0.7 or later**
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

- **Banner text.** Shown when the visitor first arrives. British English default.
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

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
