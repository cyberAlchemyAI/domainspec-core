# Most-Used Skills Efficiency Review

- Dispatch: `2026-07-22-most-used-skills-efficiency-review`
- Scope: `task-session`, `invoke`, `domainspec-subagents-strategy`, `decision-gate`, `inventory`, and `whisper`
- Review status: **ACCEPT**
- Mutation status: review artifacts only; no audited skill was changed
- Final approver: parent, after adversarial verification

## What the counts mean

The ranking uses valid signal-ledger rows with a string `sigil` field. A use is not a failure, and a workflow-gap item is not automatically a failed execution.

| Skill | Observed uses | Gap items | Qualification |
|---|---:|---:|---|
| Task Session | 113 | 21 | highest observed use |
| Invoke | 55 | 16 | six older Invoke rows omit `sigil` and remain telemetry residue |
| DomainSpec Subagents Strategy | 40 | 30 | high gap count is a review lead, not a failure rate |
| Decision Gate | 38 | 3 | gate misuse matters more than aggregate count |
| Inventory | 14 | 9 | current machine index was checked directly |
| Whisper | 14 | 16 | generated-runtime drift was checked directly |

## Verified change requests

| # | file | evidence | severity | proposed fix |
|---:|---|---|---|---|
| 1 | `arcanum/arcana/task-session/SKILL.md` | `--auto` accepts a recommendation judged “clearly safe”; failed or unavailable validation can become `FLAG` without an acceptance-critical distinction | High | Delete the subjective safe-recommendation escape. Auto-select only explicitly non-consequential, reversible choices. Required acceptance validation that fails or lacks an accepted equivalent is `BLOCK`; reserve `FLAG` for named noncritical residue. |
| 2 | `arcanum/arcana/task-session/SKILL.md` | routed/delegated mutation requires bounded context but has no digest-bound mutation-admission receipt | High | For routed or reusable mutation only, verify a receipt binding task/SWU, controlling artifact identities and digests, dependency frontier, allowed writes, validation surface, and authority/publication class. Rebuild on mismatch; retain live post-mutation validation. |
| 3 | `arcanum/spells/invoke/refresh.md` | `apply-approved` checks report fields but has no verdict over the actual material package, changed paths, digests, dependencies, mirrors, ownership, or mutation state | High | Add a material-package validator to mutation-capable handoffs. Proposal-only authoring may still pass with a gated or deferred handoff. Emit the mutation receipt only after the material validator passes. |
| 4 | `arcanum/spells/invoke/mode-capabilities.json`; `arcanum/spells/invoke/plan.md` | Plan authoring is active while registry release and mutation runtime are separate; `full` and `validate` remain deferred | Medium | Preserve Plan authoring and deferred modes. Represent `artifact_authored`, `registry_released`, and `mutation_runtime_ready` as separate machine-readable ceilings. |
| 5 | `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs` | current appender can record RESERVED types and orphan closes, does not enforce working-agent/final-approver separation, and uses lexical folder checks; duplicate close is already idempotent | High | Reject new RESERVED rows, orphan closes, working-agent self-approval, and destination escape using canonicalized containment including existing-parent realpath/symlink checks. Grandfather history and retain duplicate-close idempotence. Publication checks require explicit authority/publication metadata rather than path inference. |
| 6 | strategy owner/runtime surfaces and dispatch appender | two tension verdicts and explicit confirmation are not bound to the registered sheet; owner and installed surfaces contain substantive, non-identical wording | High | Persist both tension verdicts and the confirmed-sheet digest; reject a changed sheet. Classify differences as canonical contract, formatting, or declared overlay and parity-check the generated surfaces. Add no second human gate. |
| 7 | `arcanum/arcana/decision-gate/SKILL.md` | caller admissibility is implicit and the generic explicit override has no target, scope, hazard class, or one-use boundary | High | Pre-reject structurally invalid options. With no admissible option, `BLOCK`; with one safe option, route it through its owning gate; with two or more admissible options, invoke Decision Gate. Require a typed, target-bound, one-use override receipt and preserve protected owner gates. |
| 8 | `arcanum/arcana/inventory/scripts/validate-index-json.sh`; `.arcanum/inventory/index.json` | live validation fails: exactly 15 entries use out-of-enum kinds—2 `query-file`, 4 `research-findings`, 4 `research-transcript`, and 5 `strategy-result` | High | Reconcile canonical kind vocabulary, updater, current rows, validator, and consumers. A lookup must not claim validated readiness until the current validator passes. |
| 9 | Inventory source and projection surfaces | synchronization and freshness obligations are declared but not enforced bidirectionally | Medium | Check source entries, `index.json`, derived indexes, `index.md`, and enabled projections in both directions for existence, identity, coverage, and freshness. Include current validator status in lookup output; keep historical tag lint warn-only absent a closed vocabulary. |
| 10 | `arcanum/spells/whisper/README.md`; `.agents/skills/whisper/SKILL.md`; `.claude/skills/whisper/SKILL.md` | `.agents` contains current controls plus substantive local presets; `.claude` omits current canonical controls | High | Assemble runtimes from a canonical generated base plus a declared overlay manifest for all local presets. Bind base and preset digests and reject undeclared removal or authority changes while preserving legitimate overlays. |

