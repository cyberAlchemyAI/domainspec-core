# Decision Gate: Invoke Runtime Material Validator Packaging

- Target: `TASK-WFE-003` / `SWU-WFE-003B`
- Result: `PASS`
- Opened at: `2026-07-23T03:15:56Z`
- Resolved at: `2026-07-23T03:23:08Z`
- Decisions resolved: 1
- Blockers remaining: 0

## Decision

Where should the deterministic Invoke material validator live so both canonical
development and generated Invoke runtimes can execute the same authority?

### Option 1 — Promote runtime support from development (recommended)

Move runtime-required schemas into `arcanum/spells/invoke/schemas/` and runtime
code into a new `arcanum/spells/invoke/scripts/` support directory. Keep causal
fixtures, reports, and runners under `development/`.

- Benefit: the existing generator already copies top-level support directories,
  so Codex and Claude receive the same canonical validator automatically.
- Cost/risk: widens the approved canonical write scope and requires the focused
  harness imports and SWU-WFE-003A receipt to be refreshed.
- Choose when: generated runtimes must be self-contained and reproducible.
- Downstream impact: SWU-WFE-003B can add the resolver, Refresh contract,
  integration fixtures, and exact generated parity without changing bootstrap.

### Option 2 — Add a generator allowlist for runtime development support

Keep source files under `development/runtime-support/` and change bootstrap to
copy only that declared subset into generated Invoke packages.

- Benefit: preserves the current source location.
- Cost/risk: changes the shared generator, overlaps an already dirty generator
  file, and adds a special packaging rule that needs its own tests.
- Choose when: keeping all validator code under development is more important
  than generator simplicity.
- Downstream impact: SWU-WFE-003B expands to generator implementation and
  validation before Refresh integration.

### Option 3 — Require an external receipt producer

Keep generated Invoke packages as receipt consumers only; another installed
authority must produce the material receipt.

- Benefit: no generator or canonical file relocation.
- Cost/risk: generated Invoke is not self-sufficient, valid-package readiness
  depends on an undeclared external capability, and current completion claims
  must be narrowed.
- Choose when: runtime self-sufficiency is explicitly out of scope.
- Downstream impact: redesign the handoff interface and record the producer as a
  hard dependency before SWU-WFE-003B can close.

### Explain / more context

This does not select an option. It requests a deeper comparison of runtime
portability, authority, reversibility, generator risk, and downstream changes.

## Recommendation

Choose Option 1. It uses the generator's existing generic support-copy contract,
keeps tests and authoring history in `development/`, and makes the executable
authority available wherever the generated Invoke package is installed.

## Decision record

- Selected option: Option 1 — promote runtime support from development
- Source of decision: direct user reply `1`
- Rationale: use the existing generic support-directory generator contract so
  generated Invoke packages remain self-contained while development fixtures
  remain outside runtime packages.
- Assumptions: none
- Deferred decisions: none
- Mutation status: approved for the refreshed SWU-WFE-003B scope; the original
  blocked receipt remains historical evidence

## Gate result

- Result: `PASS`
- Consequential work unblocked: refresh the SWU-WFE-003B write scope and context,
  then resume the bounded implementation.
- Validation: selected option is one of the recorded options and resolves the
  only blocker-level choice.
