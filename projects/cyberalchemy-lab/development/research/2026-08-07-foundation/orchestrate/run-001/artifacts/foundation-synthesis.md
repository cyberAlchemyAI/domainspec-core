<!-- BEGIN VERBATIM RETURN: spawn-0004 foundation-synthesizer -->

# CyberAlchemy Lab Foundation Candidate

## 1. Project definition

CyberAlchemy Lab is a private, candidate-local research-navigation system that turns one bounded Research Tower snapshot into a selector-bound knowledge view inside the existing IDE workbench.

Its first purpose is modest: let a person inspect a tower’s identity, sources, claims, definitions, residue, gates, and evidence without changing the tower, source corpus, candidate ontology, or any authority artifact.

The intended chain is:

```text
immutable source and tower snapshots
  -> selector-bound evidence
  -> candidate knowledge records
  -> disposable read model
  -> read-only IDE projection
```

A separate owner decision may later create:

```text
candidate claim
  -> PromotionRecord
  -> scoped authority artifact
```

No earlier artifact or successful validation creates that edge.

Binding: `research.md@sha256:29d7a80d1ceeb1823b7bbd74579bf167167d4a66e4b6aa7f04ef6b8139e021e6#L214-L218,L403-L431`; explorer returns `spawn-0002`, `spawn-0003`; scope: current workbench reality and candidate authority model; status: **observed**.

### Non-goals

CyberAlchemy Lab is not:

- an “all research” ingester or completeness claim;
- Inventory, Ontology Vault, a canonical ontology, or a graph database;
- a persona runtime, debate engine, MOGT policy, ELO system, or oracle consensus;
- a replacement for Research Tower construction;
- an execution envelope, approval, protected-effect receipt, or Craft handoff;
- an automatic bridge, promotion, publication, or deployment mechanism;
- a route from private evidence into public Arcanum;
- implemented, promoted, published, deployed, proven useful, or production-ready.

Binding: `research.md@sha256:29d7…21e6#L14-L23,L126-L155,L243-L254,L403-L431,L509-L522`; explorer returns `spawn-0001`, `spawn-0002`, `spawn-0003`; scope: claim and authority ceilings; status: **observed**.

## 2. Corpus contract

### Frozen census

The 2026-08-07 census found 41 `TOWER.md` path occurrences, 33 byte digests, 31 duplicate-collapsed content families, 24 exact current-scaffold occurrences, and 17 custom/nonconforming occurrences. This is only a frozen `TOWER.md` census.

The Tower System source is bound as:

`research/tower-system-taxonomy/Tower-System.pdf@sha256:2318a4066b8146e7073781df7aa62589938789685b6c2c64cf83737613f32f5b`

Its reported page count remains inconsistent: 8 pages in prior metadata and `file(1)`, versus 9 `pypdf` page objects. The digest, not the page count, is the current immutable identity.

Binding: `research.md@sha256:29d7…21e6#L9-L23`; explorer return `spawn-0001`; scope: census and source identity; status: **executed** by explorer.

### Eligibility, identity, version, duplicates, and completeness

