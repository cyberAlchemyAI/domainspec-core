---
tags: [cyber-alchemy-space, architecture, research, unification, ontology, two-lane]
node_type: findings
is_session: false
layer: architecture
nature: reference
status: draft
created: 2026-06-16
dispatch_id: 2026-06-16-cyber-alchemy-space-architecture
dispatch_type: research
working_folder: research/cyber-alchemy-space/
sources: [C:/Users/victo/Arcanum, C:/Users/victo/domainspec, C:/Users/victo/domainspec-core]
---

# Findings — Cyber-Alchemy-Space Unified Architecture (FINAL, corrected)

> **Honesty contract.** Every claim is tagged **BUILT** (on disk, shipped), **OWNED** (canonical
> doctrine, cited), **PROPOSED / novel-attempt** (synthesis, not yet owned), or **OPEN
> owner-decision** (a fork the owner must resolve). The first synthesis over-claimed; this revision
> retracts those over-claims after a 3-skeptic adversarial pass (precedent / non-vacuity /
> definitional) verified against on-disk evidence. See [research.md](research.md) for the raw returns.

## Part 1 — Build-from-OWNED (reuse as-is, do not reinvent)

1. **Engine + law compose only in the private parent.** Public `arcanum` = deterministic resolver/validator/native skills; private `implementation/domainspec` = formal behavior law; the umbrella parent composes them. Source: `SUBMODULE-DISCIPLINE.md`, `CLAUDE.md`. **OWNED.**
2. **The four ontology branches** — B1 meaning / B2 system / B3 run-context / B4 bridge, governed independently, connected by a single bridge-edge catalog. Source: `projects/ontologize/ONTOLOGY-BRANCHES.md`, `DAG-AND-METRICS.md §3`. **OWNED.**
3. **The view triad as the BUILT materialization method** — `ontology-view`/`system-view`/`engineer-view` (the `paired-views` spell) materialize the 4 branches; `BRANCH-MATERIALIZATION.md:107` **forbids** a standalone `branch-view`. hellbender uses this triad. **BUILT.**
4. **The two-lane delivery model** — Lane A (per-run object spine) / Lane B (cross-run knowledge + runtime). Source: `DELIVERY-LANES.md`, `LANE-B-DESIGN.md`. **BUILT/OWNED.**
5. **Governance spine** — single-owner principle + document-class precedence (`implementation/domainspec/AUTHORITY-MAP.md`); definitions/constitution governance; dispatch registration (`telemetry/agents/subagents-dispatch.yaml`, the `register-dispatch`/`domainspec-subagents-strategy` chain). **OWNED.**
6. **Recursive self-application (invariant I9)** + **tier-A (per-run) vs tier-B (cross-run)** — "every stage is the same process at a different altitude; the pipe runs on itself" (`framework-unification/CONCEPT-MAP.md:147`; tiers in `components/ARTIFACTS.md`). Reuse these instead of inventing a lifecycle. **BUILT.**

The **substrate chain** `inventory → ontology-vault → context-builder` (Arcanum `spells/ontology-harness`) and the **artifact-shape constitutions** (`Arcanum/framework/ARTIFACT-CONSTITUTION.md`, `ARTIFACT-METADATA-CONSTITUTION.md`, `CYBERALCHEMY-METHOD.md`) are the engine spine — **OWNED**, reuse, never re-vend.

## Part 2 — The unified architecture

### 2.1 What a cyber-alchemy-space is (honest differentiator)
A **cyber-alchemy-space** = the **per-context application** of the (Arcanum engine + domainspec law) composition, governed uniformly by the ontology/branch discipline, the two-lane model, and the artifact catalog. The definitional skeptic is right that, absent a real differentiator, this collapses into "the private umbrella parent repo." Its genuinely-novel candidate differentiator is **"ontology branches ARE the directory tree" (branch-as-view)** — which is the OPEN decision in §2.2. **So the space's distinctness DEPENDS on branch-as-view landing.** novel-attempt, conditional.

