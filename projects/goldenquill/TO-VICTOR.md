# TO-VICTOR — QA / Measurement / Epistemics

**Role:** Guardrails-as-tests, internal deployment test, claims register, canonical demo standard, instrumentation, Day-60 evidence.
**Source:** [docs/strategy/development/node-on-desk-readiness/DISPATCH-VALIDATION.md](docs/strategy/development/node-on-desk-readiness/DISPATCH-VALIDATION.md) · workbook role map [docs/golden-quill-task-role-breakdown-handoff.md](docs/golden-quill-task-role-breakdown-handoff.md)

All three core gaps are **refine-solvable and specced** — start now. Spec: [docs/features/quality-security-proof/BUILD-SPEC.md](docs/features/quality-security-proof/BUILD-SPEC.md).

## Agent execution contract — run this first

When Victor asks an agent to "read the artifacts" or start QA/measurement work,
the agent should use this file as the quality interface over the Craft nodes.

1. Read `pipeline/SESSION_BOOTSTRAP.md` for project orientation.
2. Read this handoff and linked artifacts by path.
3. Run `$craft state` for the Victor-facing ledgers below.
4. Use `$interrogation` for Victor-owned proof choices: test matrix shape,
   claims-register evidence categories, metric field names, or Day-60 evidence
   definitions. Ask one question at a time.
5. Do not invent security-review assignment, legal posture, or sales claims.
   Route owner decisions to `TO-JOSH.md` and keep claims unshippable until
   evidence exists.
6. After each answer or validation run, update the owning Craft ledger with the
   receipt, remaining residue, and next move.
7. Return a `Craft Result` plus the validation command used. Use
   `scripts/run_tests.sh` or `.venv/bin/python3 -m pytest`, not system
   `python3 -m pytest`.

### Victor-facing Craft scope

| Scope | Ledger | Victor interface |
| --- | --- | --- |
| quality/security/proof | `docs/features/quality-security-proof/.craft/ledger.yml` | Guardrail matrix, security-review scope, claims register, instrumentation. |
| white-glove Day 60 | `docs/strategy/development/white-glove-delivery-node-care/.craft/ledger.yml` | Day-60 metric definitions are supplied by QSP instrumentation. |
| company ops validation | `docs/strategy/development/company-operations-finance/.craft/ledger.yml` | Validation packet consumes QSP claims and instrumentation. |
| node readiness | `docs/strategy/development/node-on-desk-readiness/.craft/ledger.yml` | Proof gates feed parent RG-5 and downstream readiness. |

### Interrogation interface for Victor

Use `$interrogation` when proof language needs one exact choice, for example:

```text
$interrogation docs/features/quality-security-proof --mode measurement-proof
```

Good Victor questions ask for one measurable contract: a closed-set evidence
category, a metric field name, a fixture class, a fail-closed expectation, or a
review status value. Each answer should update the claims register,
instrumentation definitions, test matrix, or Craft ledger evidence.

## Build now (specs ready)

1. **Guardrails-as-tests matrix** — `GAP-QSP-TEST-PLAN` (block) → §1
   Cross-walk every gate to an acceptance test that asserts **fail-closed** behavior: all **16 F-CLASS-*** + **12 F-WPFA-*** codes + the **Five Laws**, across four axes (posture / classification / audit / fail-closed-META). Build `guardrail-test-matrix.yaml` + synthetic fixtures, wire to `scripts/run_tests.sh`. The matrix file is itself checked by `T-QSP-COV-01` (the `F-CLASS-COVERAGE-INCOMPLETE` analog).
   **Interpreter:** use `scripts/run_tests.sh` / `.venv` (Python 3.14) — system python3 (3.9) cannot collect the suite.

2. **Claims register** — `GAP-QSP-CLAIMS-REGISTER` (flag) → §2
   Schema maps every external/customer claim → evidence category (8-category closed set, on the WPFA claim→coefficient→cycle_id→trace_id model). Seed `claims-register.yaml`, resolve evidence handles, flag `sales_touch` claims and route them to Josh. **You must expose the register handles** that sales-contracting-legal and the company-ops validation packet consume.

3. **Instrumentation definitions** — `GAP-QSP-INSTRUMENTATION` (flag) → §3
   Author `instrument-definitions.yaml` for support hrs/node, usage baselines, renewal-intent capture — field names sourced from the §17 WPFA CycleReceipt; A12 Decimal / int-micro-watt-hour discipline (no float). **You must expose the field names** that the company-ops validation packet and white-glove Day-60 consume.

## Shared / downstream
- **GAP-WGD-DAY60** (white-glove) — the Day-60 template structure is authored at [docs/strategy/development/white-glove-delivery-node-care/BUILD-SPEC.md](docs/strategy/development/white-glove-delivery-node-care/BUILD-SPEC.md), but **its metric definitions are blocked on your instrumentation (#3 above)**. Supply the definitions and the template fills.
- **GAP-COF-VALIDATION-PACKET** (with Josh) — the packet at [docs/strategy/development/company-operations-finance/BUILD-SPEC.md](docs/strategy/development/company-operations-finance/BUILD-SPEC.md) consumes your claims register + instrumentation. Coordinate-ownership, no merge.

## Waiting on Josh (does not block your authoring)
- **GAP-QSP-SECURITY-REVIEWER** — an independent security reviewer is onboard-now but **unassigned**. Until Josh assigns one, security-review-backed claims stay `draft`/unshippable — but §1–§3 authoring proceeds now.
