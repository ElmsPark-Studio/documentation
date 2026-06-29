---
title: "EP Class Passes"
description: "Pre-paid class credit packs for a studio. Credits tracked in an append-only ledger, with shelf-life expiry, auto-deduct at booking, and reinstatement on an in-policy cancel."
---

EP Class Passes adds pre-paid class credit packs to a studio, the classic 10-class pass. A pass is sold as an EP Ecommerce product, and its credits are tracked in an append-only ledger so the balance is always a sum, never a stored number that can drift.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Sold as a product.** A class pass is a new EP Ecommerce product type. Buying it issues a pass to the customer.
- **Append-only ledger.** Every change (purchase, redeem, reinstate, forfeit, expire, refund, admin adjust) is a ledger row. The balance is always computed.
- **Shelf-life expiry.** Passes can expire a fixed number of days from purchase, or from first use.
- **Eligibility.** A pass can be limited to specific class types.
- **Auto-deduct at booking.** When a member books a single class at the EP Events register, one credit is deducted automatically and the card is skipped entirely.
- **Fair cancellation.** An in-policy cancel reinstates the credit; a late cancel or no-show forfeits it.
- **Owner tools.** A member balance and history view, admin comp-grant and adjust, and a nightly expiry sweep with nudges.

## Requirements

- **PageMotor 0.8.3b or later**
- **EP Ecommerce 0.1.25 or later**
- **EP Events** for the booking auto-deduct

## Installation

1. Download `ep-class-passes.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Create a class-pass product in EP Ecommerce, set its credits, validity and eligible class types, and sell it like any other product.

## Changelog

### 1.2.1

`member_pass_history` now surfaces as a native MCP tool, so an LLM connected to the site lists it directly.

### 1.2.0

Member balance and history surface, the booking pre-payment hook for auto-deduct and reinstatement, and read-only API actions for an LLM.
