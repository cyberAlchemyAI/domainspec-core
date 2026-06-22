---
tags: [findings, verification-weaver, public-private-boundary, promotion-guardrail]
node_type: findings
is_session: false
layer: research
nature: synthesis
status: candidate
created: 2026-06-21
dispatch_id: 2026-06-21-verification-weaver-research
dispatch_type: research
working_folder: ops/development/verification-weaver/research/2026-06-21-verification-weaver-research/
sources:
  - ops/development/verification-weaver/research/2026-06-21-verification-weaver-research/research.md
  - arcanum/arcana/test-derivation/SKILL.md
  - arcanum/arcana/ux-evidence-validator/SKILL.md
  - arcanum/arcana/experiment-harness/SKILL.md
  - arcanum/framework/EXPERIMENT-HARNESS-STANDARD.md
---

# Findings: Verification Weaver

## Short Verdict

`verification-weaver` is viable as a candidate public Arcana
testing-specific router and parent receipt contract.

It should classify testing targets, select owner lanes, hand off to those
owners, join native lane receipts, record gaps/residue, and track candidate
promotion routes. It is not a promoted canonical tester and must not execute,
validate, derive, promote, or mutate owner outputs.

## Verdict Matrix

| Question | Verdict | Required boundary |
| --- | --- | --- |
| Should `verification-weaver` exist? | Yes, as candidate | Router and receipt contract only. |
| Is it a canonical tester? | No | No registry or generated runtime exposure until gates pass. |
| Core verb | `route` | Classify target, select lanes, hand off, join receipts, record gaps/residue. |
| Parent output | `VERIFICATION-WEAVE` | Parent receipt only; lane outputs remain native. |
| Promotion authority | No | Track candidate routes and residue; owner capability promotes. |
| Public readiness | Not yet | Needs synthetic fixtures, public-boundary scan, quality bar, anti-patterns, output contract, and experiment evidence. |
| Failure posture | Fail closed | Mixed, unsupported, no-oracle, private, generated-only, and flaky cases block or return residue. |

## Capability Map

| Source signal | Testing role | Owner lane |
| --- | --- | --- |
| Private deterministic derivation engine has internal evidence, including an L0 pass for one feature and known generalization gates for broader corpus coverage. | Internal research precedent only: deterministic compiler-like derivation is valid for formalized inputs with an oracle and honest gaps. | `test-derivation` |
| Public `test-derivation` is draft/repository-local; its Arcanum tool is L0 state-transition scope, with no LLM/network in the obligation path and a round-trip oracle. It explicitly treats the private engine as design reference only and ports no private code. | Public formal derivation lane, status-limited. | `test-derivation` |
| `TEST-PIPELINE.md` sketches UI E2E derivation from `UI-SPEC.md`, `UI-ARCHITECTURE.md`, stories, and operations. | UI derivation evidence source, not public capability by itself. | `ux-evidence-validator` plus future bridge |
| `ux-evidence-validator` is seed/not promoted. It defines Playwright/browser evidence outputs and human residue categories, but has no executable Playwright validator code or calibrated fixture evidence yet. | Browser/UX evidence lane, seed status. | `ux-evidence-validator` |
| `experiment-harness` and `EXPERIMENT-HARNESS-STANDARD.md` define repeatable fixture/run/report mechanics and generated-output boundaries. | Registered execution mechanics and validation-evidence lane. | `experiment-harness` |
| `architecture-pattern-inventory` maps repo layers, dependency rules, tests, and recurring patterns from evidence. | Registered architecture-to-test-gap mapping lane. | `architecture-pattern-inventory` |
| `research-evidence-harness` preserves dry-run/live separation and blocks evidence upgrades without live support. | Public research evidence lane, claim-status-limited. | `research-evidence-harness` |

## Owner Boundaries

| Capability | Owns | Does not own |
| --- | --- | --- |
| `verification-weaver` | Testing-specific route, target classification, lane selection, handoff, parent receipt, gaps/residue, candidate owner routes. | Derivation, UX validation, experiment execution, architecture mapping, task execution, definition mutation, promotion. |
| `test-derivation` | Deterministic formal derivation and native specs/tests. | Cross-lane routing. |
| `ux-evidence-validator` | UX/browser evidence, L0-L6 evidence, human residue. | Formal derivation or promotion. |
| `experiment-harness` | Repeatable execution mechanics, adapter runs, experiment receipts, resume. | Semantic ownership of test meaning. |
| `architecture-pattern-inventory` | Architecture-to-test-gap mapping from repo evidence. | Test execution. |
| `research-evidence-harness` | Research schema, metrics, dry-run/live evidence sufficiency. | UX or code execution. |
| Owning capability | Promotion decisions. | Parent receipt upgrades by `verification-weaver`. |