| Rule | Foundation candidate | Binding |
|---|---|---|
| Eligibility | A candidate is the package root containing `TOWER.md`. It must express a coherent research target and navigational or contractual spine. Current-scaffold conformance is recorded separately. | `research.md@sha256:29d7…21e6#L25-L31`; `spawn-0001`; corpus classification; **observed** |
| Current scaffold | The witnessed G2 contract contains `README.md`, `TOWER.md`, L0/L1/L2 level files, closure gates, and open residue. Legacy/custom packages may still contain substantial research. | `research.md@sha256:29d7…21e6#L27-L34`; `spawn-0001`; package shape; **observed** |
| Logical identity | `tower_logical_id` must bind owner repository, package-root path, declared lineage, and owner identity. Path, digest, heading text, and list position are insufficient alone. | `research.md@sha256:29d7…21e6#L28-L35,L470-L479`; `spawn-0001`,`spawn-0003`; identity policy; **observed** |
| Snapshot identity | `tower_snapshot_id = H(tower_logical_id, canonical ordered artifact manifest)`. Each artifact entry carries normalized path, digest, byte size, role, availability, and privacy class. | `research.md@sha256:29d7…21e6#L437-L440,L470-L475`; `spawn-0003`; candidate identity contract; **observed** |
| Version | A changed source or artifact produces a new immutable snapshot. `revision_of` or `supersedes` must be owner-asserted and acyclic; prior evidence remains historical rather than being rewritten. | `research.md@sha256:29d7…21e6#L453-L464,L477-L485`; `spawn-0003`; version/invalidation; **observed** |
| Duplicate | Equal bytes prove a copy candidate, not canonical ownership, revision, equivalence, or supersession. Different bytes also do not prove supersession. | `research.md@sha256:29d7…21e6#L31-L35,L453-L458,L477-L479`; `spawn-0001`,`spawn-0003`; duplicate semantics; **observed** |
| Worktree/output copies | Worktrees, fixtures, snapshots, and handoffs remain projections or copies unless an owner establishes new lineage. | `research.md@sha256:29d7…21e6#L29-L35,L42-L123`; `spawn-0001`; occurrence manifest; **observed** |
| Completeness | Every projection declares included artifacts, excluded artifacts, missing required artifacts, and unknown count. It must never infer “all research” from the `TOWER.md` census. | `research.md@sha256:29d7…21e6#L14-L23,L143-L155,L256-L271`; `spawn-0001`,`spawn-0002`; completeness boundary; **observed** |
| Publication class | Only `arcanum/` is public. Other locations remain private/non-public absent separate publication-owner proof. | `research.md@sha256:29d7…21e6#L35-L35,L511-L522`; `spawn-0001`,`spawn-0003`; privacy boundary; **observed** |

### Required package manifest

A loadable tower snapshot requires:

```yaml
tower_logical_id:
tower_snapshot_id:
owner_repository:
package_root:
lineage:
declared_version:
generation: G0 | G1 | G2
research_status:
privacy_class:
publication_class:
source_snapshot_ids: []
artifacts:
  - normalized_path:
    role:
    sha256:
    byte_size:
    availability:
missing_required_artifacts: []
duplicate_candidates: []
owner_asserted_revision_refs: []
residue_refs: []
canonical_order_manifest_sha256:
```

The frozen census is not such a manifest. No candidate currently has a fully transcribed ordered artifact manifest and resulting `canonical_order_manifest_sha256`.

Binding: `research.md@sha256:29d7…21e6#L25-L40,L42-L123,L437-L440,L470-L475`; explorer returns `spawn-0001`,`spawn-0003`; scope: required manifest versus available census; status: **unverified** for the selected witness.

## 3. Tower System ↔ Research Tower crosswalk

