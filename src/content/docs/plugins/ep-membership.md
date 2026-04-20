---
title: "EP Membership"
description: Public membership for PageMotor. Registration, login, profiles, password management, and access control for gated content and courses.
sidebar:
  order: 38
---

EP Membership gives your PageMotor site a public-user authentication layer. Visitors register, log in, manage their profile, and you gate content or courses behind membership. Pairs naturally with [EP Courses](/plugins/ep-courses/) and [EP Ecommerce Subscriptions](/plugins/ep-ecommerce-subscriptions/) for paid members-only content.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Registration form** on a public page.
- **Login form** with password or passkey (via EP Passkeys) authentication.
- **Password reset** via email (via EP Password Reset).
- **Profile page** for members to update their own details.
- **Access control** on any page or any shortcode-gated content.
- **Member levels** so you can have Free, Pro, VIP etc.
- **Integration with EP Courses** for course enrolment tied to membership.
- **Integration with EP Ecommerce Subscriptions** so paid subscribers get membership access automatically.

## Status

**Version 0.4** — core flows work and are in use. Some enhancements are pending, particularly around social login and bulk member import.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class**
- **EP Email** (for password reset emails, welcome emails)
- **EP Password Reset** (for forgotten password flow)

Optional:

- **EP Passkeys** for passwordless login.
- **EP Courses** for course access tied to membership.
- **EP Ecommerce Subscriptions** for paid-subscriber-only membership.
- **EP GDPR** for consent logging on registration.

## Installation

1. Install EP Email and EP Password Reset first.
2. Download `ep-membership.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Create pages for registration, login, and profile:
   - `[membership-register]` at `/register/`.
   - `[membership-login]` at `/login/`.
   - `[membership-profile]` at `/my-account/`.
5. Configure the **Post-login redirect** in settings (typically back to the profile page or a members-only dashboard).

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[membership-register]` | Registration form. Configurable fields (name, email, password, profile extras). |
| `[membership-login]` | Login form. Password and/or passkey. |
| `[membership-profile]` | Profile editor. Authenticated members only. |
| `[membership-logout]` | Logout link. |
| `[members-only level=pro]...content...[/members-only]` | Gate content to members of a given level. |

## Member levels

Create levels in settings:

- **Name.** "Free", "Pro", "VIP".
- **Slug.** Used in shortcodes.
- **Description.** Internal note for admins.
- **Upgrade to.** Optional parent level, for level hierarchy.

When a member signs up, they're assigned to a default level (configurable). Upgrade them manually from the admin, or via EP Ecommerce Subscriptions when they buy a subscription.

## Gating content

### Page-level

In any page's content options, set **Required membership level**. Non-members (or members below the required level) see a login-or-register prompt instead of the page content.

### Shortcode-level

Wrap gated content in `[members-only level=pro]`:

```
[members-only level=pro]
Here's the pro-only content.
[/members-only]

[members-only level=pro show_prompt=true]
Pro content with a visible "upgrade to pro" prompt for non-members.
[/members-only]
```

## Integration with EP Ecommerce Subscriptions

When a customer purchases a subscription linked to a membership level, EP Membership:

- Adds the member at that level.
- Updates their access as renewal continues.
- Downgrades or revokes on cancel or expiry (per your cancellation policy in EP Ecommerce Subscriptions).

## Integration with EP Courses

When a course is set to require a specific membership level, the course viewer checks the member's level before rendering lesson content.

## Registration fields

Configurable in settings. Common options:

- **Required:** email, password.
- **Optional but common:** first name, last name, display name.
- **Optional extras:** phone, company, custom fields.
- **GDPR consent checkbox** (if EP GDPR is installed, consent is logged).

## Troubleshooting

### "Registration form says email already exists but the user doesn't remember registering"

Search the members admin by email. If the email exists, the user has an account they forgot about. Send them a password reset via EP Password Reset.

### "Member can log in but can't see gated content"

Check their member level matches the gate's required level. A Free member cannot access Pro content unless you upgrade them.

### "Logins work but the session doesn't persist"

Check cookies are being set correctly. Common cause: session cookie's `Secure` flag is on but the site is being accessed via HTTP. Ensure HTTPS is the only way in.

### "Password reset emails aren't arriving"

EP Email and EP Password Reset are both required. Check both are active. Check EP Email's delivery log for the specific send.

### "Subscription subscriber doesn't have membership despite paying"

Check EP Ecommerce Subscriptions has a mapping from the subscription product to a membership level. Without the mapping, payment doesn't trigger membership grant.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
