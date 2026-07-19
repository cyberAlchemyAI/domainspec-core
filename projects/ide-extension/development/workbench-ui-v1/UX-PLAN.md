# Workbench UI V1 UX Plan

## Audience

One local operator creating and reviewing agent-produced work repeatedly. The
interface should feel like a quiet workbench, not a protocol debugger or landing
page.

## Desktop Layout

```text
+---------------------------------------------------------------+
| Workbench | server | current run | stop/status                |
+------------------+---------------------------+----------------+
| Work rail        | Canvas workspace          | Inspector      |
| New task         |                           | Next action    |
| Active runs      | Current HTML artifact     | Run timeline   |
| Craft sources    | and interaction surface   | Evidence       |
+------------------+---------------------------+----------------+
```

Use stable responsive tracks: approximately `300px minmax(0, 1fr) 360px`,
collapsing the Inspector before the Work rail as width decreases.

## Mobile Layout

Use three views: Work, Canvas, Evidence. Keep the current run status and next
action visible in the top bar. Open task creation and evidence as full-height
drawers; do not squeeze a desktop grid into the viewport.

## Primary Interactions

- Segmented `Agent task` / `Dry run` mode.
- Skill is required and visible only for Agent task.
- One primary action per state: Prepare, Approve, Make available, or Inspect result.
- Secondary reject/revoke/release actions live in an overflow menu with confirmation.
- Timeline stages use labels and status icons; color is supplementary.
- Evidence drawer groups Summary, Receipt, Context, Grants, and Diagnostics.

## Content Rules

- Say `Agent task`, not `schema-v2 envelope`.
- Say `Available`, not `ready target selected`, in primary UI.
- Say `Running` for claimed and reserve `Completed` for admitted terminal result.
- Keep IDs and assurance terminology in Evidence.
- Never describe a copied command as automatic execution.

## Accessibility And Stability

- Keyboard order follows Work rail -> Canvas -> Inspector.
- Every state and icon has a text name.
- Focus moves to the newly legal primary action after a state transition.
- Fixed control dimensions prevent status changes from shifting the shell.
- Desktop and mobile tests cover the longest labels and empty/error states.
