---
title: "Self-hosted PageMotor on Vultr: SME"
description: The $24 per month Vultr plan for one busy PageMotor site. Right-sized for a single professional service or small shop.
sidebar:
  order: 6
---

One serious site, on a VPS you control. The right-sized middle between the $12 solo plan and the $55 agency box.

## Who this is for

- You run one busy PageMotor site: consultancy, booking-based practice, small shop, service business.
- You, or someone on your team, can read a Terminal window. Or you are happy to let Claude Code do the bash work.
- You want a box with enough headroom to grow into without migrating again in twelve months.

## The plan

**Vultr Cloud Compute, High Performance. 2 vCPU, 4 GB RAM, 100 GB NVMe. $24 per month.**

- 4 GB RAM handles AI plugins, image-heavy galleries and busy admin sessions without stress.
- 100 GB NVMe is enough for years of uploads, invoices and database growth.
- Dedicated CPU not required at this size. High Performance shared CPU is plenty for one site.

Auto Backups at $4.80 per month. On production, always enable.

If sustained daily traffic regularly exceeds a few thousand visitors, step up to 4 vCPU, 8 GB, 180 GB NVMe at $48 per month.

## Sign up for Vultr

Sign up through our referral link: [vultr.com/?ref=9892518-9J](https://www.vultr.com/?ref=9892518-9J). That gives you **$300 of free Vultr credit** at no extra cost to you.

:::note[What the $300 credit covers]
On the $24 per month SME plan, that is roughly 12 months of hosting. You need to link a valid card or PayPal to activate the credit, and the unused portion expires 30 days after signup, so pick the plan you actually intend to run.
:::

:::tip[Full disclosure]
If you stay on Vultr past 30 days and spend at least $100, we earn a $100 referral credit from Vultr. It costs you nothing and does not change the price you pay. You still get the same $300 credit whether you click our link or Vultr's generic signup, so we would rather you use the link and help fund the next round of PageMotor hosting tests.
:::

## What to tick on the Vultr signup screen

| Setting | Pick |
|---|---|
| Server type | Cloud Compute |
| CPU & Storage | High Performance, NVMe |
| Location | Closest Vultr region to your visitors |
| Image | Ubuntu 24.04 LTS x64 |
| Plan | 2 vCPU / 4 GB / 100 GB at $24 per month |
| Auto Backups | Enable |
| IPv6 | Enabled (free) |
| SSH Keys | Your ed25519 public key, uploaded before first boot |
| Hostname | Readable, for example `pm-sme-01` |

Generate an ed25519 key on your Mac if you do not have one:

```bash
ssh-keygen -t ed25519
```

## Claude Code runs the bootstrap

Once the VPS is up and your DNS A record points at it:

1. Install Claude Code from [claude.com/claude-code](https://claude.com/claude-code).
2. Download PageMotor 0.8.2b from the forum, unzip locally.
3. In Claude Code, paste:

```
I have a fresh Ubuntu 24.04 VPS at [VPS_IP].
I can SSH as root using my ed25519 key.

My domain is [yoursite.com]. A record already points at the VPS IP.
My PageMotor 0.8.2b core files are in [~/Downloads/pagemotor-0.8.2b/].

Please follow the full bootstrap at
https://documentation.elmspark.com/hosting/vultr/
end-to-end. Stop after the seeder runs and before admin registration.
British English. No em dashes.
```

Edit the three bracketed placeholders, hit Enter, watch it run. About 30 minutes from empty box to live PageMotor.

## Plugins you will want on day one

After registering your admin account at `/admin/`, ask Claude Code to install:

- EP Email and EP Newsletter SendGrid (transactional email and broadcast).
- EP GDPR (cookie banner and privacy policy for UK and EU sites).
- EP Password Reset (so password resets do not become your job).
- EP Diagnostics (tells you what is wrong before your visitors do).

## Settings that matter at this scale

- **SendGrid SMTP.** Vultr blocks outbound port 25. You will use SMTP relay. Free tier covers most SME volumes.
- **fastcgi_read_timeout 600.** Claude Code sets this. Verify in `/etc/nginx/sites-enabled/` if you do the bootstrap by hand.
- **Auto Backups on.** $4.80 per month for sleep at night.
- **Off-site backup of user-content and DB** on top of Vultr's snapshots. Weekly `restic` run to S3-compatible storage is standard practice.

## Growth path

The $24 plan comfortably handles one busy SME site. Once you add a second site or traffic grows:

- Second SME-size site on the same box: fine, same plan.
- Sustained four-figure daily visitors: step up to $48 per month.
- Four or more sites: move to the $55 agency box. See [Agency, self-hosted](/hosting/agency-diy/).

## Not sure you want to run the box?

[Managed hosting](/hosting/sme-managed/) is the same setup with us handling provisioning, patching, monitoring and support.
