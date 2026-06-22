# Task: Readiness Audit

SWU: `SWU-ZRIG-READINESS-AUDIT`
Findings: F1-F14
Status: pending

## Goal

After bounded remediation SWUs land, produce a current proof/no-proof table that decides whether any public-safe extraction or adapter planning can be proposed.

## Write Scope

- `projects/zrig/review/**` follow-up artifact
- `projects/zrig/architecture/PRODUCT-MODE-AUTHORITY-INVENTORY.md`
- `projects/zrig/development/arcanum-integration-remediation/WORK-PACK.md`
- Optional Craft state updates if Craft has been initialized

## Acceptance

- Each F1-F14 item has status: fixed, blocked, deferred, refuted, or not started.
- Every fixed item cites command output or source diff.
- Public/private boundary scan is clean.
- The audit explicitly states whether product-mode assurance is still blocked.

## Checks

```bash
git diff --check projects/zrig
rg -n "Z-Rig|OpenClaw|Analog|deploy/sentinel|product-mode" arcanum .agents/skills
make doctor
make bump-check
```

Run parent checks only when preparing parent publication.
