# Lifecycle Handoff: Invoke Lifecycle Progress Protocol

Status: ready for non-mutating Spellcraft assessment; mutation gated

## Target

Revise the public Invoke spell and adjacent Task Session contract to implement
the generic lifecycle-progress protocol in `DEFINE.md` and `DESIGN.md`.

## Next owner

Spellcraft, design/lifecycle assessment.

## First request

Execute only `SWU-ILP-001`:

- ratify one transition-admission owner;
- ratify exact public source locations for epoch, readiness, change-impact, and
  transition contracts;
- state which artifacts remain projections/read models;
- state which owners may submit evidence but cannot admit transitions;
- confirm that no canonical mutation follows from the decision alone.

## Sanitized public-safe requirements

1. Separate authored-plan validity from mutation-handoff readiness.
2. Bind one immutable execution epoch to one selected unit and complete
   declared control graph.
3. Assign compatible producer, independent validator, and consumer roles by
   execution mode.
4. Route mutation execution only from an epoch-bound ready receipt.
5. Preserve exact mismatch blocking and classify semantic impact separately.
6. Require successor/supersession for every epoch-control change; same-epoch
   advancement may add evidence/material only.
7. Admit progress only through allowed append-only transitions.
8. Make Refresh declare one of four transition kinds and prohibit target
   implementation.
9. Treat legacy plans as unadmitted until freshly validated.
10. Prove the topology with generic fixtures and a live generic run.

## Private boundary

Do not copy:

- names or paths of private product work;
- private research transcripts or project-specific receipts;
- DomainSpec or Saturn implementation claims;
- private Inventory or telemetry payloads.

The public package may use only generic synthetic fixture names and protocol
invariants.

## Required return

```yaml
swu_id: SWU-ILP-001
result: pass | flag | block
decision:
  transition_admission_owner: string | null
  public_source_paths: [path]
  evidence_submitters: [capability]
  excluded_authority_surfaces: [artifact-kind]
validation:
  - authority boundary review result
  - public/private review result
blockers: [string]
residue: [string]
next_route: invoke refresh plan_repair | decision-gate | deferred
```

No source mutation is authorized by this handoff.

