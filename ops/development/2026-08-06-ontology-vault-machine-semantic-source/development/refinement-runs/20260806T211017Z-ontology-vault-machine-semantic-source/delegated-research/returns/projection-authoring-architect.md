# Specialist Return: Projection Authoring Architect

## 1. Source selectors and observed facts

### Observed source facts

- `REFINE-SEED-PROPOSAL.md` — `Current Evidence-Bounded State`, `Required Invariants`, `Authoring Experience Questions`
  - No admitted semantic-package, canonicalization, compiler, projection-receipt, authoring, or migration contract exists.
  - Human and graph views must carry the exact source digest, declare generator identity/version, reject silent writeback, and not invent semantic claims.
  - Stable semantic IDs must not depend on file position or presentation order.
  - Long-form rationale, examples, corrections, invalid drafts, and migration residue must remain usable and recoverable.
- `stages/01-source-projection-xray.md` — `Hidden Missing Spine`, `Source And View Ownership`
  - `SemanticPackage`, `NormalizedSemanticModel`, `HumanView`, and `ProjectionReceipt` are missing reusable contracts.
  - The normalized model is intended as deterministic derived IR, not independently authored source.
  - Generated views are read models; owner admission and promotion remain separate.
- `stages/02-invoke-define.md` — `Desired Outcome`, `Inputs`, `Outputs`, `Functional Requirements`
  - The defined correction path is a typed `SourcePatch` against source identity, not view writeback.
  - `ProjectionDefinition` already needs audience, renderer, ordering, filters, target, and explicit writeback posture.
  - `ProjectionReceipt` must bind source, schema, compiler, output digests, warnings, and result.
  - Semantic diffs, schema-guided authoring, declared omission rules, identity-preserving migration, and drift validation are requirements.
- `stages/03-interrogation.md` — `Dialectic Review`, `Fixed Decisions`
  - Long-form content must be representable inside source modules.
  - The IR must be reproducible and source-digest-bound.
  - Machine-parseable source becomes primary only after owner admission; generated views remain derived.
- `strategy-inventory-packet.json` — `design_consequences`, `residue`
  - Inventory supplies a non-authority precedent for one machine index with human projections.
  - The packet explicitly requires a human-authoring lane.
  - Inventory findings are discovery handles, not Ontology Vault authority.
- `arcanum/arcana/inventory/SKILL.md` — `machine-index-contract`, `authority-rule`
  - Inventory treats `index.json` as the primary machine catalog and `index.md`/CSV as derived read models.
  - Projection validation binds `source_sha256`, source generation time, and `projection_sha256`.
  - Generated pages must remain source-backed and non-authoritative; contradictions and residue must remain visible.
- `arcanum/arcana/ontology-vault/README.md` — `Core Concepts`, `Project-Local Runtime Profiles`
  - Evidence confidence, commitment confidence, maturity, and promotion are distinct.
  - Runtime-profile projections are non-authority; generated projections cannot become authority.
  - Project-local labels must not silently extend reusable public vocabulary.
- `BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md` — `Entry Schema`, `Validation Rules`, `Open Decisions`
  - The candidate already provides stable record fields for claim, definition, purpose, examples, non-examples, evidence selectors, confidence rationale, edges, and governance.
  - Lifecycle, claim role, governance outcome, and bridge outcome are separate axes.
  - The full schema remains exploratory and non-canonical; only `promotion_record` is canonical as a governance decision record-kind.
  - “YAML frontmatter plus Markdown body” is only an open candidate stance, not an admitted format.

### Inference boundary

The proposed authoring workflow, strict YAML subset, content-block shape, semantic-diff operations, and exact projection fields below are candidate recommendations derived from those facts. They are not present implementations or owner decisions.

## 2. Candidate recommendation

Use a constrained, typed YAML source module format compiled into canonical JSON IR.

The admitted authored source would be the YAML package and modules. YAML must be restricted: no aliases, merge keys, custom tags, implicit timestamps, duplicate keys, or representation-dependent numeric forms. Canonical JSON is derived IR and must never be edited as another source.