### 2.2 View model — BUILT triad (canonical) vs branch-as-view (target)
**CANONICAL (BUILT):** the 3-sibling triad materializes the 4 branches; coverage is many-to-many (the `BRANCH-MATERIALIZATION.md` register), not one-view-per-branch; a standalone `branch-view` is forbidden.

**TARGET (OPEN owner-decision, novel-attempt):** "branch-as-view" — the ontology IS the tree, **FOUR** views:
```
meaning-view  = B1 meaning
engineer-view = B2 system
run-view      = B3 operational / run-context
residue-view  = B4 bridge / residue
```
Source: `refinement-runs/20260615T211104Z-branch-as-view-ontology/RESULT.md` — which states **"Runtime-backed refine stages have not run"** (an UNRUN proposal, four views). *(The first draft wrongly drew five by keeping both system-view and engineer-view for B2 — retracted.)*

**Naming-collision resolution:** the B1 branch artifact is renamed **meaning-view** (the ontology is the whole tree, so the leaf cannot be "ontology-view"), but the **SKILL keeps the name `ontology-view`** — renaming it would strand its forbidden-edge-unconstructibility differentiator.

**Migration path (novel-attempt):** owner ratifies branch-as-view (lifting the forbid clause) → rename B1→meaning-view, B2→engineer-view, add B3 run-view + B4 residue-view → run the unrun refine stages → re-point hellbender from triad to the four-view tree.

