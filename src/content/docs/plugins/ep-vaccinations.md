---
title: "EP Vaccinations"
description: "Pet vaccination tracking for PageMotor boarding sites. Clients upload a photo of the vaccination card, Claude reads the vaccines and expiry dates, renewal reminders go out automatically, and a lapsed vaccine blocks new bookings until it is renewed."
---

EP Vaccinations keeps a kennel, cattery or boarding business on the right side of its own vaccination rules without anyone having to chase paperwork.

A client uploads a photo or PDF of their pet's vaccination card. Claude reads the vaccines and their expiry dates off the image. You confirm what it read against the picture, so the record you rely on has been checked by a human. From then on the plugin emails the client as each vaccine approaches expiry, and once a confirmed vaccine lapses past your grace period that client cannot make a new boarding booking until it is renewed.

This page documents EP Vaccinations **0.2.4**.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

1. A signed-in client opens your vaccination page and sees a card for each of their pets.
2. They upload a photo or PDF of the vaccination record. The file is stored in a deny-all protected folder, not in your public uploads.
3. Claude reads the card and proposes a list of vaccines with expiry dates.
4. You review each proposed line against the uploaded image and confirm or correct it. Nothing counts until it is confirmed.
5. A daily job emails the client as a confirmed vaccine approaches its expiry date, starting the number of days before that you choose.
6. Once a vaccine has been expired for longer than your grace period, the client is blocked from making a new booking, and you can have the business copied in when that happens.
7. The block clears by itself when a fresh card is uploaded and confirmed.

One client can hold several pets, each with its own record.

## Requirements

- **PageMotor 0.9 or later**
- **EP Email**, with a working transport, for the reminder and notification emails
- **EP Cron**, which runs the daily expiry sweep
- **EP Boarding**, if you want lapsed vaccines to actually block bookings. Without it the tracking, reminders and blocking flag all still work; nothing consumes the flag.
- An **Anthropic API key**, used only to read uploaded cards. Card reading is billed to your own key.

## Installation

1. Download `ep-vaccinations.zip` from your Updates screen, or from the EP Suite downloads page.
2. Upload it under **Plugins → Manage Plugins**, then activate it.
3. Open **EP Suite → Vaccinations** and fill in the settings below.
4. Put `[ep-vaccination-card]` on a page your clients can reach when signed in.

## Settings

- **Remind from (days before expiry).** How early the renewal emails start. Default 30.
- **Grace period after expiry (days).** How long after a vaccine expires before that client is blocked from booking. Default 7.
- **Owner notification email.** Where to copy the business when a client is newly blocked. Optional.
- **Anthropic API key.** Used only for reading uploaded cards.
- **Model.** Which Claude model reads the cards.

## The client panel

`[ep-vaccination-card]` renders the client panel. It is sign-in gated: a visitor who is not signed in sees nothing of anyone's records.

The older `[vaccination-card]` and `[vaccination_card]` forms still work, as deprecated aliases. New pages should use the `ep-` prefixed name, which cannot be shadowed by a core or sibling-plugin shortcode.

## How the booking block works

The plugin exposes the block as a yes or no answer about a client, and EP Boarding asks that question before it accepts a booking. A blocked client sees the refusal at the point of booking rather than discovering it on arrival.

Nothing is blocked on an unconfirmed reading. Only a vaccine you have confirmed against the image, and which has then expired beyond the grace period, blocks anything.

## Privacy

Uploaded cards carry a client's name and their vet's details, so they are stored in a protected folder that the web server refuses to serve directly. The card image is sent to Anthropic for reading and is not used for training. Confirmed vaccine names and dates are kept in the site database.

## Changelog

### 0.2.4

- **Fixes a crash on the vaccination card upload form when an older EP plugin is installed on the same site.** Submitting the form returned an internal error and nothing was saved or sent. EP plugins share one common code library, and whichever copy loads first is the one every EP plugin on that site uses, so a single out-of-date plugin could leave this one calling a spam check its copy did not have. The check now carries its own fallback and no longer depends on another plugin being up to date.
- No change on a site where this never happened: the same spam check runs, and nothing else changed.

### 0.2.3

- **Blocks a spam bot that was getting past the form honeypot.** The scraper changed its network address on every request, so blocking by address never caught it, but it always sent a malformed browser identifier that no real browser sends. Forms now reject anything carrying that signature, with the same silent response a caught bot already got.

### 0.2.2

- The client panel shortcode is now `[ep-vaccination-card]`. The older `[vaccination-card]` and `[vaccination_card]` names still work, so existing pages are unaffected, but the prefixed name is the one to use from here. The prefix means no core or other plugin can ever take the name over.

### 0.2.1

- Maintenance: refreshed the shared EP Suite code to the current version. No change to this plugin's own features.

### 0.1.0

- First release. Multi-pet records per client, a sign-in gated client panel with upload, card storage in a protected folder, reminder and grace settings, the booking-block contract, and the daily job that drives reminders.
