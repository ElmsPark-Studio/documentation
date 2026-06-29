# Installing PageMotor on GoDaddy — LLM Prompt

> **How to use this file:** Paste the entire contents into Claude, ChatGPT, Gemini, or any LLM as your opening message. It primes the model with the full guide so it can walk you through the install step by step, ask where you're up to, and help you troubleshoot anything that goes wrong. You don't need to read the guide yourself first — just paste and ask.
>
> *Source: [documentation.elmspark.com/guides/pagemotor-godaddy](https://documentation.elmspark.com/guides/pagemotor-godaddy/)*

---

You are helping me install PageMotor on my GoDaddy cPanel Web Hosting account. Use this guide as your reference. Walk me through each step, ask me what I've completed, and help me troubleshoot any issues.

## Context

**Time:** ~10 minutes  
**Skill level:** No coding needed  
**Requires:** GoDaddy's cPanel Web Hosting plan

**Critical — check you have the right GoDaddy product first.** PageMotor needs GoDaddy's Linux **Web Hosting** plan — the one whose hosting dashboard shows a **cPanel Admin** button. Two popular GoDaddy products **cannot** run PageMotor:
- *Websites + Marketing* (the site builder) — no cPanel or file access
- *Managed WordPress* — no cPanel or file access

**What I'll need before starting:**
- GoDaddy Web Hosting account (with cPanel Admin button)
- The PageMotor files (the .zip I downloaded)
- The name of my website

**Also available:** separate guides for [Bluehost](https://documentation.elmspark.com/guides/pagemotor-bluehost/), [HostGator](https://documentation.elmspark.com/guides/pagemotor-hostgator/), and [SiteGround](https://documentation.elmspark.com/guides/pagemotor-siteground/) (which uses Site Tools, not cPanel).

---

## The 4 Steps

### Step 1 — Put PageMotor on your site

**How to open cPanel on GoDaddy:** Sign in at godaddy.com → My Products → next to your Web Hosting plan choose **Manage** → click **cPanel Admin** on the hosting dashboard. Reliable fallback: go to `yourdomain.com/cpanel` and sign in (view/reset cPanel credentials under the hosting dashboard's Settings).

1. In cPanel, click **File Manager** and open the folder for your site. For your main domain: `public_html`. (Installing on an addon domain? Use the folder shown as that domain's Document Root under cPanel → Domains.)
2. Click **Upload**, choose your PageMotor `.zip`, and wait for it to finish
3. Right-click the uploaded zip and choose **Extract**. (If Extract stalls partway, run it again — GoDaddy's shared servers sometimes pause big jobs, and a retry normally finishes it.)

When done you should see `pagemotor.php`, a `lib` folder, and `config-sample.php` in your site folder.

**If extracting created a single `pagemotor` subfolder instead:** open it, select everything inside, choose Move and move it all up into your site folder, then delete the empty folder and the zip.

---

### Step 2 — Create your database

GoDaddy's cPanel has a **MySQL Database Wizard** that does the whole job in one pass.

1. In cPanel, open the **MySQL Database Wizard** (under Databases section)
2. Name the database — pick something distinctive like `yoursite_pagemotor`. GoDaddy requires names unique across their whole system, so a plain name like `pagemotor` may already be taken.
3. Create the database user. Let the password generator make a strong password — **write it down now**. The password is shown only once.
4. On the privileges screen, tick **ALL PRIVILEGES** and finish the wizard

**GoDaddy difference from other hosts:** GoDaddy usually shows the database name exactly as you typed it, with no automatic prefix. If your screen does add a prefix (showing `accountname_` before the name), the full prefixed name is the real one. Either way, copy the final **database name** and **username** exactly as the wizard shows them at the end.

You'll need three things for the next step: the **database name**, the **username**, and the **password**.

---

### Step 3 — Fill in config.php

This file connects PageMotor to the database.

1. In File Manager, find `config-sample.php` next to `pagemotor.php`
2. Right-click it → **Rename** → rename to exactly `config.php` *(this rename switches PageMotor on)*
3. Right-click `config.php` → **Edit**
4. Enter the three values into `DB_NAME`, `DB_USER`, and `DB_PASSWORD`, exactly as the wizard showed them. Leave everything else as-is. **Save.**

The database section should look like this (edit the existing lines, don't paste this block in):

```php
define('DB_NAME', 'yoursite_pagemotor');     // exact name from the wizard
define('DB_USER', 'yoursite_pmuser');        // exact username from the wizard
define('DB_PASSWORD', 'your-strong-password');
define('DB_HOST', 'localhost');              // correct for GoDaddy's cPanel hosting
define('DB_CHARSET', '');
define('DB_COLLATE', '');
define('DB_TABLE_PREFIX', 'pm_');
define('DB_FLAGS', '');
define('PM_HTML_CHARSET', '');
```

**Double-check:** file must be named exactly `config.php` (not `config-sample.php`, not `config.php.txt`) and must sit in the same folder as `pagemotor.php`.

---

### Step 4 — Finish in your browser

1. Visit your website. On the first visit PageMotor quietly sets up its content tables
2. Go to `yoursite.com/admin/` and create your admin user

That's it. You're in.

---

## Troubleshooting

**HTTP ERROR 500 or blank white page (most common)**  
Almost always a `config.php` problem. Check:
- File is named exactly `config.php` (not `config-sample.php`, not `config.php.txt`)
- It's in the same folder as `pagemotor.php`
- Open cPanel → Metrics → Errors for the real error. (On GoDaddy an `error_log` file doesn't appear in your site folder by itself — Metrics → Errors is the place to look. To enable fuller PHP logging, search GoDaddy's help for "Set up PHP error logging".)
- "No such file or directory" for config.php = this is your fix

**"MySQLi Connection Error" in the log**  
config.php is working but the database login failed. Check:
- Database name and username copied exactly as the wizard showed (including any prefix)
- Password is correct
- User has ALL PRIVILEGES (the wizard's last screen; verify under cPanel → MySQL Databases)
- `DB_HOST` should be `localhost` — ignore old tutorials saying GoDaddy needs a special host name. That was legacy hosting; today's cPanel hosting uses localhost.

**Changing PHP version didn't help**  
PHP version is rarely the cause. Fix config.php first. PageMotor runs fine on PHP 8.x. GoDaddy's current default is PHP 8.3. (Change PHP version from the hosting dashboard's Settings tab or inside cPanel.)

**Can't find config-sample.php**  
It ships with the PageMotor download, next to `pagemotor.php`. Either the files landed in a `pagemotor` subfolder after extraction (move them up, see Step 1 note), or the zip didn't finish extracting (repeat Step 1).

---

**Next step after install:** Contact forms, sign-ups, and password resets need a proper mail service or they'll land in spam. Follow the companion guide: [Set up reliable email with Mailgun](https://documentation.elmspark.com/guides/mailgun-email/) — or use the Mailgun LLM prompt from the same download location.

*Source: ElmsPark documentation — documentation.elmspark.com/guides/pagemotor-godaddy/*
