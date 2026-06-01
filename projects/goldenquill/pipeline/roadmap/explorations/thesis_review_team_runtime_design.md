# Design Note — Thesis Review Team (TRT), Runtime Board for Drafted Grant Sections

**Status:** EXPLORATION — design intent LOCKED (Option B + strong cross-family + 3-role match per session 2026-05-06)
**Stage:** v0.2
**Created:** 2026-05-06
**Origin:** session 2026-05-06 with Josh

---

## Doctrine

Tilth was built with a thesis review board. Every architecture decision, spec card, and locked module passed through a multi-seat cross-family review committee before LOCK. That discipline is the reason v0.1 is trustworthy.

**The same discipline is required for grants.** A solo Scribe is not trustworthy — no matter which family it comes from. Quality is not produced by trusting the model; quality is *mechanized* through cross-family adversarial review. If the standard for code is "five reviewers from different families before LOCK," the standard for grants going to a federal agency cannot be lower.

> **"How else do we know we have good quality output — trust Claude?"** — Josh, 2026-05-06

The Thesis Review Team is the runtime answer.

## Topology — Option B (LOCKED design intent)

The TRT is a **separate runtime board with its own seat bindings**, distinct from the runtime Council Editor and Council Judge. Three seats, three roles, three model families, none matching Scribe's family.

### Why separate seats (not Council Editor/Judge in a different mode)

The engineering Thesis Team uses separate model bindings from the CTC reviewers. That separation is what makes the review independent — a reviewer's mental model is different when they are the "thesis review" rather than the "operational seat." Mirroring this in runtime gives:

- **Independence** — TRT seats see a clean section, not the section they helped shape during drafting.
- **Family diversity at the review layer** — Council Editor and Judge may share a family with Scribe (within cross-family rules); TRT enforces a stricter three-family-different-from-Scribe invariant.
- **Mode clarity** — Council Editor's job is whole-draft clarity polish at SP3/SP4; TRT-Editor's job is per-section adversarial voice review at SP2. Different modes, different seats, different artifacts.

The cost is one extra runtime call per section per seat — three calls per section. Acceptable given the stakes.

## Cross-Family Rule — Strong (LOCKED)

**TRT seats must come from three different model families, none matching Scribe's family.**

| Scribe (BYOK drafter) | TRT seats (3 different non-Scribe families) |
|---|---|
| Opus 4.7 (Anthropic) | OpenAI + Google + Meta (example) |
| ChatGPT 5.5 (OpenAI) | Anthropic + Google + Meta (example) |
| Future drafter (Google?) | Anthropic + OpenAI + Meta (example) |

Family roster currently in scope: OpenAI, Anthropic, Google, Meta, Alibaba, Moonshot.

The router selects three at runtime based on Scribe's BYOK binding. Selection logic captured in `router.yaml`.

## Three Roles (LOCKED)

Mirrors the engineering Thesis Team structure (Editor / Judge / Red Team) adapted for grant drafting.

### TRT-Editor

**Focus:** voice, clarity, dialect adherence (Law 4 axis a).
**Probes:**
- Does the section's voice match the locked spine's `dialect_register`?
- Are admin-risk terms in `admin_risk_terms_avoid` absent?
- Are admin-risk terms in `admin_risk_terms_in_use` consistently rendered?
- Is the section readable to a non-specialist reviewer?
- Are jargon and acronyms either defined or replaced?

### TRT-Judge

**Focus:** rubric scoring against the funder's rubric, evidence verification.
**Probes:**
- For each rubric criterion this section addresses, what score would a hostile reviewer give it?
- Where are the evidence anchors weakest (claim with no KFR-backed fact, claim with no RFA anchor)?
- Does the section's quantitative substance match KFR (cross-check)?
- Does the section's strategic claims match the locked spine's framings?

### TRT-Red-Team

**Focus:** adversarial probe — where is the section weakest?
**Probes:**
- What would a hostile reviewer pick at?
- What unstated assumption could break the section's argument?
- Where does the section invite eligibility scrutiny it doesn't need to invite?
- What single claim, if removed, would make the section stronger?
- What competing applicant could match this claim — and how would Tilth's section differentiate?

## Cycle — L-005 Two-Audit (LOCKED)

```
Scribe drafts section v1
  ↓
TRT Audit #1 (3 seats parallel)
  ↓ findings emitted
SP2: operator reviews TRT findings alongside section v1
  ↓ operator picks which findings Scribe acts on
Scribe revises → section v2
  ↓
TRT Audit #2 (verify findings addressed)
  ↓
  ├─ all addressed → promote forward
  └─ unresolved → escalate to operator (no silent third round per L-005)
```

