---
title: "EP Brain Vault"
description: "Snapshots and version history for PageMotor Brains. A periodic safety net that catches every writer, plus versioned write, history and restore verbs that give an AI agent real per-write history — because core's brain-write keeps none."
---

EP Brain Vault gives a PageMotor Brain something it does not have on its own: history, and a way back. Core's `brain-write` replaces a file outright, so whatever was there is gone the moment something writes over it. This plugin keeps every version, and lets you put any of them back.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

A Brain is a private, persistent workspace an AI agent reads and writes across sessions. That is exactly what makes it worth protecting: the more your agents rely on it, the more expensive one careless overwrite becomes, and the less likely you are to notice at the time.

The plugin does two separate jobs, sharing one store:

- **A periodic snapshot** of every Brain on the site. This catches *every* writer, including an agent calling core's `brain-write` directly without knowing this plugin exists.
- **Versioned write verbs** — `vault-write`, `vault-history`, `vault-read-version`, `vault-restore` — which give true per-write history to any agent that uses them.

The two overlap deliberately. Snapshots are coarse but universal; the verbs are precise but only cover writers that opt in. Together they mean a Brain edit is recoverable whether or not the thing doing the editing cooperated.

## How it works

1. Every version of every file is stored by the hash of its contents, so identical content is only ever stored once and snapshots stay cheap.
2. On each heartbeat, the plugin looks at every Brain. If nothing has changed since the last snapshot, it skips — no new copy, no wasted disk.
3. If something has changed, it records a snapshot: a small index mapping each file path to the version it held at that moment.
4. `vault-write` adds a finer layer. Before it writes, it files away the content it is about to replace, so you get history *per write* rather than per interval.
5. Old versions are pruned on the heartbeat, according to your retention settings.

### Where it stores things, and why it matters

The version store lives beside your Brains, not inside them, under the site's protected uploads directory. This is deliberate: `brain-search` reads every file underneath a Brain's own folder, so a version store kept inside one would fill your agent's search results with stale copies of its own history.

## Requirements

- **PageMotor 0.11 or later.** Brains do not exist before 0.11, so there is nothing for this plugin to protect on an earlier core. This is a genuine minimum, not a precaution.
- **[EP Cron](/plugins/ep-cron/)**, for the periodic snapshots. The vault verbs work perfectly well without it; only the automatic safety net needs a heartbeat.
- **EP Suite base class** (bundled with the plugin).

## Installation

1. Install [EP Cron](/plugins/ep-cron/) first if you want automatic snapshots, and confirm its heartbeat is actually arriving. A scheduler with no heartbeat is silent rather than noisy.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Brain Vault** and turn on periodic snapshots.
4. **Check your protected uploads are actually private.** See below — this is worth five minutes.

## Check your server denies the protected uploads path

Your Brain's contents, and this plugin's copies of them, live under `/user-content/uploads/protected/`. PageMotor writes a deny file there, which is enough on Apache and LiteSpeed. **On nginx it is not**, because nginx ignores `.htaccess` entirely — the directory is only private if your site's configuration says so.

Test it. Ask an admin for any file path under that directory and fetch it in a private browser window, signed out. You should get a 403. If you get the file, your Brains are readable by anyone who can guess a URL.

The nginx fix is one line in your site's server block:

```nginx
location ^~ /user-content/uploads/protected/ { return 403; }
```

The `^~` matters. A plain regex rule placed after a `location ~ \.php$` block can be skipped entirely, because nginx matches regex locations in file order and the first match wins.

This is not specific to EP Brain Vault — it applies to every protected file PageMotor stores. The plugin simply gives you more worth protecting.

## Settings

| Setting | What it does |
| --- | --- |
| **Enable periodic snapshots** | The background safety net. Off by default; the vault verbs work either way. |
| **Snapshot every** | How often the heartbeat checks for changes. 15 minutes is the recommendation. An unchanged Brain costs almost nothing, so a shorter interval is cheaper than it sounds. |
| **Keep versions for** | Age limit for snapshots and individual versions alike. 90 days by default. |
| **Snapshots kept per brain** | A second cap alongside the age limit, so a Brain that changes constantly cannot grow the store without bound. Per-write versions are not counted against it. |

