# MARS Plan: E11 Technique/Specialization Experiment

Status: execution complete (bootstrap run); evidence-grade status update on hold
Mode: mars-agent orchestration mapped back to MARS semantics
Complexity: high

## Execution Orchestrator

Primary orchestrator command:

- `mars-research-orchestrator` (agent)

E11 default mapping:

- Agent: `mars-research-orchestrator`
- Arguments: `E11 execute all waves`

Operator variants:

- staged wave rollout: `E11 execute wave <N>`
- gap closure only: `E11 execute gaps-only`
- sequential inline mode: `E11 execute interactive`
- fallback for phase-scaffolded GSD projects: `/gsd-execute-phase <phase-number>`

Behavior contract:

- `mars-research-orchestrator` is the primary orchestrator; it discovers tasks, groups dependency-safe waves, and spawns specialist MARS subagents in parallel.
- Re-running the same execution request is resumable; completed tasks are skipped and blocked tasks are reported with remediations.
- Use this orchestrator after plan artifacts exist for the target experiment/runbook.

## Planning Decisions (Locked)

- Run naming standard: `run-YYYY-MM-DD[-suffix].jsonl`
- Inventory onboarding: all 25 selected source IDs before first run row
- Adjudication tie-break: third-rater final
- Baseline pinning: E9 run2 rerun artifact hash + commit
- G4 strictness: full-tier required fields from first row
- Evidence upgrade timing: one full run plus one confirming rerun

## Current Gate Snapshot

- G1: pass
- G2: pass
- G3: pass
- G4: pass (pilot/full/rerun schema validated)
- D4: hold for claim-status upgrade until manual evidence-grade adjudication run

## Dependency-Ordered Execution Backlog

| Task ID | Task | Depends On | Gate/Stage | Claim Mapping | Required Outputs |
| --- | --- | --- | --- | --- | --- |
| T1 | Freeze protocol and baseline pin | none | G1 | C2, MARS-C2 | `protocol.md`, `results/E11-baseline-pin.md` |
| T2 | Convert source pins to immutable references | T1 | G2 | C2, MARS-C2 | `sources.md` |
| T3 | Create inventory entries and index links for all selected sources | T2 | G3 | C1, C2, MARS-C1, MARS-C2 | `inventory/*.md`, `inventory/INVENTORY-INDEX.md` |
| T4 | Preflight run package and gate checks | T3 | G1-G3 recheck | C2, MARS-C2 | gate output log in `results/` |
| T5 | Pilot extraction (first 20-30 rows) + strict G4 | T4 | S7 + G4 | C2, MARS-C2 | `data/run-<date>-pilot.jsonl` |
| T6 | Full run collection to sample minimums | T5 | S7 | C2, MARS-C2 | `data/run-<date>.jsonl` |
| T7 | Adjudication and confirming rerun | T6 | S8-S9 | C1, C2, MARS-C1, MARS-C2 | `results/E11-adjudication-log.md`, `data/run-<date>-rerun.jsonl` |
| T8 | Full analysis and claim delta package | T7 | S10 | C1, C2, MARS-C1, MARS-C2 | `results/run-<id>-results.md`, `results/E11-claim-delta.md` |
| T9 | Evidence update and audit propagation | T8 | S11-S12 | MARS-C2 primary | `research/projects/mars/results/MARS-EVIDENCE-STATUS.md` |

## Execution Waves

### Wave 0 - Protocol Freeze (T1)

1. Record baseline pin file with:
   - baseline artifact path
   - git commit
   - sha256 digest
2. Confirm protocol includes dependency declarations and full-tier G4 requirements.

Go condition:
- `protocol.md` and `results/E11-baseline-pin.md` both present and complete.

### Wave 1 - Source Pinning (T2)

1. Replace all `snapshot-*` and moving `current`-style pins in `sources.md`.
2. Keep only immutable pin forms: `release-`, `tag-`, `commit-`, `sha256-`, `isbn-`, `doi-`, `archive-`.

