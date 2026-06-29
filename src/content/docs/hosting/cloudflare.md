---
title: Cloudflare for PageMotor DNS
description: Why we recommend Cloudflare for DNS, and a step-by-step setup including letting Claude Code manage your records.
sidebar:
  order: 2
---

This guide is a companion to the Vultr hosting guide. There you set up the box that runs your PageMotor site. Here you set up the DNS that points your domain at it.

We run PageMotor sites on a simple, dependable stack: **Vultr** for compute, **Cloudflare** for DNS, and **Mailgun** for email. This page covers the middle piece.

## Why Cloudflare for DNS

You can run DNS at any registrar. We recommend moving it to Cloudflare for a few practical reasons.

**It is free at any scale.** Cloudflare's Free plan covers DNS for your domain with no per-zone or per-record charge. One domain or twenty, the DNS itself costs nothing.

**Domains renew at cost.** If you later register or transfer your domain with Cloudflare Registrar, you pay only what the registry and ICANN charge. There is no renewal markup. (More on this at the end.)

**Resolution is fast and consistent.** Cloudflare answers DNS queries from a large anycast network, so lookups resolve quickly and reliably wherever your visitors are.

**One API that Claude Code can drive directly.** This is the big one for a managed setup. Cloudflare has a single, consistent API. Once Claude Code holds a scoped token for your account, it can point your domain, add records and set redirects for you. No clicking around a registrar control panel, no copying values by hand.

**One credential surface.** Instead of separate logins scattered across different registrars, your DNS lives in one place with one account to secure.

:::tip
If you are following the Vultr guide, think of it as one stack: Vultr runs the site, Cloudflare answers DNS, Mailgun sends email. Each piece does one job well.
:::

## Move your domain's DNS to Cloudflare

### 1. Create a free account

