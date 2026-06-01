# Spec card — pipeline.seats.judge (Round 3: seat.py subprocess entry + Google binding + SFR emission + POST-gate wiring)

**STATUS:** PRE-STAGED 2026-04-29

**Parent spec:** `pipeline/engineering/spec_cards/section_7_council_seats_pipeline_modules.md` (Lane A step 5; Judge = **FULL PORT** per OQ-1).

**Framework:** per `pipeline/templates/component_analysis_template.md` (Five Laws, Four Rules, failure-mode taxonomy, standard interface pattern — not restated).

---

## 1. Blueprint anchors

- **§9 Judge blueprint — MUST be LOCKED before R3.** R3 implements the full seat entry; all §9-owned design decisions must be settled.
- `pipeline/blueprint/v0.1/section_06_operating_envelope.md` v1-r1 LOCKED — §6.3 A2 router.yaml schema (Google envelope that Judge binds to), §6.5 A3 SFR format (Judge is NOT exempt; R3 ships SFR emission), §6.6 A4 context-placement, §6.11 prompt-template compilation pipeline.
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED — §4.3 Judge invocation tuple return + A-v1-02 trust model + A-v1-13 minimal-env subprocess.
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 LOCKED + v2.2 — POST-gate slot for `F-JUDGE-EVIDENCE-NOT-IN-DRAFT` (Law 5 core); R3 wires this gate through `gate_runner.py`.
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 §D.4 Judge role, §F.1 SFR (NOT exempt), §E cross-family guard.
- `router.yaml` — `tilth.judge` primary = `google/gemini-2.5-pro`; escalation = `anthropic/claude-opus-4-6` + `openai/gpt-5.1` (Reasoner Review tier). Reference only.

**Blueprint hash-at-card** (BLUEPRINT_DEPS, computed at R3 open):
- `section_09_judge.md` — recompute (R2 may have amended)
- `section_06_operating_envelope.md` — compute
- `section_05_pipeline.md` — compute
- `section_04_logician.md` — compute (post-F-JUDGE-* slot allocation)

**Spec-card version:** v1
**Round:** §9 Judge Round 3 — seat.py subprocess entry + Google provider binding + SFR emission + Logician PRE/POST gate wiring. **R3 is the Judge seat's LOCK-closing round.**
**Canonical home:** `pipeline/seats/judge/` (R1 + R2 modules already landed)

---

## 2. Depends on

- **Judge R1 LOCKED** — types + rubric_loader + dimension_scorer.
- **Judge R2 LOCKED** — cross-rubric dispatch + responsiveness mapper + JudgeVerdict + §0.5 rows.
- **§9 Judge blueprint LOCKED** ✅ (prereq for R2; inherited by R3).
- **§6 Operating Envelope v1-r1 LOCKED** ✅ — R3's prompt compiles through §6.11's pipeline.
- **§4 Logician v2.2 LOCKED** ✅ — POST-gate F-JUDGE-* slot allocation. R3 consumes, does not author gate predicates.
- **Scribe R3 LOCKED** (soft) — R3 mirrors Scribe R3's seat.py pattern for subprocess entry + provider binding + PRE/POST wiring. Pattern reference, not hard dependency.

---

## 3. Proposed modules

```
pipeline/seats/judge/
├── seat.py                   # subprocess entry: stdin→envelope→rubric-load→score→verdict→SFR→stdout
├── provider_google.py        # thin BYOK Google binding; reads router.yaml seats.judge.*
├── sfr_emitter.py            # SFR three-block format: Premises (rubric + RFA scope),
│                             #   Execution (per-criterion scores + evidence), Conclusion (verdict + score)
├── logician_wiring.py        # PRE/POST gate assembly for Judge-specific F-JUDGE-* codes
└── BLUEPRINT_DEPS            # refresh with §6 + §4 post-gate-slot pins
```

---

## 4. What R3 does

- **seat.py subprocess entry.** Same shape as Scribe R3's seat.py: decode SeatEnvelope stdin → run Logician PRE-gate → load rubric → dispatch to cross-rubric scorer (R2) → assemble JudgeVerdict (R2) → emit SFR → run Logician POST-gate → emit JudgeOutput JSON to stdout (Rule 4: no fences, no commentary).
- **Google provider binding.** Reads `router.yaml` seats.judge.* for model, endpoint, API key reference. Constructs correct Google API envelope. BYOK — reads key from operator's keystore (§1 keys.py surface). Minimal stub at R3 (pattern from Scribe R3's provider_anthropic.py).
- **SFR emission.** Three-block Premises/Execution/Conclusion per architecture §F.1. Judge is NOT exempt. Premises = rubric citation + RFA scope summary. Execution = per-criterion score table + evidence quotes. Conclusion = overall score + pass/fail verdict + confidence.
- **Logician PRE/POST gate wiring.** PRE: F-PRE-CROSS-ORG-READ + standard PRE checks. POST: F-JUDGE-RUBRIC-MALFORMED, F-JUDGE-CRITERION-MISSING, F-JUDGE-SCORE-UNPARSEABLE, F-JUDGE-EVIDENCE-NOT-IN-DRAFT (Law 5), F-JUDGE-SCORE-OUT-OF-BOUND, F-JUDGE-RUBRIC-HASH-DRIFT. Each wired as a post_gate predicate returning (pass/fail, F-code, message).

