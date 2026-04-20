---
title: "EP Voice Messages"
description: "Voice message recording widget for PageMotor. Visitors record audio in the browser, submission is transcribed, admin gets email notification with audio and transcript."
sidebar:
  order: 58
---

EP Voice Messages adds a voice recording widget to PageMotor. Visitors click, record, and submit audio directly from their browser — no file uploads, no phone calls. The message is transcribed automatically, the admin gets an email notification with the audio file and the transcript.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Use cases:

- **Voice feedback on a page.** "What do you think of this article?" — voice replies instead of typing.
- **Testimonials.** Authentic-sounding testimonials in the customer's own voice.
- **Bug reports.** Visitors describe the problem out loud, easier than typing.
- **Accessibility.** Some users find voice easier than keyboard input.

## How it works

1. Visitor clicks the record button on your page.
2. Browser asks for microphone permission.
3. Visitor records. A timer shows elapsed seconds.
4. Visitor clicks stop, then submit.
5. Audio uploads to your server.
6. A background transcription job runs (using OpenAI Whisper or similar).
7. Admin gets an email via EP Email with the audio as attachment and the transcript inline.

## Requirements

- **PageMotor 0.7 or later**
- **EP Email** (for admin notification)
- **EP Suite base class**
- **A transcription API key** (OpenAI Whisper, AssemblyAI, or configured alternative)

## Installation

1. Install EP Email.
2. Download `ep-voice-messages.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Configure the transcription provider API key in settings.
5. Drop `[voice-message]` on any page.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[voice-message]` | Record widget. Attributes: `max_seconds=60` (default 60), `prompt="Tell us..."` (default generic). |
| `[voice-messages-inbox]` | Admin-only inbox view of all received messages with playback and transcript. |

## Settings

- **Transcription provider.** OpenAI Whisper, AssemblyAI, or others.
- **API key.**
- **Max recording duration.** Enforced client-side (prevents huge uploads). Default 60 seconds.
- **Admin notification email.** Where notifications go.
- **Storage.** Where to save audio files. Default is `user-content/uploads/voice-messages/<date>/`.
- **Auto-delete after.** Days. Default 90. Set to 0 for no auto-delete.

## Admin view

From `[voice-messages-inbox]` on an admin-only page:

- List of every received message.
- Play each in-browser.
- Read the transcript.
- Download the audio file.
- Delete individual messages.

## Privacy

- Recordings are stored on your server, not a third-party service (the transcription API does process them briefly to generate the transcript, but doesn't store).
- Visitors grant microphone permission per-session. No persistent tracking.
- GDPR-wise: voice is personal data. If a visitor invokes right-to-erasure, delete their recordings manually. EP GDPR integration may help.

## Troubleshooting

### "Record button doesn't request mic permission"

Browser quirk. Check the page is HTTPS (mic requires secure context). Some extensions block mic requests; test in incognito.

### "Recording works but submission fails"

Check max file size vs PHP upload limits. A 60-second recording is typically 500KB to 1MB. PHP defaults usually handle that, but if you have low limits, raise them.

### "Transcript is inaccurate"

Whisper is usually very good but struggles with heavy accents, background noise, or unusual names. Transcripts are a convenience; the original audio is the source of truth.

### "Admin notification didn't arrive"

Check EP Email log. Also check the transcription finished — if transcription fails (API timeout), the whole job might fail.

### "Audio files are filling up disk"

Auto-delete is on by default at 90 days. Verify. Or clean up manually from the storage path.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
