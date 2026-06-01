---
name: api-payments
description: >
  Stripe integration for Feed subscriptions and Golden Quill hardware purchases. Supports
  tier-based recurring subscriptions (Field Notes, Radar, Full Briefing) with per-category
  add-ons and Golden Filter add-on. One-time purchases for hardware. Webhook integration
  for subscription lifecycle events. Golden Quill owner discount (30% off).
metadata:
  clawdis:
    emoji: "💳"
    requires:
      bins: []
      env: ["STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET"]
---

# API Payments

## Mission

Process subscriptions to intelligence feeds and one-time hardware purchases via Stripe. Manage product catalog, pricing, checkout flows, billing portal, and webhook events. Keep subscriber data in sync with Stripe Customer records.

## Stripe Account Setup

**Environment Variables Required:**
- `STRIPE_SECRET_KEY` — Secret API key (starts with `sk_live_` or `sk_test_`)
- `STRIPE_WEBHOOK_SECRET` — Webhook signing secret (starts with `whsec_`)

**API Base URL:** `https://api.stripe.com/v1/`

**Authentication:** Use Basic auth with `STRIPE_SECRET_KEY` as username, empty password.

## Product Catalog

### Recurring Subscriptions (Feed Intelligence)

**1. Field Notes**
- **Product ID:** `prod_field_notes` (Stripe)
- **Price ID:** `price_field_notes_monthly` (Stripe)
- **Billing:** Monthly, $6.99
- **Features:** 2 opportunities per category per month, Telegram only
- **Description:** "Curated grant opportunities. 2 per category per month."

**2. Radar**
- **Product ID:** `prod_radar`
- **Price ID:** `price_radar_monthly`
- **Billing:** Monthly, $22.00
- **Features:** 2 opportunities per category per week, Telegram + Email digest (Mon/Thu)
- **Description:** "Comprehensive grant intelligence. Weekly digest and real-time alerts."

**3. Full Briefing**
- **Product ID:** `prod_full_briefing`
- **Price ID:** `price_full_briefing_monthly`
- **Billing:** Monthly, $55.00
- **Features:** All opportunities, real-time Telegram + daily email
- **Description:** "Complete grant intelligence. Real-time alerts and daily briefing."

### Add-On Subscriptions

**4. Golden Filter**
- **Product ID:** `prod_golden_filter`
- **Price ID:** `price_golden_filter_monthly`
- **Billing:** Monthly, $15.00
- **Features:** Fit scoring, sorted by relevance
- **Description:** "Fit scoring for grant opportunities (works with any tier)."
- **Metadata:** `tier: addon`, `compatibility: all`

**5. Per-Category Add-On (future if needed)**
- **Product ID:** `prod_category_{name}`
- **Price:** $5.00/category/month
- **Example:** `prod_category_mushroom_science`, `prod_category_land_remediation`

### One-Time Purchases (Hardware)

**6. Golden Quill Standard**
- **Product ID:** `prod_golden_quill_standard`
- **Price ID:** `price_golden_quill_standard_once`
- **Billing:** One-time
- **Amount:** $8,000–$12,000 (set per quote)
- **Description:** "Golden Quill — regenerative grant intelligence hardware (M1 Mac Mini, custom case, Tilth software pre-installed)"
- **Metadata:** `hardware: true`, `tier: standard`

**7. Golden Quill Pro**
- **Product ID:** `prod_golden_quill_pro`
- **Price ID:** `price_golden_quill_pro_custom`
- **Billing:** One-time
- **Amount:** Custom (request form)
- **Description:** "Golden Quill Pro — custom spec, 32GB RAM, additional storage, priority support"
- **Metadata:** `hardware: true`, `tier: pro`, `custom_quote: true`

## Stripe API Endpoints

### Create / Update Products

**Endpoint:** `POST /v1/products` (create) or `POST /v1/products/{id}` (update)

**Payload (Create):**
```
name=Field%20Notes
type=service
description=Curated%20grant%20opportunities
metadata[recurring_tier]=field_notes
metadata[max_uses]=unlimited
```

**Payload (Update Price):**
```
POST /v1/products/{product_id}/prices
currency=usd
unit_amount=699  # Amount in cents ($6.99)
recurring[interval]=month
recurring[interval_count]=1
metadata[tier]=field_notes
```

### Create Checkout Session

**Endpoint:** `POST /v1/checkout/sessions`

**Payload (Recurring Subscription):**
```json
{
  "customer": "cus_abc123def456",
  "line_items": [
    {
      "price": "price_radar_monthly",
      "quantity": 1
    },
    {
      "price": "price_golden_filter_monthly",
      "quantity": 1
    }
  ],
  "mode": "subscription",
  "success_url": "https://goldenquill.com/subscribe/success?session_id={CHECKOUT_SESSION_ID}",
  "cancel_url": "https://goldenquill.com/subscribe/cancel",
  "subscription_data": {
    "metadata": {
      "subscriber_id": "sub_abc123def456"
    }
  }
}
```

