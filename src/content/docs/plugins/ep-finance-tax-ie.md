---
title: "EP Finance Tax IE"
description: "Ireland tax pack for EP Finance. VAT3 boxes per bi-monthly period on the invoice or cash-receipts basis, an annual RTD by rate band, a registration-threshold watch, a Form 11 mapping export and the ROS deadline calendar."
---

EP Finance Tax IE turns what is already in your ledger into the figures an Irish VAT3 asks for.

This page documents EP Finance Tax IE **0.1.3**.

Published by [ElmsPark Studio](https://elmspark.com).

:::caution[It prepares figures, it does not file them and does not give tax advice]
This plugin computes figures from your own records so you or your accountant can file. It does not submit anything to Revenue, and it gives no tax advice. Check the numbers with your adviser before you file.
:::

## Requirements

- **PageMotor 0.9b or later**
- **[EP Finance](/plugins/ep-finance/)**, which holds the ledger these figures are computed from

## The VAT3

T1 output, T2 input, and T3 payable or T4 repayable, plus E1, E2, ES1 and ES2 for intra-EU movements and PA1 for postponed accounting. Computed per bi-monthly period, on either the invoice basis or the cash-receipts basis.

## The annual RTD

The Return of Trading Details, broken down by rate band, built from the same ledger the VAT3 came from so the two cannot disagree.

## Watching the registration thresholds

If you are not registered yet, the plugin watches your rolling turnover against the €42,500 services and €85,000 goods thresholds and warns you as you approach, amber then red. Crossing a threshold without noticing is expensive, and it is the sort of thing a background check should be doing rather than you.

## Form 11

A category mapping export that lines your ledger categories up with the Form 11 headings, for the self-assessment return.

## Deadlines

The calendar, with both dates: the 19th for paper filing and the 23rd for ROS.

:::note[No direct ROS integration]
Files are prepared for you or your accountant to upload. The plugin does not connect to ROS.
:::

## Changelog

### 0.1.3

*Released 1 September 2026.*

- Some of this plugin's actions used to appear as their own entries in the tool list of any connected AI client. That surface is reserved for PageMotor itself, so those entries have been removed.
- **Nothing became unreachable and nothing else changed.** Every action still works exactly as before through PageMotor's own dispatch, with identical responses. Only a caller that had been invoking one of those names directly is affected, and it should dispatch through PageMotor instead.
