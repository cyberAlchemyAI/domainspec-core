---
title: Funder Intelligence Database research project — "best damn grantwriter" depth lattice
date: 2026-05-16
authored_by: Cowork session (Anthropic-family author); operator-delegated Synthesizer mode
status: PROPOSED — operator-confirmed methodology, awaiting first-dispatch trigger
locks_affected_when_executed: §2 SUB_KIND_REGISTRY (FID sub-kinds + signed-asset pattern) + §4 Logician (F-FID-* family) + §0.5 (primitive_kind extension if FID warrants) + Wave 1+2 card content (smart-pointer migration; lifecycle-status untouched if pointers preserve thesis_passed substance)
locks_NOT_affected_at_doc_filing: any. This is a planning doc, not an amendment. L-005 dispatch fires only on individual artifacts within the project.
companion_docs:
  - pipeline/planning/funder_as_specimen_integration_2026-05-16.md   # already-filed; funder-as-training-specimen thesis aligns with FID-first architecture
  - pipeline/blueprint/v0.1/section_18_card_system.md      # card schema this project will reshape (pointers in, depth out)
  - pipeline/blueprint/v0.1/section_17_wpfa_v1.md                    # Coefficient Registry signed-asset pattern that FID mirrors byte-for-byte
  - skills/scribe-ghostwriter/references/reviewer_heuristics.md      # today's landing — seed for per-reviewer-type FID artifacts
authority: operator directive 2026-05-16 ("Design a research project to discern all you need to know to create THE BEST Capital Logic and Customer Information Cards as you conceivably can") [canonical naming policy 2026-05-17: "Customer Identity Card" is canonical; "Customer Information Card" is the legacy/working-language label preserved verbatim inside operator-quoted directives only — all new prose, schemas, code identifiers, and handoff artifacts must use "Customer Identity Card"]; follow-on "your best decision for the best project" delegating all 7 design questions to Synthesizer mode
---

# §0 — Purpose

Wave 2 Thesis (closed 2026-05-16) closed the **schema + coupling + provenance** layer on 12 Card Cards. It did NOT close the **deep domain content** layer — funder rubric weights at scale, reviewer heuristics from actual debrief letters, statutory authority citations, match-rule cascades, compliance triggers, dialect code-switching depth, reviewer-feedback patterns from real cycles.

This project closes that gap. Outcome: when the operator drops a `(CIC, CLC, basic-info)` tuple into Tilth, the resulting grantwriting should be **measurably better** than what any individual grantwriter could produce in a comparable time budget. KPIs in §6.

Architectural pivot the project enforces: deep domain content does NOT bloat cards (which stay at their Wave 1+2 schema-conformant size). Depth lives in a new workspace primitive — the **Funder Intelligence Database (FID)** — long referenced in architecture but never built. Cards become smart pointers into FID. This project lands FID.

# §1 — Decisions (operator-delegated Synthesizer mode 2026-05-16)

## 1.1 Scope first cut — exemplar-pair first

CIC-01 `food_systems` × CLC-03 `operating_capacity`. Both Wave 1 LOCK precedent; both already have partial Phase-2 prior art (VAPG FY26 rubric extracted at `pipeline/rubrics/vapg_fy26.json` + PA Dept of Ag state-overlay sketches + SARE program nuance scattered across skills + reviewer heuristics file that landed today). One real pair tests the FID-vs-card-pointer architecture against actual grantwriting before committing 6000-10000 hrs to scale. Methodology iterates on the pair. Then template. Then scale to remaining 13 card pairs + the cross-product.

## 1.2 FID-first

Build `pipeline/funder_intelligence/` as canonical funder / program / cascade / reviewer-type lattice. Cards become "smart pointers" via field-level FID references. No depth duplication across the 14 cards. FID adopts §17 v1 WPFA Coefficient Registry signed-asset pattern byte-for-byte (publisher pubkey pinned at white-glove; quarterly republish; Ed25519 verification at load). Scout DISCOVER + Archivist v1.x Lessons Memory both write into FID; cards sub-set. This is the moment FID actually lands.

## 1.3 Budget envelope — operator-time-protective

Total compute/LLM hours envelope: ~6000-10000 (3-5 person-years if done manually; not viable solo). Architecture protects operator time:

- **Operator-irreplaceable Josh-hours:** ~250 total over 20 weeks. Capped at 10-12 hrs/week. Used for interviews, decision-points, calibration review, blind-panel governance.
- **Bulk extraction:** LLM-assisted from primary sources under BYOK. Compute scales, Josh doesn't.
- **Anti-fabrication structural:** Logician PRE-gate `F-FID-FACT-ORPHAN` fails closed on any fact without a corpus pointer. `_note: "NEEDED — research or review"` marker is the only legitimate "we don't know yet" state.

## 1.4 Calibration — three-track

- **Track A — operator's 3 existing 2026 wins replayed blinded.** Deep-card vs shallow-card draft for the same opportunity. Panel: operator + 1 external grant reviewer. n=3 with survivor-bias caveats (we won — would deep have helped?).
- **Track B — partner-CDFI applicant pool.** 5-8 real in-pipeline applications consenting to deep-card piloting. Real funder decisions over months. High signal, slow turnaround, ethically careful (real applicant livelihoods).
- **Track C — synthetic blinded panel.** 10 fictionalized applicant × opportunity pairs reviewed by 3 paid blind reviewers per pair × ~$200/review = ~$6K cost. Fast iteration. Synthetic may not match real reviewers; triangulated against A + B.

Three tracks together = triangulation. No single track sufficient.

## 1.5 Consent — three-tier inherited from Tilth

FID content inherits Tilth's three-posture routing classification (architecture v7.0.10 LOCKED 2026-05-11):

- **Tier-1 commons (my-eyes-only OFF; matchable-to-opportunities + composable-with-others ON):** public-source-only content — statutory cites, public NOFO text, agency program pages, accessible 990-PF data, FOIA-returned rubrics. Future Stage-5 cooperative members read directly.
- **Tier-2 operator-derived + opt-in shareable:** operator-derived analyses, reviewer-heuristic syntheses from operator experience, funder-officer-relationship notes. Per-opportunity opt-in shareable.
- **Tier-3 my-eyes-only forever:** personal funder-officer communications, individual relationships, anything that would break trust if leaked.

Same vocabulary as Tilth substance classification. Same enforcement primitives. FID consumes the same classification register seeded at white-glove Classification Review per architecture v7.0.7.

## 1.6 Skills stay as how-to layer

No replacement. Skills + FID + Cards = three-layer architecture:

- `skills/grant-finder` reads FID at runtime for opportunity discovery matched to active CIC × inferred-CLC.
- `skills/grant-writer` reads FID + reviewer_heuristics at runtime for funder dialect + rubric weights + reviewer-feedback patterns.
- `skills/scribe-ghostwriter/references/reviewer_heuristics.md` (landed today) is the per-reviewer-type seed; FID `reviewer_heuristics/<type>.yaml` extends it.
- Card field `common_funders_observed[].funder_name` becomes `common_funders_observed[].funder_id` → FID lookup.
- Card field `scoring_weight_patterns[].rubric_example` becomes `scoring_weight_patterns[].rubric_id` → FID `programs/<program_id>` lookup.

No duplication. FID = canonical. Skills + cards = thin readers.

## 1.7 KPI — four-axis composite

No single-number target. Quarterly composite of:

| Axis | Definition | Baseline | Target at +6 months |
|------|-----------|----------|---------------------|
| (a) Win-rate uplift | % submitted that get funded | Operator's current 3-of-N (denominator NEEDED at project start) | +25-50% lift |
| (b) Time-to-funder-ready-draft | Operator-hours from "apply to X" to draft ready for final review | 20-40+ hrs today | <8 hrs |
| (c) Reviewer-rating delta on blinded comparison | Synthetic panel 5-dim rubric mean rating, deep-card minus shallow | 0 (baseline = same) | ≥1.0 SD higher |
| (d) Cost-per-win as % of award | Total operator-hours-equivalent + compute cost ÷ wins per quarter, as fraction of award | NEEDED at project start | <30% |

If 3 of 4 axes trend up at +6 months vs Wave-1+2 baseline, methodology validated. If ≤2, framework revision dispatched.

# §2 — FID architecture (canonical lattice)

