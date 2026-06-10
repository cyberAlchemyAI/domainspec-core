# Infra-Spec Schema And Taxonomy Ledger (Lane L4)

Date: 2026-06-08
Lane: L4 — Schema And Taxonomy Governor
Parent dispatch: `infra-spec-research-strategy-20260603`
Question: what fields and axes should infra-spec actually encode?
Status: research evidence only; not infra-spec authority. READ-ONLY scrub; this ledger is the only write.

Claim classification legend (per Non-Negotiables):
`implementation-backed` (a working artifact realizes it) | `documented` (a template/doc asserts it) | `analogy` (carried from Lean/reflection/residue work) | `candidate` (proposed, no in-repo realization) | `residue` (named gap, unresolved).

---

## 1. Evidence Surfaces Scrubbed

| Surface | Path | Relevance |
| --- | --- | --- |
| Infra architecture template (the de facto current "infra-spec") | `projects/whisky-doses/domainspec/templates/infra-architecture.md`; identical copy `projects/body-war/domainspec/templates/infra-architecture.md` | Primary axis source: preset, providers, IaC, environments, secrets, networking, monitoring, CI/CD, promotion |
| Dispatch schema (YAML-first, validator-backed) | `.claude/skills/dispatch-spec/dispatch.schema.yml`; mirror `arcanum/formulae/dispatch-spec/dispatch.schema.yml`; JSON twin `*/dispatch.schema.json` | Already encodes boundary/owner/receipt/state-namespace/promotion-split/gate vocabulary in `boundary_evidence` |
| Dispatch validator | `.claude/skills/dispatch-spec/scripts/validate-dispatch.py` | Proves the "schema checks shape + script checks governance rules" two-layer validator pattern infra-spec should inherit |
| Ops-level YAML schema with status enums | `ops/development/skill-agent-canonical-map.schema.yml` | Precedent for `canonical_status` / `*_status` enums incl. `residue-candidate`, `missing-canonical`, `blocked-owner` |
| Pipeline signal schema | `projects/whisky-doses/domainspec/templates/SIGNAL-SCHEMA.md` | Observability-signal / receipt / severity / category / residue (`governance-gap`, `rework`, `proposal`) vocabulary |
| SLO template | `projects/whisky-doses/domainspec/templates/slos.md` | SLO/error-budget/alert-severity (P0–P3) axis, O-rule linkage |
| Operations template | `projects/whisky-doses/domainspec/templates/operations.md` | Actor, trigger, pre/postcondition, error-state vocabulary |
| States template | `projects/whisky-doses/domainspec/templates/states.md` | State-machine / transition / invariant vocabulary |
| Events template | `projects/whisky-doses/domainspec/templates/events.md` | Event producer/consumer/payload vocabulary |
| Governance baseline | `projects/whisky-doses/domainspec/templates/governance-baseline.md` | Authority, deterministic defaults, idempotency, audit metadata, readiness gate |
| Feature architecture template | `projects/whisky-doses/domainspec/templates/architecture.md` | Component, dependency direction (inbound/outbound/internal), boundary-rule, gate-result (pass/flag/block), owners frontmatter |
| Setup scaffolder | `projects/whisky-doses/domainspec/templates/setup.sh` | Shows `infra/` directory is generated, not hand-authored |
| DomainSpec changelog | `projects/whisky-doses/domainspec/CHANGELOG.md` (lines 266–276) | Existing "Infrastructure Binding Gate", "Production Readiness gate", "infra-deploy → registry-sync" pipeline stages |
| Architecture inventory schema | `arcanum/arcana/architecture-pattern-inventory/templates/architecture-package/pattern-library/inventory/architecture-inventory.schema.yml` | Layer / `must_not_depend_on` / concept / relationship / gap-severity schema precedent |

Negative finding (`residue`): no file matching `*infra*schema*` exists anywhere in the checkout (`find . -iname "*infra*schema*"` → empty). Infra-spec is net-new as a machine-readable schema; today it is a Markdown constitution only (`projects/whisky-doses/domainspec/templates/infra-architecture.md`).

---

## 2. YAML-First Schema Candidate Ledger (axis verdicts)

Each axis tested against the L4 candidate list. "Evidence path" is where the axis is already realized or documented; absence ⇒ `candidate`/`residue`.

