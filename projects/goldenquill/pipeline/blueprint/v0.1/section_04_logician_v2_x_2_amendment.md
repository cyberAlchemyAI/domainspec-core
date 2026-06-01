---
title: Blueprint §4 Logician — Amendment v2.x.2 (Reflection v0.1 Beta hook — 8 BINDING F-REFLECTION-* predicate signatures with NotImplementedError bodies + 8 HORIZON signature-only reservations + 1 PROBE-DEPENDENT signature-only reservation + 5 F-ARCHIVIST-* sub-tag extensions + named drift-test bindings + grounding-signal-class enum + inoculation frame body Appendix)
filed: 2026-05-10
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-10 — paired-commit sub-amendment with architecture v7.0.9 + §0.5 v18 §15.x reflection (compound paired-commit triple per §6.17 Option-B; all three LOCKED atomically at this ceremony). Predicate signatures at predicate-signature layer per L-006 dormant-binding pattern (architecture v7.0.7 §5.1 precedent). 8 BINDING gate predicate signatures land with NotImplementedError bodies (7 raise NotImplementedError; 1 = F-REFLECTION-COVERAGE-INCOMPLETE has live body as META-gate dormant-binding lever per architecture v7.0.9 §5); 8 HORIZON gate signatures reserved with `# SIGNATURE-ONLY at v0.1 hook` comment-marker; 1 PROBE-DEPENDENT gate signature reserved with same comment-marker. 5 sub-tag extensions on F-ARCHIVIST-* parents inherit predicate-body from parent §4 v2.x WS-L LOCK rows 193/194 (additive sub-tag entries in the FORBIDDEN_SUB_TAGS table; no new top-level predicate). L-005 strict two-cycle Thesis CLOSED with FULL LIVE CROSS-FAMILY RIGOR (audit trail at pipeline/validation/reflection_v0_1_hook_thesis_2026-05-10/). Cycle 2 UNANIMOUS READY_TO_LOCK across Editor (Llama-3.3-70B/Groq) + Judge (Gemini-2.5-Pro/Google, 100/100) + Red Team (GPT-OSS-120B/Groq, no new probes). 17 Cycle-1 FOLDED items CLOSED + 5 BOUNDED-by-v7-LOCKED-A1+A4 MAINTAINED + 1 REJECTED-with-rationale MAINTAINED per row-170 transparent disposition pattern.
parent_lock: pipeline/blueprint/v0.1/section_04_v2_x_amendment.md  # §4 v2.x LOCKED 2026-05-10 rows 193/194 (F-CLASS-COVERAGE-INCOMPLETE META-gate ACTIVATED; canonical realization pattern this amendment mirrors)
parent_lock_row: 193
predecessor_amendments_chain:
  - §4 v2.x LOCKED 2026-05-10 rows 193/194 — Tier-3 LOCK; ~44 failure codes across 4 slices; L-006 dormant-binding ACTIVATED via F-CLASS-COVERAGE-INCOMPLETE META gate
  - §4 v2.x.1 LOCKED 2026-05-10 rows 198/199 — narrow-corrective Tilth-RT-07 closure; sub-tag-extension pattern for R-ARCHIVIST-NO-CANONICAL-MUTATE (six sub-tags); CANONICAL PRECEDENT FOR sub-tag-extension §0.5 paired-commit pattern
companion_lock_paired_commit:
  - pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md  # architectural-primitive-layer registration (17 F-REFLECTION-* primitives + 5 F-ARCHIVIST-* sub-tag extensions + grounding-signal-class registry + F-REFLECTION-COVERAGE-INCOMPLETE META-gate + inoculation frame body + internal-vs-external naming discipline)
  - pipeline/blueprint/v0.1/section_00_5_section_15_reflection_amendment.md  # interface-index row append
amendment_class: forward-binding predicate-signature-layer (BINDING set has NotImplementedError bodies; HORIZON + PROBE-DEPENDENT sets are signature-only reservations)
precedent_pattern: §4 v2.x WS-L LOCK rows 193/194 (Slice 3 F-CLASS-* dormant primitives with NotImplementedError bodies) + §4 v2.x.1 LOCK rows 198/199 (sub-tag-extension pattern). This amendment combines both: BINDING set follows v2.x Slice-3 NotImplementedError pattern; sub-tag extensions follow v2.x.1 row-198 pattern.
operator_refinement_session: 2026-05-10 mid-Thesis — operator pinned 17 → 8 BINDING reduction + 9 HORIZON/PROBE-DEPENDENT registrations + probe registry narrow + heavy-Reflection swap full defer + inoculation frame template wording + internal-vs-external naming. Refinement applied pre-LOCK; this DRAFT reflects the post-refinement state.
threat_severity_at_v0_1_v0_2: LOW — predicate signatures only; no runtime invocation; BINDING bodies raise NotImplementedError; HORIZON + PROBE-DEPENDENT have no body at all. Activation gated by F-REFLECTION-COVERAGE-INCOMPLETE PRE-cycle META-gate. The v0.1 Beta hook does NOT compete with v0.1 Beta close-out items (Intake full-impl, Uploader full-impl, Classification Review UX, WS-L Code phase).
purpose: Realize the 17 F-REFLECTION-* gate signatures + 5 F-ARCHIVIST-* sub-tag extensions registered at architecture v7.0.9 §2 in the §4 Logician predicate-signature layer. NotImplementedError bodies for the 8 BINDING; signature-only reservations for the 8 HORIZON + 1 PROBE-DEPENDENT. Named drift-test bindings per row-198 precedent for v1.x runtime amendment-author contract.
companion_code_landed:
  - "pipeline/orchestrator/seats/archivist/reflection_mode.py (NEW SCAFFOLD — Pydantic AI agent stub + 17 predicate-signature stubs + 5 sub-tag wiring + drift-test binding hooks + grounding-signal-class enum + inoculation frame body constant + inoculation_frame_body_v1_sha3_512 digest)"
  - "pipeline/logician/gates/reflection_gates.py (NEW — F-REFLECTION-* predicate signature registry; 8 BINDING NotImplementedError bodies; 9 HORIZON/PROBE-DEPENDENT signature-only reservations with marker comments; cross-reference to FORBIDDEN_SUB_TAGS for sub-tag extensions)"
companion_tests_landed:
  - "tests/logician/gates/test_reflection_gates_skeleton.py (NEW — predicate-signature presence assertions + sub-tag-coverage assertions + BINDING-vs-HORIZON tier assertions + F-REFLECTION-COVERAGE-INCOMPLETE META-gate registration test + grounding-signal-class enum membership test + inoculation frame body digest stability test)"
done_definition_at_lock:
  - "8 BINDING predicate signatures landed in pipeline/logician/gates/reflection_gates.py with NotImplementedError bodies + named drift-test bindings."
  - "8 HORIZON + 1 PROBE-DEPENDENT predicate signatures landed in the same module with `# SIGNATURE-ONLY at v0.1 hook; body lands at v0.2 SPEC / v1.x runtime` comment-markers."
  - "5 F-ARCHIVIST-* sub-tag extensions landed in pipeline/orchestrator/seats/archivist sub-mode wiring (no new top-level predicate; sub-tag entries in the parent gate's FORBIDDEN_SUB_TAGS table)."
  - "GroundingSignalClass enum at code-level (8 members per architecture v7.0.9 §4)."
  - "INOCULATION_FRAME_BODY_V1 constant (verbatim operator-drafted text per architecture v7.0.9 §7) + INOCULATION_FRAME_BODY_V1_SHA3_512 digest constant."
  - "Skeleton tests passing at predicate-signature-layer: 17 signature-present + 5 sub-tag-present + 8 BINDING-raises-NotImplementedError + 8 HORIZON + 1 PROBE-DEPENDENT signature-only + 8 enum members + digest-stable = 47 tests."
  - "AST-lint clean exit 0 (no new R-* rule needed; sub-tag extensions inherit from R-ARCHIVIST-NO-CANONICAL-MUTATE parent)."
  - "L-005 strict two-cycle Thesis CLOSED with FULL live cross-family rigor (Editor + Judge + Red Team unanimous READY_TO_LOCK)."
