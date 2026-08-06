# Operations: OpenAI Stock-Voice Audition

## FreezeManifest

**Type:** Operation  
**Actor:** Audition operator with recorded owner decisions  
**Triggers:** Request to prepare one exact candidate without rendering

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| excerpt_path | path | yes | Exact `audition-excerpt.txt`. |
| model_snapshot | string | yes | Dated model ID; alias-only manifests fail. |
| voice_id | string | yes | One documented stock voice. |
| accent_locale_decision | record | yes | Owner choice or explicit provider-native variation. |
| instructions | string | yes | Frozen non-spoken delivery instruction. |
| response_format | enum | yes | `wav` for this audition. |
| account_gate_receipts | references | yes | Actual-account rights, public-use, disclosure, data, retention, and security decisions. |
| tool_manifest | record | yes | Pinned count, decode, normalize, alignment, fidelity, VTT, and randomization tools. |

### Rules

| ID | Rule | Formal |
|---|---|---|
| FM-1 | Every required field is concrete and digest-bound. | `unknown_count == 0` |
| FM-2 | Voice is stock, not custom or cloned. | `voice_kind == stock` |
| FM-3 | Exact excerpt fits the documented selected-route limit. | `measured_tokens <= 2000` |
| FM-4 | Request preview contains no credential. | `secret_fields == 0` |
| FM-5 | Unsupported controls are absent. | `request_keys ⊆ documented_keys` |

### State transition

`AuditionState: not_ready -> admitted`

### Postconditions

- Canonical manifest bytes and SHA-256 are frozen.
- Redacted request preview is reproducible from the manifest.
- Admission receipt identifies every closed gate and owner.

### Error states

| Condition | Result |
|---|---|
| Missing owner/account/tool decision | Remain `not_ready`; name the exact blocker. |
| Stale source or provider-doc digest | Remain `not_ready`; refresh sources. |
| Secret-shaped value in persisted material | Reject and emit no preview. |

## RenderCandidate

**Type:** Operation  
**Actor:** Authorized local operator  
**Triggers:** Explicit later selection of a render SWU after admission

### Rules

| ID | Rule |
|---|---|
| RC-1 | Require an exact admitted-manifest digest. |
| RC-2 | Read the credential from process environment without printing or persisting it. |
| RC-3 | Submit the whole frozen excerpt once per repetition. |
| RC-4 | Produce exactly two repetitions with identical request fields. |
| RC-5 | Write each raw response to a new run-scoped path; never overwrite. |

### State transition

`AuditionState: admitted -> rendered`

### Error states

| Condition | Result |
|---|---|
| HTTP, timeout, truncation, or partial-write failure | Preserve diagnostic metadata without a false rendered receipt; do not retry automatically. |
| Existing target path | Stop before network call. |
| First-take “Body War” mispronunciation | Transition to `rejected`; no pronunciation workaround. |

## VerifyCandidate

**Type:** Operation  
**Actor:** Verification operator independent of forced alignment  
**Triggers:** Two immutable raw responses exist

### Rules

| ID | Rule |
|---|---|
| VC-1 | Verify hashes, WAV structure, duration 75–120 seconds, sample rate, bit depth, channels, and no truncation. |
| VC-2 | Force alignment supplies timing evidence only. |
| VC-3 | Independent transcription or token-by-token listening supplies word-fidelity evidence. |
| VC-4 | Every mismatch or low-confidence token requires manual resolution. |
| VC-5 | Manually inspect “approved,” the question, “time, confidence, and authority,” “Body War,” and “ask the responsible owner—or stop.” |

### State transition

`AuditionState: rendered -> verified | rejected`

## BlindCandidate

**Type:** Operation  
**Actor:** Blinding operator  
**Triggers:** Candidate has a passing verification receipt

### Rules

| ID | Rule |
|---|---|
| BC-1 | Use opaque candidate and repetition IDs. |
| BC-2 | Keep unblinding key separate until score sheets are locked. |
| BC-3 | Separate repetitions in each listener order. |
| BC-4 | Preserve raw score sheets and deterministic formula output. |

### State transition

`AuditionState: verified -> blinded`

## RecordOperatorDecision

**Type:** Operation  
**Actor:** Named production operator  
**Triggers:** Technical gates and blind listening are complete and unblinded

### Rules

| ID | Rule |
|---|---|
| OD-1 | Outcome is exactly `approve`, `reject`, or `defer`. |
| OD-2 | Decision cites candidate, waveform, verification, score-sheet, and unblinding hashes. |
| OD-3 | Scores are advisory and cannot override rights, data, fidelity, or operator judgment. |

### State transition

`AuditionState: blinded -> decided`
