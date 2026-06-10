# Stage 6 — Design: Ad-Network Measurement Schema & Governance

- **Role:** `ad-network-measurement` · mode `design` · receipt: native-stage · **verdict: pass**

---

## 1. System-Agnostic Network Adapter Contract

The Network Adapter is a network-neutral interface decoupling autoads from any single ad network (Meta, Google, TikTok, etc.). It accepts two operations:

### 1a. Dispatch Contract
```
dispatch(
  creative_variant: {id, audience_target, asset_bundle},
  network: {name, account_id, campaign_context},
  observation_window: {start_ts, end_ts, response_delay_hours}
)
→ OutcomeEvent (source=network_api, locator=campaign_id, captured_at)
```

### 1b. Outcome Pull Contract
```
pull_outcomes(
  campaign_id: str,
  network: str,
  observation_window: {start_ts, end_ts}
)
→ RawNetworkOutcome {
  # Canonical normalized fields (all networks must emit)
  impressions: int,
  clicks: int,
  spend_usd: float,
  conversions: int,
  ctr: float = clicks/impressions,
  cpc: float = spend_usd/clicks,
  cpa: float = spend_usd/conversions,
  
  # Network-specific fields [H] (validate per network)
  network_metrics: dict  # e.g., {view_through_conversions, add_to_cart, video_plays}
}
```

**Invariant:** every OutcomeEvent carries a mandatory `source` (network_api, api_version, endpoint, captured_at) — **rule GQ-PR-L0-001 [SB]** — or is rejected at ingest.

---

## 2. KPI Families for Creative Outcomes

Adapted from ontologize's evidence-linked KPI structure **[SB DAG-AND-METRICS.md §5]**. Each carries `veracidade + evidence_refs + response_window + interpretation_limit`.

| Family | Definition | Denominator | Veracidade guard | Evidence refs |
|--------|-----------|-----------|---|---|
| **Engagement Rate** | clicks ÷ impressions | impressions (not served, not clicked) | high requires ≥1 complete window; medium: cross-network pattern | campaign_id + window_id |
| **Cost Efficiency** | spend_usd ÷ conversions | conversions (not attributed outside window) | high: network attribution model validated; low: if missing conversion data | campaign + conversion_event_id |
| **Attribution Depth** | conversions ÷ clicks | clicks in window (not post-click attributed outside) | medium: network attribution window only | click_id + conversion_id + delay_hours |
| **Creative Lift** | outcome(variant_a) − outcome(control) | control group size ≥min_sample | medium: assumes no confound (see §4); low if uncontrolled | control_campaign_id + variant_id |

**Anti-collapse [SB]:** each N3 MetricObservation reports the denominator definition (what counts as "click"? is it window-bounded?) _and_ the source-event chain (no interpolation, no silent default). A metric value stands only as a pair: `{definition, evidence_refs}`.

---

## 3. Fail-Closed Field→Authority-Class Register

Classify ad-network fields by sensitivity and routing rule. **No real credentials or PII in this seed.**

| Field | PII/Sensitivity | Authority class | Routing rule | Fail-closed gate |
|-------|---|---|---|---|
| `impressions`, `clicks`, `conversions`, `ctr` | Aggregate signal, non-identifying | internal | compute locally; shareable as aggregate KPI | pass: used in BI |
| `spend_usd`, `cpc`, `cpa` | Financial; business-sensitive | internal | store locally only; no cloud transit | fail-closed: audit log on access |
| `audience_target` (e.g., demographics, geo) | Identifies audience; PII-adjacent | private | store locally; redacted before promotion | fail-closed: reject if shared without approval |
| `network_metrics` (network-specific) | Varies by network (e.g., view-through = identity-bearing) | varies [H] | per-network policy (validate in MVP) | fail-closed: block at dispatch until classified |
| `conversion_event_id`, `click_id` | Identifies individual actions; PII-bearing | private | used only within campaign scope; never exported | fail-closed: reject if escaped campaign boundary |

**Governance flow:**
- Ingest: accept outcome with all fields.
- Measure: compute aggregate KPI from allowed fields (impressions, clicks, conversions).
- Promote: redact PII-bearing fields; only promote aggregate metrics or generalized rules (e.g., "creative variant X had higher CTR in audience segment Y" — no individual IDs).
- Share: all shared projections (KnowledgeProjection, N6) must have `privacy_scope: internal` or `shareable_redacted` stamped. **[SB PRODUCT.md: signed field→authority-class register]**.

---

## 4. Metric ≠ Authority: Enforcement Chain

**Rule GQ-PR-L0-008 [SB]:** a MetricObservation may _not_ directly promote to a KnowledgeProjection. Enforce via:

1. **Response Window:** every metric includes `observation_window = {start_ts, end_ts, response_delay_hours}`. A click on day 1 may not count conversion on day 10 if window is 3 days. _Interpretation limit._
2. **Minimum Confidence:** a metric must carry `veracidade` and `evidence_refs`:
   - `veracidade: high` requires ≥1 complete historical window + network API validation. Blocks if missing.
   - `veracidade: low` blocks promotion unless `approved_allowed_uses` carries strategic-bet override. **[SB G-honesty-node (c)]**
3. **Confound Flags:** before a metric can feed a PromotionCandidate, flag if:
   - **Selection bias:** variant audience != control audience (mark `confound_type: audience_selection`).
   - **Temporal drift:** network changed measurement model between windows (mark `confound_type: attribution_drift`).
   - **Attribution window mismatch:** campaign response window ≠ network's default window (mark `confound_type: window_mismatch`).
   - Any flagged metric with `veracidade: low` or unresolved confounds → **does not advance to N4 PromotionCandidate** (blocked by gate).

**Concrete gate flow:**
```
OutcomeEvent (source=network_api) 
  → MetricObservation {veracidade, evidence_refs, confound_flags, response_window}
  ⊘ (blocked if: low veracidade + unresolved confound + no override)
  → [only if gate passes] PromotionCandidate + contradiction_path
  → OwnerDecision {approved_allowed_uses}
  → KnowledgeProjection {privacy_scope, evidence_refs}
```

No shortcut from metric to knowledge; **metric is evidence, not truth.**

---

## Residue

- **[H]** Network-specific metric schemas (Meta pixel events, Google Ads conversions, TikTok installs) — validate against real APIs in bounded-research pass before MVP pilot. Mark each field's network default response window.
- **[H]** Confound detection rule thresholds (e.g., sample-size minimum for statistical validity) — tune in pilot.

---

**Governance posture summary:** Outcomes are sourced (mandatory provenance), metrics are graded (veracidade + evidence), confounds are flagged (bias detection), and promotion is gated (response window + confidence + owner approval). Fail-closed on PII escape and metric self-promotion.

