# Keeping your PageMotor VPS healthy — LLM Prompt

> **How to use this file:** Paste the whole thing into Claude Code as your opening message, edit the bracketed details at the top, then hit Enter. Claude Code will SSH into your server, check what needs doing, tell you before it changes anything, and prove the site still works when it finishes.
>
> There are two prompts here. **Prompt A** is a one-off, run it once shortly after your server is built. **Prompt B** is the routine one, run it every month.
>
> *Source: [documentation.elmspark.com/guides/vps-maintenance](https://documentation.elmspark.com/guides/vps-maintenance/)*

---

## Read this first: who maintains your server?

You do.

Hostinger, Vultr, DigitalOcean and every other VPS provider sell you a **self-managed** server. In Hostinger's own words: "As our VPS solutions are self-managed, you will get full freedom to configure and manage the virtual server."

That freedom is the whole reason a VPS fixes the problems shared hosting gives PageMotor. It is also the bill. The split is:

**Your provider looks after:** the physical hardware, the hypervisor, the network, DDoS filtering at the network edge, the control panel in their dashboard, and whatever backup or snapshot feature your plan includes.

**You look after:** everything from the operating system upwards. Ubuntu security patches, the kernel, CloudPanel, nginx, PHP, MySQL or MariaDB, your TLS certificates, SSH access, the firewall, PageMotor core, and your plugins.

Nobody sends you a reminder. A server left alone for a year is running a year of known, published, publicly indexed vulnerabilities. This is the single most common way a small self-hosted site gets compromised, and it is entirely preventable in about fifteen minutes a month.

If your site collects any personal data at all, a contact form counts, then in the UK and EU this is not only good practice. UK GDPR and EU GDPR Article 32 require "appropriate technical and organisational measures" to keep that data secure, and an unpatched server is very hard to defend as appropriate.

---

## Prompt A — one-time hardening pass

Run this once, soon after your server is built and PageMotor is live. It closes the gaps that a fresh control-panel install leaves open, and it turns on automatic security patching so the routine job stays small.

Copy everything in the block below.

```
I have a PageMotor site on a self-managed VPS and I want you to harden it and set up automatic security patching.

MY DETAILS
- Server IP: [YOUR_VPS_IP]
- I SSH in as: root
- My SSH key: ~/.ssh/id_ed25519
- My site domain: [yoursite.com]
- Control panel: [CloudPanel / none / other]
- Provider: [Hostinger / Vultr / other]

HOW I WANT YOU TO WORK
- Take a snapshot or backup through my provider's dashboard BEFORE you change
  anything. If you cannot do that yourself, stop and tell me how to do it,
  and wait until I confirm it is done.
- Show me what you plan to change before you change it.
- Never restart the web server, PHP, the database or the machine itself
  without telling me first and getting a yes.
- If something is already correctly configured, say so and move on. Do not
  reconfigure things that are fine.

WHAT TO DO
1. Report the current state first: OS version, kernel, uptime, free disk,
   free memory, and which of the things below are already in place. Do not
   change anything yet. Wait for me to say go.

2. Automatic security updates. Check whether unattended-upgrades is
   installed and actually enabled. If it is not, install and enable it for
   SECURITY updates only. Do not enable automatic reboots. Show me the
   resulting config and confirm the timer is active.

3. Firewall. Confirm only the ports I actually need are open, normally
   22, 80 and 443, plus my control panel port if I use one. Tell me every
   other listening service you find before closing anything.

4. SSH. Confirm key-based login works for me RIGHT NOW before you touch
   anything, then disable password authentication and set root login to
   key-only. Getting locked out of my own server is the worst outcome here,
   so verify first, change second.

5. fail2ban. Install it if missing and enable an sshd jail. On many
   distributions the package installs inactive, so confirm it is actually
   running, not just installed.

6. Backups. Tell me exactly what backup my provider plan includes, how
   often it runs, how many copies it keeps, and how I would restore one.
   If my plan has no backups, say so plainly and tell me what it costs to
   add them.

7. TLS certificate. Confirm the certificate is valid, tell me its expiry
   date, and confirm automatic renewal is scheduled and working. If my site
   runs PageMotor behind CloudPanel, confirm that /.well-known/acme-challenge
   is still served from disk, because PageMotor MCP fixes to /.well-known/
   can break certificate renewal if they are applied carelessly.

8. Write me a plain-text summary at /root/server-notes.md recording what
   this server runs, what you changed today, and what needs checking monthly.

FINISH BY PROVING IT WORKS
Fetch https://[yoursite.com]/ over the public internet and show me the HTTP
status and the first part of the response. Then fetch the admin page and
confirm it loads. Do not tell me the server is hardened until you have
pasted that output. A command exiting successfully is not proof the site
still works.
```

---

## Prompt B — the monthly maintenance run

This is the routine one. Set a monthly reminder and paste this in. It normally takes ten to twenty minutes and most months it finds very little, which is exactly what you want.

Copy everything in the block below.

```
Monthly maintenance run on my PageMotor VPS. Work carefully and report
before you act.

MY DETAILS
- Server IP: [YOUR_VPS_IP]
- I SSH in as: root
- My SSH key: ~/.ssh/id_ed25519
- My site domain: [yoursite.com]
- Control panel: [CloudPanel / none / other]
- Provider: [Hostinger / Vultr / other]

GROUND RULES, THESE MATTER MORE THAN SPEED
- Snapshot or back up through my provider BEFORE any change. If you cannot
  trigger it, stop and tell me how, and wait for my confirmation.
- This is a live production site. Report first, act second. I want to see
  the list of what would change before it changes.
- Never upgrade a MAJOR version of PHP, MySQL, MariaDB or the operating
  system as part of routine maintenance. Those are planned projects with a
  rollback plan, not a Tuesday job. Flag them and stop.
- Never reboot without asking. If a reboot is genuinely required, tell me
  why, and let me pick the time.
- If anything looks wrong or ambiguous, stop and ask. Leaving a job half
  done and telling me is far better than guessing.

STEP 1: REPORT, CHANGE NOTHING
Give me a short status report:
- Uptime, and whether /var/run/reboot-required exists
- Free disk and free memory, and flag anything over 80 per cent used
- Everything in `apt list --upgradable`, split into security updates and
  everything else
- Whether unattended-upgrades is enabled and when it last ran successfully
- TLS certificate expiry date for my domain
- fail2ban status and how many bans in the last month
- Any service that failed to start (`systemctl --failed`)
- The last 20 authentication failures, so I can see if I am being probed
- Current PageMotor core version and whether the Updates screen shows one
  available
Then stop and wait for me.

STEP 2: AFTER I SAY GO
- Apply the operating system SECURITY updates.
- Apply non-security updates too, unless any of them touch PHP, the
  database, or the kernel, in which case list those separately and ask.
- If I am on CloudPanel, update it with `clp-update`. CloudPanel's own
  documentation says to snapshot first, so confirm the snapshot from the
  ground rules actually exists before you run it.
- Clear out old kernels and package cache if disk is tight, and tell me how
  much you freed.

STEP 3: THE APPLICATION LAYER
- Check my PageMotor admin Updates screen for a core update and tell me
  what is available and what changed. Do not install a core update without
  asking me.
- Check my installed plugins for updates the same way.
- These are separate from the operating system. A fully patched Ubuntu with
  an outdated CMS is still an outdated CMS.

STEP 4: PROVE THE SITE STILL WORKS
This is the part that matters, so do not skip it or summarise it.
- Fetch https://[yoursite.com]/ over the public internet. Paste the HTTP
  status code and enough of the response body to show the real page came
  back, not an error page or a holding page.
- Fetch the admin login page and confirm it loads.
- Submit nothing, but confirm my contact form page renders.
- Confirm the TLS certificate is still valid and shows the expected expiry.
- If any of those fail, tell me immediately and tell me how to roll back to
  the snapshot.

STEP 5: WRITE IT DOWN
Append today's run to /root/server-notes.md: the date, what you updated,
anything you deliberately did not update and why, and anything I should
watch next month.

Then give me a five-line summary I can read on my phone. Do not use the
words "done", "fixed" or "all good" unless you have pasted the live site
response from step 4.
```

---

## How often, and how to remember

**Monthly is the right cadence** for the routine run, with automatic security patching handling the urgent things in between. That combination means an unattended-upgrades job installs critical fixes within a day or so of release, and your monthly run catches everything automation cannot safely do on its own: reboots, control panel updates, the CMS, the plugins, and actually looking at the thing.

**On scheduling, be realistic.** You can ask Claude Code to run on a schedule, but it runs on your machine, and your machine is asleep in a bag most of the time. A calendar reminder on the first of the month that you actually action is more reliable than automation you assume is running. If you want it genuinely unattended, that belongs on an always-on machine, not a laptop.

**The one thing to automate properly is security patching**, because it is the one thing where the delay between a fix being published and you installing it is the whole risk. Prompt A sets that up.

---

## When to stop doing this yourself

There is no shame in deciding you do not want to be a sysadmin. Signs it is time to pay someone:

- The site earns money and an outage costs more than a support plan
- You are storing customer personal data and want the compliance question answered properly
- You have skipped the monthly run three times in a row, which is most people
- You are running more than three or four servers

At that point the honest options are a managed hosting plan, a managed VPS from a provider that sells one, or a maintenance retainer with someone who does this for a living. All three are cheaper than the incident.

---

*An ElmsPark guide. Hostinger's self-managed wording quoted from hostinger.com/vps-hosting. CloudPanel update procedure per cloudpanel.io/docs/v2/update/.*
