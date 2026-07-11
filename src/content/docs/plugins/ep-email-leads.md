---
title: "EP Email Leads"
description: "Turns EP Email contact-form submissions into a workable leads ledger with an always-current dashboard page. Keyed read-only endpoint, no cron, no page regeneration."
---

EP Email Leads is an extension for [EP Email](/plugins/ep-email/). It records every contact-form submission your site delivers into a server-side ledger, then serves that ledger to a self-contained dashboard page through a keyed, read-only endpoint. The ledger is the source of truth; the dashboard is a viewer that fetches fresh data on every load. There is no cron job, no template plumbing, and no page regeneration.

Published by [ElmsPark Studio](https://elmspark.com).

## The idea

A contact form that only sends email gives you an inbox, not a pipeline. EP Email Leads keeps the submission itself: who wrote, what they asked, when, and what happened next. Each lead carries a lane (`lead`, `spam`, `review`), a status (`new`, `open`, `closed`) and free-text notes, so the ledger doubles as a lightweight follow-up queue.

The dashboard page never goes stale and never needs rebuilding. It is a static, admin-gated page installed by the plugin; a small script inside it fetches the ledger anonymously with a read key each time the page opens and renders it in the browser. Freshness moves from publish-time to view-time.

## What gets captured

- Every **delivered** submission is stored as a lead (lane `lead`, status `new`). Name, email, company and message are extracted from the submitted fields, and the full field set is kept as JSON so nothing is lost.
- With **Capture blocked submissions** on, a submission blocked by another extension (for example [EP Email AI Triage](/plugins/ep-email-ai-triage/)) after it clears EP Email's own filters is kept in the `spam` lane, so a false positive can be rescued rather than lost.
- Submissions killed by EP Email's built-in spam stack (honeypot, time trap, content filter, gibberish filter, rate limit, IP blocklist) exit before any extension can observe them and are not captured.

Capture only observes. It never changes whether, or to whom, mail is sent.

## The dashboard page

One button on the settings screen installs the dashboard as a gated page on your own site (visible to logged-in admins only; anonymous visitors see nothing). It shows live counters, open leads as cards, and handled leads collapsed below, with a manual refresh button and the time of the last fetch. Reinstalling refreshes the page in place at the same address.

## Read keys

Access to the ledger is gated by named, 48-character read keys managed on the settings screen. Generate a key per consumer (the dashboard gets its own), rotate any key without touching the others, and revoke instantly. Rotating the dashboard key reinstalls the dashboard automatically.

Treat read keys as secrets: anyone holding a key can read the full lead ledger, including names and email addresses. Repeated requests with a wrong key are throttled per IP.

## The public read endpoint

`POST /` with `pm_ajax=EP_Email_Leads`, `action=get-leads-view`, `key=<48-hex read key>`, optional `limit` (default 100, max 200) and `status`. The endpoint is anonymous and keyed; send it with no credentials. It is strictly read-only and has no write surface.

Response shape:

```json
{"success": true, "data": {
  "leads": [{"uid": "…", "received": "…", "name": "…", "email": "…",
             "company": "…", "lane": "lead", "status": "new",
             "message": "…", "notes": ""}],
  "counts": {"new": 0, "open": 0, "closed": 0, "spam": 0, "last7days": 0, "total": 0},
  "generated_at": "2026-07-10T19:05:37Z"
}}
```

## API and MCP actions (admin tier)

The same actions are available to authenticated admin sessions and, through PageMotor's MCP surface, to AI agents you connect to your site:

- `list-leads` with `status` and `lane` filters, paginated.
- `update-lead` with `uid` plus any of `status`, `lane`, `notes`.
- `delete-lead` with `uid`. Permanent; provided for GDPR erasure.
- `leads-stats` returning the counts object.

The intended agent workflow: read new leads, research and route them, write findings back with `update-lead`. Outbound replies are always sent by a human.

## Privacy and retention

Leads are personal data. The ledger holds at most the configured retention cap (default 1000; oldest closed leads are pruned first), `delete-lead` gives you per-record erasure for GDPR requests, and nothing is ever sent off your server by this plugin.

## Requirements

- **PageMotor 0.10 or later**
- **EP Email 1.10.36 or later** (required; this is an EP Email extension)
- **EP Suite base class** (bundled)

## Installation

1. Install and configure **EP Email** first.
2. `ep-email-leads.zip` comes with an EP Suite licence, supplied directly by ElmsPark (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Open **Plugin Settings → EP Email Leads**, generate a read key, and press **Install dashboard page**.

From that point every delivered submission lands in the ledger and the dashboard shows it on next load.

## Changelog

### 0.1.0

Initial release: leads ledger, capture via EP Email's extension hooks, named rotatable read keys, keyed read-only `get-leads-view` endpoint, self-installing gated dashboard page, admin API and MCP actions (`list-leads`, `update-lead`, `delete-lead`, `leads-stats`).
