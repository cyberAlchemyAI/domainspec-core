# Runtime Handoff

## Recommended Next Invocation

Run:

```text
[$task-session] ops/development/verification-weaver/development-package/WORK-PACK.md
```

## Handoff Boundaries

The next runtime should modify primarily:

- `arcanum/arcana/verification-weaver/`

It may read this package and public owner skill files for context.

It should not modify:

- `arcanum/registry/`
- generated runtime skill packages;
- private implementation submodules;
- `validation/poker-team/`;
- existing owner capabilities, except to link to them from the new candidate
  package if needed.

## Owner Lane Handoffs

| Lane | Future owner handoff |
| --- | --- |
| Formal derivation | `test-derivation` |
| UX evidence | `ux-evidence-validator` |
| Execution mechanics | `experiment-harness` |
| Architecture gap mapping | `architecture-pattern-inventory` |
| Research evidence | `research-evidence-harness` |

## Promotion Path

Promotion requires a later route:

1. Candidate package validates locally.
2. Public-boundary scan passes.
3. Experiment-harness evidence exists.
4. Sigil-development review accepts the package.
5. Registry/generated runtime exposure is decided explicitly.

Until then, status remains candidate.

## Required Follow-On Owner

After Task Session creates and validates the candidate package, route to
`sigil-development` for lifecycle promotion review. Registry and generated
runtime exposure are blocked until that route accepts the evidence.
