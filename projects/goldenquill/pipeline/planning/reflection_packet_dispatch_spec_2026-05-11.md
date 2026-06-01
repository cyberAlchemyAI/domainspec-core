---
title: Reflection Packet — Dispatch Spec Card (§16 v1 + §4 v2.x.y F-PACKET-* family + §0.5 v20 compound triple LOCK candidate)
filed: 2026-05-11
operator: Josh Inklovich
status: DISPATCH_SPEC_DRAFT — pre-Thesis dispatch packet; no LOCK ceremony. Promoted from SCOPING_DRAFT (filed 2026-05-10 at `pipeline/planning/reflection_packet_scoping_draft_2026-05-10.md`) after operator decisions landed 2026-05-11 on all 6 OQs. L-005 strict two-cycle review (Editor + Judge + Red Team, FULL live cross-family per /AGENTS.md) MUST close before any LOCK. Spec card per `pipeline/engineering/engineering_process_v0.1.md` §11 adapted to a blueprint-amendment family (multiple sections under one compound LOCK). Sibling artifact to WPFA CycleReceipt (§17 v1 LOCKED 2026-05-11 rows 205-208); the two consume the same Logfire span tree at cycle close but emit independently to different audiences.
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                             # v7 LOCKED 2026-04-19 A1–A12; A12 Decimal mandate; A1 single-client v0.1 threat model; A4 operator-trusted preflight
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md                      # v7.0.4-M1 LOCKED 2026-05-10 row 190 — canonical-JSON signing regime; Ed25519 signature discipline this card mirrors byte-for-byte
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                         # v7.0.7 LOCKED 2026-05-10 row 180 — classification-driven routing + opaque [SLOT_<numeric_id>] discipline applies to any cloud-routed read of a packet
  - pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md                         # v7.0.9 LOCKED 2026-05-10 row 202 (Reflection sub-mode v0.1 hook) — registers F-REFLECTION-* family at architectural-primitive layer; this card's F-PACKET-* family is a SIBLING, not a child
  - pipeline/blueprint/v0.1/section_02_v7_2_amendment.md                                # §2 v7.2 LOCKED 2026-05-10 row 186 — sub-kind registry pattern; v0.1 hook DEFERS sub-kind registration to v0.2 first wave
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                                # §4 v2.x LOCKED 2026-05-10 rows 193/194 — failure-code family registration pattern; F-PACKET-* follows format
  - pipeline/blueprint/v0.1/section_04_logician_v2_x_2_amendment.md                     # §4 v2.x.2 LOCKED 2026-05-10 row 203 (Reflection sub-mode hook) — registers 17 F-REFLECTION-* predicate signatures; F-PACKET-* MUST NOT collide
  - pipeline/blueprint/v0.1/section_15_archivist.md                                     # §15 v1 SPEC LOCKED 2026-05-10 rows 191/192 — proposes-only Archivist seat; F-ARCHIVIST-* parents
  - pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md                      # §17 v1 LOCKED 2026-05-11 rows 205-208 — WPFA sibling artifact; this card's F-PACKET-SPAN-PROVENANCE-MISSING resolves the WPFA §6.5 forward-reference
  - pipeline/blueprint/v0.1/section_11_intake_v1_1_amendment.md                          # §11 v1.1 LOCKED 2026-05-11 rows 209-210 — last LOCK before this dispatch; runtime-live row at §0.5 v19 = 415
  - pipeline/research/reflection/synthesis_design_memo_2026-05-10.md                    # Reflection sub-mode design synthesis — distinguishes the AGENT (producer) from the ARTIFACT (packet) this card specs
  - pipeline/research/reflection_packet_grounding/findings_2026-05-10.md                # 5-lane research findings; Synthesis B § proposes a 12-code register currently named F-REFLECTION-* — this card RE-CASTS that register under F-PACKET-* per Path B
  - pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md           # Path B recommendation; this card adopts Path B as its naming discipline
  - pipeline/planning/reflection_packet_scoping_draft_2026-05-10.md                     # SCOPING_DRAFT this card promotes; all schema sketches + OQ batch consolidated here
related_handoffs:
  - pipeline/handoffs/ws_wpfa_handoff_2026-05-10.md                                     # WPFA Thesis dispatch packet — sibling artifact; pre-existing forward-reference now resolved
  - pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md                     # Reflection sub-mode v0.1 hook (LOCKed today) — producer of this artifact
  - pipeline/handoffs/ws_reflection_packet_handoff_2026-05-11.md                        # THIS spec card's Thesis dispatch packet (pre-staged alongside this promotion)
sibling_artifacts:
  - WPFA CycleReceipt (§17 v1 LOCKED rows 205-208)                                       # both emit at cycle close, both consume Logfire span tree, ZERO shared output/consumer/schema/gate-family
authority: operator decisions landed 2026-05-11 on all 6 SCOPING_DRAFT OQs (see §7 OQ disposition log). "lets gooo" promotion directive.
purpose: Stage a SPEC for the Reflection Packet artifact, its F-PACKET-* failure-code family, and the §0.5 row append, so a downstream Thesis round + Code phase can audit and compound-LOCK them. SPEC ONLY — no Python written beyond the schema-skeleton scaffold pattern; no LOCK ceremony invoked; no row range reserved against §0.5 until paired blueprint amendments land at compound triple LOCK.
dispatch_class: spec_card_for_blueprint_amendment_family
ws_dispatch_target: NEW WS — provisionally "WS-Reflection Packet" — not yet on `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md`. **v0.1 Beta hook dormant scope per OQ-2 operator decision 2026-05-11.** Live emission deferred to v0.2 first wave alongside §15 v2.x Archivist Reflection sub-mode SPEC LOCK.
review_discipline: L-005 strict two-cycle, FULL live cross-family per /AGENTS.md (Editor=groq/llama-3.3-70b-versatile + Judge=google/gemini-2.5-pro + Red Team=groq/openai/gpt-oss-120b) — no Section E carve-out. Mirrors the rigor level applied to §2 v7.2, §11 v1, §12 v1, §13 v1, §14 v1, §15 v1, §17 v1, §4 v2.x.
target_lock_rows: compound triple LOCK at anticipated rows 211/212/213 (after §11 v1.1 LOCK rows 209/210; verify against runtime-live row at dispatch time).
---

# §0. Why this spec card exists (motivation)

The Reflection sub-mode v0.1 hook LOCKed 2026-05-10 (compound triple rows 202/203/204) gates the *producer's behavior* — 17 F-REFLECTION-* predicate signatures + the inoculation frame + the depth bound + cross-family-rigor enforcement for the agent that consolidates lessons memory between cycles.

What was NOT specified at that LOCK: **the artifact the producer emits.** The Reflection sub-mode is one of several emission paths the §15 Archivist seat hosts — it can write proposed-lesson-deltas, digest summaries, and operator-review staging documents. The packet artifact is ONE of those emission shapes — the one downstream consumers (operator review surface, KFR cross-check via F-LOGICIAN-FACT-DRIFT, v1.x scheduled-cadence-driven invocation) need a contract for.

**This card specs the artifact.** A typed Pydantic record emitted once per grant cycle close that carries: gate-pass counts, score deltas, pattern observations, outcome status, span-provenance per quantitative claim, and an Ed25519 signing regime. Three orthogonal gate-family owners enforce the closure: F-REFLECTION-* gates the producer (already LOCKed at v7.0.9 + §4 v2.x.2); F-ARCHIVIST-* gates the substrate write (already LOCKed at §15 v1); **F-PACKET-* (this card) gates the artifact.**