**Payload (One-Time Hardware):**
```json
{
  "customer": "cus_abc123def456",
  "line_items": [
    {
      "price": "price_golden_quill_standard_once",
      "quantity": 1
    }
  ],
  "mode": "payment",
  "success_url": "https://goldenquill.com/hardware/success?session_id={CHECKOUT_SESSION_ID}",
  "cancel_url": "https://goldenquill.com/hardware/cancel"
}
```

**Response:**
```json
{
  "id": "cs_live_abc123def456",
  "url": "https://checkout.stripe.com/pay/cs_live_abc123def456",
  "status": "open"
}
```

**Store:** Save `session.id` and `session.url` in subscriber record or order record.

### Create Billing Portal Session

**Endpoint:** `POST /v1/billing_portal/sessions`

**Payload:**
```json
{
  "customer": "cus_abc123def456",
  "return_url": "https://goldenquill.com/account/settings"
}
```

**Response:**
```json
{
  "url": "https://billing.stripe.com/p/session/abc123def456"
}
```

**Purpose:** Redirect customer to self-service portal to change plan, update payment method, cancel subscription.

### Retrieve Subscription

**Endpoint:** `GET /v1/subscriptions/{subscription_id}`

**Response:**
```json
{
  "id": "sub_abc123def456",
  "customer": "cus_abc123def456",
  "status": "active",
  "current_period_end": 1718000000,
  "items": {
    "object": "list",
    "data": [
      {
        "price": {
          "id": "price_radar_monthly",
          "product": "prod_radar",
          "unit_amount": 2200
        }
      }
    ]
  },
  "metadata": {
    "subscriber_id": "sub_abc123def456"
  }
}
```

## Webhook Events

**Endpoint:** `POST /webhooks/stripe` (configure in Stripe Dashboard)

**Signature Verification:**
1. Get `Stripe-Signature` header
2. Verify using `STRIPE_WEBHOOK_SECRET`
3. Parse event JSON from body
4. Only process if signature valid

**Events to Listen For:**

### Event 1: checkout.session.completed

**Trigger:** Customer completes checkout (payment authorized)

**Payload:**
```json
{
  "type": "checkout.session.completed",
  "data": {
    "object": {
      "id": "cs_live_abc123def456",
      "customer": "cus_abc123def456",
      "subscription": "sub_abc123def456",
      "metadata": {
        "subscriber_id": "sub_abc123def456"
      }
    }
  }
}
```

**Action:**
1. Extract `subscription` ID
2. Extract `customer` ID
3. If subscription: `mode == "subscription"`, wait for next event
4. If payment: `mode == "payment"` (hardware), fulfill order immediately

### Event 2: customer.subscription.created

**Trigger:** Subscription started

**Payload:**
```json
{
  "type": "customer.subscription.created",
  "data": {
    "object": {
      "id": "sub_abc123def456",
      "customer": "cus_abc123def456",
      "status": "active",
      "items": {
        "data": [
          {
            "price": {
              "id": "price_radar_monthly"
            }
          }
        ]
      },
      "metadata": {
        "subscriber_id": "sub_abc123def456"
      }
    }
  }
}
```

**Action:**
1. Load subscriber from `pipeline/subscribers/subscribers.json` by `subscriber_id`
2. Update: `stripe_customer_id`, `stripe_subscription_id`, `status: active`
3. Extract tier from line items (`price_radar_monthly` → tier: `radar`)
4. Save updated subscriber record
5. Send confirmation email

### Event 3: customer.subscription.updated

**Trigger:** Subscription plan changed, payment method updated, etc.

**Payload:**
```json
{
  "type": "customer.subscription.updated",
  "data": {
    "object": {
      "id": "sub_abc123def456",
      "status": "active",
      "items": { ... }
    }
  }
}
```

**Action:**
1. Load subscriber
2. Extract new tier from line items
3. If tier changed: update `tier` field, log upgrade/downgrade
4. Save updated subscriber record
5. Send plan change confirmation email

### Event 4: customer.subscription.deleted

**Trigger:** Subscription cancelled

**Payload:**
```json
{
  "type": "customer.subscription.deleted",
  "data": {
    "object": {
      "id": "sub_abc123def456",
      "status": "canceled"
    }
  }
}
```

**Action:**
1. Load subscriber
2. Update: `status: cancelled`, `cancelled_at: now()`
3. Stop delivery (feed-delivery will skip cancelled subscribers)
4. Send cancellation confirmation email
5. Include re-subscribe link

### Event 5: charge.failed

**Trigger:** Payment failed (card declined, expired, etc.)

