# Design Note — Key Facts Register (KFR)

**Status:** EXPLORATION (operator-approved design intent; not yet specced)
**Stage:** v0.2 — high priority. Quantitative substance is foundational.
**Created:** 2026-05-06
**Origin:** session 2026-05-06 with Josh

---

## Doctrine

Bad numbers in a grant are not a quality problem — they are an audit-finding, clawback, "you lied to a federal agency" problem. Worst-case cost is orders of magnitude higher than narrative drift. The system cannot be trustworthy if its quantitative substrate is freeform.

Every quantitative claim Scribe makes must trace to a validated, confirmed, time-bounded entry in a structured register. No exceptions.

## Problem

Today, PROJECT_CONTEXT.md holds organizational facts as freeform fields with `[NEEDED]` markers. That works for narrative substance (mission, history, partnerships) but is inadequate for quantitative claims:

- No temporal validity — a 2024 enrollment number can be silently reused in a 2026 grant
- No validation chain — no record of who confirmed the fact, when, against what source
- No comparison anchors — projected vs actual not differentiated; peer benchmarks absent
- No expiry — stale facts not flagged before reuse
- No structured query — can't answer "give me all facts this RFA's questions require"

Result: Scribe pulls numbers from contextual cues, occasionally drifting from PROJECT_CONTEXT, occasionally inventing plausible-sounding figures. Logician's existing verbatim-substring gate catches some drift but treats numbers as opaque strings, missing semantic mismatches (200 vs 189) and unable to enforce temporal validity.

## The Key Facts Register

A **per-org structured register of validated 5W1H facts** with temporal validity, validation chain, and comparison anchors. The single source of truth for any quantitative claim a grant makes about the organization.

### File location

```
orgs/<org>/key_facts_register.yaml
```

One per org. Versioned. Operator-curated.

### Schema (per fact)

```yaml
- id: enrollment_2025_2026
  who: Dogwood Charter School
  what: Student enrollment
  when:
    period: 2025-2026 academic year
    as_of: 2025-10-01
    expiry: 2026-10-01  # next official count refreshes
  where: PA, Allegheny County
  why: PA DOE October official count
  how: PIMS submission, audited by district
  value: 247
  unit: students_FTE
  projection_or_actual: actual
  comparison_anchor:
    type: prior_year_actual
    value: 231
    delta_pct: 6.9
  benchmark:
    peer_charter_avg_ay_2024_2025: 215
    peer_source: PA Charter School Association 2024 Annual Report
  validation:
    confirmed_by: operator
    confirmed_at: 2026-04-15
    source_doc: orgs/dogwood_school/assets/PIMS_Oct2025_official.pdf
    source_doc_hash: sha256:abc123...
  confidence: HIGH
  notes: |
    Official PA DOE count. Reusable for any grant in current academic year.
    Refresh required before 2026-10-01 expiry.
```

### Schema (per credential)

```yaml
- id: ed_director_credentials
  who: Jane Doe
  what: Education Director credentials
  when:
    period: ongoing
    as_of: 2024-08-15
    expiry: null  # PhD does not expire; license does — separate fact
  where: PA
  why: position requirements + grant key-personnel sections
  how: degree verification + state license check
  value: PhD, M.Ed, PA Principal Certification
  unit: credentials_list
  projection_or_actual: actual
  validation:
    confirmed_by: operator
    confirmed_at: 2026-04-15
    source_doc: orgs/dogwood_school/assets/credentials/jane_doe_credentials_packet.pdf
  confidence: HIGH
```

### Schema (per budget line)

```yaml
- id: org_operating_budget_fy2025
  who: Dogwood Charter School
  what: Total operating budget
  when:
    period: FY2025 (July 2024 - June 2025)
    as_of: 2025-08-01
    expiry: 2026-08-01
  where: organizational
  why: audited financial statements
  how: external audit by [auditor]
  value: 4_287_000
  unit: USD
  projection_or_actual: actual
  comparison_anchor:
    type: prior_year_actual
    value: 3_950_000
  validation:
    confirmed_by: operator
    confirmed_at: 2026-04-15
    source_doc: orgs/dogwood_school/assets/audit_FY2025.pdf
  confidence: HIGH
```

### Required fields (every fact)

- `id` — stable, lowercase, snake_case
- `who`, `what`, `when` (period + as_of + expiry), `where`, `why`, `how`
- `value`, `unit`
- `projection_or_actual` — never ambiguous
- `validation` block — confirmed_by, confirmed_at, source_doc
- `confidence` — HIGH / MEDIUM / LOW