**Sibling-not-nested with WPFA CycleReceipt.** Both artifacts emit at cycle close. Both consume the same Logfire span tree. Different consumers, different audiences, different schemas. WPFA goes to operator dashboard + buyer-facing PDF (external accounting). ReflectionPacket goes to the Archivist learning loop (Tilth-internal). The two cross-reference at one place only: F-PACKET-SPAN-PROVENANCE-MISSING (this card) ↔ F-WPFA-SPAN-PROVENANCE-MISSING (§17 v1) as sibling patterns. WPFA's §6.5 forward-reference to F-PACKET-SPAN-PROVENANCE-MISSING (filed before this card LOCKed) resolves at this card's compound-LOCK.

**Why a DISPATCH_SPEC_DRAFT now rather than waiting.** Operator decided 2026-05-11 on all 6 SCOPING_DRAFT OQs (see §7). The blocking OQ (OQ-2 ship window) resolved to v0.1 Beta dormant hook only — minimal Beta close-out competition, schema + signing primitives + 19 F-PACKET-* predicate signatures at architectural-primitive layer, predicates stay NotImplementedError. Three siblings (§16 v1 + §4 v2.x.y + §0.5 v20) at compound triple LOCK — NOT four siblings like WPFA, because no sub-kind registry update at v0.1 hook scope (deferred to v0.2 first wave when live emission lands).

# §1. Compound-LOCK pairing identity

Following the WS-K §15 v1 + §0.5 v13 precedent (compound triple at rows 191/192 + §0.5 v13) and the architecture v7.0.9 / §4 v2.x.2 / §0.5 v18 triple (rows 202/203/204) — and **deliberately differing from WPFA's four-sibling quadruple** — the Reflection Packet amendment is a **compound triple LOCK across three siblings**:

| Sibling | What lands | Pairing class |
|---|---|---|
| §16 v1 (new file `pipeline/blueprint/v0.1/section_16_reflection_packet.md`) — section number proposal per §2 below | New seat-class section: Reflection Packet artifact spec + ReflectionPacket Pydantic shape + producer contract + three consumer contracts + signing regime + retention; v0.1 hook DORMANT (no live emission); schema module scaffold at `pipeline/vault/sub_kinds/reflection_packets.py` (NOT registered in SUB_KIND_REGISTRY at v0.1 hook per §6). | Primary |
| §4 v2.x.y (new amendment file `section_04_v2_x_y_packet_amendment.md`) | 19 F-PACKET-* failure codes registered at predicate-signature layer; bodies NotImplementedError per OQ-2 (a); module decomposition per spec card §4.7; PRE/POST/META layering finalized; F-PACKET-COVERAGE-INCOMPLETE META-gate gets live body (analog of F-CLASS-COVERAGE-INCOMPLETE and F-REFLECTION-COVERAGE-INCOMPLETE) | Sibling |
| §0.5 v20 amendment (new file `section_00_5_section_16_packet_amendment.md`) | Row append starting at 416 — 1 marker + 19 failure-code rows + invariant-cluster rows + signing-protocol rows; total 25 rows per §5 below. Runtime-live total after this LOCK: 440 rows. | Sibling |

Compound transaction discipline per §2 v7.2 §11 audit prompt + WS-K §15 v1 + architecture v7.0.9 paired-commit pattern: all three sibling rows enter `lock_history.v1.jsonl` at the same `lock_timestamp_utc`. F-INDEX-STALE PRE-gate fires at commit time per §6.2 order 3; all 25 new §0.5 rows must be present in the runtime-live index or the compound commit fails closed.

**Compound LOCK row(s) in lock_history:** anticipated rows 211/212/213 (current runtime-live row at §11 v1.1 LOCK 2026-05-11 = 210; verify against runtime-live row at dispatch time. If §16 row prefers `[lock_row=211]` for clarity, §4 v2.x.y = 212, §0.5 v20 = 213).

**Why three siblings rather than four (vs WPFA quadruple):** WPFA needed the Coefficient Registry signed-asset class (§2 v7.4) because live emission demands a published trust anchor. Reflection Packet at v0.1 hook scope has NO live emission, so there is NO sub-kind registry update for §2 v7.x at this LOCK. The schema module scaffold (`pipeline/vault/sub_kinds/reflection_packets.py`) is authored as DORMANT — the SUB_KIND_REGISTRY entry registers at the v0.2 first wave compound LOCK alongside §15 v2.x Archivist Reflection sub-mode SPEC. See §6 for v0.2 transition discipline.

# §2. Section number — §16 (rationale)

**Operator-confirmed §16 (OQ-1, 2026-05-11).** Synthesis default stood. Honors WPFA spec card §2 reservation: §15 Archivist + §16 Reflection Packet form the Tilth-internal between-cycle preservation cluster; §17 WPFA is the operator-and-buyer-facing accounting boundary. Topical clustering preserved.

**Current §-numbering at v0.1 (sections with LOCKed primitives):**

§0.5 Interface Index · §1 Sovereignty Envelope · §2 Vault Topology · §3 Scout · §4 Logician · §5 Pipeline · §6 Operating Envelope · §7 Scribe · §8 Editor (TBD, parked) · §9 Judge (TBD, parked) · §10 Red Team · §11 Intake (v1.1) · §12 Uploader · §13 Data Collector · §14 Report Generator · §15 Archivist · **§16 Reflection Packet (this card)** · §17 WPFA.

**Rationale:**

