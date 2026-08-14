---
title: "Supported PageMotor version"
description: "ElmsPark supports PageMotor 0.10.3b. Why there is a single supported version, how to check yours, and what to do if your site is older."
---

**ElmsPark supports PageMotor 0.10.3b.** Every site we build, host, or help with should be running it, and every EP Suite plugin is tested against it.

## Why there is only one

PageMotor has not launched publicly yet. That gives us a rare chance to set a floor now rather than carry a tail of old versions for years, so support, testing, and documentation all point at the same place. One version means a fix that works on our machines works on yours.

Release candidates such as 0.11rc4 are for testing on throwaway sites. They are not a target for a site you care about.

## Check which version you have

Log in to your admin and open **Updates**. The PageMotor row shows both numbers side by side:

```
PageMotor    Installed: 0.10.3  |  Available: 0.10.3
```

If the installed number is 0.10.3, you are current and there is nothing to do.

## If your site is older

Open **Updates** and press the update button. On a healthy site the update runs itself, the page reloads, and the version number has changed. It is normally a one-click job even when the site is several versions behind.

Two things are worth knowing if that does not happen:

- **The screen says there are no updates, but you know your version is old.** Sites on PageMotor 0.8 and earlier cannot see updates at all. The update check runs and reports success, but nothing is ever offered, because those versions cannot read what the update server now sends back. The site cannot tell you this, so the Updates screen looks reassuring while nothing is available. These sites need the update putting in by hand once, after which the button works normally.
- **The button is there but pressing it does nothing.** Take a backup first, then get in touch rather than pressing repeatedly.

In both cases the fix is the same shape: PageMotor is replaced with the current version, and your `config.php`, your pages, and your content are untouched by it. If you would rather not do that alone, ask, and we will walk it through with you.

## Plugin requirements are a separate thing

Each EP Suite plugin's page lists the minimum PageMotor version that plugin technically needs, and some of those minimums are lower than 0.10.3b. That is deliberate: it describes what the plugin itself depends on, not what we support. A plugin that runs on an older core is still running on a core we do not support, so the answer to almost any problem remains the same. Get to 0.10.3b first.

## Getting help

For a quick question, EP Support inside your admin is the fastest option. For anything bigger, open a ticket at [help.elmspark.com](https://help.elmspark.com).