### 2.3 spec ≠ system-view (the user's equation, answered)
**FALSE.** `spec` is the formal behavior contract (composite tier-A; nearest **engineer-view's schema/contract lane**). `system-view` names stances and **decides none**. And the pipeline order is `discovery → paired-views → … → spec` — **views PRECEDE spec** (spec ≈ stage 5), so "spec feeds system-view" is inverted; views feed spec. **OWNED order.**

### 2.4 run-view (B3) — NET-NEW gap, not a shipped object
On a code-less context, run-view is **EMPTY**: hellbender has 0 code, 0 pilot; the only run-trace is the research fanout (run-context of producing the doc, not of the subject system) — filling run-view from it would commit a forbidden cross-branch edge. No producer skill exists (Lane B `[H]` hard gap). **OQ, not shipped.**

### 2.5 residue-view (B4) — embedded today; extraction is a choice
Residue already exists EMBEDDED as `## Residue ledger` sections inside `hellbender/ontology-view.md:163` and `engineer-view.md:188`. A standalone `residue-view` file creates a single-owner conflict. **OPEN:** keep embedded (default) or extract with single-owner discipline.

### 2.6 Artifact catalog — two independent axes, not a clean grid (novel-attempt)
**Provenance class** (Arcanum Source/Durable/Generated/Local-Runtime) and **role tier** (core A/B/C/D, `components/ARTIFACTS.md`) are two REAL but INDEPENDENT axes. Artifacts carry **multiple provenance facets** — hellbender `receipts.md` is Source+Runtime; `dispatch.json` is Source+Durable+Runtime. **Adopt a PRIMARY-class rule OR accept multi-tag.** Not a clean single-cell grid; not owned.

### 2.7 Authority rule — principle OWNED, algorithm PROPOSED
`AUTHORITY-MAP.md` owns the **single-owner principle** + **document-class precedence** (research defs > impl root > `plan/` > feature packs). The mechanical tie-break (**nearest-`.git` / highest-VERSION / longest-PATH / vendored-never-outranks**) is **absent** from AUTHORITY-MAP (grep-confirmed) — cite it as a **PROPOSED extension**, never attribute it to AUTHORITY-MAP.

### 2.8 Lifecycle — drop "orthogonal lifecycles"
The "Orient→Discover→Shape→Stabilize→Evolve" loop appears **nowhere** in the repos — dropped. Reuse **I9 recursive self-application** + **tier-A/tier-B**. The knowledge ladder and delivery pipeline are **COUPLED** (one shared signal stream, `TUNING-LOOP.md`), not orthogonal.

## Part 3 — Consolidated OPEN owner-decisions

| # | Decision | Status | Owner must decide |
|---|----------|--------|-------------------|
| OD-1 | **branch-as-view vs triad** | Triad BUILT; branch-as-view UNRUN (4 views) | Ratify branch-as-view (lifts the `BRANCH-MATERIALIZATION.md` forbid) or keep triad. The space's distinctness depends on this. |
| OD-2 | **run-view (B3) producer** | No producer; empty on code-less contexts | Define a run-view producer + the legal run-trace source (subject runtime, not doc-production fanout) |
| OD-3 | **residue-view embedded vs extracted** | Embedded today | Keep embedded or extract with single-owner discipline |
| OD-4 | **catalog primary-class rule** | Multi-tag reality, no rule | Adopt PRIMARY-class rule or accept multi-tag |
| OD-5 | **authority tie-break algorithm** | Principle owned; algorithm PROPOSED | Adopt/reject the path/git tie-break as an AUTHORITY-MAP extension |
| OD-6 | **spec / system-view** | **ANSWERED** | spec ≠ system-view; spec ≈ engineer-view schema lane; views precede & feed spec |

## Part 4 — Ontologize pilot tree (current built model + branch-as-view migration)

```
projects/ontologize/
├── ONTOLOGY-BRANCHES.md          # OWNED: B1 meaning / B2 system / B3 run-context / B4 bridge
├── DAG-AND-METRICS.md            # OWNED: single edge catalog (§3)
├── development/
│   ├── view-triad-method/        # BUILT METHOD (canonical)
│   │   └── BRANCH-MATERIALIZATION.md   # triad materializes 4 branches; FORBIDS branch-view (L107)
│   └── refinement-runs/20260615T211104Z-branch-as-view-ontology/
│       └── RESULT.md             # TARGET (UNRUN): meaning/engineer/run/residue = 4 views
└── clients/hellbender/           # uses the BUILT triad on a code-less context
    ├── ontology-view.md          #   embeds ## Residue ledger (L163)
    ├── system-view.md            #   names stances, decides none
    ├── engineer-view.md          #   schemas/decisions; embeds ## Residue ledger (L188)
    └── sessions/hellbender-research-receipts.md   # doc-production run-trace != subject run-view

        ── MIGRATION (OD-1, if owner ratifies) ──>

    clients/hellbender/           # branch-as-view: the ontology IS the tree (4 views)
    ├── meaning-view.md           # B1   (artifact renamed; SKILL stays `ontology-view`)
    ├── engineer-view.md          # B2
    ├── run-view.md               # B3   NET-NEW — needs producer (OD-2)
    └── residue-view.md           # B4   only if extracted (OD-3); else stays embedded
```

**Bottom line:** the engine/law/two-lane/governance spine and the BUILT view-triad are reuse-ready and owned. Every four-view / catalog-grid / authority-algorithm / lifecycle-loop element from the first draft is either retracted or honestly downgraded to novel-attempt or OPEN owner-decision. **The space is only as distinct as branch-as-view (OD-1) makes it** — that is the single decision that converts this from "the umbrella repo, governed" into a genuinely new object.

## Connections

| Document | Type | Description |
|---|---|---|
| [research.md](research.md) | `derives-from` | Verbatim explorer + reviewer returns. |
| [../../projects/ontologize/ONTOLOGY-BRANCHES.md](../../projects/ontologize/ONTOLOGY-BRANCHES.md) | `cites` | The owned 4-branch model. |
| [../../projects/ontologize/development/view-triad-method/BRANCH-MATERIALIZATION.md](../../projects/ontologize/development/view-triad-method/BRANCH-MATERIALIZATION.md) | `cites` | The BUILT triad method (forbids branch-view). |
| [../../projects/framework-unification/components/ARTIFACTS.md](../../projects/framework-unification/components/ARTIFACTS.md) | `cites` | The A/B/C/D tier catalog. |
