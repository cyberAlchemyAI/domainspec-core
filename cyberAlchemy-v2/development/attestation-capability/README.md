# Attestation / Signer — sigil (README)

**Status:** in-development · **INTERNAL** (moat-adjacent — verification *results* are demonstrable,
the attestation/signing/verifier *mechanism* stays private) · **intended-not-shipped** ·
**promotes nothing** · tier: **Arcana** (private cav2 capability — not a public Arcanum sigil; lives
in `cyberAlchemy-v2/development/attestation-capability/` until the L1 MVP is built + demonstrated and
the L2 blocks resolve, then an owner route decides promotion). Same boundary logic as the
[Mint sigil](../mint/README.md).

## Problem solved
Today a cav2 "signed governance act" is only **owner-authored + git-attributed** (e.g.
[`authority/decisions/*.md`](../../authority/decisions/README.md), the resonantos decisions):
authentic *by social/repo convention*, but **not tamper-evident and not externally verifiable**
(review C7 gap). This capability **upgrades that record into a verifiable attestation**: a sealed
(and, at the moat rung, signed) `⟨actor, act, artifact-state, timestamp⟩` tuple with a **runnable
third-party `verify` checker**. It is **the moat infrastructure** — the deliberate
[attestation-IS-the-moat bet](../../../.arcanum/inventory/entries/machine-map-and-moat-synthesis.md),
greenlit by [decision 2026-06-29](../../authority/decisions/2026-06-29-mint-signer-and-boundary.md)
(Decision 1) — not a Mint sub-task.

## Use this sigil when
- a consequential, owner-ratified cav2 act (a **decision record**, a **promotion** crossing a gate,
  or a **mint act**) needs to be **tamper-evident** and later **third-party-checkable**, not just
  committed markdown;
- Mint's L2 (signed decision-gate) needs its upstream `attest(mint-act)` dependency (see *How it
  gates Mint L2*).

## Do NOT use when
- a public Arcanum sigil/spell is the target (this capability is **INTERNAL**, moat-adjacent — never
  leak the mechanism into public `arcanum/`);
- the act is non-consequential (no governance act = nothing to attest);
- you want the **L2 external-signature/actor-identity** guarantee *now* — that rung is
  **intended-not-shipped** (net-new), and claiming it is shipped is the load-bearing anti-pattern.

## Inputs / outputs
**Inputs:** `governance_act` (the ratified content + `{kind ∈ decision|promotion|mint, id}`),
`actor` (the ratifying identity), `timestamp`. **Outputs:** an **attestation artifact** = the sealed
tuple header `(actor, act, timestamp, canon_version)` + a `seal` (L1 content-hash); at L2, + an
external-actor signature. The artifact is committed **alongside** the governance record so the
attestation travels with the act and keeps L0's git attribution as its base layer.

## The upgrade ladder (claim ≤ proof)
| Rung | What it gives | Owned? |
|---|---|---|
| **L0 — attributional record** | owner-authored decision/promotion/mint record; git author + owner line. Authentic *by convention*. | **Owned today** (the decision-record convention; git attribution). |
| **L1 — integrity seal (MVP)** | a **content-hash over the attested tuple** → tamper-evidence; `verify` becomes a real **recompute + compare** check (not a convention). | **Build-from-owned** (hash primitive owned; the canonicalize+seal+verify wiring is new). |
| **L2 — external signature (the moat)** | a signature binding **actor identity** to the sealed tuple + a published, third-party-runnable verification procedure (the auditor-accepted wall). | **Genuinely net-new** — name it honestly. |

- **MVP rung = L1.** Buildable now, owned-primitive-based, and the first rung that makes `verify` a
  *runnable check* rather than a *convention*. It is sufficient to unblock Mint L2 with a tamper-evident
  record.
- **Moat rung = L2.** The bet the strategy rests on; sequenced *after* the MVP; the genuinely net-new
  commitment. **intended-not-shipped.**

claim ≤ proof: only **L0 is owned-and-done**; **L1 is the buildable MVP**; **L2 is intended-not-shipped**.
Nothing here asserts the moat is built.

## How it gates Mint L2
Mint's L2 "signed decision-gate" stage calls `attest(mint-act)` (actor = mint + ratifying owner;
artifact-state = the minted authority spine it cast). **Until this capability's L1 MVP exists, Mint L2
stays BLOCKED** ([`../mint/SKILL.md`](../mint/SKILL.md) stage 3; Mint's own L0+L1 remain buildable). This
capability is Mint L2's new upstream dependency, by Decision 1. When L1 lands, update Mint's L2 block
reason from "gated on the attestation/signer capability" to "attestation capability available (L1)".

## The moat boundary — cite results, withhold mechanism
Per [2026-06-24 engine-moat decision](../../authority/decisions/2026-06-24-engine-moat-and-free-paid-boundary.md):
the **verification results are demonstrable** (show a passing `verify`, a tamper-detected `verify`, a
checked-in specimen attestation) but the **canon rule, hash construction, serialization, and L2
signing/identity scheme stay private** — same posture as the deterministic engine algorithm. The
[Kodamai lesson](../../../.arcanum/inventory/entries/kodamai-smithe-correctness-layer-synthesis.md),
applied: their corpus markets a "proof artifact" with **no runnable checker, no specimen, no named
proof system**. Our edge is the inverse — a **runnable `verify` + a checked-in specimen** —
demonstration over assertion.

## Provenance
Design package (this folder): [SPEC](./SPEC.md) (define) · [ARCHITECTURE](./ARCHITECTURE.md) (design)
· [HANDOFF](./HANDOFF.md). Authored by `invoke`, consumed by `sigil-development`. The contract is
[SKILL.md](./SKILL.md); the experiment harness is [development/HARNESS.md](./development/HARNESS.md).
Lifecycle owner: `sigil-development`. Next: `task-session` for the L1 integrity-seal MVP SWUs.
