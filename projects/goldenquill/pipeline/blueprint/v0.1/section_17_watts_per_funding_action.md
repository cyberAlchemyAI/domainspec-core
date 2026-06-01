---
title: §17 v1 — Watts Per Funding Action (WPFA) — Cycle-close accounting blueprint
filed: 2026-05-11
operator: Josh Inklovich
status: LOCKED 2026-05-11 — compound paired-commit (sibling 1/4) with §4 v2.x.z F-WPFA-* amendment + Coefficient Registry signed-asset amendment (§2 v7.4) + §0.5 v19 paired-commit at the same `lock_timestamp_utc` per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor (audit trail at `pipeline/validation/wpfa_thesis_2026-05-10/`). Cycle 2 NEW probes folded-in at LOCK per row-170 transparent disposition pattern. Tenth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor.
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                                          # v7 LOCKED 2026-04-19 A1-A12
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md                                   # v7.0.4-M1 LOCKED 2026-05-10 row 190 — A12 Decimal mandate three-layer ban-float
  - pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md                                     # v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intel signed-asset publication precedent
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                                     # v7.0.7 LOCKED 2026-05-10 row 180 — §6.1 SN-LLC router-template Ed25519 signing (load-bearing precedent for Coefficient Registry trust mechanism)
  - pipeline/blueprint/v0.1/section_02_v7_2_amendment.md                                            # §2 v7.2 LOCKED 2026-05-10 row 186 — operational-data sub-kinds + SUB_KIND_REGISTRY pattern (cycle_receipt sub-kind extends this)
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                                            # §4 v2.x LOCKED 2026-05-10 rows 193/194 — F-CLASS-* dormant primitives + format pattern this section mirrors for F-WPFA-* family
  - pipeline/blueprint/v0.1/section_05_v8_amendment.md                                              # §5 v8 LOCKED 2026-05-10 rows 188/189 — track-registry cycle-close marker (consumer for WPFA emission trigger)
  - pipeline/blueprint/v0.1/section_15_archivist.md                                                  # §15 v1 SPEC LOCKED 2026-05-10 rows 191/192 — sibling-not-nested precedent (Archivist v1.x quarterly digest MAY compose WPFA rollups; does NOT consume per-cycle receipts)
companion_amendments: [section_04_v2_x_z_wpfa_amendment.md, section_02_v7_4_coefficient_registry_amendment.md, section_00_5_section_17_wpfa_amendment.md]
compound_lock_with: section_04_v2_x_z_wpfa_amendment.md + section_02_v7_4_coefficient_registry_amendment.md + section_00_5_section_17_wpfa_amendment.md
sibling_artifact: pipeline/research/reflection_packet_grounding/findings_2026-05-10.md → forthcoming Reflection Packet design (v0.2 horizon per operator default). Sibling-not-nested pattern: zero shared output, zero shared consumer, zero shared schema. Shared input substrate: cycle-close Logfire span tree only.
authority: orchestrator dispatch 2026-05-10 — "Tilth doesn't just route to local, it proves it routed to local, and proves the savings, with auditable methodology."
---

# §17.0 — Purpose

Golden Quill ships a per-cycle, operator-attestable, buyer-auditable telemetry artifact — the `CycleReceipt` — that proves what Tilth's inference path actually consumed (dollars + watt-hours) versus what 100%-routing to a quarterly cloud baseline would have consumed. Three load-bearing functions:

1. **Operator transparency** — per-org, per-quarter rollups for the operator's own infrastructure decisions.
2. **Buyer-facing accounting** — quarterly receipt PDF for board reports, grant reports, sales conversations.
3. **Sales lever** — converts "we have a 128 GB box on your desk" into "and here's the receipt that proves the dividend."

Every numeric claim links to (a) a SN-LLC-signed Coefficient Registry version, (b) a `cycle_id`, and (c) at least one Logfire trace_id. Methodology is open; calculation code is proprietary.

**Sibling-not-nested with Reflection Packet.** Both emit at cycle close from the same span tree. Both are independent Pydantic BaseModels. They share zero output, zero downstream consumer, zero schema. Coupling between them is structurally forbidden at write path (F-WPFA-CROSS-ORG-LEAK + F-PACKET-* family sibling discipline; documentary edit per `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md` Path B default).

# §17.1 — Architecture posture

**Always-local seat.** Cycle Accountant is always-local per v7.0.7 routing posture — the input substrate is the Logfire span tree, which carries Confidential trace content. No LLM-routed sub-agents inside Cycle Accountant; it is a deterministic Python module wrapping the §2 v7.2 vault write intent.

**Deterministic emission.** Same Logfire export + same Coefficient Registry version → byte-identical canonical-JSON output. Decimal arithmetic via the explicit-context-required helper per v7.0.4-M1 §6; ROUND_HALF_EVEN rounding to fixed precision before integer cast.

**Sub-kind extension.** A new `cycle_receipt` sub-kind extends `SUB_KIND_REGISTRY` per §2 v7.2 §12.1 pattern; vault subtree at `orgs/<org_slug>/vault/operational/cycle_receipts/`; `write-if-absent` mode; canonical-JSON round-trip; `__post_init__` invariant validation.

