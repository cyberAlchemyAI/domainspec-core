# REVIEW-QUINE — Definitional Soundness Review

## Verdict

**Revise before acceptance.** The synthesis strongly preserves owner and authority boundaries, but its ontology is not yet definitionally closed. The principal defect is that several distinct kinds are discussed without an explicit non-collapse rule, while `augmentor.experience` is allowed to own “cross-package presentation relations.” That phrase risks turning a view package into a semantic relation owner.

The draft is sound enough to continue as a candidate after the repairs below. This review grants no implementation, promotion, or acceptance authority.

## Non-collapse matrix

| Kind | Defining identity | May reference/project | Must not collapse into | Update authority |
| --- | --- | --- | --- | --- |
| System | Runtime/container boundary and owned host behavior | agents, interfaces, capabilities | agent, page, graph | system owner |
| Agent | Actor/interface identity with bounded behavior | capabilities, APIs, context | system, UI experience, capability | agent owner |
| Capability | Permission/action vocabulary; not possession or grant | declaring agent/add-on, enforcing host | agent, API, authorization decision | capability vocabulary owner; grants remain host/policy-owned |
| Add-on | Installable/registrable extension identity | SDK declarations, capabilities, surfaces | SDK, capability, agent | add-on owner; installation/grants external |
| SDK | Contract/declaration/validation vocabulary | add-ons, protocols, host adapters | runtime, API, grant, implementation success | SDK owner |
| API | Versioned host interface and adapter contract | requests, responses, capability enforcement | SDK, agent, authority | host/API owner |
| Ontology package | Versioned semantic ownership and compatibility boundary | owned nodes and declared relations | filesystem directory, compiled graph, view | package owner |
| Cross-package relation | Typed assertion with declaring owner, endpoints, evidence, status, direction | nodes in allowed imported packages | view edge, containment, ownership transfer | declaring package owner; endpoint owners do not become co-owners by reference |
| Experience projection | Disposable, digest-bound rendering/query projection | package records and source selectors | canonical ontology, runtime state, authority | regenerated from owners; never hand-promoted into truth |
| Documentation page | Human-facing rendering and interaction surface | experience projection, API | ontology package, source record, proof | page owner; content refresh must follow projection regeneration |
| Source record | Revision-bound evidence object with provenance and sensitivity | concepts, claims, selectors | ontology concept, memory index entry, authority decision | Living Archive/source owner |
| Memory index | Retrieval aid pointing to source records | source handles and freshness state | source record, semantic truth, review state | index/runtime owner; invalidation follows sources |
| Authority decision | Explicit review/policy act with actor, scope, time, and receipt | candidate records/packages | status label, API result, retrieval hit, page action | designated verifier/policy owner only |

## Query-direction checks

**Pass with repairs required.**

- The runtime path is explicit and read-only: page/consumer → API → authenticated bridge → capability check → installed projection → search/context → evidence/limits → consumer composition or abstention (`SYNTHESIS-DRAFT.md:244-269`).
- Source retrieval is defined as source-identity resolution with safety filtering, conflict preservation, reasons, freshness, limits, and abstention (`:227-230`).
- The graph query surface is underspecified. Filters and a textual relation list are promised (`:160-172`), but every result must expose: `record_id, kind, package_owner, relation_owner, source_handles, projection_digest, statuses, freshness, limitations`.
- Reverse traversal must be explicitly derived. An inverse edge must never be stored or shown as a second owner assertion unless the predicate contract declares an inverse.
- Queries over a view must resolve back to owner records and source selectors. A view-local edge alone is not evidence.

## Update-direction checks

**Fail until made explicit.**

Required direction:

```text
owner source change
→ source record revision/invalidation
→ affected owner package record status change
→ cross-package relation invalidation by dependency
→ compiled projection regeneration with new digest
→ documentation page refresh
```

Forbidden reverse direction:

```text
page edit / graph drag / query result / API success / retrieval hit
↛ source record mutation
↛ package semantic mutation
↛ capability grant
↛ review or promotion
↛ authority decision
```

The witness correctly exercises source-digest change through stale concept, relation, and view (`:271-293`), but it does not name who may perform each transition. Add `updated_by`, `update_basis`, `depends_on`, and `invalidation_receipt` to every mutable semantic record. The page may submit a separate intake request, but it may not directly update source, index, ontology, relation, or authority records.

## Exact challenges and repairs

