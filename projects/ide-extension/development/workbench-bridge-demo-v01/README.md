---
module: ide-extension-workbench-bridge-demo-v01
version: current
status: planned
updatedAt: 2026-07-17
docType: invoke-package-index
---

# Workbench Bridge Demo V0.1

This package defines, designs, and plans the next small ide-extension increment:
make the manual bridge visible and repeatable from the workbench UI.

The goal is not to add autonomous workers. The goal is to make the proven manual
loop easy to use:

```text
prepare -> ready -> poll -> claim -> result -> receipt
```

## Artifacts

- [SPEC.md](SPEC.md) - define artifact.
- [GLOSSARY.md](GLOSSARY.md) - terms used by the increment.
- [ARCHITECTURE-BUNDLE.md](ARCHITECTURE-BUNDLE.md) - six-view design.
- [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) - L0-L3 boundary.
- [WORK-PACK.md](WORK-PACK.md) - executable plan.
- [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md) - plan-size check.
- [INVOKE-RESULT.md](INVOKE-RESULT.md) - invoke closeout.

## Next Route

Run Task Session on `TASK-WBD-001`.