1. **Tilth-internal vs buyer-external axis.** §15 (Archivist seat) + §16 (Reflection Packet, the artifact §15's reflection sub-mode emits) are Tilth-internal between-cycle preservation surfaces. §17 (WPFA Cycle Receipt) is operator-and-buyer-facing accounting. The §-numbering reflects the architectural axis.
2. **Emission-orchestration symmetry preserved.** Both §16 (Reflection Packet) and §17 (WPFA) emit at cycle close from the Logfire span tree. Placing them adjacent at §-numbers signals the shared trigger without forcing schema or consumer composition. Sibling-not-nested at §-numbering layer mirrors sibling-not-nested at schema layer.
3. **§16 leaves the room §17 WPFA spec card §2 implied for it.** The §16 reservation was structural, not nominal — the Reflection Packet design fits the slot.

**Companion subsection layout (final for this card):** §16.1 schema (mirrors §3 of this card); §16.2 producer contract (mirrors §4); §16.3 consumer contracts (mirrors §5); §16.4 signing regime (subsection of §4); §16.5 versioning + retention (mirrors §6.1 of SCOPING_DRAFT); §16.6 F-PACKET-* family overview (registry lives in §4 v2.x.y amendment); §16.7 sibling-not-nested verification with WPFA.

# §3. Full ReflectionPacket schema (finalized invariants)

Following the §2 v7.2 sub-kind convention EXACTLY: `@dataclass(frozen=True, kw_only=True)`; one record = one file; SIMPLE class; `write-if-absent` mode; `__post_init__` invariant validation; canonical-JSON encode/decode round-trip; schema module at `pipeline/vault/sub_kinds/reflection_packets.py`. **At v0.1 hook scope, the schema module is authored but NOT registered in SUB_KIND_REGISTRY** per OQ-2 (a) — registration lands at v0.2 first wave compound LOCK paired with §15 v2.x Archivist Reflection sub-mode SPEC.

## §3.1 Top-level shape (final per OQ-3, OQ-4, OQ-6 resolutions)

```python
@dataclass(frozen=True, kw_only=True)
class ReflectionPacket:
    # Identity + provenance (mirrors WPFA CycleReceipt frontmatter)
    packet_id: str                                       # opaque caller-minted ID; matches filename {packet_id}.json
    cycle_id: str                                        # foreign key into the cycle this packet records; matches §5 v8 track-registry cycle close marker
    org_slug: str                                        # Law 3 binding; resolves to existing orgs/<slug>/ subtree at PRE-write
    schema_version: str                                  # semver string, e.g., "1.0.0"; tolerant-reader pattern at consumer per OQ-5a
    classification_register_version: str                 # SHA3-512 hash of the operator-signed classification register at cycle start; mirrors v7.0.7 §6.1 discipline

    # Emission context
    emitted_at: str                                      # UTC ISO-8601 'Z'
    emitted_by_seat: str                                 # canonical seat identifier of the producer; v0.1 closed set = {"archivist.reflection_submode"} exclusively
    cycle_close_marker_span_id: str                      # the Logfire span ID for the cycle-close marker; bridges packet → cycle's actual run trace

    # Pattern-level observations (per Lane 3 ExpeL / §15.9.2 instance-leak precedent)
    pattern_observations: tuple[PatternObservation, ...]  # zero-or-more pattern records; instance-level details refused at PRE-write per F-PACKET-INSTANCE-LEAK
    lessons_proposed: tuple[ProposedLesson, ...]          # zero-or-more pattern-rolled lessons; frequency ≥ 2 OR severity = HIGH per F-PACKET-PREMATURE-GENERALIZATION

    # Quantitative signals (every value MUST trace to a Logfire span; see span_provenance)
    gate_pass_counts: GatePassCounts                      # F-*-PASS / FAIL / SKIP counts per gate family observed in cycle
    score_signals: ScoreSignals                            # Judge / Red Team / Editor verdicts; deterministic field-level fields ONLY (no free-text)
    outcome: CycleOutcome                                  # status = PENDING / AWARDED / DECLINED / NO_DECISION; backfill mechanism per OQ-3 (b) emit+backfill

    # Grounding signal class declarations (mirrors v7.0.9 §4 precedence rule; defense-in-depth at artifact-side)
    grounding_signal_classes: frozenset[str]              # MUST contain ≥1 of {external_funder_outcome, operator_approval, logician_gate_outcome, kfr_drift_event, admin_risk_event, match_db_outcome}; council_split_event admitted but not alone; LLM-eval-only refused

    # Provenance — every quantitative claim must trace
    span_provenance: PacketSpanProvenance                 # trace_ids[], per_claim_span_ids; mirrors WPFA SpanProvenance pattern byte-for-byte

    # Signing regime (per v7.0.4-M1 KFR canonical-JSON Ed25519 pattern)
    canonical_bytes_hash: str                              # SHA3-512 of canonical-JSON-encoded packet (excluding signature fields themselves); 128 hex chars
    producer_signature_ed25519: str                        # producer-emitted Ed25519 signature; verifies against producer-seat pubkey at PRE-consumption
    operator_signature_ed25519: str | None                 # operator-attest signature; required for outcome.status non-PENDING per F-PACKET-OPERATOR-SIGNATURE-MISSING; None acceptable while status=PENDING

    # OQ-4 (a) RESOLVED — no operator_notes field. Operator commentary stays in §15 sub-mode's adjacent substrate; F-PACKET-MEMORY-INJECTION threat surface contained.
```

## §3.2 Field sub-shapes (final)

```python
@dataclass(frozen=True, kw_only=True)
class PatternObservation:
    pattern_summary: str                                  # pattern-LEVEL text; instance-level identifiers refused per F-PACKET-INSTANCE-LEAK
    cic: str                                              # Customer Identity Category one of six; closed set
    clc: str                                              # Capital Logic Card one of eight; closed set
    frequency: int                                        # cycles in which this pattern surfaced; ≥1 to record
    severity: str                                         # one of {LOW, MEDIUM, HIGH}; closed set
    first_observed_cycle_id: str                          # cycle_id where the pattern first surfaced; foreign key
    supporting_span_ids: tuple[str, ...]                  # MUST be non-empty; ≥1 Logfire span per observation


@dataclass(frozen=True, kw_only=True)
class ProposedLesson:
    lesson_id: str                                        # caller-minted opaque; stable across re-emits
    pattern_summary: str                                  # pattern-LEVEL text; F-PACKET-INSTANCE-LEAK applies
    proposed_rule: str                                    # actionable rule text; structural-NER + injection-pattern scanners apply at PRE-write
    frequency: int                                        # ≥2 OR severity=HIGH per F-PACKET-PREMATURE-GENERALIZATION
    severity: str                                         # {LOW, MEDIUM, HIGH}
    supporting_pattern_observation_ids: tuple[str, ...]   # foreign keys into pattern_observations
    supporting_cycle_ids: tuple[str, ...]                 # ≥ frequency cycle_ids


@dataclass(frozen=True, kw_only=True)
class GatePassCounts:
    f_class_pass: int
    f_class_fail: int
    f_archivist_pass: int
    f_archivist_fail: int
    f_reflection_pass: int                                 # producer-side gates from v7.0.9 + §4 v2.x.2
    f_reflection_fail: int
    f_packet_pass: int                                     # self-emitted (mostly trivially 0 at emission; surfaces at consumer-side replays)
    f_packet_fail: int
    f_logician_total_pass: int                             # rolled aggregate per §4 v2.x
    f_logician_total_fail: int


@dataclass(frozen=True, kw_only=True)
class ScoreSignals:
    judge_score: int | None                                # 0-100 if observed; None if Judge did not score this cycle
    red_team_score: int | None
    editor_verdict: str | None                             # closed set {READY, NEEDS_FIXES, NOT_READY}
    judge_red_team_divergence: int | None                  # absolute delta; council-split signal source
    council_split_fired: bool                              # True iff divergence > 10 per Law 4 tie-breaker
    cross_family_satisfied: bool                           # True iff L-003 cross-family rigor satisfied at this cycle


@dataclass(frozen=True, kw_only=True)
class CycleOutcome:
    status: str                                            # {PENDING, AWARDED, DECLINED, NO_DECISION}
    funder_id: str | None                                  # KFR funder_id if known; None if pre-submit
    award_amount_minor_units: int | None                   # int per A12 Decimal mandate; cents-precision per OQ-6 (sub-cent precision rejected — no sub-cent grants in practice); None if status ≠ AWARDED
    award_currency: str | None                             # ISO-4217 alpha-3; None if status ≠ AWARDED
    decision_observed_at: str | None                       # UTC ISO-8601 'Z'; None if status = PENDING
    outcome_evidence_span_ids: tuple[str, ...]             # ≥1 if status non-PENDING; refused empty per F-PACKET-OUTCOME-EVIDENCE-MISSING


@dataclass(frozen=True, kw_only=True)
class PacketSpanProvenance:
    trace_ids: tuple[str, ...]                             # ≥1; one or more Logfire trace IDs covered by this packet
    logfire_export_uri: str | None                         # optional pointer to a Logfire export bundle for offline audit
    per_claim_span_ids: dict[str, tuple[str, ...]]         # claim_key (e.g., "gate_pass_counts.f_logician_total_pass") → ≥1 span_ids backing it
```

## §3.3 OQ-3 (b) backfill mechanism — emit + backfill discipline

**Resolved 2026-05-11.** Two-packet pattern per cycle, linked by shared `cycle_id`:

- **Packet 1 (PENDING):** emitted at cycle close marker write (Uploader prepare-and-stage → operator submit → cycle close). `outcome.status = PENDING`; `outcome.decision_observed_at = None`; `outcome.outcome_evidence_span_ids = ()`; `outcome.award_amount_minor_units = None`; `outcome.award_currency = None`; `operator_signature_ed25519 = None` (acceptable for status=PENDING per invariant §3.4.12).
- **Packet 2 (BACKFILL):** emitted at decision-observed event (KFR funder-outcome ingest OR operator-direct outcome event). `outcome.status ∈ {AWARDED, DECLINED, NO_DECISION}`; `outcome.decision_observed_at` non-None; `outcome.outcome_evidence_span_ids` non-empty; `outcome.award_amount_minor_units` + `outcome.award_currency` populated iff `status = AWARDED`; **`operator_signature_ed25519` REQUIRED** (operator attestation on outcome data; F-PACKET-OPERATOR-SIGNATURE-MISSING enforces).

**Packet 2 has a different `packet_id` from Packet 1.** Linked solely by shared `cycle_id`. Consumer-A (operator review) sees both; KFR cross-check (Consumer B) prioritizes the BACKFILL packet for the funder + cycle. v1.x scheduled-cadence-driven Archivist (Consumer C) reads both for second-order pattern detection.

**Why emit + backfill rather than emit-once-at-outcome.** Consumer A benefits from pre-outcome operator review (in-cycle accountability); Consumer B's KFR cross-check on PENDING-marked packets surfaces stuck submissions (where outcome ought to have landed but hasn't). Rationale per SCOPING_DRAFT §7 OQ-3 default.

