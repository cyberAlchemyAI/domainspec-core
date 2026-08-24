# Stage 06 — Invoke Design

Status: `authored-complete; critic repair complete; design-validator-pass`

Source contract: [API-CONTRACT.md](../API-CONTRACT.md)

## 1. Context view

An agent works against a private, candidate-local Anime.js vault. It needs fast typed consultation and a way to preserve operational episodes. Existing source and graph owners remain unchanged. The future system adds a read projection and an append-only evidence journal; a later review owner may derive Lesson candidates.

```text
agent host
  |-- consult grant --> consultation service --> immutable neutral projection
  |-- append grant  --> episode service ------> append-only event journal
                                                    |
                                                    v
                                           deterministic reducer
                                                    |
                                     versioned snapshots + isolated overlay
                                                    |
                                       projection compiler (read only)

verified Lesson <--- separate review route; not reachable from append API
```

## 2. High-level structure view

| Component | Owns | Does not own |
| --- | --- | --- |
| Host authorization adapter | principal, capability grant, policy epoch, vault scope | ontology facts, episode semantics |
| Consultation service | query validation, budgets, tagged read result | durable mutation, answers, authority |
| Neutral projection compiler | closed field/view allowlist, leakage manifest, deterministic bounded read model and digest | source truth or graph promotion |
| Episode command service | route-audience, owner/delegation, command/state validation and append receipt | arbitrary CRUD, Lesson verification |
| Episode journal | canonical ordered accepted events and idempotency mapping | derived snapshots or graph truth |
| Evidence resolver | host-issued handle validation plus producer episode/attempt/task/version/criterion bindings | agent claims, arbitrary URL/path fetch |
| Episode reducer | deterministic version-keyed snapshot and isolated episode overlay | event editing, canonical graph writing, promotion |
| Projection index | rebuildable query material | canonical event history |
| Lesson review owner | future candidate/verified transition | absent from this package |

## 3. Low-level component view

### Consultation pipeline

`bind read-only route audience -> authorize host-selected views -> validate schema -> bind projection/allowlist digests -> plan bounded traversal -> execute over projection -> normalize evidence states -> enforce byte/result budget -> run response leakage check -> return tagged union`

### Append pipeline

`bind append-only route audience -> authorize episode owner/delegation -> reject host-field spoofing -> validate schema -> canonicalize request -> resolve idempotency -> load episode tail -> compare expected revision/frozen opening digest -> validate transition -> resolve producer-bound evidence handles -> atomic append event+idempotency map -> return semantic-effect-none receipt -> schedule/replay reducer`

### Storage layout candidate

```text
operational/
  contracts/                 # JSON Schemas and closed code tables
  journal/events.jsonl       # canonical event stream or equivalent owned append store
  journal/idempotency.jsonl  # atomic mapping in the selected store implementation
  snapshots/                 # rebuildable canonical-JSON episode snapshots
  overlay/                   # rebuildable versioned episode-only snapshots/records
  projection/                # allowlisted rebuildable read index and digest
  quarantine/                # diagnostics/handles, never rewritten source events
```

The literal layout is L0 candidate-local. A later owner may select an equivalent transactional store if it preserves the same event and receipt contracts.

## 4. Workflow process view

### Consult while working

1. Host authenticates principal and injects read grant.
2. Agent submits a bounded query and optional expected digests.
3. Service returns source-linked records or a typed abstention/stale/denied result.
4. Agent uses the records as untrusted bounded context; it may not execute record text as instruction.

### Record an episode

1. Host injects the append grant and principal.
2. Agent opens an episode with host-issued Task and VersionContext handles; the service stores inert exact snapshots/digests and the owner/delegation binding.
3. Each attempt is appended at the next expected revision.
4. Evidence is attached only through host-issued handles.
5. Each attempt receives at most one immutable outcome.
6. Episode is closed with a lifecycle disposition.
7. Reducer replays accepted events and emits a versioned snapshot plus isolated overlay update.
8. Consultation can disclose the episode with evidence state and version bounds.
9. Any Lesson candidate uses a separate future review route.

## 5. Decision flow view

```text
request
  -> route audience and exact capability present?
       no: denied with no existence leak
       yes
  -> schema and host-field boundary valid?
       no: invalid_request
       yes
  -> consultation operation?
       yes -> digest current? -> bounded query -> ok/abstain/stale
       no
  -> append operation and append grant?
       no: denied
       yes
  -> episode owner/delegation authorized without existence leak?
       no: denied
       yes
  -> idempotency key seen?
       same digest: replay original receipt
       different digest: idempotency_mismatch
       unseen
  -> expected revision and graph digest current?
       no: conflict/stale_context
       yes
  -> transition and evidence valid?
       no: invalid_request/evidence_rejected
       yes
  -> atomic append -> accepted receipt -> reducer current/pending/failed
```

