---
title: "EP Waivers"
description: "Versioned liability waivers and health declarations for a studio, e-signed with a typed-name signature, timestamp, IP, user agent and the exact version agreed to. Signatures are immutable legal records."
---

EP Waivers adds versioned liability waivers and health declarations to a studio. A signature records the typed name, the timestamp, the IP address, the user agent and the exact version of the document that was agreed to, and it is kept as an immutable legal record. Publishing a new version requires everyone to re-sign before their next class.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Versioned documents.** Publishing a new version does not rewrite history: the earlier signature is retained as the record of what that member actually agreed to at the time.
- **Immutable e-signatures.** Typed name, timestamp, IP, user agent and version, stored as a legal record.
- **Health declarations.** Encrypted at rest and shown only to admins and, through EP Instructors, the teacher assigned to the class.
- **Hard gate at booking.** Through the EP Events booking hook, an unsigned applicable waiver blocks the booking; the buyer signs inline before payment and the booking then continues.
- **Re-sign notifications** when a new version is published.
- **Coverage surfaces.** Who has signed, on which version, with a coverage log and read-only API and MCP tools.
- **No public surface.** The record survives a GDPR erasure of marketing data, because it is a legal record rather than marketing consent.

## Requirements

- **PageMotor 0.8.3b or later** (PageMotor 0.9 and 0.10 both supported)
- **EP Events 1.0.28 or later** for the booking gate
- **EP Instructors** if teachers should see health answers for their own classes

## Installation

1. `ep-waivers.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Create a waiver document, publish its first version, and place `[ep-waiver-sign]` on the page where members should sign. `[ep-waiver-status]` shows a member their current status.

## Changelog

### 1.2.5

Defensive load guard: if the bundled suite library is missing or truncated, the plugin now degrades to behaving as though it were not installed, with a note in the error log, instead of taking the whole site down with it. The build also verifies the bundled library is really present inside the shipped zip. No change in behaviour when everything is healthy.

### 1.2.4

Namespaced shortcodes. PageMotor's shortcode registry is first-wins and core initialises first, so a bare name can silently lose to a core shortcode of the same name. `[ep-waiver-sign]` and `[ep-waiver-status]` are now the canonical forms. The old `[waiver-sign]` and `[waiver-status]` still work as deprecated aliases, so existing pages keep working.

### 1.2.3

The admin check now routes through a version-skew-safe wrapper, so a mismatch between suite plugins can never break this plugin's admin screens. No functional change.

### 1.2.2

PageMotor 0.10 compatibility: the admin guard used a check that 0.10 removed, which failed closed and locked admins out of the plugin's admin actions. Both 0.9 and 0.10 are now supported.

### 1.2.1

Admin polish and a counting fix. The Signatures column counted every historical version, so a member who re-signed after a version bump was counted twice; it now counts members signed on the current version, while prior signatures stay in the coverage log as the legal record. The version badge now appears in the admin header. Publish and Create no longer submit the whole settings form when clicked early. New-document fields are labelled, and the version textarea is taller for pasting real legal text.

### 1.2.0

Booking pre-payment gate through the EP Events hook: an unsigned applicable waiver blocks the register, the buyer signs inline, then the booking resumes.

### 1.1.0

Health declaration capture, encrypted at rest, re-sign notifications on a new version, and the status shortcode.

### 1.0.0

First release: versioned waiver documents, immutable typed-name e-signatures, the signing shortcode, and the admin documents and coverage surfaces.
