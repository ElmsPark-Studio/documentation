---
title: "EP Host Check"
description: "Read-only host diagnostics for PageMotor. One admin panel scores what your hosting can and cannot do for PageMotor, green/amber/red, with a plain-English meaning and a plain fix for every check."
---

Roughly nine out of ten "PageMotor is broken" reports turn out to be the host quietly blocking something, not PageMotor. PHP cannot write the compiled CSS, outbound SMTP is blocked so email never sends, an upload limit is too low for a theme import. EP Host Check turns that guesswork into a clear report.

It is one admin panel that runs a battery of checks against the host your site is actually on, and gives you a plain-English green, amber or red result. Every line says what it means and how to fix it, written for a site owner, not a sysadmin. It is read-only: it diagnoses, it never changes a setting.

Published by [ElmsPark Studio](https://elmspark.com).

## The verdict

At the top of the report is a single overall verdict, taken from the worst result across every check:

- **Green, "This host runs PageMotor fully".** Every check passed. Nothing to do.
- **Amber, "This host has limits worth knowing".** PageMotor will run, but some items could cause confusion later. Worth a quick read.
- **Red, "This host will break PageMotor, fix or move".** One or more checks will cause real failures (saving designs, sending email, taking payments). Fix them with your host, or move to a VPS.

## What it checks

### Can PHP save PageMotor's files (the big one)

This replicates what PageMotor does when it compiles your design: it writes a temporary file into the active theme folder, reads it back, and deletes it, then does the same for the uploads and user-content folders. If any of them cannot be written, your design changes will appear to do nothing and uploads will fail. This single restriction is the most common cause of a "PageMotor is broken" report, and it is a host setting, not PageMotor.

### Capability checks

- **PHP version.** Fails below 8.1, warns on 8.1, passes on 8.2 and newer.
- **PHP extensions.** mysqli, curl, mbstring, json, openssl, and gd or imagick are required; zip is flagged as a warning (only needed for zip imports).
- **Blocked PHP functions.** Reads the `disable_functions` list. Fails if a file-write function or `curl_exec` is switched off; warns if only `fsockopen` is (that just affects the SMTP self-test).
- **open_basedir.** If a path restriction is set, confirms it includes your site's folders.

### Outbound connections

- **Outbound HTTPS.** A real short-timeout request to a stable endpoint. If it is blocked, Stripe payments, licence checks, AI features and web fonts all stop working.
- **Outbound mail (SMTP).** A short-timeout connection test to a known mail server on ports 587 and 465. It never sends anything. Many shared hosts block this, which presents as "PageMotor won't send email" when it is purely a host restriction.

### Resource limits and caching

- **Upload size** (`upload_max_filesize` and `post_max_size`), warned below ~64M.
- **PHP memory** (`memory_limit`), warned below 128M, with a note about SCSS-compile headroom.
- **PHP time limit** (`max_execution_time`), warned below 30 seconds.
- **Object cache** (Redis / Memcached): informational, never required.
- **PHP opcode cache** (opcache): on is faster; off is a gentle warning.

## Requirements

- **PageMotor 0.9 or later**
- **EP Suite base class** (bundled)

## Installation

1. Download `ep-host-check.zip` from the [EP Suite downloads page](https://updates.elmspark.com/download.php?plugin=ep-host-check). If you already run EP Suite plugins, it will also appear in your PageMotor admin under updates.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Host Check**. The report runs automatically.

## Using the report

1. Read the overall verdict at the top, then scan the rows. Each has a coloured dot, a plain meaning, and, for amber and red items, a prominent fix.
2. Act on the red items first (those break things), then the amber ones (those are limits worth knowing).
3. Use **Re-run checks** after you or your host changes a setting, to confirm the fix took.

## For developers and AI clients

EP Host Check exposes a `host-report` action over the PageMotor API and MCP. An MCP client (or the `/api/` endpoint) can read a host's status headlessly and reason about it, returning the same verdict and per-check data the panel shows. Useful for checking a fleet of sites, or for an AI agent diagnosing a deployment.

## What EP Host Check cannot do

- **Fix anything automatically.** It is read-only by design. It reports what it sees; the fixes are changes you or your host make.
- **See another server.** It runs on your host and reports what that host can do. It does not phone home and sends nothing anywhere.

## Built to run on broken hosts

The whole point of the plugin is to run on the hosts that block things, so it never fatals. Every probe is wrapped and every function is guarded. If your host has disabled `fsockopen`, that is reported as a finding, not a crash. Every temporary file it writes to test is cleaned up afterwards, even when a write is blocked.

## Privacy

Nothing leaves your server except the two outbound connection tests, which only check whether a connection can be opened (to a web endpoint over HTTPS, and to a mail server on 587/465). No data is sent in those tests, and no report is shared anywhere unless you choose to share it. No telemetry, no tracking.

## Troubleshooting

### "The write check is red but I'm sure the folder exists"

The folder existing is not the same as PHP being allowed to write to it. On many shared hosts the web user cannot write inside the site folder. The fix is a host permissions change, or moving to a VPS where PHP can write to its own site.

### "Outbound HTTPS or SMTP is red, but my site loads fine"

Inbound traffic (visitors reaching your site) and outbound traffic (your site reaching out to Stripe or a mail server) are different directions, controlled separately. A host can allow one and block the other. The report is about the outbound direction, which is what payments, licensing and external mail need.

### "Outbound mail shows amber on a shared host"

That is expected on many shared hosts: they block outbound SMTP. Use the host's own mail, or move external mail (such as Mailgun) to a VPS. See the [Mailgun email setup guide](/guides/mailgun-email/).

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on.

For anything bigger, a bug report, a feature request, or a "how do I..." that needs a real reply, open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply, usually within a few hours.
