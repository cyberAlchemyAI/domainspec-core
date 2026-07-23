# Design: Evidence-Bound Maintenance Route

Status: approved L1 authoring output

Source contracts: `DEFINE.md`, `GLOSSARY.md`, frozen audit findings

## 1. Context view

```text
accepted audit
    |
    v
Invoke planning package ------------------------------+
    |                                                  |
    +-> private DomainSpec tooling owner -> DSS tasks  |
    +-> Sigil Development -> TS / DG / Inventory -----+-> closure receipts
    +-> Spellcraft -> Invoke / Whisper ----------------+
                                                       |
                                                       v
                                          final cross-capability audit
```

The package coordinates evidence and ordering. It is not a new lifecycle owner
and does not centralize runtime behavior.

## 2. High-level structure view

Every maintenance request follows five components:

1. **Source contract** — accepted finding plus current exact target anchors.
2. **Admission change** — earliest owner-controlled rule that rejects the bad
   state.
3. **Negative-control harness** — at least one bad state that previously passed
   and must now fail, plus a positive compatibility control.
4. **Lifecycle synchronization** — canonical source first, generated/runtime or
   read-model projections second, with public/private separation.
5. **Closure receipt** — result, material artifacts, commands, residue, and next
   owner; no implicit promotion.

The planning-only `ChangeRequestContract` is:

```yaml
id: WFE-Rxx
target_capability: string
lifecycle_owner: sigil-development | spellcraft | private-tooling
source_contracts: [path#selector]
bad_state: string
admission_rule: string
negative_controls: [fixture]
positive_controls: [fixture]
write_scope: [repo-relative path]
generated_or_projection_surfaces: [path]
receipt_fields: [result, artifacts, validation, blockers, residue, reroute]
promotion_authority: explicit owner
```

This envelope keeps tasks comparable but is not implemented as a shared runtime
schema in this generation.

## 3. Low-level component view

| Component | Inputs | Behavior | Outputs | Owner |
| --- | --- | --- | --- | --- |
| DSS admission validator | new dispatch/close record, current ledger, repo root | reject RESERVED input, orphan close, working-agent final approver, or escaped destination; allow duplicate close no-op and historical ledger | stable error or appended row | private DomainSpec tooling |
| Task Session decision/completion guard | decision classification, done criteria, validation results | auto only explicit reversible/nonconsequential choices; block unmet acceptance-critical validation | typed session result | Sigil Development |
| Invoke material-package validator | proposed material delta, paths, digests, dependencies, owner/publication class, approval class | prove actual mutation package before handoff | pass/reject receipt | Spellcraft |
| Inventory kind reconciler | 15 invalid rows, supported enum, path/type role | normalize aliases to supported `entry` or `query`; prevent new invalid kinds | conformant index and updater rejection | Sigil Development |
| Routed readiness consumer | material-package receipt and live state | validate identity/digest/dependency/write/authority bindings before first mutation | admit or rebuild/block | Sigil Development |
| Decision Gate prefilter/override validator | candidate options, target, hazard, owner receipt | present only admissible options; consume typed one-use override without bypassing protected gates | decision or structural block | Sigil Development |
| Dispatch evidence binder | two tension verdicts, sheet digest, confirmation, runtime base/overlays | reject changed/unconfirmed sheet; classify surface differences | registered row evidence and parity report | private tooling + Sigil Development |
| Whisper runtime assembler | canonical base, repository overlay manifest, declared preset payloads, runtime metadata | run canonical generation first, validate declared additive overlays, append only at the repository-extension boundary, and reject deletion/replacement of canonical semantics | generated runtimes and parity receipt | Spellcraft + Arcanum runtime generator owner |
| Inventory projection validator | entry files, indexes, human view, projections, timestamps/digests | bidirectional identity, coverage, existence, and freshness checks | conformance report | Sigil Development |
| Invoke status resolver | mode evidence receipts | compute independent authored/released/runtime-ready ceilings | machine capability status | Spellcraft |

## 4. Workflow process view

```text
select one ready SWU
  -> lifecycle owner accepts scope
  -> Context Builder resolves exact anchors at execution time
  -> run red fixture against current behavior
  -> apply one bounded canonical/private-tool mutation
  -> run focused positive and negative controls
  -> synchronize generated/read-model surfaces from owner source
  -> rerun focused and package regression suites
  -> emit closure receipt
  -> update WORK-PACK state
  -> stop or select the next SWU
```

Public Arcanum tasks commit and validate inside the `arcanum` submodule first;
the parent repository may be updated only after the submodule result exists.

## 5. Decision flow view

```text
candidate state
  |
  +-- structurally invalid? --> reject/block; no human preference gate
  |
  +-- exactly one safe owner-admissible route? --> route it
  |
  +-- two or more admissible options? --> Decision Gate
  |
  +-- consequential authority required? --> protected owner gate
  |
  +-- deterministic and already authorized? --> validate and proceed once
  |
  +-- unknown/ambiguous evidence? --> block with exact missing witness
```

An approval never changes `invalid` to `valid`. A validator never changes
`candidate` to `promoted`.

