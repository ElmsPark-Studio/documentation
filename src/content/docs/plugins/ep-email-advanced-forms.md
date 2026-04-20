---
title: "EP Email Advanced Forms"
description: "Adds compound and layout field types to EP Email contact forms: name, address, section, HTML, email confirmation, and rating fields."
sidebar:
  order: 24
---

EP Email Advanced Forms extends [EP Email](/plugins/ep-email/)'s JSON-defined contact forms with six extra field types: compound fields that group related inputs, layout fields that structure the form visually, and validation fields like email confirmation.

Published by [ElmsPark Studio](https://elmspark.com).

## What it adds

| Field type | Purpose |
|---|---|
| **`name`** | Compound field with separate first and last name inputs that save as one structured value. |
| **`address`** | Compound field with line 1, line 2, city, county, postcode, country. |
| **`section`** | Layout element. Visible heading and description to break a long form into logical sections. |
| **`html`** | Arbitrary HTML block inside the form for notices, instructions, or images. |
| **`confirm_email`** | Paired email input — "Email" and "Confirm email" fields that must match to submit. |
| **`rating`** | Star rating or numeric rating input with configurable scale (1-5, 1-10). |

Each field type plugs into EP Email's form-definition JSON and renders automatically. No code changes to EP Email itself are needed.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Email** (required; this is an extension of EP Email)
- **EP Suite base class**

## Installation

1. Install **EP Email** first.
2. Download `ep-email-advanced-forms.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. The new field types are immediately available in EP Email form definitions.

## Using the new field types

In your EP Email form JSON, use the field type names just like built-in ones.

### Name

```json
{
  "type": "name",
  "id": "full_name",
  "label": "Your name",
  "required": true
}
```

Renders two inputs (First name, Last name) that save as a structured value: `{ "first": "Alice", "last": "Smith" }`.

### Address

```json
{
  "type": "address",
  "id": "delivery_address",
  "label": "Delivery address",
  "required": true,
  "countries": ["GB", "IE", "US"]
}
```

Renders a full address block. The `countries` array limits the country dropdown. Omit for a full country list.

### Section

```json
{
  "type": "section",
  "label": "Contact details",
  "description": "How can we reach you?"
}
```

Pure layout. Renders a heading and an optional description. No submitted value.

### HTML

```json
{
  "type": "html",
  "content": "<p>By submitting, you agree to our <a href=\"/terms/\">terms</a>.</p>"
}
```

Arbitrary HTML. Use for notices, images, or embedded media.

### Email confirmation

```json
{
  "type": "confirm_email",
  "id": "email",
  "label": "Email address",
  "required": true
}
```

Renders two email inputs. Form won't submit if they don't match. Saved value is one email string (not both).

### Rating

```json
{
  "type": "rating",
  "id": "satisfaction",
  "label": "How satisfied are you?",
  "scale": 5,
  "style": "stars"
}
```

`scale` can be 5 or 10. `style` is `stars` or `numeric`. Saved value is the chosen integer.

## Troubleshooting

### "The new field types aren't appearing in my form"

Check:
- The plugin is activated.
- The field `type` in your JSON is spelled correctly (`name`, `address`, `section`, `html`, `confirm_email`, `rating`).
- No typos in the form JSON breaking parsing.

### "Confirm email validates on submit but still lets mismatched values through"

Browser extensions can interfere with form validation. Test in incognito mode. If it still misbehaves, log in the review queue with a repro.

### "Address field shows a country I don't ship to"

Use the `countries` array to restrict the list. Without it, you get every country.

### "Rating field looks broken on mobile"

Star rating touch targets can be fiddly on small screens. Use `numeric` style on mobile-heavy sites for a more forgiving UX.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
