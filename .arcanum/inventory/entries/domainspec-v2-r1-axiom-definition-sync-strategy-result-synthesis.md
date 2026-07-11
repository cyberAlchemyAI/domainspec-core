---
tags: [inventory, strategy-result, dispatch, subagents, research, findings, v2-repo, cyberalchemy-v2, definitions-governance, build-from-owned, promotion-guardrail, claim-proof]
node_type: synthesis
is_session: false
layer: semantic-governance
nature: reference
status: candidate
created: 2026-07-09
dispatch_id: 2026-07-09-r1-axiom-definition-sync-fix-research
dispatch_type: research
working_folder: projects/domainspec-v2/development/reformulate-batch1/r1-axioms-closeout/research/axiom-definition-sync-fix/
sources: [projects/domainspec-v2/development/reformulate-batch1/r1-axioms-closeout/research/axiom-definition-sync-fix/research.md, projects/domainspec-v2/development/reformulate-batch1/r1-axioms-closeout/research/axiom-definition-sync-fix/findings.md, telemetry/agents/subagents-dispatch.yaml, projects/domainspec-v2/authority/AXIOMS.md, projects/domainspec-v2/authority/AXIOMS.yml, cyberAlchemy-v2/authority/definitions/DEFINITIONS.md]
---

# DomainSpec v2 R1 Axiom Definition-Sync Strategy Result

This is a non-authority Inventory read model for the governed research dispatch
`2026-07-09-r1-axiom-definition-sync-fix-research`. It records the accepted
strategy result and points to the durable research artifacts. It does not
promote a new CAV2 authority kind, redefine CAV2 terms, close R1 by itself, or
mutate the DomainSpec v2 AXIOMS authority files.

## Strategy Summary

**P1 trigger decision:** dispatch was justified by synthesis, context
protection, isolation, and parallelism. The run combined CAV2 definition
semantics, DomainSpec v2 AXIOMS artifact mechanics, R1 closeout lifecycle
constraints, and three skeptic gates before accepting a fix recommendation.

**Lanes / groups:**

- `explorers` ran three lenses over CAV2 canonical semantics, DomainSpec
  artifact mechanics, and R1 closeout sequencing.
- `synthesizer` reconciled the explorer returns into candidate repair options.
- `reviewers` attacked the synthesis through precedent/owner-route,
  non-vacuity, and definitional-soundness gates.
- `writer` produced `findings.md`.
- `auditor` evaluated `findings.md` only, requested one row-level repair
  revision, then approved the revised findings.

**Subagents and angles:**

- `Tarski, Alfred` — CAV2 canonical semantics and D53/D54/D49 acceptance tests.
- `van Lamsweerde, Axel` — DomainSpec artifact mechanics and patch surfaces.
- `Simon, Herbert` — R1 closeout lifecycle and decision needs.
- `Lawvere, F. William` — candidate repair synthesis.
- `Kuhn, Thomas` — precedent and owner-route attack.
- `Popper, Karl` — non-vacuity attack requiring before/after row witnesses.
- `Wittgenstein, Ludwig` — definitional-soundness attack.
- `Gadamer, Hans-Georg` — findings writer.
- `Brandenburg, Martin` — final auditor.

**Dependency flow:** explorers -> synthesizer -> reviewers -> writer ->
auditor. The sheet included a synthesizer->reviewers zig-zag (`loop_cap: 1`)
and auditor->writer feedback (`loop_cap: 1`). The auditor used the revision
edge once.

**Gate / ledger state:** check-tension returned double PASS before human
confirmation. The human confirmed. The dispatch row and close row are appended
to `telemetry/agents/subagents-dispatch.yaml`; close state is
`exit_reason: resolved`, `agents_spawned.total: 9`, and `loops_used: 1`.

## Accepted Result

The auditor accepted `findings.md`. The result is a **build-from-owned**
classification repair: patch only
`projects/domainspec-v2/authority/AXIOMS.md` and
`projects/domainspec-v2/authority/AXIOMS.yml` so the R1 continuity surface
classifies its rows against CAV2-D53, CAV2-D54, and CAV2-D49 without creating a
new authority kind or changing R1 substance.

The accepted row-level repair is:

| Row | Accepted classification |
| --- | --- |
| A1 | `local_role: invariant-shaped`; `cav2_shape.primary: CAV2-D54`; `authority_kind_rollup: Definition` cataloging only. |
| A2 | `local_role: invariant-shaped`; `cav2_shape.primary: CAV2-D54`; `authority_kind_rollup: Definition` cataloging only; rename `validates` to a downstream/non-enforcement field. |
| A3 | `local_role: invariant-shaped`; `cav2_shape.primary: CAV2-D54`; `authority_kind_rollup: Definition` cataloging only. |
| A4 | `local_role: routed-pointer`; `cav2_shape.primary: not-applicable`; stays routed to Saturn. |
| A5 | `local_role: split-routed-pointer`; `cav2_shape.primary: CAV2-D54` for the retained DomainSpec shift-left fragment and `not-applicable` for the Saturn reflection fragment. |
| A6 | `local_role: routed-pointer`; `cav2_shape.primary: not-applicable`; stays routed to Saturn. |

The result explicitly rejects splitting invariants into a new authority surface,
moving AXIOMS material into definitions, adding first-class `axiom` or
`invariant` authority kinds, encoding the upstream CAV2-D34 citation mismatch
into DomainSpec tests, changing A2/C6 substance, changing Saturn routing, or
touching R5/R6 material.

## Source Refs

- `projects/domainspec-v2/development/reformulate-batch1/r1-axioms-closeout/research/axiom-definition-sync-fix/research.md`
  — explorer transcript for CAV2 semantics, DomainSpec artifact mechanics, and
  R1 closeout sequencing.
- `projects/domainspec-v2/development/reformulate-batch1/r1-axioms-closeout/research/axiom-definition-sync-fix/findings.md`
  — auditor-approved findings, verdict matrix, row-level repair table, patch
  shape, decision needs, validation requirements, and upstream residue.
- `telemetry/agents/subagents-dispatch.yaml` — dispatch and close rows.

## Downstream Use

Use this entry when implementing `SWU-R1A-002` or deciding whether R1 can close
after the AXIOMS definition-sync repair. Treat it as a strategy-result read
model: canonical mutation still belongs to the relevant task-session or
definitions-governance owner route.

## Residue

- The AXIOMS files have not yet been patched with the accepted classification
  metadata.
- CAV2-D34 has an upstream citation mismatch in the axiom/invariant definitions;
  the accepted repair says not to encode `D34 = constitution` in DomainSpec.
- `axiom` and `invariant` remain semantic shapes, not first-class CAV2
  authority kinds, unless a future owner-gated D49 amendment changes the
  enumeration.
