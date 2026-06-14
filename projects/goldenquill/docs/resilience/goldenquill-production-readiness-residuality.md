---
title: GoldenQuill Production Readiness Residuality Spec
date: 2026-05-31
target: goldenquill-production-readiness
status: proposed
---

# Residuality Spec

## Target

GoldenQuill production-readiness route derived from the 2026-05-29 repository research package and the 2026-05-31 refine run.

## Desired Residue

After stress, interruption, partial execution, stale docs, or failed validation, the system should still leave behind:

- A clear authoritative source map.
- A surface classification map separating production target, prototype, archive, demo, generated, draft, and customer-facing artifacts.
- A maturity/proof matrix that states what is implemented, tested, scaffolded, blocked, or decision-gated.
- A verification command or manual proof path for every promoted claim.
- A decision trail that explains why a candidate goes to task-session, decision-gate, or backlog.
- Explicit runtime caveats when command resolution is proven but model-backed execution is not.

## Stressors

| Stressor | Failure Mode | Required Residue | Degradation Behavior | Owner Surface |
| --- | --- | --- | --- | --- |
| Front-door docs are stale relative to lock history | New agents act on row 279-era truth while current evidence reaches later rows | Current-truth delta table with cited paths and checked dates | Stop production mutation; allow docs-only refresh task-session | `PROJECT_STATUS.md`, `RUNTIME_MATURITY_MATRIX.md`, `pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md` |
| Product surfaces blur target/prototype/archive/demo | Prototype or generated artifact is described as production | Product surface index with status and allowed use | Block product claims; allow classification-only artifact | `apps/`, `landing/`, `docs/whitepapers/`, `docs/FRONTEND_BOUNDARY.md` |
| Feature claims outpace implementation proof | Skill or CLI is treated as shippable without module/test evidence | Implementation-status matrix with command, module, tests, maturity, blocker | Downgrade claim to scaffold/spec until proof appears | `skills/`, `pipeline/cli/`, `tests/`, `pipeline/*` |
| Local verification differs from CI | Agents mark done using partial checks | Unified verification receipt naming commands run and skipped | Allow narrow task completion only when skipped checks are explicit | `scripts/`, `.github/workflows/`, `tests/` |
| Substrate package is missing from wheels | Production install lacks contract module | Wheel/import smoke receipt | Block release packaging; allow packaging-only fix | `pyproject.toml`, `golden_quill_substrate/` |
| Signed-register context is optional in a production path | Cloud/provider boundary skips literal scan or register proof | Wiring check proving production route passes signed register | Fail closed on production route; allow test/doc task-session | `pipeline/orchestrator/provider_boundary.py`, `pipeline/vault/classification/` |
| Customer-facing language drifts | Deprecated or internal vocabulary reaches docs/site | Vocabulary check against three deployment postures | Decision-gate before customer-facing edits | `SOUL.md`, `router.yaml`, `landing/`, `docs/` |
| Org context leaks into general research | Cross-org facts contaminate production plan | Explicit non-source ledger for `orgs/*/PROJECT_CONTEXT.md` | Refuse cross-org synthesis; require named org and single context | `orgs/` |
| Runtime command surface resolves but nested execution fails | Artifact claims overstate runtime readiness | Runtime caveat and blocked-stage receipt | Permit local artifact use; block runtime proof claims | `.codex/commands/`, Arcanum runtime adapters |

## Attractors To Resist

- Building a new feature before current truth is refreshed.
- Treating a UI prototype as a production v0.1 surface.
- Treating command resolution as semantic execution proof.
- Treating a signed-register loader default as a deployment-ready provisioning path.
- Folding customer-facing language cleanup into a docs-only task without decision-gate.
- Reading org contexts to enrich a general repository design.

## Resilience Rules

1. Every production-readiness claim needs path evidence.
2. Every promoted candidate needs a validation path.
3. Every security or routing assumption needs a fail-closed behavior.
4. Every customer-facing vocabulary change needs decision-gate review.
5. Every runtime execution claim must say whether it is command resolution, deterministic local validation, or model-backed execution.
6. Every interrupted run should leave an artifact that a later agent can continue without re-reading the entire repository.

## Degraded Modes

| Mode | Trigger | Allowed Work | Blocked Work |
| --- | --- | --- | --- |
| Evidence-only | Source truth conflict or missing validation proof | Index, cite, compare, and write deltas | Production mutation |
| Docs-only | Candidate changes non-LOCKed explanatory docs | Refresh front-door docs and indexes | LOCKed architecture and production defaults |
| Gate-required | Candidate touches customer-facing language, security defaults, org data, or LOCKed text | Decision packet | Task-session implementation |
| Runtime-caveat | Command resolves but nested execution is not proven | Local design artifacts and deterministic validators | Claims of runtime-backed full lifecycle |
| Org-isolated | No named org | General repository architecture/design | Any org-specific synthesis |

## Success Criteria

- A future agent can choose the first task without rediscovering which docs are stale.
- A future agent can distinguish target, prototype, archive, demo, generated, draft, and customer-facing surfaces.
- A future agent can find the proof path for any promoted production-readiness claim.
- A future agent cannot silently route a decision-gated change into ordinary task-session.