## §3.4 Invariants (finalized — `__post_init__` + canonical-decode re-validate)

The schema sketches enforce the obvious shape; these load-bearing invariants defend against the threat models surfaced in the research findings:

1. `cycle_id` MUST resolve to an existing cycle-close marker span in the Logfire export at PRE-write (else `F-PACKET-CYCLE-ID-UNRESOLVABLE`).
2. `org_slug` MUST resolve to an existing `orgs/<slug>/` subtree AND match the org_slug of every span_id referenced in `span_provenance.per_claim_span_ids` (else `F-PACKET-CROSS-ORG-LEAK`).
3. `schema_version` matches `^\d+\.\d+\.\d+$` (semver).
4. `classification_register_version` is 128-hex-char SHA3-512 digest; matches the operator-signed register at cycle start (else `F-PACKET-CLASS-MISLABEL.register_version_drift`).
5. `emitted_by_seat` is a member of the closed seat registry set; v0.1 = `{"archivist.reflection_submode"}` exclusively.
6. `pattern_observations[i].pattern_summary` and `lessons_proposed[i].pattern_summary` pass three-layer instance-leak detection (NFKC + NER + regex per §15.9.2 RT-07 precedent; else `F-PACKET-INSTANCE-LEAK`).
7. Every `ProposedLesson` with `frequency = 1` MUST have `severity = HIGH` (else `F-PACKET-PREMATURE-GENERALIZATION`).
8. `grounding_signal_classes` MUST contain ≥1 of {external_funder_outcome, operator_approval, logician_gate_outcome, kfr_drift_event, admin_risk_event, match_db_outcome}; MUST NOT be ⊆ {council_split_event, judge_score, red_team_score, editor_verdict} (else `F-PACKET-EVAL-ONLY-GROUNDED`).
9. Every claim_key in `span_provenance.per_claim_span_ids` MUST have ≥1 resolvable Logfire span_id (else `F-PACKET-SPAN-PROVENANCE-MISSING`).
10. `gate_pass_counts.*` aggregates MUST equal aggregated `F-*` counts in the cycle's Logfire span tree (re-validated at consumer-side replay; else `F-PACKET-FABRICATION.gate_count_mismatch`).
11. `score_signals.judge_score` and `red_team_score`, if non-None, MUST equal the deterministic span-derived scores (else `F-PACKET-FABRICATION.score_mismatch`).
12. `outcome.status` non-PENDING REQUIRES `operator_signature_ed25519` non-None AND `outcome.outcome_evidence_span_ids` non-empty.
13. `canonical_bytes_hash` is 128-hex-char SHA3-512 digest matching the canonical-JSON encoding minus the signature fields themselves (mirrors v7.0.4-M1 §2 KFR canonicalization regime byte-for-byte).
14. `producer_signature_ed25519` PRE-consumption verify against producer-seat pubkey (white-glove-pinned per v7.0.7 §6.1 pattern; else `F-PACKET-SIGNATURE-INVALID`).
15. `operator_signature_ed25519` if non-None PRE-consumption verify against operator-pinned pubkey (else `F-PACKET-OPERATOR-SIGNATURE-INVALID`).
16. **OQ-5a tolerant-reader pattern resolved.** Forward-compat: if `schema_version` major-version higher than consumer's known max, consumer at v0.1 hook surfaces `F-PACKET-SCHEMA-DRIFT` advisory (informational); at v1.x consumer (Consumer C scheduled-cadence-driven Archivist) fail-closes. OQ-5b indefinite retention; pruning operator-driven.
17. **OQ-6 resolved.** `outcome.award_amount_minor_units` is `int` cents-precision (minor units of `award_currency` ISO-4217). No sub-cent quantization; no `_micro` precision. Forex multi-currency handled by storing the cycle's `award_currency` as recorded; cross-currency comparison is a downstream concern outside the packet contract.

# §4. F-PACKET-* gate family (final PRE/POST/META layering)

## §4.1 Family scope statement (mirrors §4 v2.x §0.5 family registrations)

**F-PACKET-* gates the ARTIFACT.** F-REFLECTION-* (17 codes per v7.0.9 + §4 v2.x.2) gates the PRODUCER. F-ARCHIVIST-* (5 codes + sub-tag extensions per §15 v1) gates the SUBSTRATE write. F-PACKET-* (this card; new family) gates the artifact (schema validity, signature integrity, provenance preservation, evidence-citation completeness, cross-consumer Law 3 fence).

