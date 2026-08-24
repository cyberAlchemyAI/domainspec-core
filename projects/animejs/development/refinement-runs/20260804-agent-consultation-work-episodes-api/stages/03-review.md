# Stage 03 — Interrogation Refine Review

Status: `pass`

## Dialectic

### Proposer

One agent API should make both retrieval and learning convenient.

### Authority critic

“One API” hides two materially different effects. If the same route or credential both retrieves and persists, prompt-shaped data can cross from untrusted consultation context into durable evidence without a separately auditable decision.

### Synthesis

Keep one conceptual developer package but expose distinct operations, capability grants, state namespaces, and receipts. A consumer may present them through one agent tool registry; it must not combine their authorization.

## Questions and resolutions

| Question | Resolution |
| --- | --- |
| Can an agent create a Task while opening an episode? | L0 `open_episode` accepts either an existing Task ID or an immutable `task_snapshot` and derives a content-addressed candidate Task atomically. It cannot edit an existing Task. |
| Can it create a VersionContext? | L0 requires a closed `version_context_snapshot`; its ID is content-addressed. Known contexts may be referenced by ID. No “latest” default is allowed. |
| Can an agent attach a filesystem path or URL? | No. It submits only a host-issued EvidenceHandle. Evidence intake and redaction are separate owner operations. |
| What is canonical? | Ordered EpisodeEvents in the append journal. Snapshots, graph deltas, and indexes are rebuildable projections. |
| How are corrections made? | Append a corrective event where allowed, or open a new episode that `supersedes` the closed/incorrect episode. Never edit history. |
| Does closing an episode create a Lesson? | No. Lesson derivation and verification are a separate later route. |
| Can an episode be reopened? | No. Closed terminal state is immutable; follow-up work uses a new linked episode. |
| Can the model choose its principal or grant? | No. The host injects authenticated principal, capability, policy epoch, and allowed project/vault scope. |

## Residue

- A concrete host owner is unnecessary for L0 contracts/reducer proof but required before a network route.
- Retention/redaction policy for accepted event payloads must be selected before production data.
- Verified Lesson review remains a separate future design.

## Verdict

No local evidence gap blocks design. The split route survives usefulness and authority pressure.
