---
tags: [research, raw-returns, verification-weaver, public-private-boundary]
node_type: research
is_session: false
layer: research
nature: reference
status: candidate
created: 2026-06-21
dispatch_id: 2026-06-21-verification-weaver-research
dispatch_type: research
working_folder: ops/development/verification-weaver/research/2026-06-21-verification-weaver-research/
sources:
  - implementation/domainspec/tools/test-derivation-engine/
  - implementation/domainspec/TEST-PIPELINE.md
  - arcanum/arcana/test-derivation/SKILL.md
  - arcanum/arcana/ux-evidence-validator/SKILL.md
  - arcanum/arcana/experiment-harness/SKILL.md
  - arcanum/framework/EXPERIMENT-HARNESS-STANDARD.md
---

# Research Transcript: Verification Weaver

This file preserves the parent-assembled research return for dispatch
`2026-06-21-verification-weaver-research`. It is a private-parent research
artifact: it may cite private source paths as evidence, but the future public
`arcanum` package must use synthetic/public-safe fixtures and fresh public code.

## Explorer: Private Deterministic Lane

Angle: computational/private-determinism corpus.

Key inspected surfaces:

- `implementation/domainspec/.codex/agents/domainspec-test-designer.agent.toml`
- `implementation/domainspec/tools/test-derivation-engine/README.md`
- `implementation/domainspec/tools/test-derivation-engine/package.json`
- `implementation/domainspec/tools/test-derivation-engine/src/`
- `implementation/domainspec/development/deterministic-test-derivation-engine/`
- `implementation/domainspec/development/refinement-runs/2026-06-12-test-derivation-c2-cluster/`

Findings:

- The strongest private capability is
  `implementation/domainspec/tools/test-derivation-engine/`.
- Its intended shape is compiler-like: parse DomainSpec docs -> typed graph ->
  derive deterministic delta -> content-addressed obligation keys -> emit specs
  and tests.
- `README.md` names `G` types for nodes, edges, and obligations, deterministic
  serialization, and an L0 round-trip falsification gate.
- The package scripts expose practical commands such as `roundtrip`.
- Internal private evidence is stronger than the current public Arcanum lane but
  still gated: `CRAFT.md` records an L0 pass for one feature and a fail for a
  second feature due to oracle/convention and delta-rule gaps.
- The private lane provides a public lesson, not public code: deterministic test
  derivation is legitimate only for formalized inputs with a coverage oracle.
- The public lesson should be phrased as "deterministic testing compiler for
  formalized inputs, with honest residue", not as "AI test generator".

Gaps:

- Formal-language coverage is limited.
- Semantic normalization still needs governance before any public promotion.
- Any public Arcanum package must be built fresh and must not port the private
  engine code or private examples.

## Explorer: Public Arcanum Owner Lane

Angle: information-architecture/public-Arcanum corpus.

Key inspected surfaces:

- `arcanum/arcana/test-derivation/SKILL.md`
- `arcanum/arcana/ux-evidence-validator/SKILL.md`
- `arcanum/arcana/experiment-harness/SKILL.md`
- `arcanum/arcana/architecture-pattern-inventory/SKILL.md`
- `arcanum/arcana/research-evidence-harness/SKILL.md`

Findings:

- `test-derivation` is a draft/repository-local public Arcanum lane for
  deterministic spec-to-obligation derivation. Its own tool is L0
  state-transition scope, and its contract says the private DomainSpec engine is
  a design reference only with no private code ported.
- `ux-evidence-validator` is seed/not promoted. Its validator contract and
  fixture plan exist, but executable Playwright validator code and calibrated
  fixture evidence do not.
- `experiment-harness` is the registered mechanics owner for repeatable
  development experiments, fixture validation, runtime outputs, reports, and
  observability handoff. It does not own artifact meaning.
- `architecture-pattern-inventory` is the registered mapping owner for
  architecture evidence and architecture-to-test gaps from repository evidence.
- `research-evidence-harness` is a public sigil surface for research schema,
  fixture, metric, dry-run, and evidence-status discipline; it is
  claim-status-limited and preserves dry-run/live separation.

Conclusion:

The missing public capability is not another runner. The missing capability is
a testing-specific evidence router/composer that classifies targets, selects
owner lanes, records obligations/evidence/gaps/residue, and joins native
receipts.

## Explorer: UI/UX Evidence Lane

Angle: behavioral/UI-UX evidence corpus.

Key inspected surfaces:

- `implementation/domainspec/TEST-PIPELINE.md`
- `arcanum/arcana/ux-evidence-validator/development/UX-PLAYWRIGHT-VALIDATOR-SPEC.md`
- `arcanum/arcana/ux-evidence-validator/development/UX-PLAYWRIGHT-FIXTURE-PLAN.md`
- `implementation/domainspec/apps/web/playwright.config.ts`
- Representative Playwright test surfaces under `implementation/domainspec`

Findings:

- `TEST-PIPELINE.md` already sketches UI E2E derivation when a feature has
  `UI-SPEC.md`, `UI-ARCHITECTURE.md`, or stories.
- The UI pipeline expects Playwright checks for navigation, user journeys,
  form validation, state reflection, accessibility, route behavior, and
  responsive behavior.
- Current private tests show role locators, keyboard traversal, visible focus,
  ARIA/live-region checks, route mocks, and breakpoint loops as reusable
  evidence patterns.
- `ux-evidence-validator` defines browser evidence outputs including
  screenshots, traces, accessibility output, ARIA snapshots, DOM measurements,
  console/network summaries, and a residue ledger.

Gaps:

