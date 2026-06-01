---
title: §15 v2.x — Archivist Reflection sub-mode SPEC (v0.2 first wave)
filed: 2026-05-15
operator: Josh Inklovich
status: LOCKED 2026-05-15 — compound paired-commit (sibling 4/5) with §16 v1.1 + §2 v7.x + §4 v2.x.y.1 + §0.5 v24 at same `lock_timestamp_utc`. L-005 strict two-cycle Thesis CLOSED with FULL LIVE CROSS-FAMILY rigor. v0.2 first wave SPEC for the Archivist Reflection sub-mode; producer behavior at v0.2; runtime per §15 v1 v1.x precedent.
parent_locks:
  - pipeline/blueprint/v0.1/section_15_archivist.md                                       # §15 v1 SPEC LOCKED 2026-05-10 rows 191/192 (parent; Reflection sub-mode extends here)
  - pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md                            # v7.0.9 row 202 — Reflection sub-mode v0.1 hook PRODUCER scaffold; realized here
  - pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md                           # v7.0.10 row 215 — three-posture routing; reflection always-local preserved
  - pipeline/blueprint/v0.1/section_04_logician_v2_x_2_amendment.md                        # §4 v2.x.2 row 203 — F-REFLECTION-* family (producer behavior); HORIZON rows activate at v0.2 per this amendment
  - pipeline/blueprint/v0.1/section_16_reflection_packet.md                                # §16 v1 LOCKED rows 216-218 — Reflection Packet artifact (this sub-mode's sole output)
  - pipeline/blueprint/v0.1/section_16_v1_1_amendment.md                                   # §16 v1.1 producer-flip head amendment (sibling 1/5)
companion_amendments:
  - pipeline/blueprint/v0.1/section_16_v1_1_amendment.md                                   # sibling 1/5
  - pipeline/blueprint/v0.1/section_02_v7_x_reflection_packet_subkind_amendment.md         # sibling 2/5
  - pipeline/blueprint/v0.1/section_04_v2_x_y_1_packet_bodies_amendment.md                 # sibling 3/5
  - pipeline/blueprint/v0.1/section_00_5_section_16_v1_1_amendment.md                      # sibling 5/5
compound_lock_with: section_16_v1_1_amendment.md + section_02_v7_x_reflection_packet_subkind_amendment.md + section_04_v2_x_y_1_packet_bodies_amendment.md + section_00_5_section_16_v1_1_amendment.md
amendment_class: archivist-sub-mode-SPEC (producer-side; LIVE producer at v0.2 first wave; runtime per §15 v1 v1.x amendment precedent — Archivist substrate proposes-only)
target_lock_row: 224
ws_dispatch: WS-Reflection Packet v0.2 first wave compound LOCK
review_discipline: L-005 strict two-cycle; FULL live cross-family
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out)
session_metrics: pipeline/metrics/session_log.jsonl
---

# §15 v2.x — Archivist Reflection sub-mode SPEC (v0.2 first wave)

## §15.v2.x.0 Amendment intent

§15 v1 (LOCKED 2026-05-10) established the Archivist seat with proposes-only discipline (no canonical mutation; AST-lint + Cedar + runtime guard three-layer defense) and registered the F-ARCHIVIST-* gate family (5 codes + sub-tag extensions per §4 v2.x.1). The Reflection sub-mode was named at §15 v1 §15.4.2 (weekly cadence) but the producer agent + tools + emission discipline were deferred to a future v2.x amendment.

This amendment is that future v2.x amendment. It specifies the Archivist Reflection sub-mode at v0.2 first wave: the Pydantic AI `reflection_agent` (v7.0.9 §9.1 dormant scaffold realized), three tools, emission cadence, classification routing, and v0.2-first-wave scope boundary. Producer behavior is LIVE at v0.2 first wave; substrate write discipline inherits §15 v1 proposes-only (Reflection Packet writes are artifact-emission writes, not canonical mutations — the proposes-only contract holds).

