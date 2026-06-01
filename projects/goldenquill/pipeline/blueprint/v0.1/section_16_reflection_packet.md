---
title: §16 Reflection Packet — v0.1 Beta hook artifact spec (LOCKED 2026-05-15)
filed: 2026-05-15
operator: Josh Inklovich
status: LOCKED 2026-05-15 — compound paired-commit (sibling 1/3) with §4 v2.x.y F-PACKET-* + §0.5 v22 at the same `lock_timestamp_utc` per §6.17 Option-B. L-005 strict two-cycle Thesis CLOSED with FULL LIVE CROSS-FAMILY rigor (Editor=groq/llama-3.3-70b-versatile + Judge=google/gemini-2.5-pro + Red Team=groq/openai/gpt-oss-120b via openclaw gateway bridge). Thirteenth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor (after WS-D / WS-F / WS-E / WS-H / WS-G / WS-K / WS-C-M1 / WS-L / WS-I / WS-J / WS-Reflection v0.1 hook / WS-WPFA / §11 v1.1 / WS-FG). v0.1 Beta hook DORMANT scope per OQ-2 (a) — schema + signing primitives + 19 F-PACKET-* predicate signatures at architectural-primitive layer; predicates 1-18 NotImplementedError; predicate 19 (F-PACKET-COVERAGE-INCOMPLETE) LIVE META-gate.
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                             # v7 LOCKED 2026-04-19 A1–A12; A12 Decimal mandate; A1 single-client; A4 operator-trusted
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md                      # v7.0.4-M1 LOCKED row 190 — canonical-JSON Ed25519 signing regime mirrored byte-for-byte
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                         # v7.0.7 LOCKED row 180 — classification-driven routing + opaque slot discipline
  - pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md                         # v7.0.9 LOCKED row 202 — Reflection sub-mode v0.1 hook (PRODUCER) sibling at architectural-primitive layer
  - pipeline/blueprint/v0.1/section_02_v7_2_amendment.md                                # §2 v7.2 LOCKED rows 186/187 — sub-kind registry convention; SUB_KIND_REGISTRY entry DEFERRED to v0.2
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                                # §4 v2.x LOCKED rows 193/194 — failure-code family registration pattern; META-gate dormant-binding lever
  - pipeline/blueprint/v0.1/section_04_logician_v2_x_2_amendment.md                     # §4 v2.x.2 LOCKED row 203 — F-REFLECTION-* family (producer-side); F-PACKET-* MUST NOT collide
  - pipeline/blueprint/v0.1/section_15_archivist.md                                     # §15 v1 LOCKED rows 191/192 — proposes-only Archivist; F-ARCHIVIST-* parents
  - pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md                      # §17 v1 LOCKED rows 205-208 — WPFA sibling artifact; §17.6 F-PACKET-SPAN-PROVENANCE-MISSING forward-reference resolves at this LOCK
  - pipeline/blueprint/v0.1/section_11_intake_v1_1_amendment.md                         # §11 v1.1 LOCKED rows 209/210
  - pipeline/blueprint/v0.1/section_02_v7_5_funding_goal_amendment.md                   # §2 v7.5 LOCKED rows 211-214 — most-recent compound LOCK prior to this one
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_04_v2_x_y_packet_amendment.md  # paired-commit sibling 2/3
companion_interface_index_amendment: pipeline/blueprint/v0.1/section_00_5_section_16_packet_amendment.md  # paired-commit sibling 3/3
compound_lock_with: section_04_v2_x_y_packet_amendment.md + section_00_5_section_16_packet_amendment.md
parent_lock_rows: 205 (§17 v1 sibling at artifact layer); 194 (§4 v2.x predicate-signature parent); 186 (§2 v7.2 sub-kind convention parent)
amendment_class: new-section-with-DORMANT-predicate-bodies-and-LIVE-META-gate
ws_dispatch: WS-Reflection Packet v0.1 Beta hook
review_discipline: L-005 strict two-cycle; FULL live cross-family per /AGENTS.md
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out)
session_metrics: pipeline/metrics/session_log.jsonl
sibling_artifact: §17 WPFA CycleReceipt — zero shared output / consumer / schema / gate-family; one cross-reference at F-PACKET-SPAN-PROVENANCE-MISSING ↔ F-WPFA-SPAN-PROVENANCE-MISSING (sibling pattern)
sibling_producer: §15 Archivist Reflection sub-mode (v7.0.9 / §4 v2.x.2) — F-REFLECTION-* gates PRODUCER behavior; F-PACKET-* gates the ARTIFACT this producer emits; orthogonal owners
naming_reconciliation: pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md — Path B (separate F-PACKET-* family) adopted at this LOCK
oq_disposition_log: parent spec card §7 — all 6 SCOPING_DRAFT OQs RESOLVED 2026-05-11 by operator (OQ-1 §16; OQ-2 v0.1 Beta dormant hook; OQ-3 emit+backfill; OQ-4 no operator_notes; OQ-5 tolerant-reader + indefinite retention; OQ-6 cents-precision)
---

# §16 Reflection Packet — v0.1 Beta hook artifact spec

## §16.0 Why this section exists

Reflection Packet is the typed Pydantic artifact the §15 Archivist Reflection sub-mode emits once per grant cycle close (with a BACKFILL packet at decision-observed event per OQ-3 emit+backfill discipline §16.3). It carries gate-pass counts, score signals, pattern observations, proposed lessons, cycle outcome, and per-claim Logfire span provenance, signed by the producer seat with Ed25519 against a white-glove-pinned pubkey, optionally co-signed by the operator for outcome-bearing packets.

