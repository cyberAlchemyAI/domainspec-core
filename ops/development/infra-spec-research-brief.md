# Infra-Spec Research Brief

Dispatch: `infra-spec-research-strategy-20260603` · Execution: task-session full fan-out (read-only), 2026-06-08
Status: **research synthesis — candidate only.** Not an infra-spec package; not promotion authority.

## Question the route answered

Is a future `infra-spec` capability worth creating, and if so, what shape should it take — grounded in repository evidence, not theory?

## Answer (one paragraph)

Yes, but as an **evidence substrate**, not a deployment-doc format. The repository already contains a rich infrastructure *contract* vocabulary (preset ladders, secrets/network defaults, SLOs, generate-from-spec drift sync) and one real operational *promotion* model (goldenquill's 7-state runtime maturity matrix with fail-closed, signed gates) — but it contains **no realized deployment instances** in the parent checkout. The highest-value infra-spec is therefore the layer that binds an operational contract to runtime evidence (receipts, signals, drift) and governs promotion through typed status and typed residue, never letting runtime evidence self-promote. The MVP is the operational-contract spine (runtime_profile → services → boundaries → state namespaces + promotion gate + status floor), built by reusing existing `dispatch.schema.yml` `$defs`, with the full evidence layer phased in as real receipts/instances appear.

## Evidence base (path-cited highlights)

- **Intent without instances** (central fact): no Dockerfile/compose/Pulumi/Caddyfile/prometheus.yml exists anywhere in the parent checkout — `infra-spec-runtime-atlas.md`, `infra-spec-gap-hunt-ledger.md` (repo-wide `find` = zero).
- **Operational proof status precedent**: `projects/goldenquill/RUNTIME_MATURITY_MATRIX.md`; fail-closed posture `projects/goldenquill/pipeline/orchestrator/deployment_posture.py`.
- **Contract template**: `projects/body-war/domainspec/templates/infra-architecture.md` (== whisky-doses, byte-identical → no single source).
- **Schema substrate to reuse**: `.claude/skills/dispatch-spec/dispatch.schema.yml` (`boundary`, `authority_map`, `receipt_expectation`, `state_namespace`, `promotion_split`, `gate`).
- **Receipt/observability model**: `arcanum/framework/runtime/templates/RUN.json`+`STATUS.json` (incl. real `blocked` status); `SIGNAL-SCHEMA.md`, `slos.md`.
- **Lean discipline (transferred)**: `ops/development/domainspec-lean-formalization-claim-discipline-ledger.md` (4-status separation), `…-validation-ledger.md` (block≠fail).

## Candidate definition (owner-review-gated)

> infra-spec = a YAML-first, validator-backed **evidence substrate** binding a project's operational contract (services, environments, boundaries, secrets, gates) to its runtime evidence (receipts, signals, drift), governing promotion through typed status (specified/implemented/deployed/observed/validated/reflected/promoted) and typed residue, where runtime evidence never self-promotes.

See `infra-spec-candidate-dag.md` for the concept graph and `infra-spec-interpretation-tournament.md` for why the evidence-substrate reading won.

## What is net-new (worth creating)

- A typed `infra-spec` record (no machine-readable infra schema exists today).
- A **reversal/lifecycle** obligation set (rollback/migration/backup/retention) — absent across the entire infra surface (L7 G5/G6).
- A typed-residue + drift ledger as a first-class infra-spec output.

## What must remain analogy (do not over-import)

- Reflection-tower *object*, categorical machinery, physics/Lawvere bridges — only the gate *principle* transfers (L2).

## Confidence

- High: intent-without-instances; reuse-the-dispatch-`$defs`; goldenquill promotion precedent.
- Medium: exact MVP field set (needs fixture-first validation — L4 CD).
- Bounded gap: DomainSpec + poker-team submodules empty; canonical `ghcr.io/poker-team/backend` exemplar and any generated `infra/` not inspected.

## Recommendation

Proceed to a **fixture-first schema design** for the MVP operational-contract spine (not yet a package), and resolve the submodule coverage gap first. Details in `infra-spec-next-route-handoff.md`.
