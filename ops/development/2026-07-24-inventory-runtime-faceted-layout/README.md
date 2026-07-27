---
module: inventory-runtime-faceted-layout
version: current
status: authored
updatedAt: 2026-07-24
docType: invoke-package
---

# Inventory Runtime And Faceted Entry Layout

Private Invoke authoring package for a proposed update to the public Inventory
sigil. Invoke owns these Define, Design, and Plan artifacts only.
`sigil-development` owns acceptance into the canonical Inventory development
cycle, source mutation, validation, generated-runtime synchronization, and
promotion readiness.

## Outcome

- Candidate B is planned as a deterministic append-transition receipt runtime.
- New entries gain one stable physical hierarchy:
  `entries/<namespace>/<record-class>/<stable-id>.md`.
- Concepts remain multi-valued logical facets and never create combinatorial
  directory trees.
- Legacy flat entries remain valid and are not migrated by this package.
- Apply mode remains non-atomic and must report possible partial mutation.
- Stored receipts remain historical; currentness verification is separately
  owned and excluded.

## Start Here

1. [SPEC.md](SPEC.md)
2. [ARCHITECTURE.md](ARCHITECTURE.md)
3. [WORK-PACK.md](WORK-PACK.md)
4. [SIGIL-HANDOFF.md](SIGIL-HANDOFF.md)
5. [VALIDATION.md](VALIDATION.md)

## Authority And Readiness

- Define: authored `pass`.
- Design: authored `pass`.
- Plan: authored `pass` for handoff to `sigil-development`.
- Distill: `pass` using bounded local Proposer/Balancer role simulation.
- Canonical source mutation: not performed.
- Runtime implemented or accepted: no.
- Task Session admission: blocked until `sigil-development` accepts this delta
  and reconciles the existing canonical Inventory work-pack.

## Source Evidence

- `ops/development/2026-07-24-inventory-runtime-research/findings.md`
- `ops/development/2026-07-24-inventory-runtime-research/closeout.json`
- `arcanum/arcana/inventory/development/SPEC.md`
- `arcanum/arcana/inventory/development/WORK-PACK.md`
- `arcanum/arcana/inventory/SKILL.md`
- `.arcanum/inventory/schema.md`
- `.arcanum/inventory/index.json`
