---
title: "EP Helpdesk"
description: "Support ticket system for PageMotor with AI-drafted replies, one-click approval, customer portal, and full conversation threading."
sidebar:
  order: 34
---

EP Helpdesk is a support ticket system for PageMotor. Customers raise tickets, conversations thread by ticket, staff reply, everything is searchable. The AI-drafted reply feature generates a proposed response so staff only need to review and approve, not write from scratch.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Core features:

- **Ticket submission** via a form on your site, or forwarded email.
- **Thread view** with the full conversation between customer and staff.
- **Status lifecycle**: New → Open → Waiting on customer → Resolved → Closed.
- **Staff assignment** and routing.
- **AI-drafted replies** — click a button, an LLM reads the ticket history and proposes a response.
- **One-click approval** — staff reviews the draft, edits if needed, clicks Send.
- **Customer portal** — customers see their own tickets, reply, close their own when resolved.
- **Email notifications** at every status change via EP Email.

## Requirements

- **PageMotor 0.7 or later**
- **EP Email** (required for notifications)
- **EP Suite base class**

For AI-drafted replies:

- An API key from any of the supported LLM providers.

## Installation

1. Install **EP Email** first.
2. Download `ep-helpdesk.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Create pages for the submission form and portal:
   - `[helpdesk-submit]` on a page at `/support/submit/`.
   - `[helpdesk-portal]` on a page at `/my-tickets/`.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[helpdesk-submit]` | Ticket submission form. Collects name, email, subject, body, and category. |
| `[helpdesk-portal]` | Customer's ticket history. Shows their own tickets, lets them reply and mark resolved. |

## Categories and routing

From settings:

- **Categories.** Name, description, assigned staff. Common examples: "Billing", "Technical", "General enquiry".
- **Default assignee.** Fallback staff member if no category-specific assignment.

When a ticket is submitted, it's routed to the assignee for that category.

## Status lifecycle

- **New.** Just submitted, not yet acknowledged.
- **Open.** Staff has seen it, actively working.
- **Waiting on customer.** Staff replied, ball is in the customer's court.
- **Resolved.** Staff marked it done. Customer gets asked to confirm.
- **Closed.** Ticket is over, no further action.

Status changes send emails: ticket received, reply posted, status updated.

## AI-drafted replies

From the staff ticket view, click **Draft reply with AI**. The plugin:

1. Reads the entire ticket history.
2. Reads your help centre content (if connected) and recent tickets on similar topics.
3. Asks the LLM to propose a reply.
4. Renders the draft in the reply editor.

Staff reviews, edits, and clicks **Send**. Or clicks **Discard** and writes their own.

### Tuning the AI drafts

- **System prompt** in settings — tone, greeting, sign-off, what kinds of answers are OK to auto-draft (refunds no, password resets yes).
- **Confidence threshold** — if the AI's self-rated confidence is below this, no draft is offered (forces human reply).
- **Category-specific prompts** — override the system prompt per category. Billing questions can use one tone, technical another.

## Customer portal

At `[helpdesk-portal]`, authenticated customers (via EP Passkeys, EP Membership, or just email verification token) see:

- List of their tickets with status.
- Click to see full thread.
- Reply in the thread.
- Mark as resolved.

## Search

Full-text search across tickets. Search customer email, subject, body, or staff replies. Use for:

- Finding the last ticket this customer raised.
- Seeing how a similar issue was resolved previously.
- Auditing staff responses.

## Troubleshooting

### "AI drafts aren't offered"

Check LLM API key in settings. Check confidence threshold isn't set so high that no ticket qualifies. Check the category's system prompt allows AI drafts (some categories might be configured to always require human).

### "Customer submitted a ticket but didn't get a confirmation email"

EP Email is responsible for delivery. Check EP Email's log. Usually SMTP config issue.

### "Staff replies go to spam in customer inboxes"

Your site's from-address needs SPF/DKIM/DMARC set up. Check EP Email configuration and the domain's DNS. Consider routing through [EP Email ElmsPark](/plugins/ep-email-elmspark/) for better deliverability.

### "Assignee isn't receiving their ticket notifications"

Check the assignee has a valid email saved in their PageMotor user profile. Check EP Email isn't filtering internal emails.

### "Portal shows no tickets but the customer insists they submitted one"

Auth mismatch. The portal matches tickets by email address of the authenticated user. If they submitted with `alice@example.com` but logged into the portal as `alice.smith@work.com`, no tickets show.

### "AI draft is factually wrong"

Tune the system prompt. Add more context ("This is a SaaS for X. Refunds are allowed within 30 days."). Also use the category-specific prompt to limit what the AI can confidently answer.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
