---
title: "EP Finance Autopilot"
description: "The AI bookkeeper loop for PageMotor. Suggests categories for anything unmatched, learns from your corrections, emails a weekly digest with one-tap approval, and never moves money itself."
---

EP Finance Autopilot works through the review queue so you do not have to. It suggests; you approve. It never changes a figure on its own.

This page documents EP Finance Autopilot **0.1.7**.

Published by [ElmsPark Studio](https://elmspark.com).

:::caution[It prepares figures, it does not give tax advice]
This plugin computes and presents figures from the records you and your other plugins put into the ledger. It is not an accountant and gives no tax or accounting advice, and it does not file anything on your behalf. Check your figures with your own adviser before submitting a return.
:::

## Requirements

- **PageMotor 0.9b or later**
- **[EP Finance](/plugins/ep-finance/)**, which holds the ledger this plugin reads and writes
- **[EP Finance Importer](/plugins/ep-finance-importer/)**, which owns the review queue this works through
- **[EP Email](/plugins/ep-email/)** if you want the weekly digest

## What it will and will not do

:::note[It never moves money]
Autopilot only ever drafts a suggestion. It cannot create, edit or delete a transaction, and every change is applied by a person. This is a deliberate boundary, not a limitation waiting to be lifted.
:::

## How it suggests

History first. If you have categorised the same payee the same way three times, that is a better signal than anything a language model will tell you, and it costs nothing. An AI provider is used only where configured, and only where history has nothing to offer.

## The weekly digest

Once a week you get an email listing what is waiting, with a one-tap approve link per item. Those links are signed and single-use, so one cannot be reused or altered to approve something else.

## Learning from your corrections

When you correct a suggestion, the plugin proposes a rule. A rule is not switched on until you have accepted it three times, so a one-off does not become a standing instruction. Once a month it reviews the rules it has and reports any that have stopped matching reality.

## Knowing whether it is any good

There is a scoreboard: how often its suggestions were accepted, and how that is trending. If the accuracy is poor you will see it rather than having to sense it.

## Driving it conversationally

The same loop is exposed to any connected AI client, so you can work through the queue by talking to it instead of clicking. The same rule applies there: it suggests, you approve.

## Changelog

### 0.1.9

- **Fixes stored keys and passwords reading as empty after a PageMotor 0.11.3 or 0.11.4 update.** After the core update, every secret this plugin had encrypted at rest came back blank, so anything that needed it failed with an authentication error until the value was typed in again. Nothing was deleted: the encrypted value was still in the settings row, but PageMotor 0.11.3 moved the site secret that opens it, and this plugin was still looking in the old place. It now finds the secret in both places, so an existing value opens again without re-entry, and a value that was re-entered in the meantime keeps working and is moved back under the site secret.
- If you updated PageMotor and then re-entered a key or password, there is nothing to do. If you updated and have not re-entered it, this release restores it on the next page load.

### 0.1.8

- **Works with PageMotor 0.11.3 and stays compatible with earlier releases.** PageMotor 0.11.3 changed how a plugin declares its API and MCP actions, and a plugin that still uses the old declaration has every one of its actions silently dropped from the registry on that version. This release declares its actions in the shape the running PageMotor expects, so an AI connected over API or MCP keeps every action whether the site is on 0.11.3 or on an earlier release.
- **Actions are now grouped into families**, so a connected AI that looks up one action is shown its siblings.

### 0.1.7

*Released 1 September 2026.*

- Some of this plugin's actions used to appear as their own entries in the tool list of any connected AI client. That surface is reserved for PageMotor itself, so those entries have been removed.
- **Nothing became unreachable and nothing else changed.** Every action still works exactly as before through PageMotor's own dispatch, with identical responses. Only a caller that had been invoking one of those names directly is affected, and it should dispatch through PageMotor instead.
