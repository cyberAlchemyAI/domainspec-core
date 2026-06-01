# Design Note — Narrative Spine + Human-in-the-Mix Stop Points

**Status:** EXPLORATION (operator-approved design intent; not yet specced)
**Stage:** v0.2
**Created:** 2026-05-06
**Origin:** session 2026-05-06 with Josh

---

## Doctrine

**Nothing in Tilth is automated end-to-end.** Defining human-in-the-mix stop points is a critical component of the system, not a nice-to-have. The time saved by stopping and tightening language and focus to create accurate outputs is far greater than the time required to remediate a memory contaminated with bad data downstream.

This is doctrine, not preference. Every seat operates inside a chain of explicit operator stop points. The operator is not a reviewer of finished work — the operator is a gate at every defined transition.

## Problem

Scribe drafts grant sections sequentially. Today, the funder-attractive framing identified at KGIE preflight tends to drift across sections — Section 3 silently reframes what Section 1 nailed, revisions silently lose the winning gambit, and contaminated context propagates forward. The operator notices on the third pass and has to remediate retroactively.

What's missing: a persistent artifact that holds the funder-attractive framings, is operator-approved, and is read-only at every section so Scribe can't drift away from it.

## The Narrative Spine

A **per-grant, operator-approved artifact** that holds the strategic thread of the application. Locked at SP1 after KGIE, read-only during drafting, enforced by Logician.

### Schema (sketch)

```yaml
grant_id: vapg_fy26_mycosymbiotics
locked_at: 2026-05-06T14:00:00Z
locked_by: operator

funder_attractive_framings:
  - id: framing-001
    claim: "Worker-owned cooperative scaling regenerative mushroom production"
    rationale: "VAPG explicitly values value-added activity by producer-owners"
    rfa_anchor: "VAPG FY26 §3.A.2"
  - id: framing-002
    claim: "On-farm processing creates 4x value capture"
    rationale: "VAPG rewards measurable economic uplift"
    rfa_anchor: "VAPG FY26 §3.B.1"

dialect_register: progressive  # Law 4 axis (a)
admin_risk_terms_in_use: []    # Law 4 axis (b) — none flagged
admin_risk_terms_avoid: ["DEI", "equity-centered"]  # operator-locked at SP1

smart_outcome_shape:
  primary: revenue_uplift
  secondary: jobs_created
  tertiary: market_diversification

strategic_emphasis:
  lead_with: workforce_metrics
  de_emphasize: yield_data
  rationale: "VAPG reviewers respond to economic + workforce; yield reads as production-grant noise"

cross_section_anchors:
  - methods_must_mirror: ["framing-001", "framing-002"]
  - outcomes_must_mirror: ["smart_outcome_shape.primary"]
  - budget_justification_must_cite: ["framing-002"]
```

### Properties

- **Operator-approved, not Scribe-generated.** Scribe proposes spine candidates from KGIE output. Operator reviews, edits, approves. Spine artifact written to disk on approval.
- **Read-only during drafting.** Scribe references spine at every section start. Cannot modify it.
- **Logician enforces.** Drift = `F-LOGICIAN-SPINE-DRIFT`, deterministic, fail-closed.
- **Versioned.** Spine has its own version history. Mid-grant amendments require operator re-lock.

## Four Stop Points (SP1-SP4)

Each stop point is an artifact-on-disk, not a chat prompt. Uniform review surface across sessions. Operator can revisit any stop point's artifact later for audit.

### SP1 — Spine Lock

**When:** After KGIE preflight. Before any drafting.
**What operator does:** Reviews proposed funder-attractive framings, dialect register, SMART outcome shape, strategic emphasis, admin-risk term register. Edits as needed. Approves and locks.
**Output artifact:** `orgs/<org>/grants/<grant_id>/spine.locked.yaml`
**What happens next:** Scribe begins drafting Section 1.

### SP2 — Section Boundary

