---
title: "EP Email Inbox"
description: "AI-powered incoming email handler for EP Email. Polls an IMAP mailbox, classifies messages, and auto-replies using your LLM provider. Useful for first-line support triage."
sidebar:
  order: 28
---

EP Email Inbox polls an IMAP mailbox and handles incoming email with AI. Useful for first-line support where most questions can be answered by an AI given your site context, and the remainder are routed to a human.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

How it runs:

1. **IMAP polling** against your support mailbox (e.g. `support@yoursite.com`) on a configurable interval.
2. For each new message, the plugin reads the sender, subject, and body.
3. The message is sent to your configured LLM provider with context about your site, products, and FAQs.
4. The LLM decides whether it can answer. If yes, it drafts a reply. If no, it flags the message for human attention.
5. Auto-replies (when confident) go out through EP Email's SMTP.
6. Flagged messages sit in the inbox dashboard for you to handle manually.

Every message, auto-replied or flagged, is logged with full transcript so you can audit what the AI did.

## Good fits for AI auto-reply

- **"What are your opening hours?"** — context says so.
- **"How do I reset my password?"** — standard instruction.
- **"Is feature X included in the Pro plan?"** — pricing/features are site context.
- **"My download link expired, can I have another?"** — plugin can check orders and send a new link.

## Not good fits

- **Complaints.** Always route to humans.
- **Legal questions.** Always route to humans.
- **Technical questions specific to the customer's setup.** AI guesses; a human can check the actual server.
- **Anything where the customer is upset.** The AI handles routine enquiries; emotion needs a person.

## Requirements

- **PageMotor 0.7 or later**
- **EP Email** (required)
- **EP Suite base class**
- **An IMAP mailbox** (your support email account)
- **An LLM provider API key** (Anthropic, OpenAI, or any supported)
- **PHP IMAP extension** installed on your server

## Installation

1. Install **EP Email** first.
2. Download `ep-email-inbox.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Open **Plugin Settings → EP Email Inbox**.

## Settings

### IMAP connection

- **Server.** IMAP host (e.g. `imap.fastmail.com`).
- **Port.** 993 for SSL.
- **Username / Password.** Mailbox credentials.
- **Mailbox folder.** Usually `INBOX`.
- **Poll interval.** 5, 15, 30, or 60 minutes.

### LLM

- **Provider.** Anthropic, OpenAI, etc.
- **API key.** Provider credential.
- **Model.** Pick one that balances quality and cost.

### Behaviour

- **Confidence threshold.** If the AI's self-reported confidence is below this, flag for human instead of auto-replying. Default 80%.
- **Signature.** Text appended to every auto-reply.
- **Always flag these keywords.** Comma-separated. Messages containing any keyword are always routed to a human regardless of AI confidence. Good for "refund", "complaint", "urgent", "lawyer".

### Context for the AI

- **Site description.** A paragraph about what your site does.
- **Product/service list.** What you sell, with prices if relevant.
- **FAQ context.** Paste your FAQs. The AI uses this to answer routine questions.
- **Brand voice.** Tone guidance. "British English, friendly but professional. No emojis. Sign off with 'Best, the team.'"

## Inbox dashboard

Lists every message the plugin has processed:

- **Auto-replied** (AI handled it; reply shown).
- **Flagged** (awaiting human; AI's reasoning shown).
- **Failed** (error during processing).

For flagged messages, you can click **Draft reply** to generate a suggested reply the same way [EP Email AI Reply](/plugins/ep-email-ai-reply/) does, or write your own. Either way, sending goes through EP Email.

## Audit

Every AI interaction is logged:

- Original message.
- AI's proposed reply.
- Confidence score.
- Whether auto-reply was sent or flagged.
- Cost of the LLM call (for API-billed providers).

Logs are retained for 90 days by default.

## Troubleshooting

### "IMAP connection fails"

Check:
- Host and port are correct.
- Username is the full email address.
- App-specific password if your mail provider requires one (Gmail, Fastmail).
- PHP IMAP extension installed (`phpinfo()` should list IMAP).

### "Plugin polls but no messages are being processed"

Check the poll log on the settings page. If it shows "No new messages", the mailbox is empty (or all messages are already marked as seen). IMAP polling only picks up new unseen messages.

### "Auto-replies are going to the wrong people"

The plugin replies to the `Reply-To` header if present, otherwise the `From`. If someone emailed you from an alias, replies might go to the alias unless their mail system rewrites. Test with a colleague first.

### "AI is confidently wrong about my products"

Tighten the site description and FAQ context. The AI only knows what you tell it. More context = fewer wrong answers. Also lower the confidence threshold to flag more messages for human review.

### "Auto-replies sound robotic"

Rewrite the brand voice setting. "Friendly but professional" is generic. Be specific: "Reply in plain English. Short paragraphs. One clear answer per paragraph. No buzzwords."

### "Cost is going up on the LLM API"

Switch to a smaller model (Haiku vs Opus). Or raise the poll interval to reduce frequency. Or add more keywords to the always-flag list so only straightforward messages hit the AI.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
