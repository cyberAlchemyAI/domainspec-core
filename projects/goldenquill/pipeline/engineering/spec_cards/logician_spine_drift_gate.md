# Spec card — pipeline.logician.spine_drift_gate

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_04_logician.md` — Logician POST-gate battery; Law 4 (Funder-Attractive Framing) deterministic enforcement layer.
**Spec-card version:** v1
**Round:** post-v0.1 (v0.2 roadmap)
**Priority:** v0.2 medium-high (after fabricated-ORG; before fact-drift if scope forces a choice)
**Origin:** Exploration `pipeline/roadmap/explorations/narrative_spine_design.md` (2026-05-06) — operator-approved design intent. This card converts that exploration to spec by resolving the four open design questions.

---

## Purpose

Deterministic Logician POST-gate that catches narrative drift across Scribe sections + Editor edits. Enforces that operator-approved strategic framings — locked at SP1 after KGIE preflight — survive every drafting and editing pass intact.

**Doctrine** (from exploration): nothing in Tilth is automated end-to-end. Defining human-in-the-mix stop points is a critical component of the system, not a nice-to-have. The time saved by stopping and tightening language to create accurate outputs is far greater than the time required to remediate a memory contaminated with bad data downstream.

**Example catch:** Operator locks framing-001 "Worker-owned cooperative scaling regenerative mushroom production" at SP1. Scribe drafts Section 1 with this framing. Editor R2 cleans Section 1 prose and silently weakens to "Mushroom production cooperative." Gate fires `F-LOGICIAN-SPINE-DRIFT` and DENIES Editor's edit.

---

## Open-question resolutions (from exploration § "Open questions")

| Q | Exploration proposal | **Spec resolution** |
|---|---|---|
| 1. Format | YAML | **YAML.** Same reasoning as KFR — operator-readable, diff-friendly, schema-validatable. |
| 2. Mid-grant amendment | Amendable with re-lock vs immutable post-SP1 | **Amendable with operator re-lock event recorded in version history.** Mid-grant amendment requires explicit operator override via the SP2 review surface (which already exists per design). Each amendment writes a new `spine.locked.v<N>.yaml` with diff metadata; the gate evaluates against the *current* lock; older locks are audit history. |
| 3. Multi-grant sequence | Carry-forward template vs always-fresh | **Always-fresh per grant.** Operator can manually copy a prior `spine.locked.yaml` as starting input to SP1 review; that's a workflow choice, not a Tilth automation. Carrying spine framings across grants risks framing reuse where reviewer expectation has shifted; per-grant freshness forces re-evaluation. |
| 4. Spine adherence as Judge dimension | 13th rubric dimension vs Logician-only | **Logician-only.** Adding spine adherence to Judge would: (a) dilute the rubric (rubric measures content quality vs RFA criteria; spine adherence is a process discipline); (b) make spine drift a soft scoring concern rather than a hard fail-closed boundary; (c) duplicate gating logic across two seats. Logician deterministic gate is sufficient. |

---

## Architecture

### Drop point

Logician POST-gate, fires after Scribe output AND after Editor output (two activation points). Sequenced after fabricated-ORG and fact-drift gates (substance gates first, framing gate last — substance must be present before framing-adherence is meaningful).

Wired into `run_post_gate_skeleton` for Scribe outputs; a parallel `run_editor_post_gate` (when Editor lands its POST-gate hook) calls the same gate for Editor outputs.

### Pipeline

1. **Load.** Read `orgs/<org>/grants/<grant_id>/spine.locked.yaml`. Validate schema. Missing file → FAIL with reason `spine_missing` (every grant past SP1 must have a spine; no implicit empty-spine).
2. **Extract.** For each `funder_attractive_framings[].id`, build a representation: (claim_text, mandatory_keyword_set). Mandatory keywords = the content words ≥4 chars in the framing's `claim` field, deduped, lowercased.
3. **Section scan.** For each Scribe-drafted section in scope:
   - a. Tokenize section body (lowercase, content-words-only).
   - b. For each spine framing-id required by `cross_section_anchors.methods_must_mirror` / `outcomes_must_mirror` / `budget_justification_must_cite` for this section:
      - i. Compute `keyword_recall = |framing_keywords ∩ section_tokens| / |framing_keywords|`.
      - ii. If `keyword_recall < 0.6`: FAIL with reason `spine_framing_weak` and the framing-id + missing keywords.
   - c. **Anti-contradiction check.** For each framing's `claim`, scan section for explicit negation patterns ("not a cooperative", "outside the regenerative model"). If detected: FAIL with reason `spine_framing_contradicted`.
4. **Dialect register check.** Compare section's classified dialect (Scribe self-report or Editor classification) against `spine.dialect_register`. Mismatch: FAIL with reason `spine_dialect_drift`.
5. **Admin-risk-term check.** Scan section for any term in `spine.admin_risk_terms_avoid`. Hit: FAIL with reason `spine_admin_risk_violation`.
6. **Verdict.** Zero failures → PASS with per-section adherence trace. Any failure → FAIL with full findings list.

### Properties

- **Deterministic:** YAML load + token-set operations + regex negation patterns + dialect enum compare = fully deterministic. Zero LLM tokens.
- **Fail-closed:** any drift → FAIL. M13 bypass available but audited.
- **Layered with KGIE + SP1:** gate is meaningful only post-SP1 (when spine is locked); pre-SP1 drafting flow doesn't invoke this gate.
- **Two activation points:** Scribe POST-gate AND Editor POST-gate. Same gate code; two callers.

---

## Failure codes

| Code | Trigger | Severity | Reason tag |
|---|---|---|---|
| `F-LOGICIAN-SPINE-DRIFT` | Any spine adherence rule fails | HIGH | `spine_missing`, `spine_framing_weak`, `spine_framing_contradicted`, `spine_dialect_drift`, `spine_admin_risk_violation` |

---

## Public API

```python
# pipeline.logician.gates.f_logician_spine_drift

