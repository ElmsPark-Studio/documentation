---
title: "EP Events"
description: "The PageMotor event platform. Events with tickets, registrations, check-in, Stripe Connect payments, Zoom, Schema.org, ICS feeds, six EU languages, and depth integration across the EP Suite."
---

EP Events turns a PageMotor site into a full event platform. Events with tiered ticketing, buyer registrations, attendee QR codes, an offline-capable check-in PWA, Stripe Connect payments with EU VAT compliance, automated Zoom meeting creation, Schema.org JSON-LD, ICS calendar feeds, post-event newsletter campaigns, and depth integration across the rest of the EP Suite.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

What you get end-to-end:

1. You define **events** (sub-typed as conference, workshop, retreat, gala, meetup, seminar, summit, reunion, speed-dating, tournament, webinar, or neutral). Each event gets a body laid out with the matching sub-type's editorial stack.
2. You define **tickets** as EP Ecommerce products attached to the event. Tiered pricing, member-only gating, and inventory caps are all available.
3. You optionally add **speakers**, **sponsors**, **promo codes**, **payment plans**, and a **venue** (online, hybrid, or physical).
4. Visitors browse upcoming events via the `[events]` listing page, land on an individual event, register through `[event-register]`, and pay via Stripe Connect.
5. On payment, the buyer becomes a customer, each ticket becomes an attendee with a unique QR token, a confirmation email goes out with ICS attachment, the newsletter list segment grows, and Zoom auto-creates the meeting where applicable.
6. On the day, your organiser opens `[event-checkin]` on a phone or tablet at the gate. The page works offline as a PWA, snapshots attendees to local storage, validates QR codes against the snapshot, and syncs check-ins back to the server when the network returns.
7. After the event, automated thank-you emails and a recap newsletter campaign go out. Post-event reports and a no-show sweep run on cron.

What EP Events is NOT: a one-off appointment scheduler (that is EP Booking), a course platform (EP Courses), or a generic calendar widget. It is for events with buyers, attendees, money, and operational depth.

## Requirements

- **PageMotor 0.8.3 or later**
- **EP Suite base class** (bundled)
- **EP Ecommerce** and **EP Ecommerce Stripe** for payments
- **EP Email** for transactional mail (confirmations, reminders, thank-you)

Optional siblings (each unlocks specific features when present):

- **EP SEO 1.5.4+**: per-event Open Graph and Twitter Card metadata via the `record_meta()` iteration hook
- **EP GDPR 1.1.28+**: DSR export and erasure for buyer data via the sibling-plugin hook
- **EP Assistant 1.0.4+**: AI table allowlist + PII filter so the assistant can read aggregate event data without buyer PII
- **EP MCP Bridge 0.18.0+**: three MCP tools registered: `events_list_upcoming`, `events_get_by_slug`, `events_get_stats`
- **EP Newsletter**: auto-subscribe attendees with per-event segmentation, recap + next-year-invite campaigns
- **EP Cards**: render the `[events]` listing through EP Cards' renderer
- **EP Affiliate**: capture referral attribution at registration, fire conversion tracking on confirmation
- **EP Membership**: prefill member identity on the registration form, optionally auto-apply a member promo code
- **EP Booking Zoom**: auto-create Zoom meetings for online events
- **EP Locations** / **EP Local Business**: resolve Organisation identity in Schema.org

## Installation

EP Events installs like any PageMotor plugin.

1. **Download.** Grab `ep-events.zip` from your ElmsPark account.
2. **Sign in to your PageMotor admin** at `yourdomain.com/admin/`.
3. **Go to Plugins, then Manage Plugins.**
4. **Upload the zip.** Use the plugin upload interface to upload `ep-events.zip`.
5. **Activate in your Theme.** Enable EP Events in your active Theme's plugin configuration. On first activation:
    - 17 database tables are created (`pm_ep_events_meta`, `pm_ep_events_registrations`, `pm_ep_events_attendees`, and so on).
    - The Event template is cloned from your active theme's Page template.
    - A sample event is seeded at `/ep-events-sample/`.
    - An Events listing page is auto-created at `/events/` (or your configured slug).