**A12 Decimal mandate extended to energy.** This section extends A12 from "money only" to "money AND energy quantities" — watt-hours-saved is load-bearing for the buyer-facing accounting claim; float rounding errors would corrupt audit trails. AST-lint R3-equivalent rule extends to ban `float` on field-name patterns matching `(_minor_units|_micro|_saved)$`.

# §17.2 — Section-number rationale (binding decision)

WPFA occupies §17. §16 is reserved for the forthcoming Reflection Packet design (sibling artifact; research findings 2026-05-10). Topical cluster: §15 Archivist + §16 Reflection Packet are Tilth-internal between-cycle preservation surfaces; §17 WPFA is operator-and-buyer-facing accounting. Placing WPFA after the Tilth-internal cluster signals the audience boundary. Sub-section proliferation room reserved at §16; §17 stays clean as the WPFA root.

Rejected: §16 for WPFA (Reflection Packet research already implies §16 occupancy); §17.1 as sub-section of unified cycle-close-emission §17 (independent failure-code families, independent consumers, independent classification postures).

# §17.3 — CycleReceipt Pydantic shape

Following the §2 v7.2 sub-kind convention exactly. Module at `pipeline/orchestrator/seats/wpfa/cycle_accountant.py`; schema at `pipeline/vault/sub_kinds/cycle_receipts.py`; tests at `tests/seats/wpfa/` + `tests/vault/sub_kinds/test_cycle_receipts.py`.

## §17.3.1 — Top-level shape

```python
@dataclass(frozen=True, kw_only=True)
class CycleReceipt:
    # Identity + provenance
    cycle_id: str                                       # opaque caller-minted ID; matches filename {cycle_id}.json
    org_slug: str                                       # one of orgs/<slug>/ identifiers — Law 3 binding
    schema_version: str                                 # semver "MAJOR.MINOR.PATCH"; major-version bump = tolerant-reader fallback at consumer (v0.1 ships "1.0.0")
    classification_register_version: str                # SHA3-512 hex hash of operator-signed classification register at cycle start

    # Emission context
    emitted_at: str                                     # UTC ISO-8601 'Z'
    baseline_model_id: str                              # quarter's SN-LLC-published flagship reference, e.g., "claude-sonnet-4-6"
    baseline_quarter: str                               # quarter tag, e.g., "Q3-2026"
    coefficients_registry_version: str                  # SHA3-512 hex hash of SN-LLC-signed Coefficient Registry at emission time
    coefficients_registry_signature_ed25519: str        # hex-encoded Ed25519 signature over canonical registry; verified PRE-emission

    # Active dimensions (forward-compat; v0.1 = dollars + energy only)
    dimensions_active: tuple[str, ...]                  # closed set {"dollars","energy"} at v0.1; {"dollars","energy","water","co2"} at v0.2

    # Actual consumption (this cycle)
    actual: CycleReceiptDimensionTotals
    actual_per_model: tuple[PerModelCall, ...]

    # Counterfactual (100% routed to quarterly baseline)
    counterfactual: CycleReceiptDimensionTotals

    # Regenerative-savings delta
    delta: CycleReceiptDelta

    # Provenance — every quantitative claim must trace
    span_provenance: SpanProvenance

    # Operator attestation — required for buyer-external use, optional for internal-only
    signed_by_operator_ed25519: str | None
```

## §17.3.2 — Nested shapes

```python
@dataclass(frozen=True, kw_only=True)
class CycleReceiptDimensionTotals:
    dollars_total_minor_units: int                      # smallest currency unit (e.g., cents); A12 per v7.0.4-M1 §6
    currency: str                                       # ISO-4217 alpha-3
    watt_hours_total_micro: int                         # micro-watt-hours (10^-6 Wh); A12 extension
    water_liters_micro: int | None                      # v0.2 forward-compat; None at v0.1
    co2_grams_micro: int | None                         # v0.2 forward-compat; None at v0.1


@dataclass(frozen=True, kw_only=True)
class PerModelCall:
    model_id: str                                       # canonical model identifier (matches Logfire span model_id)
    is_local: bool
    hardware_sku: str | None                            # "apple_m3_ultra" | "amd_gx_10" | "nvidia_spark" | None for cloud
    input_tokens: int
    output_tokens: int
    dollars_minor_units: int
    watt_hours_micro: int
    span_ids: tuple[str, ...]


@dataclass(frozen=True, kw_only=True)
class CycleReceiptDelta:
    dollars_saved_minor_units: int                      # counterfactual - actual; may be negative (anti-pattern flag)
    watt_hours_saved_micro: int
    percent_dollars_saved: int                          # basis points (10000 = 100%); ROUND_HALF_EVEN
    percent_watt_hours_saved: int
    water_liters_saved_micro: int | None                # v0.2
    co2_grams_saved_micro: int | None                   # v0.2


@dataclass(frozen=True, kw_only=True)
class SpanProvenance:
    trace_ids: tuple[str, ...]                          # one or more Logfire trace IDs covered by this receipt
    logfire_export_uri: str | None                      # optional offline-audit pointer
    cycle_close_marker_span_id: str                     # span ID for §5 v8 track-registry cycle-close marker
    per_claim_span_ids: dict[str, tuple[str, ...]]      # claim_key → tuple of span_ids backing it
```

