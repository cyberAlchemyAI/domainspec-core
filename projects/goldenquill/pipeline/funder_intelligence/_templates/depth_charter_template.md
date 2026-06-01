# Depth Charter — `<artifact_id>`

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2.
>
> One-page operator-signed charter. Required input to Pillar-2 corpus assembly. **Must be operator-Ed25519-signed before any Pillar-2 work begins.**
>
> **Strong-component bar (canonical 2026-05-18):** every charter answers, concretely, "what should Scribe, Judge, Red Team, Scout, or Logician do differently because this artifact exists?" If §A cannot be populated with concrete decisions, the charter is pre-spec DRAFT and held pending re-authoring.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `<canonical-id, e.g., USDA-RD-RBDG-FY26>` |
| `artifact_family` | `funder` / `program` / `compliance_cascade` / `reviewer_type` |
| `artifact_path` | `pipeline/funder_intelligence/<family>/<artifact_id>.yaml` |
| `charter_authored_by` | `<session id or human name>` |
| `charter_date` | `2026-05-XX` |
| `tied_to_cic_clc_pair` | `food_systems × operating_capacity` (Phase 1 exemplar) or other |
| `phase` | `1 — exemplar pair` / `2 — scale-out` / `3 — Stage-1.5 commons prep` |

---

## §A — Adversarial pre-checks (mandatory; canonical 2026-05-18)

Per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §2. These three blocks gate strong-component status. A charter that cannot populate them concretely is pre-spec DRAFT and held pending re-authoring.

### A.1 `runtime_consumer:` — who reads what, when, and what decision changes

```yaml
runtime_consumer:
  scout:
    reads_fields: []                                  # field paths in the artifact YAML
    stage: DISCOVER | VERIFY | both | not_applicable
    decision_changed: <one-sentence concrete behavior change OR "not_applicable">
  scribe:
    reads_fields: []
    stage: scaffold | substance | both | not_applicable
    decision_changed: <one-sentence concrete behavior change OR "not_applicable">
  judge:
    reads_fields: []
    stage: rubric_scoring | cross_check | not_applicable
    decision_changed: <one-sentence concrete behavior change OR "not_applicable">
  red_team:
    reads_fields: []
    stage: probe_generation | probe_target_selection | not_applicable
    decision_changed: <one-sentence concrete behavior change OR "not_applicable">
  logician:
    reads_fields: []
    stage: PRE | POST | COMMIT | not_applicable
    decision_changed: <one-sentence concrete behavior change OR "not_applicable">
```

At least ONE seat must be active (not `not_applicable`). All-five-`not_applicable` artifacts fail the strong-component bar.

### A.2 `artifact_must_not_contain:` — anti-drift discipline

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact
  - applicant-specific claims
  - uncited generalizations
  # Add artifact-specific exclusions below, each as a separate list item.
