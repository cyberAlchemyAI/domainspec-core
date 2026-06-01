# Spec card — pipeline.seats.scribe (Round 1: types + Phase 0 record + KGIE preflight)

**STATUS:** READY 2026-04-21 — §7 Scribe v1.1.1 LOCKED + §0.5 v7 LOCKED + §6 v1-r1 LOCKED. Scribe R1 can open immediately. Parent card: `section_7_council_seats_pipeline_modules.md` (Lane A step 5).

**Framework:** per `pipeline/templates/component_analysis_template.md` (Five Laws, Four Rules, failure-mode taxonomy, standard interface pattern — not restated).

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_07_scribe.md` **v1.1.1 LOCKED 2026-04-21** — §7.3 Phase 0 extractor contract, §7.4 KGIE preflight contract, §7.4a USER_DATA conversation anchor
- `pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md` **§0.5 v7 LOCKED 2026-04-21** — rows 118/119 (schemas), row 127 (conversation anchor), row 154 (`scribe.pre_gate.kgie_pass.v1`)
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 LOCKED — PRE-gate slot for `F-SCRIBE-KGIE-FAIL` / `F-SCRIBE-PHASE-0-MISSING` / `F-SCRIBE-RFA-MISSING` / `F-SCRIBE-RFA-DRIFT` must exist at §4.2.1 table before R1 LOCK (parent spec §6 dep 2 satisfied by Logician v2.2 waves 3+4 LOCK 2026-04-21)
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 §D.2 Scribe role, §F.1 SFR (Scribe is NOT SFR-exempt — but R1 ships no drafting path yet, SFR emission lands at R3)
- **Blueprint hash-at-card** (BLUEPRINT_DEPS pins, pre-fill at Round-open):
  - `section_07_scribe.md` — compute at card-open
  - `section_00_5_section_07_scribe_amendment.md` — compute at card-open
  - `section_04_logician.md` — compute at card-open

**Spec-card version:** v1
**Round:** §7 Scribe Round 1 — types + Phase 0 record shape + KGIE preflight predicate (zero LLM calls; pure deterministic Python)
**Canonical home:** `pipeline/seats/scribe/` (NEW — per parent spec §2; parallel to `pipeline/seats/scout/`)

---

## 1. Purpose

Round 1 lays the `pipeline.seats.scribe` shape layer + the one deterministic predicate (KGIE preflight) so that Round 2 can typecheck `SectionDraft` + `SmartObjective` + `OverlookedExpensesWalk`, Round 3 (`seat.py` subprocess entry) can call `kgie_preflight` as a gate predicate, and the Logician PRE-gate slot for `F-SCRIBE-KGIE-FAIL` has a real callable to invoke.

**Zero-LLM scope.** Every deliverable in this round is deterministic Python. No `router.call_seat`, no `pipeline.providers.<provider>.complete()`, no prompt compilation. Phase 0 RFA extraction itself is v0.2 roadmap (§7.3) — at v0.1 the `RfaExtractedRecord` is operator-hand-populated from the RFA and read as a fixture; R1 only pins the shape and a construction-time invariant checker. KGIE preflight is a pure predicate over the `KgiePreflightResult` + supplied `PROJECT_CONTEXT` + the `RfaExtractedRecord`.

**Out of scope at R1.** Drafting (`seat.py`), dialect code-switch, SMART generator, overlooked-expenses walk, program templates, admin-risk register query, prompt templates, subprocess entry, stdin/stdout envelope, cross-family report emission, SFR format, POST-gate claim-evidence grep. All land at R2 or R3.

## 2. Module layout

```
pipeline/seats/scribe/
  __init__.py              # __all__ exports (public surface for Round 1)
  types.py                 # frozen kw_only dataclasses: RfaExtractedRecord, KgiePreflightResult, KeywordCheck, GeographyRecord, IdentityClaim, ExperienceSummary, MatchRequirement, EvaluationCriterion, SectionSpec, DateTimeWithTimezone (wrapper around offset-aware datetime)
  kgie.py                  # kgie_preflight(rfa: RfaExtractedRecord, project_context: Mapping[str, Any], operator_affirmations: Mapping[str, ...]) -> KgiePreflightResult
  BLUEPRINT_DEPS           # engineering process §4.6 hash pins for §7 + §0.5 v7 + §4
