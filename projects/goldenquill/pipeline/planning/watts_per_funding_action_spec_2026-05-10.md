---
title: Watts per Funding Action (WPFA) — Dispatch Spec Card (§17 v1 + §4 v2.x.z F-WPFA-* family + §0.5 v17 compound-LOCK candidate + Coefficient Registry signed-asset class)
filed: 2026-05-10
operator: Josh Inklovich
status: DISPATCH_SPEC_DRAFT — pre-Thesis dispatch packet; no LOCK ceremony. L-005 two-cycle review (Editor + Judge + Red Team, FULL live cross-family per /AGENTS.md) MUST close before any LOCK. This is a spec card per `pipeline/engineering/engineering_process_v0.1.md` §11 adapted to a blueprint-amendment family (multiple sections under one compound LOCK) rather than a single Python module. Sibling artifact to the Reflection Packet (research `pipeline/research/reflection_packet_grounding/findings_2026-05-10.md`); the two consume the same Logfire span tree at cycle close but emit independently to different audiences.
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                             # v7 LOCKED 2026-04-19 A1–A12; A12 Decimal mandate; A1 single-client v0.1 threat model; A4 operator-trusted preflight
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md                      # v7.0.4-M1 LOCKED 2026-05-10 row 190 — Decimal-mandate three-layer ban-float (load-bearing for energy quantities too); explicit-context-required helper; canonical-JSON signing
  - pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md                         # v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intel DB + Match DB + Scout channel G; signed-asset publication pattern (Funder Intel curation slot) is precedent for the Coefficient Registry asset class
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                         # v7.0.7 LOCKED 2026-05-10 row 180 — Beta classification-driven routing; §6.1 SN-LLC router-template Ed25519 signing + white-glove-pinned pubkey + Trust-On-First-Use rotation is the load-bearing trust mechanism this spec mirrors for the Coefficient Registry
  - pipeline/blueprint/v0.1/section_02_v7_2_amendment.md                                # §2 v7.2 LOCKED 2026-05-10 row 186 — operational-data sub-kinds + SUB_KIND_REGISTRY pattern (operational/cycle_receipts/ proposed as new sub-kind)
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                                # §4 v2.x LOCKED 2026-05-10 rows 193/194 — F-CLASS-* dormant primitives activated; v7.0.4-M1 corrective predicates; format pattern this spec mirrors for F-WPFA-* family
  - pipeline/blueprint/v0.1/section_05_v8_amendment.md                                  # §5 v8 LOCKED 2026-05-10 rows 188/189 — track-registry; cycle-close trigger semantics for receipt emission
  - pipeline/blueprint/v0.1/section_15_archivist.md                                     # §15 v1 SPEC LOCKED 2026-05-10 rows 191/192 — proposes-only between-cycle preservation; v1.x Archivist quarterly digest MAY compose WPFA quarterly rollup but does NOT consume receipts directly (different audience)
  - pipeline/blueprint/v0.1/section_00_5_section_13_data_collector_amendment.md         # §0.5 v15 LOCKED 2026-05-10 — runtime-live total row 376
  - pipeline/planning/funding_goal_amendment_spec_2026-05-10.md                         # Funding Goal spec card 2026-05-10 — allocated §0.5 rows 377-399 (23 rows); WPFA row range conditional on Funding Goal LOCK ordering (see §6)
  - pipeline/research/reflection_packet_grounding/findings_2026-05-10.md                # Reflection Packet research findings 2026-05-10 — sibling artifact; both consume same Logfire span tree; emission discipline + Pydantic AI output pattern shared; F-REFLECTION-SPAN-PROVENANCE-MISSING is sibling to F-WPFA-SPAN-PROVENANCE-MISSING
authority: orchestrator dispatch 2026-05-10 — "Watts per Funding Action (WPFA) — Tilth doesn't just route to local, it proves it routed to local, and proves the savings, with auditable methodology."
purpose: Stage a SPEC for the WPFA cycle-close telemetry artifact, its signed Coefficient Registry asset class, the F-WPFA-* failure-code family, the operator-facing dashboard, and the buyer-facing PDF artifact, so a downstream Thesis round + Code phase can audit and LOCK them. SPEC ONLY — no Python written; no LOCK ceremony invoked; no row range reserved against §0.5 until paired blueprint amendments land.
dispatch_class: spec_card_for_blueprint_amendment_family
ws_dispatch_target: NEW WS — provisionally "WS-WPFA Watts per Funding Action" — not yet on `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md`. v0.1 Beta scope per operator LOCKED-2026-05-10 directive (buyer-facing PDF is sales lever, NOT deferred). v0.2 horizon for water + CO2 dimensions + fleet-level rollup.
review_discipline: L-005 strict two-cycle, FULL live cross-family per /AGENTS.md (Editor=Llama/Groq + Judge=Gemini/Google + Red Team=GPT-OSS/Groq) — no Section E carve-out. Mirrors the rigor level applied to §2 v7.2, §11 v1, §12 v1, §13 v1, §15 v1, §4 v2.x.
sibling_artifact: pipeline/research/reflection_packet_grounding/findings_2026-05-10.md → forthcoming Reflection Packet design dispatch. Sibling-not-nested pattern. WPFA and Reflection Packet share the cycle-close trigger and the Logfire span tree as input substrate; they emit independent Pydantic BaseModels to different consumers (Reflection → Archivist; WPFA → operator dashboard + buyer PDF). Their gate families (F-REFLECTION-* / F-WPFA-*) are siblings under §4 v2.x with shared SPAN-PROVENANCE-MISSING discipline.
---

# §0. Why this spec card exists

Golden Quill's brand thesis ("regenerative grant intelligence") and v7.0.7's classification-driven routing make Tilth a system that **actually routes inference to operator-owned hardware** when input is Confidential. Today, that routing is invisible to the buyer. There is no auditable per-cycle artifact that says: "this grant cycle consumed $X and Y watt-hours; if you had routed 100% to a Q3 2026 flagship cloud model, it would have cost $X' and Y' watt-hours; the difference is your regenerative-buyer dividend, and here's the methodology."

**WPFA fills that hole.** A typed Pydantic `CycleReceipt` BaseModel, emitted at every cycle close, that:

1. Reads the Logfire span tree from the cycle.
2. Joins per-model token counts with a signed Coefficient Registry (SN-LLC-published, Ed25519-signed, white-glove-pinned-pubkey-verified, same trust mechanism as v7.0.7 §6.1 router-template).
3. Computes per-model dollars and watt-hours actually consumed.
4. Computes the counterfactual: dollars and watt-hours that 100%-routing to the quarter's SN-LLC-published flagship baseline would have consumed.
5. Emits a typed delta — the regenerative savings claim — with span_provenance.trace_ids per claim.
6. Optionally (for buyer-external use) carries an operator Ed25519 attestation signature.

Three load-bearing functions:

- **Operator transparency.** Per-cycle, per-org, per-quarter, per-fleet (Stage-2+) rollups of what Tilth actually consumed. Operator can verify their own infrastructure decisions.
- **Buyer-facing accounting.** Quarterly receipt PDF for board reports, grant reports, sales conversations. "FIT Farms Commons saved $X / Y kWh in Q2 2026 by routing Z% of inference to member-owned hardware." Every dollar and kWh links back to a published coefficient + cycle_id + trace_id.
- **Sales lever for the regenerative-buyer thesis.** The thing that converts "we have a 128 GB box on your desk" into "and here's the receipt that proves the dividend."

**Sibling-not-nested with Reflection Packet.** Both artifacts emit at cycle close. Both consume the same Logfire span tree. They are independent Pydantic BaseModels — neither composes the other. Their consumers differ:

- ReflectionPacket → Archivist learning loop (Tilth-internal, operator-facing curation source).
- CycleReceipt → operator transparency surface + buyer-external attestation artifact.

This sibling discipline mirrors §15 Archivist's relationship to §13 Data Collector: both v0.2 support agents, both observe the same workspace, but they share zero runtime path. WPFA and Reflection Packet share the cycle-close trigger and the span tree as input; they share zero output, zero downstream consumer, zero schema.

# §1. Compound-LOCK pairing identity

Following the WS-H §2 v7.2 + §0.5 v11 precedent and the WS-I §13 + §0.5 v15 precedent (paired-commit per `pipeline/blueprint/v0.1/section_06_operating_envelope.md` §6.17 Option-B), the WPFA amendment is a **compound-LOCK across four siblings**:

