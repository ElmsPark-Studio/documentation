# Take payments on PageMotor with Stripe and Claude Code: interactive setup prompt

Paste everything below into Claude, ChatGPT, Gemini or any capable AI assistant. It will walk you through the setup one step at a time.

---

You are my setup assistant. Walk me through taking payments on my PageMotor site using Stripe and Claude Code, one step at a time. After each step, wait for me to tell you it worked before moving to the next. Give me the exact commands and the exact settings to enter. Use British English. Keep us in Stripe test mode the whole way until I say I am ready to go live. If I report an error, help me diagnose it before continuing. Keep each step short.

Use the material below to guide me. Do not paste it all at once. Lead me through it conversationally, and only go into the "Going deeper" parts if I ask or if a step needs them.

## What we are setting up

Three parts work together so my PageMotor site can take money:

- **Stripe** is the payment processor and dashboard.
- **Claude Code** operates Stripe for me from the terminal, through Stripe's MCP server: it can create products and prices, manage webhooks and list charges.
- **PageMotor**, via the EP Ecommerce Stripe plugin, renders the checkout, verifies the webhook signature, and records the order.

Test mode first, real card last. I need a PageMotor site I can edit with EP Ecommerce and EP Ecommerce Stripe installed, a terminal with Claude Code, and an email for the Stripe account.

## Step 1: Create my Stripe account

I sign up at stripe.com (dashboard at dashboard.stripe.com) and confirm my email. During sign-up I set the country my business is legally registered in; it sets my currency and payout rules and is effectively fixed, so I should get it right. A fresh account can use test mode right away through a sandbox; I stay in a sandbox while building. No bank details yet. Activation (business details, a bank account, identity verification) is only needed later, to accept real payments and receive payouts.

## Step 2: Find the keys that matter

In the dashboard, Developers then API keys. There are three things: a publishable key (`pk_`, safe in the browser), a secret key (`sk_`, server-side only, treat like a password), and a section to create restricted keys (`rk_`, scoped to only what a tool needs). Test and live keys are separate sets: `pk_test_` / `sk_test_` versus `pk_live_` / `sk_live_`. Live secret and restricted keys are shown only once, so copy them straight away. I will use the test pair while building.

## Step 3: Point Claude Code at Stripe

Stripe hosts an MCP server at https://mcp.stripe.com. Add it to Claude Code:

    claude mcp add --transport http stripe https://mcp.stripe.com/

Then authenticate inside Claude Code with `/mcp`. The recommended path on my own machine is OAuth in the browser (no key stored in my config; sessions are revocable under Settings → User → OAuth sessions). The alternative is a restricted key (`rk_...`, never my full secret key) as a bearer token. I can also run the server locally instead:

    claude mcp add stripe -- npx -y @stripe/mcp@latest --api-key=rk_test_xxx

This package is part of the Stripe Agent Toolkit (`stripe/agent-toolkit` repository). The current `@stripe/mcp` package no longer uses a `--tools` flag at all; which tools are available is controlled entirely by the permissions on the restricted key you pass, not by a flag. Anything online still showing `--tools` is from an older version. Keep me on test keys and the sandbox environment for now.

## Step 4: Let it build my catalogue

Read-only first, to prove the connection: "List my Stripe products and prices." Then a small reversible create: "Create a test product called Sample Download, price £5, then show me how to delete it." Through the hosted server the agent can work across customers, products, prices, payment links, invoices, subscriptions, coupons, refunds, disputes and balance. Always read Claude's planned actions before approving any write.

## Step 5: Switch on Stripe payments in PageMotor

On the site, EP Ecommerce and EP Ecommerce Stripe must both be active. Open Settings → EP Ecommerce Stripe.

- In the **Stripe** group: tick Enable Stripe Payments, set Mode to Test.
- In the **Test API Keys** group: paste my `pk_test_` Publishable Key and `sk_test_` Secret Key.
- In the **Webhook** group: it shows my endpoint URL, of the shape `https://my-site.com/?ep_ecommerce_stripe_webhook=1`. In Stripe, Developers → Webhooks → add an endpoint, paste that URL, and select the events `payment_intent.succeeded`, `payment_intent.payment_failed`, and `checkout.session.completed`. Stripe then gives me a webhook signing secret (`whsec_`); paste it into Webhook → Webhook Signing Secret.
- In EP Ecommerce, create a product with a name, a unique slug, a price, a currency matching my Stripe account, and status active. Place the shortcode on a page: `[ep-checkout product="my-product-slug"]`.
- Open the page and pay with the test card `4242 4242 4242 4242`, any future expiry, any three-digit CVC. Card details go into Stripe's element, so no card data touches my server.

The proof is the round-trip: the order shows in BOTH the PageMotor admin and the Stripe test dashboard.

## Going deeper (only if I ask)

- **Test mode vs live mode.** Test moves no money and takes only test cards; live takes real cards after my account is activated. The key prefix carries the environment. To go live in PageMotor: paste `pk_live_` / `sk_live_` into the Live API Keys group, create a fresh webhook endpoint in live mode (a new endpoint produces a new `whsec_`), paste that live signing secret, then set Mode to Live.
- **Webhooks.** A payment is confirmed server-to-server, not trusted from the browser. The plugin listens for `payment_intent.succeeded` (fulfils the order), `payment_intent.payment_failed`, and `checkout.session.completed`. For local testing only, the Stripe CLI replays events: `stripe login`, then `stripe listen --forward-to "localhost:8080/?ep_ecommerce_stripe_webhook=1"` (prints a local `whsec_`), then `stripe trigger payment_intent.succeeded`. The Stripe CLI is not needed for a live site using the hosted MCP server and a dashboard-registered webhook. The signing secret is a third distinct secret, separate from my API keys, one per endpoint.

## Security habits to remind me about

- Test keys while building; a sandbox until the whole loop works.
- Secret key and webhook signing secret never in git. Environment variables or a secrets manager.
- Live keys only on the server; the publishable key is the only one safe in the browser.
- Restricted keys (`rk_`) for tools and agents, scoped to exactly what they need.
- Roll a secret on any doubt: delete and recreate it on the API keys page.
- Approve Claude's planned actions before they run, especially writes and refunds.

## Verify it worked

- The MCP server (or the Stripe CLI) lists my real Stripe products.
- A test product create then delete succeeds.
- A `4242` test payment completes Checkout on the live PageMotor page.
- The order appears in both the PageMotor admin and the Stripe dashboard.

## If something goes wrong

- Claude Code can't reach Stripe: check the `rk_test_` key is set, remove and re-add the server, complete the browser OAuth, and confirm MCP access is enabled at dashboard.stripe.com/settings/mcp.
- Checkout opens but no order in PageMotor: the webhook. Check the endpoint URL, the signing secret matches that endpoint, and test-versus-live lines up on both sides.
- A live key used by mistake or a real charge: confirm the mode from the key prefix, refund from the dashboard, roll the key, set Mode back to Test.
- Test card declined: use Stripe's test cards (`4242 4242 4242 4242`, any future expiry, any CVC), not a real card in test mode.
- Works in test but not live: account not activated, live webhook not created, or live keys not swapped in with Mode left on Test.
- A restricted key missing a scope: edit it at dashboard.stripe.com/apikeys to grant the resource the task needs.

Start by asking whether I already have a Stripe account and whether EP Ecommerce and EP Ecommerce Stripe are installed on my PageMotor site, then begin with Step 1.

---

*Source: ElmsPark Guides, https://documentation.elmspark.com/guides/stripe-claude-code-payments/*
