---
title: "EP Finance Tax US"
description: "United States tax pack for EP Finance. A Schedule C prep report, a quarterly estimated-tax worksheet that shows its arithmetic, contractor tracking with a 1099-NEC report, and sales-tax prep with a nexus watch."
---

EP Finance Tax US turns what is already in your ledger into the figures a US federal return asks for, and keeps an eye on where you might be creating a sales-tax obligation.

This page documents EP Finance Tax US **0.1.3**.

Published by [ElmsPark Studio](https://elmspark.com).

:::caution[It prepares figures, it does not file them and does not give tax advice]
This plugin computes figures from your own records so you or your preparer can file. It does not submit anything to the IRS or to any state, and it gives no tax advice. Check the numbers with your adviser before you file.
:::

## Requirements

- **PageMotor 0.9b or later**
- **[EP Finance](/plugins/ep-finance/)**, which holds the ledger these figures are computed from

## Schedule C

Per-line totals for the Schedule C, with a warning list naming any category that is not yet mapped to a line. An unmapped category is the usual cause of a total that does not match expectations, so it is surfaced rather than quietly dropped.

## Quarterly estimated tax, with the arithmetic shown

A worksheet rather than a single number: self-employment tax at 15.3%, the deduction for the employer half, and both the 100% and 110% safe harbours, each step visible. You should be able to see why the figure is what it is, and hand the working to somebody else.

## Contractors and the 1099-NEC

Payments to contractors are tracked through the year, with a year-end report of anyone over the $2,000 threshold that applies for 2026.

## Sales tax

A per-state filing prep, plus a nexus watch that measures your activity against a shipped table of state thresholds, so you are told when you are approaching an obligation in a state rather than discovering it afterwards. The threshold file is updatable.

Stripe Tax figures can be ingested where you use it, behind a feature flag.

:::note[No rate engine, no payroll, no filing]
This is preparation, not automation. It does not calculate live sales-tax rates at checkout, it does not run payroll, and it does not file.
:::

## Changelog

### 0.1.3

*Released 1 September 2026.*

- Some of this plugin's actions used to appear as their own entries in the tool list of any connected AI client. That surface is reserved for PageMotor itself, so those entries have been removed.
- **Nothing became unreachable and nothing else changed.** Every action still works exactly as before through PageMotor's own dispatch, with identical responses. Only a caller that had been invoking one of those names directly is affected, and it should dispatch through PageMotor instead.
