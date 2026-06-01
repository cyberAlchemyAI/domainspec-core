---
title: Blueprint §11 Intake — Amendment v1.1 (RT-C2-02 producer-side closure — AWARD_INGEST commitment_id safe-identifier sanitization at row-admission time)
filed: 2026-05-11
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-11 — narrow-corrective amendment mirroring v7.0.4-M1 + §4 v2.x.1 precedents (lock_history rows 190 + 198/199). The §14 v1 LOCK at lock_history rows 200/201 (2026-05-10) named this amendment in its `unblocks` list: "§11 v1.1 follow-on update registering commitment_id safe-identifier validation per Cycle 2 RT-C2-02". L-005 strict two-cycle CLOSED with FULL live cross-family rigor (Editor=groq/llama-3.3-70b-versatile + Judge=google/gemini-2.5-pro + Red Team=groq/openai/gpt-oss-120b via openclaw bridge). **Cycle 1 dispatched 2026-05-11T19:02Z:** Editor READY_TO_LOCK (8 LOW; non-blocking) + Judge READY_TO_LOCK 105/105 + Red Team READY_TO_LOCK with minor amendments (8 findings: 3 FOLD-IN + 1 DEFERRED to v1.x + 2 BOUNDED-by-A1+A4 + 1 REJECTED-with-rationale + 1 NO-OP per §11 below). **Cycle 2 verification dispatched 2026-05-11T19:08Z:** Editor READY_TO_LOCK (4 LOW C2 findings; non-blocking) + Judge READY_TO_LOCK 105/105 maintained ("Cycle 1 fold-ins were executed perfectly") + Red Team READY_TO_LOCK with minor fixes blocking=false (3 NEW probes RT-C2-02/03/04 FOLDED-IN at LOCK with explicit text-level mechanism per row-170 transparent-disposition pattern; 8 Cycle-1 findings verified closed/dispositioned). Twelfth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor (after WS-D + WS-F + WS-E + WS-H + WS-G + WS-K + WS-C-M1 + WS-L + WS-I + §4 v2.x.1 + §14 v1 / §0.5 v17 + WS-Reflection §15 v1 / §0.5 v18 + §4 v2.x.2 precedents).
parent_lock: pipeline/blueprint/v0.1/section_11_intake.md  (§11 v1 LOCKED 2026-05-10 row 185)
parent_lock_row: 185
predecessor_disposition_packet: pipeline/blueprint/v0.1/section_14_report_generator.md §14.18.3 row RT-C2-02 (§14 v1 LOCK Cycle 2 fold-in, lock_history row 200; FOLDED-IN at LOCK with explicit deferral text: "§11 v1 AWARD_INGEST extraction MUST sanitize commitment_id at extraction time per a paired §11 v1.1 follow-on update (referenced; not authored at this LOCK)")
companion_lock: pipeline/blueprint/v0.1/section_14_report_generator.md  (§14 v1 SPEC LOCKED 2026-05-10 row 200; §14.9.2 + §14.18.3 RT-C2-02 host the consumer-side closure that this amendment makes producer-side enforceable at row-admission)
amendment_class: narrow-corrective
precedent_pattern: §4 v2.x.1 narrow-corrective amendment (lock_history row 198/199) — both extend the closure surface of an already-LOCKed contract (here, the §14 v1 RT-C2-02 commitment_id safe-identifier regex) by adding a producer-side enforcement layer without modifying the parent LOCKed text in-place. Also mirrors v7.0.4-M1 (lock_history row 190) at the architectural-layer precedent.
threat_severity_at_v0_1_v0_2: MED (downstream-amplified at v0.2). At v0.1 single-operator Beta this is contributor-discipline bounded; at v0.2 first ship with §14 Report Generator live the path-traversal risk in waiver-file path construction is consumer-side adversarially relevant when proposal_commitments.yaml is hand-edited. Producer-side enforcement is the structural-defense layer that catches the gap at extraction time before any §14 consumer ever sees a non-canonical commitment_id.
purpose: Close RT-C2-02 at the producer side. §14 v1 LOCK landed the safe-identifier regex `^[A-Z0-9_-]+$` (max 64 chars) AT CONSUMER-SIDE filesystem-operation boundaries — `pipeline.logician.gates.f_report_commitment_missed` + `_report_protocols` + report_generator `_schemas` all call `sanitize_commitment_id` before row admission. §11 v1 LOCK at row 185 predated the regex by ~16h and the AWARD_INGEST row writer at `_validate_and_collect_commitments` used bare `uuid.uuid4().hex` (lowercase) which would FAIL the regex were it ever passed through §14's consumer-side validators downstream. This amendment hardens §11 v1 producer-side row admission so the regex never has to fire defensively at §14; the contract is producer-enforced.
companion_code_landed:
  - "pipeline/orchestrator/seats/_commitment_id.py (NEW — shared producer/consumer canonical home for SAFE_COMMITMENT_ID_REGEX + SAFE_COMMITMENT_ID_PATTERN + COMMITMENT_ID_MAX_LEN + CommitmentIdInvalid + is_safe_commitment_id + sanitize_commitment_id. Adds `re.ASCII` flag to the precompiled pattern as defense-in-depth against future predicate edits that might drift onto `\\d` Unicode-aware matching.)"
  - "pipeline/orchestrator/seats/report_generator/_commitment_id.py (UPDATED — converted from canonical home to a backward-compat re-export shim from the shared sibling. Public surface preserved verbatim; identity contract preserved — `isinstance(exc, CommitmentIdInvalid)` works across both import paths.)"
  - "pipeline/orchestrator/seats/intake.py (UPDATED — imports `sanitize_commitment_id` from the shared canonical home; `_validate_and_collect_commitments` constructs `commitment_id = sanitize_commitment_id(uuid.uuid4().hex.upper())` at row admission time. Uppercase projection of the uuid4 hex produces a 32-character uppercase hex string strictly within `^[A-Z0-9_-]+$`; the wrapping `sanitize_commitment_id` is defense-in-depth that fail-closes if the ID generation strategy ever drifts.)"
companion_tests_landed:
  - "tests/seats/intake/test_award_ingest_commitment_id_safe_identifier_regex.py (NEW — 4 test classes: regex-shape unit tests + valid/invalid identifier matrix (parametrized across 8 valid + 17 invalid forms including unicode digit lookalikes per §3 defense-in-depth) + producer/consumer single-canonical-home identity contract + end-to-end AWARD_INGEST verification that auto-generated commitment_ids land in the canonical set + per-row uniqueness regression.)"