```

The first three items are canonical and non-negotiable. Logician `F-FID-CROSS-ARTIFACT-COUPLING` (HIGH) + `F-FID-FACT-ORPHAN` (P0) enforce the first two at runtime.

### A.3 `strength_test:` — three questions the artifact must answer concretely

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

§1 of this charter MUST contain explicit answers to all three. If §1 cannot supply concrete answers, mark this charter as pre-spec DRAFT in the header and hold pending re-authoring against the gold-standard quality bar.

---

## §1 — What "depth" means for THIS artifact

Each artifact family has a different shape of depth. Write the 3-5 sentences that distinguish what THIS artifact carries from a card-pointer or a shallow corpus entry. CLC-01 Public Purpose & Works depth ≠ CLC-07 Sponsorship & Corporate Support depth.

For a `funder` artifact, depth typically means: mission framing, funder dialect across the agency, program roster pointers, officer-relationship notes (Tier-2/3), compliance cascade defaults, historical award patterns.

For a `program` artifact, depth typically means: NOFO / RFA verbatim cites, rubric weighted dimensions with point allocations, eligibility rules machine-parseable for Logician, required application elements, post-award obligations, endpoint URLs for Scout VERIFY.

For a `compliance_cascade` artifact, depth typically means: statutory cites, trigger conditions, mandatory gates machine-parseable, failure modes for Red Team probes, audit + reporting obligations.

For a `reviewer_type` artifact, depth typically means: time budget per application, top-10 reviewer heuristics with provenance, common punishments + rewards, dialect cues, denial-feedback distillation.

**Write the artifact-specific depth definition here.** ≤5 sentences.

---

## §2 — Primary sources in scope

List the corpus categories that will populate `_research_corpus/<artifact_id>/`. For each, name the specific sources you expect to pull and whether FOIA / interview / public-page is the path.

| Corpus category | Specific sources | Access path | Estimated count |
|-----------------|------------------|-------------|-----------------|
| `nofos/` | e.g., USDA-RD-RBDG FY26 NOFO PDF + HTML | Public Grants.gov | 1-3 |
| `rubrics/` | e.g., FY26 scoring sheet | Public publication / FOIA | 1 |
| `awards/` | e.g., FY24 + FY25 award rosters | USAspending.gov / agency portal | 2 |
| `interviews/` | e.g., 2 RBDG program officer conversations | Operator network outreach | 0-2 (Tier-2) |
| `guidance/` | e.g., federal-register interpretive notice cited in NOFO | Federal Register | 0-2 (only if NOFO cites) |

**Case law is OUT OF SCOPE** (compliance-officer territory; not grantwriter — per planning doc §3.2).

---

## §3 — Tier classification

Per architecture v7.0.10 three-posture routing inherited by FID:

| Field | Tier (1 / 2 / 3) | Rationale |
|-------|:----------------:|-----------|
| Default for facts in this artifact | `1` / `2` / `3` | e.g., public NOFO content = Tier 1 |
| Per-field overrides (list specific fields that diverge from default) | — | e.g., `funder_officer_relationship_notes[]` = Tier 3 |

Tier-1 = commons-readable at Stage 5. Tier-2 = operator-derived + opt-in shareable. Tier-3 = my-eyes-only forever.

---

## §4 — Refresh cadence

| Cadence option | Trigger |
|----------------|---------|
| `per_cycle` | Re-fetch every cycle (e.g., annually-cycled program with annual NOFO refresh) |
| `quarterly` | Quarterly recheck against new corpus material |
| `annual` | Annual refresh for stable framework or foundation profile |
| `per_rfa` | Refresh when a new RFA / NOFO drops |
| `event_triggered` | Refresh on operator-flagged event (e.g., agency leadership change, statutory amendment) |

**Selected cadence:** `<one>`.

`F-FID-STALE-RUBRIC` PRE-gate flags rubrics > 18 months old AND annually-cycled program.

---

## §5 — Calibration applicant pair

Which CIC × CLC pair will field-test this artifact?

| Field | Value |
|-------|-------|
| `cic_pair` | e.g., `food_systems` (CIC-01) |
| `clc_pair` | e.g., `operating_capacity` (CLC-03) |
| `calibration_track_target` | `A` (operator-win replay) / `C` (synthetic panel) / both |
| `track_a_win_id` | If applicable: which operator 2026 win will this artifact be tested against? |
| `track_c_pair_id` | If applicable: which synthetic pair? |

---

## §6 — Done definition

When does this artifact graduate from `draft` to `field_tested → validated`?

| Lifecycle gate | Definition |
|----------------|-----------|
| `draft` | Pillar 2 corpus complete; Pillar 3 extraction started |
| `audited` | Pillar 3 single-cycle L-005 audit passed (Editor + Judge + Red Team unanimous READY_TO_LOCK + zero P0 findings); all facts carry `corpus_ref` + verbatim ≤2-sentence quote; no orphan facts |
| `field_tested` | Pillar 4 Track-A or Track-C run complete; reviewer ratings on record |
| `validated` | Track-A AND Track-C both signal improvement (≥1.0 SD reviewer-rating delta on Track C; deep-vs-shallow win on Track A); operator-Ed25519-signs final |

If Pillar 4 signals are mixed → artifact stays `field_tested` (NOT `validated`) and gets a revision pass before graduating.

---

## §7 — Operator signature

```
charter_signed_at: <UTC ISO-8601>
charter_signed_by_pubkey: <FID publisher pubkey fingerprint>
charter_signed_canonical_bytes_sha3_512: <hash>
charter_ed25519_signature: <signature over canonical JSON of this charter; signature field excluded from canonicalization>
```

Canonicalization rule (mirrors Cards + WPFA + Reflection Packet):

- `sort_keys=True`
- `separators=(',', ':')`
- UTF-8 encoding
- `ensure_ascii=False`
- The `charter_ed25519_signature` field set to `null` during canonicalization, then the signature is appended after.

Signed against the FID publisher pubkey at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`.

---

## §8 — Out of scope (anti-drift)

Items explicitly NOT in scope for THIS artifact, to prevent boundary drift at Pillar 3:

- e.g., other programs from this funder (their own artifacts)
- e.g., per-applicant compliance posture (lives in `orgs/`)
- e.g., case law interpretation (compliance-officer territory)
- e.g., individual reviewer-officer profiles (lives in funder-level Tier-3 only)

Explicitly list 3-5 items to constrain scope.