## 6. Dependency and interface view

| Producer | Consumer | Interface | Failure rule |
| --- | --- | --- | --- |
| INV-1 material validator | TS-2 routed admission | readiness receipt with identities/digests/dependencies/writes/validation/authority class | absent or mismatched receipt blocks/rebuilds before mutation |
| DSS-1 admission validator | DSS-2 evidence binder | trusted new-row admission behavior | DSS-2 cannot bind evidence through an appender that still admits forbidden rows |
| INT-1 kind reconciliation | INT-2 projection validator | conformant primary machine index | projection completeness cannot pass over an invalid primary index |
| WH-1 overlay manifest | generated `.agents`/`.claude` runtimes | canonical base digest plus declared preset digests and extension points | undeclared gate/status/authority removal blocks generation |
| every task validator | lifecycle owner | closure receipt | missing negative control or residue blocks lifecycle close |

No execution tasks are parallelized by default. Independent code paths do not
justify simultaneous lifecycle mutation when the maintainer explicitly wants
one change request closed at a time.

## Algorithms and rules

### Canonicalized destination containment

1. Reject absolute paths and explicit `..` segments.
2. Normalize separators and resolve the candidate beneath the repository root.
3. Resolve the repository root with `realpath`.
4. Find the nearest existing parent of a not-yet-created leaf and resolve that
   parent with `realpath`; reject if outside the root.
5. If the candidate exists, resolve it and reject if outside the root.
6. Apply the normalized `vault` prohibition after containment.
7. Return a stable error without appending.

### Inventory kind normalization

```text
path starts entries/ and kind in {strategy-result} -> entry
path starts queries/ and kind in {query-file,research-findings,research-transcript} -> query
otherwise -> block and require explicit schema owner decision
```

The migration must assert the exact before/after count and preserve IDs, types,
paths, sources, tags, selectors, and derived-map membership.

### Status precedence

Status axes are independent booleans/enums. `artifact_authored` may pass without
`registry_released`; `registry_released` may not imply
`mutation_runtime_ready`; no consumer may derive a later axis from an earlier
one without its named receipt.

## Decisions

| ID | Decision | Reason |
| --- | --- | --- |
| WFE-D01 | Keep local owner implementations; do not add a central validation framework yet. | one planning envelope is enough; runtime reuse is not proven |
| WFE-D02 | Normalize the 15 Inventory aliases to current supported kinds. | aliases encode path/type role already represented elsewhere and currently break consumers |
| WFE-D03 | INV-1 must precede TS-2. | producer receipt must exist before consumer admission can require it |
| WFE-D04 | DSS-1 must precede DSS-2; INT-1 must precede INT-2. | later evidence binding/projection proof depends on a valid admission/index base |
| WFE-D05 | No mutation lane runs in parallel. | one-change-at-a-time maintenance is the requested operating rule |
| WFE-D06 | Generated runtimes are canonical base plus declared overlay, not byte-identical copies. | current surfaces contain both stale drift and legitimate extensions |
| WFE-D07 | Closure receipt cannot promote the capability. | lifecycle and human owners retain promotion authority |
| WFE-D08 | Extend the existing bootstrap generator with a narrow optional overlay hook; do not create a second Whisper generator. | `.agents` and `.claude` already come from `arcanum/tools/bootstrap_arcanum.sh`; a side generator would preserve two competing generation paths |

### Whisper overlay authority

`arcanum/spells/whisper/` remains the public canonical base and
`arcanum/tools/bootstrap_arcanum.sh` remains the only runtime generator. The
repository-local machine authority is
`.arcanum/runtime/overlays/whisper/manifest.json` plus its declared payloads.
Generated `.agents` and `.claude` files are migration witnesses and outputs,
never overlay sources. The optional bootstrap hook may only add declared files
or append a rendered repository-extension section; it cannot replace or remove
canonical body content. Generic schema/validator/generator behavior may live in
public Arcanum, while the local manifest and local preset payload remain in the
private parent repository.

## Risks and controls

| Risk | Control |
| --- | --- |
| stricter appender rejects valid new folders | existing-parent realpath/symlink fixtures plus non-existing in-root positive fixture |
| historical ledger becomes unreadable | validate strictness only on new input; grandfather existing rows |
| accepted Inventory information is lost during kind migration | preserve all fields and exact IDs; compare before/after projections |
| Task Session blocks harmless residue | acceptance-critical classification plus retained named noncritical `FLAG` |
| material validator becomes approval theater in code | invalid-plus-approved red fixture and valid-no-extra-approval control |
| overlays become shadow authority | manifest extension points cannot remove canonical gates/status/authority |
| plan becomes a central meta-framework | no shared runtime package and one owner-specific task at a time |

## Design gate

- Six required views: complete.
- Glossary consistency: pass; all new terms remain package-local.
- Source contracts: complete and owner-bound.
- Design Distill: pass; the coherent unit is one evidence-bound maintenance
  request, not all ten changes as a single implementation.
- Upstream/source mutation: none.
- Next route: Plan.