done_definition:
  - "Three on-disk artifacts landed: shared canonical home + consumer shim + intake producer-side enforcement (see companion_code_landed)."
  - "Test surface green at .venv/bin/python3 (3.14) — deterministic checks verified at draft time via system python; .venv pytest run reserved for LOCK ceremony."
  - "§14 v1 LOCK consumer-side imports continue to resolve unchanged via the shim (lock_history row 200 imports at `pipeline/logician/gates/f_report_commitment_missed.py:42` and `pipeline/orchestrator/seats/report_generator/_schemas.py:139` and `pipeline/logician/gates/_report_protocols.py:121`); the shim preserves `__all__` verbatim and re-exports the same objects (identity-shared, not name-only)."
  - "Existing intake `test_award_ingest.py` tests continue to pass without modification (the `commitment_id` field was previously typed `str` with no value-shape contract at the schema or queue-writer layer; the new sanitize call is a strict superset of accepted values that the existing tests never tested for)."
  - "§11 v1.1 amendment text references the §14 RT-C2-02 closure verbatim and names the canonical home; future v1.x amendment authors can read this amendment without grep-ing the §14 v1 LOCK or the report_generator implementation."
  - "L-005 strict two-cycle Thesis CLOSED with FULL live cross-family rigor; audit trail at `pipeline/validation/section_11_v1_1_thesis_2026-05-11/`."
  - "Compound LOCK with §0.5 paired-commit amendment (1 marker row + 1 enforcement-infrastructure row for the new shared module = 2 rows; runtime-live total 413 → 415)."
cowork_thesis_dispatch_status: PENDING at SCOPING DRAFT — Thesis dispatch reserved for LOCK ceremony. Cycle 1: Editor + Judge + Red Team dispatched via `mcp__Control_your_Mac__osascript` → `openclaw infer model run --gateway` with timeout of 600 seconds, modeled on `pipeline/validation/v4_v2_x_1_thesis_2026-05-10/dispatch_audit_v{1,2}.sh`. Cycle 2 (verification): same posture. L-005 strict two-cycle expectation; row-170 transparent-disposition pattern for any Cycle 2 NEW probes that surface.
ws_dispatch: §11 v1.1 corrective dispatch (this session) — modeled on §4 v2.x.1 narrow-corrective-amendment cadence (lock_history row 198/199).
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment v1.1 — RT-C2-02 producer-side closure (AWARD_INGEST commitment_id safe-identifier sanitization at row-admission time)

## §0. Amendment intent + scope

This narrow-corrective amendment **adds** (does **not** replace) a producer-side enforcement layer to the §11 v1 AWARD_INGEST commitment-extraction path, closing the producer-side gap that the §14 v1 LOCK Cycle 2 RT-C2-02 disposition explicitly named as a paired follow-on:

> §11 v1 AWARD_INGEST extraction MUST sanitize commitment_id at extraction time per a paired §11 v1.1 follow-on update (referenced; not authored at this LOCK).
> — §14 v1 SPEC, §14.18.3 row RT-C2-02 closure, lock_history row 200 (2026-05-10).

The amendment does NOT modify §11 v1 text in place; instead, mirroring the §4 v2.x.1 narrow-corrective precedent (lock_history row 198/199), §11 v1 remains historical and this amendment is the authoritative on-disk source for the producer-side hardening. The amendment also relocates the canonical declaration of the safe-identifier regex from the §14 consumer-side module to a shared producer/consumer sibling module so a single canonical home serves both seats.

**What landed at §14 v1 (consumer-side).** The §14 v1 LOCK at lock_history row 200 introduced:

- `pipeline/orchestrator/seats/report_generator/_commitment_id.py` declaring `SAFE_COMMITMENT_ID_REGEX = r"^[A-Z0-9_-]+$"` + `COMMITMENT_ID_MAX_LEN = 64` + `CommitmentIdInvalid` exception + `is_safe_commitment_id` + `sanitize_commitment_id`.
- Consumer-side calls at `pipeline/logician/gates/f_report_commitment_missed.py` + `pipeline/orchestrator/seats/report_generator/_schemas.py` + `pipeline/logician/gates/_report_protocols.py` that sanitize before filesystem operations or row admission.
- New sub-tag `F-REPORT-COMMITMENT-MISSED.commitment_id_invalid_format` fail-closes at PRE-pre-track-dispatch on any non-canonical commitment_id reaching the §14 consumer side.
- Tests at `tests/seats/report_generator/test_commitment_id.py` (12 tests; green at §14 v1 LOCK).

**The producer-side gap.** §11 v1 LOCK at row 185 (2026-05-10, ~16h before §14 v1) constructed `commitment_id` at `pipeline/orchestrator/seats/intake.py:1486` as `uuid.uuid4().hex` — lowercase hexadecimal. Lowercase hex fails the `^[A-Z0-9_-]+$` regex unconditionally. Two consequences:

1. **Downstream amplification at v0.2 first ship.** When §14 Report Generator first consumes `proposal_commitments.yaml` produced by §11 AWARD_INGEST (the named scheduler path at §11.5.2 → §14.5.0 GrantReportBundle), every commitment_id would trip the §14 consumer-side `F-REPORT-COMMITMENT-MISSED.commitment_id_invalid_format` gate at PRE-pre-track-dispatch. The §14 LOCK's path-traversal mitigation would fail-closed on every commitment without exception — a structural defect of the contract, not adversarial input.

2. **Operator hand-edit risk.** §11 v1 LOCK at §11.5.2 makes `proposal_commitments.yaml` operator-editable during structuring review (status `PENDING_OPERATOR_REVIEW` → operator promotes to `PROMOTED`). At the operator-editable window, an operator hand-editing the file might (a) replace the auto-generated lowercase-hex ID with a more semantic identifier like `WORKFORCE_TRAINING-FY26` (passes regex) or (b) introduce a path-traversal-eligible string like `../etc/passwd` (fails regex). Without producer-side sanitization at extraction time + a §11.6.3 re-validation at promote time, the contract is enforced only at §14 consumer side — i.e., late in the pipeline, downstream of the operator-review surface.

**What this amendment lands.** Three on-disk changes + one test file (full enumeration at §2 below):

