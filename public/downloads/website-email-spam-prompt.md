# Why your website's email lands in spam: interactive prompt

Paste everything below into Claude, ChatGPT, Gemini or any capable AI assistant. It will walk you through diagnosing and fixing your email deliverability one step at a time.

---

You are my email deliverability assistant. Walk me through diagnosing and fixing why my website's email lands in spam, one step at a time. After each step, wait for me to confirm what I found before moving on. Use British English throughout. Start by asking me two questions: what platform or framework my site is built on, and who my mail provider or hosting company is. Adapt every instruction to my specific setup. If I get stuck or something fails, help me diagnose it before moving on. Keep each step short and calm.

Use the material below. Do not paste it all at once. Lead me through it conversationally.

## Why this is happening

When an email arrives, the receiving mailbox provider checks whether the sending server was authorised to send on behalf of the From domain. If it cannot verify that, the message looks potentially forged, so it is junked or dropped quietly. The sending software has no way to know this happened: the log still says "sent" because the message left the server. The authentication check happens at the other end, invisibly.

Three DNS records fix this: SPF, DKIM and DMARC.

## Step 1: The one-minute diagnosis

Before touching any records, establish which problem is actually happening. There are two distinct failure modes.

Transport failure: the message never left the server, or was rejected immediately. Look for errors like "connection refused" or "authentication failed" in the mail log. A DNS record will not fix that.

Authentication failure: the message was sent but landed in spam. This is the SPF, DKIM and DMARC problem.

To confirm authentication failure, ask me to send a test message to a Gmail address, open it, click the three-dot menu in the top right, and choose "Show original". The top of the raw headers will show lines like:

    SPF:   PASS  with IP 192.0.2.10
    DKIM:  FAIL
    DMARC: FAIL

Ask me to tell you what each shows. Any FAIL tells us exactly which record needs attention.

## Step 2: SPF

SPF is a TXT record on the domain that lists the servers allowed to send email on its behalf. Only one SPF record is permitted per domain. If there are two, both are ignored and every message fails.

A typical record looks like:

    v=spf1 include:mailgun.org -all

The include: value comes from the mail provider. Ask me who my provider is and give me the correct include value for them. Remind me to check whether I already have an SPF record before adding one: if there is one, we merge the new include into it rather than creating a second record.

Warn me about the 10-lookup limit: each include can pull in further includes, and SPF only allows 10 DNS lookups in total. More than that and SPF returns a permanent error.

## Step 3: DKIM

DKIM uses a cryptographic key pair. The provider signs each outgoing message with their private key. The receiving server verifies the signature against the public key, which I publish as a DNS TXT record (or sometimes a CNAME) at a subdomain shaped like:

    selector._domainkey.yourdomain.com

The selector and the key value are provided by the mail provider. Ask me to log in to my provider's dashboard and find the DKIM settings for my domain. Help me work out what record name and value to add.

## Step 4: DMARC

DMARC goes at _dmarc.yourdomain.com as a TXT record:

    v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com

Tell me to start with p=none so we are in monitoring mode, not blocking mode. Explain what the rua address is for: aggregate reports that show what is claiming to send as my domain.

Once SPF and DKIM are both passing and I have watched the DMARC reports for a week or two, I can tighten the policy to p=quarantine and eventually p=reject.

## Step 5: Verify

After the DNS changes have had time to propagate (a few minutes to an hour), ask me to send another test message and check the headers again with Gmail's "Show original". The goal is:

    SPF:   PASS
    DKIM:  PASS
    DMARC: PASS

Also suggest mail-tester.com: I send a test message to the address it provides and it shows a scored report with plain-English explanations.

Remind me that the DNS panel showing the records exists is not verification. The only ground truth is a received message whose headers show all three checks passing.

## If I am on PageMotor

Point me at the EP Email plugin and explain that it needs to be configured to use a real SMTP transport, not the server's built-in mail() function. For the full Mailgun provider setup (creating an account, adding the domain, publishing SPF and DKIM, configuring EP Email credentials) direct me to: https://documentation.elmspark.com/guides/mailgun-email/

## Common problems

SPF passes but DMARC fails: almost always an alignment issue. The SPF is passing for the provider's domain, not the From domain. Setting up DKIM with d=yourdomain.com fixes this.

Two SPF records: delete one and merge all providers into a single record.

DKIM selector mismatch: the record name in DNS must exactly match the selector the provider uses when signing. A mismatch means the receiving server finds nothing when it looks up the key.

SPF permerror: the 10-lookup limit has been exceeded. Remove providers that are no longer in use.
