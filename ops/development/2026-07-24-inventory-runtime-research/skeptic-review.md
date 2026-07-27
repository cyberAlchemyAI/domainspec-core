# Runtime Skeptic Returns

## Rittel, Horst — Precedent

No candidate is wholly precedent-clean. All three are composites over established owners; only narrow residual responsibilities are new.

### Candidate A — lifecycle bundle

**Classification: `build-from-owned`**; validator, updater, and host-package propagation are individually `already-deployed`.

- Inventory already owns `install`, `lookup`, `validate`, and `sync` modes (`arcanum/arcana/inventory/SKILL.md:26-35`), package installation (`:59-84`), and lookup readiness through the complete validator gate (`:112-123`, `:232-241`).
- The validator pair already owns conformance/readiness and structured digest/check/count output (`arcanum/arcana/inventory/scripts/validate-index-json.sh:99-112`; `validate_projection_conformance.py:383-402`).
- The consumer updater already owns deterministic append, canonical serialization, dry-run, pre-write validation, and two-view writes (`.arcanum/inventory/tools/inventory-update.cjs:130-163`, `:315-394`; contract `.arcanum/inventory/tools/README.md:3-30`).
- Arcanum Bootstrap already owns generated native-package provenance and support-directory copying, including `scripts`, schemas, and tools (`arcanum/tools/bootstrap_arcanum.sh:795-875`).

**Unique responsibility remaining:** not a new lifecycle owner, but an Inventory-owned portable payload rule: canonicalize the appender, install the complete runtime into the consumer data package, and make existing Inventory `sync` compare/refresh generated payload digests without touching consumer data. The manifest/drift check is new; install/sync authority is not.

### Candidate B — operation wrapper

**Classification: `build-from-owned`**; its component mechanics are `already-deployed`.

- Baseline/candidate mechanics must reuse the validator and updater above. The updater’s blind existing-ID no-op is explicit (`inventory-update.cjs:145-158`), and its current warning scan is whole-index/global (`:181-215`).
- Observed Invocation Loop already owns the general managed invocation path, privacy-safe envelope, observer handoff, and primary-result preservation (`arcanum/spells/observed-invocation-loop/README.md:12-18`, `:51-70`, `:83-96`).
- Signal Observer already owns exactly-one telemetry append and reflection-counter updates, and is non-blocking/non-mutating toward the observed artifact (`arcanum/arcana/signal-observer/SKILL.md:53-90`).
- Repository receipt precedent proves execution closeout, not operation semantics: `tools/arcanum` advertises runtime handoff/receipt contracts (`arcanum/tools/arcanum:28-32`, `:83-129`), while the stage receipt explicitly proves an owner stage ran rather than replacing its artifact (`arcanum/development/craft/work-packs/native-stage-execution-receipts/receipt-contract.md:3-8`, `:36-38`).

**Unique responsibility remaining:** the Inventory-operation join: bind normalized request, exact validator bundle, baseline/candidate/postwrite digests, same-ID content conflict, and introduced/resolved/inherited warning sets into one deterministic domain receipt. It must hand that receipt to OIL/Signal Observer; it must not absorb general observation or generic receipt ownership.

### Candidate C — operator coordinator

**Classification: `build-from-owned`**, with CLI/profile portions `already-deployed` and strict-root/lock/journal portions `precedent-clean`.

- `tools/arcanum` already owns the repository command surface, adapter selection, handoff, and receipt contract (`arcanum/tools/arcanum:6-32`), plus runtime profiles/config (`:83-129`, `:215-250`) and run/status/event envelopes (`:1523-1636`).
- Bootstrap already owns `.arcanum/runtime/config.json`, adapter profiles, native runtime packages, hooks, and installation validation (`arcanum/spells/arcanum-bootstrap/README.md:55-80`, `:115-130`).
- Existing runtime-profile precedent binds public capability behavior to local owners and validators; it does not create a parallel authority (`arcanum/arcana/subagent-strategy/templates/runtime-profile.md:3-5`, `:21-27`, `:51-77`).
- Inventory already owns `validate`, `lookup`, `lint`, and `sync`; therefore a broad `doctor` cannot duplicate those modes (`arcanum/arcana/inventory/SKILL.md:26-35`, `:133-160`).
- Strict root resolution is genuinely residual: the current validator falls back to `cwd` when declared-root derivation fails (`validate_projection_conformance.py:59-67`). No deployed owner surface inspected provides Inventory single-writer locking or durable two-file journal/recovery.

