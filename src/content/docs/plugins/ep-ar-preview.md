---
title: "EP AR Preview"
description: "Let a visitor hold up their phone and see a print hanging on their own wall, at true physical size, with no app to install. One shortcode, generated on the server, works on any host."
---

Somebody looking at a print online already knows what it looks like. What they cannot tell is how big it is. A 24 by 36 inch photograph is either the making of a room or far too much for it, and no thumbnail will settle that question.

EP AR Preview settles it. It adds a **See it on your wall** button to a page. A visitor taps it on their phone, points the camera at their own wall, and the framed print appears there at its real size. Nothing to install, no app, no account.

Published by [ElmsPark Studio](https://elmspark.com).

## What the visitor sees

On an iPhone or iPad, tapping the button opens the AR viewer built into the operating system. The print appears on the wall the camera is pointed at, correctly scaled, and stays put as they walk around the room. They can step back to judge it from the sofa.

On a desktop browser there is no camera to use, so the button is simply a link that does nothing useful. Pair it with your own room mock-ups for desktop visitors.

## Adding it to a page

One shortcode, placed wherever you want the button:

```
[ep-ar-preview image="/user-content/uploads/content/glacial-valley.jpg" width="36" height="24"]
```

Dimensions are in **inches**, because that is how prints are sold. The plugin converts to real-world metres for you.

### Arguments

| Argument | Required | What it does |
|---|---|---|
| `image` | Yes | The print image, as an uploaded file on your own site |
| `width` | Yes | Print width in inches |
| `height` | Yes | Print height in inches |
| `frame` | No | `dark`, `black`, `natural`, `white`, or `none` for an unframed print or canvas |
| `label` | No | Overrides the button text for this one print |

So an unframed canvas with its own wording:

```
[ep-ar-preview image="/user-content/uploads/content/canyon.jpg" width="24" height="16" frame="none" label="See this canvas on your wall"]
```

## Settings

Four settings, under the plugin's own panel in your admin.

- **Button text.** The default label on every button. A shortcode can override it.
- **Default frame.** Used when a shortcode does not name one.
- **Show the size on the button.** Appends the dimensions, so the button reads "See it on your wall · 36 × 24 in".
- **Maximum texture width.** The print image is re-encoded to at most this width so the model downloads quickly on mobile data. 2048 suits almost every case.

## Things worth knowing

**The image must live on your own site.** Point `image` at a file you have uploaded, not at an address on another service. The plugin reads the file to build the model, and it will refuse anything outside your uploads folder.

**Blank walls are the hard case for phone AR.** A plain painted wall gives the camera little to grip, which is unfortunate because that is exactly where pictures go. If placement hesitates, sweeping the camera slowly across the wall and a little of the floor gives it something to work with. Newer iPhones with a depth sensor are close to instant.

**Models are built once and reused.** The first visitor to view a given print at a given size waits a moment while the model is generated; everyone after that is served the cached copy. Changing the image regenerates it automatically.

**Android is not supported yet.** Android's AR viewer has no reliable way to be told that something belongs on a wall rather than the floor, so the button is offered to iPhone and iPad only for now.

## Requirements

- PageMotor 0.10.3 or newer
- PHP with the GD image extension, which almost every host has
- Your site served over HTTPS, which the AR viewer requires

No database tables are created, and nothing is sent to any external service. The model is built on your own server and served from it.

## Changelog

### 0.1.0

First release. Shortcode, four frame presets plus unframed, on-demand model generation with caching, and iOS AR support.
