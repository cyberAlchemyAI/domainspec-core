# TILTH-CIC-02 Educator — Amendment Proposal 2026-05-16

**Status: STAGED — NOT YET DISPATCHED**
**Source: operator-supplied content 2026-05-16 (Cowork session)**
**Target: next L-005 dispatch round following the THESIS_PASSED state set 2026-05-15.**
**Discipline: does NOT edit `pipeline/cards/CIC/educator.yaml` in place. The card is thesis-passed; in-place edits would invalidate `cross_family_thesis_status: passed` and force a new audit round outside the intended dispatch cadence.**

This doc collects operator-actionable additions surfaced during a Cowork session where the operator presented a draft Education Capital Logic Card and an Educator Client Information Card. The cross-cutting content (reviewer heuristics, score-upgrade logic, drafting strategy, denial-feedback distillation, capital-stacking patterns) was orthogonal to CIC content and landed in `skills/scribe-ghostwriter/references/reviewer_heuristics.md`. This file collects what remains — Educator-specific items that should be evaluated for the next Educator dispatch.

---

## Item A — Operator-decision items previously surfaced by FINAL_VERDICT 2026-05-15

The Wave 2 Educator FINAL_VERDICT named five operator-decision items that did not block THESIS_PASSED but were flagged for operator resolution. The 2026-05-16 operator content overlaps with three of them. Operator input requested:

### A.1 — PA-specific funders state-overlay (DEFERRED v1.x)

The card carries three PA-anchored funder entries (PDE, PCCD, PHEAA) without a state-overlay mechanism. Cross-card concern. The operator's 2026-05-16 draft did not introduce new PA-specific funders but also did not propose a state-overlay design. **Decision still deferred to v1.x cross-cutting amendment with sibling CICs.**

### A.2 — Walton Family Foundation explicit naming

Cycle 1 F-02 fold removed all named third-party orgs from `dialect_routing_table.example_funder`. The Wave 1 food_systems precedent allows named-org references to be RESTORED with URL citation under `_research_metadata.priors_consulted` (Soul Fire / NEFOC LT pattern). The 2026-05-16 operator content did not name specific funders inside the funder grammar layer — it described funder types ("public charter or public school launch," "venture philanthropy education," "learning differences and inclusive education," etc.). This is consistent with the post-L-005 card state. **Recommended: keep named-org references off the main card; if operator wants the priors_consulted research-metadata pattern populated, dispatch separately.**

### A.3 — "Gender identity" substitution candidate "biological sex (where statutorily required per EO 14168)"

The 2026-05-16 content did not address this directly. **Decision still pending operator dispatch.**

### A.4 — Title IX framework regulation-in-flux flagging

The 2026-05-16 content did not address Title IX directly. The card's existing flag ("Per active federal-regulation cycle: Tilth flags Title IX as a regulatory-environment-in-flux compliance area") remains. **Recommended: revisit on Title IX rule stabilization, not in this amendment cycle.**

### A.5 — Reviewer-context softening Wave-2 precedent for sibling CICs

The Educator Cycle 1 F-04 fold established the Law 4 neutrality posture pattern. Sibling CICs (public_agency, arts_culture, cooperative) carry overlapping admin_risk_term entries with similar EO-framing prose. The 2026-05-16 operator content does not directly enforce this on siblings but its general drafting voice (neutral, descriptive, not partisan) reinforces the pattern. **Recommended: dispatch a sibling-CIC amendment cycle that mirrors the Educator Cycle 1 F-04 fold across the three siblings, scoped narrowly.**

---

## Item B — Candidate additions from 2026-05-16 operator content

The operator content contained three Educator-specific items not currently in the card or only thinly covered. Each is presented as a candidate amendment for operator review — not as a fold-in.

### B.1 — Granular education-data privacy classification defaults

The operator's draft "Hard Gates / education_data_privacy" lists five categories that should default to specific classifications at the card-archetype layer (per the three-layer classification default discipline: card archetype → operator override at white-glove → per-grant SP0 override):

- **FERPA-protected student PII** → confidential (default)
- **IDEA / disability data** → confidential (default; severity HIGH; never sanitized without explicit operator approval)
- **Discipline / attendance data** → confidential (default; severity MEDIUM)
- **Family / student survey raw data** → confidential (default)
- **Sanitized aggregated summaries** → shareable only with explicit operator approval per Classification Review

**Where this lands if accepted:** likely under `register_defaults` (the existing sub_registers block from Cycle 1 F-01) as a `field_classification_defaults` sub-block. Schema work may be needed; if so, this is a §18 schema-refinement-adjacent amendment, not a content-only fold.

**Operator decision needed:** confirm these five defaults are correct as written. Flag any cases where the default should be tier-different (e.g., aggregated attendance might be "shareable" while individual student attendance is "confidential").

### B.2 — Per-client evidence-class enumeration (Evidence Signals quadrant strengthening)

The operator's draft enumerated 11 evidence classes for Educator clients:

1. Eligibility & authorization
2. Student need
3. Instructional model
4. Student experience
5. Educator capacity
6. Leadership capacity
7. Governance
8. Operations
9. Finance & sustainability
10. Community & family engagement
11. Evaluation & continuous improvement

The current card has `evidence_signals` and `metrics_table_template` but does not explicitly enumerate an evidence-class taxonomy at this granularity.