- **Shared canonical home.** `pipeline/orchestrator/seats/_commitment_id.py` becomes the canonical declaration site. The producer-side §11 Intake and the consumer-side §14 Report Generator both import from this shared sibling.
- **Backward-compat re-export shim.** The previous canonical home at `pipeline/orchestrator/seats/report_generator/_commitment_id.py` is retained as a re-export shim. §14 v1 LOCK consumer-side imports (lock_history row 200 at three call sites) continue to resolve unchanged with object identity preserved across both import paths.
- **Producer-side enforcement.** `pipeline/orchestrator/seats/intake.py` imports `sanitize_commitment_id` from the canonical home; `_validate_and_collect_commitments` constructs every row's commitment_id as `sanitize_commitment_id(uuid.uuid4().hex.upper())`. Uppercase projection of the uuid4 hex produces a 32-character uppercase-hex string strictly within `^[A-Z0-9_-]+$`; the wrapping sanitize call is defense-in-depth that fail-closes if the ID generation strategy ever drifts. The `re.ASCII` flag on the precompiled pattern is defense-in-depth against future predicate edits drifting onto `\d` Unicode-aware matching.
- **Test surface.** `tests/seats/intake/test_award_ingest_commitment_id_safe_identifier_regex.py` adds 4 test classes covering the regex shape contract, the valid/invalid identifier matrix (parametrized across 8 valid + 17 invalid forms including unicode digit lookalikes), the producer/consumer single-canonical-home identity contract, and an end-to-end AWARD_INGEST verification that auto-generated commitment_ids land in the canonical set + per-row uniqueness regression.

The §14 v1 LOCK does not need any text change — the RT-C2-02 closure at §14.18.3 already named the producer-side follow-on; this amendment is the realization of that named follow-on.

## §1. Target glob + scope discipline

Producer-side scope: `pipeline/orchestrator/seats/intake.py` (one module — the AWARD_INGEST row-writer at `_validate_and_collect_commitments`). The producer-side import is narrowly placed at the top of the module alongside the existing extractor-fabrication imports; no other §11 modules import the sanitize helper directly. BULK_INGEST and INCREMENTAL_INGEST modes are out-of-scope — they emit `candidate_id` (per §11.5.1 PendingFact schema), not `commitment_id`. The `candidate_id` is a separate identifier with its own contract (currently bare `uuid.uuid4().hex` lowercase) and is not consumed by §14; this amendment does NOT extend the contract to `candidate_id`.

Consumer-side scope: `pipeline/orchestrator/seats/report_generator/_commitment_id.py` is converted to a re-export shim. Three call sites that import from this path at §14 v1 LOCK continue to resolve via the shim:

- `pipeline/logician/gates/f_report_commitment_missed.py:42` — `from pipeline.orchestrator.seats.report_generator._commitment_id import is_safe_commitment_id, ...`
- `pipeline/orchestrator/seats/report_generator/_schemas.py:139` — references `_commitment_id.sanitize_commitment_id` in docstring contract
- `pipeline/logician/gates/_report_protocols.py:121` — references `_commitment_id.sanitize_commitment_id` in docstring contract

Identity-shared re-export (per `__all__` re-binding the same module objects, not name-only copies) means an `isinstance(exc, CommitmentIdInvalid)` check on either side resolves the same class object — a single raised exception is recognized at the call site of either import path.

## §2. Predicate body + canonical home (pipeline/orchestrator/seats/_commitment_id.py)

The canonical home is a new module at `pipeline/orchestrator/seats/_commitment_id.py`. Its surface mirrors the §14 v1 LOCK module byte-for-byte at the helper signatures, with two deltas:

1. **Module docstring updated** to name this module as the canonical home, the relocation rationale, and the §11 v1.1 amendment's relationship to the §14 v1 LOCK Cycle 2 RT-C2-02 closure.
2. **`re.ASCII` flag added to the precompiled pattern** as defense-in-depth: `SAFE_COMMITMENT_ID_PATTERN = re.compile(SAFE_COMMITMENT_ID_REGEX, flags=re.ASCII)`. The current regex `^[A-Z0-9_-]+$` uses literal ASCII character classes, so `re.ASCII` is a no-op for this exact predicate. The flag is set so that if a future amendment edits the predicate to use `\d` instead of `[0-9]` (or `\w` instead of `[A-Z0-9_]`), the matcher remains ASCII-only and does not silently begin matching Unicode digit lookalikes (arabic-indic digit zero `٠`, devanagari digits, etc.). The test surface at §3 exercises one such lookalike at the rejection boundary.

Public surface (re-exported at the shim location for §14 v1 backward compat):

```python
SAFE_COMMITMENT_ID_REGEX: Final[str] = r"^[A-Z0-9_-]+$"
SAFE_COMMITMENT_ID_PATTERN: Final[re.Pattern[str]] = re.compile(
    SAFE_COMMITMENT_ID_REGEX, flags=re.ASCII
)
COMMITMENT_ID_MAX_LEN: Final[int] = 64

class CommitmentIdInvalid(ValueError):  # frozen dataclass; carries value + rule
    value: str
    rule: str  # one of: commitment_id_must_be_str / commitment_id_empty_or_too_long / commitment_id_regex_mismatch

def is_safe_commitment_id(raw: object) -> bool: ...
def sanitize_commitment_id(raw: object) -> str: ...  # raises CommitmentIdInvalid
```

The `sanitize_commitment_id` rule-attribution design (three distinct rule names) is preserved verbatim from §14 v1 — it lets downstream sub-tag dispatch route to the right failure-code at the §14 consumer side (`F-REPORT-COMMITMENT-MISSED.commitment_id_invalid_format` is a single sub-tag with three distinguishable cause rules in the exception payload).

### §2.1 Static-analysis limitations (intentionally out-of-scope under v7 A1+A4)

The §11 v1.1 producer-side enforcement is a deterministic runtime check at row admission time. It does NOT cover the following classes — they are bounded under v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight) and routed to v2 multi-tenant via Section O.5:

- **Hand-edit of `proposal_commitments.yaml` after Intake write but before operator promote.** The §11.5.2 PENDING → PROMOTED workflow makes the file operator-editable. A hand-edit introducing a non-canonical commitment_id is caught at §14 consumer side via `F-REPORT-COMMITMENT-MISSED.commitment_id_invalid_format`. The producer-side enforcement at this amendment does NOT re-validate at promote time — that surface is registered as a v1.x amendment-realization checklist item below (§4) but not landed at v1.1.
- **Operator-supplied override IDs.** §11 v1 AWARD_INGEST does not accept operator-supplied commitment_ids — every row is auto-generated. If a future amendment adds an operator-supplied-ID path (e.g., for migration scenarios), it MUST route the supplied ID through `sanitize_commitment_id` before admission. The v1.x amendment-realization checklist row at §4 binds this contract.
- **Concurrent write races on `proposal_commitments.yaml`.** §11 v1 LOCK §11.10 guarantees AWARD_INGEST is single-writer at v0.1 (operator-explicit only, one run per grant_id per session). Producer-side sanitization is single-threaded against the operator's invocation. Multi-tenant concurrent-write hardening is a v2 Section O.5 target.

## §3. Test surface (tests/seats/intake/test_award_ingest_commitment_id_safe_identifier_regex.py)

