---
title: Tilth Architecture — Amendment v7.0.4-M1 (KFR canonicalization + Derivation AST whitelist + Tag-modify tamper-gate + Benchmark constant-time cross-check + Decimal currency mandate; close 5 HIGH/P0 + 2 RECOMMENDED + 4 OPTIONAL paths surfaced by 2026-05-10 cross-family verification)
filed: 2026-05-10
locked: 2026-05-10
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-10 — narrow corrective amendment that supersedes specific clauses of v7.0.4 (LOCKED 2026-05-09 row 178). v7.0.4 amendment text NOT modified in place; row 178 stands as historical record. M1 is the closure on lock_history row 181 cross-family verification's NEEDS-M1 disposition. **L-005 strict two-cycle CLOSED** with FULL live cross-family rigor (no Section E carve-out). Cycle 1 audit at `pipeline/validation/v7_0_4_m1_thesis_2026-05-10/audit_v1_synthesis.md`; Cycle 2 verification at `pipeline/validation/v7_0_4_m1_thesis_2026-05-10/audit_v2_synthesis.md`. Cycle 1: Editor READY_TO_LOCK + Judge READY_TO_LOCK 99/100 + Red Team ESCALATE blocking:true with 11 HIGH; 14 fixes applied. Cycle 2: Editor READY_TO_LOCK + Judge READY_TO_LOCK 100/100 + Red Team REQUIRES_FIXES blocking:true with 3 PARTIAL (RT-05 + RT-10 + RT-11); disposition: 2 FOLDED_IN at LOCK (RT-05 §4.2.2 atomic-read discipline + RT-11 §8.4.1 Logfire bootstrap shim), 1 REJECTED with rationale (RT-10 — gate firing ≠ attack vector per L-017/L-018). Row-170 transparent disposition pattern. v0.1 Beta gate cleared.
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
parent_amendment: pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md (LOCKED 2026-05-09 — row 178)
predecessor_audit: pipeline/validation/v7_0_4_thesis_cross_family_2026-05-10/{audit_v1_synthesis.md, audit_v1_{editor,judge,red_team}.{md,raw.json}}
companion_amendments:
  - "pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md (parent — KFR + SP0 + F-LOGICIAN-FACT-DRIFT + Intake + Benchmarks; M1 supersedes specific clauses listed in §11)"
  - "pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md (LOCKED 2026-05-10 — Funder Intel + Match DB; M1 does not modify v7.0.5)"
  - "pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md (LOCKED 2026-05-10 — Beta classification routing; M1 composes against opaque-slot discipline; routing pattern unchanged)"
companion_files_pending_edit_at_lock:
  - "pipeline/blueprint/v0.1/section_04_logician.md (new PRE/POST gates per §10 — F-KFR-YAML-CONSTRUCT-FORBIDDEN, F-KFR-CANONICAL-SIGNATURE-INVALID, F-DERIVATION-AST-FORBIDDEN-NODE, F-KFR-TAG-MODIFIED, F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING, F-CURRENCY-FLOAT-IN-COMPARISON, F-CURRENCY-UNIT-MISMATCH, F-AWARD-INGEST-ATTN-UNVERIFIED, F-KFR-DUPLICATE-KEY, F-DERIVATION-RUNTIME-ARITHMETIC-ERROR, F-INTAKE-TELEMETRY-LEAK)"
  - "pipeline/logician/canonicalization/kfr_canonical.py (NEW — deterministic JSON canonicalizer; MUST refuse YAML anchors/aliases/merge-keys per §2.3)"
  - "pipeline/logician/derivation/ast_whitelist.py (NEW — explicit ast.NodeVisitor with enumerated whitelist per §3.2)"
  - "pipeline/logician/currency/decimal_arithmetic.py (NEW — Decimal context fixed at prec=28 ROUND_HALF_EVEN; helper for tolerance comparisons; ban-float helper)"
  - "pipeline/logician/benchmarks/cross_check.py (NEW — constant-time hash compare via hmac.compare_digest; audit-log every cross-check call)"
  - "pipeline/logician/gates/f_kfr_*.py + f_derivation_ast_forbidden_node.py + f_currency_*.py + f_benchmark_*.py + f_intake_telemetry_leak.py (NEW — per §10 module set; paired Code work surfaced as WS-L Slice 4 dispatch at LOCK)"
  - "pipeline/blueprint/v0.1/section_04_v2_x_amendment.md (registers M1 gates as §6 — paired-LOCK with §4 v2.x consolidated amendment when WS-L Slice 4 lands)"
  - "orgs/_TEMPLATE/vault/kfr/register.yaml + pending_facts.yaml (regenerated post-canonicalization; example-fact field types switched to Decimal-aware shapes)"
  - "vault_shared/benchmarks/register.yaml (constant-time cross-check audit-log shape added; SN-LLC seeding allowlist seeded; Decimal types wired)"
authority_source: pipeline/validation/v7_0_4_thesis_cross_family_2026-05-10/audit_v1_synthesis.md (verdict NEEDS-M1; M1 candidate list priority-ordered); lock_history row 181 footer disposition; CLAUDE.md "v0.1 Beta gate" Coordinator handoff; AGENTS.md cross-family bridge pattern
version_wording_discipline: "LOCKED" inside this file refers to on-disk LOCKED state at filing time. Every M1 mechanism listed in §2-§9 is NEW relative to v7.0.4 LOCKED row 178. M1 is a NARROW CORRECTIVE — it does not introduce new architectural primitives beyond what's required to close the cross-family-surfaced paths.
---

# §0. Amendment intent — close the cross-family-surfaced paths before v0.1 Beta

v7.0.4 LOCKed 2026-05-09 (row 178) under a Section E carve-out. Cross-family verification 2026-05-10 (row 181) surfaced **18 new findings beyond Single-Claude's 22-finding scope: 5 HIGH/P0 + 4 MED + 9 LOW** — exactly the L-003 violation pattern cross-family rigor exists to prevent. Three of the five HIGH/P0 are explicitly cross-family-specific per Red Team's framing — implementation-surface and metadata-surface blind spots that an Anthropic-trained adversarial lens did not surface.

**v0.1 Beta cannot ship until M1 LOCKs.** Each HIGH/P0 path reaches the funder under the right adversarial conditions:

| Finding | Path-to-funder summary |
|---|---|
| CF-RT-01 (HIGH/P0) | YAML anchor/merge-key bypasses F-KFR-SIGNATURE-INVALID; tampered values reach Scribe with valid-looking signature |
| CF-RT-02 (HIGH/P0) | Derivation AST grammar is informal; dunder/Call/Subscript escape paths admit arbitrary Python execution at draft-read |
| CF-RT-04 (HIGH/P0) | `required_for_funder` tag-removal silently disables §3.2 NEEDED hard-block; required-fact draft ships absent |
| DC-CF-04 (HIGH) | F-BENCHMARK-CONTAINS-PER-ORG-REF value-leg creates boolean oracle; cross-org information leak via gate side-channel |
| DC-CF-02 (MED→HIGH at M1) | IEEE-754 float precision at 0.005 tolerance boundary fires false-positive or passes false-negative; wrong currency value ships |

Each closure ships as **deterministic Python + Cedar, fail-closed, zero token cost** — same Logician discipline as v7.0.4's existing F-LOGICIAN-FACT-DRIFT family. M1 is text-level + paired-Code; no new architectural primitives, no new seats, no scope expansion.

## §0.1 What M1 supersedes from v7.0.4

**Legend.** A v7.0.4 clause listed as "superseded by M1 §N" is no longer authoritative on its own — readers MUST consult the M1 § alongside the v7.0.4 clause. v7.0.4 clauses NOT listed in this table remain authoritative as written. At LOCK, v7.0.4 amendment file gains (a) a `[NOTE]` block prepended after frontmatter pointing to M1, and (b) a footer addendum citing M1 — see §11.3.

| v7.0.4 clause | M1 supersession |
|---|---|
| §1.1 F-KFR-SIGNATURE-INVALID — verifies on raw YAML bytes | §2 — verifies on **canonical JSON bytes** post-load; raw YAML bytes are no longer the signing surface |
| §1 KFR schema — admits any YAML construct | §2.3 — schema **forbids** YAML anchors / aliases / merge-keys; loader rejects fail-closed |
| (pre-M1 KFR files signed on raw YAML) | §2.6 — legacy migration mode (dual-verification + `--migrate-signatures`) |
| §4.5 derivation AST grammar — informal prose | §3 — explicit `ast.NodeVisitor` whitelist with enumerated allowed node types |
| §4 currency tolerance — `0.005 * kfr_value` arithmetic without type pin | §6 — mandates `decimal.Decimal` with fixed context; bans `float` from currency comparisons |
| §7.2 F-BENCHMARK-CONTAINS-PER-ORG-REF — boolean oracle on value-leg | §5 — constant-time hash compare via `hmac.compare_digest` + per-cross-check audit-log entry (write-before-compare + fsync) |
| §3.2 + §4.4 tamper-gates — covers tolerance widening, signature mutation | §4 — extended to cover `required_for_*` tag mutation (parity with §4.4 discipline) via on-disk SHA3-512 tag-set hash |

## §0.2 What M1 does NOT supersede

- A1-A12 architecture (LOCKED 2026-04-19) — unchanged.
- Five Operating Laws + Four Autonomy Rules — unchanged.
- v7.0.6 council + support-agent roster (Intake / Uploader / Data Collector / Report Generator / Archivist) — unchanged.
- v7.0.7 classification routing (Beta) + Classification Review stage + opaque-slot discipline — unchanged.
- v7.0.8 CIC × CLC orthogonality — unchanged.
- v7.0.4 §3 SP0 stop point + §4.5 chain-depth-1 + §4.6 STALE-ACKNOWLEDGED tolerance landing + §4.7 derivation_id annotation — preserved (M1 hardens the surrounding mechanisms; the structural decisions stand).
- v7.0.4 §5 Intake three-mode dispatch + §5.2 source_quote exact-match semantics + §5.3 AWARD_INGEST contract — preserved (M1 hardens the attestation-flag path and telemetry path; the mode-dispatch model stands).
- KFR's underlying schema fields, cadence-aware expiry, F-LOGICIAN-FACT-DRIFT umbrella codes — preserved.

# §1. Closure roster (priority-ordered per audit_v1_synthesis.md M1 candidate list)

| Tier | ID | Severity | M1 § | Closure mechanism |
|---|---|---|---|---|
| REQUIRED | CF-RT-01 | HIGH/P0 | §2 | KFR canonicalization + YAML construct ban + new gate F-KFR-YAML-CONSTRUCT-FORBIDDEN + F-KFR-CANONICAL-SIGNATURE-INVALID supersedes F-KFR-SIGNATURE-INVALID |
| REQUIRED | CF-RT-02 | HIGH/P0 | §3 | Explicit AST node-type whitelist via `ast.NodeVisitor` + dunder-name ban + new gate F-DERIVATION-AST-FORBIDDEN-NODE |
| REQUIRED | CF-RT-04 | HIGH/P0 | §4 | `required_for_*` tag-mutation tamper-gate (analog of §4.4) + new gate F-KFR-TAG-MODIFIED + SP0 re-evaluation hook |
| REQUIRED | DC-CF-04 | HIGH | §5 | Constant-time hash compare via `hmac.compare_digest` + per-cross-check audit-log + SN-LLC seeding allowlist + F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING |
| REQUIRED | DC-CF-02 | MED→HIGH | §6 | `decimal.Decimal` mandate w/ fixed context + ban `float` in currency comparisons via PRE-runtime gate + AST-lint rule + F-CURRENCY-FLOAT-IN-COMPARISON |
| RECOMMENDED | CF-RT-03 | MED | §7.1 | AWARD_INGEST attestation requires admin-risk-ledger entry w/ rationale + F-AWARD-INGEST-ATTN-UNVERIFIED |
| RECOMMENDED | CF-RT-05 | MED | §7.2 | Composite-key uniqueness `(who, what, when_period)` at write-time + most-recent-`when_as_of` deterministic ordering + F-KFR-DUPLICATE-KEY |
| OPTIONAL-FOLDED | DC-CF-01 | LOW | §8.1 | Derivation runtime-arithmetic-error → F-DERIVATION-RUNTIME-ARITHMETIC-ERROR mapped explicitly |
| OPTIONAL-FOLDED | CF-RT-06 | LOW | §8.2 | Canonical-unit conversion before tolerance comparison + F-CURRENCY-UNIT-MISMATCH (composes with §6) |
| OPTIONAL-FOLDED | DC-CF-05 | LOW | §8.3 | Pydantic schema validation cache key pinned to `(path, mtime, size)`; spec-only edit |
| OPTIONAL-FOLDED | CF-RT-07 | LOW | §8.4 | Logfire `disable()` for Intake tool calls + redaction filter on `source_quote` fields + F-INTAKE-TELEMETRY-LEAK |
| OPTIONAL-DEFERRED | DC-CF-03 | LOW | §9.1 | Failure-code namespace info disclosure; deferred to v0.2 multi-tenant amendment (rationale: bounded by A1 + A4 at v0.1) |
| OPTIONAL-DEFERRED | CF-E-01..06 | MED×2 + LOW×4 | §9.2 | Editor clarity-polish; deferred to v7.0.4-M2 cosmetic at operator discretion (rationale: not load-bearing for Beta gate) |