## Per-skill verdicts

### Task Session — FIX

Keep bounded context, live execution validation, recovery, and closeout. Fix the subjective `--auto` escape and acceptance-critical false-green path. Add a receipt only at routed or reusable mutation admission; a universal receipt would add ceremony without a demonstrated consumer.

### Invoke — KEEP + FIX

Keep proposal-only behavior, active Plan authoring, and deferred `full`/`validate` modes. Fix the mutation-capable handoff with a material-package validator, then expose three separate status ceilings. Proposal completeness is not registry release or execution readiness.

### DomainSpec Subagents Strategy — FIX

Keep one explicit human delegation confirmation. Make the appender enforce the invariants the strategy already claims, bind the two tension verdicts and confirmation to the same sheet digest, and classify owner/runtime differences before regeneration. Duplicate close is not a defect.

### Decision Gate — KEEP + FIX

Keep explicit consent and durable decision records. Do not ask a preference question for malformed packages or a single safe route. Invoke the choice gate only when two or more admissible options remain. Replace ambient override with scoped, typed permission that cannot bypass protected owner gates.

### Inventory — KEEP + FIX

Keep machine-index-first, read-only, non-authoritative lookup. First repair the current kind-contract failure; then enforce source/projection/freshness agreement. JSON parseability is not schema conformance.

### Whisper — KEEP + FIX

Keep editorial status ceilings, human approval, transport controls, and legitimate repository-local presets. Replace accidental generated drift with canonical-base plus declared-overlay assembly and semantic parity checks.

## Direct verification receipts

- Inventory command: `bash arcanum/arcana/inventory/scripts/validate-index-json.sh .arcanum/inventory/index.json`
- Inventory result: non-zero; `FAIL: entries have required fields`; `RESULT: fail (1 failures)`
- Out-of-enum count: 15, with the exact distribution recorded in finding 8
- Dispatch appender: RESERVED type and orphan close are warning-and-append paths; self-approval is explicitly not enforced; duplicate close is already a no-op
- Whisper surfaces: canonical and `.agents` contain current controls with declared-local candidates; `.claude` is materially stale
- Subagents surfaces: owner and installed copies are not byte- or semantics-identical and therefore require classification, not blind copying
- Tension gate: PASS/PASS before dispatch registration
- Verifier: ACCEPT after one REVISE cycle, with the path-containment and admissible-option wording corrections applied above

## Prioritized one-change-at-a-time queue

1. **DSS-1:** fail closed at dispatch, close, approver, and destination admission.
2. **TS-1:** remove consequential auto-selection and acceptance-critical false-green behavior.
3. **INV-1:** validate the material package before a mutation-capable handoff.
4. **INT-1:** restore a passing machine-index contract.
5. **TS-2:** consume a current readiness receipt for routed mutation after Invoke can produce it.
6. **DG-1:** filter inadmissible options and type overrides.
7. **DSS-2:** bind tension/confirmation evidence and classify runtime overlays.
8. **WH-1:** generate canonical base plus declared preset overlays.
9. **INT-2:** add bidirectional freshness and projection validation.
10. **INV-2:** expose the three independent Invoke status ceilings.

This is a priority order for independent maintenance requests. It is not one combined mutation and does not authorize implementation.

## Final disposition

All ten findings survived adversarial verification. Claims that did not survive were removed or narrowed: no universal Task Session receipt, no proposal-only material-package gate, no claim that Plan is unsupported, no duplicate-close defect, no byte-parity claim for Subagents surfaces, no path-only publication inference, no mandatory Decision Gate when one safe route remains, and no overwrite of Whisper's legitimate local presets.
