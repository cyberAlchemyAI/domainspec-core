# Runtime Context Pack: Agent Consultation API

Session evidence only. This pack selects evidence for the confirmed Refine run;
it is not a source of truth, API approval, or implementation receipt.

## Context Pack Summary

- Task: define, design, review, and plan a read-only agent consultation API.
- Mode: `standard --strict --emit both --handoff runtime`.
- Files selected: 14.
- Snippets selected: 24 selector-level records.
- Obligation coverage: 100% covered or explicitly deferred.
- Noise ratio: 0; every selected file closes at least one obligation.
- Output markdown: `context-builder/runtime-handoff.md`.
- Output index: `context-builder/runtime-handoff.index.json`.
- Handoff pack: runtime.
- Strict coverage: pass.
- Blockers: 0 for design work.

## Obligations

| ID | Obligation | Status | Evidence |
| --- | --- | --- | --- |
| O1 | Define callers and access checks. | covered | profile owner routes; memory-provider capability checks; open owner residue |
| O2 | Keep retrieval separate from answer generation and authority. | covered | seed boundary; README; accepted architecture thesis |
| O3 | Define bounded lookup, search, traversal, comparison, explanation, and context-pack operations. | covered | node, relation, view, context-budget, and provider-search contracts |
| O4 | Return source, owner, digest, status, confidence, freshness, and claim-ceiling fields. | covered | sources, node/relation records, profile, accepted architecture |
| O5 | Distinguish missing, insufficient, conflicting, stale, denied, invalid, and budget-exceeded outcomes. | covered | architecture capability-gap modes; reasoning outcome constraints; context-budget boundaries |
| O6 | Prohibit source, memory, ontology, routing, approval, execution, and authority writes. | covered | profile blocked outputs; knowledge forbidden moves; residue; README claim ceiling |
| O7 | Protect the private package behind a neutral bounded projection. | covered | README ownership boundary; architecture public/private boundary; source registry |
| O8 | Define how the answering agent cites, qualifies, clarifies, and abstains. | covered | seed done criteria; ReasoningPresentation boundary; compact-memory prompt constraint |
| O9 | Provide falsification scenarios and an implementation-ready but non-executed plan. | covered | seed validation surface; existing package validation receipt; architecture witness boundaries |

## Selected Evidence

1. `REFINE-SEED-PROPOSAL.md`
   - Selectors: `#Desired-Outcome`, `#Selected-Product-Boundary`,
     `#Write-Scope`, `#Done-Criteria`, `#Validation-Surface`.
   - Closes: O1-O9.
   - Evidence: confirmed scope and non-execution ceiling.

2. `projects/augmentor/ontology/unified-agent/README.md`
   - Selectors: `#Purpose`, `#Ownership-Boundary`, `#Core-Sequences`,
     `#Validation`.
   - Closes: O2, O4, O6, O7, O9.
   - Evidence: candidate-local posture, retained owners, non-collapsing flows,
     and exact claim ceiling.

3. `projects/augmentor/ontology/unified-agent/profile.json`
   - Selectors: `/status`, `/authority_effect`, `/release_admission`,
     `/owner_routes`, `/blocked_outputs`, `/claim_ceiling`.
   - Closes: O1, O4, O6, O7.

4. `projects/augmentor/ontology/unified-agent/sources.json`
   - Selectors: `/sources/*/{source_id,path,sha256,source_posture,owner}`.
   - Closes: O4, O7.

5. `projects/augmentor/ontology/unified-agent/nodes/nodes.json`
   - Selectors: `SourceRecord`, `DisposableSemanticIndex`, `ContextSnapshot`,
     `ReasoningRequest`, `JudgmentReceipt`, `MemoryIntakeRequest`,
     `OntologyCandidate`, `AuthorityDecision`.
   - Closes: O2-O6.

6. `projects/augmentor/ontology/unified-agent/relations/relations.json`
   - Selectors: source-to-context, index-to-source, context-to-index,
     context-to-reasoning, reasoning-to-judgment, judgment-to-approval,
     intake-to-provider, and candidate-to-owner relations.
   - Closes: O2-O6.

