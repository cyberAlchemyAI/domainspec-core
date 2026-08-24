# Stage 02 — Invoke Define

Status: `pass`

## Problem statement

Agents need a stable way to retrieve bounded Anime.js knowledge while acting and to leave behind evidence-bearing operational history. The system must make that history reusable without allowing an agent to rewrite documentation truth, manufacture evidence, or self-verify a Lesson.

## Defined capability surface

1. `animejs-knowledge-consult-read`
   - deterministic reads over a digest-bound neutral projection;
   - no durable mutation;
   - results cite node, relation, source, graph, and projection identities.
2. `animejs-work-episode-append`
   - append typed commands to a canonical event journal;
   - distinct credential/grant and host-injected principal;
   - optimistic concurrency plus idempotency;
   - returns an immutable append receipt.
3. `animejs-work-episode-project-read`
   - reads reducer-produced episode snapshots and candidate episode graph material;
   - may be served by the consultation owner once projection compilation is accepted;
   - has no write authority.
4. Lesson review is not an API operation in this package.

## Core definitions

| Term | Definition | Non-collapse rule |
| --- | --- | --- |
| ConsultationProjection | Immutable, bounded, neutral read model compiled from declared vault inputs. | Not the source, graph writer, or authority owner. |
| EpisodeCommand | Authenticated request to append one allowed state transition. | Not an event until validated and accepted. |
| EpisodeEvent | Immutable canonical record of one accepted transition. | Never edited or deleted by correction. |
| AppendReceipt | Digest-bound proof that a command was accepted, replayed, or rejected at a specific revision. | Not proof that the event's substantive claim is true. |
| EpisodeSnapshot | Deterministic reducer output for one episode and revision. | Rebuildable; not a second canonical store. |
| EvidenceHandle | Host-resolved reference to bounded evidence plus digest and evidence kind. | Agent-provided prose/path/URL is not evidence. |
| ClosedEpisode | Episode whose lifecycle accepts no further ordinary events. | Not necessarily succeeded and never automatically a Lesson. |
| LessonCandidate | Separately derived claim proposed from one or more closed episodes. | Not verified; absent from the append command set. |

## Acceptance conditions

- Consultation keys cannot append.
- Append keys cannot bypass command/state validation.
- Repeating the same idempotency key and body returns the same event/receipt; reusing it with a different body fails.
- Stale expected revisions fail without append.
- Reducer replay over canonical order is deterministic and digest-stable.
- Malformed, dangling, fabricated, oversized, or unauthorized evidence handles fail closed.
- Episode close cannot imply succeeded outcome or verified Lesson.
- A superseding episode references, but never mutates, the superseded episode.

## Template and technique selection

- Template: DomainSpec architecture profile plus standalone implementation-layering/work-pack companions.
- Glossary status: `linked` to existing node/relation vocabulary; new API transport terms remain candidate-local.
- Discovery: satisfied by the completed vault, current code, Inventory preflight, and Augmentor precedent.
- Distill sanity: required because read, write, projection, and promotion were initially bundled; split selected.
- Techniques: sequence, route menu, owner-boundary check, state-namespace boundary, and memory-promotion split.

## Invoke result

- Mode: `define`
- Phase status: `pass`
- Decisions: split capabilities; journal is canonical operational evidence; Lesson verification excluded
- Unresolved gaps: future host selection and non-loopback identity/deployment
- Next route: `design`
