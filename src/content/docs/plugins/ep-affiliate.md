---
title: "EP Affiliate"
description: "Affiliate management for PageMotor — partner recruitment, referral tracking, commission tiers, payouts, coupons, creatives, and a self-service affiliate portal."
sidebar:
  order: 4
---

EP Affiliate is a full affiliate programme for PageMotor. Recruit partners, track every referral via first-party cookie, calculate tiered commissions, process payouts, and give affiliates their own self-service portal with stats, marketing creatives, and a leaderboard.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

An affiliate is a partner who sends visitors to your site via a unique referral link. When those visitors convert (make a purchase, place a booking, take any action you decide counts), the affiliate earns a commission.

What you get:

- **Affiliate applications** with an optional auto-approval toggle, honeypot anti-spam, CSRF protection, and GDPR consent logging on signup.
- **Referral tracking** via a `?ref=CODE` URL parameter stored in a first-party cookie. Choose first-touch or last-touch attribution.
- **Commission tiers** as percentage or flat rate, with a configurable hold period before auto-approval for payout.
- **Recurring commissions** on subscription renewals (optional).
- **Payout management** with a minimum payout threshold so you are not cutting £2 payments.
- **Self-service portal** with stats, marketing creatives, leaderboard, and magic-link access for affiliates who lose their password.
- **Coupon codes** tied to affiliates, so a discount code also attributes the referral.
- **Marketing creatives** library: upload banners, landing page links, and any asset you want affiliates to share.
- **Email notifications** via EP Email (welcome, approval, admin alerts on new applications).
- **Fraud detection** module that flags suspicious referral patterns.
- **Six-language i18n**: de, es, fr, it, nl, pt.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite 1.9 or later**
- **EP Email** (required for notifications)

## Installation

1. **Download** `ep-affiliate.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. **Sign in to your PageMotor admin** at `yourdomain.com/admin/`.
3. **Go to Plugins, then Manage Plugins.**
4. **Upload the zip.**
5. **Activate in your Theme.** Database tables are created on first load.

## Setting up your programme

Open **Plugin Settings → EP Affiliate** and work through the sections top to bottom.

### General

- **Programme name.** Shown to affiliates in emails and the portal.
- **Terms URL.** Link to your affiliate terms of service. Required for GDPR consent on signup.
- **Registration open.** Toggle accepting new applications.
- **Auto-approve.** If on, new applications become active immediately. If off, you approve each one manually from the Affiliates tab.
- **Portal page slug.** The page on your site that hosts `[ep-affiliate-portal]`. Used for magic links sent to affiliates.

### Commissions

- **Default rate.** Percentage (e.g. `10`) or flat amount (e.g. `5.00`).
- **Commission type.** Percentage of sale, or flat per conversion.
- **Cookie duration.** 7 to 365 days. How long after clicking a referral link a visitor is still attributed to the affiliate.
- **Attribution model.**
  - **First-touch:** the first affiliate who ever referred the visitor wins the commission.
  - **Last-touch:** the most recent affiliate wins.
- **Hold period.** 0 to 60 days. Commissions sit in "pending" status during hold, then auto-approve for payout. Gives you time to catch refunds before paying.
- **Minimum payout threshold.** Commissions accrue until the affiliate's unpaid balance hits this amount.

### Recurring commissions

If your site sells subscriptions (via EP Ecommerce Subscriptions or similar), enable this so the affiliate earns commission on every renewal, not just the first sale.

### Affiliates

Lists every affiliate. Approve or reject pending applications, view each affiliate's stats, edit their commission tier, or flag them as fraudulent.

### Tiers

Create tiers with custom commission rates. Assign affiliates to tiers as they grow. Common pattern: default 10%, silver 15%, gold 20%.

### Payouts

Shows every affiliate whose unpaid balance is over the minimum threshold. Mark payouts as paid once you have sent the money via your preferred method (the plugin does not process payments directly, it tracks what is owed).

### Creatives

Upload banners (PNG, JPG, WebP), or add link-only creatives (landing page URLs with pre-tracked parameters). Affiliates see these in their portal and can copy the code or download the asset.

### Coupons

Coupon codes that tie to a specific affiliate. When a visitor applies the code at checkout, the sale is attributed to that affiliate even if they did not click a referral link. Useful for influencers who promote via codes rather than links.

## Shortcodes

Place these on any page to expose affiliate features to the public.

| Shortcode | Purpose |
|---|---|
| `[ep-affiliate-apply]` | Application form for new affiliates. Place on a public page like `/become-an-affiliate/`. |
| `[ep-affiliate-portal]` | Full self-service dashboard. The page containing this shortcode is what the **Portal page slug** setting points to. |
| `[ep-affiliate-link]` | Generate an affiliate referral link. For use inside the portal or in docs. |
| `[ep-affiliate-stats]` | Display summary statistics (clicks, conversions, commission this month). |
| `[ep-affiliate-creatives]` | Browse and copy marketing creatives. |
| `[ep-affiliate-leaderboard]` | Public or portal-only leaderboard of top affiliates. Good for motivation. |

## Tracking how referrals work

1. Affiliate shares a link like `https://yoursite.com/?ref=ALICE123`.
2. Visitor clicks. The plugin reads `?ref=` and sets a first-party cookie with the code. Cookie life matches the **Cookie duration** setting.
3. Visitor browses. The `ref` parameter no longer needs to be in the URL, the cookie carries the attribution.
4. Visitor converts (sale, booking, signup — whatever your code reports to EP Affiliate). Commission is logged against Alice's account.
5. Commission enters **hold** for the configured hold period. During hold you can refund a sale and the commission is voided.
6. After hold, commission auto-approves. It sits in the affiliate's unpaid balance until their balance crosses the **minimum payout threshold**.
7. When you are ready to pay, go to **Payouts**, click **Mark as paid**, and send the money via your preferred method.

## Fraud detection

The fraud module watches for common affiliate scams:

- **Self-referral:** an affiliate trying to claim commission on their own purchases.
- **Referral bombing:** one IP generating many clicks with different affiliate codes.
- **Cookie stuffing:** embedding referral codes in hidden iframes.

Flagged referrals are held for manual review rather than auto-approved. Review them in the Affiliates tab.

## GDPR and legal

- The application form includes GDPR consent that logs into EP GDPR's consent table if EP GDPR is installed.
- A **Terms URL** is required so applicants are consenting to something specific.
- Affiliate data is per-user in your database. If an affiliate invokes their GDPR right-to-deletion, the corresponding rows are removed through EP GDPR's workflow.

## Troubleshooting

### "Applications are not sending the admin email"

Check EP Email is installed, activated, and has working SMTP. The plugin fires notifications through EP Email's queue, so if EP Email is broken, affiliate emails are queued but not sent.

### "Referrals are not being tracked"

Three things to check:

1. Are first-party cookies blocked? Some browsers (Safari Private) block everything. Not much you can do.
2. Is the `?ref=CODE` making it to the page? If your infrastructure strips query strings (some caching layers do), attribution never happens.
3. Is your site served over HTTPS? Mixed-content cookies can fail silently in some browsers.

### "Commissions are not calculating"

The plugin only calculates commission when your other plugin (ecommerce, bookings, whatever) reports a conversion to EP Affiliate. Check that your conversion source is calling the commission API.

### "Affiliate cannot log into the portal"

Send them a magic link from the Affiliates tab. This bypasses any forgotten credentials.

### "A fraudulent affiliate is signing up repeatedly"

Turn off **Registration open** temporarily. Review the Affiliates list, mark the bad account as fraudulent (this blocks future signups from the same email and IP).

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues). Corrections land quickly.