## §17.3.3 — Sub-kind registry row (extends §2.12 SUB_KIND_REGISTRY)

```python
"cycle_receipt": SubKindDescriptor(
    intent="operational-cycle-receipt-write",
    vault_subtree="operational/cycle_receipts/",
    record_class=CycleReceipt,
    to_canonical_bytes=cycle_receipts.to_canonical_bytes,
    from_canonical_bytes=cycle_receipts.from_canonical_bytes,
    record_id_for=cycle_receipts.record_id_for,
    severity_default="YELLOW",
    severity_for=lambda record: "RED" if record.signed_by_operator_ed25519 is not None else "YELLOW",
)
```

Buyer-facing (signed) receipts elevate to RED severity in the admin-risk surface so operator attention is non-optional before the artifact ships externally.

## §17.3.4 — Invariants (`__post_init__` — fail-closed at write AND at decode round-trip)

1. `cycle_id` matches `^[A-Za-z0-9_-]{1,128}$` (Cycle 2 RT-C2-05 FIX-IN-PLACE — path-traversal defense; reject `../`, `..\\`, leading `/`, embedded dots, and any other special characters). Filename derivation is `<cycle_id>.json`.
2. `org_slug` non-empty; resolves to an existing `orgs/<slug>/` subtree at PRE-write time.
3. `schema_version` matches `^\d+\.\d+\.\d+$` (semver).
4. `classification_register_version` is a 128-hex-char SHA3-512 digest.
5. `emitted_at` matches `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$` (UTC 'Z').
6. `baseline_quarter` matches `^Q[1-4]-\d{4}$`.
7. `coefficients_registry_version` is 128-hex-char SHA3-512; matches the registry currently on disk at PRE-write.
8. `coefficients_registry_signature_ed25519` hex; PRE-write Ed25519 verify against white-glove-pinned SN-LLC pubkey MUST pass.
9. `dimensions_active` is a tuple of strings drawn from the closed set `{"dollars","energy","water","co2"}`; v0.1 MUST equal `("dollars","energy")`; any other value fails `F-WPFA-DIMENSION-UNSUPPORTED`.
10. `actual.currency == counterfactual.currency` (no mixed-currency receipts).
11. Every `PerModelCall.model_id` resolves to an entry in the loaded Coefficient Registry (else `F-WPFA-MODEL-COEFFICIENT-MISSING`).
12. `baseline_model_id` MUST equal the active registry's `baseline_model_id` field (else `F-WPFA-COUNTERFACTUAL-INFLATION`).
13. `delta.dollars_saved_minor_units == counterfactual.dollars_total_minor_units - actual.dollars_total_minor_units` (re-validated at decode); same identity for energy.
14. Every claim key in `span_provenance.per_claim_span_ids` MUST be a non-empty tuple of resolvable span_ids (else `F-WPFA-SPAN-PROVENANCE-MISSING`).
15. If `signed_by_operator_ed25519` is non-None, MUST verify against the white-glove-pinned operator pubkey over the canonical-JSON-encoded receipt (excluding the signature field itself); if None, the receipt is internal-only and MUST NOT be exported to buyer-facing PDF (else `F-WPFA-OPERATOR-SIGNATURE-MISSING`).
16. Per-model rows in `actual_per_model`: aggregate sum of `dollars_minor_units` MUST equal `actual.dollars_total_minor_units` (re-validated at decode); same identity for `watt_hours_micro` against `watt_hours_total_micro`.
17. Forward-compat: if `schema_version` major-version is higher than consuming code's known max, consumer falls through to tolerant-reader path and surfaces a `F-WPFA-SCHEMA-DRIFT` advisory (informational at consumer side; not fail-closed at v0.1).

## §17.3.5 — Energy quantization decision (LOCKED)

Energy is quantized at **micro-watt-hours (10^-6 Wh)** as integer. Rationale: a single LLM call may produce ~0.1 Wh; per-token energy is ~10 µWh; micro-Wh handles per-token granularity without floats. Milli-Wh was rejected as losing per-token resolution.

**Overflow bound (Cycle 1 RT-08 disposition).** Signed 64-bit micro-watt-hours wraps at ~9.2e18 µWh = 9.2 TWh cumulative. At v0.1 single-client (A1) this is impossible at any realistic horizon. Forward-binding marker for **Stage-2+ fleet-aggregate amendment**: explicit overflow check at write path + promotion to uint128 (or BigInteger string field) when aggregate horizon approaches the bound. v0.1 ships with the implicit Python int (no fixed-width wraparound) — overflow surfaces only at JSON serialization for tooling consumers that assume int64.

# §17.4 — Coefficient Registry — read interface (full schema in `section_02_v7_4_coefficient_registry_amendment.md`)

WPFA Cycle Accountant reads the Coefficient Registry but does not author or sign it. SN-LLC publishes; operator pins SN-LLC pubkey at white-glove onboarding; the registry is loaded via `coefficient_registry.load_active()`. Trust mechanism mirrors v7.0.7 §6.1 router-template Ed25519 signing byte-for-byte.

