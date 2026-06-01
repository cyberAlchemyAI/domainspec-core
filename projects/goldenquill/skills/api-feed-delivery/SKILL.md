---
name: api-feed-delivery
description: >
  Delivers curated intelligence to subscribers via Telegram and email. Two products:
  (1) the free Regenerative Morning Coffee newsletter covering regenerative world topics
  across six sectors (no grant content), and (2) Inbox Opportunities, the paid tier that
  delivers curated grant/funding alerts matched to subscriber sectors. Manages subscriber
  data in pipeline/subscribers/subscribers.json.
metadata:
  clawdis:
    emoji: "📬"
    requires:
      bins: []
      env: ["TELEGRAM_BOT_TOKEN", "SENDGRID_API_KEY"]
---

# API Feed Delivery

## Mission

Run two complementary feeds:

1. **Regenerative Morning Coffee (FREE).** Daily editorial newsletter covering the regenerative world — essays, field notes, profiles, and what is stirring in regenerative circles. Published to the full subscriber list regardless of tier. **No grant content.**
2. **Inbox Opportunities (PAID).** Curated grants, RFAs, and funding opportunities matched to the subscriber's selected sectors, delivered to their inbox (and optionally Telegram). This is the Golden Quill core paid service for subscribers who do not own a Quill.

Track subscriber data, respect consent, and never mix editorial and funding in the same message.

## Six Sectors

All subscriber category selection and all opportunity matching is keyed to these six sectors:

1. **Future-Proof Education** — learning design, microcredentials, apprenticeship, adaptive curricula, digital literacy, ed-tech with a human center.
2. **Workforce Development for the Future** — trades, green jobs, re-skilling, cooperative workforce pipelines, transitions.
3. **Regenerative Agriculture** — soil health, perennial systems, cover cropping, agroforestry, cooperative and small-farm development (USDA VAPG, SCBGP, SARE, SBIR, REAP, AFRI, EQIP, CSP).
4. **Urban Agriculture & Soilless Systems** — controlled-environment, hydroponic, aeroponic, aquaponic, mushroom substrate systems, rooftop and vertical.
5. **Land Conservation & Community Development** — land trusts, remediation, brownfields, watershed, community development corporations, rural revitalization (NRCS RCPP, USFWS, EPA Brownfields, state DEP/DCNR).
6. **Eco-Art** — ecologically engaged art, biodesign, land art, community-art funders (NEA, state arts councils, Mellon, Ford, Warhol, Pew, Creative Capital).

## Subscriber Management

**File:** `pipeline/subscribers/subscribers.json`

**Schema:**
```json
{
  "subscribers": [
    {
      "subscriber_id": "sub_abc123def456",
      "name": "Josh Example",
      "email": "josh@goldenquill.com",
      "chat_id": "123456789",
      "newsletter_subscribed": true,
      "opportunities_subscribed": false,
      "categories": [
        "Future-Proof Education",
        "Workforce Development",
        "Regenerative Agriculture",
        "Urban & Soilless Agriculture",
        "Land & Community Development",
        "Eco-Art"
      ],
      "golden_filter_active": true,
      "quill_owner": false,
      "joined_at": "2026-01-15T10:30:00Z",
      "last_newsletter": "2026-04-12T07:00:00Z",
      "last_opportunity": "2026-04-12T07:00:00Z",
      "status": "active|paused|cancelled",
      "delivery_channels": ["telegram", "email"],
      "timezone": "America/New_York",
      "morning_send_time": "07:00"
    }
  ]
}
```

Quill owners receive Inbox Opportunities as part of their Quill subscription and do not need a separate paid feed subscription.

**Create New Subscriber:**
1. Generate `subscriber_id` as `sub_` + 24 random alphanumeric
2. Set `joined_at` to now
3. Set `status` to `active`
4. Default `newsletter_subscribed: true`, `opportunities_subscribed: false` (opt-in)
5. Store in `pipeline/subscribers/subscribers.json`

**Update Subscriber:**
- Modify `categories`, `golden_filter_active`, `delivery_channels`, `timezone`, either subscription flag as requested
- Update `last_newsletter` / `last_opportunity` after each delivery
- Set `status` to `paused` or `cancelled`

## Telegram Bot API

**Base URL:** `https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}`

**Authentication:** Use environment variable `TELEGRAM_BOT_TOKEN`

### Send Individual Opportunity Alert

**Endpoint:** `{base_url}/sendMessage`

**Method:** POST

