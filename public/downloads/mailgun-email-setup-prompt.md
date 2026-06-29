# Mailgun Email Setup — LLM Prompt

> **How to use this file:** Paste the entire contents into Claude, ChatGPT, Gemini, or any LLM as your opening message. It primes the model with the full guide so it can walk you through the setup step by step, ask where you're up to, and help you troubleshoot anything that goes wrong. You don't need to read the guide yourself first — just paste and ask.
>
> *Source: [documentation.elmspark.com/guides/mailgun-email](https://documentation.elmspark.com/guides/mailgun-email/)*

---

You are helping me set up reliable email delivery for my PageMotor (or WordPress) site using Mailgun. Use this guide as your reference. Walk me through each step, ask me what I've completed, and help me troubleshoot any issues.

---

## Context

**What this solves:** Shared hosting sends email via a basic method that Gmail and Outlook quietly distrust — messages land in spam or disappear. Mailgun sends with DKIM (cryptographic signature), SPF (declared sender policy), and DMARC (reporting record) — the three things big providers require for inbox delivery.

**Time:** 20–30 minutes  
**Cost:** Free up to 100 emails/day  
**Works for:** PageMotor and WordPress

**What I'll need:**
- My domain name (e.g. `yourdomain.com`)
- Login to wherever my DNS is managed (Cloudflare, IONOS, GoDaddy, Namecheap, etc.)
- My PageMotor or WordPress admin login

---

## The 10 Steps

### Step 1 — Create your Mailgun account

Sign up at mailgun.com. The free plan needs no credit card. Verify the email address before continuing.

**Critical choice during sign-up: pick your Region.**
- **EU** — if site visitors are mainly in the UK or Europe
- **US** — for North American audiences

This is locked per domain for life. It cannot be changed later.

---

### Step 2 — Add your sending domain

In Mailgun: **Send → Sending → Domains → Add new domain**

Ignore the sandbox domain. Fill in the form field by field:

| Field | What to enter |
|---|---|
| Domain name | `mg.yourdomain.com` (your real domain with `mg.` prefix — keeps Mailgun records separate from existing email) |
| Domain region | Match what you chose at sign-up. Locked for life. |
| IP type | Shared IP (dedicated IPs are for 50k+ emails/month) |
| Security settings | ✅ **Use automatic sender security** — NOT "Self-manage DKIM keys" |
| DMARC / Red Sift | Leave unticked (you'll do this properly in Step 7) |

**Warning:** Mailgun pre-selects "Self-manage DKIM keys" by default. You must change this. The wrong option gives you completely different DNS records (1 TXT record instead of 2 CNAMEs) and this guide won't match.

**If you already added the domain with the wrong option:** go to Domain Settings → Delete Domain, then add it again correctly.

---

### Step 3 — Copy the DNS records

After clicking Add Domain, you land on the DNS records screen. Keep this page open.

With "Use automatic sender security" selected you'll see **7 records**:

| Type | Name / Host | Value | Purpose |
|---|---|---|---|
| TXT | `mg.yourdomain.com` | `v=spf1 include:mailgun.org ~all` | SPF — declares Mailgun is allowed to send |
| CNAME | `pdk1._domainkey.mg.yourdomain.com` | `pdk1._domainkey.<hash>.dkim5.eu.mgsend.org` | DKIM key 1 |
| CNAME | `pdk2._domainkey.mg.yourdomain.com` | `pdk2._domainkey.<hash>.dkim5.eu.mgsend.org` | DKIM key 2 |
| CNAME | `email.mg.yourdomain.com` | `eu.mailgun.org` | Open/click tracking |
| MX | `mg.yourdomain.com` | `mxa.eu.mailgun.org` (priority 10) | Bounce handling |
| MX | `mg.yourdomain.com` | `mxb.eu.mailgun.org` (priority 10) | Bounce handling (redundant) |

**US region?** Replace `eu.mailgun.org` with `mailgun.org` and `eu.mgsend.org` with `mgsend.org`. Always copy values directly from the Mailgun screen — never type them manually.

**Note on Mailgun's "Send to a Coworker" email:** It's a known bug — the setup email only shows 5 records but you need 7. The pdk1 and pdk2 CNAME rows are missing from the email. Always get your values from the Mailgun dashboard, not that email.

---

### Step 4 — Add the records at your DNS provider

Open your DNS provider in a separate tab and add all 7 records.

**Absolute rules:**
- Only one SPF record per DNS name
- Only one DMARC record per DNS name

If either already exists at `mg.yourdomain.com`, edit it rather than adding a second.

**Cloudflare:**
1. DNS → Records → Add record for each of the 7
2. **Critical:** set every record to DNS Only (grey cloud, NOT orange). The orange proxy breaks email authentication.
3. For MX: enter the priority in the Priority box, server address in Content.
4. For CNAME: paste the full value including any trailing dot.

**IONOS:** For CNAME/MX records, enter only the subdomain portion in the Host field (e.g. `pdk1._domainkey.mg` not the full domain). Allow up to 30 minutes for propagation.

**GoDaddy:** Host field takes subdomain portion only. CNAME values without trailing dot.

**Namecheap:** Domain List → Manage → Advanced DNS. Host field: subdomain portion only.

**Shortcut:** On the Mailgun DNS records screen, look for "Automatic setup" — if your provider is listed (Cloudflare, GoDaddy, Bluehost), Mailgun can add all records automatically.

---

### Step 5 — Verify the domain in Mailgun

Return to Mailgun and click **Check Status** (or **Verify DNS Settings**). Each record should change from red cross to green tick.

If records aren't turning green: DNS can take a few minutes (Cloudflare is usually under 60 seconds; IONOS up to 30 minutes). Wait and click Check Status again. If a specific record stays red, compare values character by character.

---

### Step 6 — Wait for DKIM activation

Even after all DNS records show "Verified", sending may not work yet. Mailgun activates DKIM keys asynchronously — this typically takes 30 seconds to 10 minutes.

You may see a yellow warning "Unverified domain settings" even though all rows are green. This is normal. Refresh every few minutes until the warning disappears.

If it hasn't cleared after 30 minutes, contact Mailgun support — but this almost never takes more than 5 minutes.

---

### Step 7 — Enable DMARC

In Mailgun domain settings, scroll to **Authentication records** and click **Enable DMARC**. Mailgun generates a TXT record value like:

```
v=DMARC1; p=none; pct=100; fo=1; ri=3600; rua=mailto:…@dmarc.mailgun.org; ruf=mailto:…@dmarc.mailgun.org;
```

Add a new TXT record at your DNS provider:
- **Name / Host:** `_dmarc.mg.yourdomain.com`
- **Value:** the full string from Mailgun

Then click Check Status in Mailgun — the DMARC row should turn green.

**Note:** The `p=none` policy is intentional — it's report-only mode. Do not change it to `p=reject` or `p=quarantine` until you've been sending successfully for several weeks.

---

### Step 8 — Create a sending key

In Mailgun domain settings → **Sending keys** tab → **Add sending key**.

1. Give it a name (e.g. `pagemotor-site`)
2. Click **Create sending key**
3. **Copy the key immediately** — Mailgun shows it exactly once. Miss it and you have to delete and recreate.

**WordPress + Gravity SMTP users:** You need the account-level Private API key instead (from Settings → API Security), not this domain-scoped key. Gravity SMTP explicitly doesn't support domain-scoped keys.

---

### Step 9 — Connect your site

**PageMotor (EP Suite plugins)**

Install both `ep-email-mailgun` and `ep-newsletter-mailgun`:

1. Plugins → Manage Plugins → Upload → upload and activate each zip
2. In each plugin's settings enter: Sending Key, Sending Domain (`mg.yourdomain.com`), Region
3. Click **Test Connection** — should turn green
4. EP Email → SMTP Configuration → set transport to **Mailgun**
5. EP Newsletter → Email Delivery → set driver to **Mailgun**
6. Make sure `ep-newsletter-mailgun` loads *before* `ep-newsletter` in plugin load order

**WordPress — official Mailgun plugin**

1. Plugins → Add New → search "Mailgun" → install and activate
2. Settings → Mailgun → fill in: Region, Domain (`mg.yourdomain.com`), API Key, From Address, From Name
3. Set "Use API" to Yes → Save → click **Test Configuration**

**WordPress — Gravity SMTP**

1. Install from your Gravity Forms account
2. Gravity SMTP → Settings → Integrations → add Mailgun
3. Use the **account-level Private API key** (from Mailgun Settings → API Security)
4. Fill in domain, region, From address → Save → set Mailgun as Primary

---

### Step 10 — Test it really works

"Domain active" and "connection successful" only mean credentials are valid. They don't prove email will land in an inbox. Do all three:

**A — Send a real test email** via the plugin's test button or a real contact form. Address it to a Gmail inbox you can open.

**B — Check it lands in Inbox, not Spam.** If it went to Spam, it's not set up correctly. A "Be careful with this message" warning in Gmail is also a fail.

**C — Run a mail-tester check.** Go to mail-tester.com, copy the one-off address, send a real email through your site to that address, then check your score. Aim for **9 or 10 out of 10**. Lower scores tell you exactly what's misconfigured.

**D — Check Mailgun event log.** Reporting → Logs → find your test message. Should show: Accepted → Delivered, SMTP code 250. "Failed" or "Rejected" means there's still a configuration problem.

**Only declare it working when:** email is in Inbox (not Spam) + mail-tester.com gives 9 or 10 + Mailgun shows "Delivered". All three together.

---

## Troubleshooting

**Test email lands in Spam**  
DKIM likely not fully active yet (Step 6). Wait a few minutes and resend. Make sure From address uses your domain, not a free address like gmail.com. Run mail-tester.com — it will name exactly what's missing.

**Mailgun shows "Verified" but sending fails**  
DKIM activation lag (Step 6). Wait and refresh the domain overview page. The yellow "Unverified domain settings" warning clears automatically.

**Only 1 TXT DKIM record, not 2 CNAMEs**  
You chose "Self-manage DKIM keys" in Step 2. Fix: Domain Settings → delete domain → add again with "Use automatic sender security".

**Duplicate SPF or DMARC warning**  
Edit the existing record rather than adding a second. Only one of each per DNS name.

**Cloudflare records verified but mail still fails**  
One or more records still has the orange proxy cloud enabled. All email DNS records must be DNS Only (grey cloud). Toggle each to grey and save.

**Chose wrong region during signup**  
The region is locked forever. Options: (a) delete domain + delete account + create new account with correct region; or (b) create a second Mailgun account in the correct region.

**WordPress + Gravity SMTP: "invalid API key"**  
Gravity SMTP doesn't accept domain-scoped keys. Use the account-level Private API key from Mailgun's main Settings → API Security.

**pdk1 / pdk2 CNAME rows missing from Mailgun's coworker setup email**  
Known Mailgun bug. Get all 7 records directly from the Mailgun dashboard DNS screen.

---

*Source: ElmsPark documentation — documentation.elmspark.com/guides/mailgun-email/*
