---
title: "EP Finance Tax UK"
description: "United Kingdom tax pack for EP Finance. The nine VAT100 boxes computed from the ledger under standard, cash accounting or Flat Rate, input VAT split into evidenced and unevidenced, an SA103 export and a deadline calendar."
---

EP Finance Tax UK turns what is already in your ledger into the figures a UK VAT return asks for.

This page documents EP Finance Tax UK **0.1.6**.

Published by [ElmsPark Studio](https://elmspark.com).

:::caution[It prepares figures, it does not file them and does not give tax advice]
This plugin computes figures from your own records so you or your accountant can file. It does not submit anything to HMRC, and it gives no tax advice. Check the numbers with your adviser before you file.
:::

## Requirements

- **PageMotor 0.9b or later**
- **[EP Finance](/plugins/ep-finance/)**, which holds the ledger these figures are computed from

## The nine boxes

All nine VAT100 boxes, computed straight from the ledger for whichever period you select, with a drill-down from any box to the transactions behind it. If a figure looks wrong you can see exactly which entries made it.

## Your scheme is a setting, never a guess

Standard, cash accounting or Flat Rate. You tell the plugin which scheme you are on; it never infers one from the shape of your data, because inferring it wrongly produces a return that looks plausible and is wrong.

## Evidenced and unevidenced input VAT

Input VAT is split into what you hold evidence for and what you do not. That distinction is the thing most likely to be questioned, and having it visible before you file is the point.

## Making Tax Digital, honestly

Your records are kept digitally, and the plugin produces a quarterly SA103 export for your accountant or your bridging software. It does **not** submit directly to HMRC. Direct filing is a clearly-future thing, not a hidden one, and this page will say so plainly until it exists.

## Deadlines

A calendar of your filing and payment dates, exportable as an .ics file so it lands in whatever you already use.

## Document stamps

Every accountant pack this plugin produces carries a stamp on its cover: a number and the first characters of a fingerprint taken over every other file in the pack.

If somebody sends you a pack, or you open one from a year ago, you can check whether its contents are exactly what was recorded when it was produced. The cover tells you how, in three steps with ordinary tools, because a verification scheme nobody can run is decoration.

**It is not a signature.** It says nothing about who produced the pack, only whether the contents have changed since. Anyone with access to the database could write a matching record. It protects against accident, drift and quiet edits, not against a determined party with that access, and the cover says so in those words.

Regenerating a pack records a new stamp rather than replacing the old one, so the history itself shows when a period's figures moved between one generation and the next.

## Changelog

### 0.1.6

*Released 9 September 2026.*

- **Every accountant pack now carries a document stamp.** The cover page prints a stamp number and the first characters of a fingerprint taken over every other file in the pack, so you can check whether a pack's contents are exactly what was recorded when it was produced.
- **The cover explains how to check it by hand**, in three steps using ordinary tools.
- **It is not a signature.** It says nothing about who produced a pack, only whether the contents have changed since.
- **Regenerating a pack records a new stamp rather than replacing the old one**, so the history shows when a period's figures moved between generations.
- Requires EP Finance 0.6.0 or later. With anything older the pack is produced exactly as before, without a stamp block.

### 0.1.5

*Released 1 September 2026.*

- Some of this plugin's actions used to appear as their own entries in the tool list of any connected AI client. That surface is reserved for PageMotor itself, so those entries have been removed.
- **Nothing became unreachable and nothing else changed.** Every action still works exactly as before through PageMotor's own dispatch, with identical responses. Only a caller that had been invoking one of those names directly is affected, and it should dispatch through PageMotor instead.
