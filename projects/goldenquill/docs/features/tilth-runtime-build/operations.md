# Operations: Tilth Runtime Build — Grant-Cycle Council Pipeline

The six council seats are modelled as operations (Scout/Scribe/Editor/Judge/Red Team/Logician). No seat outranks another; the applicant decides. Each operation satisfies the Four Autonomy Rules: Save State Always, Test Your Own Work, Be Explicit, Clean Output.

## ScoutDiscovery

Two-stage discovery. DISCOVER reads the union of six parallel channel families (A–F, all primary, none a fallback); VERIFY fetches a live synopsis before any candidate reaches CRITICAL-fit; REVIEW is the human gate. Scout never auto-files.

**Source:** `tilth-runtime-build.ScoutDiscovery`
**Actor:** [OpportunityCandidate](domain.md#opportunitycandidate)
**Emits:** [`tilth-runtime-build.OpportunityVerified`](events.md#opportunityverified)

### Inputs

| Field | Type | Required |
| ----- | ---- | -------- |
| sourceManifest | ChannelManifest | yes |
| candidateId | CandidateId | yes |

### Business Rules

| ID | Rule | Enforcement |
| -- | ---- | ----------- |
| R1 | [VerifyBeforeCriticalRule](#verifybeforecriticalrule): no candidate reaches CRITICAL-fit without a passed live-synopsis VERIFY | See [VerifyBeforeCriticalRule](#verifybeforecriticalrule) |
| R2 | All six channel families run as parallel primaries | `∀ ch ∈ {A..F} : ch.role == primary` |
| R3 | No CIC→CLC coupling in scoring | `F-CIC-CLC-COUPLING-VIOLATION` clean (orthogonal axes) |

### Effects

- Sets [OpportunityCandidate](domain.md#opportunitycandidate).verdict from VERIFY
- Holds at REVIEW human gate — never auto-files
- Emits `tilth-runtime-build.OpportunityVerified`

### Error States

| Code | Condition |
| ---- | --------- |
| NO_LIVE_ENDPOINT | VERIFY has no endpoint → verdict UNVERIFIED |
| VERIFY_FETCH_ERROR | Live-synopsis fetch errored → VERIFICATION_FAILED |

---

## ScribeDraft

Drafts a proposal section by section with KGIE preflight, SMART outcomes, overlooked-expenses checklist, and funder-dialect code-switching. Never silently rewrites flagged terms (Law 4 — applicant approves each substitution).

**Source:** `tilth-runtime-build.ScribeDraft`
**Actor:** [Draft](domain.md#draft)

### Inputs

| Field | Type | Required |
| ----- | ---- | -------- |
| cycleId | CycleId | yes |
| sectionPlan | SectionPlan | yes |
| gear | OperatingGear | yes |

### Business Rules

| ID | Rule | Enforcement |
| -- | ---- | ----------- |
| R4 | [Law1TraceabilityRule](#law1traceabilityrule): every section claim traces to RFA or PROJECT_CONTEXT | See [Law1TraceabilityRule](#law1traceabilityrule) |
| R5 | [GearModePolicy](workflows.md#gearmodepolicy) selects autonomy level | See [GearModePolicy](workflows.md#gearmodepolicy) |
| R6 | No `[SLOT_*]` emitted into any cloud-routed prompt | `\[SLOT_[^\]]*\]` regex never matches a cloud payload |

### Effects

- Produces [Draft](domain.md#draft) sections with [SectionProvenance](domain.md#sectionprovenance) per claim
- Flagged-term substitutions require applicant approval (never silent)
- Consumes `tilth-runtime-build.DraftRevisionRequested` to recompose flagged sections

### Error States

| Code | Condition |
| ---- | --------- |
| KGIE_PREFLIGHT_FAIL | KGIE preflight did not pass for a section |
| UNTRACEABLE_CLAIM | A claim has no RFA/PROJECT_CONTEXT source (Law 1) |

---

## EditorPass

Reads Scribe's draft through different eyes. Flags jargon, offers 2–3 concrete replacement options per issue, sorts goals/outputs/outcomes/objectives. Post-substance drafts route LOCAL.

**Source:** `tilth-runtime-build.EditorPass`
**Actor:** [Draft](domain.md#draft)

### Inputs

| Field | Type | Required |
| ----- | ---- | -------- |
| draftId | DraftId | yes |

### Business Rules

| ID | Rule | Enforcement |
| -- | ---- | ----------- |
| R7 | Each clarity flag carries 2–3 concrete replacement options | `∀ flag : 2 ≤ |flag.options| ≤ 3` |
| R8 | Substitutions require applicant approval (Law 4) | Never silent rewrite |

### Effects

- Annotates [Draft](domain.md#draft) with clarity flags + options
- Leaves substance unchanged until applicant approves

### Error States

| Code | Condition |
| ---- | --------- |
| MISSING_OPTIONS | A flag has fewer than 2 replacement options |

---

## JudgeScore

Evaluates a draft against the funder's own rubric first, then cross-checks related library rubrics. Cross-family rigor — Judge must not share a provider family with Scribe. High-stakes grants trigger the on-demand local heavy-Judge (200B-class, pre-loaded in-image, no network fetch).

**Source:** `tilth-runtime-build.JudgeScore`
**Actor:** [Draft](domain.md#draft)
**Emits:** [`tilth-runtime-build.DraftScored`](events.md#draftscored)

### Inputs

| Field | Type | Required |
| ----- | ---- | -------- |
| draftId | DraftId | yes |
| rubric | FunderRubric | yes |

### Business Rules

| ID | Rule | Enforcement |
| -- | ---- | ----------- |
| R9 | [CrossFamilyRule](#crossfamilyrule): Judge provider family ≠ Scribe family | See [CrossFamilyRule](#crossfamilyrule) |
| R10 | Every rubric dimension scored with an evidence string present in the draft | Uses [CouncilSplitDelta](#councilsplitdelta) for the split gap |

### Calculations Applied

1. [CouncilSplitDelta](#councilsplitdelta) — absolute Judge/Red-Team score gap

### Effects

- Writes [RubricScore](domain.md#rubricscore) per dimension onto the [Draft](domain.md#draft)
- Emits `tilth-runtime-build.DraftScored`

### Error States

| Code | Condition |
| ---- | --------- |
| EVIDENCE_NOT_IN_DRAFT | A scored dimension's evidence string is absent from the draft |
| SAME_FAMILY_AS_SCRIBE | Judge bound to Scribe's provider family |

---

## RedTeamChallenge

Adversarial challenge. Fires on every draft. Cross-family rigor against both Scribe and Judge — never shares a provider family with either. A ≥10-point disagreement with Judge triggers a council split.

**Source:** `tilth-runtime-build.RedTeamChallenge`
**Actor:** [Draft](domain.md#draft)
**Emits:** [`tilth-runtime-build.CouncilSplitRaised`](events.md#councilsplitraised)

### Inputs

| Field | Type | Required |
| ----- | ---- | -------- |
| draftId | DraftId | yes |
| judgeScore | RubricScore[] | yes |

### Business Rules

| ID | Rule | Enforcement |
| -- | ---- | ----------- |
| R11 | [CrossFamilyRule](#crossfamilyrule): Red Team family ≠ Scribe and ≠ Judge | See [CrossFamilyRule](#crossfamilyrule) |
| R12 | Red Team fires unconditionally on every draft | No skip path |

### Calculations Applied

1. [CouncilSplitDelta](#councilsplitdelta) — feeds the split threshold

### Effects

- Records adversarial findings on the [Draft](domain.md#draft)
- Emits `tilth-runtime-build.CouncilSplitRaised` when delta ≥ 10

### Error States

| Code | Condition |
| ---- | --------- |
| SAME_FAMILY | Red Team shares a family with Scribe or Judge |

---

## LogicianGate

Deterministic Python + Cedar validation, not AI. Fail-closed, zero token cost. Enforces all Five Laws as PRE/POST gates. Cannot be overridden by any prompt, skill, or model.

**Source:** `tilth-runtime-build.LogicianGate`
**Actor:** [GrantCycle](domain.md#grantcycle)
**Emits:** [`tilth-runtime-build.DraftRevisionRequested`](events.md#draftrevisionrequested)

### Inputs

| Field | Type | Required |
| ----- | ---- | -------- |
| cycleId | CycleId | yes |
| draftId | DraftId | yes |

### Business Rules

| ID | Rule | Enforcement |
| -- | ---- | ----------- |
| R13 | [MagicStepValidationRule](#magicstepvalidationrule): validate before marking any task complete (Rule 2) | See [MagicStepValidationRule](#magicstepvalidationrule) |
| R14 | [CouncilSplitPolicy](workflows.md#councilsplitpolicy) routes ≥10-point splits to the human gate | See [CouncilSplitPolicy](workflows.md#councilsplitpolicy) |
| R15 | No model invocation inside the gate (zero-token, deterministic) | Logician runs Python/Cedar only |

### Effects

- Fail-closes any unsatisfied Five-Laws PRE/POST gate
- Emits `tilth-runtime-build.DraftRevisionRequested` on a fail-closed gate

### Error States

| Code | Condition |
| ---- | --------- |
| GATE_FAIL_CLOSED | A Five-Laws PRE/POST gate did not pass → revise |
| LLM_CALL_IN_GATE | Model invocation attempted inside Logician (forbidden) |

---

## CouncilSplitDelta

The absolute point gap between Judge's and Red Team's total scores. A delta of 10 or more triggers a council split (boundary inclusive at threshold).

**Source:** `tilth-runtime-build.CouncilSplitDelta`

Derives values consumed by [JudgeScore](#judgescore) and [RedTeamChallenge](#redteamchallenge).

| Property | Value |
| -------- | ----- |
| Inputs | `judgeTotal: int, redTeamTotal: int` |
| Output | `delta: int` |

```
delta = abs(judgeTotal - redTeamTotal)
split = delta >= 10
```

**Properties:** non-negative; deterministic; `split` is inclusive at the threshold (per §10.6).

---

## Business Rules (standalone)

### VerifyBeforeCriticalRule

**Source:** `tilth-runtime-build.VerifyBeforeCriticalRule`

No opportunity reaches CRITICAL-fit without a passed live-synopsis VERIFY (Law 1; EPA NEETP-26 precedent).

| Property | Value |
| -------- | ----- |
| Applies To | ScoutDiscovery |
| Formula | `criticalFit → verdict == VERIFIED_FIT` |
| Violation | Hold candidate at UNVERIFIED; do not elevate |

---

### Law1TraceabilityRule

**Source:** `tilth-runtime-build.Law1TraceabilityRule`

Every claim traces to the RFA or PROJECT_CONTEXT — no secondhand descriptions substitute (Law 1).

| Property | Value |
| -------- | ----- |
| Applies To | ScribeDraft |
| Formula | `∀ claim : claim.sourceRef ∈ {rfa, project_context}` |
| Violation | Reject section with `UNTRACEABLE_CLAIM` |

---

### CrossFamilyRule

**Source:** `tilth-runtime-build.CrossFamilyRule`

Judge must not share a provider family with Scribe; Red Team must not share with either Scribe or Judge. Provider bindings live in `router.yaml` — never hardcoded.

| Property | Value |
| -------- | ----- |
| Applies To | JudgeScore, RedTeamChallenge |
| Formula | `judge.family ≠ scribe.family ∧ redteam.family ∉ {scribe.family, judge.family}` |
| Violation | Refuse the call; re-bind from `router.yaml` |

---

### MagicStepValidationRule

**Source:** `tilth-runtime-build.MagicStepValidationRule`

Before marking any task complete, validate (Rule 2 — Bug #20). Judge validates all dimensions scored and evidence strings appear in the draft.

| Property | Value |
| -------- | ----- |
| Applies To | LogicianGate |
| Formula | `complete → validate() == pass` |
| Violation | Fail-close; emit DraftRevisionRequested |
