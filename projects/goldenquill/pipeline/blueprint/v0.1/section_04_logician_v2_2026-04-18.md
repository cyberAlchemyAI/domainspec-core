# Blueprint Section 4 — Logician (v2 LOCKED 2026-04-18)

**Status:** **LOCKED v2 2026-04-18.** Verification round CLOSED unanimous Thesis Team verdict: Editor (meta/llama-3.3-70b) READY_TO_LOCK; Judge (alibaba/qwen3-32b) PASS 100/100; Red Team (openai_oss/gpt-oss-120b) READY_TO_LOCK with both v1 Bucket-A items (A-v1-01 admin-risk ledger race, A-v1-02 claim-evidence version collision) explicitly CLOSED and zero new Bucket-A residuals. Strict L-005 two-audit pass condition met. Parent Section 2 v7 LOCKED 2026-04-18. v3 hardening backlog (19 Bucket-B + 10 Bucket-C, all defence-in-depth or out-of-model under v0.1 trusted-operator) captured at `pipeline/validation/blueprint_section_04_2026-04-17/v3_hardening_backlog.md` for v0.1.x consideration. Audit trail: `pipeline/validation/blueprint_section_04_2026-04-17/`.

**Original v2 draft header preserved below for audit-trail:**

DRAFT v2 — verification audit round. v1 scoping round (2026-04-17) closed with Editor=REQUIRES_MINOR_FIXES, Judge=PASS 97/100, Red Team=REQUIRES_MAJOR_MITIGATIONS (2 Bucket-A CRIT concurrency races). v2 narrow-edits v1 to land the Bucket-A concurrency fixes by calling Section 2 v7 LOCKED primitives (append-CAS, write-if-absent), fold in all four Bucket-B hardening items (B-v1-01..04), and close the four Bucket-C documentation items. Section 2 parent upgraded from v4 LOCKED (2026-04-16) to v7 LOCKED (2026-04-18). v2 pass condition: Editor=READY_TO_LOCK, Judge ≥ 85, Red Team=READY_TO_LOCK with zero Bucket-A AND A-v1-01/A-v1-02 both closed. **Result: all three conditions met.**

**v1 → v2 changelog (narrow edits only):**

1. **Bucket-A closure A-v1-01 (admin-risk ledger race).** §4.7.3 step 7 rewritten to call `vault_write(intent="admin-risk-append", write_mode="append-cas", expected_current_file_hash=<hash-at-step-1>)` per Section 2 v7 §4.10.4 allowlist row 2. Head-update step 8 unchanged (head is single-writer under .write.lock). New §9 property test covers two concurrent POST-gate runs appending to the same ledger under CAS.

2. **Bucket-A closure A-v1-02 (claim-evidence version collision).** §4.5 step 3 rewritten to call `vault_write(intent="claim-evidence-write", write_mode="write-if-absent")` per Section 2 v7 §4.10.4 allowlist row 1 + §4.10.3 kernel-atomic primitive (Linux `renameat2(RENAME_NOREPLACE)` flag `0x01`, macOS `renamex_np(RENAME_EXCL)` flag `0x4`). `F-POST-14.claim_evidence_version_collision` now routes from kernel-atomic `F-VAULT-WRITE-EXISTS` rather than pre-check. New §9 property test covers two concurrent POST-gates racing to write `v{n}.json.unsigned`.

3. **Bucket-B closure B-v1-01 (stale dossier-verify cache).** §8.1 `DOSSIER_VERIFY_CACHE_TTL_MINUTES` set to `0` (cache disabled at v0.1; re-verify every cite). §4.6.5 + §10 amended to note the trade-off (correctness over speed at v0.1 scale).

4. **Bucket-B closure B-v1-02 (sentence-tokenizer abbreviation bypass).** §4.6.1 amended: operator-configurable extension list at `orgs/{slug}/vault/config/abbreviation_list.yaml` (M15-signed); on first-pass tokenizer miss, fall back to a full-text search of the cited file before declaring UNSOURCED (`verify_method = "grep_fulltext_fallback"`). §8.2 carries the base list unchanged; extension list is runtime-loaded.

5. **Bucket-B closure B-v1-03 (property test for F-BT10-03).** §9.6 extended with a property test: random oversized source files (> `BT10_MAX_FILE_BYTES`) always trigger `F-BT10-03.source_file_too_large`; never silent truncation; never partial grep.

6. **Bucket-B closure B-v1-04 (explicit failure sub-tags).** §6.1 adds `F-PRE-21.pre_gate_timeout` and `F-PRE-22.post_gate_timeout` inline (no longer §10 follow-ups). §6.10 adds `F-BT13-03.rigor_breach_unacknowledged_at_signing` inline with explicit trigger condition at §4.9 step 5.

7. **Bucket-C closures (documentation).** §4.5.1 + §4.9 extended with key-rotation operator-facing note (C-v1-01). §10 F-OQ-01 closed ("v0.1 English-only; non-English is v0.2 candidate"). §10 F-OQ-02 closed ("v0.1 ships with string-overlap only; semantic similarity stays OFF by default"). §10 F-OQ-03 moved to "deferred to Section 5 blueprint" per ARCH scope.

8. **Parent Section 2 pointer updated** from v4 LOCKED to v7 LOCKED (2026-04-18) throughout (§5 upstream interfaces, §5.2 vault-write interface signature, §10 ARCH-06 closure note).

**Parent architecture:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` (v5-r8). **Parent Section 2:** `pipeline/blueprint/v0.1/section_02_vault_topology.md` (LOCKED v7 2026-04-18). **Parent Section 3:** `pipeline/blueprint/v0.1/section_03_scout.md` (LOCKED v5).

**Trust model:** trusted-operator single-client-per-Golden-Quill (A1–A4 carried from Sections 1 and 2). Same-uid hostile Python, hostile third-party libraries, multi-tenant shared hardware, and hostile operator are OUT-OF-MODEL per Section 1 trusted-operator envelope and Section O of the architecture. Attacks requiring these preconditions are labelled OUT-OF-MODEL in §10 / §12 and are not defended at v0.1.

**What Section 4 does NOT own** (summary — full list in §12):
- Vault filesystem enforcement (Section 2 M14 family).
- Scout health-tuple **generation** (Section 3 — Section 4 only **verifies** the HMAC per M7).
- Scribe drafting, Editor clarity review, Judge scoring (Section 5 pipeline loop).
- Pipeline orchestration, provider rate limiting, revision-loop cap mechanics (Section 5).
- HMAC key lifecycle (Section 1 BT6 — Section 4 consumes `sign_*` / `verify_*` primitives).
- RFA re-fetch and re-hash at draft time (Section 5 calls Section 1 `reverify_rfa`; Section 4 only enforces hash-match at PRE-gate).
- Cedar policy **authoring** (operator authors; Section 4 loads + evaluates).

---

## 1. Purpose and scope containment

### 1.1 Statement of purpose

Section 4 implements Tilth's fifth seat, the Logician — the deterministic Python + Cedar fail-closed enforcement layer that guards the council output and the operator sign-off surface. Logician is the HOW of architecture D.5 (Logician role expansion), the PRE/POST gate discipline (Section J revision loop cap excluded — Logician does not consume revisions), all Five Operating Laws and all Four Autonomy Rules as enforcement obligations at exactly two pipeline gates, the claim-evidence map (BT7), DOC_SOURCED grep windowing (BT10), cross-org dossier reference policy (BT11), USER_DATA conversation-anchor integrity (BT9), health-tuple signature **verification** (M7), admin-risk ledger monotonicity (M8), per-org key scoping enforcement (M9), dossier lock verification (M11 / S11c) at cite-time, vault access gating (M14 / M15), operator final-review gate (L-001), and rails-report signing (BT13).

Logician is the last deterministic line between the council's LLM-generated output and the operator's sign-off. Every mechanism it owns is Python + Cedar; no LLM calls; no network calls except through Section 2 Vault-owned skills; no side effects outside of append-only signed logs and atomic sign-overwrite writes through the Vault write primitive.

### 1.2 Scope containment — what Section 4 owns

Section 4 owns the PRE-gate that runs before any drafting begins, the POST-gate that runs after Judge completes, the claim-evidence map pipeline (generation + atomic sign-overwrite + operator sign-off + cite-time verification), the conversation log (append-only signed per BT9), the source-tag verification engine (BT10 windowed grep + fallback + UNSOURCED resolution path routing), the cross-org dossier reference policy (BT11 secondary-confirmation gate), the admin-risk ledger writer and monotonicity checker (M8), the per-org BYOK key scoping enforcer (M9), the dossier lock verification at cite-time (M11 / S11c three-part check: canonical path, inode, content-hash), the rails-report signer (BT13), the Cedar policy loader and evaluator (M14 / M15), and the operator final-review gate (L-001 verify-gate precedent honoured).

All of these are deterministic. None involves an LLM. All fail closed. None can be overridden by a prompt, skill, or model.

### 1.3 Scope containment — what Section 4 does NOT own

Explicit non-ownership list (full version in §12; this is the summary):

- Vault filesystem enforcement (M14 vault-substrate, canonical-path + inode binding at write time, bind-mount namespace, O_NOFOLLOW discipline): **Section 2**. Logician consumes Section 2's `vault_read` / `vault_write` / `fd_broker` surfaces; it does not reimplement them.
- Scout health-tuple **generation** (Channel A–F per-channel OK/DEGRADED/FAILED enumeration, signed canonical-JSON assembly, `run_entropy` derivation, feed-level reason-tags): **Section 3**. Section 4 **verifies** the HMAC signature produced by Section 3 using the Section 1 `verify_health_tuple` primitive.
- Scribe drafting, Editor clarity review, Judge scoring, loop iteration counting, three-iteration revision cap (Section J of architecture): **Section 5 Pipeline**. Section 4 runs at the two gates bracketing this loop; it does not intervene inside it.
- Pipeline orchestration (`router.py`, `pipeline.py`), provider rate-limiting (BT5), cron scheduling, three-tab delivery mechanics: **Section 5 Pipeline**.
- HMAC key lifecycle — per-session HMAC key rotation (BT6), key material zeroization at session end, optional HSM path (BT4): **Section 1 Sovereignty Envelope**. Section 4 calls `sign_*` and `verify_*` primitives; it does not hold key material directly.
- RFA ingest and dual-hash (M1): **Section 1 primitive `dual_hash_rfa`** invoked by **Section 5** at ingest. Section 4 enforces dual-hash presence + validity at PRE-gate only.
- Cedar policy authoring: **operator**. Section 4 loads policy files (signed + M15-committed per M15.3), evaluates them against Cedar entity shapes, and returns ALLOW / DENY. Logician does not write policy text.
- Entity dossier **construction** (M11 / D.0 Entity Research Pass, source fetching, per-entity confidence tiering, S11a/b/c domain allowlist + cross-domain diversity gates at dossier-write time): **Section 3 Scout**. Section 4 enforces S11c dossier lock at **cite time** — three-part check that the dossier cited by a DOC_SOURCED claim is still the operator-signed artifact.
- Draft storage, draft versioning, revision-loop state persistence, interrupted-state checkpoints: **Section 2 Vault Topology** (storage) + **Section 5 Pipeline** (lifecycle).
- Provider fallback cascade: Scout's internal Ollama → Groq → Anthropic cascade is **Section 3**; council seat fallback (Section E M5 cross-family rigor + M10/M13 graceful degradation) is **Section 5**.
- Channel F BT12 pre-flight and per-org jurisdiction policy: **Section 3 Scout** (`channel_f_websearch.py`). Section 4 reads the per-session Channel F disclosure log that Scout emits and includes it in the BT13 rails report, but does not enforce the pre-flight itself.

### 1.4 Threat model boundary

Section 4 operates inside the Section 1 trusted-operator envelope (A1–A4, confirmed operator 2026-04-17):
- **A1.** v0.1 ships single-client-per-Golden-Quill.
- **A2.** Operator dev environments may run multi-client under trusted-operator assumption.
- **A3.** Multi-client-on-shared-hardware is v2 product scope, not v0.1.
- **A4.** Operator is trusted.

Under this envelope, the following attack classes are OUT-OF-MODEL for Section 4 at v0.1 and are not defended — they are marked OUT-OF-MODEL wherever they would otherwise surface in §9 test vectors or §10 open questions:

- Compromise of the operator's keyring (rejected per architecture O.2 — the operator's keyring IS the trust boundary at v0.1).
- Hostile third-party library or compromised Python interpreter (same-process attackers inside the same-uid perimeter are out-of-model per A4).
- Hostile OS kernel or privileged attacker (out-of-model per architecture O.3).
- Multi-tenant cross-org timing observability (out-of-model per architecture O.4 / A1 / A3).
- Physical seizure of the Golden Quill.
- Hostile operator.

In-model attacks Section 4 DOES defend at v0.1:

- Path trickery / symlink plant against DOC_SOURCED citation paths (closed via M12 whitelist + canonical path + inode).
- Signature fabrication on claim-evidence map, rails report, conversation log, admin-risk ledger (closed via operator-signed hash chain with keyring verification).
- Non-monotonic or duplicate admin-risk ledger `seq_id` (closed via M8 monotonicity check).
- Per-org BYOK key mis-scope (closed via M9 per-org key-binding check).
- Unsourced claim shipment (closed via Law 5 / S9 PRE-gate and POST-gate hard-blocks).
- Dossier symlink bypass of operator sign-off (closed via S11c three-part cite-time check).
- Post-delivery edit of rails report or claim-evidence map (closed via BT7 / BT13 atomic sign-overwrite; signature invalidates on edit).
- Missing PROJECT_CONTEXT.md `[NEEDED]` substance tokens (closed via corpus-completeness PRE-gate check per Law 1 + Law 5).
- Mid-loop Logician call attempt (closed via strict call-site wiring in Section 5; attempt is PRE-gate violation and aborts run).

### 1.5 Gate positioning precedent — L-001

Architecture L-001 (Scout VERIFY precedent, 2026-04-14 EPA NEETP-26 round) established that verification happens at elevation, not at discovery. Section 4 honours the analogue at council-output elevation: Logician's POST-gate runs after Judge completes and before the draft reaches the operator. There is no "candidate shipped" state that bypasses the POST-gate. VERIFY wins over DISCOVER (S6); analogously, Logician's POST-gate wins over the inner-loop happy path — a draft that scores high on Judge but fails the POST-gate is blocked, never shipped.

---

## 2. Data structures (frozen, signed, field-documented)

All Section 4 data structures are `@dataclass(frozen=True, kw_only=True)` or Cedar entity shapes. Every signed artifact is canonicalised to JSON with sorted keys and UTF-8 bytes before hashing/signing, matching Section 3 §2's canonicalization discipline. Byte-identical serialisation is an invariant (see §7.5).

### 2.1 `ClaimEvidenceMap`

Atomic unit produced at POST-gate. Every factual claim in the draft gets exactly one `ClaimEntry`. Map is signed with the operator keyring (same keyring as M15 signed-commits).

```python
@dataclass(frozen=True, kw_only=True)
class ClaimEntry:
    claim_id: str              # sha3_512(canonical_json({draft_hash, draft_offset, claim_text}))[:24]
    draft_offset: int          # byte offset in draft where claim begins (for operator-side highlighting)
    claim_text: str            # the factual statement extracted by Section 5 claim extractor
    tag: str                   # "DOC_SOURCED" | "USER_DATA" | "UNSOURCED"
    source_ref: SourceRef | None  # None iff tag == "UNSOURCED"
    verify_method: str         # "grep_windowed_pm2" | "grep_windowed_pm5_fallback" |
                               # "conversation_anchor" | "unresolved"
    verify_result: str         # "PASS" | "FAIL"
    verify_detail: str         # human-readable detail; for FAIL includes grep string tried,
                               # source path canonicalized, window size attempted
    rigor_breach_flag: bool    # True iff this claim was drafted under an active M13 bypass
                               # (rails report carries the same flag with bypass_authorization_id)

@dataclass(frozen=True, kw_only=True)
class SourceRef:
    source_kind: str           # "RFA" | "PROJECT_CONTEXT" | "ENTITY_DOSSIER" |
                               # "RUBRIC_LIBRARY" | "LESSONS" | "CONVERSATION_LOG"
    canonical_path: str        # Section 1 canonical_path output, rooted inside M12 whitelist
    inode: int                 # os.stat(canonical_path).st_ino bound at PRE-gate ingestion
    content_hash: str          # sha3_512 of file content as it was at ingestion
    grep_string: str | None    # None for USER_DATA; else the ±N-sentence windowed quote
                               # that verify_method used
    window_size_sentences: int | None  # 2 (default), 5 (fallback), or None for USER_DATA

@dataclass(frozen=True, kw_only=True)
class ClaimEvidenceMap:
    map_id: str                # sha3_512(canonical_json({draft_hash, rfa_hash, session_id}))[:24]
    draft_hash: str            # sha3_512(draft_bytes)
    rfa_hash: str              # M1 content_hash of the RFA this draft responds to
    session_id: str            # Section 1 session binding
    org_slug: str              # session-bound org (Law 3 / M2 binding)
    rfa_url_hash: str          # M1 url_hash (recorded alongside content_hash for audit)
    entries: tuple[ClaimEntry, ...]
    unsourced_count: int       # convenience: count of entries where tag == "UNSOURCED"
    hard_block_count: int      # convenience: count of 🔴 admin-risk flags unresolved
    rigor_breach_active: bool  # True iff any M13 review-seat bypass is active for this draft
    generated_at_utc: str      # ISO-8601 UTC timestamp, microsecond precision
    generator_version: str     # Section 4 blueprint lock tag, e.g. "s4-v1" — supports schema migration
