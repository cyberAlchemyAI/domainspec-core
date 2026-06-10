# Infra-Spec Zone Classification Ledger (Lane L1)

Date: 2026-06-08
Lane: L1 — Repository Zone Cartographer
Parent dispatch: `infra-spec-research-strategy-20260603`
Role id: L1-zone-cartographer
Status: read-only research; this ledger is the only write.

## Scope And Method

Question: where is infra knowledge already hiding, and what is each zone's owner/status?

Method: read-only `ls`/`find`/`grep`/`git submodule status`/`git ls-files` over `arcanum/`, `validation/`, `projects/`, `research/`, `docs/`, `ops/`, `tools/`, and root runtime/install surfaces. Nothing moved or deleted.

Class vocabulary follows the established precedent in `ops/ARCANUM-STATE-CLASSIFICATION.md` (canonical source / generated-local / runtime install surface split) extended with the L1 classes required by the strategy (`ops/development/infra-spec-research-strategy.md` line 51).

Scope-boundary discipline (per strategy lines 16-18): "infra" inside `arcanum/` means Arcanum **runtime/observability framework**, not infrastructure/deployment. Those are deliberately classified as `runtime install surface` and flagged out-of-scope, not folded into infra-spec.

## Submodule State (controls owner/status for three zones)

`git submodule status` evidence:

- `arcanum` — `10b52f3... (heads/main)`, no prefix: initialized and checked out. [source-backed: `.gitmodules`, `git submodule status`]
- `implementation/domainspec` — `+6f26de2... (heads/main)` prefix, but `find implementation/domainspec -type f` returns **1 file** (`implementation/domainspec/.git` only). Effectively EMPTY working tree / broken submodule pointer. Treated as **explicitly deferred** per dispatch instruction. [source-backed: `git submodule status`, `find`]
- `validation/poker-team` — `-486f39a...` prefix: **uninitialized**. Working tree empty. [source-backed: `git submodule status`, `ls` empty]

## Zone Classification Table

