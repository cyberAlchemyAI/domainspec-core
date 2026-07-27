---
id: ui-prototyping-studio-craft-view
feature: ui-prototyping-studio
title: "UI Prototyping Studio Craft Ledger (human view)"
summary: Indexed navigation surface for the active governed-state projection implementation and preserved historical deep-spec state.
status: active
node_type: craft-view
updatedAt: 2026-07-27
---

# UI Prototyping Studio Craft Ledger

Human-readable view of [.craft/ledger.yml](.craft/ledger.yml). The ledger is the
source of truth; this page is an indexed navigation surface.

## Quick Links

- Current next move: continue the bounded Task Session Until Blocker chain
  with selected
  [`SWU-GSP-003`](development/invoke-runs/20260727T042935Z-architecture-review-refresh/work-pack/tasks/TASK-GSP-003-current-head-projection.md).
- Active work:
  [`CTX-UPS-GSP-EXECUTION`](#context-ctx-ups-gsp-execution) using the
  [amended work-pack](development/invoke-runs/20260727T042935Z-architecture-review-refresh/WORK-PACK.md).
- Execution decisions: amended plan approved; shared local-`tsx` proof route;
  actor-neutral explicit acknowledgment; deterministic seven-unit chain order.
- Historical packages: June deep spec and July governed-state package remain
  proposal/evidence history, not current execution authority.
- Active blockers: [fixtures](#blocker-blk-fixture-corpus-001) · [identity types](#blocker-blk-identity-types-002) · [failure states](#blocker-blk-failure-states-003) · [invariants](#blocker-blk-invariants-uncalibrated-004).
- Active gaps: [ergonomics unproven](#gap-gap-ergonomics-unproven-001) · [component registry](#gap-gap-component-registry-002) · [conflict algebra](#gap-gap-conflict-algebra-003) · [contract drift](#gap-gap-contract-drift-004) · [docs/code split](#gap-gap-docs-code-split-005).
- Key artifacts: [deep-spec proposal](development/deep-spec-dispatch/DEEP-SPEC-PROPOSAL.md) · [one-shot plan](development/deep-spec-dispatch/ONE-SHOT-IMPLEMENTATION-PLAN.md) · [synthesized design](development/deep-spec-dispatch/SYNTHESIZED-DEEP-DESIGN.md) · [result + verdict](development/deep-spec-dispatch/RESULT.md).

## Current Execution State

### <a id="context-ctx-ups-gsp-execution"></a>CTX-UPS-GSP-EXECUTION — Governed State Projection Implementation

- Stage: `execute`
- Gate: `pass`
- Completed: `SWU-GSP-001` (typecheck, focused helper 2/2, standard Playwright
  15/15, joined closeout).
- Completed: `SWU-GSP-002` (independent-process freshness 3/3, unit/slice
  65/65, joined closeout).
- Selected unit: `SWU-GSP-003` only; the captured series has one unique
  successor at every later step.
- Plan:
  [2026-07-27 amended work-pack](development/invoke-runs/20260727T042935Z-architecture-review-refresh/WORK-PACK.md).
- Review input:
  [accepted findings](development/reviews/20260727-architecture-plan-deep-spec-review/findings.md).
- Sequence: evidence harness → persisted freshness → application projection →
  visible diff → action/annotation/mobile → handoff readiness → receipt-driven
  docs/Craft closeout.
- Boundary: implementation completion will not prove human ergonomics or
  authorize release.

The older sections below preserve dated Craft history. Where their next moves,
counts, or “current” wording disagree with this section and the source ledger,
this section and `.craft/ledger.yml` control.

## Contexts

### <a id="context-ctx-ups-root"></a>CTX-UPS-ROOT — UI Prototyping Studio

- Stage: `execute`
- Gate: `pass`
- Purpose: execute the amended governed-state projection repair while
  preserving proposal, evidence, implementation, human-study, and release
  authority boundaries.

#### <a id="next-move"></a>Next Move

Run Task Session for selected `SWU-GSP-003` from the amended 2026-07-27
work-pack. Later SWUs remain dependency-gated and execute only after a joined
predecessor closeout.

### <a id="context-ctx-ups-extraction"></a>CTX-UPS-EXTRACTION — Standalone Extraction (closed)

- Stage: `closed`
- Gate: `pass`
- Purpose: extract the feature **code** out of the deprecating `implementation/domainspec` monorepo and stand `ui-prototyping-studio` up as a self-contained, runnable project (per [DEC-DEPRECATE-PIVOT-007](#decision-dec-deprecate-pivot-007)).
- Result: the standalone backend, CLI, preview, reversible mutation core, and
  checked-in tests exist. Remaining trust defects recomposed into
  `CTX-UPS-GSP-EXECUTION`.

### <a id="decision-dec-deprecate-pivot-007"></a>DEC-DEPRECATE-PIVOT-007 — whole standalone project (closed)

- Selected: **Whole standalone project incl. code** (domainspec is being deprecated).
- Impact: supersedes the docs-only move; triggers `CTX-UPS-EXTRACTION` and resolves the docs/code split by relocating the code too.

### <a id="decision-dec-fresh-minimal-008"></a>DEC-FRESH-MINIMAL-008 — fresh minimal (closed)

- Selected: **Fresh minimal — keep code + plan, archive the rest.** Of 220 docs, 200 were a vendored reference tree and 19 the full-vision spec the deep-spec judged mostly paper.
- Impact: root spine is now `README.md` + lean `SPEC.md` (L0→L2) + `.craft/` + `development/`; the 19 vision docs and 200 reference files moved to `provenance/`. Build on the validated L0 code rather than rewrite. Code extraction (P1–P5) remains.

### <a id="context-ctx-ups-deep-spec"></a>CTX-UPS-DEEP-SPEC — Deep-Spec Dispatch Exploration

- Stage: `closed`
- Gate: `flag`
- Closure evidence: [RESULT.md](development/deep-spec-dispatch/RESULT.md), [SUBAGENT-LIFECYCLE.json](development/deep-spec-dispatch/SUBAGENT-LIFECYCLE.json) (12 agents, lifecycle pass)
- Recomposed into [CTX-UPS-ROOT](#context-ctx-ups-root) with a CONDITIONAL readiness verdict.

## Decisions

### <a id="decision-dec-one-shot-scope-002"></a>DEC-ONE-SHOT-SCOPE-002 — one-shot scope

- Question: What scope should the first one-shot implementation target?
- Status: `active`, **blocking**.
- Options: L0→L2 survival/trust floor (recommended) · Full L0–L6 one shot · Defer until fixtures + types + failure states exist.
- Impact: whether implementation can begin one-shot at a safe altitude or must wait on net-new builds.
- Evidence: [RESULT.md](development/deep-spec-dispatch/RESULT.md).

### <a id="decision-dec-oq1-trust-meter"></a>DEC-OQ1-TRUST-METER (OQ-1)

- Question: Does a session-level override/accuracy trust meter help or harm trust calibration?
- Status: `active`, **blocking** (gates L6). Plan says: do not ship the trust meter unvalidated.

### <a id="decision-dec-oq2-saw-diff"></a>DEC-OQ2-SAW-DIFF (OQ-2)

- Question: Minimal non-theater proxy that a human actually saw the diff before an irreversible apply?
- Status: `active`, **blocking** (gates L6 + apply-approval ergonomics).

### <a id="decision-dec-oq3-handoff-carry"></a>DEC-OQ3-HANDOFF-CARRY (OQ-3)

- Question: On operator handoff, does session-scoped tuning carry-with-attribution, reset, or prompt?
- Status: `active`, **blocking** (gates L5 Inv-8 operator-provenance).

### <a id="decision-dec-oq4-import-integrity"></a>DEC-OQ4-IMPORT-INTEGRITY (OQ-4)

- Question: Is artifact import-integrity (forged anchor / re-imported handoff) in the MVP or deferred?
- Status: `active`, non-blocking scope boundary.

### <a id="decision-dec-execution-scope-001"></a>DEC-EXECUTION-SCOPE-001 — how to execute the dispatch (closed)

- Selected: **Run the full route now** (operator approved subagent spend).
- Impact: 12 subagents ran end-to-end producing all artifacts and the readiness verdict.

## Blockers

### <a id="blocker-blk-fixture-corpus-001"></a>BLK-FIXTURE-CORPUS-001

- Lane: `qa` · Status: `active`, `refined` · Route: `ux-evidence-validator`.
- Summary: the `FX-*` fixture corpus is a paper design (zero FX IDs in `e2e/`) and `@axe-core/playwright` is not installed, so the strict-superset gate suite the plan relies on does not exist.
- Closure: author the corpus, add axe, run a calibrate pass to promote the 11 specified hard gates.

### <a id="blocker-blk-identity-types-002"></a>BLK-IDENTITY-TYPES-002

- Lane: `tech` · Status: `active`, `refined` · Route: `task-session`.
- Summary: L4 identity/conformance types (`UIElementIdentity`, `UIVisualSignature`, …) do not exist in `models.ts`; `DiffSummary` is only `{added,changed,removed}` counts. s8 proves the absence makes confirm-identity effectively impossible.
- Closure: add the identity/DNA types + an `IdentityEvidencePanel` surface.

### <a id="blocker-blk-failure-states-003"></a>BLK-FAILURE-STATES-003

- Lane: `tech` · Status: `active`, `refined` · Route: `task-session`.
- Summary: both state machines and `mock-api.ts` model only the happy path; no failure injection. L3/L5 need new domain + mock work.
- Closure: add `GenerationFailed`/`SynthesisTimedOut`/`SourceStale`/`ApplyConflicted` states + mock failure injection.

### <a id="blocker-blk-invariants-uncalibrated-004"></a>BLK-INVARIANTS-UNCALIBRATED-004

- Lane: `validator` · Status: `active`, `refined` · Route: `residuality-spec`.
- Summary: `Inv-1..8` are proposed-not-calibrated and the SPEC is unmutated; building against them codes to uncalibrated invariants.
- Closure: calibrate against authored fixtures and fold into the canonical SPEC first.

## Enablers

- **ENA-DEEP-SPEC-ROUTE-001** — the deep-spec dispatch validates `pass`; route-shape evidence only.
- **ENA-L0-SPINE-EXISTS-002** — L0 spine genuinely exists (10-state machine in `models.ts`, governance enforcement in `mock-api.ts`, two real e2e specs), enabling a realistic L0→L2 one-shot.

## Gaps

### <a id="gap-gap-ergonomics-unproven-001"></a>GAP-ERGONOMICS-UNPROVEN-001

- Severity: `flag` · Treatment: `human-study` · Owner: ux-evidence-validator + s8 study.
- The entire ergonomics floor — the stated first principle — is unproven; L4 is proxy-only and L6 is human-study-gated.

### <a id="gap-gap-component-registry-002"></a>GAP-COMPONENT-REGISTRY-002

- Severity: `flag` · Treatment: `resolved-by-design-merge` · Status: **resolved** (2026-06-24). Component-registry persistence/index entity (R-1) specified as **`UIIdentityIndex`** (a repo-scoped derived read-model over the append-only event log) in [UIIdentityIndex-DESIGN.md](development/component-registry-spec/UIIdentityIndex-DESIGN.md) and **merged into `SYNTHESIZED-DEEP-DESIGN §2.4`** (R-1 row marked CLOSED; R-7 fill-approach decided). Remaining: A2 implementation (`models.ts` types + projection), gated on L4 — a build node, not a design hole. Also specifies the `BLK-IDENTITY-TYPES-002` types.

### <a id="gap-gap-conflict-algebra-003"></a>GAP-CONFLICT-ALGEBRA-003

- Severity: `flag` · Treatment: `defer`. Full CommentEvent→MutationTask conflict algebra unspecified (R-2).

### <a id="gap-gap-contract-drift-004"></a>GAP-CONTRACT-DRIFT-004

- Severity: `flag` · Treatment: `resolved-by-fold` · Status: **resolved** (human-view reconciled 2026-06-24). `RevisionApplied` (staged-preview/accept-diff) and `RevisionRecorded` (committed head) are two distinct, load-bearing states in the **live CLI backend** (`apply-and-stage.ts` / `accept-staged-revision.ts`); verified by 62/62 unit/slice green. The only remaining `RevisionApplied`-absent copy is the deferred-SPA `mock-api.ts` in the `implementation/domainspec` submodule — a stale double, **superseded by the lifted backend**, downstream of `GAP-DOCS-CODE-SPLIT-005`.

### <a id="gap-gap-docs-code-split-005"></a>GAP-DOCS-CODE-SPLIT-005

- Severity: `flag` · Treatment: `resolved-by-logical-id-repoint` · Status: **resolved** (B4, `DEC-DOCS-CODE-SPLIT-022`, 2026-06-24) · Owner: operator.
- The spec moved to `projects/ui-prototyping-studio`; the submodule's `docs/features/ui-prototyping-studio/*.md` copies are gone, leaving dangling refs. **Decision: path-free logical ids** (`docs/features/ui-prototyping-studio/SPEC.md` → `ui-prototyping-studio:SPEC.md`) so the submodule can't depend on a parent path. Repointed the 5 source files (handoff `mock-api.ts` + `server.test.ts` assertions, `PRODUCT-COMPONENTS-IDEA.md` links, 2 drift reports) — **submodule commit `6f57151`**; generated data (`.data`/telemetry) regenerates. Canonical spec home = `projects/ui-prototyping-studio/`. This **supersedes `resolved-by-extraction-P4`** — the refs are decoupled now, independent of extraction timing.

## Route Handoffs (completed)

- **HND-DEEP-SPEC-VALIDATE-001** → `dispatch-spec` validate → `pass` (VALIDATION=pass).
- **HND-DEEP-SPEC-EXEC-001** → `refine` execute (12-agent workflow) → `pass` (lifecycle pass, SPEC unmutated).
- **HND-READINESS-001** → `implementation-readiness` → `flag` (CONDITIONAL: L0→L2 one-shot realistic, full L0–L6 not).

## Recomposition

`CTX-UPS-DEEP-SPEC` → `CTX-UPS-ROOT` (`pass`): exploration complete; produced deepened
design, invariants `Inv-1..8`, UX evidence, planned Playwright suite, and naive-user
findings, synthesized into proposal + plan + conditional verdict. Residue: ergonomics
floor unproven, OQ-1..4 open, fixtures/identity-types/failure-states absent, invariants
proposed-not-calibrated. Next parent move: decision-gate on scope + OQ-1..4.
