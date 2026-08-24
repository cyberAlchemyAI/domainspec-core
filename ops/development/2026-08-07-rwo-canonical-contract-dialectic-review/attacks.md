# RWO canonical-contract dialectic attacks

Dispatch: `2026-08-07-rwo-canonical-contract-dialectic-review`

The initial reports below are parent-normalized from each frozen return before
either reviewer saw the other lane. Their evidence, severity, discriminating
vectors, dispositions, and lifecycle fields are preserved; final confrontation
positions are appended after the bounded Robot-Talks exchange.

## Initial formal-interoperability report

Overall status: `major_fixes_required`. `RWO-JCS-SAFEINT-V1` has a sound
standards base, but it is not yet precise enough for independent Python, Rust,
and Go implementations to derive identical admission decisions, bytes, and
digests without extra policy choices.

### Key findings

1. **MAJOR — Numeric admission is incomplete before JCS serialization.**

   The gate bounds integers but does not define negative-zero handling or the
   grammar and canonical value equivalence of decimal strings
   (`DG-RWO-LANG-CONTRACT-001.md:30-33`). RFC 8785 §3.2.2.3 serializes IEEE-754
   values using ECMAScript rules; Appendix B serializes negative zero as `0`.
   RFC 7493 §2.2 supports the safe-integer boundary and recommends strings for
   greater precision, but does not define an application decimal-string grammar.

   Discriminating vectors: accept `9007199254740991`; reject
   `9007199254740992` as a JSON number; explicitly decide whether lexical `-0`
   and `-0.0` are rejected or canonicalized to `0`; distinguish decimal strings
   `"0"`, `"-0"`, `"01"`, `"1.0"`, `"1.00"`, `"1e0"`, and `"+1"`.

2. **MAJOR — Duplicate detection is required but not bound to a pre-map parsing
   procedure.**

   The gate says to reject duplicate object keys (`DG:27-29`), while RFC 7493
   §2.3 defines duplicates after escape processing. Common decoders may collapse
   duplicates before schema validation. The negative vector
   `{"a":1,"\u0061":2}` must be rejected before ordinary map construction;
   first-wins and last-wins both fail.

3. **MAJOR — Unicode admission and ordering need an executable profile.**

   `DG:34-35` does not say whether non-NFC input is rejected or transformed;
   `DG:65-69` calls it validation, favoring rejection, but the rule is not
   normative. RFC 8785 §3.2.2.2 rejects lone surrogates and §3.2.3 orders names
   by unsigned UTF-16 code units. RFC 7493 §2.1 rejects Unicode noncharacters.
   UAX #15 C2 defines normalization testing.

   Vectors: reject decomposed `"e\u0301"` if NFC is validation and accept
   `"\u00e9"`; reject `"\uDEAD"` and decide whether `"\uFDD0"` is rejected;
   key U+10000 must sort before U+E000 under JCS UTF-16 ordering.

4. **MAJOR — Digest identity and version compatibility are underspecified.**

   SHA-256 is over canonical value bytes alone (`DG:36-37`), so two semantic
   types containing identical JSON can alias. Closed unknown-field rejection
   conflicts with accepting a backward-compatible minor version unless the
   schema relation and canonical projection are defined.

   Vectors: `Graph {}` and `Cursor {}` must not receive the same semantic
   digest; a 1.0 consumer receiving a 1.1 value with a new field must have one
   predetermined outcome—reject or explicitly project.

5. **MAJOR — Fixture identity can recurse and expected bytes can self-bless.**

   `DESIGN.md:158-167` requires a fixture-manifest digest without specifying
   whether it is inside its own preimage. Python initially produces and checks
   vectors (`DESIGN.md:82-87`) without an operational independent expected-byte
   derivation.

   Vectors: changing only `fixtureManifestDigest` must not create a
   self-referential hash; one deliberately wrong expected byte must fail an
   independent derivation even if Python generation and checking share a bug.

### Gaps or inconsistencies

- Canonical decimal-string grammar is absent.
- Semantic ordering is delegated to future schema rules (`DG:38-39`).
- The Unicode profile does not explicitly adopt all I-JSON character rules.
- The byte-level golden-vector envelope and digest preimage are absent.
- No cross-language matrix pins parser mode, numeric representation, UTF-16
  comparator, duplicate stage, and expected-byte derivation.
- Official Protocol Buffers documentation supports rejecting protobuf as the
  canonical identity because deterministic serialization is not canonical
  across languages or stable across schema/build changes.

### Local tensions

