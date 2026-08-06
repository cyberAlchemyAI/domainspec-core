# Mappings

| Source | Target | Rule |
|---|---|---|
| runtime raw capture | `intent-route.request@1` | Preserve raw value/ref, source digest, posture, evidence refs, and unresolved fields; reject unmapped required structure. |
| canonical capability/Dispatch owners | route catalog | Project stable IDs, revisions, digests, predicates, exclusions, and dominance without creating identities. |
| disposition | runtime display | Preserve kind, candidates, traces, reason codes, clarification, digests, and `authority_effect`. |
| confirmed Dispatch/group/seat | host workflow binding input | Separate post-human binding; never synthesize from a resolver candidate. |
| private IntentRecord | generic request | Optional private compatibility mapper owned by CAV2; not public canonical source. |

