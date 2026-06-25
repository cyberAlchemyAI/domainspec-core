# Spell: Ergonomics Affordance Lifecycle

Canonical ID: `ergonomics-affordance-lifecycle`
Aliases: `new-ergonomics`, `ergonomics-development`
Scope: local reusable spell (`.arcanum/spells/`)
Status: candidate (composed 2026-06-24; experiment harness not yet initialized — see Failure Policy)
Lifecycle owner: `spellcraft`
Governing discipline: `ide-action-surface` (step-2 spell; see `projects/ide-ergonomics/disciplines/ide-action-surface.md`)
Source design: `projects/ide-ergonomics/development/ergonomics-development-spell/findings.md` (design dialectic verdict REDIRECT, 2026-06-24)

## Purpose

Move **one captured ergonomic opportunity** through a governed lifecycle —
**capture → triage/requirements → research → design → plan/implement → test → emit
admission-proof** — into an owner-admitted ergonomic affordance, **without promoting
anything itself.** It is the human-led development engine of the `ide-action-surface`
discipline.

This spell is a **Spellcraft composition; it promotes nothing.** Every promotion
routes to its owner, and the spell's outputs acquire authority only through those
owner gates (cyberAlchemy-v2 `AUTHORITY-MODEL.md` owner-route rule; `CAV2-D49`
default-deny). It is **not** an enumerated authority kind and must carry a
decision-gate + constitution-governance acknowledgement before promotion-readiness.

### Relation to siblings (build-from-owned)

- **`self-assembling-ergonomics`** — the *machine-led autonomous* variant of the same
  loop (the surface improving itself). This spell is the *human-led* variant. They
  differ on **who-leads-when**; this spell may **compose** self-assembling-ergonomics
  as the autonomous arm. Sibling, not rename.
- **`ide-assisted-arcanum-routing`** (project candidate `SPELL-IDE-ASSISTED-ARCANUM-ROUTING.md`)
  — the *runtime* action-card surface. An affordance this spell admits eventually
  **projects into** that runtime surface. Sibling, not the same spell.
- **`provisional-model-stewardship`** (cyberAlchemy-v2 discipline) — owns the coordinate
  model. This spell **hands admission-proof to** the model owner's gate; it never owns
  or invokes the coordinate-admission gate.

## Trigger Conditions

- An opportunity is captured in `projects/ide-ergonomics/opportunity-backlog.md` and triaged for development.
- A user asks to add / research / implement a new ergonomic affordance.
- A `NEW:?` candidate coordinate needs an irreducibility-proof before anything is built on it.

## Required Sigils

| Capability | Role in spell |
| --- | --- |
| `craft` | Own the work ledger: frame the opportunity, pending-by-node state, decisions, gaps, recomposition. |
| `invoke` | Author define / design / plan artifacts for the affordance. |
| `implementation-layering` | Layer the implementation from L0 proof to hardening. |
| `task-session` | Execute the first bounded SWU with runtime evidence. |
| `decision-gate` | Resolve consequential choices; carry the authority-kind acknowledgement; co-own admission with the model owner. |

## Referenced Sub-Workflows (handoff, NOT re-narrated)

These are complete workflows owned elsewhere; the spell **hands off** to them and
consumes their receipts. It does not copy their process bodies (Spellcraft authority rule).

| Sub-workflow | Owner | When |
| --- | --- | --- |
| Subagent research / review / dialectic | `domainspec-subagents-strategy` | when the affordance needs synthesis, a tensioned design dialectic, or adversarial review |
| Pre-registered experiment | `experiment-harness` | the test phase — criterion frozen before the run |

## Optional Sigils

`distill` (reduce to the SCU), `definitions-governance` (candidate terms — incl. the
absent "ergonomics" definition), `discipline-governance` (the step-1 owner gate),
`dispatch-spec` (route-shape validation), `ux-evidence-validator` (frontend evidence),
`x-ray` (visualize a route/model), `refine` (vague seeds), `inventory` / `necronomicon`
(prior knowledge + capture-first), `signal-observer` (usage telemetry).

## Prerequisites

- The `ide-action-surface` discipline is formalized (step-1; `disciplines/ide-action-surface.md`). **This spell is gated on that step.**
- An opportunity exists in the backlog with the five intake fields + a candidate coordinate.
- `.arcanum/observability/` exists for telemetry (or a gap is reported).

## Shared State

| State | Meaning | Authority |
| --- | --- | --- |
| `opportunity` | A captured backlog entry (id, friction, coordinate, owner, priority, status). | `opportunity-backlog.md` (candidate-only) |
| `craft_context` | The work ledger scope for this affordance. | `.craft/ledger.yml` (source of truth) |
| `affordance_design` | The define/design/plan artifacts. | `invoke` |
| `coordinate_placement` | Which coordinate the affordance sits on (or a `NEW:?` candidate). | the coordinate model (`UNIFIED-PRODUCT-VIEW.md`), default-deny |
| `admission_proof` | Fixture + receipts + pre-registered verdict + coordinate placement, handed to the gate. | this spell produces it; the **model owner admits** |
| `receipt` | Execution / handoff / validation / blocked proof. | producing capability |

## Execution Phases