```

Serialization: the `entries` tuple is sorted by `claim_id` ascending before canonicalization; this guarantees byte-identical re-generation (see §7.5).

### 2.2 `SignedClaimEvidenceMap`

The triple that lands on disk per BT7 atomic sign-overwrite.

```python
@dataclass(frozen=True, kw_only=True)
class SignedClaimEvidenceMap:
    map: ClaimEvidenceMap
    content_hash: str          # sha3_512 of canonical_json(map) bytes
    signature: bytes           # operator-keyring signature over content_hash (Ed25519 default;
                               # BT4 HSM path swappable at the primitive level)
    operator_key_id: str       # keyring key identifier — supports key rotation audit
    signed_at_utc: str         # ISO-8601 UTC timestamp when operator signed
```

On-disk layout: one file per version, written atomically via Section 2 `vault_write` at `orgs/{slug}/vault/claim_evidence/{rfa_hash}/v{n}.json`. The `n` is assigned by Section 5 as the draft version at the time the POST-gate ran; Section 4 does not allocate version numbers.

### 2.3 `SignedRailsReport`

BT13 output delivered to the operator alongside the claim-evidence map and the lessons delta.

```python
@dataclass(frozen=True, kw_only=True)
class RailsReport:
    report_id: str             # sha3_512(canonical_json({map_id, generated_at_utc}))[:24]
    map_id: str                # pointer to the claim-evidence map this report accompanies
    rfa_hash: str
    draft_hash: str
    session_id: str
    org_slug: str
    judge_score: JudgeScoreSummary
    admin_risk_flags: tuple[AdminRiskFlagEntry, ...]     # batched 🔴 / 🟡 / 🟢
    structural_findings: tuple[StructuralFinding, ...]   # word count / section presence / budget
    source_tag_summary: SourceTagSummary                 # counts by tag + list of UNSOURCED claim_ids
    per_channel_health: tuple[ChannelHealthEntry, ...]   # Scout health tuple consumed at PRE-gate
    channel_f_disclosures: tuple[ChannelFFetchEntry, ...]  # Scout's per-session Channel F log
    rigor_breach_flags: tuple[RigorBreachFlag, ...]      # active M13 bypass authorizations
    degradation_log_entries: tuple[DegradationLogEntry, ...]  # M10 author-seat graceful degradations
    lessons_delta: tuple[LessonDeltaEntry, ...]          # new lessons surfaced this run
    generated_at_utc: str

@dataclass(frozen=True, kw_only=True)
class SignedRailsReport:
    report: RailsReport
    content_hash: str
    signature: bytes           # Logician session-key signature (NOT operator-keyring — see §4.8)
    logician_session_key_id: str
    signed_at_utc: str
```

Critical signing-key distinction:
- `SignedClaimEvidenceMap.signature` is an **operator-keyring** signature. Only the operator can produce it; it is the operator's final-review sign-off.
- `SignedRailsReport.signature` is a **Logician per-session HMAC** signature per BT6. Logician produces it immediately before delivery; post-delivery edit invalidates it.

This matters because the claim-evidence map is the operator's attestation (Law 5 / L-001 final-review gate), while the rails report is Logician's attestation (BT13 integrity of the scoring/health/breach artifact). Different trust roots; different signatures; different failure modes.

### 2.4 `AdminRiskLedgerEntry`

M8 append-only ledger entry. Every flagged term, operator substitution decision, HIGH-severity register addition, review-seat bypass authorization, and tamper event writes exactly one entry.

```python
@dataclass(frozen=True, kw_only=True)
class AdminRiskLedgerEntry:
    seq_id: int                # monotonically increasing across the org's ledger lifetime
                               # (see §4.7.3 for monotonicity enforcement)
    utc_timestamp: str         # ISO-8601 UTC, microsecond precision
    org_slug: str              # per-org ledger (Law 3 / M2 / M9)
    entry_kind: str            # "FLAG_TERM" | "SUBSTITUTION_DECISION" |
                               # "REGISTER_ADDITION" | "BYPASS_AUTHORIZATION" |
                               # "TAMPER_EVENT" | "CORPUS_INCOMPLETE"
    term: str | None           # the flagged term; None for BYPASS_AUTHORIZATION and TAMPER_EVENT
    severity: str              # "HARD_BLOCK" | "MEMOED" | "PRECAUTIONARY" | "HIGH" | "INFO"
                               # color semantics: 🔴 = HARD_BLOCK, 🟡 = MEMOED, 🟢 = PRECAUTIONARY
    operator_decision: str | None    # "APPROVED" | "REJECTED" | "DEFERRED" | None (INFO entries)
    draft_version_ref: str | None    # e.g. "v3" — points to Section 5 draft version
    rails_report_hash: str | None    # pointer to SignedRailsReport.content_hash if any
    operator_retype_confirmed: bool  # True iff HIGH-severity add was re-type confirmed at add time
    prev_entry_hash: str       # sha3_512 of prior entry's canonical_json — hash-chained
    entry_hash: str            # sha3_512(canonical_json of this entry with entry_hash="")
    operator_signature: bytes | None  # operator-keyring signature over entry_hash, required for
                                      # entry_kind in {"REGISTER_ADDITION", "BYPASS_AUTHORIZATION",
                                      # "SUBSTITUTION_DECISION"}; None for automated entries
```

Hash-chain discipline: each entry's `prev_entry_hash` is the previous entry's `entry_hash`. Ledger head tracked at `orgs/{slug}/vault/admin_risk/head.json` (atomic update via Section 2 `vault_write`). Verification walks the chain from head backwards; any broken link or replayed entry aborts at PRE-gate.

### 2.5 `ConversationLogEntry` (BT9)

USER_DATA trust-root anchor. Append-only signed log; per-session log signed by Logician-issued session key (BT6 lifecycle).

```python
@dataclass(frozen=True, kw_only=True)
class ConversationLogEntry:
    seq_id: int                # monotonic within session
    utc_timestamp: str
    session_id: str
    org_slug: str
    speaker: str               # "operator" | "scribe" | "scout" | "editor" | "judge" | "logician"
                               # (Section 4 only accepts entries from Section 5 orchestrator write-path;
                               # speaker tag is for audit, not auth)
    content: str               # exact utterance or message
    content_hash: str          # sha3_512 of content bytes
    prev_entry_hash: str
    entry_hash: str
    session_key_signature: bytes  # Logician session key, BT6 rotation applies
```

`USER_DATA` claims in the claim-evidence map cite a `ConversationLogEntry.entry_hash` via `SourceRef.grep_string = None` and `SourceRef.canonical_path` pointing to the conversation log path under `orgs/{slug}/vault/conversations/{session_id}.jsonl`. Logician verifies:
1. The log file signature chain is intact from head back to the cited entry.
2. The cited entry's `content` matches the claim (exact substring, case-insensitive on operator policy; default case-sensitive).
3. The entry's `session_key_signature` verifies under the session's BT6-active key.

### 2.6 Cedar entity shapes

Section 4 evaluates Cedar policy against these entity types at PRE-gate (vault access gating) and at cite-time (dossier verification, cross-org reference policy).

```cedar
entity Session = {
  session_id: String,
  org_slug: String,
  org_root_hash: String,
  byok_key_id: String,
  started_at_utc: String
};

entity VaultPath = {
  canonical_path: String,
  inode: Long,
  volume_uuid: String,
  org_slug_hint: String,      // extracted from path; authoritative check is canonical_path vs org_root
  is_shared: Bool             // True iff path is under vault_shared/
};

entity Claim = {
  claim_id: String,
  tag: String,                // "DOC_SOURCED" | "USER_DATA" | "UNSOURCED"
  source_kind: String,
  cross_org_dossier: Bool     // BT11 flag
};

entity OperatorKeyringKey = {
  key_id: String,
  bound_org_slug: String      // M9 per-org key scoping
};
```

The Cedar `org_isolation` policy (authored by operator, signed + M15-committed, evaluated by Section 4) uses these entities. Section 4 does not extend or author Cedar schemas at runtime.

### 2.7 `HealthTupleVerifyResult`

Return of `verify_scout_health_tuple()` at PRE-gate. Consumes Section 3's canonical-JSON signed tuple shape.

```python
@dataclass(frozen=True, kw_only=True)
class HealthTupleVerifyResult:
    status: str                # "VERIFIED" | "UNKNOWN" | "INVALID_SIGNATURE" | "MALFORMED"
    per_channel: dict[str, str]  # {"A": "OK" | "DEGRADED" | "FAILED" | "NOT_OPTED_IN", ...}
                                 # Section 3 v5 guarantees NOT_OPTED_IN is three-state proper
                                 # (ARCH-03 acknowledged; muddied-signal limitation in §10 F-OQ-11)
    hard_abort: bool           # True iff (all Channel A endpoints FAILED) OR (≥4/6 families FAILED)
                               # OR status != "VERIFIED"
    degradation_flags: tuple[str, ...]  # channel families flagged DEGRADED for operator digest
    raw_tuple_hash: str
```

### 2.8 `PreGateContext` / `PostGateContext`

Aggregated inputs bound at gate entry. Frozen and canonicalised; hash recorded in the entry admin-risk ledger entry (entry_kind = "INFO" via Section 1 `record_admin_risk` helper with severity = "INFO").

```python
@dataclass(frozen=True, kw_only=True)
class PreGateContext:
    session: Session
    rfa_hash: str
    rfa_url_hash: str
    project_context_hash: str
    project_context_needed_fields: tuple[str, ...]  # empty tuple iff corpus complete
    health_tuple: SignedHealthTuple                  # from Section 3
    dossier_refs: tuple[DossierRef, ...]             # entity dossiers referenced for this grant
    entered_at_utc: str

@dataclass(frozen=True, kw_only=True)
class PostGateContext:
    pre_gate_context: PreGateContext
    draft_hash: str
    draft_version: int
    judge_score: JudgeScoreSummary
    editor_readiness: str       # Section 5 Editor seat output, e.g. "READY" | "NEEDS_REVISION"
    admin_risk_terms_found: tuple[AdminRiskTermMatch, ...]
    structural_findings: tuple[StructuralFinding, ...]
    entered_at_utc: str
```

### 2.9 On-disk layout — Section-4-owned paths

Every path below is a `vault_write` view owned by Section 4 per architecture N.2 Section 2 → Section 4 interface list. Section 4 never `open()`s these paths directly.

| Path under `orgs/{slug}/vault/` | Owner | Write discipline |
|---|---|---|
| `claim_evidence/{rfa_hash}/v{n}.json` | Section 4 | BT7 atomic sign-overwrite via `vault_write(intent="claim-evidence-write")` |
| `rails/{rfa_hash}/v{n}.json` | Section 4 | BT13 signed, atomic via `vault_write(intent="rails-report-write")` |
| `conversations/{session_id}.jsonl` | Section 4 | BT9 append-only signed via `vault_write(intent="conversation-append")` |
| `admin_risk/ledger.jsonl` | Section 4 | M8 hash-chained append-only via `vault_write(intent="admin-risk-append")` |
| `admin_risk/head.json` | Section 4 | M8 head-pointer atomic replace via `vault_write(intent="admin-risk-head-update")` |
| `degradation_log/entries.jsonl` | Section 1 primitive invoked by Section 4 | BT8 hash-chained append-only via `record_degradation()` |
| `dossier_verify_cache/{entity_slug}.json` | Section 4 | Cite-time S11c verification cache, per-session TTL, via `vault_write(intent="dossier-verify-cache")` |
| `operator_signoff/{rfa_hash}/v{n}.sig` | Section 4 | Operator's final-review signature artifact; written when operator runs `tilth review --sign` |

The degradation log (`BT8`) is owned physically by Section 1's `degradation_log.py` primitive per architecture BT8; Section 4 is the author of M10/M13 entries but the storage primitive is Section 1's. The distinction matters because the hash-chain writer is shared with Scout's degradation entries (per-channel DEGRADED flags) — one writer, two writers' worth of entries, one chain.

---

## 3. Module inventory

Nine modules under `pipeline/logician/`. No module depends on any sibling module by more than its narrow public API. All imports from Sections 1, 2, and 3 flow through published surfaces (see §5).

| # | Path | Purpose | Owns |
|---|------|---------|------|
| 1 | `pipeline/logician/__init__.py` | Package re-exports and version | Public surface |
| 2 | `pipeline/logician/gates/pre_gate.py` | PRE-gate check sequence — runs before any drafting | Per-check FAIL action, ordered evaluation, abort semantics |
| 3 | `pipeline/logician/gates/post_gate.py` | POST-gate check sequence — batches all flags + generates map | Claim extraction routing, batch classification, POST artifact assembly |
| 4 | `pipeline/logician/gates/gate_runner.py` | Orchestrates PRE → [silent loop] → POST sequence | Wire-up to Section 5 orchestrator entry points; silent-loop invariant |
| 5 | `pipeline/logician/claim_evidence.py` | BT7 atomic sign-overwrite of claim-evidence map | Generate, canonicalise, operator-sign flow, Vault write |
| 6 | `pipeline/logician/source_tag_verify.py` | BT10 DOC_SOURCED grep windowing + fallback + UNSOURCED routing | Window-size primitive, sentence tokenization rules, path whitelist (M12) check, canonical path + inode binding |
| 7 | `pipeline/logician/conversation_log.py` | BT9 append-only signed log for USER_DATA anchors | Append, session-key-sign, chain verify on read |
| 8 | `pipeline/logician/dossier_verify.py` | S11c dossier lock cite-time verification + BT11 cross-org policy | Three-part check (path, inode, content-hash), cross-org flag injection |
| 9 | `pipeline/logician/admin_risk.py` | M8 ledger writer + monotonicity checker + 🔴/🟡/🟢 classification | Ledger head management, hash-chain verify, per-kind entry assembly |
| 10 | `pipeline/logician/rails_report.py` | BT13 signed rails report assembly + delivery | Aggregate Scout health, per-channel disclosures, rigor-breach flags, Judge score |
| 11 | `pipeline/logician/cedar_eval.py` | Cedar policy load + evaluation for `org_isolation` and M14/M15 gates | Policy-file signature verify, evaluation call surface |

(Counter to §3's "nine modules" header — the inventory is eleven modules once `__init__.py` and `cedar_eval.py` are named; "nine" is the functional module count under the two gate-module split. Header and table are reconciled at §12.1.)

### 3.1 Module dependency constraints

Every Section 4 module imports from only these sources:
- Python standard library (stdlib only; no `requests`, no `httpx`, no async-network libraries).
- `cryptography` (Ed25519, HMAC, SHA-3 — same primitives Section 1 exposes).
- `cedar` or equivalent authorised Cedar library (pinned by operator).
- Published surfaces from Section 1, Section 2, Section 3 (see §5.1–§5.3).
- Other Section 4 modules via their published `__all__`.

No Section 4 module imports an LLM client library. This is enforced at lint-time by a Section 5 AST rule (filed as ARCH-NN candidate — see §10) analogous to Section 3's §7.16 AST-rule pattern. The rule rejects any import of provider SDKs (`anthropic`, `openai`, `groq`, `google.generativeai`, `ollama`) from under `pipeline/logician/`. Until that AST rule lands, Section 4 modules are manually audited at lock-time for the violation.

### 3.2 Why 11 and not fewer

Each of the 11 responsibilities has distinct failure semantics. Collapsing `claim_evidence.py` and `rails_report.py` into one "post-gate artifacts" module would force two different signing keys (operator keyring vs Logician session key) into one module and one code path — a known-bad pattern for cryptographic discipline. Splitting `pre_gate.py` and `post_gate.py` preserves the silent-mid-loop invariant: each file can be audited independently for the invariant that it runs at exactly one gate. `gate_runner.py` is a thin orchestrator because the invariant "Logician runs exactly at PRE and exactly at POST, never in between" is easier to verify in a narrow module than distributed across gate files.

### 3.3 Why 11 and not more

`source_tag_verify.py` could plausibly be split into `doc_sourced_grep.py`, `user_data_anchor.py`, and `unsourced_router.py`. It is kept as one module because the three branches share the M12 whitelist check, the canonical path + inode binding, and the windowed-sentence tokenizer. Splitting would duplicate those helpers or introduce a fourth "shared primitives" module.

`admin_risk.py` could split ledger writing from 🔴/🟡/🟢 classification. It is kept together because the classification feeds the ledger entry kind field, and splitting would create a circular import.

---

## 4. Mechanisms

### 4.1 Gate architecture — PRE and POST only

Logician operates at exactly two pipeline gates. It does NOT interrupt mid-loop. The revision loop cap (3 iterations max per Section J of architecture) applies to the Scout → Scribe → Editor → Judge inner loop; Logician does not consume a revision iteration.

```
OPERATOR SUBMITS RFA + PROJECT_CONTEXT
        │
        ▼
