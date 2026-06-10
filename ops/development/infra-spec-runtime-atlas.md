# Infra-Spec Runtime And Deployment Atlas

Lane: L3 — Runtime And Deployment Auditor
Parent dispatch: `infra-spec-research-strategy-20260603`
Date: 2026-06-08
Status: read-only research ledger (no infra-spec authority)
Scope: "what is the actual deploy/runtime evidence in the repo?"

Claim classification legend (per strategy Non-Negotiables):

- `implementation-backed` — a real, present, executable/config artifact exists
- `documented` — a doc/template/agent describes infra but no executable artifact is present
- `candidate` — vocabulary/axis worth testing for infra-spec
- `analogy` — borrowed from Lean/reflection/residue; must stay labeled
- `residue` — known gap, conflict, or deferred zone

Every row cites a path.

---

## Headline Findings

1. **The DomainSpec `infra/` layer is entirely aspirational.** Templates and
   agents describe a complete Pulumi + cloud-init + Caddy + Prometheus +
   Grafana + GitHub Actions VPS stack, but **zero** of the artifacts they
   reference exist anywhere in the repo (no `Dockerfile`, no
   `docker-compose*.yml`, no `*.tf`/`Pulumi.yaml`, no `Caddyfile`, no
   `prometheus.yml`, no `cloud-init.yaml`, no `infra/index.ts`, no
   `.github/workflows/deploy.yml` or `ci.yml` at any DomainSpec project).
   Classification: `documented`, not `implementation-backed`.
   Evidence: `find` for `Dockerfile`, `docker-compose*`, `*.tf`, `Pulumi*`,
   `Caddyfile`, `prometheus*`, `grafana*`, `cloud-init*` returned nothing in
   project/implementation scope (only `arcanum/benchmark/src/index.ts`, an
   unrelated TS entrypoint).

2. **The repo-root CI workflow is structurally broken right now.**
   `.github/workflows/drift-check.yml` runs `tools/check_github_drift.sh`,
   which hard-requires the `implementation/domainspec` and
   `validation/poker-team` submodules and `exit 2`s if either directory is
   unpopulated. Both submodules are currently EMPTY/broken pointers (see
   Deferred Zones). It also runs `pnpm run check:code-tags` inside
   `implementation/domainspec`, which cannot exist. Classification:
   `residue` (active operational breakage).
   Evidence: `.github/workflows/drift-check.yml:21-31`,
   `tools/check_github_drift.sh:6-12`, `git submodule status`.

3. **The only real, running runtime evidence lives in `projects/goldenquill`**
   (pinned-venv Python pipeline, Logfire observability, OpenClaw daemon,
   local Ollama/vLLM inference, Cedar policy gates) and in Arcanum's
   observability/runtime substrate (`.arcanum/observability/`,
   `arcanum/framework/runtime/`). `projects/body-war/app` is a tiny
   dependency-free local Python server with a real `.env.example`.
   Classification: `implementation-backed`.

4. **Two infra templates are byte-identical across projects** (body-war and
   whisky-doses), and both still carry placeholder `{project-name}` tokens —
   evidence the DomainSpec infra template is copied verbatim and never
   instantiated. Classification: `residue`/`documented`.
   Evidence: `diff` of the two `infra-architecture.md` returned identical;
   `setup.sh` still contains `{project-name}`, `{pulumi-project-name}`.

---

## Infra Artifact Atlas

