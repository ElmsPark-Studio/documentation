---
title: "EP Gallery"
description: "Album-based image gallery for PageMotor with drag-and-drop upload, client-side compression, lightbox, EXIF display, slideshow, and responsive grid layout."
sidebar:
  order: 3
---

EP Gallery adds proper album-based image galleries to PageMotor. Drop your photos onto an album, the plugin compresses them client-side to keep your upload fast, generates thumbnails server-side, strips and preserves EXIF, and renders a responsive grid with a keyboard-accessible lightbox. Two optional add-ons extend it with photographer-grade EXIF display and focal-point framing.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

An album is a named collection of images. A single shortcode renders the album as a responsive grid on any page.

What you get:

- **Album management.** Create, rename, reorder, delete. Every album has a slug, a cover image, and a status.
- **Drag-and-drop upload** directly onto an expanded album panel. Click-to-browse still works if you prefer.
- **Client-side image compression** (on by default) so large camera JPEGs don't sit on your upload pipe for minutes.
- **Automatic thumbnails** generated server-side using PHP GD.
- **Responsive grid** with 2, 3, 4 or 5 columns and five spacing presets.
- **Keyboard-accessible lightbox** with arrow-key navigation, close-on-backdrop, swipe gestures on touch, and an optional slideshow timer.
- **EXIF extraction** per image, stored in the database, surfaced in the lightbox in one of three layouts (below the image, overlay, or side panel on wide screens).
- **Captions and alt text** editable per image for accessibility.
- **Lazy loading** on every image below the fold, eager on the first row for instant paint.
- **Extension points** used by the EP Gallery EXIF and EP Gallery Presentation add-ons for photographer-grade features.

## Requirements

- PageMotor **0.8b or later**
- EP Suite (bundled)
- PHP **GD extension** (standard on almost all hosting, used for thumbnails and dimension extraction)

## Installation

Standard PageMotor plugin install.

