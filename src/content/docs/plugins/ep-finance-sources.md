---
title: "EP Finance Sources"
description: "Auto-posting bridges into the EP Finance ledger. Orders, subscription renewals, bookings and ticket sales post themselves as income, and approved instructor pay-lines post as cost, each with an id that makes a re-run harmless."
---

EP Finance Sources is the plumbing between the plugins that take money, or owe it, and the book that records it. Nothing here is typed in twice.

This page documents EP Finance Sources **0.2.0**.

Published by [ElmsPark Studio](https://elmspark.com).

:::caution[It prepares figures, it does not give accounting advice]
EP Finance Sources records what your other plugins already know. It is not an accountant and gives no tax or accounting advice. Check your figures with your own adviser before filing anything.
:::

:::note[Supplied with the finance family, not installed on its own]
EP Finance Sources does nothing without **EP Finance**, which owns the ledger it posts into. If EP Finance is not active the plugin stays dormant rather than erroring. It is supplied and configured alongside EP Finance rather than picked up on its own.
:::

## Requirements

- **PageMotor 0.9b or later**
- **EP Finance**, which provides the ledger, the accounts and the single write gateway every posting goes through
- Whichever sources you want to bridge: [EP Ecommerce](/plugins/ep-ecommerce/), [EP Ecommerce Subscriptions](/plugins/ep-ecommerce-subscriptions/), [EP Booking](/plugins/ep-booking/), [EP Events](/plugins/ep-events/), [EP Instructors](/plugins/ep-instructors/). Any that are not installed are simply skipped

## What it bridges

| Source | What posts | Direction |
|---|---|---|
| **EP Ecommerce** | Orders when fulfilled, and refunds as an exact reversal | Income |
| **EP Ecommerce Subscriptions** | Renewals | Income |
| **EP Booking** | Booking payments and refunds | Income |
| **EP Events** | Ticket sales | Income |
| **EP Instructors** | Approved and paid pay-lines | Cost |
| **Stripe** (optional) | Processing fees, synced in bulk | Cost |

## Instructor pay

EP Instructors already works out what each instructor is owed for every class taught. Until now that figure only left the plugin as a CSV somebody had to retype into the accounts. It now posts itself.

Each approved pay-line is recorded as a cost against **the class it was earned on**, not the day it happened to be approved. A class taught in August stays an August cost even if the pay-line is approved in September, so a profit and loss report, or a VAT period built on it, covers what actually happened in that period.

### Money owed and money paid are kept apart

A pay-line marked paid tells us the studio considers it settled. It does not tell us which bank account paid it, on what date, or whether a single payment covered five classes.

So the plugin records the **cost**, and leaves the **amount owed** standing. That amount clears when the real payment arrives on your bank statement and is imported through EP Finance Importer.

This is deliberate. Your bank statement stays the one place that says money left the business, which is also what stops the same wage being counted twice: once when it was approved, and again when it was paid.

### If an approved amount later changes

You are told, and nothing is altered. The sweep reports the pay-line, the figure currently in the book, and the figure now, and leaves the book alone. Changing a wage after it was approved is a bookkeeping decision, not something a background job should quietly make for you.

## Nothing is ever posted twice

Every posting carries an identifier derived from the thing it came from. Re-running a sweep, or running a backfill over a period you have already done, changes nothing. This is what makes the buttons safe to press whenever you are unsure.

Pay-lines still waiting for approval are never posted.

## Settings

| Setting | What it does |
|---|---|
| **Source toggles** | Turn any bridge off if you never want it posting to the book |
| **Account mapping overrides** | Point any of the accounts it uses at one of your own, if you already keep a real chart of accounts |
| **Stripe feed** | Off by default. A Stripe key (a restricted key with read access to Balance transactions is enough, stored encrypted), the date the first sync reads from, and a bank account for payouts. "Preview: Stripe feed" shows what would be posted without posting; "Sync: Stripe feed" posts |

The plugin creates the accounts and categories it needs the first time you press **Set up default accounts and categories**. Everything is saved with PageMotor's own Save button.

## Running a sweep

Orders post the moment they are fulfilled. The other sources are swept, nightly where EP Cron is available, and on demand from the buttons on the settings screen. There is a button per source and one for all of them.

## Changelog

### 0.3.0

*Released 17 September 2026.*

- **Money that never went through an EP plugin now reaches the book.** A Stripe invoice paid by a client, a payment link, a charge made from the Stripe Dashboard, and every payout to your bank used to be invisible to EP Finance, because every source here started from an EP plugin's own record. The new Stripe feed reads your Stripe balance and posts each movement as its own entry: payments, refunds, payouts and Stripe's own fees.
- **Payment fees are split per payment, not swept in bulk.** Each Stripe payment posts the gross to sales, the fee to payment processing and the net to the Stripe balance, from Stripe's own figures for that payment.
- **Payouts move money from the Stripe balance to a bank account** the plugin creates for you ("Bank account (Stripe payouts)"), or one you already keep, so the Stripe balance in the book tracks the one in your Dashboard.
- **A preview button shows what would be posted before anything is.** "Preview: Stripe feed" reads the balance and lists every transaction with what the feed would do with it; "Sync: Stripe feed" posts. The nightly sweep includes the feed once it is switched on.
- **Nothing is counted twice.** A payment that EP Ecommerce already booked is recognised by its Stripe reference and skipped. Re-running a sync, or overlapping the last one, changes nothing.
- **Nothing is guessed.** A transaction in a currency the book does not keep is skipped and listed for you unless a rate provider can supply that day's rate. Disputes, adjustments and transfers are counted and reported by type for a human to post.
- **The Stripe key is yours to give, and stored encrypted.** A restricted key with read access to Balance transactions is enough; the feed never writes to Stripe. Off until you switch it on.

### 0.2.0

*Released 9 September 2026.*

- **Instructor pay now reaches the book on its own.** EP Instructors already worked out what each instructor is owed for every class taught, but that figure only ever left the plugin as a CSV somebody had to retype into the accounts. Approved and paid pay-lines are now posted for you, as a cost against the class they were earned on.
- **Each posting is dated to the class, not to the day it was processed.** A class taught in August stays an August cost even if the pay-line is approved in September, so a profit and loss report, or a VAT period built on it, covers what actually happened in that period.
- **Money owed and money paid are kept apart, on purpose.** A pay-line marked paid tells us the studio considers it settled. It does not tell us which bank account paid it, on what date, or whether one payment covered five classes. So the cost is recorded and the amount owed is left standing, to be cleared against the real bank line when it comes in through EP Finance Importer. Your bank statement stays the single source of truth for money leaving, which is also what stops the same wage being counted twice.
- **Nothing is ever posted twice.** Re-running a sweep, or running a backfill over a period already done, changes nothing. Pay-lines still awaiting approval are never posted.
- **If an approved amount later changes, you are told rather than quietly corrected.** The sweep reports the pay-line, the figure in the book, and the figure now, and leaves the book alone.
- New setting to turn the bridge off, two new account mapping overrides if you already keep your own chart of accounts, and a "Sweep: Instructor pay" button alongside the existing ones.
- Nothing changes for the existing EP Ecommerce, Subscriptions, Booking or Events bridges.
