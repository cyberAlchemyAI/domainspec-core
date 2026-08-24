# Stage 07: Interrogation — Refine Design Review

## Interrogation Result

- Mode: `refine-design-review`
- Capability: `interrogation`
- Questions asked of user: 0
- Verdict: `flag`
- Blocking user ambiguity: none
- Repair owner: Stage 08 Distill Repair

The model is coherent, but eight exact repairs are required before it can be
the parent’s final candidate. These are evidence-derived design defects, not
preferences requiring another user decision.

## Dialectic Review

| Attack | Failure witness | Required repair |
|---|---|---|
| Relation double source | A record embeds an edge while `relations/*.json` contains a divergent relation with the same endpoints. | V1 must choose one authored relation location. Keep standalone relation records; derived record adjacency is projection only. |
| Axis over-requirement | A definition or evidence record is forced to carry inapplicable promotion/bridge fields. | Record schema must use `record_kind` conditionals; only stable identity/kind/title/content envelope is universal. |
| Trace can lie | A projector emits “promoted,” then writes a fabricated source selector into its trace. | Define a closed emission-operation algebra and an independent verifier that recomputes every semantic emission from the normalized model. |
| Template semantic smuggling | Template text contains a domain assertion not present in source but is labeled structural. | Templates may emit only closed structural tokens. Domain text must come through verified semantic operations. |
| Admission event ambiguity | A `revoke` record also appears to `admits_package_version`. | Model admission decisions as immutable events with event-specific subject fields and a derived current-admission projection. |
| Formatting admission ambiguity | Whitespace changes preserve canonical meaning but change exact artifact bytes. | AdmissionRecord must bind both digests and state whether the event admits exact bytes; any byte change requires a new artifact event even when semantic diff is empty. |
| Authoring profile creep | UI configuration supplies defaults that silently become semantic values. | AuthoringProfile may control labels, grouping, help, and widget choice only; semantic defaults are forbidden unless present in SchemaSuite and emitted explicitly in SourcePatch. |
| Compatibility shortcut | `read-compatible` is used to admit a package without materializing the target model. | Read-compatible permits inspection only. Admission requires exact target suite/profile digests after canonicalization or verified migration. |

## Additional Non-Blocking Challenges

- `owner_ref` inside a package is a claimed routing hint, not proof that the
  named owner accepted the package.
- Stable semantic IDs need a closed pattern and namespace uniqueness validator.
- Plain text is intentionally narrow. Rich formatting must not slip into
  templates as a workaround.
- SourcePatch removal must detect dependent relations and either include their
  removal or fail atomically.
- Split and merge migration require an owner-classified continuity decision;
  a tool may propose but cannot assert identity.
- Public leakage testing must inspect schema enums, examples, descriptions,
  fixture bytes, paths, and generated outputs—not only field names.

## Preserved Decisions

- Closed JSON remains the v1 admitted source candidate.
- Forms/editors remain the humane authoring surface through SourcePatch.
- Normalized IR and views remain derived.
- AdmissionRecord remains distinct from PromotionRecord.
- Migration remains copy-and-verify with retained rollback bytes.
- JSON-LD remains a graph projection and strict YAML remains deferred.

## Claim Ceiling

This review finds repairable candidate-design defects. It does not reject the
source-to-view architecture, validate implementations, or authorize mutation.
