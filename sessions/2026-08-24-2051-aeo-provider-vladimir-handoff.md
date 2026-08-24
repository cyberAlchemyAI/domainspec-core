---
node_type: session-handoff
session_id: aeo-provider-scope-2026-08-24-2051
date: 2026-08-24
topic: AEO provider-scope owner classification
status: ready-to-send
handoff_type: owner-decision
destination: Vladimir
target_project: domainspec-core
authority_level: session-evidence
source_dispatch: 2026-08-24-aeo-provider-owner-handoff-robot-talks
review_dispatch: 2026-08-24-aeo-provider-owner-handoff-review
---

# Session Handoff: AEO Provider Scope

## Identity and boundary

- Handoff ID: `aeo-provider-scope-2026-08-24-2051`
- Destination: Vladimir
- Requested action: answer within established authority or identify the accountable owner and route
- Authority effect: none

You built the AEO and are the best first technical interlocutor for clarifying
the original intent of its provider boundary. The inspected ownership artifacts
name `domainspec-core` or `domainspec-core operator`, not a person, so this
handoff does not presume that you are the final product owner
([`SPEC.md`](../implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md),
[`PROJECT-OVERVIEW.md`](../implementation/domainspec/docs/interviews/agent-execution-orchestrator/PROJECT-OVERVIEW.md)).

This is a private clarification request. It is not an implementation assignment
or an authority-bearing product decision.

## Bounded evidence

- The selected delivery baseline is one Sandcastle adapter, and the owning story
  requires `sandcastle`
  ([`PROJECT-DECISIONS.md`](../implementation/domainspec/docs/interviews/agent-execution-orchestrator/PROJECT-DECISIONS.md),
  [`WORK-PACK.md`](../implementation/domainspec/docs/features/agent-execution-orchestrator/WORK-PACK.md),
  [`STORIES.md`](../implementation/domainspec/docs/features/agent-execution-orchestrator/STORIES.md)).
- Avoiding hard coupling to one provider is stated, while supporting multiple
  providers remains classified as hypothesized
  ([`PROJECT-OVERVIEW.md`](../implementation/domainspec/docs/interviews/agent-execution-orchestrator/PROJECT-OVERVIEW.md)).
- The executable input accepts `provider: "sandcastle" | "custom"`, but the
  object that executes is a separately injected `SandboxProviderPort`; the label
  does not select or identify that object
  ([`models.ts`](../implementation/domainspec/backend/src/modules/agent-execution-orchestrator/domain/models.ts),
  [`execute-pipeline-route.ts`](../implementation/domainspec/backend/src/modules/agent-execution-orchestrator/application/execute-pipeline-route.ts)).
- `custom` is described as a future extension hook, while
  `approvedExtensionSet` appears in the operation rule without a located owner
  or executable admission surface
  ([`domain.md`](../implementation/domainspec/docs/features/agent-execution-orchestrator/domain.md),
  [`operations.md`](../implementation/domainspec/docs/features/agent-execution-orchestrator/operations.md)).
- The bounded caller search found an implemented and tested execution boundary,
  but no independent non-test use-site choosing between providers. This does not
  establish a current operational defect or an owned multi-provider capability.

## Owner questions

1. For `input.provider = custom` and `approvedExtensionSet`, considered
   separately, what current operative effect or obligation does each have, if
   any; what may current AEO contracts or callers rely on; and which owner
   capacity and authority-bearing source establish that answer? `Unknown` or
   `pending owner decision` is a valid answer, but leaves the handoff open.
2. Is there currently any stakeholder and owned scenario within AEO scope that
   requires a provider other than Sandcastle? If so, please identify the
   scenario, its product or operational consequence, the AEO invariants it must
   preserve, what changes—if anything—and its owner and authority-bearing source.
   A recorded, owner-backed answer that no such scenario exists is terminal for
   new alternate-provider capability machinery.
3. Do one or more authority-bearing AEO decisions already answer all or part of
   either question? If so, please cite the exact private artifacts and identify
   which requested classifications, if any, remain unresolved.
4. For every requested classification that remains unresolved, do you have the
   acting-owner capacity to make it? In every branch, please identify the
   authority-bearing source or destination artifact. If you do not have that
   capacity, please identify the accountable owner or role and the exact private
   route. Please also identify the coordination/follow-through owner and the
   return, record, and closure route; coordination does not confer authority over
   the AEO decision.

Please describe the intended status in the AEO's own vocabulary. The questions
do not assume a predefined classification or remediation.

## What this handoff does not request

It does not request or presume:

- a provider registry, descriptor, identity/digest, compatibility certificate,
  or admission gate;
- selection, failover, migration, cross-provider resume, upgrade continuity,
  replay, or pairwise substitution;
- `GovernedTypedGraph` or another evidence carrier;
- CyberAlchemy promotion or an Arcanum/public contract;
- implementation work or a Lean theorem.

Those would require a separate, owner-backed scenario and decision. They cannot
be inferred from provider-agnostic dependency injection or from the presence of
future-facing vocabulary.

## Decision trace after the response

1. **One or more authority-bearing decisions already exist:** cite them and close
   each resolved part by reference rather than creating another decision. The
   handoff as a whole closes only if those decisions classify both terms
   separately and answer the owned alternate-provider scenario question;
   otherwise continue the trace for the unresolved parts.
2. **For each unresolved part not covered by a located decision:** establish the
   acting-owner capacity, authority-bearing destination artifact, coordination
   owner, and exact return, record, and closure route.
3. **Authority or route is absent or unknown:** keep the handoff pending and
   non-authoritative while the accountable owner or role is located. A technical
   opinion alone cannot close it.
4. **An authorized owner answers the unresolved parts:** classify each
   still-unresolved term separately, answer any still-unresolved owned
   alternate-provider scenario question and its consequence, and record those
   answers in the authority-bearing artifact.
5. **The recorded answer finds no owned scenario:** close without new
   alternate-provider selection, admission, migration, substitution,
   CyberAlchemy, Arcanum, or Lean machinery. Any source-local documentation,
   vocabulary, validation, or model alignment remains a separate owner-scoped
   decision that this handoff does not authorize.
6. **The recorded answer identifies an owned scenario:** open only a separate
   source-local scope decision with its owner and preserved invariants. The
   answer does not automatically select or authorize a technical design.

## Collapse-test

If existing owner-backed decisions already classify `custom` and
`approvedExtensionSet` separately and answer whether an owned
alternate-provider scenario exists, this handoff contributes nothing beyond
locating them. If an authorized owner records that no owned alternate-provider
scenario and consequence exist, every proposal for new alternate-provider
selection, admission, migration, or substitution machinery collapses and the
result is scope clarification. That conclusion does not decide whether
source-local documentation, vocabulary, validation, or model alignment is
needed; such alignment requires a separate owner-scoped decision and is not
authorized by this handoff.

## Validation receipt

The source handoff was reviewed by three independent attackers across
fidelity/governance, mechanics/correctness, and abuse/gaming. Two independent
verifiers sustained the corrected artifact, and the final coverage audit passed.
The current review verdict is `KEEP`. This receipt validates only the handoff's
question shape and authority boundary, not an AEO capability or design.