**Eleven new failure codes total (10 fail-closed gates + 1 audit-only advisory):**

`F-KFR-YAML-CONSTRUCT-FORBIDDEN`, `F-KFR-CANONICAL-SIGNATURE-INVALID` (supersedes `F-KFR-SIGNATURE-INVALID`), `F-DERIVATION-AST-FORBIDDEN-NODE`, `F-KFR-TAG-MODIFIED`, `F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING`, `F-CURRENCY-FLOAT-IN-COMPARISON`, `F-CURRENCY-UNIT-MISMATCH`, `F-AWARD-INGEST-ATTN-UNVERIFIED`, `F-KFR-DUPLICATE-KEY`, `F-DERIVATION-RUNTIME-ARITHMETIC-ERROR`, `F-INTAKE-TELEMETRY-LEAK`.

`F-KFR-SIGNATURE-INVALID` (v7.0.4 §1.1) is **renamed and re-scoped** to `F-KFR-CANONICAL-SIGNATURE-INVALID` per §2.

# §2. CF-RT-01 closure — KFR canonicalization + YAML construct ban (HIGH/P0)

## §2.1 The path Single-Claude missed

Cross-family Red Team CF-RT-01 (verbatim, audit_v1_red_team.md): "an attacker crafts a KFR file that contains a signed *canonical* entry plus an unsigned duplicate introduced via `<<: *anchor` or a merge key. The signature is computed on the original serialized bytes; after parsing, the YAML processor merges the unsigned fields into the resulting object, and the Logician gate reads the *merged* object (which now contains tampered values) **without re‑checking the signature against the merged representation**."

The amendment v7.0.4 §1.1 said "verify Ed25519 signatures on every KFR entry **before any seat reads it**" but did NOT pin (a) what bytes the signature covers, (b) whether the verified bytes match the parsed object's representation, or (c) whether YAML constructs that decouple raw-byte representation from parsed-object representation are forbidden.

**Cross-family-specific lens:** YAML serialization edge-cases (PyYAML vs ruamel.yaml semantic differences; `&anchor`/`*alias`/`<<:` merge-keys) typically surface from non-Anthropic tooling experience. Anthropic-trained Red Team focused on higher-level logic (chain depth, tolerance widening, stale-fact landing) and missed the serialization surface entirely.

## §2.2 Closure mechanism — sign canonical bytes, not raw bytes

**Two-leg defense, both ship at M1 LOCK:**

### §2.2.1 Leg 1 — canonicalize before signing AND before verifying

Every KFR entry's signature covers the entry's **canonical JSON representation**, not its raw YAML bytes. The canonicalizer normalizes (in this exact order; deterministic pipeline):

1. **String NFC normalization (FIRST step before any byte-level work).** Every string value (mapping keys, scalar values, list elements) passes through `unicodedata.normalize('NFC', text)`. This closes the cross-loader divergence path where PyYAML may emit UTF-8 bytes while ruamel.yaml may emit `é`-style escapes for the same logical codepoint.
2. **Numeric representation pin.** Integers serialize as `<int>` (e.g., `123`). Decimal values serialize via Decimal-string shape per §6 (e.g., `"123.450000"`, never `"123.45"`). Floats are forbidden (per §6 ban-float discipline) but if encountered, fail-closed via `F-CURRENCY-FLOAT-IN-COMPARISON`. Forbidden number forms: exponential notation (`1e3`), hex/octal (`0xff`, `0o755`), `Infinity`, `-Infinity`, `NaN`, negative-zero (`-0` distinct from `0`). Negative-zero canonicalizes to `0`. Encounter of any forbidden form → `F-KFR-NUMERIC-CONSTRUCT-FORBIDDEN` (folded under `F-KFR-YAML-CONSTRUCT-FORBIDDEN`).
3. **Mapping key order: lexicographic** (Python `sorted()` semantics — codepoint comparison post-NFC).
4. **Whitespace: minimal.** No indent. One space after `:` and `,` per JSON convention. No trailing newline.
5. **Boolean representation: `true`/`false` only** (no `True`/`Yes`/`on` from YAML 1.1).
6. **Null representation: `null`** (not `~`, not empty).
7. **Array order: preserved** (lists are ordered; no implicit reorder).
8. **No comments, no aliases, no anchors, no merge-keys** — see Leg 2.

Implementation: `pipeline/logician/canonicalization/kfr_canonical.py` exposes `canonicalize(entry: dict) -> bytes`; signature verification calls `canonicalize` then verifies Ed25519 over the resulting bytes. Sign-side code path uses the same canonicalizer.

**Determinism contract:** for any operator's tooling that produces a KFR entry, `canonicalize(load(file_bytes))` returns the same bytes byte-for-byte across (a) PyYAML, (b) ruamel.yaml, (c) hand-written YAML. The contract is testable: differential test fixture under `tests/logician/canonicalization/test_kfr_canonical_differential.py` round-trips entries through three loaders and asserts byte-equal canonical output. NFC normalization is asserted explicitly in the test (input fixtures include NFC-equivalent codepoint sequences across all three loaders). Differential test is M1 LOCK ceremony pass-fail.

### §2.2.2 Leg 2 — schema forbids YAML anchors / aliases / merge-keys at the loader

The KFR YAML loader is a `yaml.SafeLoader` subclass that:

- Raises `yaml.constructor.ConstructorError` on any `Anchor` node (`&name`)
- Raises `yaml.constructor.ConstructorError` on any `Alias` node (`*name`)
- **Explicitly rejects ANY mapping key equal to the literal string `<<` BEFORE PyYAML's merge-key resolution runs** — even if the source YAML uses no anchor or alias to reach the merge key (RT-01 closure). The check happens at the constructor stage; any mapping with key `<<` raises `F-KFR-YAML-CONSTRUCT-FORBIDDEN` regardless of whether the value side is `*alias`, an inline mapping, or a sequence of mappings.
- Raises `yaml.constructor.ConstructorError` on the `tag:yaml.org,2002:merge` tag explicitly
- Raises on any tag prefix beyond the standard YAML 1.2 core tags
- Refuses any custom tag (`!!python/`, `!!set`, `!!omap`, etc.)

Implementation: `pipeline/logician/canonicalization/kfr_safe_loader.py` exposes `load_kfr_safe(path: pathlib.Path) -> dict`; failures raise `F-KFR-YAML-CONSTRUCT-FORBIDDEN` and abort the load fail-closed. Test fixture under `tests/logician/canonicalization/test_kfr_safe_loader_merge_key_reject.py` covers the merge-key path with and without explicit anchors (the path RT-01 surfaced).

**Defense in depth.** Leg 1 closes the bypass even if Leg 2 has an implementation bug (signature is over canonical, not raw — merge-key resolution would change canonical bytes and signature would fail). Leg 2 closes the bypass at first contact (no merge-key parses to begin with, so nothing reaches the canonicalizer).

## §2.3 Schema additions

KFR YAML files declare loader compliance in their preamble:

```yaml
schema_version: kfr.v1
canonicalization: kfr_canonical.v1
yaml_constructs_allowed: [scalar, mapping, sequence]
yaml_constructs_forbidden: [anchor, alias, merge_key, custom_tag]
# ... rest of v7.0.4 §1 schema unchanged ...
```

Pydantic schema validation (per v7.0.4 §1) extends to enforce `canonicalization == "kfr_canonical.v1"` and `yaml_constructs_forbidden` literal-set match.

The Benchmarks Register (`vault_shared/benchmarks/register.yaml`) also adopts canonicalization per §5.

## §2.4 New failure codes

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-KFR-YAML-CONSTRUCT-FORBIDDEN` | KFR file load encounters anchor / alias / merge-key / custom tag | HIGH (TAMPER_EVENT) | PRE-load |
| `F-KFR-CANONICAL-SIGNATURE-INVALID` | Ed25519 signature verification on canonical-JSON bytes fails | HIGH (TAMPER_EVENT) | PRE-load (replaces v7.0.4 `F-KFR-SIGNATURE-INVALID`) |

`F-KFR-AUDIT-CHAIN-BROKEN` (v7.0.4 §1.1) is unchanged — it covers chain ordering, not bytes covered.

## §2.5 What §2 does not change

- The Ed25519 keyring discipline (per v7 LOCKED M9) — unchanged.
- The audit_chain field shape — unchanged; chain entries are over canonical bytes too.
- The SP0 review surface — unchanged; canonicalization is invisible to the operator.
- v7.0.5 Funder Intelligence Database `content_hash` (SHA-3-512) — unchanged; the SHA-3-512-on-bytes pattern is for byte-equivalence, not signed-payload semantics.

## §2.6 Legacy KFR signature migration (RT-08 closure)

Pre-M1 KFR files were signed under v7.0.4 §1.1's raw-YAML-bytes contract. Under M1, those signatures are invalid against the canonical-JSON-bytes contract — first M1 read of any pre-M1 KFR would fail-closed with `F-KFR-CANONICAL-SIGNATURE-INVALID`, blocking all v0.1 Beta deployments that already have populated KFRs. M1 ships an explicit migration mode to close the operational gap:

### §2.6.1 Dual-verification mode

When the operator invokes `tilth kfr migrate-signatures --org <slug>` (one-time per org at M1 LOCK), the KFR PRE-gate enters **legacy-accept mode** for the duration of the migration cycle:

1. PRE-gate first attempts canonical-JSON signature verification (M1 §2 path)
2. If canonical-JSON verification fails AND legacy-accept mode is enabled, PRE-gate falls back to raw-YAML signature verification (v7.0.4 §1.1 path) using the original `F-KFR-SIGNATURE-INVALID` legacy gate code path
3. If raw-YAML verification PASSES, the entry is loaded; the operator is prompted at SP0 to **re-sign the entry under canonical-JSON** for forward compliance
4. Once all entries in the KFR are re-signed, legacy-accept mode auto-disables for that org (state stored at `orgs/<slug>/vault/kfr/_migration_state.yaml`, operator-Ed25519-signed)

### §2.6.2 Migration state file

```yaml
# orgs/<slug>/vault/kfr/_migration_state.yaml
schema_version: kfr_migration_state.v1
org_slug: <slug>
legacy_accept_mode: <enabled | disabled | completed>
migration_started_at_utc: <iso8601>
migration_completed_at_utc: <iso8601 | null>
operator_key_id_at_migration: <key_id>
entries_migrated: <count>
entries_pending: <count>
audit_chain:
  - operator_signature_at_migration_start
  - operator_signature_at_migration_completion
```

### §2.6.3 Forward discipline

After migration completes for an org, legacy-accept mode CANNOT be re-enabled without operator-signed admin-risk-ledger entry with rationale (analog of §4.4 tolerance-widen tamper-gate). New failure code: `F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED`.

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED` | `_migration_state.yaml` `legacy_accept_mode` mutated from `disabled`/`completed` to `enabled` without operator-signed admin-risk-ledger entry | HIGH | PRE-write |

Discipline ensures legacy-accept mode is a **migration tool, not a permanent bypass**. Once disabled, re-enabling is a tamper event.

# §3. CF-RT-02 closure — Derivation AST whitelist enumerated (HIGH/P0)

## §3.1 The path Single-Claude missed

