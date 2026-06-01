# A4 Deliberate-Defect-Injection Round — Spec (v0.1)

**Authority.** King Midas v2.1 §12c (invocation mode); Improvement Plan 2026-05-04 §A4 (originating task). Companion to:

- `pipeline/engineering/templates/committee_reviewer_prompt_template.md` — per-seat prompt convention
- `pipeline/engineering/king_midas_implementation_prompt_v2_1.md` §10 — committee discipline (must-find-one + trace-verification + severity auto-promotion)
- `pipeline/validation/defect_injection_2026-05-04/` — round 1 artifacts (reference implementation)
- King Midas brief §9 Q2 — the originating question

**Purpose.** Falsifiable test of the 5-family Code Thesis Committee architecture. Without deliberate defect injection, cycle-1-clean rates are a hypothesis: maybe the committee discipline is real, maybe it's prompt-template friendliness. A4 rounds inject ONE known defect per round and measure whether the committee catches it.

---

## 1. Cadence

**One A4 round per Wave-completion event.** Each Wave currently lands ~3-5 gates; one calibration round per Wave is light overhead and establishes ongoing measurement.

- **Trigger:** any Wave-N capstone LOCK or whole-section LOCK (e.g., §8 Editor whole-section, §9 Judge whole-section, §10 Red Team whole-section).
- **Gate timing:** A4 round fires AFTER the Wave LOCK lands, NOT before. Rationale: A4 is calibration of the committee architecture, not validation of the Wave content. Mixing them confounds the signal.
- **Skipping:** A4 is skippable if (a) the Wave's committee verdicts already surfaced ≥1 substantive defect organically (cycle-1 catches as native A4-equivalent), OR (b) the operator explicitly defers (operator-discretionary; logged in daily log).

## 2. Defect-class rotation list

Each A4 round picks ONE defect class from the rotation list. Round-N picks `defect_classes[N mod len(defect_classes)]`, OR the operator picks explicitly. Rotation prevents over-fitting the committee to one defect class.

| # | Defect class | Description | Severity (typical) |
|---|--------------|-------------|--------------------|
| 1 | regex-boundary-error | `\d` instead of `\d+`; `+` instead of `*`; missing `^`/`$` | MEDIUM |
| 2 | off-by-one | `<` instead of `<=`; index slice off-by-one | MEDIUM-HIGH |
| 3 | fail-closed-bypass | `except Exception` swallowed without DENY | HIGH |
| 4 | missing-cedar-row | Org-isolation primitive without `org_isolation` Cedar row | HIGH |
| 5 | hash-pin-mismatch | BLUEPRINT_DEPS hash drift from §0.5 Index | MEDIUM |
| 6 | taxonomy-collision | F-code reused; sub-code orphaned from parent | MEDIUM |
| 7 | property-test-coverage-hole | Test exists for happy path; negative-case test missing | MEDIUM |
| 8 | empty-vs-whitespace | `if not s:` instead of `if not s.strip():` | MEDIUM |
| 9 | boundary-inversion | `>=` instead of `<=`; truthy instead of `is True` | HIGH |
| 10 | constant-time-comparison-skip | Hash comparison via `==` instead of `hmac.compare_digest` | HIGH |

**Round 1 (2026-05-04):** class #1 regex-boundary-error. Round 2 (next Wave-completion): class #2 off-by-one. Etc.

## 3. Round artifacts checklist

Every A4 round produces:

| Artifact | Purpose | Required? |
|----------|---------|-----------|
| `00_planted_defect.md` | Sealed envelope: defect description, severity rationale, falsifiable predictions (P1/P2/P3/P4) | YES — authored BEFORE dispatch; not loaded into dispatch payload |
| `spec_card.md` | Behavioral contract for the synthetic gate | YES |
| `gate/<module>.py` | The artifact under review (with planted defect) | YES |
| `gate/_protocols_local.py` (if needed) | Protocol surface for injected dependencies | optional |
| `gate/test_<module>.py` | Tests passing under the defect (coverage hole on the planted-defect input class) | YES |
| `gate/conftest.py` (if needed) | Pytest sys.path shim for hyphenated dirs | optional |
| `dispatch.py` | 5-family parallel committee dispatcher | YES |
| `dispatch_retry_<seat>.py` (if needed) | L-011 transport-retry script for any seat that hits MAX_TOKENS / transport artifact | as needed |
| `system_base.txt` | Shared committee system prompt (verdict rubric, must-find-one, trace-verification) | YES (per template) |
| `system_<seat>.txt` × 5 | Per-reviewer lens prompts | YES (per template) |
| `pre_dispatch_hashes.json` | sha256 of every round artifact (tamper-evidence) | YES — written by dispatch.py at fire time |
| `r_<seat>.raw.json` × 5 | Per-seat raw API response | YES (auto-generated) |
| `r_<seat>.content.md` × 5 | Per-seat extracted verdict content | YES (auto-generated) |
| `committee_summary.md` | Auto-generated dispatch summary | YES (auto-generated) |
| `synthesis.md` | Post-dispatch scoring against sealed envelope; recommendations; lesson candidates | YES — authored AFTER all 5 verdicts return |

