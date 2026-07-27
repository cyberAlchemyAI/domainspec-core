# Codex Goal Profile: SWU-COOP-001

## Source

| Field | Value |
| --- | --- |
| Work-pack | `ops/development/2026-07-25-co-op-engine-browser-artifact/WORK-PACK.md` |
| Parent task | `ops/development/2026-07-25-co-op-engine-browser-artifact/work-pack/tasks/TASK-COOP-L0-CONTRACT.md` |
| Selected SWU | `SWU-COOP-001` in `SWU-MANIFEST.json` |
| Source contracts | task, SPEC, glossary, architecture, Plan Distill, validation strategy |
| Handoff pack | `ops/development/2026-07-25-co-op-engine-browser-artifact/session-evidence/20260726T044915Z-swu-coop-001/CONTEXT-PACK.md` |
| Handoff index | `ops/development/2026-07-25-co-op-engine-browser-artifact/session-evidence/20260726T044915Z-swu-coop-001/CONTEXT-PACK.index.json` |

## Readiness

| Check | Status | Evidence |
| --- | --- | --- |
| SWU selected | pass | manifest selects exactly `SWU-COOP-001` |
| Dependencies | pass | Define, Design, acceptance review, Plan, and Distill pass |
| Target baseline | pass | `projects/co-op-engine/` absent at profile creation |
| Write scope | pass | exactly four future files |
| Done criteria | pass | positive, five negative, determinism, no-dependency, hygiene checks |
| Verification surface | pass | exact npm contract test and scoped diff check |
| Closeout contract | pass | terminal result shape and later owner synchronization predeclared |
| Handoff pair | pass | Markdown and JSON/index exist |
| Strict coverage | pass | 12/12 obligations; eight digest-bound sources; zero gaps |
| Fallback exploration | pass | none allowed; a new gap stops the run |
| Blocking state | pass | no current L0 blocker |

## Native Codex Goal

```text
/goal Execute only SWU-COOP-001 from ops/development/2026-07-25-co-op-engine-browser-artifact/WORK-PACK.md.

Outcome: create a dependency-free private ESM package at projects/co-op-engine whose pure erasable-TypeScript admitProjectRecord(candidate, asOf) boundary admits the normalized Poker Agent Arena ProjectRecord only when all approved structure, truth, owner, source, claim, experiment, policy, freshness, eligibility, and required-field visibility invariants pass; return stable typed diagnostics for expected invalid inputs.

Verification surface: npm --prefix projects/co-op-engine run test:contract must pass the normalized positive fixture, the 48-hour SLA policy-mismatch fixture, stale-asOf fixture, missing-current-witness fixture, missing-visibility fixture, unknown-visibility-class fixture, and deterministic/non-mutation assertions. Then git diff --check -- projects/co-op-engine must pass, and the final changed-path inventory must equal the four allowed paths.

Constraints: read the strict handoff Markdown at ops/development/2026-07-25-co-op-engine-browser-artifact/session-evidence/20260726T044915Z-swu-coop-001/CONTEXT-PACK.md and its JSON index at ops/development/2026-07-25-co-op-engine-browser-artifact/session-evidence/20260726T044915Z-swu-coop-001/CONTEXT-PACK.index.json first; verify the selected-source SHA-256 bindings and confirm the target-path absence/conflict baseline before mutation. Use Node 22 built-in testing and erasable TypeScript. Inject asOf, collect all diagnostics, sort by code then path, and never read wall-clock, filesystem, environment, network, or browser state inside admission logic. Preserve the approved 72-hour SLA and exact 30-day expiry; retain the research-era 48-hour value only as the named negative fixture. Expected invalid records return diagnostic values rather than throwing. Do not install dependencies or create a lockfile.

Boundaries: write only projects/co-op-engine/package.json, projects/co-op-engine/src/contracts/project-record.ts, projects/co-op-engine/test/fixtures/poker-record.ts, and projects/co-op-engine/test/project-record.test.ts. Do not write anywhere else. Do not touch arcanum/, implementation/domainspec/, another project, Plan/Design evidence, observability, receipts, UI, routes, React/Vite, network, persistence, hosting, deployment, copy, or audits. Do not claim page, presentation, privacy-surface, comprehension, recruitment, deployment, or release completion.

Iteration policy: use pack-first execution. Implement the smallest contract and positive fixture, run the focused contract test, then add one negative mutation at a time and rerun. After any failure, name one evidence-backed hypothesis and make only the smallest in-scope correction. Recheck the allowed path inventory and both verification commands after every complete cycle. Broad repository exploration is not allowed because the pack has no named gaps. If a resumed run has an explicitly named new gap, inspect only the minimum source needed for that gap and report the gap, extra source path, and whether it changed the result.

Blocked stop condition: stop without broadening scope if a selected source is missing or has a digest mismatch, the target path has conflicting user changes, Node cannot execute the declared erasable-TypeScript test form without an extra dependency/file, approved policy contradicts the pack, an intended negative cannot be discriminated by its exact code/path, an extra file is required, or the same blocker survives three consecutive hypothesis-driven validation cycles. Report the exact blocker, evidence, files touched, validation results, residue, and safest reroute using the expected SWU result shape from SWU-MANIFEST.json. Mark completion only when both verification commands and the exact changed-path check pass.
```

## Audit Notes

- Outcome: one fail-closed L0 record-admission contract, not a website.
- Verification: contract tests, negative discrimination, deterministic replay,
  exact changed paths, scoped diff hygiene.
- Write boundary: four files under `projects/co-op-engine/`.
- Context boundary: strict pack and index first; no broad fallback gap exists.
- Extra-source reporting: required if a later resumed run authorizes one named
  gap.
- Iteration: positive baseline, one negative at a time, smallest correction,
  full recheck.
- Stop: source/baseline/scope/runtime/policy/discrimination blocker or three
  consecutive failed cycles on the same blocker.
- Runtime ownership: native Codex Goals; this profile does not start, pause,
  resume, or complete the goal.

## Codex Goal Profile Result

- Source work-pack:
  `ops/development/2026-07-25-co-op-engine-browser-artifact/WORK-PACK.md`
- Selected unit: `SWU-COOP-001`
- Readiness: pass
- Verification surface: exact npm contract test plus scoped diff and
  changed-path inventory
- Boundaries: four declared files; strict selected context
- Handoff pack: Markdown and JSON/index paths above
- Strict coverage: pass
- Fallback exploration: none
- Extra-source reporting: required if a named gap is later authorized
- Validation: profile/source/index/readiness checks pass
