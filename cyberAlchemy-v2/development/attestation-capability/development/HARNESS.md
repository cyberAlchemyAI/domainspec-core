# Attestation / Signer — experiment harness (scaffold)

**Status:** scaffold (no examples run yet — the capability is not implemented). Owner:
`sigil-development` + `experiment-harness`. INTERNAL; promotes nothing; intended-not-shipped.

## Falsification target (the gate the capability must pass) — the discriminating verify
The whole capability stands or falls on one **falsification-style self-test**: a `verify` that
*distinguishes* an untampered state from a mutated one. It is a real pass/fail, not a self-confirming
demo. For a fixture `x`:

- **positive arm:** `verify(attest(x), x) = valid`
- **negative control:** `verify(attest(x), tampered(x)) = tampered`

**FALSIFIED if either arm fails** — i.e. if `verify` returns `tampered` on the untampered state (a false
alarm), or returns `valid` on the mutated state (a **vacuous verifier** — the load-bearing failure). A
`verify` that always returns `valid` passes the positive arm but FAILS the negative control: that is
exactly the assertion-without-checker posture the
[Kodamai synthesis](../../../../.arcanum/inventory/entries/kodamai-smithe-correctness-layer-synthesis.md)
flags. **Both arms must hold for the same fixture under the same `canon_version`.** This harness exists
to produce that pass/fail table.

Soundness statement under test (the pin, inherited from the owned kernel —
[`AgentPermissionKernel.lean`](../../../../domainspec-lean-formalization/lean-engineer/AgentPermissionKernel.lean)'s
`decidePolicy_allow_iff` / `decidePolicy_sound`): `verify = valid ⇒ claimed state is byte-for-byte the
attested state` (no false `valid`).

## Fixtures / controls
- **Golden (positive) fixture = a real cav2 decision record.** Use a stable committed record, e.g.
  [`authority/decisions/2026-06-24-saturn-domainspec-public-disclosure.md`](../../../authority/decisions/2026-06-24-saturn-domainspec-public-disclosure.md)
  (a real owner-ratified governance act; not the in-flux mint decision, not the negative-control
  resonantos record). `attest` seals it; `verify` on the unmodified bytes must return **`valid`**.
- **Negative control = a one-byte-mutated copy of that same record.** A single deliberate edit (flip one
  character in the ratified content). `verify` on the mutated copy must return **`tampered`**. This is the
  control that proves the verifier is not vacuous — without it, `valid` means nothing.
- **L2 controls (deferred):** `bad-signature` (valid seal, wrong/absent actor signature) and
  `unknown-actor` (signature by an unpublished identity) — authored only when the L2 actor-identity model
  is decided. Out of scope for the L1 MVP run.

## Example regimes (to author at implementation — low / medium / complex)
| regime | fixture | tests |
|---|---|---|
| **low** | the golden decision record above | the two-arm discriminating self-test: `verify(attest(x),x)=valid` AND `verify(attest(x),tampered(x))=tampered` (smallest real pass/fail) |
| **medium** | a **promotion** act (a candidate crossing a gate, kind=promotion) | same two arms on a different act-kind; canonicalization stable across record shapes; `canon_version` agreement between attest and verify |
| **complex** | a **mint act** (kind=mint; artifact-state = a minted authority spine, the Mint-L2 consumer) | the two arms on the mint-act fixture; whitespace/field-order mutations the canon rule must catch; confirms `attest(mint-act)` is the shape Mint L2 consumes |

Per `experiment-harness`: require **real output bodies** (an actual attestation artifact + actual verdict
output), not save-summaries. A demo that only shows the positive arm is **not** a pass — the negative
control is mandatory. Codex runs explicit via `development/run-example-with-codex.sh` (to be created at
implementation).

## Blocks carried into the harness
- **L2 (external signature) — intended-not-shipped.** The `bad-signature` / `unknown-actor` arms wait on
  the L2 actor-identity model decision ([HANDOFF open questions](../HANDOFF.md)). The L1 MVP run covers
  `valid` / `tampered` only.
- **Mechanism stays withheld.** The harness demonstrates *results* (artifact, verdicts, the two-arm
  table); it must not document the canon rule internals, hash construction, or serialization in any
  promotable/public surface.

## Promotion-readiness gate (not yet met)
This capability may be proposed for promotion (out of `development/`) only after: the **discriminating
self-test passes both arms** on the L1 fixtures (specimen demonstrable); the **L2 actor-identity model**
is decided and the L2 rung is built (the moat); and the boundary scrub confirms no mechanism leak. Until
then: INTERNAL, intended-not-shipped, in-development. Note: this gate also unblocks **Mint L2** once L1
is demonstrable.
