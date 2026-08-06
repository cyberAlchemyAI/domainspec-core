# Interrogation — Refine Design Review

## Highest-discrimination question

**Does the first bilateral adapter prove a universal protocol, or only prove that one boundary can be projected safely?**

Safe default: it proves only the named WPRA-to-Task-Session boundary. No operator answer is needed because calling one adapter universal would exceed the evidence. Extraction of common fields requires at least a second materially different boundary and matching behavior evidence.

## Dialectic trace

| Design advocate | Risk reviewer objection | Disposition | Repair |
|---|---|---|---|
| A shared causal journal gives durable coherence. | A new global store can become operational truth and duplicate observability. | revise | Define a causal-event projection contract, not one mandated store. Existing runtime/observability owners choose storage; events remain non-authoritative. |
| OBTC validates owner roles. | An `effect_owner` field can be syntactically singular but semantically wrong. | accept | Structural pass is insufficient; consumer owner emits separate semantic/admission receipt. |
| Task Session owns the cursor. | The ordered-series reducer may try to write or reinterpret it. | accept | Task Session produces cursor under current contract; series owner consumes it and owns only frontier advancement. |
| Bilateral adapters avoid a flag day. | Shadow comparison can quietly become dual write. | accept | Native owner remains the sole authoritative writer; projection mismatch blocks cutover but never rewrites native evidence. |
| Version declarations protect compatibility. | A protocol steward could force a version on owners. | accept | Steward has no effect authority; owner-local acceptance declaration is mandatory. |
| Outcome-unknown solves crash safety. | It only names the state; it does not prove reconciliation works. | accept | Require effect-owner reconciliation fixtures and later real crash-boundary evidence; no exactly-once claim. |
| Private payloads are excluded by convention. | Identifiers, paths, and examples can still leak. | accept | Add field classification, public allowlist, redaction, and fixture scan gates. |

## Gate review

| Gate | Verdict | Reason |
|---|---|---|
| One effect owner per transition | pass for designed transitions; unresolved owner ports block their transitions | explicit owner matrix |
| Structural-versus-semantic authority | pass | separate validator and owner decision receipts |
| Crash/replay | flag | design is coherent; execution evidence absent |
| Compatibility | pass for planning | bilateral adapter and one-writer rule |
| Causal journal authority | pass after repair | projection contract only, storage owner remains local |
| Series ownership | flag | recommendation exists; lifecycle acceptance pending |
| Public/private | flag | design gate exists; scan evidence absent |
| Plan handoff | pass to non-executed Invoke Plan | design-validator-pass; mutation handoff remains blocked |

## Stable residue

- Decision Gate: series owner, protocol steward, material producer, registry release.
- Execution evidence: crash reconciliation, concurrent CAS/lease, privacy scan, second-boundary generalization, real E2E.
- Canonical maintenance: Orchestrate defects and generated parity.

## Structured Interview Result

- Target scope: `stages/06-invoke-design.md`
- Mode: refine-design-review
- Questions asked: 0 operator questions; 1 internal highest-discrimination question
- Decisions recorded: causal journal becomes a projection contract; generalization requires a second boundary
- Artifacts updated: carried to Distill Repair and Plan
- Remaining ambiguities: four owner decisions and unexecuted evidence
- Verdict: flag
- Next step: controlled protocol toy game and repair

The flag blocks architecture promotion or implementation readiness, not completion of a non-executed plan with explicit gates.

