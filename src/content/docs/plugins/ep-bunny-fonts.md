---
title: "EP Bunny Fonts"
description: "Retired. PageMotor 0.10 and later has Bunny Fonts delivery built into core — switch it on in Site Settings. This page remains for sites still running the plugin."
---

:::caution[Retired — now built into PageMotor]
**EP Bunny Fonts was retired on 22 July 2026.** PageMotor 0.10 and later includes the same GDPR-compliant font switch in core: open **Site Settings**, find **Google Fonts Delivery Service**, and select **Bunny Fonts**. That one setting swaps both the fonts API URL and the preconnect host site-wide — exactly what this plugin did.

The plugin is no longer distributed and no longer receives updates. Existing installs keep working, but the recommended path is to update PageMotor to 0.10 or later, use the core setting, and deactivate the plugin.
:::

EP Bunny Fonts replaced Google Fonts with Bunny Fonts on your site. Same fonts, same coverage, zero tracking. The swap happened server-side before any HTML reached the browser.

Published by [ElmsPark Studio](https://elmspark.com).

## Why the swap matters

The 2022 EU ruling on Google Fonts concluded that loading fonts from Google's CDN transmits the visitor's IP to Google, which is personal data under GDPR. Websites using Google Fonts without explicit consent have been sued.

[Bunny Fonts](https://fonts.bunny.net) is a drop-in GDPR-compliant mirror of the Google Fonts catalogue. Identical URL shape, identical fonts, hosted in the EU, zero tracking, no cookies.

This need has not gone away — it is simply served by PageMotor core now.

## If you're on PageMotor 0.10 or later

1. Open **Site Settings**.
2. Under **Google Fonts Delivery Service**, select **Bunny Fonts**.
3. Save, then reload your site. View source and search for the Google Fonts hostname — you should find nothing.
4. If the plugin is still installed, deactivate it. While active it forces Bunny delivery regardless of the core setting, which is harmless but makes the core selector misleading.

## If you're on PageMotor 0.9 or earlier

An existing install of the plugin keeps working as before: toggle **Enable Bunny Fonts** in **Plugin Settings → EP Bunny Fonts**. There will be no further updates, so plan to move to PageMotor 0.10+ and the core setting.

## Troubleshooting

### "Google Fonts URLs are still appearing in my page source"

A theme or plugin is hardcoding the Google Fonts hostname outside PageMotor's head pipeline (e.g. inline `<style>` with `@import`, or a plugin that echoes its own `<link>` directly). Find the culprit with a recursive grep for `googleapis` across `user-content/`, and patch the offending code to use `fonts.bunny.net` directly. Neither the core setting nor the plugin can swap URLs injected outside the head pipeline.

### "A specific font loads fine from Google but looks wrong on Bunny"

Bunny Fonts maintains parity with the Google catalogue, but occasionally lags on brand-new additions. If you hit a missing font, either use a close alternative, or self-host with `@fontsource/<family>` npm packages.

### "Is Bunny Fonts really GDPR-compliant?"

Bunny Fonts is operated by Bunny.net, a Slovenian company with EU-hosted infrastructure. No cookies, no tracking, no logs tied to identifiable users. Terms and DPA are on [fonts.bunny.net](https://fonts.bunny.net/). Read them and make your own judgement.

## Feedback and corrections

For anything this page doesn't answer — including help moving from the plugin to the core setting — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours.