- There is no public bridge yet from UI specs/stories to validator scenarios and
  persisted evidence bundles.
- UX evidence must preserve human residue for comprehension, workload, trust,
  confidence, delight, visual attention, and real-user task success.
- Until calibrated fixtures and harness code exist, UX validation remains
  seed/spec/fixture-plan evidence.

## Explorer: Practical Validation Lane

Angle: systems/practical-validation corpus.

Key inspected surfaces:

- `implementation/domainspec` package scripts and test suites.
- Backend tests using Node/TypeScript and Fastify injection patterns.
- Web Playwright test configuration and E2E suites.
- Internal tool tests using temp directories and shell validators.
- `validation/poker-team` testing and infra patterns.
- Arcanum fixture runners such as invoke/refine/dispatch validation scripts.

Findings:

- Real validation surfaces are heterogeneous: `pnpm`, `npm`, `node --test`,
  `vitest`, Playwright, shell scripts, Python tests, and Arcanum fixture
  runners.
- Useful common shapes exist: fixture directories, pass/fail controls, resume
  or safe wrappers, environment checks, receipts, and explicit generated-output
  exclusions.
- A public package should discover manifests and phase execution through owner
  adapters, not hide every command behind one opaque runner.

Gaps:

- The validation graph is fragmented across projects.
- E2E execution is environment-sensitive.
- Generated artifacts and local logs can look like evidence unless the package
  blocks them from promotion input.
- Public/private leakage risk is high if private examples are copied into
  public fixtures.

## Synthesizer Return

Recommended shape: create a new public candidate Arcana capability named
`verification-weaver`.

Core verb: `route`.

Scope:

- classify a testing target;
- select owner lanes;
- hand off to existing owners;
- join native lane receipts into a parent `VERIFICATION-WEAVE` receipt;
- preserve obligations, evidence, gaps, residue, and candidate owner routes.

Non-ownership:

- It does not derive tests.
- It does not validate UX.
- It does not execute experiments.
- It does not map architecture.
- It does not adjudicate research claims by itself.
- It does not execute task sessions.
- It does not mutate definitions.
- It does not promote artifacts.

## Reviewer Gates

### Tarski: Precedent Gate

Verdict: `REVISE`.

The precedent path is valid only if the package is a candidate/seed public
Arcana router and receipt contract. It must not be a promoted canonical tester.

Required corrections:

- Replace "tracks promotion" with "tracks promotion candidates, owner routes,
  and residue".
- Make `route` testing-specific.
- State non-ownership explicitly.
- Use synthetic/public-safe examples.
- Do not expose registry/generated runtime surfaces until public docs, quality
  bar, anti-patterns, output contract, public-boundary scan, and experiment
  evidence exist.

### Wittgenstein: Definition Gate

Verdict: `REVISE`.

The package is viable if its language is sharp:

- `route`: produce a typed route plan plus parent receipt.
- `target classification`: finite enum with discriminants.
- `owner lane`: owner capability, owned verb, input contract, output receipt,
  evidence artifact, stop conditions, and promotion boundary.
- `obligation`: source-anchored, owner-scoped requirement with stable key.
- `evidence`: concrete artifact path or handle with provenance and owner.
- `gap`: missing or failed obligation/evidence with next route.
- `residue`: unresolved material after routing/execution.
- `receipt`: structured parent record containing target, lanes, owner artifacts,
  status, gaps, residue, and next route.
- `adjudicate`: compare owner receipts against declared obligations and emit
  `pass`, `flag`, or `block`; promotion remains owner-gated.

Avoid:

- "all-in-one testing tool"
- "proves UX"
- "executes and promotes"
- "derives evidence"
- "tracks promotion" without owner gate

### Bell: Counterexample Gate

Verdict: `REVISE`.

Mitigation requirements:

- Add a fail-closed classifier with `unsupported_reason`, `oracle_type`, owner
  lane, allowed evidence roots, and decomposition rules.
- Make `VERIFICATION-WEAVE` a parent receipt only.
- Block private paths, generated outputs, local observability logs, and
  private implementation evidence from public package content.
- Require oracle binding before formal/testing claims.
- Keep promotion action to `none` or `candidate-request`.
- Treat UX validation as seed/spec/fixture-plan until calibrated Playwright
  harness evidence exists.

Required negative controls:

- `NC-MIX-001`
- `NC-UNSUPPORTED-001`
- `NC-PRIVATE-001`
- `NC-GENERATED-001`
- `NC-NO-ORACLE-001`
- `NC-UX-HUMAN-001`
- `NC-UX-DENSE-001`
- `NC-E2E-FLAKE-001`
- `NC-ADAPTER-001`
- `NC-RESEARCH-DRYRUN-001`
- `NC-ARCH-FOLDER-ONLY-001`
- `NC-RECEIPT-PROMOTE-001`

## Research Conclusion

Build the package as an Invoke development package first. The next executable
work should create a candidate public `arcanum/arcana/verification-weaver`
package with synthetic fixtures and a minimal receipt validator. It should not
copy private code or private examples into public `arcanum`.

## Internal Evidence Annex

The private parent findings may retain private source refs for traceability:

- `implementation/domainspec/tools/test-derivation-engine/`
- `implementation/domainspec/tools/test-derivation-engine/CRAFT.md`
- `implementation/domainspec/TEST-PIPELINE.md`
- `validation/poker-team/`

These references are internal research evidence only. Public package wording
must use abstracted deterministic derivation precedent, synthetic fixtures
derived from lessons, and public owner contracts. Public `arcanum` artifacts
must not contain private fixtures, private examples, private result claims, or
private implementation paths as evidence.