def check_spine_drift(
    *,
    section_text: str,
    section_id: str,                          # e.g. "1.A.2" — for cross-section-anchor lookup
    section_dialect: str,                     # Scribe / Editor self-classified
    spine_path: pathlib.Path,
) -> SpineDriftGateResult: ...

def load_spine(path: pathlib.Path) -> NarrativeSpine: ...
```

---

## Data structures

```python
@dataclass(frozen=True, kw_only=True)
class SpineFraming:
    id: str                    # framing-NNN
    claim: str
    rationale: str
    rfa_anchor: str            # e.g. "VAPG FY26 §3.A.2"
    keywords: frozenset[str]   # derived from claim at load time


@dataclass(frozen=True, kw_only=True)
class SmartOutcomeShape:
    primary: str
    secondary: str | None
    tertiary: str | None


@dataclass(frozen=True, kw_only=True)
class CrossSectionAnchor:
    section_id: str
    methods_must_mirror: tuple[str, ...] = ()           # framing-ids
    outcomes_must_mirror: tuple[str, ...] = ()
    budget_justification_must_cite: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class NarrativeSpine:
    grant_id: str
    locked_at: datetime
    locked_by: str
    version: int                                        # increments on operator re-lock
    funder_attractive_framings: tuple[SpineFraming, ...]
    dialect_register: Literal["conservative", "centrist", "progressive", "soul_fire"]
    admin_risk_terms_in_use: tuple[str, ...]
    admin_risk_terms_avoid: tuple[str, ...]
    smart_outcome_shape: SmartOutcomeShape
    strategic_emphasis: dict[str, Any]
    cross_section_anchors: tuple[CrossSectionAnchor, ...]


@dataclass(frozen=True, kw_only=True)
class SpineDriftFinding:
    framing_id: str | None       # None for non-framing failures (dialect / admin-risk-term)
    section_id: str
    reason_tag: Literal[
        "spine_missing",
        "spine_framing_weak",
        "spine_framing_contradicted",
        "spine_dialect_drift",
        "spine_admin_risk_violation",
    ]
    detail: str                  # missing keywords / contradicting phrase / hit term


@dataclass(frozen=True, kw_only=True)
class SpineDriftGateResult:
    verdict: Literal["PASS", "FAIL"]
    failure_code: str | None
    findings: tuple[SpineDriftFinding, ...]
    section_id: str
    framings_checked: int