Cycle Accountant interactions with the registry:
- **PRE-emission load** — `load_active()` reads `vault_shared/wpfa/coefficient_registry/active.yaml` + verifies signature against the pinned pubkey; failure fails-closed via `F-WPFA-COEFFICIENT-SIGNATURE-INVALID`.
- **Per-model lookup** — for each `model_id` in the cycle's span tree, resolves to a `CoefficientEntry`; absent → `F-WPFA-MODEL-COEFFICIENT-MISSING`.
- **Baseline binding** — emission MUST use the registry's `baseline_model_id` as the counterfactual model; mismatch → `F-WPFA-COUNTERFACTUAL-INFLATION`.

# §17.5 — Cycle Accountant module

Module: `pipeline/orchestrator/seats/wpfa/cycle_accountant.py`. Always-local. Deterministic.

## §17.5.1 — Input shape

```python
@dataclass(frozen=True, kw_only=True)
class CycleAccountantInput:
    run_id: str
    cycle_id: str
    org_slug: str
    cycle_close_marker_span_id: str                     # span ID from §5 v8 dispatcher at submission_mode terminal state
    logfire_export_path: str                            # local path to Logfire span tree export
    classification_register_version: str                # SHA3-512 of operator-signed register at cycle start
    coefficient_registry_path: str                      # defaults vault_shared/wpfa/coefficient_registry/active.yaml
    dimensions_requested: tuple[str, ...]               # defaults ("dollars","energy") at v0.1
    operator_attestation_requested: bool                # if True, prompt operator for Ed25519 signing
    invoked_at_utc: str                                 # ISO-8601 'Z'
```

## §17.5.2 — Outputs

- `orgs/<org_slug>/vault/operational/cycle_receipts/<cycle_id>.json` — CycleReceipt as canonical JSON.
- (if `operator_attestation_requested == True` AND operator signs) `orgs/<org_slug>/wpfa_artifacts/<cycle_id>.pdf` — buyer-facing PDF per §17.7.
- `pipeline/institutional_memory/wpfa_state/<run_id>.yaml` — Rule 1 Save State Always (success + failure paths).
- `pipeline/validation/wpfa_rejects/<run_id>/` — gate-fail audit trail per §15 precedent.

## §17.5.3 — Determinism mandate (binding)

Same `logfire_export_path` content + same `coefficient_registry_path` content → byte-identical canonical-JSON output. Decimal arithmetic via the v7.0.4-M1 §6 explicit-context-required helper; ROUND_HALF_EVEN rounding to fixed precision before integer cast. Regression test at `tests/seats/wpfa/test_cycle_accountant.py::test_deterministic_re_run_byte_identity` enforces.

**Cycle 2 RT-C2-03 fold-in (Logfire export canonicalization).** Before any aggregation reads from the Logfire export, the Cycle Accountant MUST canonicalize the export bytes: `json.loads(...)` followed by re-serialization with `sort_keys=True, separators=(",", ":")`. This forecloses determinism breaks introduced by future Logfire versions emitting maps with non-deterministic key ordering. The canonicalization step is part of the determinism invariant — non-canonical input → fail-closed with `F-WPFA-SCHEMA-INVALID.schema_drift_advisory`. Implementation lands at WPFA Code phase.

## §17.5.4 — `compose_receipt` callable (DI seam)

```python
def compose_receipt(
    inp: CycleAccountantInput,
    *,
    spans: Iterable[SpanRecord],
    registry: CoefficientRegistry,
    classification_register_version: str,
    operator_signer: OperatorSigner | None = None,
) -> CycleReceipt:
    """Deterministic composition. No I/O — caller injects spans + registry.

    Per-call cost: O(N spans + M models). No retries; gate failures raise
    explicit Logician-class exceptions that the orchestrator surface catches.
    """
```

Caller is `pipeline/orchestrator/seats/wpfa/cycle_accountant.py::run_cycle_accountant_pipeline` (the §5 v8 dispatcher hook). Tests inject spans + registry deterministically.

# §17.6 — F-WPFA-* failure-code family (registration in `section_04_v2_x_z_wpfa_amendment.md`)

Twelve F-WPFA-* failure codes. Module decomposition default per OQ-4 = collapse the coefficient-registry-validation triplet (3 codes → 1 module); rest one-module-per-code (final: 10 modules realizing 12 codes).

Reference table — full Cedar/Python predicate signatures in §4 v2.x.z amendment. **Cross-reference Path B (per `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md`):** `F-WPFA-SPAN-PROVENANCE-MISSING` is a sibling pattern to a forthcoming `F-PACKET-SPAN-PROVENANCE-MISSING` (Reflection Packet artifact, scope deferred). Sub-tags `.no_trace_id`, `.trace_id_unresolvable_in_logfire`, `.claim_key_unmapped`.

