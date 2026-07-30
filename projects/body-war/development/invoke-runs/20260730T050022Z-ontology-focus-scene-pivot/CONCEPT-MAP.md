---
module: body-war-ontology-focus-scene-pivot
version: current
status: define-seed
updatedAt: 2026-07-30
docType: ui-concept-map
authority_effect: none
---

# UI Concept Map

This map describes removable OEW presentation concepts. It is not a Body War
ontology mutation or a promotion proposal.

```mermaid
graph TD
    Graph[Admitted presentation graph] --> Rule[ProjectionBoundaryRule]
    Selection[Selected node] --> Rule
    Rule --> Scene[FocusScene]
    Scene --> Nodes[SceneNode set]
    Scene --> Internal[InternalRelation set]
    Scene --> Portals[Portal set]
    Portals --> Tuple[RelationTuple]
    Tuple --> Selected[SelectedRelation]
    Scene --> Session[SceneSession]
    Selected --> Session
    Breadcrumb[SceneBreadcrumb] --> Session
    Suspended[SuspendedSceneState] --> Session
    Witness[ProjectionWitness] -->|validates| Scene
    Interaction[InteractionWitness] -->|validates| Session
    Ceiling[ClaimCeiling] -->|constrains| Scene
```

## Layering Seed

| Boundary | Owns | Must not own |
| --- | --- | --- |
| Adapter admission | Exact presentation graph and sidecar fields | UI scene membership or interaction state |
| Pure projection core | Tour/one-hop membership and internal/portal classification | DOM, layout, browser focus, ontology mutation |
| Scene-session state | Active scene, selected relation, breadcrumb, tour suspension | Source rewriting or layout-derived meaning |
| OEW renderer | Visible scene, controls, focus destination, redundant semantic cues | Independent projection logic over the full graph |
| Acceptance harness | Test-owned fixtures, serialized state, browser/runtime receipt | Product authority or human-comprehension claims |
| Generated build | Materialized viewer bytes for validation | Canonical source ownership |

## Direction Rule

```text
admitted graph
  -> pure projection
    -> scene-session reducer
      -> renderer
        -> structural acceptance evidence
```

No reverse edge may mutate admitted graph meaning.

