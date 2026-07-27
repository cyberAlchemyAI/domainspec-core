# Codex Goal Handoff Pack

This is persisted session evidence for one execution. It is not a canonical
product, Design, or Plan document.

## Identity

- Task/SWU: `SWU-COOP-001`
- Source task:
  `ops/development/2026-07-25-co-op-engine-browser-artifact/work-pack/tasks/TASK-COOP-L0-CONTRACT.md`
- Work-pack:
  `ops/development/2026-07-25-co-op-engine-browser-artifact/WORK-PACK.md`
- Session/run id: `20260726T044915Z-swu-coop-001`
- Runtime handoff: `codex-goal`
- Repository revision before execution:
  `82be80e6ab74553d974d818160ff4b3e22313801`
- Evidence date: 2026-07-26
- Builder mode: lean, strict, runtime, Markdown plus JSON/index

## Obligation Coverage

| ID | Status | Selected evidence | Resolution |
| --- | --- | --- | --- |
| O-01 package/test entry | covered | task “Package contract” | private dependency-free ESM package with exact `test:contract` script |
| O-02 record/result types | covered | task “Data model”; SPEC “Shared Record Contract” | erasable TypeScript shapes with typed diagnostics |
| O-03 admission behavior | covered | task “Algorithm”; Architecture `RecordSchema`/`AdmissionValidator` | injected `asOf`, all diagnostics, stable order, admit only on empty diagnostics |
| O-04 current policy | covered | SPEC “Project Card Admission and Freshness”; task “Fixture contract” | 72-hour SLA, exact 30-day interval, fixed-time staleness |
| O-05 visibility admission | covered | SPEC D-004; glossary “Visibility class” | every required path has exactly one of five classes; missing/unknown blocks |
| O-06 normalized Poker fixture | covered | task “Fixture contract”; shared execution context | approved 72 hours replaces research-era 48 hours; 48 is negative fixture |
| O-07 discriminating tests | covered | validation strategy | one positive plus policy, stale, truth, missing-class, unknown-class, determinism cases |
| O-08 scope/non-goals | covered | SWU manifest; task “Write scope” | exactly four files; no dependency, lockfile, UI, persistence, hosting, or other mutation |
| O-09 verification | covered | task “Validation” | exact npm test and scoped diff-check commands |
| O-10 closeout | covered | closeout sync contract | exact source/owner receipts, target inventory, baseline, deltas, validation, no successor |
| O-11 blocked stop | covered | task “Execution owner and result” | stop on source, runtime, scope, policy, or discrimination blocker |
| O-12 evidence ceiling | covered | Plan Distill and Design acceptance | selected SWU remains admission only; planned HTML prototype cannot enter its scope |

Strict coverage: `pass` — 12/12 covered, zero resolved-by-assumption,
zero blocked.

## Selected Sources

1. `work-pack/tasks/TASK-COOP-L0-CONTRACT.md`
   - Selectors: Objective; Smallest Working Unit; Data model; Algorithm;
     Fixture contract; Package contract; Done criteria; Validation;
     Synchronization
   - Obligations: O-01–O-11
   - Evidence: source-of-truth execution contract and exact algorithm.
2. `SWU-MANIFEST.json`
   - Selector: selected `SWU-COOP-001` object
   - Obligations: O-08, O-11, O-12
   - Evidence: machine-readable singular selection, write/forbidden scope,
     result shape; separate `SWU-COOP-002` remains planned-unselected.
3. `CLOSEOUT-SYNC-CONTRACT.json`
   - Selector: contract for `SWU-COOP-001`
   - Obligations: O-10
   - Evidence: exact closeout owner, targets, baseline rule, deltas, receipts.
4. `SPEC.md`
   - Selectors: Shared Record Contract; Project Card Admission and Freshness;
     Define Owner Assignment; D-003; D-004
   - Obligations: O-02–O-06
   - Evidence: approved product and policy authority.
5. `GLOSSARY.md`
   - Selectors: Eligible experiment; Response overdue; Stale card; Claim
     ceiling; Truth record; Visibility class; Policy version
   - Obligations: O-02, O-04, O-05
   - Evidence: plain semantic boundaries and forbidden inflation.
6. `ARCHITECTURE-BUNDLE.md`
   - Selectors: Low-Level Components; Record admission; Significant Behavior
     Scenario; Planned Witness Contracts; L0 layer
   - Obligations: O-03, O-07, O-12
   - Evidence: admitted-record architecture and planned witness boundary.
7. `PLAN-DISTILL-VALIDATION.md`
   - Selectors: Current Smallest Coherent Unit; Split and Atomicity Verdict;
     Refresh Addendum; Premortem; Verdict
   - Obligations: O-08, O-12
   - Evidence: why admission is atomic and why the HTML prototype is a
     separate later selection rather than scope for this goal.