| Artifact path | Kind | What it reveals |
| --- | --- | --- |
| `projects/body-war/domainspec/templates/infra-architecture.md` | runbook/topology (template) | The richest deploy/runtime vocabulary source in the repo. Four-preset model (Dev / Single-VPS / Split-VPS / HA), stack table (VPS/DNS/IaC/proxy/registry/DB/monitoring/logs/CI), environments table, secrets table (3 manual + Pulumi-generated), `infra/` layout, networking/port table, monitoring stack, CI/CD pipeline, scaling roadmap, conventions. `documented` only — none of the layout exists. |
| `projects/whisky-doses/domainspec/templates/infra-architecture.md` | runbook/topology (template) | Byte-identical to body-war's (diff clean). Confirms the template is copied per-project, never instantiated. `residue`. |
| `projects/body-war/domainspec/templates/setup.sh` | script (deploy) | Fully-written VPS provisioning script: Pulumi stack init/select, SSH ed25519 keygen, DO + Cloudflare token config, `pulumi up`, cloud-init wait, `scp` of `docker-compose.prod.yml`/`Caddyfile`/`prometheus.yml`/`alerts`/`grafana`, remote secret generation (`openssl rand`, caddy hash-password), deploy-user SSH setup. References many files that DO NOT exist. Still has `{project-name}` placeholders. `documented`. |
| `projects/whisky-doses/domainspec/templates/setup.sh` | script (deploy) | Same template family. `documented`. |
| `.github/agents/domainspec-infra-architect.agent.md` | runbook (agent spec) | Defines the agent that authors `docs/INFRA-ARCHITECTURE.md`, `docs/slos.md`, scaffolds `infra/`, Dockerfiles, Caddyfile, GH workflows, prometheus.yml, alert rules. Codifies defaults (DO, Cloudflare, Pulumi-TS, Caddy, ghcr.io, Prometheus+Grafana, GH Actions) and hard constraints (no DB ports public, no secrets in git, IaC-only changes, mandatory health checks, ports 80/443/22, non-root containers). Source of infra-spec obligation vocabulary. `documented`. |
| `.github/agents/domainspec-otel-instrumenter.agent.md` | runbook (agent spec) | OTel instrumentation agent — observability authoring surface. `documented`. |
| `.github/agents/domainspec-otel-verifier.agent.md` | runbook (agent spec) | OTel verification agent. `documented`. |
| `.github/skills/domainspec-infra-architecture/SKILL.md` | runbook (skill) | The constitution-author skill. Lists detection targets (compose, Dockerfile, infra/, Pulumi, *.tf, workflows, Caddyfile/nginx/traefik, prometheus.yml, grafana/) and outputs. `documented`. |
| `.github/skills/domainspec-infra-deploy/SKILL.md` | runbook (skill) | The deploy-artifact generator skill — "infra equivalent of sync-registry." Targets `infra/prometheus.yml`, `infra/alerts/*.rules.yml`, `infra/docker-compose.prod.yml`, `infra/Caddyfile`, `infra/index.ts`, `.github/workflows/ci.yml`+`deploy.yml`. Carries a planner-gate preflight (work-pack discipline). `documented`. |
| `.github/workflows/drift-check.yml` | CI | Repo-root CI. Checks out submodules recursive, runs `tools/check_github_drift.sh`, then `pnpm run check:code-tags` in `implementation/domainspec`. Currently broken (submodules empty). `implementation-backed` (exists/runs) but in a failing state — `residue`. |
| `tools/check_github_drift.sh` | script (governance CI) | Hard-requires `implementation/domainspec` + `validation/poker-team` populated; `exit 2` otherwise. Inventories `.github/agents/*.agent.md` across submodules + copilot agents to detect drift. Reveals the intended three-way agent topology (root / poker-team / domainspec / copilot). `implementation-backed`. |
| `.githooks/pre-commit` | hook | Prettier auto-format on staged md/json/yaml/css/html/js/ts via `npx --yes prettier`. Only repo-level git hook. `implementation-backed`. |
| `tools/terminal_guard.sh` | script (local wrapper) | Timeout/retry guard wrapping arbitrary commands; logs to `docs/signals/terminal-guard.jsonl`. A real local runtime wrapper + signal emitter. `implementation-backed`. |
| `tools/audit_codex_skill_surface.sh`, `classify_root_github_skills.sh`, `reconcile_delegation_tuning.sh`, `sync_mars_canonical_assets.sh`, `update_experiments_index.sh`, `update_project_experiments_index.sh`, `check_research_structure.sh`, `check_markdown_links.sh` | script (repo maintenance) | Governance/maintenance tooling, not deployment. Operate on skill/agent surfaces and docs. `implementation-backed`. |
| `arcanum/framework/runtime/README.md` (+ `adapters/`, `templates/`, `development/`) | runtime/topology | Arcanum "Durable Runtime": orchestrator → `RUNTIME-HANDOFF.md` → adapter → run folder (`RUN.json`, `HANDOFF.md`, `STATUS.json`, `events.jsonl`, `artifacts/`, `children/`, `adapter-state/`). Terminal statuses `passed/flagged/blocked/failed`; validation grades `contract/adapter-safety/execution`. Adapters: `local-skill`, `dry-run`, `codex-exec`, `codex-bypass`. Config at `.arcanum/runtime/config.json`. Strongest existing "runtime contract" vocabulary in the repo. `implementation-backed`. |
| `arcanum/framework/observability/` (`ARCHITECTURE-OVERVIEW.md`, `SIGIL-OBSERVABILITY-HOOK.md`, `scripts/*.sh`, `templates/`) | metrics/runtime | ~20 shell scripts: hook post-tool-use/stop/user-prompt-submit, start/attach/finish/checkpoint observed-run, observe-invocation, reflect-invocation-signals, compact/recover/rebuild observability store, reflect-hook-health. A real telemetry pipeline. `implementation-backed`. |
| `.arcanum/observability/config.json` | runtime-state | Live observability config: `storage_model: hybrid`, source-of-truth `signals/sigil-invocations.jsonl`, per-sigil + reflection + hook paths, reflection thresholds (meaningful_executions 5, generated_outputs 10, workflow_gaps 3/severe 1, hook_failures 3, hook_skips 5). `implementation-backed`. |
| `.arcanum/observability/signals/sigil-invocations.jsonl` (10 lines), `by-sigil/experiment-harness.jsonl` (5 lines) | runtime-state | Actual recorded telemetry signals — proof the observability runtime has executed. `implementation-backed`. |
| `.arcanum/observability/reflection-state.json`, `runs/`, `hooks/`, `reflections/` | runtime-state | Reflection counters + run/hook stores (mostly `.gitkeep`/`.gitignore` shells). `implementation-backed`. |
| `.arcanum/runtimes/github-copilot/{skills,sigils,spells}` | runtime-install surface | Installed Copilot runtime surface (generated). `implementation-backed`. |
| `.arcanum/necronomicon/{sessions,capability-updates}` | runtime-state | Knowledge-harness session state. `implementation-backed`. |
| `.data/knowledge-graph-projections.sqlite` (+ `-wal`, `-shm`) | runtime-state | Live SQLite projection DB with active WAL — a real local data-store boundary that no infra doc accounts for. `implementation-backed` + `residue` (unowned state). |
| `.planning/{STATE.md,config.json,REQUIREMENTS.md,PROJECT.md,ROADMAP.md}` | runtime-state | Planning/GSD harness state. `implementation-backed`. |
| `projects/body-war/app/server.py` + `static/` + `data/.gitkeep` | container/service (no container) | Dependency-free Python HTTP server (Strava OAuth pilot). Real runnable service; `data/` holds local JSON + tokens (gitignored). No Dockerfile. `implementation-backed`. |
| `projects/body-war/app/.env.example` | env | Real env contract: `STRAVA_CLIENT_ID/SECRET/REDIRECT_URI`, `BODY_WAR_PUBLIC_BASE_URL/HOST/PORT`, `BODY_WAR_SESSION_SECRET=change-me`. Loopback `127.0.0.1:5174`. The only `.env.example` in the repo. `implementation-backed`. |
| `projects/body-war/.codex/hooks/arcanum-{user-prompt-submit,post-tool-use,stop}.sh` | hook (agent runtime) | Per-project Codex agent hooks (same family as `arcanum/.codex/hooks/*`). `implementation-backed`. |
| `projects/goldenquill/.github/workflows/ci.yml` | CI | Real, working CI: matrix py3.11/3.12, installs weasyprint system libs, pinned `.venv`, spaCy model, AST-lint, pytest, wheel build + CLI import smoke. The most complete real pipeline in the repo. `implementation-backed`. |
| `projects/goldenquill/.github/workflows/signature_roundtrip.yml` | CI | Ed25519 signature roundtrip test workflow (matches GQ's signed-router/coefficient/register trust model). `implementation-backed`. |
| `projects/goldenquill/scripts/{run_tests.sh,run_lint.sh,memory_size_check.sh}` | script | Pinned-interpreter test/lint runners + memory budget check. `run_tests.sh` enforces py>=3.11 via `.venv`. `implementation-backed`. |
| `projects/goldenquill/skills/tilth-pipeline/run.sh` | script (pipeline runner) | Single-shot organism pass: Scout live-API → Tilth scoring → DB write-back; fail-open on Scout, one-client-slug per invocation (Law 3). `implementation-backed`. |
| `projects/goldenquill/docs/LOCAL_DEVELOPMENT.md` | runbook | Real cold-clone setup path: py3.14 operator pin vs 3.11/3.12 CI vs rejected 3.9 system python; ~5GB venv+model weights; Apple-Silicon/Linux/WSL2 only. `implementation-backed`. |
| `projects/goldenquill/CLAUDE.md` | runbook/topology | Substantial real runtime topology: Pydantic AI + Logfire (observability) + Ollama/vLLM local inference + Cedar/Logician deterministic gates + DSPy/GEPA; OpenClaw LaunchAgent daemon + dashboard `http://127.0.0.1:18789`; per-org isolation under `orgs/`; signed router/coefficient/register (Ed25519) trust; CycleReceipt/ReflectionPacket typed artifacts at cycle close. The richest *real* deploy/runtime + observability + residue model in the repo. `implementation-backed`. |
| `projects/goldenquill/tools/_probe_launcher.sh`, `tilth/tests/test_cache_org_isolation.sh`, `docs/post_hardening_issues_2026-05-17.sh` | script | Probe launcher, org-isolation cache test, hardening-issue script. `implementation-backed`. |
| `arcanum/.codex/hooks/arcanum-{user-prompt-submit,post-tool-use,stop}.sh` | hook (agent runtime) | Canonical Codex agent hooks the per-project ones derive from. `implementation-backed`. |
| `arcanum/tools/{bootstrap_arcanum.sh,install_arcanum.sh,validate-*.sh}` | script (installer) | Arcanum install/bootstrap + validators. `implementation-backed`. |
| `arcanum/.github/workflows/{claude-skills.yml,pages.yml}` | CI | Arcanum submodule's own CI (skills validation + pages). `implementation-backed` (submodule scope). |
| `.github/gsd-file-manifest.json`, `.github/copilot-instructions.md`, `.github/agents/gsd-*` | topology | GSD ("get shit done") agent fleet + manifest — a parallel agent runtime topology distinct from DomainSpec/Arcanum. `documented`/`implementation-backed`. |

---

## Topology Vocabulary Candidates

All `candidate` unless noted. Sourced from the infra template, the
infra-architect agent, the Arcanum durable runtime, and the goldenquill
real stack.

| Candidate term | Source path | Note |
| --- | --- | --- |
| `preset` (dev / single-vps / split-vps / ha) | infra-architecture.md:4,21-31 | Graduation tiers — strong axis for a "runtime profile" field. |
| `environment` (local / staging / production) + deploy trigger | infra-architecture.md:50-57 | env boundary + branch→env mapping (lines 229-235). |
| `stack layer` (VPS/DNS/IaC/proxy/registry/DB/monitoring/logs/CI) | infra-architecture.md:34-46 | Component/dependency vocabulary. |
| `secret` w/ source boundary (manual vs Pulumi-generated vs GH secrets) | infra-architecture.md:60-70 | Secrets/config boundary axis. |
| `networking` (internal port / exposed-via-proxy / firewall allow-list) | infra-architecture.md:92-107 | Boundary-object vocabulary. |
| `scrape target` / `O-rule` / SLO target / alert rule | infra-architecture.md:113-139 | observability-signal → target → alert chain. |
| `image naming` `{registry}/{project}/{service}:{git-sha}` | infra-architecture.md:222-227 | deployment-unit identity. |
| `service` (app/web/postgres/caddy/prometheus/grafana) | infra-architecture.md:237-247 | service/component graph. |
| runtime `run folder` (RUN/STATUS/HANDOFF/events.jsonl) | arcanum/framework/runtime/README.md:18-33 | runtime-instance + receipt vocabulary (strongest real one). |
| terminal status `passed/flagged/blocked/failed` | arcanum/framework/runtime/README.md:39-44 | operational proof-status candidate (maps to strategy's "operational proof status"). |
| validation grade `contract/adapter-safety/execution` | arcanum/framework/runtime/README.md:46-50 | promotion-gate candidate. |
| adapter (`local-skill/dry-run/codex-exec/codex-bypass`) | arcanum/framework/runtime/README.md:64-73 | runtime-profile / execution-boundary candidate. |
| signal / reflection-state / threshold | .arcanum/observability/config.json | observability + reflection-tower vocabulary. |
| deployment posture (frontier-eligible / split-context-hybrid / local-only-sovereign) | goldenquill/CLAUDE.md | real per-call routing posture — a runtime-profile + policy-boundary axis no generic infra doc has. |
| signed-asset trust (router-template / coefficient-registry / register, Ed25519) | goldenquill/CLAUDE.md, signature_roundtrip.yml | promotion-gate + supply-chain trust candidate. |
| typed cycle-close receipt (CycleReceipt / ReflectionPacket) | goldenquill/CLAUDE.md | "receipt" + "residue after deployment" candidate, already typed Pydantic. |
| state namespace (source / runtime / generated / local-private / evidence) | .arcanum/*, .data/*, .planning/* | matches strategy's "state namespace" concept. |

---

## Operational Risk List

1. **Broken root CI on every PR.** `drift-check.yml` → `check_github_drift.sh`
   `exit 2` when `implementation/domainspec`/`validation/poker-team` are empty
   (current state). `residue`. (`.github/workflows/drift-check.yml`,
   `tools/check_github_drift.sh:6-12`)
2. **Aspirational-vs-real deploy gap.** Every DomainSpec infra artifact
   (Pulumi/compose/Caddy/prometheus/grafana/cloud-init/workflows) is described
   but absent. Any infra-spec built on these docs would encode a topology the
   repo cannot demonstrate. `residue`. (infra-architecture.md, infra-deploy
   SKILL.md, infra-architect agent)
3. **Identical un-instantiated templates with live placeholders.** `setup.sh`
   would run with literal `{project-name}`/`{pulumi-project-name}` paths and
   provision real cloud resources if executed as-is. `residue`.
   (body-war/whisky-doses `setup.sh`)
4. **Unowned runtime state.** `.data/knowledge-graph-projections.sqlite`
   (+ active WAL) is live local state with no infra doc, no retention policy,
   no namespace classification. `residue`. (`.data/`)
5. **Secret-in-example default.** `BODY_WAR_SESSION_SECRET=change-me` ships a
   weak default; no rotation/validation guard. `documented` risk.
   (`projects/body-war/app/.env.example:7`)
6. **No SLO/error-budget reality.** SLOs/alerts are template-only and
   "auto-generated from observability.md" — but no `docs/features/*/
   observability.md` or `docs/slos.md` exists at any DomainSpec project to
   generate from. `residue`. (infra-architecture.md:115-139,
   infra-architect agent:36-37)
7. **Two parallel agent-runtime topologies** (DomainSpec/Arcanum vs GSD fleet
   under `.github/`) with no single owner map; drift check covers only the
   DomainSpec/poker-team/copilot axis, not GSD. `residue`.
   (`tools/check_github_drift.sh`, `.github/gsd-file-manifest.json`)

---

## Stale Or Conflicting Deployment Claims

1. **Conflict: "scaffolds infra/ + Dockerfiles + workflows" vs no such files.**
   The infra-architect agent (lines 24-29, 40-47) and infra-deploy SKILL claim
   to generate a full `infra/` tree and `.github/workflows/{ci,deploy}.yml`;
   none exist in any DomainSpec project. Classification: `documented` claim
   contradicted by absence. (agent + SKILL vs `find` results)
2. **Stale: drift-check assumes populated submodules.** CI + `check_github_drift.sh`
   assume `implementation/domainspec` and `validation/poker-team` are present;
   both are broken pointers. Classification: `residue`/stale.
3. **Conflict: body-war app reality vs body-war infra template.** The app is a
   loopback `127.0.0.1:5174` single-file Python server with no DB and no
   container; the project's own `infra-architecture.md` describes a
   multi-service Postgres+Caddy+Prometheus VPS stack. The template is generic
   boilerplate unrelated to the actual app. Classification: `documented` vs
   `implementation-backed` mismatch. (`projects/body-war/app/*` vs
   `projects/body-war/domainspec/templates/infra-architecture.md`)
4. **Stale placeholder example.** `infra-architecture.md:227` example
   `ghcr.io/poker-team/backend:a1b2c3d` references poker-team, but the template
   lives in body-war/whisky-doses and poker-team is an empty submodule.
   Classification: stale.

---

## Residue Items

- `RES-L3-1`: Root CI (`drift-check.yml`) is failing-by-construction until the
  two submodules are restored. Unblock = `git submodule update --init
  --recursive` against valid remotes, OR make `check_github_drift.sh` degrade
  gracefully when submodules are absent.
- `RES-L3-2`: Entire DomainSpec deploy stack is `documented`-only; no
  fixture/instance proves the topology. Infra-spec must NOT treat these docs as
  `implementation-backed`.
- `RES-L3-3`: `.data/knowledge-graph-projections.sqlite` is unowned, unclassified
  runtime state.
- `RES-L3-4`: No `docs/features/*/observability.md`, `docs/slos.md`, or
  `docs/INFRA-ARCHITECTURE.md` instance exists anywhere — the generation source
  the agent/SKILL depend on is absent.
- `RES-L3-5`: goldenquill (real runtime: Logfire, OpenClaw daemon, Ollama/vLLM,
  Cedar gates, signed assets, typed cycle receipts) was scanned at doc level
  only; its actual pipeline/config files were not exhaustively read — deferred
  to L6 cross-project archaeology.
- `RES-L3-6`: Arcanum submodule has its own CI + installer + runtime that were
  surveyed at README/listing depth only, not fully audited.

---

## Deferred Zones (explicit)

- **`implementation/domainspec/` — DEFERRED (broken submodule).** The strategy's
  top starting path (`implementation/domainspec/infra/`) is unreachable: the
  submodule is an empty/broken pointer (`git submodule status` shows
  `+6f26de2...` with the working tree containing only a `.git` file; the
  worktree subdir is empty). Its `infra/` could not be scrubbed.
  **Unblock action:** `git submodule update --init implementation/domainspec`
  (remote `https://github.com/vrondelli/domainspec.git`); then re-run L3 scoped
  to `implementation/domainspec/infra/`, `.github/workflows/`, and any
  `Dockerfile`/compose there. This is also what unblocks `RES-L3-1`.
- **`validation/poker-team/infra/` — DEFERRED (empty submodule).** Directory is
  empty (`ls` shows nothing). Pointer present in `.gitmodules` (remote
  `https://github.com/vrondelli/poker-team.git`) but `git submodule status`
  shows `-486f39a...` (uninitialized). The infra-architecture template's image
  example (`ghcr.io/poker-team/backend`) implies poker-team is the canonical
  infra exemplar — making this the highest-value deferred zone.
  **Unblock action:** `git submodule update --init validation/poker-team`; then
  scrub `validation/poker-team/infra/` for real Pulumi/compose/Caddy/prometheus
  instances (the one place the aspirational template may be realized).
- Note: `.gitmodules` also has no mapping for `validation/sigil-spell-sandbox`
  yet `git submodule status` references it — a third submodule-config residue.

---

## Child-Dispatch Proposals

### Proposal CD-L3-A: poker-team infra mini-atlas (gated)

- `parent_dispatch_id`: `infra-spec-research-strategy-20260603`
- scope: After `validation/poker-team` is initialized, scrub its `infra/` for
  the only potentially-real instantiation of the DomainSpec Pulumi+compose+Caddy
  +Prometheus stack; compare instance-vs-template to confirm or refute the
  aspirational-only finding (Headline #1).
- owning lane: L3 (joins L6 cross-project)
- roles: runtime-deploy-auditor, owner-boundary reviewer
- inputs: initialized `validation/poker-team` submodule; this atlas;
  `infra-architecture.md` template
- expected artifacts: `ops/development/infra-spec-poker-team-infra-mini-atlas.md`
- stop conditions: submodule still empty after init attempt → record blocked +
  return; or 5+ new dependent subquestions → escalate
- join policy: merge into L3 atlas + L6 catalog before interpretation tournament
- validation evidence: every claim path-cited; instance files diffed vs template

### Proposal CD-L3-B: real-runtime contract extraction from goldenquill + Arcanum durable runtime (gated)

- `parent_dispatch_id`: `infra-spec-research-strategy-20260603`
- scope: Extract a fixture-first runtime/receipt contract from the two systems
  that actually run — Arcanum durable runtime (run folder, status model,
  validation grades, adapters) and goldenquill (deployment posture, signed-asset
  trust, CycleReceipt/ReflectionPacket). These are the repo's only
  `implementation-backed` runtime contracts and should anchor infra-spec's
  "operational proof status" + "receipt" + "residue after deployment" axes.
- owning lane: L3 (feeds L4 schema, L5 observability)
- roles: runtime-deploy-auditor, schema governor (read-only)
- inputs: `arcanum/framework/runtime/`, `.arcanum/observability/`,
  `projects/goldenquill/CLAUDE.md` + pipeline config
- expected artifacts: `ops/development/infra-spec-runtime-contract-evidence.md`
- stop conditions: contradiction between Arcanum status model and goldenquill
  receipt model that cannot be resolved locally → escalate
- join policy: hand candidate axes to L4/L5; keep no schema authority here
- validation evidence: each extracted field cites a present, executable artifact

---

## Receipt

- role_id: L3-runtime-deploy-auditor
- ledger_path: ops/development/infra-spec-runtime-atlas.md
- artifacts_found: ~40 (see atlas table)
- path_citation_confirmed: yes
- no-block (L3 completed read-only scrub; two zones explicitly deferred with
  unblock actions)
