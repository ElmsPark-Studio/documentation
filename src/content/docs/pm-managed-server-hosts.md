---
title: "PM Managed Server: host research"
description: VPS and mailbox host comparison for a resellable PageMotor Managed Server offering, with end-to-end CC automation verification.
sidebar:
  hidden: true
pagefind: false
head:
  - tag: meta
    attrs:
      name: robots
      content: noindex, nofollow
---

Research brief for a resellable "PageMotor Managed Server" bundle. The load-bearing criterion is API depth, because Claude Code acts as the 24/7 managed-services layer by driving the host's API. Human support quality is a secondary concern.

The target end customer is a non-technical PageMotor Forum member. One vendor, one login, one bill is the Phase 1 ideal. Phase 2 accepts a VPS plus a third-party email partner, provided both expose APIs a code agent can drive without human intervention.

Currency conversions use rates current at 21 April 2026: USD 1 is about GBP 0.78, EUR 1 is about GBP 0.85. Prices are rounded to the nearest pound in the table.

:::caution[The single biggest gotcha]
Port 25 outbound is blocked by default on nearly every cloud VPS in this review, including Hetzner, Vultr, Linode, DigitalOcean, Hostinger and IONOS. DigitalOcean refuses to unblock at all. Only OVHcloud and Hostwinds ship with port 25 open. A transactional relay (Postmark, Mailgun or AWS SES) is therefore mandatory regardless of VPS vendor.
:::


## Executive summary

### Top 3 Phase 1 picks

1. **OVHcloud (global, UK/EU-focused).** The only mainstream host in this review that ships a KVM VPS with port 25 unblocked by default, a native MX Plan mailbox product with IMAP and SMTP, a full OVH API covering compute, DNS and email, and UK and EU data centres. The obvious first call for European members.
2. **IONOS (UK/EU, US).** A genuine one-bill VPS plus mailbox shop with an active developer API PM already has credentials for. Mailbox API surface is thinner than OVH's, but the affiliate programme pays on cloud servers and the brand carries weight with non-technical members.
3. **Scala Hosting (US-focused, global locations).** SPanel is the only true whitelabel control panel in the field, the WHMCS module covers account provisioning and email mailbox creation via API, and the managed VPS product bundles email natively. The US pick where end-member branding matters most.

### Top 2 Phase 2 picks

1. **Hetzner Cloud plus Migadu.** Hetzner has the cleanest REST API in the review (compute, DNS, firewalls, load balancers). Migadu exposes a mailbox API plus Terraform provider and charges by volume rather than per mailbox, which keeps the blended cost low. EU-centric, GDPR-aligned, highly automatable.
2. **Vultr plus Fastmail (or Zoho).** Vultr's API is broad and global, Fastmail's JMAP API is the modern standard for mailbox automation, and Zoho Mail offers a formal reseller programme with a WHMCS provisioning module. Good coverage for US and APAC members where Hetzner latency hurts.


## Outbound SMTP strategy

Route all outbound application mail through a transactional relay, irrespective of VPS vendor. VPS port 25 policies change, shared-tenant IP reputation is volatile, and a dedicated relay outperforms a self-hosted mailer on deliverability even when the port is open.

The three realistic candidates are Mailgun, Postmark and AWS SES.

**AWS SES** is cheapest at USD 0.10 per 1,000 emails (about GBP 0.08). Best for volume, but sender reputation, bounces and suppression lists are the operator's responsibility. Acceptable when Claude Code is the operator, but heavier to run than Mailgun.

**Mailgun** starts at USD 35 per month (about GBP 27) for 50,000 emails, with REST API, SMTP relay, and EU plus US regions. Sensible default: one Mailgun account fronts many member domains and Claude Code provisions sending domains via API.

**Postmark** hits 98.7% inbox placement in independent tests (versus 95.3% for SendGrid) and starts at USD 15 per month (about GBP 12) for 10,000 emails. Postmark enforces transactional-only policy, which keeps the shared reputation clean.

:::tip[Recommendation]
Postmark at the low tier, Mailgun when volume grows, SES only beyond 200,000 per month. A GBP 12 Postmark seat absorbed inside a GBP 30 sticker leaves GBP 18 for VPS, mailbox and PM margin.
:::

Per-vendor port 25 policy is captured in the main table for completeness. It is not an endorsement of self-hosted outbound.


## Full comparison table