```

Corpus fixtures live under `tests/corpus/scribe/v1/` per §7.14:
```
tests/corpus/scribe/v1/
  pass/
    vapg_happy_path/
      rfa_extracted_record.json       # hand-populated from VAPG FY26 RFA per §7.3
      project_context.json            # synthetic test applicant hitting all four KGIE dimensions
      expected_kgie_result.json       # frozen fixture — test pins equality
    reap_happy_path/
      ... (same shape)
  fail/
    missing_geography/                # PROJECT_CONTEXT.location incomplete → needs_operator_input
      ...
    identity_claim_no_source/         # identity affirmation lacking source_field → fail
      ...
    experience_gap/                   # E dimension critical gap → fail
      ...
```

## 3. Public API (Round 1)

`pipeline/seats/scribe/__init__.py` declares:

```python
__all__ = (
    # Phase 0 shapes
    "RfaExtractedRecord",
    "MatchRequirement",
    "EvaluationCriterion",
    "SectionSpec",
    "DateTimeWithTimezone",
    # KGIE shapes
    "KgiePreflightResult",
    "KgieStatus",                    # Literal["pass", "fail", "needs_operator_input"]
    "KeywordCheck",
    "GeographyRecord",
    "IdentityClaim",
    "ExperienceSummary",
    # KGIE predicate
    "kgie_preflight",
    # Failure-code constants (strings; exception classes live in pipeline.logician or a forward round)
    "F_SCRIBE_PHASE_0_MISSING",      # "F-SCRIBE-PHASE-0-MISSING"
    "F_SCRIBE_KGIE_FAIL",            # "F-SCRIBE-KGIE-FAIL"
    "F_SCRIBE_RFA_MISSING",          # "F-SCRIBE-RFA-MISSING"
    "F_SCRIBE_RFA_DRIFT",            # "F-SCRIBE-RFA-DRIFT"
)
```

No `ClaimEvidence`, no `SectionDraft`, no `SmartObjective` at R1 — those are R2. No `seat.py` at R1 — that's R3.

## 4. Design decisions

1. **Frozen kw_only dataclasses across all shapes (§4.10 engineering-process discipline + §1 Round-J parent-lock pattern).** Field-addition cannot silently reorder positional calls (v0.2 futureproofing). Every shape carries `__post_init__` integrity checks — frozen-ness is mutation-prevention, not invariant-enforcement.
2. **`DateTimeWithTimezone` is a wrapper, not a bare `datetime`.** Blueprint §7.3 pins offset-aware; a wrapper type documents the invariant at the type layer and refuses construction with `datetime.tzinfo is None`. Prevents `datetime.utcnow()`-without-tz bugs.
3. **`RfaExtractedRecord.rfa_content_sha3_512` is 128 hex characters (full SHA-3-512), not a prefix.** §7.4a pins the *conversation anchor* at 32-hex prefix (128-bit birthday-bound); the RFA content hash itself is full-width because it is pinned once per session and never enters a compact-reference context. R1's `__post_init__` asserts `len == 128` + `hex`.
4. **KGIE predicate is pure over `RfaExtractedRecord` + `project_context` mapping + `operator_affirmations` mapping.** No Vault I/O, no filesystem reads, no LLM calls. The KGIE predicate's input is already materialized by the caller (seat.py at R3 will assemble it from `pipeline.vault` reads; R1 tests supply fixtures directly). Pure predicate = trivial unit test + property-test surface.
5. **KGIE PASS/FAIL/NEEDS_OPERATOR_INPUT tri-state (§7.4).** The predicate returns `KgiePreflightResult` with `status` set; it NEVER raises on missing fields (raising conflates "no data" with "invariant violation"). Caller inspects `status` — Logician PRE-gate `F-SCRIBE-KGIE-FAIL` reads `status == "fail"`; `needs_operator_input` is routed to operator-facing open-question surface, not a failure.
6. **Hash-pinning on Phase 0.** R1 does NOT read the RFA file; it only pins the shape. But R1 exposes a helper `verify_rfa_content_hash(rfa_path: Path, pinned_sha: str) -> bool` used by R3's PRE-gate for `F-SCRIBE-RFA-DRIFT`. Helper uses `pipeline.vault` canonical-bytes reader when available at R3 time; R1 supplies it as a thin wrapper over `hashlib.sha3_512` reading file bytes in 1-MiB chunks (no full-file load; Mac-Mini-8GB-safe).
7. **Operator affirmations supplied as a frozen mapping.** KGIE's K dimension requires per-term applicant affirmation. R1 pins `operator_affirmations: Mapping[str, Literal["affirmed", "not_applicable_with_reason", "unanswered"]]` with "unanswered" producing `needs_operator_input`, not silent PASS. No `default=affirmed` anywhere.
8. **Identity-claim-without-source fails the whole preflight.** §7.4 + §7.2 Law 5 — Scribe never infers identity. R1's predicate iterates `identity_claims`; any entry with empty / None `source_field_in_project_context` returns FAIL. No soft-warn path.
9. **BLUEPRINT_DEPS declaration** (per engineering process §4.6 + L-015):
   ```python
   BLUEPRINT_DEPS = {
       "pipeline/blueprint/v0.1/section_07_scribe.md": {
           "sha256_16": "<computed-at-LOCK>",
           "sections": ("§7.3", "§7.4", "§7.4a", "§7.13"),
       },
       "pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md": {
           "sha256_16": "<computed-at-LOCK>",
           "rows": (118, 119, 127, 134, 135, 154),  # rfa_extracted_record, kgie_preflight_result, conversation_anchor, phase_0_missing, kgie_fail, kgie_pass pre-gate
       },
       "pipeline/blueprint/v0.1/section_04_logician.md": {
           "sha256_16": "<computed-at-LOCK>",
           "sections": ("§4.2.1",),
       },
   }
   ```

## 5. Invariant checklist (per-dataclass `__post_init__`)

- `RfaExtractedRecord.__post_init__`:
  - `len(rfa_content_sha3_512) == 128` and all chars ∈ `0-9a-f`.
  - `len(program_name.strip()) > 0`.
  - `deadline.datetime.tzinfo is not None`.
  - `award_ceiling >= award_floor` when both present.
  - `extracted_at_utc.tzinfo is not None`.
  - `eligible_applicant_types` + `eligible_project_activities` + `required_attachments` + `key_terms` are all hashable/immutable (tuple / frozen Mapping).
- `KgiePreflightResult.__post_init__`:
  - `status ∈ frozenset({"pass", "fail", "needs_operator_input"})` — inline literal per V1 rebind-resistance.
  - If `status == "pass"`: `needed_fields == ()` (no open questions) AND every `IdentityClaim.source_field_in_project_context` is non-empty AND `geography_verified.rfa_geographic_match is True`.
  - If `status == "needs_operator_input"`: `len(needed_fields) >= 1`.
  - `preflight_at_utc.tzinfo is not None`.
- `GeographyRecord.__post_init__`: `len(state) == 2` (USPS code) or operator-documented override tag.
- `IdentityClaim.__post_init__`: `rfa_priority_points >= 0`.
- `ExperienceSummary.__post_init__`: `years_operating >= 0`; `production_metrics` is a frozen mapping; `prior_grants` / `certifications` / `partnerships` are tuples.

## 6. KGIE predicate algorithm (pure function)

```
def kgie_preflight(
    rfa: RfaExtractedRecord,
    project_context: Mapping[str, Any],                # PROJECT_CONTEXT.md parsed shape
    operator_affirmations: Mapping[str, Literal["affirmed", "not_applicable_with_reason", "unanswered"]],
    clock: Callable[[], datetime] = _default_utc_now,  # E-017 injected-callable seam
) -> KgiePreflightResult:
    needed: list[str] = []

    # K — every key_term requires an affirmation or explicit NA with reason
    keyword_checks = []
    for term in rfa.key_terms:
        affirm = operator_affirmations.get(term, "unanswered")
        if affirm == "unanswered":
            needed.append(f"kgie.K:{term}")
        keyword_checks.append(KeywordCheck(
            term=term,
            applicant_affirmation=affirm,
            source=_affirmation_source(project_context, term) if affirm == "affirmed" else None,
        ))

    # G — geography pulled from project_context.location
    geo = _build_geography_record(project_context, rfa, needed)

    # I — identity claims; any missing source_field → fail
    identities, has_identity_gap = _build_identity_claims(project_context, rfa, needed)

    # E — experience
    experience, has_experience_gap = _build_experience_summary(project_context, needed)

    # Status dispatch
    if needed:
        status = "needs_operator_input"
    elif has_identity_gap or has_experience_gap or not geo.rfa_geographic_match:
        status = "fail"
    else:
        status = "pass"

    return KgiePreflightResult(
        status=status,
        keywords_checked=tuple(keyword_checks),
        geography_verified=geo,
        identity_claims=tuple(identities),
        experience_summary=experience,
        needed_fields=tuple(needed),
        preflight_at_utc=clock(),
    )
