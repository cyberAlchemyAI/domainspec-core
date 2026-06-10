# Infra-Spec Gap-Hunt Ledger (Lane L7 — Skeptical Gap Hunter)

Date: 2026-06-08
Parent dispatch: `infra-spec-research-strategy-20260603`
Lane: L7 — Skeptical Gap Hunter
Question: what have we NOT mapped yet?
Mode: READ-ONLY (only write is this ledger)
Status: research findings only — no infra-spec authority claimed.

## Method Note

Hunted across `arcanum/`, `.github/`, `.arcanum/`, `.data/`, `ops/`, `projects/`,
`validation/`, root `.gitignore`/`.gitmodules`, and the project DomainSpec
infra/SLO templates. Classification labels per strategy non-negotiables:
`documented`, `implementation-backed`, `candidate`, `analogy`, `residue`,
`absence` (explicit negative evidence). Each finding carries a path or an
explicit absence note.

---

## A. Net-New Candidate Concepts (gaps other lanes likely miss)

### G1. Broken / unpopulated submodule = unowned hidden state (PRIMARY) [implementation-backed]
- Evidence: `git submodule status` shows `implementation/domainspec` flagged `+`
  (working tree differs from recorded commit `970dab5...`), `validation/poker-team`
  flagged `-` (uninitialized), and `validation/sigil-spell-sandbox` has
  **no `.gitmodules` mapping at all** (`fatal: no submodule mapping found in
  .gitmodules for path 'validation/sigil-spell-sandbox'`).
- Both `validation/poker-team/` and `validation/sigil-spell-sandbox/` are EMPTY
  directories in this checkout.
- `implementation/domainspec/` contains only a `.git` pointer file (89B), no source.
- Why other lanes miss it: L1/L3/L6 point at paths *inside* these submodules
  (`implementation/domainspec/infra/`, `validation/poker-team/infra/`) and will
  silently return "not found" without recognizing the submodule itself is the gap.
- Concept: infra-spec needs a **state-namespace ownership record for vendored /
  submodule state** — recorded-commit vs checked-out-commit vs populated must be
  a first-class operational-proof-status axis. A submodule with no `.gitmodules`
  entry is the canonical "unowned state" boundary object.
- Where it should have appeared: `ops/development/infra-spec-research-strategy.md`
  L1/L3 path lists, and a future `infra-spec-zone-classification-ledger.md`.

### G2. CI workflow depends on the broken submodule [implementation-backed]
- Evidence: `.github/workflows/drift-check.yml` runs
  `working-directory: implementation/domainspec` → `pnpm run check:code-tags`,
  with `submodules: recursive` on checkout.
- In this worktree that directory is empty; CI's own drift gate is structurally
  coupled to a submodule that is not guaranteed populated.
- Concept candidate: **deploy-reality coupling** — a CI/promotion gate that
  silently no-ops or hard-fails when a state namespace (submodule) is absent.
  Infra-spec should require every gate to declare which state namespaces it
  presupposes and what happens when they are absent (fail-closed vs fail-open).
- Where it should have appeared: not mapped by L3 deploy auditor (its path list
  omits `.github/workflows/`).

### G3. `.gitignore`-vs-tracked-reality drift [implementation-backed]
- Evidence: root `.gitignore` lists `.arcanum/observability/**/*.jsonl` and
  `.arcanum/observability/reflection-state.json`, yet
  `git ls-files` shows `.arcanum/observability/reflection-state.json` AND
  `.arcanum/observability/by-sigil/experiment-harness.jsonl` are **tracked**.
  (Git ignore rules do not retroactively untrack files.)
- Concept candidate: **ignore-intent vs tracked-reality** drift — a config
  boundary gap where the declared "this is local/generated state" boundary is
  contradicted by what is actually committed. Infra-spec state-namespace axis
  must reconcile declared namespace (gitignore) against actual namespace (index).
- Where it should have appeared: L5 observability/residue analyst; not flagged
  because L5 reads observability *content*, not tracking status.