| Axis | Verdict | Class | Evidence path | Rationale |
| --- | --- | --- | --- | --- |
| environment | **KEEP** | documented | `infra-architecture.md` (Environments table: local/staging/production + deploy trigger) | Already first-class; needs `name`, `purpose`, `url`, `deploy_trigger`, `branch`. Foundational coordinate for every other record. |
| actor/owner | **KEEP (merge into `owner`)** | implementation-backed | `dispatch.schema.yml` `$defs/state_namespace.owner` + `authority_map`; `architecture.md` `owners:` frontmatter; `operations.md` Actor field; `governance-baseline.md` "Backend is the business-logic authority" | "Actor" (runtime trigger, operations.md) and "owner" (governance authority, dispatch authority_map) are **two different concepts sharing a word** — see §3 conflict. Keep `owner` as the infra axis; route runtime "actor" to the operations layer, not infra-spec. |
| service/component | **KEEP** | documented | `infra-architecture.md` (Networking table services: app/web/postgres/caddy; Docker Compose service naming); `architecture.md` Component views | The unit infra binds ports/images/health to. Merge "service" and "component" — repo uses both for the same node. |
| boundary | **KEEP** | implementation-backed | `dispatch.schema.yml` `$defs/boundary` (kind enum: `state_write`, `external_context`, `capability_handoff`...); `architecture.md` "Boundary Rule"; `governance-baseline.md` "two-decimal normalized at boundaries" | Validator-backed precedent exists. Infra boundary kinds differ from dispatch kinds (network/secret/data/tenant) — reuse the **shape**, redefine the **enum**. |
| state namespace | **KEEP** | implementation-backed | `dispatch.schema.yml` `$defs/state_namespace` (required: `namespace`, `owner`, `write_policy`) | Directly reusable. Candidate Concept "State namespace" (strategy §273) wants source/runtime/generated/local/private/evidence partitioning — map to `write_policy`. |
| dependency | **KEEP** | documented | `architecture.md` "View 6: Dependency Interface View" (direction inbound/outbound/internal + boundary rule); `infra-architecture.md` stack layers; `architecture-inventory.schema.yml` `must_not_depend_on` | Topology edges between services + external providers. `must_not_depend_on` precedent gives a negative-constraint form worth keeping. |
| event/queue | **DROP from infra-spec core (defer to feature layer)** | documented | `events.md` (producer/consumer/payload); no queue/broker artifact found | Domain events are already owned by `events.md`. No message-broker, queue, or backpressure artifact exists in any infra surface (`residue` — see L7 gap-hunt overlap). Encoding event/queue in infra-spec now would duplicate the feature layer with no realization. Re-open only if a broker appears. |
| deployment unit | **KEEP (merge with service via `artifact`/image)** | documented | `infra-architecture.md` Image Naming `{registry}/{project}/{service}:{git-sha-short}`; Docker Compose stack; container-registry frontmatter | The deployable is the service image. Encode as a `deployment` block on the service record (image ref, registry, compose/IaC unit) rather than a separate top-level axis. |
| runtime profile | **KEEP (rename `preset`)** | documented | `infra-architecture.md` frontmatter `preset: dev\|single-vps\|split-vps\|ha` + Preset/Scaling-roadmap tables | Strong, already-enumerated axis. This is the single highest-signal infra axis in the repo. Each preset is a coherent runtime+IaC+monitoring+CI/CD bundle. |
| observability signal | **KEEP** | implementation-backed | `SIGNAL-SCHEMA.md` (signal envelope, type/severity/category, JSONL append-only); `slos.md` O-rule linkage; `infra-architecture.md` Prometheus/Grafana/OTel | Mature, validator-described (completeness invariants C1–C5). Infra-spec should *reference* signal definitions and declare *where* they flow (scrape targets, ports), not redefine them. |
| receipt | **KEEP** | implementation-backed | `dispatch.schema.yml` `$defs/receipt_expectation` (required_fields enum incl. `run_id`, `artifacts`, `validation_result`, `residue`); `arcanum/framework/observability/runs/` | Reusable receipt-expectation shape. Infra-spec receipt = proof a deploy/health-check ran (deploy receipt, health-check receipt). |
| failure/residue | **KEEP** | analogy+implementation-backed | `SIGNAL-SCHEMA.md` `governance-gap`/`rework`; `operations.md` Error States; `architecture.md` Risks; `skill-agent-canonical-map.schema.yml` `residue-candidate`; Lean residue work `ops/development/domainspec-lean-formalization-*` | Typed residue is carried from Lean (`analogy`) but has an in-repo enum precedent (`residue-candidate`). Each infra pattern needs ≥1 failure mode (strategy "counterexample discipline"). |
| validation gate | **KEEP** | implementation-backed | `dispatch.schema.yml` `gates[]` (kind enum: `validation`, `promotion_guardrail`, `human_approval`; on_fail: block/flag/defer/ask/reroute); `CHANGELOG.md` "Infrastructure Binding Gate", "Production Readiness gate"; `architecture.md` Gate Result (pass/flag/block) | Both an Arcanum-validator precedent AND a live DomainSpec-pipeline precedent. Strongest evidence base after runtime profile. |
| promotion status | **KEEP** | implementation-backed+analogy | `skill-agent-canonical-map.schema.yml` `canonical_status` enum; `reader.status` enum (present/missing/blocked-owner); Lean "promoted object / faithful promotion" `ops/development/domainspec-lean-formalization-glossary-deep-refresh/REFRESH-REPORT.md`; Candidate Concept "Operational proof status" (strategy §278) | Strategy proposes `specified→implemented→deployed→observed→validated→reflected→promoted`. In-repo realization exists for the *status-enum mechanism*; the **infra ladder itself is `candidate`** (no infra artifact uses these stages yet). |