## 4. Synthesis scoring rubric

Every A4 synthesis MUST report:

### 4.1 Per-reviewer scorecard
| Seat | Verdict | Findings | Caught defect? | Notes |

Where:
- **Verdict:** the reviewer's PASS / REQUIRES_FIXES / FAIL
- **Findings:** count + severity distribution
- **Caught defect?:** YES (with severity flagged) / NO (rubber-stamp, with rubber-stamp pattern named) / PARTIAL (e.g., flagged the test coverage gap but not the underlying code defect)
- **Notes:** specific evidence for the determination — what input did the reviewer probe? What did they conclude?

### 4.2 Per-lens hit rate
Group reviewers by lens (general-cross-check / blueprint-adherence / adversarial / cross-module-coherence / fast-scan); report HIT/MISS rate per lens. Pattern-matching lenses (general-cross-check, fast-scan) historically miss; probing lenses (adversarial, cross-module, blueprint) historically hit.

### 4.3 Merge-layer outcome
Under `code_merge_rule: all_pass`, would the artifact have been promoted? Apply §10b severity auto-promotion (2+ reviewers above MEDIUM → final HIGH; 3+ reviewers converging → always promote).

### 4.4 Pre-registered prediction outcome
Which of P1/P2/P3/P4 (from sealed envelope) fired? Note any prediction not covered by sealed envelope.

### 4.5 Disposition of King Midas brief §9 Q2
Confidence update: did this round narrow the validation surface? In what direction?

### 4.6 Recommendations
- Prompt-template hardenings (with specific clause text)
- Lens-specific calibrations
- Logician-side detector candidates (Wave-N gates)
- Operator-discretionary actions

### 4.7 Lesson candidates
Pre-staged for operator review; NOT filed in the A4-round session. Operator decides L-NNN filing per L-013/L-005 escalation discipline.

## 5. Round-naming convention

`pipeline/validation/defect_injection_<YYYY-MM-DD>/`

For multiple rounds in one day (rare): `pipeline/validation/defect_injection_<YYYY-MM-DD>_<defect-class>/`.

## 6. Cost guidance

**Budget per round:** ≤$5 in API spend (5-fire parallel; ~80k prompt tokens; ~5k visible completion + ~4k hidden thoughts on Gemini). Within Wave-completion-event operator budget.

**Wall-clock per round:** ≤2 min end-to-end (parallel 5-fire ~50s; 1-2 transport retries per L-011 if needed; ~30s setup + tests).

**Operator session time:** 1 working session for round setup + dispatch; ~30 min for synthesis review. Total ≤2 hr.

## 7. What this spec does NOT cover

- **The actual Wave-N gate authoring.** A4 is a calibration round, not a Wave deliverable. Wave-N gate authoring follows the standard King Midas §7 implementation loop.
- **Recurring schedule automation.** A4 rounds are operator-triggered at Wave-completion events, not cron-scheduled. (If automated, would land in §12c spec; deferred until ≥3 manual rounds prove the value.)
- **Cross-defect-class hypothesis testing.** A4 round 1 tested ONE class (regex-boundary). Cross-class confidence requires multiple rounds; estimate ≥4 rounds before strong cross-class claims hold.
- **Reviewer-model swap experiments.** Slate diversity is a separate question (King Midas brief §9 Q5). A4 holds the slate constant to isolate prompt + defect signal.
- **Lock ceremony.** A4 is process-discipline; no `lock_history.v1.jsonl` row appended. Round captured in daily log + synthesis trail.

## 8. Round 1 reference (2026-05-04)

`pipeline/validation/defect_injection_2026-05-04/` — full reference implementation. Defect class: regex-boundary-error. Outcome: 3/5 caught at MEDIUM/HIGH; merge layer correctly bounces; per-lens hit rate confirmed adversarial/cross-module/blueprint 100% vs general-cross-check/fast-scan 0%. Three lesson candidates pre-staged (L-017/L-018/L-019).

---

*A4 spec v0.1 — 2026-05-04 — authored as A4 round 1 follow-through. Revision discipline: changes land via L-005 two-audit cycle when the spec surface materially changes; minor refinements (e.g., new defect-class rotation entries) appended in-place with footnote.*