**What R3 does NOT author:**
- The Google HTTP client itself — R3 composes a thin binding. If `pipeline/providers/google.py` does not exist at R3 open, R3 ships a minimal BYOK client stub under `pipeline/seats/judge/provider_google.py` (mirrors Scribe R3 pattern).
- The prompt-template compilation pipeline — §6.11 owns that.
- The rubric loader or dimension scorer — R1 owns those.
- The cross-rubric dispatcher or verdict assembler — R2 owns those.

---

## 5. Test surface

- Subprocess lifecycle: stdin envelope → stdout JudgeOutput (happy path + every F-code trigger).
- SFR format validation: three-block structure, evidence quotes present, score table complete.
- Google provider binding: router.yaml read, envelope construction, BYOK key resolution.
- POST-gate: each F-JUDGE-* predicate fires on constructed trigger input.
- Law 5 end-to-end: evidence_quote not in draft → F-JUDGE-EVIDENCE-NOT-IN-DRAFT blocks output.
- Cross-family enforcement: provider_google reads router, not hardcoded.

---

## 6. Done definition

- All R3 modules landed in `pipeline/seats/judge/`.
- Tests ≥ 90 (R1 + R2 + R3 combined). ≥ 95% coverage. AST-lint clean.
- Full suite GREEN.
- Ledger row: `lock_class: "code"`, committee_round id, SHA-3-512[:16].
- Paired `## LOCK:` block in daily log (F-AMDT-12).
- Committee **5/5 PASS** per L-005.
- **R3 LOCK closes Judge as a full pipeline seat.** Post-R3: §9 whole-section capstone eligible.

---

## 7. Status update — Judge R2 LOCKED 2026-04-29

R2 self-LOCKed at lock_history row 148 (`code_sha3_512_prefix: f09fc9e9477774b6` over 3-module concat).
R2 ships:
- `cross_rubric_dispatch.py` — `dispatch_criteria_to_scorers` + `dispatch_score_units` + `parent_criterion_for_unit`.
- `responsiveness_mapper.py` — `KNOWN_RESPONSIVENESS_FACTOR_KEYS` + `extract_responsiveness_factors_from_rubric_json` + `build_responsiveness_map`.
- `verdict_assembler.py` — `assemble_verdict` (CriterionScore[] + Rubric → JudgeVerdict; pre-gates F-JUDGE-EVIDENCE-NOT-IN-DRAFT verbatim substring of section_drafts[*].body_text).

R2 also extends `types.py` with `JudgeVerdict` + `ResponsivenessEntry` + `ResponsivenessMap`.

R3 imports R2's `assemble_verdict` and uses it inside `seat.py` after the LLM-call loop.
R3 imports `dispatch_score_units` for the per-unit score iteration and feeds each unit to R1's `score_dimension`.
R3 imports `build_responsiveness_map` for the audit-side metadata (and chooses whether to run it on every Judge invocation or only at SFR-emit time).

### 7.a — Known R3-reconciliation item: `ClaimEvidenceLike` ↔ Scribe `ClaimEvidence` field-name divergence

R1 declared `ClaimEvidenceLike` with fields `claim_text` + `evidence_text` + `source_field`.
Scribe R2.5 ships concrete `ClaimEvidence` with fields `claim_text` + `evidence_kind` (Literal["RFA","PROJECT_CONTEXT","USER_DATA"]) + `source_pointer`.
R2 pinned the divergence at `tests/seats/judge/test_e026_section_draft_bind.py::TestClaimEvidenceLineageOnly::test_concrete_shape_does_not_match_r1_protocol_field_names`.

**R3 must reconcile via one of:**

(a) Scribe-side `judge_view` adapter — Scribe ships a `ClaimEvidence.as_judge_view()` method that returns an object structurally satisfying the Judge `ClaimEvidenceLike` Protocol. Backwards compatible.
(b) Judge-side Protocol amendment — update `ClaimEvidenceLike` to match Scribe's actual fields (`evidence_kind` + `source_pointer`); requires updating R1's adversarial test stub at `tests/seats/judge/test_types.py:366` and the pinned-divergence test in `test_e026_section_draft_bind.py`.

R3 should pick (b) unless Scribe has an outside-Judge consumer that depends on the original Protocol field names — search `grep -r "claim_evidence_map\b" pipeline/seats/` for Scribe-side adapters before committing. If only Judge consumes the Protocol, (b) is the cleaner reconciliation. The Judge-side amendment fits inside R3's LOCK round (no separate Protocol amendment round needed).

### 7.b — Coverage backfill bait

R2's `verdict_assembler.py` carries 2 lines uncovered (98%): `total_score > max_total` + `max_total > rubric.max_score`. Both are sanity guards downstream of the per-score bound check and `Rubric.__post_init__`. R3 may consider:
- Inlining a `# pragma: no cover — sanity guard, score-bound check upstream prevents this` annotation; OR
- Backfilling the 2 cases via a monkey-patched-rubric test that bypasses Rubric construction (`object.__new__(Rubric)` + `object.__setattr__` would do it, mirroring the pattern from Editor R2 cycle-1 frozen-vs-slots discovery).

Either approach is acceptable for the R3 ≥95% coverage gate; R2 is already at 99% subtree.