8. `VALIDATION-STRATEGY.md`
   - Selectors: Matrix; HTML Prototype Matrix; Evidence Ceiling
   - Obligations: O-07, O-09, O-12
   - Evidence: admission discrimination; separate browser matrix does not
     broaden the selected goal.

## Architecture Guidance

- `admitProjectRecord(candidate, asOf)` is a pure deterministic boundary.
- Expected invalid inputs return values, not thrown exceptions.
- Diagnostics sort by code and then path.
- Admission requires every invariant; do not expose partial admission.
- Use readonly or copied admitted output so negative fixture mutation cannot
  change the positive baseline.
- Do not implement collaboration transitions or render projections.

## Related Feature Context

The browser artifact will eventually project admitted records into
self-guided and facilitated modes. L0 creates only the record accepted by
those later projections.

The refreshed Plan also contains `SWU-COOP-002`, a static HTML content/IA
prototype. It is planned-unselected, has its own future one-file scope, and
cannot be executed from this pack.

The Poker source sample originally used a 48-hour response SLA. The approved
D-003 policy is 72 hours. The runtime must treat 72 as current truth and use 48
only as the named policy-mismatch fixture.

## Constraints and Non-Goals

- Preserve existing user changes and the public/private boundary.
- No source under `arcanum/` or `implementation/domainspec/`.
- No package installation or lockfile.
- No React, Vite, HTML, CSS, route, browser, network, persistence, hosting,
  deployment, copy, or audit implementation.
- Do not read the wall clock, filesystem, environment, network, or browser
  state in admission logic.
- Do not call L0 success a page, presentation, privacy, comprehension, or
  recruitment proof.

## Write Scope

- `projects/co-op-engine/package.json`
- `projects/co-op-engine/src/contracts/project-record.ts`
- `projects/co-op-engine/test/fixtures/poker-record.ts`
- `projects/co-op-engine/test/project-record.test.ts`

No other write is permitted.

## Done Criteria

- package is private, ESM, dependency-free, and has exact test command;
- record, visibility, policy, result, and diagnostic types are explicit;
- `asOf` is injected;
- current policy and every required visibility path are enforced;
- normalized Poker fixture passes;
- five independent negative mutations fail with exact code/path;
- repeat result and unmodified baseline assertions pass;
- no dependency/lockfile or extra file appears;
- both validation commands pass.

## Validation Surface

```bash
npm --prefix projects/co-op-engine run test:contract
git diff --check -- projects/co-op-engine
```

## Gaps and Blockers

None at handoff time. Broad fallback exploration is not allowed.

If an input is missing, Node cannot execute the declared TypeScript form, a
write-scope conflict exists, approved policy contradicts this pack, or a seeded
failure cannot be discriminated, stop and report the exact blocker.

## Authority Precedence

1. Approved `SPEC.md` and recorded user decisions.
2. Accepted `ARCHITECTURE-BUNDLE.md` and Design acceptance review.
3. `WORK-PACK.md`, task contract, SWU manifest, and closeout contract.
4. This selector-level runtime pack.

## Fallback Exploration Rule

No uncovered obligation or named runtime gap exists. Do not broaden repository
exploration. If a new gap appears, name it and stop; a resumed run may inspect
only the minimum source needed for that named gap and must report the source
and whether it changed the result.

## Provenance

| Source | SHA-256 |
| --- | --- |
| task contract | `218ad8be884e11123727b0ffec6fe6cab2a0c22b62e5f9caeb57c3a40bd9b8cf` |
| SWU manifest | `e2c122b318fe1ad71cce1bcf33d6dfadc97919f604725ddab852cbc2ecd6092e` |
| closeout contract | `7f738d63625ef2aecec3d41750851d6057939e9c12b6639966559f5bc0aaee60` |
| approved SPEC | `5964310e47692df81cdbe66eb68e103fd328628790d7899fbdebd4afd9b03a37` |
| glossary | `40a022de41d6540e53e1cd04bc89e1be32fd0a64f7480094014baf3d9cc4b078` |
| architecture | `9a4895d5cd5cacf2f4b6266d29a04805e1acf6241ac87127e49b4ae7a137b375` |
| Plan Distill | `503a0bfdcbaa74f8a2c993ddcd3999e6e86f463efca7d97507ffca69adb4b86b` |
| validation strategy | `3be4683d361a0ba4226980f111ecb2204a0892d46fbaa5ed546c819d90140fa0` |

## Output Paths

- Markdown: this file
- JSON/index: `CONTEXT-PACK.index.json`