Cross-family Red Team CF-RT-02 (verbatim): "the specification says 'AST‑validated' but does not enumerate the allowed node whitelist. An attacker could supply a formula like `(__import__('os').system('rm -rf /tmp')) or kfr_facts['x'].value` or `kfr_facts['x'].__class__.__mro__[1].__subclasses__()[42]()`. If the validator only checks that the AST is *syntactically* an expression and does not explicitly reject `Call`, `Attribute`, or `Subscript` nodes that reference dunder names, the formula will be accepted, signed by the operator (who may be compromised), and at **draft‑time** the Logician evaluator will execute arbitrary code **or** read data from memory that is not a KFR fact."

v7.0.4 §4.5 said:
```
derivation_formula: <expr>
<expr>: <kfr_ref> | <expr> <op> <expr> | <literal>
<kfr_ref>: kfr_facts['<fact_id>'].value
<op>: + | - | * | /
<literal>: <int> | <float>
```

That's an informal grammar in prose. The implementation surface — what `ast.NodeVisitor` accepts, what node types pass — is left to the Logician seat. Without an explicit whitelist, `ast.parse("(__import__('os').system('rm -rf /'))")` returns a syntactically valid expression. Without explicit `ast.Call` rejection, the formula accepts arbitrary code.

## §3.2 Closure mechanism — explicit whitelist visitor

**Allowed AST node types** (deterministic enumeration; closed set; any other node type fails fail-closed):

| Node type | Purpose | Constraint |
|---|---|---|
| `ast.Expression` | Top-level wrapper | exactly 1 per derivation_formula |
| `ast.BinOp` | `+`, `-`, `*`, `/`, `//`, `%` | operators restricted to `ast.Add`, `ast.Sub`, `ast.Mult`, `ast.Div` only — `Mod` and `FloorDiv` rejected at v0.1 (defer to M2 if currency tolerance work needs them) |
| `ast.UnaryOp` | unary minus / unary plus | operator restricted to `ast.USub`, `ast.UAdd` only — `Not` and `Invert` rejected |
| `ast.Constant` | numeric literal (int / Decimal-string) | Decimal-string literals must round-trip per §6.3 |
| `ast.Name` | only the literal identifier `kfr_facts` | any other Name node fails F-DERIVATION-AST-FORBIDDEN-NODE |
| `ast.Subscript` | subscript on `ast.Name(id='kfr_facts')` only | the subscript value must be `ast.Constant` of `str` type (a fact_id literal); no nested subscripts; no slice expressions; no computed indices |
| `ast.Attribute` | only `.value` on the Subscript result | attribute name MUST equal `value`; no other attribute name allowed |
| `ast.Load` | context for Name / Subscript / Attribute reads | required by AST grammar; not load-bearing semantically |

**Forbidden AST node types** (explicit reject list — any of these → `F-DERIVATION-AST-FORBIDDEN-NODE`):

`ast.Call`, `ast.Lambda`, `ast.IfExp`, `ast.Dict`, `ast.Set`, `ast.ListComp`, `ast.SetComp`, `ast.DictComp`, `ast.GeneratorExp`, `ast.Await`, `ast.Yield`, `ast.YieldFrom`, `ast.Compare`, `ast.BoolOp`, `ast.NamedExpr`, `ast.Starred`, `ast.JoinedStr`, `ast.FormattedValue`, `ast.List`, `ast.Tuple`, `ast.Slice`, **`ast.Index` (Python 3.8/3.9 legacy slice wrapper)**, `ast.Pass`, `ast.Continue`, `ast.Break`, `ast.Return`, `ast.Raise`, `ast.Try`, `ast.With`, `ast.Async*`, `ast.Class*`, `ast.Function*`, `ast.Import*`, `ast.Global`, `ast.Nonlocal`, `ast.Delete`, `ast.Assign*`, `ast.AnnAssign`, `ast.AugAssign`, `ast.For`, `ast.While`, `ast.If`, `ast.Module`, `ast.Interactive`, any `ast.Attribute` whose `attr` value contains `__` (dunder), any `ast.Name` whose `id` value starts or ends with `_` or contains `__`.

**Legacy slice-wrapper handling (RT-03 closure).** Python 3.8 and 3.9 wrap subscript slices in `ast.Index(value=...)`. The visitor MUST refuse `ast.Index` outright — only `ast.Constant` directly under `ast.Subscript.slice` is admitted. The visitor does not "descend through" `ast.Index` to inspect its child; the wrapper itself fails fail-closed. This forecloses any 3.8/3.9 cross-version inconsistency.

**Float-constant rejection (RT-10 closure).** `ast.Constant` is admitted ONLY when `type(value) in {int, str}`. `type(value) is float` → fail-closed via `F-DERIVATION-AST-FORBIDDEN-NODE` (with sub-tag `.float_constant`). Currency-typed derivations encode their numeric values as `ast.Constant(value=str)` Decimal-string literals (e.g., `Constant(value="123.45")`) which the derivation evaluator parses into Decimal in `KFR_DECIMAL_CONTEXT` per §6. Composes with §6.4 `F-CURRENCY-FLOAT-IN-COMPARISON`.

**Identifier discipline.** Any identifier (`ast.Name.id` or `ast.Attribute.attr`) that:

- Contains `__` (dunder)
- Starts or ends with `_`
- Is not `kfr_facts` (for Name) or `value` (for Attribute)

→ fails `F-DERIVATION-AST-FORBIDDEN-NODE` fail-closed.

**Subscript-key-string discipline (RT-04 closure).** When `ast.Constant.value` is used as a subscript key (i.e., the slice argument to `ast.Subscript`), the visitor validates the STRING CONTENTS of the Constant against the dunder pattern AND against any double-underscore substring. Specifically: `ast.Constant(value=<str>)` used as slice → reject if `value` matches regex `^__.*__$` OR contains `__` (substring). This forecloses `kfr_facts['__class__']` and similar attacks where the dunder is in the literal string, not the AST identifier.

## §3.3 Implementation contract

`pipeline/logician/derivation/ast_whitelist.py` exposes `validate_derivation_formula(formula: str) -> ParsedFormula`:

1. `tree = ast.parse(formula, mode='eval')` — refuses anything not a single expression
2. `visitor = WhitelistVisitor()`
3. `visitor.visit(tree)` — visits every node; non-whitelisted node type raises `F-DERIVATION-AST-FORBIDDEN-NODE` immediately
4. After successful visit, returns a `ParsedFormula` carrying the whitelisted AST + the set of `(fact_id, attribute)` pairs referenced (for derivation_formula provenance audit)

The visitor is **explicit allow-list, not deny-list** — any node type the visitor doesn't explicitly handle raises. This is the correct security posture per L-013 fail-closed defaults.

`validate_derivation_formula` runs at:

- **Write-time** — when an operator-signed derivation override is written to `pipeline/validation/fact_overrides/<rfa_hash>/<derivation_id>.yaml`, the `derivation_formula` field is validated before the signature is accepted
- **Draft-time read** — when Logician POST-gate evaluates a draft claim with `derivation_id` annotation, the override's formula is re-validated (defense-in-depth — even if write-time validation has a bug, draft-time catches)

## §3.4 Composes with v7.0.4 §4.5 chain-depth limit

§4.5's chain-depth-1 rule (derivations reference only KFR entries, not other derivations) is preserved. The whitelist visitor enforces it structurally — only `ast.Subscript(value=ast.Name(id='kfr_facts'), slice=ast.Constant(value=<fact_id>))` is admitted; any reference to `derivations[...]` would surface as `ast.Subscript(value=ast.Name(id='derivations'), ...)` and the `id != 'kfr_facts'` check fails at the `ast.Name` visitor.

## §3.5 New failure code

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-DERIVATION-AST-FORBIDDEN-NODE` | Whitelist visitor encounters non-whitelisted node type OR forbidden identifier OR forbidden attribute name | HIGH | PRE-write (override accept) AND POST-read (draft evaluation) |

# §4. CF-RT-04 closure — `required_for_*` tag-mutation tamper-gate (HIGH/P0)

## §4.1 The path Single-Claude missed

Cross-family Red Team CF-RT-04 (verbatim): "the amendment mandates a hard‑block when a `required_for_funder`‑tagged fact is in *NEEDED* state at SP0 sign‑out, but it never specifies that **removing** the `required_for_funder` tag itself is a protected operation. An operator (or a compromised key) could edit the KFR entry to delete the tag before SP0, thereby silently disabling the hard‑block and allowing the pipeline to continue with a missing required fact. Because the tag‑removal is not logged as a 'tolerance‑widen' or 'audit‑chain' event, the system would not raise any failure code."

v7.0.4 §3.2 establishes `F-LOGICIAN-FACT-NEEDED-REQUIRED` as a hard-block when a tagged-required fact is NEEDED at SP0. v7.0.4 §4.4 introduces tamper-gating for tolerance-widening (`F-LOGICIAN-FACT-TOLERANCE-DRIFT`). The combination defends against numeric drift but **leaves a hole on metadata mutation** — the tag list itself is not gated.

**Cross-family-specific lens:** Anthropic-trained Red Team focused on numeric drift (chain depth, tolerance widening, stale-fact landing); they did not explore metadata-tampering pathways. Metadata integrity vs. value integrity is a different adversarial mental model that surfaces from non-Anthropic adversarial training.

## §4.2 Closure mechanism — tag-mutation as a tamper-gate (analog of §4.4)

Any modification to the following KFR fact fields is admin-risk-ledger logged at HIGH severity, requires operator-signed re-confirmation at next SP0, and triggers `F-KFR-TAG-MODIFIED` fail-closed if no signed ledger entry exists:

- `required_for_category` — list of CIC categories the fact is required for
- `required_for_funder` — list of specific funders the fact is required for
- `key_credentials.*` (the entire key_credentials sub-block — its presence/absence is itself metadata)

**Mutation events (any one of these triggers the gate):**

- Add a tag (e.g., add `USDA-VAPG` to `required_for_funder`)
- Remove a tag (e.g., delete `USDA-VAPG` from `required_for_funder`)
- Reorder tag list (deterministically detected via canonical comparison; reorder alone doesn't trigger, but a reorder coincident with element-set change does)
- Replace tag list wholesale

### §4.2.1 Disk-state SHA3-512 hash (RT-05 closure — supersedes memory-cache comparison)

Tag-mutation detection MUST use **on-disk** state, not in-memory cache. Atomic-replace via `os.replace(tmp, kfr.yaml)` would silently bypass an in-memory-cache comparison; the disk-hash mechanism closes the path.

For each KFR fact, Logician computes a deterministic `tag_set_hash`:

```python
def compute_tag_set_hash(fact: dict) -> bytes:
    """Compute SHA3-512 over canonical tag-set tuple. Deterministic across loaders.

    Uses the §2.2.1 canonicalizer to NFC-normalize and sort tag-set members
    so that semantically equal tag sets hash identically.
    """
    tag_payload = canonical_dump({
        "fact_id": fact["id"],
        "required_for_category": sorted(fact.get("required_for_category") or []),
        "required_for_funder": sorted(fact.get("required_for_funder") or []),
        "key_credentials_present": fact.get("key_credentials") is not None,
        "key_credentials_keys": sorted((fact.get("key_credentials") or {}).keys()),
    })
    return hashlib.sha3_512(tag_payload).digest()
```

The hash is recomputed from disk (via `load_kfr_safe(path)` per §2.2.2 Leg 2) on every Logician PRE-gate invocation. The hash is compared against the most-recent admin-risk-ledger entry's `tag_set_hash` (where the ledger is also loaded from disk per cycle).

**Inode-change detection.** The KFR file's inode is tracked in `_migration_state.yaml`-style metadata (`orgs/<slug>/vault/kfr/_disk_state.yaml`); on inode change (file replaced atomically), Logician INVALIDATES any in-memory cache before the next read. This composes with the disk-hash discipline — disk-hash is authoritative; cache is a performance optimization that fails-safe on inode change.

### §4.2.2 KFR + ledger atomic-read discipline (Cycle-2 RT-05 closure)

The disk-hash mechanism in §4.2.1 reads two artifacts: (a) the KFR file containing the fact's tag set, and (b) the admin-risk ledger entry containing the operator-signed `tag_set_hash_after`. Reading them sequentially admits a race window where an attacker with write access could atomic-replace BOTH artifacts within the read window, leaving the gate to compare the new KFR hash against the new ledger hash (matching) without an operator signature on the new ledger entry actually existing on the previous read.

Closure: both reads occur under a shared advisory lock + symlink rejection.

```python
import fcntl, os, errno
from pathlib import Path

