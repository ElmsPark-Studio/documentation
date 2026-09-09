---
title: "EP Finance"
description: "A double-entry ledger for a PageMotor site that keeps its own books. Accounts, categories, transactions with splits, registers with running balances, profit and loss, cash flow, seeded UK, Ireland and US charts, and a nightly audit that proves the book adds up."
---

EP Finance is the book. It holds your accounts, records every transaction as a balanced double entry, and reports on the result. The rest of the finance family sits on top of it.

This page documents EP Finance **0.3.5**.

Published by [ElmsPark Studio](https://elmspark.com).

:::caution[It prepares figures, it does not give accounting advice]
EP Finance records and reports what you and your other plugins put into it. It is not an accountant and gives no tax or accounting advice. Check your figures with your own adviser before filing anything.
:::

## Requirements

- **PageMotor 0.9b or later**

Nothing else. EP Finance is the base of the family; the other finance plugins require it, not the other way round.

## What it gives you

| | |
|---|---|
| **Accounts** | Your chart of accounts, in four classes: asset, liability, revenue and expense |
| **Categories** | What a line was for, kept separate from which account it moved through |
| **Transactions** | Every entry is a group of two or more splits that must balance to zero |
| **Registers** | Per-account listings with a running balance |
| **Profit and loss** | Built on the category tree, with drill-down to the transactions behind any figure |
| **Cash flow** | Money in and out over a period |
| **Seeded charts** | Sensible starting charts for the UK, Ireland and the United States |
| **Nightly audit** | Re-checks the whole book and reports anything inconsistent |

## Money is never a decimal

Every amount is held as a whole number of pence or cents. Nothing is stored as a fraction, so nothing drifts by a penny after a few hundred additions. This is the single most important decision in the plugin and everything else is built on it.

## One door in, and what it enforces

Every write goes through one gateway. Nothing writes to the book around the side, including the other finance plugins. That gateway refuses anything that would leave the book inconsistent:

- **A transaction must balance.** Splits sum to exactly zero, or it is refused. A single-legged entry is rejected by name as an orphan.
- **Transfers pair up.** Money moving between two of your own accounts is recorded as two matching legs.
- **The same thing cannot post twice.** Anything arriving from another plugin carries an identifier from its source, so a repeated import, a re-run sweep or a retried webhook is a no-op rather than a duplicate.
- **A reconciled line cannot be quietly edited.** Once a split is matched to a closed bank statement it is immutable until you deliberately unlock that statement.

The nightly audit re-checks all of this across the whole book and tells you if anything has slipped.

## Working in more than one currency

Optional, and off unless you turn it on.

A transaction entered in a foreign currency carries the exchange rate you gave it and converts once, at the moment it is posted. Reports are in your book currency, a bank account's own register is in that bank's currency, and the difference that appears when a foreign invoice finally settles is recorded as a realised gain or loss.

A rate is never guessed. If you have not supplied one, the plugin asks rather than inventing a number.

## The rest of the family

EP Finance holds the book. These add to it, and each needs it:

- **EP Finance Invoicing** issues quotes and invoices and posts the result
- **EP Finance Importer** brings in bank statements and reconciles them
- **EP Finance Receipts** captures expense receipts and matches them to bank lines
- **[EP Finance Sources](/plugins/ep-finance-sources/)** posts orders, bookings, ticket sales and instructor pay automatically
- **EP Finance Autopilot** suggests categories for anything unmatched, and you approve
- **Tax packs** for the UK, Ireland and the United States prepare the figures for your return

## Changelog

### 0.3.5

*Released 1 September 2026.*

- Four of this plugin's actions used to appear as their own entries in the tool list of any connected AI client. That surface is reserved for PageMotor itself, so those entries have been removed.
- **Nothing became unreachable and nothing else changed.** Every action still works exactly as before through PageMotor's own dispatch, with identical responses. Only a caller that had been invoking one of those names directly is affected, and it should dispatch through PageMotor instead.

### 0.3.4

*Released 6 August 2026.*

- Hardening: if the plugin's bundled shared file is ever missing or damaged, the plugin now stands down quietly instead of taking the site down with it. No change when everything is healthy.
