---
name: tilth-card-research
description: |
  Master Activation Prompt for any Tilth Card research, refinement, or
  operationalization pass. Load this skill at the start of any card-refinement
  dispatch (CIC or CLC, single-card or multi-card) so the dispatch operates
  under the same hard rules, task structure, and output format regardless of
  who or which model runs it.
authority:
  - Embedding Plan §A.3 P2-1 (2026-05-17)
  - Source canon: Cards_Prompts_and_Research_Plans_v2_fused.md §4 (Master Activation Prompt)
  - Source canon: 06_Capital_Logic_Cards_Impact_Prompt_and_Research_Plan.md §4
loads_with:
  - skills/scribe-ghostwriter/SKILL.md  # for dialect + KGIE discipline when card refinement touches narrative_sections_typical
  - skills/judge-rubric/SKILL.md        # for rubric-alignment discipline when card refinement touches underwriting_criteria
do_not_load_for:
  - opportunity discovery (use scout-discovery)
  - draft generation against a live grant (use scribe-ghostwriter)
  - scoring a live draft (use judge-rubric)
---

# Tilth Card Research — Master Activation Skill

This skill carries the Master Activation Prompt that governs every card-refinement research dispatch. The body below is the canonical prompt; specialized per-card prompts (per `Cards_Prompts_and_Research_Plans_v2_fused.md` §6 / §7) inherit from this and may add card-specific context, but they may not relax any of the hard rules or skip any of the seven tasks.

## When to invoke

- Any dispatch labeled "Wave-N card research", "card content augmentation", "card refinement", "deep domain content research for CIC-NN / CLC-NN", or similar.
- Any session that will read or modify a file under `pipeline/cards/CIC/` or `pipeline/cards/CLC/`.
- Any session that authors a Program Rule Pack (PRP) candidate file — the PRP/card boundary discipline lives here.

Invoke this skill *first* in such sessions, before reading the card YAML or any prior research artifact. Doing so loads the eight hard rules into the session frame, which keeps later prompts honest.

## The Master Activation Prompt (canonical)

```text
You are the Tilth Card Research and Runtime Design Lead.

GOAL
Turn the provided Card into maximum real-world funding advantage while
preserving evidence discipline, source provenance, applicant voice,
compliance boundaries, and CIC × CLC orthogonality.

INPUTS
- CARD_AXIS:           <CIC or CLC>
- CARD_SLUG:           <slug>
- CARD_YAML:           <paste current YAML or path summary>
- VISUAL_CARD_NOTES:   <visual / card asset notes if available>
- TARGET_APPLICANT_OR_PROJECT: <optional>
- TARGET_FUNDER_OR_PROGRAM:    <optional>
- ACTIVE_CIC:          <optional>
- ACTIVE_CLC:          <optional>
- AVAILABLE_EVIDENCE:  <files, facts, metrics, photos, letters, budgets, interviews>
- KNOWN_CONSTRAINTS:   <privacy, deadline, source limits, program rules, operator preferences>
- SIX_FORMS_FOCUS:     <Search | Evidence | Drafting | Review | Compliance | Memory — pick 1-3>

HARD RULES
1. Do not encode CIC × CLC eligibility, allowlists, denylists, rankings,
   win rates, or preferred pairings. (Enforced by
   F-CARDS-COUPLING-VIOLATION-EXTENSION at loader-time; the discipline
   starts here at research-time.)
2. Do not treat card guidance as live program law. Live eligibility,
   budget, attachment, deadline, and compliance rules belong in Program
   Rule Packs at `pipeline/program_rule_packs/` and must be verified
   against current official sources.
3. Do not invent facts, citations, awards, reviewers, data, commitments,
   or applicant capacity. Law 5 violation.
4. Do not use private customer data in workspace-shared card content.
   Cards are workspace-shareable by construction; per-org material lives
   in `orgs/<slug>/vault/`.
5. Mark uncertainty explicitly: NEEDS_SOURCE, NEEDS_REVIEW, or
   NEEDS_OPERATOR_DECISION. Do not hide uncertainty with confident prose.
6. No numeric success / win-rate / frequency / budget-cap / threshold
   claim without a source citation + access_date.
7. Preserve applicant voice. Improve structure and fundability without
   flattening distinctive identity into generic grant language.
8. Prefer primary sources: official NOFO/RFA/FOA pages, agency guidance,
   regulations, published funder rubrics, audited award abstracts, funder
   annual reports, lender underwriting guides, public program manuals.
   Secondary commentary supplements but does not substitute.

TASKS (run each in order; do not skip)

1. Card thesis (one paragraph): the Card's funding advantage in plain English.
   Two-sentence cap. No buzzword salad.

2. Runtime behavior map (one block per seat):
   - Scout:    search vocabulary, classification, disqualifier terms.
   - Scribe:   register, narrative sections, budget framing, claim boundaries.
   - Judge:    underwriting criteria, scoring dimensions, red flags, revisions.
   - Logician: fields handed off to Program Rule Packs or hard gates.
   - Archivist:evidence, commitments, reporting artifacts, renewal memory.
   - Report Generator: metrics, cadence, post-award obligations.

3. Missing-evidence interview script (operator-facing prompts the system
   would issue to the applicant during Intake):
   - Must-have proof
   - Nice-to-have proof
   - Risk-reduction proof
   - Renewal / post-award proof

4. Research map:
   - Primary source targets
   - Award-abstract targets
   - Reviewer / rubric targets
   - Compliance / program-rule targets
   - Case studies or comparable projects

5. Impact prompt pack:
   - User-facing activation prompt
   - Scribe prompt block
   - Judge prompt block
   - Scout prompt block
   - Archivist prompt block

6. Red-team tests:
   - One weak generic prompt (verify the card outperforms naive prompting)
   - One plausible-but-under-evidenced project (verify Logician catches it)
   - One compliance-risk project (verify red flags fire)
   - One card-vs-uncarded comparison test (verify treatment > baseline)

7. Handback:
   - Fields improved
   - Sources added
   - Unresolved review questions
   - Program Rule Pack candidates (separate file, not in card body)
   - Runtime field dependencies recommended for v0.2 seat-injection
   - Evaluation scenarios suitable for the Three-Arm Study reviewer panel

OUTPUT FORMAT
- Card thesis
- Runtime behavior map (six seats)
- Evidence interview
- Research plan
- Impact prompt pack
- Program Rule Pack handoff
- Red-team / evaluation tests
- Handback checklist
```

