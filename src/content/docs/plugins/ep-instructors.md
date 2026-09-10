---
title: "EP Instructors"
description: "Instructors as first-class records for a class-based studio: roster, public bio pages with live upcoming classes, pay-rate rules, snapshot pay-lines, and a payroll CSV."
---

EP Instructors makes the people who teach your classes first-class records. It carries the roster, public bio pages, the pay-rate rules, and a one-button payroll export for the bookkeeper. It never moves money; payroll is an export, not a payment.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Roster.** Each instructor has specialisms and a home studio.
- **Public bio pages.** A bio block shows an instructor's real upcoming classes, pulled live from the schedule.
- **Pay-rate rules.** Flat, base plus per-head bonus, or a cover premium, scoped by class type and location with effective dates.
- **Snapshot pay-lines.** At class close, a pay-line is written from the attended head-count, so payroll reflects who actually showed up.
- **Payroll CSV.** One button exports the pay-lines for a period for your bookkeeper.

It integrates with EP Events (the schedule) and EP Events Recurring (cover overrides).

## Requirements

- **PageMotor 0.8.3b or later**
- **EP Events 1.0.23 or later** for the schedule

## Installation

1. `ep-instructors.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **EP Suite nav → Instructors**, add your instructors, and set their pay-rate rules.

## Changelog

### 1.1.15

- **Corrects the PageMotor 0.11.3 preparation shipped in 1.1.14.** That release grouped this plugin's API and MCP actions into families, but in a shape PageMotor 0.11.3 does not accept. On 0.11.3 the plugin would have registered none of its actions, and nothing on screen would have said so.
- This version uses the shape 0.11.3 expects, and keeps the earlier shape for sites still on an older PageMotor. One build serves both, so there is no order you have to update things in.
- Safe to install now. Nothing you can see changes.

### Changed

- **Roster Active control is now an obvious on/off toggle switch.** Previously the inactive state ("— Inactive") read like plain text, so it wasn't clear you could click it to show a teacher. It is now a labelled switch (green = active/shown, grey = inactive/hidden) with a state-aware tooltip ("click to hide…" / "click to show…") and a keyboard-accessible `role="switch"`.

### Fixed

- **Roster Active/Inactive toggle (and the other admin buttons) jumped to the bare "Manage Plugins" page.** After an action succeeded, the admin JS called `window.location.reload()`, which re-requested `/admin/plugins/` as a GET and lost the POST that opens this plugin's panel, dropping you on the plugin list. It now re-opens the EP Instructors panel after each action. All admin buttons are also explicitly `type="button"` so they can never submit the surrounding settings form.

### Added

- **Pay rates → Class type is now a pickable list.** The field is a combobox populated from the class types on your schedule (you can still type a new one, or leave it blank for "any").
- **Payroll → Export .md.** A Markdown payroll report alongside the CSV, written for pasting into an LLM to analyse: a context preamble, per-instructor totals, and the full pay-line table. (Markdown over JSON here — it is self-describing, LLMs read MD tables reliably, and it stays human-readable; the CSV remains for the bookkeeper.)

### Changed

- **Settings → Currency is now a dropdown** of common symbols (with an "Other…" option to type your own) instead of a free-text box.

### Fixed

- **EP Studio Dashboard could not generate or approve payroll (fatal).** Its one-click "Generate pay-lines" and "Approve all pending" buttons call this plugin's `generate_paylines()` / `approve_paylines()` directly on the resolved instance, but both methods were `private`, so PHP threw "Call to private method … from scope EP_Studio_Dashboard". They are now `public` (matching how the dashboard already calls EP Class Passes' public operations). No change is needed in EP Studio Dashboard.

### Changed

- **Currency is no longer hard-coded to US dollars.** A new Settings section lets you set the currency symbol shown before every amount (pay rates, pay-lines, payroll totals). It defaults to **£**. The exported payroll CSV stays symbol-free for the bookkeeper.
- **Dates display in a friendlier, locale-aware way.** Stored dates now show as e.g. "17 Jun 2026" instead of "2026-06-17", and the payroll From/To boxes are native date pickers that follow your browser's local format. Values are still stored as ISO dates internally.

### Fixed

- **New instructors were created hidden, so `[instructors]` showed nothing and `[instructor slug="…"]` said "Instructor not found".** The Add-instructor form never sent an `active` flag, and the save defaulted a missing flag to inactive, so every teacher added through the admin landed inactive — and both public shortcodes only show active teachers. New instructors are now active by default, and an explicit flag is still honoured. (Verified live on the dev rig: add via the form → row is `active=1` → grid + bio render.)

### Added

- **Active toggle in the roster.** Each teacher row now has a one-click Active/Inactive toggle, so an inactive teacher can be shown (or any teacher hidden) without touching the database. This also recovers any instructor added on 1.1.2 or earlier that is stuck inactive.

### Changed

- **Clearer pay-rate labels.** The Pay rates section now explains what a rate rule is, the "Over" column is labelled "Bonus after", "Cover +" is "Cover bonus", and the add-rate fields carry plain-English placeholders and tooltips.

### Fixed

- **Version badge missing from the admin header.** The plugin never defined its `EP_INSTRUCTORS` root constant (so `ep_version()` could not locate the plugin file), and the header `Version:` line sat past byte 500 behind a long `Description:` line, beyond the window `ep_version()` reads. The constant is now defined and the header fields are reordered so `Version:` comes first.
### 1.1.1

`instructor_upcoming` now surfaces as a native MCP tool, so an LLM connected to the site lists it directly.

### 1.1.0

The instructor roster, pay-rate rules, snapshot pay-lines, the payroll CSV, and read-only API actions for an LLM.