- Dependency-free Python oracle versus exact ECMAScript/JCS numeric rendering.
- Closed schemas versus backward-compatible minor-version acceptance.
- Preserve code points versus transforming input to NFC.
- Python fixture production versus independent conformance authority.
- Bare-value digests versus typed semantic identity.

### Questions for synthesis

1. Is NFC reject-only or transforming?
2. Is the profile full I-JSON, including noncharacter rejection?
3. Is negative zero rejected or erased to zero?
4. What decimal-string grammar and equality relation is schema-owned?
5. Is identity an envelope or a domain-prefixed digest?
6. How is a manifest digest detached from its identified manifest?
7. What independent procedure owns initial expected bytes?

### Per-artifact disposition

- `DG-RWO-LANG-CONTRACT-001.md` — **FIX**: add normative admission, decimal,
  Unicode, duplicate-preserving parse, ordering, version, digest, and fixture rules.
- `option-admissibility-request.json` — **FIX**: qualify the ambiguity-removal claim.
- `option-admissibility-receipt.json` — **FIX**: rerun after request revision.
- `RESULT.md` — **KEEP**: architecture and claim ceiling remain sound.
- `DESIGN.md` — **FIX**: define typed preimages, manifest hashing, independent
  vector derivation, and edge vectors.
- `PLAN.md` — **FIX**: make these contract details acceptance prerequisites.
- `WAY-MAKER.md` — **FIX**: Stage 1 must require the repaired profile.
- `strategy-inventory-packet.json` — **KEEP**.
- `dispatch-sheet.json` — **KEEP**.

### Formal lifecycle receipt

```json
{
  "agent_id": "/root/rwo_formal_interop_review",
  "role_id": "formal-interop-reviewer",
  "spawn_status": "spawned",
  "join_status": "completed",
  "close_status": "closed",
  "dispatch_id": "2026-08-07-rwo-canonical-contract-dialectic-review",
  "step_id": "s1",
  "capability_ref": "domainspec-subagents-strategy",
  "capability_mode": "review",
  "wave_id": "dialectic-review",
  "write_scope": [],
  "status": "completed_with_major_fixes_required",
  "validation": "complete named corpus and official primary standards reviewed; mutation none",
  "blockers": [
    "numeric_and_decimal_admission_underspecified",
    "duplicate_detection_stage_unspecified",
    "unicode_profile_underspecified",
    "digest_and_minor_version_semantics_underspecified",
    "fixture_identity_and_independent_derivation_underspecified"
  ],
  "residue": [
    "no_executed_python_rust_go_cross_language_vectors",
    "target_inventory_source_coverage_blocked"
  ],
  "reroute": "bounded_robot_talks_confrontation_then_owner_synthesis"
}
```

Official evidence: RFC 8785; RFC 7493; Unicode UAX #15; Protocol Buffers
serialization-not-canonical and deterministic API documentation.

## Initial domain-lifecycle report

Verdict: `major_fixes_required`. The profile stabilizes JSON bytes, but does
not yet define complete domain-semantic identity across graph, event, cursor,
fixture, and version lifecycles.

### Key findings

1. **MAJOR — SHA-256 identity lacks type/domain separation.**

   The profile hashes only canonical JSON bytes while exposing distinct value
   domains (`DG:36-43`, `DESIGN.md:58-74`, `WAY-MAKER.md:49-56`). Define a
   domain-separated preimage containing contract/profile version, schema/type
   ID, and canonical payload bytes.

2. **MAJOR — Accepted-event identity and cursor identity are unspecified.**

   `reduce` promises exact duplicate convergence and divergent-duplicate
   detection, but the corpus does not define event identity, payload equality,
   or whether cursor identity means canonical value, history position, or
   accepted-event lineage (`DESIGN.md:60-74,117-125`; selected RWO current-state
   evidence at `findings.md:76-86`). Define `event_identity`,
   `event_payload_digest`, `cursor_identity`, and the comparison algorithm.

3. **MAJOR — Semantic ordering is delegated to unspecified future schemas.**

   Every order-insensitive collection needs a total comparator, normalization
   point, duplicate policy, and tie-breaker (`DG:38-39`,
   `DESIGN.md:65-74`, `PLAN.md:36-49`).

4. **MAJOR — Fixture governance still permits self-blessing.**

   Python is both initial fixture producer and checker. Existing independent
   review and immutable-test prose does not require independent derivation, a
   two-party update gate, or non-recursive manifest identity (`DG:42-45`,
   `DESIGN.md:82-87,169-177`, `WAY-MAKER.md:53-58`).

