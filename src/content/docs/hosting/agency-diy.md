---
title: "Self-hosted PageMotor on Vultr: Agency"
description: The $55 per month VX1 Vultr plan for agencies running 50 to 100 PageMotor client sites on a single dedicated-CPU box.
sidebar:
  order: 8
---

The test rig we built for PageMotor's Discovery AI work. One $55 per month Vultr box, sized to carry 50 to 100 light-traffic client sites before the fleet needs to split. Dedicated vCPU is the setting that makes the difference.

## Who this is for

- Agencies, service providers, or solo operators hosting five or more PageMotor sites for paying clients.
- You have run a VPS before, or you have Claude Code as your SSH hands.
- You want the cheapest box that still holds a real fleet without performance collapsing at 3 pm.

## The plan

**Vultr VX1 Cloud Compute Dedicated. 2 vCPU, 8 GB RAM, 120 GB NVMe. $55 per month.**

- Dedicated vCPU is the critical difference from cheaper shared-CPU tiers. Noisy-neighbour latency is what makes shared-CPU boxes feel slow in the PageMotor admin.
- 8 GB RAM covers AI plugins running on multiple sites simultaneously.
- 120 GB NVMe carries a 50 to 100 site fleet including uploads and databases.
- VX1 is Vultr's current name for their dedicated-CPU NVMe tier. Older docs say "Cloud Compute Dedicated". Same product.

Auto Backups at $11 per month, which is 20 per cent of the plan. On a shared agency box, always enable. One client mistake becoming every client's problem is a tax you do not want to pay.

### Scaling past 60 to 80 active sites

Step up to **VX1, 4 vCPU, 16 GB, 240 GB NVMe, $111 per month**. Roughly doubles capacity.

At fleet sizes past 200 sites, split across multiple boxes before going bigger on a single one. A failure domain that takes down 200 clients is bad engineering, not good pricing.

## Sign up for Vultr

Sign up through our referral link: [vultr.com/?ref=9892518-9J](https://www.vultr.com/?ref=9892518-9J). That gives you **$300 of free Vultr credit** at no extra cost to you.

:::note[What the $300 credit covers]
On the $55 per month agency VX1 plan, that is roughly 5 months of hosting. You need to link a valid card or PayPal to activate the credit, and the unused portion expires 30 days after signup, so pick the plan you actually intend to run.
:::

:::tip[Full disclosure]
If you stay on Vultr past 30 days and spend at least $100, we earn a $100 referral credit from Vultr. It costs you nothing and does not change the price you pay. You still get the same $300 credit whether you click our link or Vultr's generic signup, so we would rather you use the link and help fund the next round of PageMotor hosting tests.
:::

## What to tick on the Vultr signup screen

| Setting | Pick |
|---|---|
| Server type | Cloud Compute |
| CPU & Storage | Dedicated CPU, NVMe |
| Location | Closest Vultr region to the majority of your clients |
| Image | Ubuntu 24.04 LTS x64 |
| Plan | VX1 2 vCPU / 8 GB / 120 GB at $55 per month |
| Auto Backups | Enable |
| IPv6 | Enabled (free) |
| SSH Keys | ed25519 public key, uploaded before first boot |
| Hostname | For example `pm-agency-01` |
| Everything else | Default. No startup script, no VPC, no DDoS add-on at this scale. |

## Bootstrap via Claude Code

If you do not already have an automated provisioning flow, start here:

```
I have a fresh Ubuntu 24.04 VPS at [VPS_IP].
I can SSH as root using my ed25519 key.

My primary domain is [yoursite.com]. A record already points at the
VPS IP. My PageMotor 0.8.2b core files are in
[~/Downloads/pagemotor-0.8.2b/].

Please follow the full bootstrap at
https://documentation.elmspark.com/hosting/vultr/
end-to-end, stopping after the seeder runs and before admin
registration. I will provision additional client sites on this box
afterwards as a separate pass. British English. No em dashes.
```

Agency fleets usually want an automated multi-site provisioner layered on top of the base bootstrap. The Discovery AI test rig uses a shell script that creates a per-client docroot, database, Nginx vhost and SSL certificate in under 90 seconds per site. The shape is standard: loop over a list of client slugs, `mkdir`, create DB + user scoped to it, drop a per-site Nginx vhost, `certbot --nginx` for SSL, done.

## Per-site economics

Base box at $55 per month, sized for 100 sites conservatively: roughly $0.55 per site per month at full capacity. Even at the more cautious 50-site figure, just over a dollar per site.

Compare to shared hosting at £5 to £15 per site per month, where AI plugins cannot run reliably anyway. The margin between your hosting cost and what clients will pay for managed hosting is where the agency economics live.

## Settings that must be right on a shared agency box

- **`fastcgi_read_timeout` 600 or higher.** Default 60 seconds kills AI plugins mid-call. The single most common cause of "works in test, fails in prod" tickets on PageMotor fleets.
- **PHP `max_execution_time` 300.** Match PHP to Nginx. PHP timeout shorter than Nginx means 504s. PHP longer means processes still running after Nginx gave up.
- **MariaDB `character-set-server = utf8mb4`.** Without this, emojis land in the database as `?`. Silent corruption is the worst kind.
- **Per-site database and DB user.** Never share a database across client sites. Breach surface and restore blast radius both get much worse.
- **Per-site SSL certs, not a wildcard.** Each site manages its own cert and renewal. Isolated failure mode.
- **UFW before anything else.** A new server is scanned within minutes of first boot.
- **Password auth off once keys work.** `PasswordAuthentication no` in `/etc/ssh/sshd_config`.
- **opcache on.** Default on Ubuntu 24.04, verify with `php -m | grep -i opcache`.

## Backup strategy at fleet scale

Vultr Auto Backups snapshot the whole box. Necessary, not sufficient. Add:

- **Off-site DB dumps per client**, daily, to an S3-compatible bucket. `restic` or `rclone` both work.
- **Off-site user-content backup**, weekly or daily depending on how write-heavy the fleet is.
- **Quarterly restore drill.** A backup you have never restored is a belief, not a backup.

## Not sure you want to run the fleet yourself?

[Managed agency hosting](/hosting/agency-managed/) takes the whole fleet off your plate. Same infrastructure shape, run by us.