| Sibling | What lands | Pairing class |
|---|---|---|
| §17 v1 (new file `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md`) — section number proposal, see §2 below for rationale | New seat-class section: WPFA Cycle Accountant module spec + CycleReceipt Pydantic shape + emission triggers + per-org dashboard surface + buyer-facing PDF template; new vault subtree `operational/cycle_receipts/`; consumes Logfire span tree + Coefficient Registry; ties to §5 v8 track-registry cycle-close marker | Primary |
| §4 v2.x.z (new amendment file `section_04_v2_x_z_wpfa_amendment.md`) | F-WPFA-* failure codes registered; PRE/POST gate rows allocated; module skeletons pointed at | Sibling |
| Coefficient Registry signed-asset spec (new file `pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md` OR a §17 internal sub-section — see §7 below for OQ) | SN-LLC-published per-model coefficient table; Ed25519 signing; white-glove-pinned pubkey verify; quarterly cadence; rollback protocol | Sibling |
| §0.5 v17 amendment (new file `section_00_5_section_17_wpfa_amendment.md`) | Row append starting at 400 OR conditionally adjusted per Funding Goal LOCK ordering (see §6) | Sibling |

Compound transaction discipline per §2 v7.2 §11 audit prompt + WS-I §13 paired-commit pattern: all four sibling rows enter `lock_history.v1.jsonl` at the same `lock_timestamp_utc`. F-INDEX-STALE PRE-gate fires at commit time per §6.2 order 3; all new §0.5 rows must be present in the index or the compound commit fails closed.

**Compound LOCK row(s) in lock_history:** anticipated rows ≥ 200 (current runtime-live row at §13 v1 LOCK = 197 + Funding Goal compound-LOCK candidate ~198 + WPFA compound-LOCK candidate ~200; pre-staging only — actual row depends on which other LOCKs land first).

# §2. Section number proposal — §17 (rationale)

**Current §-numbering at v0.1 (sections that have LOCKed primitives):**

- §0.5 Interface Index · §1 Sovereignty Envelope · §2 Vault Topology · §3 Scout · §4 Logician · §5 Pipeline · §6 Operating Envelope · §7 Scribe · §8 Editor (TBD, parked) · §9 Judge (TBD, parked) · §10 Red Team · §11 Intake · §12 Uploader · §13 Data Collector · §14 Report Generator (v0.2 horizon) · §15 Archivist.

**§16 is reserved.** Per recent practice, the Reflection Packet design (sibling artifact, research findings 2026-05-10) is the natural occupant of §16 — it is a Tilth-internal between-cycle learning surface, structurally adjacent to §15 Archivist (which consumes Reflection Packets), and the research findings explicitly seed a packet-emission-as-Pydantic-output design. The Reflection Packet design has not yet dispatched, but pre-staging §16 for it preserves topical clustering.

**WPFA lands at §17.** Rationale:

1. **Topical cluster preserved.** §15 Archivist + §16 Reflection Packet are Tilth-internal between-cycle preservation surfaces. §17 WPFA is operator-and-buyer-facing accounting — different audience, structurally adjacent at emission timing (cycle-close), but architecturally a different concern. Placing WPFA after the Tilth-internal cluster signals the boundary.
2. **Emission-orchestration symmetry.** Both Reflection Packet (§16) and WPFA (§17) emit at cycle close from the Logfire span tree. Placing them as adjacent sections lets a future §16/§17 "shared cycle-close emission orchestrator" sub-section sit cleanly between them — OR (alternative) lets each section own its own emission discipline without forcing a shared orchestrator.
3. **§17 leaves room for a hypothetical §16 sub-spec proliferation.** Reflection Packet may grow §16.1 (Packet schema), §16.2 (emission orchestrator), §16.3 (Archivist consumption contract). §17 stays clean as the WPFA root.

**Alternative considered: §16 for WPFA.** Rejected because Reflection Packet research already implies §16 occupancy and the Tilth-internal-vs-buyer-external distinction is a useful architectural axis at the §-numbering layer.

**Alternative considered: WPFA as §17.1 sub-section of a unified cycle-close-emission §17.** Rejected for v0.1 because the two emission surfaces have independent failure-code families (F-REFLECTION-* / F-WPFA-*), independent consumers (Archivist / dashboard+PDF), and independent classification postures (Reflection is Tilth-internal; WPFA buyer-facing PDF is operator-attested external). Forcing them under one §17 risks coupling.

**OQ-1 (operator-decision):** confirm §17 for WPFA, or pick a different number. Default = §17.

# §3. CycleReceipt Pydantic shape

Following the §2 v7.2 sub-kind convention EXACTLY: `@dataclass(frozen=True, kw_only=True)`; one record = one file; SIMPLE class; `write-if-absent` mode; `__post_init__` invariant validation; canonical-JSON encode/decode round-trip; module at `pipeline/orchestrator/seats/wpfa/cycle_accountant.py` + schema at `pipeline/vault/sub_kinds/cycle_receipts.py` (registered as new SUB_KIND per §2 v7.2 pattern); tests at `tests/seats/wpfa/` + `tests/vault/sub_kinds/test_cycle_receipts.py`.

```python
@dataclass(frozen=True, kw_only=True)
class CycleReceipt:
    # Identity + provenance
    cycle_id: str                                       # opaque caller-minted ID; matches filename {cycle_id}.json
    org_slug: str                                       # one of orgs/<slug>/ identifiers — Law 3 binding
    schema_version: str                                 # semver string, e.g., "1.0.0"; tolerant-reader pattern at consumer
    classification_register_version: str                # SHA3-512 hash of the operator-signed classification register at cycle start

    # Emission context
    emitted_at: str                                     # UTC ISO-8601 'Z'
    baseline_model_id: str                              # the quarter's SN-LLC-published flagship model identity, e.g., "claude-sonnet-4-6"
    baseline_quarter: str                               # quarter tag, e.g., "Q3-2026"
    coefficients_registry_version: str                  # SHA3-512 hash of the SN-LLC-signed Coefficient Registry at emission time
    coefficients_registry_signature_ed25519: str        # hex-encoded Ed25519 signature over the registry; verified PRE-emission

    # Active dimensions (forward-compat; v0.1 = dollars + energy only)
    dimensions_active: tuple[str, ...]                  # e.g., ("dollars", "energy") at v0.1; ("dollars", "energy", "water", "co2") at v0.2

    # Actual consumption (this cycle)
    actual: CycleReceiptDimensionTotals                 # see below
    actual_per_model: tuple[PerModelCall, ...]          # one row per distinct model_id encountered in the span tree

    # Counterfactual (100% routed to quarterly baseline)
    counterfactual: CycleReceiptDimensionTotals

    # Regenerative-savings delta
    delta: CycleReceiptDelta

    # Provenance — every quantitative claim must trace
    span_provenance: SpanProvenance                     # trace_ids[], span_ids per claim, Logfire export reference

    # Operator attestation — required for buyer-external use, optional for internal-only
    signed_by_operator_ed25519: str | None              # hex-encoded Ed25519 signature over canonical-JSON-encoded receipt; None for internal-only


@dataclass(frozen=True, kw_only=True)
class CycleReceiptDimensionTotals:
    dollars_total_minor_units: int                      # smallest currency unit (e.g., cents); A12 Decimal mandate per v7.0.4-M1 §6
    currency: str                                       # ISO-4217 alpha-3, e.g., "USD"
    watt_hours_total_micro: int                         # micro-watt-hours (10^-6 Wh) as integer; A12 Decimal mandate applied to energy by analogy
    # v0.2 forward-compat fields (refuse if dimensions_active does not include):
    water_liters_micro: int | None                      # micro-liters; None at v0.1
    co2_grams_micro: int | None                         # micro-grams CO2-equivalent; None at v0.1


@dataclass(frozen=True, kw_only=True)
class PerModelCall:
    model_id: str                                       # e.g., "groq/llama-3.3-70b-versatile", "anthropic/claude-sonnet-4-6", "local/m3-ultra-llama-70b"
    is_local: bool                                      # local hardware vs cloud; drives counterfactual logic
    hardware_sku: str | None                            # Apple M3 Ultra / AMD GX-10 / NVIDIA Spark — None for cloud models
    input_tokens: int
    output_tokens: int
    dollars_minor_units: int                            # this call's dollar cost
    watt_hours_micro: int                               # this call's energy
    span_ids: tuple[str, ...]                           # Logfire span IDs this row aggregates


@dataclass(frozen=True, kw_only=True)
class CycleReceiptDelta:
    dollars_saved_minor_units: int                      # counterfactual - actual; may be negative (anti-pattern flag)
    watt_hours_saved_micro: int
    percent_dollars_saved: int                          # basis points (10000 = 100%); A12 Decimal-derived but stored int
    percent_watt_hours_saved: int
    # v0.2 forward-compat:
    water_liters_saved_micro: int | None
    co2_grams_saved_micro: int | None


@dataclass(frozen=True, kw_only=True)
class SpanProvenance:
    trace_ids: tuple[str, ...]                          # one or more Logfire trace IDs covered by this receipt
    logfire_export_uri: str | None                      # optional pointer to a Logfire export bundle for offline audit
    cycle_close_marker_span_id: str                     # the span ID for the cycle-close marker (per §5 v8 track-registry)
    per_claim_span_ids: dict[str, tuple[str, ...]]      # claim_key (e.g., "actual.dollars_total") → tuple of span_ids backing it
```