No silent third round. Two audits, then operator decides.

## SP2 — Operator Stop Point (between audits)

The operator review surface at SP2 captures:

- The drafted section v1
- TRT Audit #1 findings from all three seats, structured by severity
- The operator's decisions on which findings Scribe will act on (each finding: address / defer / dismiss with reason)
- Optional spine amendments if a discovered framing should propagate forward (rare — re-locks the spine)

Output artifact: `orgs/<org>/grants/<grant_id>/sections/<section_id>/sp2_review.yaml`.

## Output type — Advisory, Not Gate-Keeping

TRT findings are **advisory**, not gates. They flow into Scribe's revision loop via operator review. They do not pass/fail-block promotion.

Logician's POST-gate battery (verbatim-substring, F-LOGICIAN-FABRICATED-ORG, F-LOGICIAN-FACT-DRIFT, F-LOGICIAN-SPINE-DRIFT) does the gate-keeping. TRT does the *guidance*. Distinct functions.

## Connection to existing pieces

| Existing | TRT connection |
|---|---|
| Code Thesis Committee (CTC) | TRT is the runtime sibling of CTC. CTC reviews engineering at LOCK; TRT reviews grants at section boundary. Same DNA, different domain. |
| Council Editor (runtime, whole-draft) | TRT-Editor focuses on per-section adversarial review; Council Editor focuses on whole-draft clarity polish at SP3/SP4. Different scopes. |
| Council Judge (runtime, scoring) | TRT-Judge does per-section rubric probe at SP2; Council Judge does final whole-draft scoring after Editor pass. Different scopes. |
| Council Logician (gate-keeping) | TRT is advisory; Logician is fail-closed. TRT findings inform; Logician enforces. |
| L-003 cross-family rule | TRT applies the strong version: three different families, none matching Scribe. |
| L-005 two-audit cycle | TRT applies it per section. Audit #1 → operator review → revision → Audit #2 → promote or escalate. |
| Narrative Spine | TRT seats read the spine and check section adherence. Spine drift identified at TRT becomes a Scribe revision instruction. |
| Key Facts Register | TRT-Judge cross-checks numeric claims against KFR. Numeric drift surfaces at TRT before Logician's hard gate fires at promotion. |

## Cost considerations

Per section: 3 calls Audit #1 + (operator review + Scribe revision) + 3 calls Audit #2 = 6 model calls.
For a 10-section grant: 60 TRT calls + Council Editor + Council Judge.

This is meaningful BYOK token cost. Two mitigations:

1. **Per-section TRT can be conditional.** Sections that consist primarily of structured facts (budget table, timeline) may not need full TRT pass — operator decides at SP1 which sections require TRT.
2. **Audit #2 can be lighter.** Audit #2 only re-checks findings flagged in Audit #1. If Audit #1 was clean (rare), Audit #2 is skipped.

## Failure modes

- **TRT family unavailable.** If the operator's BYOK keys don't include three non-Scribe families, the strong cross-family rule cannot be satisfied. Router falls back to weak rule (any non-Scribe family) with operator notification, and TRT runs with fewer seats. Logged.
- **TRT seats disagree heavily.** Acceptable — disagreement is signal, not failure (per L-005). Operator reviews divergent findings at SP2. If unresolvable, operator escalates.
- **TRT and Scribe loop indefinitely.** Prevented by L-005 two-audit cap. After Audit #2, escalation is mandatory.

## Open questions

1. **Are TRT findings structured uniformly across the three seats** (same SFR-style verdict format), or each seat has its own format reflecting its role? Lean: same SFR format with role-specific severity dimensions.
2. **Does TRT see the locked spine and KFR**, or just the drafted section? Lean: TRT sees spine + section + relevant KFR subset. Without spine + KFR, TRT cannot detect drift, only voice issues.
3. **Per-section TRT vs whole-draft TRT** — purely per-section as stated, or do we add a whole-draft TRT pass after SP3 (between Editor and Judge)? Lean: per-section only at v0.2; revisit if per-section reveals coordination gaps that whole-draft would catch.
4. **TRT failure-mode telemetry** — track which TRT seat catches the most findings per section type. Used for router-config tuning (e.g., always use Anthropic seat for adversarial probe on regen-ag grants). Worth instrumenting from day one.

## Non-goals

- TRT is not a Logician replacement. Logician gates are deterministic; TRT is statistical model output.
- TRT is not a Council Editor or Council Judge replacement. Different scopes, different stop points.
- TRT findings are not auto-applied. Operator review at SP2 is non-optional.
- TRT does not modify the spine, the KFR, or PROJECT_CONTEXT.md. Read-only relative to all three.
