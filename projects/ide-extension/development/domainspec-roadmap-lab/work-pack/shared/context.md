# Shared Execution Context

## Objective

Implement the approved [Roadmap Lab design](../../ARCHITECTURE-BUNDLE.md) in the
value order governed by [implementation layering](../../IMPLEMENTATION-LAYERING.md).
The browser teaches and returns reviewable evidence; it never owns DomainSpec,
Craft, Whisper, research, acceptance, or promotion.

## Source Contracts

- [Design context](../../DESIGN-CONTEXT.md) — bounded source selectors and
  obligations.
- [Architecture bundle](../../ARCHITECTURE-BUNDLE.md) — six views, interfaces,
  operations, state, and rules.
- [UX plan](../../UX-PLAN.md) — newcomer journey, states, and real human gate.
- [Design decisions](../../DESIGN-DECISIONS.md) — accepted choices and
  deferrals.
- `projects/ide-extension/SPEC.md:232-278` and
  `projects/ide-extension/ARCHITECTURE.md:146-185` — current Canvas contract.
- `projects/ide-extension/schemas/canvas-interaction-request.schema.json` —
  generic event request oracle.
- `projects/ide-extension/public/demo/l0.html:1390-1432` — exact message adapter.
- `projects/domainspec-v2/development/first-production-release/visibility/` —
  private roadmap projection, builder, data, template, tests, and generated HTML.

## Execution Invariants

1. One selected SWU per Task Session.
2. Inspect current dirty status and overlapping diff before mutation.
3. Never clean, revert, or silently absorb unrelated user changes.
4. Stable copy fields and semantic-event oracles precede UI behavior.
5. Proposal bindings are not editable participant inputs.
6. Canvas revision and roadmap input fingerprint remain separate.
7. Source requests do not grant browser filesystem access.
8. Owner evidence is referenced, not forged or replaced by local events.
9. Human/owner unavailability returns a truthful block.
10. Private material never moves into public `arcanum/`.

## Expected Return

Every SWU returns its ID, pass/flag/block/interrupted status, exact files,
validation with results, blockers, and a continuation note. Task Session stores
the receipt under the work-pack evidence/task-session surface selected at run
time.