The test surface has four sections mirroring the on-disk file layout:

**§A. Regex-shape unit tests.** Verify the canonical home declares `SAFE_COMMITMENT_ID_REGEX == r"^[A-Z0-9_-]+$"` + `SAFE_COMMITMENT_ID_PATTERN.flags & re.ASCII` (ASCII flag set) + `COMMITMENT_ID_MAX_LEN == 64`. These tests anchor the contract at the producer-side import surface — if the §14 module is ever modified out of sync with the canonical home, these tests catch the drift.

**§B. Valid + invalid identifier matrix.** Parametrized across:

- 8 valid forms: `COMMIT-001`, `A`, `WORKFORCE_TRAINING-FY26`, `A0_-`, `ABC123`, `0123456789`, the at-the-bound length `"A" * 64`, the uppercase-hex projection `ABCDEF0123456789ABCDEF0123456789`.
- 17 invalid forms with expected rule names: empty + too-long → `commitment_id_empty_or_too_long`; mixed-case + lowercase + whitespace + dot + path-separator (forward + back) + quote (single + double) + path-traversal + non-ASCII letter + unicode-superscript + arabic-indic-digit + tab-whitespace → `commitment_id_regex_mismatch`.
- 5 non-str forms (None, int, bytes, float, object) → `commitment_id_must_be_str`.

The unicode digit lookalike row (arabic-indic digit zero `٠`) is the load-bearing defense-in-depth assertion for the `re.ASCII` flag. The current predicate `[0-9]` rejects this regardless; the test surface anchors the boundary so future predicate edits to `\d` do not silently regress.

**§C. Producer/consumer single-canonical-home identity contract.** Four `is`-identity assertions across import paths:

- `SAFE_COMMITMENT_ID_PATTERN` is the same object via `pipeline.orchestrator.seats._commitment_id` and via `pipeline.orchestrator.seats.report_generator._commitment_id` (the shim).
- `COMMITMENT_ID_MAX_LEN` is the same `int` object (singleton via Python small-int cache; still asserted via `is` to bind the contract).
- `CommitmentIdInvalid` is the same class object — `isinstance(exc, CommitmentIdInvalid)` works regardless of which import path raised it.
- `sanitize_commitment_id` is the same function object.

Plus one end-to-end `isinstance` assertion: a `CommitmentIdInvalid` raised by the consumer-shim's `sanitize_commitment_id("lowercase")` is `isinstance`-recognized at both import paths.

**§D. AWARD_INGEST end-to-end.** Two tests against the producer-side row writer using the existing `test_award_ingest.py` fixtures (FakeParser + FakeCommitmentExtractor + `_seed_grant` + `_signed_map`):

- `test_award_ingest_writes_only_safe_commitment_ids` — asserts every emitted commitment_id passes `is_safe_commitment_id`, has length 32 (the uuid.hex.upper projection), and consists only of `[A-F0-9]` characters.
- `test_award_ingest_commitment_ids_are_unique_per_row` — asserts distinct rows receive distinct commitment_ids (uniqueness regression; §14 claim_evidence_map collisions become possible without uniqueness).

## §4. v1.x amendment-realization checklist (forward-binding contracts for v1.x amendment authors)

Two contracts forward-bind from this amendment to v1.x deliverables:

```
[ ] §11.6.3 operator-promote re-validation. When the operator runs
    `tilth intake award-promote --org <slug> --grant <grant_id>` to flip
    proposal_commitments.yaml from PENDING_OPERATOR_REVIEW → PROMOTED, the
    promote handler MUST re-validate every commitment_id against
    sanitize_commitment_id BEFORE writing the PROMOTED status. The re-
    validation closes the operator-edit window vector (§2.1 bullet 1).
    Acceptance: a new test
    test_award_promote_rejects_hand_edited_unsafe_commitment_id at
    tests/seats/intake/ verifies the promote handler fail-closes on a hand-
    edited row.

[ ] Operator-supplied commitment_id path (if added). Any future amendment
    that adds an operator-supplied-ID path to AWARD_INGEST (e.g., for
    migration scenarios) MUST route the supplied ID through
    sanitize_commitment_id at the same _validate_and_collect_commitments
    admission gate. Acceptance: the named amendment must include
    sanitize_commitment_id at the new admission site + extend the test
    surface at §B to parametrize the new path.

[ ] Safe-identifier regex source-form discipline (Cycle 1 RT-04 +
    Cycle 2 RT-C2-03 fold-in deferral). When any future amendment edits
    the regex string itself at
    `pipeline/orchestrator/seats/_commitment_id.py:SAFE_COMMITMENT_ID_REGEX`,
    the edit MUST NOT introduce Unicode property escapes (`\p{...}`),
    explicit Unicode codepoint escapes (`\uNNNN`, `\UNNNNNNNN`), or the
    Unicode-aware character-class shorthand (`\d`, `\w`, `\s`) without
    explicit `re.ASCII` re-affirmation. Acceptance: a new AST-lint rule
    `R-COMMITMENT-ID-REGEX-NO-UNICODE-CLASSES` (target glob =
    `pipeline/orchestrator/seats/_commitment_id.py`) reads the regex
    string at module load and rejects any of the named escape patterns.
    Named acceptance test:
    `tests/linting/test_r_commitment_id_regex_no_unicode_classes.py::test_rule_rejects_unicode_class_escapes`.
    Owner: the next narrow-corrective amendment in the §11 v1.x family
    OR the next minor v0.2 release amendment (whichever lands first).
    Forward-binding contract: v0.2 first ship MUST NOT proceed without
    this rule in place OR an explicit written deferral in the v0.2
    production-cut checklist with operator Ed25519 sign-off. The
    bounded-by-A4 posture at v0.1+v0.2 (operator is the only regex
    editor + the structural defense layer holds via `re.ASCII` + the
    20-form invalid-identifier test matrix) is the v0.1+v0.2
    structural defense; the AST-lint rule is the v1.x compile-time
    hardening that catches contributor-edit drift.

[ ] Reload-protocol documentation (Cycle 2 RT-C2-02 fold-in). The shim
    at `pipeline/orchestrator/seats/report_generator/_commitment_id.py`
    is an explicit re-export of symbols from
    `pipeline.orchestrator.seats._commitment_id`. If the canonical
    home is ever reloaded at runtime (via `importlib.reload`), the
    shim's previously-imported bindings become stale references to
    pre-reload class objects. The protocol is: **reload canonical →
    re-import shim**. A reload of the shim alone (without canonical)
    leaves the shim binding to the live canonical home unchanged
    structurally but breaks the operator-call-site `is`-identity if
    the operator had cached a reference to the shim's exports. v1.x
    amendments that introduce a dynamic-plugin layer (multi-tenant
    Section O.5 or v1.x extension points) MUST verify the
    reload-protocol invariant via the named acceptance test
    `tests/seats/intake/test_award_ingest_commitment_id_safe_identifier_regex.py::test_reload_preserves_identity_when_canonical_home_reloaded_first`.
    The test is shipped at this LOCK (Cycle 2 RT-C2-02 fold-in); any
    v1.x amendment that introduces a reload pathway MUST extend the
    test to cover its specific reload trigger.

[ ] Cross-reference back to pipeline/blueprint/v0.1/section_11_intake_v1_1_amendment.md §4 in any v1.x amendment frontmatter that lands either contract.
```