cowork_thesis_dispatch_status: BOTH CYCLES COMPLETE 2026-05-10. Cycle 1 dispatched 18:03Z..18:09Z. Cycle 2 dispatched 18:16Z..18:17Z. All dispatches via mcp__Control_your_Mac__osascript → openclaw bridge per AGENTS.md. Working templates cloned from pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh + adapted to pipeline/validation/reflection_v0_1_hook_thesis_2026-05-10/dispatch_audit_v{1,2}.sh. L-005 strict two-cycle CLOSED at UNANIMOUS READY_TO_LOCK.
ws_dispatch: WS-Reflection v0.1 Beta hook (architecture v7.0.9 + §4 v2.x.2 + §0.5 v18 §15.x triple).
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment v2.x.2 — Reflection v0.1 Beta hook (F-REFLECTION-* gate-family realization at predicate-signature layer)

## §0. Amendment intent + scope

This amendment **realizes** at the §4 Logician predicate-signature layer the F-REFLECTION-\* gate-family registered at architecture v7.0.9 §2. It is a **paired-commit sub-amendment** with architecture v7.0.9 (registration) + §0.5 v18 §15.x (interface-index row append). All three LOCK atomically per §6.17 Option-B compound-paired-commit discipline; neither LOCKs without the other two.

**Operator-refined scope (2026-05-10 mid-Thesis).** The synthesis-default 17 BINDING primitives were operator-narrowed to **8 BINDING** primitives at architecture v7.0.9 §2.1. The remaining **8 HORIZON** primitives (§2.2) + **1 PROBE-DEPENDENT** primitive (§2.3) still register in this amendment but as signature-only reservations — no NotImplementedError body, just signature presence + comment-marker. **5 F-ARCHIVIST-\* sub-tag extensions** (§2.3 unchanged from synthesis §4.2) ride under existing parent gates per the §4 v2.x.1 row-198 sub-tag-extension precedent.

**Composition with §4 v2.x and §4 v2.x.1.** The existing §4 v2.x amendment (rows 193/194) hosts the F-ARCHIVIST-\* gate family at §15.9.x + the F-CLASS-COVERAGE-INCOMPLETE META-gate pattern. The §4 v2.x.1 amendment (rows 198/199) demonstrates the sub-tag-extension pattern (six sub-tags on R-ARCHIVIST-NO-CANONICAL-MUTATE). This amendment uses BOTH patterns:

- **F-REFLECTION-\* primitives (top-level)** use the v2.x Slice-3 NotImplementedError-body pattern for the 8 BINDING set; signature-only reservation pattern for the 8 HORIZON + 1 PROBE-DEPENDENT set.
- **F-ARCHIVIST-\* sub-tag extensions** use the v2.x.1 row-198 pattern — sub-tag entries added to the parent gate's FORBIDDEN_SUB_TAGS table; no new top-level predicate; no new module file.

## §1. Target glob + scope discipline

Target modules:

- `pipeline/logician/gates/reflection_gates.py` (NEW) — owns the 17 top-level F-REFLECTION-\* predicate signatures + the grounding-signal-class enum + the inoculation frame body constant + digest.
- `pipeline/orchestrator/seats/archivist/reflection_mode.py` (NEW SCAFFOLD) — Pydantic AI agent skeleton + predicate-stub wiring + sub-tag extension wiring into existing F-ARCHIVIST-\* parent gates.
- `pipeline/orchestrator/seats/archivist/` existing tree (UPDATED additive only) — FORBIDDEN_SUB_TAGS table per parent gate gains the 5 new `.reflection_*` entries. No predicate-body change; sub-tag entries inherit existing parent enforcement (AST-lint + runtime guard + Cedar policy).

Out of scope (NOT touched by this amendment):

- Existing F-ARCHIVIST-\* predicate bodies at §4 v2.x WS-L (rows 193/194). Sub-tag entries are additive to FORBIDDEN_SUB_TAGS only; predicate body unchanged.
- Existing F-CLASS-\* gate family at §4 v2.x Slice 3 (rows 193/194). Reflection composes against F-CLASS-ROUTING-INDETERMINATE for the always-local routing posture but does not modify F-CLASS-\* predicates.
- Any existing AST-lint rule. No new R-REFLECTION-\* rule needed (R-ARCHIVIST-NO-CANONICAL-MUTATE already forbids the low-level write primitives reflection would otherwise reach for per architecture v7.0.9 §1.1).
- Runtime guard wrapper at §15.9.3 line 521. Sub-tag extensions inherit existing wrapper coverage; v1.x runtime amendment may extend wrapper set if the BINDING predicate bodies surface a need (forward-binding; not v0.1 hook scope).

## §2. BINDING predicate signatures (8 — NotImplementedError bodies)

The 8 BINDING predicates land in `pipeline/logician/gates/reflection_gates.py` with NotImplementedError bodies, named drift-test bindings, and architecture-v7.0.9-§2.1-row cross-references in docstring. Each predicate signature matches the §4 Logician PRE/POST/COMMIT/META layer convention from §4 v2.x rows 193/194.

| # | Code | Stage | Function signature | NotImplementedError body | Drift-test binding |
|---|---|---|---|---|---|
| 1 | F-REFLECTION-NO-EXTERNAL-SIGNAL | PRE-write | `def predicate_no_external_signal(reflection_input: ReflectionInput) -> GateOutcome:` | `raise NotImplementedError("F-REFLECTION-NO-EXTERNAL-SIGNAL body lands at v1.x runtime per architecture v7.0.9 §2.1 row 1; signature reserved + grounding_signal_classes field-presence semantic registered at v0.1 hook")` | `tests/logician/gates/test_reflection_no_external_signal_body_drift.py::test_signature_matches_v7_0_9_row_1` |
| 2 | F-REFLECTION-EVAL-ONLY-GROUNDED | PRE-write | `def predicate_eval_only_grounded(reflection_input: ReflectionInput) -> GateOutcome:` | `raise NotImplementedError("F-REFLECTION-EVAL-ONLY-GROUNDED body lands at v1.x runtime per architecture v7.0.9 §2.1 row 2; signature reserved + grounding_signal_classes set-membership semantic registered at v0.1 hook")` | `tests/logician/gates/test_reflection_eval_only_grounded_body_drift.py::test_signature_matches_v7_0_9_row_2` |
| 3 | F-REFLECTION-INSUFFICIENT-EVIDENCE | PRE-write | `def predicate_insufficient_evidence(reflection_input: ReflectionInput, evidence_count_threshold: EvidenceCountThreshold) -> GateOutcome:` | `raise NotImplementedError("F-REFLECTION-INSUFFICIENT-EVIDENCE body lands at v1.x runtime per architecture v7.0.9 §2.1 row 3; signature reserved + evidence-count threshold semantic registered at v0.1 hook (default 3 per-funder, 2 per-CIC, 5 per-CLC)")` | `tests/logician/gates/test_reflection_insufficient_evidence_body_drift.py::test_signature_matches_v7_0_9_row_3` |
| 4 | F-REFLECTION-RFA-SPEC-OVERRIDE | PRE-write | `def predicate_rfa_spec_override(reflection_input: ReflectionInput, rfa_context: RFAContext) -> GateOutcome:` | `raise NotImplementedError("F-REFLECTION-RFA-SPEC-OVERRIDE body lands at v1.x runtime per architecture v7.0.9 §2.1 row 4; signature reserved + RFA-substrate-scan + Law-4 admin-risk-term semantic registered at v0.1 hook")` | `tests/logician/gates/test_reflection_rfa_spec_override_body_drift.py::test_signature_matches_v7_0_9_row_4` |
| 5 | F-REFLECTION-DEPTH-EXCEEDED | PRE-fire | `def predicate_depth_exceeded(reflection_invocation_context: ReflectionInvocationContext, depth_cap: int) -> GateOutcome:` | `raise NotImplementedError("F-REFLECTION-DEPTH-EXCEEDED body lands at v1.x runtime per architecture v7.0.9 §2.1 row 5; signature reserved + depth-counter semantic registered at v0.1 hook (hard cap depth-1 at v0.2; v1.x configurable)")` | `tests/logician/gates/test_reflection_depth_exceeded_body_drift.py::test_signature_matches_v7_0_9_row_5` |
| 6 | F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH | PRE-fire | `def predicate_self_evaluator_family_clash(reflection_invocation_context: ReflectionInvocationContext, router_config: RouterConfig) -> GateOutcome:` | `raise NotImplementedError("F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH body lands at v1.x runtime per architecture v7.0.9 §2.1 row 6; signature reserved + router.yaml family-field-comparison semantic registered at v0.1 hook; extends A3 cross-family rigor")` | `tests/logician/gates/test_reflection_self_evaluator_family_clash_body_drift.py::test_signature_matches_v7_0_9_row_6` |
| 7 | F-REFLECTION-WRITE-WITHOUT-COMMIT | COMMIT | `def predicate_write_without_commit(reflection_write_attempt: ReflectionWriteAttempt, journal_state: JournalState) -> GateOutcome:` | `raise NotImplementedError("F-REFLECTION-WRITE-WITHOUT-COMMIT body lands at v1.x runtime per architecture v7.0.9 §2.1 row 7; signature reserved + journal/commit-pattern semantic registered at v0.1 hook (mirrors §12 Uploader prepare-and-stage discipline)")` | `tests/logician/gates/test_reflection_write_without_commit_body_drift.py::test_signature_matches_v7_0_9_row_7` |
| 8 | F-REFLECTION-COVERAGE-INCOMPLETE | META PRE-cycle | `def predicate_coverage_incomplete(gate_realization_registry: GateRealizationRegistry) -> GateOutcome:` | **ACTIVE body at v0.1 hook** — checks the 8 BINDING set for predicate-body realization. Body: `return GateOutcome.PASS if all(_predicate_has_body(code) for code in _BINDING_F_REFLECTION_CODES) else GateOutcome.FAIL_CLOSED("F-REFLECTION-COVERAGE-INCOMPLETE: BINDING gate(s) lack predicate body — v1.x runtime amendment not yet LOCKed.")` | `tests/logician/gates/test_reflection_coverage_incomplete_meta_gate.py::test_meta_gate_fires_on_missing_binding_body` |

