---
title: "EP 3D Viewer"
description: "Interactive 3D models on a PageMotor page, with numbered labels pinned to points on the surface. Everything served from your own domain: no account, no key, no third-party request."
---

EP 3D Viewer puts a real, rotatable 3D model on a page, with numbered labels pinned to points on its surface. Build a library of models in Admin, then place one anywhere with a shortcode.

Everything is served from your own site: the viewer, the compressed-geometry decoders, the models themselves. A page carrying a 3D reference makes no third-party request at all.

Published by [ElmsPark Studio](https://elmspark.com).

## Why this exists

The hosted 3D reference services are genuinely good at what they do, and for medically accurate anatomy their content is not replicable. But the delivery model is always the same: a paid plan, a domain-locked developer key, and an iframe pointing at someone else's server on every page view.

For a physiotherapist explaining a knee, a manufacturer showing a part, or a gallery showing a sculpture, that is a subscription and a data transfer bought to solve a problem the browser can already solve. A `.glb` file plus a WebGL viewer does the same visible job from your own document root. This plugin is the wiring.

## Overview

Features:

- **Model library.** Define each model once in Admin — file, alt text, poster, caption, labels — then place it by name. Edit the row and every page using it updates.
- **Labels that stay put.** Numbered hotspots anchored to a point and surface normal on the mesh. They reveal a description on hover, keyboard focus or tap, and hide automatically when they rotate to the back of the model.
- **A picker for those labels.** A hotspot is six numbers in model space, and nobody can guess them. Load a model in Admin, click points on it, and the exact lines come out ready to paste.
- **Nothing downloads until asked.** Models default to loading on click, behind a poster image, because a 30 MB mesh on mobile data should be a choice.
- **A sample model included**, so the plugin does something the moment it is activated.
- **No third-party requests.** See below; this is the part that is easy to get wrong.

## The part worth reading

The viewer is built on Google's `<model-viewer>`, which is Apache-2.0 licensed and bundled with the plugin rather than loaded from a CDN. That much is straightforward.

Less straightforward: out of the box, `<model-viewer>` fetches its Draco geometry decoder and KTX2 texture transcoder from `www.gstatic.com` the first time it meets a **compressed** model. An uncompressed test model never triggers it, so the request survives casual testing and appears in production the day someone uploads a Draco-exported file.

Both decoders are bundled here and the loader is repointed at them. You can check the claim yourself: open a page with a viewer, watch the browser's network tab, and confirm every request is same-origin. The bundled sample model is Draco-compressed precisely so that this path is exercised on first run.

**One deliberate exception,** off by default. If you enable **view in your room**, tapping that button hands the model to the phone's own AR app, which on Android is Google Scene Viewer. That is a third party, it only happens for visitors who tap, and the setting stays off until you turn it on.

## Requirements

- **PageMotor 0.10.3b or later**
- **EP Suite base class**
- A browser with WebGL 2

No account, key, subscription or external service.

## Installation

1. `ep-3d-viewer.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Drop `[ep-3d-viewer model="sample"]` on any page to see it working immediately, using the model bundled with the plugin.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[ep-3d-viewer model="sample"]` | The bundled hex bolt. Works with no configuration. |
| `[ep-3d-viewer model="knee"]` | The bundled knee joint, for the clinical case. Bone only, three labels. |
| `[ep-3d-viewer model="heart"]` | A model from your library, by its reference name. |
| `[ep-3d-viewer src="/user-content/uploads/content/valve.glb" alt="A globe valve"]` | A one-off model, without a library entry. |

Attributes override the library row: `model`, `src`, `alt`, `poster`, `caption`, `height`, `reveal` (`interaction` or `auto`), `auto-rotate`, `ar`.

For a set of labels that should apply on one page only, without changing the shared library row, use the enclosing form. One label per line:

```
[ep-3d-viewer model="heart"]
position="0.01m 0.32m 0.10m" normal="0m 1m 0m" label="1" text="Aorta"
position="-0.04m 0.28m 0.09m" normal="0m 1m 0m" label="2" text="Left ventricle"
[/ep-3d-viewer]
```

Lines beginning `#` are ignored, and a line without a valid `position` is skipped rather than placed at the origin where it would sit inside the model looking like a fault.

## Settings

**Admin → Plugins → EP 3D Viewer.**

| Group | What it holds |
|---|---|
| Model Library | One row per model: reference name, file, alt text, poster, caption, labels |
| Display Defaults | Height, when to download, auto-rotate, AR, label colour |
| Label Picker | Load a model, click to place labels, copy the lines |

The status cards at the top report how many models and labels you have, whether every model file was actually found on disk, and confirm that no external requests are being made.

## Placing labels

Open **Label Picker**, load a model, and click points on its surface. Each click writes a line like this:

```
position="0.364m 1.449m 0.304m" normal="0.060m 0.558m 0.828m" label="1" text="Describe this point"
```

Edit the `label` (what shows in the dot) and the `text` (what shows when a visitor hovers, focuses or taps it), then paste the block into that model's **Labels** box.

Two things worth knowing:

- **Anchor labels on surfaces that face the viewer's opening camera position.** A label on the far side loads correctly and is then hidden as back-facing, which looks like it failed.
- **A click that misses the model is reported**, not silently ignored. If the picker says the click missed, aim at the surface rather than the background.

## Preparing a model

Any `.glb` file works. Two things are worth doing before upload:

- **Compress it.** `gltf-transform optimize in.glb out.glb --compress draco` typically cuts a mesh by 70 to 90 per cent. The bundled sample goes from 300 KB to 7 KB. Draco and KTX2 are both decoded locally by this plugin.
- **Scale it in metres.** The viewer treats one unit as one metre, which matters for AR and for label positions reading sensibly.

## Limitations

Both of these are deliberate, and both exist because supporting them would mean an external fetch:

- **Meshopt compression** has no decoder bundled, so meshopt models will not load. Use Draco.
- **Lottie textures**, a rare glTF extension, would pull a loader from jsDelivr. The location is repointed at the plugin's own directory, so such a model fails to decode rather than reaching out.

## Changelog

### 0.1.3

Adds a knee joint sample for the medical case, reachable with `[ep-3d-viewer model="knee"]`. Femur, patella, tibia and fibula from one CT scan of a single leg, cropped to the joint, 77 KB, with three labels. It is CC0: sourced from NIH 3D entries 3DPX-000168/169/170, segmented by SquareL (Luc Labey, KU Leuven), and credited in the plugin's `NOTICE.md` as courtesy rather than obligation.

The model is bone only, with no menisci, ligaments or cartilage, and the caption says so. There is deliberately no fibula label: the source delivers the tibia and fibula as a single fused body with no separation, so such a label could only be a guess at which lump it sat on.

Bundled model URLs are now version-stamped, so an updated model is no longer masked by a browser cache. Customer paths are left untouched.

### 0.1.2

Fixes a viewer that rendered as an empty box on a fresh install. `reveal="interaction"` holds the model behind a poster until the visitor asks for it, which is right for a large mesh on mobile data and is the default. But with no poster image set there was nothing to look at and nothing to click, so the model downloaded and was simply never shown — and a brand-new install lands in exactly that state, because interaction is the default and a fresh library has no posters.

Viewers set to reveal on interaction now render an explicit **View in 3D** button, and labels stay hidden until the model is actually on screen rather than floating over an empty box.

### 0.1.1

Adds a bundled sample model, so the plugin does something the moment it is activated rather than presenting an empty library and no obvious next step. It is an M10 hex bolt at true size, generated for this plugin rather than taken from a sample-model library, and Draco-compressed to 7 KB from 300 KB. That compression is not only about size: the sample exercises the bundled Draco decoder on first run, so the one path most likely to leak to a third party is the first thing every install proves.

The Label Picker now pre-fills with that sample and loads it eagerly, so its **Load model** button does something on a site that has uploaded nothing yet. The settings page gained a documentation link, and this page.

### 0.1.0

First release. Model library, `[ep-3d-viewer]` shortcode in self-closing and enclosing forms, surface labels with a click-to-place picker, deferred loading behind a poster, and a bundled runtime with the Draco and KTX2 decoders repointed at local copies so no page view reaches `www.gstatic.com`.
