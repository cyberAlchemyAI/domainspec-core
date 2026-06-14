---
module: m2-pipeline
version: current
status: draft
updatedAt: 2026-06-14
docType: work-pack
---

# WORK-PACK: M2 Pipeline (roadmap)

This is a **milestone roadmap**, not 6 full work-packs. Each capability becomes its own `invoke plan` work-pack when picked up (per-capability decomposition deferred — authoring 6 complete plans up front would be speculative). This pack owns the scope, sequence, entry criteria, and owner per capability.

## Control Fields
| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | block | Gated on the M1 spec-contract freeze (see B-M2-1) before L1. |
| complexity | high | 6 capabilities, 4 new sigils, cross-sigil; staged. |
| outputMode | split (per capability, on pickup) | Roadmap here; capability work-packs later. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | |
| readinessProfile | pilot | |

## Objective
Ship the 6 capabilities that consume the public DomainSpec spec template, in dependency + value order, each as a validated arcanum sigil/improvement.

## Capability Slices
| Slice | Capability | Layer | Owner | Entry criteria | First-cut SWU sketch |
| --- | --- | --- | --- | --- | --- |
| M2-C1 | sync-registry → definitions-governance | L0 | sigil-development (update) | M1 Concept Registry contract frozen | parse SPEC concept tables → aggregate typed registry + edges + dup/drift |
| M2-C2 | code-tag toolchain (sigil) | L0 | sigil-development (new) | tag schema decoupled from DS paths | package extract/validate/composability/drift as a sigil + scripts; configurable schema+root |
| M2-C3 | test-derivation engine (fresh) | L1 | sigil-development (new) | C-contract frozen; design ref = private skeleton | L0-of-C3: one rule type (state-transition → existence test) → content-addressed TEST-SPEC + round-trip oracle; then expand cardinalities |
| M2-C4 | observability-derivation (O1–O16) | L1 | sigil-development (new) | C-contract frozen | shared derivation kernel w/ C3, metric-obligation rule profile from OBSERVABILITY rules |
| M2-C5 | sync-user-stories (sigil) | L2 | sigil-development (new) | aspect-doc contract frozen | slice taxonomy + STORIES emit + concept-coverage matrix (flag unmapped) |
| M2-C6 | audit-alignment (sigil) | L2 | sigil-development (new) | C3 obligations available as evidence source | spec-vs-code classifier (compliant/partial/missing/extra) + remediation; NO governance-chain import |

## Sequence (from layering)
**L0:** M2-C1 + M2-C2 (parallel — C2 is spec-independent, the cleanest standalone wedge). 
**L1:** M2-C3 + M2-C4 (shared deterministic kernel, two rule profiles). 
**L2:** M2-C5 + M2-C6 (consume specs + C3 output). 
**L3:** validation suites + worked examples + R-IB framing for all → promotion.

## Blockers
- **B-M2-1 (gating L1):** freeze the M1 aspect-doc + Concept Registry interface as `keystone-lift/.../M2-CONTRACT.md` (keystone TASK-VERIFY) before C3/C4/C5 build against it.
- **B-M2-2:** C6 must be authored without importing `validate-governance-chain`/promotion-DAG logic (moat). Verified at C6 design.
- **B-M2-3:** C3 fresh-build discipline (B3) — no DS engine code ported; skeleton is reference only.

## Validation Strategy
Per capability: a validation-example suite (sigil-development) + a worked example against a real DomainSpec spec + R-IB-1/3 framing check. Deterministic capabilities (C2, C3) add a determinism/round-trip check.

## Recorded Gaps
- **G-M2-1:** per-capability full work-packs not authored (deliberate — each via `invoke plan` on pickup). This roadmap defines their scope + entry criteria.
- **G-M2-2:** C3's internal layering (which rule types first) sketched, not fully planned — done at C3 pickup.

## Next Route
Per capability: `invoke plan <capability>` → `sigil-development --new/--update` → `task-session`. Start with L0 (M2-C1, M2-C2) once B-M2-1 (contract freeze) is satisfied by keystone-closeout.