| Zone path | Class | Owner | Status | Infra-relevance note |
| --- | --- | --- | --- | --- |
| `arcanum/` (submodule) | canonical source (Arcanum framework) | Arcanum submodule owner (`cyberAlchemyAI/Arcanum`) | initialized, checked out | Runtime/observability framework only (`arcanum/framework/runtime/`, `arcanum/framework/observability/`). NOT deployment infra. Out-of-scope per strategy boundary. [source-backed: `.gitmodules`; `arcanum/framework/`] |
| `arcanum/framework/observability/` | canonical source | Arcanum owner | active | Sigil telemetry/hook architecture (`ARCHITECTURE-OVERVIEW.md`, `SIGIL-OBSERVABILITY-HOOK.md`). Analogy source for infra observability/receipt discipline, NOT deployment infra. [source-backed] |
| `arcanum/framework/runtime/` | canonical source | Arcanum owner | active | Runtime adapters/templates for skill execution, not service runtime. [source-backed] |
| `implementation/domainspec/` (submodule) | implementation source | DomainSpec owner (`vrondelli/domainspec`) | EMPTY / broken pointer — DEFERRED | Strategy named `implementation/domainspec/infra/` as a known infra path (line 125) but it is not materialized in this checkout. Primary implementation-infra evidence is currently UNREACHABLE here. [source-backed: `find` = 1 file] |
| `validation/poker-team/` (submodule) | validation sandbox | poker-team owner (`vrondelli/poker-team`) | uninitialized — DEFERRED | Strategy named `validation/poker-team/infra/` (line 126); not materialized. The `infra-architecture.md` example image name `ghcr.io/poker-team/backend:...` shows this is the canonical demo target. [source-backed: submodule `-` prefix; project template line 227] |
| `validation/sigil-spell-sandbox/` | validation sandbox | repo owner | empty | No infra evidence. [source-backed: `ls` empty] |
| `projects/body-war/` | project snapshot | repo owner | active, has real app | Contains `domainspec/templates/infra-architecture.md` (the richest infra template, see below) + `domainspec/templates/slos.md` + `app/.env.example` (only real env file in repo). [source-backed] |
| `projects/whisky-doses/` | project snapshot | repo owner | active | Holds an **identical** copy of `infra-architecture.md` + `slos.md` (template replication); plus `.codex/commands/domainspec-infra-deploy.md`, `domainspec-infra-architecture.md`, `.codex/agents/domainspec-infra-architect.agent.toml`, `infrastructure-guide.md`. Densest infra-command surface in `projects/`. [source-backed: `diff` identical; `find`] |
| `projects/goldenquill/` | project snapshot | repo owner | active, mature real system | `RUNTIME_MATURITY_MATRIX.md` (seven-state runtime promotion taxonomy), `router.yaml`, `pyproject.toml`, `pipeline/`, `apps/`, `PROJECT_STATUS.md`. Strongest evidence for operational-proof-status / promotion-gate concept. [source-backed] |
| `projects/sonar-loop/` | project snapshot | repo owner | active | `docs/features/`, `.arcanum/`, `.github/`. No deployment infra found. [source-backed] |
| `projects/equalizator/` | project snapshot | repo owner | docs-only | Only `docs/` + deep-research resource doc. No infra. [source-backed: `ls`] |
| `projects/pos-multilevel/` | project snapshot | repo owner | docs-only stub | `docs/` + small README. No infra. [source-backed] |
| `projects/ontologize/` | project snapshot | repo owner | active research project | Governance/tower docs (`TOWER.md`, `DAG-AND-METRICS.md`), own dispatch json. No deployment infra; relevant as reflection-tower analogy. [source-backed] |
| `projects/domainspec-language/` | project snapshot | repo owner | WIP (recent commits) | `research/`, `development/`, context pack. No deployment infra. [source-backed] |
| `research/projects/domainspec/` | research evidence | repo owner | active | `telemetry/` (`SIGNAL-SCHEMA.md`, empty `signals.jsonl`), `runbooks/`, `protocols/`, `PROJECT.yaml`. Schema/telemetry vocabulary source. [source-backed] |
| `research/projects/mars/`, `research/projects/meta-meta/` | research evidence | repo owner | active | Research workflow, not deployment infra. [source-backed] |
| `research/shared/standards/`, `research/shared/templates/` | research evidence (shared standards) | repo owner | active | Report templates (EVIDENCE/INTEGRITY/PIPELINE/TRACEABILITY). Receipt-shape analogy. [source-backed] |
| `research/registry/` | research evidence (index) | repo owner | active | `DEPENDENCY-GRAPH.md`, `PROJECT-INDEX.md`. [source-backed] |
| `docs/decisions/` | canonical source (governance) | repo owner | active | `install-profile-contract.md`, `native-runtime-skill-surface.md` — runtime-surface program, scope-adjacent NOT infra-spec. [source-backed] |
| `docs/signals/` | generated-local (evidence ledgers) | repo owner | active, large | `delegation-tuning.jsonl` (103K), `terminal-guard.jsonl` (662K). Generated signal ledgers; receipt/observability analogy only. [source-backed] |
| `docs/shared/`, `docs/glossary.md`, `docs/registry.md` | canonical source | repo owner | active | Governance baseline + registry. [source-backed] |
| `ops/` (top-level *.md) | canonical source (governance/policy) | repo owner | active | Runtime-surface convergence program (`SKILLS-FIRST-RUNTIME-POLICY.md`, `SURFACE-OWNER-BOUNDARIES.md`, `RUNTIME-SURFACE-*`). Strategy line 18: SEPARATE track; do not import. [source-backed] |
| `ops/development/` | canonical source (this research zone) | repo owner | active | Holds infra-spec strategy + dispatch + refinement-runs + this ledger. The ONLY writable surface for this route (strategy line 43). [source-backed] |
| `tools/` | canonical source (scripts) | repo owner | active | Guard/drift/sync shell + python (`check_github_drift.sh`, `terminal_guard.sh`, `sync_mars_canonical_assets.sh`). Repo-maintenance tooling, not deployment infra. [source-backed] |
| `.arcanum/` | runtime install surface + generated-local | repo owner (config) / generated (run state) | mixed (see `ops/ARCANUM-STATE-CLASSIFICATION.md`) | `observability/` config durable; `runs/`/`hooks/`/reflection-state generated-local (gitignored). `runtimes/github-copilot/` generated package cache. Arcanum-runtime, out-of-scope. [source-backed] |
| `.github/skills/` | runtime install surface (generated native skill packages) | repo owner (generated by arcanum-bootstrap) | active, 146 entries | Installed Arcanum/DomainSpec/GSD skill packages. Generated, not canonical source. [source-backed: `ls | wc -l` = 146] |
| `.github/agents/` | runtime install surface (agent definitions) | repo owner | active | **Holds `domainspec-infra-architect.agent.md` — the single richest infra-knowledge artifact in the repo** (presets, IaC, SLOs, prometheus auto-gen, secrets, CI/CD). Also `domainspec-otel-instrumenter`/`-verifier` (observability→infra contract chain). [source-backed] |
| `.github/workflows/` | runtime install surface (CI) | repo owner | active, minimal | Only `drift-check.yml` (613B). No deploy/build CI in this repo. [source-backed] |
| `.github/get-shit-done/`, `gsd-*` | runtime install surface | repo owner | active | GSD harness; not infra. [source-backed] |
| `.githooks/pre-commit` | runtime install surface (local hook) | repo owner | active | Repo git hook, not deployment. [source-backed] |
| `.codex` (root) | runtime install surface | n/a | ABSENT at root | No root `.codex/`; codex command surfaces live per-project (e.g. `projects/whisky-doses/.codex/`). [source-backed: `ls` → "NO ROOT .codex"] |
| `.claude/` | runtime install surface | repo owner | active | Skills/agents/worktrees harness (this worktree lives here). [source-backed] |
| `.planning/` | generated-local (planning state) | repo owner | active | `phases/`, `STATE.md`, `config.json`. Planning harness state. [source-backed] |
| `.data/` | generated-local (DB state) | repo owner | active | `knowledge-graph-projections.sqlite` + `-wal`/`-shm`. Generated knowledge-graph DB; local state. [source-backed] |
| `cyberAlchemy/` | research evidence (method corpus) | cyberAlchemy owner | active | `agentic-system-architecture.md`, ontology corpus. Method/analogy source, not deployment infra. [source-backed] |
| `sigils-library/` | canonical source (sigil library) | repo/Arcanum owner | active | `arcana/`, `formulae/`, `transmutations/`. Sigil packaging, not infra. [source-backed] |
| `vscode-workspaces/` | generated-local (editor config) | repo owner | active | `.code-workspace` files per zone. Not infra. [source-backed] |
| `implementation/mars/` | implementation source | mars owner | active (NOT a submodule, real files) | `templates/` (research schemas incl. `telemetry-signal-schema-template.md`, `schema-*-template.json`), `copilot/`, `definitions/`. Schema-template analogy for L4; not deployment infra. [source-backed] |