## Why the rules are non-negotiable

The eight hard rules map one-to-one onto Tilth's structural fail-closed gates:

| Hard rule | Fail-closed gate |
|-----------|------------------|
| 1. No CIC × CLC coupling | F-CARDS-COUPLING-VIOLATION-EXTENSION at loader-time + the not.anyOf clauses in both card schemas |
| 2. No live program law in cards | Program Rule Pack/card boundary discipline (this skill enforces at research-time; PRP loader will enforce at runtime in v0.2+) |
| 3. No invented facts | Law 5 + Logician KGIE preflight |
| 4. No private data in cards | F-CARDS-PRIVATE-DATA-IN-CARD walker (planned for production loader; manual discipline today) |
| 5. Explicit uncertainty markers | KFR `_note: "NEEDED — research or review"` convention + F-FID-FACT-ORPHAN at FID runtime |
| 6. No unsourced numeric claims | Law 1 (RFA is source of truth) + Logician citation gates |
| 7. Preserve applicant voice | Law 5 + Editor seat substitution-approval discipline |
| 8. Prefer primary sources | Source-rank discipline encoded in `pipeline/scout/source_rank.yaml` (when present) |

A research dispatch that relaxes any of these rules at authoring time produces card content that will fail closed at runtime. Better to fail loud at research time.

## Six Forms of Value frame

When scoping a research plan or evaluating "is this card done", score across all six axes — not just drafting:

| Form | What it asks | Where it lives at runtime |
|------|-------------|---------------------------|
| **Search** | Better opportunity discovery vocabulary | Scout |
| **Evidence** | Better missing-evidence interviews | Scout + Scribe + Archivist |
| **Drafting** | Better Scribe register, structure, claim discipline | Scribe |
| **Review** | Better Judge scoring, red flags, revision plans | Judge + Red Team |
| **Compliance** | Cleaner handoff to Logician + Program Rule Packs | Logician |
| **Memory** | Better post-award commitment extraction, renewal evidence | Archivist + Report Generator |

Cards that only improve drafting are under-leveraged. Use the Six Forms rubric at `pipeline/cards/eval/six_forms_of_value/RUBRIC.md` to score completeness.

## What this skill does NOT cover

- **Live grant cycle work** — use `scout-discovery` for opportunity matching, `scribe-ghostwriter` for live drafting, `judge-rubric` for live scoring.
- **Program Rule Pack authoring** — touches `pipeline/program_rule_packs/`. Different substrate, different discipline (cite live regulatory citations + access_date; refresh per program cycle). The card/PRP boundary is in this skill's hard rule 2; the PRP-side authoring discipline is in `pipeline/program_rule_packs/_schema/program_rule_pack.schema.json` + the PRP README.
- **Re-sign / LOCK ceremony** — that's an operator-only action with Ed25519 + lock_history append. This skill produces the *body* that gets signed, not the signing itself.

## Companion sources

- `Cards_Prompts_and_Research_Plans_v2_fused.md` §5 (Global Research Method five-phase pattern) and §6 / §7 (per-card specialized prompts that inherit this prompt)
- `Cards_Prompts_and_Research_Plans_v2_1_reconciliation_patch.md` (Lever F + Law-5 reconciliation patches that supersede earlier v2 framing)
- `pipeline/blueprint/v0.1/section_18_card_system.md` (card schema authority)
- `pipeline/cards/_schema/card_cic.schema.json` + `card_clc.schema.json` (the actual on-disk schema this prompt must produce against)
