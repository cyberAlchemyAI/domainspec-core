---
artifact: work-pack-traceability
status: candidate
updatedAt: 2026-07-18
---

# Traceability

| Requirement | Source | Planned artifact | First proof evidence |
| --- | --- | --- | --- |
| graph identity | test-engine IR + findings | normalized graph JSON | graph digest |
| node/edge admission | relationship registry | structural validation result | accepted `enforces` edge |
| obligation derivation | `rules/index.ts` | obligation JSON | deterministic obligation key |
| executable test | `emit/tests.ts` | generated test case | test result |
| binding | missing end-to-end bridge | binding JSON | adapter and fixture digest |
| evaluator | structural checker + planned local evaluator | evaluator JSON | scoped verdict |
| receipt | `residue/receipt.ts` | receipt JSON | replayable input digests |
| composability | removal/non-collapse rule | negative mutation | rejected edge/receipt |
