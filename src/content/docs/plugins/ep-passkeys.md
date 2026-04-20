---
title: "EP Passkeys"
description: "Passwordless login for PageMotor using WebAuthn passkeys. Face ID, Touch ID, Windows Hello, or hardware keys instead of passwords."
sidebar:
  order: 41
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

**Version 0.3** — core flows work. Some device-management UX is still being polished.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**
- **HTTPS** required — WebAuthn does not work over plain HTTP.
- **Modern browser** — Chrome, Firefox, Safari, Edge (recent versions).

## Installation

Not currently available for install. EP Passkeys depends on a PageMotor core change that has not yet shipped. Installation steps will be published here once the core change lands.

## User flow

### Registering a passkey

1. User logs in with their existing password (if set up first time) or passkey (if already registered).
2. Goes to their account page.
3. Clicks **Register a new passkey**.
4. Device prompts for biometric or PIN.
5. Passkey is saved on the device and registered with your site.

### Logging in with a passkey

1. User visits the login page.
2. Clicks **Log in with passkey**.
3. Device prompts for biometric.
4. They're in.

## Integrations

- **EP Membership.** When both are installed, member login supports passkeys.
- **EP Ecommerce Subscriptions.** Self-service portal can be gated behind passkey auth.
- **EP Assistant.** Admin chat can use passkey-authenticated sessions.

## Troubleshooting

### "Register passkey button doesn't appear"

Check you're on HTTPS. WebAuthn is blocked on HTTP.

### "Device prompt opens but registration fails"

Check browser console for errors. Common cause: site domain doesn't match what was registered. If you change domain after registering, passkeys break.

### "I lost my device, I can't log in"

Passkeys on the lost device are gone. If you had a backup method (password, second device, recovery email), use it. If not, admin can reset the user from the database.

### "Passkeys don't sync across my devices"

Syncing depends on the platform (iCloud, Google, etc.) and the device's settings. This plugin doesn't control syncing.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
