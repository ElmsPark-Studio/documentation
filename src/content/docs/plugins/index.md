---
title: EP Suite plugins
description: "User guides for every ElmsPark plugin in the EP Suite. Setup, configuration, troubleshooting, real-world examples."
sidebar:
  order: 0
---

## What is EP Suite?

The EP Suite is the family of commercial plugins we build for PageMotor. Every plugin is designed to solve a single concrete problem well: reliable email, newsletter sending, bookings, ecommerce, GDPR compliance, passkey auth, and more.

This section of the documentation is where each plugin lives, one guide per plugin. Installation, settings, shortcodes, troubleshooting, and answers to the questions people actually ask.

Each guide follows the same shape: what the plugin does, how to install it, how to configure it, common issues, and answers to support questions we see repeatedly.

## All plugins

### Email, newsletters, messaging

- **[EP Email](/plugins/ep-email/)**. SMTP delivery, JSON-defined contact forms, delivery logging, and a developer extension API.
- **[EP Email Advanced Forms](/plugins/ep-email-advanced-forms/)**. Adds name, address, section, HTML, email confirmation, and rating field types to EP Email forms.
- **[EP Email AI Reply](/plugins/ep-email-ai-reply/)**. AI-drafted replies to form submissions — review and send.
- **[EP Email AI Triage](/plugins/ep-email-ai-triage/)**. AI-powered spam triage. Classifies every submission, blocks confirmed spam silently, holds it in quarantine for review.
- **[EP Email ElmsPark](/plugins/ep-email-elmspark/)** / **[EP SendIt](/plugins/ep-sendit/)**. Managed delivery transport drivers for EP Email via send.elmspark.com.
- **[EP Email File Uploads](/plugins/ep-email-file-uploads/)**. Drag-and-drop file upload fields for EP Email forms.
- **[EP Email Inbox](/plugins/ep-email-inbox/)**. AI-powered IMAP inbox handler with auto-reply.
- **[EP Email Quiz](/plugins/ep-email-quiz/)**. Quiz field types with scoring and grading for EP Email forms.
- **[EP Newsletter](/plugins/ep-newsletter/)**. Subscribers, lists, campaigns, autoresponders, content digests.
- **[EP Newsletter SendGrid](/plugins/ep-newsletter-sendgrid/)**. Legacy SendGrid delivery driver. For new sites use EP Newsletter Mailgun (our recommended provider) instead.
- **[EP Voice Messages](/plugins/ep-voice-messages/)**. Record-in-browser voice messages with auto-transcription.

### Ecommerce

- **[EP Affiliate](/plugins/ep-affiliate/)**. Full affiliate programme with referral tracking, tiers, payouts, coupons.
- **[EP Ecommerce](/plugins/ep-ecommerce/)**. Information product ecommerce base — memberships, downloads, licenses, bundles, subscriptions.
- **[EP Ecommerce PayPal](/plugins/ep-ecommerce-paypal/)**. PayPal payment provider.
- **[EP Ecommerce Products](/plugins/ep-ecommerce-products/)**. Styled checkout UI for EP Ecommerce.
- **[EP Ecommerce Stripe](/plugins/ep-ecommerce-stripe/)**. Stripe payment provider.
- **[EP Ecommerce Subscriptions](/plugins/ep-ecommerce-subscriptions/)**. Recurring billing with dunning, grace periods, and UK/EU compliance.
- **[EP Reviews](/plugins/ep-reviews/)**. Product reviews with star ratings, verified-purchase badges, Schema.org markup.

### Bookings, membership, courses

- **[EP Booking](/plugins/ep-booking/)**. Appointment scheduling with services, staff, availability, Stripe payments.
- **[EP Booking Zoom](/plugins/ep-booking-zoom/)**. Auto-created Zoom meetings for confirmed bookings.
- **[EP Courses](/plugins/ep-courses/)**. Course and lesson management with multilingual content and progress tracking.
- **[EP Events](/plugins/ep-events/)**. Full event platform with tickets, registrations, check-in PWA, Stripe Connect, Zoom, Schema.org, six EU languages, and depth EP Suite integration.
- **[EP Holiday Bookings](/plugins/ep-holiday-bookings/)**. Holiday packages, enquiry-first booking, deposit/balance for independent travel agents.
- **[EP Membership](/plugins/ep-membership/)**. Public registration, login, member levels, content gating.

### Content and UX

- **[EP Breadcrumbs](/plugins/ep-breadcrumbs/)**. Breadcrumb navigation with Schema.org structured data.
- **[EP Cards](/plugins/ep-cards/)**. Native card groups and grids with LLM-driven import. Thesis Focus Cards migration via add-on.
- **[EP Cards Importer](/plugins/ep-cards-importer/)**. Migration add-on for EP Cards — imports from WordPress Thesis.
- **[EP Comments](/plugins/ep-comments/)**. Comment system with moderation, threaded replies, WordPress import.
- **[EP Documents](/plugins/ep-documents/)**. Hierarchical documentation site for PageMotor. Author docs in HTML or Markdown, organise by section, draft / improve / translate with Claude, six EU languages.
- **[EP Editor](/plugins/ep-editor/)**. Visual inline page editor (work in progress).
- **[EP FAQ](/plugins/ep-faq/)**. FAQ management with accordion, search, Schema.org markup, voting.
- **[EP Gallery](/plugins/ep-gallery/)**. Album-based image gallery with drag-and-drop upload, lightbox, EXIF display.
- **[EP Gallery EXIF](/plugins/ep-gallery-exif/)**. Enhanced EXIF extraction and display (lens, GPS, shooting mode).
- **[EP Gallery Presentation](/plugins/ep-gallery-presentation/)**. Master crop, aspect-ratio frames, focal-point picker.
- **[EP Sidebar](/plugins/ep-sidebar/)**. Sidebar layout activation with manageable widget blocks.
- **[EP Testimonials](/plugins/ep-testimonials/)**. Collect and display customer testimonials with star ratings.
- **[EP YouTube](/plugins/ep-youtube/)**. GDPR-friendly YouTube embeds for PageMotor. Click-to-load thumbnails so no Google cookies fire on page load, no-cookie iframe host by default, optional thumbnail self-hosting.