**Sibling-not-nested with WPFA CycleReceipt.** Both artifacts emit at cycle close. Both consume the same Logfire span tree. Zero shared output, zero shared consumer, zero shared schema field, zero F-* code crossing. WPFA goes to operator dashboard + buyer-facing PDF (external accounting). Reflection Packet goes to the Archivist learning loop (Tilth-internal). One cross-reference only at F-PACKET-SPAN-PROVENANCE-MISSING ↔ F-WPFA-SPAN-PROVENANCE-MISSING (sibling pattern). This LOCK resolves §17 v1 §6.5 forward-reference (line 243 of section_17_watts_per_funding_action.md).

**Sibling-with-producer with §15 Reflection sub-mode.** The Reflection sub-mode is the sole producer of Reflection Packets. F-REFLECTION-* (17 codes at v7.0.9 + §4 v2.x.2 row 203) gates the producer's behavior. F-ARCHIVIST-* (5 codes + sub-tag extensions per §15 v1 row 192) gates the substrate write. F-PACKET-* (this section; 19 codes) gates the artifact validity. Three orthogonal gate-family owners enforce the closure.

**v0.1 hook dormant scope per OQ-2 (a).** Schema module authored at `pipeline/vault/sub_kinds/reflection_packets.py`; canonical-codec helpers + signing-protocol scaffolds + `__post_init__` invariant declarations live. Eighteen of nineteen F-PACKET-* predicates carry NotImplementedError bodies; the nineteenth (`F-PACKET-COVERAGE-INCOMPLETE`) carries a LIVE META-gate body that fail-closes any v0.2-first-wave deployment lacking realized predicate bodies for the other eighteen. SUB_KIND_REGISTRY entry is NOT registered at v0.1 hook; registration lands at v0.2 first wave compound LOCK paired with §15 v2.x Archivist Reflection sub-mode SPEC.

## §16.1 Section-numbering rationale (OQ-1)

Operator-confirmed §16 (2026-05-11). Honors WPFA spec card §2 reservation. §15 Archivist + §16 Reflection Packet form the Tilth-internal between-cycle preservation cluster; §17 WPFA is the operator-and-buyer-facing accounting boundary. Topical clustering preserved at the §-numbering layer.

## §16.2 ReflectionPacket schema

Following the §2 v7.2 sub-kind convention exactly: `@dataclass(frozen=True, kw_only=True)`; one record = one file; SIMPLE class; canonical-JSON codec + SHA3-512 hash + Ed25519 signature; `__post_init__` invariant validation; canonical-decode re-validate. At v0.1 hook scope, the schema module is authored at `pipeline/vault/sub_kinds/reflection_packets.py` but NOT registered in SUB_KIND_REGISTRY per OQ-2 (a).

### §16.2.1 Top-level shape

```python
@dataclass(frozen=True, kw_only=True)
class ReflectionPacket:
    # Identity + provenance
    packet_id: str                                       # opaque caller-minted ID; matches filename {packet_id}.json
    cycle_id: str                                        # foreign key into the cycle this packet records
    org_slug: str                                        # Law 3 binding; resolves to existing orgs/<slug>/ subtree
    schema_version: str                                  # semver "1.0.0" at v0.1 hook
    classification_register_version: str                 # SHA3-512 hash of operator-signed classification register at cycle start

    # Emission context
    emitted_at: str                                      # UTC ISO-8601 'Z'
    emitted_by_seat: str                                 # closed registry set; v0.1 = {"archivist.reflection_submode"}
    cycle_close_marker_span_id: str                      # Logfire span ID of the cycle-close marker

    # Pattern-level observations
    pattern_observations: tuple[PatternObservation, ...]
    lessons_proposed: tuple[ProposedLesson, ...]

    # Quantitative signals
    gate_pass_counts: GatePassCounts
    score_signals: ScoreSignals
    outcome: CycleOutcome

    # Grounding signal class declarations
    grounding_signal_classes: frozenset[str]              # ≥1 of the external/operator/logician/kfr/admin/match closed set

    # Provenance
    span_provenance: PacketSpanProvenance

    # Signing regime (per v7.0.4-M1 KFR canonical-JSON Ed25519 pattern — mirrors byte-for-byte)
    canonical_bytes_hash: str                              # 128 hex chars SHA3-512 (canonical-JSON minus signature fields)
    producer_signature_ed25519: str                        # 128 hex chars; verifies against white-glove-pinned producer pubkey
    operator_signature_ed25519: str | None                 # 128 hex chars when present; REQUIRED when outcome.status non-PENDING
```

### §16.2.2 Field sub-shapes

