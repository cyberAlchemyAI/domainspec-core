# Events: OpenAI Stock-Voice Audition

These are planned repository-local lifecycle records, not a message bus.

## ManifestAdmitted

**Produced by:** FreezeManifest  
**Transition:** `not_ready -> admitted`

Payload: manifest ID/digest, closed gate IDs, source digests, decision-owner IDs, UTC timestamp. No credential.

## TwoRendersCaptured

**Produced by:** RenderCandidate  
**Transition:** `admitted -> rendered`

Payload: manifest digest, two attempt IDs, raw SHA-256 values, redacted request digest, request/response IDs where available, timing, billed units where available, native format metadata.

## CandidateVerified

**Produced by:** VerifyCandidate  
**Transition:** `rendered -> verified`

Payload: attempt and derivative hashes, format inspection, duration, normalization metrics, alignment result, independent-fidelity result, manual phrase review, reviewer ID.

## CandidateRejected

**Produced by:** RenderCandidate or VerifyCandidate  
**Transition:** `rendered|verified -> rejected`

Payload: exact disqualifier, affected attempt/manifest hashes, reviewer, UTC timestamp. Rejection does not delete evidence.

## CandidateBlinded

**Produced by:** BlindCandidate  
**Transition:** `verified -> blinded`

Payload: opaque asset IDs, listener-order manifest hashes, protected unblinding-key locator, rubric version.

## OperatorDecisionRecorded

**Produced by:** RecordOperatorDecision  
**Transition:** `blinded -> decided`

Payload: named operator, `approve|reject|defer`, reasons, candidate and evidence hashes, UTC timestamp. It grants no release or deployment authority.
