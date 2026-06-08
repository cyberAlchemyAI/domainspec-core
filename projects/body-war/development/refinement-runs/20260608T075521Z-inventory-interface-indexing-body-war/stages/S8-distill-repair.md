---
stage: S8-distill-repair
capability: distill
mode: validate
status: pass
updatedAt: 2026-06-08
---

# S8 Distill Repair

## Validation Checks

| Check                                                              | Result |
| ------------------------------------------------------------------ | ------ |
| Target boundary is Body War.                                       | pass   |
| Arcanum Inventory remains capability source.                       | pass   |
| Pilot mutation remains deferred.                                   | pass   |
| First coherent pilot corpus is bounded.                            | pass   |
| Existing open decisions are preserved.                             | pass   |
| Local command/runtime surfaces are evidence, not mutation targets. | pass   |

## Repair Applied

No conceptual repair required.

The earlier DomainSpec-framework route is superseded for this target. The Body
War route should be treated as the current target-specific refinement.

## Runtime Surface Note

Body War has local `.codex/commands/` wrappers for the needed Arcanum
capabilities. This is stronger than the previous framework-target route, where
some repo-local `tools/arcanum --resolve` handles were missing.

## Verdict

Pass.
