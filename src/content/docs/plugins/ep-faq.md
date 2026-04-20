---
title: "EP FAQ"
description: "FAQ management for PageMotor with accordion display, search, Schema.org FAQPage structured data, voting, and analytics. Import from Markdown or JSON."
sidebar:
  order: 30
---

EP FAQ is a proper FAQ plugin for PageMotor. Database-backed questions grouped into categories, accordion display, visitor search, Schema.org FAQPage markup for rich-result eligibility, and voting so you can see which answers help and which don't.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Features:

- **Categories** to group questions.
- **Accordion display** with smooth expand/collapse.
- **Search** with live filtering as the visitor types.
- **Schema.org FAQPage** structured data, emitted as JSON-LD in the head.
- **Voting** — "Was this helpful?" with up/down buttons and anonymous aggregate counts.
- **View counts** per question, so you can see which get read.
- **Import from Markdown or JSON** for bulk setup.
- **Drag-to-reorder** questions within a category.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**

## Installation

1. Download `ep-faq.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Create a page for your FAQ and drop in `[faq]`.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[faq]` | Full FAQ with every active category and question, in category order, in question order. |
| `[faq category=billing]` | Only questions in the `billing` category. |
| `[faq search=true]` | Include the search box above the accordion. |

Combine attributes: `[faq category=billing search=true]` shows the billing FAQ with a search restricted to that category.

## Managing questions

Open **Plugin Settings → EP FAQ → Questions**.

- **Add Question.** Title (the question), body (the answer, HTML allowed), category, sort order, status.
- **Edit** or **Delete** from each row.
- **Drag handle** on each row to reorder within a category.

## Categories

**Plugin Settings → EP FAQ → Categories.**

- Name, slug, description, sort order.
- Display order controls the order categories appear when the `[faq]` shortcode renders without a category filter.

## Import from Markdown

A fast way to bulk-populate an FAQ.

Upload a Markdown file with this shape:

```markdown
## Billing

### How do I cancel my subscription?

Go to your account page and click Cancel.

### When will I be charged?

Every month on the day you signed up.

## Using the product

### Can I upgrade later?

Yes, upgrades prorate the cost.
```

`##` headings become categories. `###` headings become questions. Following paragraphs become the answer.

## Schema.org structured data

When an FAQ page loads, EP FAQ emits a JSON-LD `FAQPage` schema in the document head. Every question-answer pair is included. Google uses this for rich-result eligibility — your FAQ can appear as expandable results in search.

No configuration needed. If you have an FAQ page with valid schema, test it in [Google's Rich Results Test](https://search.google.com/test/rich-results).

## Voting

Each question has thumbs-up and thumbs-down buttons. Clicking either:

- Increments the respective counter.
- Stores a cookie so the same visitor can't vote twice on the same question.
- Updates the display immediately.

Aggregate counts are visible in the admin. A question with 90% thumbs-down is a signal to rewrite the answer.

## Analytics

The admin dashboard shows per-question:

- **Views.** Every time the question was shown (the question is considered viewed when the accordion expands).
- **Helpful votes.** Thumbs-up count.
- **Unhelpful votes.** Thumbs-down count.

Sort by views to see the most-asked; sort by unhelpful to see answers that need work.

## Search

When `search=true` on the shortcode, a search input renders above the accordion. Typing filters questions in real time, matching on question title and body text. If no questions match, a "No results" message appears.

Search is client-side JavaScript. On very large FAQs (hundreds of questions), performance might suffer — in that case, restrict with the `category` attribute and expose multiple FAQ pages instead of one.

## Troubleshooting

### "Rich results test shows no FAQ schema"

Confirm the `[faq]` shortcode is on the page. Schema is only emitted when the shortcode is rendered. Also check your page has at least one active question in an active category, otherwise nothing to mark up.

### "Search doesn't find a question I know is there"

Check the question is `status = active`. Inactive questions don't render, so search can't find them.

### "Voting buttons do nothing"

Check browser console for JS errors. Also check that AJAX endpoints are reachable — voting is an AJAX call, and something blocking it (CSP, cache) will break it.

### "Import from Markdown puts everything in 'Uncategorised'"

Your Markdown must use `##` for category headings and `###` for questions. Other header levels aren't recognised. Check the shape against the example above.

### "FAQ page loads slowly with many questions"

If you have 200+ questions and are rendering all of them, the accordion HTML + JS is heavy. Split into multiple pages by category using `[faq category=X]` on each.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
