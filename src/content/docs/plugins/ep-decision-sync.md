---
title: "EP Decision Sync"
description: "Server-side save and load for interactive plan documents. Ticks, notes and calculator settings persist per document key, attributed and versioned, over a small JSON endpoint."
---

EP Decision Sync gives an interactive HTML document a memory. A gated strategy page with checklists, decision toggles or a calculator can save its state to the site rather than to one person's browser, so the next reader sees where things were left, and who left them there.

Published by [ElmsPark Studio](https://elmspark.com).

## What it does

- **Saves state per document.** Each document has a key (lowercase letters, digits and dashes, up to 60 characters). The page posts its state object; the plugin stores it against that key.
- **Attributed and versioned.** Every save records who saved it and when (UTC), and keeps the last 50 versions. The newest is the current one.
- **A front-end JSON endpoint** at `/ep-decision-sync` for the page's own script: `op=get` reads the current state and version count, `op=save` appends a version.
- **API actions for tooling.** `get-state`, `get-history` and `save-state` at producer access, `clear-state` at admin, all under the `decision-state` family, so an MCP client can read or reset a document's state.

## Limits, by design

- A state object is capped at 20,000 bytes.
- Saves are rate-limited to one every two seconds across the site.
- The endpoint checks a shared token before it does anything. Keep the pages that carry it behind a gate such as EP Private Pages; the token protects against casual writes, not against a determined reader of the page source.
- Names are stripped of markup and cut to 60 characters. An empty name is saved as "Anonymous".

## Requirements

- **PageMotor 0.10.0 or later**
- A page or standalone HTML document whose script posts to the endpoint. The plugin ships no front-end script of its own.

## Installation

1. `ep-decision-sync.zip` is a private-tier plugin: ElmsPark supplies it directly, and after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. There are no settings. Give each document a key and point its script at `/ep-decision-sync`.

## Using the endpoint

Read the current state:

```
POST /ep-decision-sync
op=get&doc=creator-programme-v02&token=…
```

Returns `{"success":true,"data":{"current":{"state":{…},"saved_by":"Kenn","saved_at":"2026-09-17 03:40:12"},"versions":7}}`, or `"current":false` when nothing has been saved yet.

Save a new version:

```
POST /ep-decision-sync
op=save&doc=creator-programme-v02&name=Kenn&token=…&state={"ticks":{"a":true}}
```

Returns `{"success":true,"data":{"saved_by":"Kenn","saved_at":"…","versions":8}}`. Failure reasons are `bad_request`, `bad_token`, `too_large`, `bad_state`, `slow_down` and `unknown_op`.

## Changelog

### 1.0.2

First release on the ElmsPark update channel. The plugin now tells PageMotor where its updates and documentation live, so future versions arrive through your site's Updates screen instead of by hand. No change to how it saves or serves decision state.

### 1.0.1

Server-side save and load for interactive plan documents: decision checklists, ticks, notes and calculator settings, persisted per document key, attributed and versioned, over a front-end JSON endpoint for gated strategy pages.