def read_kfr_and_ledger_atomic(kfr_path: Path, ledger_path: Path) -> tuple[dict, dict]:
    """Read KFR + ledger entry under shared fcntl.flock; refuse symlinked paths.

    Discipline:
      1. Reject if either path is a symlink (os.path.islink).
      2. Acquire shared (LOCK_SH) flock on the org's vault directory FD.
      3. Open both files via os.open(O_RDONLY | O_NOFOLLOW) on the same directory FD.
      4. Read both contents under the lock.
      5. Release lock on close.

    fcntl.flock prevents the atomic-replace path: any rename(2) on the locked
    directory blocks until the read completes (BSD/Linux semantics; documented).
    O_NOFOLLOW closes the symlink-swap path: a path that became a symlink
    during the read window fails ELOOP at open(2) time.
    """
    if os.path.islink(kfr_path) or os.path.islink(ledger_path):
        raise FKfrPathSymlinkForbidden(...)  # F-KFR-PATH-SYMLINK-FORBIDDEN

    org_vault_dir = kfr_path.parent.parent  # orgs/<slug>/vault/
    dir_fd = os.open(org_vault_dir, os.O_RDONLY)
    try:
        fcntl.flock(dir_fd, fcntl.LOCK_SH)  # shared lock; blocks atomic-replace
        try:
            kfr_fd = os.open(kfr_path, os.O_RDONLY | os.O_NOFOLLOW)
            ledger_fd = os.open(ledger_path, os.O_RDONLY | os.O_NOFOLLOW)
            try:
                kfr_bytes = os.read(kfr_fd, MAX_KFR_BYTES)
                ledger_bytes = os.read(ledger_fd, MAX_LEDGER_BYTES)
            finally:
                os.close(kfr_fd)
                os.close(ledger_fd)
        finally:
            fcntl.flock(dir_fd, fcntl.LOCK_UN)
    finally:
        os.close(dir_fd)

    return load_kfr_safe(kfr_bytes), load_ledger(ledger_bytes)
```

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-KFR-PATH-SYMLINK-FORBIDDEN` | KFR or ledger path is a symlink at read time | HIGH | PRE-load |

Trade-off note: the shared `flock` introduces a serialization point during gate evaluation. Empirical wall-clock impact at v0.1 single-client A1 is negligible (one operator at a time; lock contention rare). At Stage-2+ multi-tenant horizon, lock granularity can be tightened to per-fact rather than per-vault-directory if contention surfaces.

### §4.2.3 Ledger entry shape

The admin-risk-ledger entry includes:

```yaml
ledger_kind: kfr_tag_modified
fact_id: <fact_id>
tag_set_hash_before: <hex SHA3-512>  # disk-state hash captured by previous PRE-gate
tag_set_hash_after: <hex SHA3-512>   # disk-state hash captured by current PRE-gate
tag_field_changed: required_for_category | required_for_funder | key_credentials | multiple
tag_set_before: [<tag>, ...]  # canonical-sorted (audit-readable)
tag_set_after: [<tag>, ...]   # canonical-sorted (audit-readable)
operator_key_id: <key_id>
signed_at_utc: <iso8601>
rationale: <operator-supplied free text>
```

**SP0 re-evaluation hook.** At every SP0 sign-out, Logician re-loads the current KFR tag set FROM DISK and re-evaluates `required_for_funder` matches against the current RFA. If a tag was REMOVED for a funder that matches the current RFA AND the corresponding fact is in NEEDED state, **F-LOGICIAN-FACT-NEEDED-REQUIRED still fires** (even though the tag is now absent — SP0 reads the ledger and treats the pre-removal tag set as authoritative if no operator re-confirmation has landed in the current cycle).

The combination defeats the bypass: removing the tag still triggers the hard-block via SP0's ledger-aware re-evaluation; the operator must explicitly re-confirm the tag removal at SP0 (with rationale) to clear the block.

## §4.3 Schema additions

KFR fact entry gains a derived-at-load field (not on-disk; computed by Logician PRE-gate):

```yaml
# Derived at load (NOT stored in YAML):
required_for_funder_authoritative: <ledger-aware merge of on-disk tags + most-recent operator-confirmed mutation history>
required_for_category_authoritative: <same pattern>
```

Logician gates use the `_authoritative` view for hard-block evaluation, not the on-disk view. This is the structural enforcement of "tag-removal cannot silently disable the hard-block."

## §4.4 New failure code

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-KFR-TAG-MODIFIED` | KFR fact's `required_for_*` or `key_credentials` field modified without admin-risk-ledger entry + operator signature | HIGH (TAMPER_EVENT) | PRE-write |

## §4.5 Composes with v7.0.4 §3.2 + §4.4

§3.2 NEEDED hard-block now reads `required_for_funder_authoritative` (ledger-aware), not the on-disk YAML field directly.
§4.4 tolerance-widening tamper-gate is unchanged; M1 §4 is the structural parity for metadata mutation.
v7.0.4 §1.1 audit_chain captures signature events; M1 §4 captures tag-mutation events. Both flow into the same admin-risk ledger format.

# §5. DC-CF-04 closure — Benchmark constant-time cross-check + audit-log (HIGH)

## §5.1 The path Single-Claude missed

Cross-family Judge DC-CF-04 (verbatim): "An actor with write access to the shared Benchmarks Register can probe for the existence of specific numeric facts within the entire Tilth instance, confirming if *any* organization has a KFR entry with that value. This is a side-channel attack that violates the strict 'no cross-org reads' tenet of Law 3."

v7.0.4 §7.2's `F-BENCHMARK-CONTAINS-PER-ORG-REF` checks "value tolerance-matches a value in any per-org KFR." The match check uses workspace-shared canonical-value hashing. The amendment claimed "no per-org KFR content is exposed cross-org by the gate; the gate computes a value-hash check pair only." This is true at the data layer but creates a **boolean oracle at the gate layer** — the gate's response (PASS / FAIL) is itself the leaked bit per cross-check attempt.

## §5.2 Closure mechanism — three concurrent defenses

### §5.2.1 Defense 1 — constant-time hash compare

Replace any short-circuit boolean equality (`if hash_a == hash_b`) with `hmac.compare_digest(hash_a, hash_b)`. The constant-time comparison eliminates timing side-channels (which an attacker can use to differentiate "the gate fired because the byte-prefix matched 0 bytes" from "the gate fired after byte-prefix matched N bytes" — still a leakage signal even if the boolean output is suppressed).

Implementation: `pipeline/logician/benchmarks/cross_check.py` exposes `value_hash_match(benchmark_hash: bytes, kfr_hash: bytes) -> bool` using `hmac.compare_digest`. All call sites use this helper; AST-lint rule R-BENCHMARK-NO-SHORT-CIRCUIT-COMPARE forbids direct `==` on cross-org hash bytes (per CodeBase guard).

### §5.2.2 Defense 2 — audit-log every cross-check (success AND failure)

Every benchmark cross-check call writes a row to `pipeline/logician/audit/<utc-date>.jsonl`:

```yaml
ledger_kind: benchmark_cross_check
benchmark_id: <id>
target_org_kfr_namespace: orgs/<slug>/vault/kfr/  # the namespace queried
result: matched | not_matched
operator_key_id: <key_id of the writer/seeder>
checked_at_utc: <iso8601>
caller_seat: <scout | scribe | editor | judge | red_team | logician | sn_llc_seeder>
```

Audit-log entry is mandatory; if the entry is missing for any cross-check call, `F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING` fires fail-closed at the next read.

The audit-log makes every probe attempt a permanent record. An attacker probing K values to find a specific fact accumulates K log entries — **the probe is no longer free; it's monotonically expensive**. Combined with admin-risk-ledger HIGH-severity at log-write, even a single probe is operator-visible.

**Ordering discipline (RT-06 closure — eliminates audit-log timing side-channel).** The audit-log write occurs **BEFORE** the constant-time `compare_digest` call, with both branches padded to constant-size payload:

```python
def cross_check_with_audit(benchmark_hash: bytes, kfr_hash: bytes,
                            org_slug: str, caller_seat: str,
                            audit_log_path: Path) -> bool:
    """Constant-time cross-check with timing-equalized audit-log write.

    Discipline:
      1. Write audit-log row FIRST (before comparison) with placeholder result
      2. fsync the audit-log file descriptor
      3. THEN run hmac.compare_digest
      4. Update audit-log row with actual result via fixed-size append
      5. fsync again

    Both branches (matched/not_matched) execute identical I/O paths.
    """
    # Step 1: write placeholder row, FIXED SIZE
    placeholder = {
        "ledger_kind": "benchmark_cross_check",
        "result": "PENDING_____",  # fixed-width placeholder
        # ... other fields ...
    }
    with open(audit_log_path, "a") as f:
        f.write(json.dumps(placeholder) + "\n")
        f.flush()
        os.fsync(f.fileno())

    # Step 2: constant-time comparison
    matched = hmac.compare_digest(benchmark_hash, kfr_hash)

    # Step 3: append result-update row (fixed size; both branches identical write)
    result_row = {
        "ledger_kind": "benchmark_cross_check_result",
        "placeholder_id": ...,
        "result": "matched_____" if matched else "not_matched_",  # fixed-width
    }
    with open(audit_log_path, "a") as f:
        f.write(json.dumps(result_row) + "\n")
        f.flush()
        os.fsync(f.fileno())

    return matched
```

Both branches execute identical syscalls (write + fsync × 2). The audit-log writer cannot leak boolean outcome via timing — the I/O cost is paid uniformly. Implementation contract is testable: `tests/logician/benchmarks/test_cross_check_constant_time.py` measures wall-clock variance across matched/not_matched branches; M1 LOCK requires variance < 1ms per call across 1000 invocations.

### §5.2.3 Defense 3 — SN-LLC seeding allowlist (Ed25519-signed; integrity-protected)

`vault_shared/benchmarks/_seeding_allowlist.yaml` (operator-curated) lists the canonical funder/agency/research-source domains and document-paths that benchmark seeding may draw from. Sources outside the allowlist fail `F-BENCHMARK-CONTAINS-PER-ORG-REF.source_doc_unauthorized` PRE-write.

**Allowlist integrity protection (RT-09 closure).** The allowlist file is signed with the operator's Ed25519 key on every modification; the allowlist loader verifies the signature on every load and refuses unsigned/tampered allowlists fail-closed. The signing surface uses canonical-JSON bytes per §2.2.1 (same canonicalization discipline as KFR).

```yaml
# vault_shared/benchmarks/_seeding_allowlist.yaml
schema_version: benchmark_seeding_allowlist.v1
canonicalization: kfr_canonical.v1  # same canonicalizer as KFR
populated_by: <operator_key_id>
populated_at: <iso8601>
allowed_source_domains:
  - "*.usda.gov"
  - "*.nsf.gov"
  - "*.census.gov"
  - "*.bls.gov"
  - "data.pa.gov"
allowed_source_path_prefixes:
  - "vault_shared/funder_intelligence/docs/"  # if a funder doc has been operator-curated, benchmarks derived from it can be seeded
  - "vault_shared/seeding_imports/"  # SN-LLC seeding upload path
forbidden_source_path_prefixes:
  - "orgs/"   # any orgs/<slug>/... source is forbidden as a benchmark source
  - "/tmp/"
  - "/var/"
audit_chain:
  - operator_signature_at_initial_population
  - operator_signature_per_modification
signature_ed25519: <base64-encoded signature over canonical-JSON bytes>
signature_key_id: <operator key_id>
```

**Loader discipline.** `pipeline/logician/benchmarks/seeding_allowlist_loader.py` MUST:

1. Read the file from disk
2. Compute canonical-JSON bytes per §2.2.1 (excluding `signature_ed25519` and `signature_key_id` fields)
3. Verify Ed25519 signature against operator-keyring active-key catalog (per v7.0.4 §1.1 keyring discipline)
4. On verification failure → `F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID` fail-closed; refuse to load; benchmark seeding refuses pre-write
5. On verification success → load the allowlist into the gate

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID` | Allowlist file Ed25519 signature verification fails | HIGH (TAMPER_EVENT) | PRE-load |

