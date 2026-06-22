# Task: Z-Rig Craft Management State

SWU: `SWU-ZRIG-MGMT-001`
Type: private management artifact
Status: ready, not selected

## Goal

Create scoped Craft state for Z-Rig review/remediation so blockers, decisions, gaps, definitions, artifacts, and next moves are indexed locally.

## Write Scope

- `projects/zrig/.craft/ledger.yml`
- `projects/zrig/CRAFT.md`

## Acceptance

- Ledger and view exist.
- Rows link to review evidence and this remediation packet.
- Blockers, decisions, gaps, and next moves are represented.
- No row claims Craft gives runtime authority, product-mode assurance, or public promotion readiness.

## Check

```bash
test -f projects/zrig/.craft/ledger.yml
test -f projects/zrig/CRAFT.md
rg -n "F1|F3|F4|F6|F8|product-mode|authority" projects/zrig/.craft/ledger.yml projects/zrig/CRAFT.md
```

## Handoff Note

This task may use the `craft` skill. It is management work only and should not be mixed with engine mutation.