Go condition:
- G2 command returns `g2_violations=0`.

### Wave 2 - Inventory Readiness (T3)

1. For each selected `SRC-*` source, add inventory entry markdown containing:
   - source ID
   - exact pin string from `sources.md`
   - category/type
   - experiment refs including E11
2. Add each source ID to `INVENTORY-INDEX.md`.
3. Re-run G3; resolve missing index links and pin mismatches.

Go condition:
- `missing_inventory_index=0`
- `missing_inventory_entries=0`
- `pin_mismatches=0`

### Wave 3 - Preflight And Pilot (T4-T5)

1. Re-run G1/G2/G3 checks from protocol.
2. Start pilot file `data/run-YYYY-MM-DD-pilot.jsonl`.
3. Collect 20-30 mixed rows (edge + scenario).
4. Run strict G4 full-tier validator.

Stop condition (D1):
- Any G4 violation.

Go condition:
- G4 violations = 0 and no mixed protocol/version configuration.

### Wave 4 - Full Collection (T6)

1. Continue data collection until sample minima are met:
   - edge rows >= 120
   - scenario rows >= 30
   - domains >= 8
   - >= 3 scenarios per required technique family
   - adjudication subset >= 20%
2. Freeze SC thresholds; do not modify post first row.

Stop condition (D2):
- rolling median overhead > 0.35 and no quality gain.

### Wave 5 - Adjudication + Rerun (T7)

1. Run dual-rater on adjudication subset.
2. Resolve disagreements with third-rater final decisions.
3. Record rationale in `results/E11-adjudication-log.md`.
4. Execute confirming rerun (`run-YYYY-MM-DD-rerun.jsonl`) with same protocol hash.

Go condition:
- Adjudication complete and rerun generated with same protocol version/hash.

### Wave 6 - Analysis + Evidence Update (T8-T9)

1. Produce analysis report and claim-delta artifact.
2. Apply anti-false-confidence checks before status changes:
   - protocol drift
   - subgroup contradiction
   - sensitivity checks
   - reproducibility check
   - triangulation with E6/E9
3. Update C2 adjudication first, then propagate to MARS-C2.
4. Update MARS evidence matrix after claim-level proof is complete.

## Stop/Go Decision Points

| Decision ID | Stage | Stop If | Go If |
| --- | --- | --- | --- |
| D0 | Pre-run | G2 or G3 not passed | Both passed |
| D1 | Pilot | Any G4 violation | Zero violations |
| D2 | Mid-run | SC-TS-1 or SC-TS-5 trailing by >10pp and not recoverable | Trend recoverable |
| D3 | Pre-analysis | Sampling floors not met | All minima met |
| D4 | Status update | No full adjudication or no rerun | Full analysis + adjudication + rerun complete |

## Verification Commands

Use protocol-local commands from:
- `research/projects/domainspec/experiments/E11-technique-specialization/protocol.md`

Repository-level readiness commands:

```bash
set -e
./tools/check_github_drift.sh
implementation/domainspec/tools/check_docs_sync.sh
```

## Evidence Update Sequence

1. S0 Baseline freeze note only.
2. S1 Readiness note after G2+G3 pass, no claim-status change.
3. S2 Data-quality note after first full run + G4 pass, no claim-status change.
4. S3 Claim adjudication update for C2 first, then MARS-C2.
5. S4 Confidence hardening update after confirming rerun.

## Governance Notes

- MARS semantics are authoritative for gates and claim/evidence state changes.
- No C2 or MARS-C2 status upgrade is allowed before D4 go condition.
- D4 clearance preparation artifacts are available in experiment results:
   - `results/E11-D4-clearance-plan-2026-04-22.md`
   - `results/E11-manual-adjudication-worklist-2026-04-22.md`
   - `results/E11-manual-adjudication-sheet-template.csv`
   - `results/E11-inventory-freshness-check-2026-04-22.md`