| Vendor | Region | KVM VPS | Mailbox native | API coverage | Port 25 | Whitelabel | Affiliate | VPS from (GBP/mo) | Mailbox from (GBP/mo) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| IONOS | UK, EU, US | Yes, 1 vCore from USD 2 | Yes (Mail Business) | Compute and DNS solid. Mailbox provisioning via API is available but documentation thinner than OVH. PM has an active API key provisioned. | Blocked by default on cloud servers | No true whitelabel. Reseller via Agency Partner portal. | Yes, USD 5 to USD 50 per sale (about GBP 4 to GBP 39) | From GBP 2 | From GBP 1 | Attractive price, shallow mailbox API versus OVH. Big brand helps non-technical members. |
| Hostinger | Global | Yes, from USD 4.24 | Titan email add-on | Public API thin. Reseller and whitelabel programme not published at the level PM needs. | Blocked by default | No | Yes, affiliate | From GBP 4 | From GBP 1 | Low price, low automation. Acceptable as a cheap Phase 2 VPS, weak on API. |
| OVHcloud | UK, EU, US, CA, APAC | Yes, Starter VPS from GBP 4.76 | Yes, MX Plan mailbox product | Deep. Compute, DNS, email mailbox provisioning, billing all exposed. One of the most complete vendor APIs in the review. | Open by default | Partial (reseller through OVH Spirit for registrars, not true whitelabel on hosting) | Yes | From GBP 5 | From GBP 1 | Closest thing to a one-vendor answer for Phase 1. Control panel is clunky for humans, but that is fine when Claude Code drives it. |
| Scala Hosting | US, UK, EU, APAC | Yes, Entry Cloud from USD 13.45 | Yes, native via SPanel | SPanel has its own WHMCS module for provisioning accounts, domains, mailboxes. True whitelabel of the control panel itself. | Open (managed VPS) | Yes, true whitelabel SPanel | Yes | From GBP 11 | Included | Only real whitelabel on this list. US pick. Higher floor price reflects managed posture. |
| Namecheap | US, UK (via partner) | Yes, VPS Pulsar from USD 6.88 | Yes, Private Email (Open-Xchange) | Namecheap has a domains and DNS API but no documented mailbox provisioning API. Mailbox creation is manual via the billing UI. | Blocked by default on VPS | No | Yes | From GBP 6 | From GBP 1 | PM has a Namecheap API key. Good for DNS and domain registration. Not a candidate for mailbox automation. |
| A2 Hosting (now hosting.com) | US, EU | Yes | Yes, Titan-backed | Reseller plans whitelabel through cPanel plus WHMCS. No published HTTP API for the compute layer. | Blocked by default | Yes, cPanel reseller | Yes | From GBP 9 | From GBP 1 | cPanel-centric. Automation goes through WHMCS, not a native API. Workable but legacy-shaped. |
| DreamHost | US | DreamCompute uses OpenStack (not classic KVM VPS) | Yes, DreamHost email | DreamCompute has full OpenStack API. Standard VPS has no API. Email is an add-on at USD 1.67 per mailbox per month (about GBP 1.30). | Blocked by default | No | Yes | From GBP 8 | From GBP 1.30 | Pick DreamCompute if choosing DreamHost, not the standard VPS product. |
| Hostwinds | US | Yes | Yes, through cPanel | Whitelabel reseller API through WHMCS. No first-party REST API for VPS. | Open by default | Yes, true whitelabel reseller | Yes | From GBP 6 | Included in reseller plan | Port 25 open is the standout feature. Whitelabel is genuine but WHMCS-shaped. |
| Liquid Web / Nexcess | US, EU | Yes, managed VPS from USD 33 | Yes, USD 1 to USD 3 per mailbox per month | API-first managed platform with reseller features and centralised client control. Premium segment, premium pricing. | Blocked by default | Yes, reseller programme | Yes | From GBP 26 | From GBP 0.80 | Over budget for the GBP 20 to GBP 40 sticker. Worth keeping for premium tier. |
| Infomaniak | EU (Switzerland) | Yes, VPS Lite and VPS Cloud | Yes, native Mail Service | Full REST API covering domains, DNS, email, web hosting, kDrive, VPS. MCP server exists. Swiss-hosted, privacy-first. | Open by request | Reseller programme (Cloud Partner) | Yes | From GBP 4 | From GBP 1.30 | Strong Phase 1 candidate for EU. Overlooked in the mainstream conversation. |
| Hetzner | EU, US | Yes, CX22 from EUR 3.79 (about GBP 3.20) | No native mailbox product | Best-in-class REST API: compute, DNS, firewalls, load balancers, networks, volumes. No mailbox. | Blocked by default, unblocked after first paid invoice | No | No formal affiliate | From GBP 3 | N/A | Phase 2 only. Pair with Migadu or Fastmail for mail. |
| Vultr | Global | Yes, from USD 5 | No native mailbox | Full API for compute, DNS, block storage, load balancers, firewalls. Global footprint. | Blocked by default, unblock requires approval | No | Yes, affiliate | From GBP 4 | N/A | Phase 2. Pair with Fastmail or Zoho. |
| Linode / Akamai | Global | Yes, from USD 5 | No native mailbox | Full v4 API, mature SDKs. DNS Manager free. | Blocked by default for new accounts on 25, 465, 587 | No | Yes | From GBP 4 | N/A | Phase 2. Well documented API, Akamai-owned. |
| DigitalOcean | Global | Yes, Droplet from USD 6 | No native mailbox | Full API, large SDK ecosystem. Paperspace brand for GPU. | Blocked. Unblock is not granted. | No | Yes, USD 25 credit | From GBP 5 | N/A | Phase 2. Hard block on port 25 means relay is mandatory, not just advised. |
| Fastmail | Global | N/A | Yes | JMAP API for mail, calendars, contacts. Business admin console for provisioning. | N/A | No reseller programme published | Yes, referral | N/A | From GBP 3 per user | JMAP is the modern standard. Best-in-class for pairing with a Phase 2 VPS. |
| Zoho Mail | Global | N/A | Yes | RESTful provisioning API, Partner Admin Console, WHMCS provisioning module. | N/A | Yes, Partner programme with whitelabel admin | Yes | N/A | From GBP 0.80 per user | Formal reseller tier, WHMCS module documented. Closest thing to a "mailbox SaaS PM can white-label". |
| Migadu | EU (Switzerland) | N/A | Yes | REST API, Terraform provider, MCP server. Pricing by volume, unlimited addresses per domain. | N/A | No formal reseller | No formal affiliate | N/A | From GBP 16 per domain | Cheapest per-member cost at low mailbox counts if members have multiple addresses per domain. |
| MXroute | US | N/A | Yes | cPanel API. Storage-based pricing, unlimited mailboxes. | N/A | No formal reseller | Yes | N/A | From GBP 7 per account | cPanel-shaped. Cheap, but API is cPanel API, not modern REST. |
| Purelymail | US | N/A | Yes | REST-ish API, storage-based pricing. | N/A | No | No | N/A | From GBP 8 per account | Niche. Small team. Use only if extreme cost-sensitivity trumps everything. |


