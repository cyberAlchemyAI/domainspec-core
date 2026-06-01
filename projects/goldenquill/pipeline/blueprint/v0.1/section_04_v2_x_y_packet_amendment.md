---
title: Blueprint §4 Logician — Amendment v2.x.y (F-PACKET-* failure-code family — 19 codes; 18 NotImplementedError + 1 LIVE META; v0.1 Beta hook dormant artifact gate primitives)
filed: 2026-05-15
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-15 — paired-commit sub-amendment with §16 v1 + §0.5 v22 (compound paired-commit triple per §6.17 Option-B; all three LOCKED atomically at this ceremony). Predicate signatures at predicate-signature layer per L-006 dormant-binding pattern (architecture v7.0.7 §5.1 precedent). 18 of 19 F-PACKET-* predicates land with NotImplementedError bodies; 1 (F-PACKET-COVERAGE-INCOMPLETE) carries LIVE META-gate body as the dormant-binding lever. L-005 strict two-cycle Thesis CLOSED with FULL LIVE CROSS-FAMILY rigor (Editor=groq/llama-3.3-70b-versatile + Judge=google/gemini-2.5-pro + Red Team=groq/openai/gpt-oss-120b via openclaw gateway bridge). Thirteenth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor.
parent_lock: pipeline/blueprint/v0.1/section_04_v2_x_amendment.md  # §4 v2.x LOCKED rows 193/194 (F-CLASS-COVERAGE-INCOMPLETE META-gate ACTIVATED; canonical realization pattern this amendment mirrors)
parent_lock_row: 194
predecessor_amendments_chain:
  - §4 v2.x LOCKED 2026-05-10 rows 193/194 — ~44 failure codes across 4 slices; L-006 dormant-binding ACTIVATED via F-CLASS-COVERAGE-INCOMPLETE META gate
  - §4 v2.x.1 LOCKED 2026-05-10 rows 198/199 — narrow-corrective Tilth-RT-07 closure; sub-tag-extension pattern for R-ARCHIVIST-NO-CANONICAL-MUTATE
  - §4 v2.x.2 LOCKED 2026-05-10 row 203 — F-REFLECTION-* family (PRODUCER-side; 17 codes; 8 BINDING + 8 HORIZON + 1 PROBE-DEPENDENT); sibling at architectural-primitive layer to THIS amendment
  - §4 v2.x.z LOCKED 2026-05-11 row 207 — F-WPFA-* family (12 codes / 10 modules); LIVE predicate bodies; sibling at artifact-validity layer to THIS amendment
  - §4 v2.x.4 LOCKED 2026-05-11 row 213 — F-FG-* family (8 codes / 5 modules); SPEC-ONLY at v0.2 with STUB bodies
companion_lock_paired_commit:
  - pipeline/blueprint/v0.1/section_16_reflection_packet.md                          # §16 v1 (compound-LOCK sibling 1/3)
  - pipeline/blueprint/v0.1/section_00_5_section_16_packet_amendment.md              # §0.5 v22 (compound-LOCK sibling 3/3)
amendment_class: forward-binding predicate-signature-layer (18 NotImplementedError + 1 LIVE META)
precedent_pattern: §4 v2.x.2 F-REFLECTION-* BINDING pattern (NotImplementedError + 1 LIVE META) byte-for-byte; F-PACKET-COVERAGE-INCOMPLETE LIVE body mirrors F-REFLECTION-COVERAGE-INCOMPLETE at row 404 of §0.5 v18 byte-for-byte
threat_severity_at_v0_1_v0_2: LOW — predicate signatures only; no runtime invocation; 18 BINDING bodies raise NotImplementedError; META-gate LIVE body inspects the gate-realization-registry. Activation gated by F-PACKET-COVERAGE-INCOMPLETE PRE-cycle META-gate at v0.2 first wave.
purpose: Realize the 19 F-PACKET-* gate signatures at the §4 Logician predicate-signature layer. NotImplementedError bodies for 18; LIVE body for 1 (F-PACKET-COVERAGE-INCOMPLETE META-gate dormant-binding lever).
companion_code_landed:
  - "pipeline/vault/sub_kinds/reflection_packets.py (NEW SCAFFOLD — ReflectionPacket + 6 sub-shapes + canonical-codec helpers + 21 __post_init__ invariants; NO SUB_KIND_REGISTRY entry per OQ-2 (a))"
  - "pipeline/logician/gates/f_packet_*.py (NEW — 19 module files; 18 NotImplementedError; 1 LIVE for f_packet_coverage_incomplete.py)"
  - "pipeline/vault/policies/reflection_packet.cedar (NEW — 19 Cedar rules; 18 fail-closed-pending-implementation; 1 LIVE)"
  - "pipeline/orchestrator/seats/archivist/reflection_packet_producer.py (NEW SCAFFOLD — emit_packet_v0_1_dormant stub raising NotImplementedError per architecture v7.0.9 §9.1 dormant discipline)"