### G4. Committed runtime DB + write-ahead log at repo root [implementation-backed / residue]
- Evidence: `.data/knowledge-graph-projections.sqlite` (4K),
  `...sqlite-shm` (32K), `...sqlite-wal` (543K) are all **git-tracked**
  (`git ls-files .data/` returns them) and `.data/` is in NO `.gitignore`.
- A 543KB WAL file in version control is uncommitted-transaction residue: it
  represents an open/unflushed SQLite transaction state captured in git.
- Concept: **runtime-state residue** — generated mutable state (SQLite + WAL/SHM)
  living in the source namespace with no owner, no retention policy, and no
  flush/checkpoint discipline. This is the cleanest "residue after deployment"
  artifact in the repo.
- Where it should have appeared: state-namespace and data-lifecycle axes
  (strategy L4 candidate axes + "Candidate Concepts To Test → State namespace").

### G5. No rollback / migration / disaster-recovery section in infra constitution [absence]
- Evidence: `projects/body-war/domainspec/templates/infra-architecture.md` section
  headers are: Preset, Stack, Environments, Secrets, Infrastructure Layout,
  Networking, Monitoring Stack, CI/CD Pipeline, Scaling Roadmap, Conventions.
  Grep for `rollback|revert|migrat|backup|recover|disaster` in the template body
  returns ZERO hits. "Deploy Flow" and forward-only "scaling checklists" exist;
  there is no reverse path.
- Concept: infra-spec must encode a **reversal/rollback obligation** as a peer of
  deploy flow. The current constitution is forward-only — it can describe how to
  reach a topology but not how to retreat from a bad one.
