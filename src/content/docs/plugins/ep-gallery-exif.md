---
title: "EP Gallery EXIF"
description: Enhanced EXIF extraction and display for EP Gallery. Lens ID, shooting mode, white balance, GPS, copyright fields, and camera-specific metadata.
sidebar:
  order: 31
---

EP Gallery EXIF extends [EP Gallery](/plugins/ep-gallery/)'s built-in EXIF support with richer metadata extraction and display. Base EP Gallery gets camera body, exposure, aperture, ISO, and focal length. This add-on adds lens identification, shooting mode, white balance, GPS coordinates (if present), copyright fields, and camera-specific details.

Published by [ElmsPark Studio](https://elmspark.com).

## What gets added

On top of EP Gallery's default EXIF:

- **Lens identification** — lens make, model, focal length range, aperture range.
- **Shooting mode** — Manual, Aperture priority, Shutter priority, etc.
- **White balance** — Auto, daylight, cloudy, tungsten, custom K temperature.
- **Metering mode** — spot, centre-weighted, matrix.
- **Flash** — fired, didn't fire, compensation.
- **Exposure bias.**
- **GPS coordinates** and altitude (if the camera recorded them).
- **Copyright** and **Artist** fields.
- **Image description** and **User comment**.
- **Camera-specific notes** — MakerNote fields for Canon, Nikon, Sony, Fujifilm, and other major brands.

## Requirements

- **PageMotor 0.7 or later**
- **EP Gallery** (required; this is an extension)
- **EP Suite base class**
- **PHP exif extension** installed on your server (usually standard)

## Installation

1. Install **EP Gallery** first.
2. Download `ep-gallery-exif.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.

From this point on, every new image uploaded to EP Gallery gets enhanced EXIF extraction. Existing images don't automatically reprocess — see below.

## Re-extracting EXIF on existing images

Use the admin dashboard's **Re-extract EXIF** button on any album or any specific image. The plugin re-reads the file and updates the stored EXIF JSON with the richer data.

Re-extraction is idempotent and safe to run multiple times.

## What the lightbox shows

With EP Gallery EXIF installed, the lightbox EXIF panel includes sections for:

- **Camera** (body, firmware).
- **Lens** (make, model, focal length, aperture).
- **Exposure** (mode, shutter, aperture, ISO, compensation).
- **Flash and metering**.
- **Location** (GPS coordinates with a link to Google Maps if recorded).
- **Copyright** and authorship.

The `exif_layout` attribute on the `[gallery]` shortcode still controls where the panel appears (below, overlay, or side) — the add-on only adds what the panel can show.

## Privacy note on GPS

GPS coordinates identify exactly where a photo was taken. If you're showing wedding photos from private homes, personal travel, or anywhere sensitive, strip GPS before uploading. Most camera phones embed GPS by default.

EP Gallery EXIF displays whatever is in the file. It does not strip GPS unless you configure it to:

- In settings, enable **Strip GPS on display** to hide GPS even if present in the EXIF data.
- For bulk stripping at upload time, use a desktop tool like ExifTool before upload.

## Troubleshooting

### "Enhanced EXIF isn't showing despite installing the add-on"

Re-extract EXIF on the image from the admin. Existing images carry only the base EP Gallery EXIF until re-processed.

### "GPS coordinates are wrong"

The coordinates are exactly what the camera recorded. If they're wrong, the camera's GPS was drifting (indoors, urban canyon, tunnel). Nothing this plugin can fix.

### "Some images show more EXIF than others"

Older cameras, phone cameras, and processed files (from Lightroom, Photoshop) often write different EXIF fields. The plugin shows what's present and hides what isn't. Partial EXIF is normal.

### "The lens identification is wrong or missing"

Lens identification depends on the lens ID code being in the EXIF. Some third-party lenses don't write IDs or write ambiguous ones. Manual correction isn't yet supported — feature request in the review queue.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