## Per-vendor deep dives

### OVHcloud

The strongest all-round Phase 1 candidate. OVH sells a Starter VPS (1 vCore, 2 GB RAM) from GBP 4.76 per month and an MX Plan mailbox from around GBP 1 per mailbox per month. Both products sit inside one billing account and one API surface.

The OVH API covers compute operations (create, start, stop, reboot, reinstall, snapshot), DNS zones and records, and email domain plus mailbox provisioning. The mailbox API is the key win over IONOS and Namecheap: Claude Code can create, suspend, delete and password-reset mailboxes programmatically, which is exactly the 24/7 managed-services loop PM needs.

Port 25 is open by default on OVH VPS, which distinguishes it from every other mainstream cloud vendor in this review. OVH will block the port at the network level if the IP generates abuse signals, but legitimate mail operations pass through. Even so, a Postmark or Mailgun relay is still recommended for deliverability reasons.

Whitelabel is partial. OVH does not offer a true whitelabel on the hosting control panel, but the reseller Spirit program for domain registration is established, and PM's branding can live at the customer-facing layer because Claude Code hides the OVH UI from end members.

**Blended cost at the three sticker tiers:**

- GBP 20 sticker: GBP 5 VPS plus GBP 1 mailbox plus GBP 12 Postmark relay (shared across members at scale, so the per-member slice is well under GBP 1) equals around GBP 7 cost, leaving GBP 13 margin.
- GBP 30 sticker: step up to a 2 vCore VPS at around GBP 8 per month, two mailboxes at GBP 2, shared relay. Around GBP 11 cost, GBP 19 margin.
- GBP 40 sticker: 4 GB RAM VPS at around GBP 13, three mailboxes at GBP 3, shared relay. Around GBP 17 cost, GBP 23 margin.

**Gotchas.** The OVH control panel UX is clunky, which is why this review is premised on Claude Code driving the API. OVH account suspensions have historically been heavy-handed, so PM must keep a senior human on file for escalations.

### IONOS

The obvious Phase 1 candidate for PM because PM already has an IONOS Developer API key provisioned. That head start is worth a lot in setup friction terms.

VPS entry pricing is aggressive: roughly GBP 2 per month for 1 vCore plans, GBP 3 for 2 vCore. Mailbox products (Mail Business, Mail Plus) start around GBP 1 per month per mailbox. KVM console is available in the IONOS Cloud Panel.

The IONOS API covers compute, DNS, domains, SSL, and some mail operations, but the mailbox provisioning API is less fully documented than OVH's. Claude Code can drive compute and DNS confidently; mailbox provisioning may need either Puppeteer-style UI automation against the Cloud Panel or a manual step for initial mailbox creation. This is the single structural gap compared to OVH.

Port 25 is blocked by default on IONOS cloud servers, so the Postmark or Mailgun relay is required, not optional.

Affiliate programme pays USD 5 to USD 50 per sale (roughly GBP 4 to GBP 39) depending on product, with a 60-day minimum retention. There is no true whitelabel. Agency Partner programme offers reseller shape without a branded control panel.