Axes evaluated: **14**. Verdicts: KEEP 12 (3 via merge/rename), DROP-defer 1 (event/queue), plus owner/actor split flagged as conflict.

---

## 3. Vocabulary Conflicts

1. **"actor" vs "owner"** — `operations.md` "Actor" = runtime trigger (Authenticated User / System / Scheduler); `dispatch.schema.yml authority_map` + `architecture.md owners:` = governance owner. Same candidate axis "actor/owner" collides two meanings. *Resolution:* infra-spec keeps `owner` (governance authority over a resource); runtime "actor" stays in the operations/feature layer. `documented` conflict.

2. **"infra/runtime" overload** — the strategy itself (§18, `infra-spec-research-strategy.md`) warns that `ops/SKILLS-FIRST-RUNTIME-POLICY.md` etc. govern *skill-install/orchestration runtime*, NOT infrastructure. The word "runtime" in `infra-architecture.md` (Preset "Runtime" column = Docker Compose/managed containers) is the infra meaning. Do not import ops/runtime-surface vocabulary. `documented` conflict.

3. **"status" namespace collision** — at least four distinct status enums coexist: frontmatter `status: draft` (`slos.md`, `architecture.md`); gate result `pass/flag/block` (`architecture.md`, SIGNAL-SCHEMA step-verdict); `canonical_status` (`skill-agent-canonical-map.schema.yml`); deploy/promotion ladder (proposed). Infra-spec must namespace these: `doc_status`, `gate_result`, `promotion_status` — not a single `status`. `implementation-backed` conflict.

4. **"service" vs "component" vs "deployment unit"** — three words, one node. `infra-architecture.md` uses "service" (compose/networking); `architecture.md` uses "component"; the deployable image is the "deployment unit". *Resolution:* one `service` record with a nested `deployment` block. `documented` conflict.

5. **"boundary kind" enum mismatch** — `dispatch.schema.yml $defs/boundary.kind` enumerates *capability/artifact/memory* boundaries, not *network/secret/data/tenant* infra boundaries. Reusing the schema shape without redefining the enum would mis-type infra boundaries. `implementation-backed` conflict.

---

## 4. Minimal Viable Infra-Spec Record Shape (YAML-first, validator-backed)

Proposal class: `candidate`. Inherits the dispatch-spec two-layer pattern (schema = shape via `.schema.yml`; `validate-*.py` = governance rules) per Non-Negotiables. Keep only KEEP-verdict axes; event/queue omitted.

