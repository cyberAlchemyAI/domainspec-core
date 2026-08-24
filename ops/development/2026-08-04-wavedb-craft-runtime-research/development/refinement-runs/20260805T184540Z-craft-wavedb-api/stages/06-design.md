# Stage 06 — Invoke Redefine and Design

## Invoke result

- Mode: `design`
- Phase status: `pass`
- Profile: DomainSpec architecture profile
- Design selection: `design-selection/selection-result.json`, `pass`
- Evidence state: `design-validator-pass`
- Evidence ceiling: Design selection and authored contracts only; planned tests
  are not Plan evidence
- Selected companions: authority/trust, security/abuse, persistence/concurrency,
  failure/compensation, integration/versioning, privacy/data lifecycle,
  validation contracts
- UX companion: not applicable; no rendered human semantic surface
- Plan evidence: `plan-evidence-pending`
- Work Pack: not created at this stage

## Redefined unit

The first system is not “Craft on WaveDB.” It is a read-only snapshot
consultation service whose sole durable input is one immutable, fully verified
WaveDB projection. Source-ledger ownership, refresh, and source mutation remain
outside the service.

## 1. Context view

Craft owners write `.craft/ledger.yml`. A separately authorized builder can
produce a derived snapshot. Authorized local agents/tools consult that snapshot
through a private service. The service never becomes an owner, writer, promoter,
or proof of current source truth.

## 2. High-level structure view

```text
caller -> authentication -> authorization policy -> HTTP contract
                                                -> snapshot catalog
                                                -> raw reader
                                                -> conditional row adapter
immutable WaveDB handle -> integrity verifier ---^
optional source observer -> freshness record ----^
```

The source observer and snapshot builder are external capabilities. They are not
request handlers and are not included in L0 implementation.

## 3. Low-level components view

| Component | Owns | Does not own |
| --- | --- | --- |
| HTTP transport | parsing, status, headers, problem responses | policy or persistence |
| Policy port | principal/action/resource decisions | identity provider or source state |
| Snapshot loader | open, byte normalization, manifest/record closure | writes or repair |
| Space catalog | opaque IDs, authorized metadata, pagination | global project identity |
| Raw reader | exact verified bytes and ETag | YAML semantics |
| Normalizer registry (L1) | version adapter selection and row envelopes | source migration |
| Row index (L1) | family-scoped unique lookup | source authority or cross-space identity |
| Freshness record | `fresh|stale|unknown` observation | promotion or rebuild |

## 4. Workflow process view

Startup opens the store, reads and byte-normalizes the manifest, derives all
expected keys, verifies metadata and raw bytes, and publishes a ready immutable
handle only if the full set closes. A request authenticates, authorizes before
enumeration, captures one handle, performs a read, attaches derived provenance
and freshness, then releases the handle. No request writes, flushes, rebuilds,
or switches snapshots.

## 5. Decision flow view

```text
process live? no -> connection failure
snapshot closed? no -> /healthz ok; /v1/* 503
principal valid? no -> 401
space visible for action? no -> concealed 404
raw route? yes -> exact bytes + provenance
row route advertised? no -> 409 capability_unavailable
row identity unique and exact? no -> 404 or 409 ambiguous; never arbitrary row
otherwise -> normalized derived envelope
```

Freshness is `fresh` only with a matching authorized source observation, `stale`
on detected mismatch, and `unknown` without a valid observation.

## 6. Dependency interface view

- Runtime dependency: npm `@vijayee/wavedb@0.15.8` under Node `v26.6.0` is the
  only locally proven pairing; implementation must pin it until changed by new
  evidence.
- Snapshot adapter: accepts string or Buffer reads, normalizes before decode/hash,
  sequential-write provenance only, and never uses the failed atomic batch path.
- Policy port: `authorize(principal, action, opaqueResource) -> allow|deny`; deny
  carries no caller-visible rationale.
- Normalizer port: pure input bytes plus declared version to validated rows or a
  typed unsupported/invalid result.
- Source observer port: optional immutable observation record; absence yields
  `unknown`. It is not called by the request path.

## Decisions

1. L0 exposes status, authorized space metadata, and exact raw bytes.
2. Row routes are conditional L1 and family-scoped; search is deferred.
3. Snapshot identity is the exact manifest-record digest; space IDs are opaque
   and snapshot-local.
4. Full manifest/record closure is required; partial serving is forbidden.
5. All API data declares `authority: derived`.
6. Refresh/replacement is a separately authorized capability and owner.
7. Generic public contract and private adapter/fixtures are separate placements.

## Risks and recovery

- Missing/corrupt manifest: stay not-ready; rebuild through another owner.
- Mixed WaveDB value types: normalize to bytes; reject other types.
- Atomic-batch loss: forbidden path; future upstream evidence required.
- Schema drift/duplicates: keep raw route, disable row capability for that space.
- Stale/unknown snapshot: report honestly; never trigger refresh.
- Policy uncertainty: deny and conceal.

## Dispatch technique trace

- `sequence` binds define -> denominator -> two-pass selection -> design.
- `authority_split_gate` fixes source, builder, store, and service ownership.
- `component_descriptor` and `entity_component_reference` shape components and
  interfaces.
- `conditional_component` gates normalizers and row routes.
- `state_namespace_boundary` makes space and row identities snapshot/family
  scoped.
- `assessment_failure_reference` preserves the batch and mixed-type failures.
- `validation_loop` requires manifest closure and later executable witnesses.
- `residue_ledger` keeps deployment/authentication/legacy adapter gaps visible.

## Distill design-unit check

Pass. L0 is one coherent read behavior with one acceptance boundary: authorized
retrieval of bytes proven by the same immutable manifest. L1 row projection,
snapshot rebuilding, deployment, and publication are separable and deferred.

## Outputs

- `API-CONTRACT.md`
- `DATA-MODEL.md`
- `SECURITY-BOUNDARY.md`
- `design-selection/scope-manifest.json`
- `design-selection/denominator-receipt.json`
- `design-selection/selection-result.json`

## Gaps for review

- Cursor integrity and authorization-view binding need adversarial review.
- Snapshot replacement is designed only as an external boundary, not a protocol.
- Authentication/deployment owners remain unselected.
- Legacy `0.1` remains unsupported-unproven.

## Review disposition

This file preserves the initial stage-06 design decision. Stage 07 correctly
blocked that design from advancing unchanged. The current top-level contracts
were repaired in stage 08; `stages/08-distill-repair.md` is the controlling
change record.