## §3.1 A12 Decimal mandate dispatch — applied to BOTH dollars AND energy

Per architecture v7.0.4-M1 §6 the Decimal mandate is three-layer (AST-lint ban on `float` for monetary fields + dedicated decoder helper + explicit-context-required helper). WPFA extends this discipline to **energy quantities** because watt-hours-saved is load-bearing for the buyer-facing accounting claim — float rounding errors would corrupt audit trails.

- `dollars_total_minor_units` is `int` (minor units, e.g., cents) — same pattern as §2.11.2 FinancialsRecord.amount_minor_units.
- `watt_hours_total_micro` is `int` (micro-watt-hours, 10^-6 Wh) — NEW pattern, not previously in §2 v7.2 corpus; this spec proposes it.
- `percent_dollars_saved` / `percent_watt_hours_saved` are `int` basis points (10000 = 100%) — Decimal arithmetic happens in the Cycle Accountant; result is rounded `ROUND_HALF_EVEN` to integer basis points for on-disk stability.

The decoder helper `from_canonical_bytes` MUST re-validate that the JSON-parsed values are `int` and not float; tampered-on-disk receipts with `dollars_total_minor_units: 12500.0` (decoded as float) fail-close on `F-WPFA-SCHEMA-INVALID` (sub-tag `.numeric_field_float`). AST-lint R3-equivalent rule applies — extension to ban `float` on `(_minor_units|_micro|_saved)$` field-name patterns.

**OQ-2 (operator-decision):** is energy quantization at micro-watt-hours (`10^-6 Wh`) the right precision, or should it be milli-watt-hours (`10^-3 Wh`)? Trade-off: micro-Wh handles per-token granularity (a single LLM call may produce ~0.1 Wh; per-token energy is ~10 µWh) without resorting to floats; milli-Wh is more human-readable but loses per-token resolution. Default: micro-Wh.

## §3.2 Invariants (`__post_init__` — fail-close at write AND at decode round-trip)

1. `cycle_id` non-empty; matches expected filename derivation.
2. `org_slug` non-empty; resolves to an existing `orgs/<slug>/` subtree (PRE-write).
3. `schema_version` matches `^\d+\.\d+\.\d+$` (semver).
4. `classification_register_version` is 128-hex-char SHA3-512 digest.
5. `emitted_at` ends with `'Z'`.
6. `baseline_quarter` matches `^Q[1-4]-\d{4}$`.
7. `coefficients_registry_version` is 128-hex-char SHA3-512 digest; matches the registry currently on disk (PRE-write).
8. `coefficients_registry_signature_ed25519` is hex; PRE-write Ed25519 verify against white-glove-pinned SN-LLC pubkey MUST pass.
9. `dimensions_active` is a tuple of strings from the closed set `{"dollars", "energy", "water", "co2"}`; v0.1 deployments MUST have `dimensions_active == ("dollars", "energy")`; any other value at v0.1 fails `F-WPFA-DIMENSION-UNSUPPORTED`.
10. `actual.currency == counterfactual.currency` (no mixed-currency receipts).
11. For every `PerModelCall` row, `model_id` resolves to an entry in the loaded Coefficient Registry (else `F-WPFA-MODEL-COEFFICIENT-MISSING`).
12. `counterfactual.dollars_total_minor_units` and `counterfactual.watt_hours_total_micro` MUST trace to the `baseline_model_id` coefficient in the SN-LLC-signed registry (else `F-WPFA-COUNTERFACTUAL-INFLATION`).
13. `delta.dollars_saved_minor_units == counterfactual.dollars_total_minor_units - actual.dollars_total_minor_units` (re-validated at decode); same for energy.
14. Every claim key in `span_provenance.per_claim_span_ids` MUST have at least one resolvable Logfire span_id (else `F-WPFA-SPAN-PROVENANCE-MISSING`).
15. `signed_by_operator_ed25519`: if non-None, MUST verify against the white-glove-pinned operator pubkey over the canonical-JSON-encoded receipt (excluding the signature field itself); if None, the receipt is internal-only and MUST NOT be exported to buyer-facing PDF (else `F-WPFA-OPERATOR-SIGNATURE-MISSING`).
16. Per-model rows in `actual_per_model`: aggregate sum of `dollars_minor_units` MUST equal `actual.dollars_total_minor_units` (re-validated at decode); same for energy.
17. Forward-compat: if `schema_version` major-version is higher than consuming code's known max, consumer falls through to tolerant-reader path and surfaces a `F-WPFA-SCHEMA-DRIFT` advisory (NOT fail-closed at v0.1; informational at consumer side).

## §3.3 Sub-kind registry row (§2.12 amendment)

```python
"cycle_receipt": SubKindDescriptor(
    intent="operational-cycle-receipt-write",
    vault_subtree="operational/cycle_receipts/",
    record_class=CycleReceipt,
    to_canonical_bytes=cycle_receipts.to_canonical_bytes,
    from_canonical_bytes=cycle_receipts.from_canonical_bytes,
    record_id_for=cycle_receipts.record_id_for,
    severity_default="YELLOW",
    severity_for=lambda record: "RED" if record.signed_by_operator_ed25519 is not None else "YELLOW",  # signed = buyer-facing → admin-risk surface attention
),
```

# §4. Coefficient Registry — signed-asset specification

The Coefficient Registry is a **new signed-asset class** under v7.0.7 §6.1 trust discipline (mirrors the router-template publication mechanism). It carries per-model coefficients (dollars-per-million-tokens + watt-hours-per-million-tokens) for every model Tilth can route to, plus per-hardware-SKU baseline metrics for local nodes.

## §4.1 CoefficientRegistry Pydantic shape

```python
@dataclass(frozen=True, kw_only=True)
class CoefficientRegistry:
    schema_version: str                                 # semver
    quarter: str                                        # e.g., "Q3-2026"
    published_at: str                                   # UTC ISO-8601 'Z'
    sn_llc_signature_ed25519: str                       # hex Ed25519 signature over canonical-JSON-encoded registry (excl. signature field)
    sn_llc_signing_key_id: str                          # opaque key identifier; rotates per A12 crypto-agility envelope
    baseline_model_id: str                              # the quarter's flagship counterfactual reference (e.g., "claude-sonnet-4-6")
    entries: tuple[CoefficientEntry, ...]               # one per model
    methodology_url: str                                # stable URL where coefficients + citations + methodology document live
    rollback_pointer: str | None                        # optional SHA3-512 of the prior registry version; for operator-driven rollback


@dataclass(frozen=True, kw_only=True)
class CoefficientEntry:
    model_id: str                                       # canonical model identifier — MUST match the model_id reported in Logfire spans
    is_local: bool
    hardware_sku: str | None                            # "apple_m3_ultra" | "amd_gx_10" | "nvidia_spark" | None for cloud
    dollars_per_million_input_tokens_minor_units: int   # A12 int — minor units per million
    dollars_per_million_output_tokens_minor_units: int
    watt_hours_per_million_input_tokens_micro: int      # A12 int — micro-Wh per million
    watt_hours_per_million_output_tokens_micro: int
    idle_watts_baseline_micro: int | None               # local only — baseline draw of the hardware at idle
    peak_watts_under_load_micro: int | None             # local only — peak draw during inference
    citation_url: str                                   # where this coefficient was published — Anthropic / OpenAI / Google docs or measured-on-hardware report
    measurement_date: str                               # UTC ISO-8601 'YYYY-MM-DD'
    measurement_methodology_url: str                    # detailed methodology document
```

## §4.2 Trust mechanism — mirrors v7.0.7 §6.1 router-template signing

- **SN-LLC signs every Coefficient Registry release with Ed25519** over the canonical-JSON-encoded registry (excluding the signature field itself).
- **Golden Quill verifies the signature against the white-glove-pinned SN-LLC public key BEFORE loading any registry update** — failure → fail-closed via `F-WPFA-COEFFICIENT-SIGNATURE-INVALID`; deployment stays on the previous pinned version.
- **Public-key rotation** requires the new key co-signed by the previous key (Trust-On-First-Use rotation, audited). Same discipline as v7.0.7 §6.1 router-template pubkey rotation.
- **Per-deployment registry** is derived from the SN-LLC publication; deployments don't auto-update — operator opts in per release via `tilth wpfa registry update` CLI verb (TTY-gated per Intake §11.7 precedent; no `--yes`/`--auto-confirm`/`--force` flags; argparse-level rejection).