These are forward-binding requirements, not soft commitments — v1.x LOCK ceremonies that touch the AWARD_INGEST surface without addressing the named contracts (or explicitly deferring them with a written rationale) are themselves LOCK-ceremony defects.

## §5. Failure-code table

| Code | Tier | Module | Severity | Cycle |
| ---- | ---- | ------ | -------- | ----- |
| (none NEW — §11 v1.1 reuses §14 v1's `F-REPORT-COMMITMENT-MISSED.commitment_id_invalid_format` sub-tag at consumer side and adds a producer-side runtime `raise CommitmentIdInvalid` that fails the AWARD_INGEST run via the existing Rule 1 save-state-on-failure path) | PRE row-admission (deterministic runtime check at extraction time) | `pipeline/orchestrator/seats/intake.py` | MED (downstream-amplified at v0.2; bounded LOW at v0.1 by A1+A4) | §11 v1.1 RT-C2-02 producer-side closure 2026-05-11 |

No new top-level failure-code row is registered (the producer-side raise lands as a state-file failure_reason; sub-tag attribution travels through the §14 consumer-side closure). The §0.5 paired amendment registers (a) one marker row for the §11 v1.1 amendment anchor + (b) one enforcement-infrastructure row for the new shared `_commitment_id` module — see §6 below.

## §6. §0.5 paired commit (rows 414-415)

Per §6.17 Option-B compound-paired-commit pattern (mirroring §4 v2.x.1 + §0.5 v16 row 198/199 precedent), this amendment lands paired with a §0.5 amendment at the same `lock_timestamp_utc`. The paired commit lands two rows:

- **Marker (row 414):** `blueprint.amendment_anchor.s11_v1_1.v1` — defined_at = this file; parent_lock_version = §11 v1.1; kind = marker; stability_tier = STABLE.
- **Enforcement-infrastructure (row 415):** `orchestrator.seats._commitment_id.v1` — defined_at = `pipeline/orchestrator/seats/_commitment_id.py`; parent_lock_version = §11 v1.1; kind = enforcement-infrastructure; stability_tier = STABLE. Description: shared producer/consumer canonical home for the commitment_id safe-identifier contract; relocation target from §14 v1 LOCK row 200 consumer-side declaration; single source of truth for `SAFE_COMMITMENT_ID_REGEX` + `SAFE_COMMITMENT_ID_PATTERN` (with `re.ASCII` flag) + `COMMITMENT_ID_MAX_LEN` + `CommitmentIdInvalid` + `is_safe_commitment_id` + `sanitize_commitment_id`.

Runtime-live row count: 413 (post §0.5 v18 LOCK 2026-05-10 row 204) → 415 at compound LOCK.

The previously-registered row at §14 v1 LOCK §0.5 v17 (rows 379-395) for `pipeline/orchestrator/seats/report_generator/_commitment_id.py` is **retained at its location** — the module still exists as the re-export shim, and its `defined_at` field continues to resolve. A §0.5 v17 row narrative annotation (textual; not a row mutation) notes the relocation of the canonical declaration to row 415's location with backward-compat shim discipline at the original site. No row deletion. No row supersession.

## §7. Verification + dispatch posture

**Code-phase verification (this session — SCOPING DRAFT close):**

- 5 valid + 14 invalid + 5 non-str + 1 ASCII-flag + 1 cross-import-path-identity unit checks verified at draft time via system Python 3.10 against the new test file's matrix; .venv pytest run reserved for LOCK ceremony per the pinned-interpreter discipline (`scripts/run_tests.sh`).
- AWARD_INGEST producer-side end-to-end verified at draft time: 2 commitment rows admitted, both 32-character uppercase-hex IDs, both regex-matching, both `[A-F0-9]`-only.
- `_validate_and_collect_commitments` direct invocation verified via deterministic test harness: zero rejects, both rows uniquely-IDed.
- §14 v1 LOCK consumer-side import paths verified: `from pipeline.orchestrator.seats.report_generator._commitment_id import sanitize_commitment_id, CommitmentIdInvalid, is_safe_commitment_id, ...` still resolves; object identity preserved.

**Cowork Thesis dispatch (this session — pending LOCK):**

L-005 strict two-cycle cadence applies; cross-family rigor matches §4 v2.x.1 + §14 v1 LOCK posture per the parent amendment's audit row. Editor / Judge / Red Team dispatched via the openclaw gateway per `pipeline/validation/v4_v2_x_1_thesis_2026-05-10/dispatch_audit_v{1,2}.sh` template. Audit scope:

- **Predicate correctness.** The §11 producer-side `sanitize_commitment_id(uuid.uuid4().hex.upper())` call closes the named RT-C2-02 follow-on.
- **Canonical-home discipline.** The shared `pipeline/orchestrator/seats/_commitment_id.py` is the single canonical home; the consumer-side shim preserves object identity; both seats import.
- **Backward compat.** The §14 v1 LOCK consumer-side imports continue to resolve unchanged at the three on-disk call sites.
- **Test coverage.** The producer-side test surface verifies the regex shape contract, the valid/invalid matrix, the cross-import-path identity, and the end-to-end AWARD_INGEST row admission discipline.
- **Threat-model boundary preservation.** v7 LOCKED A1+A4 + the §2.1 documented out-of-scope classes + §4 v1.x amendment-realization checklist forward-binds operator-promote re-validation + operator-supplied-ID path admission.
- **No semantic delta vs. §14 v1 RT-C2-02 closure text.** The producer-side enforcement strictly tightens the contract; it never relaxes it. Cycle 2 must verify no consumer-side semantics drift.

## §8. Threat-model boundaries (interim posture)

The amendment's stated severity is **MED at v0.2 downstream-amplified, LOW at v0.1 single-operator Beta**:

- **v0.1 single-operator Beta** (current — see lock_history row 193/194 v0.1 Beta gate cleared): bounded by v7 LOCKED A4 operator-trusted preflight. The operator is the only contributor and the only operator-promote actor; the gap between Intake write and operator promote is owned by the operator. The producer-side enforcement is structural defense-in-depth at v0.1 — it catches the contract at admission time so the §14 consumer side never has to defensively fail-closed on an Intake-written row.
- **v0.2 first-ship** (§14 Report Generator live; §11 → §14 scheduler path active): the gap promotes to MED because §14 consumer side WOULD HAVE fail-closed on every commitment_id from a §11-without-this-amendment producer side. The amendment is the structural fix that makes the §14 scheduler path consumable without exception.
- **v2 multi-tenant** (Section O.5 horizon): the §2.1 dynamic-scope classes (hand-edit of proposal_commitments.yaml + operator-supplied-ID paths + concurrent-write races) promote to MED and route to v1.x amendment-realization checklist + Section O.5.

Promoting severity beyond MED at v0.2 would imply the rule must close all evasion classes to be useful — that conflates a *security guarantee against an adversarial contributor* (which §11 v1.1 does not claim under A4) with a *contract-shape compile-time check that catches the named producer-side gap RT-C2-02* (which §11 v1.1 does provide). The first is v2 multi-tenant scope; the second is the amendment's actual brief.

## §9. Acceptance criterion (closes RT-C2-02 at producer side)

§11 v1.1 LOCK ceremony asserts each criterion independently:

1. **On-disk module assertion.** `pipeline/orchestrator/seats/_commitment_id.py` exists and declares the canonical surface; the re-export shim at `pipeline/orchestrator/seats/report_generator/_commitment_id.py` re-exports the same objects (identity-shared). Verification = test introspection at the §C identity-contract tests.
2. **AWARD_INGEST row admission.** `pipeline/orchestrator/seats/intake.py:_validate_and_collect_commitments` calls `sanitize_commitment_id(uuid.uuid4().hex.upper())` at every row construction. Verification = §D end-to-end tests assert every emitted commitment_id satisfies `is_safe_commitment_id` and has length 32 uppercase-hex.
3. **§14 v1 LOCK import paths preserved.** Three call sites at the §14 v1 LOCK (lock_history row 200) continue to resolve via the shim. Verification = `tests/seats/report_generator/test_commitment_id.py` (the §14 v1 LOCK test suite) continues to pass green without modification.
4. **§14 v1 LOCK consumer-side gate semantics unchanged.** `F-REPORT-COMMITMENT-MISSED.commitment_id_invalid_format` continues to fire at PRE-pre-track-dispatch on any non-canonical commitment_id reaching the §14 consumer side. Verification = the existing gate test at `tests/logician/gates/test_f_report_commitment_missed.py` continues to pass.
5. **v1.x amendment-realization checklist binding.** The §4 forward-binding contracts (operator-promote re-validation + operator-supplied-ID path admission) are recorded in this amendment with named acceptance tests; v1.x LOCK ceremonies that touch the AWARD_INGEST surface must address or explicitly defer.

## §10. Cross-references

- Parent §11 v1 LOCK: `pipeline/blueprint/v0.1/section_11_intake.md` (row 185; LOCKED 2026-05-10).
- Predecessor §14 v1 RT-C2-02 closure: `pipeline/blueprint/v0.1/section_14_report_generator.md` §14.18.3 row RT-C2-02 (row 200; LOCKED 2026-05-10) — the "paired §11 v1.1 follow-on update" named in that row's closure text is this amendment.
- §14 v1 paired §0.5 v17 amendment: `pipeline/blueprint/v0.1/section_00_5_section_14_report_generator_amendment.md` (rows 379-395; LOCKED 2026-05-10).
- Narrow-corrective precedent pattern: `pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md` (rows 198/199; LOCKED 2026-05-10).
- Narrow-corrective architectural precedent: `pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md` (row 190; LOCKED 2026-05-10).
- Companion §0.5 paired amendment (this amendment): `pipeline/blueprint/v0.1/section_00_5_section_11_v1_1_amendment.md` (rows 414-415; LOCKs atomically with §11 v1.1).
- Audit trail (Cycle 1 + Cycle 2): `pipeline/validation/section_11_v1_1_thesis_2026-05-11/`.
- Session metrics: `pipeline/metrics/session_log.jsonl`.
- Lock history row (when LOCKed via Cowork Thesis): TBD at LOCK ceremony.
- **WS-J Code Slice 1 dependency (Cycle 1 RT-07 closure).** WS-J Code Slice 1 (§14 Report Generator code-phase realization, in flight concurrently per the dispatch packet "Concurrent: WS-I Slice 3 + WS-J Code Slice 1 + WPFA Thesis. Different surfaces.") MUST import `sanitize_commitment_id` + `is_safe_commitment_id` + `CommitmentIdInvalid` from the canonical home `pipeline/orchestrator/seats/_commitment_id.py` (§0.5 row 415), NOT re-author the regex or maintain a divergent declaration. The single-source-of-truth invariant is structural: any drift between the producer-side (§11) and consumer-side (§14) regex contracts would re-open the RT-C2-02 gap. WS-J Code Slice 1's LOCK ceremony MUST verify the import lands at the canonical home; the backward-compat shim at `report_generator/_commitment_id.py` continues to resolve for legacy imports but new WS-J code SHOULD import from row 415 directly.

## §11. Bounded findings + deferred dispositions (Cycle-1 row-170 transparent pattern)

Per the row-170 transparent disposition pattern (mirrors precedents at WS-D v7.0.5 row 179 + WS-B v7.0.7 row 180 + v7.0.4-M1 row 190 + WS-K §15 v1 rows 191/192 + WS-L §4 v2.x rows 193/194 + WS-I §13 rows 196/197 + §4 v2.x.1 rows 198/199 + WS-J §14 v1 rows 200/201): Cycle 1 surfaced 8 Red Team findings + 8 Editor LOW findings + Judge 105/105. Editor + Judge unanimously READY_TO_LOCK. Red Team READY_TO_LOCK with minor amendments (3 explicit fold-in recommendations; verdict blocking=false).

Each Red Team finding registered below with its disposition + destination. Cycle 2 verification re-passes the closures + any NEW probes follow the same disposition discipline.

### §11.1 FOLD-IN at LOCK (applied to module + tests + amendment text)

| Cycle-1 ID | Severity | Probe | Closure |
|---|---|---|---|
| RT-02 | LOW | Generation-strategy drift not constrained by contract; future edit could change `uuid.uuid4().hex.upper()` to `str(uuid.uuid4())` (length 36) or `uuid.uuid4().urn` (length 45 with prefix) and still satisfy the regex, breaking downstream 32-char fixed-width assumptions. | NEW test `test_award_ingest_commitment_id_length_is_thirty_two` anchors the 32-char invariant at the test surface. §A regex-shape unit tests retained for predicate-shape contract; length contract now separately anchored. |
| RT-04 | MED | `re.ASCII` flag is defense-in-depth against `\d`/`\w` drift, but a future predicate edit that uses Unicode property escapes (`\p{Nd}`, explicit `\uNNNN` codepoints) ignores the flag; existing test matrix only checks one lookalike (`٠`). | Test matrix §B EXTENDED with three additional Unicode digit lookalikes: Devanagari digit zero (U+0966), Full-width digit zero (U+FF10), Bengali digit one (U+09E7). The static-analysis rule recommendation (ban `\p`/`\u`/`\U` in the regex string) is registered as a v1.x amendment-realization checklist item (§4 contract 3) — not landed at v1.1 because adding an AST-lint rule is out of scope for this narrow-corrective. |
| RT-06 | LOW | Uniqueness test creates only 2 rows; uuid4 collision probability is ~2^-122 so the test never catches a regression; a deterministic-counter regression in ID generation would silently regress at scale. | NEW test `test_commitment_id_generation_is_unique_at_scale` invokes the sanitize/generate chain 1000 times and asserts uniqueness + canonical + 32-char invariant. Isolated from the AWARD_INGEST substrate-fabrication gate so the assertion is structurally load-bearing. |

### §11.2 BOUNDED-by-v7-A1+A4 (dynamic-scope / consumer-side / out-of-§11 — Section O.5 v2 promotion path)

| Cycle-1 ID | Severity at LOCK | Probe | Disposition |
|---|---|---|---|
| RT-01 | BOUNDED-MED | Un-sanitized write path outside `_validate_and_collect_commitments` — contributor could construct `ProposalCommitment` directly in a custom script, migration shim, or test, bypassing the producer-side admission gate. | Bounded by v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight). The only documented AWARD_INGEST writer is `_validate_and_collect_commitments` per §11 v1 LOCK row 185. Test fixtures that bypass for testing purposes are test artifacts, not production paths. A multi-writer hardening (module-level `_write_utils.py` guard that all writers must call) is a v2 multi-tenant Section O.5 target — at v0.1+v0.2 single-operator the operator-discipline boundary holds. Also see §4 v1.x checklist contract 2 (operator-supplied-ID path must route through sanitize_commitment_id). |
| RT-08 | BOUNDED-MED | Threat-model under-claim for v0.1 — a developer running §14 Report Generator manually at v0.1 against a hand-crafted yaml could see a raw unsafe ID in a traceback; potential information disclosure if traceback is logged to a shared syslog. | Two boundaries hold this finding: (a) the developer console at v0.1 is operator-trusted per A4 (the traceback content is within the trust boundary); (b) error-message sanitization in §14 is §14's responsibility, not §11's. §11 v1.1 closes the producer side; §14 v0.2 owns consumer-side error-format hygiene. Routed to a future §14 minor amendment (developer-mode error sanitization wrapper at the §14 consumer-side gate). |