**META-gate scope at v0.1 hook.** F-REFLECTION-COVERAGE-INCOMPLETE is the ONLY F-REFLECTION-\* gate with a live (non-NotImplementedError) predicate body at v0.1 hook. Its scope is the 8 BINDING set: it inspects each BINDING gate's predicate function and asserts the function body does NOT raise NotImplementedError. At v0.1 hook, all 8 BINDING predicate bodies DO raise NotImplementedError (per the table above), so the META-gate fires FAIL_CLOSED at every cycle start — which is correct: v1.x Beta deployment cannot run Reflection cadence until v1.x runtime amendment LOCKs and realizes the 8 BINDING bodies. v0.1 Beta deployment is NOT affected because v0.1 Beta does not invoke the Reflection cadence at all (the cadence is dormant).

**Why F-REFLECTION-COVERAGE-INCOMPLETE has a live body at v0.1 hook.** Architecture v7.0.9 §5 names this gate ACTIVE at v0.1 hook as the dormant-binding lever. Per L-006, the META-gate enforces the dormant-binding contract; its body must be live for the contract to fire. The body is small (gate-realization-registry inspection) and deterministic. This matches the F-CLASS-COVERAGE-INCOMPLETE precedent from §4 v2.x WS-L LOCK rows 193/194.

## §3. HORIZON predicate signatures (8 — signature-only reservations)

The 8 HORIZON predicates land in `pipeline/logician/gates/reflection_gates.py` with **no predicate body** — not even NotImplementedError. Each is registered via a `# SIGNATURE-ONLY at v0.1 hook; body lands at v0.2 SPEC §15 v2.x` comment-marker + an empty function body (`pass`). The gate-realization-registry recognizes these as signature-only and excludes them from F-REFLECTION-COVERAGE-INCOMPLETE checks at v0.1 hook.

| # | Code | Stage | Function signature | Realization horizon |
|---|---|---|---|---|
| 1 | F-REFLECTION-INTENT-ANCHOR-DRIFT | POST-write META | `def predicate_intent_anchor_drift(reflection_history: ReflectionHistory, rolling_window: int) -> GateOutcome:` | v0.2 SPEC: signature-present + NotImplementedError body. v1.x runtime: body. |
| 2 | F-REFLECTION-CONTENT-LOOP-DETECTED | POST-write | `def predicate_content_loop_detected(reflection_input: ReflectionInput, similarity_index: SimilarityIndex, threshold: float) -> GateOutcome:` | v0.2 SPEC: signature-present + NotImplementedError body. v1.x runtime: body. |
| 3 | F-REFLECTION-EVAL-SURROGATE-DIVERGENCE | META cycle-level | `def predicate_eval_surrogate_divergence(class_7_8_ledger: EvalLedger, class_1_ledger: FunderOutcomeLedger, window: int) -> GateOutcome:` | v0.2 SPEC: signature-present + NotImplementedError body. v1.x runtime: body. |
| 4 | F-REFLECTION-OPERATOR-OVERRIDE-MASK | PRE-write | `def predicate_operator_override_mask(reflection_input: ReflectionInput, operator_pin_set: OperatorPinSet) -> GateOutcome:` | v0.2 SPEC: signature-present + NotImplementedError body. v1.x runtime: body. |
| 5 | F-REFLECTION-INOCULATION-FRAME-MISSING | PRE-fire (template) | `def predicate_inoculation_frame_missing(reflection_prompt_template: ReflectionPromptTemplate, expected_digest: str = INOCULATION_FRAME_BODY_V1_SHA3_512, exact_match: bool = True) -> GateOutcome:` (Cycle-1 RT-04 closure — `exact_match: bool = True` default kwarg locks the v1.x body to `hash == INOCULATION_FRAME_BODY_V1_SHA3_512` rather than substring/containment check per architecture v7.0.9 §7 exact-match-semantics contract) | v0.2 SPEC: signature-present + NotImplementedError body + template-store substrate. v1.x runtime: hash-verification body (exact-match only; substring-match fails closed). |
| 6 | F-REFLECTION-SELF-REPORTED-CONFIDENCE | POST-write | `def predicate_self_reported_confidence(reflection_text: str, evidence_class_counts: EvidenceClassCounts) -> GateOutcome:` | v0.2 SPEC: signature-present + NotImplementedError body. v1.x runtime: body. |
| 7 | F-REFLECTION-FABRICATION-ON-FAILURE | POST-effect | `def predicate_fabrication_on_failure(reflection_claimed_verdict: ReflectionVerdict, gate_outcome_ledger: GateOutcomeLedger) -> GateOutcome:` | v0.2 SPEC: signature-present + NotImplementedError body. v1.x runtime: hash-comparison body. |
| 8 | F-REFLECTION-PROBE-COVERAGE-INCOMPLETE | META pre-cycle deployment | `def predicate_probe_coverage_incomplete(probe_registry: ProbeRegistry, required_families: tuple[str, ...] = REQUIRED_PROBE_FAMILIES) -> GateOutcome:` | v0.2 SPEC: signature-present + NotImplementedError body. v1.x runtime: body. REQUIRED_PROBE_FAMILIES = `("sycophancy_probes", "proxy_metric_drift_probes", "fabrication_on_failure_probes")` per architecture v7.0.9 §6 narrowed probe registry. |

## §4. PROBE-DEPENDENT predicate signature (1 — signature-only reservation)

The 1 PROBE-DEPENDENT predicate lands in `pipeline/logician/gates/reflection_gates.py` with the same signature-only reservation pattern. Body lands when the corresponding probe family (`sycophancy_probes` per architecture v7.0.9 §6) ships at v1.x runtime.

