# RWO canonical-contract dialectic findings

Dispatch: `2026-08-07-rwo-canonical-contract-dialectic-review`
Decision input only: `authority_effect: none`; `promotion_effect: none`

## Parent verdict

**FIX before owner acceptance.** The architecture direction survives: retain a
language-neutral semantic contract, RFC 8785 canonical payload bytes, a Python
reference oracle, later Rust/Go probes, and a separate Go-capable command/event
service boundary. The current `RWO-JCS-SAFEINT-V1` prose is not precise enough
for independent Python, Rust, and Go implementations to derive identical input
admission, semantic identity, fixtures, and reducer results.

The two reviewers converged after one confrontation. No material finding was
refuted. Parent verification confirmed the cited repository bytes and the
primary standards claims.

## Surviving findings by artifact

### `DG-RWO-LANG-CONTRACT-001.md` — FIX

| # | Evidence | Severity | Proposed fix |
|---|---|---|---|
| F1 | Lines 27–35 require duplicates, numeric limits, decimal strings, and NFC but do not define a pre-map parser, negative zero, decimal grammar/equality, or reject-versus-normalize behavior. | MAJOR | Add a normative admission phase before ordinary map construction. Reject decoded-equivalent duplicate keys and lone surrogates; make NFC handling, noncharacters, negative zero, and decimal grammar explicit. |
| F2 | Lines 38–39 preserve array order while delegating unordered collection ordering to unnamed semantic rules. | MAJOR | Require each order-insensitive schema field to define a total comparator, normalization point, duplicate policy, and tie-breaker before JCS. |
| F3 | Lines 36–37 hash bare canonical payload bytes even though graph, event, cursor, and fixture domains can share the same JSON shape. | MAJOR | Define typed/domain-separated identity using contract/profile version, schema/type ID, and canonical payload bytes. Keep canonical payload bytes distinct from semantic digest identity. |
| F4 | Lines 40–41 combine closed unknown-field rejection with optional minor compatibility but do not define a registry, direction, validator schema, or projection. | MAJOR | Fail closed on undeclared versions. Admit a minor only through an explicit directional schema/projection matrix with deterministic canonical output. |
| F5 | Lines 42–45 require reviewed immutable vectors but do not define a non-recursive manifest preimage or independent expected-byte derivation. | MAJOR | Exclude the manifest digest field from its preimage or use a detached receipt; require an independently derived expected-byte path and explicit update approval. |

Primary standards verification:

- RFC 8785 requires duplicate-free I-JSON input, preserves admitted string code
  points rather than normalizing them, serializes numbers with ECMAScript rules,
  maps IEEE-754 minus zero to `0`, preserves array order, and sorts object names
  by unsigned UTF-16 code units.
- RFC 7493 rejects duplicate names after escape processing, rejects surrogates
  and noncharacters, supports the safe-integer boundary, and leaves extended-
  precision string semantics to the application.
- Official Protocol Buffers documentation confirms deterministic serialization
  is not canonical and hashes are not stable across schema/build/library changes.

### `option-admissibility-request.json` — FIX

| # | Evidence | Severity | Proposed fix |
|---|---|---|---|
| F6 | Lines 14–16 claim that safe integers plus NFC validation remove numeric and Unicode ambiguity, but F1 remains unresolved. | MAJOR | Make structural admissibility conditional on the repaired normative profile; do not claim semantic ambiguity is closed before the grammar and vectors exist. |

### `option-admissibility-receipt.json` — FIX/regenerate

| # | Evidence | Severity | Proposed fix |
|---|---|---|---|
| F7 | Line 9 records `ownerGate: null` although the candidate request names an owner gate; line 14 has no reasons. | MINOR | Clarify whether `null` means the option set routes to a separate Decision Gate or represents dropped metadata, then regenerate after the request changes. Do not treat this receipt as semantic-completeness proof. |

### `DESIGN.md` — FIX

| # | Evidence | Severity | Proposed fix |
|---|---|---|---|
| F8 | Lines 60–74 promise duplicate convergence, divergent-duplicate rejection, cursor preservation, and stable defect ordering without defining event identity, payload equality, cursor identity, or total defect ordering. | MAJOR | Define graph identity, accepted-event identity, event-payload digest/equality, cursor identity, and the exact duplicate/divergent reduction algorithm in semantic schemas, not transport adapters. |
| F9 | Lines 82–87 let Python produce and check initial vectors; lines 158–177 bind a manifest digest without its preimage/update protocol. | MAJOR | Make Python a candidate producer, not sole fixture authority; add independent derivation, non-recursive manifest identity, review ownership, and update authorization. |

