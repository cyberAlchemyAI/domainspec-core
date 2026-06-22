# What Craft Is

## 1. Craft in one paragraph

Craft is a first-tier Arcana **sigil** and a recursive, **file-backed
project-ledger method**. Its core idea is to keep recursive development state
**explicit and durable** so important work survives the conversation that
produced it: a project carries a small, machine-readable ledger of nested
**contexts**, working **descriptions**, **blockers**, **enablers**, open
**decisions**, **gaps**, candidate **definitions**, **next moves**, **child
contexts**, route/validation **evidence**, and **recomposition** records. As the
method puts it, Craft "turns intention into stable artifacts by moving between
schema and data, finding the smallest coherent unit, validating it, and
recomposing it into its upper context." It is intentionally small — it governs
file-backed state, human views, linking, indexing, blocker/decision/gap
visibility, and recomposition evidence; it ships no command runner, renderer, or
automated index builder today. It is not a global definition authority and not a
generic task executor.

## 2. Storage contract

A Craft space lives per-scope under a project (a repo may hold several at once):

```text
.craft/
  ledger.yml          # source of truth (machine-readable YAML)
  index.json          # optional, rebuildable machine index derived from the ledger
  artifacts/          # receipts, handoffs, evidence, reports, exports
CRAFT.md              # human-readable, linked view of the ledger
```

- `.craft/ledger.yml` is **the source of truth**.
- `CRAFT.md` is a **linked human view or summary only** — never authoritative.
  If the two disagree, the ledger wins.
- `.craft/index.json`, when present, is a **rebuildable machine index** derived
  from the ledger; it must point back to row IDs, never redefine row content, and
  must not be made more authoritative than `ledger.yml`.
- `.craft/artifacts/` holds receipts, handoffs, validation evidence, and
  supporting material.

The ledger also carries an embedded `indexes` section with at least: `by_id`,
`open_decisions`, `blocking_decisions`, `active_blockers`, `active_gaps`,
`next_moves`, and `artifacts_by_path`. Every row has a stable ID and enough
description to be useful outside its original conversation; references between
rows use valid IDs or explicit `links: [{label, target, kind}]`.

## 3. Core methods and their key invariants

| Method | What it does |
| --- | --- |
| `start_project` | Resolve workspace first; write root context, description, candidate definitions, first `next_move`. Returns root `context_id` and ledger path. |
| `state` | Read-only. Returns context stage/gate, latest description, blockers, enablers, open decisions, gaps, definitions, children, recomposition status, current `next_move`. For "all status / pending" requests, returns **every** discovered Craft space with a `Pending by node` section — never collapsed to counts. |
| `describe` | Write a description row; **preserve description history**. |
| `add_blocker` | Write a typed blocker (summary, `blocker_type`, `lane`, evidence, `closure_condition`, role hints). |
| `refine_blocker` | Update a blocker to `refinement_status: refined`, supplying closure criteria (not closure evidence). |
| `add_enabler` | Write an enabler typed item and optional `enables` relation. |
| `next` | Set one current context `next_move` (route, evidence). |
| `open_decision` | Write an active decision row (question, options, blocking flag, impact, links). |
| `decide` | Close a decision with `selected_option`, `rationale`, `evidence`; retain question/impact. |
| `add_gap` | Write an active gap (summary, severity, treatment, owner_route, evidence). |
| `add_definition` | Write a **candidate local** definition row. |
| `open_child_context` | Write a child context with parent and `recomposition_target`. |
| `link` | Write a typed relation between rows. |
| `validate` | Return `pass`, `flag`, or `block` with evidence and residue. |
| `recompose` | Write a recomposition record (child→parent, evidence, `parent_fit_summary`, `next_parent_move`). |
| `export_ledger` | Write the human-readable `CRAFT.md` view. |

Key invariants (quoted exactly):

- "raw blockers cannot be resolved directly" — a raw blocker must first be typed
  and refined, or explicitly waived by a human/governance decision.
- "refinement supplies closure criteria, not closure evidence by itself."
- "if `requires_human` is true, closure needs decision, policy, or human
  evidence; route-shape validation alone is not enough."
- blocking decisions "stop dependent execution until closed, waived, or
  deferred."
- "local definitions do not become canonical definitions" (promotion is a
  separate authority decision).
- `state` is "read-only."
- "export never replaces `.craft/ledger.yml` authority, and exported row IDs
  remain navigable."
- `CRAFT.md` must never be made the source of truth.
- "dispatch validation proves route shape, not execution" — route-shape evidence
  ≠ execution evidence.
- a child context cannot be closed without **recomposition evidence**.
- "lane names the responsibility type; role fields suggest local handlers but do
  not assign authority without owner, decision, policy, route, or receipt
  evidence."

## 4. The recursion (child contexts) and why it matters

Craft is built for **projects inside projects**. A context is a bounded
development space with its own purpose, stage, gate, artifacts, blockers,
enablers, decisions, gaps, and next move. A context may contain **child
contexts**, each with its own state — and contexts also relate **across
branches** (cross-context blockers, enablers, dependencies, supersession) via
typed `relations`, not only parent/child containment. This is the **recursive
ledger**.