**Where this lands if accepted:** as an `evidence_class_taxonomy` block under the existing `evidence_signals` field, with cross-reference to KFR fact_class names per the Wave 2 schema. Each evidence class would carry: description, example artifacts, KFR fact_class mapping, default classification, hard-gate behavior, and Tilth-seat consumption rule (Scribe, Judge, Logician).

**Operator decision needed:** is an 11-class taxonomy the right granularity, or should related classes collapse (e.g., "leadership capacity" + "governance" → "leadership and governance")? Schema work may be needed.

### B.3 — Educator-specific reviewer heuristic enumeration in card-level reviewer_lens block

The card currently has a `reviewer_lens` block (verify in YAML; field name may differ). The operator's 2026-05-16 draft enumerated 10 reviewer heuristics — most of which are cross-CIC (now in `skills/scribe-ghostwriter/references/reviewer_heuristics.md`). Three of them have specifically Educator-flavored upgrades that may merit card-level enumeration:

- **Inclusion without infrastructure** — Educator-specific upgrade requirements include differentiated instruction strategy, intervention/enrichment tiers, special-education / IEP process, educator training, family-communication protocol, progress monitoring. These are more granular than the cross-cutting version.
- **Shared governance without decision rights** — Educator-specific upgrade requirements include board-vs-school-leader decision boundary (charter governance pattern), committee responsibilities, school-leader-evaluation process, conflict-of-interest policy, succession plan.
- **Compliance without articulation** — Educator-specific upgrade requirements include compliance calendar, designated compliance owner, legal-counsel role, staff training schedule, board review cadence, internal-audit process, corrective-action procedure — all framed under the Educator regulatory stack (ESEA / ESSA, IDEA, Section 504, ADA Title II, FERPA, McKinney-Vento, CIPA, Title IX, state authorizer rules).

**Where this lands if accepted:** as an Educator-flavored extension under the existing reviewer-lens / evidence-signals block. The cross-cutting versions stay in scribe-ghostwriter; only the Educator-specific upgrade content moves to the card.

**Operator decision needed:** confirm these three are worth Educator-specific enumeration, or whether the cross-cutting versions are sufficient. Anti-duplication discipline: any text that appears in both files is a violation.

---

## Item C — Items NOT recommended for card amendment

The following items in the operator's 2026-05-16 draft were evaluated and are NOT recommended for the card:

- **Funder grammars table** (public charter, venture philanthropy, learning differences, teaching reimagined, learning solutions) — already covered by the card's `dialect_routing_table` post-L-005, in canonical political-axis × dialect form.
- **Hard gates: eligibility / required_attachments / compliance / budget** — covered by Logician's deterministic gates (F-CLASS-*, F-LOGICIAN-FACT-*), not card content. Lives in `pipeline/logician/gates/`.
- **Drafting strategy / default voice / avoid-strengthen / response-shape** — cross-cutting; now in `skills/scribe-ghostwriter/references/reviewer_heuristics.md`. Do not duplicate.
- **Score upgrade logic** (absent → emerging → effective → exemplary) — cross-cutting; same scribe-ghostwriter reference.
- **Denial feedback distillation methodology** — cross-cutting; same scribe-ghostwriter reference. The institutional-memory canonical home is `pipeline/institutional_memory/lessons.md` per CLAUDE.md.
- **Capital stacking patterns** (planning → launch, public → philanthropy, denial → resubmission) — cross-cutting and META-level; same scribe-ghostwriter reference. Cannot live on a single CIC without re-introducing CIC → CLC binding (forbidden per F-CIC-CLC-COUPLING-VIOLATION).
- **"Education Capital Logic Card" as a 9th CLC** — rejected. The CLC closed set is eight per architecture v7.0.11 §6.1. Education-related capital flow distributes across the existing eight CLCs (Public Purpose & Works for public-charter / district funding; Catalytic Change for venture philanthropy education and innovation grants; Operating Capacity for capacity grants and launch grants; Research & Evidence for SARE / AFRI / NSF EDU / IES; etc.).
- **"Customer / Client Information Card" as a new card type** — rejected. Per-client information architecture already exists at `orgs/_TEMPLATE/PROJECT_CONTEXT.md` + KFR (`orgs/<slug>/vault/kfr/register.yaml`) + classification register (`orgs/<slug>/vault/classification/register.yaml`). The operator's draft schema duplicates these systems. If the operator wants Educator-flavored extensions to the org template, that's a `orgs/_TEMPLATE/` extension, not a new card type.

---

## Next steps

1. **Operator review of this proposal.** Operator confirms which of Item B candidates (B.1, B.2, B.3) to dispatch in a follow-on Educator amendment cycle.
2. **If any Item B is accepted:** author a v0.2 amendment to `pipeline/cards/CIC/educator.yaml`, dispatch through cross-family L-005 two-cycle review per the Wave 2 thesis pattern, update `cross_family_thesis_status: pending` during dispatch and back to `passed` on completion.
3. **Item A.5 (sibling-CIC reviewer-context softening)** is a separate cross-card dispatch and should be scoped to the three siblings (public_agency, arts_culture, cooperative). Not in scope for this Educator-only amendment.
4. **Cross-cutting content already landed** in `skills/scribe-ghostwriter/references/reviewer_heuristics.md` (this session); no further action required on that file from this proposal.

---

*Authored: 2026-05-16 (Cowork session). Operator review pending.*