**Blended cost at the three tiers:**

- GBP 20 sticker: GBP 2 VPS plus GBP 1 mailbox plus relay share. Around GBP 4 cost, GBP 16 margin.
- GBP 30 sticker: GBP 5 VPS plus GBP 2 for two mailboxes plus relay. Around GBP 8 cost, GBP 22 margin.
- GBP 40 sticker: GBP 9 VPS plus GBP 3 mailboxes plus relay. Around GBP 13 cost, GBP 27 margin.

**Gotchas.** IONOS upsell pressure on customer billing is aggressive and the renewal-price jump is significant; PM would absorb this inside the sticker rather than expose members to it. The mailbox API gap means IONOS is a strong second choice, not a first choice, unless OVH is ruled out for a specific member reason.

### Scala Hosting

The only true whitelabel in the field. SPanel is Scala's own control panel, free on managed VPS, and it can be rebranded so the end-member sees "PageMotor Managed Server" rather than any Scala identifier. The WHMCS module for SPanel exposes provisioning, billing and mailbox creation via API, and email is bundled into the VPS plan rather than sold as a separate line item.

Entry-level managed Cloud VPS starts at USD 13.45 per month (about GBP 11) for 2 CPU cores and 2 GB RAM. UK data centre available. Port 25 is open on managed VPS plans because Scala controls the mail stack.

SPanel includes anti-spam (inbound and outbound), automatic SPF and DKIM record application, and catch-all failed-message logging. The SShield security layer is advertised as a managed-security feature that reduces the Claude Code workload on hardening.

**Blended cost at the three tiers:**

- GBP 20 sticker: entry managed VPS at GBP 11, mailboxes included, no separate relay needed for light mail (though Postmark relay still recommended for deliverability). Around GBP 11 cost, GBP 9 margin. This is the tight tier for Scala.
- GBP 30 sticker: Build 1 VPS at around GBP 39. Over budget. Skip this tier or stay on entry plan.
- GBP 40 sticker: Build 1 VPS at GBP 39. Around GBP 40 cost, GBP 0 margin. Scala only works at the GBP 20 to GBP 25 tier realistically.

**Gotchas.** Scala's margin structure squeezes PM at higher stickers because the VPS jumps are steep. The affiliate commission is generous on first sale but the underlying plan pricing leaves less PM margin at the GBP 30 and GBP 40 tiers than IONOS or OVH. Pick Scala for members who explicitly want the whitelabel branding or who are allergic to seeing any "OVH" or "IONOS" string in their stack.

### Hetzner plus Migadu (Phase 2)

The automation-native choice for EU members. Hetzner Cloud has the cleanest REST API in this review, period: compute, DNS, firewalls, load balancers, networks, volumes, storage boxes, and full programming examples in the official docs. CX22 (2 vCPU, 4 GB RAM, 40 GB) is EUR 3.79 per month (about GBP 3.20).

Hetzner has no native mailbox product. Pair with Migadu, which offers an API, a Terraform provider, and volume-based pricing rather than per-mailbox. At the Mini tier (EUR 19 per year, about GBP 16 per year, so around GBP 1.40 per month), Migadu allows up to 5 incoming and 3 outgoing messages per day per domain, which is too tight for anything but personal. The Standard tier at EUR 9 per month (about GBP 8) allows 200 outgoing per day per domain with unlimited addresses.

Port 25 on Hetzner is blocked by default and unblocked after the first paid invoice. For PM's purposes the relay is mandatory anyway.

**Blended cost at the three tiers:**

- GBP 20 sticker: CX22 at GBP 3 plus Migadu Mini at GBP 1.40 plus Postmark relay share. Around GBP 5 cost, GBP 15 margin.
- GBP 30 sticker: CX32 at around GBP 7 plus Migadu Standard at GBP 8 plus relay. Around GBP 16 cost, GBP 14 margin.
- GBP 40 sticker: CX42 at around GBP 14 plus Migadu Standard plus relay. Around GBP 23 cost, GBP 17 margin.

**Gotchas.** Two vendors, two logins, two bills, even though Claude Code hides this from the end member. Hetzner account trust-building delays port 25 unblock, which is moot if using a relay. Migadu daily message caps catch people out at the low tier. Hetzner has no formal affiliate programme, so PM makes margin from the sticker markup rather than vendor commissions.

### Vultr plus Fastmail (Phase 2)

The global answer. Vultr has 32 data centre locations, a mature REST API covering compute, block storage, DNS, firewalls, load balancers, and Kubernetes, and pricing from USD 5 per month (about GBP 4) for a 1 GB instance.

Pair with Fastmail for mailbox. Fastmail's JMAP API (RFC 8620) is the modern successor to IMAP for programmatic management and the cleanest mailbox API in this review. Business Basic is USD 4 per user per month (about GBP 3). Admin console supports programmatic user provisioning, storage limits, security and billing.