| Tower System concern | Existing Research Tower precedent | Foundation disposition | Binding |
|---|---|---|---|
| L1 queryable graph | Markdown spine and cross-links | Partial. Build a disposable bounded read model first; no runtime graph is witnessed. | `research.md@sha256:29d7…21e6#L126-L130,L494-L507`; `spawn-0001`,`spawn-0003`; **observed** |
| L1 persona set | No generated persona schema/artifact | Net-new and excluded from the first witness. | `research.md@sha256:29d7…21e6#L128-L129`; `spawn-0001`; **observed** |
| L2 distill-build | Source → L0/L1/L2 → glossary, definitions, distill, learning pack | Strong owned/executed precedent; reuse the artifact boundary, not an inferred runtime. | `research.md@sha256:29d7…21e6#L129-L130`; `spawn-0001`; **observed** |
| L2 human read-through | No defined human accrual method | Absent; later UX/research concern. | `research.md@sha256:29d7…21e6#L130-L131`; `spawn-0001`; **observed** |
| L2 promote | Research outputs remain local; promotion belongs elsewhere | Preserve as an external owner gate. | `research.md@sha256:29d7…21e6#L131-L132,L509-L522`; `spawn-0001`,`spawn-0003`; **observed** |
| L3 debate/dispatch/application | Governed subagents and closeout ledger | Partial transport precedent only; no reusable persona operation. | `research.md@sha256:29d7…21e6#L132-L133`; `spawn-0001`; **observed** |
| Lφ MOGT | Separate design-stage system | Excluded. | `research.md@sha256:29d7…21e6#L133-L134`; `spawn-0001`; **observed** |
| L4 scoring/adjudication | Claim kinds, bridge status, closure gates, source labels | Research adjudication only; no ELO/oracle-consensus engine. | `research.md@sha256:29d7…21e6#L134-L135`; `spawn-0001`; **observed** |
| Recursion | Decomposition and evidence handoff | Partial; sub-tower identity and cycle guards are not witnessed. | `research.md@sha256:29d7…21e6#L135-L136`; `spawn-0001`; **observed** |
| Evidence boundary | Source-first, local-only, claim ≤ proof | Strong alignment and mandatory for the first witness. | `research.md@sha256:29d7…21e6#L136-L140`; `spawn-0001`; **observed** |

## 4. Candidate ontology contract

All records are candidate-local unless an external owner creates a scoped promotion decision.

| Record family | Candidate role and owner | Authority boundary | Binding |
|---|---|---|---|
| `SourceSnapshot` | Corpus owner records immutable source bytes and provenance. | Path is not identity; snapshot does not assert truth. | `research.md@sha256:29d7…21e6#L437`; `spawn-0003`; **observed** |
| `TowerPackageSnapshot` | Research/corpus owner binds one ordered package manifest. | Package status is not ontology or publication authority. | `research.md@sha256:29d7…21e6#L438`; `spawn-0003`; **observed** |
| `KnowledgeRecord` | Lab candidate compiler preserves witnessed claim, definition, example, residue, gate, or route records. | No inferred “topics”; local IDs are preserved or explicitly registered. | `research.md@sha256:29d7…21e6#L439,L479`; `spawn-0003`; **observed** |
| `EvidenceAnchor` | Evidence owner binds one selector to exactly one source snapshot. | Missing or drifted selectors fail closed. | `research.md@sha256:29d7…21e6#L440,L456`; `spawn-0003`; **observed** |
| `ClaimCandidate` | Research owner proposes one statement with separate evidence and commitment confidence. | Candidate only; contradiction and falsification paths remain live. | `research.md@sha256:29d7…21e6#L441`; `spawn-0003`; **observed** |
| `DefinitionReference` | References the applicable public or private definition owner. | It may not copy, redefine, imply `sameAs`, or cross the public/private boundary. | `research.md@sha256:29d7…21e6#L442,L458,L520`; `spawn-0003`; **observed** |
| `BridgeDecisionRecord` | Named bridge/review owner records `aligned`, `partial`, `drift`, `insufficient`, or `contradicted`. | Pending assessment has `authority_effect: none`; one-sided evidence cannot align. | `research.md@sha256:29d7…21e6#L443,L460,L519`; `spawn-0003`; **observed** |
| `ResidueRecord` | Routed owner records missing/observed state and resolution conditions. | Residue is not automatically a defect. | `research.md@sha256:29d7…21e6#L444`; `spawn-0003`; **observed** |
| `ValidationRecord` | Validator records exact inputs, validator/version, environment, command, and result. | Conformance is not truth, implementation, approval, or promotion. | `research.md@sha256:29d7…21e6#L445,L483`; `spawn-0003`; **observed** |
| `WorkbenchProjection` | IDE owner generates an immutable revision from bound inputs and projection rules. | Disposable read model; no inverse mutation edge and `authority_effect: none`. | `research.md@sha256:29d7…21e6#L446,L459,L463`; `spawn-0003`; **observed** |
| `PromotionRecord` | External ontology/authority owner decides one primary claim. | Default fixture gate is `block`; only the named owner can create `approved_by` or `promotes_to`. | `research.md@sha256:29d7…21e6#L447,L461-L462,L558-L561`; `spawn-0003`; **observed** |