Go to [dash.cloudflare.com](https://dash.cloudflare.com) and sign up with an email and password. Verify the email Cloudflare sends you. The Free plan is the default and no card is needed to get a domain onboarded.

### 2. Add your domain and pick the Free plan

In the dashboard, go to **Domains**, then select **Onboard a domain**. Enter your apex domain (for example `example.com`), choose how to add your records, and select **Continue**. When you are asked to choose a plan, pick **Free**.

### 3. Let Cloudflare scan your records, then check them carefully

Cloudflare runs a quick scan of your current DNS and copies the records it finds into your new zone. This is a real time-saver, but Cloudflare is clear that the scan is best-effort and may miss records. **You must review them.**

Before you change anything at your old registrar, go through the **DNS records** table in Cloudflare and confirm each of these came across exactly:

- **MX** records (mail routing). The value and the **priority** must match.
- **SPF**, published as a **TXT** record starting `v=spf1`.
- **DMARC**, a **TXT** record at `_dmarc.yourdomain`.
- **DKIM**, a **TXT** or CNAME record at your selector host, for example `selector._domainkey.yourdomain`.
- Any **verification TXT** records (Google, Microsoft, SSL providers and so on). These are the ones the scan most often misses.

A good habit is to pull your current zone from your existing provider first (an export, or a `dig` lookup) and compare it line by line against what Cloudflare imported.

:::caution
This step protects your email. A missing **MX** or **SPF** record means mail stops being delivered the moment your nameservers switch over. Do not move on until every email and verification record is present and correct.
:::

### 4. Change the nameservers at your registrar

Cloudflare assigns your zone **two nameservers**. The pair is **unique to your zone** and shown during onboarding and on the zone **Overview** page. You cannot pick or change which pair you get.

At your current registrar, remove the existing nameservers and add Cloudflare's two. Copy them exactly, character for character, or your domain will not resolve.

:::caution
If your domain currently uses **DNSSEC**, turn it off at your registrar before switching nameservers. Leaving it on with a new DNS provider can make the domain unreachable.
:::

### 5. Wait for activation and verify

When the switch takes effect, your domain shows as **Active** on the **Domains** page and Cloudflare emails you to confirm. Propagation can take a while depending on your registrar and old TTLs, so be patient.

Confirm it yourself with `dig`:

```bash
dig ns example.com @1.1.1.1
dig ns example.com @8.8.8.8
```

Both should return the Cloudflare nameservers assigned to your zone.

## Point the record at your Vultr box (grey cloud)

In the **DNS records** table, each A, AAAA or CNAME record has a **Proxy status** you can toggle:

- **Grey cloud (DNS only)** means Cloudflare hands back your server's real IP address and stays out of your web traffic.
- **Orange cloud (Proxied)** means Cloudflare sits in front of your server, caching and protecting traffic.

For your initial setup, set your site's **A record to DNS only (grey cloud)**. This points your domain straight at your Vultr box.

You need this for the certificate step in the Vultr guide. With the grey cloud on, certbot can issue your Let's Encrypt certificate against the real origin, and PageMotor sees genuine HTTPS.

:::tip
Want Cloudflare's CDN, caching and DDoS protection later? You can. Turn the cloud **orange only after your certificate is live**, then go to **SSL/TLS > Overview** and set the encryption mode to **Full (strict)**.
:::

:::caution
Never use the **Flexible** SSL mode. Flexible talks to your origin over plain HTTP, which makes PageMotor emit `http://` links and can trigger a redirect loop. If you proxy through Cloudflare, use **Full (strict)** so traffic to your origin is encrypted and the certificate is validated.
:::

See the Vultr guide's TLS and certbot section for the matching server-side steps.

## Add Mailgun's email records here

If you use Mailgun for email (recommended in the Vultr guide), this is where its DNS records live.

Add Mailgun's **SPF**, **DKIM** and **tracking** records on your `mg.` sending subdomain. By type, these are TXT and CNAME records, so they are always **DNS only (grey cloud)**. Never proxy them.

:::caution
Add Mailgun's records to your **`mg.` sending subdomain only**. Never put Mailgun's MX records on your apex domain. Doing so hijacks inbound mail for your whole domain.
:::

See the Email section of the Vultr guide for the exact values Mailgun gives you.

## Let Claude Code manage your DNS (optional but recommended)

This is where the single consistent API pays off. Once Claude Code holds a Cloudflare API token for **your** account, it can do the DNS work for you: point your domain, add records (including the Mailgun ones above) and set redirects, all without you touching the dashboard.

You stay in control. The token you create is least-privilege and revocable, and you scope it to your own account and zone only.

### Create the token

1. In the Cloudflare dashboard, open **My Profile > API Tokens**, then select **Create Token**.
2. Find **Create Custom Token** and select **Get started**.
3. Add two permission rows. Each row is **Group > Permission > Access**:
   - **Zone > DNS > Edit**
   - **Zone > Zone > Read**
4. Under **Account Resources**, select your own account. Under **Zone Resources**, choose **Include** and then a **Specific zone** (your domain). You can include all your zones instead if you prefer Claude Code to manage every domain on your account.
5. *(Optional)* Restrict the token in the **Client IP Address Filtering** and **TTL (time to live)** fields. A TTL gives the token an expiry date, which is handy for rotating it once a year.
6. Create the token and copy it now. Cloudflare shows the full value only once.

Why those two permissions:

- **Zone:DNS:Edit** is full create, read, update and delete access to your DNS records. This is what lets Claude Code add and change records.
- **Zone:Zone:Read** lets the token find your zone in the first place. Without it, the token cannot look up which zone your domain belongs to.

This exact pair is the least-privilege set for managing DNS records, and it matches Cloudflare's own built-in "Edit zone DNS" template.

### Store it securely

Keep the token in a file that only you can read. A generic location works well:

```bash
mkdir -p ~/.config/cloudflare
printf 'CLOUDFLARE_API_TOKEN=your-token-here\n' > ~/.config/cloudflare/token.env
chmod 600 ~/.config/cloudflare/token.env
```

`chmod 600` means only your user account can read the file. Never commit this file to git, and never paste the token into a chat, an issue or a screenshot.

### Verify it works

Load the token and ask Cloudflare to verify it:

```bash
source ~/.config/cloudflare/token.env

curl -s https://api.cloudflare.com/client/v4/user/tokens/verify \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

A working token returns `"success": true` with a result whose `"status"` is `"active"`. If you see that, Claude Code can now manage your DNS.

:::note
**What this token can and cannot do.** It is deliberately least-privilege: it can edit DNS records and read zone information, and nothing else. It **cannot** transfer your domain, change your billing, or touch SSL, Workers or any other Cloudflare feature, because none of those permissions are granted. You can revoke it instantly from **My Profile > API Tokens** in the dashboard, and you should rotate it about once a year. Always scope it to your own account and your own zone.
:::

## Optional: move your domain registration to Cloudflare too

Once your DNS is on Cloudflare, you can also move the domain registration there. This is a bonus, not a requirement, and your DNS works fine either way.

The draw is at-cost renewals with no markup. A few conditions apply:

- Your zone must already be **active on Cloudflare DNS** (the steps above) before you can transfer.
- The domain must have been registered **at least 60 days ago** and not transferred in the last 60 days. This is an ICANN rule, not a Cloudflare one.

:::note
Cloudflare Registrar supports many extensions, including `.com` and UK domains such as `.uk` and `.co.uk` (handled via Nominet). It does not support every TLD, though. Check Cloudflare's supported-TLD list for your specific domain. If yours is not supported, keep it at a different registrar. You can still use Cloudflare for DNS regardless.
:::