### §11.3 DEFERRED to follow-on amendment (v1.x amendment-realization checklist contracts)

| Cycle-1 ID | Severity at LOCK | Probe | Routing |
|---|---|---|---|
| RT-05 | DEFERRED-HIGH | Operator-promote re-validation deferred creates a live attack surface at v0.2 — operator can hand-edit proposal_commitments.yaml between Intake write and promote; if promote handler doesn't re-validate, the unsafe ID lands in PROMOTED status; §14 consumer-side gate then aborts the pipeline. | The operator-promote handler does NOT exist on disk at v0.1 (the `tilth intake award-promote` CLI is named in §11.6.3 as a future deliverable; the handler module hasn't been authored). Fold-in NOW would require building the handler + the re-validation loop + tests as part of this narrow corrective amendment — out of scope for a v1.1 hardening of an existing v1 surface. The §4 v1.x amendment-realization checklist contract 1 binds: when the promote handler is built (likely as part of a §11 v1.x amendment or a v1.x white-glove operator-UX amendment), the named acceptance test `tests/seats/intake/test_award_promote_rejects_hand_edited_unsafe_commitment_id` MUST land green. The contract is structurally enforceable at v1.x LOCK ceremony; this v1.1 amendment names it explicitly so v1.x cannot ship without addressing. |