Required relations are `snapshot_of`, owner-asserted `revision_of`/`supersedes`, `package_contains`, `anchored_by`, `supports`/`challenges`, `references_definition`, `derived_from`, `bridge_assessed_by`, `blocked_by`, owner-created `approved_by`/`promotes_to`, `projected_as`, and `invalidated_by`.

Every edge requires declared endpoint types, cardinality, provenance, and cycle policy. Edge IDs hash predicate, ordered endpoint snapshot IDs, and provenance-anchor IDs. Inverses are computed, not independently authored.

Binding: `research.md@sha256:29d7…21e6#L449-L466`; explorer return `spawn-0003`; scope: candidate relation invariants; status: **observed**.

## 5. IDE integration map

Current key-byte bindings transcribed by the workbench explorer are:

- `projects/ide-extension/src/server.mjs@sha256:e69bdb17fb9a7b517d5089963c294c1d18f7656a3a2ac3c525b518404e5a16f7`
- `projects/ide-extension/src/kernel/projector.mjs@sha256:3ff4a94492f064548513517efc1e0c018e15ed2b474fcb9cf97055e91ecb09f6`
- `projects/ide-extension/src/kernel/canvas.mjs@sha256:53e6b522b52f6c47eede5cc1fe758863e7c4b5f564b0122dc42f74a3dcb5a47d`
- `projects/ide-extension/public/demo/l0.html@sha256:e5f5ed5d82e8984eb4b663c74a23cc6ad2ddc8f4bd12c12cd1c96df218cadea7`
- `projects/ide-extension/schemas/canvas-interaction-request.schema.json@sha256:249f508d57e115a11f2872f415bcee7a0ce8e8e5cb52be7bfbbeac8c0e044de`

Binding: `research.md@sha256:29d7…21e6#L220-L239`; explorer return `spawn-0002`; scope: current source-byte inspection; status: **observed**. Explorer `node --check` passed for four JS modules, but no Node or Playwright suite ran (`#L373-L377`); that narrower syntax check is **executed**.

| Concern | Current | Required | Binding |
|---|---|---|---|
| Module | Shape-validated manifest with unresolved string `source_refs`. | Lab module whose source refs resolve to digest, selector, revision, privacy, and verification state. | `research.md@sha256:29d7…21e6#L243-L244,L256-L271`; `spawn-0002`; **observed** |
| Runtime state | Event-derived run, approval, receipt, claim, and evidence state. | Separate tower selection/projection state; tower nodes never masquerade as runs or receipts. | `research.md@sha256:29d7…21e6#L245-L248`; `spawn-0002`; **observed** |
| Evidence inspection | Existing ID-addressed evidence endpoints and Inspector. | Typed source anchors, digests, selectors, claim ceilings, and residue. | `research.md@sha256:29d7…21e6#L248-L249,L260-L267`; `spawn-0002`; **observed** |
| Canvas | Trusted local HTML publication with revision binding, but publication appends audit/projection state. | For strict no-write witness, use a direct GET-rendered trusted shell. Never render source-supplied HTML. | `research.md@sha256:29d7…21e6#L249-L252,L278-L283,L324`; `spawn-0002`; **observed** current, **unverified** required |
| Navigation | Generic interaction names are accepted. | Allow only `tower.node_selected`, `tower.evidence_selected`, and `tower.residue_selected` with exact projection/revision binding. | `research.md@sha256:29d7…21e6#L252-L253,L268-L283`; `spawn-0002`; **observed** current, **unverified** required |
| Freshness | Final Canvas HTML digest is guarded; underlying tower inputs are not. | Reverify every package/source lock before serving; changed digest invalidates the projection and preserves last verified view. | `research.md@sha256:29d7…21e6#L250-L251,L270-L281`; `spawn-0002`; **observed** current, **unverified** required |
| Containment | Same-origin iframe has no sandbox; no CSP; containment is deferred. | Fixed trusted shell plus safe DOM/text construction; no general Canvas-containment claim. | `research.md@sha256:29d7…21e6#L278-L279`; `spawn-0002`; **observed** current, **unverified** required |
| Tower Navigator | No module, schema, route, fixture, compiler, or UI exists. | Candidate projection/interaction schemas, kernel adapter, GET endpoint, safe shell, and scoped tests. | `research.md@sha256:29d7…21e6#L236-L238,L304-L322`; `spawn-0002`; **observed** absence, **unverified** required |

