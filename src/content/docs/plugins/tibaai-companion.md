---
title: "TIB AI Companion"
description: "Turns the wait while your site is being built into a useful session: your share cards appear one by one as the progress, and an assistant helps you get ready to launch."
---

TIB AI Companion fills the gap between finishing your interview and your site going live. Instead of a spinner, you get your pages appearing one at a time and an assistant to talk to while you wait.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Your pages are the progress bar.** As each page is finished, the card that will represent it when it is shared appears on screen. No percentages and no jargon: you can see the site arriving.
- **An assistant to use the time with.** It talks about getting the word out, what to say in your launch announcement, asking customers for reviews, which photographs are worth taking, and what your new site can actually do.
- **Anything useful is kept.** Notes made during the wait are saved, so your dashboard can act on them once the site is live rather than you having to remember.
- **It cannot touch the site while it is being built.** The assistant can save a note, record something you asked for, and look up what is available. It cannot edit a page. Your site is mid-build, and a second writer racing the builder would be reckless.
- **It will not promise you anything.** If you ask for something that does not exist, it says so plainly and records exactly what you asked for. It is not allowed to say "soon" or "the team is working on that", because it does not know that, and a promise made here would be a broken promise on your first day.

## Requirements

- **PageMotor 0.6 or later**

## Installation

Installed as part of the build. There is nothing to configure: the companion appears on its own while your site is being built, and steps aside once it is live.

## Changelog

### 1.0.2

- **Fixes the plugin never appearing on your Updates screen.** PageMotor only offers updates for a plugin that tells it where to look, and this one did not, so it had been invisible to the update check since release. Getting onto this version needs one manual upload; after that updates arrive normally.

### 1.0.1

- **Fixes the companion using your site's title instead of your business name.** It looked for the business name under a key that has never existed, so it always fell back to the site title. It now reads the name your business details actually store it under, on both current and older PageMotor versions.

### 1.0

- First release.
