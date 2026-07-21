---
module: ide-extension-workbench-ui-v1
version: 1.0.0-plan
status: in_progress
updatedAt: 2026-07-20
docType: invoke-package-index
---

# Workbench UI V1

Workbench UI V1 turns the proven local workbench capabilities into one coherent
operator product. It does not add a new authority layer. It reorganizes task
preparation, approval, bridge execution, Canvas output, Craft work, and evidence
around the workflow a person is actually trying to complete.

## Product Flow

```text
Create agent task -> approve -> make available -> agent runs -> inspect result in Canvas
```

Dry run remains available as an explicit secondary mode.

## Artifacts

- [SPEC.md](SPEC.md)
- [GLOSSARY.md](GLOSSARY.md)
- [ARCHITECTURE-BUNDLE.md](ARCHITECTURE-BUNDLE.md)
- [UX-PLAN.md](UX-PLAN.md)
- [GLOSSARY-CONSISTENCY.md](GLOSSARY-CONSISTENCY.md)
- [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md)
- [WORK-PACK.md](WORK-PACK.md)
- [EXECUTION-PACK.md](EXECUTION-PACK.md)
- [PLAN-TRANSPORT.md](PLAN-TRANSPORT.md)
- [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md)
- [INVOKE-RESULT.md](INVOKE-RESULT.md)
- [PLAN-REFRESH.md](PLAN-REFRESH.md)

## Next Route

`SWU-WUI-001` through `SWU-WUI-010` passed their shell, compatibility,
request-mode, pure projection, ordered lifecycle, legal-action, retained
Canvas, read-only Craft seed, and receipt-linked Inspector checks. Run Task
Session on `SWU-WUI-011` in
[TASK-WUI-005-VALIDATE.md](work-pack/tasks/TASK-WUI-005-VALIDATE.md) to record
the explicit human usefulness verdict. The machine matrix is already green;
V1 remains unpromoted until that verdict exists.
