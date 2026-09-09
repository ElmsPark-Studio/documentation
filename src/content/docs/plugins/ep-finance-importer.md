---
title: "EP Finance Importer"
description: "Bank statement import for PageMotor. Mapping profiles for the common UK and Irish banks, a preview that catches sign-flips, hash dedup so a re-import cannot double-post, a rules engine with a review queue, and reconciliation."
---

EP Finance Importer brings in the money your website never saw: the bank statement. It reads a CSV, works out what each line is, and posts it into the ledger without ever posting it twice.

This page documents EP Finance Importer **0.1.5**.

Published by [ElmsPark Studio](https://elmspark.com).

:::caution[It prepares figures, it does not give tax advice]
This plugin computes and presents figures from the records you and your other plugins put into the ledger. It is not an accountant and gives no tax or accounting advice, and it does not file anything on your behalf. Check your figures with your own adviser before submitting a return.
:::

## Requirements

- **PageMotor 0.9b or later**
- **[EP Finance](/plugins/ep-finance/)**, which holds the ledger this plugin reads and writes

## Mapping profiles

Every bank exports a different CSV. The plugin ships profiles for AIB, Bank of Ireland, Revolut, Barclays, Monzo and Chase, and you can define your own for anything else: point it at which column is the date, which is the amount, which is the description, and it remembers.

## The sign-flip trap, and why the preview exists

Banks disagree about what a positive number means. Some write money leaving your account as a positive figure, some as a negative one. Get it backwards and every expense becomes income.

So nothing posts straight from the file. The preview shows you what the plugin thinks each line is, anchored against the statement's own opening and closing balance. If the signs are inverted the totals will not reconcile and you will see it before anything reaches the book.

## A re-import can never double-post

Every imported line is fingerprinted from the account, date, amount and description. Import the same statement twice, or overlap two exports by a fortnight, and the lines already in the book are recognised and skipped. This is what makes the import safe to retry when you are not sure whether it worked.

## Rules and the review queue

A rule matches on the description and assigns a category, so your regular payments file themselves. Anything no rule matches goes to a review queue rather than being guessed at. You clear the queue; nothing is categorised behind your back.

## Statements and reconciliation

Import a statement, tell the plugin its opening and closing balance, and it will tell you whether the lines add up. Once a statement is closed the lines inside it are locked, which is what stops a reconciled figure being edited later.

## Bringing in history

There is a separate migration screen for loading prior months or years, kept apart from routine importing so a large historical load cannot be confused with this month's statement.

## Changelog

### 0.1.5

*Released 6 August 2026.*

- Hardening: if the plugin's bundled shared file is ever missing or damaged, the plugin now stands down quietly instead of taking the site down with it. No change when everything is healthy.
