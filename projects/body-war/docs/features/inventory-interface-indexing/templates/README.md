# Body War Inventory Templates

These templates define the Body War-local interface for using Inventory before
any pilot slice is generated.

## Template Set

| Template | Use |
| --- | --- |
| `target-confirmation.md` | Ask for confirmation before Inventory mutates Body War files. |
| `inventory-home-view.md` | Show the current Inventory package state in a chat session. |
| `status-view.md` | Report freshness, coverage, gaps, blockers, and next owner. |
| `explain-view.md` | Explain what Inventory is doing and what it is not doing. |
| `lookup-result-view.md` | Answer a lookup with selected evidence, exclusions, gaps, and next route. |

## Interface Rule

When a user invokes `$inventory` in a Body War session, infer the target from the
prompt, show `target-confirmation.md`, and wait for explicit confirmation before
creating or updating generated cards, indexes, retrieval fixtures, or coverage.

Do not create `pilot/park-track-control/` from these templates alone. That
slice waits for selector/link/index examples, validator checks, and operator
confirmation.
