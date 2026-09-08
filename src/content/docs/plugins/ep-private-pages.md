---
title: "EP Private Pages"
description: "Passwordless private pages. An unlisted URL serves an email and one-time code gate, then a hub of draft HTML documents served verbatim. Allowlist controlled, noindexed everywhere, never public."
---

EP Private Pages gives you a place to put documents that are not for the public and not for search engines, without building a login system for them. You share one unlisted URL. Whoever opens it enters their email address, gets a one-time code, and lands on a hub of your documents. Anyone not on the allowlist gets nowhere.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **No passwords, no accounts.** The reader enters an email and a one-time code arrives. Nothing to remember, nothing to reset, nothing for you to administer.
- **Allowlist controlled.** Only the addresses you name can get in. Everyone else sees the gate and stops there.
- **Never public, by construction.** Pages are noindexed, they never go live, and they never reach your sitemap or IndexNow. There is no state in which one of these documents becomes a public page by accident.
- **Documents served verbatim.** Drop in HTML and it is served as written, so a document you designed elsewhere arrives looking exactly as you built it.

## Requirements

- **PageMotor 0.10 or later.**
- **A working email transport** so the one-time codes actually arrive. [EP Email](/plugins/ep-email/) with a real transport driver is the usual answer; codes sent through PHP `mail()` frequently land in spam, which reads to your reader as the gate being broken.

## Installation

1. Download `ep-private-pages.zip` from your ElmsPark account.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Add the email addresses that should have access.
4. Add your documents, and share the unlisted hub URL with those people.

## How the gate works

1. Someone opens the unlisted hub URL.
2. They are asked for an email address.
3. If that address is on your allowlist, a one-time code is emailed to it. If it is not, they are told nothing useful, so the allowlist is not something an outsider can probe.
4. The code lets them into the hub, where your documents are listed.

The unlisted URL on its own is not the security boundary; the allowlist is. Sharing the URL more widely than you intended does not expose anything.

## When to use it

Good for a report for one client, a plan circulated to two colleagues, board papers, draft work you want a specific person to read and nobody else to find. It suits documents with a small, named readership.

It is not a membership system and not a paywall. If you want tiers, self sign-up, or payment, you want [EP Membership](/plugins/ep-membership/) instead.

## Support

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on.

For anything bigger, open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours.

## Changelog

### 1.0.6

**This plugin can now be updated.** It had no update header, so every update check your site ran skipped it silently: no error, no warning, just permanently absent from the Updates screen. It has one now, and a row on the ElmsPark update channel, so future releases reach you the same way every other EP plugin does.

No change to what the plugin does. Your private pages behave exactly as before.

### 1.0.5

Passwordless private pages: an unlisted URL serves an email and one-time code gate, then a hub of draft HTML documents served verbatim. Allowlist controlled, noindexed everywhere, nothing ever goes live or reaches sitemaps or IndexNow.