5. **MAJOR — Minor-version compatibility conflicts with closed-schema rejection.**

   The profile rejects unknown fields and version mismatches yet permits a
   “known minor” when its schema declares backward compatibility, without
   identifying the registry, validator schema, or meaning of compatibility
   (`DG:27-29,40-45`, `DESIGN.md:117-125`). Define exact-version selection and
   a directional compatibility matrix; unknown minors fail closed.

### Gaps or inconsistencies

- Canonical payload, typed semantic, graph, event, cursor, transport, and
  fixture identities are not separate functions/domains.
- Decimal-string grammar and equality are absent.
- The request names an owner gate, while the receipt records `ownerGate: null`.
- The receipt proves option routing, not semantic completeness.
- Inventory evidence leaves schema/reducer migration unresolved.

### Local tensions

- JCS byte stability is asked to carry semantic identity without a typed preimage.
- Closed schemas conflict with an unowned minor-version projection.
- Python is a reference oracle but also originates fixtures.
- Undefined event/cursor identity could let journal or retry conventions become
  the de facto semantic owner.
- Transport and ARE remain consumers in prose but become covert owners if
  event identity, replay, or compatibility are unresolved.

### Questions for synthesis

1. Does a digest identify JSON, a typed value, or an operation artifact?
2. Which fields distinguish exact from divergent duplicate events?
3. Is cursor identity a complete value, accepted-history head, or operation result?
4. Who owns version compatibility, and is it byte-preserving or semantic?
5. What independent path establishes expected fixture bytes?
6. Which collections are semantically unordered, and what comparator applies?

### Per-artifact disposition

- `DG-RWO-LANG-CONTRACT-001.md` — **FIX**: add typed domains, identity
  distinctions, ordering tables, version semantics, decimal grammar, fixtures.
- `option-admissibility-request.json` — **FIX**: make admissibility conditional.
- `option-admissibility-receipt.json` — **FIX**: regenerate and preserve owner gate.
- `RESULT.md` — **KEEP**.
- `DESIGN.md` — **FIX**: define event/cursor/graph identity and fixture independence.
- `PLAN.md` — **FIX**: require independent derivation and explicit conformance tests.
- `WAY-MAKER.md` — **FIX**: add identity and fixture requirements.

### Discriminating scenarios

- Graph `{}` and Cursor `{}` must have different typed digests.
- Same `event_id` with payload A then payload B must return
  `DivergentDuplicate` without cursor mutation.
- Opposite input orders with equal primary sort keys must converge through an
  explicit tie-breaker.
- A shared Python generator/checker bug must fail against independent fixtures.
- A 1.1 field unknown to a 1.0 consumer must reject or use an explicit projection.

### Domain-lifecycle receipt

```json
{
  "agent_id": "/root/rwo_domain_lifecycle_review",
  "role_id": "domain-lifecycle-reviewer",
  "spawn_status": "spawned",
  "join_status": "completed",
  "close_status": "closed",
  "dispatch_id": "2026-08-07-rwo-canonical-contract-dialectic-review",
  "step_id": "s1",
  "capability_ref": "domainspec-subagents-strategy",
  "capability_mode": "review",
  "wave_id": "dialectic-review",
  "write_scope": [],
  "status": "major_fixes_required",
  "validation": "pass: named corpus reviewed read-only; every major finding has a discriminating scenario",
  "blockers": [
    "typed_digest_domain_unspecified",
    "accepted_event_and_cursor_identity_unspecified",
    "semantic_ordering_not_total",
    "fixture_update_can_self_bless",
    "minor_version_compatibility_underspecified"
  ],
  "residue": [
    "target_inventory_source_coverage_blocked",
    "schema_reducer_migration_owner_unresolved",
    "no_executed_cross_language_conformance"
  ],
  "reroute": "bounded_confrontation_then_owner_synthesis"
}
```

## Formal-interoperability confrontation result

Convergence was reached: both lanes independently support
`major_fixes_required`.

### Peer claims

- **RETAINED — Typed/domain-separated digest.** Bare canonical JSON permits
  `Graph {}` and `Cursor {}` to alias.
- **REFINED — Event and cursor identity.** These belong in semantic schemas and
  the L1 reducer contract, not generic JCS rules. Transports, journals, and
  retries consume rather than define them.
- **RETAINED — Semantic collection ordering.** JCS preserves array order, so
  every order-insensitive collection needs a schema-owned comparator,
  normalization point, duplicate rule, and tie-breaker.
- **RETAINED — Fixture self-blessing risk.** Independent byte derivation and a
  non-recursive manifest digest are mandatory.