```
pipeline/funder_intelligence/
  README.md
  _schema/
    fid_funder.schema.json
    fid_program.schema.json
    fid_compliance_cascade.schema.json
    fid_reviewer_type.schema.json
    fid_capital_raise.schema.json          # added 2026-05-19 per P0 #3; Reg CF instrument layer
  publisher_pubkey.signed.yaml             # white-glove-pinned operator publisher key; mirrors v7.0.7 §6.1 byte-for-byte
  funders/
    USDA-RD.yaml                            # agency level
    USDA-NIFA.yaml
    USDA-AMS.yaml
    EPA.yaml
    EDA.yaml
    SBA.yaml
    NEA.yaml
    NEH.yaml
    CNCS.yaml
    PA-DEP.yaml                             # state agencies
    PA-DCED.yaml
    PA-DEPT-AG.yaml
    PCCD.yaml
    PHMC.yaml
    HEINZ-FOUNDATION.yaml                   # foundations + intermediaries
    BENEDUM-FOUNDATION.yaml
    NCBA-CLUSA.yaml
    DAWI.yaml
    USFWC.yaml
    SOUL-FIRE-FARM.yaml
    NEFOC-LT.yaml
    # ... ~60-80 funders at maturity; 8-12 at exemplar pair
  programs/
    USDA-RD-RBDG-FY26.yaml                  # program × cycle keyed
    USDA-RD-RCDG-FY26.yaml
    USDA-AMS-VAPG-FY26.yaml                 # this one has rubric extracted already
    USDA-NIFA-SARE-NE-FY26.yaml
    USDA-NIFA-AFRI-FY26.yaml
    USDA-RD-CFP-FY26.yaml
    EPA-NEETP-FY26.yaml
    PA-DEPT-AG-AGINNOV-FY26.yaml
    # ... ~30-50 programs at maturity; 6-10 at exemplar pair
  compliance_cascades/
    2-CFR-200-UG.yaml                        # uniform guidance
    DAVIS-BACON-PREVAILING-WAGE.yaml
    BUILD-AMERICA-BUY-AMERICA.yaml
    SINGLE-AUDIT-A133.yaml
    NEPA-CATEGORICAL-EXCLUSIONS.yaml
    FERPA-IN-RESEARCH.yaml
    IRB-COMMON-RULE.yaml
    SBA-7A-UNDERWRITING.yaml
    SBIR-PHASE-III-COMMERCIALIZATION.yaml
    # ... ~8-15 cascades at maturity; 3-5 at exemplar pair
  reviewer_heuristics/
    federal-program-officer.yaml
    foundation-program-officer.yaml
    peer-reviewer-academic.yaml
    sba-7a-credit-committee.yaml
    cdfi-underwriter.yaml
    state-arts-council-panelist.yaml
    irb-human-subjects-reviewer.yaml
    marketing-manager-sponsorship-reviewer.yaml
    # ... ~8-12 types at maturity; 4-6 at exemplar pair
  _research_corpus/                          # raw primary-source artifacts (Tier-1 unless tagged otherwise)
    <artifact_id>/
      nofos/
      rubrics/
      awards/
      interviews/                            # operator + collaborator interview transcripts (Tier-2 default)
      guidance/                              # federal-register interpretive notices ONLY when a NOFO cites them and the notice materially changes applicant framing (Tier-1); case law explicitly out-of-scope (compliance-officer territory, not grantwriter)
      manifest.yaml                          # SHA256 + URL + access_date per file
  lessons_seed/                              # Archivist v1.x seed loop; CycleReceipts write here
    <cycle_id>.yaml
```

FID consumers (read paths):

| Component | Reads | When |
|-----------|-------|------|
| Scout DISCOVER | `funders/`, `programs/` | Opportunity discovery |
| Scout VERIFY | `programs/<program_id>.yaml` `endpoints` + `live_check_url` | Pre-CRITICAL-fit validation |
| Scribe | `programs/<program_id>.yaml` `rubric` + `reviewer_heuristics/*` + `funders/<id>.yaml` `dialect_notes` | Section drafting |
| Judge | `programs/<program_id>.yaml` `rubric.weighted_dimensions` + `compliance_cascades/*` | Scoring |
| Red Team | `reviewer_heuristics/<type>.yaml` `common_punishments` + `compliance_cascades/*` `failure_modes` | Adversarial probes |
| Logician | `compliance_cascades/*` `mandatory_gates` + `programs/<id>` `match_rules` | Deterministic PRE/POST gates |
| Report Generator | `programs/<id>` `post_award_obligations` + `commitment_extraction_pattern` | Reporting templates |
| Cards (CIC + CLC) | Field-level `funder_id` / `program_id` / `cascade_id` / `reviewer_type_id` resolved at load | Card load time |

## 2.1 Signed-asset pattern (mirrors §17 v1 §17.6 byte-for-byte)

- Publisher Ed25519 keypair operator-controlled. Public key pinned at white-glove Classification Review.
- Each FID artifact carries `ed25519_signature` field over canonical-JSON-bytes (sort_keys=True, separators=(',', ':'), UTF-8, ensure_ascii=False, signature field excluded from canonical computation).
- Loader fails closed via `F-FID-SIGNATURE-INVALID` on signature verification failure.
- Quarterly republish cadence (each Q1/Q2/Q3/Q4 anchor date). Out-of-cycle hot-patches signed individually.
- Trust mechanism mirrors v7.0.7 §6.1 router-template + §17 v1 §17.6 Coefficient Registry — no marketplace fetch from appliance; manual signed-tarball delivery; appliance verifies against pinned pubkey.

## 2.2 New F-FID-* failure-code family

Owned by §4 v2.x.z follow-on amendment (filed when project executes):

| Code | Severity | Predicate |
|------|----------|-----------|
| F-FID-SIGNATURE-INVALID | P0 | Artifact signature does not verify against pinned publisher pubkey |
| F-FID-FACT-ORPHAN | P0 | Any fact in a FID artifact lacks a corpus pointer (corpus_ref absent or unresolvable) |
| F-FID-CORPUS-HASH-MISMATCH | HIGH | corpus_ref artifact SHA256 ≠ manifest.yaml recorded value |
| F-FID-CLASSIFICATION-LEAK | P0 | Tier-2 or Tier-3 FID content routed to cloud under Frontier-Eligible posture (mirrors F-CLASS-* family) |
| F-FID-CROSS-ARTIFACT-COUPLING | HIGH | FID artifact embeds another FID artifact's content rather than pointer (anti-duplication) |
| F-FID-STALE-RUBRIC | MED | program_id rubric > 18 months from access_date AND program is annually-cycled |
| F-FID-REVIEWER-HEURISTIC-FABRICATION | P0 | reviewer_heuristics entry lacks operator-verified interview source OR documented public reviewer-debrief source |
| F-FID-COVERAGE-INCOMPLETE | META PRE-cycle | Card pointer resolves to nonexistent or unsigned FID artifact |

# §3 — 4-pillar methodology (per FID artifact)

Every funder, program, cascade, reviewer-type artifact passes through four pillars.

## 3.1 Pillar 1 — Depth Charter

One-page operator-signed charter per artifact answering:

1. What depth means for THIS artifact (CLC-01 Public Purpose & Works ≠ CLC-07 Sponsorship & Corporate).
2. What primary sources are in scope (statutory cites? FOIA-returned rubrics? interview-required?).
3. Tier classification (1 / 2 / 3) for this artifact's content.
4. Refresh cadence (quarterly / annual / per-cycle / per-RFA).
5. Calibration applicant pair (which CIC × CLC pair will field-test this artifact).
6. Done definition (when does this artifact graduate from DRAFT to thesis_passed-equivalent?).

Operator-signed before Pillar 2 starts. Ed25519-signed charter goes in `_research_corpus/<artifact_id>/charter.signed.yaml`.

## 3.2 Pillar 2 — Primary-source corpus

Build `_research_corpus/<artifact_id>/`:

- `nofos/` — NOFO/RFA/FOA PDFs + HTML snapshots, original + extracted text
- `rubrics/` — scoring sheets where FOIA-available or publicly published
- `awards/` — public award database extracts (Grants.gov fetchOpportunity, USAspending.gov, foundation 990-PF, state portals)
- `interviews/` — operator + collaborator interview transcripts, Tier-2 default
- `guidance/` — federal-register interpretive notices ONLY when a NOFO cites them and the notice materially changes applicant framing (Tier-1). Case law is OUT-OF-SCOPE (compliance-officer territory, not grantwriter).
- `manifest.yaml` — SHA256 hash + URL + access_date + content_type per file
- `charter.signed.yaml` — Pillar 1 output

Every artifact in the corpus carries provenance. Verbatim quotes pulled from corpus are ≤2 sentences each (OQ-4 inherited from Wave-1+2 card discipline).