**Payload:**
```json
{
  "type": "charge.failed",
  "data": {
    "object": {
      "id": "ch_abc123def456",
      "customer": "cus_abc123def456",
      "failure_code": "card_declined"
    }
  }
}
```

**Action:**
1. Lookup customer
2. Log failure with reason
3. Send recovery email with link to update payment method in billing portal
4. Stripe auto-retries up to 3x; if all fail, suspend subscription

## Golden Quill Owner Discount

**Eligibility:** `quill_owner: true` in subscriber record

**Discount:** 30% off Morning Rundown (feed subscription pricing)

**Implementation via Stripe:**

1. **Coupon Setup (in Stripe Dashboard):**
   - Coupon ID: `quill_owner_30pct`
   - Discount: 30% off
   - Applies to: Product types = subscription
   - Metadata: `quill_owner: true`

2. **At Checkout:**
   - If creating checkout session for quill_owner, add coupon:
   ```json
   {
     "discounts": [
       {
         "coupon": "quill_owner_30pct"
       }
     ]
   }
   ```

3. **Pricing Examples (with 30% discount):**
   - Field Notes: $6.99 → $4.89
   - Radar: $22.00 → $15.40
   - Full Briefing: $55.00 → $38.50

4. **Verification:**
   - After subscription created, query Stripe subscription object
   - Check `discount` field for applied coupon
   - Log in subscriber record: `discount_applied: quill_owner_30pct`

## Customer Record Management

**Stripe Customer Object:**

```json
{
  "id": "cus_abc123def456",
  "email": "josh@goldenquill.com",
  "name": "Josh Example",
  "metadata": {
    "subscriber_id": "sub_abc123def456",
    "quill_owner": "true",
    "organization": "mycosymbiotics_cooperative"
  }
}
```

**Create Customer:**

**Endpoint:** `POST /v1/customers`

**Payload:**
```json
{
  "email": "josh@goldenquill.com",
  "name": "Josh Example",
  "metadata": {
    "subscriber_id": "sub_abc123def456",
    "quill_owner": "true"
  }
}
```

**Sync Logic:**
1. Before checkout, check if `stripe_customer_id` exists in subscriber record
2. If not, create customer
3. Store `stripe_customer_id` in subscriber record
4. Reuse customer ID for all future checkouts for that subscriber

## Tax & Compliance

**Tax Handling (v0.1):**
- Assume all customers are US-based
- No sales tax calculation (v0.1 is headless, no jurisdiction lookup)
- Future: Integrate Stripe Tax API for automatic calculation

**Invoice & Receipts:**
- Stripe auto-generates invoices at subscription renewal
- Invoices sent to customer email automatically
- No custom invoice generation needed in v0.1

## Error Handling

**Stripe API Errors:**

- `401 Unauthorized` — Invalid `STRIPE_SECRET_KEY`. Check env var.
- `400 Bad Request` — Malformed request. Log request body and error message.
- `429 Too Many Requests` — Rate limited. Backoff 5 seconds, retry.
- `500 Internal Server Error` — Stripe issue. Retry with exponential backoff (5s, 10s, 20s).

**Webhook Signature Invalid:**
- Log error with timestamp and signature
- Discard event (do not process)
- Alert Josh (possible security issue or webhook secret mismatch)

**Missing Environment Variables:**
- Fail-closed: Do not attempt API calls
- Log error and halt payment processing
- Alert Josh

## Validation Rules

1. **Amount Validation:** All amounts in cents (integers). Never use floats.
2. **Currency:** Always `usd` for v0.1.
3. **Customer Matching:** Always match by `subscriber_id` in metadata, not email (email can change).
4. **Subscription Status:** Only active subscriptions should be reflected in `pipeline/subscribers/subscribers.json` with `status: active`.
5. **Webhook Authenticity:** Verify signature before processing any webhook event.

## Operating Law Compliance

- **Rule 3 (Org Isolation):** Store `organization` in customer metadata. Each org's subscription data kept separate.
- **Rule 2 (Test Your Own Work):** Validate webhook signatures. Log all API calls for audit.

## Scheduling & Triggers

- **On-demand:** Customer initiates checkout → create session
- **Webhook-driven:** Stripe sends events → process subscription lifecycle
- **Scheduled:** Weekly invoice reconciliation (verify Stripe records match subscriber data)

## Roadmap (Post v0.1)

- **Stripe Tax API:** Auto-calculate sales tax by jurisdiction
- **Webhooks:** Expand to `invoice.payment_failed`, `charge.refunded` for better customer support
- **Invoicing:** Generate custom invoices with Golden Quill branding
- **Coupon Management:** Create per-org or per-campaign coupons (e.g., "promo_spring_2026")
- **Usage-Based Billing:** If features scale to per-API-call pricing (future)