- **RETAINED — Minor-version contradiction.** Closed unknown-field rejection
  cannot coexist with unspecified minor compatibility.
- **RETAINED — Decimal grammar missing.** I-JSON recommends strings for extended
  precision but does not define their application grammar.
- **REFINED — `ownerGate` inconsistency.** Clarify whether `null` means routed to
  a separate gate or lost metadata before classifying it as invalid.
- **REFINED — Covert transport ownership.** This is a concrete design risk, not
  evidence that transport or ARE currently owns semantics.

### Exact lane tensions

- Formal reproducibility needs lexical admission; lifecycle identity begins
  after admission.
- Event/cursor identity is required for reducer conformance but stays schema-owned.
- A typed envelope and a prefixed hash preimage both prevent aliasing but produce
  different identities.
- Exact-version failure is immediately reproducible; projections require more
  compatibility machinery.
- Python may produce candidate fixtures but cannot be their sole derivation and
  conformance authority.

### Minimal refinements surviving both lanes

1. Duplicate-preserving parsing before map construction.
2. Numeric, negative-zero, decimal, Unicode/NFC, surrogate, noncharacter, and
   UTF-16-order rules and vectors.
3. Schema-owned total orders for unordered collections.
4. Domain-separated semantic digests with profile/version/type identity.
5. Schema-owned event identity, payload equality, cursor identity, and duplicate
   reduction rules.
6. Fail closed on unknown versions absent an explicit directional projection.
7. Detached/self-field-excluding manifest identity and independent expected bytes.
8. One shared positive/negative vector suite for Python, Rust, and Go.

Remaining owner choices: negative zero; reject versus transform non-NFC; full
I-JSON versus narrower character policy; typed envelope versus prefixed digest;
event/cursor identity fields; exact-only versus projected minor compatibility;
and the independent fixture approver.

Final disposition: DG, request, receipt, DESIGN, PLAN, and WAY-MAKER are **FIX**;
RESULT, Inventory packet, and dispatch sheet are **KEEP**. Final position:
**converged on FIX before owner acceptance**.

## Domain-lifecycle confrontation final position

### Peer claims

- **RETAINED — Numeric admission is incomplete.** Safe integers do not decide
  negative zero or decimal-string grammar/equality.
- **RETAINED — Duplicate rejection must occur before map collapse.** Decoded-
  equivalent keys such as `"a"` and `"\u0061"` must reject during parsing.
- **REFINED — Unicode policy.** The prose most naturally means reject non-NFC,
  then preserve admitted code points. That must be normative. Lone surrogates
  reject; full noncharacter rejection remains an owner choice.
- **RETAINED — Typed digests and versions are underdefined.** Bare JCS aliases
  types, and closed schemas need explicit compatibility machinery.
- **RETAINED — Fixtures can self-bless.** Manifest identity must be non-recursive
  and expected bytes independently derived.

No peer claim was refuted on substance.

### Exact lane tensions

- Formal asks whether all languages admit and serialize the same values;
  lifecycle asks whether those bytes identify the same semantic kind.
- Valid JCS numbers do not define application equality for decimal strings.
- Pre-map duplicate detection and post-validation semantic ordering are distinct.
- Closed schemas deterministically reject; minor compatibility requires an owned
  projection matrix.
- Python can implement the oracle but cannot independently bless its fixtures.
- Transport neutrality holds only when graph/event/cursor/fixture identities are
  kernel-defined before transport consumers use them.

### Minimal refinements surviving both lanes

1. Pre-map admission rejecting decoded duplicates, lone surrogates, non-NFC,
   unknown fields, and undeclared versions.
2. Normatively select NFC rejection unless transformation is explicitly chosen.
3. Define negative-zero behavior and decimal-string grammar/equality.
4. Define total comparators, duplicate rules, and tie-breakers for unordered fields.
5. Define a typed digest preimage.
6. Separate graph, accepted-event, payload, cursor, and fixture identities.
7. Replace generic minor compatibility with a directional projection matrix.
8. Define non-recursive manifest identity, independent bytes, and update authority.
9. Add shared positive and negative Python/Rust/Go vectors.

Remaining owner choices: NFC handling; noncharacters; negative zero; decimal
grammar/equality; envelope versus prefix; event/cursor fields; compatible minor
projections; and fixture derivation/review/update ownership.

Final disposition: DG, request, receipt, DESIGN, PLAN, and WAY-MAKER are **FIX**;
RESULT, Inventory packet, and dispatch sheet are **KEEP**. **Convergence reached:**
yes; the lanes differ only in emphasis.
