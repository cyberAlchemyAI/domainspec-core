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
| `cards.example.json` | Example source-backed Evidence Cards for Park Track Control. |
| `selector-index.example.json` | Example source selector to card/index mapping. |
| `link-index.example.json` | Example non-authority Inventory read-model links. |
| `gap-risk-index.example.json` | Example unresolved decisions, risks, and next owners. |
| `index.example.json` | Example slice summary, tag index, and file manifest. |
| `retrieval.example.json` | Example lookup result with selected evidence, exclusions, gaps, and next owner. |

## Interface Rule

When a user invokes `$inventory` in a Body War session, infer the target from the
prompt, show `target-confirmation.md`, and wait for explicit confirmation before
creating or updating generated cards, indexes, retrieval fixtures, or coverage.

Do not create `pilot/park-track-control/` from these templates alone. That
slice waits for selector/link/index examples, validator checks, and operator
confirmation.

The `*.example.json` files must remain valid JSON because `TASK-BW-INV-004`
uses them as validator input fixtures.

## Validator

Run the feature-local validator from the Body War root:

```bash
python3 docs/features/inventory-interface-indexing/validators/validate-body-war-inventory-examples.py
```

The validator checks:

- positive example JSON parseability,
- source reference paths,
- selector-to-card references,
- controlled link edge vocabulary,
- non-authority link notices,
- required gap preservation,
- retrieval card, selector, and gap references,
- negative fixtures for bad source refs, bad edges, and missing gaps.
