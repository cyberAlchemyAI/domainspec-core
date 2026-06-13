# Arcanum Copilot Instructions

This repository uses Arcanum governance for reusable agent capabilities.

For Arcanum work:

- Read `AGENTS.md` first when available.
- Treat `dispatch-spec` as the route-shape validator.
- Treat `invoke` as the define/design/plan/handoff authoring surface.
- Treat `task-session` as the execution owner for one bounded task or SWU.
- Prefer native Copilot agent execution with repository instructions over nested model-backed CLI calls.
- Keep `tools/arcanum` as a deterministic resolver, validator, handoff, and legacy adapter compatibility surface.
- Return artifact paths, validation result, observer status, blockers, and follow-up.