```yaml
# infra-spec.schema.yml — top-level record (one per project/environment binding)
infra_spec_id: string            # required, minLength 1
schema_version: string           # required (precedent: skill-agent-canonical-map.schema.yml)
project: string                  # required
runtime_profile:                 # required (was "preset")
  name: dev | single-vps | split-vps | ha
environments:                    # required, >=1
  - name: string                 # local | staging | production | ...
    purpose: string
    url: string
    deploy_trigger: string       # branch/push/manual
    branch: string
services:                        # required, >=1  (service == component == deployment unit)
  - name: string                 # app | web | postgres | caddy | ...
    owner: string                # governance authority (NOT runtime actor)
    deployment:                  # nested deployment-unit block
      image: string              # {registry}/{project}/{service}:{sha}
      registry: string
      internal_port: integer
      exposed: boolean
    dependencies:                # topology edges
      - target: string
        direction: inbound | outbound | internal
        must_not_depend_on: [string]   # negative constraint (architecture-inventory precedent)
boundaries:                      # network/secret/data/tenant — infra-specific enum
  - boundary_id: string
    kind: network | secret | data_store | tenant | policy | environment
    contract: string
    on_violation: block | flag | defer | ask | reroute
state_namespaces:                # reuse dispatch.schema.yml $defs/state_namespace shape
  - namespace: source | runtime | generated | local | private | evidence
    owner: string
    write_policy: string
observability:                   # reference, do not redefine SIGNAL-SCHEMA
  signal_refs: [string]          # O-rule / signal type ids
  scrape_targets: [string]       # host:port (e.g. app:9464)
  slo_refs: [string]
receipts:                        # reuse $defs/receipt_expectation
  - receipt_id: string           # deploy-receipt | health-check-receipt
    producer: string
    required_fields: [run_id | artifacts | validation_result | status | residue]
    on_missing: block | flag | defer
gates:                           # reuse dispatch gates + DomainSpec binding gate
  - gate_id: string              # infra-binding | production-readiness | health-check
    kind: validation | promotion_guardrail | human_approval
    owner: string
    condition: string
    on_fail: block | flag | defer | ask | reroute
residue:                         # typed, >=1 required (counterexample discipline)
  - summary: string
    kind: failure_mode | unowned_state | drift | missing_receipt
    severity: low | medium | high | severe
promotion_status:                # namespaced; ladder is candidate
  stage: specified | implemented | deployed | observed | validated | reflected | promoted
doc_status: draft | active | deprecated   # frontmatter status, namespaced
```

Required-field floor (smallest validatable record): `infra_spec_id`, `schema_version`, `project`, `runtime_profile`, `environments[>=1]`, `services[>=1]`, `gates[>=1]`, `residue[>=1]`, `promotion_status`. Everything else is optional-but-typed, matching dispatch-spec's "required core + `additionalProperties: true`" posture.

One-line summary: **runtime_profile + environments + services(owner/deployment/dependencies) + boundaries + state_namespaces + observability-refs + receipts + gates + typed residue + namespaced promotion/doc status.**

---

## 5. Legacy-Schema Migration Cautions

| # | Caution | Evidence | Class |
| --- | --- | --- | --- |
| M1 | The current "infra-spec" is a **Markdown constitution with YAML frontmatter**, not a validator-backed schema. Migration must extract the body tables (Environments, Networking, Secrets) into the structured record, not just lift the frontmatter. | `infra-architecture.md` (frontmatter = 11 keys; the load-bearing data is in body tables) | documented |
| M2 | `infra/` is **generated by the `domainspec-infra-architecture` skill / setup.sh**, not authored. A schema must declare which fields are source-of-truth vs generated-derivative, or it will fight the generator. | `setup.sh` line 3 "Generated by domainspec-infra-architecture skill"; `CHANGELOG.md` line 276 | implementation-backed |
| M3 | Do **not** collapse the four status enums into one. Preserve `doc_status` / `gate_result` / `canonical_status` / `promotion_status` separately (§3 conflict 3). | `architecture.md`, `SIGNAL-SCHEMA.md`, `skill-agent-canonical-map.schema.yml` | implementation-backed |
| M4 | Reusing `dispatch.schema.yml $defs` (boundary/state_namespace/receipt/promotion_split) is tempting but the **boundary.kind enum is capability-shaped, not infra-shaped** — must be redefined, not imported verbatim (§3 conflict 5). | `dispatch.schema.yml` `$defs/boundary` | implementation-backed |
| M5 | Provide both `.schema.yml` and `.schema.json` (the dispatch precedent ships dual form) so existing JSON-only tooling keeps working. | `dispatch.schema.yml` + `dispatch.schema.json` both present | implementation-backed |
| M6 | The existing pipeline already has infra gates ("Infrastructure Binding Gate", "Production Readiness gate"). A new infra-spec gate set must **adopt these gate ids**, not invent parallel ones, or the pipeline will double-gate. | `CHANGELOG.md` lines 266–269 | implementation-backed |
| M7 | `validation/poker-team/infra/` is referenced by the strategy (L3 known path) and implied by template examples (`ghcr.io/poker-team/backend`) but **does not exist** in the checkout. Do not seed schema defaults from a phantom reference. | `find validation/poker-team/infra` → No such file; `infra-architecture.md` line 227 example | residue |

---

## 6. Residue Items