**Payload:**
```json
{
  "chat_id": "123456789",
  "text": "<b>🔴 GRANT</b>\n<b>Title:</b> Sustainable Agriculture Innovation Fund\n<b>Agency:</b> USDA\n<b>Sector:</b> Regenerative Agriculture\n<b>Deadline:</b> 2026-05-30\n<b>Award Range:</b> $50K–$500K\n<b>Fit Score:</b> 89/100\n<a href=\"https://grants.gov/...\">View Details</a>",
  "parse_mode": "HTML",
  "disable_web_page_preview": true
}
```

**Rate Limit:** 1 message per chat per second. Queue if needed.

## Message Formatting — Opportunities

Each alert includes:
1. **Emoji Tag + Type:**
   - 🔴 GRANT
   - 🟡 FELLOWSHIP
   - 🟢 RESEARCH
   - 🟣 RESIDENCY
   - 🟠 POLICY

2. **Title** (bold, clickable)
3. **Agency / Funder**
4. **Sector** (one of the six)
5. **Deadline** (human-readable)
6. **Award range**
7. **Fit Score** if Golden Filter active (0–100)
8. **Link**

## SendGrid Email API

**Base URL:** `https://api.sendgrid.com/v3/mail/send`

**Authentication:** Bearer token from `SENDGRID_API_KEY`.

### A. Morning Coffee (Free Newsletter)

Daily send to every `newsletter_subscribed: true` subscriber.

**Content scope:**
- Editorial — essays, reported notes, profiles, practitioner voices
- Sector coverage across the six lanes (rotating focus)
- No RFAs, no grants, no funding CTAs
- Light links to Golden Quill content, events, or community pieces

**Payload (abbreviated):**
```json
{
  "personalizations": [
    {
      "to": [{"email": "josh@goldenquill.com", "name": "Josh"}],
      "subject": "Regenerative Morning Coffee — April 12, 2026"
    }
  ],
  "from": {"email": "coffee@goldenquill.com", "name": "Regenerative Morning Coffee"},
  "content": [{"type": "text/html", "value": "<html>...{newsletter_html}...</html>"}]
}
```

### B. Inbox Opportunities (Paid)

Daily send to every `opportunities_subscribed: true` **or** `quill_owner: true` subscriber.

**Build:**
1. Load subscriber record.
2. Filter opportunities (last 24h) by the subscriber's `categories` (the six sectors).
3. If `golden_filter_active`, sort by `fit_score` desc.
4. Deduplicate against prior deliveries.
5. Render opportunity email (template below).
6. Send via SendGrid; update `last_opportunity`.

