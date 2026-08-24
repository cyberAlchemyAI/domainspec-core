# Queries: OpenAI Stock-Voice Audition

## InspectManifest

**Type:** Query (read-only)  
**Actor:** Owner, operator, reviewer, or later Task Session

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| manifest_path | path | yes | Candidate manifest under the future audition runtime root. |

### Output

| Field | Type | Source | Description |
|---|---|---|---|
| manifest_digest | SHA-256 | AuditionManifest | Identity of canonical manifest bytes. |
| state | AuditionState | AuditionManifest | Current lifecycle state. |
| unresolved_gates | list | AuditionManifest | Exact blockers; empty only when admitted. |
| request_preview | JSON | ManifestToSpeechRequest | Redacted provider payload with no authorization header. |
| source_bindings | list | AuditionManifest | Frozen excerpt, provider docs, and owner-decision bindings. |

### Reads from

| Entity | Relationship | Fields used |
|---|---|---|
| AuditionManifest | queries | all non-secret persisted fields |

This query performs no provider call and cannot change admission.
