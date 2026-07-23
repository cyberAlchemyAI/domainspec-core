# TASK-WFE-007 — Bind Dispatch Evidence And Runtime Overlays

- Change: DSS-2 / WFE-R06
- Layer/slice/wave: L1 / S1 / W1
- Lifecycle owner: private DomainSpec tooling plus `sigil-development`
- Status: complete; SWU-WFE-007A and SWU-WFE-007B passed

## Objective

Prove that the registered dispatch is the same sheet that passed two tension
checks and received human confirmation, then make owner/runtime differences
declared rather than accidental.

## Sources

- owner `domainspec-subagents-strategy/SKILL.md`: double tension, explicit
  confirmation, frozen sheet, private adapter boundary
- current registration row/appender schema
- installed `.claude` and `.agents` strategy surfaces and their provenance
- accepted findings DSS-2

## SWU-WFE-007A — Sheet evidence binding

- Dependency: SWU-WFE-001 pass.
- Primary behavior: registration verifies two tension verdicts and explicit
  confirmation against the exact sheet digest.
- Acceptance boundary: one verdict, failing verdict, absent confirmation, or
  post-confirmation sheet mutation rejects; two pass verdicts plus matching
  confirmation admits.
- Split analysis: verdict pair, digest, and confirmation are one evidence-binding
  invariant; partial persistence cannot prove the sheet.

Design the smallest schema extension that records evidence handles and digest;
do not embed full chat returns. Schema/version changes must be explicit and old
rows remain readable.

## SWU-WFE-007B — Classified runtime composition

- Dependency: 007A pass.
- Primary behavior: each owner/runtime difference is classified as canonical
  contract, allowed runtime metadata/formatting, or declared local overlay.
- Acceptance boundary: undeclared removal/addition of lifecycle, owner,
  research-output, or public/private rules fails; formatting metadata and
  declared overlay pass.
- Split analysis: classification and parity validation produce one semantic
  equivalence verdict.

## Scope and validation

- Owner/private canonical and appender schema/tests under
  `implementation/domainspec/internal_tools/subagents-dispatch-hooks/`.
- Generated strategy runtimes only through their declared generation/adaptation
  mechanism.
- Forbidden: another human gate, byte-identity as semantic proof, public core
  importing private adapter prose.

```bash
node implementation/domainspec/internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs
git diff --check -- implementation/domainspec/internal_tools/subagents-dispatch-hooks .agents/skills/domainspec-subagents-strategy .claude/skills/domainspec-subagents-strategy
```

- Execution owner: private tooling + `sigil-development`.
- Receipt: schema/version decision, substitution fixtures, classified diff,
  parity result, no second confirmation.

## Done

Registration is bound to the reviewed sheet, legitimate runtime differences are
declared, and semantic drift fails without overwriting local behavior blindly.
