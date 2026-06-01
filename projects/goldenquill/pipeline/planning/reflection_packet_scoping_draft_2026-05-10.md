---
title: Reflection Packet — Scoping Draft (artifact spec; sibling-to-WPFA at the artifact layer)
filed: 2026-05-10
operator: Josh Inklovich
status: SCOPING_DRAFT — pre-Thesis, no LOCK ceremony, no row reservation against §0.5, no Cedar/Python written. Operator review pass + Thesis dispatch fire as separate sessions after operator weighs in on the OQ batch (§7).
authority: orchestrator dispatch 2026-05-10 — author the engineer-facing artifact schema for the cycle-close reflection record that the §15 Archivist Reflection sub-mode (LOCKed today rows 202/203/204) emits. Operator confirmed (Q2) that a separate spec card IS needed: the Reflection synthesis design memo + Lessons Memory one-pager are operator/customer-facing surfaces; this card is the engineer-facing artifact schema.
audit_class: spec_card_for_blueprint_amendment_family — when promoted past SCOPING_DRAFT, becomes a compound-LOCK candidate covering §16 v1 (new section) + §4 v2.x.y F-PACKET-* family + §0.5 v?? amendment + (conditionally) §2 v7.x cycle-close packet sub-kind. SCOPING_DRAFT now means: schema sketch + producer/consumer contracts + gate-family sketch + OQ batch. Spec card consolidation lands at a separate authoring session after operator answers OQs in §7.
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                             # v7 LOCKED 2026-04-19 A1–A12; A12 Decimal mandate; A4 operator-trusted preflight
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md                      # v7.0.4-M1 LOCKED 2026-05-10 row 190 — KFR canonical-JSON signing regime; Ed25519 signature discipline this card mirrors byte-for-byte for the Reflection Packet artifact
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                         # v7.0.7 LOCKED 2026-05-10 row 180 — classification-driven routing + opaque [SLOT_<numeric_id>] discipline applies to any cloud-routed read of a packet
  - pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md                         # v7.0.9 LOCKED 2026-05-10 row 202 (Reflection sub-mode v0.1 hook) — registers F-REFLECTION-* family at architectural-primitive layer; this card's F-PACKET-* family is a SIBLING, not a child
  - pipeline/blueprint/v0.1/section_02_v7_2_amendment.md                                # §2 v7.2 LOCKED 2026-05-10 row 186 — sub-kind registry pattern; Reflection Packet is a candidate new sub-kind under operational/reflection_packets/
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                                # §4 v2.x LOCKED 2026-05-10 rows 193/194 — failure-code family registration pattern; F-PACKET-* follows format
  - pipeline/blueprint/v0.1/section_04_logician_v2_x_2_amendment.md                     # §4 v2.x.2 LOCKED 2026-05-10 row 203 (Reflection sub-mode hook) — registers 17 F-REFLECTION-* predicate signatures; F-PACKET-* must NOT collide
  - pipeline/blueprint/v0.1/section_15_archivist.md                                     # §15 v1 SPEC LOCKED 2026-05-10 row 191/192 — proposes-only Archivist seat; F-ARCHIVIST-* parents
  - pipeline/research/reflection/synthesis_design_memo_2026-05-10.md                    # Reflection sub-mode design synthesis — distinguishes the AGENT (producer) from the ARTIFACT (packet) this card specs
  - pipeline/research/reflection_packet_grounding/findings_2026-05-10.md                # 5-lane research findings; Synthesis B § proposes a 12-code register currently named F-REFLECTION-* — this card RE-CASTS that register under F-PACKET-* per Path B
  - pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md           # Path B recommendation; this card adopts Path B as its naming discipline
  - pipeline/planning/watts_per_funding_action_spec_2026-05-10.md                       # WPFA spec card — sibling-not-nested artifact; cross-references F-PACKET-SPAN-PROVENANCE-MISSING (this card defines that code)
related_handoffs:
  - pipeline/handoffs/ws_wpfa_handoff_2026-05-10.md                                     # WPFA Thesis dispatch packet — sibling artifact; Cycle 1 absorption applies the F-PACKET-* documentary edit
  - pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md                     # Reflection sub-mode v0.1 hook (LOCKed today) — producer of this artifact
sibling_artifacts:
  - WPFA CycleReceipt (operator/buyer-facing accounting)                                 # both emit at cycle close, both consume Logfire span tree, ZERO shared output/consumer/schema/gate-family
naming_path: Path B — F-PACKET-* family; F-REFLECTION-* stays reserved for §15 Archivist sub-mode (producer); F-ARCHIVIST-* stays reserved for Vault substrate writes. Three orthogonal owners.
---

# §0. What this card is, and what it is NOT