Long-form material belongs in explicit source fields, for example:

```yaml
content:
  claim: Human views are derived from one admitted semantic source.
  rationale:
    format: plain-text
    blocks:
      - id: rationale-source-view-split
        text: |
          A readable explanation can be long without becoming a second
          authority surface.
  examples:
    - id: example-markdown-projection
      text: A Markdown page is regenerated from the normalized record.
```

Block IDs provide patch targets and stable review anchors. Display order is explicit (`display_order` or ordered ID lists), while semantic identity remains independent of array/file position.

### Complete author journey

1. **Create**
   - The author selects an ontology type/profile and creates a draft module through a schema-guided editor, form, or command.
   - The tool assigns or validates a stable semantic ID and emits a typed `SourcePatch`; it does not write a generated view.
2. **Add explanation**
   - Claim, definition, rationale blocks, examples, non-examples, and confidence rationale are authored in source fields.
   - Long prose uses block scalars but remains typed source data, not an authoritative Markdown body.
3. **Link evidence**
   - The author adds immutable source references with selectors, role, proof posture, and provenance.
   - Inventory references retain their non-authority notice.
4. **Validate and preview**
   - Structural and cross-field validation runs first.
   - A deterministic normalizer creates the source-bound IR.
   - Markdown and graph/query previews compile from that same IR and are visibly marked generated and non-authoritative.
5. **Review**
   - The reviewer sees a semantic diff keyed by stable record/block IDs: add/remove record; replace a typed field; add/remove relation; change lifecycle/confidence/governance value; change evidence selector; or reorder display only.
   - YAML key order, indentation, wrapping, and comments appear separately as formatting-only changes.
6. **Propose correction**
   - Selecting content in a generated view resolves through projection provenance to a source record/field/block selector.
   - The tool drafts a `SourcePatch` against the exact package digest. Owner review remains required.
7. **Handle invalid state**
   - Invalid drafts remain in a draft workspace with typed diagnostics and the pending patch intact.
   - Invalid drafts cannot replace the last admitted source or produce governed projections.
   - Preview may show a clearly marked partial draft view only if omissions and failures are explicit.
8. **Recover**
   - Rebase the patch against the current admitted source, correct the failing field, and rerun validation.
   - If recovery fails, restore the last admitted package and retain the rejected patch plus diagnostics as residue.

### `ProjectionDefinition` candidate fields

- `projection_id`, `schema_version`, `projection_kind`
- `audience`, `purpose`
- `input_model_schema`, compatible version range
- `renderer_id`, `renderer_version`
- `selection`: included record kinds/types/branches and filters
- `ordering`: stable keys, explicit display lists, deterministic tie-breakers
- `field_mapping`: source fields to sections, node attributes, edges, or query columns
- `template_id` and `template_digest`
- `unknown_policy`, `contradiction_policy`, `omission_policy`
- `reference_policy`, escaping/serialization profile
- `output_format`, media type, target locator
- graph-specific node/edge selection or query-specific declared query set
- `invented_claim_policy: reject`
- `writeback_posture: forbidden`
- generated/non-authority banner requirements

### `ProjectionReceipt` candidate fields

- `receipt_id`, receipt schema version, result
- semantic package ID/version
- raw source-module-set digest
- canonical source digest
- SchemaSuite module IDs/versions/digests and aggregate digest
- normalizer ID/version/digest
- normalized-model digest
- ProjectionDefinition ID/digest
- renderer/compiler ID/version/digest
- template digest
- resolved selection, ordering, filters, and output profile
- output locator, media type, byte size, output digest
- warnings, omissions, unknowns, contradictions, validation diagnostics
- invented-claim check and writeback check
- reproducibility check result
- optional run time/run ID explicitly outside the governed deterministic output-byte domain

The receipt should bind distinct digest domains rather than one ambiguous “build digest.”

## 3. Representation comparison

