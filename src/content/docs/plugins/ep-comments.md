---
title: "EP Comments"
description: Comment system for PageMotor with moderation, threaded replies, spam protection, Gravatar avatars, and WordPress comment import.
sidebar:
  order: 14
---

EP Comments is a proper comment system for PageMotor. Database-backed, admin moderation queue, threaded replies with email notifications, spam protection via honeypot and rate limiting, Gravatar avatars, and a WordPress-to-PageMotor comment import path.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Comments attach to pages via a shortcode. Each page has a content-options toggle to enable or disable comments on that specific page, so you can let readers comment on blog posts but not on sales pages.

Features:

- **Threaded replies.** Reply to a comment and the parent commenter gets an email.
- **Moderation queue.** New comments start as pending by default. Admin reviews, approves, or rejects.
- **Auto-approve** option for sites where moderation is overkill, plus **trusted returning commenters** detection so regulars don't queue every time.
- **Honeypot spam protection** on the form.
- **IP-based rate limiting** with a configurable interval.
- **CSRF protection** via double-submit cookie.
- **Gravatars** with initial-based fallback for commenters without one.
- **Schema.org DiscussionForumPosting** structured data for SEO.
- **WordPress comment import** from JSON so you can bring years of discussion across.
- **Auto-close** comments on posts older than N days.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class** (bundled)
- **EP Email** (optional but recommended for styled notification emails; without it, the plugin falls back to PHP's `mail()`)

## Installation

1. Download `ep-comments.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Drop the `[comments]` shortcode on any page where you want comments.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[comments]` | Full comment list for the current page, plus the submission form. |
| `[comment-form]` | Form only, no list. Useful if you want the form above the list (default is below). |

## Per-page comment toggle

On any page's content options:

- **Enable comments.** Checkbox. Default can be set globally; this overrides per page.

Pages without comments enabled won't render the `[comments]` shortcode, even if the shortcode is present in the content.

## Settings reference

Accessed through **EP Suite nav → Comments**.

| Setting | Purpose |
|---|---|
| **Admin notification email** | Where admin-alert emails go when new comments are submitted. |
| **Auto-approve** | On: comments appear immediately without moderation. Off: comments queue for admin review. |
| **Trusted returning commenter detection** | When a commenter has N previously-approved comments under the same email, subsequent comments auto-approve even if global auto-approve is off. |
| **Honeypot** | On by default. Adds a hidden form field that bots fill but humans don't. Submissions with the honeypot populated are rejected silently. |
| **Rate limit interval** | Seconds between comments from the same IP. Default 60. |
| **Comments per page** | Pagination size. Default 20. |
| **Display order** | Newest first or oldest first. |
| **Auto-close after N days** | Locks comments on pages older than this. |

## Moderation dashboard

The admin dashboard lists every comment with:

- Filtering by status (Pending / Approved / Spam / Trash).
- Search by commenter name, email, or body text.
- Pagination.
- Bulk actions: approve, unapprove, mark as spam, trash, delete permanently.

Clicking a comment shows full context including the commenter's history on your site.

## How replies work

A commenter clicks **Reply** under any approved comment. Their reply is submitted with a `parent_id` reference. When approved:

- The reply is rendered nested under its parent in the comment list.
- The parent commenter gets an email notification telling them their comment was replied to, with a link back to the page.

## Spam protection layers

Three layers, applied in order:

1. **Honeypot.** If the hidden field has a value, the submission is rejected. Most bots fill every field.
2. **Rate limit.** Same IP cannot post faster than the configured interval.
3. **CSRF via double-submit cookie.** Cross-site forms posting to your comments endpoint are rejected.

Bots that pass all three are rare. If you see any that do, they go through moderation (unless auto-approve is on) so no damage is done.

## Gravatars

The plugin looks up each commenter's email against Gravatar. If they have one, their avatar renders next to their comment. If they don't, a coloured initial-letter circle renders instead (based on the first letter of their name, with a deterministic background colour).

## WordPress comment import

From the settings page:

1. Export your WordPress comments to JSON via a tool like WP All Export.
2. Paste or upload the JSON into EP Comments' import panel.
3. Review the preview, click Import.

Imported comments are stamped with an `import_batch_id`. If something goes wrong, you can delete every comment from a specific import in one operation via the Import History panel.

## Troubleshooting

### "Comments don't appear on any page"

Check the page has **Enable comments** ticked in its content options, and that the `[comments]` shortcode is actually in the page body.

### "Admin notifications aren't arriving"

Install and configure EP Email. The plugin's own `mail()` fallback often fails on modern hosts because raw PHP `mail()` is blocked or spam-filtered. EP Email with proper SMTP fixes this.

### "Commenter got a reply notification for a reply to their own comment"

That's the design — someone replied to their comment, they should know. If you don't want that for some category of replies, the feature request can go in the review queue.

### "All new comments are queuing as pending even though I turned auto-approve on"

Check the global auto-approve setting saved correctly. Also check the trusted-returning-commenter threshold is 0 or low; if it's high, first-timers still queue.

### "A specific commenter keeps being marked as pending despite being trusted"

They may be submitting from different email addresses or different IPs. Trust is tied to email + approved history. Same commenter with three emails has three trust records.

### "Spam is still getting through"

Drop the rate limit to 120 or 300 seconds. Investigate specific IPs with the moderation dashboard's IP filter and block persistent offenders at the nginx or Cloudflare level.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
