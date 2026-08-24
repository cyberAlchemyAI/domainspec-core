# TASK-OAVA-CONSULTATION — Candidate consultation gate

## Task objective

Provide one deterministic, consumer-owned boundary that builds the Sequence 6 animation candidate, consults the existing local Anime.js vault, binds the exact returned evidence identities, and refuses tournament eligibility unless every hard trust gate passes.

Layer: L0. Captured unit: `SWU-OAVA-002` only.

## Source contracts

- `INTERFACES.md` — `buildCandidate` and `consultCandidate` contracts.
- `STATES.md` — `draft`, `consultation_pending`, `consultation_blocked`, and `tournament_eligible` transitions.
- `stages/06-design.md` — S6 source meaning, hard-gate ordering, and claim boundary.
- `VALIDATION-CONTRACTS.md` — causal negative controls and zero-delta obligations.
- `prototype/contracts/animation-hypothesis-candidate.schema.json` and `prototype/lib/validate-candidate.mjs` — completed OAVA-001 consumer boundary.
- `projects/animejs/ontology/agent-knowledge-vault/operational/` — existing transport-neutral capability, consultation, and projection contracts.
- `projects/animejs/ontology/agent-knowledge-vault/views/task-recipes.json` and `views/documentation-coverage.json` — read-only local evidence views.

## Primary behavior and atomicity

The unit implements four collaborating pieces as one atomic consumer behavior:

1. `buildCandidate(sceneBeat, residue)` reconstructs the already-valid OAVA-001 seed deterministically from its source-bound parts. It preserves the schema-valid `abstain` posture and existing source binding; it does not invent an unsupported `consultation_pending` value or fake consultation evidence.
2. `consultCandidate(candidate, hostContext)` uses the exact `animejs-knowledge-consult-read` capability, compiles an allowlisted local neutral projection, and returns a consumer receipt containing the unchanged service request/result plus the current projection fingerprint. Typed negatives are never converted into success.
3. A pure receipt-binding helper creates a new OAVA-002 candidate only for a current, correlated, non-empty `ok` receipt. Non-`ok` receipts remain outside the candidate as `consultation_blocked` evidence, so the closed candidate schema is not weakened.
4. `evaluateEligibility(candidate, receipt, validation)` applies hard gates before any score and returns one stable decision code.

Splitting the adapter from the eligibility gate would permit a temporary consumer that treats records, empty results, or typed failures as success. Runtime, scene construction, animation, browser evidence, review, and episode capture remain independently testable later units.

## Inputs

- Completed valid candidate fixture and source snapshot from OAVA-001.
- Current candidate schema and validator.
- Host-injected principal/workspace, policy epoch, request identity, exact audience credential, authorization port, view grants, bounded limits, and expected graph/projection digests.
- Canonical vault task-recipe/documentation views and operational library modules, all read-only.
- Version context `animejs@4.5.0`; this is documentation/source context, not runtime proof.

## Exact material writes

- `prototype/lib/build-candidate.mjs`
- `prototype/lib/consult-animejs.mjs`
- `prototype/lib/evaluate-eligibility.mjs`
- `prototype/test/consultation.test.mjs`

No directory glob is authorized.

## Consultation projection and request

The consumer adapter must:

1. Read only the canonical allowlist, task recipes, and documentation-coverage view beneath the injected vault root.
2. Require the view graph digests to agree; any parse/read/drift failure returns `temporary_failure` or `stale` with zero evidence.
3. Convert only allowlisted recipe/documentation fields into neutral records. Instruction-shaped text remains inert data.
4. Compile a deterministic projection with the existing `compileNeutralProjection` export and hash it through the existing `canonical-json.mjs` behavior.
5. Import exactly `createCapabilityAdapters`, `createConsultationService`, and `compileNeutralProjection` from the resolved canonical vault root. Invoke through the adapter; never bypass exact audience or host `authorize` checks.
6. Look up exactly `recipe:consult:timeline`, `recipe:consult:svg`, and `topic:documentation:svg/createdrawable` for this candidate.
7. Preserve the closed `animejs-knowledge-consult-request/0.1.0` body and unchanged `animejs-knowledge-consult-result/0.1.0` result in a consumer envelope. The request binds version context, expected graph/projection digests, limits, and exact lookup nodes; the result binds request ID, policy epoch, graph/projection digests, records, explanation path, and typed diagnostic.
8. Preserve `ok`, `abstain`, `stale`, `denied`, `invalid_request`, and `temporary_failure` exactly.
9. Return no fallback records, fabricated evidence, arbitrary path supplied by the candidate, or write effect.

