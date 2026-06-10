# Stage 01 — Context Builder Evidence Baseline

Capability: `context-builder` · Mode: `standard` · Runtime: native (Claude Code) · Status: **pass (re-baselined)**
Request frame: `--strict --emit both --handoff runtime --persist <run-folder>/context-builder`

## Target Correction (recorded honestly)

The first pass of this baseline mis-resolved the target as the `ops/` **runtime-surface convergence** program (skills-first cleanup / install profiles / orchestration). That was wrong. The `dispatch-route-reviewer` subagent read the actual files and surfaced the real target. Corrected:

**The target is the existing artifact pair, dated 2026-06-03 on branch `codex/infra-spec`:**

- `ops/development/infra-spec-research-strategy.md` — a research strategy toward a *future* `infra-spec` capability.
- `ops/development/infra-spec-research-strategy.dispatch.json` — the machine-checkable route for that strategy.

`infra-spec` here means a **governed infrastructure contract** (source intent ↔ runtime realization ↔ schemas/instances ↔ environment boundaries/state namespaces ↔ deployment topology/operational behavior ↔ observability/receipts/reflection ↔ failure residue/repair ↔ owner boundaries/promotion gates), inheriting discipline from the DomainSpec **Lean formalization** work. This is **distinct** from the runtime-surface convergence program — a scope adjacency that caused the initial mis-resolution and is itself an improvement opportunity (Stage 06).

## Selectors and Obligation-Linked Excerpts

| Selector | Source | Obligation for the refinement |
| --- | --- | --- |
| Strategy objective + starting thesis | `infra-spec-research-strategy.md` (Objective, Starting Thesis) | "The route makes the package worth creating"; infra-spec ≠ "deployment docs with nicer names." Preserve this framing. |
| Non-Negotiables (6) | same | Path-cited evidence; YAML-first validator-backed schemas; runtime evidence ≠ promotion authority; label analogies; child fan-out behind approval; writes only `ops/development/infra-spec-*`. |
| 7 fan-out lanes (L1–L7) | same (Fan-Out Lanes) | Cartographer, Lean translator, runtime/deploy auditor, schema/taxonomy governor, observability/residue analyst, project archaeologist, gap hunter — each with a receipt contract. |
| 9 dispatch steps + gates | `infra-spec-research-strategy.dispatch.json` | mode `research`; steps recover→x-ray→fanout→child-gate→zigzag→tournament→synthesize→validate→handoff; 5 gates; boundary_evidence; promotion_guardrails. |
| **Validation gate self-test** | `.md` "Validation" + dispatch `validate-research-coverage` step | The strategy mandates its own dispatch must pass `validate-dispatch.py`. **It currently does not** (see coverage assessment). |
| Lean discipline source | `.md` (Starting Thesis), `ops/development/domainspec-lean-formalization-*` | schema/instance, proof/build/status separation, typed residue, counterexample discipline, analogy demotion. |

## Coverage Assessment (the headline finding)

Running the **working** native validator against the existing dispatch:

```text
VALIDATION=block
BLOCK: subagent_strategy.receipt_requirements missing native receipt fields (artifacts, blockers, capability_ref, dispatch_id, handoff_note, observer_status, residue, status, step_id, validation)
BLOCK: subagent_strategy.receipt_requirements missing lifecycle fields (agent_id, close_status, join_status, reroute, residue, role_id, spawn_status)
FLAG ×4: capability_ref 'x-ray' / 'decision-gate' / 'robot-talks' / 'implementation-readiness' is not canonical and has no candidate metadata
```

So the strategy **violates its own non-negotiable** that the route must pass dispatch validation. This is the strongest, most concrete "make it better."

Second finding: the `.md` "Validation" command points at `arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py`, but the `arcanum/` submodule is **uninitialized (empty)** in this worktree. The runnable validator is `.claude/skills/dispatch-spec/scripts/validate-dispatch.py`. The documented self-test command is therefore broken as written.

## Runtime Handoff Pack

- Target artifact: `ops/development/infra-spec-research-strategy.dispatch.json` (+ companion `.md`)
- Write boundary: this run folder + the two target artifacts (parent-owned `ops/development/infra-spec-*`, consistent with the strategy's own non-negotiable)
- Frame handle: `context-builder-frame`; Evidence handle: `context-builder-artifact` (this file)

## Verdict

`pass` — coverage is strong and, critically, surfaced a concrete blocking defect plus a broken self-test command. Sufficient to define the refinement around making the strategy *valid, runnable, and unambiguous* without discarding its (good) design.
