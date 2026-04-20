---
title: "EP Email File Uploads"
description: "Adds drag-and-drop file upload fields to EP Email contact forms. Multi-file, MIME filtering, size caps, admin-side download of received files."
sidebar:
  order: 27
---

EP Email File Uploads adds a file upload field type to [EP Email](/plugins/ep-email/)'s contact forms. Visitors drop files onto the form; files are stored on your server; you download them from the submission in the admin.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Common use cases:

- **Job applications** — CV and cover letter.
- **Quote requests** — photos of the job.
- **Support tickets** — screenshots.
- **Creative briefs** — reference images and documents.

Features:

- **Drag-and-drop** zone plus click-to-browse.
- **Multi-file** upload support (configurable cap per field).
- **MIME filtering** per field — accept images, PDFs, documents, or anything.
- **Size caps** per file and per submission.
- **Server-side filtering** blocks executable types regardless of client claims.
- **Admin download links** in EP Email's submission inbox for every uploaded file.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Email** (required)
- **EP Suite base class**

## Installation

1. Install **EP Email** first.
2. Download `ep-email-file-uploads.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. The `file_upload` field type is now available in EP Email form definitions.

## Adding a file upload field

In your EP Email form JSON:

```json
{
  "type": "file_upload",
  "id": "attachments",
  "label": "Attach files",
  "required": false,
  "accept": "image/*,application/pdf",
  "ext": "jpg,jpeg,png,pdf",
  "max_files": 3,
  "max_size_mb": 10,
  "prompt": "Drop your files here or click to upload"
}
```

Field options:

| Option | Purpose |
|---|---|
| `accept` | MIME filter for the browser file picker. `image/*,application/pdf` shows only images and PDFs in the OS dialog. |
| `ext` | Server-side extension allowlist. Enforced regardless of client-side claims. |
| `max_files` | Maximum files per submission. Default 1. |
| `max_size_mb` | Maximum size per file in megabytes. |
| `prompt` | Custom text in the drop zone. |

Server-executable extensions (php, cgi, sh, etc.) are **always blocked** regardless of your allowlist. This is a hard safety rule that can't be turned off.

## Where uploaded files live

Files are saved under `user-content/uploads/ep-email/<form-id>/<submission-id>/`. Each submission gets its own folder keyed by the submission ID, so downloads are unambiguous.

The admin-side submission view in EP Email shows every uploaded file with:

- Filename.
- Size.
- Download link (admin-authenticated).
- Delete button (removes the file from disk).

## Security

- **CSRF protection** on the upload endpoint.
- **Session-bound uploads**: files are attached to a draft submission keyed to the visitor's session. Without an active form session, uploads are rejected.
- **Extension allowlist** at the server, independent of client claims.
- **Executable extensions blocked** regardless of allowlist.
- **MIME type verification** from actual file content, not just the claimed content-type.
- **Size caps** enforced server-side.

## Configuration for large files

If you need to accept large files (>10MB), check:

- Your PHP `upload_max_filesize` and `post_max_size` in `php.ini`. Set to at least your `max_size_mb` setting plus headroom.
- Your `max_execution_time` is long enough to receive the upload. 60 seconds is a reasonable minimum.
- Your web server upload limits (nginx `client_max_body_size`, Apache `LimitRequestBody`).

## Troubleshooting

### "The drop zone doesn't highlight when I drag over it"

JS isn't loaded. Check browser console. Clear any caching plugin if you have one.

### "Uploads fail with 'file too large' at 2MB even though I set max_size_mb to 10"

Server-level limit is kicking in before the plugin's check. Raise PHP `upload_max_filesize` and `post_max_size`, and web-server limits (nginx `client_max_body_size`).

### "Rejected extensions I thought I'd allowed"

The hardcoded blocklist of executable extensions (php, cgi, etc.) overrides your allowlist. This cannot be disabled.

### "Uploaded files aren't appearing in the submission"

Check the upload completed — the drop zone shows a progress bar. If the browser showed an error, the file never reached the server. Also check the `user-content/uploads/ep-email/` directory has write permission for the PHP user (`www-data` typically).

### "I want to clean up old uploaded files"

No auto-cleanup yet. Delete the `user-content/uploads/ep-email/<form-id>/<submission-id>/` folder when the submission is closed. Feature request for auto-purge is in the review queue.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