Zoho Mail is the alternative pairing: cheaper at USD 1 per user per month (about GBP 0.80), with a formal Partner programme including a WHMCS provisioning module, Partner Admin Console and rebrandable admin surface. The trade-off is Zoho's overall user experience, which many PM members would find busier and less calm than Fastmail.

Port 25 on Vultr is blocked by default, unblock is discretionary and has become harder to obtain in recent years. Relay is mandatory.

**Blended cost at the three tiers using Vultr plus Fastmail:**

- GBP 20 sticker: Vultr 1 GB at GBP 4 plus Fastmail Business Basic at GBP 3 plus relay share. Around GBP 7 cost, GBP 13 margin.
- GBP 30 sticker: Vultr 2 GB at GBP 9 plus Fastmail Standard at GBP 5 plus relay. Around GBP 14 cost, GBP 16 margin.
- GBP 40 sticker: Vultr 4 GB at GBP 19 plus Fastmail Professional at GBP 8 plus relay. Around GBP 27 cost, GBP 13 margin.

**Gotchas.** Vultr's port 25 unblock posture has hardened: new accounts should assume the port will never open, which makes the relay non-negotiable. Fastmail has no formal reseller programme, so PM is buying at retail and marking up inside the sticker; Zoho is the better pairing if formal reseller margin matters.


## Recommendation

### Phase 1 lead partner by region