companion_tests_landed:
  - "tests/vault/sub_kinds/test_reflection_packets.py (NEW — dataclass mechanics + canonical-codec round-trip + 21 __post_init__ invariant skeletons under pytest.mark.skip for v0.1 hook)"
  - "tests/logician/gates/test_f_packet_*.py (NEW — 19 test files; LIVE module = real assertions; NotImplementedError modules = signature-only regressions)"
  - "tests/logician/gates/test_f_packet_coverage_incomplete_meta_gate.py (NEW — META-gate LIVE body FAIL_CLOSED regression)"
ws_dispatch: WS-Reflection Packet v0.1 Beta hook
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment v2.x.y — F-PACKET-* gate-family realization at predicate-signature layer

## §1. Amendment intent + scope

This amendment realizes at the §4 Logician predicate-signature layer the F-PACKET-* gate family registered at §16 v1 §16.8. It is a paired-commit sub-amendment with §16 v1 (parent section) + §0.5 v22 (interface-index row append). All three LOCK atomically per §6.17 Option-B compound-paired-commit discipline.

**Path B naming discipline.** F-PACKET-* is the artifact gate family (this amendment). F-REFLECTION-* (§4 v2.x.2 row 203) is the producer gate family. F-ARCHIVIST-* (§15 v1 row 192) is the substrate-write gate family. F-WPFA-* (§4 v2.x.z row 207) is the sibling artifact gate family. F-PACKET-* MUST NOT collide with any other family. F-CIC-CLC-COUPLING-VIOLATION-class regression test at LOCK ceremony enforces (see §6 below).

**v0.1 hook body state per OQ-2 (a).**

