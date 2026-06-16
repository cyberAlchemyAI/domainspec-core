# DESIGN - Ontologize View-Triad Method

Design-mode artifact. Converts [SPEC.md](SPEC.md) into a six-view architecture bundle for the method extension, including the branch materialization refinement in [BRANCH-MATERIALIZATION.md](BRANCH-MATERIALIZATION.md).

## Design Intent

The method turns Ontologize from "ontology+DAG plus BI optimization chains" into a broader governed explanation and decision system. It adds the view triad as the authoring path that makes a target understandable, decidable, and type-safe before claims are packaged for clients or reused by agents.

The refinement decision is that each view is a materialization of ontology branches: B1 meaning, B2 system, B3 run-context, and B4 bridge. The method constrains the existing triad with branch coverage evidence instead of introducing a fourth `branch-view`.

## View 1 - Context

Ontologize currently takes a source corpus or client operating context, builds an ontology+DAG layer, then expresses business intelligence through optimization chains. The view-triad method sits between corpus discovery and BI expression:

```text
source evidence
-> discovery or corpus summary
-> branch materialization register
-> view triad
-> optimization chains
-> client/package/agent handoff
```

Actors:

- Owner or operator: approves method use, product-facing edits, and any client-data work.
- Author: runs the default single-author view triad path.
- Optional peer wave: explorer, skeptic, writer, auditor through `domainspec-subagents-strategy`.
- Client or stakeholder: consumes the resulting shape, decisions, and typed ontology.

## View 2 - High-Level Structure

```text
Method Boundary
  -> Source Inventory
  -> Branch Materialization Register
  -> System View Authoring
  -> Engineer View Authoring
  -> Ontology View Authoring
  -> Integration and Validation
```

Components:

| Component | Owns | Primary Skill |
| --- | --- | --- |
| Method boundary | Eligibility, source scope, output paths, dispatch mode | `domainspec-interview-kits`, `domainspec-decision-gate` if blocked |
| Source inventory | Bounded selectors, evidence anchors, sibling source list | `domainspec-context-builder` |
| Branch materialization register | B1/B2/B3/B4 selectors mapped to consuming view authority | `domainspec-context-builder`, `ontology-view` for edge legality |
| System-view pass | Branch-shaped stakes, tensions, live stances, no verdicts | `system-view` |
| Engineer-view pass | Branch-boundary decisions, schemas/contracts, runtime mechanics | `engineer-view` |
| Ontology-view pass | Typed branch nodes/edges, forbidden-edge guards, schema graph | `ontology-view` |
| Integration pass | Deliverable references, optimization-chain links, validation and signals | `domainspec-task-session`, `domainspec-emit-signals` |

## View 3 - Low-Level Components

### 3.1 Method Boundary Record

Required fields:

- target name and source corpus path;
- intended audience;
- output path decision;
- source freshness decision;
- dispatch mode: `single`, `task-fan-out`, or `zig-zag`;
- sibling availability: discovery, system-view, engineer-view, ontology-view;
- product-facing mutation status: blocked, proposed, or approved.

### 3.2 Source Inventory

The source inventory is a selector table, not a transcript dump. It records:

- source file;
- relevant heading or selector;
- claim/decision/term role;
- which view consumes it;
- freshness or authority note.

### 3.3 Branch Materialization Register

The branch materialization register is created after the source inventory and before view authoring. It is run evidence, not a replacement for `ONTOLOGY-BRANCHES.md`.

Required coverage:

- B1 meaning: intended policy, rule, value claim, outcome, or stakeholder meaning.
- B2 system: implementation artifact, runtime behavior, record, event, metric, test, or gate.
- B3 run-context: run boundary, denominator, lifecycle state, scope/posture, and stage-vs-outcome separation.
- B4 bridge: governed bridge edge, evidence gap, raw drift signal, adjudicated contradiction, test link, or owner-decision route.

The full register schema is [BRANCH-MATERIALIZATION.md](BRANCH-MATERIALIZATION.md).

### 3.4 B3 Run-Context Record

B3 is load-bearing. The method blocks publication when the pilot cannot state:

- run boundary;
- denominator and interpretation limit;
- lifecycle state;
- scope/posture;
- stage-vs-outcome check;
- source events;
- unresolved run-boundary owner decision.

### 3.5 B4 Bridge Ledger

B4 records cross-branch evidence through the edge catalog in [../../DAG-AND-METRICS.md](../../DAG-AND-METRICS.md). It separates raw drift from adjudicated contradiction and records the owner-decision route for promotion blockers.

### 3.6 View Artifacts

The pilot output should be:

```text
projects/ontologize/view-triad/
  branch-materialization-register.md
  system-view.md
  engineer-view.md
  ontology-view.md
  validation-report.md
```