## 6. First representative-tower selection

| Candidate | Strength | Blocking concern | Disposition | Binding |
|---|---|---|---|---|
| T04 Agentic Context Management | Public owner, unique, exact G2 scaffold, explicit closure and promotion ceiling. | Explorer return does not carry its complete ordered artifact manifest or per-source locks. | **Preferred representative candidate**, not yet witness-ready. | `research.md@sha256:29d7…21e6#L47,L157-L160`; `spawn-0001`; **observed** |
| T11/T09 Categorical Learning System | Complete private G2 package plus byte-identical handoff copy; strong provenance test. | Private boundary and canonical-copy handling add complexity to the first witness. | Second duplicate/provenance witness. | `research.md@sha256:29d7…21e6#L52-L55,L157-L160`; `spawn-0001`; **observed** |
| T08/T21/T41 Triton Top2 | Same digest across public, private, and fixture locations; strongest hostile identity case. | Canonical owner unresolved; custom G0; active GPU/runtime residue. | Stress witness only; explicitly not first. | `research.md@sha256:29d7…21e6#L49,L61,L81,L157-L160`; `spawn-0001`; **observed** |
| T26 Cognitive Tools Reflection | Unique G2 candidate; five exact artifact locks and useful source/claim/residue selectors are available. | Currently untracked, candidate-only, not established as representative; five locks are not a complete package manifest. | Mechanical fallback fixture only. | `research.md@sha256:29d7…21e6#L66,L285-L302`; `spawn-0001`,`spawn-0002`; **observed** |

Selection result: **T04 is the preferred representative candidate**, but final selection and writer handoff remain blocked until the corpus feedback edge returns its full ordered manifest, source locks, selectors, and package-manifest digest. T26 must not silently replace it merely because more partial locks were transcribed.

## 7. Smallest read-only witness contract

The smallest acceptable witness is one direct GET-rendered, trusted-shell projection of exactly one fully bound tower snapshot.

```yaml
fixture_id: cxl-one-tower-001
status: candidate
authority_effect: none

input:
  tower_logical_id: REQUIRED
  tower_snapshot_id: REQUIRED
  canonical_order_manifest_sha256: REQUIRED
  source_snapshots: [at_least_one]
  expected_digests: REQUIRED
  selector_resolution: REQUIRED

records:
  tower_package_snapshots: [exactly_one]
  knowledge_records:
    claim: exactly_one
    definition_reference: exactly_one
    residue_or_missing_evidence: exactly_one
  evidence_anchors: at_least_one_per_claim_or_definition
  bridge_decision:
    status: insufficient
  promotion_record:
    gateResult: block
    reviewOwner: ontology-owner
    useScope: fixture-review-only

projection:
  transport: GET
  trusted_shell: true
  source_html_rendering: forbidden
  domain_source_writes: forbidden
  local_audit_or_projection_writes: forbidden
  authority_effect: none
  interactions:
    - tower.node_selected
    - tower.evidence_selected
    - tower.residue_selected

failure_policy:
  changed_digest: invalidate_and_preserve_last_verified_view
  missing_selector: abstain
  duplicate_identity: reject_until_classified
  dangling_relation: reject
  unsupported_record_kind: reject
  private_source_exposure: reject
  stale_revision: reject
  unsupported_interaction: reject_without_append
  promotion_attempt: reject
```