## 3.3 Pillar 3 — Extraction + structuring

LLM-assisted (Scout DISCOVER → Scribe extract → Logician verify) but human-spot-check at every fact:

1. Scout DISCOVER scans corpus, surfaces candidate facts.
2. Scribe extracts structured facts into FID artifact draft (rubric weights, statutory cites, reviewer heuristics, dialect notes, post-award obligations).
3. Each fact carries `corpus_ref: <artifact_id>:<filename>:<page_or_line>` + verbatim quote ≤2 sentences.
4. Logician PRE-gate `F-FID-FACT-ORPHAN` fails closed on any orphan fact.
5. Operator spot-check on flagged-uncertainty facts (Scribe marks `_confidence: low` when source ambiguous).
6. Cross-family Thesis (lighter than Wave-2 card Thesis since provenance verification IS the audit) — single-cycle review by Editor + Judge + Red Team running on card-Thesis dispatch infrastructure.

Output: `funders/<id>.yaml` or `programs/<id>.yaml` etc. with `lifecycle.cross_family_thesis_status: passed` after Pillar 3 closure.

## 3.4 Pillar 4 — Field-test calibration

Three tracks per §1.4. Each artifact field-tested before flipping `lifecycle.field_test_status` to `validated`:

- Track A run: replay 1+ operator wins where this artifact would have been consulted. Deep-vs-shallow blind comparison.
- Track B run: partner-CDFI applicant pilot consults this artifact. Real outcome over months.
- Track C run: synthetic panel rates deep-vs-shallow draft on a synthetic applicant × opportunity pair touching this artifact.

If Track-A + Track-C both signal improvement (Track B is slow), artifact graduates to `field_test_status: validated`. If signals are mixed, artifact stays `pending` and gets a revision pass.

## 3.5 Optional Pillar 5 — Refresh

Per Depth Charter `refresh_cadence`. Quarterly/annual recheck against new corpus material. Diff applied via paired-commit pattern (signature re-issued). Stale-detection via `F-FID-STALE-RUBRIC` PRE-gate.

# §4 — Exemplar-pair charter (CIC-01 food_systems × CLC-03 operating_capacity)

## 4.1 Why this pair

- Both Wave 1 THESIS_PASSED + LOCKED. Schema discipline already verified.
- Operator has partial Phase-2 depth already: VAPG FY26 rubric extracted at `pipeline/rubrics/vapg_fy26.json`; PA Dept of Ag overlay sketches; SARE program nuance scattered in skills; reviewer heuristics file just landed.
- Cross-pair coverage: food_systems × operating_capacity touches USDA RD + USDA NIFA + USDA AMS + foundations + state ag departments — the full funder cross-section the operator works in.
- Three of the operator's 2026 wins were food_systems-CIC applicants seeking operating-capacity-CLC mechanisms. Calibration Track-A natural fit.

## 4.2 Artifacts in exemplar scope

**Funders (8):**
- USDA-RD (Rural Development)
- USDA-NIFA
- USDA-AMS
- PA-DEPT-AG
- PA-DCED
- HEINZ-FOUNDATION (regional foundation example)
- NCBA-CLUSA (intermediary example)
- ONE additional state foundation (operator chooses at Pillar 1)

**Programs (6):**
- USDA-AMS-VAPG-FY26 (rubric already extracted; reference depth)
- USDA-RD-RBDG-FY26
- USDA-RD-RCDG-FY26
- USDA-NIFA-SARE-NE-FY26
- PA-DEPT-AG-AGINNOV-FY26
- USDA-RD-CFP-FY26 (Community Facilities; operating-capacity-flavored)

**Compliance cascades (3):**
- 2-CFR-200-UG
- DAVIS-BACON-PREVAILING-WAGE (touches CFP)
- SINGLE-AUDIT-A133

**Reviewer types (4):**
- federal-program-officer (USDA-flavored)
- foundation-program-officer
- peer-reviewer-academic (SARE-flavored)
- state-program-officer (PA Dept of Ag)

Total: 21 FID artifacts. Estimated 40-80 hrs per artifact (LLM-bulk + Josh-spot-check). 850-1700 compute-hours + ~60 Josh-hours. Doable in ~6-8 weeks.

## 4.3 Exemplar-pair done definition

All 21 artifacts at `cross_family_thesis_status: passed` + `field_test_status: validated` (Track A + Track C minimum; Track B optional pending CDFI partner availability).

Card migration: `pipeline/cards/CIC/food_systems.yaml` + `pipeline/cards/CLC/operating_capacity.yaml` migrated to smart-pointer form. Substance preserved (thesis_passed lifecycle UNTOUCHED — operator-Ed25519 re-sign required for that). Smart-pointer migration is mechanical and additive, not substantive.

Methodology output: `pipeline/funder_intelligence/_methodology/v1.0.md` — template for the scale-out phase.

# §5 — Calibration protocol (three-track)

## 5.1 Track A — operator-win replay

