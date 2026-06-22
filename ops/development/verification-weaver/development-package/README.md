# Verification Weaver Development Package

Package status: `candidate`.

Target future capability: `arcanum/arcana/verification-weaver`.

Core verb: `route`.

This package is the Invoke authoring output for creating a public-safe Arcanum
verification weaving capability. The capability should route testing targets to
owner lanes and join their native receipts into a parent `VERIFICATION-WEAVE`
receipt. It must not become a generic all-in-one tester.

## Package Files

- `DEFINE.md` - problem statement, non-goals, and glossary.
- `DESIGN.md` - classifier, lane model, deny/allow rules, and oracle binding.
- `PLAN.md` - implementation order and validation gates.
- `OUTPUT-CONTRACT.md` - parent receipt schema.
- `QUALITY-BAR.md` - pass/flag/block criteria.
- `ANTI-PATTERNS.md` - false-success patterns to block.
- `IMPLEMENTATION-LAYERING.md` - layer and promotion boundary decisions.
- `DISPATCH-TRACE.md` - Dispatch Spec technique trace.
- `DISPATCH.json` - full handoff dispatch document for the cross-owner route.
- `DISTILL-VALIDATION.md` - Distill validation receipt for SWU readiness.
- `fixtures/synthetic/README.md` - public-safe fixture families.
- `negative-controls/NEGATIVE-CONTROLS.md` - fail-closed controls.
- `tasks/SWU-VW-001.md` - smallest coherent execution unit contract.
- `WORK-PACK.md` - executable work package for `task-session`.
- `RUNTIME-HANDOFF.md` - owner-lane handoff and promotion boundary.
- `INVOKE-RESULT.md` - package receipt.

## Boundary

Private implementation evidence in this parent repository is research input
only. The future public package must use synthetic fixtures, public-safe
contracts, and fresh public code.