| # | Phase | Owner | Input | Output | Gate | Failure Policy |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Capture / Frame | `craft` (+ intake) | a triaged `opportunity` | craft context + next move | opportunity has 5 fields + a candidate coordinate | route back to intake; ask for the missing field |
| 2 | Triage + requirements | `craft` + `distill` | opportunity | requirements + SCU; coordinate identified | owner named; `NEW:?` coordinate flagged for the admission gate | keep as candidate; one scope question |
| 3 | Research *(referenced)* | → `domainspec-subagents-strategy` | requirements | findings / hardened design | tensioned sheet + human confirm (owned there) | proceed with recorded gaps; do not invent |
| 4 | Design + bind | `invoke` (+ `definitions-governance`) | requirements / findings | spec/design; bound cav2 authority | glossary-consistency; bindings cite real owners | flag mis-binding; route absent terms to definitions-governance |
| 5 | Plan + first SWU | `invoke` plan / `implementation-layering` → `task-session` | design | work-pack; first SWU runtime evidence | validation-before-implementation (CAV2-C9) | report partial; next safest route |
| 6 | Test *(referenced)* | → `experiment-harness` | the implemented slice | SURVIVED / FALSIFIED + report | criterion pre-registered (frozen before run) | FALSIFIED leaves residue; iterate or drop |
| 7 | Emit admission-proof | `decision-gate` + **model owner** | proof package | admission verdict; backlog + ledger update | **owner admits; the spell never owns/invokes the coordinate-admission gate** | hand off the proof and stop; record blocked admission |

Phases 3 and 6 are **named handoffs** to owning capabilities, not re-narrated bodies
(satisfies the Spellcraft "no multiple workflows in one spell" anti-pattern). Phase 7
**produces proof and hands it to the gate** — the spell has no admission authority.

## Handoff Artifacts

- **Research handoff** → `domainspec-subagents-strategy` (a dispatch sheet; receipts = findings.md).
- **Experiment handoff** → `experiment-harness` (a pre-registered criterion; receipt = SURVIVED/FALSIFIED report).
- **Admission-proof package** → coordinate-model owner / `decision-gate` (fixture + receipts + frozen verdict + coordinate placement). The spell's terminal output; admission is the owner's act.

## Gates

- **Default-deny / no-promotion (load-bearing).** The spell promotes nothing; outputs acquire authority only through owner gates (`CAV2-D49`). Before promotion-readiness, a `decision-gate` + `constitution-governance` note must confirm the spell is a composition that routes promotion out, not a new authority kind.
- **Coordinate-admission is not owned here.** A new coordinate or primitive is admitted only by the `PRODUCT-VIEW.md` / governance owner; the spell hands over proof and never routes the gate (avoids the circularity recorded at `UNIFIED-PRODUCT-VIEW.md:160`).
- **Bindings bind, never promote.** cav2 authority is referenced, not mutated; `CAV2-D46` is *Experience Evidence Lifecycle* (a process), the `D45/D46/D47 + CAV2-C15` cluster is the governance binding for the experience surface; "ergonomics" has no cav2 definition → route to `definitions-governance` as residue, never cite as canon.
- **HMI served, not promoted.** Outputs may feed the `CAV2-CAND-HMI-001` proof surface (Connective + IDE Ergonomics); the cav2 owner promotes the term, never this spell.
- Candidate definitions → `definitions-governance`; consequential choices → `decision-gate`; reusable spell/sigil changes → `spellcraft` / `sigil-development`; canonical mutations → their owning lifecycle.

## Failure Policy

- Missing intake field → route back to the intake, do not invent it.
- Owner undeterminable → one focused question or a bounded route menu.
- Research/experiment handoff declines → record the gap, proceed with recorded residue, never fabricate the receipt.
- Admission not granted → keep the affordance as a candidate; record the blocked admission as residue; do not self-admit.
- **Experiment harness not yet initialized (current named block):** this spell has no `development/VALIDATION-EXPERIMENT.md` yet. Promotion-readiness is **blocked** until `experiment-harness` initializes the harness (low/medium/complex examples) on the first opportunity that enters the lifecycle.

## Local Customization

- Backlog: `projects/ide-ergonomics/opportunity-backlog.md`; intake: `OPPORTUNITY-INTAKE.md`.
- Craft scope: `projects/ide-ergonomics/.craft/`.
- Coordinate model: `projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md`.
- Default admission owner: `PRODUCT-VIEW.md` owner / governance review.

## Observability

When `.arcanum/observability/` exists, record: opportunity id + coordinate; phases
attempted; sub-workflow handoffs (research, experiment) + their receipts; gates passed/blocked;
admission verdict; files changed; user corrections; whether a `NEW:?` coordinate was
proposed; recommended spell updates.

## Output Contract

```markdown
## Ergonomics Affordance Lifecycle Result
- Opportunity: <OPP-id> (<coordinate>)
- Phases run: <list> (referenced handoffs: research? experiment?)
- Design artifacts: <paths or none>
- Test verdict: SURVIVED | FALSIFIED | not-run
- Admission-proof: <path or none>  (handed to: <owner>)
- Admission verdict: admitted | rejected | blocked (owner-gated; not self-admitted)
- Backlog status update: captured | triaged | in-lifecycle | admitted | dropped
- Promotion routed to: <owners or none>
- Next action: <step>
```