| Code | Tier | Severity |
|---|---|---|
| `F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED` | PRE-load | P0 |
| `F-WPFA-COEFFICIENT-SIGNATURE-INVALID` | PRE-load | P0 |
| `F-WPFA-COEFFICIENT-ROLLBACK-INVALID` | PRE-load | HIGH |
| `F-WPFA-MODEL-COEFFICIENT-MISSING` | PRE-emission | HIGH |
| `F-WPFA-BASELINE-MISSING` | PRE-emission | HIGH |
| `F-WPFA-SPAN-PROVENANCE-MISSING` | PRE-emission | HIGH |
| `F-WPFA-COUNTERFACTUAL-INFLATION` | PRE-emission | P0 |
| `F-WPFA-OPERATOR-SIGNATURE-MISSING` | PRE-PDF-emit | HIGH |
| `F-WPFA-DIMENSION-UNSUPPORTED` | PRE-emission | HIGH |
| `F-WPFA-REGISTRY-DRIFT` | POST-load (advisory) | MEDIUM |
| `F-WPFA-SCHEMA-INVALID` | PRE-write + POST-read | HIGH |
| `F-WPFA-CROSS-ORG-LEAK` | PRE-write | P0 |
| `F-WPFA-PDF-CONFIDENTIAL-LEAK` | PRE-PDF-emit | P0 |

(Per §4 v2.x.z amendment: F-WPFA-REGISTRY-VERSION-DRIFT is a sub-tag under F-WPFA-REGISTRY-DRIFT per OQ-5 default. F-WPFA-PDF-AUDITABILITY-BROKEN is a sub-tag `.pdf_claim_unlinked` under F-WPFA-SPAN-PROVENANCE-MISSING per OQ-7 default. Net code count: 13 above includes both coefficient-registry codes and the rollback; consolidated module count = 10. Per OQ-6 default, F-WPFA-* is **EXCLUDED** from F-CLASS-COVERAGE-INCOMPLETE META gate registry — F-WPFA-* is its own family, the META gate stays focused on F-CLASS-*.)

# §17.7 — Buyer-facing PDF — quarterly receipt template

## §17.7.1 — Purpose

Sales-lever artifact for board reports, grant reports, sales conversations. Renders an operator-attested CycleReceipt (or quarterly rollup of attested receipts) into a brand-consistent PDF.

## §17.7.2 — Template structure

1. **Header** — Golden Quill mark + tagline ("Golden Quill — regenerative grant intelligence."); operator-defined client name; quarter + cycle_id(s); operator attestation ribbon ("Attested by [operator] on YYYY-MM-DD").
2. **Headline** — single-sentence claim: "In Q2 2026, [client] saved $X / Y kWh by routing Z% of grant-cycle inference to member-owned hardware." Each numeric value carries a footnote-style superscript linking to the methodology citation (`CoefficientEntry.methodology_url`).
3. **Per-cycle breakdown table** — one row per cycle in the quarter: cycle_id · grant identifier · actual dollars/kWh · counterfactual dollars/kWh · delta dollars/kWh · trace_id reference.
4. **Per-model breakdown table** — one row per distinct model_id used in the quarter: model_id · is_local · hardware_sku · tokens · dollars · watt-hours.
5. **Methodology footer** — coefficient registry version (SHA3-512) · SN-LLC signing key id · methodology_url · operator pubkey id · receipt file path(s) for audit.
6. **Auditability block** — "Every dollar and watt-hour in this report links to a published coefficient + cycle_id + Logfire trace_id. Methodology is open; calculation code is proprietary."

## §17.7.3 — Brand consistency

- Parchment-card aesthetic per CIC card families (`assets/cards/customer_identification/*.png`).
- Brand thesis footer subhead (operator-tunable): *"Strong organizations are not short on substance — they lack funding infrastructure."*
- Typography matches website palette per `assets/website/about.md`.
- Single-page-per-quarter default; multi-page if breakdown tables overflow.

## §17.7.4 — Generation substrate (LOCKED)

PDF generation via Pydantic AI tool wrapping **weasyprint** (HTML→PDF). Always-local. No external rendering service. Substrate addition to Golden Image per ADR-001 substrate-frozen-at-Golden-Image discipline.

Template source: `pipeline/orchestrator/seats/wpfa/templates/buyer_facing_pdf.html`. Emitter: `pipeline/orchestrator/seats/wpfa/pdf_emitter.py`.

## §17.7.5 — Auditability mandate (binding)

Every dollar/kWh claim in the PDF MUST link back to: (a) the Coefficient Registry version (SHA3-512); (b) the `cycle_id`(s) covered; (c) at least one Logfire trace_id per claim. Failing any link fails-closed via `F-WPFA-SPAN-PROVENANCE-MISSING.pdf_claim_unlinked`.

## §17.7.6 — Classification register cross-check (binding)

