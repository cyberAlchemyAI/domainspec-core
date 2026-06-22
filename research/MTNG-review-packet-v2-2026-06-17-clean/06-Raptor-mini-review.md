# MTNG Audit Report

Reviewer: GitHub Copilot (Raptor mini)

## 1. Executive verdict

MTNG is a conceptually sound proposal for an on-demand artifact extraction pipeline, and it fits ResonantOS’s documented direction only if it stays:
- offline/sidecar/on-demand,
- audit-first,
- authority-bounded,
- memory-safe,
- add-on/engine-mediated rather than autonomous runtime.

The local MTNG docs are high quality in framing scope and risk. The GitHub repo docs strongly favor this approach, especially because ResonantOS is explicitly positioning itself as a browser-first AI layer with safe provider routing, gated memory writes, and add-on mediation.

However, the proposal is still too abstract to implement directly. Its strongest promise is as a schema and inspection pipeline, not as a live runtime. If MTNG is built as a runtime system without a careful Phase 0 integration map, it is likely to fail.

## 2. Strongest parts of the proposal

- Clear on-demand / “not always-on” stance
  - Both local docs and repo docs stress preview-grade, selective execution and avoiding broad data inspection.
- Strong safety-oriented separation
  - MTNG explicitly defers contribution valuation, authority escalation, memory promotion, and runtime ownership to future phases.
- Good alignment with ResonantOS guardrails
  - ResonantOS docs emphasize add-on capability gating, provider fabric central routing, Living Archive review/verify/promote pipeline, and trusted memory writes only through controlled flows.
  - MTNG matches that by proposing an engine-plus-tools model and a validation/contract layer.
- Practical pilot orientation
  - The spec asks for a smallest useful pilot and explicitly calls for Phase 0 integration mapping before implementation.
- Risk-aware design additions in `05-changelog.md`
  - fast-path rules
  - overhead budgets
  - misrouting recovery
  - partial merge / conflict handling
  - explicit runtime deferral

## 3. Weakest or riskiest parts

- Classification/branching ambiguity
  - The signal/mode/tone taxonomy is conceptually useful, but it is underspecified.
  - This is the core failure point: if branch detection is wrong, MTNG can either over-branch into useless complexity or under-branch into the same failure modes it’s trying to avoid.
- Lack of concrete integration anchors
  - The GitHub docs do not show existing `Signal`, `Mode`, `Node`, `Branch`, or `Contribution Record` state in the current codebase.
  - The MTNG spec acknowledges this gap, but the implementation risk remains high without a real mapping into Guardian Core, Bridge Server, provider nodes, event bus, and memory-provider broker.
- Graph recombination and merge rules are still abstract
  - The proposal describes partial merges and conflict-resolution branches, but no explicit schema or algorithm is provided.
  - That makes it hard to validate whether the proposed merge model will actually preserve auditability and avoid false synthesis.
- Potential scope creep
  - MTNG touches many domains: debugging, memory, workflow extraction, contribution accounting, export, safety, provider routing.
  - That breadth makes it easy to overbuild and to collide with existing ResonantOS roadmap items like Living Archive, provider strategy, and add-on SDK.
- Possible mismatch with current product focus
  - ResonantOS docs currently prioritize browser-first app, add-on registry, and Living Archive memory system.
  - MTNG is a good complementary engine, but not a first-class UI surface; if it is treated as a full runtime, it conflicts with the “do not replace existing architecture” stance.

## 4. Integration questions for ResonantOS

1. Which existing component should own MTNG’s core state?
   - Best candidate: the add-on / tool runtime layer, not core chat UI.
   - But the spec asks whether `Signal`, `Mode`, `Branch`, `Synthesis`, `Memory Candidate`, and `Contribution Record` should belong to existing ResonantOS state. My read says these are most naturally owned by:
     - the Bridge Server or lifecycle engine
     - the provider/memory/tool orchestration layer
     - a separate audit/artifact service
2. Should MTNG be implemented as:
   - a developer inspection panel,
   - a schema-only pipeline,
   - or a runtime system?
   - The safest first step is schema-only / sidecar artifact pipeline.
3. How should MTNG use existing provider fabric?
   - It should rely on current provider routing and model policies, not introduce its own model-routing layer.
4. Where will MTNG store its audit log?
   - Ideally under the existing `ResonantOS_User/Memory` audit/artifact path, not a new uncontrolled path.
