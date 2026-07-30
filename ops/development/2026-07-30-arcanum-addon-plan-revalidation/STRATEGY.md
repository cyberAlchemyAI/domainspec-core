# Arcanum Add-on Plan Revalidation Strategy

## P1 Trigger

Dispatch is required by parallelism and isolation. `B-DESIGN-001` can close
only if two fresh judgments independently verify the parent-reconciled current
bytes; combining them before return would erase the disagreement evidence the
gate needs.

## Lanes And Subagents

One group contains two read-only agents that run in parallel over the same
complete corpus:

| Lane | Pooled identity | Role | Anti-bias angle | Expected output |
| --- | --- | --- | --- | --- |
| Proposer | Artin, Emil | explorer | formal closure proof over every previous finding, owner boundary, dependency, SWU, and first-unit obligation | current-byte receipt with prior-finding closure matrix and PASS/BLOCK |
| Balancer | Capucci, Matteo | explorer | adversarial failure falsification across authority, Bootstrap, state, lifecycle, evidence, and browser-gate bypass | current-byte receipt with failure traces and PASS/BLOCK |

The anti-bias axis is methodology: formal closure proof versus adversarial
failure falsification. Fresh identities avoid asking the first review’s agents
to validate their own accepted objections.

## Dependency Flow

The lanes are independent and have no feedback edge. After exact confirmation,
the parent will:

1. register one schema-0.8.0 dispatch row;
2. spawn both agents once in one parallel wave;
3. join and close both;
4. preserve their raw receipts and assemble `attacks.md` and `findings.md`;
5. accept `B-DESIGN-001` closure only if both validations pass over the bound
   corpus digest; and
6. append exactly one close row.

The route does not reconcile target planning files, select an SWU, implement
the add-on, or run a browser.

## Inventory Preflight

- Owner machine index: ready; 259 entries; projection conformance pass.
- Warnings: 117 uncontrolled historical tags, non-blocking.
- Target machine index: unavailable.
- Selected:
  - prior Arcanum add-on Invoke Distill review result;
  - accepted Arcanum/ResonantOS add-on research result;
  - Invoke Distill evidence-enforcement review.
- Excluded:
  - the prior strategy sheet as stale for the current changed-byte digest;
  - broader Augmentor architecture;
  - unrelated product review strategies.
- Design consequence: use fresh pooled identities, bind the complete literal
  corpus digest, regression-test every prior finding, and refuse authored
  labels or Inventory summaries as proof.
- Authority ceiling: Inventory is discovery only.

Machine packet:
`strategy-inventory-packet.json`.

## Bound Corpus

- Product worktree:
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha-arcanum-addon-plan`
- `HEAD` and `origin/dev`:
  `80dcd79677ad73b21dbaded12e0e9cd47aace82b`
- Define digest:
  `dadac41fc6f10fe006da6307cb5b9b77168efd753a19ddcf1771aaf6e9cca375`
- Design digest:
  `5aeb5b65c11a81aa6d5413c308888e45d186af0626b95e2708c1241023a2a15b`
- Plan digest:
  `8a5dfe41cf3854f566712d2c29268528106b574612e0449b43f1698b76a2caef`
- Aggregate corpus digest:
  `bb0a6f31cf1142902693d30c53ecc2ee08b6747e14ea12f7dff5b81d08d64b14`

## Gate And Ledger State

- Decision Gate: `OPT-REVALIDATE` selected.
- Dispatch type: live `review`.
- DomainSpec form: schema `0.8.0`.
- Candidate sheet: `DISPATCH-SHEET.json`.
- Dispatch Spec route: `DISPATCH-ROUTE.json`.
- Confirmation-readiness: pass at sheet SHA-256
  `cc655251c83bb1fba988921680870be78bcad5644fc43c77729aafa286905646`.
- Dispatch Spec admission validation: pass; admitted route SHA-256
  `080a851e12cd1437c73d62994ca79088251561e8177f8d8201e32b122fe05451`.
- Check-tension: PASS/PASS with distinct handles recorded in
  `CHECK-TENSION.md`.
- Human confirmation: accepted at the exact admitted sheet digest.
- Registration: appended once.
- Review execution: complete; both fresh agents spawned once, joined, and
  closed.
- Native gate: `gate_block`; both receipts returned `validation: block`.
- Result: all six prior findings closed, but two new MAJOR findings survive;
  `B-DESIGN-001` remains open.
- Closeout: appended once with `exit_reason=resolved`; the review deliverable
  is the blocking finding set, not a passing validation.
- Closeout route SHA-256:
  `4f920b9899129e8b104e9d906de9fe8870fe70c321d26db4e175852e9cba6745`.
- Closeout Dispatch Spec verdict: expected `block`, sourced only from the
  blocking lifecycle and two blocking native stage receipts.

## Claim Ceiling

Even a double-PASS revalidation can close only `B-DESIGN-001`. Governance,
Bootstrap compatibility, owner binding, native adapter, retention, SWU
selection, implementation, browser evidence, readiness, promotion, deployment,
and release remain independent.

## Next Owner Action

Repair the per-SWU/wave dependency topology in the implementation dispatch and
split the lifecycle validator's enabled-degradation binding from the shared
disabled uninstall/rollback binding. Preserve `selectedSWU: none`, then route a
new exact-byte independent revalidation.
