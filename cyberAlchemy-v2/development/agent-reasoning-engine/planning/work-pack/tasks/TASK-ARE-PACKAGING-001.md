# TASK-ARE-PACKAGING-001 — private packaging and rollout

Layer: L3. Status: deferred until G-ARE-L2.

## SWU-ARE-008 — versioned private interface

- Execution owner recommendation: `subagent`.
- Inputs: terminal L2 package APIs/receipts and private interface decision.
- Outputs: versioned private library/CLI/API adapter and compatibility receipt.
- Dependencies: G-ARE-L2 and BLK-ARE-ROLLOUT-001 interface scope.
- Write scope: `cyberAlchemy-v2/implementation/agent-reasoning-engine/interfaces/private/**`.

Algorithm: map versioned request to existing components; preserve typed outcomes,
digests, full gate records, and non-authority metadata; reject unknown versions,
missing authorization, and envelope mismatch; expose no real effect unless a
separate protected-action plan later supplies it.

Done when compatibility, invalid-version, authorization, privacy, and zero-
effect contract tests pass. Verification: `node --test cyberAlchemy-v2/implementation/agent-reasoning-engine/interfaces/private/test/*.test.mjs`.

## SWU-ARE-009 — operational readiness

- Execution owner recommendation: `subagent`; rollout itself remains a separate
  `manual` owner gate.
- Inputs: versioned private interface, expected load/failure/security envelope,
  observability and rollback policy.
- Outputs: load/security/privacy results, runbooks, staged rollout proposal, and
  owner decision.
- Dependencies: SWU-ARE-008 and BLK-ARE-ROLLOUT-001.
- Write scope: `cyberAlchemy-v2/implementation/agent-reasoning-engine/operations/**`.

Algorithm: run bounded load matrix; inject allowed failures; verify resource and
privacy ceilings; check trace/redaction; rehearse rollback; stage canary; require
manual owner verdict. No test count or throughput admits a broader capability.

Done when load, failure, secret/privacy, observability, rollback, and owner-gate
evidence passes. Verification commands are pinned with the future deployment
profile before this SWU is selected; minimum command:
`node --test cyberAlchemy-v2/implementation/agent-reasoning-engine/operations/test/*.test.mjs`.

Future write scope is selected only after L2. Public Arcanum, general engine
promotion, and real effect enablement are separate owner routes.

Split rationale: a versioned compatibility contract and operational rollout
evidence have independently reviewable acceptance and may not be bundled.
Handoff
context is this task, terminal L2 receipts, private rollout decision, and one
selected SWU. Return the result shape in
[`../../EXECUTION-PACK.md`](../../EXECUTION-PACK.md).