### SEO, discoverability, analytics

- **[EP Analytics](/plugins/ep-analytics/)**. Privacy-respecting server-side page view analytics. No cookies, no pixel.
- **[EP Local Business](/plugins/ep-local-business/)**. Schema.org LocalBusiness emission for single-location businesses on PageMotor. Address, hours, geo, payment methods, areas served, and a coexistence handshake with EP SEO.
- **[EP Locations](/plugins/ep-locations/)**. Multi-location LocalBusiness schema for PageMotor with built-in store finder. MapLibre + MapTiler tiles, postcode search, GDPR consent gating, six EU languages.
- **[EP Redirects](/plugins/ep-redirects/)**. URL redirect manager with wildcards and 404 log.
- **[EP RSS](/plugins/ep-rss/)**. RSS 2.0 and Atom 1.0 feed generation.
- **[EP Search](/plugins/ep-search/)**. Site search with results page, form shortcode, basic analytics.
- **[EP SEO](/plugins/ep-seo/)**. Open Graph, Twitter Card, favicon, Schema.org. Per-page overrides.
- **[EP Sitemap](/plugins/ep-sitemap/)**. Dynamic XML sitemap with image references.
- **[EP Social Share](/plugins/ep-social-share/)**. Share buttons for X/Twitter, Facebook, LinkedIn, email.
- **[EP Tracking](/plugins/ep-tracking/)**. Tracked short URLs with click analytics and conversion attribution.
- **[EP Txt Files](/plugins/ep-txt-files/)**. Dynamic robots.txt and llms.txt served from admin settings.

### Privacy, security, auth

- **[EP Bunny Fonts](/plugins/ep-bunny-fonts/)**. GDPR-compliant font delivery. Replaces Google Fonts with Bunny Fonts.
- **[EP GDPR](/plugins/ep-gdpr/)**. Cookie consent, data subject requests, consent logging across EP Suite.
- **[EP Passkeys](/plugins/ep-passkeys/)**. Passwordless login via WebAuthn. *Not yet available, awaiting a PageMotor core change.*
- **[EP Password Reset](/plugins/ep-password-reset/)**. Email-based password reset for admin accounts. *Not yet available, awaiting a PageMotor core change.*

### Operations, AI, admin

- **[EP Agent](/plugins/ep-agent/)**. Claude Code CLI in your admin panel for server-side work.
- **[EP Assistant](/plugins/ep-assistant/)**. Customer-facing AI website manager. Chat interface with nine LLM providers.
- **[EP Audit Log](/plugins/ep-audit-log/)**. Activity log for content, users, and plugin events.
- **[EP Connect](/plugins/ep-connect/)**. Outbound webhooks for Zapier, Make, Slack, or any URL.
- **[EP Diagnostics](/plugins/ep-diagnostics/)**. System report for support requests.
- **[EP Flows](/plugins/ep-flows/)**. The EP Suite automation engine. Trigger, conditions, actions, authored by talking to your site over MCP instead of a drag-and-drop builder.
- **[EP Helpdesk](/plugins/ep-helpdesk/)**. Support ticket system with AI-drafted replies.
- **[EP Host Check](/plugins/ep-host-check/)**. Read-only host diagnostics. A green/amber/red report of what your hosting can and cannot do for PageMotor: file writes, outbound HTTPS and SMTP, PHP version, extensions and limits, each with a plain fix.
- **[EP Maintenance](/plugins/ep-maintenance/)**. Coming-soon and maintenance-mode overlays.
- **[EP MCP Bridge](/plugins/ep-mcp-bridge/)**. JSON-RPC API for remote PageMotor management via MCP clients.
- **[EP Provisioning](/plugins/ep-provisioning/)**. Remote provisioning receiver for automated site setup.
- **[EP Scheduled Content](/plugins/ep-scheduled-content/)**. Publish pages at a scheduled future time.
- **[EP Support](/plugins/ep-support/)**. AI support chatbot for admins. Knows every EP Suite plugin.
- **[EP WP Exporter](/plugins/ep-wp-exporter/)**. WordPress companion plugin. Install on a WordPress source site to produce a JSON snapshot for migration to PageMotor. Read-only.

## While you wait (or when in doubt)

Every plugin ZIP includes a `CLAUDE.md` capabilities file that describes its settings, methods and integration points. If you use [Claude Code](https://claude.com/claude-code) or Claude Desktop, pointing Claude at the plugin folder is a fast way to get answers alongside these guides.

For PageMotor hosting, see the [Vultr for PageMotor](/hosting/vultr/) guide.
