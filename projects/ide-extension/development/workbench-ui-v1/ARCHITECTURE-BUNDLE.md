---
id: ide-extension-workbench-ui-v1-architecture
project: ide-extension
status: planned
updatedAt: 2026-07-17
invoke_mode: design
---

# Architecture Bundle: Workbench UI V1

## 1. Context View

The operator uses one local browser page. The local kernel remains authoritative
for envelopes, approvals, claims, results, Canvas projection, events, and
receipts. The active agent session remains outside the browser and crosses the
bridge through `workbench-poll`.

## 2. High-Level Structure View

```text
Workbench shell
  +-- Work rail: compose, active runs, Craft sources
  +-- Canvas workspace: retained HTML output and interaction
  +-- Inspector: state action, timeline, evidence drawer
        |
        v
Existing local APIs and event-derived projections
        |
        v
Existing kernel authority and durable receipts
```

## 3. Low-Level Components View

| Component | Responsibility |
| --- | --- |
| Mode selector | Explicitly selects Agent task or Dry run. |
| Task composer | Validates task and mode-specific skill requirements. |
| Run list | Shows active first, history second, with stable status labels. |
| Run timeline | Maps envelope and receipt state into ordered stages. |
| State action | Shows only the next legal operator action. |
| Canvas workspace | Preserves existing revision loading and interaction behavior. |
| Craft source list | Reads verified frontier items and seeds task text/context. |
| Evidence drawer | Shows grants, refs, receipts, validation, and diagnostics on demand. |
| Responsive shell | Desktop three-region layout and mobile tab/drawer layout. |

## 4. Workflow Process View

1. User opens New task; Agent task is selected.
2. User enters task and skill, optionally seeded from Craft.
3. Prepare creates a schema-v2 awaiting-approval request.
4. Inspector presents Approve request.
5. Approved state presents Make available.
6. Available state shows the opaque handle and session command.
7. Claim changes the timeline to Running without implying completion.
8. Admitted result changes the timeline to complete and exposes receipt evidence.
9. Linked Canvas output stays in the workspace and can receive interactions.

## 5. Decision Flow View

| Question | Decision |
| --- | --- |
| How is request type selected? | Explicit segmented mode, never inferred from an empty field. |
| What dominates the screen? | Canvas output, with work and evidence in side regions. |
| Can the browser execute Codex? | No; it displays the command and observes admitted state. |
| When is a run complete? | Only after a terminal kernel-admitted result/receipt. |
| Does selecting Craft mutate the ledger? | No; it seeds context only. |
| Does V1 require a frontend framework? | No; preserve the current single-page implementation unless evidence forces a split. |

## 6. Dependency Interface View

| Interface | Use | Constraint |
| --- | --- | --- |
| `POST /api/envelopes/prepare` | Prepare explicit task mode payload. | Agent task requires requested skill. |
| Approval endpoints | Approve/reject/revoke. | Operator action only. |
| Bridge ready/unready projection | Availability and opaque handle. | No pre-claim task disclosure to pollers. |
| `/api/state` and focused detail routes | Run projection and receipts. | UI never reads durable files. |
| Canvas routes/events | Display and interact with retained HTML. | Canvas is not protected-effect authority. |
| `/api/craft/frontier` | Read pending Craft sources. | Read-only; no direct Craft mutation. |

## Risks

| Risk | Treatment |
| --- | --- |
| UI hides governance too aggressively. | Evidence drawer stays one action away and timeline remains visible. |
| Responsive layout buries Canvas. | Mobile uses explicit Work, Canvas, and Evidence tabs. |
| Current state payload encourages coupling. | Keep a UI mapper boundary; add focused reads only when tests prove need. |
| V1 is confused with Operations V1. | Name this milestone Workbench UI V1 in all artifacts. |

## Design Distill

Pass. The UI shell, composer, lifecycle projection, Canvas/Craft composition,
and validation close as one product unit. Worker, provider, browser, and IDE
host integrations remain independent packages.