┌───────────────────┐
│   PRE-GATE (§4.2) │  ← Logician runs here. Hard-blocks or passes.
└───────────────────┘
        │ PASS
        ▼
  Scout (Section 3 VERIFY + REVIEW)
        │
        ▼
  Scribe Phase 1 → Editor → Judge
        │                    ▲
        ▼                    │
  Scribe Phase 2 → Editor → Judge   [NO LOGICIAN INTERRUPTIONS]
        │                    │
        ▼                    │
  Scribe Phase 3 → Editor → Judge
        │
        ▼  (revision loop cap reached OR Judge PASS)
┌───────────────────┐
│  POST-GATE (§4.4) │  ← Logician runs here. Batches ALL flags.
└───────────────────┘
        │
        ▼
  Claim-evidence map + rails report + lessons delta delivered to operator
  Operator reviews batch, approves/rejects, signs off (§4.9)
```

**Invariants bound to this architecture:**
1. Logician executes exactly zero times per run with `gate_runner.py` not invoked by Section 5. The PRE/POST invocations are explicit Section 5 call-sites; no other entry point exists.
2. Within the Scribe–Editor–Judge loop, no Section 4 module is imported or invoked. This is a Section 5 wiring invariant; Section 4 enforces it indirectly via §4.2's rejection of any mid-loop-originated call (see §4.2.3).
3. PRE-gate FAIL aborts the pipeline before any council LLM call is issued. No tokens consumed, no provider rate-limit consumed, no partial state written.
4. POST-gate runs exactly once per completed draft. If the draft is re-drafted after operator rejects the POST result, a NEW POST-gate invocation occurs on the new draft version — not a continuation of the prior one.

**Cost posture:** PRE-gate + POST-gate are zero-token by construction. The architecture's "zero token cost" commitment for Logician is realised here.

### 4.2 PRE-gate — what runs before any drafting begins

Logician PRE-gate executes the check sequence in §4.2.1 in strict order. Any FAIL aborts the pipeline immediately with the corresponding `F-PRE-*` reason-tag (see §6.1). All checks are deterministic (Python + Cedar). No LLM calls. No network calls except through Section 2 `vault_read` with declared `intent` values enumerated in §5.2.

#### 4.2.1 PRE-gate check order

Order matters: each check in the list below must pass before the next runs. Earlier checks establish preconditions for later checks (e.g., Cedar policy can't be evaluated before the Cedar policy file's signature has been verified).

| # | Check | Architecture ref | FAIL action / reason-tag |
|---|---|---|---|
| 1 | Section 2 lock marker present + operator-signed + M15-committed | N.4.1 / N.4.2 | Hard abort — `F-PRE-01.section_2_lock_missing` / `.section_2_lock_unsigned` / `.section_2_lock_ledger_mismatch` |
| 2 | `router.yaml` signature valid against operator keyring | S5 | Hard abort — `F-PRE-02.router_yaml_unsigned` / `.router_yaml_signature_invalid` |
| 3 | `vault_shared/` seed files signatures valid | M15 | Hard abort — `F-PRE-03.vault_shared_seed_unsigned` (lists offending paths in detail) |
| 4 | Cedar policy files signature + M15 ledger entry | M15.3 | Hard abort — `F-PRE-04.cedar_policy_unsigned` / `.cedar_policy_ledger_mismatch` |
| 5 | Process-wrapper hash + signature valid | M14.4.4 | Hard abort — `F-PRE-05.wrapper_hash_mismatch` / `.wrapper_signature_invalid` |
| 6 | Logician trust-root mirror signature + `(st_dev, st_ino)` match | N.4.2 / v5-r8 γ | Hard abort — `F-PRE-06.trust_root_unsigned` / `.trust_root_inode_mismatch` / `.trust_root_mount_over_detected` |
| 7 | RFA dual-hash (`url_hash` + `content_hash`) valid and signed | M1 | Hard abort — `F-PRE-07.rfa_hash_missing` / `.rfa_hash_invalid` / `.rfa_unsigned` |
| 8 | SESSION org-root hash bound; `PROJECT_CONTEXT.md` hash matches bound org | M2 | Hard abort — `F-PRE-08.session_unbound` / `.project_context_org_mismatch` |
| 9 | BYOK key scoped to session org | M9 | Hard abort — `F-PRE-09.byok_key_wrong_org` / `.byok_key_missing` |
| 10 | Admin-risk ledger `seq_id` monotonic and no duplicate `seq_id`; hash chain intact | M8 | Hard abort — `F-PRE-10.admin_risk_non_monotonic` / `.admin_risk_chain_break` / `.admin_risk_replayed_seq_id` |
| 11 | Per-seat `rlimits` (RLIMIT_CORE=0, stdio null) inherited from wrapper | M14.4.1 / M14.4.2 | Hard abort — `F-PRE-11.rlimit_core_nonzero` / `.stdio_not_null` |
| 12 | Scout health tuple HMAC valid (Logician-issued session key) | M7 | `UNKNOWN` → hard abort — `F-PRE-12.health_tuple_malformed` / `.health_tuple_signature_invalid` / `.health_tuple_abort_threshold_reached` |
| 13 | Vault subtree filesystem exposes stable volume UUID | BT14(g.1) | Hard abort — `F-PRE-13.volume_uuid_absent` |
| 14 | Entity dossiers: operator sign-off hash present for all DOC_SOURCED entities | M11 / S11c | Hard abort if unsigned dossier cited — `F-PRE-14.dossier_unsigned` (lists offending entity slugs) |
| 15 | Corpus completeness: `PROJECT_CONTEXT.md` contains zero `[NEEDED]` tokens | Law 5 / Law 1 | Hard abort — `F-PRE-15.corpus_incomplete` (operator-facing message lists every unfilled field) |
| 16 | No interrupted-state checkpoint has unresolved UNSOURCED claims | §4.2.4 | Hard abort — `F-PRE-16.interrupted_unsourced_unresolved` (pre-run condition, not mid-loop) |
| 17 | Cedar `org_isolation` policy loads and compiles | M14 | Hard abort — `F-PRE-17.cedar_policy_compile_error` |
| 18 | Section 3 Scout PRE-VERIFY health (from Section 3's own §4.10 `start_scout_run`) signed and intact | Section 3 M7 | Hard abort — `F-PRE-18.scout_pre_verify_unsigned` |

All eighteen checks are explicitly enumerated here. Adding a nineteenth check is a Section 4 blueprint amendment, not a quiet insertion at implementation time.

#### 4.2.2 Corpus completeness rationale

A `[NEEDED]` token in `PROJECT_CONTEXT.md` is a missing substance token — an EIN, UEI, address, production metric, or qualifying fact that Scribe cannot fabricate per Law 5. If Scout and Scribe run against a PROJECT_CONTEXT containing `[NEEDED]`, the pipeline either hallucinates the missing value (fabrication, Law 5 violation), or produces a draft with an unresolved placeholder (waste of API budget and un-shippable). Both outcomes are worse than blocking pre-run.

Making corpus completeness a hard PRE-gate check converts an implicit convention into deterministic enforcement: no corpus, no pipeline. The operator-facing message on FAIL must list every unfilled `[NEEDED]` field by name, grouped by PROJECT_CONTEXT section, so the operator knows exactly what to supply before re-running. Token-match is a regex `r"\[NEEDED\]"` case-sensitive (per §8); match count > 0 → FAIL.

#### 4.2.3 Mid-loop call rejection

If any Section 4 gate module is invoked during the Scribe–Editor–Judge loop (not from Section 5's gate-runner call-site), it treats that invocation as a PRE-gate violation and aborts the partial run with `F-PRE-19.logician_mid_loop_call`. Section 5's orchestrator enforces this by routing Scribe output only to Editor and then Judge before Logician sees anything. The belt-and-suspenders is:
1. Section 5 orchestrator never calls Section 4 mid-loop (primary enforcement).
2. Section 4 `gate_runner.py` records the current gate state (`PRE` | `BETWEEN` | `POST` | `DONE`) in a module-local variable set at gate entry and cleared at gate exit; any PRE or POST invocation while state == `BETWEEN` raises `F-PRE-19` (secondary enforcement).
3. Section 4 AST-lint check (ARCH-NN candidate — §10) rejects any `from pipeline.logician ...` or `import pipeline.logician` under `pipeline/pipeline/loop/` (the planned Section 5 inner-loop module tree).

Defence-in-depth aligns with Section 3's §7.16 pattern of runtime + AST layers.

#### 4.2.4 Interrupted-state resume policy

If the pipeline is resuming from an Autonomy Rule 1 interrupted-state checkpoint, the checkpoint's state may include a partial draft with claims that were already tagged UNSOURCED at the prior run's POST-gate but not resolved. PRE-gate check #16 walks the checkpoint's claim-evidence map (if present) and rejects resume if any UNSOURCED claim lacks a resolution-path record (operator removal, queue-route, new source, or USER_DATA statement per §4.4.1). This prevents silent resume of a blocked run.

If no prior claim-evidence map exists on the checkpoint (the run was interrupted before POST-gate ever ran), check #16 passes by construction.

### 4.3 Mid-loop — Logician is silent

During the Scout → Scribe → Editor → Judge loop, Logician:
- Does NOT receive Scribe drafts for claim checking.
- Does NOT receive Editor output for term scanning.
- Does NOT interrupt for admin-risk term detections.
- Does NOT interrupt for word count violations.
- Does NOT interrupt for structural compliance failures.
- Does NOT interrupt for DOC_SOURCED source-tag failures.
- Does NOT emit any admin-risk ledger entry except in the single edge case §4.3.1.

#### 4.3.1 Sole permitted mid-loop write: rigor-breach flag persistence

If Section 5 activates an M13 review-seat bypass mid-loop (because all compliant review-seat families have been FAILED for `max_review_outage_hours`), the bypass authorization writes a `BYPASS_AUTHORIZATION` entry to the admin-risk ledger at activation time (Section 5 calls `admin_risk.record_bypass_authorization()`). This is the only Section 4 code path invoked mid-loop. It is write-only, operator-signed at activation, and does not interrupt the loop.

The distinction: this is the operator pre-authorizing a rigor breach, not Logician enforcing anything. The enforcement happens at POST-gate where the rails report's `rigor_breach_flags` carry the bypass authorization ID and the operator must explicitly acknowledge at sign-off.

#### 4.3.2 Rationale — why silent

Interrupting at mid-loop creates a robotic-micromanager dynamic where the operator is reduced to clicking approve/reject on a stream of micro-tasks per iteration. All of those checks are deterministic and can be batched. The operator's attention is worth more than real-time compliance reporting.

This is not a performance claim; it is a product claim. If Logician interrupted for every detected admin-risk term or every grep-fail, the operator would develop a click-through reflex that defeats the point of the ceremony. Batching the review at POST-gate preserves the ceremony.

### 4.4 POST-gate — claim-evidence map and batched flags

After Judge completes (Section 5 signals `draft_ready_for_post_gate`), the pipeline passes the full draft to Logician POST-gate. Logician runs all checks that were suppressed during the loop, batches them, and produces the claim-evidence map, rails report, and lessons delta in one pass.

#### 4.4.1 POST-gate check sequence

| # | Check | Architecture ref | FAIL action / reason-tag |
|---|---|---|---|
| 1 | Section 5 draft-ready signal is present and signed | Section 5 | Hard abort — `F-POST-01.draft_not_ready` / `.draft_signal_unsigned` |
| 2 | Re-verify PRE-gate invariants still hold (mirror, Cedar policy, M15, RFA hash) | §4.2.1 subset | Hard abort — `F-POST-02.pre_invariant_drift` (lists drifted check) |
| 3 | Extract claims from draft (invoke Section 5 claim extractor, receive frozen tuple) | Section 5 | Hard abort — `F-POST-03.claim_extraction_failed` |
| 4 | For each claim, run source-tag verification (§4.6 BT10) | S9 / BT10 / M12 | Classify each claim DOC_SOURCED / USER_DATA / UNSOURCED; hard-block on any unresolved UNSOURCED |
| 5 | For each DOC_SOURCED claim citing an entity dossier, run S11c three-part lock verify (§4.7-BT11) | S11c / M11 | Reclassify UNSOURCED on failure; flag cross-org dossier citations (BT11) |
| 6 | Admin-risk term scan (Law 4) — batch into 🔴 / 🟡 / 🟢 | Law 4 / S2 / M8 | Hard-block on unresolved 🔴 after Section 5 one-shot Scribe rewrite (§4.4.3) |
| 7 | Structural compliance (word count, required sections, budget lines, matching fund) | Section 5 rubric | Route failures to Section 5 micro-recovery; batch findings into rails report |
| 8 | Rigor-breach flag enumeration — any active M13 bypass? | M10 / M13 / BT13 | Inject into rails report `rigor_breach_flags`; no block |
| 9 | Assemble `ClaimEvidenceMap` (§2.1); canonicalise; hash; prepare for operator sign | BT7 | n/a — artifact produced |
| 10 | Assemble `RailsReport` (§2.3); canonicalise; Logician-session-key-sign | BT13 | n/a — artifact produced |
| 11 | Assemble lessons delta from this run's surfaced lessons | Section I / lessons.md | n/a — artifact produced |
| 12 | Write all three artifacts atomically via Section 2 `vault_write` | BT7 / BT13 / BT9 | Hard abort — `F-POST-12.vault_write_failed` (rolls back partial artifacts) |
| 13 | Signal Section 5 "POST-gate produced — awaiting operator sign" | Section 5 | n/a — state transition |

The operator-final-review gate (§4.9) happens AFTER POST-gate produces its artifacts. POST-gate does not block on operator sign-off; it produces the artifacts and parks them.

#### 4.4.2 UNSOURCED resolution paths at POST-gate

For every claim classified UNSOURCED (either at step 4 grep-fail or step 5 dossier-fail), the operator has exactly four resolution paths:

1. **Operator removes the claim from the draft.** The draft re-enters Section 5 revision loop with the claim excised; a new POST-gate runs on the edited draft. Revision iteration count increments.
2. **Operator converts the claim to a `needs_confirmation/` queue item.** Scribe re-runs that section with an explicit operator-question artifact; counts as one revision iteration. The queue lives at `orgs/{slug}/vault/needs_confirmation/{rfa_hash}/` per Section 2 subtree enumeration; Section 4 writes the queue entry via `vault_write(intent="needs-confirmation-enqueue")`.
3. **Operator adds a supporting source to the project folder.** A file drop under `orgs/{slug}/materials/` (M12 whitelist root) that contains a grep-matching quote for the claim. On re-run, BT10 re-verifies and the claim reclassifies DOC_SOURCED.
4. **Operator states the fact directly in session.** The statement lands in the conversation log (BT9) under the current session's log. On re-run, the claim reclassifies USER_DATA via the conversation anchor (§4.6.4).

No fifth path exists. A claim that cannot be resolved by any of these four paths cannot ship. This is the hard floor of Law 5 (Applicant Brings the Substance).

#### 4.4.3 Admin-risk term classification and Scribe one-shot rewrite

At POST-gate step 6, the term scanner reads the admin-risk register (`pipeline/institutional_memory/admin_risk_register.yaml`, signed + M15-committed) and walks the draft token-by-token looking for matching terms. Matches classify as:

- **🔴 HARD_BLOCK** (`severity: HARD_BLOCK` in register): pipeline cannot ship without operator substitution approval. Logician proposes 2–3 alternatives per blocked term, drawn from the register's `alternatives` field.
- **🟡 MEMOED** (`severity: MEMOED`): flagged, logged, auto-approved. Operator sees in rails report; no action required.
- **🟢 PRECAUTIONARY** (`severity: PRECAUTIONARY`): flagged, logged, auto-approved. Operator sees in rails report; no action required.

For each 🔴 match, Section 5 MAY invoke Scribe once per Law 4 / Section 5 micro-recovery with the proposed alternatives in the prompt. If Scribe's rewrite still contains any 🔴 terms (same or different), the flag escalates to operator and the draft is blocked at POST-gate step 6. The one-shot-rewrite budget is per-draft, not per-term; Section 5 tracks this.

Operator reviews ALL 🔴 flags in one batch screen before sign-off — not per-iteration, not per-term as they arise. This is the operator-attention preservation discipline (§4.3.2).

#### 4.4.4 What POST-gate produces

1. **`SignedClaimEvidenceMap`** — every claim + tag + source pointer, signed by the operator keyring at sign-off time (§4.9). Until operator signs, the map exists but is not a `SignedClaimEvidenceMap` — it is a `ClaimEvidenceMap` awaiting signature.
2. **`SignedRailsReport`** — scores, all flags (batched), per-channel Scout health, sovereignty disclosures (Channel F domain fetches per session), source-tag summary, rigor-breach flags, evidence trail — signed by Logician's per-session key (BT13).
3. **Lessons delta** — any new lesson entries surfaced by this run, formatted for `lessons.md` append. Written via Section 2 `vault_write(intent="lessons-delta-append")` to `pipeline/institutional_memory/pending_lessons.jsonl`; Section 5 delivery tab renders for operator.

Operator sees all three tabs. Signs off on the claim-evidence map before the pipeline marks the draft "shipped."

### 4.5 Claim-evidence map (BT7) — atomic sign-overwrite

The BT7 pattern is five steps. Steps 1–3 happen at POST-gate (§4.4.1 step 9); steps 4–5 happen at operator sign-off (§4.9).

```
1. (POST-gate) Generate ClaimEvidenceMap (claim list + tags + source pointers)
2. (POST-gate) canonical_json(map) bytes → sha3_512 → content_hash
3. (POST-gate) Write (map, content_hash) tuple atomically via Section 2 vault_write
   under orgs/{slug}/vault/claim_evidence/{rfa_hash}/v{n}.json.unsigned
   USING write_mode="write-if-absent" — Section 2 v7 §4.10.4 allowlist row 1 +
   §4.10.3 kernel-atomic primitive (Linux renameat2(RENAME_NOREPLACE) flag 0x01;
   macOS renamex_np(RENAME_EXCL) flag 0x4). Two concurrent POST-gates for the
   same draft_version cannot both succeed; the second receives kernel EEXIST
   surfaced as F-VAULT-WRITE-EXISTS, which Section 4 maps to
   F-POST-14.claim_evidence_version_collision (§6.5).

