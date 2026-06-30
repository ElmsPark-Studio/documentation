---
title: "EP Passkeys"
description: "Passwordless login for PageMotor using WebAuthn passkeys. Face ID, Touch ID, Windows Hello, or hardware keys instead of passwords."
---

EP Passkeys replaces passwords with passkeys: the WebAuthn standard that backs Face ID, Touch ID, Windows Hello, and physical security keys. Users register their device once, then log in with a biometric or tap instead of a password. Phishing-resistant by design.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Why passkeys:

- **No password to steal, forget, or phish.** The private key never leaves the user's device.
- **Biometric convenience.** Face ID, Touch ID, or Windows Hello on modern devices.
- **Cross-device.** Passkeys sync via iCloud Keychain, Google Password Manager, or 1Password.
- **Phishing-resistant.** Passkeys bind to the domain, so a phishing site can't capture them.

## Status

**Version 0.4.0.** Available now. Migrated to PageMotor 0.9's open-tier AJAX. Passwordless sign-in is served from a dedicated page at `/?ep_passkey_login=1`.

## Requirements

- **PageMotor 0.9 or later** (verified on 0.9.4b)
- **EP Suite base class**
- **HTTPS** required — WebAuthn does not work over plain HTTP.
- **Modern browser** — Chrome, Firefox, Safari, Edge (recent versions).

## Installation

1. Download `ep-passkeys.zip` from the [EP Suite downloads page](https://updates.elmspark.com/download.php?plugin=ep-passkeys).
2. Upload it via **Plugins → Manage Plugins** and activate.
3. Register a passkey from your account page, then sign in at `/?ep_passkey_login=1`.

Current version **0.4.0**. Installs and works on PageMotor 0.9.x.

## User flow

### Registering a passkey

1. User logs in with their existing password (if set up first time) or passkey (if already registered).
2. Goes to their account page.
3. Clicks **Register a new passkey**.
4. Device prompts for biometric or PIN.
5. Passkey is saved on the device and registered with your site.

### Logging in with a passkey

1. User visits the passkey sign-in page at `/?ep_passkey_login=1`.
2. Clicks **Sign in with Passkey**.
3. Device prompts for biometric.
4. They're in.

## Integrations

- **EP Membership.** When both are installed, member login supports passkeys.
- **EP Ecommerce Subscriptions.** Self-service portal can be gated behind passkey auth.
- **EP Assistant.** Admin chat can use passkey-authenticated sessions.

## Troubleshooting

### “Register passkey button doesn't appear”

Check you're on HTTPS. WebAuthn is blocked on HTTP.

### “Device prompt opens but registration fails”

Check browser console for errors. Common cause: site domain doesn't match what was registered. If you change domain after registering, passkeys break.

### “I lost my device, I can't log in”

Passkeys on the lost device are gone. If you had a backup method (password, second device, recovery email), use it. If not, admin can reset the user from the database.

### “Passkeys don't sync across my devices”

Syncing depends on the platform (iCloud, Google, etc.) and the device's settings. This plugin doesn't control syncing.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