Per win (Josh's 3 confirmed 2026 wins):

1. Snapshot the applicant-context + opportunity-RFA + final-submitted-draft AS-WAS at submission time. Already on disk; verify.
2. Run Tilth-shallow (card alone, no FID) generating a competing draft on same applicant×opportunity. ~4 hrs compute.
3. Run Tilth-deep (card + FID) generating a competing draft. ~4 hrs compute.
4. Three blind reviewers (operator + 2 external grant reviewers, $300/review × 2 external = $600/win) rate three drafts on the funder's rubric. Reviewers don't know which is human / shallow / deep.
5. Aggregate: does Tilth-deep score within ±0.5 SD of human draft? Above human draft? Below shallow?

Output: `pipeline/funder_intelligence/_calibration/track_a/<win_id>/comparison.yaml` + signed blind-reviewer ratings.

Cost per win: ~$600 cash + ~8 compute-hrs + ~3 operator-hrs. Three wins × ~$1800 cash + ~25 operator-hrs.

## 5.2 Track B — partner-CDFI applicant pilot

Operator identifies 1-2 CDFI / regional-foundation partners willing to pilot deep-card grantwriting on 5-8 in-pipeline applicants. Pilot terms:

- Applicants opt in to Tilth-deep drafting their proposals (vs current process).
- Funder decisions arrive over 3-9 months.
- Win rate + reviewer feedback compared against partner's historical baseline rate.
- All applicant data Tier-3 (operator-private + partner-private; never enters FID Tier-1).

Slow but real-world. Optional for exemplar-pair done; required for scale-out validation.

Output: `pipeline/funder_intelligence/_calibration/track_b/<applicant_id>/outcome.yaml`. Tier-3 access only.

## 5.3 Track C — synthetic blinded panel

10 fictionalized (anonymized + fabricated-but-plausible) applicant × opportunity pairs. Each pair:

1. Generate applicant-context + opportunity-RFA (5 hrs per pair, mostly Scribe-generated then operator-tweaked).
2. Run Tilth-shallow + Tilth-deep drafts. 4 hrs compute each.
3. Three paid blind reviewers ($200/review × 3 reviewers × 10 pairs = $6K) rate drafts.
4. Reviewers don't know which is shallow / deep / which applicant is fictional.

Cost: ~$6K cash + ~90 compute-hrs + ~50 operator-hrs (heavy operator involvement in pair construction to maintain plausibility).

Output: `pipeline/funder_intelligence/_calibration/track_c/<pair_id>/comparison.yaml`.

## 5.4 Calibration governance

- Blind reviewers recruited from outside Tilth's customer base + outside the operator's professional network. No conflict-of-interest.
- Pre-registration: rubric + comparison method + statistical threshold posted to `pipeline/funder_intelligence/_calibration/preregistration.signed.yaml` BEFORE any draft is shown to a reviewer. Prevents methodology-cherrypicking ex post.
- Reviewer-rater agreement check: Krippendorff's α across reviewers per pair. If α < 0.6, pair is excluded from aggregate signal.
- Per feedback memory `feedback_no_historical_wins_as_eval_fixtures.md` (operator 2026-05-15 PM): operator's wins ARE valid for Track A here only because each Track-A run involves NEW reviewers comparing deep vs shallow — not Tilth-evaluating-Tilth on operator's wins. Survivor bias caveat documented in every Track-A output.

# §6 — KPI dashboard

Quarterly publish. JSON-Lines schema at `pipeline/funder_intelligence/_kpi/quarterly.jsonl`. Schema:

```json
{
  "quarter": "2026-Q3",
  "axis_a_win_rate_uplift_pct": 0.0,
  "axis_a_denominator": 0,
  "axis_b_time_to_draft_median_hrs": 0.0,
  "axis_b_baseline_median_hrs": 0.0,
  "axis_c_reviewer_rating_delta_sd": 0.0,
  "axis_c_n_pairs": 0,
  "axis_d_cost_per_win_pct_of_award": 0.0,
  "axis_d_baseline_pct": 0.0,
  "trending_up": ["a", "b", "c"],
  "trending_down_or_flat": ["d"],
  "verdict_3_of_4_passing": true,
  "notes": "free-text"
}
```

Decision logic at +6 months:

- 3 of 4 axes trending up vs Wave-1+2 baseline → methodology validated → proceed scale-out.
- 2 of 4 → framework partial revision (which axes failed? targeted fix dispatched).
- ≤1 of 4 → framework full revision (return to §1 decisions).

# §7 — Dispatch + audit pattern

## 7.1 Per-artifact dispatch

Each FID artifact gets a Cowork session (or Codex / Paul / external research-lead session) to author. Dispatch prompt template:

- Pillar-1 Depth Charter input (operator-signed)
- Corpus pointer + access instructions
- Schema reference
- Extraction methodology reference (Pillar 3)
- Done definition

Author session writes draft. L-005 single-cycle audit fires (lighter than card Thesis because the audit is mostly provenance-chain verification — does every fact have a valid corpus pointer with verbatim quote ≤2 sentences? Does each rubric weight cite the rubric source?). Single cycle, three-seat cross-family rigor preserved (Editor + Judge + Red Team).

## 7.2 Cross-family rigor

Same model roster as Wave 1+2: Editor=meta, Judge=google, Red Team=openai-oss. Author=Anthropic. No family overlap.

## 7.3 Audit threshold

Single audit cycle. Pass = unanimous READY_TO_LOCK + zero P0 findings. Fail = REQUIRES_FIXES → author folds → second cycle. Maximum two cycles (L-005). No third cycle. Fix-in-place at LOCK per row-170 transparent disposition pattern.

## 7.4 Lifecycle promotion

`lifecycle.draft_status: draft → audited → field_tested → validated` (4 states, sequential).

# §8 — Lessons-Memory feedback loop

## 8.1 CycleReceipt → FID update

Per §17 v1 WPFA, every grant cycle emits a typed CycleReceipt. Receipt extension at this project: `cycle_receipts/<cycle_id>.yaml` `lessons_emitted[].fid_target` field flags which FID artifact gets a candidate amendment.

Archivist v0.2 / v1.x consumes the candidate amendment + operator-approves the fold-in. Approved folds:

- Update FID artifact draft (`lifecycle` flips to `revision_pending`).
- Re-sign on operator Ed25519.
- Republish quarterly bundle on next anchor date.

## 8.2 Anti-drift discipline

- Field-test re-runs every artifact-revision (Track C synthetic panel; cheaper than Track A/B).
- Stale-detection PRE-gate `F-FID-STALE-RUBRIC` flags rubrics > 18 months old AND annually-cycled program.
- Refresh cadence per Depth Charter — no exception.

## 8.3 Lessons seed for v0.1 horizon

`pipeline/funder_intelligence/lessons_seed/<cycle_id>.yaml` accumulates pre-Archivist-formal lessons. At Archivist v1.x landing, seed migrates to Archivist's canonical store. Bridge mechanism similar to Reflection Packet v0.1-hook → v0.2-first-wave dormant→live transition (§16 v1 → v1.1 LOCK precedent).

# §9 — Sequencing + timeline

## 9.1 Phase 1 — Exemplar pair (weeks 1-8)

- Week 1: Operator + Cowork session author Pillar-1 Depth Charters for all 21 exemplar-pair artifacts. Operator Ed25519 signs.
- Weeks 2-3: Pillar-2 corpus assembly. LLM-bulk fetching + operator spot-check. Manifest signing.
- Weeks 4-5: Pillar-3 extraction + structuring. Per-artifact dispatch via openclaw bridge. Single-cycle audit fires.
- Weeks 6-7: Pillar-4 field-test calibration. Track A on 3 operator wins. Track C on 5 synthetic pairs.
- Week 8: Exemplar-pair retrospective + methodology v1.0 doc filed + card smart-pointer migration applied (lifecycle untouched).

Operator-time budget weeks 1-8: ~80 hours total. Compute: ~1500 hrs LLM-extraction equivalent.

## 9.2 Phase 2 — Scale-out (weeks 9-32)

- Remaining 12 cards paired up with FID artifacts touching them. 7 batches of 2 cards each. ~3 weeks per batch with 4-way dispatch parallelism (reduced from Wave 2's 4-way after gateway saturation lesson).
- KPI dashboard publishes weeks 13 (Q3 anchor) + 26 (Q4 anchor).
- Decision review at week 26: 3-of-4 KPIs validate → proceed to Phase 3; ≤2-of-4 → revision dispatch.

Operator-time budget weeks 9-32: ~150 hours. Compute: ~6000-8000 hrs.

## 9.3 Phase 3 — Stage 1.5 commons preparation (weeks 33-52)

- Tier-1 FID content audited for commons-readiness.
- Stage 2-5 cooperative consent-tier infrastructure pre-staged (architecture v7.0.x amendment to land).
- Match Database seeded from accumulated CycleReceipts.

Phase 3 may overlap with v0.2 horizon work; not blocking.

# §10 — Risks + mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| LLM-extraction fabricates facts at scale | HIGH | P0 (Law 5) | F-FID-FACT-ORPHAN PRE-gate + operator spot-check + corpus-pointer mandatory + verbatim ≤2-sentence quote per fact |
| Operator burnout from 250-hr commitment | MED | HIGH | Cap at 12 hrs/week + protect via LLM-bulk + delegate non-irreplaceable work |
| Calibration panel reviewers don't match real reviewers | MED | MED | Triangulate Track A + B + C; pre-register methodology; Krippendorff's α threshold |
| FOIA-returned rubrics unavailable for many programs | HIGH | MED | Document as `_note: NEEDED — FOIA pending` + use publicly-available NOFO weights + flag for operator decision |
| Gateway/quota saturation under parallel dispatch | MED | LOW (recoverable) | Wave-2 lesson: cap concurrent dispatches at 2 card-pairs × 3 seats = 6 simultaneous calls + seat-stagger |
| Win-rate uplift target unachievable due to baseline noise (small-n) | MED | MED | Composite 4-axis KPI dilutes single-axis noise; Track C synthetic-panel removes survivor bias |
| Operator-private content leaks via Frontier-Eligible routing | LOW | P0 | F-FID-CLASSIFICATION-LEAK PRE-gate inherits from F-CLASS-* family + three-tier classification at white-glove |
| Stage-5 commons consent boundaries unclear | LOW | MED (deferred) | Tier-1/2/3 vocabulary inherits from Tilth; Stage-5-specific consent UI is Phase 3 work |
| Refresh cadence falls behind volatile administrations | MED | MED | Quarterly publish baked into FID lifecycle; per-cycle CycleReceipt → FID update at every grant cycle close |

# §11 — Open operational decisions (operator confirm before Phase 1 starts)

1. **Phase 1 start anchor date.** Soft propose: Monday 2026-05-18 (next operator-working-week). Operator confirms or pushes.
2. **External grant reviewers for Track A.** Operator identifies 2 external reviewers — preferably people who have served on actual federal review panels but are NOT in operator's professional network. Operator names or asks me to draft a recruitment ask.
3. **CDFI / regional-foundation partners for Track B.** Operator names a 1-2 partner candidates OR defers Track B to Phase 2 scale-out.
4. **Synthetic panel reviewer recruitment.** Operator confirms ~$6K cash budget OR proposes alternative (Track C deferred / pay-per-review staggered).
5. **Operator publisher Ed25519 key.** Same key as Cards publisher pubkey (vault_shared/cards/publisher_pubkey.signed.yaml), or new dedicated FID publisher key? Soft propose: new dedicated key (separation-of-concerns).
6. **First FID artifact to dispatch under methodology.** Soft propose: USDA-RD-RBDG-FY26 program file (clean federal NOFO, operator-familiar, single program scope) as methodology test before fanning out the rest.

# §12 — Cross-references

- **Funder-as-specimen integration:** `pipeline/planning/funder_as_specimen_integration_2026-05-16.md` — already-filed thesis that funders are training specimens, not card primitives. FID architecture is the operational realization of that thesis.
- **Cards Wave 1+2 Thesis precedent:** `pipeline/validation/cards_wave_1_thesis_2026-05-15/` + `pipeline/validation/cards_wave_2_thesis_2026-05-15/` — dispatch + audit infrastructure reusable for FID.
- **§17 v1 WPFA Coefficient Registry signed-asset pattern:** `pipeline/blueprint/v0.1/section_17_wpfa_v1.md` — byte-for-byte mirrored at FID `publisher_pubkey.signed.yaml` + per-artifact signature.
- **§16 v1 Reflection Packet:** `pipeline/blueprint/v0.1/section_16_reflection_packet_v1.md` — lessons-memory feedback loop precedent.
- **Architecture v7.0.7 white-glove Classification Review:** classification-tier seeding at appliance setup; FID consumes the same register.
- **Architecture v7.0.10 three-posture routing:** Tier-1/2/3 vocabulary inherited.
- **Today's reviewer_heuristics landing:** `skills/scribe-ghostwriter/references/reviewer_heuristics.md` — seed for per-reviewer-type FID artifacts.
- **§18 Cards System:** `pipeline/blueprint/v0.1/section_18_card_system.md` (filename retained pending separate operator-confirmed rename dispatch) — smart-pointer migration target.
- **Five Operating Laws:** `/SOUL.md` — Law 1 (RFA is truth — FID-cited facts trace to corpus); Law 4 (admin-risk + dialect — FID dialect_notes power Scribe code-switching); Law 5 (applicant brings substance — no fabricated reviewer heuristics).
- **AGENTS.md cross-family bridge pattern:** for FID artifact L-005 single-cycle audit dispatch via openclaw gateway.
- **Anti-fabrication memory:** `feedback_no_historical_wins_as_eval_fixtures.md` — Track A survivor-bias caveat handling.

---

# §13 — When this doc executes

When operator says "go on FID exemplar-pair Phase 1", or assigns Codex / Paul / external research lead.

Until then: this doc sits in planning. No L-005 dispatch fires. No card migration applied. No FID directory created. Wave 1+2 cards stay at thesis_passed lifecycle as currently signed.

When it executes: Phase 1 kickoff dispatch = one Cowork (or Codex) session with the §9.1 weeks-1-8 timeline. Operator-confirms §11 open ops decisions before kickoff.

---
# Candidate Funders Awaiting Verification — Added 2026-05-19 (from operator-supplied seeds)
**Source:** Tilth-only Gemini sanity audit redispatch 2026-05-19. All entries `verification_status: pending_primary_source`.
**Source authority rule applied:** Workbook entries → TIER 2 (operator-derived). Gemini PDF entries → TIER 3 (conjecture). Primary URL verification (Scout VERIFY) promotes individual rows to TIER 1.
**Scope filter:** Tilth-only. MyCel + Loom Console rows excluded (separate workstream).

## A. From master workbook `02 Opportunity Universe` (46 entries — TIER 2 operator-derived)
| # | Name | Funder | Tier | Type | Amount | Deadline/Status | Verification |
|---|------|--------|------|------|--------|------------------|--------------|
| A01 | NGI Zero Commons Fund | NLnet Foundation / EU NGI | A | Open internet / digital common | Typical €5K–€50K; larger possible if pro | Open call; next cited call closes 2026-06-01 12:00 | pending_primary_source |
| A02 | NSF PESOSE Phase I / AI Agent Ecosystem DCL | National Science Foundation | A | Federal R&D / open-source ecos | Up to $300K; 12 months | Next full proposal date cited 2026-09-01 | pending_primary_source |
| A03 | Coefficient Giving Technical AI Safety Research RFP | Coefficient Giving | A | Private AI safety philanthropy | First-time grants often $200K–$2M/year;  | Rolling EOI; active 2026 | pending_primary_source |
| A04 | NSF SBIR/STTR Phase I — Human-Computer Interaction | NSF Seed Fund | A | Federal SBIR/STTR | Phase I up to $305K; Phase II up to $1.2 | Project Pitch required; rolling windows depend on  | pending_primary_source |
| A05 | Astera Residency | Astera Institute | A | Open science / public-good res | $125K–$250K salary + up to $1.5M project | Fall 2026 cycle closed; monitor next cohort | pending_primary_source |
| A06 | AI Grant | AI Grant / Friedman-Gross orbit | A | Private open-source AI | $5K–$50K cash or compute | Batches/acceptance to verify; open-source program  | pending_primary_source |
| A07 | a16z Open Source AI Grant | Andreessen Horowitz | A | Private OSS AI grant / ecosyst | Cash + compute; public ceiling not fixed | Rolling/batch status to verify | pending_primary_source |
| A08 | Long-Term Future Fund | EA Funds / LTFF | A | AI safety / longtermist philan | $20K–$80K independent research typical;  | Rolling | pending_primary_source |
| A09 | Survival and Flourishing Fund — Speculation Grants / HSEE / Climate Theme | Survival and Flourishing Fund | A | AI safety / survival & flouris | $20M–$40M 2026 overall; theme grants var | Speculation grants rolling; 2026 theme windows inc | pending_primary_source |
| A10 | GitHub Secure Open Source Fund | GitHub | A | Open-source security / maintai | Amount to verify; security services/ment | Cohort status to verify | pending_primary_source |
| A11 | GitHub Accelerator | GitHub / M12 | A | Open-source accelerator | $40K/project + GitHub/M12/Azure support | Cohort status to verify | pending_primary_source |
| A12 | Cosmos Grants | Cosmos Institute | A | AI + philosophy / autonomy / d | $1K–$10K; larger possible for exceptiona | Rolling review aligned to rounds | pending_primary_source |
| A13 | Cosmos Fellowship | Cosmos Institute | A | AI + human flourishing fellows | Funding, mentorship, network; amount var | Applications visible; timing to verify | pending_primary_source |
| A14 | Mozilla Democracy x AI — next cohort / Sustain Track | Mozilla Foundation | B | Tech philanthropy / democracy  | $50K base; possible $250K Sustain Track | 2026 cohort timeline closed; monitor next cycle | pending_primary_source |
| A15 | Patrick J. McGovern Foundation — Data and Society / Data Practice Accelerator | Patrick J. McGovern Foundation | B | Data/AI for social impact phil | Up to $125K cited in uploaded pitch; ver | Rolling / program-dependent | pending_primary_source |
| A16 | Sloan Foundation — Digital Technology / Open Source in Science | Alfred P. Sloan Foundation | B | Research software / digital te | Variable; mid-six figures possible; inst | Rolling LOI; program-dependent | pending_primary_source |
| A17 | NSF Future CoRe / Human-Centered Computing | National Science Foundation | B | Federal academic research | Up to $1M, typically $150K–$250K/year fo | Target dates include 2026-09-10 and 2027-02-04 | pending_primary_source |
| A18 | NSF I-Corps National Teams | National Science Foundation | B | Customer discovery / commercia | Up to $50K for accepted teams | Rolling cohorts / eligibility dependent | pending_primary_source |
| A19 | NIDILRR SBIR | ACL / NIDILRR | B | Federal disability R&D / SBIR | Phase I small-business awards; caps vary | Annual/forecast; verify current NOFO | pending_primary_source |
| A20 | NIDILRR RERC on AI-driven Assistive / Rehabilitation Technology | ACL / NIDILRR | B | Federal disability research ce | Approximately multi-year center-level su | Current/forecast cycles to verify | pending_primary_source |
| A21 | ED / IES SBIR | U.S. Department of Education / IES | B | Federal education technology S | Phase I up to $250K; Phase II up to $1M  | Annual cycles; verify active solicitation | pending_primary_source |
| A22 | Open Technology Fund — Internet Freedom Fund | Open Technology Fund | B | Internet freedom / digital sec | $10K–$900K; ideal $50K–$200K over 6–12 m | Rolling, two-stage | pending_primary_source |
| A23 | OTF Free and Open Source Software Sustainability Fund | Open Technology Fund | B | Open-source sustainability / i | $7K/month for 6–24 months to up to $400K | Status to verify | pending_primary_source |
| A24 | Sovereign Tech Fund / Challenge / Fellowship | Sovereign Tech Agency | B | European digital sovereignty / | Varies by program | Program-dependent; current fellowship cycle noted  | pending_primary_source |
| A25 | Internet Society Foundation Research Grant Program | Internet Society Foundation | B | Internet research philanthropy | Amount varies; 2026 application window c | 2026 window open/closing as cited; verify before a | pending_primary_source |
| A26 | Google.org Impact Challenge: AI for Government Innovation | Google.org | B | Tech philanthropy / public-sec | $1M–$3M + technical support; 2026 applic | Closed 2026; monitor future cycles | pending_primary_source |
| A27 | Google.org Impact Challenge: AI for Science | Google.org | B | Tech philanthropy / AI for sci | $500K–$3M + technical support; 2026 appl | Closed 2026; monitor future cycles | pending_primary_source |
| A28 | AWS Imagine Grant — Pathfinder / nonprofit AI | AWS | B | Cloud/nonprofit technology phi | US 501(c) nonprofit categories; amounts  | 2025 cycle closed; monitor next cycle | pending_primary_source |
| A29 | VentureWell E-Team Program | VentureWell | B | Student innovation / commercia | Up to $25K non-dilutive funding + traini | Cycles to verify | pending_primary_source |
| A30 | OpenAI Foundation / People-First AI Fund / AI Resilience | OpenAI Foundation | B | AI philanthropy / strategic in | $50M People-First AI Fund announced; bro | No open general RFP found; monitor grants portal | pending_primary_source |
| A31 | Schmidt Sciences AI2050 | Schmidt Sciences | B | AI fellows / science philanthr | Cohort-level awards vary; AI2050 has fun | Cohort timing to verify | pending_primary_source |
| A32 | Anthropic Fellows Program for AI Safety Research | Anthropic | C | AI safety fellowship | $3,850/week + compute (~$15K/month) + me | 2026 cohort dates cited; application status verify | pending_primary_source |
| A33 | Astra Fellowship | Constellation Institute | C | AI safety fellowship/incubatio | $8,400/month stipend + compute budget +  | Application timing to verify | pending_primary_source |
| A34 | BERI collaborations / fiscal/operations support | Berkeley Existential Risk Initiative | C | AI safety / x-risk operations  | Operational support; not a standard open | Relationship-based | pending_primary_source |
| A35 | NEA Grants for Arts Projects | National Endowment for the Arts | C | Federal arts funding | $10K–$100K for many applicants; categori | 2026 deadlines included Feb and July windows | pending_primary_source |
| A36 | NEA Our Town | National Endowment for the Arts | C | Creative placemaking / public  | Amount varies; matching often required | Annual cycle; verify current dates | pending_primary_source |
| A37 | Pittsburgh Foundation — Foundation-Directed Grants / Small and Mighty / Arts ... | The Pittsburgh Foundation | C | Regional community foundation | Varies; fall 2026 deadline 2026-07-15 fo | Fall 2026 deadline cited 2026-07-15 | pending_primary_source |
| A38 | Heinz Endowments — rolling LOI / strategic programs | The Heinz Endowments | C | Regional foundation | Varies; rolling LOI | Rolling LOI | pending_primary_source |
| A39 | The Grable Foundation — Education / youth / public schools | The Grable Foundation | C | Regional education philanthrop | Varies; trustee review deadlines listed  | Inquiry deadlines include 2026-08-10 for Nov 2026  | pending_primary_source |
| A40 | AlphaLab / Innovation Works Accelerator | Innovation Works / AlphaLab | C | Startup accelerator / regional | Investment/support varies; not a grant i | Applications rolling/cycle-based | pending_primary_source |
| A41 | PA Manufacturing Innovation Program (PMIP) via CMU | PA DCED / CMU / PA universities | C | State university-industry rese | Varies by state budget; supports student | Program-dependent | pending_primary_source |
| A42 | DOE ASCR / Genesis Mission: AI for Science | DOE Office of Science / ASCR | C | Federal R&D | $68M FY26 envelope cited in official DOE | FY26 deadlines included May 2026; verify current s | pending_primary_source |
| A43 | NIST CAISI / AI standards collaboration | NIST CAISI | C | Federal standards / research c | Varies; CAISI has CRADA/collaboration pa | Program-dependent | pending_primary_source |
| A44 | DARPA AI Exploration / DARPAConnect | DARPA | D | Defense R&D | Up to ~$1M per AIE in uploaded pitch; op | Opportunity-specific | pending_primary_source |
| A45 | IARPA AI / BENGAL-type programs | IARPA / ODNI | D | Intelligence R&D | Per opportunity | Opportunity-specific | pending_primary_source |
| A46 | Microsoft AI for Good Lab Open Call | Microsoft Research | D | Corporate AI for good | $5M/credits in some calls; eligibility m | Program-dependent; some calls region-specific | pending_primary_source |

## B. From master workbook `07 Integrated Funder Metadata` — entries not in §A (123 unique — TIER 2 operator-derived)
| # | Name | Funder Class | Geography | Verification |
|---|------|--------------|-----------|--------------|
| B001 | Share Our Strength / No Kid Hungry | Anti-hunger / food access nonprofit | National | pending_primary_source |
| B002 | Greater Pittsburgh Community Food Bank – Impact Grants | Anti-hunger / food access nonprofit | Varies | pending_primary_source |
| B003 | Local Initiatives Support Corporation (LISC) | CDFI / impact lender | National | pending_primary_source |
| B004 | Mad Capital – Perennial Fund | CDFI / impact lender | National | pending_primary_source |
| B005 | Potlikker Capital | CDFI / impact lender | National | pending_primary_source |
| B006 | Black Farmer Fund (BFF) | CDFI / impact lender | PA / Pittsburgh region | pending_primary_source |
| B007 | Foodshed Capital | CDFI / impact lender | PA / Pittsburgh region | pending_primary_source |
| B008 | Walden Mutual Bank | CDFI / impact lender | PA / Pittsburgh region | pending_primary_source |
| B009 | Centre Foundation | Community foundation | Regional (community foundation | pending_primary_source |
| B010 | POISE Foundation — Community Impact Grants | Community foundation | Regional (community foundation | pending_primary_source |
| B011 | POISE Foundation — Critical Community Needs Fund (CCNF) | Community foundation | Regional (community foundation | pending_primary_source |
| B012 | POISE Foundation — Greater Hill District Development Growth Fund | Community foundation | Regional (community foundation | pending_primary_source |
| B013 | POISE Foundation — Human Equity & Justice Fund (HEJF) | Community foundation | Regional (community foundation | pending_primary_source |
| B014 | POISE Foundation — Urban Youth Action Grants | Community foundation | Regional (community foundation | pending_primary_source |
| B015 | Pittsburgh Foundation | Community foundation | Regional (community foundation | pending_primary_source |
| B016 | The Pittsburgh Foundation | Community foundation | Regional (community foundation | pending_primary_source |
| B017 | Cooperative Development Foundation | Cooperative development organization | Varies | pending_primary_source |
| B018 | Campbell Soup Foundation | Corporate foundation / giving | National | pending_primary_source |
| B019 | PNC Foundation — Philanthropy | Corporate foundation / giving | National | pending_primary_source |
| B020 | AEO Foundation / AE Foundation™ Community Grants | Corporate foundation / giving | National with regional prefere | pending_primary_source |
| B021 | Alcoa Foundation — Community Investments | Corporate foundation / giving | National with regional prefere | pending_primary_source |
| B022 | BNY — Corporate Giving & Community Champions | Corporate foundation / giving | National with regional prefere | pending_primary_source |
| B023 | Clif Family Foundation | Corporate foundation / giving | National with regional prefere | pending_primary_source |
| B024 | Allegheny Health Network / Highmark — Grant & Sponsorship Requests | Corporate foundation / giving | PA / Pittsburgh region | pending_primary_source |
| B025 | Dollar Bank — Corporate Social Responsibility (Grants/Sponsorships) | Corporate foundation / giving | PA / Pittsburgh region | pending_primary_source |
| B026 | Giant Eagle — Community Giving / Food Donations & Local Support | Corporate foundation / giving | PA / Pittsburgh region | pending_primary_source |
| B027 | Highmark Foundation — Grants (Guidelines & Priority Areas) | Corporate foundation / giving | PA / Pittsburgh region | pending_primary_source |
| B028 | Highmark Foundation — School Grants Program (2025–2026) | Corporate foundation / giving | PA / Pittsburgh region | pending_primary_source |
| B029 | AHN / Highmark – Grant & Sponsorship Requests (web-based application) | Corporate foundation / giving | Varies | pending_primary_source |
| B030 | Live Well Allegheny / ACHD – REACH coalition pathway | County health department (Allegheny) | County / sub-state | pending_primary_source |
| B031 | Farm Credit East AgEnhancement Grants | Farm credit / agricultural lender | PA / Pittsburgh region | pending_primary_source |
| B032 | Biomass Research and Development Initiative Grants | Federal agency | Federal (national) | pending_primary_source |
| B033 | EQIP Organic Initiative (NRCS) | Federal agency | Federal (national) | pending_primary_source |
| B034 | Farm & Food Workers Relief Grant Program | Federal agency | Federal (national) | pending_primary_source |
| B035 | Federal-State Marketing Improvement Program (FSMIP) | Federal agency | Federal (national) | pending_primary_source |
| B036 | Northeast SARE | Federal agency | Federal (national) | pending_primary_source |
| B037 | Northeast SARE Farming Community Grants | Federal agency | Federal (national) | pending_primary_source |
| B038 | Northeast SARE Research & Education Grants | Federal agency | Federal (national) | pending_primary_source |
| B039 | Northeast SARE Research for Novel Approaches Grants | Federal agency | Federal (national) | pending_primary_source |
| B040 | SARE Agroecosystems Research Grants | Federal agency | Federal (national) | pending_primary_source |
| B041 | SARE Farmer & Rancher Grants | Federal agency | Federal (national) | pending_primary_source |
| B042 | SARE Northeast | Federal agency | Federal (national) | pending_primary_source |
| B043 | SARE Partnership Grants | Federal agency | Federal (national) | pending_primary_source |
| B044 | SARE Professional Development Grants | Federal agency | Federal (national) | pending_primary_source |
| B045 | SARE Sustainable Community Grants | Federal agency | Federal (national) | pending_primary_source |
| B046 | USDA | Federal agency | Federal (national) | pending_primary_source |
| B047 | USDA AMS – FMPP (Farmers Market Promotion Program) | Federal agency | Federal (national) | pending_primary_source |
| B048 | USDA AMS – LFPP (Local Food Promotion Program) | Federal agency | Federal (national) | pending_primary_source |
| B049 | USDA AMS – RFSP (Regional Food System Partnership) | Federal agency | Federal (national) | pending_primary_source |
| B050 | USDA Disaster Assistance Programs | Federal agency | Federal (national) | pending_primary_source |
| B051 | USDA NRCS – AMA | Federal agency | Federal (national) | pending_primary_source |
| B052 | USDA NRCS – CSP | Federal agency | Federal (national) | pending_primary_source |
| B053 | USDA NRCS – EQIP (general) | Federal agency | Federal (national) | pending_primary_source |
| B054 | USDA Renewable Energy Systems & Energy Efficiency Improvements Program (REAP) | Federal agency | Federal (national) | pending_primary_source |
| B055 | USDA Rural Development – Value-Added Producer Grants (VAPG) | Federal agency | Federal (national) | pending_primary_source |
| B056 | USDA – LAMP (Local Agriculture Market Program) | Federal agency | Federal (national) | pending_primary_source |
| B057 | Value-Added Producer Grants (VAPG) | Federal agency | Federal (national) | pending_primary_source |
| B058 | GRACE Communications Foundation | Foundation (other) | National | pending_primary_source |
| B059 | Sustainable Agriculture & Food Systems Funders (SAFSF) | Funder network (not direct grantmaker) | National | pending_primary_source |
| B060 | Jewish Healthcare Foundation — Grants | Health system / healthcare foundation | PA / Pittsburgh region | pending_primary_source |
| B061 | UPMC Health Plan — Community Engagement (Funding & In-kind) | Health system / healthcare foundation | PA / Pittsburgh region | pending_primary_source |
| B062 | First Nations Development Institute | Indigenous / Native ag funder | National | pending_primary_source |
| B063 | Native American Agriculture Fund (NAAF) | Indigenous / Native ag funder | National | pending_primary_source |
| B064 | BEA Fund (Building Equity & Alignment for Environmental Justice) | Intermediary / participatory fund | National | pending_primary_source |
| B065 | Builders Initiative | Intermediary / participatory fund | National | pending_primary_source |
| B066 | Builders Vision | Intermediary / participatory fund | National | pending_primary_source |
| B067 | Fund to Build Grassroots Power | Intermediary / participatory fund | National | pending_primary_source |
| B068 | Growing Justice Fund | Intermediary / participatory fund | National | pending_primary_source |
| B069 | Wildseeds Fund | Intermediary / participatory fund | National | pending_primary_source |
| B070 | Climate and Clean Energy Equity Fund | Intermediary / participatory fund | PA / Pittsburgh region | pending_primary_source |
| B071 | POISE Foundation — Fiscal Sponsorship Services | Intermediary / participatory fund | PA / Pittsburgh region | pending_primary_source |
| B072 | URA – Greater Hill District programs (rolling) | Municipal authority (Pittsburgh URA) | Municipal | pending_primary_source |
| B073 | Kresge Foundation | National private foundation | National | pending_primary_source |
| B074 | Robert Wood Johnson Foundation (RWJF) | National private foundation | National | pending_primary_source |
| B075 | Surdna Foundation | National private foundation | National | pending_primary_source |
| B076 | The Rockefeller Foundation | National private foundation | National | pending_primary_source |
| B077 | W.K. Kellogg Foundation | National private foundation | National | pending_primary_source |
| B078 | Walton Family Foundation | National private foundation | National | pending_primary_source |
| B079 | Bradshaw-Knight Foundation | Regional private foundation | Regional (PA / Pittsburgh) | pending_primary_source |
| B080 | Claude Worthington Benedum Foundation | Regional private foundation | Regional (PA / Pittsburgh) | pending_primary_source |
| B081 | Eden Hall Foundation — Grants (rolling LOI) | Regional private foundation | Regional (PA / Pittsburgh) | pending_primary_source |
| B082 | Foundation for Pennsylvania Watersheds (FPW) | Regional private foundation | Regional (PA / Pittsburgh) | pending_primary_source |
| B083 | Richard King Mellon Foundation | Regional private foundation | Regional (PA / Pittsburgh) | pending_primary_source |
| B084 | The Buhl Foundation — Grant Application Process | Regional private foundation | Regional (PA / Pittsburgh) | pending_primary_source |
| B085 | The Fine Foundation — About / Grantmaking | Regional private foundation | Regional (PA / Pittsburgh) | pending_primary_source |
| B086 | The Grable Foundation — Grant Inquiries | Regional private foundation | Regional (PA / Pittsburgh) | pending_primary_source |
| B087 | The Heinz Endowments | Regional private foundation | Regional (PA / Pittsburgh) | pending_primary_source |
| B088 | The Hillman Family Foundations | Regional private foundation | Regional (PA / Pittsburgh) | pending_primary_source |
| B089 | Farm Bill Conservation Programs (multiple) | State agency (NJ) | State | pending_primary_source |
| B090 | Farm Gleaning & Seafood Recovery Support Program | State agency (NJ) | State | pending_primary_source |
| B091 | Farmers Market Promotion Program (FMPP) / Farmers Market Assistance | State agency (NJ) | State | pending_primary_source |
| B092 | NJ Agritourism Grant Program (NJATP) | State agency (NJ) | State | pending_primary_source |
| B093 | NJ Clean Energy Program | State agency (NJ) | State | pending_primary_source |
| B094 | NJ SmartStart Buildings Program | State agency (NJ) | State | pending_primary_source |
| B095 | NJ Training Programs (Customized Training, Literacy Skills, YTTW, NJMEP) | State agency (NJ) | State | pending_primary_source |
| B096 | Organic Certification Cost Share Program (OCCSP) | State agency (NJ) | State | pending_primary_source |
| B097 | Resilient Food Systems Infrastructure (RFSI) Program | State agency (NJ) | State | pending_primary_source |
| B098 | Risk Management and Crop Insurance Education | State agency (NJ) | State | pending_primary_source |
| B099 | Soil & Water Conservation Grants (NJ SADC) | State agency (NJ) | State | pending_primary_source |
| B100 | Specialty Crop Block Grants (SCBGP) | State agency (NJ) | State | pending_primary_source |
| B101 | Specialty Crop Multi-State Program (SCMP) | State agency (NJ) | State | pending_primary_source |
| B102 | Spotted Lanternfly Treatment Grants | State agency (NJ) | State | pending_primary_source |
| B103 | Underserved, Beginning & Military Veteran Farmers Mini-Grant Program | State agency (NJ) | State | pending_primary_source |
| B104 | City of Pittsburgh | State agency (PA) | State | pending_primary_source |
| B105 | City of Pittsburgh – Food Justice Fund (Grassroots Grants) | State agency (PA) | State | pending_primary_source |
| B106 | City of Pittsburgh – Grant Opportunities (Community Development / CDBG hub) | State agency (PA) | State | pending_primary_source |
| B107 | City of Pittsburgh – Love Your Block (micro awards) | State agency (PA) | State | pending_primary_source |
| B108 | City of Pittsburgh – Neighborhood Economic Development (NED) Grant | State agency (PA) | State | pending_primary_source |
| B109 | Cumberland County Conservation District | State agency (PA) | State | pending_primary_source |
| B110 | PA Department of Agriculture | State agency (PA) | State | pending_primary_source |
| B111 | PA Department of Agriculture — Agricultural Innovation Grant | State agency (PA) | State | pending_primary_source |
| B112 | PA Department of Agriculture — Agricultural Promotion Matching Grant Program | State agency (PA) | State | pending_primary_source |
| B113 | PA Department of Agriculture — Agriculture & Youth Program Grant | State agency (PA) | State | pending_primary_source |
| B114 | PA Department of Agriculture — Farm Vitality Planning Grant | State agency (PA) | State | pending_primary_source |
| B115 | PA Department of Agriculture — Federal Specialty Crop Block Grant (2026 cycle... | State agency (PA) | State | pending_primary_source |
| B116 | PA Department of Agriculture — PA Farm Bill (program hub) | State agency (PA) | State | pending_primary_source |
| B117 | PA Department of Agriculture — PA Specialty Crop Grant | State agency (PA) | State | pending_primary_source |
| B118 | PA Department of Agriculture — Resilient Food Systems Infrastructure (RFSI) (... | State agency (PA) | State | pending_primary_source |
| B119 | PA Department of Agriculture — Urban Agriculture Infrastructure Grant | State agency (PA) | State | pending_primary_source |
| B120 | PA Department of Labor & Industry — Workforce Development Grant Opportunities... | State agency (PA) | State | pending_primary_source |
| B121 | PASA | Sustainable ag nonprofit | Varies | pending_primary_source |
| B122 | United Way of Southwestern Pennsylvania — Impact Grants (overview) | United Way affiliate | Regional (United Way footprint | pending_primary_source |
| B123 | United Way of Southwestern Pennsylvania — Multi-Year Impact Grants (2026 cycle) | United Way affiliate | Regional (United Way footprint | pending_primary_source |

## C. Net-new from Gemini PDF (`SN_LLC_Supplementary_Funding_Research_Net_New_Funders_May_2026.pdf`) — entries not already in workbook (32 candidates — TIER 3 conjecture)
**Caveat:** All names + facts in this section are Gemini-research-derived. Primary-source verification required before any operational use per Law 1.

| # | Name | Funder | Type | Lane | Route | Verification |
|---|------|--------|------|------|-------|--------------|
| C01 | DIU Commercial Solutions Opening — MYSTIC DEPOT line + follow-ons | Defense Innovation Unit | Federal OTA prototype | DoD AI-eval | Tilth | pending_primary_source |
| C02 | AFWERX SBIR/STTR Open Topic Phase I (FY26) | Department of the Air Force | Federal SBIR | DoD | Tilth + co-applicant | pending_primary_source |
| C03 | SOFWERX (USSOCOM) SBIR/STTR 2025.4 | USSOCOM | Federal SBIR | DoD | Tilth | pending_primary_source |
| C04 | Army xTechSearch / xTechIgnite | US Army | Cash prize competition | DoD | Tilth | pending_primary_source |
| C05 | DARPA Young Faculty Award | DARPA | Federal R&D | DoD R&D (academic PI) | Tilth via academic partner | pending_primary_source |
| C06 | DARPA I2O Office-Wide BAA | DARPA I2O | Federal R&D | DoD R&D | Tilth | pending_primary_source |
| C07 | DHS S&T SBIR (Dec-Jan annual) | DHS Science & Technology | Federal SBIR | DoD/DHS | Tilth | pending_primary_source |
| C08 | DoW "Pace-Setting Projects" (suspected — verify) | DoD/DoW | Federal | DoD AI-First | Tilth — VERIFY | pending_primary_source |
| C09 | Coefficient Giving Biosecurity RFP | Coefficient Giving | Foundation | AI-safety + biosecurity | Tilth | pending_primary_source |
| C10 | Manifund regranting (Marcus Abramovitch + others) | Manifund | Regranting fund | AI-safety | Tilth | pending_primary_source |
| C11 | Manifund AISTOF (AI Safety Tactical Opportunities Fund) | Manifund | Pooled fund | AI-safety | Tilth | pending_primary_source |
| C12 | Foresight Institute AI for Science & Safety Nodes | Foresight Institute | Foundation + community hub | AI-safety | Tilth | pending_primary_source |
| C13 | Lightcone Infrastructure | Lightcone | Community infrastructure | AI-safety / rationalist | Tilth | pending_primary_source |
| C14 | BlueDot Impact small grants | BlueDot Impact | Small grants | AI-safety | Tilth — requires BlueDot course | pending_primary_source |
| C15 | NLnet NGI TALER | NLnet | EU NGI | Open internet | Tilth? | pending_primary_source |
| C16 | NLnet NGI Fediversity | NLnet | EU NGI | Open internet | Tilth? | pending_primary_source |
| C17 | John Templeton Foundation Intelligence Venture 2026 | John Templeton Foundation | Foundation (academic PI) | Diverse Intelligences | Tilth via academic PI | pending_primary_source |
| C18 | Allen Institute for AI Open Research Fellowships | Allen Institute | Foundation (selective) | AI infrastructure | Tilth via academic | pending_primary_source |
| C19 | NSF I-Corps Mid-Atlantic Hub (Penn State regional) | NSF | Federal commercialization | Workforce/comm. | Tilth | pending_primary_source |
| C20 | IMLS National Leadership Grants for Libraries FY27 | Institute of Museum and Library Services | Federal | AI literacy / customer pass-through | Tilth via Carnegie Library of Pittsburgh | pending_primary_source |
| C21 | IMLS Museums for America / Inspire! / NLG-Museums | Institute of Museum and Library Services | Federal | Customer pass-through | Tilth via Pittsburgh museum partner | pending_primary_source |
| C22 | Forbes Funds Management Assistance Grants (MAGs) | The Forbes Funds (Pittsburgh) | Foundation | Capacity building | Tilth-as-vendor | pending_primary_source |
| C23 | USDA Community Food Projects Competitive Grant (CFPCGP) | USDA NIFA | Federal | Community food | Tilth via Mystic Mamas / Keystone fiscal sponsor | pending_primary_source |
| C24 | USDA LAMP / FMLFPP / RISE / Rural Business Development Grant | USDA Rural Development | Federal | Rural business | Tilth via MycoSymbiotics Cooperative | pending_primary_source |
| C25 | Andy Warhol Foundation Visual Arts (small orgs track) | Andy Warhol Foundation | Foundation | Visual arts / customer pass-through | Tilth via Pittsburgh 501(c)(3) partner | pending_primary_source |
| C26 | Mid-Atlantic Arts Foundation Cultural Sustainability | Mid-Atlantic Arts Foundation | Foundation (regional) | Arts / customer pass-through | Tilth via 501(c)(3) partner | pending_primary_source |
| C27 | Mellon Foundation Public Knowledge / Higher Learning | Mellon Foundation | Foundation | Academic / customer pass-through | Tilth via Pitt/CMU | pending_primary_source |
| C28 | Seed Commons (national co-op CDFI network) | Seed Commons | CDFI / non-extractive loan fund | Cooperative capital | Tilth via MycoSymbiotics | pending_primary_source |
| C29 | Shared Capital Cooperative | Shared Capital Cooperative | Co-op CDFI | Cooperative capital | Tilth via MycoSymbiotics | pending_primary_source |
| C30 | The Working World | The Working World | Patient capital | Cooperative capital | Tilth via MycoSymbiotics | pending_primary_source |
| C31 | LEAF (Local Enterprise Assistance Fund) | LEAF | Co-op CDFI | Food/housing/worker-owned | Tilth via MycoSymbiotics | pending_primary_source |
| C32 | National Cooperative Bank Impact Loans | National Cooperative Bank | Co-op finance | Cooperative capital (>$100K) | Tilth via MycoSymbiotics | pending_primary_source |

## D. Totals
- §A workbook Opportunity Universe: 46 TIER 2 entries
- §B workbook Integrated Funder Metadata (not in §A): 123 TIER 2 entries
- §C Gemini PDF net-new: 32 TIER 3 entries
- **Total candidates: 201**

All entries default to `verification_status: pending_primary_source`. Scout VERIFY pass elevates individual rows to TIER 1 on live-synopsis fetch + endpoint reachability per Law 1.