1. **Status vocabulary lacks applicability and actor semantics**  
   Selector: `SYNTHESIS-DRAFT.md:30-40`.  
   Repair: define which axes apply to which kinds. An authority decision should not itself be “promoted”; an API route should not receive semantic promotion status by default. Add `not_applicable` or per-kind admissible-value constraints. Define the actor/receipt required for every semantic transition.

2. **Capability is conflated with capability environment and enforcement**  
   Selectors: `:12-16`, `:49-53`, `:83-86`, `:189-193`, `:244-269`.  
   Repair: define capability as vocabulary/declaration, capability grant as a separate host/policy record, and enforcement as runtime behavior. SDK declaration, host grant, and bridge enforcement must be separately queryable.

3. **Experience package risks owning semantic cross-package truth**  
   Selectors: `:103-118`, especially `:112`; predicate rules at `:133-142`.  
   Repair: `augmentor.experience` may own only view definitions, layout, annotations, and derived edge instances carrying `derived_from`. Semantic cross-package relations must be owned by the declaring source package. Rename “cross-package presentation relations” to “derived presentation edges.”

4. **Relation identity is underdefined**  
   Selectors: `:120-137`.  
   Repair: require `subject`, `predicate`, `object`, `declaring_package`, `source_handles`, `status_axes`, `direction`, `cardinality`, `valid_from`, `invalidated_by`, and optional declared inverse. Relation IDs must not be minted merely because a view draws an edge.

5. **Legacy alias rule can preserve false identity**  
   Selectors: `:129-131`, acceptance criterion `:301`.  
   Repair: an alias is allowed only for same referent, same meaning, and same owner. Otherwise use `supersedes`/`replaced_by`; never an alias. Query responses must label aliases and return the canonical ID.

6. **Source record and memory index are not separated**  
   Selectors: `:57-59`, `:107-112`, `:217-242`.  
   Repair: define source record as evidence-bearing revisioned content metadata; define memory index as a disposable retrieval structure pointing to it. Index rebuilding cannot alter source meaning or review status.

7. **Authority decision has no first-class record kind**  
   Selectors: `:57-59`, `:232-242`, `:267-269`, `:295-319`.  
   Repair: add an authority-decision record with decision ID, actor/role, candidate digest, scope, decision, policy basis, timestamp, expiry/withdrawal, and receipt. Status text alone is not authority evidence.

8. **Robot/body visual versus technical proof boundary is implicit**  
   Selectors: `:174-183`; evidence display at `:195-209`.  
   Repair: label the robot/anatomy visual as an explanatory metaphor whose cards link to technical records. Only the technical graph plus owner record, source selector, status, and digest may support a technical claim. Shape, proximity, body part, color, or animation must never imply containment, ownership, execution order, authority, or runtime presence.

9. **Evidence matrix is not source-local enough for audit**  
   Selectors: `:321-342`, especially `:330`, `:332-340`.  
   Repair: replace “cited lines/functions/headings” with repository-relative paths plus stable heading, symbol, JSON Pointer, or line selector for every load-bearing claim.

## Killed alternatives

- **KILL:** `Augmentor = ResonantOS`. An agent-facing experience is not its host system.
- **KILL:** `agent = capability`. An actor may declare/use capabilities; it is not the permission vocabulary.
- **KILL:** `add-on = SDK`. An add-on consumes SDK contracts; validation does not make it the SDK or grant installation.
- **KILL:** `SDK = API`. Declaration/validation contracts and a host invocation interface have different owners and effects.
- **KILL:** `API success = authority`. A successful read proves only bounded interface behavior.
- **KILL:** `Living Archive = Augmentor memory/database`. It remains an external source-memory and review boundary.
- **KILL:** `source record = ontology concept`. Evidence and typed meaning must remain separately revisioned and owned.
- **KILL:** `memory index = source truth`. An index is rebuildable retrieval infrastructure.
- **KILL:** `review state = authority decision`. The decision requires an explicit owner, scope, digest, and receipt.
- **KILL:** `view edge = semantic relation`. Presentation geometry is derived, never canonical.
- **KILL:** `documentation page = experience projection`. The page renders/queries a projection; it does not own its semantic records.
- **KILL:** six logical packages imply six directories or repositories. The draft correctly rejects this (`:22-25`, `:114-118`).
- **KILL:** a unified monolith or view-only graph. The draft correctly rejects both (`:139-142`).

## Residue

Open owner decisions remain: admissible statuses by kind; authoritative owners for cross-package predicate definitions; relation cardinalities/inverses; whether authority decisions live in Living Archive or a separate policy-owned package; physical package placement; legacy-ID migration; and page relocation. The installed projection and live browser/runtime state remain unverified.
