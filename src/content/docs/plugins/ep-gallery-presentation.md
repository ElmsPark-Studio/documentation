---
title: "EP Gallery Presentation"
description: Master crop, gallery frame aspect ratios, focal point picker, and per-image display settings for EP Gallery. Photographer-grade presentation controls.
sidebar:
  order: 32
---

EP Gallery Presentation adds photographer-grade presentation controls to [EP Gallery](/plugins/ep-gallery/). Master crop with revert, aspect-ratio frame options on the grid, focal-point picker so cropped frames keep the important part of the image, and per-image display settings.

Published by [ElmsPark Studio](https://elmspark.com).

## What it adds

### Master crop with revert

Set a custom crop on any image that applies everywhere it's displayed (grid and lightbox). Crop is destructive to the displayed image but non-destructive to the source — the original file is preserved. **Revert** at any time returns to the original.

### Gallery frame aspect ratios

Without this add-on, EP Gallery renders every image at its native aspect ratio, giving a variable-height grid. With it, the `aspect` shortcode attribute on `[gallery]` becomes functional:

- `1-1` — perfect squares.
- `4-3` — classic photography.
- `16-9` — widescreen.
- `3-2` — 35mm classic.
- `original` — no frame, native aspect.

When a frame is set, every grid cell is that aspect. Images are cropped to fit, centred on their focal point.

### Focal point picker

For any image, click to set a focal point (x,y coordinate from 0 to 100 on each axis). When the grid frame crops the image, the crop is positioned so the focal point stays visible.

Example: a portrait photo's subject is in the top-third. Set focal point to (50, 25) and a 16:9 frame will crop to keep the subject visible even though the top and bottom of the portrait get chopped.

### Per-image display settings

Any image can override:

- **Caption display** — on/off for this image.
- **Fullscreen-in-lightbox** — force the lightbox to open this one full-window.
- **Alt text override** — separate from title, specifically for accessibility.

## Requirements

- **PageMotor 0.7 or later**
- **EP Gallery** (required; this is an extension)
- **EP Suite base class**
- **PHP GD** extension (for server-side crop)

## Installation

1. Install **EP Gallery** first.
2. Download `ep-gallery-presentation.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.

Once installed, new options appear in every image's admin edit panel.

## Using the focal point picker

1. In the admin, open any image's edit panel.
2. Scroll to **Focal point**.
3. Click on the image preview to set the point. A dot marks the spot.
4. Save.

The focal point is stored as `data-focal="x,y"` on the grid cell. EP Gallery's renderer uses it for `object-position` CSS framing.

## Using the master crop

1. Open any image's edit panel.
2. Click **Crop**.
3. Drag the crop rectangle to your preferred framing.
4. Save.

The displayed version is re-cropped on the server. Click **Revert to original** at any time to restore.

## Aspect-ratio frame examples

```text
[gallery album=portfolio aspect=1-1]
[gallery album=interviews aspect=16-9]
[gallery album=classic-film aspect=3-2]
```

Combine with other attributes freely:

```text
[gallery album=products aspect=1-1 columns=4 gap=0]
```

Four-column grid of perfect squares with no gap — good for product catalogues.

## Coordination with EP Gallery core

Presentation hooks into EP Gallery's renderer via the extension points documented in EP Gallery. Specifically:

- Overrides grid and lightbox image URLs to point at the master-cropped version when one exists.
- Emits `data-focal="x,y"` on each grid cell.
- Cleans up preserved-original files when an image is deleted.

All backward-compatible: EP Gallery works without Presentation installed.

## Troubleshooting

### "Aspect-ratio frame attribute has no effect"

Confirm EP Gallery Presentation is installed and activated. Without it, `aspect` on the shortcode is inert.

### "Focal point doesn't seem to keep the subject in frame"

Double-check the focal point is where you think it is. Re-open the image edit panel and look at the marker. Focal point uses 0-100 on each axis; (50, 50) is dead centre.

### "Master crop revert doesn't work"

The original file needs to be preserved. Check the `preserved_originals/` directory in your uploads exists and is writable. If it's missing, the plugin can't revert.

### "Cropping a large image fails with a memory error"

GD needs roughly 4x the pixel dimensions in RAM. For a 6000x4000 photo that's about 100MB. Raise PHP `memory_limit` to 256M or higher.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