7. `projects/augmentor/ontology/unified-agent/views/knowledge.json`
   - Selectors: `/sequences`, `/allowed_readings`,
     `/forbidden_authority_moves`.
   - Closes: O2, O3, O6, O7.

8. `projects/augmentor/ontology/unified-agent/views/experience.json`
   - Selectors: `/sequences/AUG-EXP-ORDINARY`, `/allowed_readings`,
     `/forbidden_authority_moves`.
   - Closes: O2, O8.

9. `projects/augmentor/ontology/unified-agent/residue.json`
   - Selectors: `AUG-RES-001`, `AUG-RES-002`, `AUG-RES-005`,
     `AUG-RES-006`, `AUG-RES-007`.
   - Closes: O1, O5-O7, O9.

10. `projects/augmentor/ontology/unified-agent/receipts/validation-receipt.json`
    - Selectors: `/checks`, `/claim_ceiling`.
    - Closes: O9.

11. `research/2026-07-29-augmentor-unified-agent-architecture/findings.md`
    - Selectors: `#Status-and-direct-thesis`, `#Non-collapsing-object-model`,
      `#Exact-connection-catalog`, `#Capability-gap-modes`,
      `#Public-private-boundary`, `#Exact-future-v0-witness-contract`.
    - Closes: O1-O9.

12. `cyberAlchemy-v2/development/agent-reasoning-engine/spec/SPEC.md`
    - Selectors: evaluator outcome algebra, functional requirements,
      reasoning receipt, effort limits, and success boundary.
    - Closes: O2, O4-O6, O8, O9.

13. `../workspace-resonant/2.0.0-alpha/src/core/context-memory.ts`
    - Selectors: `ContextBudgetInput`, `buildContextBudget`,
      `shouldAutoCompactContext`, `shouldHardStopContext`,
      `formatCompactStateForPrompt`.
    - Closes: O3, O5, O8.

14. `../workspace-resonant/2.0.0-alpha/src/core/memory-provider.ts`
    - Selectors: `MemoryProviderBroker`, `capabilityGranted`,
      `livingArchiveMemoryProvider`, `httpJsonMemoryProvider`,
      `resolveMemoryProviderBroker`.
    - Closes: O1, O3, O5, O6.

## Evidence And Inference

Evidence establishes a private, candidate-local read model; immutable source
references; a provider search seam; context budgets; bounded evaluator
receipts; and strict non-authority boundaries. It does not establish a working
consultation API, neutral projection owner, approved authentication policy, or
measured answer quality.

The selected two-layer API and agent adapter is therefore a design inference,
not an observed runtime. It preserves existing ownership and gives later work a
small interface to test.

## Constraints And Non-goals

- Read-only consultation only.
- No arbitrary filesystem, graph query, or owner-service execution.
- No raw private ontology package in a consumer response.
- No trusted-memory intake or mutation.
- No ontology admission, promotion, routing, approval, or effects.
- No external research without a new, named gap and separate confirmation.
- No implementation or deployment in this run.

## Gaps And Resolutions

- Neutral projection owner: unresolved; the design names an interface and
  future owner decision instead of choosing an owner.
- Authentication and disclosure policy: unresolved; the design defines the
  required policy input and denies calls when it is absent.
- Measured budgets and answer quality: unresolved; the plan starts with local
  fixtures and configurable conservative defaults, not performance claims.
- Protocol choice: resolved for planning as one application service with a
  native agent-tool adapter first and an optional HTTP adapter later. This is a
  recommendation, not an owner-approved production decision.

## Fallback Exploration Rule

If an obligation remains unclear, inspect only the named source selector or its
owner-held contract. Record an explicit gap if that evidence does not close the
question. Do not expand to external research or infer owner approval.

## Authority Precedence

Owner-held source and runtime contracts outrank this context pack. The private
ontology is a candidate read model. Inventory and retrieval outputs are
discovery evidence only. The user confirmation authorizes this Refine run, not
implementation, promotion, or deployment.

