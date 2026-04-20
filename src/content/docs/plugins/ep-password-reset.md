---
title: "EP Password Reset"
description: "Email-based password reset for PageMotor admin accounts. Tokenised reset links, single-use, time-limited. Integrates with EP Email."
sidebar:
  order: 42
---

EP Password Reset adds a "Forgot your password?" flow to PageMotor's admin login. The admin enters their email, gets a tokenised reset link, clicks it, sets a new password. Token is single-use and time-limited.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

PageMotor core has no built-in password reset for admin accounts. If an admin forgets their password, they need database access to reset it. This plugin adds the email-based flow users expect from any modern system.

Flow:

1. Admin clicks **Forgot your password?** on the login page.
2. Enters their email address.
3. Plugin generates a single-use token, stores it, sends a reset link via EP Email.
4. Admin clicks the link (must be within the expiry window, 1 hour by default).
5. Admin sets a new password. Token is invalidated.
6. Admin can now log in with the new password.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Email** (required for the reset email)
- **EP Suite base class**

## Installation

Not currently available for install. EP Password Reset depends on a PageMotor core change that has not yet shipped. Installation steps will be published here once the core change lands.

## Settings

- **Token expiry.** Minutes before a reset link becomes invalid. Default 60.
- **Email template.** Subject and body of the reset email. Supports the `{reset_link}` placeholder.

## Security

- **Single-use tokens.** After a successful reset, the token is invalidated. Trying to reuse it fails.
- **Time-limited.** Tokens expire after the configured window.
- **Cryptographically random.** 32 bytes from a secure random source.
- **Email-only delivery.** The token is only ever sent to the admin's registered email.
- **Generic success message.** The plugin says "if that email is registered, a link has been sent" whether or not the email exists, so attackers can't enumerate valid admin emails.

## Troubleshooting

### "Reset email doesn't arrive"

EP Email handles delivery. Check EP Email's log. Common causes: SMTP config wrong, email in spam folder, admin's email address is outdated in the PageMotor user record.

### "Reset link says 'expired' despite clicking quickly"

Token expiry default is 1 hour. If the admin forwarded the email to another account or clicked in a delayed session, more than 60 minutes may have passed. Request a new reset.

### "Link says 'already used'"

Single-use tokens. If the admin clicked twice (once to set password, once accidentally), the second click fails. Request a new reset if the password wasn't actually set.

### "Reset flow works but admin still can't log in"

After reset, the admin is logged out of any existing sessions. Close all browser tabs, start fresh at the login page, use the new password.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