Zones classified: 38 rows above (33 distinct zone paths + sub-zone breakdowns).

## Owner / Status Map

- Arcanum submodule owner: `arcanum/` (canonical framework) — initialized, out-of-scope-as-deployment.
- DomainSpec submodule owner: `implementation/domainspec/` — EMPTY/broken, deferred.
- poker-team submodule owner: `validation/poker-team/` — uninitialized, deferred.
- Repo owner (this repo): everything else — `projects/`, `research/`, `docs/`, `ops/`, `tools/`, root runtime surfaces, `cyberAlchemy/`, `sigils-library/`, `implementation/mars/`.

## Generated-vs-Source-vs-Runtime Split

- Canonical source: `arcanum/framework/*`, `docs/decisions`, `docs/shared`, `ops/*.md`, `ops/development`, `tools/`, `sigils-library/`.
- Implementation source: `implementation/mars/` (live), `implementation/domainspec/` (deferred-empty).
- Validation sandbox: `validation/poker-team/` (deferred), `validation/sigil-spell-sandbox/` (empty).
- Project snapshot: all `projects/*`.
- Research evidence: `research/*`, `cyberAlchemy/`.
- Generated-local: `.arcanum/observability/runs|hooks`, `.arcanum/runtimes/github-copilot`, `docs/signals/*.jsonl`, `.planning/`, `.data/*.sqlite*`, `vscode-workspaces/`.
- Runtime install surface: `.github/skills` (146 generated packages), `.github/agents`, `.github/workflows`, `.githooks`, `.claude`, `.arcanum` (config tier).

