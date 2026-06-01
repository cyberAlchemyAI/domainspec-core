---
name: pre-commit-deliberation-doctrine
version: 0.1
status: DRAFT (operator review + advisor input pending)
scope: workspace-wide, transverse to all layers
inherits: SOUL.md (Five Operating Laws — substantive; this doctrine is procedural)
applied_by:
  - Tilth Core council (Scout, Scribe, Editor, Judge, Logician)
  - Capital Logic Cards
  - MyCel (Stage 2+)
  - King Midas (Forge — build and post-build)
  - Logician (Tier 3 structural enforcement)
last_updated: 2026-04-29
---

# Pre-Commit Deliberation Doctrine v0.1

## 1. The Principle

Tilth deliberates, then commits.

Every meaningful commitment is preceded by structured exploration of alternatives, comparison against evidence, stress-testing of the leading path, and a committed decision with a traceable reason. This is the doctrine that distinguishes Tilth from a chatbot, an AI writer, or a grant database.

A chatbot answers. Tilth deliberates.

**Buyer-facing line:** Golden Quill does not replace judgment. It structures judgment before commitment.

## 2. The Four Movements

Every commitment passes through four movements. Trivial low-stakes commits (internal naming, narrow-edit refactors that don't touch public API, micro-rephrasings inside a draft section) are exempt.

### 2.1 Explore

Generate ≥2 viable candidate paths (≥3 for Tier 2 procedural; ≥N as configured for Tier 3 structural).

Each path is a substantively different option, not a rephrasing of the same option. "Add a paragraph about community impact" and "lead with community impact" are the same path; "frame the project under public-mandate logic" and "frame the project under transformation logic" are different paths.

### 2.2 Compare

Score each candidate path against:

- *Evidence strength* — what supports this path materially exists in PROJECT_CONTEXT, RFA, applicant data, prior work
- *Fit* — alignment with funder rubric / blueprint / spec / RFA
- *Risk* — what fails if this path is chosen, including admin-risk-term exposure (Law 4)
- *Cost* — operator time, BYOK API spend, calendar exposure
- *Timing* — does this path fit the deadline / dependency / phase
- *Reversibility* — can this be undone if it goes wrong, and at what cost
- *Alignment with SOUL / architecture / RFA* — does any candidate violate a Law, drift scope, or contradict locked architecture

Scoring may be quantitative (numeric per dimension) or qualitative (ranked/described per dimension). Tier 3 commits require quantitative scoring with weights documented per commitment_type.

### 2.3 Stress-Test

Subject the leading path to adversarial review by the appropriate machinery:

- *Judge* — funder-rubric scoring; cross-family
- *Logician* — deterministic policy gates; fail-closed; zero-token
- *Code Thesis Committee* — cross-family code review (build-side commits)
- *Operational Committee* — cross-family operational consultation (post-build commits with multiple defensible paths)
- *Capital Logic Card rubric* — funder-worldview-specific stress-test
- *Operator review* — for commits requiring operator-voice judgment

The stress-test asks: "What does the leading path miss? What's the strongest counter-argument? What's the failure mode that wasn't surfaced in compare?"

If stress-test surfaces a substantive issue, the leading path returns to *compare* with the issue as a new dimension; or the path is rejected and a different candidate is promoted; or all candidates are rejected and a new exploration round begins.

### 2.4 Commit

Select, reject, defer, or escalate — with a traceable reason.

- *Select* — this path becomes the commitment; downstream work proceeds
- *Reject* — this path is documented as considered-and-rejected; reason captured
- *Defer* — commit blocked pending external input (operator, advisor, missing data); deadline tracked
- *Escalate* — commit exceeds Midas/persona authority; routed to operator with proposed action

A commit is not a commit until the deliberation_trace.jsonl row is written and (where Tier 3 applies) Logician validates.

## 3. Application Surfaces

The doctrine applies to all meaningful commitments. Examples:

| Surface | Domain |
|---|---|
| Proposal direction (Scribe lead-framing) | Grant lifecycle |
| Grant pursuit/no-pursuit decisions (Scout shortlisting) | Grant lifecycle |
| Capital Logic Card weighting in active session | Grant lifecycle |
| Final draft readiness | Grant lifecycle |
| Budget strategy | Grant lifecycle |
| Post-award reporting position | Grant lifecycle |
| Engineering patches > narrow-edit | Forge |
| Persona updates / version bumps | Forge |
| Architecture LOCK | Forge |
| Logician policy changes | Forge |
| Midas maintenance actions touching public surface | Forge |
| Lesson append (lessons.md) | Workspace |
| Blueprint amendment proposal | Workspace |

Trivial low-stakes commits exempt: internal variable naming, micro-rephrasing, narrow-edit refactors that don't change public API, daily_log routine entries, telemetry row writes.

## 4. Enforcement Tiers

The doctrine is tiered by stakes, not uniform.

### Tier 1 — Cultural

Persona prompts must follow the explore→compare→stress-test→commit shape. No external trace artifact required; the discipline lives in the prompt structure and the persona's self-audit step.

**Application examples:**
- Scout shortlisting candidates (consider alternatives before recommending)
- Editor suggesting clarity edits within a draft section
- Midas during routine triage that resolves to a narrow-edit
- Day-to-day spec-card execution where the spec already represents a deliberated commit

**Validation:** none structural. Persona's signature block records the deliberation in narrative form ("considered X and Y, chose X because…").

### Tier 2 — Procedural

The pipeline structurally generates ≥2 candidate paths and scores them before commit. A `deliberation_trace.jsonl` artifact is written per candidate path.

**Application examples:**
- Scribe final draft direction (≥3 framings, Judge ranks, top-1 commits)
- Capital Logic Card weighting decisions in a multi-card-active session
- Spec card authorship by Midas (≥2 implementation approaches considered)
- Operator-facing recommendation
- Operational committee dispatch (the committee output IS the stress-test for a Tier 2 commit)

**Validation:** deliberation_trace.jsonl exists; ≥2 rows; selected candidate has decision="selected"; rejected candidates have decision_reason.

### Tier 3 — Structural

Logician fail-closes on commits without a valid deliberation_trace.jsonl artifact and operator authorization. Failure code: `M-NO-DELIBERATION-RECORD`.

**Application examples:**
- Architecture LOCK (any v0.x → v0.x+1)
- Persona registry changes (any current_version, current_path, allowed_modes, active_status field)
- Post-advisor promotion events (King Midas → autonomous post-build operations)
- Logician policy changes (new F-* code, modified gate threshold)
- Client data-boundary exception (engineering persona reads client PROJECT_CONTEXT)
- Blueprint amendment LOCK
- Real-engineer validation gate transitions
- Doctrine amendment (this document's own LOCK)

**Validation:** Logician runs `validate_deliberation_trace(round_id)` before LOCK accepts. Fail → M-NO-DELIBERATION-RECORD; commit blocked; operator notified.

## 5. The Deliberation Trace Artifact

Schema (one JSONL row per candidate path):

```json
{
  "round_id": "string",
  "commitment_type": "proposal_direction | draft_commit | spec_card | patch | lock | escalation | card_weighting | doctrine_amendment | persona_registry | architecture_lock | blueprint_amendment | lesson_append",
  "tier": "1 | 2 | 3",
  "candidate_id": "option_a | option_b | ...",
  "option_summary": "one-sentence description of the path",
  "evidence_summary": "what supports this path materially",
  "active_cards": ["card_id_1", "card_id_2"],
  "score": "number (Tier 3 quantitative) | string (Tier 2 qualitative) | null (Tier 1)",
  "score_dimensions": {
    "evidence": "...",
    "fit": "...",
    "risk": "...",
    "cost": "...",
    "timing": "...",
    "reversibility": "...",
    "soul_alignment": "..."
  },
  "risk_notes": ["string array of named risks"],
  "stress_test_result": "passed | concerns | block | not_applicable",
  "stress_test_machinery": "judge | logician | code_committee | operational_committee | capital_logic_card | operator | none",
  "decision": "selected | rejected | deferred | escalated",
  "decision_reason": "why this decision",
  "expedited": "boolean",
  "human_authority": "pending | approved | rejected | not_required",
  "timestamp_iso8601": "string"
}
```

**Storage:** `<round>/deliberation_trace.jsonl`

`<round>` resolves to:
- `pipeline/validation/code_reviews/<round_id>/` for build-side code commits
- `pipeline/validation/operational_reviews/<round_id>/` for post-build operational commits
- `pipeline/drafts/<draft_id>/` for grant proposal commits
- `pipeline/architecture/v0.1/<lock_id>/` for architecture commits
- `pipeline/personas/<persona>/<change_id>/` for persona registry commits

**Validation:** Logician's `validate_deliberation_trace(round_id)` checks:
- File exists and is parseable JSONL
- ≥2 rows for Tier 2 expedited; ≥3 rows for Tier 2 normal; ≥N rows per commitment_type config for Tier 3
- Each row has all required fields populated (no nulls in non-optional fields)
- Exactly one row has decision="selected" OR no row has decision="selected" with all rows decision="rejected"/"deferred"/"escalated" (full-rejection commits surface to operator)
- selected row has stress_test_result in {"passed", "concerns_with_mitigation"} — not "block"
- expedited:true rows require operator signature in `<round>/operator_signature.json`

## 6. Expedited Mode

The doctrine survives deadline pressure by compressing, not by being bypassed.

**Conditions for expedited:**
- Operator declares expedited mode for this round (signed authorization)
- ≥2 candidate paths (not N)
- Qualitative scoring allowed in lieu of quantitative
- Abbreviated stress-test (single-machinery instead of multi-machinery)
- Trace row tagged `"expedited": true`
- Operator signature file present at `<round>/operator_signature.json`

**Conditions where expedited is NOT allowed (must use full doctrine):**
- Architecture LOCK
- Persona registry change with `active_status` field modification
- Real-engineer validation gate transition
- Logician policy change introducing new F-* code
- Doctrine amendment (this document's own LOCK)

**Bypassing the doctrine entirely** (no trace artifact, no candidate paths, no stress-test) **is a Five-Laws-of-the-self violation**. Auto-suspension under v2.1 §15 revocation kill-switch.

## 7. Failure Codes

| Code | Trigger | Action |
|---|---|---|
| `M-NO-DELIBERATION-RECORD` | Tier 3 commit attempted without deliberation_trace.jsonl | halt; operator notified; commit blocked |
| `M-INSUFFICIENT-CANDIDATES` | Tier 2 with <2 candidates (expedited) or <3 (normal); Tier 3 with <N per config | halt; commit blocked |
| `M-DELIBERATION-TRACE-INVALID` | Schema validation failure on trace row | halt; commit blocked; trace returned to author for fix |
| `M-EXPEDITED-WITHOUT-AUTHORIZATION` | Expedited:true without operator_signature.json | halt; commit blocked |
| `M-STRESS-TEST-BYPASSED` | Selected candidate has stress_test_result="not_applicable" or null on Tier 2/3 commit | halt; stress-test required |
| `M-EXPEDITED-PROHIBITED` | Expedited:true on a commitment_type in §6 prohibited list | halt; full doctrine required |

These codes are part of the M-* failure code namespace defined by King Midas's §12c charter. Logician enforces them at Tier 3 commit boundaries.

## 8. Relationship to SOUL.md

The Five Operating Laws (SOUL.md) govern *what* Tilth is allowed to claim, scope, contain, speak, and represent — substantive constraints. This doctrine governs *how* Tilth arrives at its commitments — procedural discipline. They are complementary; neither subsumes the other.

**SOUL.md amendment** (operator-authored when this doctrine LOCKs at v1.0):

> ## Pre-Commit Deliberation
>
> The system follows the Pre-Commit Deliberation Doctrine. Every meaningful commitment is preceded by exploration of alternatives, comparison against evidence, stress-testing of the leading path, and a committed decision with a traceable reason.
>
> See `pipeline/doctrines/pre_commit_deliberation.md`.
>
> The Five Operating Laws govern what is allowed; the Doctrine governs how decisions are made. Both apply to every layer.

This paragraph is not auto-applied. The operator decides when the doctrine is mature enough to wire into SOUL.md.

## 9. Application by Persona / Layer

| Persona / Layer | Tier 1 use | Tier 2 use | Tier 3 use |
|---|---|---|---|
| Scout | Routine candidate consideration | Shortlist commits | Pursuit-cohort lock |
| Scribe | Section-level rephrasing | Final draft direction (≥3 framings) | — |
| Editor | Clarity suggestions | — | — |
| Judge | Provides stress-test capability | Cross-rubric scoring | — |
| Logician | — | — | Enforces Tier 3 structural; deterministic |
| King Midas (build) | Spec-card execution within scope | Spec-card authorship | Architecture/blueprint/persona-registry locks |
| King Midas (post-build) | Routine narrow-edits, nightly auto-remediation | Spec card drafting, operational committee dispatch | Doctrine/architecture amendment proposals, persona registry changes, post-advisor promotion |
| Capital Logic Cards | — | Card-rubric stress-test of candidate paths | — |
| MyCel (Stage 2+) | — | Multi-dimensional thought exploration interface | — |

## 10. Capital Logic Cards Under the Doctrine

Each card participates in pre-commit deliberation as a domain-specific exploration and stress-test machinery. Cards are not personalities; they are deliberation engines. Examples (illustrative; canonical card schemas live under `pipeline/cards/`):

**Mandate Guardian** — explores public-mandate / compliance / risk-reduction framings. Scores eligibility, public purpose, documentation, civic outcomes. Stress-tests against private-benefit risk, procurement weakness, public accountability gap.

**Transformation Weaver** — explores human-change / equity / community-voice framings. Scores access, dignity, lived experience, outcome clarity. Stress-tests against savior tone, vague impact, weak community leadership.

**Market Scout** — explores customer-demand / revenue / value-added-product framings. Scores buyer clarity, margin, channel, demand evidence. Stress-tests against unrealistic projections, missing buyer, weak distribution.

When multiple cards are active in a session, the deliberation_trace.jsonl includes per-card scoring per candidate path, allowing cross-worldview comparison.

## 11. MyCel Under the Doctrine

In v0.1, project-thought exploration runs through Tilth's core council (Scout discovery, Scribe framing, Judge scoring, Logician policy gates). MyCel is a Stage 2+ advanced thought-design instrument that productizes pre-commit exploration into a multidimensional interface — but the doctrine itself does not depend on MyCel.

Tilth Core practices the doctrine through the council pipeline. MyCel extends the practice into a deeper exploration surface for projects with significant strategic complexity. v0.1 ships without MyCel; the doctrine still applies.

## 12. Versioning and Amendment Discipline

This doctrine evolves through versioned amendments. The Five Laws (SOUL.md) remain frozen.

- v0.1 — initial draft (this document)
- v0.x — amendments before v1.0 lock
- v1.0 — first locked release; gated on operator review + real-engineer advisor input + first round of dogfood evidence

Amendments to this doctrine are themselves Tier 3 commits — the doctrine applies to its own evolution. M-NO-DELIBERATION-RECORD enforces this recursively: amending the doctrine without a deliberation trace is forbidden by the doctrine.

## 13. The Buyer-Facing Sentence

> Golden Quill does not replace judgment. It structures judgment before commitment.

This sentence belongs in the cover material, the foundation/CDFI infrastructure pitch, and the first paragraph of any Tilth product description. It answers two questions in one breath: it is not AI replacement (judgment stays human) and it is not AI slop (judgment is structured, not hand-waved).

---

*v0.1 — 2026-04-29 — initial draft. References: SOUL.md, pipeline/engineering/king_midas_implementation_prompt_v2_1.md, pipeline/engineering/king_midas_12c_post_build_charter.md*
