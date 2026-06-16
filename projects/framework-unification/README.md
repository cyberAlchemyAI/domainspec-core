# framework-unification

Workspace for unifying three adjacent layers of the **CyberAlchemy agentic-system** (the
machine that turns user intent into finished code) into one coherent high-level view, and
then deciding how to join the pieces — assigning a **single owner** to each concept that is
currently defined in more than one place.

This is **engine work**, not an application: the three folders under `layers/` are facets of
the motor itself, not products built with it.

## Structure

```
framework-unification/
├── research/    Phase 1 — how everything communicates (RESEARCH.md). DONE.
└── layers/      the three layers being unified (moved here, history preserved)
    ├── domainspec-language/            representation — the contract/schema language
    ├── dispatch-composition-attack/    communication / observability — dispatch made visible
    └── cyber-alchemy-lean-fusion/      epistemology / gate — claim ≤ proof + typed residue
```

## The layers at a glance

| Layer | Owns | Status |
|---|---|---|
| **representation** (`domainspec-language`) | the language for contracts/schemas that validate pipeline artifacts | design |
| **communication** (`dispatch-composition-attack`) | making multi-agent dispatch an observable signal in the ledger | Phase 1 ready, Phase 2b blocked |
| **epistemology** (`cyber-alchemy-lean-fusion`) | the subset-rule gate (claim ≤ proof) + typed residue | blocked on residue-type question |

## Path (pipeline)

`research → discovery → paired-views (ontology-view / system-view / engineer-view) → unification plan`

- **research/** — complete. See [research/RESEARCH.md](research/RESEARCH.md).
- **discovery** — next: distill research into one map (components, boundaries, open decisions).
- **paired-views** — assign a single owner to every concept; resolve the two duplicated owners
  ("dispatch composition" and "type of residue").

## Open decisions to resolve

1. **"Dispatch composition" has two homes** — analytical ontology (cyber-alchemy View 03) vs
   executable schema (dispatch-composition-attack); both wait on the same `v0.5.2` typed-DAG
   ratification.
2. **"Type of residue"** — cyber-alchemy's residue-type blocker ≡ domainspec-language's
   `obligation_id` bridge (B-1). One decision, two faces.
3. **Observability producer gap** — the central ledger has a writer but no producer; building
   it unblocks the feedback loop.