Companion to §16 v1.1 (this sub-mode's sole emission is the Reflection Packet artifact specified at §16). Without §15 v2.x the artifact has no producer; without §16 v1.1 the producer has no schema. The two amendments LOCK atomically per §6.17 Option-B compound-commit.

## §15.v2.x.1 `reflection_agent` Pydantic AI construction

Producer module: `pipeline/orchestrator/seats/archivist/reflection_mode.py`. Replaces the v0.1 hook scaffold (NotImplementedError on `emit_packet_v0_1_dormant()`) with a live Pydantic AI agent.

```python
from pydantic_ai import Agent
from pipeline.orchestrator.seats.archivist._tools import (
    read_priors,
    record_reflection,
    score_against_priors,
)

reflection_agent: Agent = Agent(
    model="local:llama-3.3-70b-instruct",  # always-local per v7.0.9 §9 + v7.0.10 §1
    system_prompt=REFLECTION_SUBMODE_SYSTEM_PROMPT,  # §15.v2.x.3 below
    tools=[read_priors, record_reflection, score_against_priors],
    deps_type=ReflectionDeps,  # Logfire span tree handle + KFR + admin-risk ledger + classification register
    result_type=ReflectionPacket,
)
```

**Model binding.** Always-local per v7.0.9 §9 + v7.0.10 §1. The producer's input substrate is the cycle's Logfire span tree + KFR per-org + lessons memory + admin-risk ledger; under v7.0.10's three-posture model, none of these fields ever route cloud. The model binding `local:llama-3.3-70b-instruct` resolves at runtime via Ollama / vLLM (per ADR-001 substrate); router-config maps to the deployment's pinned local model — 70B-class is the v0.2 floor; 200B-class heavy-Reflection swap is operator-flagged per-grant SP0 optional and defers to v1.x demand-realization.

**ReflectionDeps shape.**

```python
@dataclass(frozen=True, kw_only=True)
class ReflectionDeps:
    cycle_id: str
    org_slug: str
    logfire_span_tree_handle: SpanTreeHandle
    kfr_handle: KfrHandle
    admin_risk_ledger_handle: AdminRiskLedgerHandle
    classification_register_handle: ClassificationRegisterHandle
    operator_sp0_grant: ReflectionPriorsGrant | None  # whether prior-read is granted for this cycle
    cycle_close_marker_span_id: str
```

## §15.v2.x.2 Emission cadence — Packet 1 PENDING + Packet 2 BACKFILL

Per §16 v1 §16.3 emit + backfill discipline:

- **Cycle-close marker fires** `reflection_agent.emit_packet_pending(deps)`. Synchronous; agent runs over the cycle's accumulated span tree + KFR + admin-risk + lessons memory; emits one `ReflectionPacket` with `outcome.status="PENDING"` + `operator_signature_ed25519=None` + `outcome.decision_observed_at=None` + `outcome.outcome_evidence_span_ids=()`. Validated by `__post_init__` invariants + F-PACKET-* PRE-emission predicates (now LIVE per §4 v2.x.y.1).
- **Decision-observed event fires** `reflection_agent.emit_packet_backfill(deps, outcome, operator_signature_ed25519)`. Synchronous; agent re-runs over the cycle's now-final span tree + KFR funder-outcome ledger entry; emits a SECOND `ReflectionPacket` with `outcome.status ∈ {"AWARDED", "DECLINED", "NO_DECISION"}` + `operator_signature_ed25519` non-None + `outcome.decision_observed_at` non-None + `outcome.outcome_evidence_span_ids` non-empty. Operator Ed25519 signature gates emission per F-PACKET-OPERATOR-SIGNATURE-MISSING.

Both invocations write under the `archivist.reflection_submode` `emitted_by_seat` registry binding per §16 v1 §16.2.1 invariant 7. Same `cycle_id` shared between Packet 1 and Packet 2; different `packet_id`. Consumer A operator-review CLI surfaces both.

**Mid-cycle reflection guard.** Producer module raises `CadenceViolationError` at the call site if `emit_packet_pending()` is invoked before the cycle-close marker span is observable in the Logfire span tree. F-PACKET-CADENCE-VIOLATION composes at PRE-emission. Defense against "mid-cycle reflection contaminating producer's own context window" — the agent runs strictly post-cycle-close.

## §15.v2.x.3 System prompt — REFLECTION_SUBMODE_SYSTEM_PROMPT

The system prompt is operator-tuned via DSPy + GEPA at offline Card refinement time (per ADR-001 substrate; not at runtime). v0.2 first wave ships with a tuned baseline; the prompt scope:

1. **Identify what worked + what didn't** in the cycle. Surface gate-pass / gate-fail patterns, score signals, Editor verdict trend, council-split status, cross-family satisfaction.
2. **Propose pattern-level observations**, not instance-level. The schema-layer + F-PACKET-INSTANCE-LEAK reject instance-level text; the prompt frames the task in pattern-level vocabulary up front.
3. **Propose lessons** only when `frequency >= 2` OR `severity == "HIGH"`. F-PACKET-PREMATURE-GENERALIZATION enforces; the prompt frames the threshold.
4. **Cite span_ids** for every quantitative claim. F-PACKET-SPAN-PROVENANCE-MISSING enforces; the prompt requires the agent to surface span_id citations as it composes the packet.
5. **Refuse to fabricate** funder outcomes. Outcome status comes from KFR or operator-direct event, never from the agent's reasoning.

The prompt does NOT include any client-name lists, funder-name lists, or instance-level details — the prompt is org-agnostic. Org-specific signal enters via `ReflectionDeps`.

## §15.v2.x.4 Three tools (per §16 v1.1 §16.v1.1.1)

### §15.v2.x.4.1 `read_priors(packet_ids: Iterable[str], deps: ReflectionDeps) -> Iterable[ReflectionPacket]`

Reads prior Reflection Packets within Law-3 org boundary. Tool internals:

1. Operator SP0 grant check: `deps.operator_sp0_grant` MUST be active for the cycle_id; if None or expired, tool raises `ReflectionPriorReadDenied` (no operator-granted prior-read permission).
2. Per-packet_id path resolution: `orgs/<deps.org_slug>/vault/operational/reflection_packets/<packet_id>.json`; cross-org paths blocked by F-PACKET-CROSS-ORG-LEAK PRE-read (now LIVE).
3. PRE-load gates: F-PACKET-SIGNATURE-INVALID (LIVE) + F-PACKET-OPERATOR-SIGNATURE-MISSING (for outcome-bearing BACKFILLs) + F-PACKET-SCHEMA-DRIFT (advisory at v0.2; fail-closed at v1.x). Failure → tool raises typed error.
4. Returns: tuple of validated `ReflectionPacket` objects.

Defense against MINJA / AgentPoison / PoisonedRAG at this tool: F-PACKET-RETRIEVAL-CORRUPTION + F-PACKET-MEMORY-INJECTION PRE-load (both LIVE at v0.2; consumer wiring deferred to v1.x for the scheduled-cadence Archivist; Reflection sub-mode prior-read inherits the same protections).

### §15.v2.x.4.2 `record_reflection(packet: ReflectionPacket, deps: ReflectionDeps) -> None`

Submits the packet for vault write via the SUB_KIND_REGISTRY dispatch (registered per §2 v7.x sibling). Tool internals:

1. `packet.org_slug == deps.org_slug` cross-check; mismatch raises.
2. PRE-write gates: full F-PACKET-* PRE-emission set (1, 2, 4, 5, 6, 7, 8, 10, 12, 16, 17, 18) — all LIVE.
3. Atomic write via `vault_write.write_record(..., intent="operational-reflection-packet-write")`; underlying `os.open(O_CREAT | O_EXCL | O_WRONLY)` for collision-detect (F-PACKET-CADENCE-VIOLATION sub-tag `.packet_id_collision`).
4. POST-write: F-PACKET-FABRICATION POST-emission replay over the cycle's Logfire span tree.

### §15.v2.x.4.3 `score_against_priors(observation: PatternObservation, prior_packets: Iterable[ReflectionPacket], deps: ReflectionDeps) -> float`

Deterministic similarity score in `[0.0, 1.0]` over `observation.pattern_summary` against the union of `prior_packets[i].pattern_observations[j].pattern_summary`. v0.2 first wave uses BM25-shaped token-overlap; no LLM eval. Result feeds `observation.frequency` increment heuristic (operator-tunable threshold; default 0.7 → frequency += 1).

v1.x may extend to local-embedding cosine similarity (bge-large-en-v1.5 per §11 substrate); v0.2 ships with the cheap deterministic baseline.

## §15.v2.x.5 Substrate-write discipline — inherits §15 v1 proposes-only

Reflection Packet writes are **artifact emissions**, not canonical-vault mutations. The §15 v1 proposes-only discipline applies at the **substrate-write predicate level**: F-ARCHIVIST-AUTO-APPLY-ATTEMPTED + F-ARCHIVIST-CROSS-ORG-LEAK + F-ARCHIVIST-LESSON-INSTANCE-LEAK + F-ARCHIVIST-CADENCE-DRIFT + F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT.

For Reflection Packets specifically:

- **F-ARCHIVIST-AUTO-APPLY-ATTEMPTED** — N/A; Reflection Packets are emitted, not applied. Lessons proposed within packets are READ by operator at v0.2 (Consumer A) and applied to canonical surfaces (lessons.md, L-NNN) at v1.x scheduled-cadence Archivist only via operator-decision-driven update flow.
- **F-ARCHIVIST-CROSS-ORG-LEAK** — composes with F-PACKET-CROSS-ORG-LEAK at the substrate-write level. Defense-in-depth.
- **F-ARCHIVIST-LESSON-INSTANCE-LEAK** — composes with F-PACKET-INSTANCE-LEAK at the pattern_summary + proposed_rule field level. Defense-in-depth.
- **F-ARCHIVIST-CADENCE-DRIFT** — Reflection Packet cadence is per-cycle (not weekly/quarterly per §15 v1 §15.4.2 schedule cadence); the cadence-drift predicate does NOT compose at the per-cycle level. Reflection sub-mode cadence governance is at F-PACKET-CADENCE-VIOLATION (per-cycle) + F-REFLECTION-CADENCE-DRIFT (sub-mode-level; §4 v2.x.2 row 203).
- **F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT** — composes when `read_priors` tool reads a packet; intent string `"operational-reflection-packet-read"` (mirror of write intent) carries through Cedar.

## §15.v2.x.6 v0.2 vs v1.x scope boundary

**v0.2 first wave (this amendment):**

- Producer Pydantic AI `reflection_agent` LIVE per cycle-close marker + decision-observed event.
- Three tools LIVE.
- F-REFLECTION-* family fully ACTIVE (16 of 17 codes; F-REFLECTION-HEAVY-SWAP-INVALID remains PROBE-DEPENDENT per §4 v2.x.2 row 203).
- F-PACKET-* artifact-validity family fully ACTIVE (per §4 v2.x.y.1 sibling).
- Consumer A operator-review CLI live (Tilth-archivist packets list / show).
- Always-local routing per v7.0.9 + v7.0.10.

**v1.x runtime amendment scope:**

- Consumer B (KFR cross-check at quarterly cadence) runtime wiring.
- Consumer C (scheduled-cadence Archivist v2.x sub-mode reading accumulated packets across cycles) runtime wiring.
- Cedar full enforcement (18 of 19 BINDING rules flip from placeholder to enforcing).
- Tolerant-reader flip — F-PACKET-SCHEMA-DRIFT ADVISORY → fail-closed at major-version drift.
- Heavy-Reflection swap analog (optional, operator-demand-driven).
- F-PACKET-INSTANCE-LEAK Layer 2 NER upgrade (regex+blocklist → spaCy or local NER model; SP0 opt-in).
- F-PACKET-MEMORY-INJECTION Layer 3 small classifier default-enable.

## §15.v2.x.7 Cycle 1 + Cycle 2 disposition log (row-170 transparent-disposition)

Disposition log lands at `pipeline/validation/reflection_packet_v0_2_first_wave_thesis_2026-05-15/`. Inherited from the compound sibling Thesis cycles.

## §15.v2.x.8 Test surface (v0.2 first wave scope)

`tests/seats/archivist/test_reflection_v0_2_*.py` — new test directory:

- `test_reflection_v0_2_agent_construction.py` — Pydantic AI agent construction; always-local model binding; tool registration.
- `test_reflection_v0_2_emit_pending.py` — emit_packet_pending happy path; CadenceViolationError on pre-marker call.
- `test_reflection_v0_2_emit_backfill.py` — emit_packet_backfill happy path; F-PACKET-OPERATOR-SIGNATURE-MISSING on missing operator sig; outcome-status cross-check.
- `test_reflection_v0_2_tools.py` — read_priors / record_reflection / score_against_priors happy paths + error cases.
- `test_reflection_v0_2_cross_org_isolation.py` — Law 3 regression; tools refuse cross-org paths.
- `test_reflection_v0_2_classification_routing.py` — verifies always-local routing per v7.0.10 §1 (no cloud egress in normal-path emission).

## §15.v2.x.9 Done definition

- [x] Pydantic AI `reflection_agent` LIVE per cycle-close + decision-observed.
- [x] Three tools LIVE.
- [x] Emission cadence (Packet 1 PENDING + Packet 2 BACKFILL) per §16 v1 §16.3.
- [x] Mid-cycle reflection guard via F-PACKET-CADENCE-VIOLATION composition.
- [x] Always-local routing per v7.0.9 + v7.0.10.
- [x] Substrate-write discipline inherits §15 v1 proposes-only (defense-in-depth).
- [x] v0.2 vs v1.x boundary documented.
- [x] Test surface at `tests/seats/archivist/test_reflection_v0_2_*.py`.

## §15.v2.x.10 Audit trail

See `pipeline/validation/reflection_packet_v0_2_first_wave_thesis_2026-05-15/`.

---

**Filed:** 2026-05-15. LOCKED via L-005 strict two-cycle Thesis with FULL LIVE CROSS-FAMILY rigor. Compound paired-commit sibling 4/5.
