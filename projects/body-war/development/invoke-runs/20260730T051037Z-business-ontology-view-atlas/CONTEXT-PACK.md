# Context Pack — Body War Business Ontology View Atlas

Status: `define-input-current`

## User intent

Apply the proposed actor/type-view idea to the whole Body War business
ontology, first define and design it with Invoke, then plan and execute the
complete finite implementation frontier through Task Session.

## Current admitted package

- `projects/body-war/ontology/business/nodes/`: 237 candidate node files,
  excluding `manifest.json`.
- `projects/body-war/ontology/business/relations/relations.json`: 231 admitted
  relation rows with zero missing endpoints.
- `projects/body-war/ontology/business/views/business.json`: the current
  business meaning branch contract.
- `projects/body-war/ontology/business/authoring/view-catalog.mjs`: current
  manually curated view catalog.
- `projects/body-war/ontology/business/scripts/generate-views.mjs`: current
  deterministic Markdown, SVG, print-HTML, and journey-HTML generator.
- `projects/body-war/ontology/business/tests/business-views.test.mjs`: current
  generated-view tests; baseline is 9/9 passing.

## Accepted research

- Relationship coverage:
  `projects/body-war/development/research/20260730-business-ontology-relationship-coverage/findings.md`.
- Current exact graph facts: 237 nodes, 231 relations, 193 incident nodes,
  44 explicit zero-degree nodes, and zero missing endpoints.
- The 44 zero-degree nodes are not permission to synthesize edges. They include
  lifecycle-policy members, standalone vocabulary, deferred concepts, source
  defects, associations awaiting owner review, and owner decisions.

## Projection facts

The current node set has 17 distinct `business_kind` values. A closed editorial
catalog assigns every observed kind to exactly one of six removable lenses:

| Lens | Kinds | Nodes | Internal relations | Cross-lens relations | Zero-degree nodes |
| --- | --- | ---: | ---: | ---: | ---: |
| Participants and boundaries | `actor`, `external_system`, `interface` | 17 | 1 | 25 | 2 |
| Responsibilities | `bounded_context`, `capability` | 30 | 34 | 0 | 1 |
| Behavior | `workflow`, `operation`, `query`, `event` | 72 | 40 | 74 | 0 |
| Business objects | `entity`, `value_object`, `ledger`, `metric` | 37 | 20 | 8 | 7 |
| Governance and lifecycle | `policy`, `lifecycle_state` | 69 | 26 | 0 | 24 |
| Hypotheses and outcomes | `premise`, `outcome` | 12 | 1 | 2 | 10 |

This yields 237 core memberships, exactly one per node; 122 relations whose
endpoints share a lens; and 109 exact cross-lens portal relations. All 231
relation IDs remain unique and are rendered once; inbound and outbound lens
indexes reference that canonical relation instead of copying it.

## Governing boundary

`cyberAlchemy-v2/ontology/BRANCH-AS-VIEW.md` defines a branch as an
interpretive view and forbids collapsing branch views into node types,
lifecycle states, owner routes, promotion state, or source authority.

The atlas therefore uses the term **editorial lens**. An editorial lens is a
removable UI grouping over a closed mapping of literal `business_kind` values;
it is not a semantic ontology branch or a new kind. The business branch remains
the sole meaning view in scope.

## Existing adjacent work excluded from this target

`projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/`
targets an OEW/upstream dashboard focus-scene overlay. It is current
user-owned evidence but not the local Body War business-view generator target.
This run neither overwrites nor completes it.

## Authority ceiling

Candidate-local projection only:

- `authority_effect: none`
- `release_admission: not-granted`
- no ontology node, relation, lifecycle policy, profile, or owner-route
  mutation
- no comprehension, release, deployment, or production-readiness claim
