---
spec_card: Logician §4 v2.2 Consolidated Blueprint Amendment Thesis Dispatch
version: v1 (filed 2026-04-21, pre-staged by King Midas v1 session B)
parent_lock: pipeline/blueprint/v0.1/section_04_logician.md (§4 v2.1 LOCKED 2026-04-18, hash e0507e6daaa18676)
target_artifact: pipeline/blueprint/v0.1/section_04_v2_2_consolidated_amendment.md
rolls_up:
  - section_04_v2_2_amendment.md            (Wave 1 — F-AMDT-02, F-AMDT-03; LOCKED 2026-04-20)
  - section_04_v2_2_wave_2_amendment.md     (Wave 2 — F-AMDT-01, F-AMDT-06, F-AMDT-07 v1+v1.1, F-AMDT-12; LOCKED 2026-04-21)
  - [WAVE 3 per-wave amendment]             (Wave 3 — F-AMDT-05, F-AMDT-10, F-AMDT-11, F-AMDT-08, F-AMDT-09; LOCKED 2026-04-21)
  - [WAVE 4 per-wave amendment]             (Wave 4 — F-AMDT-04; LOCKED 2026-04-21)
amendment_status: pre-staged — all 12 constituent gates individually LOCKED; consolidation is a zero-semantic-delta roll-up
---

# Spec — §4 Logician v2.2 Consolidated Blueprint Amendment

**STATUS:** LOCKED

## 0. Purpose

Twelve structural amendment-enforcement gates (F-AMDT-01 through
F-AMDT-12, including F-AMDT-07's v1.1 author-family anti-collision
extension) were LOCKED across four waves in four separate per-wave
blueprint amendments. This consolidation produces a single §4 v2.2
blueprint artifact as the Group-10-outside-audit single-artifact
reading surface. **Zero semantic delta** vs. the four per-wave
amendments — the constituent gate modules, semantics, failure-code
taxonomies, and committee synthesis artefacts remain canonical on
disk.

## 1. Assembly procedure (operator side)

1. Read the Wave 1, Wave 2, Wave 3, Wave 4 per-wave amendment bodies
   on disk.
2. Merge per-gate blueprint row tables into unified §4.5 PRE-gate +
   §4.6 POST-gate row tables covering all 12 gates.
3. Merge per-gate failure-code registries into a unified taxonomy
   (§6 extension).
4. Merge per-gate Protocol surface references into §4.A (single
   shared Protocol module).
5. Preserve every committee-round synthesis pointer (audit trail
   continuity for Group 10).
6. Run AST-lint R1-R7 on the §4 v2.2 blueprint-dependency hash set;
   verify no drift.
7. Dispatch single Thesis round against the consolidated draft —
   verdict is "faithful to per-wave LOCKs" (not re-litigating
   semantic content).
8. Operator signs → §4 v2.2 LOCKED as canonical.

## 2. Thesis dispatch — review scope

The consolidated amendment Thesis round verdict is **faithfulness,
not semantic novelty**. Reviewers must confirm:

1. **Gate-row coverage** — All 12 gates (F-AMDT-01..12 plus the v1.1
   F-AMDT-07 author-family anti-collision sub-code) appear in the
   consolidated §4.5/§4.6 row tables with their correct PRE/POST
   placement, failure-code, emitted-event, and spec-card pointer.
2. **Failure-code taxonomy** — Every parent + sub code listed in
   each per-wave amendment appears in the consolidated §6 taxonomy.
   No code collisions; no sub-code orphaned from its parent.
3. **Protocol surface** — §4.A reference to `pipeline/logician/gates/_protocols.py`
   lists every Protocol actually imported by the 12 gate modules.
4. **Synthesis pointer continuity** — Every per-wave committee
   synthesis path (12 synthesis.md files) is linked from the
   consolidated amendment's audit trail section.
5. **Parent-LOCK delta** — §4 v2.1 base semantics unchanged; v2.2
   consolidated amendment adds only structural enforcement rows
   delegating to the 12 gate modules.
6. **No hidden scope** — Reviewers flag any consolidated-amendment
   row / claim / code / protocol that is NOT traceable to one of
   the four per-wave amendments or to an individually-LOCKed gate
   module on disk.

## 3. Pass/fail criteria

- **PASS:** consolidation is faithful to the four per-wave LOCKs.
  Each reviewer returns PASS verdict with zero real-defect findings
  OR findings strictly of informational severity.
- **FAIL:** any reviewer surfaces a HIGH finding that identifies a
  semantic-delta claim, a missing row, a taxonomy collision, a
  Protocol omission, or an audit-trail break.
- **REFRESH:** typo / cross-reference-link / cosmetic cleanup that
  does not change the faithfulness verdict.

## 4. Non-negotiables

- Consolidation introduces zero new semantic content vs. per-wave
  LOCKs. Any semantic novelty surfaces as HIGH.
