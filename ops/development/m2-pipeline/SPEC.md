---
module: m2-pipeline
version: current
status: draft
updatedAt: 2026-06-14
docType: spec
---

# SPEC: M2 — DomainSpec Capability Pipeline

## What This Milestone Owns
The capabilities that **consume the now-public DomainSpec spec template** to derive, sync, and audit downstream artifacts. M1 (keystone) made the spec template + canonical taxonomy public; M2 builds the engines that read it. All wedge; all under the public DomainSpec brand.

## Capabilities (6)
| # | Capability | Kind | Reads | Owner lifecycle |
| --- | --- | --- | --- | --- |
| C1 | **sync-registry** | improve `definitions-governance` | SPEC Concept Registry | sigil-development (update) |
| C2 | **code-tag toolchain** | new (deterministic tooling) | source code + tag schema | sigil-development (new) |
| C3 | **test-derivation engine** | new sigil (fresh build, B3) | aspect docs (states/operations/…) | sigil-development (new) |
| C4 | **observability-derivation** (doc→metrics O1–O16) | new sigil | aspect docs + SPEC capabilities | sigil-development (new) |
| C5 | **sync-user-stories** | new sigil | aspect docs + concept IDs | sigil-development (new) |
| C6 | **audit-alignment** | new sigil | SPEC + implementation code | sigil-development (new) |

## Behavior Contracts
1. **Single spec contract (invariant):** every capability consumes the frozen DomainSpec aspect-doc + Concept Registry interface from M1. Any change to that interface is versioned, not silent.
2. **Determinism where claimed:** C2 and C3 are deterministic (no LLM in the derivation path); C3 is built fresh in arcanum (no DS code ported, per decision B3).
3. **Wedge-only:** no capability pulls moat material. Audits (C6) stay decoupled from the CyberAlchemy governance chain.
4. **Framing (R-IB-1):** any public claim uses "relocate review upstream, don't reduce it"; no unmeasured bug-reduction claims (R-IB-3).

## Success Condition
Each capability ships as an arcanum sigil/improvement with: a passing validation suite, a worked example against a real DomainSpec spec, and the R-IB framing baked into its docs.

## Out of Scope
The deferred improvements (workflow-reflect thresholds, context-builder scoring, orchestrate planner-gate, etc.) and free-standing sigils (brownfield, ontology-view, delegation-adapter) — separate milestone (M3).