## §4.3 On-disk location + update cadence

- **Canonical workspace path:** `vault_shared/wpfa/coefficient_registry/active.yaml` (current pinned version) + `vault_shared/wpfa/coefficient_registry/history/<sha3_512>.yaml` (full history; receipts may reference historical versions for re-emission audits).
- **Pinned pubkey:** `vault_shared/wpfa/sn_llc_pubkey.signed.yaml` — set at white-glove onboarding; rotated via co-signing per §4.2.
- **Update cadence:** SN-LLC publishes per quarter (soft commitment, paired with the router-template quarterly review). Emergency updates (model deprecation, coefficient correction) follow the 7-day discipline per v7.0.7 §6.1.
- **Rollback protocol:** every published registry carries `rollback_pointer` to the prior version's SHA3-512. Operator-initiated rollback (`tilth wpfa registry rollback --to <sha3>`) re-pins the prior registry. PRE-gate: rollback target SHA3 MUST resolve to a registry on disk under `history/`; absent → fail-closed via `F-WPFA-COEFFICIENT-ROLLBACK-INVALID` (NEW gate — propose adding).
- **OQ-3 (operator-decision):** should rollback be operator-direct or require a co-signed SN-LLC acknowledgment? Default: operator-direct (operator owns deployment), with audit-ledger entry recording the rollback reason.

## §4.4 Registry vs receipt versioning interplay

- Receipts pin the `coefficients_registry_version` at emission time. A re-emission (e.g., correcting a buggy cycle) against the same `cycle_id` MAY pin a different registry version IF operator-signed admin-risk ledger entry justifies the recomputation. PRE-gate: receipts with different `coefficients_registry_version` than the currently-active registry MUST carry an admin-risk-ledger reference (else `F-WPFA-REGISTRY-VERSION-DRIFT` — NEW advisory gate; default operator-tunable to fail-closed for buyer-attested receipts).

# §5. Cycle Accountant — module skeleton

Module: `pipeline/orchestrator/seats/wpfa/cycle_accountant.py` (NEW). Purpose, inputs, outputs only — NO Python implementation in this spec.

**Purpose:** at cycle close (per §5 v8 track-registry submission_mode/eval_mode terminal-state marker), read the Logfire span tree for the cycle, join with the active Coefficient Registry and the current classification register, compute per-model actual + counterfactual + delta dimensions, emit a typed `CycleReceipt`, write under `orgs/<org_slug>/vault/operational/cycle_receipts/<cycle_id>.json` via the §2 Vault write intent, and (if operator-attested) emit the buyer-facing PDF.

**Inputs (Pydantic `CycleAccountantInput`, frozen, kw_only):**
- `run_id: str`
- `cycle_id: str`
- `org_slug: str`
- `cycle_close_marker_span_id: str` — span ID emitted by §5 v8 dispatcher at submission_mode terminal state
- `logfire_export_path: str` — local path to Logfire span tree export for the cycle
- `classification_register_version: str` — SHA3-512 of operator-signed register at cycle start
- `coefficient_registry_path: str` — defaults to `vault_shared/wpfa/coefficient_registry/active.yaml`
- `dimensions_requested: tuple[str, ...]` — defaults to `("dollars", "energy")` at v0.1; refused for any other tuple per `F-WPFA-DIMENSION-UNSUPPORTED`
- `operator_attestation_requested: bool` — if True, prompt operator for Ed25519 signing at end of emission
- `invoked_at_utc: datetime`

**Outputs:**
- `orgs/<org_slug>/vault/operational/cycle_receipts/<cycle_id>.json` (CycleReceipt as canonical JSON)
- (if `operator_attestation_requested == True` AND operator signs) `orgs/<org_slug>/wpfa_artifacts/<cycle_id>.pdf` (buyer-facing PDF per §8)
- `pipeline/institutional_memory/wpfa_state/<run_id>.yaml` (Rule 1 Save State Always — success + failure paths)
- `pipeline/validation/wpfa_rejects/<run_id>/` (gate-fail audit trail per §15 precedent)

**Determinism mandate:** same Logfire export + same Coefficient Registry version → byte-identical canonical-JSON output. Decimal arithmetic via the explicit-context-required helper per v7.0.4-M1 §6; ROUND_HALF_EVEN rounding to fixed precision before integer cast.

**Always-local routing:** Cycle Accountant is always-local per v7.0.7 routing posture (the input substrate is the Logfire span tree, which carries Confidential trace content). Cycle Accountant joins with classification register before emission and ensures no Confidential content leaks into the buyer-facing PDF (per F-CLASS-OUTBOUND-BOUNDARY family + new F-WPFA-PDF-CONFIDENTIAL-LEAK gate; see §6).

# §6. F-WPFA-* failure-code family (§4 v2.x.z follow-on amendment seed)

Following the §4 v2.x format (tier / module / severity / §ref columns) and the F-CLASS-* + F-REFLECTION-* family naming conventions, this spec proposes **twelve F-WPFA-* failure codes**. The §4 v2.x.z amendment registers them; module skeletons land at `pipeline/logician/gates/`; Cedar predicate bodies land at WS-WPFA follow-on.

| Code | Tier | Module (proposed) | Severity | Rationale / Trigger |
|---|---|---|---|---|
| `F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED` | PRE-load | `f_wpfa_coefficient_registry_unsigned.py` | P0 (trust mechanism) | Registry loaded without a `sn_llc_signature_ed25519` field, or field is empty. Mirrors `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` (v7.0.7) at the registry layer. M13 audited. |
| `F-WPFA-COEFFICIENT-SIGNATURE-INVALID` | PRE-load | `f_wpfa_coefficient_signature_invalid.py` | P0 | Registry signature does not verify against white-glove-pinned SN-LLC pubkey. Deployment stays on prior pinned version. Sub-tags `.pubkey_mismatch`, `.signature_bytes_invalid`, `.canonical_json_mismatch`. M13 audited. |
| `F-WPFA-MODEL-COEFFICIENT-MISSING` | PRE-emission | `f_wpfa_model_coefficient_missing.py` | HIGH | Span tree references a `model_id` that has no entry in the loaded Coefficient Registry. Common cause: operator added a new local model SKU without updating the registry. Sub-tags `.unknown_model_id`, `.deprecated_model_referenced`. M13 audited. |
| `F-WPFA-BASELINE-MISSING` | PRE-emission | `f_wpfa_baseline_missing.py` | HIGH | Counterfactual baseline not set for the cycle's quarter (registry's `baseline_model_id` is unset or does not resolve to an entry in the registry's `entries` tuple). Cannot compute counterfactual → cannot emit receipt. M13 audited. |
| `F-WPFA-SPAN-PROVENANCE-MISSING` | PRE-emission | `f_wpfa_span_provenance_missing.py` | HIGH | Any quantitative claim in the receipt (`actual.dollars_total`, per-model row, `counterfactual.*`, `delta.*`) does not carry an originating `trace_id` / `span_id` in `span_provenance.per_claim_span_ids`. Mirrors `F-REFLECTION-SPAN-PROVENANCE-MISSING` (sibling artifact). Sub-tags `.no_trace_id`, `.trace_id_unresolvable_in_logfire`, `.claim_key_unmapped`. M13 audited. |
| `F-WPFA-COUNTERFACTUAL-INFLATION` | PRE-emission | `f_wpfa_counterfactual_inflation.py` | P0 (audit integrity) | Counterfactual computed using a baseline model NOT actually in the SN-LLC-signed registry — defends against deployment-side number inflation (a malicious deployment that quietly substitutes a high-cost flagship to inflate the savings claim). PRE-gate verifies `baseline_model_id` matches `coefficient_registry.baseline_model_id` exactly. M13 NOT bypassable for buyer-attested receipts; internal-only receipts permit M13 with HIGH-severity admin-risk entry. |
| `F-WPFA-OPERATOR-SIGNATURE-MISSING` | PRE-PDF-emit | `f_wpfa_operator_signature_missing.py` | HIGH | Buyer-facing PDF artifact emission attempted without `signed_by_operator_ed25519` set on the source receipt. PDF emission fail-closes. Internal-only dashboard surfaces are unaffected. Sub-tag `.pdf_emission_without_attestation`. M13 NOT permitted (this is the structural attestation boundary; M13 would defeat the purpose). |
| `F-WPFA-DIMENSION-UNSUPPORTED` | PRE-emission | `f_wpfa_dimension_unsupported.py` | HIGH | Receipt asserts a dimension (water/CO2) not in `dimensions_active` for this schema version, OR `dimensions_active` at v0.1 contains anything other than `("dollars", "energy")`. Defends against premature v0.2 dimension surfacing. Sub-tags `.water_at_v0_1`, `.co2_at_v0_1`, `.unknown_dimension`. M13 audited. |
| `F-WPFA-REGISTRY-DRIFT` | POST-load (advisory) | `f_wpfa_registry_drift.py` | MEDIUM (advisory) | Local hardware measurement deviates >X% from SN-LLC registry coefficient for the same SKU (advisory threshold operator-tunable; default X=20%). Surfaces measurement-vs-publication mismatch — does NOT fail-close pipeline. Sub-tags `.idle_watts_drift`, `.peak_watts_drift`, `.watt_hours_per_million_drift`. M13 NOT needed (advisory). |
| `F-WPFA-SCHEMA-INVALID` | PRE-write + POST-read | `f_wpfa_schema_invalid.py` | HIGH | Schema validation failure (any of the 17 invariants in §3.2) at write OR at decode round-trip. Sub-tags `.numeric_field_float`, `.classification_register_version_invalid`, `.dimensions_active_invalid`, `.per_model_aggregate_mismatch`, `.delta_arithmetic_mismatch`, `.semver_version_invalid`. Mirrors `F-OPERATIONAL-SCHEMA-INVALID` (§2 v7.2 §7). M13 audited. |
| `F-WPFA-CROSS-ORG-LEAK` | PRE-write | `f_wpfa_cross_org_leak.py` | P0 (Law 3) | Any CycleReceipt write whose path resolves to `orgs/<other_slug>/vault/operational/cycle_receipts/...`. Defense-in-depth on top of `operational_org_isolation.cedar` Rule 1. Mirrors `F-OPERATIONAL-ORG-MISMATCH` from §2 v7.2. No M13 bypass. |
| `F-WPFA-PDF-CONFIDENTIAL-LEAK` | PRE-PDF-emit | `f_wpfa_pdf_confidential_leak.py` | P0 (Law 3 + v7.0.7) | Buyer-facing PDF emission attempts to render any field value whose classification register entry is `confidential` (e.g., the operator forgot to opt the `goal_name`-equivalent field as `shareable` and the PDF would have rendered Confidential text). PRE-gate scans PDF content against classification register; fail-closes if Confidential content detected. Sub-tags `.confidential_field_in_pdf`, `.classification_register_unread_at_emit`. M13 NOT bypassable for buyer-attested artifacts. |

