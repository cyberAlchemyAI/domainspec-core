# Execution Pack

## Selected frontier

- First selected unit: `SWU-IRO-001`.
- Explicit one-shot stream: `IRO-FULL-STREAM`.
- Machine contract:
  `work-pack/shared/EXECUTION-CONTRACT.json`.
- Stream purpose: preserve and finish the full objective across turns while
  pausing at every owner, mutation, public, consumer, and private boundary.

Starting the native Goal is a separate runtime action. This pack authorizes
Goal/profile creation only; it does not authorize implementation or public
mutation.

## IRO-001 executable route

1. Context Builder binds the strict Markdown and JSON/index handoff pack.
2. Decision Gate emits the complete bundle required by
   `work-pack/shared/DECISION-BUNDLE.schema.json`:
   - `OPTION-ADMISSIBILITY-REQUEST.json`;
   - `OPTION-ADMISSIBILITY-RECEIPT.json`;
   - `DECISION.json`;
   - `DECISION-SUMMARY.md`.
3. Task Session emits `terminal-receipt.json` using
   `work-pack/shared/TERMINAL-RECEIPT.schema.json`.
4. Invoke Refresh consumes that immutable terminal receipt, updates only the
   exact planning targets declared in the closeout request, and returns a
   joined `closeout-owner-receipt.json`.
5. The stream pauses before IRO-002 until the separate candidate-mutation gate
   is satisfied.

## Full-stream capability policy

| Capability | Allowed use | Forbidden use |
|---|---|---|
| `context-builder` | strict pack creation/refresh for the selected epoch | broad repository dump |
| `decision-gate` | blocker-level owner and authority decisions | inferred or ambient approval |
| `invoke:refresh` | exact planning/evidence closeout targets | implementation or cross-owner mutation |
| `task-session` | one selected owner-bounded SWU at a time | recursive next-unit execution |
| `sigil-development` | IRO-002/003 and separately approved IRO-004 | consumer/private ownership |
| `arcanum-bootstrap` | isolated IRO-005 generation and rollback proof | canonical acceptance or consumer install |
| shared Playwright | IRO-003/005 browser witnesses only | network access or product acceptance claims |

Subagents are denied by default. A unit may use one bounded helper only when an
owner contract or explicit operator instruction authorizes it; the parent must
join a terminal role receipt before synthesis. No multi-agent dispatch is
implied by this stream.

## Budget and iteration policy

- Maximum Task Session requests in one goal epoch: 10, one per declared unit.
- Maximum repair cycle per unit: 1; a second failure pauses and reports the
  exact owner/blocker instead of refreshing again.
- Maximum simultaneously active helpers: 1.
- Browser launches: at most 2, only the IRO-003 and IRO-005 witnesses.
- Network calls: 0 unless a later owner contract explicitly authorizes one.
- Each iteration revalidates controlling digests and the current WPRA epoch.

## Exact pause gates

| Before unit | Required receipt |
|---|---|
| IRO-002 | passing IRO-001 terminal plus joined closeout and explicit candidate-mutation approval |
| IRO-004 | passing IRO-003 receipt plus explicit public Arcanum owner approval and clean-worktree receipt |
| IRO-006 | passing IRO-005 parity receipt plus disposable-consumer locator/owner approval |
| IRO-007 | passing IRO-006 receipt plus exact ResonantOS worktree planning scope approval |
| IRO-008 | passing IRO-007 receipt plus orchestrator owner, catalog, and normalization bindings |
| IRO-009 | passing IRO-008 receipt plus private CAV2/ACI owner and field-binding approval |

Any semantic change to owner, material scope, validation, receipt, closeout, or
successor invalidates the current WPRA epoch and pauses for regeneration.

## Stop conditions

- Missing, stale, malformed, unjoined, or wrong-owner receipt.
- Any write outside the current unit's coordinator and owner scopes.
- Any unresolved mutation-critical owner or authority binding.
- Any attempt to treat the decision profile, native Goal, WPRA, or a prior
  receipt as ambient authorization.
- Any private content in public candidate/canonical/generated outputs.
- Any failed acceptance-critical validation, browser witness, parity check, or
  rollback check.
- Any attempt to claim release, deployment, production readiness, or whole
  reasoning-engine completion.

## Final report

The Goal report must list each unit and receipt, every pause/resume approval,
all extra sources used for named gaps, exact validation results, browser/runtime
provenance, changed files by owner, unresolved residue, and the honest lifecycle
ceiling reached.

