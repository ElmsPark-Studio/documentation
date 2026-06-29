---
title: "EP YouTube"
description: "GDPR-friendly YouTube embeds for PageMotor. Click-to-load thumbnails so no Google cookies fire on page load, no-cookie iframe host by default, optional thumbnail self-hosting."
---

EP YouTube embeds YouTube videos on your PageMotor site without the privacy and performance costs of a plain `<iframe>`. The visitor sees a lightweight thumbnail. YouTube only loads when they click play.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

PageMotor's built-in oEmbed renders a YouTube `<iframe>` immediately when the page loads. That:

- Drops YouTube cookies in the visitor's browser before they've decided to watch anything.
- Ships ~600KB of YouTube player JavaScript per video on the page.
- Tanks Lighthouse scores on any page with more than one video.
- Pings `i.ytimg.com` (a Google CDN) for the player poster image.

EP YouTube replaces all of that with a thumbnail placeholder. The heavy iframe is only built when the visitor clicks play, and on that click the iframe loads from `youtube-nocookie.com` so YouTube does not store tracking cookies unless the visitor actually interacts with the player.

Optional: enable Self-Host Thumbnails to download each video's thumbnail to your own server on first pageview. After that, no request to Google ever happens until the visitor clicks play.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class** (bundled)

## Installation

1. Download `ep-youtube.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP YouTube**.
4. Defaults are sensible. No-Cookie Mode is on, default aspect ratio is 16:9, default thumbnail resolution is Standard. Most sites need nothing else.
5. Insert your first video by adding `[youtube id="dQw4w9WgXcQ"]` to any page or post.

## Use

The shortcode accepts a bare YouTube ID, a `youtu.be/` link, a `youtube.com/watch?v=` URL, an `/embed/` URL, or a `/shorts/` URL — paste whichever you have.

```text
[youtube id="dQw4w9WgXcQ"]
[youtube id="https://youtu.be/dQw4w9WgXcQ"]
[youtube id="https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
```

All four forms produce the same output.

### Optional attributes

| Attribute | Example | Effect |
|---|---|---|
| `title` | `title="A Day on the Lake"` | Heading overlay on the thumbnail, gradient-down to clear, line-clamped to 2 lines. Matches YouTube's idle-state title bar so the visitor has context before clicking play. |
| `aspect` | `aspect="4:3"` | Override the default aspect ratio. Accepts `16:9`, `4:3`, `1:1`, `21:9`, `9:16`, or any `WIDTH:HEIGHT`. |
| `thumb` | `thumb="https://example.com/poster.jpg"` | Use your own thumbnail image instead of YouTube's. |
| `alt` | `alt="Demo of the new feature"` | Alt text for the thumbnail image. |
| `params` | `params="start=30&end=120"` | Extra YouTube player parameters appended to the iframe URL. Use ampersand-separated `key=value` pairs. |
| `class` | `class="extend"` | Extra CSS class on the `.youtube` container, for skin "break out" or other layout hooks. |
| `wrap` | `wrap="container"` | Wrap the video in an outer `<div>` with this class. |

## Settings

- **Default Aspect Ratio.** Used when the shortcode does not specify an `aspect` attribute. 16:9 by default. The plugin supports 16:9, 4:3, 1:1, 21:9, and 9:16 (vertical / Shorts).
- **Default Thumbnail Resolution.** YouTube serves thumbnails at three tiers. **Standard** (`sddefault.jpg`) is always available and works for every video. **High Quality** (`hqdefault.jpg`) is slightly sharper. **Maximum** (`maxresdefault.jpg`) is the sharpest but is missing for many older or custom-thumbnail videos — if your thumbnails go blank, drop back to Standard.
- **No-Cookie Mode** (on by default). Loads the player iframe from `youtube-nocookie.com` instead of `youtube.com`. YouTube does not store tracking cookies after the visitor clicks play, unless they interact with the player itself. Recommended.
- **Self-Host Thumbnails** (off by default). Downloads each video's thumbnail to `user-content/ep-youtube-thumbs/` on first pageview, so subsequent visitors only ever see your domain in their network tab until they click play. Adds about 10–50KB of storage per cached video. Best for sites where you want zero Google requests even on the idle pageview state.

## How the lazy-load works

The shortcode renders a `<div class="youtube" data-embed="VIDEO_ID">` placeholder, plus a play-button arrow and optionally a title overlay. The plugin's sitewide JavaScript paints a thumbnail into the placeholder (from YouTube's CDN, your custom URL, or your self-hosted cache).

When the visitor clicks anywhere on the placeholder, the JS builds the YouTube iframe with `autoplay=1`, swaps it in for the placeholder contents, and the video starts playing immediately. One click — same as a default YouTube embed — but no cookies and no heavy assets until the click happens.

## Title overlay vs autoplay

YouTube's own iframe shows a title bar over the poster when the player is idle (before play). EP YouTube uses `autoplay=1` on click, which skips that idle state, so YouTube's title bar never appears. To restore the title context, use the `title` shortcode attribute:

```text
[youtube id="qIQReeJoAWY" title="A Day on the Lake"]
```

This paints your own heading overlay on the thumbnail with the same gradient-down-to-clear styling YouTube uses, line-clamped to 2 lines so long titles don't overrun. The overlay is removed when the iframe takes over.

## Backwards compatibility

If you've ported a Thesis/Focus site to PageMotor and the original Thesis YouTube Box markup is still in your content (`<div class="youtube" data-embed="...">`), EP YouTube's frontend JavaScript picks those up and lazy-loads them too. No content rewrite required.

This is how a number of ElmsPark migrations have brought across YouTube videos from Thesis without touching the post HTML.

## Coordination with EP GDPR

EP YouTube is GDPR-compliant on its own. The visitor's click on the thumbnail is itself an act of explicit consent under GDPR, so no separate cookie-banner gate is required for the iframe.

If [EP GDPR](/plugins/ep-gdpr/) is also installed, the two plugins agree on the privacy story. The privacy policy generated by EP GDPR can mention the EP YouTube no-cookie default, and the site's overall compliance dashboard reflects the embed setup.

## Troubleshooting

### “My thumbnail is blank”

YouTube doesn't have a `maxresdefault.jpg` for every video — particularly older uploads or videos with non-default custom thumbnails. If you've set Default Thumbnail Resolution to Maximum, try dropping back to Standard. The JS also auto-falls-back from Max to Standard on image-load error.

### “The video is playing but there's no title shown”

EP YouTube's autoplay-on-click flow skips YouTube's idle-state title overlay. Use the `title` shortcode attribute to paint your own heading over the thumbnail before click.

### “I want the YouTube branding visible”

The `params` shortcode attribute is passed through to the iframe URL. To re-enable YouTube branding, pass `params="modestbranding=0"`. To show related videos on the end screen, omit the default `rel=0` — actually you can't, but you can override with `params` if you have a specific need.

### “How do I match my old `<iframe>` embeds for the visual diff?”

Add the `title` attribute to match the heading overlay a vanilla YouTube iframe shows in its idle state. The poster image will be the same since both pull from `i.ytimg.com`. The difference: yours loads YouTube on every pageview, EP YouTube only loads it after the click.

## Credit

The lazy-load mechanism is inspired by Chris Pearson's [Thesis YouTube Box](https://diythemes.com/thesis/rtfm/boxes/youtube/) (DIYthemes, GPL v3.0, 2019). EP YouTube is a clean-room PageMotor implementation with the same architecture plus two privacy upgrades: the `youtube-nocookie.com` iframe host by default, and the optional thumbnail self-hosting.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
