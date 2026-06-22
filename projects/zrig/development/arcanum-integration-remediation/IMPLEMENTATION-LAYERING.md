# Implementation Layering: Z-Rig Remediation

Status: invoke plan support artifact
Purpose: define the smallest useful progression from private management artifacts to bounded engine remediation and later readiness review.

## Layer Overview

| Layer | Name | Goal | Outputs | Promotion Gate |
| --- | --- | --- | --- | --- |
| L0 | Private planning state | Make the evidence, authority map, and work-pack reviewable. | Invoke packet, authority inventory, observability obligations, split work-pack, optional Craft state. | No public/private boundary violations; selected SWU exists. |
| L1 | First engine proof | Close the F1 generic-gate gap for selected product waves. | W10/W11 fail-closed tests and implementation evidence. | Failed deploy/sentinel payloads no longer pass via generic gate. |
| L2 | Auditability and operator contracts | Fix residue fatality/deps, live identity, deploy/sentinel reachability, and command trust boundaries. | F3/F4/F5/F6/F7/F8 remediation evidence. | Dry-run/live/deploy/sentinel claims are separately validated. |
| L3 | Runtime authority readiness review | Resolve failover/accounting/spec drift/metrics and decide public-safe extraction policy. | F9-F14 evidence, readiness audit, promotion/no-promotion decision. | Public-safe extraction policy exists and product proofs are current. |

## L0: Private Planning State

Scope:

- This remediation package.
- `projects/zrig/architecture/PRODUCT-MODE-AUTHORITY-INVENTORY.md`.
- Design-only `OBSERVABILITY-OBLIGATIONS.md`.
- Scoped Craft management state if created by a later task.

Checks:

- `git diff --check projects/zrig/development/arcanum-integration-remediation projects/zrig/architecture`
- Review all new public-surface references; no Z-Rig product assumptions may be introduced into public Arcanum.

## L1: Gate Authority Proof

Selected first SWU: `SWU-ZRIG-F1-GATE-PROOF`.

Target write scope:

- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/gates.py`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/tests/test_pipeline.py` or a focused gate test file

Expected behavior:

- Missing/generic evaluators for spec-governed waves fail closed in product/live contexts, or specific evaluators exist.
- Failed W10 deploy payloads do not pass.
- Failed W11 sentinel payloads do not pass.
- The result remains explicit about what is tested and what is not product-mode proof.

## L2: Auditability And Operator Contracts

Target finding groups:

- F3 residue schema and fatality policy.
- F4 live identity trust boundary.
- F5 bridge contract docs.
- F6 deploy/sentinel reachability.
- F7 deploy command trust boundary.
- F8 runtime/test dependencies.

Expected behavior:

- Product/live modes cannot silently complete after audit residue failure unless an explicit degraded-assurance policy is documented and surfaced.
- Operator docs distinguish dry-run, live dispatch, deploy, sentinel, and validation commands.
- Verification dependencies are declared before live/test evidence is claimed.

## L3: Runtime Accounting And Promotion Readiness

Target finding groups:

- F9 shared wave failover cap.
- F10 clean-run policy/log alignment.
- F11 FULL-mode failure routing.
- F12 skipped wave accounting.
- F13 `AUTO` spec/code/docs reconciliation.
- F14 metrics status and trigger wiring.

Expected behavior:

- Accounting and routing surfaces are under trusted orchestrator authority.
- Metrics are either wired and validated or clearly marked non-product/prototype.
- A public-safe extraction decision can be made only after L1-L3 evidence exists.

## Cross-Layer Rules

- One execution SWU at a time.
- No public Arcanum promotion until readiness review passes.
- No product-mode trust claim from planning artifacts.
- Blocked dependency checks count as evidence of F8, not as successful F1/F3 completion.
- Craft rows may track blockers, decisions, gaps, and next moves, but not runtime proof.
