---
title: "EP Courses"
description: "Course and lesson management for PageMotor with enrolment, card payments through Stripe, progress tracking, expiring links for paid video, and 24-language multilingual content support. Work in progress."
---

EP Courses is course and lesson management for PageMotor. Courses contain lessons, students enrol, their progress is tracked as they work through the material, and content can be translated into any of 24 languages including Welsh, Irish, and several South African languages.

Published by [ElmsPark Studio](https://elmspark.com).

## Status

**Work in progress** (version 0.5.0). The core structure is stable but some features are still being built. This guide describes what is currently shipping. Expect changes in subsequent versions.

## What EP Courses does

- **Course catalogue** with title, slug, description, learning outcomes, access, price, status. **Access is the free / premium switch**: the edit form offers **Free** and **Premium**. A Free course is joined with one click; a Premium course with a price is bought through Stripe (see [Selling courses](#selling-courses)). Before 0.4.13 this field was labelled Level, with Premium labelled Intermediate. Same switch, clearer name.
- **Lessons** attached to courses, with ordered sequence and translatable content.
- **Selling courses** from 0.5.0. Set Access to Premium with a price and the catalogue shows a Buy button; the student pays on a Stripe-hosted page and comes back enrolled. Needs [EP Ecommerce Stripe](/plugins/ep-ecommerce-stripe/).
- **Enrolment tracking** — which student is in which course.
- **Progress tracking** — which lessons has the student completed.
- **Multilingual content** — store title and body as JSON translations per course and per lesson.

## What EP Courses does NOT do (yet)

This plugin deliberately has a narrow scope. It does not:

- **Handle frontend student login** — that's [EP Membership](/plugins/ep-membership/)'s job.
- **Host videos**. Embed from YouTube, Vimeo, or an MP4 file you host yourself. If that file lives in your own S3-compatible bucket, [EP Media Storage](/plugins/ep-media-storage/) will serve it behind a link that expires.
- **Issue certificates** — not currently built in.
- **Run quizzes inside lessons** — not currently built in.
- **Sell recurring access.** A course sale is a one-off purchase. For subscription billing, pair with [EP Ecommerce Subscriptions](/plugins/ep-ecommerce-subscriptions/).
- **Refund or revoke a purchase from the admin.** Refund in Stripe, then remove the enrolment by hand.
- **Sell to a signed-out visitor.** An enrolment belongs to a user account, so the buyer needs to be registered and signed in before they can pay.

For a full learning management system, combine EP Courses with EP Membership (for login and access control) and EP Ecommerce Stripe (to take the payment).

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**

Optional but commonly paired:

- **EP Membership** for student accounts and authenticated course access.
- **[EP Ecommerce](/plugins/ep-ecommerce/) and [EP Ecommerce Stripe](/plugins/ep-ecommerce-stripe/) 0.1.21 or later** to sell courses. Both are required to charge for one; EP Ecommerce Stripe builds on EP Ecommerce and does nothing without it.
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

1. Create a course with title, description, outcome, access, and price.
2. Add lessons to the course. Each lesson has a title, body, and sort order.
3. (Optional) Tick the languages you need in settings, then fill in each language's fields in the **Translations** accordion on the course and lesson edit forms.
4. Create a page with the viewer slug, add `[ep-course-viewer]`.
5. Create a catalogue page, add `[ep-courses]`.
6. If the course is paid, set Access to **Premium** with a price, and make sure both EP Ecommerce and EP Ecommerce Stripe are active, with your Stripe keys saved in EP Ecommerce Stripe.
7. If gated, configure EP Membership to require login for the viewer page.

## Selling courses

From 0.5.0 a course can be sold. Set **Access** to Premium, give it a price and currency, and the catalogue shows a **Buy** button in place of the old disabled "Coming Soon".

You need **both** [EP Ecommerce](/plugins/ep-ecommerce/) and [EP Ecommerce Stripe](/plugins/ep-ecommerce-stripe/) 0.1.21 or later active, with your Stripe keys saved in the latter. EP Ecommerce Stripe does nothing on its own: it builds on EP Ecommerce, and without it the payment confirmation never runs.

If any part of that chain is missing, the catalogue keeps showing the old disabled "Coming Soon" button rather than a Buy button. That is deliberate. A Buy button is only offered where a payment could actually be completed, so nobody can pay into a site that cannot finish the enrolment.

The buyer must be signed in first. An enrolment belongs to a user account, so a signed-out visitor sees a link to register instead.

### How access is granted

This is the part worth understanding, because it is deliberately strict.

Pressing Buy records the enrolment as **pending** and sends the student to a Stripe-hosted payment page. A pending enrolment grants nothing: the course stays locked, exactly as if they had never pressed the button. Someone who reaches the payment page and abandons it is in no different a position from someone who never started.

The course unlocks in one place only, when Stripe confirms the payment. Returning to the success page does not by itself grant anything, because anyone can visit a URL. If the confirmation has not arrived yet, that page says the payment went through and the course is being set up.

The price is read from the course record at the moment the payment session is created. The browser only ever says which course, never what it costs.

### Timing

Confirmation is not always instant. Stripe notifies your site, your site records that notification, and the enrolment is completed on the next page view. In practice that is usually seconds. It is normal for a student to land back on the course a moment before it opens, which is what the "setting up your course" message covers.

### What is not covered

Refunds are not wired up. Refund in Stripe as usual, then remove the enrolment by hand. A refund does not revoke access on its own.

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

Two different things, so pick the one you mean. To sell a course outright, set Access to **Premium** with a price and let EP Ecommerce Stripe take the payment (see [Selling courses](#selling-courses)). To gate a course behind an existing membership rather than a single sale, that is EP Membership's access rules on the viewer page, optionally with EP Ecommerce Subscriptions handling the recurring billing.

### “A Premium course shows Coming Soon instead of a Buy button”

The Buy button only appears where a payment could actually be completed, which is deliberate. Check all four: [EP Ecommerce](/plugins/ep-ecommerce/) is active, [EP Ecommerce Stripe](/plugins/ep-ecommerce-stripe/) is active with your keys saved, the course has a price above zero, and you are signed in rather than viewing signed out. Missing EP Ecommerce is the easy one to overlook, because EP Ecommerce Stripe looks installed and configured while the half that completes the sale is absent.

### “A student paid but the course has not opened”

Give it a page view. Confirmation is recorded when Stripe notifies your site and applied on the next request, so the enrolment completes moments later rather than instantly.

If it is still closed after that, check the payment actually succeeded in your Stripe dashboard, and that the webhook endpoint in Stripe points at your site with the signing secret saved in EP Ecommerce Stripe. A payment that never produced a webhook cannot complete an enrolment.

### “Previous is missing, and Next goes back to lesson one”

Fixed in 0.4.15. The Sort Order box on each lesson used to arrive pre-filled with `0`, and leaving it alone left every lesson at position 0, so the viewer could not tell them apart. Previous never rendered, Next returned to the first lesson, and every sidebar link went to the same place.

Updating repairs existing courses automatically on the next admin page load. Lessons you had already numbered keep their order and stay in front; only the zeros are renumbered, in the order they were created. A course already numbered properly is left untouched.

New lessons now leave Sort Order blank, meaning "add at the end".

### “Students can see lessons they haven't completed prerequisites for”

Prerequisite-based progression isn't built in yet. On the roadmap but not shipped. See the review queue.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
