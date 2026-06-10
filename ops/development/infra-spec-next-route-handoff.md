# Infra-Spec Next-Route Handoff

Dispatch step: `handoff-next-route` · Status: recommendation only (cannot authorize package creation by itself)
Date: 2026-06-08 · Produced by: task-session full fan-out execution of `infra-spec-research-strategy-20260603`

## Where we are

The strategy's first read-only execution is complete. Evidence says infra-spec is worth creating as an **evidence substrate** (see `infra-spec-research-brief.md`). No `formulae/infra-spec`, schema, skill, validator, or registry entry was created — per the strategy's non-negotiables.

## Recommended next routes (in order; each needs its own approval)

1. **Clear the coverage gap first (cheap, unblocks the most).**
   - Fix the `implementation/domainspec` submodule pointer upstream (its pinned commit is not on the remote), then `git submodule update --init implementation/domainspec validation/poker-team`.
   - Register or remove `validation/sigil-spell-sandbox` in `.gitmodules`.
   - Re-run lanes L3 + L6 against the now-present `infra/` surfaces (child dispatches CD-L3-A, CD-L6-1).

2. **Fixture-first MVP schema design (not yet a package).**
   - Target the candidate DAG critical path (the operational-contract spine): `runtime_profile → services → boundaries → state_namespaces + promotion_gate + status floor`.
   - Reuse `dispatch.schema.yml` `$defs` (boundary/authority/receipt/state_namespace/promotion_split/gate); redefine `boundary.kind` for infra (network/secret/data/tenant).
   - Author one pass fixture + one violation fixture per kept axis (child dispatch CD-L4-1). Output: `infra-spec.schema.yml` candidate + fixtures under `ops/development/infra-spec-*`.
   - Route: `task-session` (or `refine` if the field set is still contested).

3. **Add the net-new reversal/lifecycle obligations.**
   - Rollback / migration / backup / retention — absent across the whole infra surface today (L7 G5/G6). Required before any `promoted` status is trustworthy.

4. **Repo-hygiene follow-ups (separate owners, not infra-spec scope).**
   - `.github/workflows/drift-check.yml` is coupled to the empty `implementation/domainspec` submodule (breaks CI when unpopulated) — DomainSpec/CI owner.
   - `.data/*.sqlite{,-shm,-wal}` committed unowned runtime state + `.arcanum/observability/` gitignore-vs-tracked drift — repo maintainer.

## Held child-dispatch proposals (12, behind approval gate)

L1×2, L2×1, L3×2, L4×1, L5×2, L6×2, L7×2. Each carries `parent_dispatch_id=infra-spec-research-strategy-20260603` and full bounded-scope fields in its lane ledger. **None executed.** Approve individually before running.

## Promotion guardrail (reaffirmed)

The handoff may *recommend* creating `formulae/infra-spec`, but cannot authorize it. Any mutation route must start from a validated candidate schema + explicit owner decision. Runtime evidence does not become promotion authority by itself.