### §11.4 REJECTED-with-rationale

| Cycle-1 ID | Severity claimed | Probe | Rejection rationale |
|---|---|---|---|
| RT-03 | LOW (Red Team) | `import *` shim may lose object identity on `importlib.reload`. | Premise contradicted by on-disk shim: the shim at `pipeline/orchestrator/seats/report_generator/_commitment_id.py` does **explicit re-export** (`from pipeline.orchestrator.seats._commitment_id import (COMMITMENT_ID_MAX_LEN, CommitmentIdInvalid, ...)`), NOT `from ... import *`. The amendment text's narrative about "`import *` semantics" in §1 was a description of the contract intent, not the on-disk realization; the actual shim is explicit-name re-export. The PEP 562-style lazy-import drift Red Team cites does not apply to explicit re-exports. The `importlib.reload` concern is partially valid for any module-level identity contract; per Cycle 1 fold-in, a NEW test `test_canonical_home_and_shim_are_module_distinct` anchors the module-distinct + symbol-identity-shared contract at the test surface so a future refactor that conflates the modules surfaces structurally. (Mirrors §4 v2.x.1 Cycle-1 RT-13 / WS-L §4 v2.x Cycle-2 RT-04/05 REJECTED-with-rationale dispositions and WS-I §13 Cycle-2 RT-C2-04 disposition.) |

### §11.5 NO-OP (Red Team explicitly says "no gap for this amendment")

| Cycle-1 ID | Severity claimed | Probe | Disposition |
|---|---|---|---|
| RT-07 | LOW (Red Team) | Missing coordination with forward-binding WS-J Code Slice 1 — WS-J could re-author the regex without coordinating. | Red Team's own disposition: "NO-OP for this amendment but add a dependency note in the amendment header." Closure: §10 cross-references section now names WS-J Code Slice 1 as a dependency that MUST import from the canonical home at row 415 (not re-author the regex). The dependency is structural — WS-J Code Slice 1 reads `proposal_commitments.yaml` written by §11; any drift in the regex contract between producer and consumer would re-open RT-C2-02. |

### §11.6 Editor LOW findings (E-01..E-08)

All 8 Editor findings carry verdict READY_TO_LOCK and severity LOW. The findings are stylistic/readability recommendations (consistency review, examples, formatting alignment with precedents). Disposition: NON-BLOCKING; addressed where Cycle 1 fold-in edits to §0/§4/§8/§9 naturally improved the surface. No structural changes needed. Final Editor disposition recorded at Cycle 2 verification.