5. What should “fast path for simple signals” mean in the current app?
   - Likely: if a signal is purely a bug report or a single terminal log, do not branch at all; produce a single artifact.
6. How should MTNG interact with add-on capability grants?
   - If specialty tools are implemented as add-ons, MTNG must ask for capability grants through the add-on manifest system rather than bypassing it.

## 5. V1 pilot recommendation

The smallest useful pilot is:

- `mtng` as an offline/artifact pipeline, not a runtime.
- Input sources:
  - terminal logs
  - chat transcripts
  - git diffs
  - bug reports
- Output artifacts:
  - `signal-manifest.yaml`
  - `branch-nodes.yaml`
  - `developer-issue-packet.md`
  - `memory-candidates.md`
  - `validator-report.md`
  - `audit-log.jsonl`
  - OKF/metadata export

Pilot scope should exclude:
- automatic live agent delegation
- direct memory promotion
- wallet or browser control actions
- full contribution valuation
- runtime reconstruction

Pilot should include:
- Phase 0 integration mapping into current codebase
- a deterministic schema for branch contracts
- a simple classifier that can admit “fast path / no branch”
- an audit/log output path that matches existing Living Archive intake patterns
- explicit human override and reject flow

## 6. Sections to remove, defer, or simplify

### Remove or postpone
- Any claim that MTNG is “not to make agents more autonomous” but then suggests runtime branch-based execution.
  - Keep it strictly as an analysis/partitioning engine in V1.
- Any direct memory promotion or trusted wiki write path.
  - These should remain deferred and only proposed as intake candidates.
- Any economic/contribution accounting logic beyond capture metadata.
  - The docs correctly defer valuation, and that should stay deferred.

### Defer
- exact OKF type names until the OKF ecosystem stabilizes.
- the runtime integration layer until the product confirms the on-demand pipeline value.
- contribution “weights” or “compensation” decisions until the architecture is settled.

### Simplify
- The Tone / Mode taxonomy
  - Make it a small, operational list for V1 instead of a broad conceptual taxonomy.
- Graph recombination rules
  - For V1, prefer “branch if validation contract changes” and keep merge rules narrow.
- Output artifact list
  - Start with a minimal set and expand based on real review feedback.

## 7. Questions to take back to Tom / ResonantOS maintainers

1. Is MTNG intended as a product-visible feature or an internal review/tooling layer?
2. Which existing ResonantOS state store should own MTNG artifacts and audit logs?
3. Should an MTNG pilot be packaged as a local CLI only, or also as a UI panel in the browser-first app?
4. Do you want MTNG to consume Living Archive intake only, or also produce standard issue/bug-report artifacts?
5. Can MTNG reuse the existing provider fabric and memory-provider broker without adding a separate runtime route?
6. What is the acceptable failure mode in V1?
   - more missed branches, or more false positive branches?
7. Which ResonantOS feature backlog item should be considered the “top integration target” for MTNG?
   - provider strategy,
   - Living Archive review,
   - add-on SDK,
   - browser job audit,
   - or recovery/Engineer?

## High-quality logic assessment

### What is high quality
- The GitHub docs are strong on:
  - browser-first, modular architecture
  - safe provider routing
  - add-on capability gating
  - memory review/promotion boundary
  - audit-first design
  - on-demand and preview-grade execution
- The MTNG proposal matches those directions when it is kept as a sidecar/pipeline and not a live control system.

### What is lower quality or missing
- No explicit existing architecture mapping for the MTNG concepts
- No concrete schema or algorithm for branch/merge lifecycle
- No clear ownership of MTNG state in the current codebase
- The broad “graph” metaphor may hide complexity in implementation

## Final recommendation

MTNG is worth pursuing only as a carefully scoped, on-demand analysis pipeline with:
- explicit Phase 0 integration mapping,
- minimal branch rules,
- audit-first artifact output,
- Living Archive intake compatibility,
- and strict non-autonomy.

If the team wants to build it, the first concrete step should be:
1. map MTNG concepts to existing ResonantOS components,
2. choose a narrow pilot data set,
3. implement a schema-only proof of concept,
4. validate against actual ResonantOS review workflows,
5. then decide whether to extend it beyond a tooling pipeline.

If MTNG is instead treated as a runtime architecture, the current proposal is not yet ready.
