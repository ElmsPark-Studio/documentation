---
title: "EP Finance Invoicing"
description: "Quotes and invoices for PageMotor. Gap-free sequential numbering per series, a swappable tax pack, a branded PDF, a tokenised hosted invoice page, a one-tap pay link that reuses your existing payment provider, EP Email reminders, and clean postings into the EP Finance ledger."
---

EP Finance Invoicing issues quotes and invoices, takes payment for them, and posts the result into your books. It is part of the EP Finance family and sits on top of the EP Finance ledger.

This page documents EP Finance Invoicing **0.2.0**.

Published by [ElmsPark Studio](https://elmspark.com).

:::caution[It prepares figures, it does not give tax advice]
EP Finance Invoicing computes and presents tax using the rates you configure. It is not an accountant and gives no tax advice. Check your figures with your own adviser before filing anything.
:::

## Requirements

- **PageMotor 0.9b or later**
- **EP Finance**, which provides the ledger, the money handling and the chart of accounts. EP Finance Invoicing is a member of the finance family and is not a standalone install: it is supplied and configured alongside EP Finance rather than picked up on its own
- **[EP Ecommerce](/plugins/ep-ecommerce/)** with a payment provider configured, if you want pay links. It reuses whatever provider you already have, normally [EP Ecommerce Stripe](/plugins/ep-ecommerce-stripe/)
- **[EP Email](/plugins/ep-email/)** if you want due-soon and overdue reminders

## Settings

Everything on the settings screen is saved with PageMotor's own Save button.

| Setting | What it does |
|---|---|
| **Business name** | Shown on the PDF and hosted page. Blank falls back to your site title |
| **Address / VAT number / contact** | One item per line. Appears in the seller block on every document |
| **Payment details** | Account name, sort code, account number, one per line. Printed on invoices |
| **Default payment terms (days)** | Used to compute the due date. Defaults to 30 |
| **Due-soon reminder lead time** | How many days before the due date the reminder goes out. Defaults to 3 |
| **Send reminders** | Turns the due-soon and overdue reminder emails on or off |

## Numbering, and why it is built this way

Invoice numbers must be sequential and gap-free. Most systems allocate the number when the draft is created, which produces gaps every time a draft is abandoned, and can collide if two people issue at the same moment.

This plugin allocates the number at **issue**, not at creation, inside a locked counter. Two simultaneous issues cannot gap and cannot collide. Each series keeps its own counter, and quotes and invoices number separately.

Voiding an invoice **keeps its number**. The issue posting is reversed in the ledger, but the number stays used, because removing it would create the gap the whole design exists to prevent.

## The document lifecycle

1. **Draft.** Create a quote or an invoice with line items. Nothing touches the ledger yet.
2. **Issue.** The next number in the series is allocated and the receivable is posted to the ledger. Revenue is recognised at this point.
3. **Pay.** A settlement is recorded: bank up, receivable down. Revenue is not posted again, because it was recognised at issue.
4. **Void.** Available for an issued invoice that has not been paid. Reverses the issue posting and keeps the number. **A paid invoice cannot be voided.**

## Getting paid

Each invoice has a **hosted page** at an unguessable tokenised URL, in the form `?ep_inv=<token>`, with `&format=pdf` for the branded PDF. The page is print-friendly, so a customer can save or print it without an account.

Every response from that endpoint is served **noindex**, whether the token is valid or not, so invoices never reach a search engine.

The **pay link** creates an order through EP Ecommerce and reuses your existing payment extensions. There is no second payment integration to configure, and no second set of keys to keep in step.

## The double-posting wall

The risk in any system where an invoice can be settled from more than one direction is that a payment posts twice, once from the invoice and once from the payment feed. This plugin holds a single-source-of-truth wall so an invoice payment posts exactly once.

You can test that wall rather than trust it. The `invoice_simulate_paylink` action fulfils a pay-link order for a real invoice, runs the genuine EP Ecommerce fulfilment broadcast, and reports how many settlement groups resulted. **The correct answer is 1.** It also reports whether the sources feed correctly skipped the transaction, and whether the audit came back clean.

## Structured output

Documents are shaped to **EN 16931**, the European standard for electronic invoicing. The PDF is branded, and the same underlying document drives the hosted page.

## API actions

Every action is admin-only.

| Action | What it does |
|---|---|
| `invoice_create` | Create a draft invoice or quote with line items. Returns the id, token and total. Nothing posts to the ledger |
| `invoice_issue` | Issue a draft: allocate the next gap-free number and post the receivable |
| `invoice_get` | Full invoice: fields, computed lines, tax breakdown, events, hosted and PDF URLs |
| `invoice_pay` | Record a settlement once. Idempotent |
| `invoice_void` | Void an invoice, reversing the issue posting and keeping the number |
| `invoice_series` | The current next number for every series |
| `invoice_simulate_paylink` | Test the double-posting wall, as described above |

Line items are passed as JSON, each with a description, quantity, unit price in cents, and a tax rate in basis points.

## Tax packs

Tax is handled through a swappable interface, so a jurisdiction-specific pack can be dropped in without changing the invoicing code. A working manual-rate default ships with the plugin, so it is usable immediately with rates you set yourself.

## Things worth knowing

**It loads defensively.** PageMotor includes plugin files with no try/catch, so a fatal at file scope takes the whole site down. This plugin guards its bundled requires, so a missing or corrupt file degrades to "plugin absent" with a note in the error log rather than an outage.

**It carries a `Model: EP_Ecommerce` header.** That registers it as an EP Ecommerce extension, which is how a fulfilled pay-link order reaches it.

**Money is held in cents.** Line unit prices are integers, not floats, which is what keeps totals exact.

## Related plugins

- [EP Ecommerce](/plugins/ep-ecommerce/) and [EP Ecommerce Stripe](/plugins/ep-ecommerce-stripe/), which provide the payment rail for pay links
- [EP Email](/plugins/ep-email/), which delivers the reminders

## Document stamps

Every invoice and quote PDF carries a stamp in its footer: a number and the first characters of a fingerprint taken over the invoice's own figures.

If a client queries an invoice, or you are looking at one from two years ago, the stamp lets you check whether its figures are exactly what was recorded when it was issued.

**The fingerprint covers the figures, not the file.** Two renders of an unchanged invoice produce the same fingerprint, so reprinting one does not make it look altered. Changing a single line total produces a different one, and so does reordering two lines even when every total stays identical.

**It is not a signature.** It says nothing about who produced the invoice, only whether its figures have changed since. Anyone with access to the database could write a matching record. It protects against accident, drift and quiet edits, not against a determined party with that access.

Requires [EP Finance](/plugins/ep-finance/) 0.6.0 or later for the stamp to be recorded. With anything older the invoice is produced exactly as before, simply without a stamp line.

## Changelog

### 0.2.0

*Released 9 September 2026.*

- **Every invoice and quote PDF now carries a document stamp** in its footer: a number and the first characters of a fingerprint taken over the invoice's own figures.
- **The fingerprint covers the figures, not the file.** Two renders of an unchanged invoice agree; changing one line total, or reordering two lines while every total stays identical, does not.
- **It is not a signature.** It tells you whether the figures match what was recorded, not who produced the document.
- Requires EP Finance 0.6.0 or later. With anything older the invoice is produced exactly as before, without a stamp line.

### 0.1.11

- **Prepares the plugin for PageMotor 0.11.3, which requires every plugin to group its API and MCP actions into named families.** On that release an action declaring no family is refused silently, so without this update the plugin's actions would stop being offered with nothing on screen to say why.
- Families exist so that an AI working on your site sees the related actions together instead of stopping at the first one it tries.
- Safe to install on your current PageMotor. No behaviour changed.

### 0.1.10

*Released 1 September 2026.*

- The plugin's API actions no longer appear as individual top-level tools in connected MCP clients. Seven actions carried a flag that promotes an action alongside PageMotor's own dispatch entry points, and core reserves that surface for itself.
- **Nothing became unreachable.** Action ids, methods, access tiers, arguments and behaviour are unchanged. Every action is still discoverable through `list-actions`, described by `describe-action`, and invoked through `call-action`. Only a caller that invoked one of the promoted names directly as an MCP `tools/call` is affected; it should dispatch through `call-action` instead.

### 0.1.9

*Released 22 August 2026.*

- **Reminders no longer retire themselves when the send fails.** The reminder stage was previously marked done immediately after the send was attempted, without checking whether any mail actually left. An inactive EP Email, a missing From address, or any transport error therefore silently ended the chase and the invoice was never followed up again.

  There are now three outcomes instead of one: mail sent (stage done), no recipient on file (stage done, because retrying cannot help), and send failed (**retried on the next run**). The Reminders panel reports failures inline, so a dead transport no longer reads identically to "nothing was due".

### 0.1.8

*Released 6 August 2026.*

- Defensive load guard. The plugin now checks its bundled files at load and wraps every file-scope require in try/catch, so a missing or corrupt bundle degrades to "plugin absent" with a note in the error log instead of taking the whole site down. The build also verifies the bundle inside the shipped zip. No behaviour change when the bundle is healthy.

### 0.1.7

*Released 19 July 2026.*

- Command Centre quick actions. Arriving from "New invoice" or "New quote" in EP Dashboard 0.2.3 or later opens the New tab with the kind already selected.

### 0.1.6

*Released 19 July 2026.*

- The Send button now stays disabled for at least four seconds after a send completes, so repeated identical attempts in quick succession are no longer possible.
- A failed send now looks like a failure. A send with no transport was previously reported in green despite having failed; it is now red.

### Earlier releases

- Earlier releases covered the ledger postings, the gap-free numbering counter, the tax pack interface, the branded PDF and hosted invoice page, and the pay link.