The contract is derived from `research.md@sha256:29d7…21e6#L273-L324,L524-L574`; explorer returns `spawn-0002`,`spawn-0003`; scope: negative cases and candidate fixture; status: **unverified** because no fixture, adapter, schema, or tests exist.

## 8. Phased project route

| Phase | Owner and artifact | Entry/exit gate | Binding |
|---|---|---|---|
| 0. Feedback closure | Corpus explorer returns T04 ordered manifest, source locks/selectors, identity decision, and manifest digest; IDE owner chooses and binds direct GET adapter fields. | Exit only when all closure-matrix required rows are immutable-bound. | `research.md@sha256:29d7…21e6#L157-L160,L285-L324,L572-L574`; `spawn-0001..0003`; **unverified** |
| 1. Research foundation | Research owner accepts this bounded model and non-goals. | Evidence closure ready; writer may synthesize findings, but gains no implementation authority. | `research.md@sha256:29d7…21e6#L126-L160,L403-L431`; `spawn-0001`,`spawn-0003`; **observed** |
| 2. Candidate ontology fixture | Ontology fixture owner creates candidate schemas/records with `authority_effect: none`. | Schema, selector, privacy, relation, invalidation, and negative-case validation pass on exact bytes. | `research.md@sha256:29d7…21e6#L433-L485,L524-L574`; `spawn-0003`; **unverified** |
| 3. Workbench implementation | IDE owner implements module, projection/interaction schemas, adapter, GET route, trusted shell, and scoped tests. | No tower/ontology writes; strict allowlist; hostile labels inert; source locks checked. | `research.md@sha256:29d7…21e6#L273-L324`; `spawn-0002`; **unverified** |
| 4. Validation | Independent validator emits immutable `ValidationRecord`s and browser evidence. | Unit, failure, read-only, selector, privacy, relation, desktop/mobile, and last-good-view checks pass. Human usefulness remains a separate gate. | `research.md@sha256:29d7…21e6#L317-L322,L373-L385,L445`; `spawn-0002`,`spawn-0003`; **unverified** |
| 5. Promotion | Named ontology/authority owner reviews one primary claim and bridge evidence. | Explicit owner decision; default remains `block`. Validation cannot promote. | `research.md@sha256:29d7…21e6#L443-L447,L509-L522,L558-L561`; `spawn-0003`; **unverified** |
| 6. Publication | Publication owner performs privacy scrub and decides a bounded public artifact. | Explicit authorization and public/private boundary review. No private prose enters Arcanum by implication. | `research.md@sha256:29d7…21e6#L35,L515-L522`; `spawn-0001`,`spawn-0003`; **unverified** |
| 7. Deployment | Deployment owner chooses environment, security, transport, rollback, and operations contract. | Separate deployment authorization and executed environment evidence. | `research.md@sha256:29d7…21e6#L214-L238,L509-L522`; `spawn-0002`,`spawn-0003`; **unverified** |

## 9. Exact-binding closure matrix