4. (operator sign-off) Operator runs `tilth review --sign` (Section 5 CLI).
   Operator reads the map, decides to sign, keyring retrieval happens through
   Section 1 keystore, signature over content_hash is produced.

5. (operator sign-off) Write (map, content_hash, signature, key_id, signed_at_utc)
   triple atomically via Section 2 vault_write under
   orgs/{slug}/vault/claim_evidence/{rfa_hash}/v{n}.json — replacing the .unsigned
   file atomically. Uses write_mode="overwrite" because the path now points to a
   different filename (the signed v{n}.json, not the .unsigned variant). The
   .unsigned file is left for archival (per §4.5.1 rejection-path discipline).
```

The `.unsigned` intermediate exists so that an operator who decides NOT to sign (rejects the draft) leaves a traceable artifact. Rejected maps are archived by Section 5 under `orgs/{slug}/vault/claim_evidence/{rfa_hash}/rejected/v{n}.unsigned.json` with an operator-signed rejection note written to the admin-risk ledger.

Post-generation modification invalidates the signature: any byte change in the `map` field breaks `content_hash`; any `content_hash` change breaks the signature. Verification at cite-time (if a downstream consumer reads a prior signed map — e.g., the institutional memory learner) re-hashes and re-verifies; fail → treat as UNSOURCED.

#### 4.5.1 Version-number provenance

The `v{n}` is assigned by Section 5 as the draft version at the time the POST-gate ran. Section 4 does not allocate version numbers; it consumes `draft_version` from `PostGateContext`. If Section 5 produces two drafts for the same `rfa_hash` with `draft_version = 3`, that is a Section 5 bug (filed as ARCH-NN candidate in §10 if encountered); Section 4 rejects the second write at `vault_write` collision time with `F-POST-14.claim_evidence_version_collision`.

#### 4.5.2 Keyring binding

The operator signature in `SignedClaimEvidenceMap.signature` is produced by the operator's keyring (Section 1 `keys.py` retrieves the private key material; Section 4 never sees raw private key bytes). The keyring key ID is recorded in `operator_key_id` — this supports key rotation: a prior signed map still verifies under its historical key because the key ID points into Section 1's key-retirement catalogue (BT6 lifecycle; retired keys are retained for verification but not used for new signs).

BT4 switch: if the operator has opted into HSM-backed keyring, the signing call routes through the HSM primitive transparently. Section 4 does not know which backend is in use; it only sees the signature output.

**v2 keyring-rotation operator-facing note (closes C-v1-01):** if the operator's keyring has rotated between POST-gate generation (when the unsigned map was written and `operator_key_id_advisory` was recorded as the then-active key) and `tilth review --sign` invocation (which retrieves the now-active key from the keyring), the sign-off CLI MUST display both the recorded advisory key id and the current keyring key id and require the operator to confirm "I intended to sign with key id `<current>`" before proceeding. Section 1 key-retirement catalogue retains the prior key for verification but never for new signs. This prevents an unintended cross-rotation sign without forcing the operator to remember which key was active at draft time.

### 4.6 DOC_SOURCED grep windowing (BT10)

BT10 requires windowed grep verification of DOC_SOURCED claims against cited files. The window-size default is ±2 sentences of surrounding context; configurable per-project via `orgs/{slug}/vault/config/bt10_window.yaml` (signed + M15-committed if overriding default).

#### 4.6.1 Sentence tokenization

Default tokenizer: a deterministic regex-based sentence splitter (no NLP library, no ML). Sentence boundaries are:
- `.` followed by whitespace + uppercase letter or paragraph break.
- `?` or `!` followed by whitespace.
- Paragraph breaks (`\n\n` or more).

Abbreviation handling (v2 — closes B-v1-02): a two-tier list. Tier 1 is the fixed base list of English abbreviations (`Mr.`, `Dr.`, `Prof.`, `Inc.`, `Ltd.`, `Co.`, `etc.`, `vs.`, `e.g.`, `i.e.`, `U.S.`, `U.K.`), pinned verbatim in §8.2 and not runtime-modifiable. Tier 2 is an operator-configurable extension list at `orgs/{slug}/vault/config/abbreviation_list.yaml`, M15-signed per Section 2 discipline; loaded at PRE-gate, merged with the base list, cached for the run. Extension entries have no override power — they can only ADD to the carved-out set, never remove base entries.

Full-text fallback: if the windowed-grep pass (§4.6.2) fails to locate the claim's grep string `g` in any sentence window AND both the ±2 and ±5 windows miss, Section 4 runs a final full-file substring search on the raw file bytes (no tokenization) before declaring UNSOURCED. If the full-text search finds `g`, the verify succeeds with `verify_method = "grep_fulltext_fallback"` and a BT10 rails-report note: "claim located via full-text fallback — tokenizer likely missed a sentence boundary; consider adding surrounding abbreviations to `abbreviation_list.yaml`". This prevents a tokenizer bug from silently marking a well-sourced claim UNSOURCED. The fallback runs only when both windowed passes miss — it does not displace windowed-grep as the authoritative source of `verify_method`.

Non-English drafts: out-of-scope for v0.1. Operator confirmation 2026-04-17: all v0.1 drafts are English. Filed as an architectural scope boundary — see §12.

#### 4.6.2 Window primitive

Given a claim `c` and a cited file `f` with canonical path inside the M12 whitelist:
1. Load `f` via Section 2 `vault_read(path=f, intent="doc-sourced-verify-read", session_id=..., slug=...)`.
2. Tokenize `f.content` into sentences per §4.6.1.
3. Tokenize `c.claim_text` into sentences; use the first full sentence as the grep string `g` (if `c.claim_text` has no sentence terminator, use the full text).
4. Find the sentence index `i` in `f.content` where `g` first appears as a substring (case-sensitive by default; case-insensitive opt-in per `bt10_window.yaml`).
5. If `i` exists: the window is sentences `[max(0, i-2), min(len(f.sentences), i+3)]`. Verify PASS.
6. If `i` does not exist: run fallback — same search with window `[max(0, i-5), min(len(f.sentences), i+6)]`. If found → PASS with `verify_method = "grep_windowed_pm5_fallback"`. If still not found → UNSOURCED with `verify_method = "unresolved"`.
7. Optional semantic similarity: if operator has enabled local embedding primitive (default off per §8.3), compute cosine similarity between claim and candidate paragraph; threshold 0.75. When enabled, a similarity pass backs up the grep result (both must agree); when disabled, grep-only is authoritative.

The window size has architectural teeth: it prevents a claim from citing a sentence in one section of the source while the actual context (caveats, disclaimers, qualifiers) lives in another section. A ±2 window catches the common case; ±5 catches the long-discussion case. Beyond ±5 is treated as "the source does not actually support this claim in context" and classifies UNSOURCED.

#### 4.6.3 M12 source-directory whitelist

Every DOC_SOURCED claim MUST cite a file whose canonical path (Section 1 `canonical_path` primitive) resolves under one of these directory roots, and only these roots:
- `rfa/` — ingested RFA and funder program-page captures for the active session.
- `orgs/{session_slug}/` — applicant materials for the session-bound org only, EXCLUDING `orgs/{session_slug}/vault/cached/` (Scout cache is not a DOC_SOURCED root).
- `orgs/{session_slug}/dossier/entities/` — M11-produced signed entity dossiers for the session-bound org only.
- `pipeline/rubrics/` — funder rubric library (read-only shared).
- `pipeline/institutional_memory/` — `lessons.md` / `lessons.json` (read-only shared).

Any path outside these roots is UNSOURCED even if the grep string matches. Symlinks into these roots are rejected — Section 4 calls `os.lstat()` on each intermediate path component during canonicalization; any `S_IFLNK` in the chain fails the check with `F-POST-04.symlink_in_source_path`.

Inode binding: at PRE-gate, for each DOC_SOURCED source cited in the ingest pass, Section 4 records `(canonical_path, inode, content_hash)` in the `SourceRef` and binds these to the claim's tag. At POST-gate, the claim's source is re-opened and re-stat()ed; inode mismatch (indicating file replacement) → UNSOURCED with `F-POST-04.inode_drift`.

#### 4.6.4 USER_DATA anchor verification

USER_DATA claims cite a conversation log entry (§2.5) via:
- `SourceRef.source_kind = "CONVERSATION_LOG"`.
- `SourceRef.canonical_path = "orgs/{slug}/vault/conversations/{session_id}.jsonl"`.
- `SourceRef.grep_string = claim_text` (exact substring).
- `SourceRef.window_size_sentences = None`.
- The claim's `verify_method = "conversation_anchor"`.

Logician verifies:
1. The log file exists at the cited path (via Section 2 `vault_read(intent="conversation-log-verify-read")`).
2. The log's signature chain is intact from head back to the entry whose `content` contains `claim_text` as a substring.
3. The session key that signed that entry was active during the current session (BT6 session-key catalog lookup via Section 1).
4. No later log entry supersedes or corrects the cited one (superseding is a Section 5 convention: an explicit `{"corrects": "<prior_entry_hash>"}` field in the new entry's metadata).

Fail any of (1)–(4) → UNSOURCED with `F-POST-05.conversation_anchor_invalid` and per-case sub-tag.

#### 4.6.5 UNSOURCED hard block

At POST-gate step 4/5, any claim that ends up UNSOURCED with `verify_method = "unresolved"` hard-blocks the draft. The `ClaimEvidenceMap.unsourced_count > 0` invariant at step 9 means the map carries an unresolved-UNSOURCED list and POST-gate step 12 writes the map but refuses to produce the operator-sign-off prompt. Section 5 delivery tab renders the UNSOURCED list and surfaces the four resolution paths (§4.4.2); operator acts; re-run.

### 4.7 Admin-risk ledger (M8, Law 4)

M8 enforces monotonic sequence IDs, hash-chained entries, append-only writes, and per-entry operator signatures on specific entry kinds.

#### 4.7.1 Per-org ledger scope

Each org's ledger is separate per Law 3 / M2 / M9. Ledger path: `orgs/{slug}/vault/admin_risk/ledger.jsonl`. Head pointer at `orgs/{slug}/vault/admin_risk/head.json`. Cross-org reads of another org's ledger are rejected by the Cedar `org_isolation` gate at Section 2 `vault_read` time — a session bound to org-slug A cannot even request org-slug B's ledger path.

#### 4.7.2 Entry kinds and severity taxonomy

| `entry_kind` | When written | `severity` values | Requires operator signature? | Requires re-type confirmation? |
|---|---|---|---|---|
| `FLAG_TERM` | POST-gate step 6 on each term match | HARD_BLOCK / MEMOED / PRECAUTIONARY | No (automated) | No |
| `SUBSTITUTION_DECISION` | Operator approves/rejects/defers a 🔴 substitution at sign-off | HARD_BLOCK | Yes | No |
| `REGISTER_ADDITION` | Operator adds a new term to the admin-risk register | HIGH / HARD_BLOCK / MEMOED / PRECAUTIONARY | Yes | Yes iff severity in {HIGH, HARD_BLOCK} |
| `BYPASS_AUTHORIZATION` | M13 review-seat bypass activated by operator | HIGH | Yes | Yes |
| `TAMPER_EVENT` | Trust-root mirror mismatch, inode drift on a source, Cedar policy unsigned, etc. | HIGH | No (automated) | No |
| `CORPUS_INCOMPLETE` | PRE-gate check #15 FAIL | INFO | No (automated) | No |

The 🔴 / 🟡 / 🟢 display emoji map to severities as: HARD_BLOCK = 🔴, MEMOED = 🟡, PRECAUTIONARY = 🟢. HIGH and INFO are not visualized with emoji (they are register-level or diagnostic, not term-level).

#### 4.7.3 Monotonicity enforcement (v2 — CAS-based, closes A-v1-01)

At ledger-append time (called from any code path above), Section 4:
1. Reads current ledger.jsonl atomically via Section 2 `vault_read(intent="admin-risk-ledger-read")` AND records `current_ledger_hash = sha3_512(file_bytes)` at the same read. (The sha is computed inside the same vault_read response so it is consistent with the bytes the read returned.)
2. Reads current head.json atomically via Section 2 `vault_read(intent="admin-risk-head-read")`.
3. Verifies head.json signature (per-session HMAC via Section 1).
4. Computes `candidate_seq_id = head.max_seq_id + 1`.
5. Loads prior `entry_hash` from head (chain continuation).
6. Constructs the new `AdminRiskLedgerEntry` with `seq_id = candidate_seq_id`, `prev_entry_hash = prior_entry_hash`, `entry_hash = sha3_512(canonical_json(entry with entry_hash=""))`.
7. If entry requires operator signature (per §4.7.2), routes to operator-keyring signing (Section 5 CLI prompt if interactive; pre-signed bundle if batch).
8. Atomic-appends to ledger.jsonl via `vault_write(intent="admin-risk-append", write_mode="append-cas", expected_current_file_hash=current_ledger_hash)` — Section 2 v7 §4.10.4 allowlist row 2 + §4.10.2 CAS primitive. The vault hashes the file inside `.write.lock` and compares against `expected_current_file_hash`; mismatch → `F-VAULT-CAS-HEAD-MISMATCH`, which Section 4 maps to `F-PRE-10.admin_risk_cas_head_mismatch` and re-runs steps 1-8 up to `ADMIN_RISK_LEDGER_APPEND_RETRY_MAX = 3` (§8.1) times. CAS guarantees that two concurrent POST-gate runs cannot both append at `seq_id = N`; the loser observes a stale `expected_current_file_hash` and retries with the fresh head.
9. Atomic-replaces head.json with `{max_seq_id: candidate_seq_id, head_entry_hash: entry_hash, updated_at_utc: ...}` via `vault_write(intent="admin-risk-head-update", write_mode="overwrite")`. Head update is single-writer under the same `.write.lock` cycle as step 8 (Section 2 v7 §4.10.1 lock semantics) — no race window between ledger commit and head commit.

At PRE-gate check #10, Section 4 walks the ledger from head backwards, verifying at each entry:
- `seq_id` is strictly monotonic decreasing (since walking backwards).
- `entry_hash` matches the recomputed hash.
- `prev_entry_hash` matches the predecessor's `entry_hash`.
- No two entries share a `seq_id`.

Any violation → hard abort with `F-PRE-10.admin_risk_*` sub-tag.

#### 4.7.4 HIGH-severity re-type confirmation

Per S2 and §4.7.2, `REGISTER_ADDITION` with severity HIGH or HARD_BLOCK, and every `BYPASS_AUTHORIZATION`, requires the operator to re-type a confirmation phrase at add time (not at POST-gate scan time). Section 5 CLI prompts; Section 4 records the confirmation phrase hash in the ledger entry's metadata. This prevents an operator who is click-through-approving from silently promoting a PRECAUTIONARY term to HARD_BLOCK.

#### 4.7.5 Rate limits (BT3)

Per-org rate limits on low-severity ledger additions are Section 1 BT3's responsibility (the ledger primitive itself is Section 1 per BT3 owner column). Section 4 invokes `record_admin_risk()` and receives `rate_limit_exceeded` errors from Section 1; on rate-limit FAIL, Section 4 reports `F-POST-06.admin_risk_rate_limit_exceeded` in the rails report and batches the overflow for next-run delivery.

### 4.8 Rails report signing (BT13)

Final rails report is signed by Logician's per-session HMAC key (BT6 lifecycle) before delivery to operator. The distinction from BT7 (operator-keyring signature on claim-evidence map) is deliberate: BT13 is Logician attesting that the rails artifact it produced is intact; BT7 is the operator attesting to the map's contents.

#### 4.8.1 What the rails report contains

Per `RailsReport` schema (§2.3):
- Judge score summary (from Section 5 Judge seat).
- Admin-risk flags batched (all 🔴 / 🟡 / 🟢 with operator decisions where applicable).
- Structural findings (word count, section presence, budget lines, matching fund statement).
- Source-tag summary: counts by tag + list of UNSOURCED claim_ids + M13 rigor-breach claims.
- Per-channel Scout health consumed at PRE-gate (`A`/`B`/`C`/`D`/`E`/`F` tuple).
- Channel F disclosures: per-session fetch log Scout emitted under `orgs/{slug}/vault/run_log/{run_id}.channel_f.jsonl` — Section 4 walks this log and folds entries into the rails report so the operator has one place to review outbound-call disclosures per Section A sovereignty posture.
- Rigor-breach flags: every active M13 bypass authorization with `bypass_authorization_id`, bypassed seat, active duration, and operator acknowledgment pointer.
- Degradation log entries: M10 author-seat graceful degradations from this run (Scribe fell back to a non-preferred provider; Editor ran with rigor-breach-flag; etc.).
- Lessons delta: new lessons surfaced.

#### 4.8.2 Signing and delivery

At POST-gate step 10:
1. Canonicalise `RailsReport` per §2.
2. `content_hash = sha3_512(canonical_bytes)`.
3. `signature = hmac_sha3_512(logician_session_key, content_hash)` via Section 1 `hmac_sha3_512` primitive.
4. Record `logician_session_key_id` (for verification + rotation audit).
5. Write `SignedRailsReport` atomically via `vault_write(intent="rails-report-write")` to `orgs/{slug}/vault/rails/{rfa_hash}/v{n}.json`.

Post-delivery edit invalidates the signature: any byte change in the `report` field breaks `content_hash`; any `content_hash` change breaks the HMAC. Verification at any subsequent read re-hashes and re-HMACs; mismatch → the report is treated as tampered, and Section 4 raises `F-POST-07.rails_report_tampered` + writes a TAMPER_EVENT ledger entry.

#### 4.8.3 Rigor-breach flag prominence

Rigor-breach flags are rendered first in the rails report (Section 5 delivery tab convention). Operator cannot ship a draft produced under an M13 bypass without explicitly acknowledging the flag at sign-off (§4.9 step 5). The acknowledgment is an operator-keyring signature over the specific `bypass_authorization_id`, not just a checkbox.

### 4.9 Operator final-review gate (L-001)

The pipeline marks a draft "shipped" ONLY after all of:

1. Operator has received the claim-evidence map, rails report, and lessons delta (Section 5 delivery tab opens).
2. Operator has reviewed all 🔴 admin-risk flags (batched, not per-iteration).
3. Operator has signed the claim-evidence map — operator-keyring signature verified against Section 1 keyring retrieve, recorded as `SignedClaimEvidenceMap`.
4. No UNSOURCED claims remain unresolved (map's `unsourced_count == 0`).
5. If a rigor-breach flag is active, operator has explicitly acknowledged it in the sign-off via per-bypass operator-keyring signature.
6. Operator has explicitly confirmed no 🔴 HARD_BLOCK substitution is unresolved (map's `hard_block_count == 0` OR every 🔴 has an operator `APPROVED` decision in the ledger).

Section 5 CLI surface: `tilth review --sign <rfa_hash> --version <n>`. The CLI reads the unsigned claim-evidence map, renders the batch of flags, prompts for sign-off, retrieves the operator's keyring key (Section 1), produces the signature, writes the `SignedClaimEvidenceMap`, and transitions Section 5's state machine to `SHIPPED`.

No draft ships without step 3. The pipeline produces candidates; the operator ships.

#### 4.9.1 Rejection path

If the operator reviews and decides NOT to sign (common case: draft needs more work), Section 5 CLI provides `tilth review --reject <rfa_hash> --version <n> --reason "<text>"`. The reject path:
- Writes an operator-signed rejection note to the admin-risk ledger (entry_kind = `INFO`, operator_signature required).
- Archives the unsigned map to `orgs/{slug}/vault/claim_evidence/{rfa_hash}/rejected/v{n}.unsigned.json`.
- Signals Section 5 to either (a) re-enter the revision loop (if revisions remaining), or (b) terminate the run (if revision cap reached).

No signed artifact exists for a rejected draft. The rejection itself is signed; the draft is not.

#### 4.9.2 Partial sign-off rejected

Signing a subset of flags is not permitted. Either all flags in the batch are acknowledged (with the specific operator action recorded per flag — APPROVE substitution / REJECT substitution / ACKNOWLEDGE breach) and the map is signed, or none are and the map stays unsigned. Splitting sign-off into partial ceremonies would dilute the L-001 verify-at-elevation discipline.

### 4.10 Files owned by Section 4

```
pipeline/logician/
├── __init__.py
├── gates/
│   ├── pre_gate.py          ← All PRE-gate checks (§4.2, deterministic)
│   ├── post_gate.py         ← All POST-gate checks + map generation (§4.4)
│   └── gate_runner.py       ← PRE → [silent loop] → POST orchestration (§4.1)
├── claim_evidence.py        ← BT7 atomic sign-overwrite (§4.5)
├── source_tag_verify.py     ← BT10 grep windowing + M12 whitelist (§4.6)
├── conversation_log.py      ← BT9 append-only signed log (§4.6.4)
├── dossier_verify.py        ← S11c cite-time lock verify + BT11 cross-org policy (§4.6.5 / §4.4.1 step 5)
├── admin_risk.py            ← M8 ledger writer + monotonicity + 🔴/🟡/🟢 classification (§4.7)
├── rails_report.py          ← BT13 signed rails report (§4.8)
└── cedar_eval.py            ← Cedar policy load + evaluation (M14/M15 eval surface)
```

Every file has a published `__all__` enumerating its public surface; sibling modules import only from `__all__`. No file under `pipeline/logician/` imports any provider SDK (enforced by §3.1 AST rule; ARCH-NN candidate until the rule lands).

---

## 5. Interfaces consumed from Sections 1, 2, and 3

Section 4 is a net consumer. It publishes one surface (the gate-runner entry points) and otherwise imports narrow interfaces from the three sibling sections. Every import is cited here with §-number so audit can confirm no re-implementation.

### 5.1 Section 1 (Sovereignty Envelope) — primitives consumed

Section 1 is LOCKED 2026-04-17 at v5. Section 4 imports:

- `Session`, `start_session`, `end_session` — session lifecycle. Section 4 consumes the bound-org-root hash from `Session` at PRE-gate.
- `resolve_keystore()`, `KeyStore.retrieve()` → `SecretBytes` — BYOK key retrieval for M9 check.
- `hmac_sha3_512(key, data) -> bytes` — used by `rails_report.py` for BT13 signing.
- `sign_operator(data) -> bytes`, `verify_operator(data, sig) -> bool` — operator-keyring sign/verify (Ed25519 default; BT4 HSM swappable). Used by `claim_evidence.py` for BT7, by `admin_risk.py` for signed ledger entries, by N.4.2 trust-root mirror verify at PRE-gate check #6.
- `canonical_slug(str) -> str` — Section 1 slug canonicalization; used for org-slug comparison throughout.
- `within_org_root(path, org_slug) -> bool` — path-containment predicate used in source_tag_verify M12 check.
- `canonical_path(str) -> str` — canonical path resolver; used to close symlink-bypass attack surface.
- `record_admin_risk(org_slug, entry) -> AdminRiskLedgerEntry` — Section 1 primitive delegating to Section 4's `admin_risk.py` append (circular-import avoidance pattern via dependency inversion).
- `record_degradation(org_slug, entry) -> DegradationLogEntry` — Section 1 BT8 primitive used by `rails_report.py` to fold degradation entries into the rails report.
- `hmac_audit_writer(path, entry) -> None` — Section 1 append-only hash-chained writer used by `conversation_log.py` and `admin_risk.py` via `vault_write`.
- `atomic_flush(path, bytes_) -> None` — Section 1 temp-file-plus-rename primitive invoked indirectly via `vault_write`.
- `reverify_rfa(rfa_hash) -> RFAVerification` — used at PRE-gate check #7 (RFA dual-hash re-verify).
- `sha3_512_hex(data) -> str` — content-hash primitive.
- `dual_hash_rfa(rfa_bytes, nonce) -> (url_hash, content_hash)` — only called by Section 5 ingest; Section 4 consumes the outputs at PRE-gate.

### 5.2 Section 2 (Vault Topology + Enforcement Envelope) — surfaces consumed

Section 2 is LOCKED 2026-04-17 at v4. Section 4 consumes exclusively through the Vault-owned skills; no direct filesystem `open()` of a vault path. Declared `intent` values:

| Intent | Purpose | Called from |
|---|---|---|
| `claim-evidence-write` | Write unsigned or signed claim-evidence map | `claim_evidence.py` |
| `rails-report-write` | Write signed rails report | `rails_report.py` |
| `conversation-append` | Append to conversation log | `conversation_log.py` |
| `admin-risk-append` | Append to admin-risk ledger | `admin_risk.py` |
| `admin-risk-head-update` | Atomic replace of head.json | `admin_risk.py` |
| `admin-risk-head-read` | Read current head for monotonicity walk | `admin_risk.py` |
| `doc-sourced-verify-read` | BT10 grep-target read | `source_tag_verify.py` |
| `conversation-log-verify-read` | BT9 anchor verify | `source_tag_verify.py` |
| `dossier-verify-read` | S11c three-part verify | `dossier_verify.py` |
| `dossier-verify-cache` | Per-session cite-time verify cache | `dossier_verify.py` |
| `needs-confirmation-enqueue` | Queue a claim for operator confirmation | `post_gate.py` |
| `lessons-delta-append` | Append lessons delta | `post_gate.py` |
| `channel-f-disclosure-read` | Aggregate Scout Channel F log into rails report | `rails_report.py` |
| `degradation-log-read` | Aggregate degradation log into rails report | `rails_report.py` |
| `cedar-policy-read` | Load signed Cedar policy at PRE-gate | `cedar_eval.py` |
| `rfa-manifest-read` | Read RFA dual-hash manifest at PRE-gate | `pre_gate.py` |
| `trust-root-mirror-read` | N.4.2 mirror verify at PRE-gate | `pre_gate.py` |
| `project-context-read` | PROJECT_CONTEXT hash + [NEEDED] scan | `pre_gate.py` |
| `health-tuple-read` | Read Scout signed health tuple | `pre_gate.py` |
| `wrapper-artifact-read` | M14.4.4 wrapper hash + signature verify | `pre_gate.py` |

Every intent string is a Section 2 Cedar-policy trigger. Cedar evaluates per-intent before the read/write proceeds. Missing intent or unexpected intent → Section 2 rejects at the gate with `F-VAULT-*` — Section 4 treats this as an internal invariant violation and aborts with `F-POST-*`/ `F-PRE-*` at the call-site.

Section 4 also consumes:
- `fd_broker.request_fd(path, intent, session_id)` and `fd_broker.release_fd(fd)` — Section 2 v4 FD broker protocol. Used for large-source reads where BT10 grep windowing would otherwise load full files; Section 4 streams via fd broker for files > `BT10_STREAMING_THRESHOLD_BYTES` (§8.5).
- `IdentityTuple` — intent-binding tuple checked at every vault read; Section 4 asserts `IdentityTuple.intent == <declared intent>` post-read per Section 3 A-v3-04 pattern (defence-in-depth: Section 2 enforces, Section 4 re-asserts).
- PRE-gate failure codes (`F-VAULT-*`, `F-GATE-*`) — re-raised from Section 4 gate modules with context.

### 5.3 Section 3 (Scout) — surfaces consumed

Section 3 is LOCKED 2026-04-17 at v5. Section 4 consumes:

- Scout's signed health tuple schema — `SignedHealthTuple` from Section 3 §2.8. Section 4 verifies HMAC via Section 1 `verify_health_tuple` and extracts per-channel state at PRE-gate check #12.
- Scout's admin-risk ledger entries — Scout emits ledger entries for per-channel degradation and admin-risk events (Section 3 §4.10). Section 4 reads these via `record_admin_risk` delegation and folds into the rails report at POST-gate.
- Scout's dossier output shape — `DossierFile` from Section 3 §2.6. Section 4 verifies S11c lock via `dossier_verify.py` at cite time.
- Scout's canonical-JSON signing shape — same byte-identical serialisation Section 4 uses.
- Scout's run_id format, candidate_id namespace, portal slug namespace — Section 4 does not allocate these, only references them in the rails report.
- Scout's Channel F disclosure log shape — `ChannelFFetchEntry` in `run_log/{run_id}.channel_f.jsonl`. Section 4 reads per-session to assemble the BT13 disclosure section.
- Scout's reason-tag set (`F-SCOUT-*`, `F-BT12-*`, `F-GATE-*`, etc.) — Section 4 references these in rails-report `per_channel_health` entries and does not re-define.

Section 4 does NOT consume Scout's internal candidate data structures (`Candidate`, `ReviewRecord`, etc.) — those are Scout-internal and stop at Section 3's surface.

### 5.4 What Section 4 publishes

One public surface, consumed by Section 5:

- `gate_runner.run_pre_gate(context: PreGateContext) -> PreGateResult` — idempotent on `context`; returns either `PASS` or a populated `FailureReason` with sub-tag and operator-facing detail.
- `gate_runner.run_post_gate(context: PostGateContext) -> PostGateResult` — idempotent on `context`; returns either `(SignedClaimEvidenceMap_unsigned, SignedRailsReport, LessonsDelta)` or a populated `FailureReason` with sub-tag.
- `gate_runner.operator_signoff(rfa_hash, draft_version, operator_keyring) -> SignedClaimEvidenceMap` — invoked by Section 5 CLI at `tilth review --sign`.
- `admin_risk.record_bypass_authorization(...)` — invoked by Section 5 at M13 bypass activation time.

No other surface is published. Section 5 imports only the gate runner and `admin_risk.record_bypass_authorization`.

---

## 6. Failure codes

Every FAIL action in §4 emits a reason-tag from the enumeration below. No code path invents a reason-tag at runtime; every tag is declared here or filed as a §10 open question pending declaration. Sub-tags (the `.foo` suffix) are declared at the mechanism's sub-tag list; adding a sub-tag is a blueprint amendment.

### 6.1 `F-PRE-*` — PRE-gate failures

| Tag | Trigger | Admin-risk severity |
|---|---|---|
| `F-PRE-01.section_2_lock_missing` | Section 2 lock marker file absent | HIGH — TAMPER_EVENT |
| `F-PRE-01.section_2_lock_unsigned` | Marker exists but operator signature missing/invalid | HIGH — TAMPER_EVENT |
| `F-PRE-01.section_2_lock_ledger_mismatch` | Marker not in M15 signed-commit ledger | HIGH — TAMPER_EVENT |
| `F-PRE-02.router_yaml_unsigned` | `router.yaml` has no operator signature | HIGH — TAMPER_EVENT |
| `F-PRE-02.router_yaml_signature_invalid` | Signature fails verify against operator keyring | HIGH — TAMPER_EVENT |
| `F-PRE-03.vault_shared_seed_unsigned` | A `vault_shared/` seed file lacks signed-commit | HIGH — TAMPER_EVENT |
| `F-PRE-04.cedar_policy_unsigned` | `vault_shared/cedar/org_isolation.cedar` unsigned | HIGH — TAMPER_EVENT |
| `F-PRE-04.cedar_policy_ledger_mismatch` | Cedar policy not in M15 ledger | HIGH — TAMPER_EVENT |
| `F-PRE-05.wrapper_hash_mismatch` | Process-wrapper hash ≠ committed hash | HIGH — TAMPER_EVENT |
| `F-PRE-05.wrapper_signature_invalid` | Wrapper signature fails verify | HIGH — TAMPER_EVENT |
| `F-PRE-06.trust_root_unsigned` | Logician trust-root mirror unsigned | HIGH — TAMPER_EVENT |
| `F-PRE-06.trust_root_inode_mismatch` | Mirror `(st_dev, st_ino)` does not match signed manifest | HIGH — TAMPER_EVENT |
| `F-PRE-06.trust_root_mount_over_detected` | Immutability flag present but `(st_dev, st_ino)` drifted | HIGH — TAMPER_EVENT |
| `F-PRE-07.rfa_hash_missing` | RFA manifest missing `url_hash` or `content_hash` | HIGH — TAMPER_EVENT |
| `F-PRE-07.rfa_hash_invalid` | Re-verify differs from recorded | HIGH — TAMPER_EVENT |
| `F-PRE-07.rfa_unsigned` | RFA manifest unsigned | HIGH — TAMPER_EVENT |
| `F-PRE-08.session_unbound` | Session lacks org-root binding | INFO |
| `F-PRE-08.project_context_org_mismatch` | PROJECT_CONTEXT.md hash does not match bound org | HIGH — TAMPER_EVENT (possible cross-org attempt) |
| `F-PRE-09.byok_key_wrong_org` | BYOK key bound to a different org (M9 violation) | HIGH — TAMPER_EVENT |
| `F-PRE-09.byok_key_missing` | BYOK key not present in keyring | INFO |
| `F-PRE-10.admin_risk_non_monotonic` | `seq_id` not monotonic | HIGH — TAMPER_EVENT |
| `F-PRE-10.admin_risk_chain_break` | `prev_entry_hash` mismatch | HIGH — TAMPER_EVENT |
| `F-PRE-10.admin_risk_replayed_seq_id` | Duplicate `seq_id` detected | HIGH — TAMPER_EVENT |
| `F-PRE-10.admin_risk_cas_head_mismatch` | CAS append to ledger observed stale `expected_current_file_hash` (closes A-v1-01; retry up to `ADMIN_RISK_LEDGER_APPEND_RETRY_MAX = 3`, §8.1) | INFO on first `< RETRY_MAX` miss, HIGH on exhaustion |
| `F-PRE-11.rlimit_core_nonzero` | RLIMIT_CORE ≠ 0 — wrapper ineffective | HIGH — TAMPER_EVENT |
| `F-PRE-11.stdio_not_null` | stdout/stderr not redirected to null | HIGH — TAMPER_EVENT |
| `F-PRE-12.health_tuple_malformed` | Scout tuple does not match schema | HIGH |
| `F-PRE-12.health_tuple_signature_invalid` | HMAC verify fails | HIGH — TAMPER_EVENT |
| `F-PRE-12.health_tuple_abort_threshold_reached` | All Channel A FAILED OR ≥4/6 families FAILED | HIGH |
| `F-PRE-13.volume_uuid_absent` | Vault subtree filesystem does not expose UUID | HIGH |
| `F-PRE-14.dossier_unsigned` | DOC_SOURCED-referenced dossier lacks operator sign-off | HIGH |
| `F-PRE-15.corpus_incomplete` | PROJECT_CONTEXT.md contains `[NEEDED]` tokens | INFO — CORPUS_INCOMPLETE |
| `F-PRE-16.interrupted_unsourced_unresolved` | Resume with unresolved UNSOURCED claim | INFO |
| `F-PRE-17.cedar_policy_compile_error` | Cedar parser rejects policy | HIGH |
| `F-PRE-18.scout_pre_verify_unsigned` | Section 3 PRE-VERIFY health unsigned | HIGH — TAMPER_EVENT |
| `F-PRE-19.logician_mid_loop_call` | Mid-loop invocation attempt detected | HIGH — TAMPER_EVENT |
| `F-PRE-21.pre_gate_timeout` | PRE-gate total wall-clock > `PRE_GATE_TOTAL_TIMEOUT_MS` (§8.1 = 30000ms); raised by gate_runner watchdog before any check returns (closes B-v1-04) | HIGH — denial of service indicator |
| `F-PRE-22.post_gate_timeout` | POST-gate total wall-clock > `POST_GATE_TOTAL_TIMEOUT_MS` (§8.1 = 60000ms); raised by gate_runner watchdog before any check returns (closes B-v1-04) | HIGH — denial of service indicator |

### 6.2 `F-POST-*` — POST-gate failures

| Tag | Trigger | Admin-risk severity |
|---|---|---|
| `F-POST-01.draft_not_ready` | Section 5 has not signalled draft-ready | INFO |
| `F-POST-01.draft_signal_unsigned` | Draft-ready signal from Section 5 unsigned | HIGH — TAMPER_EVENT |
| `F-POST-02.pre_invariant_drift` | A PRE-gate invariant has changed mid-loop | HIGH — TAMPER_EVENT |
| `F-POST-03.claim_extraction_failed` | Section 5 claim extractor returned error | HIGH |
| `F-POST-04.symlink_in_source_path` | A DOC_SOURCED source path contains a symlink component | HIGH — TAMPER_EVENT |
| `F-POST-04.inode_drift` | Source inode changed between PRE-gate ingest and POST-gate verify | HIGH — TAMPER_EVENT |
| `F-POST-04.path_outside_m12_whitelist` | Source path not under M12 whitelist | HIGH |
| `F-POST-04.content_hash_mismatch` | Source file content hash differs from ingest | HIGH — TAMPER_EVENT |
| `F-POST-05.conversation_anchor_invalid` | USER_DATA anchor fails verify | HIGH |
| `F-POST-05.conversation_anchor_missing_entry` | Cited entry not in log | HIGH |
| `F-POST-05.conversation_anchor_superseded` | Entry has a `corrects:` successor | INFO |
| `F-POST-05.conversation_anchor_wrong_key` | Entry signed by key not active in session | HIGH — TAMPER_EVENT |
| `F-POST-06.admin_risk_rate_limit_exceeded` | BT3 rate limit tripped | INFO |
| `F-POST-07.rails_report_tampered` | Post-delivery rails report edit detected | HIGH — TAMPER_EVENT |
| `F-POST-08.dossier_s11c_fail_path` | S11c path canonicalization fail | HIGH — TAMPER_EVENT |
| `F-POST-08.dossier_s11c_fail_inode` | S11c inode mismatch | HIGH — TAMPER_EVENT |
| `F-POST-08.dossier_s11c_fail_hash` | S11c content-hash mismatch | HIGH — TAMPER_EVENT |
| `F-POST-09.bt11_cross_org_unconfirmed` | Cross-org dossier cited without draft-time secondary confirmation | HIGH |
| `F-POST-10.hard_block_unresolved` | 🔴 admin-risk match persists after Scribe one-shot rewrite | HARD_BLOCK |
| `F-POST-11.unsourced_unresolved` | UNSOURCED claim remains at POST-gate output | HARD_BLOCK |
| `F-POST-12.vault_write_failed` | Section 2 `vault_write` returned error | HIGH |
| `F-POST-13.structural_section_missing` | Required draft section absent | INFO (routed to Section 5 micro-recovery) |
| `F-POST-13.structural_word_count_over` | Word count exceeds rubric ceiling | INFO |
| `F-POST-13.structural_budget_line_missing` | Budget section lacks required line item | INFO |
| `F-POST-13.structural_match_fund_missing` | Matching fund statement absent | INFO |
| `F-POST-14.claim_evidence_version_collision` | Two drafts claim same `rfa_hash` + `v{n}` | HIGH — Section 5 bug |
| `F-POST-15.lessons_delta_write_failed` | Appending to pending_lessons.jsonl failed | INFO |

### 6.3 `F-BT7-*` — claim-evidence map discipline

| Tag | Trigger | Admin-risk severity |
|---|---|---|
| `F-BT7-01.canonical_json_non_idempotent` | Round-trip canonicalization produces different bytes | HIGH — invariant break |
| `F-BT7-02.signature_verify_failed` | Operator signature verify fails at read time | HIGH — TAMPER_EVENT |
| `F-BT7-03.atomic_write_interrupted` | Write aborted between `.unsigned` and signed replace | INFO (Autonomy Rule 1 resume path) |
| `F-BT7-04.key_id_unknown` | Cited `operator_key_id` not in Section 1 key catalog | HIGH |

### 6.4 `F-BT9-*` — conversation log integrity

| Tag | Trigger | Admin-risk severity |
|---|---|---|
| `F-BT9-01.chain_break` | Conversation log hash chain broken | HIGH — TAMPER_EVENT |
| `F-BT9-02.session_key_retired` | Entry signed by retired session key | INFO (BT6 rotation audit) |
| `F-BT9-03.append_race` | Concurrent append detected | HIGH |

### 6.5 `F-BT10-*` — grep windowing discipline

| Tag | Trigger | Admin-risk severity |
|---|---|---|
| `F-BT10-01.tokenizer_failed` | Sentence tokenization raised | HIGH |
| `F-BT10-02.window_empty` | Claim's cited file yielded zero sentences | HIGH |
| `F-BT10-03.streaming_read_truncated` | FD-broker streaming read ended before file end | HIGH |

### 6.6 `F-BT11-*` — cross-org dossier policy

| Tag | Trigger | Admin-risk severity |
|---|---|---|
| `F-BT11-01.cross_org_reference_created_without_audit_entry` | Reference created but no audit entry | HIGH |
| `F-BT11-02.cross_org_reference_missing_draft_time_confirmation` | Secondary confirmation not provided at draft time | HIGH |

### 6.7 `F-BT13-*` — rails report signing

| Tag | Trigger | Admin-risk severity |
|---|---|---|
| `F-BT13-01.session_key_unavailable` | BT6 session key missing (Section 1 fault) | HIGH |
| `F-BT13-02.canonical_json_non_idempotent` | Rails report canonicalization non-idempotent | HIGH |
| `F-BT13-03.rigor_breach_unacknowledged_at_signing` | At §4.9 step 5, an active M13 rigor-breach bypass exists in the rails report but the operator's sign-off ceremony has no per-bypass operator-keyring signature for it; CLI MUST refuse the sign and surface the missing acknowledgment (closes B-v1-04 inline; was §10 candidate in v1) | HARD_BLOCK — sign refused |
| `F-BT13-03.channel_f_disclosures_truncated` | Channel F disclosure log exceeded `RAILS_REPORT_MAX_BYTES`; rails report carries an explicit `channel_f_disclosures_truncated = True` flag (closes v1 §10 F-OQ-07) | INFO — observability flag |

### 6.8 `F-M7-*` — health-tuple verification

| Tag | Trigger | Admin-risk severity |
|---|---|---|
| `F-M7-01.session_key_unknown` | Scout's tuple signed with a key not in catalog | HIGH — TAMPER_EVENT |
| `F-M7-02.tuple_schema_version_unsupported` | Tuple claims an unsupported schema version | HIGH |

### 6.9 `F-M8-*` — admin-risk ledger discipline

Covered inline in `F-PRE-10.*` (pre-gate invariant) and `F-POST-06.*` (rate limit). No separate tag set.

### 6.10 `F-M9-*` — per-org key scoping

Covered inline in `F-PRE-09.*`.

### 6.11 `F-M11-*` / `F-S11c-*` — dossier lock

Covered inline in `F-PRE-14.*` (PRE-gate unsigned) and `F-POST-08.*` (cite-time three-part fail).

### 6.12 Reason-tag invariants

Three invariants bind the reason-tag set:
1. Every code path that returns a failure produces exactly one reason-tag. No multi-tag returns.
2. No reason-tag is silently reclassified. Severity is fixed at tag declaration time; a HIGH-severity tag never becomes INFO.
3. Every reason-tag emitted to the rails report has a companion admin-risk ledger entry with matching `draft_version_ref` and `rails_report_hash` — guarantees a paper trail.

---

## 7. Durable enforcement rules (regression-protected invariants)

These invariants survive code changes. Property tests (§9.7) exercise them against adversarial inputs. A future blueprint revision that would break any invariant requires explicit architectural justification and is not a Bucket-B narrow edit.

### 7.1 Two-gate invariant

Logician runs at exactly two gates per pipeline invocation: PRE before Scout and POST after Judge. Any runtime path that observes a third invocation (mid-loop, nested, re-entered) is an invariant break; `gate_runner.py` sets `_GATE_STATE ∈ {IDLE, PRE, BETWEEN, POST, DONE}` module-local and raises `F-PRE-19` on unexpected transitions. Property test: simulate mid-loop call attempts across all 20 module-internal entry points; every attempt raises `F-PRE-19`.

### 7.2 Silent-mid-loop invariant

No Section 4 code path runs between PRE gate exit and POST gate entry, with the single documented exception of `admin_risk.record_bypass_authorization()` invoked by Section 5 at M13 activation. Property test: AST-lint that counts `pipeline.logician` imports under `pipeline/pipeline/loop/` — expected zero; any non-zero count fails.

### 7.3 Fail-closed invariant

Every check returns either `PASS` or a populated `FailureReason`; no check returns `None`, `UNKNOWN`, or an abstaining value in a pass path. Property test: run every PRE-gate and POST-gate check against an input that triggers each failure branch; assert the return matches the declared reason-tag.

### 7.4 No-LLM invariant

No Section 4 module imports or invokes an LLM client library, directly or transitively. Property test: AST-lint across `pipeline/logician/**/*.py` for imports matching `anthropic|openai|groq|google.generativeai|ollama`; expected zero.

### 7.5 Canonical-JSON byte-identical invariant

For any `ClaimEvidenceMap`, `RailsReport`, `AdminRiskLedgerEntry`, or `ConversationLogEntry`, `canonical_json(round_trip(x)) == canonical_json(x)` bytewise. Property test: fuzz 10,000 random valid instances; assert round-trip preservation; any miss → `F-BT7-01` or `F-BT13-02`.

### 7.6 No direct vault `open()` invariant

No Section 4 module invokes `open()` on any path rooted under `orgs/` or `vault_shared/`. Property test: AST-lint for `open(...)` calls where the first argument's static analysis resolves to a string literal under those roots. The AST rule pattern is analogous to Section 3's AST-NO-INDIRECT-VAULT-READ.

### 7.7 Claim-evidence atomic sign-overwrite invariant

A `SignedClaimEvidenceMap` on disk either (a) fully verifies (signature, hash, content) or (b) fails completely. No intermediate state where hash matches but signature does not, or vice versa. Property test: interrupt sign-overwrite at every byte boundary during write; fsck confirms either `.unsigned` or fully-signed; never partial-signed.

### 7.8 Ledger monotonicity invariant

For any two entries `e_i` and `e_{i+1}` in the admin-risk ledger, `e_{i+1}.seq_id == e_i.seq_id + 1` and `e_{i+1}.prev_entry_hash == e_i.entry_hash`. Property test: walk ledger from head; assert invariant at every pair; break → `F-PRE-10.*`.

### 7.9 Operator-signed HARD_BLOCK resolution invariant

A `ClaimEvidenceMap` with `hard_block_count > 0` cannot become a `SignedClaimEvidenceMap`. The CLI at `tilth review --sign` refuses to sign; the invariant is enforced both at the CLI surface and at `claim_evidence.py`'s `finalize_signed_map()` entry. Property test: attempt to sign a map with `hard_block_count = 3`; expect refusal with message naming the 3 blocks.

### 7.10 UNSOURCED resolution invariant

A `ClaimEvidenceMap` with `unsourced_count > 0` cannot become a `SignedClaimEvidenceMap`. Same dual enforcement as §7.9. Property test: attempt to sign; expect refusal.

### 7.11 Rigor-breach acknowledgment invariant

A `ClaimEvidenceMap` with `rigor_breach_active = True` requires per-bypass operator signature in addition to the map-level signature. The CLI collects per-bypass signatures before permitting map-level signature. Property test: attempt to sign without per-bypass signatures; expect refusal.

### 7.12 Cedar policy load-before-eval invariant

Cedar policy must be signature-verified and M15-ledger-checked BEFORE any evaluation. `cedar_eval.py` refuses to evaluate if `policy.verified == False`. Property test: inject an unverified policy; attempt evaluation; expect refusal with `F-PRE-04.*`.

### 7.13 Intent-match invariant

Every `vault_read` / `vault_write` call from Section 4 passes an `intent` string from the enumeration in §5.2, and after the call asserts `IdentityTuple.intent == <declared>`. Mismatch → hard abort (defence-in-depth, Section 2 enforces at gate time; Section 4 re-asserts post-read). Property test: inject a mismatched tuple; expect abort.

---

## 8. Concrete numbers pinned

Every cap, timeout, retry count, window size, and key length used by Section 4 is pinned here. Changing a number is a blueprint amendment, not an implementation-time decision.

### 8.1 Constants table

| Name | Value | Purpose | Rationale |
|---|---|---|---|
| `BT10_DEFAULT_WINDOW_SENTENCES` | 2 | ±2 sentence window for DOC_SOURCED grep | Default from architecture BT10; covers common case (claim + one sentence context on each side) |
| `BT10_FALLBACK_WINDOW_SENTENCES` | 5 | ±5 fallback window | Covers long-discussion case; beyond this classifies UNSOURCED |
| `BT10_FALLBACK_ATTEMPTS_MAX` | 1 | One fallback attempt before UNSOURCED | Prevents window-size escalation as evasion path |
| `BT10_STREAMING_THRESHOLD_BYTES` | 524288 (512 KB) | Files larger than this stream via FD broker | Memory bound on large source files |
| `BT10_STREAMING_CHUNK_BYTES` | 65536 (64 KB) | Streaming chunk size | Matches Section 2 v4 FD broker chunk size |
| `BT10_SEMANTIC_SIMILARITY_THRESHOLD` | 0.75 | Optional similarity pass threshold (if enabled) | Empirical threshold; opt-in default off |
| `ADMIN_RISK_LEDGER_ENTRY_MAX_BYTES` | 16384 (16 KB) | Max bytes per ledger entry | Prevents unbounded-size entry DoS |
| `ADMIN_RISK_LEDGER_APPEND_RETRY_MAX` | 3 | Max append retries on contention | Concurrent write protection |
| `ADMIN_RISK_LOW_SEVERITY_RATE_LIMIT_PER_HOUR` | 100 | BT3 rate limit on PRECAUTIONARY adds | Anti-flood |
| `ADMIN_RISK_HIGH_SEVERITY_RATE_LIMIT_PER_HOUR` | 10 | BT3 rate limit on HARD_BLOCK adds | Anti-flood |
| `CLAIM_EVIDENCE_MAP_MAX_ENTRIES` | 10000 | Max claims per map | Prevents unbounded-map DoS |
| `CLAIM_EVIDENCE_UNSIGNED_TTL_HOURS` | 72 | Unsigned map TTL before auto-archive | 72h matches Section 5 revision-loop-total timeout |
| `RAILS_REPORT_MAX_BYTES` | 5242880 (5 MB) | Max rails report size | Bounded artifact |
| `CONVERSATION_LOG_ENTRY_MAX_BYTES` | 32768 (32 KB) | Max entry size | Prevents unbounded-utterance DoS |
| `CONVERSATION_LOG_SEGMENT_MAX_BYTES` | 10485760 (10 MB) | Log segment rotation threshold | Section 2 write discipline |
| `CEDAR_POLICY_LOAD_TIMEOUT_MS` | 2000 | Cedar parse + compile timeout | Blocks adversarial policy DoS |
| `PRE_GATE_TOTAL_TIMEOUT_MS` | 30000 | PRE-gate total wall-clock timeout | Bounds PRE-gate; FAIL → `F-PRE-21.pre_gate_timeout` |
| `POST_GATE_TOTAL_TIMEOUT_MS` | 120000 | POST-gate total wall-clock timeout | Bounds POST-gate (claim extraction + scan) |
| `POST_GATE_CLAIM_EXTRACTION_TIMEOUT_MS` | 60000 | Section 5 extractor timeout | Guard against extractor hang |
| `OPERATOR_SIGNOFF_IDLE_TIMEOUT_HOURS` | 168 | Idle sign-off timeout (1 week) | Draft archives to rejected if operator never signs |
| `DOSSIER_VERIFY_CACHE_TTL_MINUTES` | 0 | S11c cite-time cache (DISABLED at v0.1 per B-v1-01) | Re-verify on every cite; correctness over speed at v0.1 throughput. Operator may set non-zero per-org via `orgs/{slug}/vault/config/dossier_cache.yaml` (M15-signed); each enable is logged as a TAMPER_EVENT-class operator decision (INFO severity, not blocking). |
| `LOGICIAN_SESSION_KEY_LENGTH_BYTES` | 64 | BT6 session key length | SHA-3 block size |
| `OPERATOR_SIGNATURE_ALGORITHM` | `"Ed25519"` | Operator-keyring signature algorithm | Default; BT4 HSM path preserves algorithm |

### 8.2 Sentence tokenizer abbreviation list (§4.6.1)

Carved out to prevent false sentence breaks:
```
Mr. Mrs. Ms. Dr. Prof. Inc. Ltd. Co. Corp. etc. vs. e.g. i.e. U.S. U.K. U.N. a.m. p.m. No. Vol. Ch. St. Ave. Blvd. Rd. Jr. Sr. Ph.D. M.D. B.A. M.A. B.S. M.S.
```

Non-English abbreviations are out-of-scope for v0.1 (operator confirmation 2026-04-17). Expansion of the list is a §8 amendment.

### 8.3 Cedar entity schema version

Section 4 v1 pins Cedar entity schema at `s4-v1`. Entity shapes in §2.6 are the canonical definitions. Schema version is recorded in the Cedar policy header and verified at PRE-gate check #4.

### 8.4 Reason-tag admin-risk severity table

See §6.1–§6.11 inline. The severity column is authoritative; changing a severity is a §6 amendment.

### 8.5 M12 whitelist roots

See §4.6.3. Adding a root is an architectural amendment (M12 widen), not a blueprint change.

---

## 9. Test vectors

### 9.1 PRE-gate pass case

**Input:** Session bound to `mycosymbiotics_inc`, RFA dual-hash valid and signed, PROJECT_CONTEXT with zero `[NEEDED]`, Cedar policy signed + M15-committed, Scout health tuple signed with all channels OK, BYOK key bound to `mycosymbiotics_inc`, admin-risk ledger monotonic, wrapper hashed, trust-root mirror intact.

**Expected:** `PreGateResult.status == "PASS"`, no ledger entry written, gate transitions to `BETWEEN`.

### 9.2 PRE-gate FAIL cases (one per `F-PRE-*` sub-tag)

Enumerated property tests, one per sub-tag in §6.1. Each test:
1. Constructs a valid PRE-gate context.
2. Mutates exactly one invariant to trigger the target sub-tag.
3. Invokes `run_pre_gate`.
4. Asserts return `FailureReason.sub_tag == <target>`.
5. Asserts ledger entry written with matching severity.

Example:
```python
def test_f_pre_09_byok_key_wrong_org():
    ctx = valid_pre_gate_context()
    ctx.session.byok_key_id = "key-bound-to-different-org"
    result = run_pre_gate(ctx)
    assert result.fail_reason.sub_tag == "F-PRE-09.byok_key_wrong_org"
    assert latest_ledger_entry().entry_kind == "TAMPER_EVENT"