| # | Code | Stage | Function signature | Realization horizon |
|---|---|---|---|---|
| 1 | F-REFLECTION-SYCOPHANCY-LOOP-DETECTED | META cycle-level | `def predicate_sycophancy_loop_detected(reflection_history: ReflectionHistory, sycophancy_probes: SycophancyProbes, n_cycles: int = 4) -> GateOutcome:` | v0.2 SPEC: signature-present + NotImplementedError body. v1.x runtime: body realizes when `sycophancy_probes` family ships. |

## §5. F-ARCHIVIST-* sub-tag extensions (5 — additive entries; no new top-level predicate)

Per the §4 v2.x.1 row-198 sub-tag-extension pattern: sub-tag entries land in the parent gate's FORBIDDEN_SUB_TAGS table; predicate body inherits from the parent gate already LOCKed at §4 v2.x rows 193/194. No new top-level predicate. No new module file. No new R-\* AST-lint rule (the existing R-ARCHIVIST-NO-CANONICAL-MUTATE forbids the low-level write primitives reflection would reach for per architecture v7.0.9 §1.1).

| Parent F-ARCHIVIST-* code | Owner module (existing) | New sub-tag entry | Wire-form reason_tag |
|---|---|---|---|
| F-ARCHIVIST-CROSS-ORG-LEAK | `pipeline/logician/gates/archivist_gates.py` (existing) | `.reflection_cross_org_read` | `archivist_cross_org_leak.reflection_cross_org_read` |
| F-ARCHIVIST-AUTO-APPLY-ATTEMPTED | `pipeline/logician/gates/archivist_gates.py` (existing) | `.reflection_attach_unsigned` | `archivist_auto_apply_attempted.reflection_attach_unsigned` |
| F-ARCHIVIST-LESSON-INSTANCE-LEAK | `pipeline/logician/gates/archivist_gates.py` (existing) | `.reflection_instance_in_pattern_field` | `archivist_lesson_instance_leak.reflection_instance_in_pattern_field` |
| F-ARCHIVIST-CADENCE-DRIFT | `pipeline/logician/gates/archivist_gates.py` (existing) | `.reflection_interval_drift` | `archivist_cadence_drift.reflection_interval_drift` |
| F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT | `pipeline/logician/gates/archivist_gates.py` (existing) | `.reflection_evidence_out_of_run` | `archivist_read_without_vault_intent.reflection_evidence_out_of_run` |

**Predicate body inheritance.** Each parent gate's existing predicate body (LOCKed at §4 v2.x rows 193/194) is unchanged. Sub-tag entry is purely declarative — added to the parent's FORBIDDEN_SUB_TAGS table; the parent predicate fires when the relevant invocation matches the sub-tag's predicate sketch (per architecture v7.0.9 §3 + this amendment §5 table). At v0.1 hook the sub-tag entries are present but the Reflection cadence is not invoked, so the sub-tags do not fire at runtime.

**Dot-handling + wire-form convention** (per §4 v2.x.1 §2.2): FORBIDDEN_SUB_TAGS table values are bare sub-tag names (no leading dot). The parent gate's emitter prepends the parent's reason-tag root (e.g., `archivist_auto_apply_attempted.`) at emit time to produce the wire-form reason_tag.

**Monotonic `run_id` binding for `.reflection_attach_unsigned` (Cycle-1 RT-01-C closure).** The Ed25519 signature on `(input_hash, output_hash, run_id)` per architecture v7.0.4-M1 audit-log monotonic-counter pattern + architecture v7.0.9 §3 binding contract: v1.x runtime amendment MUST realize the `.reflection_attach_unsigned` sub-tag predicate body with a Vault-stored monotonic counter check. The `run_id` MUST be strictly greater than the last recorded `run_id` for the `(input_hash, output_hash)` pair; rejection on equal-or-less + admin-risk ledger entry. v1.x amendment-realization checklist row binding at §11 below.

**Dynamic-dispatch sub-tag bypass class is BOUNDED-by-v7-LOCKED-A1+A4 (Cycle-1 RT-01-A disposition).** Sub-tag wire-form emission via `getattr` / `__dict__` / wildcard imports bypassing parent-gate predicate execution is bounded by v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight) per the §4 v2.x.1 §11.1 row 198 precedent. AST-lint is contributor-hygiene compile-time defense; v2 Section O.5 multi-tenant amendment-realization addresses this class via runtime gate-signature binding on audit-log entries.

## §6. Grounding-signal-class enum (code-level realization of architecture v7.0.9 §4)

Lands in `pipeline/logician/gates/reflection_gates.py`:

```python
from enum import Enum

class GroundingSignalClass(str, Enum):
    """Eight signal classes per architecture v7.0.9 §4, precedence-ordered.

    Highest authority (rank 1) → lowest (rank 8).
    F-REFLECTION-NO-EXTERNAL-SIGNAL fail-closes when the set is empty.
    F-REFLECTION-EVAL-ONLY-GROUNDED fail-closes when the set ⊆ {EDITOR_VERDICT,
    JUDGE_SCORE, RED_TEAM_SCORE, SCRIBE_SELF_ASSESSMENT}.
    At least one of classes 1-6 must be present per the precedence rule.
    """
    EXTERNAL_FUNDER_OUTCOME = "external_funder_outcome"       # rank 1
    OPERATOR_APPROVAL = "operator_approval"                   # rank 2
    LOGICIAN_GATE_OUTCOME = "logician_gate_outcome"           # rank 3
    KFR_DRIFT_EVENT = "kfr_drift_event"                       # rank 4
    ADMIN_RISK_EVENT = "admin_risk_event"                     # rank 5
    MATCH_DB_OUTCOME = "match_db_outcome"                     # rank 6
    COUNCIL_SPLIT_EVENT = "council_split_event"               # rank 7 — NOT primary alone
    EDITOR_VERDICT = "editor_verdict"                         # rank 8 — NEVER primary alone
    JUDGE_SCORE = "judge_score"                               # rank 8 — NEVER primary alone
    RED_TEAM_SCORE = "red_team_score"                         # rank 8 — NEVER primary alone
    SCRIBE_SELF_ASSESSMENT = "scribe_self_assessment"         # rank 8 — NEVER primary alone

# Rank 1-6 (primary-eligible)
PRIMARY_ELIGIBLE_CLASSES: frozenset[GroundingSignalClass] = frozenset({
    GroundingSignalClass.EXTERNAL_FUNDER_OUTCOME,
    GroundingSignalClass.OPERATOR_APPROVAL,
    GroundingSignalClass.LOGICIAN_GATE_OUTCOME,
    GroundingSignalClass.KFR_DRIFT_EVENT,
    GroundingSignalClass.ADMIN_RISK_EVENT,
    GroundingSignalClass.MATCH_DB_OUTCOME,
})

# Rank 7 (admitted-with-class-1-6; never primary alone)
COUNCIL_SPLIT_CLASS: GroundingSignalClass = GroundingSignalClass.COUNCIL_SPLIT_EVENT

# Rank 8 (NEVER primary alone; F-REFLECTION-EVAL-ONLY-GROUNDED fail-closes on subset)
LLM_EVAL_ONLY_CLASSES: frozenset[GroundingSignalClass] = frozenset({
    GroundingSignalClass.EDITOR_VERDICT,
    GroundingSignalClass.JUDGE_SCORE,
    GroundingSignalClass.RED_TEAM_SCORE,
    GroundingSignalClass.SCRIBE_SELF_ASSESSMENT,
})
```

The enum + frozensets are persistent at v0.1 hook. NotImplementedError predicate bodies in the BINDING set reference these constants by name; v1.x runtime amendment uses them as the structural enforcement substrate for F-REFLECTION-NO-EXTERNAL-SIGNAL + F-REFLECTION-EVAL-ONLY-GROUNDED.

## §7. Inoculation frame body Appendix (architecture v7.0.9 §7 realization at code-level)

Lands in `pipeline/logician/gates/reflection_gates.py`:

```python
# Architecture v7.0.9 §7 operator-drafted authoritative wording (verbatim).
# UTF-8, LF line endings, no trailing whitespace, no BOM.
# Hash-verified at v1.x runtime by F-REFLECTION-INOCULATION-FRAME-MISSING.
INOCULATION_FRAME_BODY_V1: str = (
    "Reflection is permitted to improve process memory, identify recurring "
    "failure patterns, and propose safer future defaults. Reflection is not "
    "permitted to rewrite facts, override operator judgment, infer commitments, "
    "invent lessons from insufficient evidence, or treat evaluator approval as "
    "real-world success."
)

# Computed once at module load; tests assert stability.
INOCULATION_FRAME_BODY_V1_SHA3_512: str = (
    # Resolved at module load via hashlib.sha3_512(INOCULATION_FRAME_BODY_V1.encode("utf-8")).hexdigest()
    # Test test_inoculation_frame_body_v1_digest_stable asserts this value
    # matches the module-load computation; drift in the body string fails the test.
    "<RESOLVED_AT_MODULE_LOAD>"
)
```

The constant + digest are persistent at v0.1 hook. F-REFLECTION-INOCULATION-FRAME-MISSING (HORIZON per §3 row 5) carries `INOCULATION_FRAME_BODY_V1_SHA3_512` as a default keyword argument so the v0.2 SPEC signature presence + v1.x runtime body have a stable hash anchor. The digest is computed at module load (not hardcoded as a literal in the source) — the test `test_inoculation_frame_body_v1_digest_stable` asserts the literal value in the module's source matches the runtime-computed digest, so any drift in the body string fails the test before runtime invocation.

## §7.1 Internal-vs-external naming alignment with architecture v7.0.9 §8 (Cycle-1 E-02 closure)

Architecture v7.0.9 §8 is the authority for the internal-vs-external naming discipline. This blueprint amendment is internal-context per §8.1 — all code identifiers, predicate function names, gate-realization-registry keys, drift-test bindings, and audit-trail directory naming use the internal `reflection_*` / `F-REFLECTION-*` / `predicate_*` convention. External-context surfaces (operator-facing CLI strings, customer-facing materials, business-plan language) use "Lessons Memory" / `tilth archivist lessons` per architecture v7.0.9 §8.2. This amendment's text + companion code + companion tests are internal-context and MUST continue to use `reflection_*` for grep-anchor coherence; v0.2 SPEC + v1.x runtime amendment authors MUST cross-reference architecture v7.0.9 §8 before authoring any customer-facing surface that would touch this gate family.

## §8. PRE/POST/COMMIT/META position distribution

Per architecture v7.0.9 §2.1 + §2.2 + §2.3, the 17 F-REFLECTION-\* primitives distribute across the §4 Logician PRE/POST/COMMIT/META layering as follows:

| Layer | BINDING (v0.1 hook NotImplementedError body) | HORIZON (v0.1 hook signature-only) | PROBE-DEPENDENT (v0.1 hook signature-only) |
|---|---|---|---|
| **PRE-fire** | F-REFLECTION-DEPTH-EXCEEDED, F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH | F-REFLECTION-INOCULATION-FRAME-MISSING (template) | — |
| **PRE-write** | F-REFLECTION-NO-EXTERNAL-SIGNAL, F-REFLECTION-EVAL-ONLY-GROUNDED, F-REFLECTION-INSUFFICIENT-EVIDENCE, F-REFLECTION-RFA-SPEC-OVERRIDE | F-REFLECTION-OPERATOR-OVERRIDE-MASK | — |
| **POST-write** | — | F-REFLECTION-CONTENT-LOOP-DETECTED, F-REFLECTION-SELF-REPORTED-CONFIDENCE, F-REFLECTION-INTENT-ANCHOR-DRIFT (META) | — |
| **POST-effect** | — | F-REFLECTION-FABRICATION-ON-FAILURE | — |
| **COMMIT** | F-REFLECTION-WRITE-WITHOUT-COMMIT | — | — |
| **META** (cycle / deployment) | F-REFLECTION-COVERAGE-INCOMPLETE (PRE-cycle — ACTIVE body at v0.1 hook) | F-REFLECTION-EVAL-SURROGATE-DIVERGENCE (cycle), F-REFLECTION-PROBE-COVERAGE-INCOMPLETE (deployment) | F-REFLECTION-SYCOPHANCY-LOOP-DETECTED (cycle) |

This distribution matches the §4 Logician v2.x.1 PRE/POST/COMMIT layering precedent. The META-gate cluster (3 codes: F-REFLECTION-EVAL-SURROGATE-DIVERGENCE, F-REFLECTION-PROBE-COVERAGE-INCOMPLETE, F-REFLECTION-SYCOPHANCY-LOOP-DETECTED) is the new structural axis Reflection introduces — cycle-level / deployment-level analysis rather than per-call analysis. Pattern-matches `F-PIPE-TRACK-FROZEN` META (rows 188-189) but at a different temporal scope.

## §9. Failure-code table (registry per row-198 precedent)

| Code | Tier | Module | Severity | Cycle |
|---|---|---|---|---|
| F-REFLECTION-NO-EXTERNAL-SIGNAL | BINDING (v0.1 hook NotImplementedError) | `pipeline/logician/gates/reflection_gates.py` | HIGH (inherits Lane 3 grounding-signal-class enforcement) | §4 v2.x.2 Reflection v0.1 Beta hook 2026-05-10 |
| F-REFLECTION-EVAL-ONLY-GROUNDED | BINDING (v0.1 hook NotImplementedError) | same | HIGH | same |
| F-REFLECTION-INSUFFICIENT-EVIDENCE | BINDING (v0.1 hook NotImplementedError) | same | HIGH | same |
| F-REFLECTION-RFA-SPEC-OVERRIDE | BINDING (v0.1 hook NotImplementedError) | same | HIGH (inherits Law 2 admin-risk severity) | same |
| F-REFLECTION-DEPTH-EXCEEDED | BINDING (v0.1 hook NotImplementedError) | same | MEDIUM | same |
| F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH | BINDING (v0.1 hook NotImplementedError) | same | HIGH (inherits A3 cross-family rigor severity) | same |
| F-REFLECTION-WRITE-WITHOUT-COMMIT | BINDING (v0.1 hook NotImplementedError) | same | HIGH (mirrors §12 Uploader prepare-and-stage severity) | same |
| F-REFLECTION-COVERAGE-INCOMPLETE | BINDING (v0.1 hook ACTIVE body) | same | HIGH (META-gate dormant-binding lever) | same |
| F-REFLECTION-INTENT-ANCHOR-DRIFT | HORIZON (v0.1 signature-only; v0.2 SPEC NotImplementedError; v1.x body) | same | MEDIUM | same |
| F-REFLECTION-CONTENT-LOOP-DETECTED | HORIZON (v0.1 signature-only) | same | MEDIUM | same |
| F-REFLECTION-EVAL-SURROGATE-DIVERGENCE | HORIZON (v0.1 signature-only) | same | HIGH | same |
| F-REFLECTION-OPERATOR-OVERRIDE-MASK | HORIZON (v0.1 signature-only) | same | HIGH | same |
| F-REFLECTION-INOCULATION-FRAME-MISSING | HORIZON (v0.1 signature-only; template body recorded per §7) | same | HIGH | same |
| F-REFLECTION-SELF-REPORTED-CONFIDENCE | HORIZON (v0.1 signature-only) | same | MEDIUM | same |
| F-REFLECTION-FABRICATION-ON-FAILURE | HORIZON (v0.1 signature-only) | same | HIGH | same |
| F-REFLECTION-PROBE-COVERAGE-INCOMPLETE | HORIZON (v0.1 signature-only) | same | HIGH (META deployment-gate analog of F-REFLECTION-COVERAGE-INCOMPLETE) | same |
| F-REFLECTION-SYCOPHANCY-LOOP-DETECTED | PROBE-DEPENDENT (v0.1 signature-only) | same | MEDIUM | same |
| **5 F-ARCHIVIST-\* sub-tag extensions** | additive (inherit parent severity) | `pipeline/logician/gates/archivist_gates.py` (existing) | inherits parent | same |

