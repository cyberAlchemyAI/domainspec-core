---
node_type: review
date: 2026-08-20
dispatch_id: 2026-08-20-factory-ai-vladimir-handoff-review
target: sessions/2026-08-20-1150-factory-ai-vladimir-handoff.md
status: resolved
verdict: FIX
authority_level: session-evidence
---

# Review - Factory.ai handoff for Vladimir

## Coverage

| attacker | lens | findings raised | zero-findings defence |
| --- | --- | ---: | --- |
| Heunen, Chris | fidelity / governance | 5 | n/a; two attempted attacks were explicitly defended as non-findings |
| Rittel, Horst | literal-evidence verification | 4 survived, 1 refuted | n/a |

- Collapse note: no `robot_talks` group was used; the single attacker and independent verifier ran sequentially, so premature attacker convergence was not applicable.
- Lens coverage: the complete handoff was attacked from fidelity/governance and every candidate was independently checked against the literal artifact and cited owner sources.
- Refutation discipline: A4 was dropped because the handoff already discloses the unstable conversation source, flags strict coverage, and grants no mutation authority.
- Inventory preflight: no Factory or dispatch-governance match was found; Inventory was not used as review evidence, and its Bash validation remained unavailable because WSL could not start.

## `sessions/2026-08-20-1150-factory-ai-vladimir-handoff.md`

| # | file | evidence quoted from the artifact | severity | proposed fix |
| --- | --- | --- | --- | --- |
| R1 | `sessions/2026-08-20-1150-factory-ai-vladimir-handoff.md` | "Arcanum observability... can benefit from Factory-like runtime signals:" followed by "cost and duration per work-pack or capability", "retries, failures, and intervention points", "execution status and produced receipts", and "failure and rollback reasons". | MAJOR | Separate documented Factory API fields from proposed receipt fields and make per-Mission export feasibility an explicit unresolved gate. |
| R2 | `sessions/2026-08-20-1150-factory-ai-vladimir-handoff.md` | "`execution projection`: determine whether one approved work-pack can become a Mission without losing owner, gate, context, acceptance criteria, or non-goals" and "Its question is whether the projection preserves our contracts..." | MAJOR | Bind projection success to every required Task Session runtime-adapter field and fail closed on any unrepresentable field. |
| R3 | `sessions/2026-08-20-1150-factory-ai-vladimir-handoff.md` | "Factory is strongest, in its public product and documentation surfaces, as an operational software-development runtime" and "Our stack is strongest in the layers that determine what work means and when its results count". | MINOR | Replace "strongest" with "publicly emphasizes" for Factory and "is designed to govern" for the local stack. |
| R4 | `sessions/2026-08-20-1150-factory-ai-vladimir-handoff.md` | "cyberAlchemy-v2 | authority spine, evidence boundaries, and promotion" under "Current responsibility". | MINOR | Label cyberAlchemy-v2 as staging a candidate authority spine while promoted/current owners retain authority. |

**Verdict:** FIX

### Verification basis

R1 survives because Factory's cited Analytics API documents aggregate organization/user metrics such as credits, tokens, tool calls, sessions, models, and productivity, but does not document all proposed receipt fields or their per-work-pack exportability. Mission documentation shows monitoring, intervention, retries, and validation behavior, but not the proposed structured receipt bridge.

R2 survives because the current Task Session runtime-adapter contract requires a broader handoff envelope than the abbreviated experiment criterion, including identity, source links, dependencies, blocker state, bounded write scope, done criteria, validation evidence, strict context coverage, fallback rules, runtime limits, result evidence, and ownership boundaries.

R3 survives only as wording precision. The handoff contains enough qualification to prevent the comparative language from becoming a structural defect.

R4 survives only as status precision. The cyberAlchemy-v2 owner README presents the project as a candidate/start-state consolidation surface, while the handoff's table can be read as assigning it a fully current responsibility.

## Change requests

1. MAJOR - Split observed Factory analytics from desired adapter telemetry, and make exportability a gate rather than an assumed capability.
2. MAJOR - Replace the abbreviated execution-projection preservation list with the complete Task Session runtime-adapter contract and fail closed on any unsupported field.
3. MINOR - Demote comparative "strongest" language to source-bounded emphasis and design intent.
4. MINOR - Mark cyberAlchemy-v2's authority-spine role as candidate/staging rather than fully current.

## Closeout

- Final approver: `parent`
- Approval result: accepted; all surviving findings quote the artifact and the refuted candidate was dropped.
- Exit reason: `resolved`
- Agents spawned: total `2`; explorer `1`; skeptic `1`; helpers `0`; loops used `1`.
- Fix application: not performed; applying change requests is a separate follow-up.

