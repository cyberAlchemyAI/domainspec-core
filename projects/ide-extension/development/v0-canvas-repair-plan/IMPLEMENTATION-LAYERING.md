---
module: ide-extension-v0-canvas-repair
version: current
status: completed
updatedAt: 2026-07-12
docType: implementation-layering
---

# Implementation Layering: V0 Canvas Repair

## Purpose

Repair the current complete-file canvas contract without turning the trusted-
local value experiment into a larger security or Operations V1 project.

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Included scope | Deferred scope | Exit evidence |
| --- | --- | --- | --- | --- | --- |
| L0 policy coherence | Can the specification say exactly why canvas publication does not require an approval/execution receipt? | Explicit preview/display exception in `SPEC.md` and `ARCHITECTURE.md`. | Protected-effect distinction, canvas audit-event semantics, no source mutation claim. | New approval schema or UI. | Review obligations G1-A/G1-R/G1-I map to one non-contradictory policy. |
| L1 canonical admission | Can publication and content fetch admit only the resolved target beneath the canonical workspace root? | Realpath containment plus file-handle read. | Root/target canonicalization, safe error mapping, in-root symlink behavior. | Hostile multi-user race guarantees and native `openat2`. | External symlink and retargeted content cannot be served or committed. |
| L2 adversarial regression | Do normal, missing, in-root link, external link, nested link, and retarget cases remain deterministic? | Focused helper/API/restart tests. | No-event rejection, no-byte leakage, normal publish/serve/revision behavior. | Remote filesystem matrix. | Focused and existing canvas suites pass. |
| L3 closeout | Does the repaired V0 still prove the original value loop without overclaiming? | Integrated audit and work-pack synchronization. | Schema, canvas, bridge, diff, and traceability checks. | Operations V1 and region behavior. | Review findings have implementation receipts and no regression. |

## Active Window

Execute L0 through L3 sequentially. L0 resolves policy before implementation so
the path repair does not accidentally add an approval subsystem.

## Promotion Rules

- The trusted-local exception applies only to canvas preview/display state.
- It does not authorize shell, network, source-file write, Craft execution,
  provider action, commit, push, export, or remote browser control.
- Canvas events remain durable audit evidence but are not relabeled as
  `skill.execution` receipts.
- Canonical containment must protect both publish and historical content-fetch
  paths because both call `readWorkspaceHtml`.
- No Operations V1 route, schema, storage, parser, or region work enters this
  package.

## Smallest Coherent Unit

`SWU-VCR-001` is the first unit because it resolves the documented policy that
the implementation must satisfy. `SWU-VCR-002` is the first runtime unit:
canonicalize, contain, open, and read one target through one helper used by
publish and content serving.
