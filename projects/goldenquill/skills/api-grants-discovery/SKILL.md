---
name: api-grants-discovery
description: >
  Connects Scout to federal grant APIs (Grants.gov, NSF, SBIR/STTR, USAspending.gov, ProPublica).
  Discovers grant opportunities across federal, regional, and foundation sectors. Validates all URLs
  and deadlines before output. Saves results to pipeline/radar/ as JSON.
metadata:
  clawdis:
    emoji: "📡"
    requires:
      bins: []
      env: []
---

# API Grants Discovery

## Mission

Scout uses this skill to discover grant opportunities across federal databases. Every URL must resolve. Every deadline must be in the future. Output is JSON saved to `pipeline/radar/`.

## Grants.gov REST API

**Endpoint:** `https://apply07.grants.gov/grantsws/rest/opportunities/search`

**IMPORTANT:** This is a POST endpoint, not GET. Send JSON body.

**Method:** POST with `Content-Type: application/json`

**Request Body (JSON):**
```json
{
  "keyword": "specialty crops",
  "oppStatuses": "posted|forecasted",
  "rows": 25,
  "sortBy": "openDate|desc"
}
```

**Body Parameters:**
- `keyword` — search term (e.g., "agricultural innovation", "soil remediation", "mushroom")
- `cfda` — optional CFDA code (e.g., "10.170" for Specialty Crop Block Grant)
- `oppStatuses` — filter: `forecasted`, `posted`, or `forecasted|posted` (pipe-delimited)
- `sortBy` — `openDate|desc` or `closeDate|asc`

**Response:** XML. Parse these fields from each `<opportunity>`:
- `<oppId>` — Opportunity ID
- `<title>` — Grant title
- `<agencyCode>` — Funding agency code
- `<agencyName>` — Full agency name
- `<cfdaNumber>` — CFDA code
- `<synopsis>` — One-line summary
- `<description>` — Full description
- `<closingDate>` — ISO 8601 timestamp
- `<awardCeiling>` — Max award amount (cents, divide by 100)
- `<awardFloor>` — Min award amount (cents, divide by 100)
- `<eligibleApplicants>` — List of eligible entity types

**Rate Limit:** No published limit. Be respectful: 1 request per second.

**Validation:**
- Construct full URL: `https://www.grants.gov/search?applicant={applicantId}` — verify it resolves
- Parse closingDate to ISO 8601; reject if in the past
- If awardCeiling is null, use awardFloor as single value

## NSF Awards API

**Endpoint:** `https://api.nsf.gov/services/v1/awards.json`

**Query Parameters:**
- `keyword` — search term
- `dateStart` — YYYY-MM-DD (typically last 90 days)
- `dateEnd` — YYYY-MM-DD (today)
- `printFields` — comma-separated: `id,title,agency,awardAmountToDate,expDate,startDate`
- Per NSF docs, add `&offset=0&limit=25` for pagination

**Response:** JSON array. Parse each award:
- `id` — Award ID
- `title` — Award title
- `agencyCode` — NSF or partnering agency
- `awardAmountToDate` — Total award value (integer, in dollars)
- `expDate` — Expiration date ISO format
- `startDate` — Start date ISO format

**Rate Limit:** 1000 requests per hour. Add email header `X-Email: josh@goldenquill.com` (polite pool).

**Validation:**
- Construct NSF Award URL: `https://nsf.gov/awardsearch/showAward?AWD_ID={id}` — verify resolves
- expDate must be in the future

## SBIR/STTR API

**Endpoint:** `https://www.sbir.gov/api/solicitations.json`

**Query Parameters:** None required. Returns all open solicitations.

**Response:** JSON array of solicitations. Parse:
- `solicitation_number` — ID
- `title` — Solicitation title
- `agency` — Federal agency
- `release_date` — ISO 8601
- `close_date` — ISO 8601 (deadline)
- `topics` — Array of topic objects with `topic_number`, `title`, `description`

**Rate Limit:** None specified. 1 request per 2 seconds (conservative).

**Validation:**
- close_date must be in the future
- Construct URL: `https://www.sbir.gov/sbirsearch/detail/{solicitation_number}` — verify resolves

