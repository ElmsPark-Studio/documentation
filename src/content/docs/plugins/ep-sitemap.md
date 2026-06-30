---
title: "EP Sitemap"
description: "Dynamic XML sitemap for PageMotor. Generated on every request from live content, respects Meta Robots noindex, no files written to disk."
---

EP Sitemap intercepts requests for `/sitemap.xml` and returns a standards-compliant XML sitemap built on the fly from your live PageMotor content. No physical file is written to disk; every request renders the current state of the site.

Published by [ElmsPark Studio](https://elmspark.com).

## What EP Sitemap does

- **Dynamic generation.** Every hit on `/sitemap.xml` runs a single SQL query and returns fresh XML. No "rebuild" step.
- **Standards-compliant.** Emits `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">` with `<loc>` and `<lastmod>` per URL.
- **Respects Meta Robots noindex.** Any page flagged noindex via PageMotor's core Meta Robots plugin is excluded automatically.
- **Exclude by slug.** A textarea in settings lets you exclude specific pages by slug, one per line.
- **Lastmod from modified date.** Uses each row's `modified_gmt` if present, falls back to `date_gmt`.
- **Subdirectory installs supported.** If PageMotor lives under a subdirectory, the interceptor strips the install slug before matching.
- **Physical file override.** If a real `sitemap.xml` exists in your site root, the web server serves that file directly and EP Sitemap stays out of the way.
- **Bing notify** with one click and step-by-step Google Search Console instructions on the settings page.
- **EP Txt Files integration.** If EP Txt Files is active, one click adds the `Sitemap:` line to your `robots.txt`.

## What EP Sitemap is NOT

- An image sitemap, video sitemap, or news sitemap generator. Just URLs.
- A sitemap index. Single `<urlset>` only. PageMotor sites are well under the 50,000-URL ceiling.
- A multilingual (hreflang) sitemap. PageMotor is not multilingual at the page level.
- A way to add external URLs to the sitemap. The output is derived strictly from your content table.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class** (bundled)
- Optional: **EP Txt Files** for the one-click `Sitemap:` line in `robots.txt`
- Optional: **Meta Robots** (PageMotor core plugin) if you want noindex flags honoured

## Installation

1. Download `ep-sitemap.zip` from the [EP Suite downloads page](https://updates.elmspark.com/download.php?plugin=ep-sitemap).
2. Upload via **Plugins, then Manage Plugins**. Activate.
3. Visit `https://yoursite.com/sitemap.xml`. You should see XML.
4. Submit the URL to Google Search Console (Indexing, then Sitemaps). Use the **Notify Bing** button on the settings page, or submit manually at bing.com/webmasters.

## Settings

- **Exclude Pages.** Textarea, one slug per line. The slug is the last part of a page URL. So to exclude `https://example.com/privacy-policy/`, type `privacy-policy`. No slashes, no full URL.
- **Preview.** Two buttons. **View Sitemap** opens `/sitemap.xml` in a new tab. **Regenerate Preview** runs the generator and shows the first 20 URLs in the settings page along with the total URL count.
- **Search Engines.** **Notify Bing** button and printed step-by-step instructions for submitting to Google Search Console.

## Custom content types

EP Sitemap defers to PageMotor's own enumerator, `$motor->content->types_with_url(true)`, to decide which content types are URL-bearing on the front end. Reading the filter logic in `lib/content.php`, the rule is straightforward: include every content type that has a URL and is enabled in the `theme` environment.

On a vanilla PageMotor 0.8.3b install with the EP Suite active, the complete set of registered content types is:

| Source | Type | Appears in `/sitemap.xml`? |
| --- | --- | --- |
| PM core | `home` | Yes (one row) |
| PM core | `page` | Yes |
| PM core | `error` | No: `no-slug` and not `home` |
| PM admin | `admin-content`, `admin-plugins`, `admin-themes`, `admin-theme` | No: `environment` is admin-only |
| Bundled `modular-content` plugin | `modular` | No: no `url` flag (used as embedded blocks, not standalone pages) |
| [EP Events](/plugins/ep-events/) | `event` (plus 12 sub-types: conference, workshop, meetup, webinar, etc.) | Yes |
| [EP Locations](/plugins/ep-locations/) | `location` | Yes |

### Minimum registration for sitemap inclusion

If you have a custom content type registered by your own plugin or theme and its rows are not appearing in `/sitemap.xml`, your registration needs:

```php
'url'         => true,
'environment' => ['theme'],   // 'theme' must be present
// AND not 'no-slug' (unless the type is 'home')
```

`'theme'` is the only environment value required for sitemap inclusion. Add `'admin'` only if you want the type to be manageable from PageMotor's admin Content area, which for most custom content types you probably don't want.

### Worked examples

A type your code populates programmatically (an importer, a feed processor, a derived archive). The rows live in the database and are not edited by site admins:

```php
public function content_types() {
    return [
        'post' => [
            'name'        => 'Imported Post',
            'environment' => ['theme'],
            'url'         => true,
            'fields'      => ['title', 'content'],
        ]
    ];
}
```

A type that IS edited by site admins (the EP Events case — event records are managed in admin Content and also render on the front end). It uses both environments by design:

```php
public function content_types() {
    return [
        'event' => [
            'name'        => 'Event',
            'environment' => ['admin', 'theme'],
            'url'         => true,
            'fields'      => ['content-info', 'title', 'content-url', 'content'],
        ]
    ];
}
```

Both register correctly with EP Sitemap because both have `'theme'` in their environment array. The difference is whether the type also surfaces in admin Content for human editing.

### Most common miss

Leaving `'theme'` out of the `environment` array, or omitting the `environment` key entirely. `'theme'` is what tells PageMotor "this type renders on the public site", and EP Sitemap requires it to include the type. Fix that one entry and EP Sitemap picks the type up on the next request.

## Search engine submission

### Bing

The settings page has a **Notify Bing** button that pings Bing's sitemap endpoint. One click, no account required.

Note that Microsoft retired their classic `bing.com/ping?sitemap=` endpoint in May 2022 in favour of IndexNow. The button still completes successfully but Bing's behaviour on that endpoint is no longer documented. The reliable route for Bing is to submit your site directly at [Bing Webmaster Tools](https://www.bing.com/webmasters/).

### Google

Google requires a free Search Console account. Submit your sitemap once:

1. Sign in to [Google Search Console](https://search.google.com/search-console).
2. Add your site as a property and verify ownership (the HTML tag method is easiest).
3. In the left sidebar, click **Indexing**, then **Sitemaps**.
4. Paste your sitemap URL (`https://yoursite.com/sitemap.xml`) and click Submit.

Google starts checking the sitemap within a few days. One submission is enough; you do not need to resubmit when the sitemap changes.

### robots.txt

Search engines that crawl `robots.txt` discover the sitemap automatically if you add a `Sitemap:` line. If EP Txt Files is active, the EP Sitemap settings page surfaces a one-click **Add Sitemap Line** button. Otherwise add this manually:

```text
Sitemap: https://yoursite.com/sitemap.xml
```

## Troubleshooting

### `/sitemap.xml` returns the wrong content or a 404

Check for a physical `sitemap.xml` file in your site root. If one exists, the web server serves it directly and EP Sitemap never runs. The status card on the settings page surfaces this as **Blocked**. Delete the physical file to use dynamic serving.

### A specific page is not appearing

Check, in order:

- The page status is **live** (not draft or trash).
- The page is not marked **noindex** in its Meta Robots options.
- The page slug is not in the **Exclude Pages** list on the settings page.
- The page's content type has `url => true`, `environment` includes `theme`, and is not `no-slug`. See [Custom content types](#custom-content-types) above.

### A whole content type is missing

This is almost always a registration shape issue, not a sitemap issue. See [Custom content types](#custom-content-types) above for the three required flags. EP Sitemap defers entirely to PageMotor's core enumerator, so if PageMotor itself does not consider your type URL-bearing, EP Sitemap will not include it.

### Lastmod dates look off by a few hours

EP Sitemap emits `<lastmod>` in UTC (suffix `+00:00`). If your local timezone is not UTC, the printed datetime will not match what you see in PageMotor's admin (which displays local time). This is by design and matches the sitemaps.org spec.

### Bing notify says "Could not reach Bing"

Outbound HTTP from your server is blocked or Bing is throttling. Submit manually at [Bing Webmaster Tools](https://www.bing.com/webmasters/) instead.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger, a bug report, a feature request, or a "how do I" that needs a real reply, open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