**Unique responsibility remaining:** an Inventory-local executable boundary that is independent of upstream checkout/cwd, with fail-closed helper/root resolution. If lock+journal are retained, they are new transactional responsibilities requiring their own witnesses. `doctor` should be narrowed to runtime-integrity diagnostics, and the proposed profile should be a subordinate Inventory bundle manifest—not a competing global runtime profile.

## Popper, Karl — Non-vacuity

Current substrate verification passed: updater tests 9/9 groups; conformance tests 10/10. This proves deterministic pure add/no-op, unsupported-kind non-mutation, and causal conformance failures—not the proposed receipt runtime. The current updater still treats every existing ID as a no-op without comparing content and writes JSON then Markdown sequentially ([updater:130-159,315-394](.arcanum/inventory/tools/inventory-update.cjs); [tests:124-239](.arcanum/inventory/tools/test/test-inventory-update.cjs); [conformance fixtures:99-200](arcanum/arcana/inventory/development/test_projection_conformance.py)).

| Closed witness | A | B | C |
|---|---:|---:|---:|
| Controlled add over historical warnings | Yes, proposed | Yes | Yes, proposed |
| Exactly one introduced warning | Yes, proposed | Yes | Yes, proposed |
| Missing helper | Yes: `tooling_blocked` | Yes: `tooling-unavailable` | Yes: `runtime_incomplete` |
| Identical normalized ID/content | No: ID presence only | Yes | No: preserves blind updater |
| Same ID/conflicting content | No | Yes: `id-conflict` | No |
| Stale receipt digest | Yes only by external comparison | Yes only by external comparison | Yes only by external comparison |
| Repeated dry run | Underspecified receipt determinism | Yes | Yes, proposed |
| Write/postwrite failure | No exact failure contract | Yes, non-atomic | Yes, journal-based but unwitnessed |

A’s `already_present` cannot establish identity, and `partial_projection_gap`/`mutation_status` do not specify exact write-failure semantics ([research.md:26-29](ops/development/2026-07-24-inventory-runtime-research/research.md)). C explicitly preserves the current updater and adds lock/journal/recovery without an implemented fixture; therefore it does not solve conflict detection and its crash claim remains proposed ([research.md:239-256,288-301](ops/development/2026-07-24-inventory-runtime-research/research.md)). B is the only candidate closing normalized equality versus conflict ([research.md:59-71,159-182](ops/development/2026-07-24-inventory-runtime-research/research.md)).

Smallest B witnesses and exact outcomes:

1. Baseline warning set `H`; controlled candidate adds none: `status=dry-run-ready`, `candidate.disposition=added`, `warning_delta.introduced=[]`, `resolved=[]`, `inherited_count=|H|`, stable `inherited_set_sha256`; `write.attempted=false`, `committed=false`, `changed_paths=[]`.
2. Candidate adds one uncontrolled `(code,subject,selector)`: same successful status; `introduced=[sha256(tuple)]`, inherited digest unchanged; warning remains nonblocking.
3. Remove one declared helper: `status=tooling-unavailable`, helper path/digest identifies the missing member; candidate absent; zero writes.
4. Existing identical normalized entry: `status=identical-no-op`, disposition likewise, candidate digests equal baseline, `generated_at` unchanged, zero writes.
5. Existing same ID/different normalized entry: `status=id-conflict`, `candidate.disposition=id-conflict`, zero writes.
6. Receipt binds index digest A; live index is B: receipt remains historical `dry-run-ready`, never current. This is closed only if a verifier compares A≠B. The schema has no `currentness` field or verification verb, so claiming runtime-enforced staleness would overstate the design.
7. Repeat identical dry run: byte-identical canonical JSON/`receipt_sha256`; byte-identical filesystem. This requires the stated ban on wall-clock fields.
8. Inject write failure: `status=write-failed`, `write.attempted=true`, `committed=false`, `changed_paths` lists actually altered paths, residue requires repair. Inject altered postwrite bytes: `status=postwrite-digest-mismatch`, actual postwrite digests differ from candidate, no success claim. Partial mutation is possible; atomicity is expressly excluded ([synthesis.md:140-160](.arcanum/observability/tmp/inventory-runtime-improvement-synthesis.md)).

All cases emit one canonical JSON receipt on stdout; diagnostics only on stderr ([synthesis.md:27-52,54-113](.arcanum/observability/tmp/inventory-runtime-improvement-synthesis.md)).

