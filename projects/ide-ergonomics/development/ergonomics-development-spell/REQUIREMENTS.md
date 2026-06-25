---
tags: [ide, ergonomics, spell, spellcraft, requirements, two-lane, cyberalchemy-v2]
node_type: requirements
is_session: false
layer: workflow
nature: design-seed
status: draft
created: 2026-06-24
craft_scope: projects/ide-ergonomics/.craft/
craft_context: CTX-ERGO-SPELL-ROOT
---

# Requirements: `ergonomics-development` spell

Drawn **before** harvesting concepts (your method: requirements first, then go to
`cyberAlchemy-v2/` for the definitions/constitutions/authority). This is the
**concept shopping list** the two-lane harvest must gather and reconcile.

## What the spell is

A governed, reusable Spellcraft spell that moves **one new ergonomics affordance**
(a human-machine-integration improvement to the IDE Ergonomics surface) through a
full lifecycle — **propose → requirements → two-lane research → design → implement
→ test → owner-gated admission** — never promoting it without its owner. It is the
governed engine behind the project's existing `self-assembling-ergonomics`
primitive and the `ide-action-surface` discipline candidate, and it routes new
affordances through the **coordinate-admission gate** the spine-model review
installed.

## Proposed phases (capability requirement)

| # | Phase | Owner sigil | Gate / handoff |
| --- | --- | --- | --- |
| 0 | **Frame** — open/resolve the Craft scope, record the proposal | `craft` | a context + next_move; no mutation |
| 1 | **Requirements** — draw what the affordance must do + concept list | `craft` (+ `distill`) | a requirements artifact |
| 2 | **Two-lane research** — capability lane + cav2-authority lane | `domainspec-subagents-strategy` (`research`) | tensioned sheet → human confirm → findings |
| 3 | **Design** — author spec/design, bind authority, place on a coordinate | `invoke` (define/design) | glossary-consistency gate |
| 4 | **Plan** — layer the implementation (L0 PoC → hardening) | `invoke` plan / `implementation-layering` | SWUs named |
| 5 | **Implement** — execute the first bounded SWU | `task-session` | runtime evidence shape |
| 6 | **Test** — pre-registered criterion, run, verdict | `experiment-harness` | SURVIVED / FALSIFIED |
| 7 | **Admit** — owner-gated promotion through the coordinate-admission gate | `decision-gate` (+ the model's admission gate) | assembled+green ≠ shipped; route to real owner |
| — | **Adversarial check** (any phase) | `domainspec-subagents-strategy` (`review`) | verified change requests |

## Required sigils (to confirm in the harvest)

`craft`, `domainspec-subagents-strategy` (research + review), `invoke`,
`implementation-layering`, `task-session`, `experiment-harness`, `decision-gate`,
`dispatch-spec`.

**Optional:** `distill`, `x-ray`, `refine`, `ux-evidence-validator`,
`definitions-governance`, `discipline-governance`, `constitution-governance`,
`inventory`, `necronomicon`.

## Concepts to harvest from `cyberAlchemy-v2/` (authority requirement)

The two-lane harvest's **authority lane** must return the *exact* governed
artifacts the spell binds (build-from-owned — bind, never re-define):

| Need | Candidate cav2 source (to confirm/expand) |
| --- | --- |
| Authority kinds + closed enumeration | `authority/AUTHORITY-MODEL.md`; `CAV2-D48` (authority promotion lifecycle), `CAV2-D49` (closed authority-kind enumeration / default-deny) |
| Promotion ladder / gates | `authority/promotion-policy.md` |
| Public/private boundary | `authority/boundaries.md` |
| Governing constitutions | `authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md`, `VAULT-CONCEPT-ADOPTION-CONSTITUTION.md` |
| The HMI proposition the spell serves | `CAV2-CAND-HMI-001` (synergetic cybernetic human-machine integration) + `authority/decisions/2026-06-23-hmi-candidate-promotion-prep.md` (proof surface = Connective + IDE Ergonomics) |
| UX/UI knowledge governance | `ux-ui/UX-UI-KNOWLEDGE-GOVERNANCE.md` |
| The ergonomics/experience definition | `CAV2-D46` (UI/experience) and any ergonomics-bearing definitions in `DEFINITIONS.md` |
| Cross-capability practice | `disciplines/DISCIPLINES.md` + the `ide-action-surface` discipline candidate |
| Value/philosophy framing | `VALUE-AND-PHILOSOPHY-PROPOSITION.md` |
| Reusable primitives (claim≤proof, intent, gate, provenance) | `CAV2-D31`–`D39` cluster |

## The two-lane discipline (BLK-CAV2-HARVEST)

- **Capability lane** (`primary_lane: capability`) — confirm the required/optional
  sigil set + the phase map above; find composition gaps.
- **cav2-Authority lane** (`secondary_lane: authority`) — return the exact
  definitions/constitutions/authority the spell binds, each with its owner and its
  promotion guardrail.
- **Reconcile** — produce one bound concept set: every capability the spell
  composes, paired with the authority that governs it; flag anything that would
  require *creating* new authority (route to its owner, never invent in the spell).

## Boundaries (non-negotiable)

- The spell **composes** sigils; it does not re-define any sigil contract
  (Spellcraft authority rule).
- It **binds** cav2 definitions/constitutions; it does not promote or mutate them
  (promotion routes to definitions-governance / constitution-governance /
  decision-gate).
- A new affordance is **admitted** only through the coordinate-admission gate
  (open + default-deny + irreducibility); assembled-and-green is never shipped
  without the owner gate.
- HMI (`CAV2-CAND-HMI-001`) is **served, not promoted** — the spell produces proof
  surface, the cav2 owner promotes.

## Exit of this requirements step

The open blocker `BLK-CAV2-HARVEST` and the blocking decision `DEC-SPELL-IDENTITY`
(name/scope/sigil-set) are resolved by the two-lane harvest, after which Spellcraft
composes the spell contract.
