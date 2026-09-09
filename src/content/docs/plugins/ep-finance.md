---
title: "EP Finance"
description: "A double-entry ledger for a PageMotor site that keeps its own books. Accounts, categories, transactions with splits, registers with running balances, profit and loss, cash flow, seeded UK, Ireland and US charts, and a nightly audit that proves the book adds up."
---

EP Finance is the book. It holds your accounts, records every transaction as a balanced double entry, and reports on the result. The rest of the finance family sits on top of it.

This page documents EP Finance **0.5.0**.

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

## Closing a period

Once you have filed a return, close the book up to that date. Set **Book closed up to and including** on the settings screen and anything dated on or before it is refused: it cannot be posted, edited or deleted. Leave it empty and nothing is locked, which is how a book behaves until you choose otherwise.

The date is inclusive, the way an accountant reads it. Closing at 31 August closes the 31st itself, not just everything before it.

### Why this matters more than it sounds

Before this existed, the only thing the book protected was a transaction reconciled against a closed bank statement. Most postings never go through that path, so a manual journal entry or an invoice posting stayed editable forever, including after a VAT return had been filed on it. The return could be computed today and the figures underneath it changed next month, with no error and no trace.

### The override password

Optional. Set one and somebody who knows it can still post into a closed period when there is a genuine reason to. Leave it unset and the closed period cannot be written to at all, by anyone, until you move the date. Removing it later is one click.

It is stored as a one-way hash, so it cannot be recovered, only replaced, and it is set with its own button rather than a settings box so it never travels through a saved form.

### What it does not do

It does not stop you resetting the whole book, which is a deliberate exclusion: that is a factory reset with its own confirmation, and guarding it would make a book that has ever been closed impossible to reset.

Routine work is unaffected. Anything already posted stays recognised as already posted, so re-running an import or a sweep over a closed month is the same harmless no-op it has always been.

## The change history

Every change made to the book through EP Finance is recorded: what changed, who changed it, when, and what the value was before. It appears on the Audit tab, under the consistency check.

### It answers a different question from the audit above it

These two are easy to confuse and they are not the same thing.

The **consistency audit** asks whether the book adds up right now. The **change history** asks how it got to be this way. A book can be perfectly consistent and still have had a figure quietly changed after a return was filed on it, which is exactly the case where the audit tells you nothing useful and the history tells you everything.

### What it catches that a total does not

The obvious ones are amounts. The useful ones are the changes that move a figure without touching an amount at all:

- Moving a transaction to a different category, which shifts money between profit and loss lines
- Renaming or reclassifying an account
- Unlocking a bank statement, which makes its reconciled lines editable again

Each of those leaves the arithmetic intact and changes what your reports say.

### Attribution

Every entry names a person, or names **system** where there was no person, for a scheduled job or an automatic posting. It is never left blank, so an entry with no name would itself be a sign something was wrong rather than routine.

### What it does not claim

It records changes made **through EP Finance**. Somebody with direct database access editing a table by hand is outside what any plugin can see, and this does not pretend otherwise. Part of that gap is covered separately: the plugin installs database-level guards that refuse a direct change to a reconciled transaction, where your host permits them.

Nothing is deleted automatically. There is no retention period, because you cannot tell a clean history from a pruned one. Trimming old entries is possible and is always your decision.

## The rest of the family

EP Finance holds the book. These add to it, and each needs it:

- **EP Finance Invoicing** issues quotes and invoices and posts the result
- **EP Finance Importer** brings in bank statements and reconciles them
- **EP Finance Receipts** captures expense receipts and matches them to bank lines
- **[EP Finance Sources](/plugins/ep-finance-sources/)** posts orders, bookings, ticket sales and instructor pay automatically
- **EP Finance Autopilot** suggests categories for anything unmatched, and you approve
- **Tax packs** for the UK, Ireland and the United States prepare the figures for your return

## Changelog

### 0.5.0

*Released 9 September 2026.*

- **The book now keeps a change history: who changed what, when, and what it was before.** It appears under the existing consistency check on the Audit tab.
- **This answers a different question from the nightly audit.** The audit says whether the book adds up now. The history says how it got that way. A book can be consistent and still have had a figure quietly changed after a return was filed on it.
- **Every change is attributed to a person, or explicitly to "system".** Never blank, so an unattributed entry would itself be a signal.
- **It catches the changes that move a figure without touching an amount**: recategorising a transaction, reclassifying an account, and unlocking a statement so its reconciled lines become editable again.
- **A reset of the whole book is recorded, and the history survives it.**
- Nothing is deleted automatically and there is no retention period, because you cannot tell a clean history from a pruned one.

### 0.4.0

*Released 9 September 2026.*

- **You can now close the book at a date, so a filed figure cannot change behind your back.** Anything dated on or before the closing date is refused: it cannot be posted, edited or deleted. Leave the setting empty and nothing is locked.
- **The date is inclusive**, the way an accountant reads it: closing at 31 August closes the 31st itself.
- **An optional override password**, if you want one, stored as a one-way hash and set through its own button rather than a settings box. Leave it unset and the closed period cannot be written to at all until you move the date.
- **Routine re-imports and sweeps are unaffected.** Anything already posted stays recognised as already posted, so re-running an import over a closed month is the same harmless no-op it has always been.

### 0.3.5

*Released 1 September 2026.*

- Four of this plugin's actions used to appear as their own entries in the tool list of any connected AI client. That surface is reserved for PageMotor itself, so those entries have been removed.
- **Nothing became unreachable and nothing else changed.** Every action still works exactly as before through PageMotor's own dispatch, with identical responses. Only a caller that had been invoking one of those names directly is affected, and it should dispatch through PageMotor instead.

### 0.3.4

*Released 6 August 2026.*

- Hardening: if the plugin's bundled shared file is ever missing or damaged, the plugin now stands down quietly instead of taking the site down with it. No change when everything is healthy.
