# Z-Rig / Arcanum Integration Research

Dispatch: `2026-06-17-zrig-arcanum-integration-handoff`

## Research Question

Should Z-Rig incorporate Arcanum, DomainSpec, or Craft surfaces, and if so, how
should that work be handed off for a later architecture and plan pass?

## Answer

Use Arcanum and DomainSpec as private parent-local lifecycle framing around
Z-Rig: governance, planning, review, evidence, Craft state, architecture
inventory, and bounded handoff. Do not treat Z-Rig as execution authority for
Arcanum, do not promote Z-Rig into public Arcanum, and do not create runtime
adapter or public command surfaces until engine authority proofs land.

The first concrete move is not "integrate Arcanum into Z-Rig." It is: create a
private remediation work-pack and Craft management state, then execute exactly
one bounded remediation SWU, preferably F1 gate fail-closed behavior or F3
residue schema/fatality policy.

## Evidence Boundary

Primary Z-Rig evidence:

- `projects/zrig/review/2026-06-17-zrig-engine-product-mode/findings.md`
- `projects/zrig/review/2026-06-17-zrig-engine-product-mode/understanding-map.md`
- `projects/zrig/ZRIG-ENGINE-PRODUCT-MODE-REVIEW-STRATEGY.md`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/`

Primary Arcanum/DomainSpec/Craft evidence:

- `/home/vrondelli/.codex/skills/invoke/SKILL.md`
- `/home/vrondelli/.codex/skills/context-builder/SKILL.md`
- `/home/vrondelli/.codex/skills/task-session/SKILL.md`
- `arcanum/arcana/craft/SKILL.md`
- `arcanum/arcana/architecture-pattern-inventory/SKILL.md`
- `arcanum/arcana/observability-derivation/SKILL.md`
- `arcanum/arcana/signal-observer/SKILL.md`
- `AGENTS.md`
- `SUBMODULE-DISCIPLINE.md`

## Synthesis

All four explorer lenses converge on the same boundary:

- **GO:** private parent-local governance, planning, review, management, and
  handoff artifacts.
- **REVISE / DEFER:** bounded execution until a ready work-pack and exactly one
  private remediation SWU exist.
- **NO-GO:** live authority, product-mode trust, public promotion, runtime
  adapter claims, public Z-Rig command surfaces, or treating Arcanum as Z-Rig's
  internal execution engine.

Source exists for Z-Rig review artifacts, F1-F14 findings, generic Arcanum
lifecycle contracts, Craft management rules, and public/private repository
boundaries.

Promotion-ready evidence does not exist for a Z-Rig-Arcanum runtime adapter,
Signal Observer bridge, Experiment Harness integration, public Z-Rig sigil or
spell, generated runtime package, or product-mode execution claim.

## Collected Explorer Returns

### Abramsky, Samson - Arcanum Capability Transfer

Verdict summary: integrate Arcanum/DomainSpec as an outer governance wrapper and
artifact handoff layer, not as Z-Rig's inner execution engine yet.

Z-Rig already has a coherent orchestrator skeleton: mode-aware waves, gates,
manifests, dispatch, residue, deploy/sentinel, and run summaries. But the
current review says it is "not yet product-mode trustworthy" because too much
success can pass through fallback, underdocumented, or non-authoritative paths
(`projects/zrig/review/2026-06-17-zrig-engine-product-mode/understanding-map.md:99-109`).
Arcanum should therefore wrap and harden evidence, planning, review, and
promotion. It should not be embedded as a live Z-Rig runtime substitute until
Z-Rig's own gate/residue/live trust issues are fixed.

Candidate verdicts:

- Z-Rig product-mode remediation pack via `invoke define/design/plan`: GO.
  Owner surface: Arcanum `invoke`, targeting
  `projects/zrig/development/product-mode-remediation/`. Artifact to create:
  `SPEC.md`, `DESIGN.md`, `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`,
  `EXECUTION-PACK.md`. Evidence: Invoke owns intent-to-artifact authoring and
  hands off execution (`/home/vrondelli/.codex/skills/invoke/SKILL.md:70-79`);
  findings rank F1-F14 (`projects/zrig/review/2026-06-17-zrig-engine-product-mode/findings.md:31-37`).
  Collapse-test: if the pack claims product readiness instead of producing
  bounded remediation tasks, it collapses into false assurance.
- Per-finding bounded execution with `task-session`: GO after a work-pack exists.
  Evidence: Task Session requires exactly one task, context pack, gates,
  validation, and evidence sync. Z-Rig findings are already discrete and
  ordered. Collapse-test: batching F1-F14 violates task-session's one-task
  boundary and hides gate failures.
- Runtime handoff adapter from Arcanum Task Session into Z-Rig dry-run/live:
  DEFER. Evidence: Context Builder runtime handoff must have strict obligation
  coverage and JSON/index evidence; Task Session blocks without complete
  handoff coverage; Z-Rig live bridge is underdocumented and identity-trusting
  (`findings.md:19-20`). Collapse-test: if "adapter exists" is treated as "live
  governed execution works," it collapses.
- Architecture Pattern Inventory for Z-Rig: GO. Owner surface:
  `architecture-pattern-inventory`. Artifact: `projects/zrig/architecture/`.
  Evidence: Z-Rig has architecture material: CLI commands, gate/state
  boundaries, bridge/deploy/audit boundaries. Collapse-test: if it documents
  ideal architecture as current behavior, it collapses.
- DomainSpec observability derivation over Z-Rig run/wave/gate/residue metrics:
  GO, design first. Owner surface: DomainSpec observability rules plus Z-Rig
  observability. Artifact:
  `projects/zrig/development/observability-derivation/OBSERVABILITY.md`.
  Collapse-test: if metrics are wired without tying them to product obligations,
  it becomes telemetry theater.
- Signal Observer bridge for Arcanum runs that review or execute Z-Rig tasks:
  GO narrow. Use for Arcanum-managed runs first; Z-Rig native telemetry adapter
  later.
- Experiment Harness for a reusable `zrig-integration` sigil/spell: DEFER until
  wrapper contract exists.
- Governed subagent dispatch for future Z-Rig reviews: GO.
- Embed Arcanum as Z-Rig's internal wave/gate engine: NO-GO now.

Source exists: yes for Z-Rig engine/review artifacts, Arcanum contracts,
DomainSpec observability rules, subagent governance, and Signal Observer.
Promotion-ready: no for a Z-Rig-Arcanum adapter or wrapper as reusable
capability. The missing proof is bounded execution evidence: work-pack, strict
context handoff, per-task validation, experiment harness examples, and
observer-compatible telemetry.

Best next move: create an Invoke-authored remediation/integration development
pack for Z-Rig with three lanes: product-mode remediation, runtime handoff
adapter design, and observability derivation. Then execute only F1 or F3 first
through `task-session`, because those are the sharpest tests of whether
governance makes Z-Rig stricter rather than merely better narrated.

### Ashby, W. Ross - Z-Rig Engine Preconditions

Overall verdict: NO-GO for product-mode Arcanum/DomainSpec/Craft integration
that treats Z-Rig as an execution authority. Narrow verdict: DEFER for any
live/side-effectful integration; GO only for read-only research ingestion,
dry-run demos, or an external harness that explicitly labels Z-Rig output as
untrusted until engine proofs land.

The engine has a coherent shape, but its authority surfaces are not yet reliable
enough: gates can pass semantically failed waves, live identity can be spoofed,
deploy/sentinel are not operator-reachable through the normal context, residue
can fail while success is reported, and failover caps are not shared wave
authority.

Obligation map:

- F1: Engine must fix. Implement specific gates or fail closed for missing gates
  in product/live modes. This is non-wrappable because gate pass/fail is the core
  authority boundary. Verdict: NO-GO.
- F2: Dry-run can remain demo/test if Arcanum labels it non-assurance and
  refuses to promote stub success. Verdict: GO for demo only.
- F3: Residue schema mismatch must be repaired; product/live mode must fail
  closed or visibly degrade assurance on residue failure. Verdict: DEFER.
- F4: Identity must come from trusted seat metadata or signed runtime metadata,
  not bridge output. Verdict: NO-GO.
- F5: Arcanum can document/validate the bridge contract, but cannot substitute
  for executable bridge proof. Verdict: DEFER.
- F6: W10/W11 side-effect paths require top-level context keys not supplied by
  normal pipeline context; CLI has no deploy/monitor path. Verdict: NO-GO for
  deploy/sentinel.
- F7: Arcanum can reject arbitrary deploy command configs, but product deploy
  support needs constrained operations or explicit approval gates inside/around
  the engine. Verdict: DEFER.
- F8: Dependencies must be declared before verification or live import can be
  trusted. Verdict: DEFER.
- F9: Failover cap must be shared per wave with concurrency control; external
  wrappers cannot reliably correct internal concurrent dispatch accounting.
  Verdict: NO-GO for live concurrent dispatch.
- F10: Clean-run semantics must align with W4/W5 evidence and skip behavior for
  W5.5/W8.5. Verdict: DEFER.
- F11: W6/W7 failure routing must be explicit or documented/tested as default
  escalation. Verdict: DEFER for FULL mode.
- F12: Arcanum can post-process completed vs skipped, but engine result
  accounting should be corrected. Verdict: GO with wrapper correction.
- F13: Treat `AUTO` as implementation extension unless promoted into spec.
  Verdict: GO with policy label.
- F14: Arcanum/Craft can maintain separate telemetry, but cannot claim Z-Rig
  metrics triggers are active. Verdict: GO for external metrics; DEFER for
  Z-Rig metrics.

First acceptance checks:

1. Gate proof: failed W10/W11 payloads must fail, and all spec-governed waves
   must use specific evaluators or fail closed in product/live mode.
2. Identity proof: spoofed W2 outputs from one actual model must not satisfy
   three-family diversity.
3. Context proof: normal CLI/pipeline path must pass intentional
   deploy/sentinel config or fail closed when absent.
4. Residue proof: a product/live run with residue write failure must not report
   clean success.
5. Failover proof: concurrent seats must share one protected per-wave failover
   counter.
6. Verification proof: fresh install must declare dependencies and run
   tests/imports without missing `pytest`, `requests`, or `psycopg2`.
7. Integration policy proof: Arcanum wrapper must refuse promotion from stub
   dry-run, generic gates, skipped-wave completion inflation, and unwired
   metrics.

### Loregian, Fosco - Craft Management Surface

Ledger recommendation: GO to start `projects/zrig/.craft/ledger.yml` and
`projects/zrig/CRAFT.md`. Result: pass for management-surface integration,
block for any runtime/product-mode execution claim.

Integration verdicts:

- GO: Start scoped Craft state for Z-Rig. Evidence: no
  `projects/zrig/.craft/ledger.yml` or `projects/zrig/CRAFT.md` exists, while
  Craft requires per-scope resolution and says to create only when no discovered
  space owns the scope (`arcanum/arcana/craft/SKILL.md:129-145`,
  `arcanum/arcana/craft/SKILL.md:310-319`). Z-Rig now has durable review
  artifacts and a structured F1-F14 backlog, so it fits Craft's durable local
  ledger use case (`arcanum/arcana/craft/SKILL.md:103-111`).
- GO: Treat Craft as Z-Rig management surface only. Craft governs file-backed
  state, human views, linking, blocker/decision/gap visibility, and
  recomposition evidence, but does not provide an automated command runner
  (`arcanum/arcana/craft/SKILL.md:14-18`).
- DEFER: Architecture/plan pass. The review packet produced verified findings,
  but `findings.md` is still "pending final coverage approval"
  (`projects/zrig/review/2026-06-17-zrig-engine-product-mode/findings.md:3-4`).
  Craft can index this state now; architecture/plan should wait until coverage
  approval and recomposition evidence are recorded.
- NO-GO: Any product-mode trust claim. The current assessment says Z-Rig is
  structurally promising but "not yet product-mode trustworthy"
  (`understanding-map.md:99-101`). F1 is critical; F6/F7 show deploy/sentinel
  reachability and SSH command-trust gaps.

Proposed ledger shape:

- Root context: `CTX-ZRIG-PRODUCT-MODE`
- Artifacts: `ART-ZRIG-REVIEW-STRATEGY`, `ART-ZRIG-ATTACKS`,
  `ART-ZRIG-FINDINGS`, `ART-ZRIG-UNDERSTANDING`
- Blockers: `BLK-ZRIG-GATES-GENERIC`, `BLK-ZRIG-LIVE-DEPLOY-SENTINEL`,
  `BLK-ZRIG-AUDITABILITY`, `BLK-ZRIG-RUNTIME-AUTHORITY`,
  `BLK-ZRIG-SPEC-DRIFT`
- Decisions: `DEC-ZRIG-GATE-POLICY`,
  `DEC-ZRIG-LIVE-IDENTITY-AUTHORITY`, `DEC-ZRIG-DEPLOY-SURFACE`,
  `DEC-ZRIG-RESIDUE-FATALITY`, `DEC-ZRIG-AUTO-SPEC`,
  `DEC-ZRIG-METRICS-STATUS`
- Gaps: `GAP-ZRIG-COVERAGE-APPROVAL`, `GAP-ZRIG-OPERATOR-CONTRACT`,
  `GAP-ZRIG-DEPENDENCY-MANIFEST`, `GAP-ZRIG-REPRO-HARNESS`,
  `GAP-ZRIG-RECOMPOSITION-PACKET`
- Next moves: `NEXT-ZRIG-CRAFT-START`, `NEXT-ZRIG-COVERAGE-APPROVAL`,
  `NEXT-ZRIG-ARCH-PASS`

Recomposition evidence required later:

- coverage approver receipt for the F1-F14 list;
- source-evidence plus executable-reproduction receipts per finding class;
- explicit distinction between dispatch/route evidence and execution evidence;
- child-context recomposition records before closing any lane;
- final parent-fit summary explaining which product-mode claim is supported,
  downgraded, or still blocked.

### Rittel, Horst - Public/Private Product Boundary

Overall verdict: DEFER for integration, with narrow GO paths for reference-only
use of existing public Arcanum contracts and strong NO-GO on copying
Z-Rig/OpenClaw/product material into public `arcanum`.

Boundary facts:

- `domainspec-core` is the private umbrella; `arcanum/` is public and must be
  treated as world-readable (`AGENTS.md:3-12`, `SUBMODULE-DISCIPLINE.md:5-17`).
- Public + private compose only in the private parent. Private content must not
  land in `arcanum` (`AGENTS.md:11`, `SUBMODULE-DISCIPLINE.md:16`).
- Arcanum already defines generic lifecycle owners: `dispatch-spec` validates
  route shape, `invoke` authors artifacts, `task-session` executes bounded work
  (`AGENTS.md:14-16`).
- Z-Rig is currently private/product-local corpus under `projects/zrig`, with
  OpenClaw/Analog/live/deploy/sentinel details.

GO:

- Use public Arcanum as the integration frame, not the payload.
- Use `invoke` for private handoff authoring.
- Use `task-session` for one bounded private execution task after a Z-Rig
  adapter/work-pack exists.
- Treat Z-Rig as an external/private runtime candidate only through
  adapter/handoff evidence.

DEFER:

- Any public Arcanum Z-Rig sigil/spell.
- Direct conversion of Z-Rig into a reusable sigil; use `skill-decomposer` first
  if extracting a neutral capability.
- Runtime installation or command exposure.

NO-GO:

- Copy `projects/zrig` review artifacts, QuickStart, OpenClaw bridge details, or
  product-mode claims into public `arcanum`.
- Make Z-Rig the orchestrator for Arcanum lifecycle authority.
- Publicly register Z-Rig as promotion-ready while product-mode findings remain
  open.
- Add broad new command surfaces in public Arcanum for `zrig`, `openclaw`,
  deploy, sentinel, or Analog-specific flows.

Recommended integration shape:

- Public reusable contracts: `arcanum/arcana`, `arcanum/formulae`,
  `arcanum/spells`, registry.
- Private product evidence and Z-Rig artifacts: `projects/zrig/**`.
- Private integration adapters/handoffs: parent-local artifacts, not public
  `arcanum`.

Public promotion path, later: run `skill-decomposer` on Z-Rig to extract only a
neutral reusable capability, then `skill-transcriptor`/`sigil-development` with
validation evidence. Until then: DEFER.

## Reviewer Calibration

The reviewer group accepted the handoff with edits:

- Popper: too many GO labels were non-vacuous only if narrowed to concrete
  artifacts, owners, commands/checks, and acceptance evidence. The first real
  proof should be a private remediation work-pack and one F1/F3 SWU.
- Tetlock: completed evidence supports governance/planning/review/state/handoff
  scaffolding, but not execution readiness, public promotion, runtime authority,
  live adapter readiness, or experiment-harness promotion.
- Kochen: adapter-shaped work must move from near-term plan to parked
  constraints. The handoff must say private governance now, runtime authority
  later or never.
