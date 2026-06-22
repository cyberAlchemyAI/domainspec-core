# Invoke Refresh Report - Poker Agent Arena Two Rule Views

Mode: `refresh`
Mutation mode: `apply-approved`
Evidence date: `2026-06-19`
Target workflow root: `projects/poker-agent-arena`

## Source Signals

### RS-PAA-RULES-HUMAN-VIEW

- Type: `evidence_added`
- Source: user `/invoke` request on `2026-06-19`
- Target artifacts:
  - `RULES.md`
  - `SPEC.md`
  - `DESIGN.md`
  - `WORK-PACK.md`
- Claim: The arena needs a human/product rule view that explains the competition without becoming the machine contract.
- Evidence: User requested one view for humans, product/explainer oriented.
- Confidence: `high`
- Mutation safety: `safe`

### RS-PAA-RULES-AGENT-VIEW

- Type: `evidence_added`
- Source: user `/invoke` request on `2026-06-19`
- Target artifacts:
  - `AGENT-RULES.md`
  - `SPEC.md`
  - `DESIGN.md`
  - `WORK-PACK.md`
- Claim: The arena needs an engineer/agent rule view that complements the spec for agent authors, validators, and future implementation agents.
- Evidence: User requested another engineer/agent view and named two rule files as the example structure.
- Confidence: `high`
- Mutation safety: `safe`

### RS-PAA-L0-HANDOFF-TREE-DRIFT

- Type: `artifact_drift`
- Source: user `/invoke` request on `2026-06-19`
- Target artifacts:
  - `DESIGN.md`
  - `IMPLEMENTATION-LAYERING.md`
  - `WORK-PACK.md`
  - `INVOKE-RESULT.md`
- Claim: The L0 handoff output tree and acceptance gates drifted because the two required rule files were not represented.
- Evidence: Existing `SWU-PAA-001R` tree named protocol, transcript, namespace, and fixture surfaces but not the requested human/product and engineer/agent rule surfaces.
- Confidence: `high`
- Mutation safety: `safe`

## Delta Summary

- `evidence_added`: added `RULES.md` for the human/product view.
- `evidence_added`: added `AGENT-RULES.md` for the engineer/agent view.
- `artifact_drift`: updated root artifacts so `SWU-PAA-001R` and `SWU-PAA-001` preserve the two-view split.

## Applied Changes

1. Added `RULES.md` as the human/product rule view.
2. Added `AGENT-RULES.md` as the engineer/agent rule view.
3. Updated `SPEC.md` with the rule-view contract and L0 refresh requirement.
4. Updated `DESIGN.md` with rule-view architecture and the expanded L0 output tree.
5. Updated `GLOSSARY.md` with both rule-view terms.
6. Updated `IMPLEMENTATION-LAYERING.md` with L0R deliverables and exit gates for the two rule files.
7. Updated `WORK-PACK.md` so `SWU-PAA-001R` and `SWU-PAA-001` preserve the rule-view split.
8. Updated `INVOKE-RESULT.md` to list the two new outputs and refresh delta.

## Skipped Changes

- Did not create versioned `spec/l0/` schema files; that remains owned by later task-session execution.
- Did not implement runtime protocol or game logic.
- Did not change scoring or engine-selection gates.

## Validation

Ran checks:

```sh
python3 -m json.tool projects/poker-agent-arena/development/invoke-refreshes/20260619T141951Z-two-rule-views/refresh-report.json >/dev/null
find projects/poker-agent-arena -name '*.json' -print0 | xargs -0 -n1 python3 -m json.tool >/dev/null
git diff --check -- projects/poker-agent-arena
rg -n "RULES.md|AGENT-RULES.md|human/product|engineer/agent|Rule View" projects/poker-agent-arena
bash -lc "! rg -n 'Status: first Invoke artifact|Run `task-session` on `SWU-PAA-001` next|Replay \\| Seed handle' projects/poker-agent-arena/*.md"
```

## Phase Status

`pass`: approved refresh deltas were applied to scoped target artifacts, with runtime execution still gated to `task-session`.

## Next Route

`task-session` on `SWU-PAA-001R: Repair L0 Contract Handoff`.