- **R1 (net-new gap):** No machine-readable infra schema exists today (`find . -iname "*infra*schema*"` empty). The infra-spec is currently a prose constitution only. Class: `residue`.
- **R2 (vocabulary):** `promotion_status` ladder (`specified→...→promoted`) has an enum-mechanism precedent but **no infra artifact uses it** — the ladder semantics are unproven for infrastructure. Class: `candidate`/`residue`.
- **R3 (phantom reference):** `validation/poker-team/infra/` cited as a starting path but absent (M7). Either L3/L6 must locate it elsewhere or it is stale. Class: `residue`.
- **R4 (deferred axis):** event/queue has no broker/queue/backpressure artifact anywhere; dropped from infra-spec core but the *gap* (no idempotency/backpressure infra) is real and overlaps L7. Class: `residue`.
- **R5 (boundary enum):** infra boundary kinds (network/secret/data/tenant/policy) are proposed with no in-repo realization beyond firewall rules in `infra-architecture.md` Networking; the enum is `candidate` and needs a fixture before promotion.

---

## 7. Child-Dispatch Proposals

**CD-L4-1 — Infra-spec schema fixture-first validation child.** Triggered by strategy §259 ("schema design needs fixture-first validation") and §257. Schema design (§4) cannot be promoted without a positive fixture + ≥1 violation fixture per axis (counterexample discipline). This crosses into validator-authoring territory and is a real DAG (one fixture set per KEEP axis = 12 branches > 5-subquestion trigger).

- parent_dispatch_id: `infra-spec-research-strategy-20260603`
- scope: author `infra-spec.schema.yml` + `infra-spec.schema.json` + `validate-infra-spec.py` + a passing fixture and a violation fixture per KEEP axis; do NOT wire into the DomainSpec pipeline.
- owning lane: L4 (schema/taxonomy), with validation-owner review.
- roles: schema author; skeptical validator-author; owner-boundary reviewer.
- inputs: this ledger §4/§5; `dispatch.schema.yml` + `validate-dispatch.py` as the pattern template; `infra-architecture.md` for axis data.
- expected artifacts: `infra-spec.schema.yml`, `.schema.json`, `validate-infra-spec.py`, `fixtures/` (pass + violation), a validation ledger entry.
- stop conditions: blocked if it requires editing `infra-architecture.md` (that is owned by the `domainspec-infra-architecture` skill, not this route) or claims infra-spec authority.
- join policy: parent_synthesis behind explicit approval gate (strategy §42).
- validation evidence: `validate-infra-spec.py` exits 0 on pass fixtures and `VALIDATION=block` on violation fixtures.

Count: **1** child-dispatch proposal.

---

## 8. Structured Receipt

- role_id: L4-schema-taxonomy-governor
- ledger_path: `ops/development/infra-spec-schema-taxonomy-ledger.md`
- axes_evaluated: 14
- minimal_record_shape: runtime_profile + environments + services(owner/deployment/dependencies) + boundaries(infra-kind enum) + state_namespaces + observability-refs + receipts + gates + typed residue + namespaced promotion/doc status; required floor = infra_spec_id, schema_version, project, runtime_profile, environments>=1, services>=1, gates>=1, residue>=1, promotion_status
- key_findings:
  - No infra schema exists; current infra-spec is a prose constitution only (`projects/whisky-doses/domainspec/templates/infra-architecture.md`; `find . -iname "*infra*schema*"` empty).
  - `dispatch.schema.yml` already encodes reusable boundary/owner/receipt/state_namespace/promotion_split/gate `$defs` (`.claude/skills/dispatch-spec/dispatch.schema.yml`) — reuse shapes, redefine boundary.kind enum.
  - Live pipeline precedent for infra gates and promotion: "Infrastructure Binding Gate" + "Production Readiness gate" (`projects/whisky-doses/domainspec/CHANGELOG.md` lines 266–269).
  - Status-enum mechanism precedent with residue/blocked-owner states (`ops/development/skill-agent-canonical-map.schema.yml`).
  - Observability/signal/receipt/severity vocabulary mature in `SIGNAL-SCHEMA.md` + `slos.md`; infra-spec should reference, not redefine.
  - "Runtime profile" (`preset`) is the highest-signal already-enumerated axis (`infra-architecture.md` frontmatter + Preset table).
  - event/queue dropped from core: no broker/queue artifact exists (gap, overlaps L7).
  - Four colliding status enums + actor/owner + service/component/deployment-unit + infra/runtime word overloads documented as conflicts.
- residue: R1 no infra schema (net-new); R2 promotion ladder unproven for infra; R3 phantom `validation/poker-team/infra/`; R4 no event/queue/backpressure infra; R5 infra boundary-kind enum lacks fixture.
- child_dispatch_proposals: 1 (CD-L4-1, fixture-first schema validation, parent `infra-spec-research-strategy-20260603`)
- path_citation_confirmed: yes
- blocked_fields_or_no_block: no-block