- **UK and EU members: OVHcloud.** Port 25 open, native mailbox API, UK data centre in London, EU data centres in Roubaix and Frankfurt, deep API, GDPR-aligned billing entity. Accept the clunky panel as a non-issue because Claude Code drives the API.
- **US members: Scala Hosting.** The true whitelabel argument wins in the US market where members care more about branding ownership and less about the underlying vendor identity. SPanel plus WHMCS is a tested reseller stack. The pricing floor constrains the offering to the GBP 20 to GBP 25 sticker, which aligns with the lower end of the target range anyway.
- **Global fallback: IONOS.** When OVH or Scala is a bad fit for member-specific reasons (existing OVH account with suspension history, allergic reaction to Scala's branding, and so on), IONOS is the safe second choice. The API key is already provisioned and the brand recognition helps the non-technical buyer feel safer. Accept the shallower mailbox API as a current limitation and plan to cover the gap with UI automation or a manual provisioning step for mailbox creation.

### Phase 2 lead partners

- **EU members wanting maximum automation: Hetzner plus Migadu.** For members who care about EU data residency, Swiss email hosting, and the cleanest possible API surface, this pairing is unbeaten on engineering elegance. Accept two bills as the price of API quality.
- **Global members: Vultr plus Zoho Mail.** Zoho over Fastmail for the Phase 2 pairing, because Zoho's formal Partner programme and WHMCS provisioning module give PM a real reseller margin structure, whereas Fastmail is always a retail markup. Fastmail is the right pick only if the individual member is allergic to Zoho's UX and is willing to pay a retail price.

### Phased rollout

Start with OVHcloud as the single Phase 1 offering, because it is the only vendor in the field that genuinely satisfies all five core criteria (KVM VPS, native mailbox, deep API across both, port 25 open as a bonus, partial reseller shape). Ship the OVH-backed offering first, under the "PageMotor Managed Server" brand, with Postmark as the bundled transactional relay. Add Scala Hosting as the US-branded variant once Forum demand from US members is confirmed, and keep IONOS as the escape hatch for members who already have an OVH history that rules OVH out.

:::note
Do not attempt a multi-vendor orchestration layer on day one. The product is "calm", and calm comes from one vendor, one stack, one code path in Claude Code's management loop. Expand the vendor list only when the Phase 2 API surface is genuinely needed, and only with the two pairings named above.
:::


## End-to-end automation verification

The recommendation above rests on the claim that Claude Code can drive the full provisioning flow via vendor APIs. This section verifies that claim for both OVH and Scala, walks through a fictional member "Jane" end-to-end on each, and corrects three assumptions baked into the earlier research.

### Summary of findings

**OVHcloud.** End-to-end automation is realistic, with one documented caveat. The OVH API covers sub-account creation, service ordering with autopay, VPS provisioning with cloud-init user data, DNS zone and record operations, and MX Plan mailbox provisioning, all from one API surface. The caveat is OVH's fraud and abuse validation step, which fires on a fraction of new orders and moves the order into "Awaiting documents" status. This step requires a human upload of ID and proof of address. It is not triggered per order by design, but it can trigger. Mitigation: PM holds one parent OVH account under its own identity, provisions Jane's sub-account on top, and orders services on the parent. Validation is resolved once at account opening and never again per member.

**Scala Hosting via SPanel plus WHMCS.** End-to-end automation is realistic only within a reseller model, and only for account creation on an already-provisioned VPS. SPanel has a direct REST API for creating user accounts, mailboxes, databases, DNS zones, and SSL, fully scriptable by CC via `https://<server>/spanel/api.php`. What SPanel does not have is a VPS provisioning API. The scaling model is therefore "one PM-owned managed VPS, many Jane accounts inside it", not "one fresh VPS per Jane". WHMCS is optional, not required, if CC is the automation layer.

**Biggest single blocker across both vendors.** Neither vendor can create a brand new customer account on behalf of a third party without a human signup moment somewhere. OVH requires a human to create the parent OVH account once. Scala requires PM to buy its managed VPS once. Both are one-time setup costs absorbed by PM, not per-member friction.

### OVH flow walkthrough for Jane

**Prerequisite, done once at launch.** PM registers as an OVH customer under ElmsPark Studio Ltd. PM completes any KYC validation OVH asks for. PM contacts OVH Sales and requests the "Reseller Tag" on the account. Reseller Tag is the feature flag that enables `POST /me/subAccount`. Without it, sub-account creation returns a permissions error. PM generates an API application key, secret, and consumer key, stored in the CC secrets store.

**Per-member flow for Jane's GBP 30 PM Managed Server.**

1. **DNS pointing.** Jane already owns janes-site.com. The Managed Server offer tells her to update NS records to point at OVH's DNS or to update A and MX records once provisioning completes. CC drafts the records and emails Jane the copy-paste block.
2. **Create Jane's OVH sub-account.** `POST /me/subAccount` with Jane's email and a description. OVH returns a sub-account ID. `POST /me/subAccount/{id}/createConsumerKey` returns a consumer key scoped to Jane's sub-account. CC stores this key against Jane's PM member record.
3. **Order the VPS on the parent account.** CC uses the cart flow from OVH's `order-cart-examples`. Sequence: `POST /order/cart` to create a cart, `POST /order/cart/{cartId}/assign` to attach it to PM's account, `POST /order/cart/{cartId}/vps` to add the chosen plan code, `POST /order/cart/{cartId}/item/{itemId}/configuration` for datacenter, OS and region, `GET /order/cart/{cartId}/checkout` to preview, `POST /order/cart/{cartId}/checkout` with `autoPayWithPreferredPaymentMethod: true`. PM's stored card is charged.
4. **Cloud-init user data on boot.** The YAML installs PageMotor core, creates the www user, sets hostname, enables ufw, installs certbot, drops SSH keys, and writes the Postmark SMTP relay credentials into PM's config. Execution time from order validation to ready-SSH is 3 to 5 minutes on OVH Starter VPS. CC polls `GET /vps/{serviceName}` until `state: running`.
5. **Create DNS zone and records.** `POST /domain/zone` to create the zone (or use Namecheap API for the existing zone), `POST /domain/zone/{zoneName}/record` for each A, AAAA, MX, SPF, DKIM, DMARC, then `POST /domain/zone/{zoneName}/refresh` to publish.
6. **Provision MX Plan mailbox.** `POST /email/domain/{domain}/account` creates a mailbox with `accountName`, `password`, and `size`. DKIM activation is `POST /email/domain/{domain}/dkim/{selector}`, which returns the public selector value for publication in DNS.
7. **Configure outbound SMTP.** Postmark API: `POST /servers` to create a Postmark server for Jane, `POST /domains` to register janes-site.com as a sending domain. Postmark returns DKIM and Return-Path values. CC adds those to Jane's DNS zone.
8. **Deliver to Jane.** CC sends Jane the welcome email with site URL, PM admin login, mailbox credentials, and any DNS records she still needs to verify at her registrar.

**Human-required steps for OVH.**

- *Parent account KYC validation*: one-time PM setup, then automated.
- *Reseller Tag request*: one-time PM setup via sales contact.
- *Sub-account fraud validation on individual orders*: rare but possible. Mitigation: PM's ops loop watches for "Awaiting documents" status via the order API and pages Kenn if it fires.
- *Jane's DNS update at her own registrar*: expected friction, not a PM blocker.

### Scala Hosting flow walkthrough for Jane

**Prerequisite, done once at launch.** PM buys one Scala managed VPS under a reseller-appropriate plan, for example "Build 3" at around GBP 39 per month. PM rebrands SPanel via the admin interface: replace Scala logo with PM logo, set a custom admin URL such as `control.pagemotor.com`, set private nameservers `ns1.pagemotor-managed.com` and `ns2.pagemotor-managed.com`. PM generates an Admin API token from the SPanel admin interface. Token stored in CC secrets.

**Per-member flow for Jane's GBP 30 PM Managed Server.**

1. **DNS pointing.** Jane updates her registrar to point at PM's private nameservers. CC emails the copy-paste block.
2. **Create Jane's SPanel account.** `POST https://control.pagemotor.com/spanel/api.php` with `token`, `action=accounts/wwwacct`, and parameters for username, domain, password, quota, plan. SPanel creates the user account, sets document root, provisions FTP, and returns the account details.
3. **Provision DNS zone.** SPanel's DNS functions expose zone and record creation via the same `api.php` endpoint. Since PM owns the nameservers and the zone is auto-created on account creation, this step is often a no-op.
4. **Create mailbox.** `action=email/createemailaccount`, `accountuser=jane`, `email=hello`, `domain=janes-site.com`, `password`, `quota`. SPanel auto-applies SPF and DKIM records.
5. **Install PageMotor core.** PM pre-installs a PageMotor skeleton image into `/home/jane/public_html` during the `wwwacct` step using a post-create hook, or CC uses SPanel's file manager API to unpack the PM core tarball. Database creation via `database/createdatabase`, then CC writes credentials into PM's config.
6. **Configure outbound SMTP.** Same Postmark flow as OVH.
7. **Deliver to Jane.** CC sends the welcome email with site URL, SPanel login at `control.pagemotor.com`, mailbox credentials, and any registrar DNS records.

**Human-required steps for Scala.**

- *Initial managed VPS purchase*: one-time PM setup.
- *SPanel whitelabel configuration*: one-time PM setup via SPanel admin UI.
- *Private nameserver DNS setup*: one-time PM setup at PM's registrar.
- *Scaling beyond VPS capacity*: per-VPS setup when N members fill a given box.

### Side-by-side gap analysis

**Per-member human steps.** OVH requires zero per-member human steps inside PM's ops loop, provided the parent account avoids fraud validation flags. Scala requires zero per-member human steps within the capacity of the current VPS. Tie.

**Per-PM-setup human steps.** OVH: KYC on parent account, Reseller Tag request, API key setup. Three one-time steps. Scala: managed VPS purchase, SPanel whitelabel configuration, private nameserver DNS, API token setup. Four one-time steps. Slight edge to OVH.

**API ergonomics.** OVH's API is a mature consistent REST surface with public SDKs (python-ovh, php-ovh, Go), an OAuth2 service account flow, a public console at `api.ovh.com/console`, and published examples. SPanel's API is a single-endpoint `api.php` style with token authentication. Functional but older in feel. Clear edge to OVH.

**Operational risk profile.** OVH carries the "Awaiting documents" risk on individual orders, which is real but rare on a sub-account model with a trusted parent payment profile. Scala carries the "capacity of shared VPS" risk: if many Janes land quickly, performance can degrade and PM must split the tenant pool. OVH's risk is rare and external. Scala's risk is predictable and internal.

**Whitelabel.** Scala wins outright. SPanel supports full logo, URL, and admin interface rebrand on a PM-owned domain. OVH's control panel is never rebranded, but CC hides the panel from Jane entirely.

**Pricing at the GBP 30 sticker.** OVH blended cost is around GBP 11, margin GBP 19. Scala blended cost is the PM-owned VPS amortised across N members plus the Postmark share. At 20 members per GBP 39 VPS, cost per member is GBP 2 VPS share plus GBP 3 Postmark share, margin around GBP 25. Scala margins improve with density, OVH margins are flat per member.

**GDPR posture.** OVH is a French incumbent with EU and UK data centres, very clean. Scala is US-based with UK and EU data centres available. Both workable for UK and EU members, but OVH is the cleaner data-residency story in EU-regulated contexts.

### Corrections to the Phase 1 model

The OVH for UK/EU and Scala for US split survives the deep dive, with three corrections.

**Correction 1. OVH is a parent-plus-sub-accounts model, not one OVH account per member.** PM holds a single parent OVH account, pays for all services on it, and creates a sub-account per member to isolate visibility. This eliminates per-member KYC friction, keeps billing consolidated on PM's card, and scales cleanly. The parent account must carry the Reseller Tag, which is a one-time sales request.

**Correction 2. Scala is a reseller managed VPS model, not one fresh VPS per member.** PM holds a single managed Cloud VPS from Scala, rebrands SPanel as PageMotor Managed Server, and provisions Jane as an SPanel user account inside PM's VPS. This is the only pattern where the pricing actually works at the GBP 20 to GBP 30 sticker.

**Correction 3. WHMCS is optional, not required.** The SPanel REST API is directly drivable by CC. WHMCS only adds value if PM wants WHMCS's client portal, and it does not. Skipping WHMCS removes a licensing cost (USD 16 per month upwards) and removes a layer of indirection between CC and SPanel.

### Launch order

Ship OVH first under the parent-sub-account model, branded as "PageMotor Managed Server", Postmark relay bundled. Validate the end-to-end flow on one friendly early member before opening it to the Forum. Add Scala as the US offering only once OVH is stable and US Forum demand is confirmed. Do not run both on day one.

### Escalation path

Keep IONOS as the escape hatch for the edge case where OVH's fraud team blocks a sub-account or a specific member has a pre-existing OVH dispute. IONOS covers the compute and DNS parts cleanly, with the known mailbox-API gap covered by a one-off manual step until IONOS closes it.


## Sources

### Vendor pricing and product

- [IONOS Cloud API Overview](https://docs.ionos.com/reference/api-specification-files/api-overview)
- [IONOS VPS Hosting](https://www.ionos.co.uk/servers/vps)
- [IONOS Affiliate Program UK](https://www.ionos.co.uk/agency-partner/affiliate)
- [OVHcloud VPS UK](https://www.ovhcloud.com/en-gb/vps/cheap-vps/)
- [OVHcloud AntiSpam and port 25](https://support.us.ovhcloud.com/hc/en-us/articles/16100926574995-OVHcloud-AntiSpam-Best-practices-and-unblocking-an-IP)
- [Scala Hosting SPanel](https://www.scalahosting.com/spanel.html)
- [Scala Hosting agencies and whitelabel](https://www.scalahosting.com/hosting-for-agencies.html)
- [ScalaHosting reseller hosting](https://www.scalahosting.com/reseller-hosting.html)
- [SPanel WHMCS module](https://marketplace.whmcs.com/group/SPanel)
- [Hetzner Cloud API docs](https://docs.hetzner.cloud/)
- [Hetzner DNS API](https://dns.hetzner.com/api-docs)
- [Vultr SMTP block](https://docs.vultr.com/support/products/compute/why-is-smtp-blocked)
- [Linode API v4](https://techdocs.akamai.com/linode-api/reference/api)
- [DigitalOcean SMTP block](https://docs.digitalocean.com/support/why-is-smtp-blocked/)
- [Fastmail API Documentation](https://www.fastmail.com/dev/)
- [Zoho Mail Partner Program](https://www.zoho.com/mail/email-partnership-program.html)
- [Zoho Mail WHMCS module](https://www.zoho.com/mail/help/partnerportal/whmcs-integration.html)
- [Migadu Terraform provider](https://registry.terraform.io/providers/metio/migadu/latest/docs/resources/mailbox)
- [Hostwinds white label reseller](https://www.hostwinds.com/hosting/whitelabel)
- [Infomaniak sovereign cloud](https://www.infomaniak.com/en)
- [Postmark review and deliverability](https://hackceleration.com/postmark-review/)
- [Mailgun vs SES comparison](https://comparestacks.com/saas-software/transactional-email/vs/aws-ses-vs-mailgun/)

### OVH API walkthrough

- [First Steps with the OVHcloud APIs](https://help.ovhcloud.com/csm/en-api-getting-started-ovhcloud-api?id=kb_article_view&sysparm_article=KB0042777)
- [OVHcloud API console EU](https://eu.api.ovh.com/console/)
- [OVHcloud API console US](https://api.us.ovhcloud.com/console/)
- [Create an OVH sub-account and user account with OVH API](https://help.ovhcloud.com/csm/en-api-ovh-api-sub-account?id=kb_article_view&sysparm_article=KB0042773)
- [Managing OVHcloud service accounts via the API](https://help.ovhcloud.com/csm/en-manage-service-account?id=kb_article_view&sysparm_article=KB0059343)
- [OVH order-cart-examples GitHub](https://github.com/ovh/order-cart-examples)
- [OVH Eco server order process walkthrough](https://gist.github.com/adns44/09e71aa60658f02357e65992af6d77ef)
- [OVHcloud order validation FAQ](https://support.us.ovhcloud.com/hc/en-us/articles/29332308749587-OVHcloud-order-validation-FAQ)
- [Launching a script when an instance is created (OVH cloud-init)](https://help.ovhcloud.com/csm/en-public-cloud-compute-launch-script-at-instance-creation?id=kb_article_view&sysparm_article=KB0050912)
- [OVH python-ovh SDK](https://github.com/ovh/python-ovh)
- [OVH DKIM in DNS zone](https://help.ovhcloud.com/csm/en-dns-zone-dkim?id=kb_article_view&sysparm_article=KB0058258)

### SPanel API walkthrough

- [SPanel API basics](https://www.spanel.io/docs/article/api-functions/api-basics/)
- [SPanel accounts/wwwacct](https://www.spanel.io/docs/article/api-functions/admin-functions/accounts-functions/accounts-wwwacct/)
- [SPanel email/createemailaccount](https://www.spanel.io/docs/article/api-functions/user-functions/user-email-functions/email-createemailaccount/)
- [SPanel WHMCS module installation](https://www.spanel.io/docs/article/whmcs-provisioning-module/install-and-configure-spanel-whmcs-server-module/)
- [SPanel branding guide](https://www.scalahosting.com/blog/branding-spanel/)
- [SPanel WHMCS Server Module on WHMCS marketplace](https://marketplace.whmcs.com/product/6247-spanel-whmcs-server-module)
- [WHMCS provisioning module developer docs](https://developers.whmcs.com/provisioning-modules/)