**How to verify:** after activation, go to **Plugins then Plugin Settings**. You should see **EP Events Settings** with the Quick Start panel at the top showing the sample event URL and listing URL. Both should resolve when you click them.

## Configuration

EP Events settings are split into sections you can collapse and expand:

- **Quick Start**: sample event, listing URL, hint for creating your next event.
- **Configuration**: listing slug, timezone, default sub-type, currency, payment provider routing.
- **Stripe Connect**: onboard your platform Stripe account so payments route correctly.
- **VAT and tax**: EU rate table (27 countries plus UK) with VIES B2B reverse-charge validation.
- **Email reminders**: pre-event 7-day, 24-hour, 1-hour windows; post-event thank-you. Idempotent via the email_sends log.
- **Cron**: three trigger paths (admin-page-load throttled to 60s, external secret endpoint, admin AJAX). The secret is autogenerated and shown here.
- **Newsletter integration**: per-event segmentation, recap, next-year invites.
- **AI Organiser Suite**: 11 bundled `ep-agent` skills for event-from-brief, pricing, promo copy, schedule, speaker outreach, sponsor outreach, FAQ, follow-up, attendance prediction, anomaly detection, recap.
- **AI Schema**: export an event as Markdown, import a full event definition (event + tickets + speakers + sponsors + promos + email sequence + theme) atomically.
- **Shortcodes reference**: every shortcode the plugin registers, with the key arguments. Useful while authoring event bodies.

### Stripe Connect

Stripe Connect is required for payments to route to the right place. EP Events itself does not collect funds. It routes payments via your Stripe platform account so each event's organiser can be paid directly if you operate a multi-organiser site, or all funds flow to a single account if you do not.

1. In EP Events Settings, open **Stripe Connect**.
2. Click **Onboard with Stripe**.
3. Complete the Stripe Connect onboarding (business details, bank account, identity verification).
4. Return to the plugin and confirm the status reads **Connected**.

### EU VAT

For events sold to EU customers, the plugin handles VAT automatically:

- **B2C sales**: the destination country's standard VAT rate is applied at checkout.
- **B2B sales**: the buyer enters their VAT number. If VIES validates it, reverse-charge applies; the invoice records the buyer's VAT number and zero-rates the line.
- **Inclusive vs exclusive pricing** is configurable per site.

## Shortcodes

EP Events registers 17 shortcodes, grouped by purpose. The Shortcodes Reference panel inside Settings shows the full list with arguments.

### Listings (use on any page)

| Shortcode | What it does |
|---|---|
| `[events]` | Upcoming-events listing, paginated. Renders through EP Cards when present, falls back to a native grid. |
| `[event-calendar]` | Month/week/day/list calendar view of events. |

### Single event (use inside an Event content row)

| Shortcode | What it does |
|---|---|
| `[event-hero]` | Hero section with title, dates, location, hero image. |
| `[event-schedule]` | Schedule of talks, sessions, breaks. |
| `[event-speakers]` | Speaker grid for this event. |
| `[event-sponsors]` | Sponsor tiers and logos. |
| `[event-location]` | Map and address for physical events, virtual-meeting block for online. |
| `[event-faq]` | FAQ section configured per event. |
| `[event-register]` | Registration form with ticket selection, promo codes, payment plan toggle. |
| `[event-countdown]` | Live countdown to event start. |
| `[event-attendees-count]` | Live attendee count (with privacy threshold). |

### Buyer and organiser tools

| Shortcode | What it does |
|---|---|
| `[event-attendee-dashboard]` | "My tickets" view for logged-in buyers: download tickets, cancel, request refund-to-credit. |
| `[event-checkin]` | Organiser check-in screen with QR scanner, offline mode, attendee list. |
| `[event-speaker-portal]` | Token-gated self-serve portal for speakers to update their bio and headshot. |
| `[event-submit]` | Community event submission form (moderation required). |
| `[event-ics-feed]` | Renders a button or link to subscribe to the per-organiser ICS feed. |
| `[event-recap]` | Post-event recap block (highlights, photos, links). |

## The check-in PWA

