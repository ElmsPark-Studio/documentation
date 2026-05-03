---
title: "EP Documents"
description: "Hierarchical documentation site for PageMotor. Author docs in HTML or Markdown, organise by section, draft / improve / translate with Claude, six EU languages."
sidebar:
  order: 17
---

EP Documents turns any PageMotor site into a documentation site. Hierarchical sections, HTML or Markdown content, draft / published workflow, optional Claude-assisted writing, and a translate action that produces French / German / Spanish / Italian / Dutch / Portuguese versions on demand.

Published by [ElmsPark Studio](https://elmspark.com).

## What EP Documents does

- Lets you create, edit, and delete documents from the PageMotor admin
- Organises documents hierarchically by section (`hosting`, `plugins/ep-email`, `internal/sops/expenses`)
- Stores content as HTML or Markdown, with a per-document format toggle
- Tracks status (Draft / Published) and a per-section sort order
- Adds three optional Claude-assisted actions: **Draft with Claude**, **Improve with Claude**, **Translate with Claude**
- Logs every Claude call to an audit table with full input, output, model and status
- Rate-limits Claude calls at 20 successful calls per hour per admin user
- Speaks six EU languages out of the box for its admin UI

## What EP Documents doesn't do (yet)

- v0.3 is **admin-only**. Documents you create do not appear on the public site. There is no router, no theme, no shortcode, no syntax highlighting yet.
- Frontend routing, themes, and code highlighting arrive in later versions.
- No per-document permissions. Any admin who can see the EP Documents settings page can create, edit, and delete every document.

If you need a public docs site today, EP Documents v0.3 lets you author and stage everything inside admin, ready for the day frontend routing lands.

## Requirements

- **PageMotor** 0.8 or later
- **EP Suite** base class (auto-loaded with any EP plugin)
- **Anthropic API key** (only required for the three Claude actions; plain CRUD works without one)

## Installation

1. Download the latest `ep-documents.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. In PageMotor admin go to **Plugins → Manage Plugins → Upload**, select the zip, and activate.
3. Click **EP Documents** in the admin nav to open the dashboard. The first time you load the page the plugin creates two database tables (`{prefix}ep_documents` and `{prefix}ep_documents_generations`).

## Settings

The settings page has three groups:

### Documents (dashboard)

- Three summary cards: Total documents, Published count, Drafts count
- An **Add Document** button that opens the create form
- A list of every document, grouped by section, with Edit and Delete actions per row

### Claude AI assistance

- **Anthropic API key** — your key from [console.anthropic.com](https://console.anthropic.com). Stored as plain text in the plugin options. Required for Draft, Improve, and Translate.
- **Model** — Claude Sonnet 4.6 (default, recommended), Claude Opus 4.7 (highest quality, higher cost), or Claude Haiku 4.5 (faster, lower cost).
- **Max tokens** — upper limit on response length. 2048 suits most documents; raise for long reference pages. Clamped between 256 and 16384.
- **English variant** — which spelling and idiom Claude should use. Choices:
  - **Auto** (default) — for Draft, matches the variant of your brief (American brief gets an American draft). For Improve, preserves the document's existing variant (won't switch British spellings to American or vice versa). Sensible default for most sites.
  - **British English** — forces British spellings (organise, colour, behaviour) regardless of input.
  - **American English** — forces American spellings (organize, color, behavior).
  - **International English** — neutral; avoids regional spellings where a neutral form exists.

  Translate is not affected by this setting — the target language is chosen per call.

Leave this group blank if you only want plain CRUD. The Draft / Improve / Translate buttons disable automatically when no key is set.

### About this plugin

A short note about what v0.3 ships and what is planned for later versions.

## Creating and editing documents

Click **Add Document** to open the form. Fields:

- **Title** — display title, free text
- **Section** — hierarchical path. Slashes allowed. Examples: `hosting`, `plugins/ep-email`. The dropdown autocompletes from existing sections.
- **Slug** — URL piece. Lowercase letters, numbers, hyphens. Auto-slugified on save. Unique per section, so two documents can both have slug `intro` if they live under different sections.
- **Content format** — HTML or Markdown
- **Status** — Draft or Published
- **Order** — numeric. Controls position within a section. Lower numbers come first.
- **Content** — the document body, in whichever format you chose above

Below the form you'll see three Claude buttons. They enable when an API key is configured. **Draft** is shown only on a new document; **Improve** and **Translate** appear once a document has content to work with.

## Working with Claude

All three actions open a modal with a preview of what Claude produced. Nothing is written to your document until you click **Apply to document**.

### Draft with Claude

Tell Claude what the document should cover. It returns a complete first draft in the format you've selected (HTML or Markdown), in your chosen English variant (see settings above; default is Auto, which matches the spelling of your brief), with no AI filler and no top-level heading (so it slots into your section structure cleanly).

Example briefs:

- "How to set up a fresh PageMotor site on Vultr. Cover signup, DNS, SSL and first-login."
- "Refund policy for a small consulting business. Cover the 14-day cooling-off period, what counts as a deliverable, and how to request a refund."
- "Step-by-step on changing a tap washer for a domestic customer. Tools, isolation, swap, test."

### Improve with Claude

Pass Claude the current document and (optionally) notes about what you want changed. It returns a polished version that keeps your facts, structure, and voice intact but tightens the prose, fixes spelling and grammar within your document's existing English variant (won't switch British to American or vice versa), and breaks dense paragraphs into lists where appropriate.

Useful for: tidying a draft you wrote in a hurry, sharpening prose a customer flagged as confusing, or running a final pass before flipping a document to Published.

### Translate with Claude

Pick a target language (French, German, Spanish, Italian, Dutch, Portuguese, Polish, Swedish, or English). Claude translates the prose and leaves all HTML tags, Markdown constructs, code blocks, URLs, class names, and product names untouched.

For multilingual sites: use Translate as a first-pass cost saver, then have a native speaker review the output. Don't ship a translated document directly to customers without a human eye on it.

## Languages

The admin UI is fully translated into:

- German (de)
- Spanish (es)
- French (fr)
- Italian (it)
- Dutch (nl)
- Portuguese (pt)

English is the baseline and the fallback for any missing translation key. Switch UI language from the EP Suite language dropdown in the admin nav.

The Claude system prompts themselves remain in English regardless of UI language. This is deliberate: instructions to Claude should be consistent across all installs so the output quality is predictable.

## Privacy

EP Documents makes outbound HTTPS calls to `https://api.anthropic.com/v1/messages` whenever an admin clicks Draft, Improve, or Translate. Three things matter for your privacy posture:

1. **What leaves your site.** The full text of the brief (Draft) or the document content (Improve, Translate). Plus the model name and your max-tokens setting. Plus your API key in the request header. Nothing else.
2. **What Anthropic does with it.** Subject to [Anthropic's API data usage policy](https://www.anthropic.com/legal/aup). At time of writing, Anthropic does not train on API inputs by default.
3. **What stays on your server.** Every Claude call (success or failure) is logged to `{prefix}ep_documents_generations` with the user ID, action type, full input, full output, model, status, and any error message. There is no automatic retention policy. If your site is subject to data-minimisation requirements you should periodically prune the table.

EP Documents does not currently integrate with EP GDPR for explicit consent gating, because the user triggering each call is the admin who configured the API key in the first place — they are the data controller for their own action. If you give other admins access who haven't agreed to this flow, brief them before they start clicking Draft.

If your documents contain personal data (customer names, employee records, anything sensitive), think before you click Improve or Translate on them. The content will leave your server.

## Coexistence with other EP plugins

EP Documents is independent of the other EP Suite plugins. It uses the EP Suite design system and shares the language switcher, but it does not depend on EP SEO, EP Local Business, EP Locations, or EP GDPR.

## Troubleshooting

### "Claude API key is not configured"

You haven't set an Anthropic API key in **EP Documents → Claude AI assistance**. Get one from [console.anthropic.com](https://console.anthropic.com), paste it into the field, and save. The Draft / Improve / Translate buttons will enable on the next page load.

### "You have hit the hourly Claude limit. Please wait a while before trying again."

The plugin enforces 20 successful Claude calls per hour per admin user. The window is rolling — check back in an hour. If you regularly hit this limit, you're either drafting a lot of new content (legitimate, just wait) or Improve-looping on the same document (try saving a final draft instead of regenerating).

### "Claude API key is invalid"

The key in your settings has been revoked or has a typo. Check the key against your Anthropic console, paste it back into the settings field, and save.

### Saving a document silently does nothing

Almost always a missing or duplicate slug. Slugs are unique per section. If you already have a document with slug `intro` in section `hosting`, you can't save another one with the same combination. Either change the slug or change the section.

### The Claude buttons are disabled

Check three things in order: (1) is an API key set in **Claude AI assistance**? (2) for **Improve** and **Translate** specifically, does the document have any content? (3) for **Draft**, is this a new document (Draft only enables on a fresh form, not on an existing record)?

### "Cannot reach Claude right now"

Network problem between your server and `api.anthropic.com`. Check your server can resolve and reach the host. If you're behind a corporate firewall, your egress rules may need updating.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
