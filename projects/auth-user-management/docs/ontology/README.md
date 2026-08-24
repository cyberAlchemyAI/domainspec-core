# Ontology

Machine-readable ontology for this project, produced by the `ontology-vault` sigil.

## Source-of-truth contract

Follows the repository policy in `arcanum/arcana/craft/templates/ledger.schema.yml`
(`source_of_truth_policy`) — the same split `.craft/ledger.yml` and `CRAFT.md` use:

| File | Role |
| ---- | ---- |
| `auth-domain-ontology.json` | **Source of truth.** Owns node IDs, roles, edges, enums, findings, confidence. |
| `ontology.schema.json` | JSON Schema (draft 2020-12) for the graph. Owns required fields and value domains. |
| `AUTH-DOMAIN-ONTOLOGY.md` | **Generated view.** Overwritten on every render — never edit by hand. |
| `validate.py` | Schema + referential-integrity + branch-discipline checks. |
| `render.py` | Regenerates the markdown view from the graph. |
| `indexes` (inside the JSON) | Rebuildable derived lookup surface, not authority. |

## Commands

Run from the project root (`projects/auth-user-management`):

```bash
python3 docs/ontology/validate.py     # exits non-zero on error
python3 docs/ontology/render.py       # rewrites AUTH-DOMAIN-ONTOLOGY.md
```

Edit the graph, then always run both — `validate.py` checks the indexes for
staleness, so a hand edit that skips a re-render is caught.

## What the validator checks

1. **Schema** — the graph conforms to `ontology.schema.json`.
2. **Identity** — node and edge IDs are unique; every node role is declared.
3. **Edge integrity** — every `from`/`to` resolves to a node, every edge type is
   declared, and endpoint roles satisfy the edge type's `from_roles`/`to_roles`.
4. **Finding cross-links** — every `finding_ref`, finding subject, confidence-cluster
   member, and promotion recommendation resolves.
5. **Evidence** — every evidence path exists on disk.
6. **Orphans** — nodes with no edge are reported (warning; decisions are exempt).
7. **Branch discipline** — a `business` branch graph may contain no bridge edge type
   (`realized_by`, `tested_by`, `observed_by`, `drifts_from`, …) and may not cite a
   system-branch source. This is what stops the ontology from silently claiming that
   documented intent is implemented.
8. **Registry non-collapse** — every node claiming `spec_registered: true` must actually
   appear in `docs/auth-access-control/SPEC.md#concept-registry`, and vice versa. The
   ontology may not invent authority by proximity.
9. **Index freshness** — recomputed counts and role indexes must match what is stored.
10. **Authority non-collapse** — `authority_effect` must be `none` and
    `promotion_policy.executes_promotion` must be `false`. An ontology map describes;
    only a named owner route may promote.

## Querying the graph

```bash
# every blocker and its owner route
jq -r '.findings[] | select(.severity=="blocker") | "\(.id)\t\(.owner_route)\t\(.summary)"' \
  docs/ontology/auth-domain-ontology.json

# concepts referenced but never defined
jq -r '.indexes.referenced_undefined[]' docs/ontology/auth-domain-ontology.json

# clusters where commitment outruns evidence
jq -r '.confidence_clusters[]
       | select(.commitment_confidence=="high" and .evidence_confidence=="low")
       | .label' docs/ontology/auth-domain-ontology.json

# everything constrained by invariant I1
jq -r '.edges[]
       | select(.type=="constrains" and .from=="auth-access-control.constraint.I1")
       | .to' docs/ontology/auth-domain-ontology.json

# which decision fixes a given concept's meaning
jq -r '.edges[] | select(.type=="decided_by" and .from=="auth-access-control.PermissionKey") | .to' \
  docs/ontology/auth-domain-ontology.json
```

## Boundaries

The graph is an **evidence artifact**, not source authority.

- `docs/auth-access-control/` remains the DomainSpec source of truth.
- `.craft/ledger.yml` remains the project knowledge source of truth.
- No finding here asserts anything about `src/`. Findings are defects *between
  documents*; whether the implementation already resolves any of them is a separate
  `business-system-bridge` question.
