# Infra-Spec Research Strategy

Date: 2026-06-03
Dispatch: `infra-spec-research-strategy-20260603`
Branch: `codex/infra-spec`
Status: proposed research route, not implementation authority

## Objective

Build the evidence base for a future `infra-spec` capability by scrubbing the whole repository, extracting lessons from `domainspec-lean-formalization`, comparing every available implementation and validation infra surface, and deliberately hunting for concepts we have not mapped yet.

The output of this route is not the infra-spec package. It is the route that makes the package worth creating.

## Starting Thesis

Infra-spec should not be "deployment docs with nicer names."

The likely shape is a governed infrastructure contract that connects:

- source intent and runtime realization
- schemas and deployed instances
- environment boundaries and state namespaces
- deployment topology and operational behavior
- observability, receipts, and reflection
- failure residue and repair routes
- owner boundaries and promotion gates

Lean formalization gives the core warning: schema preservation, instance preservation, proof status, build status, and bridge language are different budgets. Infra-spec should inherit that discipline.

## Non-Negotiables

- Research claims need concrete path evidence.
- New canonical machine-readable schemas should be YAML-first and validator-backed.
- Runtime evidence cannot become promotion authority by itself.
- Analogies from Lean, reflection tower, residue, or CyberAlchemy must be labeled as theorem-backed, documented, implementation-backed, analogy, candidate, or residue.
- Child fan-outs are allowed when a lane becomes a real DAG, but execution stays behind an explicit approval gate.
- The strategy may write `ops/development/infra-spec-*` artifacts only.

## Parent Route

1. Recover prior lessons.
   Read dispatch-spec guardrails, Lean formalization research outputs, schema constitution memory, repository-zone cleanup memory, and existing ops/runtime surface reports.

2. X-ray the repository shape.
   Classify every top-level and nested evidence zone as canonical source, implementation source, validation sandbox, project snapshot, generated/local state, runtime install surface, or research evidence.

3. Fan out full-surface research lanes.
   Each lane returns path-cited receipts, contradictions, stale claims, candidate concepts, and residue.

4. Gate child dispatches.
   If a lane finds more than five dependent subquestions, crosses owner boundaries, or needs deeper external comparison, it proposes a child dispatch with `parent_dispatch_id=infra-spec-research-strategy-20260603`.

5. Zig-zag critique.
   Each lane is reviewed by a skeptical role and an owner-boundary role. Unsupported claims are demoted, not deleted.

6. Run an interpretation tournament.
   Candidate readings of infra-spec compete: deployment spec, operational contract, evidence substrate, reflection tower, residue-reduction system, and schema/runtime bridge.

7. Synthesize.
   Produce the infra-spec research brief, candidate DAG, concept ledger, validation ledger, and next-route handoff.

## Fan-Out Lanes

### L1: Repository Zone Cartographer

Question: where is infra knowledge already hiding?

Scrub:

- `arcanum/`
- `implementation/domainspec/`
- `domainspec-lean-formalization/`
- `validation/`
- `projects/`
- `research/`
- `docs/`
- `ops/`
- `tools/`
- root runtime/install surfaces such as `.codex`, `.arcanum`, `.github`, and skill/agent directories

Receipt:

- zone classification table
- owner/status map
- generated/local/runtime/source split
- deletion or stale-state candidates only as research findings

### L2: Lean Infra Translator

Question: which formalization lessons should constrain infra-spec?

Extract:

- schema versus instance distinction
- reflection tower and promotion gates
- typed residue
- counterexample discipline
- build/proof/status separation
- analogy demotion rules
- active-sorry/build-blocker style claim discipline

Receipt:

- Lean-to-infra transfer ledger
- concepts safe to reuse
- concepts that must remain analogy
- proof/build/status caution list

### L3: Runtime And Deployment Auditor

Question: what is the actual deploy/runtime evidence in the repo?

Scrub for:

- Dockerfiles, compose files, Pulumi, Caddy, Prometheus, Grafana, CI, hooks, env examples, setup scripts, deploy docs, runbooks, cloud-init, agent runners, local wrappers, runtime state, and service topology.

Known starting paths:

- `implementation/domainspec/infra/`
- `validation/poker-team/infra/`
- `projects/*/domainspec/templates/infra-architecture.md`
- `tools/*.sh`
- `.github/` surfaces
- `arcanum/framework/runtime/`
- `arcanum/framework/observability/`

Receipt:

- infra artifact atlas
- topology vocabulary candidates
- operational risk list
- stale or conflicting deployment claims

### L4: Schema And Taxonomy Governor

Question: what fields and axes should infra-spec actually encode?

Map:

- schema files
- templates
- feature docs
- architecture docs
- taxonomy and glossary surfaces
- status labels
- validation scripts
- DomainSpec feature pack conventions

Candidate axes to test:

