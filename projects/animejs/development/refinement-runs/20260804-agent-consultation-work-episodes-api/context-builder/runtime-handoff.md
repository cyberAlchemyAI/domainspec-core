# Runtime Handoff Pack

## Identity

- Task/SWU: `REFINE-AKVE-API`
- Source task/work-pack: `REFINE-SEED-PROPOSAL.md`
- Session/run id: `20260804-agent-consultation-work-episodes-api`
- Session evidence path: `projects/animejs/development/refinement-runs/20260804-agent-consultation-work-episodes-api/`
- Runtime handoff: `runtime`
- Repository revision: `ab46061bf14db23a01054c2fd3fafec60fb5eb2f`
- Evidence date: `2026-08-04`

## Obligation Coverage

| Obligation | Status | Selected evidence | Resolution |
| --- | --- | --- | --- |
| O1 current vault boundary | covered | `profile.json` and `ONTOLOGY-VAULT-RESULT.json` | private candidate, authority effect none |
| O2 episode semantics | covered | `contracts/node-vocabulary.json` | append-only WorkEpisode/Attempt/Outcome and reviewed Lesson transition |
| O3 relation semantics | covered | `contracts/relation-vocabulary.json` | usesVersion, producedEvidence, supportedByEvidence, generalizesFrom, boundedBy, invalidatedBy, supersedes |
| O4 current query surface | covered | `scripts/query.mjs` | CLI coverage/decision only; agent API is absent |
| O5 current consultation precedent | covered | Augmentor Refine result and current consumer API guide | read-only neutral projection with separate authorization |
| O6 implementation authorization | resolved | user intent plus Refine boundary | design/plan only; future task selection remains unapproved |

Strict coverage: `pass`

## Architecture Guidance

Use capability separation and event sourcing. Append commands produce immutable receipts. Reducers and graph materializers are deterministic consumers, not alternative writers. A Lesson requires a later review route.

## Constraints And Non-Goals

- No direct mutation of existing vault bytes.
- No combined consult-and-write key.
- No arbitrary server-side path or URL fetch from an agent payload.
- No automatic Lesson verification.
- No external research in this run.
- No consumer/runtime integration in this run.

## Validation Surface

- JSON Schema fixtures for query, commands, events, receipts, and reductions.
- Deterministic reducer replay and shuffled-input negative control.
- Idempotency and stale-revision integration fixtures.
- Capability-separation and evidence-handle security fixtures.
- Existing vault validation plus graph digest preservation.

## Gaps And Blockers

- The exact future host for the append capability is not selected; L0 remains candidate-local.
- Non-loopback transport, identity federation, and deployment remain L3 decisions.
- Lesson verification workflow is explicitly deferred to a separate owner.

## Authority Precedence

1. Direct current vault contracts and source digests.
2. Current consumer-owned Augmentor API contract for read-only precedent.
3. Inventory and memory as discovery only.

## Output Paths

- Markdown: `context-builder/runtime-handoff.md`
- JSON/index: `context-builder/runtime-handoff.index.json`
