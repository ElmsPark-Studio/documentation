---
title: "EP Finance Receipts"
description: "Snap-and-capture expense receipts for PageMotor. A mobile capture page, optional AI extraction, and matching that proposes a link to the bank line for you to confirm. Receipt images are never web-servable."
---

EP Finance Receipts turns the photo of a receipt into an expense before its bank line has even arrived.

This page documents EP Finance Receipts **0.1.8**.

Published by [ElmsPark Studio](https://elmspark.com).

:::caution[It prepares figures, it does not give tax advice]
This plugin computes and presents figures from the records you and your other plugins put into the ledger. It is not an accountant and gives no tax or accounting advice, and it does not file anything on your behalf. Check your figures with your own adviser before submitting a return.
:::

## Requirements

- **PageMotor 0.9b or later**
- **[EP Finance](/plugins/ep-finance/)**, which holds the ledger this plugin reads and writes

## Capture

A mobile-friendly page that opens the camera on a phone. Photograph the receipt when you get it, not three weeks later when you are trying to remember what it was for.

## Reading the receipt

If you have an AI provider configured, the plugin will attempt to read the payee, date, total and VAT from the image and fill the form in for you. If you have not, you type them. There is no dependency on AI: it is an assist, not a requirement, and you can correct anything it reads.

## Matching, never auto-linking

When the bank line for that receipt eventually arrives, the plugin looks for a match on a date window and an exact amount, and **proposes** it. It does not link them silently. You confirm, and only then is the image attached to the reconciled transaction.

This matters because a wrong automatic match is very hard to spot later and very easy to make: two similar amounts a day apart is all it takes.

## VAT evidence

A receipt with no VAT number on it is flagged as not being VAT evidence. That is a fact about the receipt, not a judgement about your return, and it is there so you find out before your accountant does.

## Receipt images are not on the web

Receipt photographs are financial personal data. They are never placed anywhere a browser can reach directly: the bytes live in the database or in a folder outside the web root, and they are streamed only through a handler that checks you are an administrator first.

There is a retention setting, and the plugin honours EP GDPR delete requests.

## Changelog

### 0.1.8

*Released 1 September 2026.*

- Some of this plugin's actions used to appear as their own entries in the tool list of any connected AI client. That surface is reserved for PageMotor itself, so those entries have been removed.
- **Nothing became unreachable and nothing else changed.** Every action still works exactly as before through PageMotor's own dispatch, with identical responses. Only a caller that had been invoking one of those names directly is affected, and it should dispatch through PageMotor instead.