| Representation | Authoring/review | Determinism | Graph semantics | Recommendation |
|---|---|---|---|---|
| Closed JSON | Strong schema tooling and canonicalization; weak long-form/manual editing; noisy punctuation diffs | Strongest | Explicit but verbose | Retain as normalized IR and interchange, not preferred human-authored source |
| Constrained JSON-LD | Natural graph vocabulary | Requires frozen local contexts and expansion rules; aliases obscure diffs | Strongest native graph posture | Defer; complexity exceeds the demonstrated local need |
| Strict typed YAML compiled to canonical JSON | Best prose, examples, patch review, and manageable modules | Strong only with a closed subset and deterministic compiler | Relations remain explicit typed records | Preferred candidate |

## 4. Finite positive and negative witnesses

### Positive witnesses

1. One record with rationale blocks, two examples, and evidence selectors generates byte-identical Markdown twice; both receipts share source, schema, compiler, definition, and output digests.
2. The same IR generates a Markdown page and graph/query view; each output has its own definition and output digest but shares the canonical source and normalized-model digests.
3. Reordering YAML keys or changing indentation changes the optional raw-byte digest but leaves canonical source/IR digests unchanged; semantic diff is empty.
4. A generated-view correction resolves to `record-id/content.rationale/block-id` and emits a source patch; owner acceptance followed by regeneration produces a new receipt.

### Negative witnesses

1. Source changes without regeneration: receipt canonical-source digest differs from current source; view is stale and rejected.
2. Markdown projector emits “promoted” when IR says “candidate”: invented-claim check blocks the projection.
3. Relation targets a missing record: validation blocks governed projection while preserving the invalid draft and patch.
4. Renderer inserts current time into governed output bytes: repeated builds differ; reproducibility fails.
5. Reviewer edits generated Markdown directly: writeback is rejected; the edit may only be converted into a source-patch proposal.
6. Missing evidence is rendered as “supported”: unknown-policy validation rejects the projection.
7. Two records rely on file position for identity: normalization rejects unstable identity rather than silently renumbering.

## 5. Rejected alternatives

- **Editable generated Markdown:** creates parallel authority and stale-view writeback.
- **Hand-authored closed JSON only:** technically clean but needlessly hostile to long prose and routine review.
- **Unconstrained JSON-LD:** remote/context aliasing and expansion rules weaken local closure and semantic-diff clarity.
- **General YAML:** aliases, implicit typing, duplicate keys, and implementation variance undermine deterministic normalization.
- **Unstructured Markdown body beside YAML metadata:** semantic content can escape typed fields and become difficult to patch or validate.
- **One aggregate digest:** cannot distinguish source drift, schema drift, compiler drift, definition drift, and output corruption.
- **Projection templates containing semantic rationale:** permits views to invent meaning absent from source.

## 6. Claim ceiling

This return recommends a candidate authoring and projection contract. It does not establish a canonical representation, public convention, schema, compiler, admitted ontology package, promoted meaning, implemented authoring tool, migration, or runtime. The explored branch-aware schema remains non-canonical except for its already-stated `promotion_record` record-kind boundary.

## 7. Residue and reroute

- Owner selection is still required for the representation and exact canonicalization profile.
- Schema/source owners must decide allowed rich-text formats, extension rules, comment preservation, block identity, and raw-versus-canonical digest policy.
- Invoke Design should specify the exact `ProjectionDefinition`, `ProjectionReceipt`, semantic-diff, and `SourcePatch` schemas.
- The governance specialist must resolve AdmissionRecord overlap, migration compatibility, rollback, and public/private fixture boundaries.
- Stage 5 Distill should reconcile this usability recommendation with the formal-schema and governance receipts.
- Any public change must reroute through Ontology Vault convention update and later Sigil Development.
- The paused RWO identity gate remains untouched.

**Status: pass. Blockers: none for read-only specialist synthesis; representation admission, public mutation, implementation, migration, and promotion remain owner-gated.**