## §5.3 v0.1 single-client posture

A1 (single-client per Golden Quill) makes the cross-org leak surface theoretically zero at v0.1 — there's only one org's KFR per Tilth, so "cross-org" has no other org to leak to. M1 §5 still ships full defense because:

1. **Stage-2+ multi-tenant horizon will reuse the gate** — the structural defense lives in the v0.1 LOCKed code surface, not invented at Stage 2.
2. **Even at v0.1, the gate defends against operator/SN-LLC accidentally seeding a benchmark from THIS client's KFR** — bad provenance even if not Law-3 leak.
3. **Constant-time + audit-log + allowlist are all cheap** — no architectural cost.

## §5.4 New failure codes

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING` | Benchmark cross-check call has no corresponding audit-log row | HIGH | POST-check (next read) |
| `F-BENCHMARK-SEEDING-SOURCE-UNAUTHORIZED` | Benchmark seeding source_doc not in `_seeding_allowlist.yaml` | HIGH | PRE-write |

`F-BENCHMARK-CONTAINS-PER-ORG-REF` (v7.0.4 §7.2) is preserved with its source_doc-path leg + an updated value-leg: the value-leg now uses `hmac.compare_digest` with mandatory audit-log per §5.2.2.

# §6. DC-CF-02 closure — Decimal currency mandate; ban float in tolerance comparisons (MED→HIGH)

## §6.1 The path Single-Claude missed

Cross-family Judge DC-CF-02 (verbatim): "The currency tolerance rule is specified mathematically but the amendment does not mandate the use of `Decimal` types in the Pydantic schema and Logician implementation. Standard floating-point arithmetic is subject to precision errors that could cause the gate to fail or pass incorrectly at the tolerance boundary."

v7.0.4 §4 specifies `abs(draft_value - kfr_value) > max(0.005 * kfr_value, $2500)`. The arithmetic is mathematically clean but Python's default numeric type is `float` (IEEE-754 double). At the `0.005 * kfr_value` boundary, IEEE-754 can drift by ±epsilon. Over a $5M currency fact, ±epsilon × $5M ≈ ±$0.0025 — small but nonzero. At `$2500` floor + epsilon-boundary draft values, the comparison can fire false-positive ("tolerance violated by $0.0001") or false-negative ("tolerance preserved despite $0.0001 over").

**Severity escalation at M1.** Audit synthesis flagged DC-CF-02 as MEDIUM. M1 promotes to **HIGH** because the amendment's primary goal (P1: "bad numbers cannot ship") fails directly on this path — a wrong currency value passes the gate due to float imprecision.

## §6.2 Closure mechanism — Decimal context, helper, ban float

### §6.2.1 Decimal context fixed at Golden Image (with explicit-context-required guard)

`pipeline/logician/currency/decimal_arithmetic.py` exposes:

```python
import decimal
from decimal import Decimal

KFR_DECIMAL_CONTEXT = decimal.Context(
    prec=28,
    rounding=decimal.ROUND_HALF_EVEN,  # banker's rounding
    Emin=-99999, Emax=99999,
    capitals=1, clamp=0,
    flags=[], traps=[
        decimal.DivisionByZero,
        decimal.Overflow,
        decimal.InvalidOperation,
        # Note: Inexact NOT trapped — Decimal arithmetic SHOULD be inexact for non-terminating divisions.
    ]
)

# RT-07 closure — module-import-time runtime guard.
# Asserts that decimal.getcontext() returns KFR_DECIMAL_CONTEXT semantics
# at every helper-call entry. Any code that mutated the global context
# via decimal.localcontext() must have RESTORED before our helper is called.
def _assert_kfr_context_active():
    """Runtime guard asserting decimal.getcontext() == KFR_DECIMAL_CONTEXT.

    Compares prec + rounding + traps explicitly. If any drifted (e.g., from a
    decimal.localcontext() block that exited improperly OR from third-party
    code mutating decimal.getcontext()), raise F-CURRENCY-DECIMAL-CONTEXT-DRIFT.
    """
    current = decimal.getcontext()
    if (current.prec != KFR_DECIMAL_CONTEXT.prec
            or current.rounding != KFR_DECIMAL_CONTEXT.rounding
            or current.traps != KFR_DECIMAL_CONTEXT.traps):
        raise FCurrencyDecimalContextDrift(...)  # F-CURRENCY-DECIMAL-CONTEXT-DRIFT

def to_currency(value: int | str | Decimal, *, context: decimal.Context = None) -> Decimal:
    """Canonical conversion to currency-typed Decimal. Refuses float input fail-closed.

    REQUIRES explicit context argument (RT-07 closure) — passing context=None
    raises F-CURRENCY-CONTEXT-OMITTED. The caller MUST pass KFR_DECIMAL_CONTEXT
    explicitly. This forecloses fallback to decimal.getcontext() which third-party
    code may have mutated.
    """
    if context is None:
        raise FCurrencyContextOmitted(...)  # F-CURRENCY-CONTEXT-OMITTED
    if context is not KFR_DECIMAL_CONTEXT:
        raise FCurrencyContextMismatch(...)  # F-CURRENCY-CONTEXT-MISMATCH
    _assert_kfr_context_active()
    if isinstance(value, float):
        raise FCurrencyFloatInComparison(...)  # F-CURRENCY-FLOAT-IN-COMPARISON
    return Decimal(str(value), context=context).quantize(Decimal("0.01"), context=context)

def tolerance_check_currency(draft: Decimal, kfr: Decimal, *,
                              tolerance_pct: Decimal = Decimal("0.005"),
                              tolerance_floor: Decimal = Decimal("2500"),
                              context: decimal.Context = None) -> bool:
    """Returns True if PASS (within tolerance), False if FAIL (out of tolerance).

    REQUIRES explicit context argument. Refuses float for any of:
    draft, kfr, tolerance_pct, tolerance_floor.
    """
    if context is None:
        raise FCurrencyContextOmitted(...)
    if context is not KFR_DECIMAL_CONTEXT:
        raise FCurrencyContextMismatch(...)
    _assert_kfr_context_active()
    for arg_name, arg in [("draft", draft), ("kfr", kfr),
                           ("tolerance_pct", tolerance_pct),
                           ("tolerance_floor", tolerance_floor)]:
        if isinstance(arg, float):
            raise FCurrencyFloatInComparison(arg_name, ...)
    delta = abs(draft - kfr)
    threshold = max(tolerance_pct * kfr, tolerance_floor)
    return delta <= threshold
```

**Explicit-context discipline.** The helper API REQUIRES every caller to pass `KFR_DECIMAL_CONTEXT` explicitly. Omitting the context argument raises `F-CURRENCY-CONTEXT-OMITTED`; passing a different context raises `F-CURRENCY-CONTEXT-MISMATCH`. The runtime guard `_assert_kfr_context_active()` catches the case where a `decimal.localcontext()` block has not properly restored the global context before the helper runs. Three layers of defense — explicit-context-required + identity-check + runtime-guard — close the context-hijack path.

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-CURRENCY-CONTEXT-OMITTED` | Currency helper called with `context=None` | HIGH | PRE-runtime |
| `F-CURRENCY-CONTEXT-MISMATCH` | Currency helper called with `context is not KFR_DECIMAL_CONTEXT` | HIGH | PRE-runtime |
| `F-CURRENCY-DECIMAL-CONTEXT-DRIFT` | `decimal.getcontext()` semantics differ from `KFR_DECIMAL_CONTEXT` at helper-call entry | HIGH | PRE-runtime |

### §6.2.2 Pydantic schema enforcement

KFR currency-typed values use `pydantic.Decimal` (or `pydantic.condecimal(max_digits=28, decimal_places=2)`). Pydantic schema validation refuses `float` input fail-closed.

KFR `unit: USD` and `unit: <currency-iso-code>` fields signal currency type; values for those entries must be Decimal-shape strings on disk (e.g., `"123450.00"` not `123450.0` not `123450`). The Pydantic schema validator enforces shape match.

### §6.2.3 Ban float in comparisons — three-layer defense

**Layer 1 — runtime gate.** `tolerance_check_currency` and all currency arithmetic helpers raise `F-CURRENCY-FLOAT-IN-COMPARISON` fail-closed if any input is `float`.

**Layer 2 — AST-lint rule R-CURRENCY-NO-FLOAT-COMPARE.** `pipeline/linting/r_currency_no_float_compare.py` scans Logician + KFR + Benchmarks code paths and forbids `float` literals adjacent to currency-typed `Decimal` arithmetic. Surfaces at CI gate (test suite).

**Layer 3 — type-check guard.** `mypy` strict mode on currency-arithmetic modules; `Decimal` types declared explicitly; `float` input rejected at typecheck.

## §6.3 Composes with §3 derivation AST whitelist

The derivation AST whitelist (§3) admits `ast.Constant` with numeric literals. M1 extends the whitelist constraint:

- Currency-typed derivation formulas REQUIRE Decimal-string literals (`Decimal("123.45")` literal — but since `ast.Call` is forbidden, the Decimal-string literal pattern is encoded as a `ast.Constant` of `str` type that the derivation evaluator parses into Decimal at evaluation time).
- The derivation evaluator runs in the `KFR_DECIMAL_CONTEXT` for currency-typed derivations.
- Mixing Decimal and float in a single derivation formula → `F-CURRENCY-FLOAT-IN-COMPARISON` fail-closed.

## §6.4 New failure code

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-CURRENCY-FLOAT-IN-COMPARISON` | `float` value reaches a currency tolerance comparison OR a currency arithmetic helper | HIGH | PRE-runtime (helper-call entry) |

## §6.5 Tolerance config table — Decimal-aware (supersedes v7.0.4 §4 row)

| Fact type | Tolerance | Implementation |
|---|---|---|
| Identifiers | Exact match | string equality |
| Legal claims | Exact match | string equality |
| Counts | ≤2% (configurable) | Decimal arithmetic; `Decimal("0.02")` constant |
| **Currency** | **≤0.5% with floor of $2,500** | **Decimal arithmetic; `Decimal("0.005")` and `Decimal("2500")`; float input → F-CURRENCY-FLOAT-IN-COMPARISON** |
| Percentages and rates | ±1 pp absolute | Decimal arithmetic |
| Dates | Exact (or `tolerance_days` if specified) | datetime arithmetic |
| Ranges | Bound-by-bound per underlying type | Decimal or count rule |

# §7. RECOMMENDED closures (close before Stage-2 horizon — fold in at M1)

## §7.1 CF-RT-03 — AWARD_INGEST attestation requires operator rationale (MED)

v7.0.4 §5.3 admits an `--attest-unsigned-award-doc` operator flag that bypasses signature verification when the funder doesn't sign. The flag is single-bit trust anchor; no rationale, no admin-risk-ledger trail.

**Closure:** any invocation of the attestation flag requires a non-empty `--rationale` argument (operator-supplied free text). Logician PRE-gate writes:

```yaml
ledger_kind: award_ingest_attestation
grant_id: <id>
award_doc_path: <path>
attestation_rationale: <operator text>
operator_key_id: <key_id>
signed_at_utc: <iso8601>
```

Missing rationale → `F-AWARD-INGEST-ATTN-UNVERIFIED` fail-closed; the AWARD_INGEST refuses.

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-AWARD-INGEST-ATTN-UNVERIFIED` | Attestation flag invoked without rationale field OR without admin-risk-ledger entry | MED | PRE-AWARD_INGEST |

## §7.2 CF-RT-05 — Composite-key uniqueness + most-recent-`when_as_of` ordering (MED)

v7.0.4 §4.6 STALE-ACKNOWLEDGED tolerance landing iterates KFR entries in file order. When operator marks fact A STALE then promotes A' (different `id`, same `who/what/when_period`), gate iteration ordering can land on either entry; spec does not pin tie-breaking.

**Closure:** two-leg defense.

### §7.2.1 Leg 1 — composite-key uniqueness at write-time

KFR write enforces `(who, what, when_period)` uniqueness across the active KFR (entries past expiry can co-exist for historical audit but are excluded from active gate evaluation). Duplicate write attempts → `F-KFR-DUPLICATE-KEY` fail-closed.