## Where Infra Knowledge Is Actually Hiding (ranked)

1. `.github/agents/domainspec-infra-architect.agent.md` — full infra contract vocabulary: presets (Dev/Single-VPS/Split-VPS/HA), IaC (Pulumi), Caddy, Prometheus/Grafana, SLOs, secrets, firewall, CI/CD, prometheus-from-observability auto-gen. [source-backed]
2. `projects/body-war/domainspec/templates/infra-architecture.md` (= `projects/whisky-doses/...`, identical) — the "Infrastructure Architecture Constitution" template: Preset / Stack / Environments / Secrets / Layout / Networking / Monitoring / CI/CD / Scaling Roadmap / Conventions. Closest existing thing to an infra-spec record shape. [source-backed]
3. `projects/goldenquill/RUNTIME_MATURITY_MATRIX.md` — seven-state runtime promotion taxonomy (dormant/historical → schema-scaffold → spec-locked → asset-signed → gate-live → runtime-live) with "promotion requires dated evidence" rule. Real-system precedent for operational-proof-status. [source-backed]
4. `.github/agents/domainspec-otel-instrumenter.agent.md` + `-verifier` — the observability→infra contract chain (`OBSERVABILITY.md` derivation rules → `observability.md` per feature → `instruments.ts` → telemetry infrastructure). [source-backed]
5. `projects/body-war/domainspec/templates/slos.md` (= whisky-doses) — SLO template linked from infra-architect. [source-backed]
6. `research/projects/domainspec/telemetry/SIGNAL-SCHEMA.md` + `implementation/mars/templates/telemetry-signal-schema-template.md` — signal/telemetry schema vocabulary. [source-backed]

## Classified Claims

- `domainspec-infra-architect.agent.md` defines preset/IaC/SLO/monitoring contract — source-backed.
- The infra-architecture template is the closest existing infra-spec record shape — source-backed (analogy for "infra-spec record" is candidate).
- goldenquill maturity matrix = operational-proof-status precedent — implementation-backed (real project) / analogy when transferred to infra-spec.
- The two project infra templates are byte-identical — source-backed (`diff` = identical).
- `implementation/domainspec/infra/` and `validation/poker-team/infra/` (strategy lines 125-126) are UNREACHABLE in this checkout — source-backed negative result; the strategy's known-paths are stale relative to current submodule state — **contradiction** between strategy line 125-126 and checkout state.
- No Dockerfile/compose/Pulumi/Caddy/Prometheus/Grafana FILES exist anywhere in the parent checkout — only templates/docs describe them — source-backed (negative). The repo holds infra *intent*, not infra *instances*. This is itself the central infra-residue finding for L3.
- arcanum/ "infra" hits are runtime-framework, not deployment — source-backed; confirms strategy scope boundary (line 18).

## Deletion / Stale-State Candidates (RESEARCH FINDINGS ONLY — not actions)

- `validation/poker-team` uninitialized pointer (`-486f39a`) — stale relative to its role as the canonical demo infra target (named in template image `ghcr.io/poker-team/backend`). Candidate: needs init to recover poker-team infra evidence, OR strategy known-paths need updating. [candidate / stale]
- `implementation/domainspec` materializes as `.git` only despite `+` (committed-differs) pointer — broken/empty working tree. Candidate: the richest implementation-infra source is currently inaccessible; do NOT treat absence as "no infra exists." [candidate / stale]
- Identical `infra-architecture.md` + `slos.md` in body-war and whisky-doses — replication-without-single-source. Candidate: a shared `research/shared/templates/` or DomainSpec-canonical home would prevent drift. [candidate]
- `research/projects/domainspec/telemetry/signals.jsonl` is 0 bytes — empty signal ledger. [stale/empty, evidence-of-absence]
- `docs/signals/terminal-guard.jsonl` (662K) and `delegation-tuning.jsonl` (103K) are large generated ledgers tracked in `docs/` — generated-local churn living in a source zone. [candidate, per `ops/ARCANUM-STATE-CLASSIFICATION.md` split policy]

