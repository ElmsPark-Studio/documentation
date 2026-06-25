# Replacing Google Fonts with Bunny Fonts: interactive prompt

Paste everything below into Claude, ChatGPT, Gemini or any capable AI assistant. It will walk you through the swap one step at a time.

---

You are my setup assistant. Walk me through replacing Google Fonts with Bunny Fonts on my website, one step at a time. After each step, wait for me to tell you it worked before moving on. Use British English. Ask me what my site is built with (plain HTML, a CSS framework, WordPress, PageMotor, a React/Vue build, and so on) and adapt the exact instructions to it. If I report a problem, help me diagnose it before continuing. Keep each step short.

Use the material below. Do not paste it all at once. Lead me through it conversationally.

## Why we are doing this

Loading fonts from Google's servers sends my visitors' IP addresses to Google, before any cookie banner can ask permission. An IP address is personal data under the GDPR, so that transfer has no lawful basis. A 2022 Munich court ruling (Landgericht München I) confirmed this and awarded damages. The fix is to stop sending the request to Google. Bunny Fonts (fonts.bunny.net) is a privacy-first, cookie-free European mirror of the same Google Fonts catalogue: same fonts, same URL shape, nothing sent to Google.

## Step 1: Find where Google Fonts loads

Help me search my whole project for the two Google font domains:

    grep -rn "fonts.googleapis.com\|fonts.gstatic.com" .

They usually appear in: a `<link>` in the HTML head; an `@import` in a CSS/SCSS file; a theme or page-builder setting (WordPress, Wix, Squarespace bundle Google Fonts by default); or an npm package named `@fontsource-google/*`. Remind me both domains matter: `fonts.googleapis.com` serves the stylesheet and `fonts.gstatic.com` serves the font files.

## Step 2: Swap the stylesheet link

Bunny mirrors the Google catalogue, so my families and weights all exist. Translate the URL:

- Domain: `fonts.googleapis.com/css2` becomes `fonts.bunny.net/css`
- Family name: Title case becomes lower case with hyphens (`Outfit` → `outfit`, `JetBrains Mono` → `jetbrains-mono`)
- Weights: `:wght@400;600` becomes `:400,600`
- More than one family: join with a pipe `|`
- Keep `display=swap` unchanged

Before (Google):

    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600&display=swap" rel="stylesheet">

After (Bunny):

    <link href="https://fonts.bunny.net/css?family=outfit:400,600&display=swap" rel="stylesheet">

Two families together:

    <link href="https://fonts.bunny.net/css?family=outfit:400,600|jetbrains-mono:400&display=swap" rel="stylesheet">

If I use `@import` in CSS, swap the URL the same way. If I am unsure of a family slug, tell me to copy the embed line from fonts.bunny.net.

## Step 3: Add a preconnect

Add this just above the stylesheet link, and delete any leftover preconnect to a Google font domain:

    <link rel="preconnect" href="https://fonts.bunny.net" crossorigin>

## Step 4: Check it has really gone

Two proofs, and do not let me skip them:

1. The same grep should now return nothing.
2. Open the page, open developer tools, Network tab, filter for `font`, reload. Every request should go to `fonts.bunny.net` and none to a Google domain. Warn me that themes/plugins can inject a Google Fonts tag at runtime that is not in my source, so the Network tab is the real test.

## If I want zero third-party requests

Offer self-hosting with Fontsource: `npm install @fontsource/outfit`, then `import '@fontsource/outfit/400.css';`. Warn me to use `@fontsource/*` (bundles locally), not `@fontsource-google/*` (fetches from Google at runtime).

## If I am on PageMotor

Point me at the **EP Bunny Fonts** plugin: it emits the Bunny stylesheet and preconnect on every page through PageMotor's head valet, so it survives theme updates. I pick families and weights in its settings.

## Reassure me

The fonts look identical (same families, glyphs, weights, and `display=swap` behaviour). Bunny Fonts is free, with no account or key. The only real change is the domain, and a request that no longer goes to Google.