```yaml
# Derived at write:
composite_key: sha3_512(canonical(who) + "\0" + canonical(what) + "\0" + canonical(when_period))[:24]
```

### §7.2.2 Leg 2 — deterministic ordering on legitimate historical duplicates

Where historical entries with same composite_key co-exist (e.g., revised value mid-cycle), gate evaluation uses **most-recent `when_as_of`** as the active entry; older entries are accessible only via explicit historical query.

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-KFR-DUPLICATE-KEY` | KFR write attempts to add an entry with `composite_key` matching an existing active entry | MED | PRE-write |

# §8. OPTIONAL-FOLDED closures (cheap; ship at M1)

## §8.1 DC-CF-01 — Derivation runtime-arithmetic-error mapped to failure code (LOW)

v7.0.4 §4.5 derivation grammar admits `/` (divide). `kfr_facts['enrollment_stub_year'].value` may evaluate to 0; division by zero raises `decimal.DivisionByZero` (trapped per §6.2.1 context).

**Closure:** the derivation evaluator catches Decimal traps explicitly and maps them:

| Trap | Failure code |
|---|---|
| `decimal.DivisionByZero` | `F-DERIVATION-RUNTIME-ARITHMETIC-ERROR.divide_by_zero` |
| `decimal.Overflow` | `F-DERIVATION-RUNTIME-ARITHMETIC-ERROR.overflow` |
| `decimal.InvalidOperation` | `F-DERIVATION-RUNTIME-ARITHMETIC-ERROR.invalid_operation` |

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-DERIVATION-RUNTIME-ARITHMETIC-ERROR` | Decimal trap raised during derivation evaluation | LOW (HARD-BLOCK the claim; logged at MEDIUM if recurring) | POST-eval |

## §8.2 CF-RT-06 — Canonical-unit conversion before tolerance comparison (LOW)

v7.0.4 §7.2 value-leg compares `12.5 (thousands USD)` to `12500 (USD)` without unit normalization. Same value, different unit-string, gate silently passes.

**Closure:** Logician `tolerance_check` helpers REQUIRE both sides have matching `unit` strings. Where units are convertible (e.g., `thousands_usd` → `usd` via factor 1000), conversion happens BEFORE comparison, in `KFR_DECIMAL_CONTEXT`. Mismatched non-convertible units → `F-CURRENCY-UNIT-MISMATCH` fail-closed.

Canonical unit map for v0.1 (small set; extensible at M2):

| Canonical unit | Convertible from |
|---|---|
| `usd` | `thousands_usd`×1000, `millions_usd`×1_000_000 |
| `count` | (no conversions) |
| `acres` | `hectares`×2.471, `square_meters`×0.000247 |
| `percentage` | (no conversions; `percentage_points` is the same) |

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-CURRENCY-UNIT-MISMATCH` | Tolerance comparison receives mismatched non-convertible unit strings | LOW (MED at currency type) | PRE-comparison |

## §8.3 DC-CF-05 — Pydantic schema-validation cache key pinned (LOW)

v7.0.4 §1 mandates "Pydantic schema validation runs on every read." Without caching guidance, hot paths drift toward unbounded latency.

**Closure (spec-only):** companion blueprint `pipeline/blueprint/v0.1/section_04_logician.md` at LOCK gains a sub-section pinning the safe cache pattern:

> **KFR Pydantic validation cache key.** Cache parsed-and-validated KFR entries with key `(absolute_path, mtime, size)`. mtime change OR size change OR path change → cache miss → revalidate. No time-based eviction. Memoize for the lifetime of the agent invocation. Cross-invocation persistence forbidden (each agent invocation revalidates from disk on first access).

No new failure code (spec-only edit).

## §8.4 CF-RT-07 — Logfire telemetry of confidential source_quotes (LOW)

v7.0.4 §5 Intake uses Pydantic AI tool calls. The substrate (v7.0.3) includes Logfire by default. Intake operates on Confidential per-org content (`source_quote` may be a proprietary number).

**Closure:** Intake-related tool calls EITHER (a) `LOGFIRE_ENABLED=0` set as an environment variable BEFORE any Intake module import (process-wide policy; closes RT-11 path where late `logfire.disable()` after imports already captured events), OR (b) configure Logfire with a redaction filter that strips `source_quote` and any field declared `classification: confidential` per v7.0.7.

**RT-11 closure — Logfire pre-import discipline.** The Intake subprocess SHALL set `LOGFIRE_ENABLED=0` in its environment before any `import` statement that transitively imports Logfire OR any Pydantic AI module. The CLI entry point for Intake (e.g., `tilth intake bulk-ingest --org <slug>`) is a small wrapper script that:

```python
#!/usr/bin/env python3
# pipeline/cli/tilth_intake.py — Intake CLI entry point
import os
os.environ["LOGFIRE_ENABLED"] = "0"  # MUST be first; before any Pydantic AI / Intake import
# Now safe to import Intake modules
from pipeline.orchestrator.seats.intake import run_intake
# ...
```

Lazy-init pattern: any Logfire-aware module checks the env var at first use (not at import time) and refuses to initialize if `LOGFIRE_ENABLED=0`. AST-lint rule `R-INTAKE-NO-LOGFIRE-IMPORT-BEFORE-ENV` validates that no Intake module imports Logfire before reading the env var.

### §8.4.1 Process-wide Logfire bootstrap shim (Cycle-2 RT-11 closure)

The Cycle-1 RT-11 closure (env-var pre-import + lazy-init) closes direct-import paths but leaves transitive-import bypasses: a shared utility module (e.g., `pipeline.shared_utils`) imported by both Intake and another seat may itself transitively import Logfire BEFORE the Intake CLI's env-var setup runs. Subprocesses spawned by Intake inherit the env var but a Logfire import at module-load time of the subprocess's bootstrap-imports could fire before the subprocess respects the flag.

Closure: process-wide Logfire stub injection BEFORE any other import.

```python
#!/usr/bin/env python3
# pipeline/cli/tilth_intake.py — Intake CLI entry point with bootstrap shim
import sys
import os

# Step 1: set env var BEFORE any import that could touch Logfire transitively
os.environ["LOGFIRE_ENABLED"] = "0"

# Step 2: insert stub module into sys.modules BEFORE any import resolves logfire
class _LogfireDisabledStub:
    """Stub that raises on any attribute access; closes transitive-import path."""
    def __getattr__(self, name):
        raise RuntimeError(
            f"Logfire access denied during Intake (LOGFIRE_ENABLED=0). "
            f"Attempted access: logfire.{name}. Per F-INTAKE-TELEMETRY-LEAK §8.4.1."
        )
    def __setattr__(self, name, value):
        raise RuntimeError(f"Logfire mutation denied during Intake.")

sys.modules["logfire"] = _LogfireDisabledStub()

# Step 3: NOW safe to import Intake. Any transitive `import logfire` resolves to the stub.
from pipeline.orchestrator.seats.intake import run_intake
# ...
```

**Subprocess discipline.** Any subprocess that Intake spawns (e.g., for parallel bulk-ingest) MUST inherit the same bootstrap discipline. Intake's subprocess-launch wrapper:

1. Sets `LOGFIRE_ENABLED=0` in the subprocess environment via `subprocess.Popen(..., env={**os.environ, "LOGFIRE_ENABLED": "0"})`
2. Passes a Python `-c "..."` bootstrap that injects the same `_LogfireDisabledStub` into `sys.modules` BEFORE the actual subprocess work begins

```python
def spawn_intake_subprocess(target_module: str, *args) -> subprocess.Popen:
    bootstrap = (
        "import sys, os; "
        "os.environ['LOGFIRE_ENABLED']='0'; "
        "class _S:\n"
        "    def __getattr__(s,n): raise RuntimeError('logfire denied')\n"
        "sys.modules['logfire']=_S(); "
        f"import {target_module}; {target_module}.main()"
    )
    return subprocess.Popen(
        [sys.executable, "-c", bootstrap, *args],
        env={**os.environ, "LOGFIRE_ENABLED": "0"},
    )
```

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-INTAKE-LOGFIRE-STUB-MISSING` | `sys.modules["logfire"]` is not the `_LogfireDisabledStub` at Intake CLI entry OR at any subprocess entry | HIGH | PRE-Intake-CLI + PRE-subprocess |

Combined with §8.4 env-var-pre-import + lazy-init + AST-lint, the four-layer defense closes direct-import, transitive-import, and subprocess-import paths.

Per Sovereignty Promise + v7.0.7 always-local discipline for Intake, option (a) is the v0.1 default. Option (b) becomes the v0.2+ pattern when telemetry is operationally useful.

| Code | Trigger | Severity | Layer |
|---|---|---|---|
| `F-INTAKE-TELEMETRY-LEAK` | Logfire event emitted during Intake tool-call AND event includes `source_quote` field OR field tagged `confidential` OR `LOGFIRE_ENABLED != "0"` at Intake CLI entry | LOW (advisory; logged at MEDIUM if recurring; HARD-BLOCK at HIGH if endpoint is non-local) | POST-tool-call + PRE-Intake-CLI |

# §9. OPTIONAL-DEFERRED closures (rationale)

## §9.1 DC-CF-03 — AWARD_INGEST failure-code namespace info disclosure (LOW; defer to v0.2)

The namespace `F-EXTRACTOR-AWARD-SIGNATURE-INVALID.{proposal | award}` reveals which leg failed. At v0.1 single-client A1 + A4-trusted-operator, this is bounded — debug aid > attack aid. At Stage-2+ multi-tenant horizon, this becomes a probe oracle.

**Defer rationale:** v0.2 multi-tenant amendment will collapse to single primary-log code with secrets-vault audit channel. Closing at M1 would require introducing a secrets-vault audit substrate that doesn't exist at v0.1 (overhead exceeds the v0.1 attack surface).

**Forward marker:** v0.2 multi-tenant amendment owns this closure.

## §9.2 CF-E-01..06 — Editor clarity-polish (MED×2 + LOW×4; defer to v7.0.4-M2 cosmetic)

Six Editor findings are clarity improvements (schema legibility, INCREMENTAL_INGEST naming, SP0 ergonomics under deadline pressure, tolerance-table layout, cross-amendment composition narrative, substrate alignment). Three of six (CF-E-01, CF-E-03, CF-E-05) are MEDIUM; remainder LOW.

**Defer rationale:** clarity improvements only, not load-bearing for closure of v0.1 Beta gate. Folding into M1 would expand scope beyond the HIGH/P0 corrective intent and risk landing M2-shaped issues at M1 review.

**Forward marker:** v7.0.4-M2 cosmetic amendment at operator discretion when v0.1 Beta is otherwise stable. Editor findings tracked at `pipeline/validation/v7_0_4_thesis_cross_family_2026-05-10/audit_v1_editor.md`.

# §10. New failure-code registry summary (post-Cycle-1)

