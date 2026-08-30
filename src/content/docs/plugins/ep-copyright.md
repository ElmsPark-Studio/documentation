---
title: "EP Copyright"
description: "A copyright line that keeps its own year right. Two shortcodes, no settings required, nothing to remember every January."
---

EP Copyright puts a copyright notice in your footer that never goes out of date. Drop one shortcode in and it writes the symbol, the current year and your business name, and it stays correct every January without anyone touching it.

Published by [ElmsPark Studio](https://elmspark.com).

## Why this exists

A year typed into a footer is a small time bomb.

It is correct on the day it is written. A year later it is wrong, and nobody notices, because nobody reads their own footer. Two years later a visitor lands on the site, sees a year that has clearly not moved, and quietly concludes the business has stopped trading. That is a real cost, paid by the one page element nobody is watching.

The usual answers are both bad. Remembering to update it every January means it will eventually be forgotten. Leaving the year off entirely avoids the rot, but throws away a genuine signal that somebody is still here and still minding the shop.

Neither trade-off is necessary. The year is one line of arithmetic.

## Usage

The whole line:

```
[ep-copyright]
```

renders as:

> © 2026 Your Business

Just the year, if you would rather build the sentence yourself:

```
[ep-year]
```

renders as:

> 2026

## Options

Every option is optional. Set them once on the settings screen and the bare `[ep-copyright]` uses them, or pass them per use to override.

| Option | What it does |
|---|---|
| `name` | Your business name. Defaults to your site title. |
| `from` | The year you started. Renders a range instead of a single year. |
| `symbol` | Defaults to `©`. Use `(c)` or anything else you prefer. |
| `suffix` | Words after the name, such as `All rights reserved`. |
| `tz` | A timezone, such as `Europe/Dublin`. See below. |

For example:

```
[ep-copyright name="JR Carpentry & Construction" from="2022" suffix="All rights reserved"]
```

renders as:

> © 2022–2026 JR Carpentry & Construction · All rights reserved

## About the range

`from` shows how long you have been going, which is worth saying if it has been a while.

It only renders a range when a range makes sense. If the year you give is this year, in the future, or before 1990, you get a single current year instead. A typo produces a sensible line rather than `2026–2026` or `2099–2026`.

## About the timezone

PageMotor has no site-wide timezone setting, so without `tz` the year comes from the server clock, which runs on UTC.

For almost everyone this never matters. It matters for a few hours around New Year, and only if you are far from UTC: a site in Auckland would otherwise show the old year for most of 1 January. If that is you, set `tz` to your own zone, either on the settings screen or on the shortcode.

If the timezone name is not one the server recognises, the plugin falls back to server time rather than failing. A footer should never be the thing that breaks a page.

## Both shortcodes are self-closing

There is no wrapping form. This will not work:

```
[ep-copyright]Some text[/ep-copyright]
```

That is not a limitation of this plugin. Enclosing shortcodes do not work anywhere in PageMotor — the interior is read and then discarded before your plugin ever sees it, with no error to explain why. Everything here is an attribute for that reason.

## Requirements

- **PageMotor 0.8.3 or later**
- **EP Suite base class** (bundled — no separate install)

## Changelog

### 1.0.0

First release.

`[ep-copyright]` renders the full notice and `[ep-year]` renders the year alone. Both take an optional business name, start year, symbol, suffix and timezone, all of which can also be set once on the settings screen so the bare shortcode needs no options at all.

The business name falls back to your site title when you have not set one, so in most cases `[ep-copyright]` on its own is the whole job.
