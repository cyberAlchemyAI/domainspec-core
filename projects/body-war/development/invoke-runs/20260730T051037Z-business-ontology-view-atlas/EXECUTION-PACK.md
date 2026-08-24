# Execution Pack — Body War Business Ontology View Atlas

Status: `plan-ready`

## Wave order

```mermaid
flowchart LR
  W1[W1 pure projection] --> W2[W2 static atlas]
  W2 --> W3[W3 browser evidence]
```

| Wave | SWU | Entry gate | Exit evidence |
| --- | --- | --- | --- |
| W1 | `SWU-BWVA-001` | current semantic digest lock; exact task selected | projection tests and coverage receipt |
| W2 | `SWU-BWVA-002` | W1 terminal and refresh receipts pass | generated atlas, freshness/static tests |
| W3 | `SWU-BWVA-003` | W2 terminal and refresh receipts pass; shared runtime resolves | browser receipt and screenshots |

## Execution rules

- Run one SWU per fresh Task Session.
- Rebuild a strict execution context from the corresponding context JSON.
- Re-resolve live semantic-source digests before every mutation.
- Stop on scope drift, unknown ownership, stale output, failed negative control,
  browser-runtime ambiguity, or failed closeout synchronization.
- Preserve failed receipts and route residue; do not repair ontology inputs.
- Use only the current repository Node and shared Playwright runtime.
- Do not add dependencies or a package root.

## Recomposition

```text
pure conserved ID indexes
  + exact original source records
  -> complete static-first HTML
  + pinned browser runtime
  -> structural prototype evidence
```

The recomposed claim is limited to the generated local prototype. It does not
prove application behavior, comprehension, release, or production readiness.