No **KILL**: every gap is closable by contract/fixture refinement. B remains the smallest viable candidate, but stale-currentness must be explicitly assigned to a verifier, and write failure must expose observed partial mutation rather than implying rollback.

## Wittgenstein, Ludwig — Definitional soundness

Only **B has a unique, presently evidenced runtime responsibility**. **KILL A as a standalone candidate.** Do not kill C outright: decompose it and defer its sole unique responsibility—transaction/concurrency safety.

### A — Ashby lifecycle bundle: **KILL**

**Claimed responsibility:** generic lookup/append mechanics plus installation lifecycle.

**Collapse:** every semantic part already has an owner:

- Deterministic append, timestamp input, idempotence, and canonical bytes belong to the updater (`.arcanum/inventory/tools/inventory-update.cjs:5-22,130-163`).
- Lookup readiness and the complete conformance verdict belong to the validator (`arcanum/arcana/inventory/scripts/validate_projection_conformance.py:383-402`; wrapper composition at `validate-index-json.sh:99-104`).
- Package creation and synchronization already belong to Inventory `install`/`sync` (`arcanum/arcana/inventory/SKILL.md:26-35,59-84`).
- Lookup orchestration and residue already belong to Inventory and the maintenance spell (`Inventory SKILL.md:112-123`; `sigil-maintenance-loop/README.md:104-127`).

A “bundle” or digest manifest is installation machinery under existing Inventory lifecycle, not a new responsibility. A’s `partial_projection_gap` is also unsound: the canonical gate says any human-view failure blocks readiness (`Inventory SKILL.md:112-114,232-241`).

**Explicit non-responsibilities:** no operation attribution, observer telemetry, maintenance approval, transaction safety, ontology/definition/promotion, or consumer-data ownership.

Retain A’s public/generated-versus-consumer-state boundary as a constraint on B; do not instantiate A as an owner.

### B — Spivak operation wrapper: **KEEP**

**Unique responsibility:** produce a deterministic, digest-bound witness of one attempted state transition:

```text
exact baseline + exact record + exact validator bundle
→ candidate disposition + warning delta + mutation outcome
```

This is not owned elsewhere:

- The updater silently treats every existing ID as a no-op without content comparison (`inventory-update.cjs:145-158`), performs only its narrow self-check (`:181-215`), prints all inherited warnings (`:364-374`), and writes JSON/Markdown sequentially without a structured receipt (`:376-394`).
- The full validator proves one current snapshot, not baseline→candidate causation (`validate_projection_conformance.py:170-306,308-402`).
- Signal Observer records behavior telemetry and must not alter the primary result (`signal-observer/SKILL.md:67-90,106-127`).
- Observed Invocation Loop owns the general invocation envelope/handoff, not Inventory transition validity (`observed-invocation-loop/README.md:12-18,61-96`).
- Inventory install/sync owns distribution, not operation attribution.
- Maintenance consumes lookup evidence and explicitly avoids install/sync/mutation during exploration (`sigil-maintenance-loop/README.md:112-127`).

Thus B uniquely owns conflict detection, baseline/candidate validation binding, introduced/resolved/inherited warning attribution, helper/input/output digests, and the append receipt.

**Explicit non-responsibilities:** install/sync, search/query synthesis, observability append, maintenance/reflection routing, semantic authority, historical cleanup, lock/journal recovery, or atomic-apply claims.

### C — Wiener operator coordinator: **DECOMPOSE / DEFER**

Most of C collapses:

- `validate` and `lookup` belong to Inventory and its validator.
- `append` plus receipt attribution belongs to B.
- `doctor` overlaps Inventory `validate`/`sync`.
- Observer handoff belongs to Signal Observer/OIL (`observed-invocation-loop/README.md:83-115`).
- Root/helper binding belongs in B’s installed-runtime manifest; it should fix the validator’s unsafe `cwd` fallback (`validate_projection_conformance.py:59-67`), not create another owner.

C nevertheless has one genuinely unique responsibility: **single-writer coordination plus durable journal/recovery across the two-file commit**. The current updater writes files separately (`inventory-update.cjs:382-383`), so this is not tautological. But no current concurrency/crash witness supports making it MVP.

**Explicit non-responsibilities:** lifecycle install/sync, ordinary validation/lookup, operation receipt semantics, telemetry, auto-repair, or authority/promotion.

**Disposition:** preserve C only as a later transaction-safety proposal with its own failure fixtures; reject the current omnibus “operator coordinator” shape.
