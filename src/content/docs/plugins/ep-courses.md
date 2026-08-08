---
title: "EP Courses"
description: "Course and lesson management for PageMotor with enrolment, progress tracking, expiring links for paid video, and 24-language multilingual content support. Work in progress."
---

EP Courses is course and lesson management for PageMotor. Courses contain lessons, students enrol, their progress is tracked as they work through the material, and content can be translated into any of 24 languages including Welsh, Irish, and several South African languages.

Published by [ElmsPark Studio](https://elmspark.com).

## Status

**Work in progress** (version 0.4.12). The core structure is stable but some features are still being built. This guide describes what is currently shipping. Expect changes in subsequent versions.

## What EP Courses does

- **Course catalogue** with title, slug, description, learning outcomes, level, price, status. **Level is the free / premium switch**, not a difficulty scale: the edit form offers **Free** and **Intermediate**, and only a Free course can be enrolled in today (see below).
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
- **Sell paid courses yet.** Any course whose level isn't Free renders in the catalogue as a **Premium Course** with a disabled "Coming Soon" button, and the enrol handler refuses it with "Paid courses are coming soon". Set the level to Free if you want students in a course today.

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
| `[ep-courses]` | Course catalogue grid. Shows every published course with lesson count, duration, and whether it's free or paid. Links each course to its first lesson. |
| `[ep-course-viewer]` | Lesson viewer. Renders the current lesson with navigation to previous and next. Place on a single page — the viewer URL is shared across all lessons. |

## Database tables

- `{prefix}ep_courses` — course catalogue rows.
- `{prefix}ep_lessons` — lesson content with translations JSON.
- Enrolment and progress tables keyed to course ID and student ID.

## Multilingual content

Each course and lesson stores its translations as a JSON map keyed by language **name**, exactly as the language appears in settings — not by language code:

```json
{
  "Welsh": { "title": "Cyflwyniad", "content": "...", "video_url": "..." },
  "Irish": { "title": "Réamhrá", "content": "...", "video_url": "..." }
}
```

Lessons translate title, content, and video URL (so each language can carry its own cut of the video). Courses translate title, description, and outcome. English isn't in the map: the English text lives on the course or lesson itself, and it is also the fallback wherever a translation is missing.

The language a student reads is stored on their **enrolment**, chosen at enrol time — the language of the catalogue they enrolled from — and the viewer renders every lesson in that language from then on. The catalogue's own language comes from the shortcode, `[ep-courses language="Welsh"]`, defaulting to the default language in settings. The site language plays no part.

The 24 supported languages are ticked on and off in settings. Welsh, Irish, Scots Gaelic, and a full set of South African languages (Afrikaans, isiZulu, isiXhosa, Sepedi, Setswana, Sesotho, Xitsonga, siSwati, Tshivenda, isiNdebele) are available alongside the usual European set.

## Typical setup flow

1. Create a course with title, description, outcome, level, and price.
2. Add lessons to the course. Each lesson has a title, body, and sort order.
3. (Optional) Tick the languages you need in settings, then fill in each language's fields in the **Translations** accordion on the course and lesson edit forms.
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

Only **published** courses appear. Check your courses have status = Published, not Draft.

### “Clicking a course goes to a 404”

The viewer page must exist at the slug configured in **Settings → Viewer slug**, and that page must contain `[ep-course-viewer]`. Verify both.

### “Translations aren't appearing”

The viewer renders the language stored on the student's **enrolment**, set when they enrolled — not the site language. Check the student enrolled from a catalogue in the right language, and that the translation keys are full language names exactly as they appear in settings (`Welsh`, not `cy`). Anything missing falls back to the untranslated English content.

### “I want to restrict a course to paid subscribers only”

That's a job for EP Membership plus EP Ecommerce Subscriptions. Gate the viewer page's parent, or specific courses, via EP Membership's access rules.

### “Students can see lessons they haven't completed prerequisites for”

Prerequisite-based progression isn't built in yet. On the roadmap but not shipped. See the review queue.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
