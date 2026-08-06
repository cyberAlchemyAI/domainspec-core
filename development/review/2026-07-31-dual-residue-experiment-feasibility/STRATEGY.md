# Dual-Residue Experiment Feasibility Review Strategy

Status: completed and audit-accepted for the frozen digest.

## P1 trigger

Dispatch is required. The question needs synthesis across at least three independent lenses, benefits from parallel attack, and needs independent verification before a feasibility conclusion can be trusted.

## Lanes and subagents

- `attackers` runs in parallel and robot-talks across the `methodology` axis:
  - Abramsky: formal protocol fidelity and claim/gate logic.
  - Saxe: executable mechanics, statistics, runtime assumptions, and test receipts.
  - Ashby: ownership, lifecycle, canonical/mirror drift, and DomainSpec context fit.
- `synthesizer` waits for all attacker initial and final positions:
  - Shannon writes only `attacks.md` and `findings.md` in this folder.
- `verifiers` runs in parallel with bounded zig-zag over the `attack-vector` axis:
  - Popper tries to refute findings with executable counter-examples.
  - Russell tries to refute findings through definitional and authority-boundary errors.
- `auditor` waits for verifier convergence:
  - Brandenburg is the dedicated final approver and performs no working role.

## Dependency flow

`attackers -> synthesizer <-> verifiers -> auditor`, with one conditional `auditor -> synthesizer` feedback edge. Later waves cannot start until the owner-typed gate for the exact upstream receipts returns ready.

## Inventory consequence

The owner Inventory validates as ready and contains two relevant boundaries: schema/instance residue is a two-budget design principle, and dual-residue model training remains a proposed empirical witness rather than an implemented/validated DomainSpec capability. The target has no Inventory package, so current code, protocol, results, and prior review bytes must be checked directly. This makes the formal lane separate motivation from measured advantage, the mechanics lane test current emissions, and the ownership lane enforce the adjacent-repository evidence ceiling.

## Gate and ledger state

- Sheet schema: `0.8.0`.
- Confirmation readiness: `PASS`, schema `0.8.0`, SHA-256 `a0218865ca67aa800df9f182269f527bf4e5ec2f08e8a91eb9ff407303acfad7`, ledger mutation `none`.
- Dispatch Spec: `PASS`; capability-bound route executed under explicit authorization.
- Check-tension: checker `PASS` and independent reviewer `PASS` on the same digest; no phase-2 comparison required.
- Human confirmation: recorded as `chat-confirmation-2026-07-31-a0218865` for the exact digest.
- Registration: appended exactly once for `2026-07-31-dual-residue-experiment-feasibility-review`.
- Runtime: all seven agents joined and closed; one verifier/synthesizer zig-zag repaired citation and definition precision.
- Audit: `ACCEPT`; Orchestrate terminal state `complete`.
- Closeout: exactly one dispatch append and one `resolved` close append.

## Result

The accepted review returns per-artifact KEEP/FIX decisions, five CRITICAL findings, dependency-ordered change requests, and the bounded conclusion `NOT-YET-FEASIBLE`. The repository remains architecturally fit as a candidate-local evidence harness. No fixes were applied to the target.

## Next owner action

Select and freeze one claim/comparator/verdict contract before implementation. Then admit a separate bounded repair work pack; do not treat this review as implementation authority or empirical validation.
