---
title: "EP Media Storage"
description: "Serve paid videos, audio and downloads from your own S3-compatible bucket behind links that expire, so a shared link stops working instead of giving your content away. Works automatically with EP Courses."
---

EP Media Storage serves paid media from your own object storage behind links that expire. A member watches a lesson normally and notices nothing. A link copied out of the page is dead by the time it reaches anyone else.

It works with any S3-compatible store: Amazon S3, Cloudflare R2, Backblaze B2, Wasabi and self-hosted MinIO.

Published by [ElmsPark Studio](https://elmspark.com).

## Status

**Version 0.1.0, released 4 August 2026.** The link signing is tested against a live bucket and the plugin has been proven end to end alongside [EP Courses](/plugins/ep-courses/) on a PageMotor site. It is on the same licence tier as EP Courses, so if you have that, this is covered.

Because it is new rather than an update, the first copy has to be uploaded by hand: ask at [help.elmspark.com](https://help.elmspark.com) and we will send the zip. After that it updates through your **Updates** screen like everything else.

You also need **EP Courses 0.4.12 or later** for protected lesson videos. That one arrives in your Updates screen on its own.

## The problem it solves

Gating a page is not the same as gating a file.

A course lesson can be perfectly locked to enrolled students while the video URL printed inside that page is an ordinary bucket link. Anyone who views the page can copy that link, and it keeps working for anyone they send it to, indefinitely, because the file itself was never checked. The gate is on the door and not on the file.

That is the exact hole this plugin closes. Instead of the plain bucket URL, the page receives a **presigned URL**: the same file, addressed with a cryptographic signature and an expiry stamped into the address. Your storage provider checks the signature and the clock before it serves a byte.

## What it does

- Signs every media link with **AWS Signature Version 4**, the same mechanism your storage provider uses internally.
- Lets you set how long a link lives, from thirty minutes to twenty-four hours. Two hours is the default.
- Serves protected media through the `[ep-media]` shortcode anywhere on your site.
- Protects [EP Courses](/plugins/ep-courses/) MP4 lessons automatically, with nothing to configure in EP Courses itself.
- Leaves anything outside your bucket alone, so YouTube and Vimeo lessons carry on exactly as before.
- Offers `media_storage_status` and `sign_media_url` as admin actions, so your AI assistant can check the configuration or mint a one-off link.

## What it does not do

Be clear-eyed about this before you promise anything to your own customers.

**It does not stop an entitled viewer downloading the file while their link is valid.** Somebody watching a lesson can capture the stream inside that window. No link-based scheme prevents that, and the large course platforms sit in exactly the same position. Preventing it needs DRM, which brings its own costs, browser restrictions and customer complaints.

What expiring links do stop is the link travelling, which is how paid content usually escapes in practice: a member pastes a URL into a chat group, and by the time anyone clicks it the link is dead.

**It does not decide who is entitled.** EP Courses knows about enrolment and EP Membership knows about membership. Each does its own check and then asks this plugin for a link. That separation is deliberate: it means this plugin never has to learn anyone's access rules.

**It does not write to your storage.** A read-only key is all it needs, and all you should give it.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class**
- A bucket on an S3-compatible provider, and a read-only access key scoped to it

Optional but the obvious pairing:

- **[EP Courses](/plugins/ep-courses/)** 0.4.12 or later for automatic protection of lesson videos.

## Installation

1. Upload the zip via **Plugins, then Manage Plugins, then Upload**.
2. **Tick it in the plugin list, then press Save Plugins.** There is no Activate button in PageMotor: the tick box is the switch, and it only takes effect when you save.
3. Open **EP Media Storage** in your admin settings.
4. Fill in your bucket details and keys, as below.
5. Tick **Enable protected media** and save.

Until you tick that box, every link is served exactly as entered, so you can install and configure without changing what your visitors see.

## Settings

| Setting | What to put in it |
|---|---|
| **Enable protected media** | The master switch. Off means links are served untouched. |
| **A link stays valid for** | 30 minutes, 1 hour, 2 hours (recommended), 6 hours or 24 hours. |
| **Provider** | Amazon S3, Cloudflare R2, Backblaze B2, or Other S3-compatible. This only sets the default link style; the signing is identical everywhere. |
| **Bucket name** | Just the name, for example `my-course-videos`. |
| **Region** | For example `us-east-1`, or `eu-central-003` on Backblaze. Cloudflare R2 uses `auto`. |
| **Endpoint** | Leave blank for Amazon S3. Paste what your provider shows you; the scheme and any trailing slash are optional. |
| **Link style** | Leave on "choose for me" unless links come back rejected. |
| **Access key ID** and **Secret access key** | A read-only key for this one bucket. See below. |

### Endpoint by provider

| Provider | Endpoint | Region |
|---|---|---|
| Amazon S3 | leave blank | your bucket's region, for example `eu-west-1` |
| Cloudflare R2 | `<account-id>.r2.cloudflarestorage.com` | `auto` |
| Backblaze B2 | `s3.<region>.backblazeb2.com` | for example `eu-central-003` |
| Wasabi | `s3.<region>.wasabisys.com` | for example `eu-central-1` |
| MinIO | your own host, for example `files.example.com` | whatever you configured |

### Getting a read-only key

Give this plugin the least power that works. It never uploads, deletes or lists anything.

- **Amazon S3.** In IAM, create a user with programmatic access and a policy allowing only `s3:GetObject` on `arn:aws:s3:::your-bucket/*`. Take the access key ID and secret at the end of the wizard; the secret is shown once.
- **Cloudflare R2.** In R2, go to Manage API Tokens and create a token with **Object Read only** permission, scoped to the one bucket. Cloudflare gives you an S3-style access key ID and secret alongside the token.
- **Backblaze B2.** In App Keys, add a new application key, restrict it to the single bucket, and set access to **Read Only**. Copy `keyID` and `applicationKey` immediately; the key is shown once.
- **Wasabi and MinIO.** Create a user with a read-only policy on the bucket, exactly as for S3.

## Using it with EP Courses

There is nothing to configure. With both plugins active and this one enabled:

1. Edit a lesson and set **Video Type** to **MP4**.
2. Paste the bucket URL of the video file, exactly as you would have anyway.

The lesson page is still gated by enrolment as before. What changes is that the player now receives a link that expires rather than the plain bucket URL. YouTube and Vimeo lessons are untouched, and so is any MP4 hosted somewhere other than your configured bucket.

Seeking still works. A presigned URL supports the range requests browsers use to jump around inside a video, and a video that is already playing is not interrupted when its link expires.

## The `[ep-media]` shortcode

Put a protected file anywhere on your site.

```
[ep-media url="https://my-bucket.s3.eu-west-1.amazonaws.com/lesson-1.mp4"]
[ep-media key="handbook.pdf" type="link" label="Download the handbook"]
[ep-media key="episode-3.mp3" type="audio"]
[ep-media key="trailer.mp4" public="yes"]
```

| Attribute | Purpose |
|---|---|
| `url` | The full bucket URL of the file. |
| `key` | The object key on its own, for example `lessons/week-1.mp4`. Use either this or `url`. |
| `type` | `video` (the default), `audio`, or `link`. |
| `label` | The text of the link when `type="link"`. |
| `public` | `yes` serves the file to signed-out visitors, still behind an expiring link. |

By default the shortcode requires a signed-in visitor. That is the most it can safely assume on its own: it has no way of knowing which course, tier or product a given file belongs to. For anything stricter, gate the page with EP Membership, or use the plugin that owns that concept and let it ask for the link.

## For developers

Other plugins reach it through three methods.

```php
$store->configured();                        // bucket and both keys present
$store->owns($url);                          // does this URL point at the configured bucket
$store->signed_url($url_or_key, $seconds);   // the one you want
```

`signed_url()` takes a full bucket URL or a bare object key, and the seconds argument is optional. Anything it does not recognise comes back untouched, so you can pass every media URL you hold without checking it first.

It never throws. If signing fails for any reason it logs the problem and returns the original URL, which fails open. A lesson that plays unprotected is a smaller problem than a paying student staring at a dead player.

Find the instance the way every EP plugin finds a sibling, and guard the call:

```php
global $motor;
if (in_array('EP_Media_Storage', (array)($motor->plugins->active ?? array()))) {
    foreach (array('theme', 'admin') as $ctx) {
        if (empty($motor->$ctx->_plugins->active)) continue;
        foreach ($motor->$ctx->_plugins->active as $plugin) {
            if (!empty($plugin->_class) && $plugin->_class === 'EP_Media_Storage'
                && method_exists($plugin, 'signed_url'))
                $url = $plugin->signed_url($url);
        }
    }
}
```

## Admin actions

| Action | What it answers |
|---|---|
| `media_storage_status` | Is protected media configured and switched on, for which provider and bucket, with what link lifetime. |
| `sign_media_url` | Mint one expiring link for a file, optionally overriding the lifetime. Useful for testing, or for a one-off share. |

Both are admin-tier, so they are available to your AI assistant through the site's own API.

## Security notes

**Keep the bucket private.** Expiring links achieve nothing if the object is also readable by anyone with the plain URL. Protecting the link and leaving the bucket public is the most common way to get no protection at all.

**Use a read-only, single-bucket key.** PageMotor core cannot currently render a masked password field, so the secret is present in the source of the settings page. That is a page only your admins can open, but it means the blast radius of a leaked admin screenshot should be "somebody can read files they were already being shown", not "somebody can empty my storage".

**Prefer shorter lifetimes.** Two hours comfortably covers a sitting, and nothing is interrupted when a link expires mid-playback.

## Troubleshooting

### "The video does not play, and the link returns 403"

Almost always the signature. Work through these in order.

- **Region or endpoint wrong.** The signature includes both. A Backblaze bucket in `eu-central-003` signed as `us-east-1` produces a valid-looking link that is always rejected.
- **Link style.** Switch **Link style** from "choose for me" to the other option and try again. Some providers and some bucket names only accept one form.
- **The key is not allowed to read that object.** Test the same key with your provider's own tool.
- **Server clock.** Signature Version 4 is time-based. If your web server's clock has drifted by more than a few minutes, every link it mints is outside its own validity window. `timedatectl` on the server will tell you, and enabling NTP fixes it permanently.

### "The link returns 401, or says the request has expired"

The link is past its expiry, which is the plugin working. Reload the page to get a fresh one. If it happens within seconds of loading, suspect the server clock as above.

### "Links are not being signed at all, the plain URL still appears"

- **Enable protected media** is not ticked, or the bucket, access key ID or secret is blank. All three are required before anything is signed.
- The file is not in the configured bucket. The plugin only signs what it owns, on purpose, so a link to another host passes through untouched.
- For an EP Courses lesson, check **Video Type** is set to **MP4**. YouTube and Vimeo lessons are never signed.

### "Can I use my CDN or custom domain in front of the bucket?"

Not in this version. Links are signed against the bucket endpoint you configure. CloudFront signed URLs and R2 custom domains use a different signing scheme, which is a candidate for a later release.

### "Does this work for downloads and audio, not just video?"

Yes. Use `type="link"` for a download and `type="audio"` for a player. Anything in the bucket can be served this way.

## Changelog

### 0.1.0

Initial release: AWS Signature Version 4 presigned URLs for any S3-compatible store, configurable link lifetime, virtual-hosted and path-style buckets, the `[ep-media]` shortcode, automatic protection of EP Courses MP4 lessons, and the `media_storage_status` and `sign_media_url` admin actions.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger, a bug report, a feature request, or a "how do I..." that needs a real reply, open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