## USAspending.gov Award API

**Endpoint:** `https://api.usaspending.gov/api/v2/search/spending_by_award/`

**Method:** POST with JSON body:
```json
{
  "filters": {
    "award_type_codes": ["grant"]
  },
  "keyword": "{search_term}",
  "limit": 50,
  "offset": 0
}
```

**Response:** JSON. Parse results array, focusing on historical award patterns:
- `award_id`
- `recipient_name` — Organization that received award
- `award_amount` — Dollar value
- `award_date` — When awarded
- `awarding_agency` — Agency

**Purpose:** Understand past award patterns in a sector. Not a discovery source (these are past awards), but validates that agencies DO fund the area you're targeting.

**Rate Limit:** No published limit. Max 1 request per 2 seconds.

## ProPublica Nonprofit Explorer

**Endpoint:** `https://projects.propublica.org/nonprofits/api/v2/search.json`

**Query Parameters:**
- `q` — Organization name or EIN
- `state` — Two-letter state code (optional)

**Response:** JSON with organization records. Parse:
- `irs_classification` — Organization type
- `name` — Legal name
- `ein` — Employer ID number
- `tax_exempt_status` — e.g., "Automatically Revoked" or "Tax Exempt"
- `latest_annual_revenue` — From 990 form
- `latest_asset_amount` — From 990 form
- `years_of_990_data` — How many years of 990 data available

**Purpose:** Verify partner organizations. Detect if a proposed partner has lost tax-exempt status. Understand an org's revenue/asset scale.

**Rate Limit:** No published limit. 1 request per second (conservative).

## Output Format: JSON

Save all discoveries to `pipeline/radar/{source}_{timestamp}.json`:

```json
{
  "source_api": "grants.gov|nsf|sbir|usaspending|propublica",
  "source_name": "Full API Name",
  "opportunities": [
    {
      "id": "opportunity_id_or_eid",
      "title": "Full Grant Title",
      "agency": "Federal Agency or Funder Name",
      "deadline": "2026-06-30T23:59:59Z",
      "award_floor": 50000,
      "award_ceiling": 500000,
      "cfda_code": "10.001",
      "url": "https://grants.gov/search?applicantId=...",
      "fit_score_placeholder": null,
      "summary": "One-line summary of opportunity",
      "eligibility_notes": "Small business, nonprofits, states, etc.",
      "source_api": "grants.gov",
      "fetched_at": "2026-04-12T14:32:18Z"
    }
  ],
  "validation_passed": true,
  "validation_notes": "All URLs resolved. All deadlines in future."
}
```

## Validation Rules (Pre-Output)

Before saving to `pipeline/radar/`:

1. **URL Validation:** For every URL in output, attempt GET request. If 404 or timeout, omit the record and log error.
2. **Deadline Validation:** Parse closingDate/close_date/expDate as ISO 8601. Reject if before `now()`. Log rejections.
3. **Deduplication:** Within each API response, check for duplicate titles or IDs. Keep first occurrence, log duplicates.
4. **Null Handling:** If awardCeiling is null but awardFloor exists, use awardFloor as range floor/ceiling both. If both null, omit award_floor/award_ceiling from output.
5. **Rate Limit Compliance:** Add 1-second delay between Grants.gov requests. NSF: track call count; if > 800 in one hour, pause 60 seconds.

## Operating Law Compliance

- **Rule 1 (RFA is Truth):** This skill only queries APIs; it does not interpret funder intent. Scribe reads the RFA directly.
- **Rule 2 (Test Your Own Work):** Every URL is validated. Every deadline is checked. Validation result is logged.
- **Rule 4 (Admin-Risk Scanning):** Output format does not include admin-risk flagging—that's Logician's job. Scout reports raw data.

## Error Handling

If an API is unreachable:
- Log the error with timestamp
- Continue with next API in queue
- Save partial results to `pipeline/radar/`
- Return non-zero exit status if 3+ APIs failed

## Scheduling & Triggers

- Run on demand by Scout operator
- Optionally scheduled: 1x per day (early morning ET) to catch new postings
- After each run, validate output before handing to Radar staging
