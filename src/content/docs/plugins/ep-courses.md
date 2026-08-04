---
title: "EP Courses"
description: "Course and lesson management for PageMotor with enrolment, progress tracking, expiring links for paid video, and 24-language multilingual content support. Work in progress."
---

EP Courses is course and lesson management for PageMotor. Courses contain lessons, students enrol, their progress is tracked as they work through the material, and content can be translated into any of 24 languages including Welsh, Irish, and several South African languages.

Published by [ElmsPark Studio](https://elmspark.com).

## Status

**Work in progress** (version 0.4.12). The core structure is stable but some features are still being built. This guide describes what is currently shipping. Expect changes in subsequent versions.

## What EP Courses does

- **Course catalogue** with title, slug, description, learning outcomes, level (beginner / intermediate / advanced), price, status.
- **Lessons** attached to courses, with ordered sequence and translatable content.
- **Enrolment tracking** — which student is in which course.
- **Progress tracking** — which lessons has the student completed.
- **Multilingual content** — store title and body as JSON translations per course and per lesson.

## What EP Courses does NOT do (yet)

This plugin deliberately has a narrow scope. It does not:

- **Handle frontend student login** — that's [EP Membership](/plugins/ep-membership/)'s job.
- **Host videos**. Embed from YouTube, Vimeo, or an MP4 file you host yourself. If that file lives in your own S3-compatible bucket, [EP Media Storage](/plugins/ep-media-storage/) will serve it behind a link that expires.
- **Issue certificates** — not currently built in.
- **Run quizzes inside lessons** — not currently built in.

For a full learning management system, combine EP Courses with EP Membership (for login and access control) and EP Ecommerce Subscriptions (for paid course access).

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**

Optional but commonly paired:

- **EP Membership** for student accounts and authenticated course access.
- **EP Ecommerce Subscriptions** for paid enrolment.
- **[EP Media Storage](/plugins/ep-media-storage/)** to serve lesson videos from your own bucket behind expiring links.

## Installation

1. `ep-courses.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open the settings page and set the **viewer slug** (URL slug of the page that will host the lesson viewer).
4. Create a PageMotor page with that slug and add the `[ep-course-viewer]` shortcode to it.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[ep-courses]` | Course catalogue grid. Shows every active course with lesson count, duration, and whether it's free or paid. Links each course to its first lesson. |
| `[ep-course-viewer]` | Lesson viewer. Renders the current lesson with navigation to previous and next. Place on a single page — the viewer URL is shared across all lessons. |

## Database tables

- `{prefix}ep_courses` — course catalogue rows.
- `{prefix}ep_lessons` — lesson content with translations JSON.
- Enrolment and progress tables keyed to course ID and student ID.

## Multilingual content

Each course and lesson stores its title and body as a JSON map:

```json
{
  "en": { "title": "Introduction", "body": "..." },
  "cy": { "title": "Cyflwyniad", "body": "..." },
  "ga": { "title": "Réamhrá", "body": "..." }
}
```

The viewer picks the correct translation based on the active site language. Missing translations fall back to the site's default language.

The 24 supported languages are configured in settings. Welsh, Irish, Scots Gaelic, and multiple South African languages (Afrikaans, isiZulu, Xhosa, Sesotho) are supported alongside the usual European set.

## Typical setup flow

1. Create a course with title, description, outcome, level, and price.
2. Add lessons to the course. Each lesson has a title, body, and sort order.
3. (Optional) Enable translations on a course and add translated title / body per language.
4. Create a page with the viewer slug, add `[ep-course-viewer]`.
5. Create a catalogue page, add `[ep-courses]`.
6. If paid, configure EP Ecommerce Subscriptions to sell access to the course.
7. If gated, configure EP Membership to require login for the viewer page.

## Protecting paid video

Enrolment gates the lesson **page**. Until version 0.4.12 it did not gate the video **file**: the page carried the plain storage URL, so a student could copy that URL and pass it to anyone, and it kept working.

From 0.4.12, if [EP Media Storage](/plugins/ep-media-storage/) is installed and pointed at your bucket, an MP4 lesson is served through a link that expires instead, two hours by default. Nothing changes in EP Courses itself: set **Video Type** to MP4 and paste the bucket URL as before. Enrolment gating is unchanged, seeking still works, and a video already playing is not interrupted when its link expires.

Without EP Media Storage, or for a file hosted outside your bucket, the URL is emitted exactly as it always was. YouTube and Vimeo lessons are unaffected either way.

Worth being honest with your own students about what this is: expiring links stop a shared link from working later, which is how course content usually escapes. They do not stop somebody who is entitled to watch from saving the file while they watch it. No link scheme does.

## Troubleshooting

### “The course catalogue is empty”

Only **active** courses appear. Check your courses have status = Active, not Draft.

### “Clicking a course goes to a 404”

The viewer page must exist at the slug configured in **Settings → Viewer slug**, and that page must contain `[ep-course-viewer]`. Verify both.

### “Translations aren't appearing”

The viewer uses the active site language. Check your translation JSON has the exact language code your site uses (e.g. `en-GB` vs `en`). Missing translations fall back to the default language.

### “I want to restrict a course to paid subscribers only”

That's a job for EP Membership plus EP Ecommerce Subscriptions. Gate the viewer page's parent, or specific courses, via EP Membership's access rules.

### “Students can see lessons they haven't completed prerequisites for”

Prerequisite-based progression isn't built in yet. On the roadmap but not shipped. See the review queue.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
