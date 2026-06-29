# Installing PageMotor on SiteGround — LLM Prompt

> **How to use this file:** Paste the entire contents into Claude, ChatGPT, Gemini, or any LLM as your opening message. It primes the model with the full guide so it can walk you through the install step by step, ask where you're up to, and help you troubleshoot anything that goes wrong. You don't need to read the guide yourself first — just paste and ask.
>
> *Source: [documentation.elmspark.com/guides/pagemotor-siteground](https://documentation.elmspark.com/guides/pagemotor-siteground/)*

---

You are helping me install PageMotor on my SiteGround hosting account using Site Tools. Use this guide as your reference. Walk me through each step, ask me what I've completed, and help me troubleshoot any issues. Pay special attention to SiteGround's cache — it causes the most problems and is the first thing to check when anything behaves unexpectedly.

## Context

**Time:** ~20 minutes  
**Skill level:** One copy-paste, no real coding  
**Special requirement:** SiteGround's full-page cache must be tamed before PageMotor will behave

SiteGround uses its own control panel called **Site Tools** (not cPanel). Open it per-site via: Client Area → Websites → Site Tools.

**If you're on a cPanel host instead** (Bluehost, HostGator, GoDaddy), use those guides — the steps are simpler.

**What I'll need before starting:**
- A SiteGround hosting account
- The PageMotor files (the .zip I downloaded)
- The name of my website

---

## The 6 Steps

### Step 1 — Put PageMotor on your site

1. In Site Tools, open **Site → File Manager** and go into `public_html`
2. Click the **File Upload** icon and upload your PageMotor `.zip` (SiteGround's File Manager has no upload size limit)
3. Right-click the uploaded zip and choose **Extract**, extracting into `public_html`

When done you should see `pagemotor.php`, a `lib` folder, and `config-sample.php` in `public_html`.

**If extracting created a single `pagemotor` subfolder instead:** open it, select everything inside, choose Move and move it all up into `public_html`, then delete the empty folder and the zip.

---

### Step 2 — Tame SiteGround's cache (do not skip this)

SiteGround runs a full-page cache (Dynamic Cache) on every site, on by default, with no off switch in Site Tools. Its only built-in exceptions are for WordPress and Drupal. Everything else — including PageMotor — gets cached like a static page for up to 12 hours. Skip this step and the install will feel haunted: pages that refuse to change, an admin screen that won't appear, a login that goes in circles.

1. In File Manager, look for `.htaccess` in `public_html`. If it exists, right-click → Edit. If not, create it (New File).
2. Paste this at the very top and save:

```apache
# Temporary while installing PageMotor: stops SiteGround's
# full-page cache serving stale copies of your pages.
<IfModule mod_headers.c>
  Header set Cache-Control "private"
</IfModule>
```

3. Flush the cache once: **Site Tools → Speed → Caching → Dynamic Cache** → Flush Cache action. SiteGround only applies .htaccess caching changes after a flush — this part is not optional.

**How to verify it worked:** Load any page of your site and look at the `x-proxy-cache` response header (browser dev tools → Network → click the page request). **BYPASS** or **MISS** is good. **HIT** means the cache is still answering — flush again.

---

### Step 3 — Create your database

SiteGround chooses the database and username names for you — you don't get to pick them.

1. In Site Tools, open **Site → MySQL** → Databases tab → **Create Database**. SiteGround generates the name (e.g. `dbabc123xyz`).
2. Switch to the **Users** tab → **Create User**. Username and password are generated. The password is shown **once, in a notice** — copy it somewhere safe now.
3. Still under Users, find your new user → **Manage Access** (or Add New Database) → pick your new database → choose **All Privileges** → confirm.

**The step nearly everyone misses on SiteGround:** a freshly created user has access to nothing. If you skip the Manage Access step, PageMotor will be turned away at the door.

You'll need three things for the next step: the generated **database name**, the generated **username**, and the **password** from the notice.

---

### Step 4 — Fill in config.php

This file connects PageMotor to the database.

1. In File Manager, find `config-sample.php` next to `pagemotor.php`
2. Right-click it → **Rename** → rename to exactly `config.php` *(this rename switches PageMotor on)*
3. Right-click `config.php` → **Edit**
4. Enter the three generated values into `DB_NAME`, `DB_USER`, and `DB_PASSWORD`. Leave everything else as-is. **Save.**

The database section should look like this (edit the existing lines, don't paste this block in):

```php
define('DB_NAME', 'dbabc123xyz');              // the generated name from Site Tools
define('DB_USER', 'the-generated-username');   // from the Users tab
define('DB_PASSWORD', 'the-password-from-the-notice');
define('DB_HOST', 'localhost');                // correct for SiteGround
define('DB_CHARSET', '');
define('DB_COLLATE', '');
define('DB_TABLE_PREFIX', 'pm_');
define('DB_FLAGS', '');
define('PM_HTML_CHARSET', '');
```

**Double-check:** file must be named exactly `config.php` (not `config-sample.php`, not `config.php.txt`) and must sit in the same folder as `pagemotor.php`.

---

### Step 5 — Finish in your browser

1. Flush **Dynamic Cache** once more (Site Tools → Speed → Caching) so the first visit is answered by PageMotor, not a cached copy
2. Visit your website. On the first visit PageMotor quietly sets up its content tables
3. Go to `yoursite.com/admin/` and create your admin user
4. **Straight after creating it:** flush Dynamic Cache again AND clear your browser's cookies for the site, *then* log in. This prevents the login loop described in troubleshooting.

---

### Step 6 — Give visitors the cache back (optional)

The Step 2 kill switch turns the cache off for everyone, which is fine for a small site. If you want visitors to get cached pages for speed, swap the kill switch for a scoped rule that only excludes the admin area:

```apache
# Cache public pages, but never the PageMotor admin.
<If "%{THE_REQUEST} =~ m#/admin#">
  <IfModule mod_headers.c>
    Header set Cache-Control "private"
  </IfModule>
</If>
```

Replace the Step 2 block with this, save, and flush Dynamic Cache once more. Every .htaccess caching change needs a flush to take effect.

**Trade-off:** with the cache back on, an edit to a public page can take up to 12 hours to show for visitors unless you flush after every edit. If you edit often, the simple site-wide line from Step 2 is the calmer choice. If anything starts acting stale or the login plays up again, revert to the Step 2 version.

---

## Troubleshooting

**"The user login cookie was not created!" (most common)**  
Your browser got the cookie — the problem is the next page. SiteGround's cache answers it with an old copy saved before you logged in, so PageMotor never sees your cookie. Fix in order:
1. Log out (or just close the tab)
2. Flush Dynamic Cache in Site Tools (Speed → Caching)
3. Delete your browser's cookies for the site
4. Log in again
5. If you just created your first admin user, flush once more straight after creating it
6. Still looping? Check the Step 2 kill switch is actually in `.htaccess` and that you flushed after saving it

**Admin screen won't appear on a fresh install**  
Same cause: cache serving an old copy of `/admin/`. Giveaway: a friend on a different connection can see it but you can't. Do the Step 2 kill switch, flush Dynamic Cache, reload. Check `x-proxy-cache` reads BYPASS or MISS, not HIT.

**My changes don't show up**  
Flush Dynamic Cache in Site Tools. If a page still won't budge, check its `x-proxy-cache` header — HIT means the cache answered. Flush again and re-check your .htaccess rule (each .htaccess change itself needs a flush to take effect).

**HTTP ERROR 500 or blank white page**  
Almost always a `config.php` problem. Check the file is named exactly `config.php`, sits next to `pagemotor.php`, then read the real reason in **Site Tools → Statistics → Error Log**.

**"Access denied" or "MySQLi Connection Error"**  
PageMotor reached the database but couldn't get in. On SiteGround this is nearly always the privileges step:
- User was given All Privileges on the database (Step 3 Manage Access). A new user starts with none.
- Generated database name and username are copied exactly as Site Tools shows them
- `DB_HOST` is `localhost` on SiteGround

**Can't find config-sample.php**  
It ships with the PageMotor download. Either files landed in a `pagemotor` subfolder (move them up, see Step 1 note), or the zip didn't extract completely (repeat Step 1).

---

**Next step after install:** Contact forms, sign-ups, and password resets need a proper mail service or they'll land in spam. Follow the companion guide: [Set up reliable email with Mailgun](https://documentation.elmspark.com/guides/mailgun-email/) — or use the Mailgun LLM prompt from the same download location.

*Source: ElmsPark documentation — documentation.elmspark.com/guides/pagemotor-siteground/*
