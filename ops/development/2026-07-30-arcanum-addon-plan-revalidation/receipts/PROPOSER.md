schema_version: `arcanum.native-dispatch-runner.receipt.v0.1`  
action_id: `spawn-0001`  
dispatch_id: `2026-07-30-arcanum-addon-plan-revalidation`  
run_id: `arcanum-addon-plan-revalidation-cc655251`  
wave_id: `revalidation`  
step_id: `s1-revalidate`  
role: `Proposer`  
capability_ref: `distill`  
agent_id: `/root/revalidation_proposer_spawn_0001`  
status: `block`  
validation: `block`  
started_at: `2026-07-30T13:36:00-03:00`  
finished_at: `2026-07-30T13:47:30-03:00`  
blockers:

- `NEW-001`: the implementation dispatch can advance layers after one generic selected-SWU receipt rather than complete prior-wave closure.
- Existing non-revalidation blockers remain: `B-GOV-001`, `B-BOOT-001`, `B-OWNER-001`, `B-ADAPTER-001`, and `B-RETENTION-001`.

artifacts:

- All 13 files under `development/arcanum-addon/define/`
- All 21 files under `development/arcanum-addon/design/`
- All 41 files under `development/arcanum-addon/plan/`
- `development/arcanum-addon/BASELINE-REFRESH.md`
- Regression checklist only: `ops/development/2026-07-30-arcanum-addon-invoke-distill-review/findings.md`
- Produced files: none

# Distill revalidation result

Review verdict: **BLOCK**  
Validation verdict: **BLOCK**

The six prior findings are literally closed in the current corpus. However, a new MAJOR route-shape defect survives: the executable implementation dispatch does not faithfully encode the complete wave dependency topology authored by the work-pack.

## Corpus binding

- Source commit verified: `80dcd79677ad73b21dbaded12e0e9cd47aace82b`.
- Corpus count: 75 files across `define/`, `design/`, and `plan/`.
- Aggregate command:

```bash
find "$addon_root/define" "$addon_root/design" "$addon_root/plan" \
  -type f -print0 |
  sort -z |
  xargs -0 sha256sum |
  sha256sum
```

- Observed digest: `bb0a6f31cf1142902693d30c53ecc2ee08b6747e14ea12f7dff5b81d08d64b14`.
- Digest validation: **PASS**.
- All 25 JSON files parsed successfully with `jq -e empty`.

## Closure matrix

| Prior finding | Result | Current literal evidence |
| --- | --- | --- |
| F-001 durable L0 continuation | CLOSED | `TASK-1-CATALOG-PREVIEW.md:95-113` defines an owner-issued, digest-bound, durable decision; `TASK-2-APPROVAL-STATE.md:10-11,32-33` requires current `continue`; `W2.md:6-8` repeats the exact gate; `CLOSEOUT-SYNC.md:18-19` binds successor eligibility. |
| F-002 isolated uninstall/rollback | CLOSED | `TASK-4-LIFECYCLE-ACCEPTANCE.md:49-72` defines isolated copies and preservation invariants; lines 98-104 require the branch join; `W4.md:5-9` makes neither branch consume the other; `CLOSEOUT-SYNC.md:31-33` binds both receipts into security. |
| F-003 lifecycle witnesses/counters | CLOSED | `VALIDATION-CONTRACTS.md:18-22` supplies degradation, owner-loss, uninstall-preservation, rollback-success/failure fixtures; lines 26-34 define digest/branch/counter validation; `PLANNED-WITNESSES.json` contains `PW-DEGRADED-001`, `PW-UNINSTALL-001`, and `PW-ROLLBACK-001`. |
| F-004 degradation acceptance | CLOSED | `TASK-4-LIFECYCLE-ACCEPTANCE.md:23-39` defines `DEGRADE-001`, zero starts, honest projections, preserved history, and explicit recovery; `WORK-PACK.md:87,121` schedules and atomically classifies it; `CLOSEOUT-SYNC.md:29` requires the full matrix. |
| F-005 complete atomicity and BOOT-002 | CLOSED | `WORK-PACK.md:99-125` enumerates every non-exempt SWU, including BOOT-002, PROPOSAL-UI-001, and RUN-UI-001; `TASK-0-GOVERNANCE-COMPATIBILITY.md:67-89` requires staged validation plus all-or-nothing commit/restoration, otherwise pre-execution splitting. |
| F-006 atomic governance receipt | CLOSED | `TASK-0-GOVERNANCE-COMPATIBILITY.md:24-45` requires one digest-bound complete authority packet and makes partial synchronization non-pass; `WORK-PACK.md:103` and `CLOSEOUT-SYNC.md:11` preserve the same contract. |

## New finding

### NEW-001 — Implementation dispatch can bypass complete wave closure

Severity: **MAJOR**

Failure trace:

1. `DISPATCH.json:118-147` executes one selected L0 SWU and emits only `receipts/L0-selected-swu.json`.
2. `DISPATCH.json:152-188` makes L1 depend on that single generic receipt plus the L0 decision, rather than the complete CATALOG, STATUS, PROPOSAL, PROPOSAL-UI, and L0-decision receipt set.
3. The same compression recurs at `DISPATCH.json:192-224` for L2 and `DISPATCH.json:228-261` for L3.
4. `DISPATCH.json:265-297` allows verification after one `L3-selected-swu.json`.
5. This conflicts with the authoritative plan topology: `EXECUTION-PACK.md:23-28` requires complete wave exit evidence; `W1.md:6-13`, `W2.md:5-12`, `W3.md:5-15`, and `W4.md:5-15` require full intra-wave sequences and joins; `TASK-5-VERIFY-DECIDE.md:25-28` requires every prior required SWU and a complete evidence set.

A conforming runner could therefore follow the dispatch literally, close one SWU per layer, and reach verification without the complete wave receipts. The later verification stop condition detects missing evidence only after the invalid route has already crossed layer boundaries; it does not close the dependency graph.

One-line repair: replace generic per-layer selected-SWU edges with explicit per-SWU re-entry/loop gates and complete wave-receipt joins, then bind verification to the complete W4 bundle rather than `L3-selected-swu.json`.

## Recomposed expected end state

The intended system remains coherent:

- Arcanum Bootstrap owns generated package selection, refresh, provenance, and restoration.
- ResonantOS owns manifest, grants, authenticated mediation, approval, run/child/artifact records, and product lifecycle.
- Augmentor owns intent capture and redacted conversational projection only.
- Stable public Arcanum operations own capability execution truth.
- Living Archive owns intake, review, and trusted-memory promotion.
- Readiness, promotion, and release remain independent decisions.

The layer decomposition is also appropriately narrow:

- L0: governance, no-write compatibility, no-authority catalog/status/proposal, then durable continuation.
- L1: exact approval, replay-safe fixture state, reload/Unknown.
- L2: stable Strategy/Whisper owners, isolated clarification, four separate result actions.
- L3: degradation, disable, isolated uninstall/rollback branches, security, browser evidence, verification.

The first unit is narrow: `GOV-001`, then no-write `BOOT-001`; the first repository mutation remains `CATALOG-001` (`IMPLEMENTATION-LAYERING.md:42-55`). No SWU is selected.

## Attacks attempted

- Durable continuation staleness, owner identity, disposition exclusivity, and successor binding
- Bootstrap selection drift, partial apply, restoration, and required pre-execution splitting
- Partial issue/Project/owner/retention synchronization
- Absent Strategy/Whisper owner and forbidden fallback substitution
- Stale, edited, expired, provenance-drifted, and grant-drifted approval
- Replay, crash boundary, duplicate start, HTTP-success inflation, and partial-child isolation
- Reload fidelity, cached terminal truth, and `Unknown`
- Clarification cross-child leakage
- Open/attach/consume/intake side-effect collapse
- Compatibility drift and owner-loss degradation
- Cached launch after disable
- Uninstall mutation of Bootstrap inventory or retained history
- Rollback success/failure collapse and loss of disabled fallback
- Shared-state contamination between uninstall and rollback branches
- Secret, token, private-material, raw-path, prompt, screenshot, record, and argv disclosure
- Planned-witness inflation
- Browser start before deterministic/security closure
- Readiness/promotion/release inference
- SWU atomicity completeness
- First-unit narrowness and hidden third runtime
- Ambiguous successor and dispatch-to-work-pack dependency mismatch

All attacks except NEW-001 were closed by literal current contracts.

## Technique trace

- Abstraction-level guard: the owner-preserving product integration remains the correct broad unit.
- Recomposition proof: Define → Design views → L0-L3 → W0-W5 closes semantically, but the machine dispatch does not preserve every dependency.
- Evolution profile: later capability breadth remains deferred behind exact owner operations and layer gates.
- Boundary-object check: digests, opaque handles, and owner receipts remain the correct cross-owner objects.
- Premortem: the most likely failure is a runner treating one generic layer receipt as complete wave closure; the required guard is an explicit receipt-set join.
- Navigable-result check: start remains GOV-001, but dispatch repair and revalidation must precede mutation routing.
- Cycle guard: one Validate round was sufficient because the surviving defect is a direct structural contradiction, not a recurring renamed split.

## Residue

- The prior `B-DESIGN-001` reason can be superseded only after the parent joins both fresh revalidation receipts; this Proposer receipt alone cannot close the governed all-role gate.
- NEW-001 blocks Distill PASS even though F-001 through F-006 are closed.
- Existing governance, compatibility, owner, adapter, and retention blockers remain.
- Planned fixtures and witnesses are not executed evidence.
- No implementation, browser execution, readiness, promotion, or release is proven.

## Handoff

Join this receipt with the fresh Balancer receipt. If the Balancer corroborates NEW-001, route the dispatch topology back to the Plan/dispatch owner for the one-line repair above, preserve `selectedSWU: none`, and require another exact-byte validation before mutation handoff.
