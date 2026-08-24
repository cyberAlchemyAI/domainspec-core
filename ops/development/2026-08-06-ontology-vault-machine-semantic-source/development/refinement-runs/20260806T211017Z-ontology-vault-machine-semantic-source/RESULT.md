# Refine Result: Ontology Vault Machine Semantic Source

## Result

- Target: Ontology Vault source/projection convention update
- Status: `flag`
- Preset: `standard`
- Research: confirmed local three-specialist wave; no external research
- Exact candidate model: authored and repaired
- Public Ontology Vault mutation: none
- Generated skill mutation: none
- Inventory mutation: none
- Work Pack: split, non-executed, and gate-blocked
- Authority effect: none

The Refine objective is achieved at candidate-design level: there is now one
exact model for how a machine semantic source, schemas, normalized model,
human/graph/query views, corrections, receipts, admission, promotion, and
migration interact. The flag preserves missing implementation, validation, UX,
and owner evidence rather than inflating the result into readiness.

## Exact Model

```text
closed JSON SemanticPackage
  -> five-module source SchemaSuite
  -> OV-CANON-JSON/v1
  -> deterministic disposable NormalizedSemanticModel
  -> closed ProjectionDefinition operation graph
  -> HumanView | GraphView | QueryView
  -> independently verified ProjectionTrace + ProjectionReceipt

human correction
  -> SourcePatch against exact base digest
  -> atomic candidate source version
  -> package-owner review

package source authority
  -> external immutable AdmissionRecord event

claim/relation lifecycle authority
  -> existing one-primary-item PromotionRecord

legacy adoption
  -> total MigrationMap
  -> copy + verify + typed residue + retained rollback bytes
  -> owner cutover event
```

### Source representation decision

Closed local JSON is the v1 admitted-source candidate. This does not require
people to hand-maintain JSON: schema-guided forms/editors create explicit,
reviewable SourcePatch operations. Strict YAML is deferred until finite
authoring evidence proves the form/patch route insufficient. JSON-LD is a
derived graph projection, not the source.

### Schema boundary

The source SchemaSuite has five modules:

1. semantic package
2. semantic record with conditional record families
3. standalone semantic relation
4. projection definition
5. exactly one ontology-type constraint module, initially knowledge-vault

Normalized model, trace, receipt, patch, admission, and migration schemas are
protocol/governance contracts outside the authored-source suite.

### One relation source

V1 authors standalone relation records only. Record adjacency is derived. This
prevents embedded-edge and graph-file drift while still reusing the existing
relation field semantics.

### Projection correctness

A receipt cannot merely claim that a view is source-backed. Projection uses a
closed operation algebra, and an independent verifier re-executes every
semantic emission from the normalized model. Templates may contribute only
structural tokens. Untraced or strengthened claims fail.

### Human creation and correction

An optional AuthoringProfile controls labels, help, grouping, and widgets only.
It cannot hide or default semantic values. Every semantic edit appears in a
SourcePatch with stable selectors, base digest, preconditions, rationale, and
atomic operations. Invalid drafts retain patches/diagnostics and never replace
the last admitted source.

### Authority boundary

Schema, canonicalization, normalization, and projection produce evidence only.
AdmissionRecord binds one exact package artifact/version/scope and lives outside
the bytes it admits. PromotionRecord remains one-claim/one-relation scoped.
Neither replaces the other.

## Ontology Integration

Candidate node kinds:

- semantic package version, semantic module, SchemaSuite/schema module;
- semantic record and standalone semantic relation;
- ProjectionDefinition, normalized model, derived view;
- ProjectionTrace and ProjectionReceipt;
- SourcePatch;
- AdmissionRecord and existing PromotionRecord;
- MigrationMap and MigrationReceipt;
- non-semantic AuthoringProfile.

Load-bearing relations include package-includes-module,
package-constrained-by-suite, module-contains-record/relation,
relation-from/to-record, package-declares-projection, package-normalizes-to-model,
model-projects-to-view, view-evidenced/traced-by receipt/trace,
patch-proposes-change-to-package, admission-admits-package-version,
promotion-promotes-one-item, and migration-from/to-package-version.

Prohibited relations prevent normalized models becoming source, views writing
back, validation receipts admitting/promoting, package self-admission, bundled
package promotion, private-profile leakage, and RWO gate inference.

## Implementation Layering

- L0: package -> canonical model -> verified Markdown -> SourcePatch trust kernel.
- L1: schema-guided authoring, semantic diff, recovery, GraphView/QueryView parity.
- L2: admission event chain, migration, rollback, compatibility, and privacy hardening.
- L3: owner-approved public lifecycle integration, generated parity, packaging, and observability.

The Plan is medium/split. SWU-OVSS-001 is the narrowest future frontier, but no
unit is selected and allowed routes are empty. Governance/migration and public
lifecycle SWUs must be split again before any mutation-capable handoff.

## Evidence Summary

| Stage | Verdict | Artifact |
|---|---|---|
| Context Builder baseline | pass | `stages/01-context-pack.json` and x-ray |
| Invoke Define | pass | `stages/02-invoke-define.md` |
| Interrogation refine-review | pass | `stages/03-interrogation.md` |
| Research decision/synthesis | pass | `stages/04-research-synthesis.md` |
| Distill | pass | `stages/05-distill.md` |
| Invoke Design | flag | exact authored design; independent validator/UX evidence absent |
| Interrogation design review | flag repaired | eight bounded defects |
| Distill Repair | pass | repaired model and designed toy-game negatives |
| Invoke Plan | block for execution | honest non-executed Work Pack |
| Final Interrogation | flag | candidate complete; implementation/public gates absent |

Structural validation passed for the current dispatch, all run JSON, native
receipts/events, causal sequence, local links, ledger open/close cardinality,
and plan placeholder scan. These checks do not execute the planned semantic
schemas, canonicalizer, projector, authoring workflow, migration, or lifecycle
integration.

## Open Blockers

- B-001: independent DesignScope/denominator/fixed-point and exact schema evidence.
- B-002: formal UX plan and executed authoring usability evidence.
- B-003: public Ontology Vault owner approval of the representation and ontology delta.
- B-004: exact runtime, paths, commands, allowed routes, baselines, closeout receipts, and Sigil Development handoff.

## Recommended Next Routes

1. Ontology Vault lifecycle owner reviews the closed-JSON and ontology-delta candidate.
2. Invoke Design/UX materializes B-001 and B-002 evidence.
3. Invoke Plan refresh splits the flagged SWUs and binds exact routes/closeout contracts.
4. Sigil Development may implement L0 only after those gates pass.
5. Inventory post-result ingestion remains deferred because this confirmed run forbade Inventory mutation.

No next route is executed by this Refine result. The paused RWO composition-form
ontology identity decision remains separate and unresolved.
