---
title: "EP Email AI Triage"
description: "AI-powered spam triage for EP Email contact forms. Classifies every submission, blocks confirmed spam silently, holds it in quarantine for review."
sidebar:
  order: 25.5
---

EP Email AI Triage adds intent-aware spam protection to [EP Email](/plugins/ep-email/) contact forms. Every submission that survives EP Email's free heuristics is classified by an LLM. Real enquiries reach your inbox. Confirmed spam is blocked silently and held in a quarantine you can audit.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

EP Email's built-in [Spam Protection](/plugins/ep-email/#spam-protection) — honeypot, time trap, URL count, keyword blocklist, rate limit — catches the obvious bot junk for free. It cannot read intent. It cannot tell a customer enquiry from an SEO pitch when both look like plain text submitted by a human-looking visitor.

AI Triage closes that gap. Every submission that passes the free heuristics is sent to your chosen LLM provider with a short context line about your site. The model returns one of four classifications with a confidence score:

- **real** — Genuine enquiry, customer interest, prayer request, support question, application, sign-up.
- **spam** — SEO pitch, link-building, marketing offer, crypto/casino, irrelevant promotion.
- **hostile** — Threats, harassment, manipulation attempts, abusive content.
- **unclear** — Cannot reliably classify with the information available.

What happens next is a configurable decision matrix.

## Decision matrix

| Classification | Confidence | Outcome |
|---|---|---|
| real | at or above threshold | Delivered as normal |
| real | below threshold | Delivered with `[REVIEW]` prefix on the email subject |
| spam | at or above threshold | Blocked silently, held in quarantine |
| spam | below threshold | Delivered with `[FLAGGED]` prefix |
| hostile | any | Blocked silently, held in quarantine, optional admin alert |
| unclear | any | Delivered with `[REVIEW]` prefix |
| Classifier error or timeout | n/a | Delivered with `[REVIEW]` prefix (fail-open) |

**Silent blocks return the same friendly success message** ("Thank you for your submission") as the honeypot. Spammers cannot tell whether their message reached your inbox or hit the filter, so they cannot tune around the rules. Real customers are never told their message looked like spam.

**Fail-open on errors is non-negotiable.** If the LLM call fails for any reason — API outage, network blip, malformed response — the submission is delivered with a `[REVIEW]` flag rather than dropped. Genuine messages must never be eaten by an AI provider's bad day.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Email 1.10.1 or later** (provides the `should_send` extension hook)
- **An API key** from Anthropic (recommended) or OpenAI

## Installation