```

---

## Dependencies

- `pyyaml>=6.0` — already in pyproject.toml. Spine YAML load.
- (No new substrate deps. Pure stdlib + pyyaml + existing tilth tooling.)
- **No spaCy required.** Token extraction is regex-based content-word matching; this gate stays lighter than fabricated-org / fact-drift (no NER/POS, just word sets).

---

## Test surface

### Failure-code tests

- Section that mirrors all required framings → PASS.
- Section missing keywords from a required framing → `F-LOGICIAN-SPINE-DRIFT` / `spine_framing_weak`.
- Section explicitly contradicting a framing claim → `spine_framing_contradicted`.
- Section using a `dialect_register: progressive` claim but classified as `conservative` by Scribe → `spine_dialect_drift`.
- Section containing a term in `admin_risk_terms_avoid` → `spine_admin_risk_violation`.
- Missing spine file → `spine_missing`.
- Spine present but `cross_section_anchors` doesn't reference this section → PASS (gate is silent for sections not anchored).

### Edge cases

- Re-locked spine (version=2): gate evaluates against current version only; older versions in audit history but not in spine_path lookup.
- Multi-keyword framing: keyword recall threshold (0.6) gives operator some flexibility for paraphrase but catches gross drift. Tunable.
- Operator re-lock during a drafting run: gate evaluation pinned to the spine version active at *section start* (read once per section, not on every check).

### Integration tests

- Wire into `run_post_gate_skeleton` via new `spine_path` + `section_id` + `section_dialect` kwargs (backward-compat pattern).
- Wire into Editor POST-gate at the same wire-in convention when Editor lands.
- Combined run: F-POST-10 + F-LOGICIAN-FABRICATED-ORG + F-LOGICIAN-FACT-DRIFT + F-LOGICIAN-SPINE-DRIFT all surface together when all four fire.

---

## Interaction with existing gates

| Gate | Scope | Relation |
|---|---|---|
| Law 4 dialect classification | Funder dialect register | **Upstream input.** Dialect classifier produces the section_dialect this gate compares against the spine. |
| Law 4 admin-risk register | Term-level dialect drift | **Sibling.** Admin-risk register catches funder-dangerous terms broadly; spine `admin_risk_terms_avoid` is the *grant-specific* per-spine override. Gate checks both — admin-risk-register fail is via existing path; spine-specific avoid-list fail is via this gate. |
| KGIE preflight | RFA-required-section affirmation | **Upstream sibling.** KGIE confirms operator has answered required questions; spine confirms operator has framing strategy. Both pre-drafting; spine is the post-KGIE step. |
| F-LOGICIAN-FABRICATED-ORG | Fabricated organisations | **Adjacent — substance vs framing.** Fabricated-org catches the substance bug; spine-drift catches the framing bug. |
| F-LOGICIAN-FACT-DRIFT | Numeric value drift | **Adjacent — substance vs framing.** Same axis. |

---

## Stop-point integration (from exploration)

- **SP1 — Spine Lock.** Operator reviews proposed framings, dialect register, SMART outcome shape, strategic emphasis, admin-risk term registers. Approves and locks. Output: `spine.locked.yaml`.
- **SP2 — Section Boundary.** Operator reviews TRT findings + drafted section against spine. Adjusts before continuing — flags drift, picks which TRT findings Scribe acts on, edits the spine itself if a discovered framing should propagate forward (operator re-lock event).
- **SP4 — Post-Editor / Pre-Judge.** Operator sees Editor's clarity changes alongside *spine adherence delta*. Anything Editor moved that drifted the spine surfaces explicitly via this gate's findings. Operator approves, reverts, or sends back to Editor.

This gate is the runtime enforcement layer that makes the SP1 lock + SP2/SP4 review surfaces meaningful.

---

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Keyword-recall threshold (0.6) too strict on paraphrase | Tunable per-spine via `keyword_recall_threshold` field on the spine YAML. Default 0.6 is the conservative starting point; operator can relax per grant if false positives accumulate. |
| Anti-contradiction patterns miss subtle weakening | Acceptable for v0.2 — gate covers explicit contradiction. Subtle weakening surfaces at SP2/SP4 operator review. |
| Operator re-lock mid-grant surfaces all sections as "drifted" against new lock | Re-lock event records `re_evaluated_sections` field; gate skips re-evaluation of sections drafted before the re-lock by default; operator opts into re-checking. |
| Dialect classification noise | Dialect classifier returns confidence; gate treats low-confidence classifications as `unknown` rather than triggering drift. Fail-closed only on confident-dialect mismatch. |
| Spine YAML hand-edited inconsistently across grants | Schema validation at load — same JSON Schema discipline as KFR. |

---

## Implementation sequencing

1. **Round v0.2.A** — Spine loader + schema validation + dataclasses. (~150 LOC + 150 LOC tests.)
2. **Round v0.2.B** — Keyword extraction + recall computation + contradiction patterns. (~150 LOC + 150 LOC tests.)
3. **Round v0.2.C** — `check_spine_drift` entry point + `run_post_gate_skeleton` Scribe-side wiring + integration tests. (~150 LOC + 150 LOC tests.)
4. **Round v0.2.D** — Editor-side wire-in (when Editor POST-gate hook lands).

Total gate scope: ~450 LOC production + ~450 LOC tests = ~900 LOC across 3-4 rounds. Lighter than fact-drift (~1250 LOC) because no NER/POS dep — keyword sets only.

---

## Sequencing recommendation against KFR gate

If both spine-drift and fact-drift gates are queued for v0.2 and operator must choose order:

**Build spine-drift first.** Tighter spec, lighter dependency surface (no spaCy/POS for v0.2.A-B), shorter implementation arc, and the SP1 lock workflow it enables is more valuable per dollar of spec work than the SP0 KFR review workflow (which is operator-already-doing-this-by-hand at v0.1; spine drift is a runtime enforcement that operator currently has no recourse for at v0.1).