- Per-wave amendment files remain on disk as the audit trail source
  of truth. The consolidated file is a reading-surface convenience,
  NOT a supersession.
- **Blueprint-class roster = Tilth 3-seat Thesis Team**
  (Editor / Judge / Red Team) per `router.yaml` — Llama-3.3-70B
  (Meta) via Groq + Gemini-2.5-Pro (Google) via Google +
  GPT-OSS-120B (OpenAI-OSS) via Groq. **Not** the 5-family Code
  Thesis Committee slate — that roster is code-class only. The
  original 2026-04-21T07:16:35Z LOCK (ledger row 91) used the
  5-family roster in error; the retroactive 3-seat round at
  `pipeline/validation/blueprint_section_04_v2_2_consolidated_2026-04-21/`
  restores roster convention without reverting the historic
  first-blueprint-class-lock row. Cross-family discipline preserved
  in both rounds (reviewer family ≠ Anthropic author family).
- Transport-retry carve-out applies (retry = cycle-1 iff verdict is
  invariant AND trigger is transport / finding-field hallucination
  with top-line verdict unchanged).

## 5. Evidence of readiness

- **Per-wave amendments LOCKED on disk:**
  - Wave 1: `pipeline/blueprint/v0.1/section_04_v2_2_amendment.md` (LOCKED 2026-04-20)
  - Wave 2: `pipeline/blueprint/v0.1/section_04_v2_2_wave_2_amendment.md` (LOCKED 2026-04-21)
  - Wave 3: per-gate amendment rows LOCKED 2026-04-21 (F-AMDT-05/10/11/08/09)
  - Wave 4: per-gate amendment row LOCKED 2026-04-21 (F-AMDT-04)
- **Gate modules LOCKED on disk:** 12 modules in
  `pipeline/logician/gates/` (F-AMDT-01 through F-AMDT-12 plus
  F-AMDT-07 v1.1 extension in-module).
- **Test suite green:** full suite 3791 pass / 3 skip / 1 xfail at
  Wave-4 close; ~928 tests in `tests/logician/gates/`.
- **AST-lint:** R1-R7 exit 0 pipeline-wide.
- **Committee audit trail:** 12 synthesis.md files across four
  round directories under `pipeline/validation/code_reviews/`.
- **Individual lock_history rows:** 12 rows appended under
  respective committee_round tags in `pipeline/engineering/lock_history.v1.jsonl`.

## 6. Queue-close artefacts after Thesis dispatch

Initial LOCK already landed 2026-04-21T07:16:35Z by the 5-family
round (ledger row 91, first `lock_class: "blueprint"` row ever).
The 3-seat Tilth Thesis Team round at
`pipeline/validation/blueprint_section_04_v2_2_consolidated_2026-04-21/`
is a retroactive confirmation — its disposition controls the
supplementary artefacts below, not the primary LOCK.

On 3-seat `all_pass` (Editor READY_TO_LOCK + Judge PASS ≥ 85 with
`ready_to_lock: true` + Red Team LOCK):

1. Supplementary ledger row appended to
   `pipeline/engineering/lock_history.v1.jsonl` with
   `lock_class: "blueprint"`, `committee_round:
   "logician_v2_2_consolidated_tilth_thesis_2026-04-21"`,
   `supplementary_confirmation: true`, `cross_reference: line 91`.
2. Supplementary `## LOCK-CONFIRMED:` block appended to
   `daily_logs/2026-04-21.md` pointing at the 3-seat evidence.
3. Front-matter of the consolidated amendment updated to reference
   both rounds (initial 5-family drift; retroactive 3-seat confirm).
4. Lesson entry in `pipeline/institutional_memory/lessons.md` —
   blueprint-class → Tilth 3-seat; code-class → 5-family slate.
5. §0.5 Interface Index paired-commit row for the consolidated
   amendment (separate LOCK target — not part of this Thesis
   dispatch).

On 3-seat BLOCK (any seat fails):

- Route through L-005 two-audit cycle.
- Escalate to operator — retroactive-confirmation failure forces a
  conversation on whether to revert ledger row 91 or amend the
  consolidated artifact before a second 3-seat dispatch.

## 7. Out of scope

- Re-litigating per-gate semantics (all 12 gates LOCKED under
  `code_merge_rule=all_pass`).
- §4 v2.1 base-layer changes (parent-LOCK is stable).
- §0.5 Interface Index re-LOCK (separate artefact, separate round).
- New F-AMDT-* gate additions (not part of v2.2 scope).

## 8. Author persona directive

King Midas v1 Anthropic Claude Code, or any subsequent operator
persona authorised to dispatch Code / Blueprint Thesis rounds.
Consolidation dispatch is **blueprint-class** (not code-class)
because no gate modules change; only the blueprint reading-surface
changes.