| Load-bearing row | Required closure | Current evidence | State |
|---|---|---|---|
| Tower System source | Immutable source identity | PDF SHA-256 bound; page-count discrepancy retained as residue. `research.md@sha256:29d7…21e6#L9-L23`; `spawn-0001`; source identity; **executed** | Closed by digest |
| Frozen occurrence census | Command, snapshot date, counts, claim ceiling | Census command and counts transcribed. `#L9-L23`; `spawn-0001`; corpus census; **executed** | Closed for `TOWER.md` occurrences only |
| Corpus eligibility | Explicit rule distinct from conformance | Rule transcribed. `#L25-L40`; `spawn-0001`; eligibility policy; **observed** | Candidate-closed |
| Preferred tower logical identity | Owner-approved T04 logical ID and lineage | Candidate ranking only. `#L47,L157-L160`; `spawn-0001`; selection evidence; **unverified** | **Open** |
| T04 package snapshot | Complete ordered artifact manifest and digest | Only `TOWER.md` digest D04 is transcribed; sibling locks absent. `#L47,L86-L123`; `spawn-0001`; occurrence manifest; **unverified** | **Open** |
| T04 source/evidence bindings | Per-source digest, byte size, and selector resolution | Not present in explorer return. `#L157-L160`; `spawn-0001`; witness recommendation; **unverified** | **Open** |
| Duplicate semantics | No canonicality inferred from bytes | Rule and examples bound. `#L31-L35,L42-L123,L453-L464`; `spawn-0001`,`spawn-0003`; identity policy; **observed** | Closed as candidate rule |
| Triton canonical owner | Owner decision across T08/T21/T41 | Explicitly unresolved. `#L49,L61,L81,L198-L201`; `spawn-0001`; residue; **unverified** | Open residue, not first-witness blocker |
| Candidate record/relation model | Typed records, edge invariants, authority ceiling | Fully transcribed candidate model. `#L433-L485`; `spawn-0003`; ontology contract; **observed** | Candidate-closed |
| Definition binding | Exact canonical definition digest/version/selector for witness term | Required but not instantiated. `#L442,L540-L543`; `spawn-0003`; definition reference; **unverified** | **Open** |
| Candidate fixture | Concrete IDs, records, anchors, validation inputs | Fixture fields remain blocked/NOT_RUN. `#L524-L574`; `spawn-0003`; fixture; **unverified** | **Open** |
| Current IDE substrate | Current source digests and interface selectors | Five current digests and implementation selectors transcribed. `#L220-L271,L348-L376`; `spawn-0002`; IDE substrate; **observed/executed syntax only** | Closed for research description |
| Read-only adapter | Actual route, session/revision, generator digest, input-lock digest | Tower Navigator absent; Canvas writes local state; direct GET is only a requirement. `#L236-L238,L256-L324`; `spawn-0002`; adapter binding; **unverified** | **Open** |
| Runtime/browser validation | Tests on staged exact bytes | No Node or Playwright suite executed. `#L317-L322,L373-L385`; `spawn-0002`; test status; **unverified** | **Open** |
| Human usefulness | Human verdict | Existing Workbench UI verdict remains pending. `#L229-L230,L384`; `spawn-0002`; historical UI status; **unverified** | Open, later gate |
| Promotion/publication/deployment | Explicit owner decisions and executed evidence | Forbidden automatic edges are defined; no decisions or execution exist. `#L509-L522`; `spawn-0003`; authority ceiling; **unverified** | Correctly blocked |

**EVIDENCE_CLOSURE_READY: no**

Unresolved load-bearing rows:

1. Owner-approved T04 logical identity and lineage.
2. Complete T04 ordered artifact manifest and `canonical_order_manifest_sha256`.
3. T04 per-source digests, byte sizes, source-local selectors, and selector-resolution evidence.
4. Exact canonical definition binding for the fixture’s `DefinitionReference`.
5. Instantiated candidate fixture IDs, records, relations, privacy decisions, and validation inputs.
6. Actual strict-read-only GET adapter, generator contract digest, projection revision, and session/revision binding.
7. Current unit, negative-case, read-only, integration, and browser validation on exact staged bytes.

The writer must remain blocked. These gaps should return through the declared corpus/provenance and IDE feedback edges; they must not be filled by choosing T26 silently, synthesizing IDs from headings, treating current Canvas behavior as strict read-only, or promoting candidate relations into authority.