## Eligibility algorithm and failure precedence

1. If the OAVA-001 seed validation result is not `VALID`, return `CANDIDATE_INVALID`.
2. If the consumer request ID, host request ID, and service result request ID differ, return `CONSULTATION_REQUEST_MISMATCH`.
3. If the requested Anime.js version context is not exactly `4.5.0`, return `VERSION_CONTEXT_MISMATCH`.
4. If result status is `stale`, return `CONSULTATION_STALE`.
5. If result status is any other non-`ok` value, return `CONSULTATION_NOT_OK` and preserve the source status and diagnostic.
6. If result graph or projection digest differs from the consumer receipt's current projection fingerprint or the request's expected digest, return `CONSULTATION_STALE`.
7. If records, explanation path, or evidence identities are empty, return `CONSULTATION_EVIDENCE_EMPTY`.
8. Bind the receipt into a new candidate, re-run `validateCandidate`, and return `CANDIDATE_INVALID` if the derived candidate fails the completed contract.
9. If derived candidate status is not `ok` or its evidence bindings do not exactly equal the sorted unique evidence handles returned by the result, return `CONSULTATION_BINDING_MISMATCH`.
10. If contradiction status is not `clear`, return `CONTRADICTION_OPEN`.
11. If standard and reduced terminal semantics differ, return `REDUCED_MOTION_MISMATCH`.
12. Otherwise return `TOURNAMENT_ELIGIBLE` with `eligible: true`, `semantic_effect: none`, and the exact evidence identities. This authorizes no implementation.

## Causal cases

- Repeated builds from equal inputs are byte-equivalent and do not mutate inputs.
- Current authorized consultation makes one non-mocked call through the actual local capability/service/projection exports and returns the three exact local record IDs and their documentation evidence handles.
- Wrong expected graph or projection digest returns `stale` and zero records.
- `abstain`, `denied`, `invalid_request`, and `temporary_failure` receipts each return ineligible without fallback.
- Empty successful receipt, request mismatch, version mismatch, candidate/result status mismatch, and evidence-binding mismatch each fail with one stable code.
- OAVA-001 invalid result, unresolved contradiction, and reduced-motion mismatch remain hard failures.
- Before/after SHA-256 maps for canonical vault files are identical.
- Static source scan finds no URL fetch, HTTP client, process execution, vault write, or runtime Anime.js import.

## Expected decision shape

```json
{
  "eligible": true,
  "code": "TOURNAMENT_ELIGIBLE",
  "state": "tournament_eligible",
  "evidence_bindings": ["evidence:documentation:..."],
  "semantic_effect": "none",
  "claim_limit": "consultation evidence only; no runtime proof"
}
```

Negative results set `eligible` to `false`, use one stable code and state, preserve the typed consultation status when applicable, and return no implementation authority.

## Validation and acceptance evidence

Run from the refinement-run root:

```text
node --test prototype/test/consultation.test.mjs
node --test prototype/test/candidate.test.mjs
```

Acceptance requires every causal case to pass, no undeclared writes, exact material reconciliation, zero byte delta under the source video package, `projects/autoads/`, and `projects/animejs/ontology/agent-knowledge-vault/`, and a terminal Task Session receipt whose claim ceiling remains consultation-only.

## Execution owner and handoff

Task Session owns the single-use implementation execution. `invoke:refresh:apply-approved` owns closeout synchronization. The terminal handoff may expose `SWU-OAVA-003` but must set `successor_executed=false`.