```python
@dataclass(frozen=True, kw_only=True)
class PatternObservation:
    pattern_summary: str                                  # pattern-LEVEL text only; instance-level refused per F-PACKET-INSTANCE-LEAK
    cic: str                                              # one of six CIC closed set
    clc: str                                              # one of eight CLC closed set
    frequency: int                                        # cycles in which the pattern surfaced; ≥1
    severity: str                                         # one of {"LOW", "MEDIUM", "HIGH"}
    first_observed_cycle_id: str
    supporting_span_ids: tuple[str, ...]                  # ≥1 Logfire span per observation


@dataclass(frozen=True, kw_only=True)
class ProposedLesson:
    lesson_id: str                                        # caller-minted opaque
    pattern_summary: str                                  # pattern-LEVEL text only
    proposed_rule: str                                    # actionable rule; NER + injection-scanner scope per F-PACKET-MEMORY-INJECTION
    frequency: int                                        # ≥2 OR severity="HIGH" per F-PACKET-PREMATURE-GENERALIZATION
    severity: str                                         # {"LOW", "MEDIUM", "HIGH"}
    supporting_pattern_observation_ids: tuple[str, ...]
    supporting_cycle_ids: tuple[str, ...]                 # ≥ frequency cycle_ids


@dataclass(frozen=True, kw_only=True)
class GatePassCounts:
    f_class_pass: int
    f_class_fail: int
    f_archivist_pass: int
    f_archivist_fail: int
    f_reflection_pass: int
    f_reflection_fail: int
    f_packet_pass: int
    f_packet_fail: int
    f_logician_total_pass: int
    f_logician_total_fail: int


@dataclass(frozen=True, kw_only=True)
class ScoreSignals:
    judge_score: int | None                                # 0-100 if observed; None if Judge did not score
    red_team_score: int | None
    editor_verdict: str | None                             # {"READY", "NEEDS_FIXES", "NOT_READY"} when present
    judge_red_team_divergence: int | None
    council_split_fired: bool
    cross_family_satisfied: bool


@dataclass(frozen=True, kw_only=True)
class CycleOutcome:
    status: str                                            # {"PENDING", "AWARDED", "DECLINED", "NO_DECISION"}
    funder_id: str | None
    award_amount_minor_units: int | None                   # int cents per A12 Decimal mandate + OQ-6 cents-precision
    award_currency: str | None                             # ISO-4217 alpha-3
    decision_observed_at: str | None                       # UTC ISO-8601 'Z'
    outcome_evidence_span_ids: tuple[str, ...]             # ≥1 when status non-PENDING


@dataclass(frozen=True, kw_only=True)
class PacketSpanProvenance:
    trace_ids: tuple[str, ...]                             # ≥1 Logfire trace IDs
    logfire_export_uri: str | None                         # optional pointer to offline-audit export bundle
    per_claim_span_ids: dict[str, tuple[str, ...]]         # claim_key → ≥1 span_id
```

### §16.2.3 Invariants (`__post_init__` + canonical-decode re-validate)

1. `cycle_id` MUST match `^[A-Za-z0-9_-]{1,128}$` per §17 cycle_id grammar precedent (RT-C2-05 fix-in-place mirrored); file-path-traversal defense for packet filename `{packet_id}.json` under `orgs/<slug>/vault/operational/reflection_packets/`.
2. `packet_id` MUST match `^[A-Za-z0-9_-]{1,128}$` (same grammar; filename binding).
3. `org_slug` MUST match `^[a-z][a-z0-9_]{0,63}$` (existing org-slug grammar; Unicode NFKC normalization at PRE-write per RT precedent).
4. `schema_version` MUST match semver `^\d+\.\d+\.\d+$`.
5. `classification_register_version` MUST be 128-hex SHA3-512 digest.
6. `emitted_at` and `decision_observed_at` (when non-None) MUST match UTC ISO-8601 `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$`.
7. `emitted_by_seat` MUST be in the closed registry set `{"archivist.reflection_submode"}` at v0.1; predicate signature for F-PACKET-PRODUCER-UNAUTHORIZED defends.
8. `pattern_observations[i].cic` MUST be one of the six closed CIC categories; `clc` one of the eight closed CLC cards. (Mirror of FG closed-set discipline.) No pre-mapped (CIC, CLC) subset binding — orthogonal per `feedback_cic_clc_orthogonal.md`.
9. `pattern_observations[i].pattern_summary` and `lessons_proposed[i].pattern_summary` and `lessons_proposed[i].proposed_rule` length floor 1, ceiling 4096; three-layer instance-leak detection scope per §15.9.2 RT-07 precedent (NFKC + NER + regex) — predicate F-PACKET-INSTANCE-LEAK enforces at v1.x body; v0.1 NotImplementedError.
10. Every `ProposedLesson` with `frequency == 1` MUST have `severity == "HIGH"`.
11. `grounding_signal_classes` MUST contain ≥1 of `{"external_funder_outcome", "operator_approval", "logician_gate_outcome", "kfr_drift_event", "admin_risk_event", "match_db_outcome"}`; MUST NOT be a subset of `{"council_split_event", "judge_score", "red_team_score", "editor_verdict"}` (LLM-eval-only refused).
12. Every claim_key in `span_provenance.per_claim_span_ids` MUST map to ≥1 non-empty string span_id.
13. `gate_pass_counts.*` are non-negative `int` (A12 Decimal mandate; bool excluded).
14. `score_signals.judge_score`, `red_team_score`, `judge_red_team_divergence` are non-negative `int` when non-None (0-100 for judge / red_team; bool excluded).
15. `outcome.status` ∈ `{"PENDING", "AWARDED", "DECLINED", "NO_DECISION"}` closed set.
16. `outcome.status` non-`"PENDING"` REQUIRES `operator_signature_ed25519` non-None AND `outcome.outcome_evidence_span_ids` non-empty.
17. `outcome.award_amount_minor_units` is `int` cents (A12 mandate; bool excluded) when `outcome.status == "AWARDED"`; None otherwise.
18. `canonical_bytes_hash` is 128-hex SHA3-512 digest of `to_canonical_bytes(packet)` with the two signature fields excluded.
19. `producer_signature_ed25519` is 128 hex chars (64-byte Ed25519 signature) when present.
20. `operator_signature_ed25519` is 128 hex chars when non-None.
21. **OQ-5a tolerant-reader:** v0.1-hook consumers surface `F-PACKET-SCHEMA-DRIFT` as informational advisory when `schema_version` major exceeds known max; v1.x consumers fail-closed.