A child context typically opens to investigate or refine a blocker, run a
review, or produce a proof. It is **not done when its files change or its gate
passes** — it is done only when the parent ledger records, via `recompose`, what
changed upstream (`parent_fit_summary`, `next_parent_move`, evidence). This
matters because it separates **child progress from parent readiness**: a child
review can pass (`gate: pass`, `stage: closed`) while the parent root stays
`flag` because residue remains. Work cannot silently vanish without parent fit,
and the project never pretends the whole thing is ready just because one slice
closed.

## 5. Residue and the typed ledger

The unifying idea is that **what is not yet resolved stays tracked and visible**.
Translating intention into artifacts always leaves **residue** — "meaningful
mismatch, loss, ambiguity, contradiction, unexpressed structure, scope pressure,
or validation gap." Craft refuses to drop residue: it surfaces it as blockers,
gaps, open decisions, and recomposition residue, and keeps it visible "until
closed, waived, deferred, or routed."

State is **typed**, not free prose:

- **Blocker types** (base condition types) name the cause:
  `decision_blocker`, `definition_blocker`, `design_blocker`,
  `dependency_blocker`, `artifact_blocker`, `validation_blocker`/`evidence_blocker`,
  `authority_blocker`, `resource_blocker`, `sequence_blocker`,
  `recomposition_blocker`. There are parallel base **gate types** and **enabler
  types**, plus optional context-specific subtypes (e.g.
  `ledger.cross_context_relation_blocker`).
- **Lanes** name the *responsibility type* needed: `business`, `tech`, `qa`,
  `validator`, `auditor`, `governance`, `planner`, `operations`, `integrator`,
  `blocker_refiner`. A lane is a responsibility category, never a person, tool,
  or final delegation route.
- **Role hints** (`default_role`, `allowed_roles`, `delegation_route`,
  `requires_human`, `role_confidence`) suggest local handlers but are **advisory**
  until backed by owner policy, a decision, a route contract, a receipt, or human
  evidence. The intended future shape is
  `condition type + lane -> role -> responsible capability or human`, but role
  delegation automation is deferred.
- **Decisions** carry question, options, blocking state, selected option,
  rationale, impact, and evidence; **gaps** carry severity, treatment, owner
  route, and evidence.

This is why a blocker has "a shape instead of a mood": every row records *why* it
can be trusted (or not) and *what* would close it.

## 6. A concrete worked example (product-launch fixture)

A product launch has an API boundary question and missing pilot evidence. The
ledger (`examples/product-launch-ledger.yml`, view in `product-launch-CRAFT.md`)
shows a tiny end-to-end run:

1. **start_project** → root context `CTX-PRODUCT-LAUNCH-ROOT` ("Product launch
   readiness", `stage: plan`, `gate: flag`), with a description and candidate
   definitions (`DEF-READINESS-SLICE-001`, `DEF-CONTRACT-BOUNDARY-001`).
2. **add_blocker** → `BLK-PILOT-EVIDENCE-001`, an `evidence_blocker` on lane
   `validator`: "launch readiness cannot pass until at least one pilot evidence
   receipt exists." Closure condition: a pilot run produces a receipt satisfying
   the launch evidence checklist.
3. **open_child_context** → `CTX-PRODUCT-LAUNCH-API-REVIEW`, a child to resolve
   the API boundary, with `recomposition_target` = the root.
4. **open_decision / decide** → `DEC-API-BOUNDARY-001` ("Which API boundary
   should the launch slice use?") is closed with selected option
   `narrow-contract-adapter`, rationale, impact, and evidence
   (`docs/decisions/api-boundary.md`); a `receipts/api-contract-review.json`
   handoff receipt backs the child review.
5. **refine_blocker** → `BLK-PILOT-EVIDENCE-001` becomes `refinement_status:
   refined` (typed, lane-owned, closure condition set), routed to `task-session`.
6. **add_gap** → `GAP-SEED-DATA-001` (`severity: flag`, `treatment: plan`):
   "seed data exists only as a fixture and has not been checked against a live
   pilot run."
7. **next** → root next move: "Run the first pilot-evidence task and attach the
   receipt to BLK-PILOT-EVIDENCE-001."
8. **recompose** → `CTX-PRODUCT-LAUNCH-API-REVIEW` (now `stage: closed`,
   `gate: pass`) recomposes into the root with the selected boundary as evidence.
   **The child passes, but the root stays `flag`** because residue remains:
   `BLK-PILOT-EVIDENCE-001` and `GAP-SEED-DATA-001`.
9. **validate** → ledger is structurally valid but readiness is `flag` (pending
   work remains); indexes (`active_blockers`, `active_gaps`, `next_moves`, etc.)
   reflect the residue.
10. **export_ledger** → `CRAFT.md` renders quick links, contexts, blockers,
    decisions, gaps, route evidence, and the recomposition note, all as
    navigable anchors back to row IDs — a view, never the source.

The lesson the fixture teaches: Craft "lets one part of the work pass without
pretending the whole project is ready."
