---
title: "EP Flows"
description: "The EP Suite automation engine: trigger, conditions, actions, stored as flows on your own site with a run ledger. Authored by talking to your site over MCP, not a drag-and-drop builder."
---

EP Flows is the PageMotor-native answer to Zapier, Make, or Pabbly: trigger, conditions, actions, stored as a flow on your own site, with a run ledger you can read at any time. It composes with [EP Connect](/plugins/ep-connect/) for the event bus and outbound fan-out, EP Cron for schedules, and EP Email for notifications.

Published by [ElmsPark Studio](https://elmspark.com).

## The idea

Off-the-shelf automation tools sell you a connector catalogue: thousands of pre-built integrations, hosted on someone else's servers. EP Flows takes a different view. Every modern service already speaks inbound HTTP, and a PageMotor site is already an always-on runtime, so one good templated HTTP action covers the large majority of cases people reach for Zapier-style tools for. Pabbly and Zapier remain useful as optional bridges a flow can call out to; they are not the engine.

The differentiator is how flows get built: talk to your site over MCP and describe what you want, rather than dragging boxes around a canvas. Every action EP Flows exposes is also a live MCP tool, so an AI agent connected to your site can list, create, test, and inspect flows directly.

## Triggers

| Trigger | Fires when |
|---|---|
| **Inbound** | An external service POSTs JSON to your site's tokenless hook URL. |
| **Event** | Another EP Suite plugin (or your own code) emits an event on the [EP Connect](/plugins/ep-connect/) bus. |
| **Schedule** | Every N minutes, claimed atomically so a heartbeat cannot double-fire. |
| **Manual** | Fired on demand, from the admin screen or the `flow_test` action. |

## Conditions

Each flow can carry a list of conditions checked against the trigger payload before any action runs, for example "`kind` equals `lead`". A flow with no conditions always proceeds. A payload that fails its conditions is recorded in the run ledger as **skipped**, not as a failure.

## Actions

| Action | What it does |
|---|---|
| **http_request** | Sends a templated HTTP request (method, headers, body) to any URL. |
| **email** | Sends a notification through EP Email. |
| **emit_event** | Emits a new event back onto the EP Connect bus, so flows can chain. |
| **log** | Records a message in the run ledger. Useful while building a flow. |

Any field in an action's configuration can use `{{trigger.field}}`, `{{flow.name}}`, `{{now}}`, `{{site.url}}` and similar placeholders, filled in from the trigger payload and flow metadata at run time.

## Hardening

- **Signed inbound.** Setting a flow's trigger to require a signature verifies `X-EP-Signature`, an HMAC-SHA256 of the raw request body, using the same scheme EP Connect signs its own outbound webhooks with, so a PageMotor site calling another PageMotor site can verify at both ends.
- **Rate limiting.** Every attempt against a flow's inbound hook counts towards its per-minute limit, valid or not, so a flood of bad secrets throttles rather than exhausts the endpoint.
- **SSRF guard.** `http_request` actions block loopback, private, link-local and `.local` targets by default. A flow author can opt a specific action in with `allow_internal` when the target is genuinely a same-box service.
- **Opt-in retry.** An `http_request` action can request one deferred retry roughly two minutes after a failure, claimed atomically so a retry can never fire twice.

## Authoring over MCP

All seven of EP Flows' API actions are exposed as MCP tools the moment the plugin is active: `flows_list`, `flow_get`, `flow_save`, `flow_delete`, `flow_test`, `flow_runs`, `flow_inbound`. Connect an MCP-capable AI client to your site and it can build, test, and monitor flows in the same conversation you describe them in.

## The inbound hook

Add the `[ep-flows-hook]` shortcode to a page to get a tokenless inbound endpoint for that flow. POST JSON to that page's URL with `?ep_flow=<flow-slug>&ep_secret=<flow-secret>` in the query string; both values are shown on the flow's row in the admin screen. The endpoint responds before any page content renders, so a slow or unreachable trigger source never waits on PageMotor's own rendering.

## Requirements

- **PageMotor 0.10 or later**
- **EP Connect 1.1.0 or later** — only needed if a flow uses an event trigger or an `emit_event` action. Inbound, schedule and manual triggers, and the `http_request`, `email` and `log` actions, work without it.
- **EP Email**, any current version — only needed for the `email` action.
- **EP Suite base class** (bundled)

## Installation

1. `ep-flows.zip` comes with an EP Suite licence, supplied directly by ElmsPark (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Flows** for a read-only overview of your flows, recent runs, and the run-ledger retention setting.
4. Build your first flow by talking to your site over MCP, or use `flow_save` directly if you are scripting against the API.

## Changelog

### 0.2.0

The hardening pass: signed inbound trigger mode (`X-EP-Signature`, HMAC-SHA256), per-flow rate limiting on the inbound hook, an SSRF guard on `http_request` (with an `allow_internal` opt-out), opt-in single retry for `http_request`, a server-rendered action-trail detail view on the admin runs table, and translations for `de`, `es`, `fr`, `it`, `nl`, `pt`.

### 0.1.0

First release. Trigger, conditions, actions, stored on-site with a run ledger. Inbound triggers via the tokenless `[ep-flows-hook]` page endpoint and the authenticated `flow_inbound` action; event triggers via the EP Connect 1.1.0 bus listener; schedule triggers via EP Cron; manual firing via `flow_test`. Actions: templated `http_request`, `email`, `emit_event`, `log`. Seven `api()` actions, all exposed as MCP tools. Read-only admin screen.