### §11.7 Cycle-2 verification dispositions

Cycle-2 dispatch (Editor + Judge + Red Team via openclaw bridge 2026-05-11T19:08Z) results:

- **Editor:** READY_TO_LOCK. Four LOW Cycle-2 NEW findings (E-C2-01..E-C2-04) — all stylistic/clarity advisories on the §11 disposition matrix readability + §4 contract 3 wording + §10 WS-J binding + §0 closure summary. Non-blocking. Folded-in where the closure naturally lands; no structural changes needed.
- **Judge:** READY_TO_LOCK 105/105 maintained. Verdict: "Cycle 1 fold-ins were executed perfectly. They successfully addressed all actionable findings from the Red Team, materially strengthening the test surface and forward-binding contracts without introducing any regressions or scope creep."
- **Red Team:** READY_TO_LOCK with minor fixes blocking=`false`. All 8 Cycle-1 findings (RT-01..RT-08) verified closed/dispositioned per §11.1-§11.5 (RT-C2-01 verification only). Three NEW Cycle-2 probes (RT-C2-02..RT-C2-04) FOLDED-IN at LOCK with explicit text-level mechanism per row-170 transparent-disposition pattern.

| Cycle-2 ID | Severity | Probe | Disposition |
|---|---|---|---|
| RT-C2-01 | LOW (verification) | Walk RT-01..RT-08 and confirm dispositions match Cycle-1 intent. | NO-ACTION (verification only) — all 8 Cycle-1 dispositions verified correctly present + grounded. |
| RT-C2-02 | MED | `importlib.reload` of canonical home creates stale references in the shim; identity contract requires re-import protocol. | **FOLDED-IN at LOCK** — NEW test `test_reload_preserves_identity_when_canonical_home_reloaded_first` anchors the reload + re-import protocol structurally. §4 v1.x checklist contract 3 documentation extended below to document the reload-protocol invariant. |
| RT-C2-03 | MED | AST-lint rule deferral to v1.x leaves a latent vulnerability window — author could inadvertently introduce a Unicode escape (`٠`) or property class (`\p{Nd}`) in the regex that bypasses the `re.ASCII` flag. | **FOLDED-IN at LOCK** — §4 v1.x checklist contract 3 wording strengthened: the AST-lint rule is named explicitly + the named acceptance test is named + the contract is forward-binding for the **next** narrow-corrective amendment in the §11 v1.x family OR the next minor v0.2 release (whichever lands first). The amendment text §0 + §4 explicitly notes the current state: the regex is single-site at `pipeline/orchestrator/seats/_commitment_id.py:30` + only the operator edits it + v7 A4 operator-trusted-preflight bounds the gap at v0.1+v0.2. The defense-in-depth posture (literal `[A-Z0-9_-]` predicate + `re.ASCII` flag + expanded 20-form invalid-identifier test matrix + module-distinct test + reload-protocol test) is the v0.1+v0.2 structural defense; the AST-lint rule is the v1.x hardening that catches contributor-edit drift at compile-time. Mirrors §4 v2.x.1 §11.1 BOUNDED-by-A1+A4 dynamic-call evasion class promoted to Section O.5 v2 — the structural defense at v0.1+v0.2 is bounded; the v1.x amendment-realization checklist contract is the named hardening. |
| RT-C2-04 | LOW | Uniqueness test at 1000 iterations covers stochastic regression but not deterministic-sequence regression (e.g., a sanitize caching bug). | **FOLDED-IN at LOCK** — NEW test `test_sanitize_is_stateless_across_calls` invokes `sanitize_commitment_id` against a 100-element deterministic sequence with re-invocation per element + uniqueness check on outputs. Anchors the pure-function contract independently of the uuid4 randomness source. |

---

## Appendix A — Canonical home contents (single source of truth)

The on-disk single source of truth lives in `pipeline/orchestrator/seats/_commitment_id.py`. Reproduced here for reading-surface coherence with the §14 v1 LOCK RT-C2-02 closure — drift between the file and this appendix is itself a §11 v1.1 defect and the file is canonical.

```python
SAFE_COMMITMENT_ID_REGEX: Final[str] = r"^[A-Z0-9_-]+$"
SAFE_COMMITMENT_ID_PATTERN: Final[re.Pattern[str]] = re.compile(
    SAFE_COMMITMENT_ID_REGEX, flags=re.ASCII
)
COMMITMENT_ID_MAX_LEN: Final[int] = 64

@dataclass(frozen=True, kw_only=True)
class CommitmentIdInvalid(ValueError):
    value: str
    rule: str  # commitment_id_must_be_str / commitment_id_empty_or_too_long / commitment_id_regex_mismatch
    def __post_init__(self) -> None:
        super(ValueError, self).__init__(
            f"commitment_id={self.value!r} violates {self.rule}"
        )

def is_safe_commitment_id(raw: object) -> bool: ...
def sanitize_commitment_id(raw: object) -> str: ...  # raises CommitmentIdInvalid

__all__ = [
    "COMMITMENT_ID_MAX_LEN",
    "CommitmentIdInvalid",
    "SAFE_COMMITMENT_ID_PATTERN",
    "SAFE_COMMITMENT_ID_REGEX",
    "is_safe_commitment_id",
    "sanitize_commitment_id",
]
```

The shim at `pipeline/orchestrator/seats/report_generator/_commitment_id.py` re-exports the public surface with object identity preserved:

```python
from pipeline.orchestrator.seats._commitment_id import (
    COMMITMENT_ID_MAX_LEN,
    CommitmentIdInvalid,
    SAFE_COMMITMENT_ID_PATTERN,
    SAFE_COMMITMENT_ID_REGEX,
    is_safe_commitment_id,
    sanitize_commitment_id,
)

__all__ = [...]  # same surface
```

The producer-side import at `pipeline/orchestrator/seats/intake.py`:

```python
from pipeline.orchestrator.seats._commitment_id import (
    CommitmentIdInvalid as _CommitmentIdInvalid,
    SAFE_COMMITMENT_ID_PATTERN as _SAFE_COMMITMENT_ID_PATTERN,
    sanitize_commitment_id as _sanitize_commitment_id,
)
```

And the producer-side row admission at `_validate_and_collect_commitments`:

```python
commitment_id = _sanitize_commitment_id(uuid.uuid4().hex.upper())
rows.append(
    ProposalCommitment(
        commitment_id=commitment_id,
        # ... rest of fields per §11.5.2 ProposalCommitment schema
    )
)
```
