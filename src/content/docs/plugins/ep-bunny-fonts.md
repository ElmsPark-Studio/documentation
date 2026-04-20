---
title: "EP Bunny Fonts"
description: GDPR-compliant font delivery for PageMotor. Redirects Google Fonts requests to Bunny Fonts at the server level so visitor data never reaches Google.
sidebar:
  order: 12
---

EP Bunny Fonts replaces Google Fonts with Bunny Fonts on your site. Same fonts, same coverage, zero tracking. The swap happens server-side before any HTML reaches the browser, so you don't need to hunt through your theme and edit every font link by hand.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Why this matters: the 2022 EU ruling on Google Fonts concluded that loading fonts from Google's CDN transmits the visitor's IP to Google, which is personal data under GDPR. Websites using Google Fonts without explicit consent have been sued.

[Bunny Fonts](https://fonts.bunny.net) is a drop-in GDPR-compliant mirror of the Google Fonts catalogue. Identical URL shape, identical fonts, hosted in the EU, zero tracking, no cookies.

EP Bunny Fonts does the swap for you site-wide:

- Every reference to Google's Fonts API host becomes `fonts.bunny.net`.
- The `preconnect` link to Google's font-asset host becomes the Bunny Fonts equivalent.
- Font selector labels in the admin change from `(G)` (Google) to `(B)` (Bunny) so you can see the switch took effect.

No visitor data ever reaches Google servers.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class** (bundled)

## Installation

1. Download `ep-bunny-fonts.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Bunny Fonts**.
4. Toggle **Enable Bunny Fonts** on.
5. Reload your site. View source and search for the Google Fonts hostname — you should find nothing.

## Settings

- **Enable Bunny Fonts.** On/off toggle. Off makes the plugin inert so the swap stops happening, useful for debugging without uninstalling.

The settings page also shows a status dashboard with:

- Current font provider in use (should say "Bunny Fonts" when enabled).
- GDPR compliance status (green tick when Bunny is active).
- EP GDPR integration status (if EP GDPR is installed, shows the coordination).
- Count of available fonts in the catalogue.

## How the swap works

PageMotor emits font links via the standard theme head. EP Bunny Fonts registers a filter that runs after the head is built but before it is sent to the browser. The filter:

1. Searches the head output for the Google Fonts API host and replaces with `fonts.bunny.net`.
2. Searches for `preconnect` tags pointing to Google's font-asset host and swaps the host.
3. Returns the modified head.

This happens server-side. The browser never sees the Google URLs.

## Coordination with EP GDPR

If [EP GDPR](/plugins/ep-gdpr/) is installed, EP Bunny Fonts tells it that the site is compliant on the font front. This surfaces in EP GDPR's compliance dashboard as a green tick, so your overall GDPR status is easy to audit.

## Troubleshooting

### "Google Fonts URLs are still appearing in my page source"

A theme or plugin is hardcoding the Google Fonts hostname in a way that bypasses PageMotor's head pipeline (e.g. inline `<style>` with `@import`, or a plugin that echoes its own `<link>` directly). Find the culprit with a recursive grep for `googleapis` across `user-content/`, and patch the offending code to use `fonts.bunny.net` directly. EP Bunny Fonts cannot swap URLs that are injected outside the filter chain.

### "A specific font loads fine from Google but looks wrong on Bunny"

Bunny Fonts maintains parity with the Google catalogue, but occasionally lags on brand-new additions. If you hit a missing font, either use a close alternative, or self-host with `@fontsource/<family>` npm packages.

### "Is Bunny Fonts really GDPR-compliant?"

Bunny Fonts is operated by Bunny.net, a Slovenian company with EU-hosted infrastructure. No cookies, no tracking, no logs tied to identifiable users. Terms and DPA are on [fonts.bunny.net](https://fonts.bunny.net/). Read them and make your own judgement.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