**This card specs the ARTIFACT.** The Reflection Packet is a typed Pydantic record emitted once per grant cycle close. It carries the structured facts a cycle produced — gate-pass counts, score deltas, pattern observations, outcome status — in a form the Archivist Reflection sub-mode can later consume to propose lessons-memory deltas. The packet is the *contract* between the producing agent (§15 Archivist's third cadence, LOCKed today at row 191/192 + the Reflection sub-mode v0.1 hook at row 202/203/204) and downstream consumers (operator review surface; KFR cross-check via F-LOGICIAN-FACT-DRIFT; future v1.x reflection-cadence-driven invocation).

**This card is NOT the agent.** The Reflection sub-mode design memo at `pipeline/research/reflection/synthesis_design_memo_2026-05-10.md` covers the producer's seat-home, cadence, classification posture, prompt-template inoculation frame, and the 17 F-REFLECTION-* primitives that gate the *producer's* behavior. Reading the agent spec and assuming it covers the artifact is the disambiguation hazard this card exists to close.

**Three orthogonal gate-family owners.** The producer (Reflection sub-mode) is gated by F-REFLECTION-* (17 top-level codes registered in v7.0.9 / §4 v2.x.2). The substrate write of the packet to disk is gated by F-ARCHIVIST-* (5 codes + sub-tag extensions per §15 v1 LOCK). The artifact itself is gated by F-PACKET-* (this card; new family). No code crosses ownership. Per Path B naming reconciliation: `F-PACKET-*` never `F-REFLECTION-PACKET-*` (would collide with the producer family at the prefix layer).

**Sibling-not-nested with WPFA.** WPFA CycleReceipt and Reflection Packet share the cycle-close trigger and the Logfire span tree as input substrate. They emit independent Pydantic BaseModels to different consumers (CycleReceipt → operator dashboard + buyer-facing PDF; Reflection Packet → Archivist learning loop). Zero shared output, zero shared consumer, zero shared schema. Their gate families (F-WPFA-* / F-PACKET-*) are siblings under §4 v2.x.z with parallel SPAN-PROVENANCE-MISSING discipline; the WPFA spec card §6.5 row references `F-PACKET-SPAN-PROVENANCE-MISSING` as the parallel code on the Reflection Packet side, defined here.

# §1. Why a SCOPING_DRAFT rather than a full DISPATCH_SPEC_DRAFT

Three reasons the artifact-vs-agent distinction has been deferred to a scoping pass rather than rolled directly into the Reflection sub-mode synthesis:

1. **The producer LOCK landed first.** §15 Archivist Reflection sub-mode v0.1 hook LOCKed today (compound triple rows 202/203/204). The producer's predicates fire at PRE/POST-write of the *substrate* (lessons memory writes). The packet artifact is one possible substrate write — but the producer also writes proposed-lesson-deltas, digest summaries, and operator-review staging documents. Specifying the artifact AFTER the producer LOCK lets the artifact be one shape the producer can emit, not the only shape.

2. **The Reflection Packet has a v0.1 / v0.2 scope question of its own.** v0.1 cycle close exists today (Uploader prepare-and-stage → operator submit → cycle close marker). The Reflection sub-mode's runtime invocations are v1.x horizon per §15 J-06 slot transition. The Reflection Packet could ship: (a) at v0.1 Beta dormant — schema + signing primitives only, no live emission; (b) at v0.2 — packet emission live but Archivist consumption still operator-cadenced; (c) at v1.x — full scheduled-cadence-driven consumption. Operator decision (OQ-2 in §7) drives this.

3. **WPFA cross-reference creates a forcing function.** WPFA spec card §6.5 cites `F-PACKET-SPAN-PROVENANCE-MISSING` as a parallel code. WPFA Thesis Cycle 1 fires before WPFA LOCKs — either this card lands first (so the cross-reference resolves), or WPFA Cycle 1 absorbs a documentary-only edit pointing forward to this card. Path B reconciliation chose the latter; but the longer this card stays SCOPING_DRAFT, the more brittle that forward-reference becomes.

# §2. Section number proposal — §16

WPFA spec card §2 reserved §16 for the Reflection Packet design. Rationale stands: §15 Archivist + §16 Reflection Packet form the Tilth-internal between-cycle preservation cluster; §17 WPFA is the buyer-facing-accounting boundary. §16 captures the artifact spec + emission orchestrator + cross-references to §15's consumption contract. Companion subsection layout (provisional, finalized at spec-card consolidation): §16.1 schema; §16.2 emission contract + producer interface; §16.3 consumer contracts; §16.4 signing regime; §16.5 versioning + retention; §16.6 F-PACKET-* family overview (registry lives in §4 v2.x.y amendment).

**OQ-1 (operator-decision):** confirm §16 for Reflection Packet, or pick a different number. Default = §16. See §7.

# §3. Artifact schema (sketch — finalized at spec-card consolidation)

Following the §2 v7.2 sub-kind convention EXACTLY: `@dataclass(frozen=True, kw_only=True)`; one record = one file; SIMPLE class; `write-if-absent` mode; `__post_init__` invariant validation; canonical-JSON encode/decode round-trip; SUB_KIND_REGISTRY entry under operational/reflection_packets/; schema module at `pipeline/vault/sub_kinds/reflection_packets.py`.

## §3.1 Top-level shape

```python
@dataclass(frozen=True, kw_only=True)
class ReflectionPacket:
    # Identity + provenance (mirrors WPFA CycleReceipt frontmatter)
    packet_id: str                                       # opaque caller-minted ID; matches filename {packet_id}.json
    cycle_id: str                                        # foreign key into the cycle this packet records; matches §5 v8 track-registry cycle close marker
    org_slug: str                                        # Law 3 binding; resolves to existing orgs/<slug>/ subtree at PRE-write
    schema_version: str                                  # semver string, e.g., "1.0.0"; tolerant-reader pattern at consumer per Lane 5 / Lane 3 reflection
    classification_register_version: str                 # SHA3-512 hash of the operator-signed classification register at cycle start; mirrors v7.0.7 §6.1 discipline

    # Emission context
    emitted_at: str                                      # UTC ISO-8601 'Z'
    emitted_by_seat: str                                 # canonical seat identifier of the producer; v0.1 Beta = "archivist.reflection_submode"; closed set, validated against seat registry
    cycle_close_marker_span_id: str                      # the Logfire span ID for the cycle-close marker; bridges packet → cycle's actual run trace

    # Pattern-level observations (per Lane 3 ExpeL / §15.9.2 instance-leak precedent)
    pattern_observations: tuple[PatternObservation, ...]  # zero-or-more pattern records; instance-level details refused at PRE-write per F-PACKET-INSTANCE-LEAK
    lessons_proposed: tuple[ProposedLesson, ...]          # zero-or-more pattern-rolled lessons; frequency ≥ 2 OR severity = HIGH per F-PACKET-PREMATURE-GENERALIZATION

    # Quantitative signals (every value MUST trace to a Logfire span; see span_provenance)
    gate_pass_counts: GatePassCounts                      # F-*-PASS / FAIL / SKIP counts per gate family observed in cycle
    score_signals: ScoreSignals                            # Judge / Red Team / Editor verdicts; deterministic field-level fields ONLY (no free-text)
    outcome: CycleOutcome                                  # status = PENDING / AWARDED / DECLINED / NO_DECISION; backfilled per OQ-3

    # Grounding signal class declarations (per §15 synthesis §3.1 — F-REFLECTION-* discipline at producer-side; mirrored here at artifact-side)
    grounding_signal_classes: frozenset[str]              # MUST contain ≥1 of {external_funder_outcome, operator_approval, logician_gate_outcome, kfr_drift_event, admin_risk_event, match_db_outcome}; council_split_event admitted but not alone; LLM-eval-only refused

    # Provenance — every quantitative claim must trace
    span_provenance: PacketSpanProvenance                 # trace_ids[], per_claim_span_ids; mirrors WPFA SpanProvenance pattern byte-for-byte

    # Signing regime (per v7.0.4-M1 KFR canonical-JSON Ed25519 pattern)
    canonical_bytes_hash: str                              # SHA3-512 of canonical-JSON-encoded packet (excluding signature field itself); 128 hex chars
    producer_signature_ed25519: str                        # producer-emitted Ed25519 signature; verifies against producer-seat pubkey at PRE-consumption
    operator_signature_ed25519: str | None                 # operator-attest signature; required for outcome.status non-PENDING per F-PACKET-OPERATOR-SIGNATURE-MISSING; None acceptable while status=PENDING
```

## §3.2 Field sub-shapes (sketch)

```python
@dataclass(frozen=True, kw_only=True)
class PatternObservation:
    pattern_summary: str                                  # pattern-LEVEL text; instance-level identifiers (client name, specific funder name, specific reason) refused
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
    f_reflection_pass: int                                 # producer-side gates
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
    award_amount_minor_units: int | None                   # int per A12 Decimal mandate; None if status ≠ AWARDED
    award_currency: str | None                             # ISO-4217 alpha-3; None if status ≠ AWARDED
    decision_observed_at: str | None                       # UTC ISO-8601 'Z'; None if status = PENDING
    outcome_evidence_span_ids: tuple[str, ...]             # ≥1 if status non-PENDING; refused empty per F-PACKET-OUTCOME-EVIDENCE-MISSING


@dataclass(frozen=True, kw_only=True)
class PacketSpanProvenance:
    trace_ids: tuple[str, ...]                             # ≥1; one or more Logfire trace IDs covered by this packet
    logfire_export_uri: str | None                         # optional pointer to a Logfire export bundle for offline audit
    per_claim_span_ids: dict[str, tuple[str, ...]]         # claim_key (e.g., "gate_pass_counts.f_logician_total_pass") → ≥1 span_ids backing it
```

## §3.3 Invariants (sketch — `__post_init__` + canonical-decode re-validate; finalized at spec-card consolidation)

The schema sketches enforce the obvious shape; the load-bearing invariants are the ones that defend against the threat models surfaced in the research findings:

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
16. Forward-compat: if `schema_version` major-version higher than consumer's known max, consumer falls through to tolerant-reader path AND surfaces `F-PACKET-SCHEMA-DRIFT` advisory (informational at v0.1; fail-closed at v1.x consumer when Archivist consumption runtime lands).

# §4. Producer contract (one producer, well-bounded)

## §4.1 Sole producer

`archivist.reflection_submode` — the §15 Archivist Reflection sub-mode (compound LOCK rows 191/192 + 202/203/204). No other seat may emit a ReflectionPacket. PRE-write gate `F-PACKET-PRODUCER-UNAUTHORIZED` fail-closes any emission from a seat outside the closed registry set.

This is structurally narrower than the §15 sub-mode's broader emission surface (which also emits proposed-lesson-deltas, digest summaries, and operator-review staging docs). The packet is ONE of the sub-mode's emission shapes; the sub-mode's other emissions are gated by F-REFLECTION-* alone and never touch F-PACKET-*.

## §4.2 Cadence

v0.1 Beta hook: **dormant**. No live packet emission. Schema + signing primitives + F-PACKET-* gate predicate signatures registered at architectural-primitive layer (matches L-006 dormant-binding pattern + the v0.1 Beta hook treatment of the Reflection sub-mode itself).

v0.2 (provisional, see OQ-2): **operator-invoked at cycle close**. Operator runs `tilth archivist reflection --org <slug> --emit-packet` after Uploader has staged the cycle close marker. Packet writes to `orgs/<slug>/vault/operational/reflection_packets/<packet_id>.json` per §3 schema.

v1.x (provisional): **scheduled-cadence-driven** per §15 J-06 slot transition. Auto-emission at cycle close marker write; outcome backfill at decision-observed event.

## §4.3 Input evidence — closed set

The producer reads from these substrates and ONLY these substrates when composing a packet:

1. **Logfire span tree for `cycle_id`** — gate pass/fail counts, score signals, council-split event, timing, cross-family-rigor satisfaction. Span data is the deterministic ground truth; pattern_observations may NOT contradict span-derived counts (else F-PACKET-FABRICATION at consumer-side replay).
2. **Classification register signed at cycle start** — `classification_register_version` field.
3. **Operator-signed seat registry** — `emitted_by_seat` validation.
4. **KFR canonical snapshot at cycle close** — for outcome.funder_id resolution and `kfr_drift_event` grounding signal class detection. Read-only via the existing F-LOGICIAN-FACT-DRIFT cross-check surface.
5. **Match DB rollup at cycle close** — for outcome.status backfill and `match_db_outcome` grounding signal class detection.
6. **Admin-risk ledger** — for `admin_risk_event` grounding signal class detection.

The producer does NOT read free-text operator commentary or session transcripts directly for packet composition. (Operator commentary, if any, lives in a separate substrate the §15 sub-mode handles per its own seat spec — never propagated into packet free-text fields, which would re-introduce MINJA threat surface per Lane 5.)

## §4.4 Output validator hook

Per Lane 4: emission travels through Pydantic AI `@agent.output_validator` on the producer's reflection_agent dispatcher. F-PACKET-* PRE-emission gates fire at output_validator. On validation failure, emission journal entry preserved (Rule 1) but packet never reaches `orgs/<slug>/vault/operational/reflection_packets/` live state (journal-and-commit pattern mirrors §12 Uploader prepare-and-stage).

# §5. Consumer contracts (three named consumers; no others)

## §5.1 Consumer A — Operator review surface

Operator runs `tilth archivist review --org <slug> --reflection-packet <packet_id>` to load a packet for human review. Read path: existing `vault_read_intent_reflection_packet` wrapper (NEW; lands in §2 v7.x amendment paired with this card's LOCK). Read intent is logged (F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT-class enforcement applies at the substrate read layer).

PRE-load gates on the consumer side: `F-PACKET-SIGNATURE-INVALID`, `F-PACKET-CANONICAL-BYTES-HASH-MISMATCH`, `F-PACKET-SCHEMA-DRIFT` (informational at v0.1), `F-PACKET-CROSS-ORG-LEAK` (PRE-load fence; defense-in-depth against tampered-org-slug-on-disk).

Operator reviews + signs (or rejects). Operator's Ed25519 signature lands on `operator_signature_ed25519`. Subsequent reads (Archivist learning loop) see the operator-attested packet.

## §5.2 Consumer B — KFR cross-check via F-LOGICIAN-FACT-DRIFT

The KFR fact-drift detector (existing in §4 v2.x; F-LOGICIAN-FACT-DRIFT) reads packets at quarterly cadence to detect cases where the packet's claimed outcome (e.g., outcome.award_amount_minor_units) drifts against the KFR's canonical signed fact for the same funder + cycle.

Read interface: `read_packets_for_funder_cross_check(funder_id, cycle_id_range)`. Read-intent classification: `confidential` (packets carry operator-Ed25519-signed outcome data; cloud routing is refused per v7.0.7).

PRE-load gates on the consumer side: same as §5.1 + additional `F-PACKET-OUTCOME-EVIDENCE-MISSING` (an outcome.status non-PENDING packet without supporting span_ids is itself a fact-drift signal even before the KFR comparison happens).

This consumer is in scope from v0.1 onward (F-LOGICIAN-FACT-DRIFT is already LOCKed); but it is dormant until the producer ships at v0.2.

## §5.3 Consumer C — v1.x runtime reflection-cadence-driven invocation

When §15 J-06 slot transitions and the Reflection sub-mode's scheduled-cadence-driven invocation activates, the sub-mode reads its own prior packets to construct second-order observations (reflections of reflections, depth-bounded per F-REFLECTION-DEPTH-EXCEEDED on the producer side).

Read interface: `read_priors_for_reflection(org_slug, depth_bound=1)`. Read-intent classification: `confidential` (defense-in-depth even for self-reads).

PRE-load gates: same as §5.1 + `F-PACKET-RETRIEVAL-CORRUPTION` (defense against AgentPoison-style embedding-shaped triggers in packet content per Lane 5).

Out of scope for v0.1; in scope for v1.x amendment.

## §5.4 No other consumers

No other seat reads ReflectionPackets. Closed-set membership enforced by `vault_read_intent_reflection_packet` wrapper at substrate layer. Cedar policy refuses read intent for principals outside the closed consumer set.

# §6. F-PACKET-* gate family (Path B; new family, no collision)

## §6.1 Family scope statement (mirrors §4 v2.x §0.5 family registrations)

**F-PACKET-* gates the ARTIFACT.** The 17 F-REFLECTION-* codes gate the PRODUCER (Reflection sub-mode's prompt template, grounding signal discipline, content-loop / inoculation-frame / depth bounds — the *behavior* of the agent that emits packets). The 5+ F-ARCHIVIST-* codes gate the SUBSTRATE (cross-org reads, auto-apply attempts, lesson-instance leaks at the Vault write layer). F-PACKET-* gates the ARTIFACT (schema validity, signature integrity, provenance preservation, evidence-citation completeness, cross-consumer Law 3 fence) — the *thing* that passes between producer and consumers.

Owner: §16 Reflection Packet (this card's section). Registered in §4 v2.x.y companion amendment when this card promotes past SCOPING_DRAFT. Per F-CIC-CLC-COUPLING-VIOLATION-class regression: no F-PACKET-* code crosses to §15 or §17 (WPFA); no F-REFLECTION-* code crosses to §16.

## §6.2 Initial F-PACKET-* register (12 codes — re-cast from research findings Synthesis B under Path B)

The research-findings Synthesis B at `pipeline/research/reflection_packet_grounding/findings_2026-05-10.md` proposes a 12-code register currently named F-REFLECTION-* (authored before the Path B reconciliation landed). Re-cast under Path B (no semantic changes — just prefix swap + ownership relocation):

| # | Code | Layer | Predicate sketch | Cross-family-rigor scope |
|---|------|-------|------------------|--------------------------|
| 1 | `F-PACKET-INSTANCE-LEAK` | PRE-emission | `pattern_observations[i].pattern_summary` / `lessons_proposed[i].pattern_summary` carry instance-level identifiers (client name, specific funder name, specific reason). Three-layer detection (NFKC + NER + regex) per §15.9.2 RT-07 precedent. | Sub-tags `.client_name_present`, `.funder_specific_with_client`, `.reason_attributable_to_specific_outcome`, `.ner_entity_match`, `.unicode_homoglyph`. |
| 2 | `F-PACKET-CROSS-ORG-LEAK` | PRE-emission + PRE-load | `org_slug` does not match source path's org or spans' org_slug; substrate-read path resolves outside declared subtree. Mirrors `F-ARCHIVIST-CROSS-ORG-LEAK` but at packet artifact layer. | Sub-tags `.path_outside_org`, `.symlink_escape`, `.span_org_slug_mismatch`. |
| 3 | `F-PACKET-FABRICATION` | POST-emission + POST-load | Packet asserts quantitative claim (gate count, score, timing, outcome amount) not matching Logfire span tree. Defends against MemoryGraft / Lane 5 F-13 single-seat false success. | Sub-tags `.gate_count_mismatch`, `.score_mismatch`, `.span_id_unresolvable`, `.timing_mismatch`, `.classification_register_version_mismatch`. |
| 4 | `F-PACKET-CLASS-SLOT-LEAK` | PRE-emission | Cloud-routable producer emits packet with semantic slot name (`[SLOT_ANNUAL_REVENUE]`) instead of opaque `[SLOT_<numeric_id>]`. Mirrors `F-CLASS-SLOT-ID-NON-OPAQUE` from v7.0.7. | None (closed enforcement). |
| 5 | `F-PACKET-CLASS-MISLABEL` | PRE-emission | `classification_register_version` does not match operator-signed register at cycle start. Defends against MINJA-shaped in-cycle relabeling. | Sub-tags `.register_signature_invalid`, `.register_version_drift`, `.confidential_field_in_shareable_packet`. |
| 6 | `F-PACKET-EVAL-ONLY-GROUNDED` | PRE-emission | `grounding_signal_classes` ⊆ {`council_split_event`, `judge_score`, `red_team_score`, `editor_verdict`}. Sibling to producer-side `F-REFLECTION-EVAL-ONLY-GROUNDED` but enforced at artifact-validity layer (defense-in-depth). | None. |
| 7 | `F-PACKET-PREMATURE-GENERALIZATION` | PRE-emission | `ProposedLesson` with `frequency = 1` AND `severity != HIGH`. Mirrors lessons.json convention. Operator override per-lesson via SP0-signed exception. | Sub-tag `.frequency_one_no_severity`. |
| 8 | `F-PACKET-SPAN-PROVENANCE-MISSING` | PRE-emission | Quantitative claim field (`gate_pass_counts.*`, `score_signals.*`, `outcome.award_amount_minor_units`) does NOT have an entry in `span_provenance.per_claim_span_ids` OR has an entry with no resolvable span_id. **Cross-references WPFA's `F-WPFA-SPAN-PROVENANCE-MISSING` as sibling pattern.** | Sub-tags `.no_trace_id`, `.trace_id_unresolvable_in_logfire`, `.claim_key_unmapped`, `.span_id_from_different_cycle`. |
| 9 | `F-PACKET-RETRIEVAL-CORRUPTION` | PRE-load (consumer C) | Packet content includes embedding-shaped triggers (high-entropy token bursts, optimized-trigger fingerprints). Defends against AgentPoison / PoisonedRAG via packet path. | Sub-tags `.high_entropy_burst`, `.optimized_trigger_match`, `.embedding_anomaly_detected`. |
| 10 | `F-PACKET-MEMORY-INJECTION` | PRE-emission | Free-text fields (`pattern_summary`, `proposed_rule`) contain prompt-injection-shaped substrings. Three-layer detection (regex + Unicode-normalized regex + small classifier). Mirrors MINJA threat model. | Sub-tags `.injection_pattern_regex`, `.unicode_normalized_match`, `.classifier_score_above_threshold`. |
| 11 | `F-PACKET-SCHEMA-DRIFT` | PRE-load (all consumers) | `schema_version` unknown to consuming code. PRE-load refuses (v1.x) OR surfaces advisory (v0.1, see invariant §3.3.16). Defends against drift between v0.1 emission and v1.x consumption. | Sub-tags `.unknown_schema_version`, `.required_field_missing`, `.deprecated_field_present`. |
| 12 | `F-PACKET-CADENCE-VIOLATION` | PRE-emission | Emission attempted before cycle-close marker is written (i.e., before Uploader has staged). Defends against mid-cycle reflection contaminating producer's own context window. | Sub-tags `.no_cycle_close_marker`, `.uploader_not_staged`, `.partial_council_pass`. |

## §6.3 Additional codes surfaced by this card's scoping pass

Not in the research findings register; surfaced by the artifact-spec discipline this card adds beyond the producer-side discipline the research findings focused on:

| # | Code | Layer | Predicate sketch |
|---|------|-------|------------------|
| 13 | `F-PACKET-SIGNATURE-INVALID` | PRE-load (all consumers) | `producer_signature_ed25519` does not verify against producer-seat pubkey OR `canonical_bytes_hash` does not match canonical-JSON encoding minus signature fields. Mirrors v7.0.4-M1 §2 KFR canonical-signature-invalid byte-for-byte. |
| 14 | `F-PACKET-OPERATOR-SIGNATURE-MISSING` | PRE-load (consumer B + C) | `outcome.status` non-PENDING AND `operator_signature_ed25519` is None. Operator attestation required for outcome-bearing packets. |
| 15 | `F-PACKET-OPERATOR-SIGNATURE-INVALID` | PRE-load | `operator_signature_ed25519` does not verify against operator-pinned pubkey. |
| 16 | `F-PACKET-CYCLE-ID-UNRESOLVABLE` | PRE-emission | `cycle_id` does not resolve to a cycle-close marker span in Logfire export at PRE-write. |
| 17 | `F-PACKET-OUTCOME-EVIDENCE-MISSING` | PRE-emission + PRE-load | `outcome.status` non-PENDING AND `outcome.outcome_evidence_span_ids` is empty. |
| 18 | `F-PACKET-PRODUCER-UNAUTHORIZED` | PRE-emission | `emitted_by_seat` is not a member of the closed producer-registry set (v0.1 = `{"archivist.reflection_submode"}`). |
| 19 | `F-PACKET-COVERAGE-INCOMPLETE` | META (PRE-cycle) | Any F-PACKET-* primitive unrealized at runtime; analog of `F-CLASS-COVERAGE-INCOMPLETE` from v7.0.7 + `F-REFLECTION-COVERAGE-INCOMPLETE` from v7.0.9. PRE-cycle gate prevents v0.2/v1.x consumer deployment shipping without realized predicates. |

Total initial F-PACKET-* family: **19 codes** (12 re-cast from research + 7 new from artifact-spec discipline). Open to growth at Cycle-1 / Cycle-2 fold-in per L-005 row-170 precedent (anticipate +3-5 codes from Red Team review).

## §6.4 Realization timing

v0.1 Beta hook: **dormant**. Predicate signatures registered; bodies raise `NotImplementedError`. Matches v0.1 Beta hook treatment of §15 Reflection sub-mode F-REFLECTION-* family + the v7.0.7 F-CLASS-* family. F-PACKET-COVERAGE-INCOMPLETE (#19) is the META gate that prevents v0.2/v1.x consumer deployment shipping with un-realized predicates.

v0.2: live emission-side predicates fire at producer output_validator hook. Consumer-side PRE-load predicates live for Consumer A (operator review). Consumer-B (KFR cross-check) consumer-side PRE-load predicates also live (F-LOGICIAN-FACT-DRIFT is LOCKed and consumes packets).

v1.x: Consumer-C (scheduled-cadence Archivist) consumer-side PRE-load predicates live. F-PACKET-COVERAGE-INCOMPLETE flips from META-stub to live PRE-cycle gate.

## §6.5 Realization owner

Cedar/Python realization lives at **§4 v2.x.y companion amendment** (paired-commit with §16 v1 + §0.5 v?? at compound-LOCK time). One module per code per §4 v2.x precedent (no triplet-collapse; F-PACKET-* family has 19 codes, none of which fit the "validation triplet" collapse pattern).

# §7. Open questions for next operator review pass

Five operator-decisions block promoting this SCOPING_DRAFT to a DISPATCH_SPEC_DRAFT. Each carries a recommended default; defaults are Thesis-overrideable but not Thesis-blocking — except where flagged.

**OQ-1. Section number.** Confirm §16 for Reflection Packet (per WPFA spec card §2 reservation), or pick a different number. *Default: §16.* Non-blocking — if changed, §0.5 row allocation and the §4 v2.x.y amendment path rename.

**OQ-2. Ship window.** Three options:
- (a) **v0.1 Beta dormant hook only** — schema + signing primitives + 19 F-PACKET-* predicate signatures at architectural-primitive layer; matches the Reflection sub-mode v0.1 hook pattern. ~2-3 sessions to LOCK.
- (b) **v0.2 first wave with live emission** — Consumer A (operator review) + Consumer B (KFR cross-check) live; producer emits on operator-invoked cadence; mirrors the §13/§14 v0.2 SPEC-only template but with live emission at v0.2 (KFR consumer is already LOCKed via F-LOGICIAN-FACT-DRIFT). ~5-7 sessions to LOCK.
- (c) **v0.2 second wave** — co-locks with §15 v2.x Archivist Reflection sub-mode v0.2 SPEC; lands after §15 v2.x. ~3-5 sessions to LOCK on top of §15 v2.x timing.

*Recommended default: (a) v0.1 Beta dormant hook only.* Rationale: matches the Reflection sub-mode v0.1 hook posture (LOCKed today); minimizes Beta close-out competition; WPFA's `F-PACKET-SPAN-PROVENANCE-MISSING` cross-reference resolves at v0.1 hook; live consumers wait until v0.2 when §15 v2.x SPEC unblocks. **Operator-decision-blocking** for downstream timing of WPFA Cycle 1 absorption.

**OQ-3. Outcome backfill mechanism.** Two options:
- (a) **Emit once at outcome** — packet emission deferred until decision-observed event; pre-outcome cycle close produces no packet.
- (b) **Emit at submission with PENDING + backfill at outcome** — packet emits at every cycle close with `outcome.status = PENDING`; a second emission lands at decision-observed event with the operator-signed AWARDED/DECLINED/NO_DECISION status. Two packets per cycle, linked by shared `cycle_id`.

*Recommended default: (b) emit at submission + backfill at outcome.* Rationale: pre-outcome packet is useful to Consumer A (operator review for in-cycle accountability) and Consumer B (KFR cross-check on PENDING-marked packets surfaces stuck submissions). Operator-decision-blocking only if (a) is preferred — affects Consumer A's review cadence.

**OQ-4. Operator commentary handling.** The §15 Reflection sub-mode synthesis flags that operator-authored notes at cycle close are classification-routed and MINJA-threat-bearing. Two options for packet schema:
- (a) **No operator-notes field on the packet** — operator commentary lives entirely in the §15 sub-mode's separate substrate; packet stays deterministic-fields-only. Cleaner threat model.
- (b) **Optional `operator_notes_local_only: str | None` field** — classified `confidential`, routes through slot-fill, never reaches cloud-routed Archivist. F-PACKET-MEMORY-INJECTION applies.

*Recommended default: (a) no operator-notes field on the packet.* Rationale: packet stays the deterministic spine; operator commentary stays in the §15 sub-mode's adjacent substrate; threat surface contained. Non-blocking — if (b) is preferred, F-PACKET-MEMORY-INJECTION sub-tags expand.

**OQ-5. Schema versioning + retention.** Two sub-questions:
- 5a. Schema version evolution: tolerant-reader pattern at consumer (semver + advisory `F-PACKET-SCHEMA-DRIFT` at v0.1; fail-closed at v1.x) — *or* strict-reader pattern (fail-closed at v0.1)?
- 5b. Retention: packets live indefinitely under `orgs/<slug>/vault/operational/reflection_packets/` — *or* age out after N quarters (recommend N=8, mirrors KFR retention pattern)?

*Recommended defaults: 5a tolerant-reader (v0.1 advisory, v1.x fail-closed); 5b indefinite retention (Tilth-internal substrate; storage cost is negligible; pruning is operator-driven).* Non-blocking; both Thesis-overrideable.

**OQ-6 (optional — minor; can resolve at Thesis Cycle 1).** Should `outcome.award_amount_minor_units` (int, A12 Decimal mandate) extend to `_micro` precision the way WPFA energy quantities do — i.e., should award amounts be stored at sub-cent precision to handle multi-currency/forex cases? *Recommended default: no — `_minor_units` cents-precision is sufficient for grant award amounts (no sub-cent grants in practice).* Non-blocking.

# §8. Recommended next steps after operator review

If operator confirms defaults (OQ-1 §16 + OQ-2 (a) v0.1 dormant + OQ-3 (b) emit+backfill + OQ-4 (a) no operator-notes + OQ-5 tolerant-reader/indefinite + OQ-6 cents-precision), this scoping draft promotes to a DISPATCH_SPEC_DRAFT in one author session:

1. **Spec card consolidation** — convert this SCOPING_DRAFT to DISPATCH_SPEC_DRAFT at `pipeline/planning/reflection_packet_spec_2026-05-1?.md` mirroring the WPFA spec card template (§0 motivation, §1 compound-LOCK pairing, §2 §16 numbering rationale, §3 full schema with finalized invariants, §4 F-PACKET-* family with PRE/POST/META layering finalized, §5 §0.5 row allocation, §6 sub-kind registry update for §2 v7.x, §7 OQ disposition log, §8 dispatch readiness checklist).

2. **Pre-Thesis reconciliation update** — add a one-line entry to `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md` confirming Path B adopted + this spec card's authoring path.

3. **WPFA Cycle 1 absorption** — the WPFA handoff packet at `pipeline/handoffs/ws_wpfa_handoff_2026-05-10.md` already cites the Path B documentary edit; when this card lands as DISPATCH_SPEC_DRAFT, WPFA Cycle 1 has a live definition to cite.

4. **Thesis dispatch fires as separate session** — Editor (Llama/Groq) + Judge (Gemini/Google) + Red Team (GPT-OSS/Groq) per L-005 strict two-cycle + bridge pattern. Anticipate ~3-4 sessions total: 1 spec card consolidation + 1 Thesis Cycle 1 + 1 Thesis Cycle 2 + 1 compound-LOCK ceremony.

5. **Compound LOCK target** — §16 v1 + §4 v2.x.y F-PACKET-* family + §0.5 v?? amendment + (conditionally per OQ-2) §2 v7.x sub-kind registry update. Anticipated rows ≥ 205 (after Reflection v0.1 hook at row 202/203/204 + Funding Goal compound-LOCK candidate + WPFA compound-LOCK candidate).

# §9. Sibling-not-nested verification (operator-overridable; default OK)

This card's §16 ReflectionPacket and the WPFA spec card's §17 CycleReceipt are **sibling artifacts**. Verified at the schema layer:

| Axis | §16 ReflectionPacket | §17 WPFA CycleReceipt |
|------|----------------------|------------------------|
| Trigger | Cycle close | Cycle close |
| Input substrate | Logfire span tree + KFR + Match DB + Admin-risk ledger | Logfire span tree + Coefficient Registry |
| Producer | `archivist.reflection_submode` (one) | Cycle Accountant (deterministic module, no LLM) |
| Primary consumer | Archivist learning loop (Consumer A: operator review; Consumer B: KFR cross-check; Consumer C: v1.x scheduled) | Operator dashboard + buyer-facing PDF |
| Audience | Tilth-internal + operator | Operator + external buyer |
| Schema | ReflectionPacket (pattern_observations + lessons_proposed + gate_pass_counts + outcome) | CycleReceipt (actual + counterfactual + delta) |
| Signing | producer Ed25519 + operator Ed25519 (optional pre-outcome) | operator Ed25519 (optional pre-buyer-export) |
| Gate family | F-PACKET-* (19 codes) | F-WPFA-* (12 codes) |
| Cross-reference | F-PACKET-SPAN-PROVENANCE-MISSING ↔ F-WPFA-SPAN-PROVENANCE-MISSING (sibling pattern) | (mirror) |

Zero shared output. Zero shared consumer. Zero shared schema field. F-CIC-CLC-COUPLING-VIOLATION-class regression test at every Thesis cycle ensures no F-PACKET-* code crosses to §17 and no F-WPFA-* code crosses to §16.

# §10. Done definition (this scoping draft)

- [x] Conceptual disambiguation: ReflectionPacket (artifact) vs Reflection sub-mode (agent) made explicit in §0.
- [x] Artifact schema sketched (§3) with fields, types, signing regime (Ed25519 per v7.0.4-M1 KFR pattern), semver, retention.
- [x] Producer contract: sole producer, cadence (dormant v0.1 → operator-invoked v0.2 → scheduled v1.x), input evidence closed set (§4).
- [x] Three consumer contracts named (§5): operator review (A) + KFR cross-check via F-LOGICIAN-FACT-DRIFT (B) + v1.x runtime reflection-cadence-driven (C).
- [x] F-PACKET-* gate family sketched (§6): 19 codes (12 re-cast from research findings under Path B + 7 new from artifact-spec discipline); orthogonal to F-REFLECTION-* (producer) and F-ARCHIVIST-* (substrate).
- [x] Naming discipline per Path B (§0 + §6.1 + §9): F-PACKET-* family, never F-REFLECTION-PACKET-*.
- [x] OQ batch surfaced for next operator review pass (§7): 6 OQs (1 blocking + 4 default-overridable + 1 minor).
- [x] No Thesis dispatch. No LOCK ceremony. No row reservation against §0.5. No Cedar/Python written.
- [x] Filed at `pipeline/planning/reflection_packet_scoping_draft_2026-05-10.md`.

# §11. Hand-back

This scoping draft is filed. Operator review pass + Thesis dispatch fire as separate sessions after operator answers OQs in §7. The blocking OQ is **OQ-2 ship window** (v0.1 Beta dormant hook / v0.2 first wave / v0.2 second wave). The other five OQs have defaults that can absorb at Thesis without operator pre-decision.

Coordinator: surface OQ batch (§7) to operator. When OQ-2 lands (or operator confirms default), promote this SCOPING_DRAFT to DISPATCH_SPEC_DRAFT per §8 step 1. Estimated authoring cost: 1 session (~45 min) for spec card consolidation; 3 sessions for Thesis cycles + compound LOCK.

## Sources

- pipeline/planning/operator_spec_card_status_2026-05-10.md (orchestrator discovery report — Q2 default = "yes, separate spec card" confirmed by operator)
- pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md (Path B = F-PACKET-* separate family adopted here)
- pipeline/research/reflection/synthesis_design_memo_2026-05-10.md (Reflection sub-mode design — agent, not artifact; producer of this card's artifact)
- pipeline/research/reflection_packet_grounding/findings_2026-05-10.md (5-lane research; Synthesis B 12-code register re-cast under Path B in §6.2)
- pipeline/handoffs/ws_wpfa_handoff_2026-05-10.md (sibling spec card pattern; WPFA defines its packet artifact format byte-for-byte mirroring this card)
- pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md (Reflection sub-mode v0.1 hook — producer LOCKed today rows 202/203/204)
- pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md (KFR canonical-JSON Ed25519 signing pattern this card mirrors)
- pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md (classification-driven routing + opaque slot discipline applies to cloud-routed packet reads)
- pipeline/blueprint/v0.1/section_02_v7_2_amendment.md (sub-kind registry pattern — Reflection Packet candidate sub-kind under operational/reflection_packets/)
- pipeline/blueprint/v0.1/section_04_v2_x_amendment.md (failure-code family registration pattern)
- pipeline/blueprint/v0.1/section_15_archivist.md (§15 v1 LOCK — proposes-only Archivist seat owning the Reflection sub-mode that produces this artifact)

---

**Filed:** 2026-05-10. SCOPING_DRAFT — pre-Thesis, no LOCK ceremony, no row reservation. Operator review pass + Thesis dispatch fire as separate sessions.
