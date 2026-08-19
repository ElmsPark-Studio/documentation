---
title: "EP Attribution"
description: "Adds a small \"Built on PageMotor. Designed by ElmsPark.\" credit line to your site footer. One toggle, works on standard themes and bespoke designs alike."
---

EP Attribution adds a small credit line to the footer of every page on your site:

> Built on [PageMotor](https://pagemotor.com). Designed by [ElmsPark](https://elmspark.com).

It is one toggle, it styles itself to suit your theme, and it works whether your site uses a standard PageMotor footer or a bespoke design with no footer at all.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **One setting.** A single checkbox turns the credit line on or off sitewide.
- **Theme-agnostic placement.** Appends into your site's own footer where there is one, or renders a slim strip at the foot of the page where there is not.
- **Adapts to your design.** The stylesheet inherits your theme's text colour and sits at low opacity, so it reads correctly on light and dark backgrounds without configuration.
- **On by default.** Ticked once on first activation so the credit appears immediately. Unticking it is respected permanently.
- **No tracking.** The plugin renders two links and nothing else. No cookies, no analytics, no external requests.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class** (bundled)

## Installation

1. Download `ep-attribution.zip` from the [EP Suite downloads page](https://updates.elmspark.com/download.php?plugin=ep-attribution).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Load any page on your site and scroll to the bottom. The credit line should be there.

The credit is switched on the moment you activate the plugin, so there is no third step.

## Settings

Everything lives under **Footer Credit**:

- **Show the credit line.** Tick to display the credit sitewide, untick to hide it. That is the whole plugin.

The settings screen also shows a small status panel telling you whether the credit is currently showing or hidden, and which two sites it links to.

### Turning it off permanently

The box is ticked once, automatically, the first time the plugin activates. After that your choice wins: if you untick it, it stays unticked. Deactivating or reactivating the plugin will not silently switch it back on.

## Where the credit appears

PageMotor has no server-side "sitewide footer" hook, because footers are theme instances rather than a single global template. EP Attribution therefore places the credit in the browser, just before the end of the page, which is what lets one toggle cover every site regardless of theme.

It looks for your site's footer and picks the **last visible** one on the page. That matters on sites where individual articles have their own `<footer>` element: the credit lands in the site footer at the bottom, not inside the last article.

- **Standard themes** render a footer, so the credit is appended inside it and inherits its spacing and colour.
- **Bespoke designs** often hide or omit the footer entirely. When no visible footer is found, the credit renders instead as a standalone strip at the foot of the page.

Because the credit is added in the browser, it will not appear in the page's initial HTML source, and it will not appear at all for visitors browsing with JavaScript disabled.

## Troubleshooting

### "The credit line does not appear"

Check the box is ticked under **Footer Credit** first. If it is, open your browser's developer console and look for a JavaScript error from another plugin or theme script. The credit is injected by a small script at the end of the page, so an unrelated script that throws earlier can stop it running.

Also confirm you are looking at a normal page rather than the admin, and that you are not viewing a cached copy.

### "It appears inside an article instead of at the bottom of the page"

The plugin targets the last visible `footer` or `#footer` on the page. If an article footer is rendering after the site footer, or the site footer is hidden, the article footer becomes the last visible one. Either make the site footer visible, or hide the trailing article footer.

### "It appears as a strip rather than inside my footer"

That is the fallback, and it means no visible footer was found. Usually the theme hides `#footer` with `display: none` or does not render one. This is expected on bespoke designs and needs no fix unless you would rather place it yourself.

### "I unticked it but it is still showing"

The setting takes effect on the next page load, so refresh. If it persists, you are almost certainly seeing a cached page: clear your browser cache, and any server-side or CDN cache in front of the site.

### "The text is hard to read against my footer"

The stylesheet deliberately inherits the surrounding text colour at reduced opacity rather than hardcoding a colour. If your footer sets an unusual colour, or sets none at all, add a rule for `#ep-attribution` in your theme CSS to override it.

### "It disappeared after a theme change"

Nothing to reconfigure. The placement is decided per page load, so a new theme simply changes whether the credit lands inside a footer or as a standalone strip. If it vanished entirely, check the plugin is still active on the new theme.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