| Code | Severity | Layer | M1 § | Owner |
|---|---|---|---|---|
| `F-KFR-YAML-CONSTRUCT-FORBIDDEN` | HIGH | PRE-load | §2.4 | KFR YAML loader (covers anchor/alias/merge-key/forbidden-numeric-construct) |
| `F-KFR-CANONICAL-SIGNATURE-INVALID` | HIGH | PRE-load | §2.4 | KFR PRE-gate (replaces v7.0.4 `F-KFR-SIGNATURE-INVALID`) |
| `F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED` | HIGH | PRE-write | §2.6.3 | Legacy migration mode tamper-gate |
| `F-DERIVATION-AST-FORBIDDEN-NODE` | HIGH | PRE-write + POST-read | §3.5 | Derivation AST visitor (covers ast.Index, ast.Slice, float-Constant, dunder-subscript-key) |
| `F-KFR-TAG-MODIFIED` | HIGH | PRE-write | §4.4 | KFR tag-mutation tamper-gate (disk-state SHA3-512 hash comparison per §4.2.1) |
| `F-KFR-PATH-SYMLINK-FORBIDDEN` | HIGH | PRE-load | §4.2.2 | KFR + ledger atomic-read symlink rejection |
| `F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING` | HIGH | POST-check | §5.4 | Benchmark cross-check audit-log gate |
| `F-BENCHMARK-SEEDING-SOURCE-UNAUTHORIZED` | HIGH | PRE-write | §5.4 | SN-LLC seeding allowlist |
| `F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID` | HIGH | PRE-load | §5.2.3 | Allowlist Ed25519 signature gate |
| `F-CURRENCY-FLOAT-IN-COMPARISON` | HIGH | PRE-runtime | §6.4 | Decimal arithmetic helper |
| `F-CURRENCY-CONTEXT-OMITTED` | HIGH | PRE-runtime | §6.2.1 | Decimal helper context-discipline |
| `F-CURRENCY-CONTEXT-MISMATCH` | HIGH | PRE-runtime | §6.2.1 | Decimal helper context-discipline |
| `F-CURRENCY-DECIMAL-CONTEXT-DRIFT` | HIGH | PRE-runtime | §6.2.1 | Decimal helper context-drift guard |
| `F-AWARD-INGEST-ATTN-UNVERIFIED` | MED | PRE-AWARD_INGEST | §7.1 | AWARD_INGEST gate |
| `F-KFR-DUPLICATE-KEY` | MED | PRE-write | §7.2 | KFR composite-key gate |
| `F-DERIVATION-RUNTIME-ARITHMETIC-ERROR` | LOW (HARD-BLOCK claim) | POST-eval | §8.1 | Derivation evaluator |
| `F-CURRENCY-UNIT-MISMATCH` | LOW (MED for currency) | PRE-comparison | §8.2 | Tolerance comparison helper |
| `F-INTAKE-TELEMETRY-LEAK` | LOW (advisory; HIGH if non-local endpoint) | POST-tool-call + PRE-Intake-CLI | §8.4 | Intake Logfire wrapper |
| `F-INTAKE-LOGFIRE-STUB-MISSING` | HIGH | PRE-Intake-CLI + PRE-subprocess | §8.4.1 | Logfire bootstrap shim integrity gate |

Nineteen codes total (one is a renaming + scope-expansion of v7.0.4 `F-KFR-SIGNATURE-INVALID`; eighteen are net-new). Cycle-1 added five codes; Cycle-2 added two codes (`F-KFR-PATH-SYMLINK-FORBIDDEN` per §4.2.2 RT-05 closure; `F-INTAKE-LOGFIRE-STUB-MISSING` per §8.4.1 RT-11 closure). All registered in `pipeline/blueprint/v0.1/section_04_v2_x_amendment.md` §6 (paired-LOCK with §4 v2.x consolidated amendment when WS-L Slice 4 lands).

# §11. Companion file edits at LOCK + WS-L Slice 4 dispatch

The text-level closure ships at M1 LOCK. The paired Cedar/Python predicate work exceeds Cowork scope and is surfaced as **WS-L Slice 4** dispatch at LOCK ceremony.

## §11.1 Companion files at M1 LOCK ceremony (Cowork-authored)

- `pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md` — this file, frontmatter promotes SCOPING DRAFT → LOCKED
- `pipeline/blueprint/v0.1/section_04_v2_x_amendment.md` — §6 row-additive registration of M1 gate family (paired with §4 v2.x at WS-L Slice 4)
- `memory/project_architecture_v7_0_4_M1_locked.md` — memory file
- `MEMORY.md` — index entry prepended at line 1

## §11.2 WS-L Slice 4 dispatch packet (Code-side; surfaced at M1 LOCK)

WS-L Slice 4 implements the Cedar/Python predicate work for M1's twelve gate codes. Slice plan:

- `pipeline/logician/canonicalization/{kfr_canonical.py, kfr_safe_loader.py}` (NEW; ~200-300 LOC)
- `pipeline/logician/derivation/ast_whitelist.py` (NEW; ~150-200 LOC)
- `pipeline/logician/currency/decimal_arithmetic.py` (NEW; ~150 LOC)
- `pipeline/logician/benchmarks/cross_check.py` (UPDATE; replace `==` with `hmac.compare_digest`; add audit-log writer)
- `pipeline/logician/gates/f_kfr_yaml_construct_forbidden.py` (NEW)
- `pipeline/logician/gates/f_kfr_canonical_signature_invalid.py` (NEW; supersedes existing `f_kfr_signature_invalid.py` if present)
- `pipeline/logician/gates/f_derivation_ast_forbidden_node.py` (NEW)
- `pipeline/logician/gates/f_kfr_tag_modified.py` (NEW)
- `pipeline/logician/gates/f_benchmark_cross_check_audit_missing.py` (NEW)
- `pipeline/logician/gates/f_benchmark_seeding_source_unauthorized.py` (NEW)
- `pipeline/logician/gates/f_currency_float_in_comparison.py` (NEW)
- `pipeline/logician/gates/f_award_ingest_attn_unverified.py` (NEW)
- `pipeline/logician/gates/f_kfr_duplicate_key.py` (NEW)
- `pipeline/logician/gates/f_derivation_runtime_arithmetic_error.py` (NEW)
- `pipeline/logician/gates/f_currency_unit_mismatch.py` (NEW)
- `pipeline/logician/gates/f_intake_telemetry_leak.py` (NEW)
- `pipeline/vault/policies/kfr_canonical.cedar` (NEW; canonicalization-discipline policy)
- `pipeline/vault/policies/derivation_ast_whitelist.cedar` (NEW)
- `pipeline/vault/policies/kfr_tag_mutation.cedar` (NEW)
- `pipeline/vault/policies/benchmark_seeding.cedar` (NEW)
- `pipeline/vault/policies/currency_decimal.cedar` (NEW)
- `pipeline/linting/r_currency_no_float_compare.py` (NEW; AST-lint rule)
- `pipeline/linting/r_benchmark_no_short_circuit_compare.py` (NEW; AST-lint rule)
- `tests/logician/canonicalization/test_kfr_canonical_differential.py` (NEW; PyYAML/ruamel/hand-written round-trip)
- `tests/logician/derivation/test_ast_whitelist.py` (NEW; whitelist enforcement; dunder-attack vectors)
- `tests/logician/currency/test_decimal_arithmetic.py` (NEW; tolerance boundary; float input rejection)
- `tests/logician/benchmarks/test_cross_check_constant_time.py` (NEW; timing side-channel discipline; audit-log presence)
- `tests/logician/gates/test_f_*.py` (one per gate; ~12 modules)