**When:** After each Scribe section draft is produced. Before Scribe moves to next section.
**What operator does:** Reviews TRT findings (per `thesis_review_team_runtime_design.md`) alongside the drafted section. Sees what spine elements Scribe carried forward and how it strengthened them. Adjusts before continuing — flags drift, picks which TRT findings Scribe acts on, edits the spine itself if a discovered framing should propagate forward.
**Output artifact:** `orgs/<org>/grants/<grant_id>/sections/<section_id>/sp2_review.yaml` — operator decisions captured.
**What happens next:** Scribe revises section per operator-approved findings, then moves to next section.

### SP3 — Pre-Editor / Confidence Declarations

**When:** After all sections drafted. Before runtime Council Editor passes whole-draft clarity review.
**What operator does:** Reviews Scribe's per-section confidence declarations (FWHP "I do not know" discipline). Sections marked low-confidence get explicit operator review before Editor runs. Operator either approves the section as-is, edits it, or sends back to Scribe.
**Output artifact:** `orgs/<org>/grants/<grant_id>/sp3_confidence_review.yaml`
**What happens next:** Editor runs whole-draft clarity pass.

### SP4 — Post-Editor / Pre-Judge

**When:** After Editor's clarity pass. Before Judge scores against rubric.
**What operator does:** Sees Editor's clarity changes alongside spine adherence delta. Anything Editor moved that drifted the spine surfaces explicitly. Operator approves, reverts, or sends back to Editor.
**Output artifact:** `orgs/<org>/grants/<grant_id>/sp4_post_editor_review.yaml`
**What happens next:** Judge scores. Logician's full gate battery fires (including spine-drift gate). Promotion or escalation.

## Failure Code

`F-LOGICIAN-SPINE-DRIFT` — any Scribe revision or Editor edit that removes, weakens, or contradicts a locked spine element. Deterministic check (string-level cross-reference + framing-id presence). Fail-closed.

## Connection to other layers

| Layer | Scope | Lifetime | Provides |
|---|---|---|---|
| Capital Logic Cards (A6 Option C) | Per funder | Reusable across grants | Funding-relationship strategy |
| Sector Knowledge Packs | Per sector | Reusable across grants | Vocabulary + dialect |
| Key Facts Register (KFR) | Per org | Refreshed on cycle | Validated 5W1H facts |
| **Narrative Spine (this)** | **Per grant** | **Single-use** | **Strategic thread** |

All four operator-curated. None Scribe-generated. The spine is the per-grant glue that ties the others to a specific application.

## Candidate Lesson

**L-XXX — Cost of stopping at SP < cost of remediating contaminated memory downstream.**

- **Frequency:** observed across multiple grants (Josh, 2026)
- **Severity:** HIGH
- **Pattern:** When operator skips a defined stop point to keep momentum, downstream sections accumulate framing drift. By the time the issue surfaces, Scribe's working context contains the bad framing as ambient truth, and remediation requires either restarting drafting or surgical context corrections that often miss instances. Time cost of remediation typically exceeds 5x the time saved by skipping the stop point.
- **Pre-check:** Every Scribe drafting session must declare which stop points apply and confirm operator has acknowledged each before proceeding past it. SP-skip requires explicit operator override, logged.
- **Origin:** Session 2026-05-06 with Josh.

Promote to numbered Lesson in `lessons.md` when the design lands.

## Open questions

1. Spine schema — YAML (proposed) vs JSON vs markdown with structured frontmatter? YAML balances operator-readability with machine-parseability.
2. Mid-grant amendment workflow — when operator discovers a stronger framing at SP2, should the spine be amendable (with re-lock) or strictly immutable post-SP1?
3. Multi-grant sequence — when an organization applies for related grants in a series, does the spine carry framings forward as a starting template, or is each grant's spine fully fresh?
4. Spine adherence as Judge dimension — should Judge add "spine adherence" as a 13th rubric dimension, or is Logician's deterministic gate sufficient?

## Non-goals

- Not a replacement for KGIE preflight. Spine is the *output* of KGIE plus operator approval, not a substitute.
- Not a Scribe writing aid. Scribe still does its own drafting with its own primitives. The spine is the constraint, not the content.
- Not auto-generated. Operator approval at SP1 is non-optional.