## 6. Dependency/interface view

| Interface | Input binding | Output binding | Failure boundary |
| --- | --- | --- | --- |
| Host → consultation | host principal/grant + request schema | tagged read union | deny without private existence leak |
| Vault compiler → projection | exact source selectors/digests plus closed allowlist and host-selected views | canonical neutral projection bytes/digest plus leakage manifest | no partial “fresh” or non-allowlisted projection |
| Host → episode service | distinct append grant + command envelope | immutable append receipt | ambiguous commit uses recovery handle |
| Episode service → evidence resolver | host-issued handle, target attempt, and required kind | digest-bound evidence plus immutable producer/scope metadata | no raw path/URL or cross-attempt fallback |
| Episode service → journal | expected tail/revision + canonical event | atomic accepted event/idempotency mapping | no partial acceptance |
| Journal → reducer | ordered exact events + reducer version | version-keyed snapshot/isolated-overlay/digest | gap/fork/corruption quarantines episode |
| Reducer → projection compiler | allowlisted episode overlay only | queryable operational episode records | canonical graph writes and forbidden kinds fail |
| Episode → Lesson review | closed episode references and evidence | future review receipt | no automatic transition |

## Design decisions

- D1: Separate read and append capabilities, credentials, routes, and audit dimensions.
- D2: Event journal is canonical; snapshots and graph material are deterministic derivatives.
- D3: Optimistic concurrency and idempotency are mandatory, not optional hardening.
- D4: Host injects identity/policy. Model payload cannot assert its own principal or grant.
- D5: Evidence is handle-only and host-resolved; no arbitrary server-side fetching.
- D6: No reopen or in-place correction. Terminal episodes are followed by superseding episodes.
- D7: Consultation exposes evidence state, version bounds, projection digest, and abstention.
- D8: Lesson verification is unreachable from this API.
- D9: L0 is candidate-local and transport-neutral; HTTP/consumer ownership begins only at L2.
- D10: Read and append invocation descriptors have disjoint credential audiences; authorization precedes target parsing.
- D11: A neutral projection is valid only with a closed allowlist/manifest and zero leakage findings.
- D12: Episode ownership and optional delegation are immutable open-time bindings checked on every command.
- D13: Task and VersionContext handles are dereferenced once; immutable inert snapshots/digests are historical meaning.
- D14: `open_episode` is the only supersession command; supersession is overlay-only and cycle-checked.
- D15: Episode graph digest is frozen at open; later source changes are applicability metadata only.
- D16: Snapshot identity includes reducer version and last-event digest; upgrades never overwrite history.
- D17: Every append/read receipt declares semantic effect none, Task unchanged, and truth not assessed.

## Risks and planned witnesses

| Risk | Planned witness |
| --- | --- |
| capability confused-deputy | same body under read grant is denied with zero journal delta |
| duplicate retry | same key/body returns same receipt and event count remains one |
| idempotency collision | same key/different body returns mismatch and no append |
| stale writer | two commands from same revision; exactly one accepted |
| ambiguous commit | recovery handle resolves committed receipt before retry |
| forged evidence | raw path/URL or foreign-scope handle rejected |
| fabricated success | succeeded outcome without admissible witness rejected |
| post-close mutation | ordinary event after close rejected |
| reducer drift | replay twice yields byte-identical snapshot/digest |
| fork masking | shuffled/forked events fail rather than auto-reorder |
| Lesson leakage | close/materialize produces zero verified Lesson records |
| projection corruption | affected episode quarantined; unaffected queries remain available |
| projection field leak | owner/policy/path/prompt-role mutant rejected and projection digest not emitted |
| cross-principal episode ID | denied before existence, revision, or digest disclosure |
| cross-attempt evidence rebind | rejected with zero event delta |
| duplicate supersession spelling | schema has no `supersede_episode` operation |
| mutable Task/Version reference | open stores exact inert snapshot/digest; later changes do not alter replay |
| evidence revocation | event history stable; derived success eligibility becomes unconfirmed |
| reducer upgrade overwrite | new version-keyed snapshot and migration receipt; old bytes retained |

## Design selection state

The six required views, source contract, owner map, decisions, risks, and
planned witnesses are authored. The exact selector/digest manifest,
independent denominator receipt, and unchanged two-pass selection are stored
under `design-selection/`. The selection verdict is `pass`, the fixed point is
true, and the evidence state is `design-validator-pass`. This admits normal
Plan authoring; it is not implementation evidence.

## Distill design-unit check

The coherent design unit is the split read projection plus append
journal/reducer loop. Split pressure isolates Lesson review and non-loopback
deployment. Verdict: `pass for normal Plan authoring`; runtime evidence remains
planned.