### Optional fields

- `comparison_anchor` — prior year, projection-vs-actual, baseline
- `benchmark` — peer comparison
- `notes` — operator commentary

## Pipeline Behavior

### SP0 — KFR Freshness Review

**When:** Before KGIE preflight. First operator stop point in the grant flow.
**What operator does:**
1. Sees list of facts in KFR with their expiry status (current / expiring soon / expired).
2. Reviews list of fact-IDs the RFA's structured questions require (auto-derived from rubric scan).
3. Refreshes any expired facts (operator updates value + as_of + validation).
4. Fills any RFA-required gaps (creates new KFR entries).
5. Confirms KFR is ready for this grant.
**Output artifact:** `orgs/<org>/grants/<grant_id>/sp0_kfr_review.yaml`
**What happens next:** KGIE preflight runs.

### Scribe consumption

Before drafting any quantitative claim, Scribe queries KFR:

```
get_fact(id="enrollment_2025_2026")
  → returns full structured fact
get_facts_for_rfa_section(section_id="3.A.2")
  → returns all KFR entries that section's rubric questions require
```

Scribe's drafting context is augmented with the structured facts. Numbers in the draft must trace to a returned fact's `value` field.

### Logician POST-gate — `F-LOGICIAN-FACT-DRIFT`

For every numeric claim in the Scribe draft:
1. Extract number + surrounding context (subject, units).
2. Match to a KFR fact (by `who` + `what` + temporal validity).
3. Verify draft number = KFR `value` within tolerance (default 0% — exact match required).
4. If no matching KFR fact, gate fails.
5. If matching fact but value differs, gate fails with both values shown.

Operator can override individual findings via M13 bypass (audited) — used for legitimate derivations (e.g., draft says "approximately 250 students" when KFR says 247; operator approves the rounding).

## Connection to existing pieces

| Existing | KFR connection |
|---|---|
| PROJECT_CONTEXT.md `[NEEDED]` numeric fields | Migrate to KFR with proper structure. PROJECT_CONTEXT keeps narrative substance only. |
| Law 5 verbatim-substring gate | Catches fabricated string credentials. KFR catches numeric drift. Sibling gates. |
| F-LOGICIAN-FABRICATED-ORG NER gate | Catches fabricated organizations. KFR catches fabricated/drifted numeric facts. |
| Explain-grounding diagnostic | Sentences with numbers cross-reference against KFR specifically. Far higher signal than freeform PROJECT_CONTEXT. |
| Narrative Spine | Spine holds *strategic framings*. KFR holds *quantitative substance*. Spine's `cross_section_anchors.budget_justification_must_cite` reference framing IDs; KFR provides the numbers those framings rest on. |

## Multi-grant consistency

Same fact reused across grants — but versioned source-of-truth means you cannot have one grant claim 200 graduates and another claim 189 in the same year. KFR is the source; both grants pull the same `value` field. If a grant needs a different framing of the same number (e.g., "200" vs "approximately 200"), that's a Scribe presentation choice, not a fact change.

## Open questions

1. **Format** — YAML (proposed) vs JSON vs markdown with structured frontmatter. YAML balances operator-readability with machine-parseability. Validation via JSON Schema.
2. **Tolerance for numeric matching** — exact (0%) by default seems right, but some grant questions want rounded figures. Operator-overridable per fact via `display_tolerance_pct: 5` field?
3. **Per-grant subset** — should Scribe see the whole KFR (manageable for small registers) or a grant-specific subset auto-derived from the RFA? Subset pattern reduces context budget but adds derivation complexity.
4. **Cross-org benchmarks** — peer benchmarks (state averages, comparable charters) sometimes apply across orgs. Per-org KFR entries duplicate them; a separate `pipeline/benchmarks_register.yaml` could hold cross-org benchmark facts. Lean: same KFR, dedup acceptable for now.
5. **Refresh cadence** — fact-level expiry handles per-fact refresh, but should there be an org-level annual review event (e.g., every July, operator does a full KFR audit)?

## Non-goals

- Not a database. YAML files in version control. Diff-friendly, audit-friendly, sovereignty-friendly.
- Not auto-populated by Scribe. Operator-curated, full stop.
- Not a replacement for source documents. Source docs live alongside (in `assets/`); KFR holds the validated extract.
- Not a substitute for grant-specific custom data — those still live in PROJECT_CONTEXT or per-grant context files.
