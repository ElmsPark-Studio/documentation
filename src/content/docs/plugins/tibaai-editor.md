---
title: "TIB AI Page Editor"
description: "A code editor for the HTML documents Discovery builds. Lists every editable document, edits with a live preview, saves through the same core path the builder uses, and keeps a save history so no edit is ever lost."
---

TIB AI Page Editor is the missing HTML body editor for a Discovery-built site. PageMotor's own Edit HTML screen is a read-only preview plus a download-and-re-upload loop; this plugin replaces that with a real editor at `/site-editor/`, with a live preview and a per-document save history.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Every document in one list.** Only `html` and `home-html` rows are reachable, so nothing else on the site can be read or written through this surface.
- **Live preview.** Debounced, in a sandboxed iframe with scripts off.
- **Saves through core.** Edits go through the same `api_save()` path the Discovery builder uses, so core validation applies and the managed head block stays idempotent.
- **Stale-save guard.** The editor sends a hash of the document it loaded. If the stored document has changed since (another tab, an agent, a rebuild), the save is refused rather than clobbering that edit.
- **Save history.** Per document, with a load-any-earlier-version action. History is strictly best-effort: if the history table is unavailable, the save still goes through.
- **Page details panel.** Page title, an optional custom title tag, the search description and the social share image, for the currently open document.
- **Colours panel.** The site's palette, editable in place.
- **Self-test.** A Check button runs a full diagnostic (reachability, session, exact bytes received, hash agreement, history writability, PHP version, post size) and prints a report you can paste into a support message.

## Requirements

- **PageMotor 0.10 or later**
- An administrator account. The editor is admin-only and has no public surface.

## Installation

1. `tibaai-editor.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Activation seeds the `/site-editor/` page. Visit it as an admin and the editor is there. The page is set to noindex, so it stays out of search engines and your sitemap.

## Changelog

### 0.3.5

- **Fixes the editor opening with no toolbar on some sites.** The editor covers the whole screen, but a site whose own header claimed a higher stacking order was painted on top of it, so the buttons were there and simply hidden. This was never a fault in the site: the value that header used is an entirely ordinary one. The editor now ranks above it and also lifts itself clear of the theme's own layout, because ranking alone is not enough when a theme wraps the page in certain ways.
- **New: the editor's own features are now reachable over the API and MCP.** Listing documents, opening one, saving it, reading the save history, the palette and the page details can all be driven by an assistant. The documents themselves were always reachable through PageMotor's own content actions; what was locked to the browser was everything this plugin adds on top, the save history most of all.
- Uploading a social share image is deliberately not included, because it needs a real file upload.

### 0.3.4

- **The Download button is back.** The 0.3.0 redesign dropped it without meaning to. It was not a deliberate removal: it simply did not survive the new toolbar. It behaves exactly as it did before and now sits next to Open live.

### 0.3.1

- **Fixes the page list losing its highlight after a save.** The list refreshes after every save so it can show when each page was last saved, and rebuilding it cleared the marker showing which page you had open.

### 0.3.0

- **A full design pass on the editor.** The chrome now matches the owner dashboard, and the code sits in a dark well that is the dashboard's own darkest green. The editor claims the whole screen, which makes the toolbar a permanent fixture rather than something that can scroll away.
- **A better answer when two people save the same page.** Instead of a bare recovery link, you get a calm banner with three choices: see exactly what changed line by line, keep yours, or take theirs. Whichever you choose, both versions survive. Nothing is thrown away by design.
- **Your unsaved text is protected by the browser.** While you have unsaved changes they are kept locally, so closing the tab by accident no longer costs you the edit. Reopening offers to restore or discard it. Nothing is ever saved to the server on your behalf: publishing stays a deliberate act.
- **Page details, Colours and History are now drawers** that slide over the preview instead of pushing the page down, one at a time, closed with Escape. History is a proper list with Open, Compare and Restore on each version rather than a dropdown.
- **Switching pages with unsaved work no longer risks losing it.** You are asked inline whether to save and switch, switch anyway, or stay. Switching anyway keeps your text so you can put it back.
- Cards and the page list now show when each document was last saved, and the history shows who saved each version, so you can tell your own edits from another session's. Older history entries that predate this simply show the time and size.
- The syntax-highlighting layer was deliberately held back for a later release. Everything proven in earlier versions is kept underneath unchanged.

### 0.2.8

- **Fixes the stale-save recovery throwing away your edit.** When a save was refused because someone else had changed the page, the offered "load the latest version" link replaced your unsaved text with the server copy and discarded what you had written, on the very path whose own instruction told you to redo your edit. Your text is now banked first, so after the latest version loads you can put your edit straight back and save it.

### 0.2.7

- Merge release: the admin-only script handling from one build and the sticky toolbar from another, brought together.

### 0.2.6

The editor's own admin JavaScript was being written into the source of themed pages, where a logged-out visitor could read it. It is now sent only to a logged-in administrator. Nothing was exposed and nothing could be done with it: every editor control is checked for admin rights on the server and refuses anonymous calls, and the editor page already showed logged-out visitors a login prompt and no data. Updating removes the code from public view.

### 0.2.5

`[svg icon="…"]` shortcodes now work in the editor: because Discovery pages are standalone HTML served verbatim, core shortcodes never run on them, so the icon is expanded into real inline SVG at save time and the stored document is self-contained. The seeded `/site-editor/` page also self-heals to noindex, which drops it from the XML sitemap; a live site was otherwise advertising its editor login page to search engines.

### 0.2.4

Update channel address corrected. The plugin header pointed one level too deep, so every update check asked for the wrong path. It worked only because of a server-side quirk, and one configuration change would have stopped this plugin seeing updates silently.

### 0.2.3

Both panels now have a visible Close button, opening one closes the other, Escape closes whichever is open, and the panel buttons read correctly as toggles to assistive technology.

### 0.2.2

New **Page details** panel: page title, custom title tag, search description and social share image for the open document, saved as content options with no document body submitted, so every byte of your page survives untouched and the address can never drift. Social images upload to the same folder core's own share settings use. Also fixes a core restriction that stopped any user whose username contains a hyphen from saving their own profile, including changing their password.

### 0.1.3

Saving now works on stricter hosts. Two causes, both ours: the editor depended on browser confirmation dialogs, so a browser set to suppress them made Cancel and document switching do nothing; and the whole document was posted as a plain field, which security filters on some Apache stacks reject outright as suspicious. Documents now travel encoded, and any non-JSON reply reports its real status instead of a generic failure. Adds the Check self-test.

### 0.1.2

History can no longer block a save: it is best-effort end to end, with a database collation fallback, and a save proceeds even when history is unavailable. A refused stale save now explains itself and offers a one-click "Load the latest version".

### 0.1.1

Cancel. Restores the document to exactly what was last loaded or saved, clears the unsaved flag and redraws the preview. Escape does the same.

### 0.1.0

First release. Document list, code editor, live preview, save with Cmd/Ctrl+S, download, load-from-file, per-document history, and the stale-save guard.
