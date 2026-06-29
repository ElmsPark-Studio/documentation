# Installing PageMotor on A2 Hosting — LLM Prompt

> **How to use this file:** Paste the entire contents into Claude, ChatGPT, Gemini, or any LLM as your opening message. It primes the model with the full guide so it can walk you through the install step by step, ask where you're up to, and help you troubleshoot anything that goes wrong. You don't need to read the guide yourself first — just paste and ask.
>
> *Source: [documentation.elmspark.com/guides/pagemotor-a2hosting](https://documentation.elmspark.com/guides/pagemotor-a2hosting/)*

---

You are helping me install PageMotor on my A2 Hosting account (cPanel shared hosting). Use this guide as your reference. Walk me through each step, ask me what I've completed, and help me troubleshoot any issues.

## Context

**Time:** ~10 minutes  
**Skill level:** No coding needed  
**Works on:** All A2 Hosting shared plans (standard cPanel)

**What I'll need before starting:**
- My A2 Hosting account login
- The PageMotor files (the .zip I downloaded)
- The name of my website

**Also available:** the same install on other cPanel hosts — [Bluehost](https://documentation.elmspark.com/guides/pagemotor-bluehost/), [HostGator](https://documentation.elmspark.com/guides/pagemotor-hostgator/) and [GoDaddy](https://documentation.elmspark.com/guides/pagemotor-godaddy/) — plus [SiteGround](https://documentation.elmspark.com/guides/pagemotor-siteground/) (which uses Site Tools, not cPanel) and [Vultr](https://documentation.elmspark.com/guides/vultr-hosting/) (a VPS, not shared hosting).

---

## The 4 Steps

### Step 1 — Put PageMotor on your site

1. Sign in to A2 Hosting at `my.a2hosting.com`, go to **My Accounts**, click **Manage** next to your hosting package, then **Login to Control Panel** to open cPanel
2. Click **File Manager** and open your site folder — `public_html` for your main domain (for an addon domain, use that domain's **Document Root** shown under cPanel → Domains)
3. Click **Upload**, choose your PageMotor `.zip`, and wait for it to finish
4. Back in File Manager, right-click the uploaded zip and choose **Extract**, then delete the zip to keep things tidy

When done you should see `pagemotor.php`, a `lib` folder, and `config-sample.php` in your site folder.

**If extracting created a single `pagemotor` subfolder instead:** open it, select everything inside, choose Move and move it all up into your site folder, then delete the empty folder and the zip.

---

### Step 2 — Create your database

PageMotor stores content in a database. A2 Hosting's cPanel has a wizard that does the whole job in one pass.

1. In cPanel, open the **MySQL Database Wizard** (under the Databases section)
2. Name the database — something like `pagemotor`. A2 Hosting prefixes it with your account name automatically, so the full name shown at the end (e.g. `accountname_pagemotor`) is the one to copy
3. Create the database user. Let the password generator make a strong password, and **write it down now**
4. On the privileges screen, tick **ALL PRIVILEGES** and finish the wizard

Copy the final **database name** and **username** exactly as the wizard shows them (including the account prefix). You'll need those two plus the **password** in the next step.

---

### Step 3 — Fill in config.php

This file connects PageMotor to the database.

1. In File Manager, find `config-sample.php` next to `pagemotor.php`
2. Right-click it → **Rename** → rename to exactly `config.php` *(this rename switches PageMotor on)*
3. Right-click `config.php` → **Edit**
4. Enter your three values into `DB_NAME`, `DB_USER`, and `DB_PASSWORD`, using the full prefixed names from the wizard. Leave everything else as-is. **Save.**

The database section should look like this (edit the existing lines, don't paste this block in):

```php
define('DB_NAME', 'accountname_pagemotor');   // exact name from the wizard
define('DB_USER', 'accountname_pmuser');      // exact username from the wizard
define('DB_PASSWORD', 'your-strong-password');
define('DB_HOST', 'localhost');               // correct for A2 Hosting cPanel
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
- Open cPanel → Metrics → Errors, or the `error_log` file in your `public_html`, for the real error message
- "No such file or directory" for config.php = this is your fix

**"MySQLi Connection Error" in the log**  
config.php is working but the database login failed. Check:
- Database name and username include the full account prefix (the `accountname_` part)
- Password is correct
- User has ALL PRIVILEGES on the database (the wizard's last screen; re-check under cPanel → MySQL Databases)
- Host is `localhost` — correct for all A2 Hosting cPanel accounts

**Site is slow on the first few page loads**  
A2 Hosting's Turbo plans use LiteSpeed with heavy caching. On the first visit after install, LiteSpeed may need a moment to warm its cache, and later loads are fast. If it stays slow, check the cache is enabled under cPanel → **LiteSpeed Web Cache Manager**.

**Can't find config-sample.php**  
It ships with the PageMotor download, next to `pagemotor.php`. Either the files landed in a `pagemotor` subfolder after extraction (move them up, see Step 1 note), or the zip didn't finish extracting (repeat Step 1).

---

**Next step after install:** Contact forms, sign-ups, and password resets need a proper mail service or they'll land in spam. Follow the companion guide: [Set up reliable email with Mailgun](https://documentation.elmspark.com/guides/mailgun-email/) — or use the Mailgun LLM prompt from the same download location.

*Source: ElmsPark documentation — documentation.elmspark.com/guides/pagemotor-a2hosting/*