```yaml
receipt:
  action_id: spawn-0004
  dispatch_id: 2026-08-07-cyberalchemy-lab-foundation
  run_id: run-001
  wave_id: wave-02-synthesis
  role: foundation-synthesizer
  capability_ref: research
  status: pass
  validation: pass_with_evidence_closure_blocked
  evidence_closure_ready: no
  blockers:
    - T04 logical identity and lineage are not owner-approved
    - T04 complete ordered package manifest and manifest digest are absent
    - T04 source digests and selector-resolution bindings are absent
    - candidate ontology fixture is uninstantiated and its validations are NOT_RUN
    - exact canonical definition binding is absent
    - strict-read-only GET adapter and projection revision binding do not exist
    - current runtime and browser validation were not executed
  transcript_bindings:
    - projects/cyberalchemy-lab/development/research/2026-08-07-foundation/research.md@sha256:29d7a80d1ceeb1823b7bbd74579bf167167d4a66e4b6aa7f04ef6b8139e021e6#L5-L210
    - projects/cyberalchemy-lab/development/research/2026-08-07-foundation/research.md@sha256:29d7a80d1ceeb1823b7bbd74579bf167167d4a66e4b6aa7f04ef6b8139e021e6#L212-L399
    - projects/cyberalchemy-lab/development/research/2026-08-07-foundation/research.md@sha256:29d7a80d1ceeb1823b7bbd74579bf167167d4a66e4b6aa7f04ef6b8139e021e6#L401-L622
  normalized_receipt_bindings:
    - corpus-explorer.json@sha256:42cea1a0c4b710fe46d1faff20042fc6146968936a047fc99eff701848a4120b
    - workbench-explorer.json@sha256:b6be183f04a8d40c293882fc503e1839dfdf892cfa9358bd7502292d3230b4a6
    - ontology-explorer.json@sha256:f417af8eabc8e0ee186f30bb4138501751551f6b392d115bf3858e207456b941
  repository_bindings_relied_on:
    - research/tower-system-taxonomy/Tower-System.pdf@sha256:2318a4066b8146e7073781df7aa62589938789685b6c2c64cf83737613f32f5b
    - projects/ide-extension/src/server.mjs@sha256:e69bdb17fb9a7b517d5089963c294c1d18f7656a3a2ac3c525b518404e5a16f7
    - projects/ide-extension/src/kernel/projector.mjs@sha256:3ff4a94492f064548513517efc1e0c018e15ed2b474fcb9cf97055e91ecb09f6
    - projects/ide-extension/src/kernel/canvas.mjs@sha256:53e6b522b52f6c47eede5cc1fe758863e7c4b5f564b0122dc42f74a3dcb5a47d
    - projects/ide-extension/public/demo/l0.html@sha256:e5f5ed5d82e8984eb4b663c74a23cc6ad2ddc8f4bd12c12cd1c96df218cadea7
    - projects/ide-extension/schemas/canvas-interaction-request.schema.json@sha256:249f508d57e115a11f2872f415bcee7a0ce8e8e5cb52be7bfbbeac8c0e044de
  residue:
    - Tower System PDF page-count discrepancy
    - Triton canonical owner unresolved
    - non-TOWER research eligibility remains an owner decision
    - no primary graph substrate is warranted
    - hostile Canvas containment and human usefulness remain open
    - no implementation, ingestion, ontology authority, promotion, publication, deployment, or production proof
  reroute_needs:
    - corpus provenance feedback edge for T04 identity, manifest, and source selectors
    - ontology owner binding for the fixture definition reference and later promotion gate
    - IDE owner binding for strict-read-only GET projection and validation
  observer_status: not_emitted_read_only_scope
  handoff_note: >
    Synthesis is internally consistent and exact-bound to the explorer transcript,
    but evidence closure is not ready. Keep the writer blocked and route the seven
    unresolved load-bearing rows through the declared feedback edges.
```

<!-- END VERBATIM RETURN: spawn-0004 foundation-synthesizer -->