**OQ-4 (operator-decision):** module decomposition — keep one module per code (12 modules, clean ownership) OR collapse F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED + F-WPFA-COEFFICIENT-SIGNATURE-INVALID + F-WPFA-COEFFICIENT-ROLLBACK-INVALID into a single `f_wpfa_coefficient_registry_validation.py` (3 sub-codes; matches §4 v2.x F-AMDT-08/09/10/11 + F-CLASS-* sub-code-collapse precedent). Default: **collapse the three coefficient-registry-validation codes into one module** (closer to precedent); keep the rest one-module-per-code. Final module count under default: 10 modules realizing 12 codes.

**OQ-5 (operator-decision):** should `F-WPFA-REGISTRY-VERSION-DRIFT` (mentioned in §4.4) be a 13th gate? Default: yes, as advisory POST-emission gate; sub-tag of F-WPFA-REGISTRY-DRIFT. Final code count under default: 12.

**Composition with F-CLASS-COVERAGE-INCOMPLETE META gate (per L-006 dormant-binding pattern):** the META gate's `REQUIRED_F_CLASS_CODES` registry currently covers F-CLASS-* only. **OQ-6 (operator-decision):** should F-WPFA-* join the META gate's coverage? Default: **exclude** — F-WPFA-* is its own family, the META gate stays focused on F-CLASS-*. Document explicitly in §6 of the §4 v2.x.z amendment why F-WPFA-* is out of META scope.

# §7. §0.5 v17 amendment — row range allocation (conditional on Funding Goal LOCK ordering)

Current runtime-live total at §13 LOCK = **376**. Funding Goal spec card 2026-05-10 allocates rows 377–399 (23 rows). **Two ordering scenarios:**

**Scenario A — Funding Goal LOCKs first (runtime-live becomes 399 before WPFA).**
WPFA row allocation = **rows 400–419 (20 rows)**:

| Row | primitive_id | kind | parent |
|---|---|---|---|
| 400 | `blueprint.section_anchor.s17_wpfa.v1` | marker | §17 v1 |
| 401 | `vault.sub_kinds.cycle_receipt.v1` | schema | `CycleReceipt` frozen kw_only |
| 402 | `vault.sub_kinds.cycle_receipt.dimension_totals.v1` | schema | `CycleReceiptDimensionTotals` |
| 403 | `vault.sub_kinds.cycle_receipt.per_model_call.v1` | schema | `PerModelCall` |
| 404 | `vault.sub_kinds.cycle_receipt.delta.v1` | schema | `CycleReceiptDelta` |
| 405 | `vault.sub_kinds.cycle_receipt.span_provenance.v1` | schema | `SpanProvenance` |
| 406 | `vault.sub_kinds.cycle_receipt.canonical_codec.v1` | interface-contract | `to_canonical_bytes`/`from_canonical_bytes` |
| 407 | `vault.sub_kinds.registry.cycle_receipt_descriptor.v1` | interface-contract | `SUB_KIND_REGISTRY["cycle_receipt"]` row |
| 408 | `vault.policy.operational_subkinds.cedar.cycle_receipt_org_isolation.v1` | interface-contract | Cedar rule extension |
| 409 | `vault.policy.operational_subkinds.cedar.cycle_receipt_operator_attestation.v1` | interface-contract | Cedar rule for operator-Ed25519 attestation |
| 410 | `vault.post_gate_allowlist.operational-cycle-receipt-write.v1` | interface-contract | §2.13 allowlist row |
| 411 | `wpfa.coefficient_registry.v1` | schema | `CoefficientRegistry` |
| 412 | `wpfa.coefficient_registry.entry.v1` | schema | `CoefficientEntry` |
| 413 | `wpfa.coefficient_registry.sn_llc_signature_verify.v1` | interface-contract | Ed25519 verify callable (mirrors v7.0.7 §6.1) |
| 414 | `wpfa.cycle_accountant.compose_receipt.v1` | interface-contract | `compose_receipt(input) → CycleReceipt` deterministic callable |
| 415 | `wpfa.dashboard.per_org_rollup.v1` | interface-contract | Cowork HTML artifact spec (§8 below) |
| 416 | `wpfa.dashboard.per_quarter_rollup.v1` | interface-contract | per-quarter aggregation read |
| 417 | `wpfa.pdf_artifact.buyer_facing_template.v1` | interface-contract | per §8 below |
| 418 | `wpfa.pipeline.cycle_close_emission_hook.v1` | interface-contract | §5 v8 cycle-close marker → Cycle Accountant trigger |
| 419 | `logician.failure_code.F-WPFA-*.v1` (12 codes — register one row per code; rows 419 → 419+11 = 430 if expanded) | failure-code | per §6 |

**Correction to scenario A row count.** If each F-WPFA-* code gets its own row (per §0.5 explode-per-failure-code precedent — §10 / §11 / §12 / §13 / §15), the total row count is **20 non-failure-code rows + 12 failure-code rows = 32 rows**. **Revised scenario A allocation: rows 400–431 (32 rows).**

**Scenario B — WPFA LOCKs first (runtime-live still 376 before WPFA, Funding Goal pending).**
WPFA row allocation = **rows 377–408 (32 rows)**. Funding Goal would re-allocate downstream to start at 409.