When you place `[event-checkin]` on a page and pin that page to a phone or tablet at your venue, it becomes a Progressive Web App. The first time the page loads online, it pulls a snapshot of confirmed attendees into local storage. From then on:

- Scans are validated against the local snapshot, not against the server. The server is contacted only to record the check-in.
- If the network drops mid-event, scans queue locally. A status row at the top shows online/offline state and the pending-queue count.
- When the network returns (or the organiser hits **Sync now**), the queue drains and the server records each check-in with the original scan timestamp.
- The check-in audit trail records what time the scan actually happened, not what time the device caught up.

## Privacy and GDPR

When EP GDPR is active, EP Events contributes to data-subject requests via the sibling-plugin hook:

- **Export** surfaces the data subject's registrations, attendances, payment history, credits, consent log, lawful basis map, and retention policy.
- **Erasure** anonymises buyer PII (name, email, IP, user-agent) while retaining financial records (Stripe IDs, amounts) under HMRC's seven-year retention rule.
- **Retention**: IP, user-agent, and referrer data are purged at 90 days by a cron sweep.
- **Consent**: registration captures marketing-consent and GDPR-consent with UTC timestamps and a lawful basis map per PII field.

## Recovery panels

EP Events watches for two specific failure modes that can leave events rendering blank and surfaces a fix for each.

### Stripped Event template

If an admin removes blocks from the Event template via Admin > Theme > Editor and reduces it to just the body wrapper, every event renders blank. EP Events detects this state on admin page loads, snapshots the broken state, and re-clones the template from the Page template. A transparent banner in Settings explains what happened and offers a one-click revert.

If you land on a broken event page before any admin page (the auto-heal hasn't fired yet), an admin-only floating panel appears on the public event page offering **Restore template now**. Conservative threshold protects deliberately minimal custom templates from being touched.

### Empty event body

If an admin creates an event via Admin > Content > New Event (skipping the seeded body) or empties the body via the editor, the event will render blank. An admin-only floating panel surfaces on the public event page offering **Insert default layout**, which seeds the matching sub-type's editorial stack.

Non-admins never see either panel.

## Troubleshooting

**The Quick Start "Create your next event" link goes to a content type picker, not directly to the new-event form.**

That is intentional. PageMotor's admin content navigation uses POST forms for content-type selection, not GET URLs. From the picker, choose **Event** and click **Add New**.

**My event page is blank.**

If you're signed in as an admin, look for a yellow or rose-tinted floating panel at the bottom of the page. It will tell you which failure mode you've hit (empty body or stripped template) and offer a one-click fix. If you see no panel, confirm:

- The body has visible blocks. Open the event in Admin > Content > Events and check the body field is not empty.
- The Event template has chrome blocks. Open Admin > Theme > Editor and check the Event template's Body block has children (Header, Navigation, Content_Page, Footer at minimum).

**Reminder emails are not arriving.**

Check the cron status in Settings. Three triggers are configured:

- **Admin page load**: throttled to once per 60 seconds. If no admin has visited the site in over an hour, reminders may be delayed.
- **External endpoint**: `https://yoursite/?ep_events_cron=<your-secret>`. Wire this to a real cron service for reliable triggering.
- **Admin AJAX**: **Run cron now** button in Settings for manual ad-hoc runs.

The `pm_ep_events_email_sends` table records every send and dedupes future attempts, so triggering cron repeatedly is safe.

**Open Graph type on event pages is `article`, not `event`.**

A PageMotor core limitation. The `Open_Graph` plugin overrides per-record contributions for non-home pages. Event-specific titles, descriptions, hero images, and `event:start_time` flow correctly. A PM core patch will close this gap.

**Apple Wallet and Google Wallet passes are not generated.**

Deferred to a later release pending Apple cert provisioning. The plugin currently emits ICS attachments on every confirmation email, which covers iOS Calendar, Google Calendar, Outlook, and every other modern calendar app.

## Feedback

EP Events is in active development. Bug reports, feature requests, and notes on rough edges are welcome via the **Send feedback** link at the bottom of the plugin's settings page, or by emailing ElmsPark.

If your site uses a sibling plugin EP Events does not yet integrate with, let us know. The sibling-plugin valet pattern means most integrations are a single method on each side.
