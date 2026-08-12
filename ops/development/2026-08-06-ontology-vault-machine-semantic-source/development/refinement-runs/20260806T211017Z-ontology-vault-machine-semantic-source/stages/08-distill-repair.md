# Stage 08: Distill Repair And Projection-Drift Toy Game

## Distill Repair Result

- Capability: `distill`
- Mode: `validate` with repair focus
- Input: Stage 06 exact design plus Stage 07 eight-item change list
- Verdict: `pass`
- Recomposition: `pass`
- Remaining evidence state: `authored-complete`
- Executed implementation evidence: none

## Repairs Applied To The Candidate Model

### R1 — One authored relation source

V1 authors relations only as standalone objects in declared relation modules.
Records do not contain authored edge copies. A HumanView or GraphView may show
derived adjacency, and the normalized model may index relations by endpoint,
but those are disposable projections. Existing candidate embedded edges require
an explicit migration into relation records; their field semantics are reused,
not their duplicate storage shape.

### R2 — Conditional record families

Universal record fields are only:

- `record_id`
- `record_kind`
- `title`
- typed `content`
- lifecycle/residue envelope required where the selected record family needs it

`semantic-record.schema.json` selects a closed `oneOf` family by `record_kind`.
Claim, definition, evidence, policy, and PromotionRecord families carry only
their applicable axes. Unknown properties remain rejected outside declared
extensions.

### R3 — Verifiable projection algebra

`ProjectionDefinition` cannot execute arbitrary semantic templates. It declares
a closed operation graph:

| Operation | Input | Output | Rule |
|---|---|---|---|
| `copy_scalar` | one typed field | escaped scalar | exact value after declared escaping |
| `copy_block` | one content block | escaped block | exact block text and ID |
| `format_enum` | one enum plus public label table | label | table digest-bound; no stronger state |
| `join_list` | typed item sequence | delimited list | ordering and delimiter declared |
| `emit_relation` | one source relation | edge/row/link | endpoint/type unchanged |
| `emit_reference` | one evidence ref | citation/link | locator policy declared |
| `structural_token` | public template token | heading/layout | token allowlist; no domain assertion |

Each output emission records the operation and exact inputs. An independent
`ProjectionVerifier` re-executes the operation graph from the normalized model
and compares trace plus output bytes. A trace asserted only by the projector is
not proof.

### R4 — Structural templates cannot carry meaning

Template tokens are limited to headings, punctuation, table scaffolding,
non-authority banners, and accessibility/navigation labels from a public
digest-bound allowlist. Claims, rationale, confidence, lifecycle, evidence, and
relations must flow through semantic operations.

### R5 — Admission is an immutable event chain

Closed event kinds:

- `admit_package_version`: binds exact/canonical digests, exact suite/profile,
  owner, scope, gate, and rollback target;
- `reject_package_version`: binds the candidate and reasons;
- `revoke_admission`: binds a prior admission ID and reason;
- `supersede_admission`: binds prior and new admission IDs.

The current admitted package is a derived query over the acyclic event chain.
No mutable `admitted` flag is source authority.

### R6 — Exact artifact and semantic bindings stay separate

Admission binds both `exact_source_digest` and `canonical_source_digest`.
Formatting-only changes preserve semantic diff and canonical digest but create a
new exact artifact. Reusing the old artifact admission for the new bytes is
invalid; an owner may issue a bounded superseding artifact event without
re-promoting unchanged claims.

### R7 — AuthoringProfile is non-semantic

AuthoringProfile may declare widget choice, labels, help text, grouping, and
layout. It cannot declare semantic defaults, hidden semantic fields, lifecycle
transitions, evidence posture, owner decisions, or projection meaning. Every
semantic value appears explicitly in SourcePatch and its semantic diff.

### R8 — Exact admission target

`read-compatible` allows inspection and migration planning only. A new
AdmissionRecord requires an exact target suite/profile digest and successful
canonicalization/normalization under that target. `partial-with-residue`,
`incompatible`, and `unknown` block cutover.

## Atomic Patch Semantics

SourcePatch validates all preconditions against the same base digest and applies
all operations atomically. Removing a record with surviving relations fails
unless the same patch removes or validly rewrites those relations. Patch
application creates candidate bytes and validation evidence only.

## Projection-Drift Toy Game

This is a designed falsification table, not an executed test run.

Base toy package:

- record `r-source`: claim that human views derive from one semantic source;
- record `r-receipt`: definition of ProjectionReceipt;
- relation `rel-binds`: `r-receipt binds r-source`;
- one Markdown ProjectionDefinition using the closed operation algebra;
- package remains structurally valid but intentionally has no AdmissionRecord.

| Move | Perturbation | Expected observable result | Model verdict |
|---|---|---|---|
| T1 | Compile unchanged package twice | Identical model, trace, and output digests | survives |
| T2 | Reorder JSON keys/whitespace | Exact digest changes; canonical/model/output digests remain | survives |
| T3 | Projector writes “promoted” for candidate record | Independent verifier cannot derive emission; projection fails | survives |
| T4 | Edit generated Markdown | Output digest fails; no source change; correction may become SourcePatch only | survives |
| T5 | Fabricate a trace selector for invented text | Verifier recomputation fails operation/output equality | survives after R3 |
| T6 | Delete `r-receipt` but keep `rel-binds` | Atomic patch/cross-reference validation fails | survives after R1/R8 |
| T7 | Schema-valid package has no AdmissionRecord | View may be previewed as non-authority; package is not admitted | survives |
| T8 | Migration leaves one ID unresolved | Candidate retained as `partial-with-residue`; cutover blocked | survives |
| T9 | Public fixture contains a private namespace/example | Leakage validator fails public bundle | survives by planned negative contract |
| T10 | AuthoringProfile supplies hidden `promoted` default | Profile validation fails; SourcePatch cannot omit semantic operation | survives after R7 |
| T11 | Renderer inserts current time into governed bytes | Repeat digest mismatch; reproducibility fails | survives |
| T12 | Normalized model is submitted as source | Format/source-kind validation rejects it | survives |

## Recomposition And Non-Regression

The repairs preserve one source, humane patch authoring, deterministic views,
distinct authority owners, and copy-and-verify migration. They narrow rather
than widen L0. The operation algebra and independent verifier are required
because a digest-only receipt cannot prove non-invention.

## Remaining Gaps

- Schema, operation-algebra, event, and receipt bytes are still unimplemented.
- Toy-game rows are planned witnesses, not executions.
- Independent Design selection, formal UX validation, and public owner approval
  remain absent.
- The paused RWO identity gate remains untouched.

## Claim Ceiling

Stage 08 repairs the private candidate model. It proves design consistency only;
it does not prove a compiler, validator, human usability, admission, migration,
public convention, or runtime.
