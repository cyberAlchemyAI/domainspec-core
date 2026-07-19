---
id: ide-extension-workbench-bridge-demo-v01-glossary
project: ide-extension
status: planned
updatedAt: 2026-07-17
invoke_mode: define
---

# Glossary

| Term | Meaning | Status |
| --- | --- | --- |
| Workbench bridge | The local ide-extension flow that prepares approved work for a session and admits a bound result. | linked |
| Ready request | An approved envelope selected as generally available for polling. | linked |
| Request handle | Opaque identifier returned by `ready`; it must not reveal task or requested skill. | linked |
| Claim | Atomic session action that binds a ready request to `agent_ref` and `session_ref`. | linked |
| Blind boundary | Rule that task and requested skill appear only after successful claim. | linked |
| Execution receipt | Kernel-admitted `skill.execution` receipt created after a bound result. | linked |
| Demo recipe | Workbench UI flow that explains the manual loop through status, commands, and receipt. | new-local |
| Poller | Interested local session that runs `ready` and `claim`; not a background worker. | linked |

## Glossary Consistency

No new global Arcanum term is promoted. `Demo recipe` is local to this increment.
