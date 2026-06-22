# S07 - Interrogation Design Review

Owner: `interrogation`
Mode: `refine-design-review`
Verdict: `pass`

## Review Question

Is the design specific enough to plan implementation without reopening the language decision?

## Verdict

Pass. The design names the TypeScript package layout, DomainSpec layer responsibilities, auth workflows, Strava provider boundaries, Body War consumer boundary, and validation expectations. The Python path is no longer a valid implementation target.

## Findings

| Finding | Severity | Resolution |
| --- | --- | --- |
| Body War currently remains a Python app | flag | Work-pack must choose an explicit consumer bridge or migration SWU; auth cannot be accepted while Python imports own the auth runtime. |
| Production session store not selected | flag | L0/L1 can use memory/JSON adapters behind ports; L2 selects durable store and token encryption. |
| Strava live credential proof requires secrets | non-blocker | Use mocked gateway and contract tests first; real smoke test remains manual/secret-gated. |
| Existing auth docs still mention Python package | flag | Future implementation should update or replace those docs. |

## Readiness Decision

Proceed to repair and plan. No blocker prevents a non-executed work-pack.

## Structured Interview Result

- Target scope: TypeScript auth design
- Mode: refine-design-review
- Questions asked: 0
- Decisions recorded: 1, Body War auth must not depend on Python auth runtime
- Remaining ambiguities: production adapter choices assigned to L2/L3
- Verdict: pass
- Next step: distill repair
