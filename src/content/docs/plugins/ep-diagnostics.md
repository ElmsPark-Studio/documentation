---
title: "EP Diagnostics"
description: "System diagnostics and environment report for PageMotor. One-click copy of your PHP/MySQL/server details plus active plugins, for sharing in support requests."
sidebar:
  order: 17
---

EP Diagnostics is a single-purpose plugin: it generates a full report of your server environment, installed plugins, and client browser, and lets you copy the whole thing to your clipboard as plain text. When you contact support, paste the report into the email. No more "what PHP version are you on again?"

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

What the report includes:

### PageMotor

- Version number and beta status (e.g. "0.8b").
- Active frontend theme with version.
- Active admin theme with version.

### EP Suite inventory

- Every installed EP plugin with its class name, version, and whether it's currently active.
- Every non-EP plugin alongside, so support can see if something third-party might be interfering.

### Server environment

- PHP version and SAPI (fpm, cgi, cli).
- MySQL / MariaDB version.
- Server software (nginx, Apache, LiteSpeed).
- Operating system.
- Upload limits: `upload_max_filesize`, `post_max_size`.
- Memory limit.
- Max execution time.

### PHP extension checks

Ticks and crosses for the extensions most EP plugins need:

- `curl` — outbound HTTP
- `openssl` — SSL, encryption, JWT
- `mbstring` — multibyte string handling
- `json` — obvious
- `mysqli` — database
- `fileinfo` — MIME detection for uploads

A red cross next to any of these is almost always the cause of a plugin not working.

### Client side (browser)

JavaScript probes and reports:

- Browser name and version.
- Operating system.
- Screen resolution.
- Viewport size.

Useful when a bug might be browser-specific.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class** (bundled)

## Installation

1. Download `ep-diagnostics.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Diagnostics**. The report is already there.

## Using the report

1. Scroll through and check the red/green indicators. Any red is a potential issue worth fixing before it becomes the cause of your support ticket.
2. Click **Copy report to clipboard**.
3. Paste into your support email, the community forum, or an issue on [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).

The report is plain text, formatted for readability. No markdown, no HTML — just key/value pairs and section headers.

## What EP Diagnostics cannot do

- **Fix issues automatically.** The plugin is read-only. It reports what it sees; fixes are manual.
- **Remote diagnostics.** It runs on your server and reports what that server sees. It doesn't phone home, doesn't send data anywhere, doesn't share anything without your explicit copy-paste.

## Privacy

Nothing leaves your server unless you choose to share the report. No telemetry, no usage tracking, no analytics. The report is generated on-demand when you open the settings page.

## Troubleshooting

### "Copy to clipboard doesn't work"

Browser permissions on clipboard have tightened. Some browsers only allow clipboard writes on user-initiated clicks. If your browser blocks it, select the text manually and Cmd/Ctrl+C.

### "The report says an extension is missing but I installed it"

The extension needs to be enabled for the SAPI PHP is running under (usually `fpm` for web). Check `/etc/php/8.2/fpm/conf.d/` for the extension's `.ini` file. Reload PHP-FPM after adding it.

### "The report doesn't see my custom plugin"

The plugin must be in `user-content/plugins/` and activated in the active theme to appear. Inactive plugins are listed separately with their status greyed out.

### "I want to share the report but it contains information I'd rather not make public"

The report is deliberately information-dense for support purposes. It doesn't contain credentials or personal data, but it does reveal your server software and versions. If you're pasting into a public forum, skim first and redact anything you're uncomfortable sharing.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