These 21 invariants extend the 17 invariants enumerated in the parent spec card §3.4. The additions (1-3, 5-6, 13-15, 17-20) are length/grammar/type defenses surfaced by review of the §17 WPFA Cycle 2 RT-C2-05 fix-in-place precedent (path-traversal class) and the §2 v7.2 sub-kind convention.

### §16.2.4 Canonical-bytes codec

`to_canonical_bytes(packet) -> bytes` — UTF-8 JSON with `sort_keys=True`, `separators=(",", ":")`, signature fields (`canonical_bytes_hash`, `producer_signature_ed25519`, `operator_signature_ed25519`) excluded from the bytes input to SHA3-512. Mirrors v7.0.4-M1 §2 KFR canonicalization regime byte-for-byte.

`from_canonical_bytes(payload: bytes) -> ReflectionPacket` — decodes, re-runs invariant `__post_init__`. Tampered bytes fail at invariant check.

## §16.3 Producer contract — emit + backfill (OQ-3)

Sole producer: `archivist.reflection_submode` per v7.0.9 row 202 + §4 v2.x.2 row 203. The producer ID is the `emitted_by_seat` value; F-PACKET-PRODUCER-UNAUTHORIZED validates closed-set membership.

**Two-packet emit + backfill pattern per cycle**, linked by shared `cycle_id`:

- **Packet 1 (PENDING)** — emitted at cycle-close marker write. `outcome.status="PENDING"`; `outcome.decision_observed_at=None`; `outcome.outcome_evidence_span_ids=()`; `outcome.award_amount_minor_units=None`; `outcome.award_currency=None`; `operator_signature_ed25519=None`. F-PACKET-CADENCE-VIOLATION fails closed if emission attempted before the cycle-close marker.
- **Packet 2 (BACKFILL)** — emitted at decision-observed event (KFR funder-outcome ingest OR operator-direct outcome event). `outcome.status ∈ {"AWARDED", "DECLINED", "NO_DECISION"}`; `outcome.decision_observed_at` non-None; `outcome.outcome_evidence_span_ids` non-empty; `outcome.award_amount_minor_units` + `outcome.award_currency` populated iff status="AWARDED". `operator_signature_ed25519` REQUIRED — F-PACKET-OPERATOR-SIGNATURE-MISSING enforces.

Packet 2 has a different `packet_id` from Packet 1. Consumer A (operator review) sees both; Consumer B (KFR cross-check at quarterly cadence) prioritizes the BACKFILL packet; Consumer C (v1.x scheduled Archivist) reads both for second-order pattern detection.

**Cloud-routability + classification routing.** The producer's `reflection_agent` SCAFFOLD at `pipeline/orchestrator/seats/archivist/reflection_mode.py` is bound to **always-local** routing at v0.1 hook per architecture v7.0.9 §9 (drafts contain Confidential KFR-resolved slot values per v7.0.7). When the producer's input contains `confidential` content, F-CLASS-ROUTING-INDETERMINATE per v7.0.7 forces local-only routing BEFORE any F-PACKET-CLASS-SLOT-LEAK or F-PACKET-CLASS-MISLABEL predicate fires (defense-in-depth ordering).

## §16.4 Consumer contracts (three orthogonal audiences)

### §16.4.A Operator Review (always-local)
CLI surface `tilth archivist packets list --org <slug>` + `tilth archivist packets show --packet-id <id>` lands at v0.2 first wave. PRE-load gates: F-PACKET-SIGNATURE-INVALID + F-PACKET-SCHEMA-DRIFT (informational at v0.1) + F-PACKET-OPERATOR-SIGNATURE-MISSING (PRE-load for outcome-bearing packets).

### §16.4.B KFR Cross-Check (always-local; quarterly cadence)
Pulled into the KFR drift-detection workflow at quarterly cadence. Compares BACKFILL packet `outcome.funder_id` + `outcome.award_amount_minor_units` against KFR funder-outcome ledger; surfaces `F-LOGICIAN-FACT-DRIFT` (existing predicate at §4 v2.x) when divergence detected. PRE-load gates: F-PACKET-SIGNATURE-INVALID + F-PACKET-OPERATOR-SIGNATURE-MISSING + F-PACKET-OUTCOME-EVIDENCE-MISSING + F-PACKET-FABRICATION (POST-load replay).

### §16.4.C v1.x Scheduled-Cadence Archivist
Reads accumulated packets across cycles for second-order pattern detection (lessons memory at scale). PRE-load gates: full set including F-PACKET-RETRIEVAL-CORRUPTION (defends embedding-shaped trigger / AgentPoison / PoisonedRAG injection via packet path) + F-PACKET-MEMORY-INJECTION (defends MINJA-shaped free-text injection).

All three consumers are always-local at v0.1 / v0.2 / v1.x. F-PACKET-CLASS-MISLABEL prevents `confidential`-classified packet fields from reaching any cloud route at producer time.

## §16.5 Signing regime (mirrors v7.0.4-M1 KFR byte-for-byte)

**Producer signing.** Producer seat carries an Ed25519 keypair pinned at white-glove onboarding (mirror of v7.0.7 §6.1 router-template publisher pubkey pinning). Producer signs the canonical bytes (signature fields excluded) producing `producer_signature_ed25519`. Trust-On-First-Use rotation: new producer pubkey co-signed by previous pubkey (mirror of v7.0.7 §6.1 router-template rotation discipline).

**Operator signing.** Operator carries the Ed25519 keypair pinned at white-glove onboarding (already pinned per v7.0.7 classification-register operator signature). Operator signs the canonical bytes of the BACKFILL packet (outcome attestation) producing `operator_signature_ed25519`.

