---
title: "EP Email"
description: "Reliable SMTP delivery, JSON-defined contact forms, delivery logging, and a developer extension API for PageMotor."
sidebar:
  order: 1
---

EP Email routes your PageMotor site's outgoing mail through a proper SMTP server, provides JSON-defined contact forms with conditional logic and file uploads, logs every message, and exposes an extension API for building premium add-ons.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

By default, PageMotor sends email through your server's built-in `mail()` function. That works, but messages are frequently blocked, delayed, or marked as spam, because a raw PHP server is not a trusted sender to the big mail providers.

EP Email fixes this by routing outgoing email through a proper SMTP server, the same way Gmail, Outlook and every professional email provider delivers mail.

What you get:

- **SMTP delivery.** Route all outgoing mail through your SMTP provider. Supports SSL/TLS, authentication and custom ports.
- **Contact forms.** Define forms in JSON, render with a shortcode. Conditional logic, custom field types and validation built in.
- **Email logging.** Every email is logged with recipient, subject, status and timestamp.
- **Email queue.** Failed sends can be queued for automatic retry on subsequent page loads.
- **Extension API.** Build add-ons that register custom field types, hook into submissions, add settings, and extend the frontend.

## Installation

EP Email installs like any PageMotor plugin. Under a minute end to end.

1. **Download.** Grab `ep-email.zip` from your ElmsPark account or the link provided with your purchase.
2. **Sign in to your PageMotor admin** at `yourdomain.com/admin/`.
3. **Go to Plugins, then Manage Plugins.**
4. **Upload the zip.** Use the plugin upload interface to upload `ep-email.zip`. PageMotor extracts it to the correct location automatically.
5. **Activate in your Theme.** Enable EP Email in your active Theme's plugin configuration. Database tables are created on first load.

**How to verify:** after activation, go to **Plugins then Plugin Settings**. You should see **EP Email Settings** with SMTP configuration, contact form settings, and the delivery log. If it appears, you are installed and ready to configure SMTP.

## SMTP Configuration

SMTP is the industry standard for sending email reliably. EP Email connects to your SMTP provider so messages actually reach inboxes.

### Configure it

1. Open **Admin then Plugins then EP Email** (Settings).
2. Under **SMTP Settings**, enter the host, port, encryption, username and password for your mail provider.
3. Click **Test Connection** to verify credentials without sending an email.
4. Click **Send Test Email** to confirm end-to-end delivery to a real inbox.

### SMTP Settings Reference

| Setting | Description |
|---|---|
| SMTP Host | Mail server hostname, for example `smtp.gmail.com` or `smtp.office365.com` |
| SMTP Port | Usually **587** (TLS) or **465** (SSL) |
| Encryption | TLS (recommended), SSL, or None |
| Username | SMTP authentication username |
| Password | SMTP authentication password |
| From Name | Sender name for outgoing emails |
| From Email | Sender email address |

**Gmail users:** you will need an App Password. Regular passwords no longer work with SMTP. Go to your Google Account, then Security, then 2-Step Verification, then App Passwords.

**VPS users:** most providers block outbound port 25, so direct server-to-server SMTP is not an option anyway. A dedicated SMTP provider like SendGrid, Mailgun or Postmark is the right answer.

## Contact Forms

EP Email includes a contact form engine. Define forms in JSON, render them anywhere with a shortcode. Conditional logic, custom field types and validation are built in.

### Adding a form

1. Go to **EP Email Settings then Contact Forms** and enter your form definition in the **Forms JSON** field.
2. Place `[ep-email name="form-name"]` on any page to render it.

### JSON structure

Each form is a named object with a recipient, subject, success message, button text, and an array of fields.

```json
{
    "contact": {
        "recipient": "info@example.com",
        "subject": "Contact from {name}",
        "success": "Thanks! We'll reply within 24 hours.",
        "button": "Send Message",
        "fields": [
            {"type": "text", "name": "name", "label": "Name", "required": true},
            {"type": "email", "name": "email", "label": "Email", "required": true},
            {"type": "textarea", "name": "message", "label": "Message", "rows": 5, "required": true}
        ]
    }
}
```

Render it with:

```html
[ep-email name="contact"]
```

### Form properties

| Property | Description |
|---|---|
| recipient | Email address that receives form submissions (required) |
| subject | Email subject line. Use `{field_name}` for placeholder substitution. |
| success | Message shown after successful submission |
| button | Submit button text. Default: "Send Message" |
| fields | Array of field definitions |
| messages | Custom validation and UI messages (optional) |

### Field types

| Type | Description |
|---|---|
| text | Single-line text input |
| email | Email address with validation |
| textarea | Multi-line text area |
| select | Dropdown menu |
| checkbox | Single checkbox or checkbox group |
| radio | Radio button group |
| hidden | Hidden field (not visible to user) |
| file | File upload (requires the File Uploads extension) |

### Field properties

| Property | Type | Description |
|---|---|---|
| type | string | Field type (required) |
| name | string | Form field name (required) |
| label | string | Display label |
| required | boolean | Make field required |
| placeholder | string | Placeholder text |
| rows | integer | Textarea rows |
| options | array | Options for select, checkbox, radio |
| conditional | object | Show or hide based on another field |