**Recommended default ordering:** Funding Goal LOCKs first (Funding Goal is closer to v0.2 first-wave per its spec card OQ-1 default; WPFA is operator-LOCKED for v0.1 Beta per today's directive). Scenario A allocation applies — **rows 400–431 (32 rows)**.

**§0.5 vocabulary check:** every row resolves against the v5 + v6 closed vocabulary (marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check). NO vocabulary extension required.

**Parent-wins discipline:** each row's `parent_lock_version` + `parent_lock_commit_hash` point at §17 v1 (rows 400–410 + 414–418), Coefficient Registry signed-asset amendment (rows 411–413), §4 v2.x.z (rows 419–430 + 431).

# §8. Buyer-facing PDF artifact + operator-facing dashboard

## §8.1 Buyer-facing PDF — quarterly receipt template

**Purpose:** sales-lever artifact for board reports, grant reports, sales conversations. Renders an operator-attested CycleReceipt (or quarterly rollup of attested receipts) into a brand-consistent PDF.

**Template structure (proposed sections):**
1. **Header.** Golden Quill mark + tagline "Golden Quill — regenerative grant intelligence." Operator-defined client name (FIT Farms, etc.). Quarter + cycle_id(s). Operator attestation ribbon ("Attested by [operator] on YYYY-MM-DD").
2. **The headline.** Single-sentence claim: "In Q2 2026, [client] saved $X / Y kWh by routing Z% of grant-cycle inference to member-owned hardware." Each numeric value carries a footnote-style superscript linking to the methodology citation (§4.1 `CoefficientEntry.methodology_url`).
3. **Per-cycle breakdown table.** One row per cycle in the quarter: cycle_id · grant identifier · actual dollars/kWh · counterfactual dollars/kWh · delta dollars/kWh · trace_id reference.
4. **Per-model breakdown table.** One row per distinct model_id used in the quarter: model_id · is_local · hardware_sku · tokens · dollars · watt-hours.
5. **Methodology footer.** Coefficient registry version (SHA3-512) · SN-LLC pubkey id · methodology_url · operator pubkey id · receipt file path(s) for audit.
6. **Auditability block.** "Every dollar and watt-hour in this report links to a published coefficient + cycle_id + Logfire trace_id. Methodology is open; calculation code is proprietary. Methodology document: [URL]." Note that v0.2 expansion to water + CO2 will follow the same auditability discipline; v0.1 ships dollars + energy only.

**Brand consistency requirements (from assets/cards/customer_identification/ + assets/website/about.md idiom):**
- Parchment-card aesthetic per CIC card families (assets/cards/customer_identification/*.png).
- Brand thesis sentence per locked website: "Strong organizations are not short on substance — they lack funding infrastructure." Quote as footer subhead OR omit (operator-tunable).
- Typography matches website palette per assets/website/about.md (read at build time).
- Single-page-per-quarter default; multi-page if breakdown tables overflow.

**Auditability mandate.** Every dollar/kWh claim in the PDF MUST link back to: (a) the Coefficient Registry version (SHA3-512); (b) the cycle_id(s) covered; (c) at least one Logfire trace_id per claim. Failing any link → `F-WPFA-PDF-AUDITABILITY-BROKEN` (NEW gate — propose adding).

**OQ-7 (operator-decision):** is `F-WPFA-PDF-AUDITABILITY-BROKEN` a 13th F-WPFA-* code, or covered under F-WPFA-SPAN-PROVENANCE-MISSING via sub-tag? Default: cover under F-WPFA-SPAN-PROVENANCE-MISSING sub-tag `.pdf_claim_unlinked` (closer to existing structure).

**Generation surface (v0.1).** PDF generation via Pydantic AI tool wrapping a pure-Python PDF builder (reportlab or weasyprint; substrate decision per ADR-001 substrate-frozen-at-golden-image discipline). Always-local. No external rendering service.

**Source path:** template at `pipeline/orchestrator/seats/wpfa/templates/buyer_facing_pdf.html` (rendered to PDF by always-local generator) OR direct reportlab generator at `pipeline/orchestrator/seats/wpfa/pdf_emitter.py`. **OQ-8 (operator-decision):** which generation substrate? Default: weasyprint (HTML→PDF; easier to maintain brand-consistent CSS shared with future website surfaces; needs operator-confirmed inclusion in Golden Image build per ADR-001 substrate-frozen discipline).

## §8.2 Operator-facing dashboard — Cowork HTML artifact

**Purpose:** transparent operator-facing surface for per-org, per-quarter, per-fleet rollups.

**Pattern:** Cowork artifact (HTML rendered via `mcp__visualize__show_widget` or equivalent). Reads from disk-state files only — never invokes external APIs, never writes back. Pure read.

**Three rollup tiers (v0.1 ships per-org + per-quarter; per-fleet is Stage-2+):**
1. **Per-org rollup.** For a given `org_slug`, list all CycleReceipts in date order. Show cumulative dollars saved + watt-hours saved. Operator-attested receipts highlighted. Internal-only receipts visible but not exportable to PDF.
2. **Per-quarter rollup.** For a given `quarter` tag (e.g., Q2-2026), aggregate across all orgs the operator owns. Workspace-aggregate discipline per §15.2 Law 3 enforcement (operator IS the multi-org actor; aggregate statistics permitted; per-org content does NOT leak across orgs).
3. **Per-fleet rollup (Stage-2+).** Across all Tilth deployments in the cooperative (12-Tilth fleet milestone). OUT OF SCOPE for v0.1 + v0.2; surfaced as `[Stage-2+]` placeholder card in v0.1 dashboard.

**On-disk read pattern:** dashboard reads `orgs/<slug>/vault/operational/cycle_receipts/*.json` + `vault_shared/wpfa/coefficient_registry/active.yaml` only. No write capability. Refresh = re-read on operator request.

**Cheap pre-stage discipline:** the dashboard is a Cowork artifact spec, not a separate amendment. The §17 v1 spec text describes the read pattern + rollup logic + classification-respecting display rules; the actual artifact authoring happens at Code-phase per WS-WPFA.

# §9. Cedar policy additions

Lives at `pipeline/vault/policies/operational_subkinds.cedar` (extending the v7.2 file). Two new rules + one extension:

1. **Extension to `operational_org_isolation`:** add `sub_kind == "cycle_receipt"` to the default-permit set so cycle-receipt writes match the per-org isolation rule with no new rule required. F-WPFA-CROSS-ORG-LEAK at the Logician layer is defense-in-depth.
2. **`cycle_receipt_operator_attestation`:** permits buyer-facing PDF emission ONLY when `signed_by_operator_ed25519` is non-None AND the signature verifies against the white-glove-pinned operator pubkey. Falls through to implicit deny → F-WPFA-OPERATOR-SIGNATURE-MISSING. Operator key rotation requires co-signing per v7.0.7 §6.1 pattern.
3. **`cycle_receipt_read_isolation`:** permits reading a CycleReceipt under `orgs/<slug>/vault/operational/cycle_receipts/...` only when the requesting principal's `org_slug` attribute matches the path's `<slug>` OR when the requesting principal is `wpfa_dashboard_workspace_aggregate` (the Stage-1 operator-as-multi-org-actor principal — per §15.2 Law 3 workspace-aggregate carve-out). Implicit deny otherwise → F-WPFA-CROSS-ORG-LEAK.

The Python evaluator at `pipeline/vault/sub_kinds/policy_eval.py` is authoritative at v0.1 per §2 v7.1 §3.4 + v7.2 §6 lifecycle.

# §10. §7 Invariants — receipt emission discipline

Per §7 (Sovereignty Envelope) invariants pattern, this spec proposes the following invariants for receipt emission. **These are §7 amendments candidates, not §17 internal invariants — the cycle-receipt-emission discipline crosses the Sovereignty Envelope boundary.**

- **§7.NN-1 — Receipt emission MUST be deterministic.** Same Logfire export + same Coefficient Registry version → byte-identical canonical-JSON output. Re-runs must reproduce.
- **§7.NN-2 — Receipt without operator signature is internal-only.** Buyer-facing PDF emission requires operator Ed25519 attestation. F-WPFA-OPERATOR-SIGNATURE-MISSING PRE-emission gate enforces.
- **§7.NN-3 — Receipt content is org-isolated.** Per §17 + Cedar `cycle_receipt_org_isolation` rule extension. F-WPFA-CROSS-ORG-LEAK PRE-write gate enforces.
- **§7.NN-4 — Every claim traces to a Logfire span.** F-WPFA-SPAN-PROVENANCE-MISSING PRE-emission gate enforces.
- **§7.NN-5 — Counterfactual references SN-LLC-signed registry baseline.** F-WPFA-COUNTERFACTUAL-INFLATION PRE-emission gate enforces.

**OQ-9 (operator-decision):** are these §7 amendments (§7 numbering carved out) or §17 internal invariants? Default: §7 amendments — receipt-emission discipline IS a Sovereignty Envelope-class concern (it crosses the org-isolation + operator-attestation + cloud-vs-local boundaries that §7 owns).

# §11. §15 Archivist composition note (forward, not v0.1 dependency)

Per §15 v1 LOCK §15.0 cross-amendment composition map, Archivist reads workspace-shared substrates quarterly. WPFA quarterly rollups (per-org cumulative + workspace-aggregate) ARE workspace-shared read substrates Archivist could compose into its quarterly digest.

**Future composition (NOT v0.1 dependency):**
- Archivist v1.x quarterly digest MAY include a "Regenerative-savings rollup across the quarter" section sourced from WPFA per-quarter aggregates.
- F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT (§15.9.5) extends with new wrapper `vault_read_intent_wpfa_quarterly`; F-ARCHIVIST-CROSS-ORG-LEAK applies (Archivist reads workspace-aggregate, not per-org-content).
- Archivist's pattern-detection prompt (v1.x) does NOT process individual receipts; it reads pre-aggregated quarterly rollups.

**Out of scope for v0.1 + v0.2.** This composition is a v1.x forward-design marker. Archivist v0.2 SPEC LOCK does not need WPFA-side amendment.

# §12. v0.1 vs v0.2 boundary table

| Element | v0.1 Beta | v0.2 first wave | v1.x / horizon |
|---|---|---|---|
| `CycleReceipt` schema + sub-kind registry row | **v0.1 Beta** — per operator LOCKED-2026-05-10 directive | — | — |
| Coefficient Registry signed-asset class | **v0.1 Beta** — SN-LLC publishes inaugural Q3-2026 registry; white-glove pins SN-LLC pubkey at onboarding | Quarterly cadence (per v7.0.7 §6.1 router-template parallel); 7-day emergency updates | — |
| Cycle Accountant module | **v0.1 Beta** — emits CycleReceipt at cycle close per §5 v8 marker | — | — |
| F-WPFA-* failure-code family (12 codes) | **v0.1 Beta** — paired with §17 v1 LOCK; predicate bodies live (not skeleton) | — | — |
| Operator-facing dashboard (per-org + per-quarter) | **v0.1 Beta** — Cowork HTML artifact reading from disk | — | — |
| Buyer-facing PDF artifact (per cycle + per quarter) | **v0.1 Beta — operator-LOCKED sales lever, NOT deferred** | — | — |
| Operator Ed25519 attestation flow | **v0.1 Beta** — TTY-gated CLI surface per Intake §11.7 precedent | — | — |
| Per-fleet (Stage-2+) rollup | — | — | **Stage 2 (12-Tilth fleet milestone)** — multi-deployment aggregation; out of scope for v0.1 + v0.2 |
| Water dimension | — | **v0.2** — `dimensions_active` extends to `("dollars", "energy", "water")` once Coefficient Registry adds per-model water-consumption coefficients; methodology document peer-review may be operator-required at v0.2 ship | — |
| CO2 dimension | — | **v0.2** — same pattern as water; SN-LLC publishes per-model CO2-equivalent coefficients; per-region grid-mix lookups deferred to v1.x | — |
| Peer review of methodology | — | **v0.2 candidate** — operator-decision per foundation-funder pressure; methodology document at stable URL is the v0.1 ship; formal peer review is a v0.2 enhancement | — |
| Stage-5 commons consent-tier wpfa aggregation | — | — | **Stage 5** — cooperative-owned compute commons; per consent tier; out of scope per v7.0.5 §4 on-ramp |
| Archivist v1.x composition (quarterly digest WPFA rollup section) | — | — | **v1.x** — per §11 above |
| Dashboard scheduled-refresh (vs operator-on-demand) | — | **v0.2** — scheduled-task per the `schedule` skill pattern | — |
| Multi-currency support | — | **v0.2** — v0.1 ships USD-only; FX handling deferred | — |
| Tilth-side coefficient measurement (vs SN-LLC-published only) | — | — | **v1.x** — operator runs on-hardware energy measurement; F-WPFA-REGISTRY-DRIFT surfaces deviation; full operator-measured coefficient pathway is v1.x |

# §13. L-005 two-cycle Thesis discipline notes

Per `/AGENTS.md` § "Cross-family review — bridge pattern" and recent precedents (rows 178–197), this amendment family requires:

- **Cycle 1 (driver):** Editor (Llama 3.3 70B / Groq, Meta family) + Judge (Gemini 2.5 Pro / Google) + Red Team (GPT-OSS 120B / Groq, OpenAI-OSS family). Three live model IDs per /AGENTS.md. Templates: `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`.
- **Cycle 2 (verification):** same three reviewers on a delta-review packet per `pipeline/engineering/engineering_process_v0.1.md` §7. NEW probes (mirroring recent precedents) follow row-170 transparent disposition — FOLD-IN at LOCK with explicit text-level mechanisms OR forward-track to a follow-on minor amendment.
- **Section E carve-out:** NOT invoked unless a logged dispatch failure per `/AGENTS.md` § "Section E carve-out — invocation discipline".
- **L-006 dormant-binding hook:** F-CLASS-COVERAGE-INCOMPLETE META gate checks the F-WPFA-* family's coverage IF OQ-6 selects "include F-WPFA-* in META gate". Default: exclude (per §6 OQ-6 default).
- **Sibling-not-nested verification:** at every Thesis cycle, the audit prompt's "sibling artifact discipline" rubric MUST verify the WPFA emission path does NOT consume Reflection Packet output, and vice versa. Coupling would violate the sibling pattern.
- **A12 Decimal-mandate extension to energy.** This spec extends A12 from "money only" to "money AND energy quantities" — the Thesis Team MUST audit this extension explicitly; if rejected, the spec falls back to milli-Wh integer (still A12-compliant; less precision).
- **Coefficient Registry trust mechanism mirroring v7.0.7 §6.1.** Thesis Team MUST verify the SN-LLC signing mechanism, white-glove pubkey pinning, Trust-On-First-Use rotation, and rollback protocol all mirror v7.0.7 §6.1 router-template discipline byte-for-byte. Deviation → escalate to operator.
- **Sales-lever scope check.** Thesis Team MUST verify the buyer-facing PDF artifact does not silently violate Law 3 (no per-org-content leakage in workspace-aggregate views) and Law 5 (no fabricated savings claims — every kWh links to a published coefficient + cycle_id + trace_id).

## §13.1 HARD-LOCKED elements (Thesis cannot relitigate)

- A12 Decimal mandate for `dollars_total_minor_units` (int minor units; no float) per v7.0.4-M1 §6.
- Sibling-not-nested pattern with Reflection Packet — both consume the same span tree at cycle close but share zero output/consumer (operator LOCKED 2026-05-10).
- v0.1 dimensions = dollars + energy ONLY; water + CO2 deferred to v0.2 (operator LOCKED 2026-05-10).
- Buyer-facing PDF is a v0.1 Beta sales lever, NOT deferred (operator LOCKED 2026-05-10).
- Coefficient Registry trust = SN-LLC Ed25519, white-glove-pinned pubkey, same mechanism as router-template (operator LOCKED 2026-05-10).
- `write-if-absent` discipline + canonical-JSON encode/decode round-trip per §2 v7.2 §1.
- Law 3 Org Isolation — receipts live under `orgs/<slug>/vault/operational/cycle_receipts/` per §2 v7.2 §5.
- Operator attestation is REQUIRED for buyer-external use; internal-only receipt is emitted but not signed.

## §13.2 OPEN QUESTIONS for the Thesis dispatch (Thesis-resolvable; operator-overridable)

- Energy quantization precision (§3.1 OQ-2: micro-Wh vs milli-Wh).
- Coefficient Registry rollback authority (§4.3 OQ-3: operator-direct vs SN-LLC-co-signed).
- F-WPFA-* module decomposition (§6 OQ-4: collapse coefficient-registry-validation triplet vs one-module-per-code).
- F-WPFA-REGISTRY-VERSION-DRIFT as separate gate (§6 OQ-5: yes or sub-tag under REGISTRY-DRIFT).
- F-WPFA-* in F-CLASS-COVERAGE-INCOMPLETE META gate registry (§6 OQ-6: include or exclude).
- F-WPFA-PDF-AUDITABILITY-BROKEN as separate code (§8.1 OQ-7: yes or sub-tag under SPAN-PROVENANCE-MISSING).
- PDF generation substrate (§8.1 OQ-8: weasyprint vs reportlab; both substrate-frozen-at-Golden-Image candidates).
- §17 invariants placement (§10 OQ-9: §7 amendment vs §17 internal).

# §14. DECISIONS-PENDING-CONFIRMATION (operator-proposed defaults flagged for Thesis or operator confirmation)

These are operator-proposed defaults from the orchestrator dispatch — flagged here so Thesis can either accept or surface for explicit operator override.

- **DPC-1 — Counterfactual baseline cadence: quarterly.** SN-LLC publishes a single named flagship reference model identity per quarter (e.g., "Q3 2026 baseline: claude-sonnet-4-6"). Counterfactual = "100% routed to quarterly flagship." Update cadence = quarterly (paired with router-template review). Emergency baseline change = 7-day cadence per v7.0.7 §6.1.
- **DPC-2 — Methodology disclosure level: open coefficients + methodology document at stable URL; calculation code stays proprietary.** Coefficients + citations + methodology document published openly at a stable URL Sovereign Node LLC maintains. The Cycle Accountant's calculation code (Python) remains proprietary. Open question: foundation-funder pressure may push toward formal peer review of the methodology document at v0.2; that decision deferred. Document this default explicitly in §17 §V or §VI so Thesis or operator can override.

# §15. OPEN QUESTIONS for Josh (operator-decision-required-first)

Each is framed with trade-offs so Josh can decide quickly.

**OQ-A — Section number for WPFA: §17 (default) or different?**
- §17 places WPFA after the Tilth-internal Archivist + Reflection Packet cluster (Reflection occupies §16). Topical clustering preserved; emission-orchestration adjacency at §16/§17; clean room for §16 sub-spec proliferation.
- §16 places WPFA before Reflection Packet — rejected unless Reflection Packet design defers to a later section number.
- §17.1 as sub-section of a unified cycle-close-emission §17 — rejected for v0.1 (independent failure-code families, independent consumers, independent classification postures).
- *Recommended default: §17.*

**OQ-B — §0.5 row range — 32 rows under Scenario A (Funding Goal LOCKs first, rows 400–431) or 32 rows under Scenario B (WPFA LOCKs first, rows 377–408)?**
- Scenario A aligns with Funding Goal spec card default (Funding Goal recommended for v0.2 first wave per its OQ-1; WPFA operator-LOCKED for v0.1 Beta per today's directive — so WPFA actually LOCKs first chronologically even though Funding Goal's spec lands first).
- Operator decision likely flips the ordering: WPFA LOCKs in v0.1 Beta cascade; Funding Goal LOCKs at v0.2 first wave. Scenario B applies.
- *Recommended default: Scenario B (rows 377–408) — WPFA LOCKs first.*

**OQ-C — Quarterly baseline cadence (DPC-1): accept default or change?**
- Default: quarterly + 7-day emergency updates, paired with router-template review.
- Alternative: monthly cadence (more frequent baseline updates → more accurate counterfactual but more operator overhead).
- Alternative: only-on-flagship-model-deprecation (most stable but lags model landscape evolution).
- *Recommended default: quarterly + 7-day emergency.*

**OQ-D — Methodology disclosure (DPC-2): accept default or push to peer review at v0.1?**
- Default: open coefficients + methodology document at stable URL; calculation code stays proprietary; peer review deferred to v0.2.
- Alternative: ship v0.1 with peer-reviewed methodology — slower v0.1 ship but stronger buyer-facing trust.
- Alternative: ship v0.1 with closed methodology (operator publishes coefficients only) — fastest v0.1 ship but weakest trust posture.
- *Recommended default: open + deferred peer review.*

**OQ-E — `F-WPFA-OPERATOR-SIGNATURE-MISSING` M13 bypass: NOT permitted (default) or M13-audited?**
- NOT permitted: structural attestation boundary; M13 would defeat the purpose of operator attestation as the buyer-trust mechanism.
- M13-audited: operator can bypass in extraordinary circumstances with HIGH-severity admin-risk-ledger entry.
- *Recommended default: NOT permitted (mirrors §11.7 four-layer defense for autopromote; the four-layer pattern is non-bypassable by design).*

**OQ-F — Internal-only (unsigned) receipts: emitted at every cycle close, or only when operator-attestation-requested == True?**
- Emitted at every cycle close (default proposed): operator dashboard always has fresh data; buyer-facing PDF only emits when operator explicitly attests; receipts in internal directory carry None signature.
- Emit-on-request only: operator must explicitly request even the unsigned receipt; lighter disk footprint but operator dashboard has gaps.
- *Recommended default: emit at every cycle close; PDF emission gated by attestation.*

**OQ-G — `CoefficientEntry.measurement_date` precision: date-only ('YYYY-MM-DD') or full datetime?**
- Date-only matches §2 v7.2 TimelineActivity `started_at` convention for date-bounded events.
- Datetime matches Logfire span timing precision.
- *Recommended default: date-only — coefficient measurement is a daily-bounded event, not a per-second event.*

**OQ-H — Per-fleet rollup placeholder in v0.1 dashboard: render `[Stage-2+]` card or omit entirely?**
- Render placeholder: signals roadmap to operator + future buyer audiences; preserves topology for Stage-2 transition.
- Omit entirely: cleaner v0.1 surface; operator decides when to enable.
- *Recommended default: render `[Stage-2+]` placeholder — preserves Stage-2 transition story for buyer-facing materials.*

**OQ-I — Re-emission discipline (correcting a buggy cycle): allow operator-direct re-emit + audit-ledger entry, or require full Thesis-style review for any re-emitted receipt?**
- Operator-direct + ledger: lightest weight; mirrors §2 v7.2 re-key path discipline.
- Thesis-style review: highest rigor; matches buyer-attested-document gravity but adds significant operator overhead.
- *Recommended default: operator-direct + ledger for internal-only receipts; full re-attestation flow + ledger for buyer-attested receipts (a re-emitted attested receipt requires the operator to re-sign, which is its own audit trail).*

**OQ-J — Dashboard refresh model: operator-on-demand only at v0.1, scheduled-refresh at v0.2?**
- Operator-on-demand only at v0.1: aligned with §15 Archivist v0.2 operator-driven cadence pattern.
- Scheduled-refresh at v0.1: dashboard auto-updates on cycle close; lighter operator overhead.
- *Recommended default: operator-on-demand at v0.1; scheduled-refresh at v0.2 (matches §15 cadence story).*

**OQ-K — Cross-org workspace-aggregate dashboard view: surface raw aggregate numbers (default per §15.2 carve-out) or require explicit operator-multi-org-principal flag at session start?**
- Raw aggregate numbers: matches §15.2 Law 3 workspace-aggregate carve-out — operator IS multi-org actor.
- Explicit flag: defense-in-depth against accidental cross-org viewing in a context where operator's screen might be visible to a client.
- *Recommended default: raw aggregate at v0.1; explicit flag at v0.2 with operator-set per-session.*

# §16. Pre-dispatch checklist (self-check before this spec is handed to a Thesis-dispatch session)

Per `pipeline/engineering/engineering_process_v0.1.md` §11 Done definition pattern:

- [x] §11 spec-card template followed (header + parent locks + dispatch_class + L-005 review note).
- [x] §2 v7.2 sub-kind convention followed exactly (frozen kw_only; canonical bytes codec; SUB_KIND_REGISTRY row; vault subtree; admin-risk severity; SIMPLE write-if-absent).
- [x] A12 Decimal mandate respected (no float fields; int minor units for dollars; int micro-Wh for energy; explicit-context-required helper; AST-lint ban referenced).
- [x] Sibling-not-nested pattern with Reflection Packet structurally enforced (zero shared output/consumer/schema; only shared span-tree input substrate).
- [x] Law 3 Org Isolation enforced at three layers (Cedar default-permit extension; F-WPFA-CROSS-ORG-LEAK defense-in-depth; vault subtree path).
- [x] v7.0.7 Classification-routing applied (F-WPFA-PDF-CONFIDENTIAL-LEAK guards PDF emission; classification register read at emission).
- [x] §0.5 row range allocated correctly with both scenario A and scenario B conditional allocations.
- [x] L-005 two-cycle Thesis discipline notes flagged (HARD-LOCKED vs OPEN QUESTIONS vs DECISIONS-PENDING-CONFIRMATION).
- [x] v0.1 vs v0.2 boundary table explicit; water + CO2 deferred; buyer-facing PDF in v0.1 Beta per operator LOCK.
- [x] Open questions for Josh enumerated with trade-offs and recommended defaults.
- [x] No Python written (SPEC, not implementation).
- [x] No LOCK ceremony invoked.
- [x] Path-only references (no content dumps of locked sections per L-002).
- [x] Section number proposed with rationale (§17; OQ-A enumerates alternatives).
- [x] Coefficient Registry trust mechanism mirrors v7.0.7 §6.1 router-template Ed25519 signing exactly.
- [x] Operator attestation as load-bearing buyer-trust boundary; F-WPFA-OPERATOR-SIGNATURE-MISSING is structural.

# §17. Changelog

- 2026-05-10 v1 DISPATCH_SPEC_DRAFT filed. Grounded in v7.0.4-M1 + v7.0.5 + v7.0.7 LOCKED architecture; §2 v7.2 + §4 v2.x + §5 v8 + §15 v1 + §13 v1 LOCKED blueprints; Reflection Packet research findings 2026-05-10; Funding Goal spec card 2026-05-10. Section number proposal: §17. §0.5 row allocation: conditional 32 rows (Scenario A 400–431 OR Scenario B 377–408). F-WPFA-* family: 12 codes default; module count 10 under recommended OQ-4 collapse. Buyer-facing PDF artifact: v0.1 Beta scope per operator LOCK. Awaiting operator OQ-A through OQ-K dispositions; awaiting Thesis dispatch for OQ-1 through OQ-9.
