---
title: "TIB AI Dashboard"
description: "The business owner's landing page, in plain English: whether the site is healthy, how it looks on Google and when shared, and one suggested next thing to do."
---

TIB AI Dashboard is what a business owner sees when they sign in to their own site. It leads with reassurance rather than statistics: the site is live and healthy, this is how it looks when someone finds it on Google or shares it in a message, and here is one thing worth doing next.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Reassurance first.** The top of the page tells you the site is live and working, in those words, before anything else.
- **How your site looks to other people.** A preview of your Google result and of the card that appears when someone shares your site in a message.
- **Your business details, editable in place.** Your name, address, hours and contact details, changed without leaving the page.
- **One suggested action at a time.** Not a list of twelve things. One, with the next appearing when that one is done.
- **Your pages and your conversations**, listed plainly.
- **Your own photographs.** Upload a logo or a photograph yourself, in the usual image formats, rather than asking anyone to put it on the server for you.
- **Where your site came from.** A link back to the interview the site was built from.
- **Nothing here can break the site.** No jargon, no percentages, and no control that leaves you worse off than before you touched it.

## Requirements

- **PageMotor 0.10 or later**

## Installation

Installed as part of the build, and appears automatically for an account with owner access.

## Changelog

### 0.10.9

- **Fixes the assistant damaging a page when asked to move something.** Asked to move content from one page to another, the assistant could write the change back in a form browsers cannot read, which broke images and styling on a live page while reporting that nothing had happened. It could also place new content inside the site footer rather than the page body.
- Two checks now refuse both before anything is written, and tell the assistant exactly what to correct. Ordinary edits to footer text, a phone number or an email address, are unaffected: those are normal requests and still work.
- Verified by replaying the exact change that caused the damage, which is now refused, while a plain phone-number edit and a clean new section both still succeed.

### 0.9.5

- **Connecting your AI stops being a task once you have done it.** The panel folds away into a reference once something is actually connected, instead of continuing to sit on your dashboard as an outstanding job. It reads the same source as the Connected Apps screen, so it cannot disagree with what you see there.

### 0.9.4

- **The dashboard is a panel, not a wall.** It had grown to eleven stacked sections and roughly twelve thousand pixels of scrolling, with the way back to the admin at the very bottom. Sections are now grouped by what they are for, and the ones you have finished with collapse.

### 0.9.2

- **The assistant panel can no longer both read your site and change it through the same route.** The route it used to fetch a page could also write one. It is now limited to reading on that path, and writes go through the checked route only.

### 0.9.1

- **Separates what the assistant reads from what it can do.** This panel is the most capable assistant on the site: it can edit and create pages, set images and install software. It also reads your site's content, and a site built from an interview contains text gathered from elsewhere on the web. That is a path, however indirect, from a stranger's page to an assistant that can install things. This release closes it.

### 0.9.0

- **You can add your own photographs.** Until now you could only swap an existing picture, never add a new one, so a new logo or photograph had to be put on the server for you. You can now upload JPG, PNG, WebP, GIF and SVG yourself, through the same upload path the share card has always used.