```

Helpers `_build_geography_record`, `_build_identity_claims`, `_build_experience_summary` are module-private and pure. `_default_utc_now` is module-level `lambda: datetime.now(tz=timezone.utc)`; tests pass a fixed-clock callable for determinism (E-017 injected-callable pattern; 11th firing).

## 7. Test surface (target: 40+ tests; coverage ≥ 95%)

**Type-shape tests (happy path — 10+):**
- Every frozen dataclass constructible with the full documented field set.
- `__all__` export surface matches exactly (no leakage, no missing symbols).
- `RfaExtractedRecord.rfa_content_sha3_512` rejects 127-char / 129-char / non-hex inputs.
- `DateTimeWithTimezone` rejects naive datetimes.

**KGIE PASS tests (4+):**
- VAPG happy-path fixture → `status == "pass"`, `needed_fields == ()`.
- REAP happy-path fixture → same.
- Two-identity claim (e.g. veteran + beginning farmer) with both sourced → PASS.
- All-N/A keywords with reasons → PASS.

**KGIE FAIL tests (6+):**
- Identity claim missing `source_field_in_project_context` → `status == "fail"`.
- `geography_verified.rfa_geographic_match is False` → `status == "fail"`.
- `ExperienceSummary` with `years_operating == 0` AND no certifications AND no partnerships (E critical gap) → `status == "fail"`.

**KGIE NEEDS_OPERATOR_INPUT tests (4+):**
- Any `operator_affirmations[term] == "unanswered"` → `status == "needs_operator_input"`.
- Missing `PROJECT_CONTEXT.location.state` → `needed_fields` contains `kgie.G:state`.
- Multiple gaps accumulate (K + G + I + E all missing) → `len(needed_fields) == 4+`.

**Property tests (6+, via `hypothesis`):**
- **Idempotence under fixed clock:** `kgie_preflight(rfa, ctx, affirm, clock=fixed)` called twice returns equal `KgiePreflightResult` with identical `preflight_at_utc`.
- **Monotonic-add-affirmation property:** if adding one more affirmed keyword to `operator_affirmations`, the `needed_fields` set loses at most that one entry (cannot grow).
- **PASS requires four-dimension hit:** generate KGIE results with random missingness; every PASS must have zero `needed_fields` AND all identities sourced AND geography match.

**Adversarial tests (6+):**
- `object.__setattr__` on frozen field raises (documents the frozen invariant even though this is OUT-OF-MODEL per CPython dataclass semantics).
- Round-trip through JSON via `dataclasses.asdict` + re-construct: preserves all invariants.
- Sha input with uppercase hex → `__post_init__` rejects (canonical lowercase per §2 vault canonical-bytes discipline).
- RFA record where `eligible_project_activities` contains a duplicate string → R1 does NOT reject (duplicate is an authoring decision), but test pins the permissiveness.
- KGIE with empty `rfa.key_terms` (RFA has no glossary): no K-dimension gaps; rest of algorithm still runs.
- Injected clock that raises `RuntimeError` → predicate propagates, does not swallow.

**Adversarial tests specific to Logician gate integration (R1 lands the symbols; R3 wires the gate):**
- `F_SCRIBE_KGIE_FAIL` string value exactly `"F-SCRIBE-KGIE-FAIL"` (matches §7.13 + §0.5 row 135).
- `F_SCRIBE_PHASE_0_MISSING`, `F_SCRIBE_RFA_MISSING`, `F_SCRIBE_RFA_DRIFT` string values match §7.13 exactly.

## 8. Done definition (R1)

- Module exists at `pipeline/seats/scribe/` with `__init__.py`, `types.py`, `kgie.py`, `BLUEPRINT_DEPS`.
- Public API surface exactly matches §3 above — `__all__` leakage = LOCK fail.
- Every §5 invariant enforced via `__post_init__`; fuzz-pass on 1000 random permutation cases per Hypothesis.
- Every §7 test surface item from §7.14 touching R1 (4 listed in blueprint: frozen, kgie_pass-requires-four-dims, smart/overlooked are R2) covered by explicit named tests.
- Fixture corpus at `tests/corpus/scribe/v1/{pass,fail}/` with ≥ 2 pass + ≥ 3 fail fixtures populated.
- **Coverage ≥ 95%** on `pipeline/seats/scribe/` module tree at R1.
- **AST-lint R1-R7 clean** — seat code imports from `pipeline.logician` (exception classes at R3 wiring; R1 has no Logician import yet), imports `hashlib` / `datetime` / stdlib only. R2 `loop-logician-ban` does not apply to `pipeline/seats/` (parent spec §8).
- **BLUEPRINT_DEPS sha-pinned** against §7 + §0.5 v7 + §4; L-015 regression test `test_blueprint_deps_citations.py` extended to validate `pipeline/seats/scribe/BLUEPRINT_DEPS` cited sections resolve.
- **Full suite green** (current baseline 4988 pass post-Vault-Batch-3-Phase-1 remediation 2026-04-21; R1 expected delta ≈ +40-60 tests).
- **LOCK row** appended to `pipeline/engineering/lock_history.v1.jsonl` with reviewer tokens, test count, F-code surface.
- Self-LOCK eligible per §5 precedent (12 consecutive §5 single-cycle self-LOCKs R3→R12.B; Scribe R1 is shape-only + one pure predicate — similar complexity envelope to §5 R1 foundations).

## 9. Committee composition (if committee is dispatched)

Scribe production binding = Anthropic; none of the five standard code-reviewers are Anthropic (codex / qwen3-32b / llama-3.3-70b / gpt-oss-120b / kimi-k2 per `router.yaml`). Cross-family clean.

**Self-LOCK recommendation.** R1 is pure-Python shape + one predicate with no I/O and no LLM call. Prior §5 R1 foundations (analogous scope: types + config + errors) self-LOCKED without committee. Same discipline applies here — dispatch committee only if the coverage or AST-lint findings raise a flag during LOCK-prep verification. Committee credits conserved for R3 (subprocess entry, subprocess-envelope schema, cross-family telemetry emission — materially higher composition risk).

## 10. Failure modes (delta — framework taxonomy per template §3)

- **Aspiration-as-enforcement on `RfaExtractedRecord` shape (L-006):** pinning the shape without yet having a Phase 0 extractor module means R1 ships a record shape that can only be hand-populated. Dev-mode symptom: tests pass on hand-crafted fixtures. Prod-mode failure: operator misses a field in the manifest and the gap doesn't surface until Scribe R3's drafting path. Mitigation: `KgiePreflightResult.needed_fields` is the operator-facing safety net; `kgie_preflight` fails-loud on missing data, not silently.
- **`rfa_content_sha3_512` length not validated early:** if R1's `__post_init__` skips the 128-hex assertion, R3's `F-SCRIBE-RFA-DRIFT` compare could false-positive on truncation. Mitigation: explicit assertion at R1 type-level.
- **Timezone-naive `datetime` snakes through as "UTC assumed":** platform-dependent `datetime.utcnow()` returns naive on some call sites. Mitigation: `DateTimeWithTimezone` wrapper refuses construction; tests pass explicit `tzinfo=timezone.utc` everywhere.
- **Property-test flakiness under `hypothesis`:** idempotence property requires deterministic clock; if injected-clock seam isn't wired correctly, `preflight_at_utc` drifts across property runs. Mitigation: E-017 injected-callable pattern; `_default_utc_now` overridden explicitly in every Hypothesis test.

## 11. Hardenings (delta — template §4 checklist)

- [ ] Frozen, kw-only, slots=True on every dataclass (A-13 memory-layout discipline — M1 Mac Mini 8GB dev node friendliness).
- [ ] `__post_init__` invariant enforcement on every frozen dataclass.
- [ ] `__all__` in `__init__.py` is a tuple literal (V1 rebind-resistance; no `__all__.append`).
- [ ] `DateTimeWithTimezone` rejects naive datetimes at construction.
- [ ] KGIE predicate is pure (no I/O, no globals mutation, no LLM call).
- [ ] Injected-clock seam pinned (E-017) — tests supply fixed clock, production default supplies `utc_now`.
- [ ] Phase 0 extractor module absence is DOCUMENTED in `types.py` docstring + spec-card §9 OQ-1 (call-out to v0.2 roadmap).
- [ ] BLUEPRINT_DEPS pin present + L-015 citation-check clean.
- [ ] Coverage ≥ 95%; Hypothesis fuzz pass on 1000 cases.

## 12. Open questions for operator (non-blocking — R1 can dispatch on defaults)

- **OQ-1 — Phase 0 extractor timing.** §7.3 defers extractor to v0.2. At v0.1 `RfaExtractedRecord` is hand-populated. Confirm v0.1 launch ships with operator-hand-populated records (no parser) OR request Phase 0 extractor spec card to be pre-staged for v0.1.5.
- **OQ-2 — Fixture corpus source RFAs.** R1 needs ≥ 2 pass + ≥ 3 fail KGIE fixtures. Proposed: VAPG FY26 (already extracted at `pipeline/rubrics/vapg_fy26.json`) + REAP (known structure from prior grants). Confirm, or supply alternative RFA pair Josh has on-disk.
- **OQ-3 — PROJECT_CONTEXT shape.** R1's KGIE predicate reads fields `.location.{state,county,zone_tags}`, `.identity_affirmations`, `.experience.{years_operating,production_metrics,prior_grants,certifications,partnerships}`. These are already present in every `orgs/<slug>/PROJECT_CONTEXT.md` per CLAUDE.md + `orgs/_TEMPLATE/`. Confirm shape pin or request Template round to align.
- **OQ-4 — E dimension "critical gap" definition.** R1's FAIL condition requires `years_operating >= 0 AND (years_operating > 0 OR certifications != () OR partnerships != ())` — i.e., a zero-year brand-new entity with no credentials cannot pass E. This excludes newly-founded operations that have partnerships instead. Confirm the threshold, or relax to "any non-empty experience signal."

## 13. Non-goals at R1

- No drafting — no `seat.py` — no subprocess entry.
- No SMART / Overlooked / Dialect / Templates — all R2.
- No admin-risk register integration — R3.
- No claim-evidence grep POST-gate — R3 / Logician.
- No prompt-template compilation — R3 + §6 prompt-template pipeline.
- No LLM provider calls — zero across R1.
- No cross-family telemetry emission — R3.
- No Phase 0 RFA extractor module — v0.2 roadmap (§7.3).

## 14. Changelog

- **v1 READY 2026-04-21.** Authored post-§7 LOCK + post-§0.5 v7 LOCK + post-§6 v1-r1 LOCK (all three prerequisites SATISFIED). Scribe R1 unblocked for Code-session open. Parent spec card (`section_7_council_seats_pipeline_modules.md`) line-3 forward-reference now resolves.

*End spec card — READY to dispatch at Code-session open.*
