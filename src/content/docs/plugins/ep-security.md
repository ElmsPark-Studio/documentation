---
title: "EP Security"
description: "Scaffold release. EP Security 0.0.3 installs its database surface and settings page only — no firewall enforcement, no log ingestion, no AI explanations and no two-factor gating are active yet."
---

:::danger[This release does not protect your site]
EP Security 0.0.3 is a **scaffold**. It installs its database tables and renders its settings page, and that is all it does. There is no firewall enforcement, no log ingestion, no AI explanation of events, and no two-factor gating. Every control on the settings page is a placeholder: nothing in the plugin reads them yet.

Installing it does not make your site safer, and its settings being switched on does not mean anything is switched on. Do not count it as one of your protections.
:::

EP Security is the intended home for AI-era security on PageMotor: web-server firewall management, log-driven attack detection, plain-English explanation of security events, and two-factor gating on sensitive admin actions. This page documents what has actually shipped, which today is the groundwork for those features rather than the features.

Published by [ElmsPark Studio](https://elmspark.com).

## Why it shipped in this state

The remaining work depends on things outside the plugin: a PageMotor core `api()` valet method that has not shipped, and an open question about how far the login flow can be extended. Rather than sit unversioned, the database surface and the settings shape went out first so they are stable when the behaviour lands.

That is a reasonable engineering decision and a dangerous documentation one, which is why the warning above is the first thing on this page.

## What is actually present in 0.0.3

- The plugin's database tables.
- A settings page whose controls render correctly.
- Nothing that reads those controls.

The settings you can see, none of which currently do anything, cover detection (login path, lockout threshold, lookback window), firewall rules and enforcement mode, two-factor enrolment and gate window, log ingestion interval, and AI explanations including model choice. Treat the list as a statement of intent about where the plugin is going.

## Requirements

- **PageMotor 0.8.3 or later**
- **EP Suite base class** (bundled with the plugin)

## Installation

There is no reason to install 0.0.3 on a production site. If you are tracking the plugin's development:

1. `ep-security.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Security**.

## What to use in the meantime

Nothing here replaces the basics. Keep your PageMotor core current, keep admin accounts few and their passwords strong, and use [EP Host Check](/plugins/ep-host-check/) to confirm your hosting is not undermining you. For sign-in hardening today, [EP Passkeys](/plugins/ep-passkeys/) is a shipped, working plugin; EP Security's two-factor gating is not.

## Changelog

### 0.0.3

Fixes six settings toggles that never rendered. Each was declared as a checkbox with no `options` array, and PageMotor's form builder silently emits an empty wrapper for a field type it cannot match, so the controls were invisible rather than broken-looking.

The toggles are still not wired to anything. Making them visible made the declarations correct for when the features land; it did not make them functional.