Slice 4 estimated scope: ~25 modules + ~150-200 unit tests + 5 Cedar policies. Estimated Code-session wall-clock: 4-6 hours (matches WS-L Slice 1's wall-clock at 7-module scope).

**Slice 4 spec card** lands at LOCK ceremony in `pipeline/handoffs/ws_l_slice_4_m1_corrective_2026-05-10.md` per AGENTS.md compact-handoff discipline.

## §11.3 v7.0.4 amendment text — supersession-pointer markers at LOCK (DC-JG-01 + RT-08 closure)

v7.0.4 amendment text substantive content is NOT modified in place. Two supersession-pointer markers land at M1 LOCK to make the supersession unmissable to any future reader:

### §11.3.1 Top-of-file `[NOTE]` block (DC-JG-01 closure)

A non-breaking `[NOTE]` block prepended to v7.0.4 amendment file IMMEDIATELY AFTER the YAML frontmatter close `---`:

```markdown
> **[NOTE — SUPERSEDED CLAUSES SINCE 2026-05-10]**
>
> Specific clauses of this amendment are SUPERSEDED by **v7.0.4-M1** (LOCKED 2026-05-10). See `pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md` §0.1 for the supersession table.
>
> Superseded clauses include:
> - §1.1 (F-KFR-SIGNATURE-INVALID raw-bytes signing) → M1 §2 canonical-JSON signing + §2.6 legacy migration mode
> - §1 schema YAML constructs admitted → M1 §2.3 anchor/alias/merge-key forbidden
> - §4.5 derivation AST grammar (informal) → M1 §3 explicit AST whitelist
> - §4 currency tolerance arithmetic (no type pin) → M1 §6 Decimal mandate
> - §7.2 F-BENCHMARK-CONTAINS-PER-ORG-REF (boolean oracle) → M1 §5 constant-time + audit-log + signed allowlist
> - §3.2 + §4.4 tamper-gates (no metadata coverage) → M1 §4 tag-mutation gate via disk-hash
>
> v7.0.4 clauses NOT listed remain authoritative.
```

### §11.3.2 Frontmatter footer addendum

YAML frontmatter footer line:

```yaml
m1_supersession: "M1 LOCKED 2026-05-10 row 190 supersedes specific clauses; see architecture_v7_0_4_M1_amendment.md §0.1"
```

### §11.3.3 Companion blueprint pointer discipline

At LOCK, companion blueprint files point to M1 mechanisms:

- v7.0.4 §1.1 `F-KFR-SIGNATURE-INVALID` reference: blueprint companions point to `F-KFR-CANONICAL-SIGNATURE-INVALID` per M1 §2.
- v7.0.4 §4.5 derivation grammar: blueprint companions point to M1 §3 AST whitelist.
- v7.0.4 §7.2 value-leg semantics: blueprint companions point to M1 §5 constant-time + audit-log.
- v7.0.4 §4 currency tolerance arithmetic: blueprint companions point to M1 §6 Decimal mandate.
- v7.0.4 §3.2 NEEDED hard-block: blueprint companions point to M1 §4 ledger-aware re-evaluation.

Both edits are non-breaking (additive markers + footer line + companion pointers); substantive v7.0.4 text unchanged.

## §11.4 Operator-facing impact summary (E-06 closure)

M1 introduces ONE operator-facing UX change beyond v7.0.4. Everything else is internal Logician-discipline tightening that operators do not interact with directly.

| Change | Operator impact | Where |
|---|---|---|
| **AWARD_INGEST `--rationale` flag** | When invoking AWARD_INGEST with the `--attest-unsigned-award-doc` flag (for funders that don't sign awards), the operator MUST also provide `--rationale "<text>"` explaining why the attestation flag is being used. | §7.1 |
| Legacy KFR signature migration | One-time per org at M1 LOCK: operator runs `tilth kfr migrate-signatures --org <slug>` to enable dual-verification mode. Existing pre-M1 KFR files are accepted under their raw-YAML signatures during the migration cycle and re-signed under canonical-JSON format. Auto-disables on completion. | §2.6 |
| Decimal-typed currency in KFR | Existing KFR files with float-typed currency values are auto-coerced to Decimal-string shape during migration cycle. Operator confirms each migration entry at SP0 (audit trail preserved). | §6 |
| Tag-modification re-confirmation prompt | When operator modifies any `required_for_*` tag list, M1 requires admin-risk-ledger entry with rationale; SP0 surfaces the re-confirmation prompt at next sign-out. | §4.2.2 |

All other changes (canonicalization, AST whitelist, audit-log discipline, allowlist signing) are invisible to the operator — Logician PRE/POST gates handle them automatically.

White-glove onboarding playbook updates at M1 LOCK to include the migration-cycle walkthrough.

# §12. What this amendment does NOT do

- Does not modify A1-A12.
- Does not modify v7.0.4 substantive text in place (footer-only addendum at LOCK).
- Does not modify Five Operating Laws or Four Autonomy Rules.
- Does not introduce new council seats or support agents (v7.0.6 roster preserved).
- Does not modify v7.0.5 Funder Intelligence Database / Match DB / Channel G design.
- Does not modify v7.0.7 Beta classification routing or Classification Review stage.
- Does not modify v7.0.8 CIC × CLC orthogonality.
- Does not modify SP0 stop point structural design (M1 §4 only adds the ledger-aware re-evaluation hook).
- Does not modify Intake three-mode dispatch (BULK_INGEST / INCREMENTAL_INGEST / AWARD_INGEST) — M1 §7.1 only adds rationale-required gate to the AWARD_INGEST attestation flag path.
- Does not modify Pydantic AI substrate decision (v7.0.3) — uses substrate primitives.
- Does not introduce new architectural primitives — all M1 mechanisms reuse existing primitives (Logician PRE/POST gates, admin-risk ledger, Ed25519 signatures, Cedar policies, Pydantic schema validation, AST visitor patterns).
- Does not specify v0.2 Data Collector / Report Generator / Archivist interaction with M1 gates (v0.2 amendment territory).
- Does not bump amendment version (v7.0.4-M1 is a corrective; v7.0.5 / v7.0.6 / v7.0.7 / v7.0.8 sequencing preserved).
- Does not address the 4 MED/9 LOW non-HIGH/P0 findings beyond the priority-ordered M1 candidate list at audit_v1_synthesis.md (DC-CF-03 + CF-E-01..06 deferred per §9; remainder folded per §7-§8).

# §13. Lock-history note + sequencing

- v7.0.1 (DRAFT): Section E.P Governance Plan Preflight — awaiting Thesis round
- v7.0.2 (SELF-LOCKED 2026-05-04): Section A textual reconciliation
- v7.0.3 (SELF-LOCKED 2026-05-08): Substrate corrective
- v7.0.4 (LOCKED 2026-05-09 — row 178; cross-family verification CLOSED 2026-05-10 row 181 verdict NEEDS-M1): KFR + SP0 + F-LOGICIAN-FACT-DRIFT + Intake + Benchmarks
- v7.0.5 (LOCKED 2026-05-10 — row 179): Funder Intel + Match DB
- v7.0.6 (SELF-LOCKED 2026-05-09): Roster
- v7.0.7 (LOCKED 2026-05-10 — row 180): Beta classification routing
- v7.0.8 (LOCKED 2026-05-08): CIC × CLC orthogonality
- **v7.0.4-M1 (SCOPING DRAFT 2026-05-10, this file)**: Narrow corrective amendment closing 5 HIGH/P0 + 2 RECOMMENDED + 4 OPTIONAL paths surfaced by 2026-05-10 cross-family verification

**Sequencing.** M1 supersedes specific clauses of v7.0.4. M1 does not modify v7.0.5 / v7.0.6 / v7.0.7 / v7.0.8. M1 unblocks v0.1 Beta deployment (per CLAUDE.md Beta-gate criterion: classification routing + KFR fact-substrate + Intake + Uploader + WS-L Logician realization).

**Thesis-round priorities for v7.0.4-M1 LOCK** (cross-family LIVE — Editor=Llama 3.3 70B/Groq, Judge=Gemini 2.5 Pro/Google, Red Team=GPT-OSS 120B/Groq):

- **Editor pass:** clarity of supersession discipline (which v7.0.4 clauses are superseded; what v7.0.4 readers need to know); legibility of canonicalization spec (§2); legibility of AST whitelist (§3); legibility of Decimal mandate (§6).
- **Judge pass:** rubric scoring against M1's stated goal (close 5 HIGH/P0 paths). Does each closure actually close the path the cross-family verification surfaced? Does the closure introduce new architectural defect? Score per dimension: D1 closure-correctness (do the gates actually close the surfaced paths?), D2 self-consistency, D3 substrate alignment (Pydantic AI + Logician + Ed25519), D4 enforceability (deterministic Python + Cedar fail-closed), D5 completeness (anything missed from the synthesis priority-ordered list?).
- **Red Team pass:** adversarial — does each closure introduce a new evasion surface? Specifically: (1) Can a YAML construct still slip past the canonicalizer? (2) Can the AST whitelist be bypassed via novel attack vectors (`__getattribute__` shadow, generator expressions disguised as comprehensions, decorator chains)? (3) Can the tag-mutation tamper-gate be bypassed via partial-write / file-rename / atomic-replace tricks? (4) Can the constant-time benchmark cross-check leak via memory-allocation timing or audit-log buffering tricks? (5) Can Decimal context manipulation (rounding mode change, precision change) reintroduce IEEE-754-equivalent imprecision?

The Red Team pass on M1 is load-bearing because M1's premise is "the 2026-05-10 cross-family verification surfaced everything"; if Cycle-1 surfaces NEW HIGH/P0 paths beyond the verification's 5, M1 should close those at Cycle-2 or scope-expand at operator escalation.

## §13.1 Thesis round closure (L-005 strict two-cycle — CLOSED 2026-05-10)

**Cycle 1 audit** at `pipeline/validation/v7_0_4_m1_thesis_2026-05-10/audit_v1_synthesis.md` filed 2026-05-10. Three reviewers in parallel via openclaw gateway (osascript bridge from Cowork session). Editor=`groq/llama-3.3-70b-versatile` (Meta) READY_TO_LOCK with 7 LOW/MED clarity findings; Judge=`google/gemini-2.5-pro` (Google) READY_TO_LOCK 99/100 with 1 LOW DC-JG-01 supersession-visibility; Red Team=`groq/openai/gpt-oss-120b` (OpenAI-OSS) ESCALATE blocking:true with 11 HIGH findings (RT-01..RT-11).

**Cycle 1 → Cycle 2 fixes applied (14 distinct fixes producing 5 net-new failure-code entries):**

| Finding | Disposition | Closure landed in |
|---|---|---|
| RT-01 (HIGH) | FOLD | §2.2.2 explicit `<<` key reject + `tag:yaml.org,2002:merge` reject |
| RT-02 (HIGH) | FOLD | §2.2.1 NFC normalization Step 1; differential-test fixture |
| RT-03 (HIGH) | FOLD | §3.2 ast.Index + ast.Slice in forbidden list |
| RT-04 (HIGH) | FOLD | §3.2 subscript-key dunder string-content validation |
| RT-05 (HIGH) | FOLD | §4.2.1 disk-state SHA3-512 hash + inode-change cache invalidation |
| RT-06 (HIGH) | FOLD | §5.2.2 audit-log write-before-compare + dummy-pad + fsync |
| RT-07 (HIGH) | FOLD | §6.2.1 explicit-context-required helper + identity-check + drift-guard |
| RT-08 (HIGH) | FOLD (NEW §2.6) | §2.6 dual-verification migration mode + auto-disable + F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED |
| RT-09 (HIGH) | FOLD | §5.2.3 allowlist Ed25519 signing + F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID |
| RT-10 (HIGH) | FOLD | §3.2 ast.Constant float-type rejection |
| RT-11 (HIGH) | FOLD | §8.4 LOGFIRE_ENABLED=0 pre-import + R-INTAKE-NO-LOGFIRE-IMPORT-BEFORE-ENV |
| DC-JG-01 (LOW) | FOLD | §11.3.1 NOTE block + §11.3.2 frontmatter footer at v7.0.4 file |
| E-01 (MED) | FOLD | §0.1 supersession-table legend |
| E-06 (MED) | FOLD (NEW §11.4) | §11.4 operator-facing impact summary |
| E-02..E-05, E-07 (LOW × 5) | NOTED | non-blocking; preserved as audit-trail record |

**Cycle 2 verification** at `pipeline/validation/v7_0_4_m1_thesis_2026-05-10/audit_v2_synthesis.md` filed 2026-05-10. Editor READY_TO_LOCK (all 7 closed; E-08 self-contradicted severity REJECTED per L-018); Judge READY_TO_LOCK 100/100 ("design now fully upholds its core invariants; exemplary security discipline"); Red Team REQUIRES_FIXES blocking:true with 3 PARTIAL probes — author disposition manifest at LOCK (row-170 transparent pattern):

| Cycle-2 finding | Disposition at LOCK | Rationale |
|---|---|---|
| RT-05 PARTIAL (race / symlink during atomic read) | FOLDED_IN at LOCK | §4.2.2 NEW atomic-read discipline (`fcntl.flock(LOCK_SH)` on org-vault dir FD + `O_NOFOLLOW` + symlink rejection); F-KFR-PATH-SYMLINK-FORBIDDEN |
| RT-10 PARTIAL (integer division yields runtime float) | REJECTED with rationale | Per L-017 trace-verification + L-018 lens-vulnerability: gate firing fail-closed is the gate doing its job, NOT an attack vector. Red Team's "DoS" framing conflates `fail-closed gate` with `attacker can deny service`. Per-capita derivations encode results as Decimal-string-literal-via-Constant per §6.3 (already specified). Workaround documented; no Cycle-2 amendment edit required. Severity downgrade: usability concern, not security defect. Forward marker: v7.0.4-M2 cosmetic worked-example |
| RT-11 PARTIAL (transitive Logfire import / subprocess) | FOLDED_IN at LOCK | §8.4.1 NEW process-wide Logfire bootstrap shim (sys.modules stub injection BEFORE any import + subprocess discipline via env-var inheritance + `-c` bootstrap stub); F-INTAKE-LOGFIRE-STUB-MISSING |
| Editor E-08 (formatting) | REJECTED per L-018 | Severity self-contradicted by Editor's own framing ("minor issue"); HIGH classification misassigned. Non-blocking; deferred to v7.0.4-M2 cosmetic |

**Two Cycle-2 amendment text edits at LOCK** (Red Team's own recommended fixes, transparent disposition matching row-170 / v7.0.5 row 179 / v7.0.7 row 180 / §12 v1 row 182 precedents):

- §4.2.2 KFR + ledger atomic-read discipline (NEW)
- §8.4.1 Process-wide Logfire bootstrap shim (NEW)

**Two Cycle-2 new failure codes registered:** `F-KFR-PATH-SYMLINK-FORBIDDEN` (§4.2.2) + `F-INTAKE-LOGFIRE-STUB-MISSING` (§8.4.1).

**L-005 cycle-cap respected.** Cycle 1: 18 findings; 14 fixes applied. Cycle 2: 3 PARTIAL probes + 1 misclassified Editor finding; 2 FOLDED_IN at LOCK; 2 REJECTED with rationale captured for audit trail. **No silent third audit cycle. No re-dispatch beyond two rounds.**

**Cross-family rigor.** Editor=Llama 3.3 70B/Groq (Meta family) + Judge=Gemini 2.5 Pro/Google + Red Team=GPT-OSS 120B/Groq (OpenAI-OSS family) across both cycles. Three distinct non-Anthropic families. **Section E carve-out NOT invoked** — fourth v0.1 round to LOCK with FULL live cross-family rigor after WS-D v7.0.5 (row 179), WS-F §12 v1 (row 182), WS-E §11 Intake (row 185).

## §13.2 Companion files edited at LOCK

Per dispatch packet done definition + §11.1 + §11.3 + §11.4:

- `pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md` — this file; frontmatter promoted SCOPING DRAFT → LOCKED 2026-05-10; §13.1 + §13.2 filled
- `pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md` — `[NOTE]` block prepended after frontmatter (DC-JG-01 closure) + frontmatter footer `m1_supersession` line added; substantive text unchanged
- `pipeline/validation/v7_0_4_m1_thesis_2026-05-10/{audit_prompt_v{1,2}_*.md, audit_v{1,2}_{editor,judge,red_team}.{md,raw.json}, audit_v{1,2}_synthesis.md, dispatch_audit_v{1,2}.sh, dispatch_audit_v{1,2}_parallel.sh, dispatch_v{1,2}.log}` — full audit trail
- `pipeline/engineering/lock_history.v1.jsonl` — row 190 appended (lock_class=architecture_amendment_M1; parent_lock_row=178; cross_family_posture=LIVE FULL)
- `memory/project_architecture_v7_0_4_M1_locked.md` — memory file written
- `MEMORY.md` — index entry prepended at line 1
- `daily_logs/2026-05-10.md` — WS-C-M1 LOCK entry appended with full self-check
- `pipeline/metrics/session_log.jsonl` — session metrics row appended
- `pipeline/handoffs/ws_l_slice_4_m1_corrective_2026-05-10.md` — Slice 4 spec card pre-staged for Code-side dispatch (paired-Code work for §11.2 modules)

## §13.3 What M1 establishes for future amendments

M1 is the **first cross-family-verification-corrective amendment** — the narrow-corrective pattern for closing HIGH/P0 paths surfaced by a deferred cross-family verification round. The discipline:

1. Cross-family verification on already-LOCKED amendment surfaces NEW findings (NEEDS-M1 verdict)
2. Coordinator dispatches narrow corrective amendment (M1) — DOES NOT modify the LOCKED amendment in place
3. M1 supersedes specific clauses of the parent amendment via §0.1 Supersession table
4. M1 runs full L-005 strict two-cycle Thesis with cross-family rigor
5. M1 LOCKs as a new amendment row in lock_history; parent amendment row stands as historical record
6. Companion blueprint edits at LOCK point to M1 mechanisms; v7.0.4-style narrative reference preserved
7. NOTE block prepended to parent amendment file at LOCK makes supersession unmissable

This pattern is callable for any future amendment LOCKed under Section E carve-out where cross-family verification later surfaces HIGH/P0 paths. Discipline preserves audit-trail integrity AND surfaces gaps that motivated cross-family rigor.