**Verification at consumer.** F-PACKET-SIGNATURE-INVALID predicate: verify `producer_signature_ed25519` against the producer pubkey AND `canonical_bytes_hash` against re-computed SHA3-512 over canonical bytes. F-PACKET-OPERATOR-SIGNATURE-INVALID predicate: verify `operator_signature_ed25519` against operator pubkey (when present). Failure → fail-closed.

**Canonical-bytes-must-include cycle_id, packet_id, classification_register_version.** Defense against replay-across-cycles: a malicious producer cannot capture a valid signature from cycle X and re-render as cycle Y by swapping cycle_id (RT precedent — closed at the canonical-bytes inclusion boundary).

## §16.6 Versioning + retention (OQ-5)

**OQ-5a Tolerant-reader pattern.** v0.1 hook consumers treat `schema_version` major exceeding known max as informational advisory (`F-PACKET-SCHEMA-DRIFT` predicate body returns advisory at v0.1; v1.x runtime amendment flips to fail-closed). Backward-compatible minor / patch version differences are silent at all consumers.

**OQ-5b Indefinite retention.** All packets stay under `orgs/<slug>/vault/operational/reflection_packets/` indefinitely. No automatic aging at v0.1 hook. Operator-driven pruning only — operator may delete packets via the operator-review CLI at v0.2 first wave; pruning is audited via the existing admin-risk ledger pattern. Tilth-internal substrate cost profile justifies indefinite retention (storage negligible; lessons memory value compounds).

## §16.7 Sibling-not-nested verification (with WPFA + Reflection sub-mode producer)

Verification table per spec card §9 — sibling-not-nested confirmed at every layer:

