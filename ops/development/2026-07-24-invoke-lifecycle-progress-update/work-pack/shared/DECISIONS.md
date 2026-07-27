# Shared Decisions and Transition Relation

## Same-epoch rule

Same-epoch advancement is permitted only when:

1. `epoch_control_digest` is byte-identical;
2. the selected SWU, mode, roles, paths, dependencies, writes, validation, and
   required artifact/receipt classes are unchanged;
3. new evidence or material satisfies an already-declared requirement;
4. the requested edge is explicitly allowed.

Any control change requires a successor epoch and `superseded`. No `plan_repair`
label overrides this rule.

## Allowed edges

| From | To | Kind | Minimum witness |
| --- | --- | --- | --- |
| none | `epoch_issued` | `epoch_issue` | complete epoch + Plan owner receipt + independent completeness receipt |
| `epoch_issued` | `handoff_gated` | `readiness_assessment` | readiness receipt with exact missing requirements |
| `epoch_issued` | `handoff_blocked` | `readiness_assessment` | readiness receipt with incompatible requirement and blocker fingerprint |
| `epoch_issued` | `handoff_ready` | `readiness_assessment` | epoch-bound ready receipt |
| `handoff_gated` | `handoff_blocked` | `readiness_assessment` | new incompatibility evidence |
| `handoff_gated` | `handoff_ready` | `material_production_validation` or `route_selection` | unchanged control digest + newly satisfied requirements + ready receipt |
| `handoff_blocked` | `handoff_gated` | `plan_repair` or `route_selection` | unchanged control digest + removed incompatibility + remaining exact gaps |
| `handoff_blocked` | `handoff_ready` | `material_production_validation` or `route_selection` | unchanged control digest + removed blocker + ready receipt |
| `handoff_ready` | `admission_blocked` | `task_admission` | epoch-bound failing Task Session admission receipt |
| `handoff_ready` | `admitted` | `task_admission` | epoch-bound passing Task Session admission receipt |
| `admission_blocked` | `admitted` | `task_admission` | new preconditions + new passing receipt; failed receipt retained |
| `admitted` | `mutation_crossed` | `execution_effect` | first-effect receipt |
| `mutation_crossed` | `execution_complete` | `execution_validation` | execution + independent live-validation receipts |
| `execution_complete` | `closeout_joined` | `closeout_join` | exact join + required impact receipt |
| `closeout_joined` | `epoch_terminal` | `terminalization` | named terminal postcondition + complete receipt chain |
| `epoch_issued`, `handoff_gated`, `handoff_blocked`, `handoff_ready`, `admission_blocked`, or `admitted` | `superseded` | `plan_repair` | successor ID + old/new digests + reason + retained history; admitted also proves no mutation crossed |
| `execution_complete` | `superseded` | `plan_repair` | independent `execution_invalidating` receipt + successor ID + retained execution history |

`plan_repair` may advance `handoff_blocked` only when the epoch control digest is
unchanged. If the repair changes a control field, the only legal edge for the
old epoch is `superseded`.

## Rejected edges

- self, backward, skipped, or unlisted edges;
- transitions out of `epoch_terminal` or `superseded`;
- direct `mutation_crossed -> superseded`;
- `execution_complete -> superseded` without independent
  `execution_invalidating`;
- any lifecycle edge from `projection_synchronization`;
- any transition admitted by a producer, consumer, writer, observer, Inventory,
  projection, cursor, or status file instead of the ratified owner.

## Refresh kinds

| Kind | Postcondition | May admit lifecycle edge? |
| --- | --- | --- |
| `plan_repair` | exact plan delta or successor request | only through transition owner and same-epoch/successor rule |
| `material_production_validation` | mode material and validator receipt exist | readiness edge only through transition owner |
| `projection_synchronization` | declared views match their owner receipt | no |
| `route_selection` | one next owner/route selected from current evidence | readiness edge only when no control field changes |

