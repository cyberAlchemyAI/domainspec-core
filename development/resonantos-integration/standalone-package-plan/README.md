---
module: resonantos-cyberalchemy-standalone-package
status: draft
updatedAt: 2026-06-29
docType: invoke-plan-index
---

# ResonantOS CyberAlchemy Standalone Package Plan

This folder contains the canonical Invoke plan files for creating a standalone package for the
ResonantOS CyberAlchemy integration.

## Canonical Files

- `IMPLEMENTATION-LAYERING.md`: L0-L3 decision boundaries and promotion evidence.
- `WORK-PACK.md`: executable planning manifest and SWU index.
- `EXECUTION-PACK.md`: wave choreography for medium-complexity execution.
- `DISTILL-VALIDATION.md`: smallest-unit and recomposition validation.
- `PLAN-TRANSPORT.md`: Invoke transport report and next-route summary.
- `work-pack/shared/`: shared source context, decisions, gaps, and traceability.
- `work-pack/waves/`: execution ordering.
- `work-pack/tasks/`: task-local SWU contracts.

## Package Objective

Create a standalone, scrubbed package that lets a ResonantOS collaborator inspect the integration
boundary, copy or port public-safe governance contracts, run validator checks where applicable, and
see exactly which host-side implementation work remains.

## First Executable Unit

Start with `SWU-RCI-001` in `work-pack/tasks/TASK-PACKAGE-BOUNDARY.md`.
