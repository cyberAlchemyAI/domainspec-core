# Implementation Layering - Public App Server Adapter Repair

| Layer | Decision | SWU-RWO-CX-003R slice | Required evidence | Deferred |
| --- | --- | --- | --- | --- |
| L0 contract | Preserve Task Session semantic ownership and provider-neutral raw-host boundary. | Public adapter profile, method allowlist, authority-null result. | Contract review and exact source baselines. | Live provider semantics. |
| L1 transport | Make app-server selectable and execute bounded stdio JSON-RPC. | tools/arcanum registration plus stdlib adapter driver. | Fake process success, permission request, interrupt, malformed, timeout, and teardown cases. | Network transports and daemon control. |
| L2 governance | Prove installed schema parity and no private-state/controller leak. | Local schema generator validation and Task Session adapter contract. | Seven method witnesses, binary identity, no credential/model/network use, E/O/V/P/C/B/T. | Installed live App Server parity beyond schema. |
| L3 lifecycle | Return to evidence-based sufficiency review. | Fresh CX003 audit attempt after repair terminal. | CX003R T plus immutable prior finding. | CX004 and all later migration units. |

## Promotion Rules

- L1 cannot register `app-server` without L0 authority-null and ownership boundaries.
- L2 cannot pass from fake traces alone; it requires regenerated schemas from the bound installed Codex binary.
- L3 cannot route directly to CX004. Only a fresh CX003 audit may decide sufficiency.
- No layer authorizes live App Server, provider, network, credential, model, publication, or production effects.

## Atomicity

Possible child concerns are registration, transport, fake validation, installed parity, and documentation. They are retained as one SWU because each independently incomplete subset would expose an unusable or misleading public adapter; the reviewable acceptance boundary is the single selectable/executable generic adapter with both fake execution and installed-schema proof.