- environment
- actor/owner
- service/component
- boundary
- state namespace
- dependency
- event/queue
- deployment unit
- runtime profile
- observability signal
- receipt
- failure/residue
- validation gate
- promotion status

Receipt:

- YAML-first schema candidate ledger
- vocabulary conflicts
- minimal viable infra-spec record shape
- legacy-schema migration cautions

### L5: Observability And Residue Analyst

Question: how should infra-spec expose drift, failure, and reflection?

Map:

- Arcanum observability
- workflow-reflect surfaces
- signal ledgers
- validation ledgers
- CI/test outputs
- runtime receipts
- project signal files
- failure modes and blocked states

Receipt:

- observability/residue map
- receipt requirements
- failure taxonomy candidates
- reflection loop candidates

### L6: Project Comparative Archaeologist

Question: what do concrete projects teach that generic infra theory misses?

Compare:

- `validation/poker-team`
- `projects/whisky-doses`
- `projects/body-war`
- `projects/sonar-loop`
- `projects/goldenquill`
- `projects/equalizator`
- `projects/pos-multilevel`
- `research/projects/domainspec`
- `implementation/domainspec`

Receipt:

- cross-project pattern catalog
- repeated infra obligations
- project-specific anomalies
- evidence-backed reusable templates

### L7: Skeptical Gap Hunter

Question: what have we not mapped yet?

Hunt for:

- unowned state
- hidden environment assumptions
- absent SLO/SLA/error-budget language
- secrets/config boundary gaps
- tenant or policy boundaries
- migration/rollback gaps
- dependency/version pinning gaps
- data lifecycle and retention gaps
- queue/backpressure/idempotency gaps
- observability blind spots
- mismatch between architecture docs and deploy reality
- missing "residue after deployment" accounting

Receipt:

- net-new candidate list
- rejected candidates
- open questions
- child-dispatch proposals

## Child Dispatch Triggers

Spawn a child dispatch proposal when:

- a lane finds more than five dependent subquestions
- a lane crosses into another owner surface
- external standard research becomes necessary
- a project has enough infra material to deserve its own mini-atlas
- schema design needs fixture-first validation
- a contradiction cannot be resolved by local evidence

Child dispatch minimum fields:

- parent dispatch id
- scope
- owning lane
- roles
- inputs
- expected artifacts
- stop conditions
- join policy
- validation evidence

## Candidate Concepts To Test

- Infra residue: what does not cross cleanly from spec to deployment, runtime, telemetry, or incident recovery.
- Runtime instance: the deployed or executable counterpart of a schema/spec.
- State namespace: explicit boundary around source, runtime, generated, local, private, and evidence state.
- Operational proof status: separate "specified", "implemented", "deployed", "observed", "validated", "reflected", and "promoted".
- Reflection tower for infra: local run evidence climbs only through receipt, validation, synthesis, decision, and owner review.
- Counterexample discipline: every positive infra pattern needs at least one failure mode or violation fixture.
- Evidence substrate: infra-spec as the bridge from runtime facts to governance, not just a static architecture doc.
- Boundary object: service, data store, queue, secret, policy, environment, actor, capability, and generated state each need different boundary rules.
- Topology versus obligation split: component graph is not the same as operational responsibility graph.

## Expected Artifacts

The execution route should produce:

- `ops/development/infra-spec-fanout-receipts.md`
- `ops/development/infra-spec-zone-classification-ledger.md`
- `ops/development/infra-spec-lean-transfer-ledger.md`
- `ops/development/infra-spec-runtime-atlas.md`
- `ops/development/infra-spec-schema-taxonomy-ledger.md`
- `ops/development/infra-spec-observability-residue-ledger.md`
- `ops/development/infra-spec-cross-project-pattern-catalog.md`
- `ops/development/infra-spec-gap-hunt-ledger.md`
- `ops/development/infra-spec-interpretation-tournament.md`
- `ops/development/infra-spec-candidate-dag.md`
- `ops/development/infra-spec-research-brief.md`
- `ops/development/infra-spec-validation-ledger.md`
- `ops/development/infra-spec-next-route-handoff.md`

## Validation

Dispatch validation command:

```bash
cd /home/vrondelli/projects/domainspec-core/arcanum
python3 formulae/dispatch-spec/scripts/validate-dispatch.py ../ops/development/infra-spec-research-strategy.dispatch.json
```

Coverage validation should check:

- every top-level zone was classified or explicitly deferred
- every candidate concept has evidence or residue status
- every lane returned a receipt
- every child-dispatch proposal has a bounded scope
- no research output claims infra-spec authority
- future schemas are `.schema.yml` and validator-backed

## Next Route

After this strategy passes dispatch validation, the next route is a task-session or refine execution of the fan-out. The first execution should remain read-only and produce the expected artifacts above.

Only after that should we create `infra-spec` as a formulae package, schema, skill, validator, and fixture set.
