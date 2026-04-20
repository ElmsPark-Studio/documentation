---
title: "EP Email AI Reply"
description: AI-powered draft replies for EP Email contact form submissions. Generates a professional draft response you can review, edit, and send.
sidebar:
  order: 25
---

EP Email AI Reply adds an AI draft-reply feature to [EP Email](/plugins/ep-email/)'s submissions inbox. Open a contact form submission, click **Draft reply with AI**, get a draft response you can edit and send.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

A customer submits a contact form. You open the submission in EP Email's inbox. A **Draft reply with AI** button appears. Clicking it:

1. Sends the submission (name, email, message, form metadata) to your configured LLM provider.
2. Receives a proposed reply that answers the customer's question in a professional tone matching your brand voice.
3. Populates a reply editor with the draft.
4. You review, edit as needed, click Send.

The reply goes out through EP Email's normal SMTP config, so it's signed, tracked, and deliverable.

## Requirements

- **PageMotor 0.7 or later**
- **EP Email** (required)
- **EP Suite base class**
- **An API key** from a supported LLM provider (Anthropic, OpenAI, etc. — same options as [EP Assistant](/plugins/ep-assistant/))

## Installation

1. Install **EP Email** first.
2. Download `ep-email-ai-reply.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Configure your LLM provider API key in the plugin settings.

## Settings

- **LLM provider.** Anthropic, OpenAI, or any of the nine providers EP Assistant supports.
- **API key.** Paste from your provider's dashboard.
- **Model.** Pick the model that balances quality and cost for your volume.
- **System prompt.** Extra instructions appended to every draft request. Use this to set tone: "Reply in a warm, British English voice. Sign off as 'The team at Acme'."
- **Rate limit.** Drafts per admin per hour, to cap API costs.

## Using it

1. Go to **EP Email → Submissions**.
2. Open a submission.
3. Click **Draft reply with AI**.
4. Wait a few seconds — the draft appears in the reply editor.
5. Review. Edit anything that's wrong or that needs your personal touch.
6. Click **Send**.

The reply goes out with your site's from-address via EP Email. The submission is marked as replied.

## Good drafting practice

- **Read before sending.** The AI doesn't always know what you know. If a customer asks a factual question about your business, the AI will guess. Check the answer is actually correct.
- **Strip anything generic.** AI draft tone can be flat by default. Trim filler sentences so the reply sounds like you.
- **Personalise.** Mention specifics from their message. "I saw you're in Glasgow" beats "Thanks for reaching out".

## Troubleshooting

### "Draft button doesn't appear"

Check:
- The plugin is activated.
- An API key is saved in settings.
- You're viewing a specific submission (not the list view).

### "Draft fails with 'Unauthorized'"

API key is wrong or expired. Rotate it.

### "Draft takes ages to generate"

LLM provider is slow or rate-limited. Switch to a faster model or a different provider temporarily. Check your provider's status page.

### "Drafts are being charged to my account but I'm not actually sending them"

Cost is incurred when the draft is generated, not when you send it. If you're generating drafts and discarding them all, that's still billable tokens. Use the rate limit setting to cap generations.

### "Draft answers a different question than the customer asked"

The AI sometimes misreads submissions, especially ones with unusual phrasing. Always read before sending. If a specific submission confuses the AI, file a note in the review queue — bad outputs help us improve the system prompt.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
