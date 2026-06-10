# Infra-Spec Cross-Project Pattern Catalog (Lane L6)

Role: L6 — Project Comparative Archaeologist
Parent dispatch: `infra-spec-research-strategy-20260603`
Date: 2026-06-08
Status: read-only research findings; NOT infra-spec authority
Classification legend: `[impl]` implementation-backed · `[doc]` documented · `[analogy]` analogy · `[candidate]` candidate · `[residue]` residue

## Question

What do concrete projects teach that generic infra theory misses?

## Projects Compared

| Project | Path | Infra maturity | Note |
| --- | --- | --- | --- |
| poker-team | `validation/poker-team` | — | EMPTY (submodule not populated). DEFERRED. Referenced indirectly: the `infra-architecture.md` template's image-naming example is `ghcr.io/poker-team/backend:a1b2c3d` (`projects/body-war/domainspec/templates/infra-architecture.md:227`), so poker-team is the apparent template origin. |
| whisky-doses | `projects/whisky-doses` | template + agent surface | Carries the full DomainSpec template bundle AND live infra skills/agent. |
| body-war | `projects/body-war` | template + real running app | Only project with an actual deployable app (`app/server.py`) and a real `.env.example`. |
| sonar-loop | `projects/sonar-loop` | spec/docs-only | Runtime-fallback governance is a documented spec concept, no deploy artifacts. |
| goldenquill | `projects/goldenquill` | production-grade operational doc set | Richest operational evidence in repo: deployment runbook, runtime maturity matrix, per-call posture, signed per-deployment router. |
| equalizator | `projects/equalizator` | early DomainSpec baseline | No infra artifacts; feature `domain/operations/interfaces/mappings` docs only. |
| pos-multilevel | `projects/pos-multilevel` | early DomainSpec baseline | No infra artifacts; baseline `docs/` only. |
| research/projects/domainspec | `research/projects/domainspec` | research evidence program | Evidence/claims/telemetry program, not a deployable system. `telemetry/signals.jsonl` is 0B. |
| implementation/domainspec | `implementation/domainspec` | — | EMPTY broken submodule (`.git` pointer only). DEFERRED per strategy. |

Count: 9 targeted, 7 populated and inspected, 2 empty/deferred (poker-team, implementation/domainspec).

A spectrum is visible: early-baseline projects (equalizator, pos-multilevel) have **zero** infra; mid projects carry the **template bundle** (whisky-doses, body-war); one project (goldenquill) has hand-built **production operational doctrine** that the templates do not yet capture. The gap between the template bundle and goldenquill's reality is the single most valuable L6 finding.

---

## Cross-Project Pattern Catalog

