---
title: "EP Testimonials"
description: "Collect and display customer testimonials on PageMotor. Star ratings, moderation, Schema.org Review markup, carousel or grid display."
sidebar:
  order: 55
---

EP Testimonials lets you collect customer testimonials through a form on your site, moderate them, and display approved testimonials in carousel, grid, or list layouts. Star ratings and Schema.org Review markup are included.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Submission form** for customers to leave testimonials.
- **Star rating** (1-5).
- **Photo upload** (optional) for the testifier's picture.
- **Moderation queue** — approve, reject, mark as spam.
- **Display shortcodes** — carousel, grid, single, or list.
- **Schema.org Review** structured data.
- **Import from CSV** for migrating existing testimonials.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Email** (for admin alerts on new submissions)
- **EP Suite base class**

## Installation

1. Install EP Email.
2. Download `ep-testimonials.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[testimonials-submit]` | Submission form for new testimonials. |
| `[testimonials]` | List/grid display of approved testimonials. |
| `[testimonials style=carousel]` | Rotating carousel. |
| `[testimonials style=grid columns=3]` | Grid layout. |
| `[testimonials limit=6]` | Only show 6. |
| `[testimonials featured=true]` | Only featured testimonials. |

## Collecting testimonials

Drop `[testimonials-submit]` on a page like `/leave-a-review/`. The form collects:

- Name
- Email (not displayed publicly)
- Company (optional)
- Testimonial text
- Star rating
- Photo (optional)

On submit, the testimonial queues for admin moderation.

## Moderation

From **Plugin Settings → EP Testimonials → Pending**:

- Review each submission.
- Approve, reject, or mark as spam.
- Optionally **feature** notable testimonials so they appear first.

An email notification fires to admin on each new submission (via EP Email).

## Display options

### Carousel

Rotating display, one testimonial at a time. Auto-advance or manual controls. Good for homepage hero areas.

### Grid

Multiple testimonials in columns. Good for dedicated testimonials pages.

### List

Stacked, one per row. Good for long-form reviews.

### Single

Show a specific testimonial by ID. For hero quotes or case-study page highlights.

## Schema.org

Each testimonial renders with `Review` schema plus an aggregate `AggregateRating` schema on pages with multiple testimonials. Google's rich result snippets can pick these up.

## Troubleshooting

### "Submission form shows but submissions don't arrive"

Check EP Email is configured. Without EP Email, admin notifications fail silently.

### "Photos don't appear"

Check the uploads directory has write permission. Also check file sizes — uploads over the PHP limit fail.

### "Carousel doesn't auto-advance"

Check browser console for JS errors. Also check the carousel has at least 2 testimonials — 1-item carousels don't rotate.

### "Testimonials appear but without star rating icons"

CSS might not be loading. Check the plugin's stylesheet is enqueued. Hard refresh to bypass cache.

### "Imported CSV assigns all testimonials to the wrong person"

CSV needs specific headers: `name,email,company,body,rating,featured`. Case-sensitive. Check your CSV.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
