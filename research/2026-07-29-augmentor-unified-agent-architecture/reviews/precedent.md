# Precedent and duplicated-ownership review

- Action: `spawn-0005`
- Reviewer: `Lakatos, Imre`
- Verdict: `REPAIR`
- Scope: precedent and duplicated ownership only
- Mutation: none

## Row findings

- `AUA-C01`, `C05`, `C11`, `C12`, `C13`, `C15`, and `C16` are
  `BUILD_FROM_OWNED`: ResonantOS retains conversation, delegation, workspace,
  goal, artifact, and blocker owners; Dispatch Spec validates route shape;
  Orchestrate owns actions and lifecycle joins
  (`synthesis.md:82-83,86,92-97`;
  `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:1958-2008,2019-2105,2769-2778`;
  `arcanum/formulae/dispatch-spec/SKILL.md:65-100`;
  `arcanum/runtime/orchestrate/SKILL.md:77-141`).
- `AUA-C02` must split user/session handle ownership from source-provider truth
  and label the handle resolver as an absent host adapter
  (`synthesis.md:49-50,83`).
- `AUA-C03` and `C04` may not appoint a generic memory domain before the
  durable owner decision. State `ABSENT adapter/owner selection required`;
  source providers retain truth
  (`synthesis.md:84-85,169-173,216-218`; `research.md:237-242`).
- `AUA-C06` is honestly proposed, but `C07` and `C08` use role descriptions,
  not current owners. Label RouteDecision, StrategyProposal projection, and
  approval registrar as absent host adapters; Dispatch Spec remains validator,
  not approval owner (`synthesis.md:87-89,171-173`;
  `research/2026-07-28-augmentor-subagent-strategy-integration/findings.md:33-57,61-89`).
- `AUA-C09`, `C10`, and `C21` pass. The evaluator is exactly an unwitnessed
  research-contract candidate, owns derivation only, and cannot approve or
  authorize effects (`synthesis.md:11-20,90-91,102,169-173`;
  `projects/cyberalchemy-orchestrator/docs/research/2026-07-22-agent-reasoning-engine-contract/findings.md:5-9,63-78,110-132`).
- `AUA-C14` must bind future addressed revisions to the selected host execution
  owner through `ownerRunId`; AttentionRequest/InputRevision and delivery are
  absent adapters (`synthesis.md:95,173`;
  `research/2026-07-28-augmentor-routing-session-fabric/findings.md:144-162`).
- `AUA-C17` and `C18` omit source-provider acceptance. Use
  `MemoryIntakeRequest -> provider review/acceptance -> accepted SourceRecord
  digest change`; only then may Inventory discover/package evidence. EvidenceSet
  remains candidate/fixture-level
  (`synthesis.md:98-100,129-138`;
  `arcanum/arcana/inventory/development/POC-VALIDATION.md:31-35,67`;
  `arcanum/arcana/inventory/development/decisions/EVIDENCESET-DECISION.md:62-76`).
- `AUA-C19` passes if it remains designed/unverified and non-authoritative.
- `AUA-C20` needs an authority-kind-specific owner and canonical selector.
  Split canonical-source writes from generated projections; promotion writer
  remains absent until AuthorityDecision/PromotionRecord identity/cardinality
  is resolved (`synthesis.md:71,101,173,216-218`; `research.md:241-242`).

## Verdict

The architecture is repairable `BUILD_FROM_OWNED + explicit absent adapters`.
No kill-level duplicate owner was found. Blockers are the unselected durable
memory/index/projection owner, absent trusted write provider, absent exact
authority owner/canonical selector for generic C20, and unresolved
AuthorityDecision/PromotionRecord cardinality.