1. Install **EP Email** first if you haven't already, and upgrade to **1.10.1 or later**.
2. Download `ep-email-ai-triage.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. In your PageMotor admin, go to **Plugins then Manage Plugins** and upload the zip.
4. Activate **AI Triage** in your active Theme's plugin configuration.
5. Database table for the quarantine is created on first load.

**How to verify:** after activation, go to **Plugins then Plugin Settings** and you should see **AI Triage** in the sidebar. The settings page includes a quarantine viewer at the bottom (empty until your first block).

## Configuration

Open **AI Triage** in your admin sidebar.

### Master switch

| Setting | Default | What it does |
|---|---|---|
| Enable AI Triage | Off | Master switch. When off, EP Email runs as if this plugin were not installed. |

The plugin ships disabled. Nothing is sent to any AI provider until you switch this on.

### AI provider

| Setting | Default | What it does |
|---|---|---|
| AI Provider | Claude (Anthropic) | Which LLM service classifies submissions. |
| API Key | (empty) | Your provider API key. |
| Model | (default per provider) | Override the model. Leave blank to use the recommended default. |

**Anthropic is the default** because their API terms exclude API inputs from training. The default model is `claude-haiku-4-5-20251001` — fast, accurate enough for triage, and cheap. **OpenAI is supported as a fallback.** Default model `gpt-4o-mini`.

To set up Anthropic: sign in to [console.anthropic.com](https://console.anthropic.com), create an API key, paste it into the API Key field. Top up the account with a small amount of credit (£5 covers many thousands of submissions).

### Site description

| Setting | Default | What it does |
|---|---|---|
| Site Description | (empty) | One or two sentences telling the classifier what your site is and who submits to its forms. |

**This is the most important single setting.** Without it the classifier guesses. With it, accuracy jumps significantly. Examples:

- **For a faith community:** "Virtual Faith Connections is an online church community for homebound Christians. Submitters are typically members or visitors looking to join services, request prayer, or contact the pastor."
- **For a local garage:** "Baytree Road Garage is a single-location MOT and servicing garage in Weston-super-Mare. Submitters are typically existing customers booking services or new customers asking about pricing."
- **For a SaaS product:** "Acme is a B2B project management SaaS targeting small UK agencies. Submitters are typically prospects asking about pricing, features, or integrations."

Be specific about audience and intent. Generic descriptions ("a business website") produce generic classifications.

### Confidence threshold

| Setting | Default | What it does |
|---|---|---|
| Confidence Threshold | 0.85 | Minimum confidence (0.0 to 1.0) for the classifier to act. Below this, borderline calls are passed through and flagged in the subject. |

Higher threshold means the classifier needs to be more sure before blocking. The default 0.85 is a sensible starting point. Raise to 0.9 if you see false positives in quarantine. Lower to 0.75 if real spam is reaching your inbox with `[FLAGGED]` prefixes.

### Hostile submissions

| Setting | Default | What it does |
|---|---|---|
| On Hostile Submissions | Block silently, hold in quarantine | What to do when classified as threatening or abusive. |
| Hostile Alert Email | (empty) | Where to send hostile-submission alerts when "Block silently, alert admin email" is selected. |

Three options for hostile submissions:

- **Block silently, hold in quarantine.** Default. Same as a confirmed-spam block.
- **Block silently, alert admin email.** Same as above plus a short alert sent to the configured address. Useful when you want to know it happened without seeing the content in your normal inbox.
- **Allow with `[HOSTILE]` flag in subject.** Lets it through with a clear warning prefix. Pick this only if you have a duty-of-care reason to read every message regardless.

### On-form disclosure

| Setting | Default | What it does |
|---|---|---|
| On-form Disclosure | Silent | `Silent`: rely on your privacy policy. `Disclosed`: render a small notice under each contact form's submit button. |
| Disclosure Text | "Submissions are AI-analysed to filter spam." | The notice shown when disclosure mode is `Disclosed`. |

For most sites, **silent** is appropriate. Update your site's privacy policy to disclose that contact form submissions are AI-analysed for spam detection by your chosen provider, and you're done.

For sites handling **special-category personal data** under UK GDPR — religion, health, sexual orientation, ethnicity, biometric or genetic data, trade-union membership — set this to **disclosed**. The on-form notice meets the higher transparency standard those categories warrant. A faith community site, a counselling service, or a medical practice should pick disclosed.

### Quarantine retention

| Setting | Default | What it does |
|---|---|---|
| Quarantine Retention (days) | 30 | Quarantined submissions older than this are auto-purged. |

The quarantine database is for review of recent decisions, not long-term storage. 30 days lets you spot a false positive in a week's catch-up; longer than that adds storage with little practical value.

## Quarantine

Every silent block writes a record to the quarantine table with the submission's content, the classification reason, the confidence score, and the submitter's IP. You can review the quarantine on the AI Triage settings page — it appears as a table at the bottom.

### Releasing a false positive

Two buttons sit on each quarantine row:

- **Release.** Re-sends the original message to the form recipient with `[RELEASED]` prepended to the subject, then removes the row from quarantine. Use this when the classifier called something spam that was actually a real customer enquiry.
- **Delete.** Permanently removes the row without sending. Use this for unambiguous spam you don't want sitting in the table.

The quarantine review pattern:

1. Once a week, open the AI Triage page in your admin.
2. Scan the quarantine list. Real enquiries are usually obvious from the submitter email and the first sentence of the message.
3. Click **Release** on any false positives. They reach your inbox marked `[RELEASED]`.
4. Click **Delete** on the rest, or leave them to auto-purge.

If you find more than one or two false positives a week, raise the **Confidence Threshold** by 0.05 and revisit the next week. If you find spam reaching your inbox flagged `[FLAGGED]`, lower it by 0.05.

## Per-form opt-out

Bypass triage on any individual form by adding `ai_triage` to its JSON definition:

```json
{
    "high-trust-form": {
        "recipient": "specific@example.com",
        "ai_triage": { "enabled": false },
        "fields": [
            {"type": "email", "name": "email", "label": "Email", "required": true},
            {"type": "textarea", "name": "message", "label": "Message", "required": true}
        ]
    }
}
```

Useful for forms behind a login wall, internal staff forms, or any case where the submitter is already known and triage would just add latency.

## Cost

Cost is bounded and small.

A single classification call uses around 250 input tokens and 30 output tokens. At Claude Haiku 4.5 prices that's roughly **£0.0002 per submission**. A thousand submissions cost about **20 pence**. Ten thousand cost about **£2**.

EP Email's per-IP rate limit runs **before** triage, so a single attacker cannot spend more than one classification per rate-limit window per IP. There is no realistic scenario where bot traffic burns through significant credit.

## Privacy

Submission text is sent to the LLM provider you configured. Anthropic's API terms exclude API inputs from training; OpenAI's API terms (since March 2023) similarly exclude API inputs from training their public models. Both providers process the request and return a classification without retaining the data for model improvement.

For UK GDPR compliance:

- Update your privacy policy to disclose that contact form submissions are AI-analysed for spam detection by Anthropic (or OpenAI), and that submissions transit to those providers as data processors.
- For special-category personal data, set **On-form Disclosure** to **disclosed** so submitters are told before they hit submit.
- Anthropic's data residency for API traffic is currently US-primary with EU options on enterprise plans. For most UK SMEs this is fine under UK GDPR with appropriate transfer mechanisms. If you have stricter residency requirements, talk to your DPO before enabling.

The plugin does not store submission content beyond what the quarantine table holds, and the quarantine auto-purges per the retention setting.

## Troubleshooting

### "AI Triage tab doesn't appear in admin"

Verify the plugin is activated in your active Theme's plugin configuration. Verify the plugin ZIP unpacked successfully — the admin UI lives in `plugin.php` of the AI Triage plugin and won't render if the file is missing or corrupted.

### "Submissions arrive but are never classified"

Open AI Triage settings. Check:

- **Enable AI Triage** is set to **Yes**.
- **API Key** is populated.
- **Site Description** is populated (the classifier needs context).

If all three look right, send a test submission with the word "bitcoin" in the message body. EP Email's free keyword filter should silently block it — that confirms Phase 1 is working. Then send a marketing-style submission ("Hi, we offer SEO services for businesses like yours, reply to discuss"). That should hit the LLM and either reach your inbox `[FLAGGED]` or appear in the quarantine.

### "Real enquiries are landing in quarantine"

Either the site description doesn't match what real submitters look like, or the confidence threshold is too low. Refine the site description first — add a sentence about your typical customer's tone and intent. Then, if needed, raise the threshold by 0.05.

Use **Release** on each false-positive row to send those messages to your inbox.

### "Spam is reaching my inbox flagged [FLAGGED]"

Confidence threshold is too high — the classifier is calling spam correctly but not confidently enough to block. Lower the threshold by 0.05. Or extend the EP Email keyword blocklist with terms specific to the spam you're seeing; that's a free Phase 1 catch and saves the LLM call.

### "Classifier returned null" or "[REVIEW]" on every submission

API key is wrong, expired, or your provider account is out of credit. Check your provider's dashboard. Test with a real submission; if the issue is API-side you'll see API errors in your server's PHP error log.

### "I want to test the classifier without sending real submissions"

Submit your own test messages from a private browser window. EP Email's per-IP rate limit may push back if you submit too fast — wait the configured rate-limit window between tests, or temporarily reduce it to 1 minute in EP Email's Contact Forms settings.

### "Cost is higher than I expected"

Check the EP Email per-IP rate limit is enabled and set to a sensible value (5 minutes is the default). A misconfigured rate limit can let a single attacker fire many classification calls per minute. Also check your **Confidence Threshold** isn't so high that every borderline submission gets passed through with `[FLAGGED]` flags — that doesn't reduce cost since the LLM call still happens, but it does mean noise in your inbox.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
