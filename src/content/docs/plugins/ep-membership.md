---
title: "EP Membership"
description: "Public membership for PageMotor. Registration, login, profiles, member levels, and level-gated content and courses."
---

EP Membership gives your PageMotor site a public-user authentication layer. Visitors register, log in, manage their profile, and you gate content behind a login or a membership level. Pairs naturally with [EP Courses](/plugins/ep-courses/) for members-only learning content and [EP Ecommerce](/plugins/ep-ecommerce/) for paid membership tiers.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Registration form** on a public page, with optional email verification.
- **Login form** with rate limiting and lockout on repeated failures.
- **Built-in password reset** via email (secure one-hour tokens, no extra plugin needed).
- **Profile page** for members to update their own details.
- **Member dashboard** showing course enrolments and progress (with EP Courses).
- **Member levels** (0.5.0): optional ordered tiers — Free, Pro, VIP or whatever fits your site.
- **Level-gated content** (0.5.0): gate a span of content or a whole page by level.
- **Purchase grants** (0.5.0): active EP Ecommerce membership purchases count towards a member's level automatically.
- **Login gating** on any shortcode-wrapped content, and login-required settings for courses and lessons.
- **Integration with EP GDPR** for consent capture and logging on registration.
- **Integration with EP Newsletter** for an opt-in checkbox on the registration form.

Members are registered as a dedicated **Learner** user type. Learners have no admin access — the plugin redirects them to their profile page if they try to reach the admin panel.

## Status

**Version 0.5** — core flows and member levels are live and verified on PageMotor 0.10 and 0.11. Social login and bulk member import remain on the roadmap.

## Requirements

- **PageMotor 0.7 or later** (0.10 and 0.11 both verified)
- **EP Suite base class**
- **EP Email** — all transactional email (verification, welcome, password reset) is sent through EP Email. Without it active, those emails are not sent.

Optional:

- **EP Courses** for login-gated course access and the dashboard's enrolment list.
- **EP Ecommerce / EP Ecommerce Subscriptions** for purchase-granted membership levels.
- **EP GDPR** for a required consent checkbox on registration, with consent logging.
- **EP Newsletter** for a newsletter opt-in checkbox on registration.

## Installation

1. Install and configure EP Email first (it delivers the verification, welcome, and reset emails).
2. `ep-membership.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Create pages for registration, login, and profile:
   - `[ep-register-form]` at `/register/`.
   - `[ep-login-form]` at `/login/`.
   - `[ep-member-profile]` at `/profile/`.
   - Optionally `[ep-member-dashboard]` at a members' landing page.
5. In settings, check the **Login Page Slug**, **Registration Page Slug**, and **Profile Page Slug** match the pages you created, and set the **After Login Redirect**.
6. Optionally define **Member Levels** (see below).

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[ep-register-form]` | Registration form: full name, email, preferred language, password with confirmation. Includes a honeypot spam trap, and GDPR consent / newsletter opt-in checkboxes when those plugins are active. |
| `[ep-login-form]` | Login form: email and password, with Remember Me and a forgotten-password flow. |
| `[ep-logout-link]` | Logout link. |
| `[ep-member-profile]` | Profile editor for the signed-in member (display name, preferred language, password change). Shows the login form to visitors. |
| `[ep-member-dashboard]` | Signed-in landing page. With EP Courses active it lists the member's active enrolments with progress bars. |
| `[ep-login-gate]...content...[/ep-login-gate]` | Gate the wrapped content to logged-in members. Visitors see a message and a login link instead. Optional `message="..."` argument overrides the default prompt. |
| `[ep-level-gate level=pro]...content...[/ep-level-gate]` | Gate the wrapped content by membership level (0.5.0). Visitors see a login prompt; members below the level see an upgrade prompt; members at or above the level see the content. Optional `message="..."`. |

The bare, unprefixed forms of the original six (`[register-form]`, `[login-form]`, `[logout-link]`, `[member-profile]`, `[member-dashboard]`, `[login-gate]`) still work as deprecated back-compat aliases for existing content. Use the `ep-` prefixed forms in new content.

## Member levels

Levels are optional. Define them in settings under **Member Levels**: one per line, **lowest tier first**, as `slug | Label`:

```
free | Free
pro | Pro
vip | VIP
```

Line order is rank order — a Vip member passes every Pro and Free gate. New members receive the **Default Level** at registration (blank means the first line). Leave the levels box empty and the plugin behaves exactly as it did before levels existed.

A member's **effective level** is the higher of:

