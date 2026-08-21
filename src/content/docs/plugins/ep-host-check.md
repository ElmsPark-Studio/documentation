---
title: "EP Host Check"
description: "Read-only host diagnostics for PageMotor. One admin panel scores what your hosting can and cannot do for PageMotor, green/amber/red, with a plain-English meaning and a plain fix for every check."
---

Roughly nine out of ten "PageMotor is broken" reports turn out to be the host quietly blocking something, not PageMotor. PHP cannot write the compiled CSS, outbound SMTP is blocked so email never sends, an upload limit is too low for a theme import. EP Host Check turns that guesswork into a clear report.

It is one admin panel that runs a battery of checks against the host your site is actually on, and gives you a plain-English green, amber or red result. Every line says what it means and how to fix it, written for a site owner, not a sysadmin. It is read-only: it diagnoses, it never changes a setting.

Published by [ElmsPark Studio](https://elmspark.com).

## The verdict

At the top of the report is a single overall verdict, taken from the worst result across every check:

- **Green, "This host runs PageMotor fully".** Every check passed. Nothing to do.
- **Amber, "This host has limits worth knowing".** PageMotor will run, but some items could cause confusion later. Worth a quick read.
- **Red, "This host will break PageMotor, fix or move".** One or more checks will cause real failures (saving designs, sending email, taking payments). Fix them with your host, or move to a VPS.

## What it checks

### Can PHP save PageMotor's files (the big one)

This replicates what PageMotor does when it compiles your design: it writes a temporary file into the active theme folder, reads it back, and deletes it, then does the same for the uploads and user-content folders. If any of them cannot be written, your design changes will appear to do nothing and uploads will fail. This single restriction is the most common cause of a "PageMotor is broken" report, and it is a host setting, not PageMotor.

### Capability checks

- **PHP version.** Fails below 8.1, warns on 8.1, passes on 8.2 and newer.
- **PHP extensions.** mysqli, curl, mbstring, json, openssl, and gd or imagick are required; zip is flagged as a warning (only needed for zip imports).
- **Blocked PHP functions.** Reads the `disable_functions` list. Fails if a file-write function or `curl_exec` is switched off; warns if only `fsockopen` is (that just affects the SMTP self-test).
- **open_basedir.** If a path restriction is set, confirms it includes your site's folders.

### Outbound connections

- **Outbound HTTPS.** A real short-timeout request to a stable endpoint. If it is blocked, Stripe payments, licence checks, AI features and web fonts all stop working.
- **Outbound mail (SMTP).** A short-timeout connection test to a known mail server on ports 587 and 465. It never sends anything. Many shared hosts block this, which presents as "PageMotor won't send email" when it is purely a host restriction.

### Resource limits and caching

- **Upload size** (`upload_max_filesize` and `post_max_size`), warned below ~64M.
- **PHP memory** (`memory_limit`), warned below 128M, with a note about SCSS-compile headroom.
- **PHP time limit** (`max_execution_time`), warned below 30 seconds.
- **Object cache** (Redis / Memcached): informational, never required.
- **PHP opcode cache** (opcache): on is faster; off is a gentle warning.

### MCP / Claude connection (v1.2.0, extended through v1.3.2)

Six checks that answer "why won't my site connect to Claude?" in one panel, each mapped to a section of the [PageMotor MCP troubleshooting guide](/guides/pagemotor-mcp-troubleshooting/):

- **Claude sign-in clock (OAuth timezone).** PageMotor stamps the 60-second sign-in code's expiry in UTC but reads it back in server-local time. A server ahead of UTC therefore treats every code as expired the instant it is issued, and browser sign-in from Claude always fails while everything else looks healthy. Red if your server is ahead of UTC now; amber if daylight saving will push it ahead later in the year. The fix is one line: `date.timezone = UTC`.
- **MCP token reaches PHP.** Some servers (typically Apache running PHP as CGI/FastCGI) strip the Authorization header before PHP sees it, so a perfectly valid token arrives as anonymous. When you run this report through the API or MCP with your token, that request is itself the definitive proof the header got through, and the check goes green. From the admin panel it reports what it can see and tells you how to get the definitive answer.
- **HTTPS as PageMotor sees it.** Behind Cloudflare Flexible SSL or a TLS-terminating proxy, your visitors use https but PageMotor thinks it is on plain http, so every sign-in URL it advertises is built wrong and the connection dies. Red when the report can see that mismatch from your proxy's own headers.
- **OAuth discovery reachable.** PageMotor serves its OAuth discovery documents as dynamic routes, and two quite different faults can stop Claude reading them. A stock nginx/CloudPanel/Plesk `.well-known` block answers them from the filesystem with a 404 (guide §6d). Or your host's bot protection decides an automated client is not welcome and answers with a CAPTCHA challenge page — an HTTP 202 carrying HTML where JSON should be (guide §6g, new in 1.3.1). They need opposite fixes, so since 1.3.1 the check tells them apart rather than giving one diagnosis for both: only a 2xx carrying an HTML body counts as a bot wall, so a genuine 404 still reports as the filesystem block it is. Failure rows now quote the response content-type as well as the status, because the content-type is what shows *why* the row is red.
  - **Bot wall.** Nothing you can edit will fix it: the filter sits in front of your web server, and your own browser is trusted so you will never reproduce the fault yourself. The row says so, and gives you support-ticket wording naming the paths to exempt — including the advice to quote the HTTP 202, not "404", because a support agent who hears 404 goes looking for a missing file.
  - **Filesystem block.** Since 1.3.2 the fix text matches the server you can actually edit. On Apache or LiteSpeed the check reads your webroot `.htaccess`: if a `.well-known` short-circuit rule is the cause it names the offending line and gives you the one-line narrowing to `acme-challenge/` only; if there is no such rule, the block sits in a layer only your host controls, so you get ticket wording instead of an edit that cannot work. On nginx you get the vhost block to fix. Before 1.3.2 every host got the nginx advice, which is useless on shared hosting where there is no vhost to open.
  - Both faults can stack on one host — 404 from the inside, CAPTCHA from the outside — and fixing only one leaves sign-in broken.
- **MCP endpoint answers POST directly.** Connector clients POST to the slash-less MCP URL; a redirect turns that into an empty GET and the handshake dies even though the URL "works" in a browser. On PageMotor 0.9.x the redirect is expected platform behaviour, and the row tells you the fix is simply using the trailing-slash URL in your connector.
- **No plugin intercepts MCP authentication** (new in 1.3.0, guide §6f). Pre-OAuth bridge plugins (the PageMotor Architect AI Claude bridge, the EP MCP Bridge) answer the MCP route themselves behind their own API key. Left active on a modern core, they hijack *authenticated* requests only: sign-in completes, Connected Apps rows appear, then every request dies with "Invalid or missing API key." — while anonymous probes, and the other five rows here, all look healthy. The check fingerprints every active plugin's own code (never just its name — PageMotor bundles a harmless core plugin with the identical "PageMotor Architect AI: Claude" name) and names the offender. Amber, with the fix: deactivate it unless you deliberately connect through it.

These rows are version-aware: on PageMotor 0.9.x (which has no browser sign-in) the OAuth-only checks report as neutral "Info" rows rather than failures, and the bridge row's advice becomes "retire it when you upgrade" since a bridge may be a 0.9 site's intended connection path. Info rows never affect the overall verdict.

## Requirements

- **PageMotor 0.9 or later.** On PageMotor 0.11, use EP Host Check 1.3.3 or later — earlier builds hit a CSRF loop when the panel opens (see Troubleshooting).
- **EP Suite base class** (bundled)

## Installation

1. Download `ep-host-check.zip` from the [EP Suite downloads page](https://updates.elmspark.com/download.php?plugin=ep-host-check). If you already run EP Suite plugins, it will also appear in your PageMotor admin under updates.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Host Check**. The report runs automatically.

## Using the report

1. Read the overall verdict at the top, then scan the rows. Each has a coloured dot, a plain meaning, and, for amber and red items, a prominent fix.
2. Act on the red items first (those break things), then the amber ones (those are limits worth knowing).
3. Use **Re-run checks** after you or your host changes a setting, to confirm the fix took.

## For developers and AI clients

EP Host Check exposes a `host-report` action over the PageMotor API and MCP. An MCP client (or the `/api/` endpoint) can read a host's status headlessly and reason about it, returning the same verdict and per-check data the panel shows (statuses `pass`, `warn`, `fail`, and the neutral `info`). Useful for checking a fleet of sites, or for an AI agent diagnosing a deployment.

Two details worth knowing from 1.2.0: calling `host-report` through the API or MCP with a Bearer token is itself the definitive Authorization-header pass-through test — if it answers at all, the token reached PHP, and the report says so. And other EP plugins can gate on MCP readiness via `EP_Host_Check_MCP::can_mcp_ready($checks)`, which is true unless any `mcp_*` check hard-failed.

## What EP Host Check cannot do

- **Fix anything automatically.** It is read-only by design. It reports what it sees; the fixes are changes you or your host make.
- **See another server.** It runs on your host and reports what that host can do. It does not phone home and sends nothing anywhere.
- **See your site from the outside.** Every probe runs on your own server, so a host that trusts its own machines but challenges outside traffic gets clean JSON on the loopback and a green "OAuth discovery reachable" row while Claude is still blocked. This is a known limitation, documented since 1.3.1 and not detectable from inside the box. If your site reports green here but still connects from nowhere, check it from another machine with `curl -sI https://yoursite.com/.well-known/oauth-authorization-server` and read the **content-type**, not the status.

## Built to run on broken hosts

The whole point of the plugin is to run on the hosts that block things, so it never fatals. Every probe is wrapped and every function is guarded. If your host has disabled `fsockopen`, that is reported as a finding, not a crash. Every temporary file it writes to test is cleaned up afterwards, even when a write is blocked.

## Privacy

Nothing leaves your server except the two outbound connection tests, which only check whether a connection can be opened (to a web endpoint over HTTPS, and to a mail server on 587/465). No data is sent in those tests, and no report is shared anywhere unless you choose to share it. No telemetry, no tracking.

## Troubleshooting

### "The write check is red but I'm sure the folder exists"

The folder existing is not the same as PHP being allowed to write to it. On many shared hosts the web user cannot write inside the site folder. The fix is a host permissions change, or moving to a VPS where PHP can write to its own site.

### "Outbound HTTPS or SMTP is red, but my site loads fine"

Inbound traffic (visitors reaching your site) and outbound traffic (your site reaching out to Stripe or a mail server) are different directions, controlled separately. A host can allow one and block the other. The report is about the outbound direction, which is what payments, licensing and external mail need.

### "Your session has expired" the moment the panel opens (PageMotor 0.11)

Update to 1.3.3, which fixes it. On PageMotor 0.11 with an earlier build, opening EP Host Check raised that alert immediately, and clicking OK reloaded straight back into it — while the admin dashboard and Content carried on working normally. Nothing was wrong with your session. Both the plugin and PM 0.11 were adding the CSRF token header to the same request, and because a browser *appends* repeated headers rather than replacing them, the token arrived twice in one header and core rejected it before the check ran. 1.3.3 sets the header only when core has not already set it, on 0.10 and 0.11 alike.

The same double-set affects the shared EP Suite admin header (the language selector and brand-colour picker) across the whole suite on 0.11. The shared code is fixed here first; each other EP plugin picks it up as it is rebuilt.

### "Outbound mail shows amber on a shared host"

That is expected on many shared hosts: they block outbound SMTP. Use the host's own mail, or move external mail (such as Mailgun) to a VPS. See the [Mailgun email setup guide](/guides/mailgun-email/).

## Changelog

### 1.3.3

Fixes the "Your session has expired" loop on PageMotor 0.11: the CSRF token header was being set twice — once by the plugin, once by 0.11's new automatic injection — and arrived carrying the token twice over, so core rejected the request before the check ran. The plugin now sets the header only when core has not already done so, with no version sniffing to go stale. Verified end to end on a real 0.11 site: before, 31 alerts in nine seconds and a panel stuck on "Running checks against your host…"; after, no alerts and the full report renders. What the plugin checks and reports is unchanged from 1.3.2.

### 1.3.2

The "OAuth discovery reachable" fix text now matches the server you can actually edit. The filesystem-block failure used to prescribe the nginx vhost block to everyone, which is right on a VPS, CloudPanel or Plesk box and useless on shared hosting where there is no vhost to open. The check now branches on your serving environment: Apache or LiteSpeed with a `.well-known` short-circuit rule in the webroot `.htaccess` gets the offending line named and a one-line fix; Apache or LiteSpeed without one gets paste-ready support-ticket wording, because the block is in a layer the host controls; nginx gets the original vhost text. The `.htaccess` scan is bounded and deliberately never blames a correctly narrowed ACME rule.

### 1.3.1

"OAuth discovery reachable" stopped giving one diagnosis for two different faults. A host bot wall answering the discovery documents with a CAPTCHA challenge was correctly failing the check, but was reported as the nginx `.well-known` block and prescribed its fix — advice that cannot work when the filter sits in front of the web server. There is now a separate branch for the bot-wall case (guide §6g) with support-ticket wording, kept deliberately narrow so a genuine 404 still reports as the filesystem block it is. Failure rows also quote the response content-type, so a red row shows why it is red. Found in the wild on SiteGround Anti-Bot AI. Known limitation, unchanged since: these probes run from your own server, so a host that trusts its own machines can produce a green row while Claude is still blocked from outside.

### 1.3.0

New check, **"No plugin intercepts MCP authentication"** (guide §6f): finds active pre-OAuth MCP bridge plugins that answer the MCP route behind their own API key. Sign-in completes and Connected Apps rows appear, then every request dies with "Invalid or missing API key.", while anonymous probes and the other MCP rows all look healthy. Detection fingerprints each plugin's own code rather than its name, because PageMotor bundles a harmless core plugin with an identical display name. Warn-only: it can turn the verdict amber, never red.

### 1.2.0

New **MCP / Claude connection** check group (guide §6a–§6e): OAuth sign-in timezone, Authorization-header pass-through, HTTPS as PageMotor sees it, OAuth discovery reachability, and MCP-endpoint redirect behaviour — the whole "why won't my site connect to Claude" class in one panel. Read-only and bounded, with a neutral **info** row status for anything that cannot be verified from inside, so a host that blocks self-connections never produces a false fail. Adds `EP_Host_Check_MCP::can_mcp_ready($checks)` for other EP plugins to gate on. Also removes `curl_close()` calls, which are deprecated on PHP 8.5 and could corrupt the report on exactly the misconfigured hosts this plugin exists to diagnose.

### 1.1.5

The admin check routes through a skew-safe wrapper, so a version mismatch between EP Suite plugins can never break this plugin's admin screens. No functional change.

### 1.1.4

PageMotor 0.10 compatibility: the admin guard used a check 0.10 removed, which failed closed and locked admins out of the plugin's admin actions. Both 0.9 and 0.10 are supported. Adds the standard build script.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on.

For anything bigger, a bug report, a feature request, or a "how do I..." that needs a real reply, open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply, usually within a few hours.