- **18 BINDING predicates** raise NotImplementedError. Predicate signatures present; predicate registries populated; module skeletons authored under `pipeline/logician/gates/f_packet_*.py`; tests scaffolded under `pytest.mark.skip` annotations with marker `v0.1 hook dormant; body lands at v0.2 first wave compound LOCK`.
- **1 LIVE predicate** — `F-PACKET-COVERAGE-INCOMPLETE` (#19). META-gate body inspects the gate-realization-registry. FAIL_CLOSED iff any of the 18 NotImplementedError-bodied predicates lacks realized body at runtime. Mirrors `F-REFLECTION-COVERAGE-INCOMPLETE` row 404 + `F-CLASS-COVERAGE-INCOMPLETE` v7.0.7 §5.1 byte-for-byte.

## §2. F-PACKET-* register (19 codes — predicate signatures with v0.1 body state)

The 18 BINDING predicates land in `pipeline/logician/gates/f_packet_<code_lowercase>.py` with NotImplementedError bodies, named drift-test bindings, and §16 v1 §16.8 cross-references in docstring. Each predicate signature matches the §4 Logician PRE/POST/COMMIT/META layer convention from §4 v2.x rows 193/194.

| # | Code | Stage | Function signature | v0.1 body |
|---|------|-------|--------------------|-----------|
| 1 | F-PACKET-INSTANCE-LEAK | PRE-emission | `def predicate_instance_leak(packet: ReflectionPacketLike) -> GateOutcome:` | `raise NotImplementedError("F-PACKET-INSTANCE-LEAK body lands at v0.2 first wave compound LOCK per §16 §16.9; signature reserved + three-layer detection scope (NFKC + NER + regex per §15.9.2 RT-07 precedent) registered at v0.1 hook")` |
| 2 | F-PACKET-CROSS-ORG-LEAK | PRE-emission + PRE-load | `def predicate_cross_org_leak(*, target_write_path: str, packet_org_slug: str, span_provenance: PacketSpanProvenanceLike) -> GateOutcome:` | NotImplementedError — body validates (a) target_write_path slug matches packet.org_slug (mirror of f_wpfa_cross_org_leak.py byte-for-byte) AND (b) every span_id's recorded org_slug matches packet.org_slug (sub-tag `.span_org_slug_mismatch` per RT-09 fold-in) |
| 3 | F-PACKET-FABRICATION | POST-emission + POST-load | `def predicate_fabrication(packet: ReflectionPacketLike, logfire_span_tree: SpanTreeLike) -> GateOutcome:` | NotImplementedError — gate_pass_counts + score_signals + outcome must equal aggregated counts in cycle's Logfire span tree |
| 4 | F-PACKET-CLASS-SLOT-LEAK | PRE-emission | `def predicate_class_slot_leak(packet_json_bytes: bytes) -> GateOutcome:` | NotImplementedError — mirrors F-CLASS-SLOT-ID-NON-OPAQUE from v7.0.7 (semantic slot name in cloud-routed payload) |
| 5 | F-PACKET-CLASS-MISLABEL | PRE-emission | `def predicate_class_mislabel(*, packet_classification_register_version: str, register_at_cycle_start: ClassRegisterLike) -> GateOutcome:` | NotImplementedError — defends against MINJA-shaped in-cycle relabeling |
| 6 | F-PACKET-EVAL-ONLY-GROUNDED | PRE-emission | `def predicate_eval_only_grounded(grounding_signal_classes: frozenset[str]) -> GateOutcome:` | NotImplementedError — sibling to F-REFLECTION-EVAL-ONLY-GROUNDED at artifact-validity layer |
| 7 | F-PACKET-PREMATURE-GENERALIZATION | PRE-emission | `def predicate_premature_generalization(lessons_proposed: tuple[ProposedLessonLike, ...]) -> GateOutcome:` | NotImplementedError — frequency==1 requires severity=="HIGH" |
| 8 | **F-PACKET-SPAN-PROVENANCE-MISSING** | PRE-emission | `def predicate_span_provenance_missing(*, per_claim_span_ids: Mapping[str, tuple[str, ...]], resolvable_span_ids: Iterable[str], required_claim_keys: frozenset[str], packet_cycle_id: str) -> GateOutcome:` | NotImplementedError — body mirrors `check_f_wpfa_span_provenance_missing` from `f_wpfa_span_provenance_missing.py` PLUS sub-tag `.span_id_from_different_cycle` per RT-08 fold-in. **RESOLVES §17 v1 §6.5 forward-reference at this LOCK.** |
| 9 | F-PACKET-RETRIEVAL-CORRUPTION | PRE-load (Consumer C) | `def predicate_retrieval_corruption(packet_text_payload: bytes) -> GateOutcome:` | NotImplementedError — high-entropy burst + optimized-trigger fingerprint detection (AgentPoison / PoisonedRAG defense) |
| 10 | F-PACKET-MEMORY-INJECTION | PRE-emission | `def predicate_memory_injection(*, pattern_summaries: tuple[str, ...], proposed_rules: tuple[str, ...]) -> GateOutcome:` | NotImplementedError — three-layer detection (regex + NFKC-normalized regex + small classifier); MINJA-shaped substring scan |
| 11 | F-PACKET-SCHEMA-DRIFT | PRE-load | `def predicate_schema_drift(*, packet_schema_version: str, consumer_known_max: str) -> GateOutcome:` | NotImplementedError — v0.1 hook returns advisory; v1.x flips to fail-closed per OQ-5a |
| 12 | F-PACKET-CADENCE-VIOLATION | PRE-emission | `def predicate_cadence_violation(*, packet_emitted_at: str, cycle_close_marker_span_resolved: bool, packet_id_collision_seen: bool) -> GateOutcome:` | NotImplementedError — defends against mid-cycle reflection contaminating producer's own context window; sub-tag `.packet_id_collision` per Cycle 2 RT-C2-01 fold-in |
| 13 | F-PACKET-SIGNATURE-INVALID | PRE-load | `def predicate_signature_invalid(*, packet: ReflectionPacketLike, producer_pubkey: bytes, expected_canonical_bytes: bytes) -> GateOutcome:` | NotImplementedError — mirrors v7.0.4-M1 §2 KFR canonical-signature-invalid byte-for-byte; producer-pubkey resolution from white-glove-pinned registry (NOT from packet's emitted_by_seat field per RT-10 fold-in) |
| 14 | F-PACKET-OPERATOR-SIGNATURE-MISSING | PRE-load (Consumer B + C) | `def predicate_operator_signature_missing(*, packet_outcome_status: str, packet_operator_signature: str | None) -> GateOutcome:` | NotImplementedError — outcome.status non-PENDING REQUIRES operator_signature_ed25519 non-None; sub-tag `.signature_present_for_pending` per Cycle 2 RT-C2-02 fold-in (Packet 1 PENDING forbids non-None operator signature; defensive symmetry) |
| 15 | F-PACKET-OPERATOR-SIGNATURE-INVALID | PRE-load | `def predicate_operator_signature_invalid(*, packet: ReflectionPacketLike, operator_pubkey: bytes) -> GateOutcome:` | NotImplementedError — operator-pubkey verification (white-glove-pinned per v7.0.7 §6.1) |
| 16 | F-PACKET-CYCLE-ID-UNRESOLVABLE | PRE-emission | `def predicate_cycle_id_unresolvable(*, packet_cycle_id: str, cycle_close_marker_span_ids: frozenset[str], packet_cycle_close_marker_span_id: str) -> GateOutcome:` | NotImplementedError — cycle_id MUST resolve to a cycle-close marker span in Logfire export AT PRE-write |
| 17 | F-PACKET-OUTCOME-EVIDENCE-MISSING | PRE-emission + PRE-load | `def predicate_outcome_evidence_missing(*, packet_outcome_status: str, packet_outcome_evidence_span_ids: tuple[str, ...]) -> GateOutcome:` | NotImplementedError — outcome.status non-PENDING REQUIRES outcome_evidence_span_ids non-empty |
| 18 | F-PACKET-PRODUCER-UNAUTHORIZED | PRE-emission | `def predicate_producer_unauthorized(*, packet_emitted_by_seat: str, producer_registry: frozenset[str]) -> GateOutcome:` | NotImplementedError — closed-set membership check; v0.1 producer_registry = frozenset({"archivist.reflection_submode"}) |
| 19 | **F-PACKET-COVERAGE-INCOMPLETE** | META PRE-cycle | `def predicate_coverage_incomplete(gate_realization_registry: GateRealizationRegistry) -> GateOutcome:` | **LIVE body at v0.1 hook** — returns GateOutcome.PASS if every code in `_BINDING_F_PACKET_CODES` (codes 1-18) has a realized predicate body; else GateOutcome.FAIL_CLOSED with detail naming the missing-body codes. **Activation lever.** Mirrors F-REFLECTION-COVERAGE-INCOMPLETE row 404 byte-for-byte. |

## §3. PRE/POST/META layer distribution

- **PRE-emission** (producer-side): 1, 2, 4, 5, 6, 7, 8, 10, 12, 16, 17, 18 — **12 codes**
- **POST-emission / POST-load (artifact-validity replay)**: 3 — **1 code**
- **PRE-load (consumer-side)**: 2, 3, 9, 11, 13, 14, 15, 17 — **8 codes (with overlap on #2 and #17 — PRE-emission AND PRE-load)**
- **META (cycle-level)**: 19 — **1 code, LIVE body**

## §4. F-PACKET-* EXCLUDED from F-CLASS-COVERAGE-INCOMPLETE META gate

Per the §17 WPFA row 207 exclusion precedent (F-WPFA-* EXCLUDED from F-CLASS-COVERAGE-INCOMPLETE per OQ-6 default) and §2 v7.5 FG row 213 exclusion precedent (F-FG-* EXCLUDED per OQ-10 default), **F-PACKET-* is EXCLUDED from F-CLASS-COVERAGE-INCOMPLETE META-gate registry.** F-PACKET-* is its own family. F-PACKET-COVERAGE-INCOMPLETE owns realization-coverage for its own 18 BINDING codes. F-CLASS-COVERAGE-INCOMPLETE stays focused on F-CLASS-* family.

## §5. Module decomposition

19 codes; **one module per code** (no triplet-collapse — F-PACKET-* family has no triplet-like clusters that fit the §4 v2.x validation-triplet collapse pattern; all 19 codes are structurally independent).

- 18 modules per NotImplementedError body: `pipeline/logician/gates/f_packet_<code_lowercase>.py`
- 1 module per LIVE body: `pipeline/logician/gates/f_packet_coverage_incomplete.py`
- Cedar policy file: `pipeline/vault/policies/reflection_packet.cedar` (one file per family; 19 rules; 18 fail-closed-pending-implementation; 1 LIVE) — co-located with existing `kfr_canonical.cedar`, `operational_subkinds.cedar`, `report_*.cedar` Cedar policies under `pipeline/vault/policies/` (Cycle 1 fold-in: aligning with WPFA Cedar location convention rather than handoff packet's proposed `pipeline/logician/cedar/` directory; on-disk verification at Cycle 1 showed no `pipeline/logician/cedar/` directory exists).
- Test scaffold: `tests/logician/gates/test_f_packet_<code_lowercase>.py` (one test file per module; LIVE module gets real assertions; NotImplementedError modules get `@pytest.mark.skip` regressions on signature only).

## §6. AST-lint regression — F-CIC-CLC-COUPLING-VIOLATION extension

Per the F-CIC-CLC-COUPLING-VIOLATION enforcement pattern (architecture v7.0.8 amendment): no F-PACKET-* code crosses to §15 / §17; no F-REFLECTION-* code crosses to §16; no F-ARCHIVIST-* code crosses to §16; no F-WPFA-* code crosses to §16.

**AST-lint extension** (in `pipeline/linting/ast_lint.py` `LOGICIAN_IMPORT_BAN` rule family; precedent: `R-ARCHIVIST-NO-CANONICAL-MUTATE` enumeration pattern from §4 v2.x.1):

- Forbid imports of `f_wpfa_*` modules from `f_packet_*.py` files (and vice versa).
- Forbid imports of `f_reflection_*` modules from `f_packet_*.py` files (and vice versa).
- Forbid imports of `f_archivist_*` modules from `f_packet_*.py` files (and vice versa).
- Forbid imports of `F_REFLECTION_*` / `F_WPFA_*` / `F_ARCHIVIST_*` Final[str] constants from `f_packet_*.py` files.
- Unicode-normalized (NFKC) regex applied at closed-set membership check on code-id strings (per Cycle 1 RT-02 fold-in).

**Scope clarification — static-import only at v0.1 hook (Cycle 1 RT-02 fold-in).** The AST-lint scope is **static import statements** (`import X` / `from X import Y`). Dynamic-import vectors (`importlib.import_module`, `__import__`, `exec`, `eval` over runtime-resolved module names) are **BOUNDED-by-v7-LOCKED-A1+A4** single-client trusted-operator envelope (mirrors §4 v2.x.1 RT-01..06 BOUNDED disposition class). v2 multi-tenant Section O.5 mitigation track marker: dynamic-import detection extension at the v2 amendment with NFKC normalization of the runtime-resolved string against the F-* family prefix set. This BOUNDED disposition holds for v0.1 + v0.2 + v1.x; v2 multi-tenant amendment re-evaluates.

## §7. Cycle 1 + Cycle 2 disposition log (per row-170 transparent-disposition)

See `pipeline/blueprint/v0.1/section_16_reflection_packet.md` §16.10 for the full disposition log (this amendment paired-commits and inherits the same Cycle 1 + Cycle 2 dispositions; row-170 transparent-disposition applies to all three siblings).

Sub-tag extensions surfaced at Cycle 1 + Cycle 2 fold-ins:

- `.span_org_slug_mismatch` — sub-tag on F-PACKET-CROSS-ORG-LEAK per RT-09.
- `.span_id_from_different_cycle` — sub-tag on F-PACKET-SPAN-PROVENANCE-MISSING per RT-08.
- `.packet_id_collision` — sub-tag on F-PACKET-CADENCE-VIOLATION per Cycle 2 RT-C2-01.
- `.signature_present_for_pending` — sub-tag on F-PACKET-OPERATOR-SIGNATURE-MISSING per Cycle 2 RT-C2-02.

These sub-tag extensions are predicate-body-internal at v0.1 hook (predicates raise NotImplementedError; sub-tags surface at v0.2 live body). Documented here for v0.2 first wave amendment author contract per §4 v2.x.1 row-198 precedent.

## §8. Test surface (v0.1 hook scope)

- `tests/vault/sub_kinds/test_reflection_packets.py`:
  - Dataclass mechanics (frozen + kw_only enforcement; non-kw_only construction raises TypeError) — LIVE.
  - Canonical-codec round-trip (to_canonical_json_bytes(packet) → from_canonical_json_bytes() → re-construct → identity) — LIVE.
  - 21 invariant skeletons under `pytest.mark.skip(reason="v0.1 hook dormant; body lands at v0.2 first wave")` — predicate signatures verified.

- `tests/logician/gates/test_f_packet_<code>.py` (one per code):
  - 18 NotImplementedError modules: signature-only skip-marked regression test asserting the predicate exists + `raises NotImplementedError`.
  - 1 LIVE module (`test_f_packet_coverage_incomplete_meta_gate.py`): real assertions:
    - META-gate fires PASS when all 18 BINDING gate signatures are present (which they are at this LOCK because the signatures land — but the bodies raise NotImplementedError, and that distinction is what META-gate enforces at v0.2 first wave).
    - META-gate fires FAIL_CLOSED when the registry indicates any BINDING code's body raises NotImplementedError at runtime call (v0.2 first wave behavior simulated).

- AST-lint regression: `scripts/run_lint.sh pipeline` clean exit 0 (extends F-CIC-CLC-COUPLING-VIOLATION regression scope to F-PACKET-* per §6).

## §9. v1.x amendment-realization checklist (forward-binding contracts)

Per the §4 v2.x.1 + §11 v1.1 + §17 v1 forward-binding checklist precedent, this amendment binds the following contracts to the v0.2 first wave compound LOCK amendment author:

1. **18 NotImplementedError predicate bodies REQUIRE realized bodies** at v0.2 first wave. F-PACKET-COVERAGE-INCOMPLETE META-gate validates against live bodies at v0.2 cycle start; deployment fail-closes if any body raises NotImplementedError.
2. **SUB_KIND_REGISTRY entry registration** for `reflection_packet` lands at v0.2 first wave under `operational/reflection_packets/` per §2 v7.x companion amendment.
3. **Producer-pubkey registry** registration at v0.2 first wave (mirror of v7.0.7 §6.1 router-template-publisher-pubkey-registry byte-for-byte).
4. **Operator-pubkey** already pinned per v7.0.7 classification-register operator signature; consumer-side verification scaffolding lands at v0.2 first wave.
5. **Sub-tag exposure surfaces** (`.span_org_slug_mismatch`, `.span_id_from_different_cycle`, `.packet_id_collision`, `.signature_present_for_pending`) surface at v0.2 first wave live body in `GateOutcome.detail` field.
6. **Cedar policy `reflection_packet.cedar` rules** flip from `default-permit` (placeholder) to enforcing per-predicate semantics at v0.2 first wave.
7. **META-gate body-realization check** (Cycle 1 RT-01 fold-in): v0.2 first wave compound LOCK strengthens `f_packet_coverage_incomplete.py` body to dry-run-probe each of the 18 BINDING predicates with a minimal test payload AND verify the predicate does NOT raise `NotImplementedError`. Failure → FAIL_CLOSED with detail naming the un-realized code. This is the runtime complement to the §6.17 Option-B compound-paired-commit atomicity guarantee.
8. **Dynamic-import detection** (Cycle 1 RT-02 fold-in): v2 multi-tenant Section O.5 amendment extends AST-lint scope to flag `importlib.import_module` / `__import__` / `exec` / `eval` calls whose first argument resolves (after NFKC) to a forbidden F-* family prefix. BOUNDED-by-v7-LOCKED-A1+A4 at v0.1/v0.2/v1.x.

## §10. Audit trail

- Spec card: `pipeline/planning/reflection_packet_dispatch_spec_2026-05-11.md`
- Thesis dispatch packet: `pipeline/handoffs/ws_reflection_packet_handoff_2026-05-11.md`
- Audit trail: `pipeline/validation/reflection_packet_thesis_2026-05-11/`
- Sibling LOCK paired-commit: §16 v1 + §0.5 v22 (all at `lock_timestamp_utc` 2026-05-15)

---

**Filed:** 2026-05-15. LOCKED via L-005 strict two-cycle Thesis with FULL LIVE CROSS-FAMILY rigor. Compound paired-commit sibling 2/3 with §16 v1 + §0.5 v22.