```

Full suite: 39 tests across 19 check IDs × avg 2 sub-tags.

### 9.3 POST-gate pass case

**Input:** PRE passed; draft completed Judge ≥ 85; claim extractor returned 23 claims; all 23 verify DOC_SOURCED or USER_DATA; admin-risk scan returned 0 🔴, 2 🟡, 5 🟢; structural checks pass.

**Expected:** `PostGateResult.status == "PASS"`; `SignedRailsReport` signed; `ClaimEvidenceMap.unsourced_count == 0`; `.hard_block_count == 0`; awaiting operator sign-off.

### 9.4 POST-gate UNSOURCED hard block

**Input:** PRE passed; draft completed; claim extractor returned 23 claims; claim #17 cites a source outside M12 whitelist.

**Expected:** `PostGateResult.status == "BLOCKED"`; `ClaimEvidenceMap.unsourced_count == 1`; `map.entries[17].tag == "UNSOURCED"`; `map.entries[17].verify_detail` names the offending path; delivery tab surfaces the four resolution paths.

### 9.5 POST-gate 🔴 rewrite escalation

**Input:** Draft contains term `"warzone"` (example 🔴 in admin-risk register). Section 5 runs Scribe one-shot rewrite with proposed alternatives; rewrite introduces term `"frontlines"` (also 🔴).

**Expected:** `PostGateResult.status == "BLOCKED"`; rails report batches 🔴 with operator sign-off required; `F-POST-10.hard_block_unresolved`.

### 9.6 Operator sign-off with rigor breach

**Input:** POST passed; draft has `rigor_breach_active = True` (Judge bypassed via M13 for 18h); operator signs map without acknowledging breach.

**Expected:** CLI refuses at per-bypass signature step; `F-BT13-03.rigor_breach_unacknowledged_at_signing` (declared inline at §6.7 in v2, no longer §10 candidate); operator prompted to acknowledge or reject.

### 9.6.1 BT10 streaming truncation (closes B-v1-03)

**Input:** A DOC_SOURCED claim cites a source file whose size > `BT10_MAX_FILE_BYTES` (§8.1). Property fuzz: 1,000 random sizes drawn uniformly from `[BT10_MAX_FILE_BYTES + 1, BT10_MAX_FILE_BYTES * 4]` bytes.

**Expected:** every iteration raises `F-BT10-03.source_file_too_large` BEFORE any grep window evaluation; never silent truncation; never partial grep; never UNSOURCED-by-truncation. The source-tag verifier MUST fail the claim's tag with the explicit too-large reason rather than degrading to an UNSOURCED tag that hides the underlying overflow.

### 9.6.2 Admin-risk CAS race (closes A-v1-01)

**Input:** Two concurrent POST-gate runs (same org, different `rfa_hash`) attempt to append to the admin-risk ledger. Property: spawn 100 paired runs; each pair is a forced concurrent append.

**Expected:** in every pair, exactly one append commits on the first try and the other observes `F-VAULT-CAS-HEAD-MISMATCH` → `F-PRE-10.admin_risk_cas_head_mismatch` (INFO, not HIGH on the first miss) → re-runs steps 1-8 with the fresh head and commits on retry attempt ≤ `ADMIN_RISK_LEDGER_APPEND_RETRY_MAX = 3`. After 100 pairs, ledger contains 200 entries with strictly monotonic `seq_id`, no gaps, no duplicates, hash chain intact.

### 9.6.3 Claim-evidence write-if-absent race (closes A-v1-02)

**Input:** Two concurrent POST-gate runs both attempt to write `orgs/{slug}/vault/claim_evidence/{rfa_hash}/v{n}.json.unsigned` (Section 5 bug — duplicate `draft_version` allocated). Property: spawn 100 paired runs.

**Expected:** in every pair, exactly one write commits via `vault_write(write_mode="write-if-absent")`; the other receives `F-VAULT-WRITE-EXISTS` → `F-POST-14.claim_evidence_version_collision`. The losing POST-gate run does NOT silently overwrite the winner's file (this is the v1 race the kernel-atomic primitive closes). The winner's `.unsigned` file bytes are exactly what the winning run wrote; no interleaving, no torn write.

### 9.7 Property tests

One property test per invariant in §7:
- §7.1 Two-gate: fuzz nested call attempts; expect `F-PRE-19`.
- §7.2 Silent-mid-loop: AST-lint run; expect zero imports.
- §7.3 Fail-closed: every check returns `PASS` or populated `FailureReason`; never `None`.
- §7.4 No-LLM: AST-lint run; expect zero provider imports.
- §7.5 Canonical-JSON byte-identical: fuzz 10,000 valid instances; assert round-trip.
- §7.6 No direct vault `open()`: AST-lint; expect zero matches.
- §7.7 Atomic sign-overwrite: interrupt write at every byte boundary; fsck binary state.
- §7.8 Ledger monotonicity: walk from head; assert invariant.
- §7.9 HARD_BLOCK sign refusal: attempt sign; expect refusal.
- §7.10 UNSOURCED sign refusal: attempt sign; expect refusal.
- §7.11 Rigor-breach sign refusal: attempt sign without per-bypass sig; expect refusal.
- §7.12 Cedar load-before-eval: inject unverified policy; expect refusal.
- §7.13 Intent-match: inject mismatched tuple; expect abort.

### 9.8 Regression tests

Every filed §10 ARCH-NN candidate, every audit finding closed in v2+, and every known Section 3 interface change re-tested against Section 4. Regression suite runs in CI at every blueprint lock.

---

## 10. Open questions / ARCH-NN candidates / deferred-to-v0.2

### F-OQ-01 — Sentence tokenization for non-English drafts — RESOLVED in v2

v0.1 scope confirmed English-only per operator 2026-04-17. Not an architectural amendment; a scope line item. **Resolution (v2, closes C-v1-02):** English-only is explicitly declared as v0.1 product scope in §12; non-English support is a v0.2 candidate deferred to future Section 4 amendments. No ARCH ticket needed until v0.2 planning begins.

### F-OQ-02 — Semantic similarity primitive — RESOLVED in v2

BT10 names optional semantic similarity as "when available." Blueprint Section 4 v1 defaults to OFF. **Resolution (v2, closes C-v1-03):** v0.1 ships with string-overlap only (the §4.6.2 step 7 opt-in stays but the constant `BT10_SEMANTIC_SIMILARITY_ENABLED` defaults to `False` and operator-override is confined to `orgs/{slug}/vault/config/bt10_window.yaml`). Architecturally binding a specific local-embedding primitive is explicitly NOT required at v0.1; deferred to v0.2 if opt-in usage becomes significant.

### F-OQ-03 — Operator sign-off UX for headless v0.1 — DEFERRED TO SECTION 5

CLI `tilth review --sign <rfa_hash> --version <n>` is the v0.1 surface. **Resolution (v2, closes C-v1-04):** this is a Section 5 (orchestrator/CLI) concern, not a Section 4 concern. Moved from Section 4 §10 to Section 5 blueprint's to-draft list. Section 4 v2 merely consumes whatever CLI Section 5 publishes; the sign-off ceremony itself is the Section 5 author's responsibility.

### F-OQ-04 — 🔴 admin-risk flag resolution timeout

If Scribe's one-shot rewrite fails to land and operator is unavailable, how long before the HARD_BLOCK expires? v0.1 default: no expiry (blocking until operator responds). `OPERATOR_SIGNOFF_IDLE_TIMEOUT_HOURS = 168` (§8.1) archives the draft as rejected after 1 week idle, but the flag itself does not auto-resolve.

### F-OQ-05 — Concurrent operator sessions per org — RESOLVED in v2

**Resolution (v2, closes A-v1-01):** Section 2 v7 §4.10.4 exposes `vault_write(intent="admin-risk-append", write_mode="append-cas", expected_current_file_hash=...)` — CAS semantics guarantee exactly-once append under concurrent writers. Section 4 §4.7.3 step 8 (v2) calls this primitive and on `F-VAULT-CAS-HEAD-MISMATCH` retries up to `ADMIN_RISK_LEDGER_APPEND_RETRY_MAX = 3` times. The previously-filed-but-undeclared `F-POST-06.admin_risk_concurrent_append` tag is superseded by the declared `F-PRE-10.admin_risk_cas_head_mismatch` tag in §6.1 (v2). Property test §9.6.2 verifies 100 forced-concurrent pairs converge correctly.

### F-OQ-06 — Key rotation mid-sign-off

If BT6 session key rotates between rails-report signing (POST-gate step 10) and operator sign-off (could be days later), verifying rails report still works via Section 1 key-retirement catalog. But if operator keyring rotates between draft-generation and sign-off, the operator-keyring signature uses the new key and verifies against the new catalog entry. Question: should a claim-evidence map signed by a retired key still "count" for shipment? Answer: yes — the key was authoritative at sign time, recorded in `operator_key_id`. Filed as test vector (§9 regression).

### F-OQ-07 — Channel F disclosure log size bound — RESOLVED in v2

**Resolution (v2):** Sub-tag `F-BT13-03.channel_f_disclosures_truncated` declared inline in §6.7 (v2). Rails report truncation with explicit `channel_f_disclosures_truncated = True` flag + rails-report note is now the documented behaviour, not a v2 amendment-to-come.

### F-OQ-08 — Cedar policy update mid-session

If the operator commits a new Cedar policy under `vault_shared/cedar/` mid-session (signed + M15), does Section 4 reload? v0.1 answer: No — Cedar policy is loaded at PRE-gate and bound for the session. Mid-session policy changes apply to the next pipeline run. This is a product decision; filed as §12 scope non-ownership line.

### F-OQ-09 — Dossier verify cache staleness boundary — RESOLVED in v2

**Resolution (v2, closes B-v1-01):** `DOSSIER_VERIFY_CACHE_TTL_MINUTES` default set to `0` (cache disabled) at v0.1. Re-verify on every cite; correctness over speed. v0.1 throughput is bounded (handful of drafts per org per week) so the three-part S11c check cost is negligible. Operator may set a non-zero TTL per-org via `orgs/{slug}/vault/config/dossier_cache.yaml` (M15-signed); each enable is logged as a TAMPER_EVENT-class INFO-severity operator decision so the audit-trail retains the fact that the cache was on during that run. Default stays at 0 permanently at v0.1.

### F-OQ-10 — Interrupted-state UNSOURCED tombstone

When a draft is interrupted with UNSOURCED claims, the checkpoint carries the unresolved list. §4.2.4 PRE-gate check #16 rejects resume. Alternative: allow resume with an explicit "operator resumes at own risk" flag. v0.1 default: no such flag; resume blocks. Filed as §12.

### F-OQ-11 — ARCH-03 muddied signal acknowledgment

Section 3 §10 filed F-OQ-11 naming the muddied-signal limitation when the NOT_OPTED_IN state interacts with certain operator-configured channel masks. Section 4 §4.2.1 check #12 consumes the tuple; if `per_channel["X"] == "NOT_OPTED_IN"`, check #12 does NOT treat this as FAILED for abort-threshold purposes (NOT_OPTED_IN is intentional, not a fault). This is the honour-line for Section 3's ARCH-03 resolution.

### F-OQ-12 — Multi-org ledger rollup in rails report

Rails report is per-run, per-org (`org_slug` binding). If the operator's dev node (A2) runs multiple orgs, there is no cross-org rails rollup. Operator-level aggregation is out-of-scope for Section 4; if ever needed, a new blueprint section owns it (not Section 4).

### F-OQ-13 — Admin-risk register source of truth

Section 4 consumes `pipeline/institutional_memory/admin_risk_register.yaml` for 🔴/🟡/🟢 classification. Register is signed + M15-committed. Section 4 does NOT author or edit the register. If the register contains a malformed severity value, Section 4 aborts PRE-gate with `F-PRE-03.vault_shared_seed_unsigned` (if unsigned) or `F-PRE-20.admin_risk_register_malformed` (filed as sub-tag candidate for §6.1 blueprint v2 amendment).

### ARCH-04 candidate — AST rule for `pipeline/logician/` provider-SDK import ban

Section 3 has AST rules in §7.16 (e.g., AST-NO-INDIRECT-VAULT-READ). Section 4 should have an analogous rule blocking `anthropic|openai|groq|google.generativeai|ollama` imports under `pipeline/logician/**`. Filing as ARCH-04 at `pipeline/validation/architecture_v0.1_findings_from_section_04/ARCH-04.md` for Thesis Team review; until landed, Section 4 modules are manually audited at lock-time.

### ARCH-05 candidate — cross-org dossier draft-time secondary confirmation UX

BT11 requires "secondary operator confirmation at draft-time (not at reference-creation time)." Section 4 enforces the flag (`F-BT11-02`), but the UX is a Section 5 CLI surface: `tilth dossier confirm-cross-org <entity_slug> --target-org <slug>` before the draft can be signed. Filing as ARCH-05 — the CLI surface split between Sections 4 and 5 is ambiguous and wants operator + Thesis Team disambiguation.

### Deferred to v0.2

- Multi-tenant shared hardware (A3 → v2 product scope). Adds O.5.a-f hardening (constant-time response padding, per-org cgroup + CPU-cache flush, HSM-default keyring). Section 4 changes needed: add per-org claim-evidence map partitioning, cross-org rails rollup with constant-time response, per-org HSM-backed signing keys.
- GUI review pane. Future affordances: per-section panels, reframe button, token-bloat banner, claim-evidence map viewer, rails dashboard. v0.1 stays headless.
- Non-English draft support. Sentence tokenizer expansion + per-language abbreviation list.
- Admin-risk register auto-learning. Flagged-term frequency across grants could auto-propose register additions; v0.1 operator manually authors.

---

## 11. Law + Autonomy Rule enforcement map

Which Law / Rule is checked at which gate, with reason-tag.

| Architecture obligation | Gate | Check | Reason-tag on FAIL |
|---|---|---|---|
| Law 1 (RFA source of truth) — RFA dual-hash present + valid + signed | PRE | §4.2.1 #7 | `F-PRE-07.*` |
| Law 1 — PRE-gate drift check at POST (RFA hash unchanged since ingest) | POST | §4.4.1 #2 | `F-POST-02.pre_invariant_drift` |
| Law 1 — corpus completeness (no `[NEEDED]` — required substance is present) | PRE | §4.2.1 #15 | `F-PRE-15.corpus_incomplete` |
| Law 2 (no boundary drift) — enforced by Section 5 rubric check | POST | §4.4.1 #7 (structural) | `F-POST-13.*` |
| Law 3 (org isolation) — session binding + PROJECT_CONTEXT hash match | PRE | §4.2.1 #8 | `F-PRE-08.*` |
| Law 3 — BYOK key per-org scoping (M9) | PRE | §4.2.1 #9 | `F-PRE-09.*` |
| Law 3 — Cedar `org_isolation` gate on every vault read/write | continuous | §5.2 intent table | `F-VAULT-*` (re-raised as `F-POST-12`) |
| Law 3 — cross-org dossier reference policy (BT11) | POST | §4.4.1 #5 | `F-POST-09.bt11_cross_org_unconfirmed` |
| Law 4 (apolitical sector language + admin-risk scan) — ledger monotonicity | PRE | §4.2.1 #10 | `F-PRE-10.*` |
| Law 4 — admin-risk term scan + 🔴/🟡/🟢 classification | POST | §4.4.1 #6 | `F-POST-10.hard_block_unresolved` |
| Law 4 — no silent rewrite: operator approves each 🔴 substitution | Sign-off | §4.9 step 6 | Sign refusal |
| Law 5 (applicant brings substance) — DOC_SOURCED grep verify (BT10) | POST | §4.4.1 #4 | `F-POST-04.*` |
| Law 5 — USER_DATA conversation anchor verify (BT9) | POST | §4.4.1 #4 | `F-POST-05.*` |
| Law 5 — UNSOURCED hard block | POST | §4.4.1 #4 | `F-POST-11.unsourced_unresolved` |
| Law 5 — entity dossier lock verify (S11c) | PRE (cite availability) + POST (cite verify) | §4.2.1 #14 + §4.4.1 #5 | `F-PRE-14.*` + `F-POST-08.*` |
| Law 5 — operator final-review gate | Sign-off | §4.9 | Sign refusal |
| Autonomy Rule 1 (save state always) — interrupted-state resume check | PRE | §4.2.1 #16 | `F-PRE-16.interrupted_unsourced_unresolved` |
| Autonomy Rule 2 (test own work) — POST-gate IS the test step for the pipeline's work | POST | all §4.4.1 | various |
| Autonomy Rule 3 (be explicit) — every failure surfaces an operator-facing reason-tag | all | §6 | all |
| Autonomy Rule 4 (clean output) — canonical JSON byte-identical | BT7 / BT13 | §7.5 | `F-BT7-01` / `F-BT13-02` |
| M1 — RFA dual-hash | PRE | §4.2.1 #7 | `F-PRE-07.*` |
| M2 — session org-root binding | PRE | §4.2.1 #8 | `F-PRE-08.*` |
| M7 — Scout health-tuple HMAC verify | PRE | §4.2.1 #12 | `F-PRE-12.*` / `F-M7-*` |
| M8 — admin-risk ledger monotonicity | PRE | §4.2.1 #10 | `F-PRE-10.*` |
| M9 — per-org BYOK scoping | PRE | §4.2.1 #9 | `F-PRE-09.*` |
| M10 — author-seat graceful degradation flag integrity (BT8) | PRE (chain verify) + POST (rollup) | §4.2.1 #10 + §4.8 | `F-PRE-10.*` + rails report injection |
| M11 — entity dossier operator sign-off | PRE (presence) + POST (cite lock) | §4.2.1 #14 + §4.4.1 #5 | `F-PRE-14.*` + `F-POST-08.*` |
| M12 — DOC_SOURCED source-directory whitelist | POST | §4.6.3 | `F-POST-04.path_outside_m12_whitelist` |
| M13 — review-seat bypass operator acknowledgment | Sign-off | §4.9 step 5 | Sign refusal |
| M14 — vault access gating via Cedar `org_isolation` | continuous | §5.2 | `F-VAULT-*` / `F-POST-12` |
| M14.4.1 — rlimit + stdio suppression | PRE | §4.2.1 #11 | `F-PRE-11.*` |
| M14.4.4 — wrapper hash + signature | PRE | §4.2.1 #5 | `F-PRE-05.*` |
| M15 — `vault_shared/` signed-commit | PRE | §4.2.1 #3 | `F-PRE-03.*` |
| M15.3 — Cedar policy signed + M15-committed | PRE | §4.2.1 #4 | `F-PRE-04.*` |
| N.4.1 — Section 2 lock marker presence | PRE | §4.2.1 #1 | `F-PRE-01.*` |
| N.4.2 — trust-root mirror + `(st_dev, st_ino)` binding | PRE | §4.2.1 #6 | `F-PRE-06.*` |
| BT7 — atomic claim-evidence sign-overwrite | POST + sign-off | §4.5 | `F-BT7-*` |
| BT8 — degraded-run flag integrity | PRE (chain) + POST (rollup) | §4.2.1 #10 + §4.8 | `F-PRE-10.*` + rails injection |
| BT9 — USER_DATA conversation-anchor integrity | POST | §4.6.4 | `F-POST-05.*` / `F-BT9-*` |
| BT10 — grep verification windowing | POST | §4.6 | `F-POST-04.*` / `F-BT10-*` |
| BT11 — cross-org dossier reference policy | POST | §4.4.1 #5 | `F-POST-09.*` / `F-BT11-*` |
| BT12 — Channel F domain pre-flight | consumed from Section 3 | §4.8 (rails rollup) | re-raised as rails entry |
| BT13 — rails report signing | POST | §4.8 | `F-BT13-*` |
| BT14(g.1) — vault UUID floor | PRE | §4.2.1 #13 | `F-PRE-13.*` |
| L-001 — operator final-review (VERIFY wins over DISCOVER analogue) | Sign-off | §4.9 | Sign refusal |
| S2 — HIGH-severity operator re-type | ledger write | §4.7.4 | `F-PRE-10.admin_risk_missing_retype` (sub-tag candidate, filed §10) |
| S5 — `router.yaml` signed-commit | PRE | §4.2.1 #2 | `F-PRE-02.*` |
| S9 — source-tag discipline (DOC_SOURCED / USER_DATA / UNSOURCED) | POST | §4.4.1 #4 | `F-POST-04.*` / `F-POST-05.*` / `F-POST-11.*` |
| S11a — per-org source-domain allowlist (dossier write-time) | consumed (Section 3 enforces) | n/a at Section 4 | n/a |
| S11b — cross-domain diversity for HIGH confidence (dossier write-time) | consumed (Section 3 enforces) | n/a at Section 4 | n/a |
| S11c — dossier lock (cite-time three-part check) | PRE + POST | §4.2.1 #14 + §4.4.1 #5 | `F-PRE-14.*` + `F-POST-08.*` |

Every Law and every Rule has an enforcement locus. Every BT and M entry with Section 4 ownership (per architecture M-prime annex) has a gate and a reason-tag.

---

## 12. Scope non-ownership

Explicit enumeration of what Section 4 does NOT own. If a reviewer flags an item below as a Section 4 gap, the correct response is "that's Section X's blueprint, not Section 4" with pointer to the owning section.

### 12.1 Reconciliation — "nine modules" vs "eleven files"

§3 opens with "Nine modules under `pipeline/logician/`" but the file table lists 11 paths. The reconciliation: the functional module count is nine (two gate files + seven subject-matter modules); the file count is eleven (nine functional modules + `__init__.py` + `cedar_eval.py`, which is a thin policy-loader helper shared across three of the functional modules). Header and table are not in conflict; the header counts responsibilities and the table counts files.

### 12.2 Section 1 (Sovereignty Envelope) — not Section 4

- Hash algorithm selection (SHA-3-512 + nonce per BT1).
- Org-root filesystem isolation (BT2).
- HMAC audit chain primitives.
- Session lifecycle.
- Key material storage and zeroization.
- BYOK key provisioning.
- Atomic flush primitive.
- `canonical_path`, `within_org_root`, `canonical_slug`.

Section 4 calls into these; it does not re-implement.

### 12.3 Section 2 (Vault Topology) — not Section 4

- Vault subtree directory layout.
- Vault-owned skill implementation (`vault-query`, `research-db-query`).
- FD broker protocol.
- Cedar `org_isolation` policy evaluation mechanism (Section 2 invokes; Section 4 loads the policy file and exposes the evaluation surface, but the per-read evaluation call-site is Section 2).
- M15 signed-commit verification of seed files at pipeline start (Section 2 walks; Section 4 consumes the verification result).
- BT14(g) volume-UUID + FS-file-ID identity tuple.
- Per-org vault initialization and operator-sign-off on new-org provisioning.

Section 4 surfaces PRE-gate failures routing through these (`F-VAULT-*` re-raised) but does not own the enforcement.

### 12.4 Section 3 (Scout) — not Section 4

- Six-channel DISCOVER (A–F).
- VERIFY stage tagging (VERIFIED_FIT / VERIFIED_NOT_FIT / UNVERIFIED / VERIFICATION_FAILED).
- REVIEW stage queue.
- Entity Research Pass (M11 / D.0) — dossier construction.
- S11a per-org source-domain allowlist (dossier write-time).
- S11b cross-domain diversity gate for HIGH confidence.
- BT12 Channel F domain pre-flight.
- Health tuple generation.
- `F-SCOUT-*` reason-tag emission.

Section 4 consumes these outputs and verifies Section 3's HMAC (M7) at PRE-gate; does not re-implement the Scout logic.

### 12.5 Section 5 (Pipeline) — not Section 4

- Section 5 is not yet drafted at Section 4 v1 authoring. Section 4 references it as the orchestrator that invokes the gate-runner entry points. Section 5 owns:
- Pipeline `router.py` / `pipeline.py` orchestration.
- Provider rate limiting (BT5).
- Revision-loop iteration counting + 3-iteration cap (Section J).
- Cron scheduling (Monday 08:30 fund-radar).
- Three-tab delivery mechanics.
- Claim extractor (invoked at POST-gate step 3).
- Scribe / Editor / Judge seat invocation and inter-seat wiring.
- Cross-family rigor enforcement at runtime (M5) — Section 4 is not the call-site; Section 5's router is.
- CLI surface (`tilth review --sign`, `tilth review --reject`, `tilth dossier confirm-cross-org`, etc.).
- Review-seat bypass activation (M13) — Section 4 provides `record_bypass_authorization` primitive; Section 5 decides when to invoke.
- Lessons learning integration with `lessons.json` / `lessons.md`.
- Interrupted-state resume policy (beyond the UNSOURCED check at PRE-gate).

### 12.6 Operator — not Section 4

- Admin-risk register authoring.
- Cedar policy authoring.
- `router.yaml` authoring.
- PROJECT_CONTEXT.md authoring (including filling `[NEEDED]` fields).
- Per-org domain allowlist authoring (`orgs/{slug}/dossier/source_domains.yaml`).
- Per-project BT10 window override (`orgs/{slug}/vault/config/bt10_window.yaml`).
- M13 bypass authorization decision.
- Operator sign-off on claim-evidence map.
- Operator acknowledgment of rigor-breach flags.

Section 4 enforces presence and signature-validity of operator-authored artifacts; it does not generate them.

### 12.7 Cedar — not Section 4 (partially)

- Cedar language semantics and evaluator implementation: the Cedar library (pinned by operator).
- Cedar entity schema authoring: operator.
- Cedar policy evaluation mechanism: Cedar library (Section 4 wraps the evaluation call via `cedar_eval.py`).

Section 4 is a Cedar consumer, not a Cedar author.

### 12.8 Out-of-model attacks — not Section 4's defence

Per Section 1 trusted-operator envelope (A1–A4) and architecture Section O, the following are explicitly OUT-OF-MODEL at v0.1 and not defended by Section 4:

- Compromised operator keyring (O.2).
- Hostile OS / kernel / privileged attacker (O.3).
- Multi-tenant cross-org timing observability (O.4 / A1 / A3).
- Hostile same-uid Python library.
- Physical seizure of the Golden Quill.
- Hostile operator.

A Red Team finding that asserts Section 4 must defend one of these must cite which of A1–A4 it believes is wrong.

---

## 13. v2 closure statement

### 13.1 Authoring intent

This v2 draft is the verification audit input. It is a narrow revision of v1: the only changes are the eight enumerated patches in the v1→v2 changelog above (header section). The aim is to land all v1 Bucket-A residuals and operator-elected Bucket-B items with zero scope creep — verification rounds are not authoring rounds.

### 13.2 Upstream lock dependencies (v2)

Section 4 v2 is authored against:
- Architecture v5-r8 LOCKED 2026-04-16.
- Section 1 LOCKED v5 2026-04-17.
- **Section 2 LOCKED v7 2026-04-18 (upgraded from v4 LOCKED 2026-04-17).** v7 adds: §4.10.1 .write.lock invariant block; §4.10.2 append-CAS primitive (`write_mode="append-cas"`, `expected_current_file_hash` kwarg, `F-VAULT-CAS-HEAD-MISMATCH`); §4.10.3 kernel-atomic write-if-absent (`write_mode="write-if-absent"`, Linux renameat2/macOS renamex_np, `F-VAULT-WRITE-EXISTS`); §4.10.4 belt-and-suspenders post-gate allowlist hook with five-intent allowlist table + four reason-tags + step 4.5 type-validation preamble.
- Section 3 LOCKED v5 2026-04-17.

Both Bucket-A v1 fixes (A-v1-01 admin-risk CAS, A-v1-02 claim-evidence write-if-absent) consume Section 2 v7 primitives directly. The v2 draft has zero Bucket-A papering-over-missing-primitive: every v2 fix calls a primitive that exists at the cited subsection of locked Section 2 v7.

### 13.3 v1 residual closure summary

v2 closes the following from v1:
- **A-v1-01** (admin-risk ledger race) — closed by §4.7.3 step 8 CAS call + property test §9.6.2.
- **A-v1-02** (claim-evidence version collision) — closed by §4.5 step 3 write-if-absent call + property test §9.6.3.
- **B-v1-01** (stale dossier-verify cache) — closed by §8.1 `DOSSIER_VERIFY_CACHE_TTL_MINUTES = 0` + §10 F-OQ-09 resolution note.
- **B-v1-02** (sentence-tokenizer abbreviation bypass) — closed by §4.6.1 v2 amendment (operator-extension list + full-text fallback).
- **B-v1-03** (missing F-BT10-03 property test) — closed by §9.6.1.
- **B-v1-04** (missing failure sub-tags) — closed by §6.1 inline (F-PRE-21/22) + §6.7 inline (F-BT13-03 two new sub-tags).
- **C-v1-01** (key-rotation note) — closed by §4.5.2 v2 amendment (cross-rotation operator confirmation).
- **C-v1-02** (non-English drafts) — closed by §10 F-OQ-01 v0.2 deferral.
- **C-v1-03** (semantic similarity) — closed by §10 F-OQ-02 string-overlap-only confirmation.
- **C-v1-04** (sign-off UX) — moved to Section 5 blueprint scope.

ARCH-06 (Section 2 architectural surface for write-side intent integrity) is closed by Section 2 v7 §4.10.4 belt-and-suspenders hook itself, which is exactly the defence-in-depth the Red Team called for at v1. No Section 4 v2 action required.

### 13.4 Pass condition for v2 lock

Per L-005 verification round:
- **Editor:** READY_TO_LOCK with no resurfaced fixes from v1; no new fixes introduced by v2 itself.
- **Judge:** total ≥ 85; every mechanism `covered`; every law `covered`; every autonomy rule `covered`; every upstream interface `preserved` against Section 2 v7 (not v4); `top_3_blockers: []`.
- **Red Team:** READY_TO_LOCK with zero Bucket-A residuals AND A-v1-01/A-v1-02 both confirmed CLOSED in body; no new Bucket-B introduced by v2 narrow edits.

If any of the three seats finds residual Bucket-A, v2 fails verification and v3 (or escalation) opens.

### 13.5 Honest gaps awaiting Thesis Team input (v2)

- The claim extractor itself — Section 5 property; v2 unchanged from v1.
- Section 5 orchestrator's invariant that it never invokes Section 4 mid-loop — v2 unchanged from v1.
- Cedar library choice and version pinning — operator authorship; v2 unchanged from v1.
- Admin-risk register initial content — operator authorship; v2 unchanged from v1.

### 13.6 Authoring note (v2)

This v2 draft was written in one Cowork session on 2026-04-18 by the operator against the v7-locked Section 2 substrate. It is submitted for the verification round. Next steps: Editor / Judge / Red Team audit → synthesis → LOCK at v2 if pass condition met; v3 narrow revision if Bucket-A residual surfaces.

Draft ends.
