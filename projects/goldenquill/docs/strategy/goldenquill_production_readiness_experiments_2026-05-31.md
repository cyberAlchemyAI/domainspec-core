---
title: GoldenQuill Production Readiness Experiments
date: 2026-05-31
status: proposed
---

# Experiments And Hypotheses

## Experiment Rules

- Every experiment must be measurable from repository evidence.
- Every experiment must name success, failure interpretation, and next action.
- Experiments do not mutate production code unless later authorized through task-session.
- Experiments must preserve org isolation; no org contexts are inputs.

## Hypotheses

| ID | Hypothesis | Experiment | Measurement | Success Threshold | Failure Interpretation | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | A current-truth refresh pack reduces stale-claim risk for future agents. | Compare `PROJECT_STATUS.md`, `RUNTIME_MATURITY_MATRIX.md`, and `ACTIVE_BLUEPRINT_INDEX.md` against lock history and card/key evidence; produce a delta table. | Count stale or missing claims before/after refresh. | All row/key/card claims either match current evidence or are explicitly marked stale/deferred. | Front-door docs are not reliable enough for production task selection. | Task-session for current-truth refresh. |
| H2 | A product surface index reduces prototype/production confusion. | Index `apps/`, `landing/`, frontend docs, and `docs/whitepapers/` into status classes. | Count surfaces with unambiguous status, owner, allowed use, and blocker. | 100% of listed product surfaces have status and allowed-use labels. | Product claims still depend on tribal memory. | Task-session for `docs/PRODUCT_SURFACE_INDEX.md`. |
| H3 | An implementation-status matrix reduces time to select safe work. | Crosswalk skills, CLIs, modules, tests, maturity, blockers, and owner surfaces. | Time/steps needed to choose a safe-first candidate from matrix. | A new agent can identify first task, proof path, and gate path from the matrix alone. | Existing maturity docs are too coarse for task selection. | Task-session for `docs/IMPLEMENTATION_STATUS_MATRIX.md`. |
| H4 | A wheel packaging smoke catches substrate installation risk. | Build a wheel in a temp environment and import `pipeline.*` plus `golden_quill_substrate.*`. | Import pass/fail and package contents. | Wheel install can import both runtime and substrate modules. | Production install may omit contract substrate. | Add packaging test or adjust package discovery through task-session. |
| H5 | A unified verification wrapper reduces local/CI drift. | Create or dry-run a command inventory from tests, lint, signature, and CI workflows. | Number of required checks captured by wrapper spec. | Wrapper covers standard local proof path and names intentionally skipped checks. | Agents will keep using partial checks inconsistently. | Task-session for `scripts/verify_all.sh` or equivalent. |
| H6 | Provider-boundary signed-register wiring check catches unsafe production omission. | Inspect/test production cloud route to prove signed-register context is passed and literal scan cannot be skipped silently. | Presence of test/lint proof for production route. | Production provider path fails closed when signed register is absent or invalid. | Security assumption is not enforceable enough for production. | Decision-gate if semantics change; otherwise task-session for test coverage. |
| H7 | Whitepaper format hygiene prevents source-of-truth ambiguity. | Run file/type inventory for `docs/whitepapers/*` and classify canonical source vs generated/binary artifact. | Count ambiguous or mismatched file extensions. | Every whitepaper artifact has clear format and canonicality. | Docs source cannot be safely edited by future agents. | Decision-gate for rename/regenerate policy. |
| H8 | Explicit UI/status documentation prevents v0.1 scope drift. | Classify `apps/tilth_ui_react/`, legacy/archive UI, and demo app against frontend boundary and v0.1 no-UI decision. | Count UI surfaces with status and v0.1 production eligibility. | No UI surface can be mistaken for v0.1 production requirement. | UI work may distract from headless v0.1 readiness. | Task-session for status docs only, or decision-gate if product stance changes. |

## Experiment Order

1. H1 current-truth refresh.
2. H2 product surface index.
3. H3 implementation-status matrix.
4. H5 unified verification wrapper.
5. H4 wheel packaging smoke.
6. H6 signed-register wiring proof.
7. H7 whitepaper hygiene.
8. H8 UI/status documentation.

## Readiness Gate

GoldenQuill is ready to start production implementation work when H1, H2, and H3 have passing artifacts, and every selected follow-on task has either a validation path or a decision-gate requirement.