Owner: §16 Reflection Packet (this card's section). Registered in §4 v2.x.y companion amendment at compound triple LOCK. Per F-CIC-CLC-COUPLING-VIOLATION-class regression: no F-PACKET-* code crosses to §15 or §17 (WPFA); no F-REFLECTION-* code crosses to §16.

## §4.2 Final F-PACKET-* register (19 codes — Path B, predicates NotImplementedError per OQ-2)

| # | Code | Layer | Predicate sketch | v0.1 body state |
|---|------|-------|------------------|------------------|
| 1 | `F-PACKET-INSTANCE-LEAK` | PRE-emission | Three-layer detection (NFKC + NER + regex per §15.9.2 RT-07 precedent) over `pattern_observations[i].pattern_summary` / `lessons_proposed[i].pattern_summary`. Sub-tags `.client_name_present`, `.funder_specific_with_client`, `.reason_attributable_to_specific_outcome`, `.ner_entity_match`, `.unicode_homoglyph`. | NotImplementedError |
| 2 | `F-PACKET-CROSS-ORG-LEAK` | PRE-emission + PRE-load | `org_slug` does not match source path's org or spans' org_slug; substrate-read path resolves outside declared subtree. Mirrors `F-ARCHIVIST-CROSS-ORG-LEAK` byte-for-byte at packet-artifact layer. Sub-tags `.path_outside_org`, `.symlink_escape`, `.span_org_slug_mismatch`. | NotImplementedError |
| 3 | `F-PACKET-FABRICATION` | POST-emission + POST-load | Packet asserts quantitative claim (gate count, score, timing, outcome amount) not matching Logfire span tree. Defends against MemoryGraft / Lane 5 F-13 single-seat false success. Sub-tags `.gate_count_mismatch`, `.score_mismatch`, `.span_id_unresolvable`, `.timing_mismatch`, `.classification_register_version_mismatch`. | NotImplementedError |
| 4 | `F-PACKET-CLASS-SLOT-LEAK` | PRE-emission | Cloud-routable producer emits packet with semantic slot name (`[SLOT_ANNUAL_REVENUE]`) instead of opaque `[SLOT_<numeric_id>]`. Mirrors `F-CLASS-SLOT-ID-NON-OPAQUE` from v7.0.7. | NotImplementedError |
| 5 | `F-PACKET-CLASS-MISLABEL` | PRE-emission | `classification_register_version` does not match operator-signed register at cycle start. Defends against MINJA-shaped in-cycle relabeling. Sub-tags `.register_signature_invalid`, `.register_version_drift`, `.confidential_field_in_shareable_packet`. | NotImplementedError |
| 6 | `F-PACKET-EVAL-ONLY-GROUNDED` | PRE-emission | `grounding_signal_classes` ⊆ {`council_split_event`, `judge_score`, `red_team_score`, `editor_verdict`}. Sibling to producer-side `F-REFLECTION-EVAL-ONLY-GROUNDED` but enforced at artifact-validity layer (defense-in-depth). | NotImplementedError |
| 7 | `F-PACKET-PREMATURE-GENERALIZATION` | PRE-emission | `ProposedLesson` with `frequency = 1` AND `severity != HIGH`. Mirrors lessons.json convention. Operator override per-lesson via SP0-signed exception. Sub-tag `.frequency_one_no_severity`. | NotImplementedError |
| 8 | `F-PACKET-SPAN-PROVENANCE-MISSING` | PRE-emission | Quantitative claim field (`gate_pass_counts.*`, `score_signals.*`, `outcome.award_amount_minor_units`) does NOT have an entry in `span_provenance.per_claim_span_ids` OR has an entry with no resolvable span_id. **Cross-references WPFA `F-WPFA-SPAN-PROVENANCE-MISSING` as sibling pattern — RESOLVES WPFA §6.5 forward-reference at this LOCK.** Sub-tags `.no_trace_id`, `.trace_id_unresolvable_in_logfire`, `.claim_key_unmapped`, `.span_id_from_different_cycle`. | NotImplementedError |
| 9 | `F-PACKET-RETRIEVAL-CORRUPTION` | PRE-load (consumer C) | Packet content includes embedding-shaped triggers (high-entropy token bursts, optimized-trigger fingerprints). Defends against AgentPoison / PoisonedRAG via packet path. Sub-tags `.high_entropy_burst`, `.optimized_trigger_match`, `.embedding_anomaly_detected`. | NotImplementedError |
| 10 | `F-PACKET-MEMORY-INJECTION` | PRE-emission | Free-text fields (`pattern_summary`, `proposed_rule`) contain prompt-injection-shaped substrings. Three-layer detection (regex + Unicode-normalized regex + small classifier). Mirrors MINJA threat model. Sub-tags `.injection_pattern_regex`, `.unicode_normalized_match`, `.classifier_score_above_threshold`. | NotImplementedError |
| 11 | `F-PACKET-SCHEMA-DRIFT` | PRE-load (all consumers) | `schema_version` unknown to consuming code. v0.1 hook = informational advisory per OQ-5a; v1.x consumer = fail-closed. Sub-tags `.unknown_schema_version`, `.required_field_missing`, `.deprecated_field_present`. | NotImplementedError |
| 12 | `F-PACKET-CADENCE-VIOLATION` | PRE-emission | Emission attempted before cycle-close marker is written (i.e., before Uploader has staged). Defends against mid-cycle reflection contaminating producer's own context window. Sub-tags `.no_cycle_close_marker`, `.uploader_not_staged`, `.partial_council_pass`. | NotImplementedError |
| 13 | `F-PACKET-SIGNATURE-INVALID` | PRE-load (all consumers) | `producer_signature_ed25519` does not verify against producer-seat pubkey OR `canonical_bytes_hash` does not match canonical-JSON encoding minus signature fields. Mirrors v7.0.4-M1 §2 KFR canonical-signature-invalid byte-for-byte. | NotImplementedError |
| 14 | `F-PACKET-OPERATOR-SIGNATURE-MISSING` | PRE-load (consumer B + C) | `outcome.status` non-PENDING AND `operator_signature_ed25519` is None. Operator attestation required for outcome-bearing packets per OQ-3 emit+backfill discipline §3.3. | NotImplementedError |
| 15 | `F-PACKET-OPERATOR-SIGNATURE-INVALID` | PRE-load | `operator_signature_ed25519` does not verify against operator-pinned pubkey. | NotImplementedError |
| 16 | `F-PACKET-CYCLE-ID-UNRESOLVABLE` | PRE-emission | `cycle_id` does not resolve to a cycle-close marker span in Logfire export at PRE-write. | NotImplementedError |
| 17 | `F-PACKET-OUTCOME-EVIDENCE-MISSING` | PRE-emission + PRE-load | `outcome.status` non-PENDING AND `outcome.outcome_evidence_span_ids` is empty. | NotImplementedError |
| 18 | `F-PACKET-PRODUCER-UNAUTHORIZED` | PRE-emission | `emitted_by_seat` is not a member of the closed producer-registry set (v0.1 = `{"archivist.reflection_submode"}`). | NotImplementedError |
| 19 | `F-PACKET-COVERAGE-INCOMPLETE` | META (PRE-cycle) | Any F-PACKET-* primitive unrealized at runtime; analog of `F-CLASS-COVERAGE-INCOMPLETE` from v7.0.7 + `F-REFLECTION-COVERAGE-INCOMPLETE` from v7.0.9. PRE-cycle gate prevents v0.2/v1.x consumer deployment shipping without realized predicates. | **LIVE body** at v0.1 hook (META-gate dormant-binding lever; same pattern as F-CLASS-COVERAGE-INCOMPLETE at v7.0.7 §5.1 + F-REFLECTION-COVERAGE-INCOMPLETE at v7.0.9 row 404) |

**Total: 19 codes.** 12 re-cast from research findings Synthesis B under Path B (#1-12) + 7 new from artifact-spec discipline (#13-19). Open to growth at Cycle-1 / Cycle-2 fold-in per L-005 row-170 precedent (anticipate +3-5 codes from Red Team review).

## §4.3 PRE/POST/META distribution (final)

- **PRE-emission** (producer-side, before output_validator commits): 1, 2, 4, 5, 6, 7, 8, 10, 12, 16, 17, 18 — **12 codes**
- **POST-emission / POST-load (artifact-validity replay)**: 3 — **1 code**
- **PRE-load (consumer-side, before any consumer reads)**: 2, 3, 9, 11, 13, 14, 15, 17 — **8 codes (with overlap on #2 and #17 — PRE-emission AND PRE-load)**
- **META (cycle-level, gate-realization-registry)**: 19 — **1 code, LIVE body**

This distribution mirrors §4 v2.x.2 F-REFLECTION-* layering at v0.1 hook scope: most predicates fail-closed at producer output_validator OR consumer PRE-load; one META-gate enforces realization coverage at architectural-primitive layer.

## §4.4 v0.1 hook body state (per OQ-2 (a) resolution)

**18 of 19 predicates: NotImplementedError bodies.** Identical to §4 v2.x.2 F-REFLECTION-* dormant-binding pattern. Predicate signatures present; predicate registries populated; module skeletons authored under `pipeline/logician/gates/f_packet_*.py`; tests scaffolded with `@pytest.mark.skip(reason="v0.1 hook NotImplementedError; body lands at v0.2 first wave")` annotations.

**1 of 19 predicates: LIVE body at v0.1 hook — `F-PACKET-COVERAGE-INCOMPLETE` (#19).** META-gate body inspects the gate-realization-registry; FAIL_CLOSED iff any of the 18 NotImplementedError-bodied predicates lack realized body at runtime. Analog of `F-CLASS-COVERAGE-INCOMPLETE` (v7.0.7 §5.1) and `F-REFLECTION-COVERAGE-INCOMPLETE` (v7.0.9 row 404 per §4 v2.x.2 §0.5 v18). Prevents v0.2 first wave deployment shipping with un-realized predicates.

## §4.5 Cross-family-rigor scope per code (mirrors §4 v2.x row precedent)

Each F-PACKET-* row in the §0.5 amendment carries a `cross_family_rigor_scope` annotation:

- **PRE-emission codes (1, 2, 4, 5, 6, 7, 8, 10, 12, 16, 17, 18)** — author-side enforcement; cross-family check at output_validator hook (the producer's reflection_agent dispatched per Lane 4 idiom). When the producer is cloud-routable AND the input contains `confidential` content, F-CLASS-ROUTING-INDETERMINATE per v7.0.7 forces local-only routing before predicate fires.
- **POST/PRE-load codes (3, 9, 11, 13, 14, 15, 17)** — consumer-side enforcement; cross-family check at consumer principal authentication (Cedar policy mirrors §13 v1 RT-C2-03 OrgScopedBot pattern).
- **META code (19)** — cycle-level enforcement; no cross-family requirement (deterministic Python over gate-realization-registry).

## §4.6 No F-CIC-CLC-COUPLING-VIOLATION-class regression

Per the F-CIC-CLC-COUPLING-VIOLATION enforcement pattern (architecture v7.0.8 amendment 2026-05-08): no F-PACKET-* code crosses to §15 Archivist or §17 WPFA; no F-REFLECTION-* code crosses to §16; no F-ARCHIVIST-* code crosses to §16. AST-lint extension enforces (mirrors `R-ARCHIVIST-NO-CANONICAL-MUTATE` enumeration pattern from §4 v2.x.1 row 198/199): forbid imports of `F-WPFA-*` or `F-REFLECTION-*` or `F-ARCHIVIST-*` from `pipeline/logician/gates/f_packet_*.py` modules; forbid imports of `F-PACKET-*` from `f_reflection_*.py` / `f_archivist_*.py` / `f_wpfa_*.py`.

## §4.7 Module decomposition (per §4 v2.x triplet-collapse precedent)

19 codes; **one module per code** (no triplet-collapse — F-PACKET-* family has no triplet-like clusters that fit the §4 v2.x validation-triplet collapse pattern; all 19 codes are structurally independent).

- 18 modules per NotImplementedError body: `pipeline/logician/gates/f_packet_<code_lowercase>.py` (e.g., `f_packet_instance_leak.py`)
- 1 module per LIVE body: `pipeline/logician/gates/f_packet_coverage_incomplete.py`
- Cedar policy file: `pipeline/logician/cedar/f_packet.cedar` (one file per family; 19 rules, 18 fail-closed-pending-implementation, 1 LIVE)
- Test scaffold: `tests/logician/gates/test_f_packet_*.py` (one test file per module; LIVE module gets real assertions; NotImplementedError modules get `@pytest.mark.skip` regressions on signature only)

# §5. §0.5 v20 row allocation (final)

**Runtime-live state at this dispatch:** §0.5 v19 LOCKED 2026-05-11 (§11 v1.1 paired commit) at runtime-live total 415 rows. Next available row: 416.

**Row range allocated for §0.5 v20 (Reflection Packet amendment):** rows 416-440. **25 rows total** at compound triple LOCK.

| Row | Class | Content |
|---|---|---|
| 416 | marker | `blueprint.amendment_anchor.reflection_packet_v0_1_hook.v1` — Reflection Packet v0.1 Beta hook amendment anchor |
| 417 | failure-code | `reflection_packet.failure_code.F-PACKET-INSTANCE-LEAK.v1` — BINDING (NotImplementedError) — PRE-emission |
| 418 | failure-code | `reflection_packet.failure_code.F-PACKET-CROSS-ORG-LEAK.v1` — BINDING (NotImplementedError) — PRE-emission + PRE-load |
| 419 | failure-code | `reflection_packet.failure_code.F-PACKET-FABRICATION.v1` — BINDING (NotImplementedError) — POST-emission + POST-load |
| 420 | failure-code | `reflection_packet.failure_code.F-PACKET-CLASS-SLOT-LEAK.v1` — BINDING (NotImplementedError) — PRE-emission |
| 421 | failure-code | `reflection_packet.failure_code.F-PACKET-CLASS-MISLABEL.v1` — BINDING (NotImplementedError) — PRE-emission |
| 422 | failure-code | `reflection_packet.failure_code.F-PACKET-EVAL-ONLY-GROUNDED.v1` — BINDING (NotImplementedError) — PRE-emission |
| 423 | failure-code | `reflection_packet.failure_code.F-PACKET-PREMATURE-GENERALIZATION.v1` — BINDING (NotImplementedError) — PRE-emission |
| 424 | failure-code | `reflection_packet.failure_code.F-PACKET-SPAN-PROVENANCE-MISSING.v1` — BINDING (NotImplementedError) — PRE-emission. **SIBLING to F-WPFA-SPAN-PROVENANCE-MISSING (§17 v1 row TBD); resolves WPFA §6.5 forward-reference.** |
| 425 | failure-code | `reflection_packet.failure_code.F-PACKET-RETRIEVAL-CORRUPTION.v1` — BINDING (NotImplementedError) — PRE-load (consumer C) |
| 426 | failure-code | `reflection_packet.failure_code.F-PACKET-MEMORY-INJECTION.v1` — BINDING (NotImplementedError) — PRE-emission |
| 427 | failure-code | `reflection_packet.failure_code.F-PACKET-SCHEMA-DRIFT.v1` — BINDING (NotImplementedError) — PRE-load |
| 428 | failure-code | `reflection_packet.failure_code.F-PACKET-CADENCE-VIOLATION.v1` — BINDING (NotImplementedError) — PRE-emission |
| 429 | failure-code | `reflection_packet.failure_code.F-PACKET-SIGNATURE-INVALID.v1` — BINDING (NotImplementedError) — PRE-load |
| 430 | failure-code | `reflection_packet.failure_code.F-PACKET-OPERATOR-SIGNATURE-MISSING.v1` — BINDING (NotImplementedError) — PRE-load (consumer B + C) |
| 431 | failure-code | `reflection_packet.failure_code.F-PACKET-OPERATOR-SIGNATURE-INVALID.v1` — BINDING (NotImplementedError) — PRE-load |
| 432 | failure-code | `reflection_packet.failure_code.F-PACKET-CYCLE-ID-UNRESOLVABLE.v1` — BINDING (NotImplementedError) — PRE-emission |
| 433 | failure-code | `reflection_packet.failure_code.F-PACKET-OUTCOME-EVIDENCE-MISSING.v1` — BINDING (NotImplementedError) — PRE-emission + PRE-load |
| 434 | failure-code | `reflection_packet.failure_code.F-PACKET-PRODUCER-UNAUTHORIZED.v1` — BINDING (NotImplementedError) — PRE-emission |
| 435 | failure-code | `reflection_packet.failure_code.F-PACKET-COVERAGE-INCOMPLETE.v1` — BINDING (**LIVE body**) — META PRE-cycle. Dormant-binding lever per L-006; analog of F-CLASS-COVERAGE-INCOMPLETE + F-REFLECTION-COVERAGE-INCOMPLETE. |
| 436 | invariant-cluster | `reflection_packet.invariant_cluster.post_init.v1` — `__post_init__` invariant set per §3.4 (17 invariants); canonical-decode re-validation enforced. |
| 437 | invariant-cluster | `reflection_packet.invariant_cluster.canonical_codec.v1` — canonical-JSON encode/decode + SHA3-512 hash regime per §3.4.13; signature-fields-exclusion enforced. |
| 438 | signing-protocol | `reflection_packet.signing_protocol.producer_ed25519.v1` — producer-seat Ed25519 signing; white-glove-pinned pubkey verification per v7.0.7 §6.1 pattern. |
| 439 | signing-protocol | `reflection_packet.signing_protocol.operator_ed25519.v1` — operator Ed25519 attestation on outcome-bearing packets per §3.3 emit+backfill discipline. |
| 440 | retention-policy | `reflection_packet.retention.indefinite_under_org_vault.v1` — OQ-5b indefinite retention under `orgs/<slug>/vault/operational/reflection_packets/` (per v0.2 first wave when sub-kind registers); pruning operator-driven; no automatic aging at v0.1 hook scope. |

**Runtime-live total at this LOCK: 440 rows** (415 + 25 new rows = 440).

**Kind-of-amendment classification:** row-append + invariant-cluster-extension + signing-protocol-extension + retention-policy. The §0.5 v20 vocabulary extension claims `invariant-cluster`, `signing-protocol`, and `retention-policy` as primitive kinds — verify against §0.5 v5 + v18 + v19 vocabulary closed set at dispatch; if unclaimed in current vocabulary, this amendment paired-commits a vocabulary extension at LOCK (mirrors §17 WPFA v1's `ast-lint` kind extension precedent per memory entry `project_blueprint_section_17_wpfa_v1_locked.md`).

# §6. Sub-kind registry update for §2 v7.x — DEFERRED per OQ-2 (a)

**At v0.1 hook scope, NO §2 v7.x amendment lands.** OQ-2 (a) resolution: dormant hook only; schema + signing primitives + 19 F-PACKET-* predicate signatures at architectural-primitive layer; no live emission.

**Schema module IS authored at v0.1 hook** at `pipeline/vault/sub_kinds/reflection_packets.py` — module file exists, `ReflectionPacket` + `PatternObservation` + `ProposedLesson` + `GatePassCounts` + `ScoreSignals` + `CycleOutcome` + `PacketSpanProvenance` dataclasses are defined with full invariants per §3, canonical-codec helpers (`to_canonical_bytes`, `from_canonical_bytes`) are scaffolded. **But the SUB_KIND_REGISTRY entry under operational/reflection_packets/ is NOT registered at v0.1 hook.** The registry entry lands at v0.2 first wave compound LOCK paired with §15 v2.x Archivist Reflection sub-mode SPEC.

**Why deferred:** §2 v7.x SUB_KIND_REGISTRY entries are read by Vault write/read dispatch. At v0.1 hook with no live emission, no Vault dispatch reads the entry. Premature registration would introduce a registered-but-never-used entry — a stale-binding hazard. Defer to v0.2 when live emission lands and the Vault dispatch can actually use the entry.

**v0.2 first wave transition:** compound paired LOCK lands:
- §16 v1.1 amendment (registers SUB_KIND_REGISTRY entry; flips producer to live emission)
- §2 v7.x amendment (registers sub-kind under operational/reflection_packets/)
- §4 v2.x.y.1 amendment (flips 18 NotImplementedError predicates to live bodies; F-PACKET-COVERAGE-INCOMPLETE META-gate validation against live bodies)
- §15 v2.x Archivist Reflection sub-mode SPEC amendment (producer behavior at v0.2; ties to §16 v1.1 producer flip)
- §0.5 v?? amendment (paired-commit rows for the v0.2 transitions)

**v1.x runtime transition:** further paired LOCK lands scheduled-cadence-driven Consumer C (Archivist learning loop) consumption with PRE-load gates live.

# §7. OQ disposition log

All 6 SCOPING_DRAFT OQs resolved by operator decision 2026-05-11. Verbatim resolution + rationale captured:

**OQ-1. Section number → §16** (synthesis default confirmed). Rationale: honors WPFA spec card §2 reservation; preserves Tilth-internal-vs-buyer-external axis at §-numbering layer; topical clustering with §15 Archivist (which consumes ReflectionPackets at v1.x runtime). Non-blocking; resolved.

**OQ-2. Ship window → (a) v0.1 Beta dormant hook only** (BLOCKING; operator-decision lever). Rationale: mirrors Reflection sub-mode v0.1 hook posture (LOCKed 2026-05-10 rows 202/203/204); minimizes Beta close-out competition (parallel to Intake full-impl, Uploader full-impl, WS-L §4 v2.x Code phase, white-glove playbook); predicate bodies stay NotImplementedError at v0.1 hook; live emission lands at v0.2 SPEC alongside §15 v2.x; resolves WPFA forward-reference (`F-PACKET-SPAN-PROVENANCE-MISSING`) at v0.1 compound triple LOCK. RESOLVED.

**OQ-3. Outcome backfill → (b) emit at submission with PENDING + backfill at outcome event** (synthesis default confirmed). Rationale: pre-outcome packet is useful to Consumer A (operator review for in-cycle accountability) and Consumer B (KFR cross-check on PENDING-marked packets surfaces stuck submissions). Two packets per cycle, linked by shared `cycle_id`; second packet requires `operator_signature_ed25519` per F-PACKET-OPERATOR-SIGNATURE-MISSING. RESOLVED.

**OQ-4. Operator-notes field → (a) no operator_notes field on the packet** (synthesis default confirmed). Rationale: packet stays the deterministic spine; operator commentary lives entirely in the §15 sub-mode's adjacent substrate; MINJA threat surface contained. Closes the prompt-injection-via-commentary-field vector at the schema layer rather than relying on F-PACKET-MEMORY-INJECTION sub-tag expansion. RESOLVED.

**OQ-5. Schema versioning + retention → (5a) tolerant-reader pattern at consumer (v0.1 advisory / v1.x fail-closed); (5b) indefinite retention.** Both synthesis defaults confirmed. Rationale: tolerant-reader matches the OQ-5a advisory layer in invariant §3.4.16; indefinite retention matches Tilth-internal substrate cost profile (storage is negligible; pruning is operator-driven). RESOLVED.

**OQ-6. Award amount precision → `_minor_units` cents-precision** (synthesis default confirmed; no `_micro` extension). Rationale: no sub-cent grants in practice; multi-currency handled by recording `award_currency` ISO-4217 alongside the amount; cross-currency comparison is a downstream concern outside the packet contract. RESOLVED.

**Net effect:** all 6 OQs resolved per synthesis defaults. No Thesis-side OQ-decision-blocking items remain. Cycle 1 author proceeds with §16 v1 + §4 v2.x.y + §0.5 v20 compound triple draft.

# §8. Dispatch readiness checklist

- [x] All 6 SCOPING_DRAFT OQs resolved by operator (§7 disposition log).
- [x] §16 numbering rationale captured (§2); honors WPFA spec card §2 reservation.
- [x] Full ReflectionPacket schema authored with 17 finalized invariants (§3.4).
- [x] F-PACKET-* family register finalized at 19 codes with PRE/POST/META layering (§4).
- [x] Module decomposition per §4 v2.x precedent: 19 modules, one per code, Cedar policy file, test scaffold (§4.7).
- [x] v0.1 hook body state: 18 NotImplementedError + 1 LIVE META-gate (`F-PACKET-COVERAGE-INCOMPLETE`) (§4.4).
- [x] §0.5 v20 row allocation: 25 rows starting at 416; runtime-live total 440 post-LOCK (§5).
- [x] Sub-kind registry update DEFERRED to v0.2 first wave (§6).
- [x] Cross-family-rigor scope annotation per code (§4.5).
- [x] F-CIC-CLC-COUPLING-VIOLATION-class regression discipline applied to F-PACKET-* (§4.6).
- [x] Sibling-not-nested verification with WPFA: ZERO shared output / consumer / schema / gate-family; one cross-reference at F-PACKET-SPAN-PROVENANCE-MISSING ↔ F-WPFA-SPAN-PROVENANCE-MISSING.
- [x] Thesis dispatch packet pre-staged at `pipeline/handoffs/ws_reflection_packet_handoff_2026-05-11.md` (companion file landed alongside this promotion).
- [ ] Compound triple LOCK fires from the pre-staged Thesis packet at a separate session (per CLAUDE.md "Thesis dispatch fires as separate session").

**Anticipated rows at compound LOCK:** 211/212/213 (verify against runtime-live row at dispatch time; if other LOCKs land between this promotion and Thesis dispatch, shift accordingly). Three siblings — NOT four — per OQ-2 (a) v0.1 hook scope (§1).

# §9. Sibling-not-nested verification (with WPFA CycleReceipt and Reflection sub-mode producer)

| Axis | §16 ReflectionPacket (this card) | §17 WPFA CycleReceipt | §15 Reflection sub-mode (producer) |
|------|----------------------------------|------------------------|--------------------------------------|
| Trigger | Cycle close + decision-observed | Cycle close | Cycle close (when invoked) |
| Input substrate | Logfire span tree + KFR + Match DB + Admin-risk ledger | Logfire span tree + Coefficient Registry | Logfire span tree + lessons memory + prior packets (v1.x) |
| Producer | `archivist.reflection_submode` (one) | Cycle Accountant (deterministic module, no LLM) | `archivist.reflection_submode` (one) — produces THIS card's artifact |
| Primary consumer | Archivist learning loop (A: operator review; B: KFR cross-check; C: v1.x scheduled) | Operator dashboard + buyer-facing PDF | (n/a — producer, not artifact) |
| Audience | Tilth-internal + operator | Operator + external buyer | Tilth-internal |
| Schema | ReflectionPacket (§3) | CycleReceipt (§17 v1 §3) | (n/a — producer behavior, not data shape) |
| Signing | producer Ed25519 + operator Ed25519 (required for outcome-bearing packets) | operator Ed25519 (optional pre-buyer-export) | (n/a — producer behavior signs the artifact this card defines) |
| Gate family | F-PACKET-* (19 codes; this card) | F-WPFA-* (12 codes; §17 v1 §6) | F-REFLECTION-* (17 codes; v7.0.9 + §4 v2.x.2) |
| Cross-reference | F-PACKET-SPAN-PROVENANCE-MISSING ↔ F-WPFA-SPAN-PROVENANCE-MISSING (sibling pattern) | (mirror) | F-REFLECTION-* gates the producer; F-PACKET-* gates the artifact the producer emits |

**Zero shared output. Zero shared consumer. Zero shared schema field. Zero F-* code crossing.** F-CIC-CLC-COUPLING-VIOLATION-class regression test at every Thesis cycle ensures no F-PACKET-* code crosses to §15 or §17; no F-REFLECTION-* code crosses to §16; no F-ARCHIVIST-* code crosses to §16; no F-WPFA-* code crosses to §16.

# §10. Done definition (this dispatch spec card)

- [x] SCOPING_DRAFT promoted to DISPATCH_SPEC_DRAFT (this file filed at `pipeline/planning/reflection_packet_dispatch_spec_2026-05-11.md`).
- [x] All 6 OQs from SCOPING_DRAFT §7 resolved by operator with verbatim disposition + rationale (§7 of this card).
- [x] Compound-LOCK pairing identity finalized at 3 siblings (§16 v1 + §4 v2.x.y + §0.5 v20); NOT 4 like WPFA, per OQ-2 (a) (§1).
- [x] Full schema (§3) + invariants (§3.4) + F-PACKET-* family (§4) + §0.5 row allocation (§5) + sub-kind registry deferral (§6) + sibling-not-nested verification (§9).
- [x] Thesis dispatch packet pre-staged at `pipeline/handoffs/ws_reflection_packet_handoff_2026-05-11.md` (companion file).
- [x] Filed at `pipeline/planning/reflection_packet_dispatch_spec_2026-05-11.md`.
- [ ] (Out of scope for this card) Pre-Thesis reconciliation update at `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md` adding one-line entry confirming Path B adopted + this spec card's authoring path. Coordinator handles at dispatch fire.

**No Thesis dispatch. No LOCK ceremony. No row reservation against §0.5 until paired blueprint amendments land at compound triple LOCK.** The Thesis dispatch fires from the pre-staged packet (§8) as a separate session.

# §11. Hand-back

This dispatch spec card is filed. The pre-staged Thesis dispatch packet at `pipeline/handoffs/ws_reflection_packet_handoff_2026-05-11.md` is ready to fire when coordinator bandwidth opens. Anticipated total cost: 3-4 sessions — 1 Thesis Cycle 1 + 1 Thesis Cycle 2 + 1 compound triple LOCK ceremony with companion edits + (conditionally) 1 fold-in author session if Cycle-1 surfaces NEW probes per L-005 row-170 precedent.

**Coordinator:** the §16 + F-PACKET-* registration plan is Thesis-ready. Fire when bandwidth opens; concurrent with WS-J Code Slice 1 + WS-FG Funding Goal Thesis + WPFA Code Phase (different surfaces — no conflict).

## Sources

- pipeline/planning/reflection_packet_scoping_draft_2026-05-10.md (SCOPING_DRAFT this card promotes; 6 OQ batch consolidated here)
- pipeline/planning/operator_spec_card_status_2026-05-10.md (orchestrator discovery report — Q2 default = "yes, separate spec card" confirmed by operator)
- pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md (Path B = F-PACKET-* separate family adopted here)
- pipeline/research/reflection/synthesis_design_memo_2026-05-10.md (Reflection sub-mode design — agent, not artifact; producer of this card's artifact)
- pipeline/research/reflection_packet_grounding/findings_2026-05-10.md (5-lane research; Synthesis B 12-code register re-cast under Path B in §4.2)
- pipeline/handoffs/ws_wpfa_handoff_2026-05-10.md (sibling spec card pattern; WPFA defines its packet artifact format byte-for-byte mirroring this card)
- pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md (Reflection sub-mode v0.1 hook — producer LOCKed 2026-05-10 rows 202/203/204)
- pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md (KFR canonical-JSON Ed25519 signing pattern this card mirrors)
- pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md (classification-driven routing + opaque slot discipline applies to cloud-routed packet reads)
- pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md (Reflection sub-mode v0.1 hook — producer LOCK row 202; this card's F-PACKET-* is sibling at architectural-primitive layer)
- pipeline/blueprint/v0.1/section_02_v7_2_amendment.md (sub-kind registry pattern — Reflection Packet candidate sub-kind DEFERRED to v0.2 per §6)
- pipeline/blueprint/v0.1/section_04_v2_x_amendment.md (failure-code family registration pattern)
- pipeline/blueprint/v0.1/section_04_logician_v2_x_2_amendment.md (Reflection sub-mode hook predicate signatures — F-REFLECTION-* family; F-PACKET-* must NOT collide)
- pipeline/blueprint/v0.1/section_15_archivist.md (§15 v1 LOCK — proposes-only Archivist seat owning the Reflection sub-mode that produces this artifact)
- pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md (§17 v1 LOCK — sibling artifact; WPFA §6.5 forward-reference to F-PACKET-SPAN-PROVENANCE-MISSING resolved at this card's compound triple LOCK)
- pipeline/blueprint/v0.1/section_11_intake_v1_1_amendment.md (most recent LOCK; runtime-live total at §0.5 v19 = 415; this card claims rows 416-440)

---

**Filed:** 2026-05-11. DISPATCH_SPEC_DRAFT — pre-Thesis, no LOCK ceremony, no row reservation. Thesis dispatch fires from the pre-staged packet (§8) as a separate session.
