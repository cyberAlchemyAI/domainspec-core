---
title: Blueprint §4 Logician — Amendment v2.1.1 (§4.14a — Governance Plan Preflight deterministic PRE-gate)
filed: 2026-04-19
operator: Josh
amendment_status: LOCKED 2026-05-08 — paired with architecture v7.0.1 + §0.5 v5. GPP three-tier closure: Tier 1 PASS (gpp_det_report_2026-05-08), Tier 2 live dispatch (council_findings_2026-05-08; Red Team groq/openai/gpt-oss-120b + Reasoner google/gemini-2.5-pro; 14 findings dispositioned), Tier 3 signed manifest (gpp_manifest_2026-05-08). L-005 two-audit predecessor: thesis_round_gpp_2026-04-19/ Audit #2 PASS.
parent_lock: pipeline/blueprint/v0.1/section_04_logician.md  (§4 v2.1 LOCKED 2026-04-18)
supersedes_relationship: inserts BEFORE the planned §4 v2.3 (Privacy Router), v2.4 (Canary), v2.5 (Runtime Integrity) amendments. v2.1.1 is non-disruptive to §4.1-§4.13 — it adds §4.14a as a new Logician PRE-gate subsection, extends §4.2.1 ordered PRE-gate table with 11 rows, extends §6 failure-code family with 12 F-GPP-* codes, and adds one §11 Law-map entry.
companion_architecture_amendment: pipeline/architecture/v0.1/architecture_v7_0_1_amendment.md  (Section E.P)
companion_index_amendment: pipeline/blueprint/v0.1/section_00_5_v5_amendment.md  (27 paired-commit §0.5 rows — Thesis-round 2026-04-19 F-2 decision)
scope_source: pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md
tool_implementation: pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_det.py
future_lock_citations:
  - pipeline/architecture/v0.1/architecture_v7_0_1_amendment.md  # paired
  - pipeline/blueprint/v0.1/section_00_5_v5_amendment.md          # paired
version_wording_discipline: "LOCKED" refers to on-disk LOCKED state only. Forward-looking targets use "target-LOCK at" wording.
---

# Amendment intent

Implement the Section E.P architectural commitment (architecture v7.0.1) as a concrete Logician PRE-gate family in §4. GPP-DET runs as ten deterministic checks plus one dispatch-time check plus one synthesis-tier check — twelve total PRE/POST-gate rows. The Python implementation is already on disk at `pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_det.py` (v1 tool); this amendment pins the contract as §4 blueprint discipline.

# Proposed new subsection — §4.14a

## §4.14a — Governance Plan Preflight (GPP) deterministic PRE-gate

### §4.14a.1 — Purpose

Plan-layer artifacts (scope-close plans, sequencing plans, dispatch plans, preflight existence audits, handoff contracts) are audited by a deterministic PRE-gate before they can gate any Thesis round or engineering phase. GPP-DET is that gate.

GPP-DET fires at two pipeline fire-points:

1. **Pipeline-start fire.** When a run invokes a Thesis round, GPP-DET runs on the round's gating plan artifact before any seat is invoked. Failure blocks round dispatch. No tokens spent on a doomed round.
2. **Manifest-dispatch fire.** When a round dispatches from a plan-layer artifact, the dispatch layer verifies a valid signed GPP manifest is present. Failure = `F-GPP-MANIFEST-MISSING`, dispatch blocked.

### §4.14a.2 — Input

- The plan-layer artifact's file path (markdown file with YAML front-matter).
- All sibling plan sub-docs in the same dispatch set (front-matter keys `scope_parent`, `architecture_parent`, `blueprint_parent`, `dispatch_parent`, `audit_parent`, `companion`, `predecessor_audit` as applicable).
- `router.yaml` (for FAMILY-TAXONOMY cross-check).
- Predecessor existence audit (for BLOCKER-CARRY-CHECK).
- §0.5 Interface Index (for INDEX-STALE-DRYRUN).

### §4.14a.3 — Predicate

GPP-DET runs the following ten deterministic checks in order. Each check returns PASS, FAIL, or FLAG.

