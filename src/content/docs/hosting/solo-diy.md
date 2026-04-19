---
title: "Self-hosted PageMotor on Vultr: Solo"
description: The $12 per month Vultr plan for one or two PageMotor sites. Claude Code does the bash work, you paste a prompt and point DNS.
sidebar:
  order: 4
---

A $12 per month Vultr plan, an SSH key, and a Claude Code prompt. That is all it takes to run one or two PageMotor sites on your own VPS.

## Who this is for

- You run one or two PageMotor sites.
- You can follow Terminal instructions, or you are happy to let Claude Code follow them for you.
- You want the lowest hosting bill that still lets AI plugins run without timing out.

## The plan

**Vultr Cloud Compute, High Performance. 1 vCPU, 2 GB RAM, 50 GB NVMe. $12 per month.**

Handles one or two brochure sites with contact forms, EP Email, EP Newsletter, and a Stripe-backed shop. If you plan to use AI plugins heavily, step up to 2 vCPU, 4 GB, 100 GB NVMe at $24 per month for the extra RAM headroom.

Add Auto Backups for $2.40 per month. On production, always enable.

## Sign up for Vultr

Sign up through our referral link: [vultr.com/?ref=9892518-9J](https://www.vultr.com/?ref=9892518-9J). That gives you **$300 of free Vultr credit** at no extra cost to you.

:::note[What the $300 credit covers]
On the $12 per month solo plan, that is roughly 25 months of hosting. You need to link a valid card or PayPal to activate the credit, and the unused portion expires 30 days after signup, so pick the plan you actually intend to run.
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
| Plan | 1 vCPU / 2 GB / 50 GB at $12 per month |
| Auto Backups | Enable |
| IPv6 | Enabled (free) |
| SSH Keys | Your ed25519 public key, uploaded before first boot |
| Hostname | Readable, for example `pm-solo-01` |

Generate an ed25519 key on your Mac first if you do not already have one:

```bash
ssh-keygen -t ed25519
```

Press Enter three times. Your public key lives at `~/.ssh/id_ed25519.pub`. Paste it into Vultr's SSH Keys field during signup.

## The rest is a Claude Code prompt

Once the VPS is up and your domain's A record points at its IP:

1. Install Claude Code from [claude.com/claude-code](https://claude.com/claude-code).
2. Download PageMotor 0.8.2b from the forum and unzip locally.
3. Open Claude Code in Terminal and paste:

```
I have a fresh Ubuntu 24.04 VPS at [VPS_IP].
I can SSH as root using my ed25519 key.

My domain is [yoursite.com]. The A record already points at the VPS IP.
My PageMotor 0.8.2b core files are in [~/Downloads/pagemotor-0.8.2b/].

Please follow the full bootstrap at
https://documentation.elmspark.com/hosting/vultr/
end-to-end. Stop after the PageMotor seeder runs and before admin
registration. Keep me informed at each step. British English. No em
dashes.
```

Edit the three bracketed placeholders, hit Enter, watch it go. About 30 minutes from empty box to live PageMotor.

## After it finishes

1. Open `https://yoursite.com/admin/` in your browser.
2. Register. Whoever registers first becomes the administrator.
3. Come back to Claude Code and ask it to install EP Email, EP Newsletter, EP Newsletter SendGrid, EP GDPR, EP Password Reset and EP Diagnostics. SendGrid is a third-party email relay service. Vultr blocks direct SMTP on port 25, so transactional email has to route through SendGrid or equivalent. The free tier covers most solo volumes.

That is the minimum plugin set for a real site.

## What to check before you forget

- **Auto Backups on** unless this is a pure test box (set this in the Vultr control panel).
- **Certbot renewal** is already wired by Claude Code. Double-check with `systemctl list-timers | grep certbot`.

## Not sure this is for you?

If the word "Terminal" put you off, [managed hosting](/hosting/solo-managed/) is the same setup with us running the box instead.
