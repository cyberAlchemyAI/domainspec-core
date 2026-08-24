---
module: body-war-ontology-focus-scene-pivot
version: current
status: approved-for-design
updatedAt: 2026-07-30
docType: feature-glossary
---

# Glossary

| Term | Exact meaning | Not this |
| --- | --- | --- |
| Focus scene | A deterministic, removable UI projection containing admitted nodes, internal relations, and boundary portals | An ontology branch, subgraph authority, or new source object |
| Tour scene | A focus scene whose members are exactly one source-declared `tour[].nodeIds` set | Proof that four nodes are sufficient for understanding |
| One-hop scene | A non-tour focus scene containing the selected node and every directly connected endpoint | A semantic cluster inferred by the UI |
| Internal relation | An admitted edge with both endpoints inside the active scene | A relation copied or rewritten by the UI |
| Portal | An admitted directed edge with exactly one endpoint inside the active scene | A new ontology relation or a visual shortcut without provenance |
| Pivot | Atomic replacement of the active scene through a portal, with destination selection and breadcrumb update | Mere inspector navigation while the full graph remains |
| Relation tuple | Exact source, target, direction, generic `type`, relation-local `description`, endpoint `filePath`, statuses, and authority | A paraphrase that strengthens source meaning |
| Scene session | Active scene, active node, selected relation, breadcrumb, and optional suspended pre-tour state | Persistent domain or ontology state |
| Suspended scene state | Complete pre-tour UI state retained only for restoration | Active out-of-scene state during a tour |
| Source literal | A value copied from admitted presentation/sidecar data, including business kind, status, authority, path, type, or description | A UI-inferred lifecycle or semantic label |
| Semantic state | Canonical state used to compare pointer, keyboard, and reduced-motion outcomes | Layout coordinates or animation frames |
| Authority surface | Visible and accessible rendering of admitted `authority:none` and candidate-local posture | Permission to promote, release, or deploy |
| Structural browser evidence | Evidence that exact DOM, state, focus, input parity, and runtime conditions occurred | Evidence of comprehension, workload, or semantic correctness |
| Type layer | Existing filter grouping over node kinds | A focus unit, tour, or semantic branch |

## Vocabulary Rules

1. Use `portal` only for an existing relation crossing a scene boundary.
2. Use `pivot` only when scene replacement, destination selection, and history
   update commit together.
3. Keep generic relation `type` distinct from relation-local `description`.
4. Do not call a tour or neighborhood a semantic branch.
5. Do not use `accepted`, `promoted`, `released`, or `production-ready` for this
   candidate-local projection.