| # | Check ID | Predicate | Failure code |
|---|---|---|---|
| 1 | CITE-RESOLVE | Every citation in the plan resolves to an on-disk file (excluding paths declared in the file's `future_lock_citations` front-matter list) | `F-GPP-CITATION-UNRESOLVED` |
| 2 | VERSION-RESOLVE | Every current-state LOCK claim matches the target file's on-disk version; forward-looking target-LOCK phrasing is exempt per the file's `version_wording_discipline` front-matter | `F-GPP-VERSION-UNRESOLVED` |
| 3 | XDOC-REF | Every cross-document section reference (`§N`, `#heading`) resolves to an existing heading in the target file | `F-GPP-CROSSDOC-BROKEN` |
| 4 | ROW-COUNT-ARITHMETIC | Every "paired commit / N rows" claim is verified by counting the row list in the same doc | `F-GPP-ROW-COUNT-MISMATCH` |
| 5 | HASH-PIN | Canonical-bytes SHA-3-512 hash (§0.5 v4 recipe) computed and recorded to manifest; subsequent runs compare | `F-GPP-CANONICAL-HASH-MISMATCH` |
| 6 | INDEX-STALE-DRYRUN | Each proposed §0.5 row has all required fields populated or explicitly marked `TO_BE_PINNED_AT_COMMIT` | `F-GPP-INDEX-STALE-ON-PROPOSED-ROWS` |
| 7 | FAMILY-TAXONOMY | Every "N families" claim cross-checks against `router.yaml` family count derived from seat-to-model bindings | `F-GPP-FAMILY-TAXONOMY-MISMATCH` |
| 8 | SCOPE-FREEZE-BACKDOOR-FLAG | Heuristic grep for scope-widening phrases outside code-span contexts; finding is FLAG (not FAIL), requires Tier 2 council disposition | `F-GPP-SCOPE-FREEZE-BACKDOOR-UNREVIEWED` |
| 9 | VERSION-SKEW-DISCLOSURE | If plan cites an on-disk version that mismatches a predecessor claim, plan must contain explicit version-skew note | `F-GPP-VERSION-SKEW-UNDISCLOSED` |
| 10 | BLOCKER-CARRY-CHECK | Every blocker in a predecessor existence audit appears in current plan as carried or resolved | `F-GPP-BLOCKER-UNCARRIED` |

Plus two non-deterministic-check dispatch-tier rows:

| # | Check ID | Predicate | Failure code |
|---|---|---|---|
| 11 | MANIFEST-PRESENT-AT-DISPATCH | Signed GPP manifest for the gating plan exists and is valid at round-open | `F-GPP-MANIFEST-MISSING` |
| 12 | FINDING-DISPOSITION-COMPLETE | Every Tier 2 COUNCIL finding has a Tier 3 SYNTHESIS disposition (FOLDED_IN / REJECTED / DEFERRED with rationale) | `F-GPP-FINDING-UNDISPOSED` |

### §4.14a.4 — Fail-closed semantics

All twelve checks fail-closed per §4.3 discipline. The tool exit code is non-zero on any FAIL. FLAGs require Tier 2 disposition before dispatch; an undisposed FLAG at round-open is equivalent to a FAIL.

### §4.14a.5 — Reference implementation

The canonical reference implementation is `pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_det.py` (tool version `v1`). The tool uses stdlib + PyYAML only. The implementation is on-disk at time of this amendment filing; Phase 0 engineering hardens it per the queue in `pipeline/engineering/da_vinci_engineer_prompt_v2.md` §7.

### §4.14a.6 — Ordering in §4.2.1

GPP-DET fires at pipeline-start, ordered **before** all other PRE-gates. Rationale: a plan-layer artifact that fails GPP-DET should not cost any further PRE-gate compute — failing-fast at the plan-layer saves the entire downstream PRE-gate chain from wasted evaluation, preserves Autonomy Rule 2 (Magic Step, Test-your-own-work) semantics at zero token cost, and keeps operator attention on the plan rather than on confusing downstream errors that trace back to a broken plan. Specifically: GPP-DET rows are ordered before Item 4c Key Presence preflight (v7.1 v2.5 target-LOCK) and before Item 4d Drift-from-Locked-Router PRE-gate (v2.5 target-LOCK) when those amendments land.

MANIFEST-PRESENT-AT-DISPATCH fires at round dispatch, ordered at the dispatch layer before any seat-binding resolution.

FINDING-DISPOSITION-COMPLETE fires at Tier 3 synthesis time.

# Proposed §4.2.1 PRE-gate-check table additions

Eleven new rows ordered at the top of the §4.2.1 ordered PRE-gate table (GPP-DET pipeline-start is the new first-gate):

| Order | Check ID | Fires at | Failure code | Source |
|---|---|---|---|---|
| 1 | GPP-DET-CITE-RESOLVE | pipeline-start | `F-GPP-CITATION-UNRESOLVED` | §4.14a |
| 2 | GPP-DET-VERSION-RESOLVE | pipeline-start | `F-GPP-VERSION-UNRESOLVED` | §4.14a |
| 3 | GPP-DET-XDOC-REF | pipeline-start | `F-GPP-CROSSDOC-BROKEN` | §4.14a |
| 4 | GPP-DET-ROW-COUNT-ARITHMETIC | pipeline-start | `F-GPP-ROW-COUNT-MISMATCH` | §4.14a |
| 5 | GPP-DET-HASH-PIN | pipeline-start | `F-GPP-CANONICAL-HASH-MISMATCH` | §4.14a |
| 6 | GPP-DET-INDEX-STALE-DRYRUN | pipeline-start | `F-GPP-INDEX-STALE-ON-PROPOSED-ROWS` | §4.14a |
| 7 | GPP-DET-FAMILY-TAXONOMY | pipeline-start | `F-GPP-FAMILY-TAXONOMY-MISMATCH` | §4.14a |
| 8 | GPP-DET-SCOPE-FREEZE-BACKDOOR-FLAG | pipeline-start (flag) → Tier 2 disposition | `F-GPP-SCOPE-FREEZE-BACKDOOR-UNREVIEWED` | §4.14a |
| 9 | GPP-DET-VERSION-SKEW-DISCLOSURE | pipeline-start | `F-GPP-VERSION-SKEW-UNDISCLOSED` | §4.14a |
| 10 | GPP-DET-BLOCKER-CARRY-CHECK | pipeline-start | `F-GPP-BLOCKER-UNCARRIED` | §4.14a |
| 11 | GPP-MANIFEST-PRESENT-AT-DISPATCH | round-open dispatch | `F-GPP-MANIFEST-MISSING` | §4.14a |

Existing PRE-gate rows (§4.2.1 v2.1) retain their ordering relative to each other; they all shift to positions 12+. The v7.1 Privacy Router PRE-gate and the v2.5 Key Presence / Drift-from-Locked-Router PRE-gates land after these 11 rows when their amendments LOCK.

Plus one POST-gate / synthesis-tier row:

| Order | Check ID | Fires at | Failure code | Source |
|---|---|---|---|---|
| POST-synth | GPP-FINDING-DISPOSITION-COMPLETE | Tier 3 synthesis close | `F-GPP-FINDING-UNDISPOSED` | §4.14a |

# Proposed §6 failure-code family extension

Add the full `F-GPP-*` family (12 codes) per `gpp_spec_v1.md` §5. Naming convention matches existing `F-PRE-*` / `F-POST-*` patterns; category prefix `F-GPP-` is new. All fail-closed semantics.

| Code | Tier | Fires at |
|---|---|---|
| `F-GPP-CITATION-UNRESOLVED` | DET | pipeline-start |
| `F-GPP-VERSION-UNRESOLVED` | DET | pipeline-start |
| `F-GPP-CROSSDOC-BROKEN` | DET | pipeline-start |
| `F-GPP-ROW-COUNT-MISMATCH` | DET | pipeline-start |
| `F-GPP-CANONICAL-HASH-MISMATCH` | DET | pipeline-start |
| `F-GPP-INDEX-STALE-ON-PROPOSED-ROWS` | DET | pipeline-start |
| `F-GPP-FAMILY-TAXONOMY-MISMATCH` | DET | pipeline-start |
| `F-GPP-SCOPE-FREEZE-BACKDOOR-UNREVIEWED` | DET→COUNCIL | pipeline-start (flag) / Tier 2 disposition |
| `F-GPP-VERSION-SKEW-UNDISCLOSED` | DET | pipeline-start |
| `F-GPP-BLOCKER-UNCARRIED` | DET | pipeline-start |
| `F-GPP-MANIFEST-MISSING` | dispatch | round-open |
| `F-GPP-FINDING-UNDISPOSED` | SYNTHESIS | Tier 3 close |

# Proposed §11 Law-map addition

| Law | Mechanism |
|---|---|
| Law 2 — No Boundary Drift | GPP-DET Check 8 SCOPE-FREEZE-BACKDOOR-FLAG + Tier 2 Red Team adversarial pass on plan-layer artifacts. Previously no mechanism gated plan-layer boundary drift; this closes the gap. |

No changes to Law 1 / 3 / 4 / 5 entries.

# Proposed §5 wiring (paragraph addition to §5 v5 / v6)

§5 run-lifecycle gains one paragraph naming GPP as a pre-round fire-point (text for §5 to absorb in its next LOCK window, or as a §5 v6.1 targeted amendment):

> When a pipeline run is triggered by a plan-layer artifact (scope-close, sequencing plan, dispatch plan, preflight existence audit, or handoff contract per §4.14a.1), §5 run-lifecycle invokes GPP-DET first. GPP-DET output is evaluated; any FAIL returns control to the operator with the failure report, no seats invoked, no tokens spent. FLAGs require Tier 2 disposition before the run proceeds. A PASS+disposed state allows the run to proceed to seat resolution.

§5 is not amended by this v2.1.1 file; the paragraph is noted here for the next §5 LOCK to absorb.

# Non-goals for this amendment

- Does not redefine §4.1-§4.13 semantics.
- Does not introduce new seat-model bindings. Tier 2 uses existing `router.yaml` red_team + reasoner_review seats.
- Does not introduce a new primitive kind in §0.5. All 26 paired-commit rows map to existing kinds (mechanism, pre-gate-check, post-gate-check, failure-code, schema, interface-contract).
- Does not add a CI hook. Operator-run in v0.1; Phase 2b may add CI integration.
- Does not touch A11 R.6 ALLOWED list.
- Does not introduce a UI.

# Paired-commit reminder

This §4 v2.1.1 amendment LOCKs atomically with:
- `pipeline/architecture/v0.1/architecture_v7_0_1_amendment.md` (Section E.P)
- `pipeline/blueprint/v0.1/section_00_5_v5_amendment.md` (27 §0.5 rows — Thesis-round F-2 decision)

F-INDEX-STALE PRE-gate in §0.5 v4 fails-closed if any of the 27 rows is missing at commit time.

# Thesis round expectations

- **Audit pass 1 (Editor + Judge):** Editor audits §4.14a.1-§4.14a.6 copy clarity, failure-code naming, §4.2.1 table-row wording. Judge scores against §4 v2.1 rubric (PRE-gate family addition), §0.5 paired-commit discipline rubric, Section E rubric (cross-family rigor preserved).
- **Audit pass 2 (Red Team + Reasoner):** Red Team adversarial on: can a plan-layer artifact be crafted to pass all 10 DET checks while smuggling scope-drift? does the pipeline-start ordering create a race condition with §5 run-lifecycle? is there a manifest-replay attack (signed manifest reused on a newer plan)? Reasoner audits decision journal for: skipped alternatives (CI hook at v0.1, Editor at Tier 2, Ed25519-only), under-justified claims.
- **Cross-family composition:** Editor + Judge + Red Team + Reasoner seats. Cross-family composition resolved at round-open via `router.yaml`; minimum four distinct provider families across the audit passes, five distinct families including Anthropic-family synthesis at Tier 3. Cross-family rigor satisfied by construction (router-level binding constraints), not by file-pinning specific model strings.
- **Synthesis:** operator + Opus 4.7 emits LOCK commit atomically with paired v7.0.1 + §0.5 v5.

# End of amendment
