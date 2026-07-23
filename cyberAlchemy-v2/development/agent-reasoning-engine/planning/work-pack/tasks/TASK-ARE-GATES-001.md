# TASK-ARE-GATES-001 — entry, policy, and exact-effect control

Layer: L1/L2. SWU-012/013/015 depend on G-ARE-L0; SWU-014 depends on G-ARE-L1
and named owner records. Status: planned.

## SWU-ARE-012 — entry gate adapter

- Execution owner recommendation: `subagent`.
- Inputs: frame, verified snapshot/manifest, bounded run envelope, complete D37
  decision from the owner-controlled gate port.
- Outputs: persisted entry decision and either closed-zero-calls or admitted run
  handle.
- Dependencies: SWU-ARE-010/011, G-ARE-L0, and the owner-controlled entry
  decision fixture/port.
- Future write scope: `cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/entry-gate-adapter/**` and fixtures.

Algorithm: validate subject/digests; persist full decision; on block/defer close;
on flag persist residue and pause; accept only a new explicit pass; increment
call-capability only after pass. Crash before durable pass remains zero-call.

Done when block/defer/flag/crash/mismatch/pass fixtures prove persisted order and
zero actor/evaluator/effect calls for every non-pass.

Verification: `node --test cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/entry-gate-adapter/test/*.test.mjs`.

Handoff context: this task, SWU-ARE-010/011 receipts, G-ARE-L0 receipt, entry
decision owner contract, and only SWU-ARE-012. Return the result shape in
[`../../EXECUTION-PACK.md`](../../EXECUTION-PACK.md).

## SWU-ARE-013 — effort controller

- Execution owner recommendation: `subagent`.
- Inputs: owned risk/effect/uncertainty facts, verified manifest-required
  candidate obligations, policy version.
- Outputs: `EffortProfile`; no technique plan, applicability, or outcome.
- Dependencies: SWU-ARE-011 and a passed SWU-ARE-012 entry handle.
- Future write scope: `cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/effort-controller/**` and fixtures.

Algorithm: apply hard protected/irreversible/authority-impact overrides; treat
unknown as non-low; select minimum satisfying tier; attach required roles,
budgets, stops, and escalations. Removing evidence/lanes cannot lower tier or
improve result.

Done when T0-T4 table, unknown, monotonicity, consensus-invariance, missing
owner, and protected-action fixtures pass.

Verification: `node --test cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/effort-controller/test/*.test.mjs`.

Split analysis: effort tiering has an independently reviewable monotonic policy
contract. Actual catalog technique selection is therefore SWU-ARE-015.

Handoff context: this task, SWU-ARE-011/012 receipts, owned effort policy, and
only SWU-ARE-013. Return the result shape in
[`../../EXECUTION-PACK.md`](../../EXECUTION-PACK.md).

## SWU-ARE-015 — technique selector

- Execution owner recommendation: `subagent`.
- Inputs: verified manifest-required candidate obligations, `EffortProfile`,
  Technique Catalog versions and activation rules.
- Outputs: operational `TechniquePlan`; no final applicability or outcome.
- Dependencies: SWU-ARE-011/013.
- Future write scope: `cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/technique-selector/**` and fixtures.

Algorithm: enumerate required candidate-obligation checks; resolve allowlisted
technique IDs/versions; evaluate activation triggers; add required roles,
artifacts, stops, and evidence expectations; reject unknown or decorative
selection; preserve skipped-reason residue. Never convert selection into
applicability, evidence, or authority.

Done when known/unknown catalog, activation, missing required technique,
decorative selection, skipped-reason, and unchanged-applicability fixtures pass.

Verification: `node --test cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/technique-selector/test/*.test.mjs`.

Handoff context: this task, SWU-ARE-011/013 receipts, current Technique Catalog
contract, and only SWU-ARE-015. Return the result shape in
[`../../EXECUTION-PACK.md`](../../EXECUTION-PACK.md).

## SWU-ARE-014 — exact-effect gate adapter

- Execution owner recommendation: `subagent`.
- Inputs: `RecommendedUnderSnapshot`, persisted receipt digest, current authority
  snapshot, owner-controlled full D37 decision, identical fixed effect envelope,
  idempotency key.
- Outputs: closed-zero-effect or one test-double dispatch eligibility record.
- Dependencies: SWU-ARE-006, G-ARE-L1, and BLK-ARE-EFFECT-001 closure.
- Future write scope: `cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/effect-gate-adapter/**` and fixtures; no real adapter.

Algorithm: reject non-positive outcome; compare every action/target/scope/
authority/receipt/envelope digest; persist full decision after receipt; non-pass
closes zero-effect; pass emits one idempotent test-double eligibility handle.

Done when mismatch, stale authority, every non-pass, non-positive outcome,
crash-order, and repeat-delivery fixtures prove zero or one logical attempt.

Verification: `node --test cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/effect-gate-adapter/test/*.test.mjs`.

Handoff context: this task, G-ARE-L1 and SWU-ARE-006 receipts, exact-effect
owner contract, and only SWU-ARE-014. Return the result shape in
[`../../EXECUTION-PACK.md`](../../EXECUTION-PACK.md).

Split analysis: entry admission, effort derivation, technique selection, and
exact-effect authorization have distinct subjects and independently reviewable
acceptance; combining them would collapse authority boundaries.