## Required Definitions

- `route`: produce a typed route plan plus parent `VERIFICATION-WEAVE` receipt.
- `target classification`: finite enum with discriminants, such as
  `spec_derivation`, `frontend_ux`, `execution_repeatability`,
  `research_evidence`, `architecture_gap`, `mixed`, and `unsupported`.
- `owner lane`: an owner capability reference, owned verb, input contract,
  output receipt, evidence artifact, stop conditions, and promotion boundary.
- `obligation`: source-anchored, owner-scoped requirement with a stable key and
  expected evidence.
- `evidence`: concrete artifact path or handle with provenance and owner.
- `gap`: missing or failed obligation/evidence with owner and next route.
- `residue`: unresolved material after routing or owner execution.
- `receipt`: structured record containing target, lanes, owner artifacts,
  status, gaps, residue, and next route.
- `adjudicate`: parent-receipt sufficiency classification only. It compares
  owner receipts against declared obligations and emits `pass`, `flag`, or
  `block`; it is not lane validation, evidence-status upgrade, promotion, or
  semantic authority.

## Gate Repairs

| Gate | Status | Repair included |
| --- | --- | --- |
| Tarski precedent | REVISE | Candidate/seed public router only; no registry/runtime until public docs, quality bar, anti-patterns, output contract, boundary scan, and experiment evidence exist. |
| Wittgenstein definition | REVISE | The package defines its core nouns and avoids generic "all-in-one testing" language. |
| Bell counterexample | REVISE | The package requires fail-closed classifier, parent receipt, deny/allow rules, oracle binding, no promotion upgrades, and UX seed-only status until calibrated harness exists. |

## Public-Safe Recommendation

Proceed with a development package for a future public
`arcanum/arcana/verification-weaver` capability.

The public implementation must be built fresh from public-safe contracts and
synthetic fixtures. Private paths, private examples, generated outputs, and
local observability logs may inform this private research package but must not
be copied into public `arcanum`.

Public package text should say "abstracted deterministic derivation precedent"
and "synthetic fixtures derived from lessons"; it should not cite private
implementation paths or private pass/fail details as public evidence.

## Required Negative Controls

| Control | Expected result |
| --- | --- |
| `NC-MIX-001` | Mixed target bundle splits into lane receipts or blocks. |
| `NC-UNSUPPORTED-001` | Arbitrary target with no classifier support blocks. |
| `NC-PRIVATE-001` | Private source path blocks public fixture use or is redacted before public output. |
| `NC-GENERATED-001` | Generated-only source cannot prove authority. |
| `NC-NO-ORACLE-001` | Formal/testing claim without oracle binding blocks. |
| `NC-UX-HUMAN-001` | Mechanically passing UI with human comprehension risk flags human residue. |
| `NC-UX-DENSE-001` | Dense expert UI remains a false-positive trap, not a hard block. |
| `NC-E2E-FLAKE-001` | Flaky E2E environment blocks promotion evidence. |
| `NC-ADAPTER-001` | Missing or unsupported adapter blocks joined receipt. |
| `NC-RESEARCH-DRYRUN-001` | Synthetic dry run cannot promote research claim evidence. |
| `NC-ARCH-FOLDER-ONLY-001` | Folder-name inference alone cannot stand in for architecture mapping. |
| `NC-RECEIPT-PROMOTE-001` | Parent receipt cannot promote lane outputs. |

## Invoke Package Decision

Create the development package under
`ops/development/verification-weaver/development-package/`.

The package should include:

- `DEFINE.md`
- `DESIGN.md`
- `PLAN.md`
- `OUTPUT-CONTRACT.md`
- `QUALITY-BAR.md`
- `ANTI-PATTERNS.md`
- `IMPLEMENTATION-LAYERING.md`
- `DISPATCH-TRACE.md`
- `DISPATCH.json`
- `DISTILL-VALIDATION.md`
- `fixtures/synthetic/README.md`
- `negative-controls/NEGATIVE-CONTROLS.md`
- `tasks/SWU-VW-001.md`
- `WORK-PACK.md`
- `RUNTIME-HANDOFF.md`
- `INVOKE-RESULT.md`

The first executable work unit should implement a candidate public Arcana
package with README/SKILL, receipt schema, classifier fixtures, negative
controls, and validation runner, without registry exposure.

## Internal Evidence Annex

Private source refs remain available in this private parent research package for
traceability. They are excluded from the future public package as fixtures,
examples, and proof claims.

Excluded from public package content:

- private implementation paths;
- private fixtures and examples;
- private pass/fail result claims;
- generated runtime outputs;
- local observability logs.
