---
title: WPFA methodology v1 (draft skeleton)
filed: 2026-05-18
status: DRAFT SKELETON — Cowork pre-stage for Sovereign Node LLC content review; not for buyer distribution; all numeric coefficients TBD pending SN-LLC measurement + governance signoff
publisher_at_publication: Sovereign Node LLC (cooperative; not FIT Farms LLC)
published_url_at_publication: https://sovereignnode.example/methodology/wpfa-v1 (placeholder; SN-LLC sets canonical at publication; matches registry field methodology_url)
parent_locks:
  - pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md                 # §17 v1 LOCKED 2026-05-11
  - pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md     # §2 v7.4 LOCKED 2026-05-11
audience: foundation funders, sales prospects, technical auditors, peer-review readers
governance: SN-LLC publishes the canonical version of this document at its official URL. The repo copy is a pre-stage skeleton intended to make the methodology shape concrete so that SN-LLC governance can ratify or amend, and so that Tilth deployments can reason about what the URL field in the Coefficient Registry resolves to. The repo copy is NOT signed; SN-LLC may sign or hash-anchor the canonical version separately at publication.
disclosure_posture_per_dpc_2: open coefficients + open methodology; calculation code stays proprietary; peer review deferred to v0.2 candidate (foundation-funder pressure may pull this forward — operator decision per PR #36 Q1)
---

# 0. Reader's note

This is a **draft skeleton**, not the published methodology. It states the shape, structure, and decision rationale that the Sovereign Node LLC governance + measurement team will fill with actual measured values and ratified text before publication. Every entry of the form `<TBD>` represents an open decision or a measurement that has not yet landed.

When SN-LLC publishes the canonical version, the published URL becomes the value of `methodology_url` in the signed Coefficient Registry. Tilth's buyer-facing PDF emitter (`pipeline/orchestrator/seats/wpfa/pdf_emitter.py`) links every numeric claim back to this URL.

# 1. What WPFA claims

WPFA is **Watts Per Funding Action** — the per-cycle accounting framework that proves, for every grant cycle Tilth runs, the dollar cost and the watt-hour cost of the inference path actually taken, compared to a quarterly cloud baseline. Three audiences and three claims:

1. **Operator transparency.** Per-org, per-quarter rollups inform the operator's own infrastructure decisions: which models routed where, what they cost, what they consumed.
2. **Buyer-facing accounting.** Quarterly buyer-attested receipt PDFs for board reports, grant reports, foundation reporting, and sales conversations: "In Q2 2026, [client] saved $X / Y kWh by routing Z% of grant-cycle inference to member-owned hardware."
3. **Methodology citation.** Every dollar and watt-hour in a buyer-attested receipt links to (a) a Coefficient Registry version (SHA3-512), (b) a `cycle_id`, and (c) at least one Logfire trace_id. Methodology open; calculation code proprietary.

# 2. Scope and frame

## 2.1 What WPFA measures

WPFA measures **per-cycle inference consumption**: the dollar cost and watt-hour cost of every LLM call (and every tool call that wraps an LLM call) within a single grant-application cycle, from cycle start to cycle-close marker emission per §5 v8 track-registry.

A *cycle* is the full multi-seat dispatch of a grant proposal through Tilth (Scout → Scribe → Editor → Judge → Red Team → Logician, including any retries and revisions, ending at the §5 v8 submission_mode terminal-state marker).

## 2.2 What WPFA does NOT measure

- Time-of-day variations in electricity grid carbon intensity (CO2 dimension deferred to v0.2; see §10).
- Water consumption of cloud providers' datacenters (water dimension deferred to v0.2).
- Capital expenditure amortization of the Golden Quill hardware (one-time purchase; not in per-cycle accounting).
- Operator labor cost (not in scope; would require time-tracking outside Tilth).
- Network bandwidth costs (assumed bundled into BYOK API pricing for cloud paths; assumed zero for local paths).
- Heating/cooling overhead of the Golden Quill (out of v0.1 scope; covered partially by `idle_watts_baseline_micro` measurement methodology — see §6).

## 2.3 Counterfactual

The counterfactual is **100% routing to the quarterly cloud baseline model** for every inference call the cycle performed, holding token counts constant. The baseline model is named per the active Coefficient Registry's `baseline_model_id` field. SN-LLC selects this each quarter per §3.

The actual is what Tilth's posture-driven router actually routed, per the Logfire span tree captured during the cycle.

The delta is counterfactual minus actual. Negative deltas (Tilth costlier than baseline) are computed and emitted unchanged — they surface as anti-pattern flags in the operator dashboard.

# 3. Baseline model selection (quarterly)

Per DPC-1 (LOCKED 2026-05-11), SN-LLC publishes a single named flagship reference per quarter. The selection criteria (governance-ratified by SN-LLC; this skeleton documents the recommended criteria pending ratification):

1. **Capability tier.** Frontier-class model widely available via BYOK as of the quarter start.
2. **Pricing transparency.** Publicly published per-token pricing.
3. **Identifier stability.** Canonical model ID stable for the full quarter; mid-quarter deprecations trigger emergency baseline change per §3.1.
4. **Currency stability.** Pricing denominated in USD; FX handling deferred to v0.2.

Recommended baseline for **Q3-2026 inaugural**: `<TBD-by-SN-LLC>` (likely `claude-sonnet-4-6` per scaffold placeholder; SN-LLC ratifies).

## 3.1 Emergency baseline change

Per v7.0.7 §6.1 / §17 DPC-1, SN-LLC may publish an out-of-cycle Coefficient Registry version with a different `baseline_model_id` within 7 days of a major vendor pricing or availability shock. Emergency cadence triggers the same Ed25519 signing ceremony as a regular quarterly publish.

# 4. Dollar coefficients

Per-million input tokens and per-million output tokens, in the smallest currency unit (cents at USD, per A12). For each model entry in the registry:

- `dollars_per_million_input_tokens_minor_units` = `<TBD-pricing-snapshot-at-quarter-start>`
- `dollars_per_million_output_tokens_minor_units` = `<TBD-pricing-snapshot-at-quarter-start>`

Sources for the snapshot:
- Anthropic API pricing page (frontier-class Claude models)
- Google Cloud Vertex AI pricing page (Gemini family)
- Groq pricing page (Llama family, OpenAI-OSS open-weight family)
- OpenAI pricing page (GPT family)
- Local hardware = 0 (the BYOK marginal cost is zero per inference; capex amortization is out of WPFA scope per §2.2).

`citation_url` for each entry points at the relevant vendor pricing page captured at quarter start. `measurement_date` is the date the snapshot was taken.

## 4.1 Local model dollar coefficients

For local models (`is_local: true`), `dollars_per_million_*` is **0 minor units**. The marginal dollar cost of running inference on operator-owned hardware is zero (per §2.2). This is a load-bearing claim of WPFA: WPFA does NOT amortize hardware capex into per-cycle dollar accounting. Capex is a separate operator decision visible at appliance purchase.

# 5. Watt-hour coefficients (cloud paths)

Cloud-routed inference's watt-hour cost is the energy consumed by the vendor's datacenter to serve the call. WPFA does not measure this directly (no API exposes it). Instead, SN-LLC publishes a per-million-tokens watt-hour coefficient derived from published vendor sustainability reports and peer-reviewed methodology snapshots.

For each cloud model entry:
- `watt_hours_per_million_input_tokens_micro` = `<TBD-derived-from-vendor-sustainability-reports>` micro-watt-hours
- `watt_hours_per_million_output_tokens_micro` = `<TBD-derived-from-vendor-sustainability-reports>` micro-watt-hours

Source notes:
- Vendor sustainability reports (Anthropic, Google, OpenAI, etc.) publish aggregate datacenter PUE + grid carbon intensity but do NOT publish per-token energy directly. SN-LLC's published methodology derives per-token energy from public training-cost-per-FLOP plus inference-FLOP-per-token estimates plus PUE adjustment, calibrated against any peer-reviewed estimates available.
- Where no peer-reviewed estimate exists, SN-LLC publishes a conservative upper-bound estimate and flags the entry's `measurement_methodology_url` accordingly.

## 5.1 Derivation methodology (pre-published shape)

The methodology document at `methodology_url` will carry:

1. The per-vendor calculation walk-through (with worked example for one model per vendor).
2. The peer-reviewed sources cited.
3. The sensitivity analysis (how does the coefficient change if PUE moves ±10%, if grid carbon intensity moves, etc.).
4. The "known unknowns" list (what SN-LLC explicitly does not claim to know about vendor inference energy).

# 6. Watt-hour coefficients (local paths — Stage-1 hardware)

For local-running models on operator-owned Golden Quill hardware (`is_local: true`), WPFA accounts the actual hardware power draw during inference.

Stage-1 hardware SKUs:
- `apple_m3_ultra` (Apple Mac Studio M3 Ultra)
- `amd_gx_10` (AMD GX-10 class workstation)
- `nvidia_spark` (NVIDIA DGX Spark / ASUS Ascent GX10)

For each local model entry:
- `watt_hours_per_million_input_tokens_micro` = `<TBD-from-on-hardware-measurement>` µWh
- `watt_hours_per_million_output_tokens_micro` = `<TBD-from-on-hardware-measurement>` µWh
- `idle_watts_baseline_micro` = `<TBD-from-vendor-spec-or-on-hardware-measurement>` µW
- `peak_watts_under_load_micro` = `<TBD-from-vendor-spec-or-on-hardware-measurement>` µW

## 6.1 Measurement methodology — v0.1 posture (SN-LLC-published heuristic)

At v0.1, SN-LLC publishes a heuristic estimate per hardware SKU derived from published vendor TDP (thermal design power) figures and a fixed utilization factor (~70% under load, ~5% idle). The heuristic is conservative — it tends to overestimate consumption, which means buyer-facing WPFA claims of regenerative savings are conservative-relative-to-truth, not over-claimed.

The methodology document carries:
1. Per-SKU TDP figures from vendor data sheets.
2. The utilization-factor derivation (linkable to standard data-center efficiency literature).
3. The "known unknowns" list (what SN-LLC explicitly does not claim about local inference energy at the v0.1 measurement posture).

## 6.2 Forward-binding marker — v1.x on-hardware measurement

Per §17.13 v1.x table row, **Tilth-side coefficient measurement** is the v1.x evolution: the operator's Golden Quill measures its own actual power draw during inference and reports a per-cycle deviation. F-WPFA-REGISTRY-DRIFT surfaces deviation when on-hardware measurement diverges from the SN-LLC-published heuristic by more than a configured threshold.

Until v1.x lands, all local-watt-hour coefficients come from SN-LLC's published heuristic.

# 7. Quantization and arithmetic

- **Currency.** Smallest currency unit (cents at USD). `int` (Python int promoted to bignum if needed). No float. A12 Decimal mandate per v7.0.4-M1 §6.
- **Energy.** Micro-watt-hours (10⁻⁶ Wh). `int`. No float. A12 extension per §17 v1 LOCK.
- **Rounding.** ROUND_HALF_EVEN to fixed precision before integer cast (per §17.5.3).
- **Decimal arithmetic.** Via the v7.0.4-M1 §6 explicit-context-required helper.

The methodology document will reproduce the rounding-mode + Decimal-context decisions explicitly so audit readers can replicate the per-cycle math by hand from raw token counts.

# 8. Counterfactual computation

For each `PerModelCall` in the cycle's span tree:
- counterfactual_dollars += `baseline_entry.dollars_per_million_input_tokens_minor_units * input_tokens / 1_000_000` (Decimal arithmetic, ROUND_HALF_EVEN)
- counterfactual_dollars += `baseline_entry.dollars_per_million_output_tokens_minor_units * output_tokens / 1_000_000`
- counterfactual_watt_hours_micro += same shape against the baseline's watt-hour coefficients

The baseline_entry's coefficients drive the counterfactual for the entire cycle, regardless of how individual calls actually routed. This is what "100% routed to the quarterly cloud baseline" formally means.

# 9. Delta computation

- `dollars_saved_minor_units` = counterfactual_dollars − actual_dollars
- `watt_hours_saved_micro` = counterfactual_watt_hours_micro − actual_watt_hours_micro
- `percent_dollars_saved` = (dollars_saved / counterfactual_dollars) × 10000 (basis points; ROUND_HALF_EVEN)
- `percent_watt_hours_saved` = analogous

Negative deltas (Tilth costlier than baseline) emit unchanged. Operator dashboard surfaces them prominently as anti-pattern indicators.

# 10. v0.1 vs v0.2 dimension boundary

| Dimension | v0.1 Beta | v0.2 first wave | Notes |
|---|---|---|---|
| Dollars | YES (USD only) | + multi-currency / FX | v0.2 introduces per-cycle currency declaration |
| Watt-hours (energy) | YES (micro-Wh int) | — | A12 extended |
| Water (liters) | — | YES | per-region grid mix proxies for evaporative cooling |
| CO2 (grams) | — | YES | per-region grid carbon intensity lookups |
| Peer-reviewed methodology | — | candidate | foundation-funder pressure may pull this forward |

# 11. Audit and verification

The buyer-facing PDF (`pipeline/orchestrator/seats/wpfa/templates/buyer_facing_pdf.html`) carries:
- Coefficient Registry SHA3-512 hash (matches registry signing-asset bytes)
- SN-LLC signing key id (matches the operator-pinned pubkey at white-glove)
- `methodology_url` (this document's published URL)
- Every cycle_id covered
- Every Logfire trace_id per claim
- Operator pubkey id (proves operator-attestation)

A foundation-funder auditor reading a buyer-attested receipt PDF can independently:
1. Verify the Coefficient Registry signature against SN-LLC's published pubkey
2. Recompute the per-cycle delta from raw token counts + coefficient table
3. Follow `methodology_url` for full derivation rationale
4. Cross-check `cycle_id` and trace_ids against the operator's Logfire export

This is the auditability claim that distinguishes WPFA from generic green-marketing claims.

# 12. Open methodology questions (governance backlog)

These are the methodology questions the v1.0 published version will resolve. SN-LLC may add or fold any of these before publication.

- M-1: Final baseline model selection for Q3-2026 inaugural (recommended `claude-sonnet-4-6`; SN-LLC ratifies).
- M-2: Should SN-LLC publish a "high-confidence" subset of coefficients with peer-review citation and flag the rest as "operator-tunable heuristic"? Default no (single tier at v0.1; uniform methodology citation).
- M-3: Should multi-currency at v0.2 use day-of-cycle FX or quarter-end FX? Default day-of-cycle.
- M-4: Should peer-reviewed methodology snapshot at v0.2 be embargoed during cycle 1 of the quarter to allow operator pre-warning? Default no (publish atomically).
- M-5: When local on-hardware measurement lands at v1.x, what F-WPFA-REGISTRY-DRIFT threshold triggers advisory vs HIGH? Default ±10% advisory, ±30% HIGH.
- M-6: Should SN-LLC publish per-region grid carbon intensity coefficients at v0.2, or fall back to nation-average until per-region data is high-quality? Default nation-average at v0.2 launch; per-region as v0.2 second wave.

# 13. Publication readiness checklist (SN-LLC governance prerequisite)

Before SN-LLC publishes the canonical methodology at `methodology_url` and signs the inaugural Coefficient Registry:

- [ ] Baseline model selection ratified (M-1)
- [ ] Per-vendor dollar snapshot captured for quarter start
- [ ] Per-vendor watt-hour derivation walk-through authored
- [ ] Stage-1 hardware SKU TDP + utilization heuristic documented
- [ ] Sensitivity analysis authored (PUE ±10%, grid carbon ±, etc.)
- [ ] "Known unknowns" list authored
- [ ] M-2 through M-6 default answers ratified or overridden
- [ ] Canonical URL stood up (typically `https://sovereignnode.example/methodology/wpfa-v1`)
- [ ] Operator-side pinned-pubkey ceremony procedure verified against this draft (`docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md`)
- [ ] SN-LLC signing ceremony executed per `docs/wpfa_sn_llc_signing_ceremony_runbook_2026-05-18.md`
- [ ] Inaugural Q3-2026 registry signed, published, and pin-roundtrip tested at one paid Beta deployment

# 14. Related files

- `docs/wpfa_status.md` — §17 status surface
- `docs/wpfa_section_17_next_dispatch_brief_2026-05-18.md` — scoping brief
- `docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md` — operator pubkey-pin ceremony
- `docs/wpfa_sn_llc_signing_ceremony_runbook_2026-05-18.md` — SN-LLC signing ceremony
- `docs/wpfa_dress_rehearsal_runbook_2026-05-18.md` — operator-only synthetic-registry dress rehearsal
- `vault_shared/wpfa/coefficient_registry/draft_Q3_2026_unsigned.yaml` — exact shape SN-LLC will publish
- `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md` — §17 v1 blueprint
- `pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md` — Coefficient Registry signed-asset class