### Conditional logic

Show or hide fields based on another field's value:

```json
{
    "type": "select",
    "name": "department",
    "label": "Department",
    "options": ["Sales", "Support", "Billing"]
},
{
    "type": "text",
    "name": "order_number",
    "label": "Order Number",
    "conditional": {"field": "department", "value": "Billing"}
}
```

The `order_number` field only appears when "Billing" is selected. Multiple values are supported: `"value": ["Support", "Billing"]`.

### Custom messages

Override default UI messages on a per-form basis:

```json
{
    "contact": {
        "recipient": "info@example.com",
        "messages": {
            "sending": "Submitting your enquiry...",
            "error": "Something went wrong. Please try again.",
            "network_error": "Connection failed. Check your internet.",
            "required": "{label} is required.",
            "invalid_email": "Please enter a valid email for {label}.",
            "success": "Thanks! We'll be in touch soon."
        },
        "fields": [ ]
    }
}
```

### Messages reference

| Key | Default | When shown |
|---|---|---|
| sending | "Sending..." | Button text while submitting |
| error | "Failed to send message. Please try again." | Server error |
| network_error | "An error occurred. Please try again." | Network failure |
| required | "{label} is required." | Missing required field |
| invalid_email | "{label}: Please enter a valid email address." | Bad email format |

**Subject placeholders:** use `{field_name}` in the `subject` property to insert submitted values. "Contact from {name}" becomes "Contact from John Smith". Placeholder names are case-sensitive and must match a field `name` exactly.

## Spam Protection

Contact forms attract spam. EP Email ships with a layered defence so most of the noise never reaches your inbox without you having to think about it.

The defence runs in this order on every submission:

1. **CSRF check.** Confirms the submission came from a real page load on your site, not a script POSTing directly to your form endpoint.
2. **Honeypot.** A hidden field invisible to humans but tempting to naive bots. Anything that fills it gets a fake success response and is silently dropped.
3. **Time trap.** A signed timestamp embedded when the form is rendered. Submissions arriving faster than a real human could fill the form are treated as bots and silently dropped.
4. **URL-count filter.** Submissions whose combined fields contain too many `http://` or `https://` links are silently dropped. SEO and link-building spam is structurally URL-heavy.
5. **Keyword blocklist.** Plain text phrases you list, one per line. Any submission containing one is silently dropped.
6. **Rate limit.** Repeat submissions from the same IP within a configurable window are rejected with a "please wait" message.

**Silent drops are deliberate.** Every spam-class block returns the same friendly success message ("Thank you for your submission") and quietly bins the message. Spammers cannot tell whether their submission landed in your inbox or hit a filter, so they cannot probe thresholds or tune around the rules.

### Settings reference

All spam-protection settings live under **EP Email Settings then Contact Forms**.

| Setting | Default | What it does |
|---|---|---|
| Enable Honeypot | On | Adds a hidden field naive bots fill in. |
| Enable Time Trap | On | Rejects forms submitted faster than a human could fill them. |
| Minimum Fill Time (seconds) | 3 | Floor on how fast a human can plausibly submit. Raise to 5 for short forms, lower to 2 only if you see legitimate complaints. |
| Maximum Links per Message | 2 | Reject submissions with more than this many `http(s)://` URLs across all fields. Set to `-1` to disable. |
| Spam Keyword Blocklist | (empty) | One phrase per line. Case-insensitive substring match. Suggested starters: `bitcoin`, `crypto`, `casino`, `seo services`, `guest post`, `backlink`, `link building`, `rank higher`, `viagra`, `cialis`. |
| Enable Rate Limiting | On | Limit repeat submissions from the same IP. |
| Rate Limit (minutes) | 5 | Minimum minutes between submissions from the same IP. |

### Tuning the keyword blocklist

Tune the blocklist to the spam your site is actually receiving. A faith community site needs different terms from a B2B SaaS site. Open the spam folder for the address that receives form submissions, look for repeated phrases, paste them in.

**Hard rule:** keep blocklist entries **specific**. "click" or "free" will eat real submissions. "click here to claim your" or "free SEO audit" will not.

### Beyond the heuristics: AI Triage

Heuristics catch the obvious. They cannot read intent. For sites under sustained spam pressure, the **[EP Email AI Triage](/plugins/ep-email-ai-triage/)** add-on classifies every submission that survives the heuristics with an LLM call — distinguishing a real customer enquiry from a spam pitch by reading the words. See its guide for setup.

### Developer note: should_send hook

Extension developers can intercept submissions silently with the `should_send($form_def, $field_data)` method on `EP_Email_Extension`. Returning anything other than `true` short-circuits delivery: the user sees the form's normal success message but no email is sent. AI Triage uses this hook. Useful for any extension that needs to filter without surfacing rejections to the submitter.

## File Uploads

The EP Email File Uploads extension adds drag-and-drop file upload fields to any contact form. Files are attached directly to the notification email as MIME attachments. They are not stored on your server.