1. **Download.** Grab `ep-gallery.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest) or the link in your ElmsPark account.
2. **Sign in to your PageMotor admin** at `yourdomain.com/admin/`.
3. **Go to Plugins, then Manage Plugins.**
4. **Upload the zip.** PageMotor extracts it automatically.
5. **Activate in your Theme.** Enable EP Gallery in your active Theme's plugin configuration. Database tables are created on first load.

**How to verify:** after activation, go to **Plugins then Plugin Settings** and open **EP Gallery**. You should see sections for Albums, Display, and Usage. If those appear, you are installed and ready.

## Managing albums

From the EP Gallery settings page:

1. Type a title in **New album title** and click **Create Album**.
2. Each album row has a slug (shown under the title), a cover image thumbnail, a reorder handle, a **Rename** button, an **Expand** toggle, and a **Delete** button.
3. Expand an album to manage its images.

The slug is the value you pass to the `[gallery album=]` shortcode. Keep it short and lowercase, no spaces. The plugin generates one automatically from the title, but you can rename.

## Uploading images

Two ways, same pipeline.

### Drag and drop

From v1.3.8 onwards, the expanded album panel is a drop target. Drop a single image or a batch onto the panel. Non-image files are silently filtered out. Dropped images go through exactly the same compression, server-side thumbnail, EXIF extraction and cover-image assignment as the button path.

### Click to browse

Click **Upload Images** to open a multi-file picker. Select as many images as you want and click open. Progress shows in the status line beside the button.

### What happens on upload

For every image, in order:

1. **Client-side compression** (if enabled in settings): the browser resizes and re-encodes to keep each file under 1.5MB. This is on by default. Turn it off only if you pre-compress your images and need pixel-perfect originals preserved.
2. **Upload** to `user-content/uploads/gallery/<album-slug>/`.
3. **Thumbnail generation** at your configured thumbnail width using GD.
4. **Dimension extraction** for layout stability (width and height are stored with the image record so the grid reserves space before the image loads).
5. **EXIF extraction** into the image's `exif_data` column, stored as JSON.
6. **Cover image assignment** if this is the first image in the album.

The first image in the album becomes the cover automatically. Click any image thumbnail in the admin to change it.

### Editing, reordering, deleting

- **Reorder** by dragging image thumbnails in the admin grid. New order is saved as you drop.
- **Edit** an image to set its title, alt text and caption.
- **Delete** to remove the image and its stored file.
- **Set cover** on any image to make it the album cover.

## Shortcode

One shortcode, with attributes for every common customisation.

```text
[gallery album=my-album-slug]
[gallery album=portfolio columns=4 lightbox=true captions=true]
[gallery album=weddings gap=16 slideshow=3000 aspect=3-2 exif_layout=overlay]
```

### Attributes

| Attribute | Values | Default | Effect |
|---|---|---|---|
| `album` | album slug | **required** | Which album to render. Must match the slug shown in the admin. |
| `columns` | 2, 3, 4, 5 | from settings | Grid columns. Clamped to the 2–5 range. |
| `lightbox` | `true`, `false` | from settings | Click an image to open the lightbox viewer. |
| `captions` | `true`, `false` | from settings | Show captions under each image. |
| `gap` | 0, 4, 8, 16, 24 | from settings | Pixel gap between images. `0` is edge-to-edge. |
| `slideshow` | 0, 2000, 3000, 5000, 10000 | from settings | Milliseconds between auto-advance slides in the lightbox. `0` disables. |
| `title` | `true`, `false` | from settings | Show the album title as an `<h2>` above the grid. |
| `exif_layout` | `below`, `overlay`, `side` | `below` | Where the EXIF panel appears in the lightbox. See below. |
| `aspect` | `original`, `1-1`, `4-3`, `16-9`, `3-2` | `original` | Aspect ratio for the grid frame. Consumed by the **EP Gallery Presentation** add-on. Without Presentation installed, every image renders in its original aspect. |

Any invalid value for an enum attribute falls back to the default rather than failing. The shortcode never throws.

## Settings reference

Global defaults for every album on your site. Shortcode attributes always win over these settings.

| Setting | Values | Purpose |
|---|---|---|
| **Default Columns** | 2, 3, 4, 5 | Fallback column count when a shortcode doesn't specify one. |
| **Lightbox** | on / off | Whether the click-to-enlarge viewer is enabled by default. |
| **Captions** | on / off | Whether image captions render below thumbnails by default. |
| **Thumbnail Width** | 200, 300, 400 px | Width of the server-generated thumbnail. Higher values mean sharper thumbnails on high-DPI screens but larger files. |
| **Compress on Upload** | on / off | Whether the browser compresses images before sending to your server. Leave on unless you know you need originals. |
| **Show Album Title** | on / off | Whether to render the album title as an `<h2>` above the grid. |
| **Image Spacing** | None, Tight (4), Normal (8), Relaxed (16), Wide (24) | Default pixel gap between grid cells. |
| **Slideshow** | Off, 2s, 3s, 5s, 10s | Default auto-advance interval inside the lightbox. |

## Lightbox

Click any image (when the lightbox is enabled) to open a full-screen viewer.

Controls:

- **Arrow keys** left and right for previous and next.
- **Escape** to close.
- **Click the backdrop** to close.
- **Swipe left and right** on touch devices.
- **Tap or click the image** to toggle the EXIF panel (overlay layout only).

When `slideshow` is set to a non-zero value, the viewer advances automatically on that interval. Manual navigation cancels auto-advance until the lightbox is reopened.

## EXIF display

Every uploaded image has its EXIF JSON stored in the database. The lightbox optionally surfaces a curated selection of fields (camera, lens, exposure, aperture, ISO, focal length, date taken).

Three layouts, chosen per-gallery via the `exif_layout` shortcode attribute:

- **`below`** (default). EXIF panel renders as a flex layout underneath the image. Always visible when EXIF data exists. Best for large screens, awkward on narrow mobile.
- **`overlay`**. Semi-transparent strip anchored to the bottom of the image. Collapsed by default so the viewer sees the full image first; tap the image to reveal. Best for photography-focused galleries.
- **`side`**. Panel beside the image on screens wide enough to fit both. Stacks below on narrow viewports. Best for galleries where every photo has meaningful metadata.

EXIF rows are rendered as `<div>` elements, not tables, to avoid Safari's long-standing flex-on-`<tbody>` bugs.

### Enhanced EXIF (optional add-on)

The **EP Gallery EXIF** add-on extends the default extraction with richer metadata (lens identification, shooting mode, white balance, GPS coordinates if present, copyright fields). Install alongside EP Gallery and both plugins coordinate automatically. The default lightbox display takes the enhanced fields into account where available.

## Focal-point framing (optional add-on)

The **EP Gallery Presentation** add-on unlocks the `aspect` shortcode attribute: force every image in a grid to render at `1:1`, `4:3`, `16:9` or `3:2` while preserving a focal point you pick per-image. Without the add-on, `aspect=original` is the only meaningful option and every image renders at its native ratio.

## Compression explained

Why client-side compression matters: a modern mirrorless camera produces 20 to 40MB JPEGs per frame. Uploading 50 of those over a typical home connection takes minutes and often times out at the PHP side. EP Gallery resizes in the browser (down to around 2000px on the long edge, re-encoded as JPEG at ~85% quality) so each file is usually under 1.5MB when it hits your server. You still get a perfectly sharp 2000px image displayed in the lightbox and generous thumbnails at your configured width.

When to turn compression off:

- You pre-compress your images in Lightroom, Capture One, Photoshop, etc., and want to keep exact control of quality.
- You need to preserve EXIF ICC colour profiles byte-for-byte (some colour-managed workflows).
- You are uploading PNG or SVG and don't want JPEG re-encoding.

For everyone else, leave it on.

## Extension points

For plugin authors. EP Gallery defines a small set of `class_exists()`-gated hooks that the Presentation and EXIF add-ons use. All hooks are fully backward-compatible: EP Gallery behaves identically when no add-on is installed.

The renderer lets companion plugins:

- Override grid and lightbox image URLs per image (used by Presentation for focal-cropped versions).
- Emit a `data-focal="x,y"` attribute on each grid cell for CSS `object-position` framing.
- Enhance EXIF extraction before it is saved (used by EP Gallery EXIF).
- Clean up preserved-original files on image delete.

Contact [ElmsPark Studio](https://elmspark.com) if you are building an add-on and want the exact hook signatures.

## Troubleshooting

### "The upload progress stalls or fails partway through"

Usually one of three things:

- Your PHP `post_max_size` or `upload_max_filesize` is too low. For batch uploads with compression on, 20MB is a safe minimum. Without compression, go higher.
- Your PHP `max_execution_time` is too short. Thumbnail generation with GD can take seconds per image on large originals. 60 seconds is a safe minimum.
- Your server has limited memory (shared hosting under 128MB). GD needs roughly 4× the pixel dimensions in RAM. Enable compression so the server sees smaller files, or upgrade to hosting with more headroom.

### "My images look pixellated in the grid"

The grid shows thumbnails, not the original. Increase **Thumbnail Width** in settings from 200px to 400px. Re-uploading existing images will regenerate the thumbnails; existing thumbnails will not update retroactively.

### "EXIF data is not appearing in the lightbox"

Check three things:

1. Were EXIF fields present in the original file? Compressed-from-phone images often strip EXIF before they reach you.
2. Client-side compression on EP Gallery preserves EXIF by default, but some browsers strip it on canvas re-encode. If EXIF is critical, turn compression off for that upload.
3. The lightbox shows EXIF only if there is extracted data. Open the image in the admin and confirm the `exif_data` column has content; if it is empty, the source file had no EXIF.

### "I want to reorder albums but there is no drag handle"

Click and hold the album row's left edge (the small handle icon). Drag up or down, drop in the new position. The order saves as you drop.

### "The cover image is wrong after I deleted the first photo"

EP Gallery does not automatically reassign the cover when you delete its source image. Open another image in the album and click **Set as cover**.

### "The drop zone highlights but the upload does not start"

The panel must be expanded for drops to register. If you drop outside the expanded `.ep-gallery-album-images` area, the browser will try to open the file as a URL in a new tab. Expand the album first, then drop.

### "I dropped a .pdf or a .mov onto the panel and nothing happened"

That's by design. Only files with an `image/*` MIME type are accepted. Other files are silently filtered rather than rejected with an error.

## Feedback and corrections

Found a bug or a missing detail in this guide? Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues). Corrections land quickly.
