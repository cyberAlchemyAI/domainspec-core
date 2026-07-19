---
module: ide-extension-open-poll-bridge
status: planned
docType: traceability
---

# Traceability

| Source Finding | Plan Response | Verification |
| --- | --- | --- |
| Ready should be open to any interested poller. | `SWU-OPB-003` changes ready semantics. | API tests and witness. |
| Identity should be claimed, not preselected. | `SWU-OPB-001`, `SWU-OPB-004`. | schema, replay, result tests. |
| One ready item is enough for L0. | OPB-PD1 and L0 guardrails. | no queue in diff review. |
| Race loser must not see payload. | `SWU-OPB-004`, `SWU-OPB-007`. | concurrency/adversarial tests. |
| Workbench copy must not imply type-based polling. | `SWU-OPB-006`. | UI tests and browser check. |
| Existing bridge proof is Codex-shaped. | `SWU-OPB-007/008`. | non-Codex witness receipt. |