| Axis | §16 ReflectionPacket | §17 WPFA CycleReceipt | §15 Reflection sub-mode (producer) |
|------|----------------------|------------------------|-------------------------------------|
| Trigger | Cycle close + decision-observed | Cycle close | Cycle close (when invoked) |
| Input substrate | Logfire span tree + KFR + Match DB + Admin-risk ledger | Logfire span tree + Coefficient Registry | Logfire span tree + lessons memory + prior packets (v1.x) |
| Producer | `archivist.reflection_submode` | `pipeline.orchestrator.seats.wpfa.cycle_accountant` (deterministic; no LLM) | `archivist.reflection_submode` (produces THIS card's artifact) |
| Primary consumer | Archivist learning loop (A/B/C) | Operator dashboard + buyer-facing PDF | (n/a — producer) |
| Audience | Tilth-internal + operator | Operator + external buyer | Tilth-internal |
| Schema | ReflectionPacket | CycleReceipt | (n/a — agent behavior) |
| Signing | producer Ed25519 + operator Ed25519 (outcome-bearing) | operator Ed25519 (buyer-attested) | (n/a — signs THIS artifact) |
| Gate family | F-PACKET-* (19 codes) | F-WPFA-* (12 codes / 10 modules) | F-REFLECTION-* (17 codes) |
| Cross-reference | F-PACKET-SPAN-PROVENANCE-MISSING ↔ F-WPFA-SPAN-PROVENANCE-MISSING (sibling pattern) | mirror | F-REFLECTION-* gates producer; F-PACKET-* gates artifact |

**Zero shared output. Zero shared consumer. Zero shared schema field. Zero F-* code crossing.**

F-CIC-CLC-COUPLING-VIOLATION-class regression test at every Thesis cycle: no F-PACKET-* code crosses to §15 / §17; no F-REFLECTION-* code crosses to §16; no F-ARCHIVIST-* code crosses to §16; no F-WPFA-* code crosses to §16. AST-lint regression at `pipeline/linting/ast_lint.py` extends import-ban scope to forbid these cross-family imports at module-import time.

## §16.8 F-PACKET-* gate family overview

Full registration in companion amendment `section_04_v2_x_y_packet_amendment.md`. 19 codes; 18 NotImplementedError + 1 LIVE META (`F-PACKET-COVERAGE-INCOMPLETE`). Module decomposition: 19 modules at `pipeline/logician/gates/f_packet_*.py`, one Cedar policy file at `pipeline/vault/policies/reflection_packet.cedar` (Cycle-1 fold-in: aligning with WPFA Cedar location convention `pipeline/vault/policies/` rather than `pipeline/logician/cedar/` proposed in handoff packet — verified at Cycle 1 against on-disk WPFA precedent).

| # | Code | Layer | v0.1 body |
|---|------|-------|-----------|
| 1 | F-PACKET-INSTANCE-LEAK | PRE-emission | NotImplementedError |
| 2 | F-PACKET-CROSS-ORG-LEAK | PRE-emission + PRE-load | NotImplementedError |
| 3 | F-PACKET-FABRICATION | POST-emission + POST-load | NotImplementedError |
| 4 | F-PACKET-CLASS-SLOT-LEAK | PRE-emission | NotImplementedError |
| 5 | F-PACKET-CLASS-MISLABEL | PRE-emission | NotImplementedError |
| 6 | F-PACKET-EVAL-ONLY-GROUNDED | PRE-emission | NotImplementedError |
| 7 | F-PACKET-PREMATURE-GENERALIZATION | PRE-emission | NotImplementedError |
| 8 | F-PACKET-SPAN-PROVENANCE-MISSING | PRE-emission | NotImplementedError — **resolves §17 v1 §6.5 forward-reference** |
| 9 | F-PACKET-RETRIEVAL-CORRUPTION | PRE-load (Consumer C) | NotImplementedError |
| 10 | F-PACKET-MEMORY-INJECTION | PRE-emission | NotImplementedError |
| 11 | F-PACKET-SCHEMA-DRIFT | PRE-load | NotImplementedError (informational at v0.1 per OQ-5a) |
| 12 | F-PACKET-CADENCE-VIOLATION | PRE-emission | NotImplementedError |
| 13 | F-PACKET-SIGNATURE-INVALID | PRE-load | NotImplementedError |
| 14 | F-PACKET-OPERATOR-SIGNATURE-MISSING | PRE-load (Consumer B + C) | NotImplementedError |
| 15 | F-PACKET-OPERATOR-SIGNATURE-INVALID | PRE-load | NotImplementedError |
| 16 | F-PACKET-CYCLE-ID-UNRESOLVABLE | PRE-emission | NotImplementedError |
| 17 | F-PACKET-OUTCOME-EVIDENCE-MISSING | PRE-emission + PRE-load | NotImplementedError |
| 18 | F-PACKET-PRODUCER-UNAUTHORIZED | PRE-emission | NotImplementedError |
| 19 | F-PACKET-COVERAGE-INCOMPLETE | META PRE-cycle | **LIVE** — dormant-binding lever; FAIL_CLOSED iff any of codes 1-18 lacks realized body |

**F-PACKET-* EXCLUDED from F-CLASS-COVERAGE-INCOMPLETE META gate** per OQ-6-style isolation (mirrors §17 WPFA exclusion at row 207 + §2 v7.5 FG exclusion at row 213). F-PACKET-COVERAGE-INCOMPLETE owns realization-coverage for its own family. F-CLASS-COVERAGE-INCOMPLETE stays focused on F-CLASS-* family.

## §16.9 v0.2 first wave transition discipline

At the v0.2 first wave compound LOCK, the following land atomically (per OQ-2 (a)):

- `§16 v1.1 amendment` — registers SUB_KIND_REGISTRY entry under `operational/reflection_packets/`; flips producer to live emission.
- `§2 v7.x amendment` — registers sub-kind row in SUB_KIND_REGISTRY.
- `§4 v2.x.y.1 amendment` — flips 18 NotImplementedError predicates to live bodies; F-PACKET-COVERAGE-INCOMPLETE META-gate now validates against live bodies (passes when all 18 land; fail-closes pending any).
- `§15 v2.x Archivist Reflection sub-mode SPEC amendment` — producer behavior at v0.2.
- `§0.5 v?? amendment` — paired-commit rows for the v0.2 transitions.

**v1.x runtime amendment** lands scheduled-cadence-driven Consumer C (Archivist learning loop) consumption with PRE-load gates live + tolerant-reader pattern flipped to fail-closed at major-version drift.

## §16.10 Probe checklist (Thesis Cycle 1 + Cycle 2 disposition log)

Per the row-170 transparent-disposition pattern (originated at §15 v1 Cycle 2; extended through §13 v1 / §14 v1 / §4 v2.x.1 / §17 v1 / §2 v7.5 FG / etc.), Cycle 1 + Cycle 2 NEW probes from Red Team review fold-in here with text-level mechanism OR defer to follow-on minor amendment.

### §16.10.1 Cycle 1 Red Team probes (disposition)

Findings dispatched against the handoff packet §"Audit #1 — scoping" probe vectors (a)-(k). Three NEW probes (RT-01 META-gate body-realization, RT-02 dynamic-import bypass, RT-13 packet_id uniqueness across cycles) folded in at Cycle 1 with text-level mechanism per row-170 transparent-disposition precedent. Full Cycle 1 disposition log at `pipeline/validation/reflection_packet_thesis_2026-05-11/cycle_1_disposition.md`.

**NEW Cycle 1 probes (folded-in here at LOCK):**

- **RT-01 META-gate body-realization check.** `f_packet_coverage_incomplete.py` LIVE body at v0.1 hook verifies signature presence + callable; it does NOT verify body realization (NotImplementedError vs live body). **DISPOSITION:** intentional dormant-binding per OQ-2 (a); FOLD-IN forward-binding contract to §16.9 + §4 v2.x.y §9 v1.x amendment-realization checklist contract 7: v0.2 first wave compound LOCK strengthens META-gate body to dry-run probe each predicate and reject NotImplementedError. v0.1 hook signature-presence semantic is correct for the dormant-binding lever; the body-realization check fires at v0.2 first wave deployment time when the realized bodies land. RT-11 atomicity guarantee at §16.9 covers the structural concern that bodies must all land atomically with producer-flip.
- **RT-02 Dynamic-import bypass.** AST-lint at `pipeline/linting/ast_lint.py` scans static imports only; `importlib.import_module` / `__import__` / `exec` / `eval` can dynamically resolve cross-family code. **DISPOSITION:** scope clarification at §4 v2.x.y §6 — static-import scope; dynamic-import detection BOUNDED-by-v7-LOCKED-A1+A4 single-client trusted-operator envelope (mirrors §4 v2.x.1 RT-01..06 BOUNDED dispositions). v2 multi-tenant Section O.5 mitigation track marker logged. v1.x amendment-realization checklist contract 8 added: dynamic-import detection extension at v2 Section O.5.
- **RT-13 packet_id uniqueness across cycles.** Schema validates `packet_id` grammar but NOT global filename uniqueness. **DISPOSITION:** FOLD-IN — sub-tag `.packet_id_collision` was previously documented under F-PACKET-CADENCE-VIOLATION at §4 v2.x.y row 12 (originally tagged Cycle-2 RT-C2-01, surfaced at Cycle 1 by Red Team and promoted to Cycle-1 RT-13 closure). v0.2 first wave realization adds the pre-write filename-existence check; F-PACKET-CADENCE-VIOLATION predicate body at v0.2 first wave checks for packet_id collision in the org's reflection_packets/ subtree.

**Standard 11 probe vectors (a)-(k) disposition:**

- **(a) META-gate bypass — RT-01:** v0.2 first wave deployment lands NotImplementedError → live body flip first WITHOUT the producer-flip → consumer-flip atomicity guarantee. **DISPOSITION:** FOLDED-IN at §16.9 — explicit atomicity guarantee added: "v0.2 first wave compound LOCK lands all four amendments at the same `lock_timestamp_utc` per §6.17 Option-B; flipping any one without the others fails the compound F-INDEX-STALE PRE-gate."
- **(b) Path B naming-collision — RT-02:** downstream module imports F-REFLECTION-* but resolves via F-PACKET-* family typo / case-insensitive matching / Unicode homoglyph collision. **DISPOSITION:** FOLDED-IN at §16.7 — AST-lint regression scope extended to forbid F-PACKET-* / F-REFLECTION-* / F-ARCHIVIST-* / F-WPFA-* cross-family imports at module-import time; Unicode-normalized regex (NFKC) applied at code-id closed-set membership check.
- **(c) Schema-drift exploit — RT-03:** packet with `schema_version: "999.0.0"` written and silently accepted by Consumer A pre-load. **DISPOSITION:** FOLDED-IN at OQ-5a v0.1 informational advisory; v1.x amendment lifts to fail-closed; predicate body NotImplementedError at v0.1 means the consumer surfaces advisory only — Cycle 2 RT-C2 may extend the advisory output channel.
- **(d) Producer-signature replay — RT-04:** capture signature from cycle X, re-render as cycle Y by swapping cycle_id + cycle_close_marker_span_id. **DISPOSITION:** FOLDED-IN at §16.5 — explicit "canonical-bytes-must-include cycle_id, packet_id, classification_register_version" boundary; any swap changes canonical bytes; signature verification fails.
- **(e) Backfill packet replay — RT-05:** Packet 2 from cycle X re-rendered as Packet 2 for cycle Y by swapping cycle_id. **DISPOSITION:** FOLDED-IN at §16.5 + §16.2.3 inv 16 — operator signature covers canonical bytes which include cycle_id; replay swap invalidates signature.
- **(f) Three-layer instance-leak bypass — RT-06:** NFKC + NER + regex bypass via homoglyph + ZWJ + entity name. **DISPOSITION:** FOLDED-IN at §16.2.3 inv 9 — F-PACKET-INSTANCE-LEAK predicate at v1.x body inherits §15.9.2 RT-07 precedent (NFKC + NER + regex three-layer); homoglyph/ZWJ closed at NFKC normalization step; entity-name closed at NER step.
- **(g) Span-provenance bypass — RT-07:** dict-key `{"fake_claim_key": ["valid_span_id"]}` passes predicate that only checks "every claim key has ≥1 span_id". **DISPOSITION:** FOLDED-IN at §16.8 #8 — F-PACKET-SPAN-PROVENANCE-MISSING predicate's required_claim_keys set (mirroring §17 WPFA `_REQUIRED_CLAIM_KEYS_V0_1` pattern at `f_wpfa_span_provenance_missing.py`) enforces schema-driven coverage of every quantitative-claim field, NOT just non-empty dict. Sub-tag `.claim_key_unmapped` fires when required keys absent.
- **(h) F-PACKET-OUTCOME-EVIDENCE-MISSING bypass — RT-08:** Packet 2 BACKFILL with `outcome_evidence_span_ids=("dummy_span_id",)` resolvable in Logfire but from a different cycle. **DISPOSITION:** FOLDED-IN at §16.8 #17 — predicate body cross-checks span_id's parent cycle_id against packet `cycle_id`; mismatch fires sub-tag `.span_id_from_different_cycle` (mirrors WPFA span-provenance pattern).
- **(i) Cross-org leak via shared logfire_export_uri — RT-09:** `span_provenance.logfire_export_uri` points to a shared bundle; org-A packet references spans from org-B's slice. **DISPOSITION:** FOLDED-IN at §16.8 #2 — F-PACKET-CROSS-ORG-LEAK predicate validates every span_id's recorded org_slug attribute matches the packet's org_slug; sub-tag `.span_org_slug_mismatch` fires on cross-org reference. Defense-in-depth alongside the path-slug match guard (mirror of WPFA `check_f_wpfa_cross_org_leak`).
- **(j) Producer-unauthorized bypass — RT-10:** malicious seat writes packet claiming right `emitted_by_seat` but signing with different seat's pubkey. **DISPOSITION:** FOLDED-IN at §16.5 — signature-verification reads producer pubkey from the white-glove-pinned producer-seat registry (NOT from the packet's `emitted_by_seat` field); circular-trust closed. F-PACKET-PRODUCER-UNAUTHORIZED + F-PACKET-SIGNATURE-INVALID compose: closed-set membership at field level + cryptographic verification at pubkey level.
- **(k) v0.2 transition unsafe — RT-11:** flip-order race window. **DISPOSITION:** REJECTED-with-rationale by §16.9 atomicity guarantee per RT-01 fold-in. Compound LOCK pattern per §6.17 Option-B precludes flip-order race.

