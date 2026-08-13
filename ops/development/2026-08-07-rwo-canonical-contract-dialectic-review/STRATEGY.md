# RWO canonical-contract dual-lane review strategy

## P1 trigger decision

Dispatch is warranted by parallelism and isolation. The contract crosses two
distinct concerns—formal cross-language byte conformance and domain/lifecycle
ownership—and an answer that mixes them in one pass is likely either to miss byte
counterexamples or to mistake serialization determinism for semantic sufficiency.

## Central question and assumptions to challenge

Central question: does `DG-RWO-LANG-CONTRACT-001`, specifically
`RWO-JCS-SAFEINT-V1`, need refinement before an owner can safely accept it as the
language-neutral contract for independent Python, Rust, and Go implementations?

Assumptions under challenge:

1. RFC 8785 plus a safe-integer and NFC profile is sufficient to produce the
   same meaningful bytes in all three languages.
2. The current rules for unknown fields, versions, semantic ordering, hashing,
   and golden-vector maintenance are precise enough to implement independently.
3. A JSON-based canonical identity can remain separate from protobuf/gRPC,
   journal/event identity, retry, ARE, runtime, authority, and promotion owners.

## Lanes and subagents

Both agents attack the full corpus read-only and run in parallel, then confront
the other lane's return once through `robot_talks` before finalizing positions.

1. `formal-interop-reviewer` — **Spitters, Bas** — formal methodology. Owns
   byte-level, schema, Unicode, numeric, hashing, fixture, and cross-language
   counterexamples.
2. `domain-lifecycle-reviewer` — **Hewitt, Carl** — adversarial methodology.
   Owns semantic identity, type/domain separation, evolution, duplicate/event
   identity, and transport/runtime ownership counterexamples.

Anti-bias axis: `methodology (formal vs adversarial)`. The single unordered pair
has one digest-owned predicted disagreement in `dispatch-sheet.json`.

## Strategy check

Alternative considered: three language-specific lanes for Python, Rust, and Go.
Rejected because each would repeat the same standard interpretation, while the
real tension is cross-language formal reproducibility versus domain/lifecycle
sufficiency. Language-specific probes belong after the contract is frozen as
conformance fixtures, not before as independent semantic owners.

## Dependency flow

The two lanes start independently in one parallel group. After both initial
returns are frozen, the parent gives each agent the other's findings for one
bounded confrontation and collects final positions. The parent joins both,
verifies citations/counterexamples, persists `attacks.md`, synthesizes only
surviving findings into `findings.md`, and remains final approver. No contract
change follows automatically; the user receives a separate human gate over each
proposed refinement.

## Inventory preflight

- Root Inventory: lookup-ready, 301 entries, 146 uncontrolled-tag warnings.
- Target Inventory: machine index exists but lookup readiness is blocked by
  source-coverage failure and contains zero entries.
- Selected: accepted RWO current-state result and adjacent browser-neutral digest
  strategy.
- Excluded: superseded RWO strategy entry and generic ontology/promotion entries.
- Design consequence: the formal lane must demand cross-runtime evidence; the
  adversarial lane must preserve the thin kernel and owner non-collapse. Neither
  may treat Inventory as proof.

See `strategy-inventory-packet.json` for selectors, sources, exclusions, and
residue.

## Gate and ledger state

- Live review type: `review`.
- Form owner: `register-dispatch` schema `0.8.0`.
- Confirmation-readiness: `PASS`, schema `0.8.0`, sheet digest
  `18265e44d863102df8491918f445d8271629d202a89d91c4c5471c828cb9b9b2`,
  ledger mutation `none`.
- Dispatch Spec: `PASS` for `DISPATCH-ROUTE.json`.
- Check-tension: `PASS/PASS` from two independent agents on the admitted sheet
  digest; see `CHECK-TENSION.md`.
- Human confirmation: required after both validations pass.
- Registration: not run; ledger mutation forbidden before confirmation.
- Execution: not run; no review agent has spawned.
- Post-result Inventory hook: candidate query preserved, but index synchronization
  blocked before write because the updater's isolated candidate staging cannot
  resolve existing repository-external source references; both real indexes remain
  byte-identical. See `receipts/inventory-strategy-result-dry-run.json`.
- Closeout expectation: exactly one registration row and one close row, with all
  agents joined and closed.

## Outputs and claim ceiling

- `attacks.md`: verbatim initial and final lane positions.
- `findings.md`: cited surviving change requests, severity, KEEP/FIX verdicts,
  counterexamples, and explicit no-change conclusions.
- `claude/current_conversations/2026-08-07-rwo-canonical-contract-dialectic-review.md`:
  Robot-Talks session preservation.

The review may recommend refining or keeping the contract. It cannot select the
owner option, edit the contract, unblock Invoke Refresh, implement fixtures,
mutate ontology or product code, register authority, promote, publish, deploy, or
release anything.

## Next human action

Reply `confirmed` to authorize registration and the exact two-agent read-only
run, or request a strategy revision. Any dispatch-sheet byte change requires
fresh form validation and two fresh independent tension verdicts; a material
strategy change also requires fresh human confirmation.
