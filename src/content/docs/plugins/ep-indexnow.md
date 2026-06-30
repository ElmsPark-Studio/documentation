---
title: "EP IndexNow"
description: "Real-time URL submission to IndexNow. When a page changes, EP IndexNow tells Bing, Yandex, Seznam and Naver at once, and through Bing the AI search engines, so your changes are found in minutes instead of waiting for the next crawl."
---

EP IndexNow tells search engines the moment a page changes, instead of waiting for them to crawl back round. One submission to [IndexNow](https://www.indexnow.org/) reaches Bing, Yandex, Seznam and Naver, and because ChatGPT Search and Copilot lean on Bing's index (and Perplexity reads IndexNow directly), the same submission also reaches the Bing-powered AI search engines. Google does not take part, so it stays crawl-only via your sitemap.

It is the modern replacement for the retired sitemap-ping: Google removed its ping endpoint in 2023, and Bing's `bing.com/ping` now returns HTTP 410 Gone.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Real-time.** When content is published or updated, the changed URLs are submitted automatically.
- **One submission, many engines.** Bing, Yandex, Seznam, Naver, and the Bing-powered AI search engines, from a single POST.
- **Automatic or on demand.** With EP Cron active, changed URLs go out every 15 minutes. There is also a "Submit changed URLs now" button.
- **Indexable only.** Draft, protected, and `noindex` pages are never advertised to search engines.
- **Self-verifying.** EP IndexNow generates your key and serves the verification file for you.

## Requirements

- **PageMotor 0.7 or later.**
- **EP Suite base class.**
- **EP Cron** (optional, recommended) for automatic 15-minute submission. Without it, the manual button still works. See [EP Cron](/plugins/ep-cron/).

## Installation

1. Download `ep-indexnow.zip` from the [EP Suite downloads page](https://updates.elmspark.com/download.php?plugin=ep-indexnow).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **EP IndexNow** settings, tick **Enable real-time URL submission**, and save. Your key and verification file are generated on save.

## How it works

When enabled, EP IndexNow generates a 32-character key and serves it at `/<key>.txt` so search engines can verify you own the site. From then on it tracks the most recent change it has submitted (a cursor). On each run it gathers every live, indexable URL modified since then and sends them in one batch to IndexNow. The first run baselines the cursor to "now", so you never flood the engines with your whole site at once.

Protected content (members-only and the like) and `noindex` pages are filtered out using the same per-page rules your sitemap respects, so you never advertise a URL you would not want indexed.

## The dashboard panel

With [EP Dashboard](/plugins/ep-dashboard/) active, EP IndexNow adds an **IndexNow** panel to the Command Centre: a status pill (Active, Off, or a failure flag), the number of indexable pages changed since the last submission, how long ago it last ran, the auto-submit cadence, and the last result. A quick read on whether your changes are reaching the engines.

## Settings

- **Enable real-time URL submission.** The on/off switch. On save it generates the key and verification file.
- **Submit changed URLs now.** Sends everything changed since the last run, on demand. Useful for a one-off push after a batch of edits.
- **Regenerate key.** Issues a fresh key and re-baselines, in case a key is ever exposed.

## Troubleshooting

### "Automatic submission is off"

Automatic submission runs through EP Cron. Activate [EP Cron](/plugins/ep-cron/) and make sure its heartbeat is being called. Until then, the **Submit changed URLs now** button works on its own.

### "The last run shows an HTTP error"

IndexNow occasionally rate-limits or has a transient error. The next run retries automatically and nothing is lost, since the cursor only advances on a successful submission.

### "Does this submit to Google?"

No. Google does not participate in IndexNow, so it stays crawl-only via your sitemap. EP IndexNow covers the engines that do take part: Bing, Yandex, Seznam, Naver, and the Bing-powered AI search engines.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