17 top-level F-REFLECTION-\* failure codes (8 BINDING + 8 HORIZON + 1 PROBE-DEPENDENT) + 5 F-ARCHIVIST-\* sub-tag extensions. New top-level failure-code row count = 17.

## §10. Acceptance test surface (in `tests/logician/gates/test_reflection_gates_skeleton.py`)

47 tests at skeleton level:

- 17 `test_<code>_predicate_signature_present` — each F-REFLECTION-\* predicate function is importable from `pipeline.logician.gates.reflection_gates` at the documented signature.
- 8 `test_<code>_predicate_body_raises_not_implemented_error` — each BINDING predicate (excluding F-REFLECTION-COVERAGE-INCOMPLETE which has live body) raises NotImplementedError on any non-trivial input.
- 1 `test_coverage_incomplete_meta_gate_fires_on_missing_binding_body` — F-REFLECTION-COVERAGE-INCOMPLETE returns FAIL_CLOSED when any of the 7 NotImplementedError-bodied BINDING predicates are inspected.
- 9 `test_<code>_signature_only_no_body` — each HORIZON / PROBE-DEPENDENT predicate has an empty `pass` body (no NotImplementedError, no live behavior) — signature reservation only.
- 5 `test_<sub_tag>_present_in_parent_FORBIDDEN_SUB_TAGS` — each of the 5 F-ARCHIVIST-\* sub-tag extensions is present in the corresponding parent gate's FORBIDDEN_SUB_TAGS table.
- 1 `test_grounding_signal_class_enum_has_8_members` — GroundingSignalClass enum has 11 members (8 distinct ranks; rank 8 has 4 members per the LLM-eval-only group) and the precedence-ordered frozenset constants resolve correctly.
- 1 `test_primary_eligible_classes_frozenset_membership` — PRIMARY_ELIGIBLE_CLASSES is exactly {EXTERNAL_FUNDER_OUTCOME, OPERATOR_APPROVAL, LOGICIAN_GATE_OUTCOME, KFR_DRIFT_EVENT, ADMIN_RISK_EVENT, MATCH_DB_OUTCOME}.
- 1 `test_llm_eval_only_classes_frozenset_membership` — LLM_EVAL_ONLY_CLASSES is exactly {EDITOR_VERDICT, JUDGE_SCORE, RED_TEAM_SCORE, SCRIBE_SELF_ASSESSMENT}.
- 1 `test_inoculation_frame_body_v1_digest_stable` — the literal value in `INOCULATION_FRAME_BODY_V1_SHA3_512` matches the runtime-computed `hashlib.sha3_512(INOCULATION_FRAME_BODY_V1.encode("utf-8")).hexdigest()`; drift in the body string fails the test.
- 1 `test_inoculation_frame_body_v1_verbatim_against_v7_0_9_section_7` — the body string matches the verbatim wording from architecture v7.0.9 §7 (test file embeds the expected text as a fixture; drift in either surface fails).
- 1 `test_required_probe_families_tuple_matches_v7_0_9_section_6` — REQUIRED_PROBE_FAMILIES tuple is exactly `("sycophancy_probes", "proxy_metric_drift_probes", "fabrication_on_failure_probes")` per architecture v7.0.9 §6.
- 1 `test_no_predicate_has_loop_divergence_probes_dependency` — no signature mentions `loop_divergence_probes` (deferred per architecture v7.0.9 §6 + operator refinement Q4).
- 1 `test_binding_horizon_probe_dependent_tier_disjoint` — the three tier sets {BINDING, HORIZON, PROBE-DEPENDENT} are mutually disjoint and cover all 17 codes.

## §11. v1.x amendment-realization checklist (named drift-test bindings per row-198 precedent)

When the v1.x runtime amendment lands, the predicate bodies for the 8 BINDING gates (excluding F-REFLECTION-COVERAGE-INCOMPLETE which is already live) realize. The v1.x amendment author MUST:

```
[ ] F-REFLECTION-NO-EXTERNAL-SIGNAL body implements the grounding_signal_classes
    field-presence check (signature reserved at v0.1 hook + §6 grounding-signal-class
    enum already on-disk; body = empty-set check + ≥1-class assertion).
    Drift-test: tests/logician/gates/test_reflection_no_external_signal_body_drift.py
    ::test_signature_matches_v7_0_9_row_1
[ ] F-REFLECTION-EVAL-ONLY-GROUNDED body implements the set-membership check against
    LLM_EVAL_ONLY_CLASSES (signature + frozenset reserved at v0.1 hook).
    Body MUST use explicit disjoint-set check: `if not (grounding_signal_classes
    & PRIMARY_ELIGIBLE_CLASSES): raise GateFailure` (Cycle-1 RT-03 closure — guards
    against class-7-alone admission via sloppy set-membership logic).
    Drift-tests:
      tests/logician/gates/test_reflection_eval_only_grounded_body_drift.py
        ::test_signature_matches_v7_0_9_row_2
      tests/logician/gates/test_reflection_eval_only_grounded_body_drift.py
        ::test_class_7_alone_fails_closed  (NEW per Cycle-1 RT-03 closure — payload
        containing only COUNCIL_SPLIT_EVENT must fail-closed; class-1-6 must accompany)
[ ] F-REFLECTION-INSUFFICIENT-EVIDENCE body implements the per-funder / per-CIC /
    per-CLC count threshold check (defaults 3 / 2 / 5 per architecture v7.0.9 §2.1 row 3).
    Drift-test: tests/logician/gates/test_reflection_insufficient_evidence_body_drift.py
    ::test_signature_matches_v7_0_9_row_3
[ ] F-REFLECTION-RFA-SPEC-OVERRIDE body implements the string-match + Law-4 admin-risk
    substrate scan (signature + RFAContext type reserved at v0.1 hook).
    Drift-test: tests/logician/gates/test_reflection_rfa_spec_override_body_drift.py
    ::test_signature_matches_v7_0_9_row_4
[ ] F-REFLECTION-DEPTH-EXCEEDED body implements the depth-counter check (hard cap
    depth-1 at v0.2; v1.x configurable per architecture v7.0.9 §2.1 row 5).
    Drift-test: tests/logician/gates/test_reflection_depth_exceeded_body_drift.py
    ::test_signature_matches_v7_0_9_row_5
[ ] F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH body implements the router.yaml family-
    field comparison (extends A3 cross-family rigor per architecture v7.0.9 §2.1 row 6).
    Drift-test: tests/logician/gates/test_reflection_self_evaluator_family_clash_body_drift.py
    ::test_signature_matches_v7_0_9_row_6
[ ] F-REFLECTION-WRITE-WITHOUT-COMMIT body implements the journal/commit-pattern check
    (mirrors §12 Uploader prepare-and-stage discipline per architecture v7.0.9 §2.1 row 7).
    Body MUST bind both stages (journal-write + output_validator-success → commit) to the
    SAME transaction-id with a cryptographic checkpoint: the journal entry stores
    `sha3_512(validated_output)` and the COMMIT gate verifies the checkpoint against the
    actual committed output before proceeding (Cycle-1 RT-06 closure — guards against
    cross-cycle replay where a crash between journal-write + output_validator allows
    a later retry to skip validation).
    Drift-tests:
      tests/logician/gates/test_reflection_write_without_commit_body_drift.py
        ::test_signature_matches_v7_0_9_row_7
      tests/logician/gates/test_reflection_write_without_commit_body_drift.py
        ::test_cross_cycle_replay_without_transaction_id_fails_closed  (NEW per
        Cycle-1 RT-06 closure)
[ ] F-REFLECTION-COVERAGE-INCOMPLETE body REMAINS the gate-realization-registry
    inspection check (live at v0.1 hook; v1.x amendment does NOT replace — only the
    BINDING set it inspects gains realized bodies, which clears the META-gate).
[ ] HORIZON gate F-REFLECTION-PROBE-COVERAGE-INCOMPLETE body MUST include explicit
    set-subset assertion: `assert set(REQUIRED_PROBE_FAMILIES).issubset(probe_registry)`
    (Cycle-1 NP-04 closure — guards against the gate's body remaining `pass` no-op
    in v1.x while pretending to enforce probe coverage). Drift test:
    tests/logician/gates/test_reflection_probe_coverage_incomplete_body_drift.py
      ::test_missing_required_family_fails_closed  (NEW at v0.2 SPEC + v1.x runtime)
[ ] HORIZON gate F-REFLECTION-INOCULATION-FRAME-MISSING body MUST enforce exact-match
    hash semantics: `hash = sha3_512(full_prompt.encode("utf-8")).hexdigest()` followed
    by `assert hash == INOCULATION_FRAME_BODY_V1_SHA3_512` — substring/containment
    checks fail closed (Cycle-1 RT-04 closure + architecture v7.0.9 §7 contract).
    Drift test: tests/logician/gates/test_reflection_inoculation_frame_missing_body_drift.py
      ::test_substring_match_fails_closed  (NEW per Cycle-1 RT-04 closure)
[ ] Drift-test files at tests/logician/gates/test_reflection_*_body_drift.py
    EXIST on disk at v1.x LOCK and assert the signature contract holds against the
    realized body.
[ ] v1.x amendment frontmatter cross-references back to this §4 v2.x.2 binding contract.
```