### Usage

Add a file field to any form with `"type": "file"`:

```json
{
    "application": {
        "recipient": "hr@example.com",
        "subject": "Application from {name}",
        "fields": [
            {"type": "text", "name": "name", "label": "Full Name", "required": true},
            {"type": "email", "name": "email", "label": "Email", "required": true},
            {"type": "file", "name": "resume", "label": "Resume / CV", "required": true}
        ]
    }
}
```

### Configuration

File upload settings live in **EP Email Settings** under the File Uploads section:

| Setting | Description |
|---|---|
| Max File Size | Maximum size per file. Default 5 MB. Limited by your server's `upload_max_filesize` PHP setting. |
| Max Files | Maximum number of files per upload field. Default 3. |
| Allowed Types | Comma-separated list of permitted file extensions, for example `pdf,doc,docx,jpg,png`. |

**How it works:** files are uploaded temporarily during form submission, attached to the outgoing email, then deleted. Nothing is stored on your server permanently. That keeps the site clean and avoids storage management entirely.

## Email Logging and Queue

EP Email maintains a complete log of every email your site sends. The log records recipient, subject, delivery status and timestamp.

- **Delivery Log.** View every email sent. Filter by status, search by recipient or subject, diagnose delivery issues at a glance.
- **Email Queue.** Failed emails can be queued for automatic retry. The queue processes on page loads, so messages eventually reach their destination even when the SMTP provider was briefly unreachable.

For most sites, direct delivery is all you need. Enable the queue only if you send high volumes of email (for example through EP Newsletter or EP Bookings) and want automatic retry for temporary failures.

## Extension API

EP Email's extension system lets developers build add-ons that integrate with the contact form engine. Extensions can register custom field types, hook into submissions, add settings, and modify frontend behaviour.

Four main extension points:

- **Custom fields.** Register new field types like signatures, ratings, date pickers, or file uploads. Extensions handle rendering, validation and email integration.
- **Submission hooks.** Hook into the submission pipeline to validate fields, modify email arguments, or trigger post-send actions like auto-responders or webhooks.
- **Settings integration.** Add configuration fields to the EP Email settings page. Keys are auto-prefixed to avoid collisions between extensions.
- **JS hooks.** Frontend JavaScript hooks let add-ons modify form behaviour, append data, react to submission success, or clean up after reset.

### Building an extension

An EP Email extension is a standard PageMotor plugin that registers an `EP_Email_Extension` subclass.

1. **Create a PageMotor plugin.** Your plugin must be a `PM_Plugin` subclass with a valid plugin header.
2. **Check for EP Email.** In `construct()`, verify `class_exists('EP_Email_Extension')` before proceeding.
3. **Require your extension class.** Include the file containing your `EP_Email_Extension` subclass.
4. **Register the extension.** Create an instance and call `EP_Email_Extension::register()`.

### Quick start

```php
// In your plugin's construct() method:
public function construct() {
    if (!class_exists('EP_Email_Extension'))
        return;

    require_once $this->path . '/includes/class-my-extension.php';
    $ext = new My_Extension();
    EP_Email_Extension::register($ext);
}
```

For the complete Extension API reference, including every hook, method and example, see the EP Email Extension Developer Guide bundled with the plugin ZIP.

## Troubleshooting

Common issues and fixes.

### SMTP connection fails

Check your host, port, encryption, and credentials. Verify them against your email provider's documentation. Use **Test Connection** in EP Email Settings to isolate the issue. Common mistakes: wrong port for the selected encryption, or a regular password where an app password is required.

### Emails go to spam

Use a proper SMTP provider, set SPF and DKIM records in your domain's DNS, and ensure the From Email address uses your own domain, not a free provider like gmail.com. A matching From address and an authenticated domain are the two biggest factors in inbox placement.

### Contact form not appearing

Verify that the `name` attribute in your shortcode matches the form key in your JSON definition. If your JSON defines a form under `"contact"`, the shortcode must be `[ep-email name="contact"]`. Check your JSON is valid as well. A missing comma or bracket will silently prevent the form from rendering.

### File uploads not working

Ensure the EP Email File Uploads extension is installed and active in your Theme's plugin configuration. Also check your PHP `upload_max_filesize` and `post_max_size` settings. If the server limit is lower than the configured max file size, uploads are rejected silently.

### Form says "Failed to send"

The form submitted correctly but the email failed to send. Go to EP Email Settings, verify SMTP credentials with **Test Connection**, and check the delivery log for error details. Common causes: an expired app password, the SMTP server temporarily unavailable, or the From Email rejected by the provider.

### Custom field type not rendering

Verify your extension is registered correctly. `EP_Email_Extension::register()` must be called in your plugin's `construct()`. Check that `field_types()` returns the type name and `render_field()` returns valid HTML. If the extension plugin is not active in your Theme, its field types are not available.

### Subject shows {name} literally

The field name in the placeholder must match a field `name` in your form definition exactly. If your field is `"name": "full_name"`, the subject placeholder must be `{full_name}`, not `{name}`. Placeholder substitution is case-sensitive.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
