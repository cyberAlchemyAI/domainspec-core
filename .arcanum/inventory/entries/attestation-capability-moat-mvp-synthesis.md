---
tags: [inventory, synthesis, moat, attestation, commercialization, defensibility, claim-le-proof, build-from-owned]
node_type: synthesis
is_session: false
status: candidate
created: 2026-06-29
boundary: INTERNAL — moat-adjacent (cite-results-withhold-mechanism); do NOT copy mechanism into public arcanum/
sources:
  - cyberAlchemy-v2/development/attestation-capability/SPEC.md
  - cyberAlchemy-v2/development/attestation-capability/SKILL.md
  - cyberAlchemy-v2/development/attestation-capability/development/specimen/DEMO.md
  - cyberAlchemy-v2/authority/decisions/2026-06-29-mint-signer-and-boundary.md
---

# Attestation capability — the moat MVP (L1 integrity-seal, BUILT + demonstrated)

Candidate Inventory synthesis (**promotes nothing**; owner = sigil-development + commercialization). A NEW cav2
capability greenlit by owner decision (2026-06-29) as the **attestation-is-the-moat** bet — and its **L1 rung is
BUILT and demonstrated**, the first spec→running artifact in the Mint arc. Build-from-owned; cross-links the moat
thread [[kodamai-smithe-correctness-layer-synthesis]] + [[moat-stack-and-authority-triage-synthesis]].

## What it is
Upgrades a cav2 "signed governance act" from an **attributional markdown record** into a **verifiable attestation**:
`attest(governance-act) → artifact{header, artifact_sha256, seal}` + a runnable `verify(artifact, claimed) →
valid|tampered`. `verify` is decidable+total, recomputes from the claimed state (never trusts an embedded copy), and
its `valid` condition is independently defined — inheriting the kernel's `decidePolicy_sound` sound-verifier discipline.

## The upgrade ladder (claim ≤ proof)
- **L0 — attributional record (owned):** decision-record convention + git attribution. Authentic, not tamper-evident.
- **L1 — integrity-seal (MVP — BUILT 2026-06-29):** content-hash over a frozen canonicalization; `verify` is a real
  recompute+compare check. **Demonstrated** on a real cav2 decision record: the **discriminating self-test PASSES** —
  `verify(untampered)=valid` AND `verify(content-mutated)=tampered` (+ controls: whitespace-absorbed=valid,
  attestation-tampered=tampered). A non-vacuous, sound verifier.
- **L2 — external signature (the moat; intended-not-shipped):** binds external actor identity to the seal + a
  third-party verification procedure. The genuinely net-new moat work; gated on the actor-identity decision.

## Why it matters (the differentiator)
**Demonstration over assertion** — the exact edge the Kodamai finding named: a runnable verifier + a checked-in
specimen, not a "proof artifact" with no checker. The moat is **attestation + governance-data** (machine-map);
this is its runnable MVP. **Gates Mint L2** (Mint's signed decision-gate calls `attest(mint-act)`).

## Boundary
INTERNAL, moat-adjacent. **cite-results-withhold-mechanism** (per the engine-moat decision): the verify *results*
(specimen, verdict surface, passing/tamper-detected runs) are demonstrable; the *mechanism* (canon rule, hash
construction, L2 scheme) stays private in `attest.py` — never public `arcanum/`. L0 owned, L1 MVP built, L2
intended-not-shipped. Inventory candidate read-model; promotes nothing.