This is a **named, location-binding contract**, not a soft commitment. Drift detected mid-v1.x is itself a F-INDEX-STALE-class defect.

**Test-file existence at §4 v2.x.2 LOCK.** The 7 drift-test files at `tests/logician/gates/test_reflection_*_body_drift.py` do **NOT** exist on disk at §4 v2.x.2 LOCK — this is intentional. The v1.x runtime amendment + the realized predicate bodies the tests pair with are v1.x deliverables; the body the test pairs with is defined by the v1.x author, not by this amendment. Creating the files as v0.1 skeleton stubs would either (a) raise NotImplementedError deterministically at pytest collection time and force §4 v2.x.2 LOCK to ship with a known-red test in the suite, or (b) assert against a non-existent body surface and falsely turn green. Neither preserves the contract. The contract is a **forward-binding requirement on v1.x**: at v1.x LOCK ceremony the 7 files must exist, the function names must match, the assertion form must hold, and v1.x amendment frontmatter must cross-reference back to this §4 v2.x.2 §11 binding contract. Mirrors the §4 v2.x.1 §4 row-198 forward-binding pattern.

## §12. Threat-model boundaries (v0.1 hook posture)

The amendment's stated severity is **LOW at v0.1 hook** because:

- No reflection_agent constructed at v0.1 hook (per architecture v7.0.9 §9.1 scope).
- No Reflection cadence invoked at v0.1 hook.
- 8 BINDING predicate bodies raise NotImplementedError if anything ever called them.
- 8 HORIZON + 1 PROBE-DEPENDENT predicate bodies are `pass` no-ops if anything ever called them (but nothing calls them at v0.1 hook).
- 5 F-ARCHIVIST-\* sub-tag extensions inherit parent gate enforcement that is already live at §4 v2.x WS-L LOCK rows 193/194 — sub-tags fire only when the parent gate fires, and reflection-attributable sub-tags don't fire if no reflection invocation happens.
- F-REFLECTION-COVERAGE-INCOMPLETE META-gate has live body that FAIL_CLOSED at any cycle attempting Reflection cadence with un-realized BINDING bodies — the dormant-binding lever per architecture v7.0.9 §5.

Three-stage progression:

- **v0.1 + v0.2 single-operator Beta deployment** (current): predicate-signature layer only. No runtime invocation surface. v0.1 Beta does not invoke Reflection cadence at all; v0.2 SPEC promotes HORIZON to signature-present but still no runtime invocation (matches §13 / §14 / §15 v0.2 SPEC-ONLY discipline).

- **v1.x first-ship**: predicate bodies realize. Reflection_agent constructed. Cadence invokable. F-REFLECTION-COVERAGE-INCOMPLETE clears (BINDING bodies realized). Threat model promotes to MED because real runtime invocation introduces real attack surface (per Lane 5 field-failure forensics — Replit auto-delete + Tay corpus poisoning + ChatGPT memory injection + Reflexion confirmation bias all materialize at runtime, not at signature layer).

- **v2 multi-tenant** (Section O.5 horizon): promotes to HIGH because cross-tenant signal leak surfaces emerge (per Lane 5 F-14 UCC default failure mode). Section O.5 v2 multi-tenant amendment author must verify §4 v2.x.2 LOCK + v1.x BINDING bodies + the sub-tag extensions retain semantic-equivalence under multi-tenant routing before declaring §15 + Reflection hardened for v2 deployment.

## §13. Acceptance criterion (closes architecture v7.0.9 §2 commitment)

§4 v2.x.2 LOCK ceremony asserts each criterion independently:

1. **17 top-level predicate signatures present.** Test introspection at `test_<code>_predicate_signature_present` across all 17 F-REFLECTION-\* codes.
2. **8 BINDING bodies raise NotImplementedError.** Test introspection at `test_<code>_predicate_body_raises_not_implemented_error` across the 7 NotImplementedError-bodied BINDING (excluding F-REFLECTION-COVERAGE-INCOMPLETE which has live body).
3. **9 HORIZON + PROBE-DEPENDENT bodies are signature-only `pass` no-ops.** Test introspection at `test_<code>_signature_only_no_body` across all 9.
4. **F-REFLECTION-COVERAGE-INCOMPLETE META-gate live and fires.** Test introspection at `test_coverage_incomplete_meta_gate_fires_on_missing_binding_body`.
5. **5 F-ARCHIVIST-\* sub-tag entries present.** Test introspection at `test_<sub_tag>_present_in_parent_FORBIDDEN_SUB_TAGS` across all 5.
6. **GroundingSignalClass enum + frozenset constants.** Tests at `test_grounding_signal_class_enum_has_8_members` + `test_primary_eligible_classes_frozenset_membership` + `test_llm_eval_only_classes_frozenset_membership`.
7. **Inoculation frame body verbatim + digest stable.** Tests at `test_inoculation_frame_body_v1_digest_stable` + `test_inoculation_frame_body_v1_verbatim_against_v7_0_9_section_7`.
8. **Probe registry narrowed to three families.** Test at `test_required_probe_families_tuple_matches_v7_0_9_section_6`.
9. **`loop_divergence_probes` not referenced anywhere.** Test at `test_no_predicate_has_loop_divergence_probes_dependency`.
10. **Tier sets disjoint + complete coverage.** Test at `test_binding_horizon_probe_dependent_tier_disjoint`.
11. **§11 v1.x amendment-realization checklist binding.** This §11 enumerates the 7 drift-test files + named function names + assertion forms. Cross-reference back from v1.x amendment frontmatter is a hard prerequisite for v1.x LOCK.

## §14. Cross-references

- Parent §4 v2.x LOCK: `pipeline/blueprint/v0.1/section_04_v2_x_amendment.md` (rows 193/194; LOCKED 2026-05-10).
- Sub-tag-extension precedent: `pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md` (row 198/199; LOCKED 2026-05-10).
- Companion §15 v1 SPEC LOCK (parent of F-ARCHIVIST-\* family): `pipeline/blueprint/v0.1/section_15_archivist.md` (rows 191/192; LOCKED 2026-05-10).
- Architecture commitment: `pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md` §2 (paired-commit sibling — registers the F-REFLECTION-\* primitives at architectural-primitive layer).
- §0.5 paired-commit sibling: `pipeline/blueprint/v0.1/section_00_5_section_15_reflection_amendment.md` (interface-index row append).
- Audit trail (this round): `pipeline/validation/reflection_v0_1_hook_thesis_2026-05-10/`.

## §15. Bounded findings + deferred dispositions (Cycle-1 row-170 transparent pattern)

Per L-005 strict two-cycle CLOSED with FULL live cross-family rigor (audit trail at `pipeline/validation/reflection_v0_1_hook_thesis_2026-05-10/`). Cycle 1 Red Team surfaced 16 probes (4 BLOCKING + 6 HIGH + 4 MED + 2 LOW). Cycle 2 verified disposition outcomes:

### §15.1 FOLDED-IN-AT-LOCK (11 — narrow text edits applied at this ceremony)

| Cycle-1 ID | Severity at Cycle 1 | Disposition | Landing |
|---|---|---|---|
| RT-04 | BLOCKING | CLOSED | Architecture v7.0.9 §7 exact-match-semantics + this amendment §3 row 5 `exact_match: bool = True` default kwarg + §11 v1.x amendment-realization checklist + skeleton predicate updated. |
| RT-05 | BLOCKING | CLOSED | Architecture v7.0.9 §5.1 META-gate body preservation contract; this amendment §13 acceptance criterion #11. No META-META gate (matches F-CLASS-COVERAGE-INCOMPLETE precedent). |
| RT-11 | BLOCKING | CLOSED | §0.5 §15.x §G single-commit atomicity contract + forward-binding interpretation for prior compound-LOCKs. |
| RT-01-C | HIGH | CLOSED | Architecture v7.0.9 §3 monotonic-`run_id` binding + this amendment §5 cross-reference + v7.0.4-M1 audit-log monotonic-counter pattern. |
| RT-03 | HIGH | CLOSED | This amendment §11 v1.x amendment-realization checklist row 2 explicit disjoint-set check + named drift-test. |
| RT-06 | HIGH | CLOSED | This amendment §11 row 7 transaction-id binding + cryptographic checkpoint + named drift-test. |
| RT-08 | HIGH | CLOSED | Architecture v7.0.9 §6.1 REQUIRED_PROBE_FAMILIES immutability contract + 3 new skeleton tests (immutable + tuple-not-list + no-loop-divergence). |
| RT-10 | HIGH | CLOSED | Architecture v7.0.9 §9.3 no-router-policy-reuse-for-F-REFLECTION-* binding + §10 explicit non-goal. |
| RT-09 | MEDIUM | CLOSED | Architecture v7.0.9 §8.3 external-naming lint promotion to v0.2 SPEC deliverable. |
| NP-02 | MEDIUM | CLOSED | 4 new skeleton tests: signature-matches-table + exact_match-default + expected_digest-binding + required_families-binding. |
| NP-04 | MEDIUM | CLOSED | This amendment §11 row 8 HORIZON probe-coverage enforcement contract + named drift-test. |

### §15.2 BOUNDED-by-v7-LOCKED-A1+A4 (5 — no text edit; documented bounded interpretation)

| Cycle-1 ID | Severity | Bounded by |
|---|---|---|
| RT-01-A | BLOCKING-at-Cycle-1 / BOUNDED-LOW-at-LOCK | v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight). Dynamic-dispatch sub-tag bypass class. Same as §4 v2.x.1 §11.1 row 198 precedent. v2 Section O.5 multi-tenant promotion path. |
| RT-01-B | HIGH-at-Cycle-1 / BOUNDED-LOW-at-LOCK | v7 LOCKED A4. NER adversarial-robustness class. Same as §15 v1 LOCK §11.1 NF-04 precedent. v2+ adds LLM-based semantic-leak detector. |
| RT-07 | MEDIUM | BT9 hash-chain integrity + repo permissions. v2 Section O.5 multi-tenant promotion adds per-entry gate-signature binding. |
| NP-01 | HIGH-at-Cycle-1 / BOUNDED-LOW-at-LOCK | Source-code integrity enforced by paired-commit + lock_history + cross-family Thesis. JSON-manifest enum is v0.2 SPEC deliverable per architecture v7.0.9 §8.3 RT-09 fold-in. |
| NP-05 | HIGH-at-Cycle-1 / BOUNDED-LOW-at-LOCK | Single-process import discipline at v0.1+v0.2; reflection_agent is single-instance per Archivist cadence invocation. v2 Section O.5 may add MappingProxyType-style immutability check. |

### §15.3 REJECTED-with-rationale (1 — premise contradicts architectural commitment)

| Cycle-1 ID | Severity | Rejection rationale |
|---|---|---|
| RT-02 | HIGH | Premise contradicts v7.0.7 §1 + synthesis §5.2 + architecture v7.0.9 §1 (reflection_agent always-local). F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL (v7.0.7 §5.1) catches any payload crossing the cloud boundary. The probe assumes a cloud-routed reflection_agent that does not exist in the architectural commitment. REJECTED — row-170 precedent applies when premise contradicts LOCKED text (mirrors §4 v2.x.1 §11.3 RT-13 + §13 Cycle-2 RT-C2-04 + §4 v2.x Cycle-2 RT-04/05 REJECTED-with-rationale dispositions). Cycle 2 verification MAINTAINED. |

### §15.4 Cycle 2 verification outcome

- **Editor (Llama-3.3-70B / Groq, Meta family):** READY_TO_LOCK — all Cycle-1 findings CLOSED; no new findings.
- **Judge (Gemini-2.5-Pro / Google):** READY_TO_LOCK at 100/100 (+1 from Cycle 1 99/100) — J-01 CLOSED; Lane 3 dimension restored to 10/10.
- **Red Team (GPT-OSS-120B / Groq, OpenAI-OSS family):** READY_TO_LOCK — all 11 FOLDED items dispositioned CLOSED; all 5 BOUNDED MAINTAINED; 1 REJECTED MAINTAINED; no new Cycle-2 probes.

**UNANIMOUS READY_TO_LOCK at Cycle 2 close.** L-005 strict two-cycle CLOSED. No third round invoked.

## Appendix A — Predicate signature table (single source of truth)

The on-disk single source of truth lives in `pipeline/logician/gates/reflection_gates.py`. Reproduced here for reading-surface coherence with architecture v7.0.9 §2 — drift between the file and this table is itself a §4 v2.x.2 defect and the file is canonical.

Function names + their tier label:

```python
# BINDING (8 — NotImplementedError bodies at v0.1 hook except META-gate which is ACTIVE)
predicate_no_external_signal              # BINDING — NotImplementedError
predicate_eval_only_grounded              # BINDING — NotImplementedError
predicate_insufficient_evidence           # BINDING — NotImplementedError
predicate_rfa_spec_override               # BINDING — NotImplementedError
predicate_depth_exceeded                  # BINDING — NotImplementedError
predicate_self_evaluator_family_clash     # BINDING — NotImplementedError
predicate_write_without_commit            # BINDING — NotImplementedError
predicate_coverage_incomplete             # BINDING — ACTIVE body (META-gate dormant-binding lever)

# HORIZON (8 — signature-only `pass` bodies at v0.1 hook)
predicate_intent_anchor_drift             # HORIZON — pass
predicate_content_loop_detected           # HORIZON — pass
predicate_eval_surrogate_divergence       # HORIZON — pass
predicate_operator_override_mask          # HORIZON — pass
predicate_inoculation_frame_missing       # HORIZON — pass
predicate_self_reported_confidence        # HORIZON — pass
predicate_fabrication_on_failure          # HORIZON — pass
predicate_probe_coverage_incomplete       # HORIZON — pass

# PROBE-DEPENDENT (1 — signature-only `pass` body at v0.1 hook)
predicate_sycophancy_loop_detected        # PROBE-DEPENDENT — pass
```

Sub-tag extensions (5 — additive entries in parent gate FORBIDDEN_SUB_TAGS tables; no top-level predicate):

```python
# In pipeline/logician/gates/archivist_gates.py FORBIDDEN_SUB_TAGS tables:
#   F-ARCHIVIST-CROSS-ORG-LEAK             += {"reflection_cross_org_read"}
#   F-ARCHIVIST-AUTO-APPLY-ATTEMPTED       += {"reflection_attach_unsigned"}
#   F-ARCHIVIST-LESSON-INSTANCE-LEAK       += {"reflection_instance_in_pattern_field"}
#   F-ARCHIVIST-CADENCE-DRIFT              += {"reflection_interval_drift"}
#   F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT  += {"reflection_evidence_out_of_run"}
```

# End of amendment
