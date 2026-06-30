---
title: "EP Studio Dashboard"
description: "The owner's operations command centre for a multi-location studio business. One live screen for revenue, members, bookings, attendance, class passes, waivers and payroll."
---

EP Studio Dashboard is the owner's operations command centre for a multi-location class-based studio. It composes one full-width, live screen from the whole EP studio suite, so the person running the business can see the state of it at a glance.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

One screen brings together:

- **Revenue** with a 30-day trend and period-on-period change.
- **Members**: active count, new joiners, and a churn watch-list of who is past due or set to cancel.
- **Bookings and attendance** across every studio, with fill bars for the next seven days.
- **Class-pass liability**: outstanding credits and passes expiring soon.
- **Waivers**: coverage, and the unsigned-before-the-mat gaps.
- **Payroll due** to instructors, and who is teaching today.

You can switch the date range (today / 7 days / 30 days / custom) and every panel refreshes without a reload, drill into any number to the list behind it, and run the safe one-click actions (sweep expired passes, grant a comp pass, generate and approve payroll).

It is a read-only aggregator over the rest of the suite. It owns no tables and degrades gracefully as sibling plugins are added or removed.

## Conversational access

The whole dashboard is also exposed as read-only PageMotor API actions and MCP tools (`studio_overview` and friends), so an owner can point an LLM at the site and ask about the business in plain language. The companion **EP Studio Assistant** plugin builds an Ask box on top of these directly inside the Admin.

## Requirements

- **PageMotor 0.8.3b or later**
- The EP studio suite siblings (EP Events, EP Class Passes, EP Waivers, EP Instructors, EP Ecommerce) for the panels that read them

## Installation

1. Download `ep-studio-dashboard.zip` from the [EP Suite downloads page](https://updates.elmspark.com/download.php?plugin=ep-studio-dashboard).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **EP Suite nav → Dashboard**. Set your operating timezone in the settings group so "today" and "this month" are measured correctly.

## Changelog

### 2.1.1

The remaining read-only actions (`studio_revenue`, `studio_waiver_gaps`, `studio_expiring_passes`, `studio_payroll_due`) now surface as native MCP tools, so an LLM connected to the site lists them directly.

### 2.1.0

Exposed the whole dashboard as read-only PageMotor API actions / MCP tools (`studio_overview` and friends).

### 2.0.0

The full interactive command centre: live panels, a switchable date range, drill-downs, and safe one-click actions.