PRE-PDF-emit, the emitter loads the operator-signed classification register (`coefficients_registry_version` matched against the receipt's `classification_register_version` field). Any field in the rendered PDF whose classification register entry is `confidential` fails-closed via `F-WPFA-PDF-CONFIDENTIAL-LEAK`. M13 is NOT bypassable for buyer-attested artifacts (structural attestation boundary).

**Indirect-template-data sub-tag (Cycle 1 RT-07 fold-in).** Static template parts (brand footer text, logo URLs, embedded reference strings) MAY embed identifiers that the explicit field-path scan would miss. Code-phase realization extends the scan to enumerate every string literal rendered in the final PDF (via post-render HTML extraction or template AST walk) and matches each against the classification register. Sub-tag `F-WPFA-PDF-CONFIDENTIAL-LEAK.indirect_static_template_data` covers this path. Implementation lands at WPFA Code phase per the `pipeline/handoffs/ws_wpfa_code_phase_handoff_<date>.md` packet.

**Cycle 2 RT-C2-02 fold-in.** The indirect-template-data scan also covers **CSS `content:` property values** and **inline JavaScript string literals** (weasyprint's CSS engine resolves `content:`, and any future template versions with `<script>` blocks emit literal strings into the final byte stream). Code-phase realization MUST walk the post-render document (CSS rules + JS AST) in addition to HTML text nodes. The sub-tag `.indirect_static_template_data` covers all three vectors (HTML text, CSS `content:`, JS literals).

# §17.8 — Operator-facing dashboard — Cowork HTML artifact

## §17.8.1 — Purpose

Transparent operator-facing surface for per-org, per-quarter (and Stage-2+ per-fleet placeholder) rollups.

## §17.8.2 — Read pattern (binding)

Pure read. Reads from disk-state only — never invokes external APIs, never writes back.
- Per-org rollup: `orgs/<slug>/vault/operational/cycle_receipts/*.json`.
- Per-quarter rollup: aggregation across all `<slug>` directories the operator owns (workspace-aggregate principal per §15.2 Law 3 carve-out).
- Coefficient context: `vault_shared/wpfa/coefficient_registry/active.yaml`.
- Pinned pubkey: `vault_shared/wpfa/sn_llc_pubkey.signed.yaml`.

## §17.8.3 — Three rollup tiers

1. **Per-org rollup (v0.1).** For a given `org_slug`, list all CycleReceipts in date order. Show cumulative dollars saved + watt-hours saved. Operator-attested receipts highlighted; internal-only receipts visible but not exportable to PDF.
2. **Per-quarter rollup (v0.1).** For a given `quarter` tag, aggregate across all orgs the operator owns. Workspace-aggregate discipline per §15.2 Law 3 enforcement (operator IS the multi-org actor; aggregate statistics permitted; per-org content does NOT leak across orgs).
3. **Per-fleet rollup (Stage-2+).** OUT OF SCOPE for v0.1 + v0.2; renders as `[Stage-2+]` placeholder card. **Cycle 1 RT-11 fold-in:** the placeholder is **static, data-free text only** — no SKU counts, no hardware enumeration, no aggregate facts. Future Stage-2+ activation MUST land a privacy-mask design with explicit operator opt-in before fleet composition is rendered (per RT-10 v2 multi-tenant track).

## §17.8.4 — Refresh model (LOCKED at v0.1)

Operator-on-demand only at v0.1. Scheduled-refresh deferred to v0.2 (matches §15 cadence story).

# §17.9 — Cedar policy additions (extends `pipeline/vault/policies/operational_subkinds.cedar`)

Two new rules + one extension; Python evaluator at `pipeline/vault/sub_kinds/policy_eval.py` is authoritative at v0.1 per §2 v7.1 §3.4 + v7.2 §6 lifecycle.

1. **Extension to `operational_org_isolation`** — add `sub_kind == "cycle_receipt"` to the default-permit set so cycle-receipt writes match the per-org isolation rule. F-WPFA-CROSS-ORG-LEAK at the Logician layer is defense-in-depth.
2. **New rule `cycle_receipt_operator_attestation`** — permits buyer-facing PDF emission ONLY when `signed_by_operator_ed25519` is non-None AND the signature verifies against the white-glove-pinned operator pubkey. Implicit deny → `F-WPFA-OPERATOR-SIGNATURE-MISSING`. Operator key rotation requires co-signing per v7.0.7 §6.1 pattern.
3. **New rule `cycle_receipt_read_isolation`** — permits reading a CycleReceipt under `orgs/<slug>/vault/operational/cycle_receipts/...` only when the requesting principal's `org_slug` attribute matches the path's `<slug>` OR when the requesting principal is `wpfa_dashboard_workspace_aggregate` (the Stage-1 operator-as-multi-org-actor principal — per §15.2 Law 3 workspace-aggregate carve-out). Implicit deny → `F-WPFA-CROSS-ORG-LEAK`.

# §17.10 — §7 Sovereignty Envelope invariants (proposed additions)

These extend §7 — receipt-emission discipline IS a Sovereignty Envelope-class concern (it crosses org-isolation + operator-attestation + cloud-vs-local boundaries that §7 owns).

- **§7.17.1** — Receipt emission MUST be deterministic. Same Logfire export + same Coefficient Registry version → byte-identical canonical-JSON output.
- **§7.17.2** — Receipt without operator signature is internal-only. Buyer-facing PDF emission requires operator Ed25519 attestation. F-WPFA-OPERATOR-SIGNATURE-MISSING PRE-emission gate enforces.
- **§7.17.3** — Receipt content is org-isolated. F-WPFA-CROSS-ORG-LEAK PRE-write gate + Cedar `cycle_receipt_org_isolation` enforce.
- **§7.17.4** — Every claim traces to a Logfire span. F-WPFA-SPAN-PROVENANCE-MISSING PRE-emission gate enforces.
- **§7.17.5** — Counterfactual references SN-LLC-signed registry baseline. F-WPFA-COUNTERFACTUAL-INFLATION PRE-emission gate enforces.

# §17.11 — Track-registry binding (extends §5 v8)

WPFA emission fires at cycle close. The cycle-close trigger is the §5 v8 track-registry's submission_mode terminal-state marker (per §5 v8 row 286). New track-registry hook: `wpfa.pipeline.cycle_close_emission_hook.v1` — a deterministic callable invoked by the §5 v8 dispatcher after the terminal-state marker span emits, before the dispatcher returns.

The hook is registered at the §0.5 v19 amendment row (per `section_00_5_section_17_wpfa_amendment.md` row 433 — see §17.13 below). The dispatcher contract clause 7 in §5 v8 §4.16 extends to permit hook registration without runtime rebind (if/elif fall-through pattern preserved).

# §17.12 — §15 Archivist composition (forward; NOT a v0.1 dependency)

Per §15 v1 LOCK §15.0 cross-amendment composition map, Archivist reads workspace-shared substrates quarterly. WPFA quarterly rollups (per-org cumulative + workspace-aggregate) ARE workspace-shared read substrates Archivist could compose into its quarterly digest at v1.x.

**v1.x forward-design markers (not v0.1 scope):**
- Archivist v1.x quarterly digest MAY include a "Regenerative-savings rollup across the quarter" section sourced from WPFA per-quarter aggregates.
- F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT (§15.9.5) extends with new wrapper `vault_read_intent_wpfa_quarterly`; F-ARCHIVIST-CROSS-ORG-LEAK applies (Archivist reads workspace-aggregate, not per-org-content).
- Archivist's pattern-detection prompt does NOT process individual receipts; it reads pre-aggregated quarterly rollups.

**Sibling-not-nested verification at every Thesis cycle:** the audit prompt MUST verify the WPFA emission path does NOT consume Reflection Packet output, and vice versa.

# §17.13 — v0.1 vs v0.2 boundary table

| Element | v0.1 Beta | v0.2 first wave | v1.x / horizon |
|---|---|---|---|
| `CycleReceipt` schema + sub-kind registry row | **v0.1 Beta** | — | — |
| Coefficient Registry signed-asset class | **v0.1 Beta** (SN-LLC publishes inaugural Q3-2026 registry) | Quarterly cadence; 7-day emergency updates | — |
| Cycle Accountant module | **v0.1 Beta** (LIVE predicates, not stubs) | — | — |
| F-WPFA-* failure-code family (12 codes; 10 modules) | **v0.1 Beta** (predicate bodies LIVE) | — | — |
| Operator-facing dashboard (per-org + per-quarter) | **v0.1 Beta** (Cowork HTML artifact) | — | — |
| Buyer-facing PDF artifact | **v0.1 Beta** — operator-LOCKED sales lever | — | — |
| Operator Ed25519 attestation flow | **v0.1 Beta** (TTY-gated CLI per Intake §11.7 precedent) | — | — |
| Per-fleet (Stage-2+) rollup | — | — | **Stage 2** (12-Tilth fleet milestone) |
| Water dimension | — | **v0.2** (`dimensions_active` extends to include `"water"`) | — |
| CO2 dimension | — | **v0.2** (per-region grid-mix lookups deferred to v1.x) | — |
| Peer review of methodology | — | **v0.2 candidate** (operator-decision per foundation-funder pressure) | — |
| Dashboard scheduled-refresh | — | **v0.2** (per `schedule` skill) | — |
| Multi-currency support | — | **v0.2** (FX handling) | — |
| Tilth-side coefficient measurement | — | — | **v1.x** (operator on-hardware energy measurement; F-WPFA-REGISTRY-DRIFT surfaces deviation) |
| Stage-5 commons consent-tier WPFA aggregation | — | — | **Stage 5** (cooperative-owned compute commons per v7.0.5 §4 on-ramp) |
| Archivist v1.x composition (quarterly digest WPFA rollup section) | — | — | **v1.x** per §17.12 |

# §17.14 — HARD-LOCKED elements (Thesis cannot relitigate)

- A12 Decimal mandate for `dollars_total_minor_units` (int minor units; no float) per v7.0.4-M1 §6.
- A12 extended to energy quantities (int micro-watt-hours; no float).
- Sibling-not-nested pattern with Reflection Packet — both consume the same span tree at cycle close but share zero output/consumer/schema.
- v0.1 dimensions = dollars + energy ONLY; water + CO2 deferred to v0.2.
- Buyer-facing PDF is a v0.1 Beta sales lever, NOT deferred.
- Coefficient Registry trust = SN-LLC Ed25519, white-glove-pinned pubkey, same mechanism as router-template per v7.0.7 §6.1 byte-for-byte.
- `write-if-absent` discipline + canonical-JSON encode/decode round-trip per §2 v7.2 §1.
- Law 3 Org Isolation — receipts live under `orgs/<slug>/vault/operational/cycle_receipts/` per §2 v7.2 §5.
- Operator attestation is REQUIRED for buyer-external use; internal-only receipt is emitted but not signed.
- §17 section number (NOT §16 — reserved for Reflection Packet) and §17.1 single-section discipline (NO sub-section split with Reflection Packet).
- PDF generation substrate = weasyprint (HTML→PDF).
- Energy quantization at micro-watt-hours (NOT milli-watt-hours).
- F-WPFA-* EXCLUDED from F-CLASS-COVERAGE-INCOMPLETE META gate (own family; META stays focused on F-CLASS-*).
- Path B naming reconciliation: Reflection Packet's family is F-PACKET-*; WPFA §17.6 cross-reference reads "F-PACKET-SPAN-PROVENANCE-MISSING" (forthcoming sibling).

# §17.15 — DECISIONS-PENDING-CONFIRMATION (operator-LOCKED defaults; Thesis-overrideable)

- **DPC-1 — Counterfactual baseline cadence: quarterly.** SN-LLC publishes a single named flagship reference per quarter. Emergency baseline change = 7-day cadence per v7.0.7 §6.1.
- **DPC-2 — Methodology disclosure level: open coefficients + methodology document at stable URL; calculation code stays proprietary.** Peer review deferred to v0.2.

# §17.15.1 — Rollback bound (Cycle 1 RT-14 disposition)

At v0.1 single-client (A1), the operator runs exactly one workflow at a time; the `tilth wpfa registry rollback` CLI is synchronous + TTY-gated, so it cannot interleave with an active cycle-close emission. Multi-process/multi-operator rollback racing is **forward-bound to v1.x WPFA amendment** with explicit registry-version lock during cycle-close (mutex pattern). v0.1 ships without the lock; the threat model (A1+A4) makes the lock superfluous at single-client scale.

# §17.16 — Re-emission discipline

Re-emission against the same `cycle_id` (correcting a buggy cycle):
- **Internal-only receipts** — operator-direct + audit-ledger entry (light weight; mirrors §2 v7.2 re-key path discipline).
- **Buyer-attested receipts** — full re-attestation flow + audit-ledger entry. The operator re-signs (the signature itself is the audit trail).

PRE-gate: receipts with different `coefficients_registry_version` than the currently-active registry MUST carry an admin-risk-ledger reference (else `F-WPFA-REGISTRY-DRIFT.registry_version_mismatch_no_ledger_entry` — sub-tag advisory).

# §17.17 — Implementation files (Code-phase realization)

| File | Class |
|---|---|
| `pipeline/orchestrator/seats/wpfa/__init__.py` | package scaffold |
| `pipeline/orchestrator/seats/wpfa/cycle_accountant.py` | Cycle Accountant module + `compose_receipt` + `run_cycle_accountant_pipeline` |
| `pipeline/orchestrator/seats/wpfa/pdf_emitter.py` | weasyprint HTML→PDF emitter; classification register cross-check |
| `pipeline/orchestrator/seats/wpfa/templates/buyer_facing_pdf.html` | Jinja2 template per §17.7.2 |
| `pipeline/vault/sub_kinds/cycle_receipts.py` | schema + canonical_codec + record_id_for + SUB_KIND_REGISTRY row |
| `pipeline/vault/sub_kinds/coefficient_registry.py` | CoefficientRegistry + CoefficientEntry + verify_signature + load_active |
| `pipeline/logician/gates/f_wpfa_coefficient_registry_validation.py` | consolidated module for F-WPFA-COEFFICIENT-{REGISTRY-UNSIGNED,SIGNATURE-INVALID,ROLLBACK-INVALID} (per §6 OQ-4 default) |
| `pipeline/logician/gates/f_wpfa_*.py` (9 more modules) | one per remaining code |
| `pipeline/vault/policies/operational_subkinds.cedar` | extend with 1 new rule + amend existing (§17.9) |
| `vault_shared/wpfa/coefficient_registry/active.yaml` | inaugural Q3-2026 seed (SN-LLC publishes) |
| `vault_shared/wpfa/sn_llc_pubkey.signed.yaml` | pinned SN-LLC pubkey scaffold (white-glove sets at onboarding) |
| `orgs/_TEMPLATE/wpfa_artifacts/.gitkeep` | per-client buyer-facing PDF output dir scaffold |
| `orgs/_TEMPLATE/vault/operational/cycle_receipts/.gitkeep` | per-client receipt vault subtree scaffold |

# §17.18 — Audit trail

L-005 strict two-cycle Thesis CLOSED with FULL LIVE CROSS-FAMILY rigor — Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq via the openclaw gateway bridge (`mcp__Control_your_Mac__osascript` → `openclaw infer model run --gateway`). Templates cloned from `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`. Audit artifacts at `pipeline/validation/wpfa_thesis_2026-05-10/{audit_prompt_v{1,2}_*.md, audit_v{1,2}_{editor,judge,red_team}.{md,raw.json}}`.

Cycle 2 NEW probes folded-in at LOCK per row-170 transparent disposition pattern (mirrors row 179 + 180 + 190 + 196/197 + 200/201 + 202/203/204 precedents). Tenth substantive v0.1+v0.2 round to LOCK at this rigor level.

# §17.19 — Changelog

- **2026-05-11 §17 v1 LOCKED** — compound paired-commit with §4 v2.x.z F-WPFA-* amendment + §2 v7.4 Coefficient Registry signed-asset amendment + §0.5 v19 paired-commit. Path B documentary edit applied to §17.6 (F-PACKET-SPAN-PROVENANCE-MISSING cross-reference, per `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md`).
