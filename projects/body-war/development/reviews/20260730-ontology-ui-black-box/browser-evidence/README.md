# Browser evidence index

This folder contains black-box evidence for the exact Body War presentation graph served by a fresh loopback viewer runtime. The source and served graph both hashed to `e8f754e6aed7b05759439df82db421eb51fa050c78b86b37d5d689e89a751433`.

## Lenses

- `attackers/cold-reader/`: search, detail, breadcrumb, tour, focus-order, and console/network observations.
- `attackers/color-accessibility/`: default, grayscale, forced-colors, keyboard-focus, selected-relation, and reduced-motion screenshots.
- `attackers/branch-pivot/`: whole-graph counts, tour-scene behavior, relation traversal, non-tour Focus behavior, focus order, screenshots, and reduced-motion evidence.

## Evidence boundary

The browser evidence can show current rendered structure, reachability, state persistence, focus presentation, color-independent cues, motion parity, counts, and console/network behavior. It cannot show that a person understands or can retell the ontology, that four nodes are sufficient for comprehension, that any relation is authoritative beyond its admitted source, or that the viewer is promoted, released, deployed, or production-ready.

Token-bearing traces were not retained. The repository evidence uses redacted targets and sanitized paths.