- Where it should have appeared: infra-architecture template + L4 schema axes
  (no "rollback" / "migration" / "recovery" axis in the strategy's candidate list).

### G6. Burn-rate / error-budget *enforcement* absent (budget is only defined) [absence + partial-reject]
- Evidence: `slos.md` DOES define Error Budget
  (`budget_minutes = (1 - slo_target) × 30 × 24 × 60`, line 49) and Alert Routing.
- BUT grep for `burn.rate` across templates, `domainspec-infra-deploy`, and
  `domainspec-otel-verify` returns ZERO. Alerts are single-threshold "for: 5m"
  rules (`<alert-template>` in infra-deploy SKILL.md), not multi-window
  burn-rate alerts, and no gate consumes the error budget.
- Concept: error budget exists as a *number* but is never an *operational
  control* (no burn-rate alerting, no budget-gated promotion). Infra-spec should
  separate "error budget declared" from "error budget enforced" as distinct
  operational-proof-status levels.
- Where it should appear: `slos.md` Error Budget section + `infra-deploy`
  alert-template.

### G7. Templates exist but no project has *instantiated* infra [absence — arch-vs-reality]
- Evidence: `find projects -name INFRA-ARCHITECTURE.md` → empty;
  `find projects -type d -name infra` → empty; repo-wide
  `find . -iname Dockerfile* -o -iname docker-compose* -o -iname Pulumi* -o
  -iname *.tf -o -iname Caddyfile*` (excluding `.git`) → ZERO files.
- The `domainspec-infra-deploy` skill's declared targets
  (`infra/prometheus.yml`, `infra/docker-compose.prod.yml`, `infra/Caddyfile`,
  `infra/index.ts` Pulumi, `.github/workflows/ci.yml`, `deploy.yml`) **do not
  exist anywhere in the checked-out repo**. `.github/workflows/` contains only
  `drift-check.yml`.
- Concept: the entire infra capability is **specified and generative but never
  realized** — pure schema with zero deployed instances. This is the strategy's
  "runtime instance" candidate inverted: the spec side is rich, the instance side
  is null. Infra-spec must be honest that "specified" ≠ "deployed" and must carry
  an instance-coverage metric.
- Where it should have appeared: L3 runtime/deployment auditor (its known-paths
  list assumes `infra/` artifacts exist).

### G8. Strategy's L3 path inventory omits the real infra skill surface [implementation-backed — strategy gap]
- Evidence: the actual infra surface lives at
  `.github/skills/domainspec-infra-architecture/`,
  `.github/skills/domainspec-infra-deploy/`,
  `.github/skills/domainspec-instrument-otel/`,
  `.github/skills/domainspec-otel-verify/`, and
  `.github/agents/domainspec-infra-architect.agent.md`.
  The strategy's L3 "Known starting paths" lists none of these
  `.github/skills/domainspec-infra-*` surfaces; it only points at
  `projects/*/domainspec/templates/infra-architecture.md`.
- Concept: the most authoritative, behavior-defining infra documents are the
  SKILL/agent specs, not the project templates. A research route that misses them
  will conclude infra is "just templates" and undercount maturity.
- Where it should have appeared: strategy L3 known-paths.

### G9. Idempotency / backpressure / dead-letter absent from infra surface [absence]
- Evidence: grep `idempoten|backpressure|dead.?letter|retry` across
  `projects/` and `domainspec-infra-deploy` hits only `projects/sonar-loop/docs/`
  (domain workflow docs), never the infra/deploy/SLO surface.
- Concept: queue/backpressure/idempotency are a **boundary-object class** with no
  infra rules. The infra constitution models HTTP services + Prometheus metrics
  but has no vocabulary for async queues, retries, or exactly-once boundaries.
- Where it should have appeared: L4 candidate axes (`event/queue` axis exists in
  the list but has no backing template evidence — axis is aspirational).

### G10. OTel→Prometheus naming map is an unowned coupling contract [candidate]
- Evidence: `domainspec-infra-deploy` SKILL.md `<prometheus-naming>` table hard-codes
  12 OTel-instrument → Prometheus-metric name mappings (e.g.
  `operation.invocation → operation_invocation_total`). `domainspec-otel-verify`
  separately enumerates O-rules (O6 calculation.drift, O15 reconciliation.mismatch).
- These two surfaces must agree on metric names but there is no shared schema
  binding them; drift between the verifier's O-rule names and the deployer's
  Prometheus map is undetectable.
- Concept: infra-spec should treat the **instrument-name contract** as a single
  validated schema consumed by both verify and deploy, not duplicated prose tables.
- Where it should have appeared: L4 schema governor + L5 observability.

---

## B. Rejected Candidates (with why)

- **"No SLO/SLA language exists"** — REJECTED. `slos.md` defines Global + Per-Feature
  SLOs, windows, alert thresholds, severities, and an error-budget formula. The
  gap is enforcement (see G6), not existence.
- **"No secrets/config boundary"** — REJECTED. infra-architecture template has a
  dedicated `## Secrets` section (3 manual GitHub secrets; app secrets generated
  by Pulumi, never committed; `.env.example` documents required secrets) and a
  `Do NOT store secrets in git` convention. Boundary is documented (residual
  question: it's prose, not validated — see open questions).
- **"No observability"** — REJECTED. Rich surface: `domainspec-instrument-otel`,
  `domainspec-otel-verify`, `.arcanum/observability/`, OTel→Prometheus map,
  alert templates, `slos.md` routing.
- **"No promotion gates"** — REJECTED. infra-deploy references "promotion gates"
  for Split-VPS+ and branch→environment mapping exists. (Residual: gates are named
  but their evidence/validation contract is unspecified.)
- **"arcanum/ is uninitialized"** — REJECTED for this lane. `arcanum/` is populated
  (`framework/runtime/`, `framework/observability/` present). Only the
  domainspec/poker-team/sandbox submodules are broken/empty.

---

## C. Residue Items (required: at least one)

- **R1 (primary residue):** `.data/knowledge-graph-projections.sqlite-wal` (543KB
  write-ahead log) committed to git = uncommitted-DB-transaction state frozen into
  source control. No owner, no checkpoint discipline, no retention policy.
- **R2:** `.arcanum/observability/reflection-state.json` + `by-sigil/*.jsonl`
  tracked despite being gitignore-declared as local/generated — orphaned tracked
  state that ignore rules can no longer reach.
- **R3:** empty `validation/poker-team/` and `validation/sigil-spell-sandbox/`
  directories = submodule-mount residue (mount points with no content), one of
  which (`sigil-spell-sandbox`) has no `.gitmodules` registration at all.
- **R4:** `domainspec-infra-deploy` declares generated targets
  (`infra/*`, `ci.yml`, `deploy.yml`) that exist nowhere = specification residue
  (instructions whose outputs were never realized or were lost).

---

## D. Open Questions

- OQ1: Is the empty `implementation/domainspec` a local-checkout artifact only, or
  is the recorded submodule commit itself unreachable? (Recorded HEAD `970dab5...`;
  `git submodule status` shows `+6f26de2...` — i.e. recorded ≠ status pointer ≠
  populated. Three-way mismatch needs an owner.)
- OQ2: Should `.data/*.sqlite*` be gitignored + checkpointed, or is committing the
  knowledge-graph projection intentional (reproducibility)? Owner decision needed.
- OQ3: Is `validation/sigil-spell-sandbox` an orphaned mount to delete, or a
  pending submodule to register in `.gitmodules`?
- OQ4: Do the infra skills' generated `infra/` artifacts live inside the
  `implementation/domainspec` submodule (hence invisible here)? If so, the whole
  infra surface is gated behind the broken submodule — escalates G1/G7 severity.

---

## E. Child-Dispatch Proposals

### CD-L7-1: Submodule & State-Namespace Ownership Audit
- parent_dispatch_id: `infra-spec-research-strategy-20260603`
- scope: Reconcile recorded vs status vs populated state for all three submodules;
  classify `.data/`, `.arcanum/observability/` tracked-vs-ignored; produce a
  state-namespace ownership table (source / generated / local / vendored / residue).
- owning lane: L7 (hands off to L1 zone cartographer)
- roles: gap-hunter (author), owner-boundary reviewer, skeptical reviewer
- inputs: `.gitmodules`, `git submodule status`, `git ls-files`, root + arcanum
  `.gitignore`, `.data/`, `.arcanum/observability/`
- expected artifacts: `ops/development/infra-spec-state-namespace-ownership-ledger.md`
- stop conditions: every namespace has exactly one owner + declared lifecycle, OR
  an unresolvable three-way commit mismatch is escalated.
- join policy: feeds L1 zone-classification ledger and L4 state-namespace axis.
- validation evidence: `git ls-files` + `git check-ignore` outputs per path.

### CD-L7-2: Reversal & Lifecycle Obligation Gap Brief
- parent_dispatch_id: `infra-spec-research-strategy-20260603`
- scope: Specify the missing rollback / migration / retention / backpressure /
  burn-rate obligations (G5, G6, G9) as candidate infra-spec axes with at least
  one counterexample fixture each (per strategy "counterexample discipline").
- owning lane: L7 (hands off to L4 schema governor)
- roles: gap-hunter (author), schema-governor reviewer, skeptical reviewer
- inputs: infra-architecture.md template, slos.md, domainspec-infra-deploy SKILL.md
- expected artifacts: `ops/development/infra-spec-reversal-lifecycle-gap-brief.md`
- stop conditions: each of rollback/migration/retention/idempotency/burn-rate has
  a defined obligation + one violation fixture, OR is explicitly deferred.
- join policy: feeds L4 schema-taxonomy ledger candidate axes.
- validation evidence: absence greps recorded here (G5, G6, G9 path citations).

---

## F. Finding Classification Summary

| ID  | Finding                                   | Class                    |
| --- | ----------------------------------------- | ------------------------ |
| G1  | Broken/unowned submodule state            | implementation-backed    |
| G2  | CI gate coupled to broken submodule       | implementation-backed    |
| G3  | gitignore vs tracked-reality drift        | implementation-backed    |
| G4  | Committed SQLite + WAL runtime state       | implementation-backed / residue |
| G5  | No rollback/migration/recovery in constitution | absence             |
| G6  | Error budget defined but not enforced     | absence + partial-reject |
| G7  | Templates exist, no instantiated infra    | absence (arch-vs-reality)|
| G8  | Strategy L3 omits real infra skill surface| implementation-backed (strategy gap) |
| G9  | No idempotency/backpressure/dead-letter   | absence                  |
| G10 | OTel→Prometheus name map unowned coupling | candidate                |

Counts: net-new candidates = 10; rejected = 5; residue items = 4;
child-dispatch proposals = 2; open questions = 4.
