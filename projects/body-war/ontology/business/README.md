# Body War Business Ontology

Status: `candidate-local`

This package is the typed business-meaning graph for the currently declared
Body War / TROQAR product. It covers the app-wide business model and the
candidate login-to-score-preview journey.

It is deliberately separate from:

- CyberAlchemy v2 ontology authority;
- DomainSpec executable nodes and logic;
- application implementation;
- source-backed route, verified score, territory-control, release, or
  production claims.

## Package shape

| Path | Role |
| --- | --- |
| `profile.json` | Package boundary, classification axes, and coverage contract. |
| `sources.json` | Exact source paths and SHA-256 bindings. |
| `schemas/` | Closed project-local JSON Schemas derived from the CAV2 candidate contracts. |
| `nodes/` | Typed business concepts grouped by one orthogonal `business_kind` family. |
| `NODE-INDEX.md` | Generated human review projection over the JSON node records. |
| `BUSINESS-VIEWS.md` | Generated SVG embeds, Mermaid topology views, and plain-language arrow chains over the business branch. |
| `BUSINESS-VIEWS.html` | Print-friendly generated gallery of relation sentences and lifecycle transition tables. |
| `BUSINESS-JOURNEY-EXPERIMENT.html` | Interactive progressive-disclosure experiment for reviewing login-to-score and activity-to-controller meaning paths. |
| `generated/views/*.svg` | Generated visual relation-sentence projections; nodes and `relations/relations.json` remain authoritative. |
| `relations/relations.json` | Typed directed relations with endpoint, owner, evidence, effect, and cycle guards. |
| `views/business.json` | Business branch as an interpretive view, never an authority route. |
| `lifecycle-policies/` | Explicit state transitions kept separate from node type and authority posture. |
| `residue.json` | Unresolved owner decisions and gaps; questions are fields, not ontology nodes. |
| `fixtures/` | Positive and negative controls. |
| `scripts/validate.mjs` | Deterministic validator and receipt builder. |
| `tests/business-ontology.test.mjs` | Node-native validation tests. |
| `receipts/validation-receipt.json` | Reproducible non-promoting validation evidence. |

## Model boundary

The package instantiates the candidate contracts in:

- `cyberAlchemy-v2/ontology/NODE-MODEL.md`;
- `cyberAlchemy-v2/ontology/RELATION-MODEL.md`;
- `cyberAlchemy-v2/ontology/BRANCH-AS-VIEW.md`;
- `cyberAlchemy-v2/ontology/PACKAGE-MODEL.md`.

`business_kind` is a Body War project-local classification axis. It does not
create a CyberAlchemy vault `node_type`. The `business` branch is a meaning
view, not a lifecycle state, namespace, owner, or promotion route.

## Validation

From the repository root:

```bash
node --test projects/body-war/ontology/business/tests/business-ontology.test.mjs
node projects/body-war/ontology/business/scripts/validate.mjs
node projects/body-war/ontology/business/scripts/generate-views.mjs
node projects/body-war/ontology/business/scripts/generate-index.mjs
```

The validator checks closed shapes, unique IDs, source digests, relation
endpoints, lifecycle transitions, value-cycle guards, required coverage, and
the prohibition on embedded executable logic.