The path is proposed, not yet mutated by this pack.

### 3.7 Integration Artifacts

Integration should add method references only after the pilot triad passes:

- `projects/ontologize/VIEW-TRIAD-METHOD.md`
- optional links from `README.md` and `OPTIMIZATION-CHAIN-METHOD.md`
- optional deliverable references where claims depend on shape, verdict, or typed ontology

## View 4 - Workflow Process

```text
1. Select target and source boundary.
2. Build source inventory.
3. Create Branch Materialization Register for B1/B2/B3/B4.
4. Record B3 run-context fields and B4 bridge ledger candidates.
5. Author system-view.
6. Extract every named stance.
7. Author engineer-view decision rows for each stance and branch boundary.
8. Verify authorities; strike and downgrade unverifiable RESOLVED rows.
9. Author ontology-view terms, nodes, edges, and guards.
10. Cross-check no double decision:
   - system-view has no verdicts;
   - engineer-view has no definitions;
   - ontology-view has no duplicate verdicts;
   - optimization chains cite instead of restating.
11. Validate branch gates:
   - B1 meaning has source/authority coverage;
   - B2 system has event/source/mechanic coverage;
   - B3 run-context has boundary, denominator, lifecycle, scope/posture, and stage-vs-outcome separation;
   - B4 bridge uses catalogued edges or explicit route/blocker.
12. Emit validation report.
13. Only then propose public/product doc integration.
```

## View 5 - Decision Flow

| Decision | Options | Current Selection | Evidence |
| --- | --- | --- | --- |
| What is the method target? | Ontologize itself, client, sub-project, research corpus | Ontologize itself first | Existing docs are available and non-client-sensitive. |
| What path should hold the pilot triad? | `view-triad/`, `development/view-triad-method/pilot/`, deliverable folder | Proposed `projects/ontologize/view-triad/` | Keeps method output near project, separate from development pack. |
| What dispatch mode should be default? | single, task-fan-out, zig-zag | single | Sibling skills default heavy dispatch to opt-in. |
| When can product docs be edited? | immediately, after L0, after full pilot | after L0 method boundary passes | Protects existing public/internal docs. |
| How does this compose with optimization chains? | replace, append, cite selectively | cite selectively | Optimization chain remains BI-expression layer. |
| Is branch materialization a fourth view? | new branch-view, constrain existing triad, ontology-view only | constrain existing triad | Prevents authority drift while making B3/B4 validation explicit. |
| Where do branch definitions live? | method pack, branch register, `ONTOLOGY-BRANCHES.md` | `ONTOLOGY-BRANCHES.md` | The method pack records coverage evidence only. |
| How are drift and contradiction separated? | one bridge status, raw/adjudicated split | raw/adjudicated split | Raw drift is evidence; adjudicated contradiction is a promotion blocker. |

## View 6 - Dependency Interface

| Interface | Direction | Contract |
| --- | --- | --- |
| Ontologize docs -> method pack | source | Read-only during planning. |
| `ONTOLOGY-BRANCHES.md` -> branch register | source | Owns branch definitions and branch interaction language. |
| `DAG-AND-METRICS.md` -> B4 bridge ledger | source | Owns edge catalog, event model, metrics, and drift/contradiction graph rules. |
| Sibling view skills -> method execution | instruction | Use their division of law exactly. |
| `domainspec-subagents-strategy` -> optional dispatch | orchestration | Only for contested/high-risk runs and with operator approval. |
| `domainspec-task-session` -> implementation | execution | Runs one SWU, updates work-pack evidence. |
| `domainspec-emit-signals` -> telemetry | observer | Appends DomainSpec pipeline signals after actual view runs. |
| Optimization-chain method -> BI integration | downstream consumer | Cites shape/verdict/ontology where needed, but does not decide twice. |

## Glossary Consistency

Status: pass-for-planning.

Terms introduced here are local to [GLOSSARY.md](GLOSSARY.md). No canonical term promotion is performed.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| View triad becomes another pile of docs. | medium | Require validation report and no-double-decision checks. |
| Engineer-view overclaims RESOLVED rows. | high | Authority-strike pass is mandatory. |
| Ontology-view coins project-local edges without route. | medium | Mark project-local/proposed-unfiled and carry OQs. |
| B3 run-context disappears into generic context. | high | Require B3 run-context record and publication-blocking validation gate. |
| Raw drift is treated as adjudicated contradiction. | high | Require B4 bridge ledger and authority map. |
| Product docs drift from development method. | medium | Block product edits until L0 method boundary passes. |
| Heavy dispatch is overused. | low | Default to single-author path; opt into `domainspec-subagents-strategy` only when contested. |

## Next Route

`plan` artifact: [PLAN.md](PLAN.md). Execution owner after planning: `task-session`.
