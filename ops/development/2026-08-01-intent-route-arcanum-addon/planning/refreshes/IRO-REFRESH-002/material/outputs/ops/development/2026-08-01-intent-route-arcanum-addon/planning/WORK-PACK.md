---
module: intent-route-arcanum-addon
version: candidate
status: runtime-admission-repair-applied; WPRA regeneration required before execution
updatedAt: 2026-08-01
docType: work-pack
---

# Work Pack: Intent Route Arcanum Add-on

## Control fields

| Field | Value |
|---|---|
| workPackGateStatus | `contract-repaired`; execution readiness is derived only from the current WPRA v2 receipt |
| complexity | high |
| outputMode | split |
| executionPackRef | `EXECUTION-PACK.md` |
| executionContractRef | `work-pack/shared/EXECUTION-CONTRACT.json` |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| designEvidenceState | `design-validator-pass` |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.md` |
| distillValidationStatus | pass |
| activeLayerWindow | L0 |
| selectedSWU | `SWU-IRO-001` |
| selectedOneShotStream | `IRO-FULL-STREAM` |
| implementationAuthorized | no |
| publicMutationAuthorized | no |
| goalAuthoringAuthorized | yes, by the direct 2026-08-01 operator request |
| executeNow | no; starting the native Goal is a separate runtime action |
| readinessProfile | `frozen-input-contractual-readiness` after a passing WPRA v2 receipt |

## Objective

Create a future public Arcanum intent-route sigil that returns bounded route
advice or visible ambiguity for any agentic runtime, generates equivalent
Claude/Codex packages through Bootstrap, and composes with Augmentor,
ResonantOS, the orchestrator, and private CAV2 without taking their authority.

## Source contracts

- [Define](../define/SPEC.md)
- [Architecture](../design/ARCHITECTURE.md)
- [Authority and trust](../design/AUTHORITY-TRUST.md)
- [Integration and versioning](../design/INTEGRATION-VERSIONING.md)
- [Validation contracts](../design/VALIDATION-CONTRACTS.md)
- [Design selection receipt](../design/DESIGN-SELECTION-RESULT.json)
- [Shared context](work-pack/shared/CONTEXT.md)
- [Traceability](work-pack/shared/TRACEABILITY.md)
- [Machine execution contract](work-pack/shared/EXECUTION-CONTRACT.json)
- [Closeout contract](work-pack/shared/CLOSEOUT-SYNC.md)

## Delivery map

| Task | SWUs | Layer/wave | Outcome | Status |
|---|---|---|---|---|
| [TASK-IRO-GATE-001](work-pack/tasks/TASK-IRO-GATE-001.md) | IRO-001 | L0/W0 | durable public-boundary and owner-binding decision | selected, not executed |
| [TASK-IRO-CANDIDATE-001](work-pack/tasks/TASK-IRO-CANDIDATE-001.md) | IRO-002, IRO-003 | L1/W1 | sanitized candidate sigil and portable witness | gated by IRO-001 plus explicit candidate-mutation approval |
| [TASK-IRO-CANONICAL-001](work-pack/tasks/TASK-IRO-CANONICAL-001.md) | IRO-004, IRO-005 | L2/W2 | canonical acceptance and Claude/Codex parity | gated by public-owner approval |
| [TASK-IRO-CONSUMER-001](work-pack/tasks/TASK-IRO-CONSUMER-001.md) | IRO-006, IRO-007, IRO-008 | L3/W3 | disposable install, ResonantOS refresh, orchestrator adapter | ordered in the one-shot stream; independently owner-gated |
| [TASK-IRO-PRIVATE-001](work-pack/tasks/TASK-IRO-PRIVATE-001.md) | IRO-009 | L4/W4 | private CAV2/ACI entry-boundary admission | gated by private-owner approval |
| [TASK-IRO-VERIFY](work-pack/tasks/TASK-IRO-VERIFY.md) | IRO-VERIFY | W5 | evidence and claim-ceiling closeout | final receipt-only unit |

## SWU manifest

The prose below defines outcomes. Exact commands, coordination outputs,
owner-material scopes, receipt contracts, budgets, successors, and pause gates
are canonical for execution in
[`EXECUTION-CONTRACT.json`](work-pack/shared/EXECUTION-CONTRACT.json).

| SWU | Behavior | Coordinator write scope | Dependencies | Done criteria | Owner route |
|---|---|---|---|---|---|
| SWU-IRO-001 | resolve public extraction/API/license and catalog/normalization/ACI/consumer owners | fixed IRO-FULL-STREAM epoch evidence only | Design pass | complete decision bundle plus terminal and joined closeout receipts | `decision-gate` then `invoke:refresh` |
| SWU-IRO-002 | author sanitized public-safe candidate closure | fixed unit terminal and closeout receipts; owner scope is separately bound | IRO-001 pass plus candidate approval | schemas/manifest/fixtures/instructions exist; private scans pass | `sigil-development` |
| SWU-IRO-003 | implement and witness pure core/JSON port | fixed unit terminal and closeout receipts; owner scope is separately bound | IRO-002 pass | frozen JSON/core, metamorphic, Node, and Chromium witnesses pass | `sigil-development` |
| SWU-IRO-004 | accept/promote canonical sigil | fixed unit terminal and closeout receipts; public worktree scope is separately bound | IRO-003 pass plus public approval | canonical acceptance receipt and public validation pass | public Arcanum owner via `sigil-development` |
| SWU-IRO-005 | generate and prove Claude/Codex parity | fixed unit terminal and closeout receipts; isolated roots are owner-resolved | IRO-004 pass | 15+15 parity and rollback pass | Bootstrap owner |
| SWU-IRO-006 | prove disposable consumer install | fixed unit terminal and closeout receipts; locator comes from IRO-001 | IRO-005 pass | install/check/disable/rollback and zero-product-effect evidence pass | add-on lifecycle owner |
| SWU-IRO-007 | refresh ResonantOS plan to consume generic disposition | fixed unit terminal and closeout receipts; exact adjacent worktree scope is owner-bound | IRO-006 pass | duplicate resolver ownership removed; product code unchanged | Invoke Refresh in ResonantOS worktree |
| SWU-IRO-008 | implement orchestrator thin adapter | fixed unit terminal and closeout receipts; orchestrator scope is owner-bound | IRO-007 pass plus catalog/normalization bindings | 27-case adapter matrix and zero-authority negatives pass | orchestrator owner Task Session |
| SWU-IRO-009 | admit private CAV2/ACI compatibility edge | fixed unit terminal and closeout receipts; private scope is owner-bound | IRO-008 pass plus ACI bindings | private conformance and boundary receipt pass | private CAV2 authority |
| SWU-IRO-VERIFY | audit all receipts and claim ceilings | fixed verification receipt only | IRO-009 pass | every lifecycle label is evidence-backed or downgraded | verification owner |

## Ordered one-shot stream

`IRO-FULL-STREAM` is the only full-work-pack stream. Its order is:

```text
IRO-001 -> IRO-002 -> IRO-003 -> IRO-004 -> IRO-005
        -> IRO-006 -> IRO-007 -> IRO-008 -> IRO-009 -> IRO-VERIFY