| Pattern | Projects showing it (paths) | Infra-spec implication | Class |
| --- | --- | --- | --- |
| **Graduated preset ladder (Dev → Single-VPS → Split-VPS → HA)** | `projects/body-war/domainspec/templates/infra-architecture.md:5,25-31,185-216`; `projects/whisky-doses/.agents/skills/domainspec-infra-architecture/SKILL.md:41-110` | Infra-spec needs a `preset`/profile axis where each profile is a *complete opinionated stack*, plus non-destructive graduation triggers (when→preset→what-changes). This is the "runtime profile" candidate concept, evidence-backed. | [impl] |
| **Infra artifacts GENERATED from domain specs (drift-sync), not authored** | `projects/whisky-doses/.agents/skills/domainspec-infra-deploy/SKILL.md:9-69,219-249`; `projects/body-war/domainspec/templates/infra-architecture.md:115-139`; `projects/body-war/domainspec/templates/slos.md:60-72` | The strongest cross-project lesson: `prometheus.yml`, `alerts/*.rules.yml`, `Caddyfile`, `docker-compose.prod.yml` are *derived* from `observability.md` + `slos.md` + `INFRA-ARCHITECTURE.md`. Infra-spec should model a **source→derived** relation with a sync/drift operation, mirroring `domainspec-sync-registry`. Confirms "evidence substrate / schema↔instance bridge" interpretations. | [impl] |
| **Observability→infra mapping table (OTel instrument → Prometheus metric)** | `projects/whisky-doses/.agents/skills/domainspec-infra-deploy/SKILL.md:72-91` | Infra-spec must carry a canonical instrument-name → metric-name mapping so alert/scrape generation is deterministic. Candidate field group: observability signal vocabulary. | [impl] |
| **SLO → error-budget → alert-routing chain** | `projects/body-war/domainspec/templates/slos.md:14-72`; `projects/whisky-doses/.agents/skills/domainspec-infra-deploy/SKILL.md:93-111` | Infra-spec should encode SLO targets, windows, alert thresholds, severity (P0–P3), error-budget formula, and alert routing per feature, each linked back to an O-rule. This is the SLO/SLA/error-budget vocabulary L7 expects; here it exists concretely. | [impl] |
| **Three-secret manual boundary + IaC-generated app secrets** | `projects/body-war/domainspec/templates/infra-architecture.md:60-70,249-256`; `projects/body-war/app/.env.example:1-8` | Two distinct secret classes: (a) small set of manual provisioning tokens in CI secrets; (b) app secrets generated by Pulumi and never committed. body-war's real `.env.example` shows the dev-time class (Strava creds, session secret `change-me`). Infra-spec needs a **secret-class boundary object** (manual-provisioning vs generated-runtime vs dev-local). | [impl]+[doc] |
| **Explicit networking/port + exposure table with firewall default-deny** | `projects/body-war/domainspec/templates/infra-architecture.md:92-108` | Infra-spec topology should record per-service internal port, exposure (via-proxy / internal-only), public URL, and firewall allow-list with default-block. "DB never exposed" is a repeated hard constraint. | [doc] |
| **Branch→environment deploy mapping** | `projects/body-war/domainspec/templates/infra-architecture.md:51-57,229-236` | Environment axis ties to git branch + deploy trigger. Infra-spec environment objects need a deploy-trigger field. | [doc] |
| **"Do NOT" operational guardrails (no SSH mutations, no secrets in git, no port exposure, no skipping health checks)** | `projects/body-war/domainspec/templates/infra-architecture.md:249-256`; `projects/whisky-doses/.agents/skills/domainspec-infra-architecture/SKILL.md:261-274` | These are *operational obligations/anti-patterns*, distinct from topology. Supports the strategy's "topology vs obligation split" candidate: infra-spec should carry an obligation/constraint list separate from the component graph. | [doc] |
| **Mandatory health check in deploy pipeline** | `projects/body-war/domainspec/templates/infra-architecture.md:163-164,255`; `projects/whisky-doses/.agents/skills/domainspec-infra-architecture/SKILL.md:189,272` | Deploy is not "done" until a runtime probe returns 200. Infra-spec promotion gate "deployed→observed" needs a health/probe receipt. | [doc] |
| **Idempotent automated provisioning script (`setup.sh`)** | `projects/body-war/domainspec/templates/setup.sh:1-70`; `projects/whisky-doses/.agents/skills/domainspec-infra-architecture/SKILL.md:194-199` | Reusable template: preflight tool checks, SSH keygen, Pulumi stack init/config/up, cloud-init wait, file copy, secret generation, GitHub-secrets summary. Infra-spec should reference a provisioning-script obligation, not just declarative IaC. | [impl] |
| **Agent runner as governed infra surface (sandboxed runtime, cost signals)** | `projects/body-war/domainspec/templates/agent-runner.md:1-105`; `projects/whisky-doses/.agents/skills/domainspec-infra-architecture/SKILL.md:79-91` | A self-hosted CI runner that executes LLM agents is itself an infra boundary object: sandboxed container with NO production secrets, tool deny-list, path allow-list, validation gate, human-review-required, concurrency=1, and emits `agent-cost` signals with threshold TH10. Net-new infra concept generic theory misses: **the agent runtime is a first-class deployable with its own secret/policy boundary**. | [impl] |
| **Runtime maturity taxonomy with promotion-by-dated-evidence** | `projects/goldenquill/RUNTIME_MATURITY_MATRIX.md` (whole file; rules at tail "Operating rules") | Seven monotone states: `historical`/`dormant` (off-axis) → `schema-scaffold` → `spec-locked` → `asset-signed` → `gate-live` → `runtime-live`. One-label-per-system-per-doc; promotion requires dated CI/test proof + lock_history row for governance-bound artifacts. This is the **operational proof status** candidate concept fully realized in a real project, and it directly inherits the Lean schema/instance/proof-status discipline (L2). Strongest single transferable artifact. | [impl] |
| **Deployment posture as a per-call runtime variable (fail-closed, signed)** | `projects/goldenquill/pipeline/orchestrator/deployment_posture.py:1-60`; routing gates `F-CLASS-*` in `RUNTIME_MATURITY_MATRIX.md` | "Posture" (local-only vs cloud) is read per-call from a process-shared atomic container, loaded from a signed register, and posture changes mid-cycle are fail-closed. Net-new: **runtime posture is itself a governed, signed, fail-closed state**, not a static env var. Generic infra theory treats environment as static config; here it is a live, attested, change-gated variable. | [impl] |
| **Per-deployment runtime config DERIVED from a signed template + per-org register** | `projects/goldenquill/router.yaml:1-20` (header doctrine) | The workspace `router.yaml` is simultaneously dev config AND the per-deployment template; each customer deployment derives its own config from (template + signed classification register + signed router-template release). Infra-spec lesson: a deployment is a **derivation** of (signed source template × per-tenant signed inputs), giving a multi-tenant derivation model. | [impl] |
| **Step-with-observable deployment runbook (operator vs automated split)** | `projects/goldenquill/docs/v0_1_beta_deployment_runbook.md:1-40` | Every runbook step has a named **observable**; if absent, operator stops and surfaces the gap. Explicit "operator action" vs "automated" labeling. Infra-spec runbook obligation: each deploy step carries a verifiable observable + actor classification. | [doc] |
| **Provider-boundary outbound enforcement + AST-lint discipline** | `projects/goldenquill/RUNTIME_MATURITY_MATRIX.md` (`runtime-live` section: `pipeline/orchestrator/provider_boundary.py`, `pipeline/linting/r_no_direct_provider_http.py`) | Outbound network calls to model providers go through a single wrapper, enforced at runtime AND by static lint. Infra-spec dependency/egress boundary: external dependency calls need a single enforced chokepoint + a lint gate. | [impl] |
| **Local-first / dependency-free runtime as a deliberate infra choice** | `projects/body-war/app/server.py:1-7` (stdlib-only, no install step); `projects/goldenquill` "Headless. Single-tenant. BYOK. Local-first." (`docs/v0_1_beta_deployment_runbook.md:21`) | Two independent projects deliberately choose zero/minimal external runtime deps for the first deployable. Infra-spec should let a profile declare a "no-external-dependency / local-first" stance as a valid topology, not force the VPS ladder. | [impl] |
| **Arcanum observability harness as project-local runtime state** | `projects/body-war/.arcanum/observability/{config.json,reflection-state.json,signals/sigil-invocations.jsonl}`; `projects/sonar-loop/.arcanum/observability/` | Projects ship a local observability/reflection state surface (signals JSONL + reflection counters). This is the meta-runtime (Arcanum's own), distinct from app monitoring. Infra-spec must distinguish **app observability** (Prometheus/Grafana) from **process/agent observability** (Arcanum signals). | [impl] |

---

## Repeated Infra Obligations (appear in ≥2 projects)

1. **Generate-from-spec, then sync/drift-check** — infra configs are derived artifacts (whisky-doses skills, body-war templates). Cited above.
2. **Secret-class separation** — manual provisioning tokens vs IaC-generated app secrets vs dev-local `.env` (body-war template + real `.env.example`).
3. **Default-deny network posture** — firewall allow-list, DB never public (body-war template; goldenquill provider-boundary chokepoint).
4. **Mandatory runtime probe before "deployed"** — health check (body-war + whisky-doses); observable-per-step (goldenquill runbook).
5. **Promotion requires dated evidence** — graduation checklists (body-war/whisky-doses) and the maturity matrix's dated-CI-proof rule (goldenquill).
6. **Local-first viability** — minimal-dependency first deployable (body-war app, goldenquill v0.1).
7. **Project-local observability/reflection state surface** — `.arcanum/observability/` (body-war, sonar-loop).

---

## Project-Specific Anomalies

- **goldenquill is the outlier**: it is the only project whose operational doctrine (`RUNTIME_MATURITY_MATRIX.md`, `deployment_posture.py`, signed per-deployment router, observable-per-step runbook) goes far beyond the shared template bundle. None of these concepts (maturity taxonomy, per-call posture, derived-per-tenant config, fail-closed routing gates) appear in body-war/whisky-doses' `infra-architecture.md`. Anomaly = template/reality gap. `[impl]`
- **body-war is the only project with a runnable deployable** (`app/server.py`, 470 lines, stdlib-only) and a *real* (non-template) `.env.example` showing third-party OAuth integration (Strava). The README explicitly frames the app as a "validation channel," not production. `[impl]`
- **sonar-loop governs runtime fallback as a pure spec** (`projects/sonar-loop/README.md`) — runtime/risk decisions are first-class but there is zero deploy artifact. Infra theory applied without deployment. `[doc]`
- **whisky-doses + body-war carry byte-identical `infra-architecture.md`** (verified identical) — confirms a single canonical template propagated across projects; infra-spec should own this as one schema-backed artifact rather than copies. `[impl]`
- **equalizator / pos-multilevel have no infra surface at all** — they sit at the pre-infra DomainSpec baseline stage, proving infra-spec must be *optional and stage-gated*, not assumed present. `[doc]`
- **research/projects/domainspec `telemetry/signals.jsonl` is 0B** — a declared telemetry surface with no data; an empty-evidence anomaly worth noting for L5. `[residue]`

---

## Evidence-Backed Reusable Templates

These exist in-tree and are directly reusable as infra-spec seed artifacts (all cite real paths):

1. **`infra-architecture.md` constitution template** — `projects/body-war/domainspec/templates/infra-architecture.md` (== whisky-doses copy). Frontmatter axes: `preset, vps-provider, dns-provider, iac-tool, container-registry, ci-cd`. Sections: preset table, stack, environments, secrets, layout, networking, monitoring, CI/CD, scaling roadmap, conventions, do-not list. `[impl]`
2. **`slos.md` template** — `projects/body-war/domainspec/templates/slos.md`. Global SLOs + per-feature SLOs linked to O-rules + error-budget formula + alert routing. `[impl]`
3. **`setup.sh` provisioning template** — `projects/body-war/domainspec/templates/setup.sh` (255 lines). Idempotent VPS bootstrap. `[impl]`
4. **`agent-runner.md` template** — `projects/body-war/domainspec/templates/agent-runner.md`. Sandboxed agent CI runtime with secret/policy/cost boundaries. `[impl]`
5. **`domainspec-infra-deploy` / `domainspec-infra-architecture` SKILLs** — `projects/whisky-doses/.agents/skills/domainspec-infra-deploy/SKILL.md`, `.../domainspec-infra-architecture/SKILL.md`, agent `projects/whisky-doses/.codex/agents/domainspec-infra-architect.agent.toml`. Executable generation/drift logic. `[impl]`
6. **`RUNTIME_MATURITY_MATRIX.md` taxonomy** — `projects/goldenquill/RUNTIME_MATURITY_MATRIX.md`. Reusable seven-state operational-proof-status model + operating rules. `[impl]`

---

## Residue

- `[residue]` **Template ↔ reality drift unresolved**: the shared `infra-architecture.md` template encodes a VPS/Pulumi/Prometheus ladder; goldenquill (the most operationally mature project) uses none of it and instead invented a maturity matrix + posture model + signed-derivation model. Which is canonical for infra-spec? Unresolved by local L6 evidence.
- `[residue]` **poker-team unreadable**: the apparent origin of the infra template (`ghcr.io/poker-team/backend` example) is an empty submodule; its real `infra/` (referenced by strategy L3 as `validation/poker-team/infra/`) could not be inspected.
- `[residue]` **implementation/domainspec empty**: broken submodule pointer; deferred per strategy.
- `[residue]` **research/projects/domainspec telemetry is 0B**: declared-but-empty runtime evidence surface.
- `[residue]` **`docker-compose.prod.yml` / `Caddyfile` / `prometheus.yml` are never present in-tree** in any inspected project — they are only *described as generation targets*. No concrete generated instance exists to validate the generator against. Counterexample discipline (L2) flags this: every "generates X" claim lacks an X fixture.

---

## Child-Dispatch Proposals

Proposed (gated behind explicit approval per strategy):

### CD-L6-1 — goldenquill operational-doctrine mini-atlas
- parent_dispatch_id: `infra-spec-research-strategy-20260603`
- scope: Extract goldenquill's full operational doctrine (maturity matrix, `deployment_posture.py`, signed router derivation, observable-per-step runbook, provider-boundary enforcement, runtime_integrity tests) into a dedicated infra-spec mini-atlas; goldenquill alone has enough infra material to warrant it (strategy trigger: "a project has enough infra material to deserve its own mini-atlas").
- owning lane: L6 (with L2 Lean-transfer and L5 observability cross-review)
- roles: archaeologist (extract), skeptic (demote unsupported promotions), owner-boundary (confirm this stays research, not goldenquill governance authority)
- inputs: `projects/goldenquill/RUNTIME_MATURITY_MATRIX.md`, `projects/goldenquill/pipeline/orchestrator/deployment_posture.py`, `projects/goldenquill/router.yaml`, `projects/goldenquill/docs/v0_1_beta_deployment_runbook.md`, `projects/goldenquill/pipeline/runtime_integrity/`, `projects/goldenquill/tests/runtime_integrity/`
- expected artifacts: `ops/development/infra-spec-goldenquill-mini-atlas.md`
- stop conditions: doctrine extracted + classified; or a contradiction with the shared template that needs L4/L7 to resolve
- join policy: feeds L4 (schema axes) and the interpretation tournament
- validation evidence: every extracted state/posture/gate cites a goldenquill path + dated lock_history/CI reference where claimed

### CD-L6-2 — generator-vs-fixture gap (counterexample discipline)
- parent_dispatch_id: `infra-spec-research-strategy-20260603`
- scope: The infra-deploy SKILL claims to generate compose/Caddy/prometheus/alerts, but no generated instance exists in any inspected project; design fixture-first validation (input observability.md/slos.md → expected generated artifact) before infra-spec trusts the generator.
- owning lane: L6 → hands to L4 (schema) / L5 (observability)
- roles: archaeologist, skeptic, schema-governor
- inputs: `projects/whisky-doses/.agents/skills/domainspec-infra-deploy/SKILL.md`, `projects/body-war/domainspec/templates/{slos.md,observability.md,infra-architecture.md}`
- expected artifacts: fixture-plan section in `ops/development/infra-spec-validation-ledger.md`
- stop conditions: a minimal input→output fixture pair is specified, or it is confirmed no source project can supply a golden output
- join policy: feeds L4 schema validation gate
- validation evidence: fixture cites template input paths; no claim of a passing generator without an output fixture

Count: 2 child-dispatch proposals.

---

## Receipt Summary

- path_citation_confirmed: yes (every pattern/obligation/anomaly/template/residue row cites a concrete in-tree path)
- empty/deferred: `validation/poker-team`, `implementation/domainspec`
- no infra-spec authority claimed; runtime evidence not promoted to authority
