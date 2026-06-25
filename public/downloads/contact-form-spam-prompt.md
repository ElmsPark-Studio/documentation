# Stopping contact-form spam without CAPTCHA: interactive prompt

Paste everything below into Claude, ChatGPT, Gemini or any capable AI assistant. It will walk you through implementing each layer one step at a time.

---

You are my setup assistant. Walk me through stopping contact-form spam without a CAPTCHA, one layer at a time. After each layer, wait for me to confirm I have implemented it before moving on. Use British English throughout. Ask me what language and framework my form handler is built in (PHP, Node, Python, Ruby, and so on) and adapt the code examples accordingly. If I report a problem, help me diagnose it before continuing. Keep each step short and practical.

Use the material below. Do not present it all at once. Lead me through it conversationally, checking in after each layer.

## Why we are doing this

CAPTCHAs add friction for every real visitor in order to stop bots. They hurt accessibility, slow conversions, and leak data to the CAPTCHA provider. Modern bots and commercial solving services bypass them within seconds. The layered server-side approach below is invisible to real visitors and catches the vast majority of automated spam without a single puzzle.

## Step 1: The honeypot field

Add a hidden text input to the form. Give it an innocuous name such as `website` or `url`. Hide it with CSS (`display:none` or `position:absolute; left:-9999px`) rather than the `hidden` attribute, since some bots skip hidden-attribute fields. On the server, reject any submission where that field is not empty.

Real people never see the field, so they never fill it in. Bots fill every field they find and trip the trap immediately.

## Step 2: The time trap

Record a timestamp when the form loads (in a hidden field or a server session). On submission, compare that timestamp to the current server time. Reject any submission that arrives faster than a human could reasonably fill in the form. A default of 3 seconds suits most contact forms. Raise to 5 seconds for short forms; lower to 2 only if real visitors report failures.

This catches scripted submitters that bypass the honeypot but still move faster than any human.

## Step 3: Rate limiting by IP

Store the IP address and timestamp of each accepted submission. On each new submission, check whether that IP has submitted within a rolling window (5 minutes is a sensible default). If so, reject the new submission.

For sites that serve audiences from shared corporate or campus IPs, consider allowing 2 submissions per IP per window rather than 1, and review if false positives appear.

## Step 4: Content heuristics, link caps and keyword blocklists

Two checks on the message content itself:

**Link cap.** Count the number of `http://` or `https://` URLs across all submitted fields. Reject if the total exceeds a maximum (2 is a safe default for a contact form). SEO spam and link-building pitches almost always include several URLs. Set the cap to -1 to disable.

**Keyword blocklist.** Maintain a list of phrases, one per line, case-insensitive substring match against all text fields. Common starters:

    bitcoin
    crypto
    casino
    seo services
    guest post
    backlink
    link building
    rank higher
    viagra
    cialis

Tune the list to the spam you are actually receiving. Keep it short and specific: broad terms cause false positives.

Run content checks after the honeypot and time trap, so most spam is already rejected before any text scanning.

## Step 5: A shared blocklist, the network effect

Track the IP addresses caught by your local filters. Report them to a central service. Fetch the aggregated list of IPs reported by all other installs, filtered to a minimum severity (for example, only block IPs reported by 3 or more independent sites). Check the incoming IP against this cached list before any other processing.

The value is pre-emptive: a bot IP that hit a dozen other sites before reaching yours is stopped on arrival. A severity of 2 or 3 (corroboration from multiple sources) is a safer default than 1 (single-report blocking).

## Optional capstone: AI triage

For borderline submissions that pass all five layers, you may optionally pass the message text to a language model with a short spam/ham classification prompt. Route only borderline cases through this step, not every submission. Use a quarantine folder rather than silent deletion so you can review false positives. Run this step last and only when cheaper checks have already passed the submission.

This is an advanced option and is not part of the core five-layer setup.

## Tuning advice to share with me

Run checks in order of cost: IP blocklist first, then honeypot, time trap, rate limit, content heuristics, AI triage last. Log all rejected submissions with the reason that fired: you cannot spot false positives in data you are not keeping. Review the keyword list monthly and adjust the time threshold if you see legitimate rejections.
