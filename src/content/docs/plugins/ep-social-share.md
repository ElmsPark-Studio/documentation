---
title: "EP Social Share"
description: Privacy-friendly share buttons for X/Twitter, Facebook, LinkedIn, and email. No tracking scripts, no cookies, just URL-based share links.
sidebar:
  order: 53
---

EP Social Share adds share buttons for X/Twitter, Facebook, LinkedIn, and email. No tracking scripts, no iframes, no cookies, no external SDK — just URL-based share links and SVG icons that visitors can click to share the current page.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Every social network has a share URL pattern. You hit that URL with the page title and URL as query parameters, they handle the rest. EP Social Share just generates those URLs, wraps them in styled buttons, and drops into any page via a shortcode.

What it avoids:

- **Official share SDKs** (Facebook, Twitter, LinkedIn all offer JavaScript buttons). Those come with trackers, cookies, and third-party privacy concerns.
- **External CSS/JS**. EP Social Share is all local CSS and inline SVG.
- **GDPR consent complications.** No visitor data leaves your site until they click.

## Supported networks

- **X / Twitter** (uses `twitter.com/intent/tweet`).
- **Facebook** (uses `facebook.com/sharer/sharer.php`).
- **LinkedIn** (uses `linkedin.com/sharing/share-offsite`).
- **Email** (uses `mailto:` with prefilled subject and body).

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class**

## Installation

1. Download `ep-social-share.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Add `[ep-social-share]` to any page or template.

## Shortcode

```text
[ep-social-share]
[ep-social-share networks=x,linkedin,email]
[ep-social-share style=icons]
[ep-social-share style=buttons]
```

Attributes:

| Attribute | Values | Default | Purpose |
|---|---|---|---|
| `networks` | Comma list of `x, facebook, linkedin, email` | all | Which networks to show. |
| `style` | `icons`, `buttons`, `inline` | `icons` | Visual style. |
| `size` | `small`, `medium`, `large` | `medium` | Icon size. |
| `label` | `true`, `false` | depends on style | Whether to show network names alongside icons. |

## Settings

- **Default networks.** Which networks are shown when the shortcode has no `networks` attribute.
- **Button colours.** Either brand colours (network-specific) or a custom single-colour scheme.
- **Show counts.** Off by default (counts require tracking pixels which this plugin avoids on principle).

## Troubleshooting

### "The share pops open but shows the wrong title or URL"

Share URLs are populated from the current page's metadata. If your Open Graph tags are wrong, the share uses the wrong values. Install [EP SEO](/plugins/ep-seo/) and configure Open Graph properly.

### "Facebook share shows generic preview instead of my image"

Facebook caches preview data. Force refresh via [Facebook's Sharing Debugger](https://developers.facebook.com/tools/debug/).

### "Sharers complain no image is appearing in the preview"

Your page needs an `og:image` meta tag pointing to an accessible image. EP SEO handles this; check your EP SEO config.

### "I want to add a network not listed"

Shortcode attributes are fixed to the four supported networks. Pinterest, Reddit, WhatsApp, Telegram — feature request in the review queue.

### "The icons look wrong on my theme"

CSS specificity might be overriding. Inspect the `.ep-social-share` elements in dev tools and adjust your theme's styles.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