- the level assigned to them (at registration, or by you in the Members panel), and
- any active purchase grant (below).

Change a member's level any time from the **Members** panel in settings — every learner is listed with a level selector.

### Purchase grants

With the **Purchase Grants** setting on and EP Ecommerce installed, an active membership purchase lifts the member's effective level automatically. Set the product's `membership_level` to one of your level slugs; EP Ecommerce Subscriptions records the grant on purchase and renewal. Grants are checked live, so an expired or cancelled subscription stops counting immediately — no sync job, no delay.

## Gating content

### By level, in content

Wrap the span in `[ep-level-gate]`:

```
[ep-level-gate level=pro]
Here's the pro-and-above content.
[/ep-level-gate]

[ep-level-gate level=vip message="This one is for VIP members."]
VIP-only content with a custom prompt.
[/ep-level-gate]
```

A gate naming a level you haven't defined **fails open** (the content shows, with a note in the PHP error log) — a typo degrades to visible, never to a page nobody can see.

### By level, per page

With levels defined, every page's content options gain a **Membership** box with a **Required membership level** select. Visitors and members below the level see a prompt in place of the page body; the page chrome renders normally. Admins always see the page.

### Sitewide (0.5.1)

To gate the whole site at once, set **Sitewide Required Level** in the Member Levels settings to a level slug. Every page then requires that level, except:

- the paths you list under **Public Paths** (one per line, `/` for the homepage — say, a landing page and an application form), and
- the login and registration pages, which are **always** public so members can never be locked out of signing in.

A page's own Required membership level always overrides the sitewide gate. Blank the setting to switch the sitewide gate off; nothing else changes.

### Login-only

Wrap content in `[ep-login-gate]...[/ep-login-gate]` — visitors get a login prompt, any logged-in member sees the content.

### Courses and lessons

With EP Courses installed, the **Access Control** section in EP Membership's settings has two switches: **Lesson Access** (require login to view lessons) and **Enrolment Access** (require login to enrol). Level-based course gating is planned for a future EP Courses release; plugin developers can already call `member_has_level($user, $slug)` on the EP Membership instance.

## Settings

- **General** — the site name used in emails and notifications.
- **Registration** — enable/disable registration, email verification on/off, default language, after-registration redirect, welcome email on/off, newsletter opt-in on/off.
- **Login** — login and registration page slugs, after-login and after-logout redirects, Remember Me duration in days, max login attempts, and lockout duration in minutes.
- **Profile** — profile page on/off and its slug.
- **Access Control** — the course and lesson login requirements above.
- **Member Levels** (0.5.0) — the level definitions, default level, purchase grants switch, and (0.5.1) the sitewide gate with its public-paths list.
- **Members** (0.5.0) — every learner account with registration date, verification state, and a level selector.

## Password reset

Built in — no separate plugin needed. The login form links to a reset-request form; the member receives an emailed link with a single-use token that expires after one hour. Requests are rate limited per account. Delivery goes through EP Email.

## Integration with EP GDPR

When EP GDPR is active, the registration form adds a required consent checkbox, and each registration logs the consent text, email, and IP through EP GDPR's consent log.

## Integration with EP Newsletter

With the **Newsletter** setting enabled and EP Newsletter active, the registration form adds an opt-in checkbox; ticked registrations are subscribed automatically.

## Planned (not in any shipped version)

- **Social login.**
- **Bulk member import.**
- **Level-gated courses** (the EP Courses side of the integration).

## Troubleshooting

### “Registration form says email already exists but the user doesn't remember registering”

Search the Members panel by email. If the email exists, the user has an account they forgot about. Point them at the **Forgot password** link on the login form.

### “Logins work but the session doesn't persist”

Check cookies are being set correctly. Common cause: session cookie's `Secure` flag is on but the site is being accessed via HTTP. Ensure HTTPS is the only way in.

### “Verification, welcome, or password reset emails aren't arriving”

EP Email is required for all of these — check it is active and configured. Check EP Email's delivery log for the specific send. If EP Email is missing, EP Membership logs the failure to the PHP error log rather than sending.

### “A member paid for a subscription but their level hasn't changed”

Check the **Purchase Grants** switch is on, and that the product's `membership_level` matches one of your level slugs exactly. The grant's level string and your defined slug must be the same word.

### “A level gate is showing its content to everyone”

The gate names a level that isn't defined in settings — undefined levels fail open by design. Check the slug in the shortcode against the Member Levels box, and check the PHP error log for the breadcrumb.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
