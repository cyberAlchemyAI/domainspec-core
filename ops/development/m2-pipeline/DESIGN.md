---
module: m2-pipeline
version: current
status: draft
updatedAt: 2026-06-14
docType: design
---

# DESIGN: M2 — DomainSpec Capability Pipeline

Design basis: [SPEC.md](SPEC.md); the harvest rows in [../domainspec-wedge-inventory.md](../domainspec-wedge-inventory.md); decisions B1/B2/B3.

## View 1 — How the 6 capabilities compose on the spec template
```
DomainSpec SPEC (M1, public)
  ├─ Concept Registry ──────────► C1 sync-registry (aggregate typed registry + edges)
  ├─ aspect docs (states/ops/…) ─► C3 test-derivation  (obligations → TEST-SPEC)
  │                              ─► C4 obs-derivation   (O1–O16 → metric obligations)
  │                              ─► C5 sync-user-stories (slices → STORIES + coverage matrix)
  └─ SPEC + code ───────────────► C6 audit-alignment   (compliant/partial/missing/extra)
source code + tag schema ───────► C2 code-tag toolchain (extract→validate→drift)  [spec-independent]
```

## View 2 — Dependency / interface rules
- All consume the **frozen M1 aspect-doc + Concept Registry contract**. Freeze it (keystone TASK-VERIFY M2-CONTRACT.md) before C3/C4/C5 build.
- C2 is independent (reads code, not the spec) → can build anytime; lowest coupling, cleanest wedge.
- C3 and C4 share the same shape ("aspect clause → typed obligation + content-addressed key") → build a shared derivation kernel, two rule profiles.
- C1 is an *update* to the existing `definitions-governance` sigil, not a new one → smaller blast radius.

## View 3 — New-sigil vs improvement vs tooling
- New sigils (sigil-development --new): C3, C4, C5, C6.
- Improvement (sigil-development --update): C1 → definitions-governance.
- Deterministic tooling packaged as a sigil + scripts: C2.

## View 4 — Governance / wedge-protection
- C6 audit-alignment must be severed from `validate-governance-chain` / promotion-DAG logic (that's CyberAlchemy moat). Audit the spec-vs-code fidelity only.
- C3 built fresh (B3): no DS engine code crosses; the private `tools/test-derivation-engine/` skeleton is design reference only.
- Each public sigil doc carries R-IB-1 framing; no bug-reduction claim without instrumentation (R-IB-3).

## Risks / mitigations
- **Spec contract drift** → freeze + version the M1 aspect/registry interface before building consumers.
- **C3 effort** (fresh deterministic compiler) → layer it: L0 = single rule type (e.g. state-transition → existence test) end-to-end, then expand cardinalities.
- **Audit coupling** → C6 starts from a clean spec-vs-code classifier; never imports governance-chain validators.
