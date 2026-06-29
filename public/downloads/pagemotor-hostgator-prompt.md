# Installing PageMotor on HostGator — LLM Prompt

> **How to use this file:** Paste the entire contents into Claude, ChatGPT, Gemini, or any LLM as your opening message. It primes the model with the full guide so it can walk you through the install step by step, ask where you're up to, and help you troubleshoot anything that goes wrong. You don't need to read the guide yourself first — just paste and ask.
>
> *Source: [documentation.elmspark.com/guides/pagemotor-hostgator](https://documentation.elmspark.com/guides/pagemotor-hostgator/)*

---

You are helping me install PageMotor on my HostGator account (or any cPanel hosting). Use this guide as your reference. Walk me through each step, ask me what I've completed, and help me troubleshoot any issues.

## Context

**Time:** ~10 minutes  
**Skill level:** No coding needed  
**Works on:** Any cPanel host

**Important — check you have the right HostGator product:** HostGator's standard Web Hosting plans all include cPanel and will work. Their separate **Website Builder** product does NOT give you cPanel or file access, and PageMotor cannot run there.

**What I'll need before starting:**
- A HostGator web hosting account (standard hosting, not Website Builder)
- The PageMotor files (the .zip I downloaded)
- The name of my website

**Also available:** separate guides for [Bluehost](https://documentation.elmspark.com/guides/pagemotor-bluehost/), [GoDaddy](https://documentation.elmspark.com/guides/pagemotor-godaddy/), and [SiteGround](https://documentation.elmspark.com/guides/pagemotor-siteground/) (which uses Site Tools, not cPanel).

---

## The 4 Steps

### Step 1 — Put PageMotor on your site

**How to open cPanel on HostGator:** Log in at portal.hostgator.com, choose Hosting in the menu, and click the **cPanel** button under Quick Links. Shortcut that always works: go to `yourdomain.com/cpanel` and log in with the cPanel details from your HostGator welcome email.

1. In cPanel, click **File Manager** and open the folder for your site — usually `public_html`. (Installing on an addon domain? Use that domain's own folder instead; shown under cPanel → Domains.)
2. Click **Upload**, choose your PageMotor `.zip`, and wait for it to finish. (File Manager accepts files up to 500 MB — far larger than the PageMotor zip.)
3. Right-click the uploaded zip and choose **Extract**

When done you should see `pagemotor.php`, a `lib` folder, and `config-sample.php` in your site folder.

**If extracting created a single `pagemotor` subfolder instead:** open it, select everything inside, choose Move and move it all up into your site folder, then delete the empty folder and the zip.

---

### Step 2 — Create your database

PageMotor stores content in a database. Three stages:

1. In cPanel, open **MySQL Databases** (under Databases section)
2. Under **Create New Database**, type a name like `pagemotor` and click **Create Database**
3. Scroll to **MySQL Users → Add New User**. Pick a username, let the password generator create a strong password, click **Create User**. **Write the password down now.**
4. Scroll to **Add User To Database**. Choose your new user and database, click **Add**, tick **ALL PRIVILEGES**, click **Make Changes**

**Critical — the prefix trap:** cPanel adds your account name to the front of both the database name and username. A database typed as `pagemotor` is saved as something like `theaccount_pagemotor`. Copy the **full names exactly as cPanel shows them**.

You'll need three things for the next step: the full **database name**, the full **username**, and the **password**.

---

### Step 3 — Fill in config.php

This file connects PageMotor to the database.

1. In File Manager, find `config-sample.php` next to `pagemotor.php`
2. Right-click it → **Rename** → rename to exactly `config.php` *(this rename switches PageMotor on)*
3. Right-click `config.php` → **Edit**
4. Enter the three values into `DB_NAME`, `DB_USER`, and `DB_PASSWORD`, using the full prefixed names from Step 2. Leave everything else as-is. **Save.**

The database section should look like this (edit the existing lines, don't paste this block in):

```php
define('DB_NAME', 'theaccount_pagemotor');   // exact name from cPanel
define('DB_USER', 'theaccount_pmuser');      // exact username from cPanel
define('DB_PASSWORD', 'your-strong-password');
define('DB_HOST', 'localhost');              // correct for HostGator and most cPanel hosts
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
- Open cPanel → Metrics → Errors for the real error. HostGator's Customer Portal also shows errors without opening cPanel: Websites → Settings → Advanced → Logs
- "No such file or directory" for config.php = this is your fix

**"MySQLi Connection Error" in the log**  
config.php is working but the database login failed. Check:
- Database name and username include the full account prefix (`theaccount_` part)
- Password is correct
- User was added to the database with ALL PRIVILEGES (Step 2, last part)
- Rarely: host uses a different DB_HOST — check host's welcome email if `localhost` doesn't work

**Changing PHP version didn't help**  
PHP version is rarely the cause. Fix config.php first. PageMotor runs fine on PHP 8.x. HostGator note: older accounts can still default to PHP 7.4 — once the install works, check cPanel → Software → MultiPHP Manager and pick a PHP 8 version if needed.

**Can't find config-sample.php**  
It ships with the PageMotor download, next to `pagemotor.php`. Either the files landed in a `pagemotor` subfolder after extraction (move them up, see Step 1 note), or the zip didn't finish extracting (repeat Step 1).

---

**Next step after install:** Contact forms, sign-ups, and password resets need a proper mail service or they'll land in spam. Follow the companion guide: [Set up reliable email with Mailgun](https://documentation.elmspark.com/guides/mailgun-email/) — or use the Mailgun LLM prompt from the same download location.

*Source: ElmsPark documentation — documentation.elmspark.com/guides/pagemotor-hostgator/*