```

The stream preserves the full objective across turns but grants no ambient
authority. It pauses before IRO-002, IRO-004, IRO-006, IRO-007, IRO-008, and
IRO-009 for the exact owner receipt named by the execution contract. A pause
does not complete, skip, or auto-select the next unit.

## Gates

| Gate | Condition | On fail |
|---|---|---|
| G0 Design | fixed-point `design-validator-pass` | block Plan |
| G1 Decision | profile-bound extraction/API/license/owner decision bundle | block all mutation |
| G2 Candidate | explicit candidate-mutation approval plus scans/core/browser witness | repair candidate only |
| G3 Canonical | explicit public owner approval in a clean Arcanum worktree | no public/generated mutation |
| G4 Runtime parity | exact two-profile closure, disable, and rollback | block consumer install |
| G5 Consumer | isolated install and each consumer's owner receipt | block only that consumer unit |
| G6 Private | CAV2/ACI authority receipt and privacy boundary | block private admission |
| G7 Claim closeout | every claim cites exact witness and lifecycle state | downgrade or block claim |
| G8 Epoch | regenerate WPRA after any owner, material, validation, receipt, or closeout semantic change | invalidate prior epoch |

## Closeout sync

Every unit emits a schema-valid terminal receipt and a separately joined
closeout-owner receipt. Exact target inventories, baseline rules, delta
classes, validation commands, and successor semantics are in
[`CLOSEOUT-SYNC.md`](work-pack/shared/CLOSEOUT-SYNC.md). The coordinator writes
only the fixed evidence paths declared in the machine execution contract.

## Validation strategy

Use the exact future commands and case contracts frozen by the accepted
addendum. Add scoped JSON/schema/link/diff checks, forbidden-private scans,
dependency inspection, cross-profile bytes, isolated rollback hashes, and the
shared real Chromium runtime. No repository package root is added merely for
Playwright. Before Goal authoring, require:

```text
python3 planning/work-pack/shared/validate-execution-contract.py --root .
python3 arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py \
  --config <audit-config-v2.json> --output-dir <new-output-directory>
```

## Handoff

- Selected unit: `SWU-IRO-001`.
- Selected full stream: `IRO-FULL-STREAM`.
- Execute now: no; Goal authoring is authorized, execution is not implied.
- First runtime capability: `decision-gate` using
  `.arcanum/profiles/decision-profile.yml`.
- Next implementation owner after a passing IRO-001 closeout and explicit
  candidate approval: `sigil-development`.
- WPRA evidence ceiling: contractual readiness only; it selects and executes
  nothing and grants no mutation, promotion, publication, or deployment authority.

## Runtime admission repair

The prior WPRA epoch omitted Task Session support outputs and is superseded. `RUNTIME-EVIDENCE.md` and execution-contract v1.1 bind the complete per-unit and outer-chain evidence paths. A new strict Context/WPRA epoch is mandatory before Goal activation evidence is written.