### §16.10.2 Cycle 2 Red Team NEW probes (disposition per row-170)

Anticipated Cycle 2 probes documented here pre-Cycle-2 dispatch per the spec card §"Audit #2 — verification" template. After Cycle 2 dispatches at this LOCK ceremony, see `pipeline/validation/reflection_packet_thesis_2026-05-11/cycle_2_disposition.md` for the actual fold-in dispositions.

- **RT-C2-01 (PROMOTED to Cycle-1 RT-13 at this LOCK)** — packet_id collision across cycles — already folded-in at §16.10.1 Cycle 1 disposition.
- **RT-C2-02** — Operator dual-signature attack: operator signs Packet 1 (PENDING) AND Packet 2 (BACKFILL) but with different intended outcomes. **DISPOSITION:** FOLDED-IN at §16.3 — Packet 1 explicitly forbids operator_signature_ed25519 (must be None); F-PACKET-OPERATOR-SIGNATURE-MISSING sub-tag `.signature_present_for_pending` fires when Packet 1 carries non-None operator signature (defensive symmetry; verified at schema level via __post_init__).
- **RT-C2-03** — frozen retention abuse: indefinite retention enables stale packet replay during disk-restore-from-backup scenarios. **DISPOSITION:** BOUNDED-by-A1+A4 — Stage-1 single-client operator-trusted envelope. v2 multi-tenant Section O.5 mitigation track logged. v0.1 hook does not authorize cross-cycle automated replay; v1.x Consumer C reads with PRE-load signature verification.