### `PLAN.md` — FIX

| # | Evidence | Severity | Proposed fix |
|---|---|---|---|
| F10 | Lines 36–49 require canonical rules and immutable fixtures but omit the concrete admission, identity, version, ordering, and independent-derivation acceptance tests. | MAJOR | Add shared positive and negative Python/Rust/Go vectors for every surviving rule before `SWU-RWO-LANG-001` can pass. |

### `WAY-MAKER.md` — FIX

| # | Evidence | Severity | Proposed fix |
|---|---|---|---|
| F11 | Lines 49–58 require canonical identity and non-self-blessing tests but do not close F1–F5 or F8. | MAJOR | Make the repaired profile, typed identities, reducer duplicate rules, and independent fixture protocol explicit Stage-1 acceptance requirements. |

### `RESULT.md` — KEEP

The language/topology architecture and claim ceiling remain sound. The result
does not itself claim to define canonical bytes.

### Strategy and dispatch evidence — KEEP

`strategy-inventory-packet.json` correctly treats Inventory as non-authority.
`dispatch-sheet.json` correctly separated formal interoperability from domain/
lifecycle ownership and predicted their actual disagreement.

## Minimal repaired model

The contract should expose five separate functions instead of making “JCS plus
SHA-256” carry every concern:

```text
raw JSON
  -> admit(profile, schema, raw tokens)
  -> normalize_semantics(schema, admitted value)
  -> canonical_payload_bytes(profile, normalized value)
  -> semantic_digest(contract, profile, schema/type, payload bytes)
  -> reduce(cursor identity, accepted-event identity, payload equality)
```

Fixture identity is a sixth concern: a detached manifest receipt binds contract,
profile, schema/vector identities, expected bytes, sizes, and digests without
hashing its own digest field.

## Required discriminating vectors

1. Safe integer endpoints and rejection immediately outside them.
2. Lexical `-0`/`-0.0` and decimal strings `0`, `-0`, `01`, `1.0`, `1.00`,
   `1e0`, and `+1` under the selected grammar.
3. Decoded duplicate keys: `{"a":1,"\u0061":2}` must reject before map collapse.
4. NFC composed/decomposed input, lone surrogate, noncharacter, and UTF-16 key
   ordering across U+10000/U+E000.
5. Same canonical `{}` in Graph and Cursor domains must have distinct semantic
   digests.
6. Same event ID/same payload converges; same event ID/different payload returns
   `DivergentDuplicate` without cursor mutation.
7. Unordered values with equal primary sort keys converge through an explicit
   secondary tie-breaker.
8. A 1.1-only field presented to a 1.0 consumer deterministically rejects or
   uses an explicitly identified projection.
9. A shared Python fixture generator/checker bug still fails against independently
   established expected bytes.

## Owner choices still open

1. Reject negative zero, or admit it with intentional equality to zero.
2. Reject non-NFC input, or transform it before admission.
3. Adopt full I-JSON character restrictions, including noncharacters, or state a
   narrower profile.
4. Select a typed canonical envelope or a domain-prefixed digest preimage.
5. Select exact event/cursor identity fields and payload equality.
6. Start exact-version-only, or admit named directional minor projections.
7. Appoint the independent fixture derivation, review, and update owner.

## Change-request list

1. Repair the normative Decision Gate profile for F1–F5.
2. Revise and regenerate the admissibility request/receipt for F6–F7.
3. Bind semantic event/cursor identities and fixture governance into DESIGN for
   F8–F9.
4. Add the complete shared vector suite to PLAN and Way-Maker acceptance for
   F10–F11.
5. Return the revised option to the RWO planning/design owner. Do not start
   Python, Rust, Go, gRPC, journal, retry, ARE, or runtime implementation from
   this review.

## Claim ceiling and next gate

This review recommends requesting a revised option set under
`DG-RWO-LANG-CONTRACT-001`; it does not itself select that response. No contract,
Work Pack, ontology, implementation, authority, promotion, publication,
deployment, or release state changed.