### Email Template: Morning Coffee (Free)

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #222; }
    .header { background: linear-gradient(135deg, #D4AF37 0%, #FFE066 100%); padding: 20px; text-align: center; }
    .header h1 { color: #fff; margin: 0; font-size: 24px; }
    .section { padding: 15px; margin: 15px 0; border-left: 4px solid #D4AF37; background: #fafaf6; }
    .section h2 { margin: 0 0 8px 0; font-size: 16px; color: #222; }
    .footer { text-align: center; font-size: 12px; color: #999; padding-top: 20px; border-top: 1px solid #eee; margin-top: 30px; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Regenerative Morning Coffee</h1>
    <p>April 12, 2026 · A daily read on the regenerative world.</p>
  </div>
  <div style="max-width: 640px; margin: 0 auto; padding: 20px;">
    <p>Good morning, Josh.</p>
    <div class="section">
      <h2>Today's Lead Essay</h2>
      <p>{essay_html}</p>
    </div>
    <div class="section">
      <h2>From the Field</h2>
      <p>{field_notes_html}</p>
    </div>
    <div class="section">
      <h2>Around the Six</h2>
      <p>{sector_roundup_html}</p>
    </div>
    <div class="footer">
      <p><a href="https://goldenquill.com/coffee">Manage newsletter</a> · <a href="https://goldenquill.com/opportunities">Upgrade to Inbox Opportunities</a></p>
      <p>&copy; 2026 Golden Quill · FIT Farms · Pittsburgh, PA</p>
    </div>
  </div>
</body>
</html>
```

### Email Template: Inbox Opportunities (Paid)

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #222; }
    .header { background: #14171A; padding: 20px; text-align: center; }
    .header h1 { color: #D4AF37; margin: 0; font-size: 22px; letter-spacing: 0.5px; }
    .opportunity { border-left: 4px solid #D4AF37; padding: 15px; margin: 15px 0; background: #f9f9f9; }
    .fit-score { display: inline-block; background: #D4AF37; color: #fff; padding: 4px 8px; border-radius: 3px; font-weight: bold; font-size: 12px; }
    .cta-button { display: inline-block; background: #D4AF37; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin-top: 10px; font-weight: bold; }
  </style>
</head>
<body>
  <div class="header"><h1>INBOX OPPORTUNITIES — {date}</h1></div>
  <div style="max-width: 640px; margin: 0 auto; padding: 20px;">
    <!-- loop of opportunity cards keyed to the six sectors -->
  </div>
</body>
</html>
```

## Products & Pricing

### Regenerative Morning Coffee — FREE
- No subscription fee
- Daily editorial, no grant content
- Channel: email (optional Telegram digest)
- Open to anyone

### Inbox Opportunities — PAID
- Curated grant/funding opportunities delivered daily
- Scoped to the subscriber's chosen sectors (up to all six)
- Available as:
  - **Standalone subscription** — monthly fee (set by Stripe product; see `api-payments`)
  - **Included with Golden Quill ownership** — free for `quill_owner: true` subscribers for the life of their Quill agreement
- Channel: email (primary), Telegram (optional)
- Golden Filter: optional add-on that enables `fit_score` sorting

### Golden Filter (add-on, optional)
- **Effect:** Enables `fit_score` in output and sorts alerts by score (highest first)
- **Score Range:** 0–100, calculated by the Scribe/Judge seats based on RFA match
- **Implementation:** When active, sort by `fit_score` descending before send

> There is no Quill-owner discount on the newsletter. The newsletter is free to everyone; Inbox Opportunities is included with Quill ownership by default.

## Morning Delivery Logic

**Trigger:** 7:00 AM ET (or subscriber's `morning_send_time`)

**Order of operations:**
1. Build and send Morning Coffee to all `newsletter_subscribed: true` subscribers.
2. Build and send Inbox Opportunities to all `opportunities_subscribed: true` OR `quill_owner: true` subscribers.
3. Log delivery status: `{subscriber_id}: sent|failed:{reason}`
4. Update `last_newsletter` / `last_opportunity` timestamps.
5. If SendGrid fails, retry up to 3× with 5-minute backoff.

## Delivery Channel Routing

- **Telegram:** Real-time opportunity alerts (paid tier only) and optional Morning Coffee digest link.
- **Email:** Primary channel for both products.
- **WhatsApp / SMS (Future):** Same schema, gated on `WHATSAPP_BUSINESS_PHONE_ID` / `TWILIO_ACCOUNT_SID`.

## Error Handling

**Telegram API Errors:**
- `403 Forbidden` (chat_id invalid): Set subscriber status to `cancelled`, alert Josh
- `429 Too Many Requests`: Backoff 60 seconds, retry
- `500 Internal Server Error`: Retry up to 3× with 10-second backoff

**SendGrid Errors:**
- `400 Bad Request`: Log payload, alert Josh (likely template issue)
- `401 Unauthorized`: Check `SENDGRID_API_KEY`, alert Josh
- `429 Too Many Requests`: Backoff and retry next batch window

**Missing Env Variables:**
- Fail-closed: If `TELEGRAM_BOT_TOKEN` or `SENDGRID_API_KEY` missing, log error and halt.

## Validation Rules (Pre-Delivery)

1. **Subscriber Status:** Only deliver to `active`.
2. **Product Flag:** Newsletter requires `newsletter_subscribed: true`; Opportunities requires `opportunities_subscribed: true` OR `quill_owner: true`.
3. **Categories Match:** Opportunity must match at least one of the subscriber's six-sector categories.
4. **Deduplicate:** Check delivery log. Do not send same opportunity twice to same subscriber.
5. **No Cross-Contamination:** Never include opportunities in the Morning Coffee. Never include editorial-only content in Inbox Opportunities.
6. **Rate Limits:** Respect Telegram (1 msg/sec/chat) and SendGrid (600 req/min) limits.

## Operating Law Compliance

- **Rule 3 (Org Isolation):** Never send opportunities from one org to another org's subscribers.
- **Rule 2 (Test Your Own Work):** Validate subscriber list, delivery counts, rate limits before sending.
- **Editorial Integrity:** Morning Coffee is cultural writing; do not insert funding CTAs that compromise trust.

## Scheduling & Triggers

- **Morning Coffee (newsletter):** Cron, 7:00 AM ET daily (email).
- **Inbox Opportunities (paid):** Cron, 7:00 AM ET daily (email); real-time Telegram alerts for high-fit matches.
- **Weekly / Monthly digests:** Optional, per subscriber preference.