## §16.11 v0.2 SPEC-ONLY discipline structurally enforced

F-PACKET-COVERAGE-INCOMPLETE META-gate (#19) LIVE body inspects gate-realization-registry. Any v0.2 deployment that has not flipped all 18 NotImplementedError → live body fails fail-closed at PRE-cycle. This is the L-006 dormant-binding pattern (origin v7.0.7 F-CLASS-COVERAGE-INCOMPLETE; precedent: F-REFLECTION-COVERAGE-INCOMPLETE at §4 v2.x.2 row 203's BINDING-with-ACTIVE-body).

## §16.12 Out of scope at this LOCK

- SUB_KIND_REGISTRY entry registration (DEFERRED to v0.2 first wave per OQ-2 (a)).
- §15 v2.x Archivist Reflection sub-mode SPEC (DEFERRED to v0.2 first wave).
- Live emission (DEFERRED to v0.2 first wave; 18 of 19 predicate bodies stay NotImplementedError).
- Consumer A operator-review CLI runtime wiring (DEFERRED to v0.2 first wave).
- Consumer B KFR cross-check runtime wiring (DEFERRED to v0.2 first wave).
- Consumer C v1.x scheduled-cadence Archivist (DEFERRED to v1.x runtime).
- Pydantic AI `reflection_agent` agent construction (DEFERRED to v1.x runtime per v7.0.9 §9.1).
- Heavy-Judge-swap analog for Reflection Packet (NO v0.1 hook scope; potential v1.x extension).
- Probe registry realization (NO v0.1 hook scope; v1.x extension).

## §16.13 Audit trail

- Spec card: `pipeline/planning/reflection_packet_dispatch_spec_2026-05-11.md`
- SCOPING_DRAFT predecessor: `pipeline/planning/reflection_packet_scoping_draft_2026-05-10.md`
- Pre-Thesis reconciliation: `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md` (Path B adopted)
- Thesis dispatch packet: `pipeline/handoffs/ws_reflection_packet_handoff_2026-05-11.md`
- Cycle 1 + 2 raw outputs: `pipeline/validation/reflection_packet_thesis_2026-05-11/{cycle_1,cycle_2}/`
- Cycle 1 disposition: `pipeline/validation/reflection_packet_thesis_2026-05-11/cycle_1_disposition.md`
- Cycle 2 disposition: `pipeline/validation/reflection_packet_thesis_2026-05-11/cycle_2_disposition.md`

## §16.14 Done definition (this section)

- [x] §16 numbered per OQ-1 (honors §17 WPFA spec card §2 reservation; topical cluster with §15 Archivist).
- [x] Full ReflectionPacket schema with 21 invariants (extends spec card §3.4's 17 with 4 length/grammar/type defenses).
- [x] Producer contract emit + backfill per OQ-3.
- [x] Three consumer contracts (A/B/C) named with PRE-load gate scope.
- [x] Signing regime mirrors v7.0.4-M1 KFR canonical-JSON Ed25519 byte-for-byte; canonical-bytes-must-include cycle_id closes RT-04/RT-05.
- [x] Versioning + retention per OQ-5 (tolerant-reader at v0.1 advisory; indefinite retention; operator-driven pruning).
- [x] Sibling-not-nested verification with WPFA + Reflection sub-mode producer.
- [x] §16.8 F-PACKET-* gate family overview (19 codes; 18 NotImplementedError + 1 LIVE META; F-PACKET-* EXCLUDED from F-CLASS-COVERAGE-INCOMPLETE per OQ-6 pattern).
- [x] v0.2 first wave transition discipline + atomicity guarantee (RT-01 fold-in).
- [x] Cycle 1 + Cycle 2 probe disposition log per row-170 transparent-disposition.
- [x] §17 v1 §6.5 forward-reference to F-PACKET-SPAN-PROVENANCE-MISSING resolved at this LOCK.

---

**Filed:** 2026-05-15. LOCKED via L-005 strict two-cycle Thesis with FULL LIVE CROSS-FAMILY rigor. Compound paired-commit sibling 1/3 with §4 v2.x.y F-PACKET-* + §0.5 v22. v0.1 Beta hook dormant artifact spec; live emission lands at v0.2 first wave compound LOCK.
