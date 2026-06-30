---
tags: [inventory, evidence-card, moat, attestation, commercialization, defensibility, claim-le-proof, build-from-owned]
node_type: evidence-card
is_session: false
status: candidate
created: 2026-06-29
boundary: INTERNAL — moat-adjacent (cite-results-withhold-mechanism)
sources: [cyberAlchemy-v2/development/attestation-capability/development/specimen/DEMO.md, cyberAlchemy-v2/development/attestation-capability/attest.py, cyberAlchemy-v2/development/attestation-capability/SKILL.md]
---

# Evidence Cards — Attestation capability (moat MVP)

Candidate Inventory read models from the attestation-capability L1 build (task-session, 2026-06-29). Promotion owners
= sigil-development / commercialization. Promote nothing. Synthesis home: [[attestation-capability-moat-mvp-synthesis]].
**cite-results-withhold-mechanism:** these cards capture verify *results*, never the mechanism internals.

## `attestation-l1-discriminating-verify-passes`
- ID: `attestation-l1-discriminating-verify-passes`
- Status: candidate
- Claim or candidate: The attestation L1 integrity-seal's **discriminating self-test PASSES** on a real cav2 decision record (`authority/decisions/2026-06-24-saturn-domainspec-public-disclosure.md`): **`verify(untampered)=valid` AND `verify(content-mutated)=tampered`** (the load-bearing two arms); plus controls — trailing-whitespace variant = `valid` (canon absorbs cosmetic), attestation's own hash swapped = `tampered`. `verify` is decidable+total, recomputes from the claimed state (never trusts an embedded copy), and is sound (`valid ⇒ claimed = attested`). A **non-vacuous, sound verifier** — not a self-confirming demo.
- Source refs: `…/attestation-capability/development/specimen/DEMO.md` (the 4-arm results table); `…/attest.py` (the runnable mechanism — private); `…/SKILL.md` §quality-bar (the discriminating self-test contract).
- Authority level: candidate capability evidence (demonstrated, runnable specimen).
- Promotion owner: sigil-development.
- Trace: task-session L1 SWU executed locally; two-arm test run + verified.
- Residue: L1 only (integrity-seal); L2 (external signature) intended-not-shipped.

## `attestation-moat-upgrade-ladder`
- ID: `attestation-moat-upgrade-ladder`
- Status: candidate
- Claim or candidate: The capability has a 3-rung ladder, claim≤proof: **L0 attributional record (OWNED** — decision-record convention + git attribution; authentic, not tamper-evident); **L1 integrity-seal (MVP — BUILT** — content-hash over a frozen canon; `verify` is a real recompute+compare check); **L2 external signature (the MOAT — intended-not-shipped** — binds external actor identity + a third-party verification procedure; the genuinely net-new work). The differentiator is **demonstration over assertion** (a runnable verifier + checked-in specimen — the exact Kodamai edge). **Gates Mint L2** (owner decision 2026-06-29 to build it).
- Source refs: `…/attestation-capability/SKILL.md` §process + §origin (the ladder + build-from-owned: kernel `decidePolicy_sound` as the verify template); `cyberAlchemy-v2/authority/decisions/2026-06-29-mint-signer-and-boundary.md` (the build decision).
- Authority level: candidate capability design (build-from-owned; L2 = net-new moat).
- Promotion owner: commercialization decision-gate / sigil-development.
- Trace: invoke define→design→handoff → sigil-development --new → task-session L1.
- Residue: L2 gated on the actor-identity model decision; the moat is attestation+governance-data (per [[machine-map-and-moat-synthesis]] / [[moat-stack-and-authority-triage-synthesis]]).
