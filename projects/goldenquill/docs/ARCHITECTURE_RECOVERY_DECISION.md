
# Architecture Recovery Decision

Status: ACTIVE
Scope: Golden Quill / Tilth truth-layer recovery

## Decision

Golden Quill / Tilth will restore a single governed runtime path before further UI expansion, productization, indexed read-model work, or advanced orchestration.

The governed path is:

```text
Python governed projection endpoint
→ strict identity envelope
→ Pydantic-validated response
→ one React API client
→ read-only UI
→ no fixture fallback in production
```

## PR #97

PR #97 is donor-only.

It must not be merged.

It must not be rebased into main.

It must not be cherry-picked as a whole branch.

Useful work may be salvaged later by specific file and only after the backend projection contract is green.

## Active UI Surface

`apps/tilth_ui_react` is the active React operator UI path for this recovery.

`apps/tilth_ui` and `apps/tilth_demo_v0` are treated as historical/prototype surfaces unless explicitly reactivated by a later decision.

## Node Shim

The Node shim must not be deleted before Python projection parity is established.

Before deletion or quarantine:

1. Pin the shim's current output against a tracked sample fixture.
2. Make the Python endpoint match the required behavior, except for intentional governance changes.
3. Confirm React no longer depends on the shim.
4. Add a static check preventing reintroduction.

## Recovery Freeze

The recovery freeze prohibits mixed-surface feature work.

No new feature is accepted unless it passes through the governed path.

The freeze exits only when PR-A, the Python projection contract PR, merges green.

## PR Lane Rule

One PR equals one lane.

Allowed lanes:

* Backend / Contract
* Frontend Consumer
* Tooling / CI
* Data Read Model
* Docs / Canon

A PR that mixes backend API, React UI, and tooling is a boundary violation.