NOTE: All above are findings, not recommended actions. No file was moved or deleted.

## Residue (negative results + leftovers)

- Residue item 1 (evidence-of-absence): The two named "known starting paths" for infra (`implementation/domainspec/infra/`, `validation/poker-team/infra/`) returned NOTHING because both submodules are unmaterialized here. Infra-spec research in this checkout must rely on the *project snapshots* (body-war/whisky-doses templates, goldenquill) and the *agent definitions* as proxies for the deferred submodule infra.
- Residue item 2: No real deployment artifact (Dockerfile/compose/Pulumi/Caddyfile/prometheus.yml/grafana) exists in the parent checkout — every such filename appears only inside templates/docs/agent specs. The gap between "infra described" and "infra instantiated" is unaccounted residue and should seed L3 (runtime auditor) and L7 (gap hunter).
- Residue item 3: `arcanum/framework/observability/` is a fully-built telemetry framework but for SIGIL runs, not service runtime — it is an analogy reservoir that risks being mis-imported as deployment observability. Labeled analogy, demote on transfer.

## Child Dispatch Proposals

Two owner-boundary crossings warrant child dispatches (parent_dispatch_id=infra-spec-research-strategy-20260603). Execution stays behind the strategy's approval gate (Non-Negotiable line 42).

### Child 1 — Submodule Infra Recovery Probe
- parent_dispatch_id: `infra-spec-research-strategy-20260603`
- owning lane: L1 (hands off to L3/L6)
- scope: initialize/inspect `implementation/domainspec` and `validation/poker-team` submodules read-only to recover their `infra/` evidence that the strategy's known-paths assume but that is absent in this checkout.
- roles: submodule-recovery reader (read-only), owner-boundary reviewer (DomainSpec + poker-team owners).
- inputs: `.gitmodules`, submodule URLs, `git submodule status`.
- expected artifacts: appended evidence rows to this ledger + `ops/development/infra-spec-runtime-atlas.md` (L3 surface).
- stop conditions: submodule unreachable/auth-blocked, OR owner declines init.
- join policy: results merge into L1 ledger + L3 atlas; do NOT promote recovered infra as authority without owner review.
- validation evidence: `git submodule status` before/after; file inventory.

### Child 2 — DomainSpec Infra-Constitution Source-Of-Truth Audit
- parent_dispatch_id: `infra-spec-research-strategy-20260603`
- owning lane: L1 (hands off to L4 schema governor)
- scope: trace the identical `infra-architecture.md`/`slos.md` templates and the `domainspec-infra-architect`/`otel-*` agents to determine their canonical home and whether the infra contract is DomainSpec-owned source vs replicated project snapshot.
- roles: schema/source auditor, owner-boundary reviewer (DomainSpec owner).
- inputs: `projects/body-war/domainspec/templates/*`, `projects/whisky-doses/domainspec/templates/*`, `.github/agents/domainspec-infra-architect.agent.md`, `.github/agents/domainspec-otel-*.agent.md`.
- expected artifacts: source-of-truth map feeding `ops/development/infra-spec-schema-taxonomy-ledger.md` (L4).
- stop conditions: canonical home is inside deferred `implementation/domainspec` (then blocks on Child 1).
- join policy: feed L4; flag drift but propose no edits to project snapshots.
- validation evidence: `diff` results, agent-spec citations.

## Return Receipt

- role_id: L1-zone-cartographer
- ledger_path: ops/development/infra-spec-zone-classification-ledger.md
- zones_classified: 38 (33 distinct zone paths + sub-zone breakdowns)
- path_citation_confirmed: yes
- blocked_fields_or_no_block: no-block (two zones explicitly deferred per dispatch: empty `implementation/domainspec`, uninitialized `validation/poker-team`)