## The verbs

Point your agent at `vault-write` instead of `brain-write` and every edit keeps its predecessor. The tool descriptions say so too, so a connected assistant will usually prefer it on its own.

| Verb | What it does | Who can call it |
| --- | --- | --- |
| `vault-write` | Creates or overwrites a file, exactly like `brain-write`, but files away what it replaces first. | Producer |
| `vault-history` | Every version of a file: when it was captured, how big it was, and whether a snapshot or a write caught it. | Producer |
| `vault-read-version` | The contents of one earlier version. Pass `current` to read the live file instead. | Producer |
| `vault-restore` | Puts a file back to an earlier version, or restores every file in a whole snapshot. | Producer |
| `vault-diff` | What actually changed between two versions, as a unified diff. Either version to version, or against the live file. | Producer |
| `vault-snapshot` | Takes a snapshot immediately rather than waiting for the heartbeat. | Admin |

`vault-history` tells you which versions exist; `vault-diff` tells you what differs between them. Use the second before a restore, so you are confirming a version rather than guessing at it from timestamps.

### Access follows the Brain, not the plugin

Every read and write goes through PageMotor's own Brain methods, so each Brain's access policy applies unchanged. A Brain restricted to admins stays restricted to admins, and a producer-tier caller cannot read its history, restore its files, or discover that any of it exists. The plugin adds a safety net; it does not add a way in.

One deliberate exception, stated plainly because it is the kind of thing you should hear from the vendor rather than discover: the *scheduled* snapshot reads Brain files directly from disk. It has to. A heartbeat has no signed-in user, so asking "may this caller read this Brain?" would answer no for every Brain, every time, and the safety net would quietly never run. Nothing is disclosed by capturing — the store is protected the same way the Brains are — and every path that *reads history back* still checks the caller's access first.

## Restores never destroy history

A restore is itself recorded, before it overwrites anything. So restoring to Tuesday's version does not discard Thursday's: Thursday is filed away on the way past, and you can restore forward again if the restore was the mistake.

## Troubleshooting

**Snapshots never happen.** Almost always the heartbeat. Check EP Cron is active and its last pulse is recent. The vault verbs will still work; only the automatic snapshots depend on the heartbeat.

**`vault-history` shows fewer versions than you expected.** Between snapshots, only `vault-write` records individual edits. If something wrote through core's `brain-write`, the change is captured at the next snapshot rather than at the moment it happened — the interval is the resolution.

**A restore did not bring back what you expected.** Restoring a whole snapshot returns the files that snapshot captured. Files created *after* it are left alone rather than deleted, on the grounds that removing something a snapshot never knew about is a surprising thing for a restore to do.

**Deleting a Brain leaves its history behind.** Known limitation in this release: `brain-destroy` removes the Brain but not the vault's copies of it, which stay on disk until removed by hand. They are unreachable through any verb and covered by the same protection as the rest of the store, but they do occupy space.

## Changelog

### 0.2.0

Adds `vault-diff`: what actually changed between two versions of a file, as a unified diff, either version to version or against the live file. It reports added and removed line counts alongside the diff text, so a caller can summarise a change without reading it. 0.1.0 shipped without one and left you comparing two versions by eye.

Bounded deliberately, at 2MB and 20,000 lines per side. Past that it declines rather than trying, because a Brain file has no size limit and one oversized comparison should not be able to exhaust a request.

Access is unchanged. `vault-diff` respects the brain's own policy exactly as the other verbs do, so a producer-tier caller cannot diff an admin-only brain or learn that one exists.

### 0.1.0

First release. Periodic snapshots of every Brain on the site, driven by the EP Cron heartbeat, with content-addressed storage so unchanged files are never stored twice and an unchanged Brain is skipped rather than re-copied. Adds `vault-write`, `vault-history`, `vault-read-version`, `vault-restore` and `vault-snapshot`, giving per-write history to any agent that uses them. Retention by age and by snapshot count, pruned on the heartbeat.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
