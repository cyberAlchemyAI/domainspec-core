# Blueprint Section 3 — Scout (v5, LOCKED 2026-04-17)

**Status:** LOCKED v5 — STRICT PASS bar met on all three Thesis Team axes. Editor=READY_TO_LOCK, Judge=PASS 100/100 (every dimension 10/10; `top_3_blockers: []`), Red Team=READY_TO_LOCK (0 Bucket-A, 0 legitimate Bucket-B; 5 MED-tagged findings self-downgrade in the Red Team's own fix-direction column — 1 ARCHITECTURAL → ARCH-04 queue, 2 LOW → out-of-model, 1 DOCUMENT → Bucket-C, 1 LOW → spec-misread). Operator (Josh Inklovich) elected Option B at v4→v5 — "most stable secure efficient effective foundation" + "no floating follow-ups" — so the Section 3 substrate feeding into Sections 4+ has zero known-but-deferred Bucket-B items. v5 closes the four legitimate v4 Bucket-B residuals (B-v5-01..04) under existing §7.16 AST rules and existing failure codes, each a ≤ 5-line edit. No new failure codes, no new §8 constants, no new mechanisms, no architectural amendments. ARCH-02 + ARCH-03 remain filed against v5-r8 at `pipeline/validation/architecture_v0.1_findings_from_section_03/{ARCH-02.md, ARCH-03.md}` (unchanged); ARCH-04 (bounded module-size for cross-module `ast.parse`) filed from RT-v5-MED-01. Audit artefacts: `pipeline/validation/blueprint_section_03_2026-04-17/{02_editor_audit_v{1..5}.md, 03_judge_score_v{1..5}.json, 04_red_team_challenge_v{1..5}.md, 05_synthesis_v{1..5}.md}`. Post-lock Bucket-C deferred-hardening list at `pipeline/validation/section_03_deferred_hardening_post_lock.md`.

### Original v5 authoring context (preserved for audit trail)

**Status at authoring:** DRAFT v5 — operator-escalation round (past the 4-round silent-revision cap). Operator directive: "most stable secure efficient effective foundation" + "no floating follow-ups" → close the four v4 Red Team residuals triaged as legitimate Bucket-B in `05_synthesis_v4.md` before lock.
- v1 round closed 2026-04-17 with Editor=READY_TO_LOCK, Judge=PASS 100/100, Red Team=REQUIRES_MAJOR_MITIGATIONS (6 CRIT + 8 MED + 3 LOW + 2 ARCHITECTURAL + 3 out-of-model).
- v2 round closed 2026-04-17 with Editor=READY_TO_LOCK, Judge=PASS 100/100, Red Team=REQUIRES_MAJOR_MITIGATIONS (every v1 A-01…A-14 replay closed; 2 CRIT + 4 HIGH + 7 MED + 3 LOW residual).
- v3 round closed 2026-04-17 with Editor=READY_TO_LOCK, Judge=PASS 10/10 on every dimension, Red Team=REQUIRES_MINOR_FIXES (every v2 A-01…A-14 replay preserved + every v3 A-v3-01…A-v3-10 replay closed; 0 CRIT + 0 HIGH + 3 MED Bucket-B + 1 LOW Bucket-C).
- v4 round closed 2026-04-17 with Editor=READY_TO_LOCK, Judge=PASS 100/100, Red Team=REQUIRES_MAJOR_MITIGATIONS (every v2+v3 replay preserved + every v4 A-v4-01..03 replay closed; on honest triage: 4 legitimate Bucket-B + 3 Bucket-C residuals, rest were overreach / out-of-model / factually wrong / restatements of v4's own defence-in-depth framing).

v5 closes every legitimate v4 Bucket-B residual within the v5-r8 envelope (no architectural amendment). All four residuals are narrow edits (≤ 5 lines each) under existing AST rules or existing failure codes; no new failure code is introduced. ARCH-02 and ARCH-03 filed against v5-r8 at `pipeline/validation/architecture_v0.1_findings_from_section_03/{ARCH-02.md, ARCH-03.md}` — unchanged from v2/v3/v4.

Audit artefacts: `pipeline/validation/blueprint_section_03_2026-04-17/{02_editor_audit_v[1234].md, 03_judge_score_v[1234].json, 04_red_team_challenge_v[1234].md, 05_synthesis_v[1234].md}`.

**v5 changelog summary** (authoritative map to §X.Y where each new Bucket-B fix lands — four narrow edits, no architectural amendment):

- B-v5-01 (RT-v4-HIGH-04, env-var-derived `Final[bool]` admitted by AST-PREFLIGHT-DOMINATES-FD-REQUEST static-SSA check) → §7.16 — the refined dominance walker now requires the `Final[bool]` initializer to be a literal `True`/`False` or a constant expression with no `ast.Call`, `ast.Attribute`, `ast.Subscript`, or `ast.Name` references whose binding is itself non-literal. Rejects `Final[bool] = bool(os.environ.get("ENABLE_PREFLIGHT"))` and all env-var / function-call / attribute-load derived initializers. Narrow ≤ 5-line edit to the CFG walker. No new failure code.
- B-v5-02 (RT-v4-MED-01, alias-walker non-termination on self-referential or adversarially long alias chains) → §7.16 — the fixed-point alias-resolution loop gains a `MAX_ALIAS_WALKER_STEPS = 1000` iteration cap; if the fixed-point is not reached within the cap the walker aborts, the module is rejected with a new reason-tag on the existing AST-rule failure path, and the blueprint invariant ("alias walker is decidable on every acceptable module") is documented alongside. Narrow edit to the walker loop. No new failure code.
- B-v5-03 (RT-v4-MED-02, imported `Final[bool]` guard may be mutated in the originating module) → §7.16 — the static-SSA check extends to resolve imported names to the originating module's AST literal: when the guard name is introduced via `from <mod> import <name>` and `<name>` is declared `Final[bool]` in `<mod>`, the walker `ast.parse`s `<mod>` and re-applies the literal-initializer check there; if the originating module's binding fails the check, the consuming module is rejected. Module lookups are bounded to the Scout package (`pipeline.scout.*`) and Section 2 (`pipeline.section_02.*`) import surface — no arbitrary filesystem walk. Narrow static-analysis enhancement. No new failure code.
- B-v5-04 (RT-v4-MED-03, `_drain_parser_buffer` assumes `parser.raw_data` attribute name) → §4.5 + §6.5 + §7.16 — the drain helper now tests `hasattr(parser, "raw_data")` first; if present it replaces the bytearray as before; else if `hasattr(parser, "reset")` it calls `parser.reset()`; else it emits the new reason-tag `F-SCOUT-E-03.drain_api_missing` and the feed is flagged FAILED (admin-risk MEDIUM — feedparser API drift is a real risk on a long-lived client). `F-SCOUT-E-03.buffer_drained` is emitted when the drain actually succeeded via either path. Narrow ≤ 5-line edit in `channel_e_rss.py` plus a new reason-tag.

**v4 changelog summary** (retained for traceability — every item shipped in v4 and verified landed in the v4 Red Team replay):

- A-v4-01 (RT-v3-MED-01, Channel E parser-internal pre-buffer of entry 101 weakens memory bound) → §4.5 + §6.5 + §7.16 — `_drain_parser_buffer(parser)` called immediately after `break`; reads-and-discards any residual HTTP chunks; zeros the parser's `raw_data` bytearray; new reason-tag `F-SCOUT-E-03.buffer_drained` emitted alongside `.streaming_break` / `.post_fetch_break`; new property-test under §7.16. Narrow ≤ 5-line edit plus helper; no new failure code.
- A-v4-02 (RT-v3-MED-02, AST-PREFLIGHT-DOMINATES-FD-REQUEST rejects benign conditional pre-flights) → §7.16 — dominance walker refined to admit import-time-static guard shapes: `if <Final[bool]>:` and single-assignment module constants; non-static conditional guards still fail. No new failure code.
- A-v4-03 (RT-v3-MED-03, AST-NO-INDIRECT-VAULT-READ bypassable via import-alias rebinding) → §7.16 — alias walker resolves `from pipeline.section_02 import vault_read as vr`, `import pipeline.section_02 as sec; vr = sec.vault_read`, and direct-rebinding aliases transitively; ban on indirect access enforced against the full alias set. Three additional property-tests under §7.16. Defence-in-depth (runtime `_assert_intent_matches` already catches). No new failure code.

**v3 changelog summary** (retained for traceability — every item shipped in v3 and verified landed in the v3 Red Team replay):

- A-v3-01 (RT-v2-HIGH-01 + MED-02 + LOW-02, VERIFY truncation bias via crafted candidate_id) → §4.7 + §8 + §6 — tiebreak uses per-run `run_tiebreak_seed` XOR `sha3_512(candidate_json)[:16]`; seed recorded in SignedHealthTuple `run_entropy` field; overflow ratio > 0.25 DEGRADES VERIFY; `F-SCOUT-V-05` reason-tag `.truncation_degrades` + new `F-SCOUT-V-06`.
- A-v3-02 (RT-v2-HIGH-02 + MED-07, unbounded `_REVIEW_DECISION_LOCKS` growth + contention) → §4.8 + §8 — striped 64-slot lock array `_REVIEW_DECISION_LOCK_STRIPES`; memory O(stripes) not O(candidates); new §8 `SCOUT_REVIEW_LOCK_STRIPES = 64`.
- A-v3-03 (RT-v2-CRIT-01 + MED-06, AST regression bypass via getattr/partial/setattr) → §7.16 — three new AST rules `AST-NO-INDIRECT-VAULT-READ`, `AST-NO-SETATTR-OPERATOR-DECISION`, `AST-NO-EVAL-IN-SCOUT`; three property-tests exercise evasions.
- A-v3-04 (RT-v2-CRIT-02 + MED-01, policy vault_read intent silently tolerated) → §4.6 + §6.6 — explicit post-read `.strip()`-normalised equality check on `IdentityTuple.intent` after every Scout `vault_read`; new `F-BT12-07`.
- A-v3-05 (RT-v2-HIGH-03, Channel D per-adapter total unbounded) → §4.4 + §8 + §6.4 — new §8 `CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER = 500`; per-adapter cumulative counter; new `F-SCOUT-CHD-03`.
- A-v3-06 (RT-v2-HIGH-04, dossier partial-read race at exact boundary) → §4.9 + §6.9 — replace two-read with `os.fstat(fd).st_size` BEFORE `os.read`; `F-SCOUT-D-02` reason-tag `.fstat_size_gt_max`.
- A-v3-07 (RT-v2-MED-03, custom adapter can call `fd_broker.request_fd` directly) → §7.16 — new AST rule `AST-PREFLIGHT-DOMINATES-FD-REQUEST` enforces CFG-dominance of `_preflight_channel_f` over every Channel F `fd_broker.request_fd`.
- A-v3-08 (RT-v2-MED-04, Channel E chunked-stream break misses entry 101) → §4.5 + §7 — streaming `feedparser` iteration; break on entry-token yield, not after full entry parse; chunked-feed regression test; `F-SCOUT-E-03` reason-tag `.streaming_break`.
- A-v3-09 (RT-v2-MED-05, operator-controlled Channel C slug collision) → §2.1 + §4.3 — `feed_or_adapter_id` namespaced (`"portal:"`, `"aln:"`, `"rss:"`, `"api:"`); `register_portal` rejects duplicate canonical slug at registration; new `F-SCOUT-C-03`.
- A-v3-10 (RT-v2-LOW-03, `os.urandom` short read) → §4.10 — `_fresh_urandom(n)` helper asserts length, retries once, then raises `F-SCOUT-H-03.urandom_short_read`.

---

**v2 changelog summary** (retained for traceability — every item shipped in v2 and verified landed in the v2 Red Team replay):

- A-01 (CRIT-01, Channel A nonce non-release on failure) → §4.1 step 6 `try/finally` wraps FD + request + retry; `F-SCOUT-A-03` reason-tag extended.
- A-02 (CRIT-02, Channel B IdentityTuple mismatch not aborting) → §4.2 new `F-SCOUT-B-04` hard-fails the file and flips Channel B to FAILED.
- A-03 (CRIT-03, TOCTOU race in `sign_off_dossier`) → §4.9 `vault_write` of sign-off record moved INSIDE the FD-holding `with` block; O_NOFOLLOW + re-fstat immediately before write; `F-SCOUT-D-01`.
- A-04 (CRIT-04, unbounded Channel D candidate creation) → §4.4 per-page cap `CHANNEL_D_MAX_CANDIDATES_PER_PAGE = 200` applied BEFORE append; new `F-SCOUT-CHD-02`; §8 constant added.
- A-05 (CRIT-05, Channel E RSS truncation after parse) → §4.5 `CHANNEL_E_RUNAWAY_MAX = 100` enforced DURING iteration; `F-SCOUT-E-03` reason-tag added.
- A-06 (CRIT-06, FD leak on Channel F pre-flight failure) → §4.6 explicit ordering: pre-flight → FD request → `try/finally` release on every exit; click-through hop same discipline; `F-SCOUT-F-04` reason-tag added.
- A-07 (MED-01, Channel B malformed-row threshold edge) → §4.2 threshold `> 10%` → `>= 10%`.
- A-08 (MED-02, Channel F policy read bypasses vault) → §4.6 `_load_channel_f_policy` routes through `vault_read` with `intent="channel-f-policy-read"`; new `F-BT12-05`.
- A-09 (MED-03, VERIFY thread-pool exhaustion) → §4.7 + §8 new `SCOUT_CANDIDATE_VERIFY_CAP = 1000`; pre-VERIFY truncation by `fit_score_cached`; new `F-SCOUT-V-05`.
- A-10 (MED-04, operator-decision race) → §4.8 per-(slug, candidate_id) `threading.Lock()` around read-check-write; `F-SCOUT-R-04` (unchanged).
- A-11 (MED-05, candidate_id collision across feeds) → §2.1 hash input expanded from `{channel, source_key}` to `{channel, feed_or_adapter_id, source_key}`.
- A-12 (MED-06, run_id collision on clock glitch) → §4.10 run_id derivation includes `time.monotonic_ns()` + `os.urandom(8)`; new `F-SCOUT-H-03`.
- A-13 (MED-07, dossier size off-by-one) → §4.9 strict `>` enforcement; §7 unit test at 5 MB + 1 byte boundary; `F-SCOUT-D-02` reason-tag.
- A-14 (MED-08, IDN homograph in BT12) → §4.6 `_registrable_domain` normalises host to ASCII Punycode before eTLD+1 extraction; new `F-BT12-06`.
- ARCH-02 (S10a enforcement locus) → filed; v2 retains Section 2 write-time locus; §7 adds a polarity-inverted defence-in-depth unit test.
- ARCH-03 (health-tuple missing `NOT_OPTED_IN` state) → filed; v2 retains three-state schema per v5-r8; new §10 F-OQ-11 documents muddied-signal limitation.

**Parent architecture:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` (v5-r8 LOCKED 2026-04-16). **Parent Section 2:** `pipeline/blueprint/v0.1/section_02_vault_topology.md` (LOCKED v4 2026-04-17).

**Trust model:** trusted-operator single-client-per-Golden-Quill (A1–A4 carried from Sections 1 and 2). A3 multi-tenant escape is OUT-OF-SCOPE for v0.1.

**Dependencies (verified):**
- Section 1 (Sovereignty Envelope) — LOCKED 2026-04-17 at v5. Section 3 consumes: `Session`, `start_session`/`end_session`, `resolve_keystore()`, `KeyStore.retrieve()` → `SecretBytes`, `sign_health_tuple(session, tuple_bytes)` (M7 primitive), `hmac_sha3_512`, `canonical_slug`, `within_org_root`, `canonical_path`, `record_admin_risk`, `record_degradation`, `checkpoint`/`detect_interrupted`/`resume_or_discard`, `hmac_audit_writer`, `atomic_flush`, `nonce_registry.reserve`.
- Section 2 (Vault Topology + Enforcement Envelope) — LOCKED 2026-04-17 at v4. Section 3 consumes: `vault_read(path, intent, session_id, slug)`, `research_db_read(key, session_id, slug)`, `vault_write(path, bytes_, intent, session_id, slug)`, `fd_broker.request_fd`/`release_fd`, `IdentityTuple`, PRE-gate failure codes (`F-VAULT-*`, `F-GATE-*`).

**What Section 3 does NOT own:**
- HMAC key lifecycle (BT6 — Section 1 `keys.py`/`session.py`).
- M7 health-tuple signature **verification** (Section 4 — Logician).
- Filesystem-level Vault enforcement (Section 2 M14 family).
- Cedar policy text + policy enforcement (Section 4).
- Draft-time RFA re-verification (Section 4 calls Section 1 `reverify_rfa`).
- Entity-dossier cite-time lock verification (Section 4 calls Section 2 S11c verify).

---

## 1. Module inventory

Eleven modules under `pipeline/scout/`. No module depends on any sibling module by more than its narrow public API. All imports from Sections 1 and 2 flow through published surfaces (see §3.2).

| # | Path | Purpose | Owns |
|---|------|---------|------|
| 1 | `pipeline/scout/__init__.py` | Package re-exports and version | Public surface |
| 2 | `pipeline/scout/channel_a_federal_apis.py` | Channel A — Grants.gov search2/fetchOpportunity, SAM.gov entities, USASpending awards | Federal-API backbone |
| 3 | `pipeline/scout/channel_b_cache.py` | Channel B — curated cached datasets via `vault_read` | Cache-backed DISCOVER rows |
| 4 | `pipeline/scout/channel_c_portals.py` | Channel C — seeded state + foundation portal fetchers | Per-portal adapters (registered) |
| 5 | `pipeline/scout/channel_d_program_pages.py` | Channel D — Federal program pages (ALN, CR advisories) | Program-page adapters |
| 6 | `pipeline/scout/channel_e_rss.py` | Channel E — RSS / Atom / newsletter watchlists | RSS adapters |
| 7 | `pipeline/scout/channel_f_websearch.py` | Channel F — client-material-driven web search (SearxNG default; Brave BYOK opt-in) + BT12 pre-flight | Web-search rails, per-org jurisdiction policy enforcement |
| 8 | `pipeline/scout/verify_stage.py` | STAGE 2 — live-synopsis elevation gate | VERIFIED_FIT / VERIFIED_NOT_FIT / UNVERIFIED / VERIFICATION_FAILED tagging |
| 9 | `pipeline/scout/review_stage.py` | STAGE 3 — human REVIEW queue and operator acceptance interface | Review queue schemas, operator acceptance record |
| 10 | `pipeline/scout/entity_research.py` | M11 / D.0 Entity Research Pass + S11a/b/c dossier hardening | Dossier writer, per-org domain allowlist, cross-domain diversity gate, operator sign-off |
| 11 | `pipeline/scout/health_tuple.py` | M7 call-site: assemble per-channel health tuple and sign via Section 1 `sign_health_tuple` | Tuple canonicalization, call-site to Section 1 HMAC primitive |

**Why 11 and not fewer.** Each channel family has distinct failure semantics (network posture, cache posture, RSS polling cadence, web-search provider routing). Collapsing Channels A–F into a single adapter would force per-family logic into branching inside one module, which is harder to audit and harder to replace one channel without touching another. BT12 pre-flight could live in `channel_f_websearch.py`; it is kept there (not split out) because it is a narrow dispatch gate bound to exactly one channel. VERIFY and REVIEW are separate modules because VERIFY is a per-row elevation gate while REVIEW is a queue + human ceremony; their failure recovery and test surfaces do not overlap.

**Why 11 and not more.** `health_tuple.py` is the sign-call-site only. Verification is Section 4. Session lifecycle lives in Section 1. A dedicated `scout_session.py` would be three functions thick and is folded into `__init__.py` + per-channel entry points. Dossier writing and entity research are one module (`entity_research.py`) because S11a/b/c are enforced at dossier-write boundary and separating them would leak internal state across module borders.

---

## 2. Data-structure schemas + on-disk layout

### 2.1 `Candidate`

DISCOVER-stage row produced by any of Channels A–F.

```python
@dataclass(frozen=True, kw_only=True)
class Candidate:
    candidate_id: str              # sha3_512(canonical_json({channel, feed_or_adapter_id, source_key}))[:24]
    channel: str                   # "A" | "B" | "C" | "D" | "E" | "F"
    feed_or_adapter_id: str        # channel-internal namespace with mandatory prefix (A-v3-09):
                                   #   channel A: "api:" + endpoint_name (e.g. "api:grants.gov")
                                   #   channel B: "cache:" + cache_source_slug
                                   #   channel C: "portal:" + canonical_slug(portal_slug)
                                   #   channel D: "aln:" + aln_number
                                   #   channel E: "rss:" + sha3_512(feed_url)[:16]
                                   #   channel F: "searxng:" + session.slug  (or "brave:" + session.slug)
                                   # Prefix is enforced at construction time (§4.N _build_candidate helpers
                                   # assert it); prevents operator-typo collisions (e.g. two Channel C
                                   # adapters registered with the same slug) AND cross-channel confusion
                                   # (e.g. a portal_slug that happens to equal an aln_number).
    source_key: str                # channel-internal unique key (e.g., Grants.gov opportunity_id)
    title: str
    funder: str
    funder_kind: str               # "federal" | "state" | "foundation" | "intermediary" | "unknown"
    url: str                       # canonical landing URL (never a Channel F search URL)
    close_date_utc: str | None     # ISO-8601 UTC; None if not surfaced by the channel
    award_ceiling: int | None      # dollars; None if not surfaced
    award_floor: int | None        # dollars; None if not surfaced
    applicant_types: tuple[str, ...]  # RAW tokens from source; NOT normalized
    program_page_url: str | None
    fetch_timestamp_utc: str       # ISO-8601 UTC
    url_hash: str                  # sha3_512 of URL bytes
    content_hash: str | None       # sha3_512 of payload bytes at fetch time; None for Channel B (cache content-hash lives in cache row)
    fit_score_cached: int          # 0..100; cache-only heuristic; NOT a VERIFY decision
    cache_provenance: str | None   # vault path that produced this row, or None for live-fetched rows
```

`candidate_id` is deterministic across runs — same `channel` + same `feed_or_adapter_id` + same `source_key` → same id. This is how VERIFY deduplicates and how REVIEW operator-decisions persist across pipeline invocations. The `feed_or_adapter_id` tier of the triple prevents the RT-v1-MED-05 collision: two RSS feeds that happen to emit the same GUID value produce **distinct** candidate_ids because their `feed_or_adapter_id` (the feed URL hash) differs.

### 2.2 `VerificationVerdict`

VERIFY-stage output for a single Candidate.

```python
@dataclass(frozen=True, kw_only=True)
class VerificationVerdict:
    candidate_id: str
    verdict: str                   # "VERIFIED_FIT" | "VERIFIED_NOT_FIT" | "UNVERIFIED" | "VERIFICATION_FAILED"
    reason_code: str               # per §6 failure codes; "V-OK" on verified
    live_synopsis_url: str | None  # the exact live URL fetched; None if UNVERIFIED
    live_content_hash: str | None  # sha3_512 of live synopsis bytes
    fetched_at_utc: str | None     # ISO-8601; None if not fetched
    timeout_seconds: int           # hard timeout used (default 10, operator-configurable)
    eligibility_live: tuple[str, ...]  # applicant-type tokens pulled from live synopsis (NOT normalized)
    award_floor_live: int | None
    award_ceiling_live: int | None
    close_date_live_utc: str | None
    evidence_quote: str | None     # single grep-able quote from the live synopsis supporting the verdict
```

`verdict == "VERIFIED_FIT"` is the only state that elevates a Candidate to CRITICAL-fit for REVIEW. All other states either downgrade, hold, or hard-fail the row.

### 2.3 `HealthTuple` and `SignedHealthTuple`

Per-channel health per Scout run. Signed by Section 1 `sign_health_tuple`.

```python
@dataclass(frozen=True, kw_only=True)
class HealthTuple:
    session_id: str
    slug: str
    run_id: str                    # sha3_512(session_id || run_wall_ns)[:24]
    run_wall_ns: int
    channel_a: str                 # "OK" | "DEGRADED" | "FAILED"
    channel_b: str
    channel_c: str
    channel_d: str
    channel_e: str
    channel_f: str
    channel_a_endpoints: dict[str, str]  # {"grants.gov": "OK", "sam.gov": "OK", "usaspending.gov": "OK"}
    backbone_failed: bool           # True iff all three Channel A endpoints FAILED


@dataclass(frozen=True, kw_only=True)
class SignedHealthTuple:
    tuple_canonical: bytes          # canonical JSON of HealthTuple
    hmac_sha3_512: bytes            # 64 bytes from Section 1 sign_health_tuple
    signed_at_utc: str
    hmac_key_id: str                # Section 1 session hmac_key_id — for verifier audit
```

`tuple_canonical` is produced by `canonical_json(HealthTuple)` with sorted keys, no whitespace, UTF-8 NFC. Scout never signs raw `HealthTuple` bytes — only the canonicalized form, so verifier canonicalization is identical.

### 2.4 `ReviewQueueItem`

```python
@dataclass(frozen=True, kw_only=True)
class ReviewQueueItem:
    candidate_id: str
    queued_at_utc: str
    queued_by_verdict: str          # "VERIFIED_FIT"
    candidate_snapshot: Candidate   # frozen at queue time
    verification_snapshot: VerificationVerdict
    fit_rationale: str              # Scout-generated; plain text; NOT a Scribe draft
    operator_decision: str | None   # "ACCEPT" | "REJECT" | "HOLD" | None if not yet decided
    operator_decided_at_utc: str | None
    operator_decision_reason: str | None
```

`operator_decision == None` means REVIEW has not yet acted. Only `ACCEPT` flows downstream to Scribe.

### 2.5 `EntityRosterEntry` + `EntityDossier` + `EntityClaim`

```python
@dataclass(frozen=True, kw_only=True)
class EntityRosterEntry:
    entity_slug: str                # canonical per §4.4
    display_name: str
    kind: str                       # per D.0 taxonomy: person_lead | person_partner | person_referenced | org_applicant | org_partner | org_referenced | product | publication
    seed_urls: tuple[str, ...]      # operator-provided starting points; may be empty
    added_by: str                   # "operator" | "scout_proposal_accepted"
    added_at_utc: str


@dataclass(frozen=True, kw_only=True)
class EntityClaim:
    claim_id: str                   # sha3_512(entity_slug || claim_text_normalized)[:24]
    claim_text: str                 # plain-text assertion
    source_url: str
    source_registrable_domain: str  # eTLD+1 of source_url
    fetched_at_utc: str
    url_hash: str                   # sha3_512 of URL bytes
    content_hash: str               # sha3_512 of fetched bytes
    evidence_quote: str             # grep-able quoted sentence from source
    confidence_tier: str            # "HIGH" | "MEDIUM" | "LOW"
    corroborating_claim_ids: tuple[str, ...]  # other claim_ids whose source is a DIFFERENT registrable domain and whose claim_text normalizes identically; S11b lives here


@dataclass(frozen=True, kw_only=True)
class EntityDossier:
    entity_slug: str
    roster_entry: EntityRosterEntry
    claims: tuple[EntityClaim, ...]
    dossier_written_at_utc: str
    dossier_content_hash: str       # sha3_512 of canonical markdown rendering
    operator_signoff: "DossierSignoff | None"  # None = UNSOURCED per Law 5


@dataclass(frozen=True, kw_only=True)
class DossierSignoff:
    signed_at_utc: str
    operator_id: str
    signed_canonical_path: str      # after canonical_path()
    signed_inode: int
    signed_content_hash: str        # must match EntityDossier.dossier_content_hash
    operator_signature: bytes       # HMAC-SHA3-512 with `tilth.dossier.signoff.hmac.v1` key
    expires_at_utc: str             # dossier_written_at_utc + 90 days (default)
```

### 2.6 `SourceDomainAllowlist` (S11a)

```python
@dataclass(frozen=True, kw_only=True)
class SourceDomainAllowlist:
    slug: str
    allowlisted_registrable_domains: frozenset[str]  # eTLD+1 only
    last_updated_at_utc: str
    last_updated_by_operator_id: str
```

File: `orgs/{slug}/dossier/source_domains.yaml`. Read by `entity_research.py` at dossier-write time.

### 2.7 `ChannelFJurisdictionPolicy` (BT12)

```python
@dataclass(frozen=True, kw_only=True)
class ChannelFJurisdictionPolicy:
    slug: str
    opt_in: bool                    # default False — NO domains allowed until operator opts in
    allowed_jurisdictions: frozenset[str]  # ISO-3166-1 alpha-2 codes the operator approved
    disallowed_registrable_domains: frozenset[str]  # per-org explicit denylist (overrides allowed_jurisdictions)
    last_updated_at_utc: str
```

File: `orgs/{slug}/scout/channel_f_policy.yaml`. Read by `channel_f_websearch.py` before any outbound fetch.

### 2.8 On-disk layout

```
pipeline/scout/
├── __init__.py
├── channel_a_federal_apis.py
├── channel_b_cache.py
├── channel_c_portals.py
├── channel_d_program_pages.py
├── channel_e_rss.py
├── channel_f_websearch.py
├── verify_stage.py
├── review_stage.py
├── entity_research.py
└── health_tuple.py

orgs/{slug}/
├── dossier/
│   ├── entities/{entity_slug}.md            # written by entity_research.py via vault_write
│   ├── entities/{entity_slug}.signoff.json  # written by review_stage.py via vault_write
│   └── source_domains.yaml                  # operator-maintained; read-only to Scout
├── scout/
│   ├── channel_f_policy.yaml                # operator-maintained
│   ├── review_queue/{candidate_id}.json     # REVIEW queue items
│   └── run_log/{run_id}.health.json         # signed health tuple per run

vault_shared/
├── cached_opportunities/                    # Channel B source; written by curation, read by Scout via vault_read
└── research_db/                             # research-db-query read surface
```

Per-org `scout/` and `dossier/` are inside the org root. Scout never writes outside `within_org_root(session.slug)` except through Section 2's `vault_read` for `vault_shared/`. Cross-org writes are PRE-gate aborts at Section 2's M14.

Per Law 3 + S10a: cached opportunity rows under `vault_shared/cached_opportunities/` MUST NOT carry any org identifier. Channel B materializes per-org fit only at read time. This invariant is a Section 2 write-time check (S10a) — Section 3 consumes the guarantee.

---

## 3. Interfaces in / out

### 3.1 `pipeline.scout.__init__`

```python
from .channel_a_federal_apis import discover_channel_a
from .channel_b_cache import discover_channel_b
from .channel_c_portals import discover_channel_c
from .channel_d_program_pages import discover_channel_d
from .channel_e_rss import discover_channel_e
from .channel_f_websearch import discover_channel_f
from .verify_stage import verify_candidate, verify_all
from .review_stage import (
    enqueue_for_review, read_review_queue, record_operator_decision,
    ReviewQueueItem,
)
from .entity_research import (
    run_entity_research, read_entity_dossier, sign_off_dossier,
    EntityRosterEntry, EntityDossier, EntityClaim, DossierSignoff,
)
from .health_tuple import assemble_and_sign_health_tuple, SignedHealthTuple

__version__ = "0.1.0"
__all__ = [...]  # explicit, no dynamic exports
```

No module-level side effects at import. Every function takes an explicit `session: Session` (Section 1). No global state.

### 3.2 Primitives consumed from Section 1

- `Session` (§3.3) — carries `slug`, `session_id`, `hmac_key_id`, `operator_id`.
- `resolve_keystore()` — for dossier sign-off HMAC via `tilth.dossier.signoff.hmac.v1`.
- `sign_health_tuple(session, tuple_bytes: bytes) -> bytes` — §4.6 M7 primitive. Scout does not open the keystore directly.
- `hmac_sha3_512(key: memoryview, data: bytes) -> bytes` — crypto primitive.
- `canonical_slug(s: str) -> str` — slug canonicalization (M3).
- `within_org_root(path, slug)` — TOCTOU-closed canonical-path-plus-inode check.
- `canonical_path(path)` — symlink-resolved path; used at dossier sign-off.
- `record_admin_risk(session, entry_kind, severity, payload)` — flagged-term admin entries.
- `record_degradation(session, event_kind, seat, reason_code, ...)` — per-channel degradation events.
- `checkpoint(session, payload)` / `detect_interrupted` / `resume_or_discard` — save state on success AND failure (Autonomy Rule 1).
- `hmac_audit_writer(ledger_path, payload)` — append-only hash-chained writes for Scout run logs.
- `atomic_flush(tmp, final)` — used for review-queue persistence.
- `nonce_registry.reserve(nonce_hex)` — replay-protected outbound Channel A request tokens (federal APIs that require a nonce).

### 3.3 Primitives consumed from Section 2

- `vault_read(path, intent="read", session_id, slug) -> bytes + IdentityTuple` — all Channel B + C + D cache reads.
- `research_db_read(key, session_id, slug) -> bytes + IdentityTuple` — thin wrapper over the research-db-query skill for shared research briefs.
- `vault_write(path, bytes_, intent="write", session_id, slug) -> ack` — only way Scout writes. Used by:
  - `review_stage.py` — review queue item writes (`intent="review-queue-write"`).
  - `entity_research.py` — dossier body writes (`intent="dossier-body-write"`) and sign-off writes (`intent="dossier-signoff-write"`).
  - `health_tuple.py` — signed-health-tuple writes to `orgs/{slug}/scout/run_log/` (`intent="scout-run-log-write"`).
- `fd_broker.request_fd` / `release_fd` — for any raw FD the seat momentarily holds (e.g., an HTTPS socket to a Channel A endpoint). The FD is obtained from the broker, not directly via `socket()`.
- PRE-gate failure-code constants `F-VAULT-*`, `F-GATE-*`, `F-MIRROR-*`, `F-WRAPPER-*` are propagated up unchanged.

Section 2 does NOT import from Section 3. The dependency is one-way, as with Section 1.

### 3.4 Surfaces offered to Section 4 (Logician)

- `SignedHealthTuple` object returned by `assemble_and_sign_health_tuple(...)` — Logician verifies and hard-aborts on mismatch per architecture line 270.
- `ReviewQueueItem` objects read via `read_review_queue(session)` — Logician's PRE-gate for "candidate must be in VERIFIED_FIT + REVIEWED_ACCEPTED state before Scribe drafts anything about it".
- `EntityDossier` + `DossierSignoff` read via `read_entity_dossier(session, entity_slug)` — Logician's PRE-gate for S11c dossier lock verification at cite time; Logician will call Section 2's `vault_read` directly for the bytes, then canonical_path + inode + content_hash verify against the signoff.

### 3.5 Surfaces offered to Section 5 (Pipeline)

- `discover_channel_*` six entry points — Pipeline invokes in parallel; each returns `list[Candidate]` + the per-channel health state that gets folded into the health tuple.
- `verify_all(session, candidates) -> list[VerificationVerdict]` — Pipeline invokes after union of the six DISCOVER results is assembled.
- `assemble_and_sign_health_tuple(session, channel_states) -> SignedHealthTuple` — Pipeline invokes after all six channels report.
- `enqueue_for_review(session, candidate, verdict, fit_rationale)` — Pipeline invokes for each `VERIFIED_FIT` verdict.
- `run_entity_research(session, roster: tuple[EntityRosterEntry, ...])` — Pipeline invokes at project-init and on operator-triggered refresh.

### 3.6 Lock-marker contract

Section 3 writes `vault_shared/section_03.lock.json` with the same schema as Section 2 §3.6 (operator-signed, binds architecture head hash + blueprint content hash + M15 ledger head + operator signature). Pipeline refuses to launch Scout if the lock is invalid. The lock is produced at the end of the final successful audit round and not before.

---

## 4. Mechanism implementations

All implementations are deterministic Python. No LLM calls inside Scout's DISCOVER, VERIFY, or dossier-write paths. Scout's operational-gears LLM affordances (fit rationales, claim extraction) are called from outside the mechanism boundary — see §9 for where.

### 4.1 Channel A — Federal APIs (`channel_a_federal_apis.py`)

Three parallel endpoints, each independently OK/DEGRADED/FAILED. `backbone_failed = True` iff all three are FAILED.

**Endpoints:**
- `grants.gov` — `POST /grantsws/rest/opportunities/search/` (search2 API) and `GET /grantsws/rest/opportunities/{id}` (fetchOpportunity). Used for both DISCOVER (search2 page sweep) and VERIFY (fetchOpportunity for the live synopsis).
- `sam.gov` — `GET /entity-information/v4/entities` for entity registration status. DISCOVER-side only; VERIFY uses Grants.gov if Grants.gov carries the record.
- `usaspending.gov` — `POST /api/v2/search/spending_by_award/` for historical award context. DISCOVER-side only.

**Request posture (every outbound Channel A request):**
1. Nonce reserved via `session.keys.nonce_registry.reserve(nonce_hex)`; rejected on duplicate.
2. FD obtained from Section 2's `fd_broker.request_fd(kind="https", host=target_host)`. Raw `socket()` is forbidden; PRE-gate catches it.
3. Per-host 10 s connect + 30 s read timeout. On timeout → endpoint state flips to FAILED for this run.
4. Per-host exponential retry with 3 attempts (1 s, 2 s, 4 s) for 5xx / connection-reset; 4xx never retried. DEGRADED after first retry; FAILED after third.
5. Response body hash recorded; body passed to the adapter's parser.
6. **A-01 / RT-v1-CRIT-01 closure:** steps 2–5 are wrapped in a `try/finally` that calls `fd_broker.release_fd(fd)` AND `session.keys.nonce_registry.release(nonce_hex)` on **every** exit path (success, timeout, 5xx exhausted, connection reset, non-retriable 4xx, any raised exception). Nonce release MUST happen before any retry decision so that a retry can reserve a fresh nonce without contending with the exhausted reservation. Reason tag `F-SCOUT-A-03` is extended to record whether the release path was "success", "timeout", "http_error", or "exception" — an un-released nonce is a hard bug, not a degradation.

```python
nonce_hex = _fresh_nonce()
session.keys.nonce_registry.reserve(nonce_hex)
try:
    fd = fd_broker.request_fd(kind="https", host=target_host)
    try:
        response = _do_request_with_retries(fd, ...)
        return _parse(response)
    finally:
        fd_broker.release_fd(fd)
finally:
    session.keys.nonce_registry.release(nonce_hex)  # F-SCOUT-A-03 path-tag
```

**DISCOVER output per endpoint:**
- `grants.gov.search2` → one `Candidate` per opportunity row in the paged response. `source_key = opp.id`. `close_date_utc`, `award_ceiling`, `award_floor`, `applicant_types` pulled from the search-result row. `content_hash` is sha3_512 of the response body that contained the row (not per-row — the page body, for audit chaining).
- `sam.gov.entities` → does NOT produce Candidates. Produces a cached entity-registration snapshot under `vault_shared/cached_entity_registrations/` (S10a: no org identifiers in cache content). Used by Logician later for eligibility PRE-gate.
- `usaspending.gov.awards` → does NOT produce Candidates. Produces a historical-award snapshot for context; written to `vault_shared/cached_awards_history/`.

**Endpoint health state transitions:**

```python
def _classify_endpoint_health(attempts: list[HTTPAttempt]) -> str:
    if all(a.succeeded for a in attempts):
        return "OK"
    if any(a.succeeded for a in attempts):
        return "DEGRADED"
    return "FAILED"
```

**Channel-A health aggregation:**

```python
def classify_channel_a(per_endpoint: dict[str, str]) -> str:
    # per_endpoint: {"grants.gov": "...", "sam.gov": "...", "usaspending.gov": "..."}
    if all(s == "OK" for s in per_endpoint.values()):
        return "OK"
    if all(s == "FAILED" for s in per_endpoint.values()):
        return "FAILED"
    return "DEGRADED"
```

`backbone_failed = (classify_channel_a(per_endpoint) == "FAILED")`. This is the hard-abort trigger per architecture line 271.

### 4.2 Channel B — Curated cached datasets (`channel_b_cache.py`)

Read-only. Zero network. Reads exclusively through Section 2's `vault_read`.

**Sources (all under `vault_shared/`):**
- `vault_shared/cached_opportunities/federal/*.jsonl`
- `vault_shared/cached_opportunities/state/*.jsonl`
- `vault_shared/cached_opportunities/foundation/*.jsonl`
- `orgs/{slug}/vault/subscribed_feeds/*.jsonl` — per-org subscription feeds; operator-curated.

**S10a invariant consumed.** Cached rows carry NO org-identifier fields. Scout treats cache rows as org-agnostic. Per-org fit computation (e.g., "is this funder likely to fund MycoSymbiotics Inc") is done at read time, never written back into the cache.

**Cache-only heuristic fit score.** `fit_score_cached` is a 0–100 heuristic based on category tags, scale band, and geography match. It is **never** a VERIFY decision; L-001 is literally "cache fit score ≠ elevation". `fit_score_cached >= 60` is the threshold for a row to enter VERIFY — below that, the row is still a Candidate but Pipeline can filter VERIFY workload.

**Cache freshness watermark.** Each cache file carries a `watermark_utc` in its header row. If `now_utc - watermark_utc > 14 days`, Scout records a MEDIUM `degradation` event with reason `cache_stale_channel_b` and tags the Channel B state as DEGRADED (not FAILED — the data is usable, just stale).

**Per-row failure:** malformed JSON → row skipped, `F-SCOUT-B-01` logged via `record_degradation`. Malformed rows do not flip channel state unless **>= 10%** of rows in a file are malformed, then DEGRADED. (A-07 / RT-v1-MED-01 closure: the threshold is inclusive so that an attacker cannot craft a file with exactly 10% malformed rows and remain OK.)

**A-02 / RT-v1-CRIT-02 closure — IdentityTuple mismatch on cache read is a hard-fail, not a degradation.** Every `vault_read` of a `vault_shared/cached_opportunities/*` file returns `(bytes, IdentityTuple)`. Scout validates that the IdentityTuple's `intent` is `"cache-read"` and that the Section 2-provided slug/session_id binding matches the current call's `session.slug` / `session.session_id`. If the IdentityTuple is malformed OR the binding mismatches, Scout raises `F-SCOUT-B-04 ChannelBIdentityTupleMismatch`, ABORTS the file (no further rows from that file are consumed), AND flips Channel B state to **FAILED** for the run. This is a hard-fail, NOT a degradation — a cache file whose vault-identity does not match cannot be trusted for any row.

### 4.3 Channel C — Seeded state + foundation portals (`channel_c_portals.py`)

Adapter-per-portal. Each adapter is a small function registered in a module-level **`OrderedDict` keyed by canonical slug**:

```python
PORTAL_ADAPTERS: "OrderedDict[str, Callable[[Session], list[Candidate]]]" = OrderedDict()

def register_portal(portal_slug: str):
    cslug = canonical_slug(portal_slug)  # Section 1 primitive; NFC + lowercase + strip
    def _wrap(fn):
        if cslug in PORTAL_ADAPTERS:
            raise ScoutConfigError(
                f"F-SCOUT-C-03: duplicate portal adapter canonical_slug={cslug!r} "
                f"(raw={portal_slug!r}); existing adapter={PORTAL_ADAPTERS[cslug].__qualname__}"
            )
        PORTAL_ADAPTERS[cslug] = fn
        return fn
    return _wrap
```

**A-v3-09 closure — canonical-slug registry + namespaced `feed_or_adapter_id`.** Duplicate detection runs at module-import time (registration), not at run-time, so an operator-typo collision is caught immediately and deterministically. Candidates built from a Channel C adapter set `feed_or_adapter_id = "portal:" + cslug`; the `"portal:"` prefix is asserted by the `_build_channel_c_candidate` helper and prevents accidental cross-channel collision with an ALN number or an RSS-feed URL hash that happens to equal a portal slug.

**Outbound posture same as Channel A** (FD broker, nonce, timeout, retry). Portals that require authentication (e.g., a foundation that gates its opportunities behind a login) are NOT adapted in v0.1 — Scout only consumes public portals.

**Portal state transitions:** per-adapter success/failure aggregated into a single Channel C state via the same `_classify_endpoint_health` rule. If ≥ 50% of registered portals FAILED → Channel C FAILED; any other partial failure → DEGRADED.

**Portal roster source:** `orgs/{slug}/scout/portals.yaml` — per-org opt-in list of portal slugs. No portal is auto-enabled. Operator adds portals by slug.

### 4.4 Channel D — Federal program pages (`channel_d_program_pages.py`)

Fetches from `sam.gov` Assistance Listing (ALN) pages and federal program pages linked from Grants.gov records. Same outbound posture as Channel A.

**DISCOVER output:** Candidates produced from program-page parse (often multi-opportunity pages that Grants.gov search2 does not paginate through). `channel == "D"`, `feed_or_adapter_id = "aln:" + aln_number` (the namespaced ALN of the program page that produced the row, A-v3-09), `source_key = opportunity_number_or_row_key_within_that_page`.

**A-04 / RT-v1-CRIT-04 closure — per-page candidate cap.** The parser applies `CHANNEL_D_MAX_CANDIDATES_PER_PAGE = 200` (pinned in §8) BEFORE any parsed row is appended to the run-level `candidates` list. If a single program-page fetch would yield more than 200 parsed rows, iteration breaks, the overflow count is recorded, and the page is flagged DEGRADED with `F-SCOUT-CHD-02 ChannelDPerPageCapReached` via `record_degradation`. Memory allocation never exceeds `200 × sizeof(Candidate)` per page regardless of attacker-controlled HTML size.

**A-v3-05 / RT-v2-HIGH-03 closure — per-adapter cumulative cap.** A single adapter can register many program pages (one per ALN). An attacker-controlled adapter that emits 50 pages each at the 200-per-page cap would still yield 10 000 Candidates and could OOM an 8 GB dev node before the VERIFY cap truncates. Channel D therefore maintains a per-adapter running counter `_channel_d_adapter_candidate_counts: dict[str, int]` (keyed by `aln:` prefix); on every would-be append, the counter is checked against `CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER = 500` (pinned in §8) BEFORE the append. If the adapter is at cap, the remaining Candidates from that and subsequent pages **within the same run** are dropped, the overflow count is recorded, and the adapter is flagged DEGRADED with `F-SCOUT-CHD-03 ChannelDPerAdapterCapReached` via `record_degradation`. The run-level Channel D state goes DEGRADED (not FAILED) — the other adapters still run.

**Channel D state:** OK if all registered program pages fetched; DEGRADED on any single fetch failure OR on any page hitting `F-SCOUT-CHD-02` OR on any adapter hitting `F-SCOUT-CHD-03`; FAILED only if all registered pages failed (rare — usually a network outage, which would also fail A and C).

### 4.5 Channel E — RSS / newsletter watchlists (`channel_e_rss.py`)

Polls per-org watchlist at `orgs/{slug}/scout/rss_watchlist.yaml`. Feed rows produce Candidates with `channel == "E"`. `content_hash` is sha3_512 of the feed entry body; `feed_or_adapter_id = "rss:" + sha3_512(feed_url)[:16].hex()` (namespaced per A-v3-09); `source_key = feed_entry_guid`. (The feed_or_adapter_id partition closes RT-v1-MED-05: two feeds that emit the same GUID value produce distinct candidate_ids.)

**Polling discipline:**
- Feed polled at most once per 15 minutes per run. Across runs, feeds are polled on Pipeline-level cadence.
- A feed with no new entries in 60 days → DEGRADED for that feed with reason `feed_stale_channel_e`, but not FAILED (newsletters legitimately go dormant).
- A feed whose TLS certificate is invalid → FAILED for that feed; adapter records `F-SCOUT-E-02` and continues with other feeds.
- **A-05 / RT-v1-CRIT-05 closure — runaway truncation happens DURING iteration, not after.** The parser iterates feed entries and increments a counter; on the 101st entry (`CHANNEL_E_RUNAWAY_MAX = 100` exceeded) the iterator exits with `break`. Excess entries are **never parsed into `Candidate` objects** and never touch memory. The feed is flagged DEGRADED with `F-SCOUT-E-03 ChannelERunawayFeedTruncated` via `record_degradation`. Memory allocation never exceeds `100 × sizeof(Candidate)` per feed regardless of attacker-controlled feed length.
- **A-v3-08 / RT-v2-MED-04 closure — streaming break on entry-token yield.** Channel E iterates the feed via a streaming parser (`feedparser.FeedParserDict` consumed one entry at a time from a chunked-body reader). The entries-seen counter is incremented on every **entry-start token** the parser yields, and the `break` is evaluated **immediately** at that token — not after the entry body has been fully deserialised into a dict. A crafted feed that inserts `<!-- pause -->` comments or otherwise causes the 101st entry to straddle a network chunk cannot defer the break: the first token of entry 101 triggers the break and the remaining bytes are drained and discarded without `Candidate` construction. Reason-tag on `F-SCOUT-E-03` is `.streaming_break` when the break fires mid-chunk; `.post_fetch_break` when the entire body was already buffered. §7 adds a regression test that feeds entry 101 as the first token in a second HTTP chunk and asserts zero `Candidate` objects are constructed beyond index 100.
- **A-v4-01 / RT-v3-MED-01 closure — explicit parser-buffer drain after break (memory-bound tightening).** The feedparser's internal chunked-input buffer may hold the still-undelivered raw bytes of entry 101 (and, in pathological chunkings, the leading bytes of entry 102+) at the instant the entry-start token for 101 is yielded and the break fires. To make the memory bound `100 × sizeof(Candidate) + O(1)` raw bytes hold strictly — not merely in the common case — Channel E **drains and zeroes the parser's internal buffer immediately after the break, before the function returns**. Concretely, after `break`, the code calls `_drain_parser_buffer(parser)` which (a) reads and discards any remaining chunks from the underlying HTTP stream to the socket's receive buffer limit (bounded by the existing per-feed read-timeout and by closing the FD after drain), and (b) zeroes the parser's internal buffer using a feedparser-version-safe dispatch (see B-v5-04 closure below for the exact attribute/method probe). The FD is released in the enclosing `try/finally` as before. Reason-tag on `F-SCOUT-E-03` is `.buffer_drained` and is emitted **in addition to** `.streaming_break` or `.post_fetch_break` when the drain ran successfully; absence of `.buffer_drained` on a truncation event is a hard bug. §7 adds a regression test that instruments the parser's `raw_data` attribute after break and asserts its length is zero and no `Candidate` object references entry-101 bytes via `content_hash` sampling. Narrow edit: ≤ 5 lines in `channel_e_rss.py` plus the `_drain_parser_buffer` helper; no new failure code. This is defence-in-depth against library-internal pre-buffering — candidate-selection correctness was never at risk.
- **B-v5-04 / RT-v4-MED-03 closure — feedparser-version-safe buffer drain.** The v4 helper assumed feedparser exposes a `raw_data: bytearray` attribute. The library may rename or drop that attribute in a future version (the Golden Quill is a long-lived client and feedparser ships minor-version renames). The v5 helper probes the API in a fixed dispatch order: (i) `if hasattr(parser, "raw_data"): parser.raw_data = bytearray()`; (ii) `elif hasattr(parser, "reset"): parser.reset()`; (iii) `else:` emit the new reason-tag `F-SCOUT-E-03.drain_api_missing`, flag the feed FAILED (not DEGRADED — the memory-bound invariant is load-bearing and cannot be silently skipped), and log `admin-risk MEDIUM feedparser_drain_api_missing` in the health tuple. `.buffer_drained` is emitted only when path (i) or (ii) ran successfully. The FD is still released in the enclosing `try/finally` on every exit path, including the `.drain_api_missing` path. Narrow ≤ 5-line edit to `channel_e_rss.py`; adds one reason-tag to the `F-SCOUT-E-03` sub-code list; no new failure code. Complements A-v4-01 as the same concern's stability floor against library API drift.

**Channel E state:** OK if all feeds OK or DEGRADED-stale; DEGRADED if any feed FAILED; FAILED if > 50% of feeds FAILED.

### 4.6 Channel F — Client-material-driven web search (`channel_f_websearch.py`)

The only channel that runs LLM- or operator-initiated queries. BT12 jurisdiction pre-flight gates every outbound fetch.

**Providers:**
- **Default:** SearxNG self-hosted on the Golden Quill. Localhost request; does not leave the machine; SearxNG in turn fetches from upstream engines per its own meta-search config.
- **Fallback:** Brave Search API BYOK, opt-in per `orgs/{slug}/scout/channel_f_policy.yaml`. Per-session operator disclosure required.

**BT12 pre-flight** (enforced on every outbound call, BEFORE the FD broker request):

```python
def _preflight_channel_f(session: Session, candidate_url: str) -> None:
    policy = _load_channel_f_policy(session)  # A-08: routes through vault_read
    if not policy.opt_in:
        raise ChannelFNotOptedIn(f"F-BT12-01: slug={session.slug} has not opted into Channel F")
    reg = _registrable_domain(candidate_url)  # eTLD+1, Punycode-normalized (A-14)
    if reg in policy.disallowed_registrable_domains:
        raise ChannelFJurisdictionReject(
            f"F-BT12-02: domain {reg} is on per-org denylist"
        )
    tld_jurisdiction = _jurisdiction_from_registrable_domain(reg)
    if tld_jurisdiction is None:
        raise ChannelFJurisdictionReject(
            f"F-BT12-03: domain {reg} has no known jurisdiction — default-deny"
        )
    if tld_jurisdiction not in policy.allowed_jurisdictions:
        raise ChannelFJurisdictionReject(
            f"F-BT12-04: domain {reg} jurisdiction {tld_jurisdiction} "
            f"not in allowed_jurisdictions {sorted(policy.allowed_jurisdictions)}"
        )
```

Default-deny per BT12: `opt_in=False` is the default, `allowed_jurisdictions=frozenset()` is the default, unknown jurisdiction → reject. Scout does NOT lazily-build a jurisdiction map; it consults a statically compiled table shipped with the package.

**A-08 / RT-v1-MED-02 closure — policy file loaded via vault_read.** `_load_channel_f_policy(session)` calls `vault_read(orgs/{session.slug}/scout/channel_f_policy.yaml, intent="channel-f-policy-read", session_id=session.session_id, slug=session.slug)` and parses the returned bytes. Direct filesystem open is forbidden (Scout's PRE-gate catches it). The identity-tuple returned by `vault_read` is checked exactly like any cache read: if malformed or mismatched, Scout raises `F-BT12-05 ChannelFPolicyVaultReadMismatch` and the pre-flight fails closed (Channel F stays OK-trivial for the run; no Channel F traffic occurs). This binds the policy file to the org root via Section 2's PRE-gate and closes the "write to the policy file to bypass BT12" attack.

**A-v3-04 / RT-v2-CRIT-02 + MED-01 closure — explicit post-read intent equality check.** After every `vault_read` call in the Scout package, the returned `IdentityTuple.intent` is compared for strict equality against the request intent, after NFC normalisation and whitespace stripping. The helper `_assert_intent_matches(identity, expected)` runs immediately after every `vault_read` in `channel_b_cache`, `channel_f_websearch._load_channel_f_policy`, `entity_research` (`source-allowlist-read`, `entity-roster-read`), and `verify_stage` (`rfa-reverify-read`). On any deviation — trailing whitespace, NFC drift, wrong intent returned by a hypothetically buggy vault — Scout raises `F-BT12-07 IntentMismatchPostRead` (Channel F path) or the corresponding `F-SCOUT-*-06` in other channels, and the downstream consumer fails closed. This is defence-in-depth: the trusted-operator threat model places Section 2 in the trusted set, but the equality check costs one comparison per `vault_read` call and forecloses a whole class of future Section-2 bugs or misconfigured vault implementations from silently bypassing Scout's intent-bound reads. Intent strings are declared as `Final[str]` module-level constants, so this is also a static check that the CALL-SITE intent matches the CONTRACT intent.

**A-14 / RT-v1-MED-08 closure — Punycode normalisation in `_registrable_domain`.** Every URL's host is parsed and normalised to ASCII Punycode (`idna.encode(host, uts46=True).decode("ascii")`) BEFORE eTLD+1 extraction. Denylist and allowlist comparisons happen exclusively in Punycode form. IDN homograph attacks (e.g., Cyrillic `а` vs Latin `a`) cannot slip past the allowlist because `_registrable_domain` sees the `xn--` form on both sides of the comparison. On invalid IDN input (`idna.IDNAError`), Scout raises `F-BT12-06 ChannelFURLPunycodeError` and the request is rejected as default-deny.

**SearxNG request path (A-06 closure — pre-flight strictly before FD acquisition; FD release in try/finally):**
1. BT12 pre-flight on the query's expected result-domain set (for SearxNG, that is itself localhost — pre-flight is trivially accepted for the search-URL dispatch, but each click-through URL is subject to pre-flight again before any body fetch). Pre-flight runs **before** any `fd_broker.request_fd` call for this request; a raised `ChannelFNotOptedIn` / `ChannelFJurisdictionReject` exits the path with zero FDs held.
2. FD broker `request_fd(kind="https", host="127.0.0.1", port=searxng_port)`.
3. POST query; parse JSON result set.
4. For each result URL the operator or Scribe wants to hydrate into a Candidate: BT12 pre-flight the result URL (**before** any second FD is requested), then fetch through a second FD.
5. All fetched bodies are sha3_512 hashed and recorded in the run audit.
6. **A-06 / RT-v1-CRIT-06 closure — FD release discipline.** Every `fd_broker.request_fd` in the Channel F path (both first-hop and click-through) is followed by a `try/finally` that calls `fd_broker.release_fd(fd)` on every exit: successful fetch, parse error, body-hash mismatch, TLS error, or a **later** pre-flight rejection on a subsequent click-through. A malicious sequence of rejections cannot exhaust the FD pool because no FD is ever held across a rejection boundary. Record `F-SCOUT-F-04 ChannelFFDReleasePathTag` on each release with one of `{success, fetch_error, parse_error, preflight_reject_after_acquire, exception}`.

**Brave BYOK path:** identical outer shape, but the first-hop FD is to `api.search.brave.com`, which requires `opt_in=True` + `BRAVE-BYOK` jurisdiction (US by default) in `allowed_jurisdictions`.

**Per-session disclosure record:** each outbound Channel F request (both hops) appends a row to `orgs/{slug}/scout/run_log/{run_id}.channel_f.jsonl` with domain and count only — no query text, no body excerpt. Operator sees this in the rails report.

**Channel F state:** OK if pre-flight + fetch succeeded on every attempted request; DEGRADED if any fetch failed post-pre-flight; FAILED if SearxNG (or Brave, when opted in) unreachable at all. Pre-flight rejections do NOT flip channel state — they are expected outcomes and are logged as admin-risk entries at severity `LOW`.

**Channel F opt-out short-circuit:** if the policy file is missing or `opt_in=False`, Scout does not call SearxNG at all. The channel state is `OK` (trivially — no work attempted) and the health tuple records `channel_f="OK"`. This preserves "silent empty union is architecturally impossible" — Channel F is present in the tuple, and the other five channels carry the DISCOVER union.

### 4.7 VERIFY stage (`verify_stage.py`)

Implements architecture D.1 STAGE 2. The single purpose is the live-synopsis elevation gate per L-001.

**Contract:**

```python
def verify_candidate(session: Session, candidate: Candidate, *, timeout_seconds: int = 10) -> VerificationVerdict:
    """Live-synopsis elevation gate. Never elevates from cache alone.

    Verdicts:
      VERIFIED_FIT            — live synopsis fetched AND eligibility + scale match applicant profile
      VERIFIED_NOT_FIT        — live synopsis fetched AND eligibility or scale disqualifies
      UNVERIFIED              — no live-synopsis endpoint exists for this channel/source
      VERIFICATION_FAILED     — live endpoint exists but fetch timed out, errored, or returned malformed data

    Never raises on fetch failure — returns VERIFICATION_FAILED and records the cause.
    """
```

**Live-synopsis endpoint resolution by channel:**

| Channel | Live endpoint | VERIFIED_FIT requires |
|---|---|---|
| A (Grants.gov) | `GET /grantsws/rest/opportunities/{opp_id}` | Grants.gov fetchOpportunity returns 200 AND eligibility tokens + award bounds pass applicant match |
| A (SAM.gov / USASpending) | N/A | Candidates from these don't elevate — they feed Logician, not REVIEW |
| B | resolves to channel-of-record (the channel that originally populated the cache row) | same as channel-of-record's rule |
| C | per-portal live endpoint, registered with the adapter | portal-specific match rule |
| D | Federal program page fetch (fresh) | page parse + eligibility match |
| E | feed entry's `source_url` live fetch | page parse + eligibility match |
| F | N/A — Channel F candidates always pass through Channel A's fetchOpportunity if they resolve to a Grants.gov record, otherwise `UNVERIFIED` | — |

**Timeout discipline (M4).** 10 s hard timeout per live fetch; operator-configurable per-channel via `orgs/{slug}/scout/verify_timeouts.yaml`. Timeout → `VERIFICATION_FAILED`, never `UNVERIFIED`. The distinction is architectural (line 280): `UNVERIFIED` means "no live endpoint exists at all", `VERIFICATION_FAILED` means "the live endpoint exists but this fetch did not succeed". Treating a timeout as `UNVERIFIED` would silently demote a transient network blip to a permanent category.

**S6 precedent: VERIFY wins over DISCOVER.** A cache row flagged CRITICAL-fit in Channel B, if `VERIFIED_NOT_FIT` at VERIFY, is tagged `VERIFIED_NOT_FIT` in the output. Scout does NOT promote cached CRITICAL-fit past VERIFY.

**Applicant-match function:**

```python
def _match_applicant(live: "LiveSynopsis", profile: "ApplicantProfile") -> tuple[bool, str]:
    """Return (is_match, reason_code). Deterministic."""
    # Eligibility: intersect live.eligibility_live (normalized tokens via _normalize_applicant_type)
    # with profile.applicant_types. Empty intersection → (False, "A-ELIG-01").
    # Scale: if profile.max_award_capacity < live.award_floor_live → (False, "A-SCALE-01").
    #         if profile.min_award_need > live.award_ceiling_live  → (False, "A-SCALE-02").
    # Geography: if profile.geography not in live.eligible_geographies → (False, "A-GEO-01").
    # Timing: if (live.close_date_live_utc - now_utc) < min_lead_time_days → (False, "A-TIME-01").
    # All pass → (True, "V-OK").
```

`ApplicantProfile` is materialized from Section 1's `PROJECTContextEnvelope` at session start. Scout does not mutate it.

**VERIFY output is frozen.** Once `verify_candidate` returns, the verdict is sealed for the run; re-verification requires a new run. This mirrors Section 1's RFA envelope seal and keeps Scout's output auditable.

**`verify_all(session, candidates)` parallelism.** Runs per-candidate verification across a bounded `concurrent.futures.ThreadPoolExecutor(max_workers=4)` pool. 4 workers is pinned in §8 for M1 8 GB dev node parity.

**A-09 / RT-v1-MED-03 closure — global candidate cap before VERIFY.** Before entering the thread pool, `verify_all` truncates the candidate list to `SCOUT_CANDIDATE_VERIFY_CAP = 1000` items (pinned in §8), sorting by `fit_score_cached` descending with a per-run-seeded secondary tiebreak (see A-v3-01 below). Overflow candidates are NOT dropped from the DISCOVER union — they remain in the run audit but are recorded via `F-SCOUT-V-05 ScoutVerifyCapReached` with the overflow count. This bounds the worst-case wall-time at `ceil(1000 / 4) × 10 s = 2500 s`, which is well above the per-channel 120 s timeout; the 1000-cap matches the §7 M1 8 GB perf smoke (1500 candidates < 120 s). An attacker inflating the candidate set via cache poisoning or Channel D explosion cannot extend VERIFY past this cap.

**A-v3-01 / RT-v2-HIGH-01 + RT-v2-MED-02 + RT-v2-LOW-02 closure — per-run-seeded tiebreak + DEGRADE-on-overflow.** The v2 tiebreak used `candidate_id` ascending, which an attacker can manipulate: because `candidate_id = sha3_512({channel, feed_or_adapter_id, source_key})[:32]`, an attacker who controls a Channel D ALN adapter or a Channel C portal adapter (or floods Channel F with crafted titles that collapse to chosen source_keys) can bias their candidates toward the low end of the lexicographic order, dominating the top-1000 slice when `fit_score_cached` collides. v3 replaces the secondary key with a per-run random seed:

```python
# Captured at run_id creation time alongside _fresh_urandom (see §4.10).
# run_tiebreak_seed is embedded in the SignedHealthTuple's run_entropy field
# (canonical-JSON stable) so the run is auditable but the seed is unpredictable.
run_tiebreak_seed: bytes = _fresh_urandom(16)   # 128-bit, fresh per run

def _verify_sort_key(c: Candidate, seed: bytes) -> tuple[float, bytes]:
    # Primary: fit_score_cached descending (negate for ascending sort).
    # Secondary: seed XOR sha3_512(canonical_json(c))[:16], ascending.
    # sha3_512 over canonical_json(c) is deterministic and covers every
    # field an attacker might control; XOR with a per-run unpredictable
    # seed makes the attacker unable to target a low secondary key.
    cj = _canonical_json(c)
    digest16 = hashlib.sha3_512(cj).digest()[:16]
    xored = bytes(a ^ b for a, b in zip(seed, digest16))
    return (-c.fit_score_cached, xored)

ordered = sorted(candidates, key=lambda c: _verify_sort_key(c, run_tiebreak_seed))
overflow = max(0, len(ordered) - SCOUT_CANDIDATE_VERIFY_CAP)
truncated = ordered[:SCOUT_CANDIDATE_VERIFY_CAP]
if overflow > 0:
    record_degradation(
        session, stage="VERIFY",
        code="F-SCOUT-V-05",
        reason_tag=".truncation_bounded" if overflow <= int(SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO * SCOUT_CANDIDATE_VERIFY_CAP) else ".truncation_degrades",
        overflow=overflow,
    )
    # A-v3-01: if overflow > 0.25 × cap, VERIFY stage DEGRADES (not FAILS).
    # Downstream REVIEW sees the health tuple as verify="DEGRADED" and the
    # operator-facing rails report names the overflow ratio explicitly.
    if overflow > int(SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO * SCOUT_CANDIDATE_VERIFY_CAP):
        _mark_verify_degraded(session, reason="F-SCOUT-V-05.truncation_degrades", overflow=overflow)
```

New `SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO = 0.25` pinned in §8. New `F-SCOUT-V-06 ScoutVerifyTiebreakIntegrity` documented in §6 for any internal invariant failure (seed missing, seed length ≠ 16, canonical_json raises). The `run_tiebreak_seed` itself is written into the SignedHealthTuple under `run_entropy` (see §4.10), not stored separately — post-run audit can replay the exact ordering given the seed, the candidate set, and the algorithm above.

### 4.8 REVIEW stage (`review_stage.py`)

Implements architecture D.1 STAGE 3: human gate. Scout never auto-files.

**Enqueue path:**

```python
def enqueue_for_review(
    session: Session, candidate: Candidate, verdict: VerificationVerdict, fit_rationale: str,
) -> ReviewQueueItem:
    if verdict.verdict != "VERIFIED_FIT":
        raise ReviewEnqueueRejected(f"F-SCOUT-R-01: only VERIFIED_FIT enqueues; got {verdict.verdict}")
    if not within_org_root(_review_queue_path(session.slug, candidate.candidate_id), session.slug):
        raise ReviewEnqueueRejected("F-SCOUT-R-02: path outside org root")
    item = ReviewQueueItem(
        candidate_id=candidate.candidate_id,
        queued_at_utc=_utc_now_iso(),
        queued_by_verdict="VERIFIED_FIT",
        candidate_snapshot=candidate,
        verification_snapshot=verdict,
        fit_rationale=fit_rationale,
        operator_decision=None,
        operator_decided_at_utc=None,
        operator_decision_reason=None,
    )
    vault_write(
        path=_review_queue_path(session.slug, candidate.candidate_id),
        bytes_=_canonical_json(item),
        intent="review-queue-write",
        session_id=session.session_id,
        slug=session.slug,
    )
    return item
```

**Operator-decision path:**

```python
# A-10 / RT-v1-MED-04 closure — per-(slug, candidate_id) lock serialises concurrent
# operator decisions. The lock is process-local; multi-process is out-of-scope for v0.1
# (a single Scout process per Golden Quill per architecture).
#
# A-v3-02 / RT-v2-HIGH-02 + RT-v2-MED-07 closure — replace the unbounded dict with a
# fixed-length striped lock array. An attacker who triggers REVIEW enqueues for many
# distinct (slug, candidate_id) pairs (e.g. via Channel D floods before the per-adapter
# cap lands, or across multiple sessions the same Golden Quill processes) cannot grow
# the lock table beyond O(stripes). Hash collisions across distinct keys serialise
# unrelated decisions, which is a correctness no-op (decisions are idempotent once
# the read-check-write is linearised) and a cheap trade: 64 stripes give <2% expected
# self-collision even under a thousand concurrent unique keys.
_REVIEW_DECISION_LOCK_STRIPES: list[threading.Lock] = [
    threading.Lock() for _ in range(SCOUT_REVIEW_LOCK_STRIPES)   # §8 = 64
]

def _review_lock(slug: str, candidate_id: str) -> threading.Lock:
    # hash(...) is salted per-process (PYTHONHASHSEED), which is fine: we do not
    # need cross-process stability, only intra-run serialisation of read-check-write.
    idx = hash((slug, candidate_id)) % SCOUT_REVIEW_LOCK_STRIPES
    return _REVIEW_DECISION_LOCK_STRIPES[idx]

def record_operator_decision(
    session: Session, candidate_id: str,
    decision: str, reason: str,
) -> ReviewQueueItem:
    if decision not in {"ACCEPT", "REJECT", "HOLD"}:
        raise ReviewDecisionInvalid("F-SCOUT-R-03")
    with _review_lock(session.slug, candidate_id):
        # Read existing item; refuse to overwrite an existing ACCEPT/REJECT
        # (operator must explicitly UNDO via admin-risk flow).
        existing = _read_queue_item(session, candidate_id)
        if existing.operator_decision in {"ACCEPT", "REJECT"}:
            raise ReviewDecisionLocked(
                "F-SCOUT-R-04: decision already recorded; use admin-risk UNDO path"
            )
        updated = replace(
            existing,
            operator_decision=decision,
            operator_decided_at_utc=_utc_now_iso(),
            operator_decision_reason=reason,
        )
        vault_write(
            path=_review_queue_path(session.slug, candidate_id),
            bytes_=_canonical_json(updated),
            intent="review-queue-write",
            session_id=session.session_id,
            slug=session.slug,
        )
        return updated
```

**No auto-file invariant.** There is no code path in `review_stage.py` that writes `operator_decision` without coming through `record_operator_decision`, which is called only from an operator-initiated Pipeline action. Scout's DISCOVER/VERIFY paths cannot reach this function. The PRE-gate (Section 4 — Logician) enforces "no Scribe draft for candidate_id unless review queue item is ACCEPT".

### 4.9 M11 Entity Research Pass + S11 dossier hardening (`entity_research.py`)

Implements architecture D.0 (M11) + S11a/b/c.

**Pass entry point:**

```python
def run_entity_research(
    session: Session, roster: tuple[EntityRosterEntry, ...],
    *, force_refresh: bool = False,
) -> dict[str, EntityDossier]:
    """Run the entity research pass for every roster entry.

    Each dossier is built from a set of fetches. Every fetch goes through Channel F's
    `_preflight_channel_f` — so BT12 applies to dossier research exactly as it applies
    to any other Channel F traffic. There is no separate dossier-fetch bypass.

    Returns {entity_slug: EntityDossier}. Dossiers are written via vault_write with
    intent='dossier-body-write'. Sign-off is a separate operator-invoked call to
    sign_off_dossier.
    """
```

**Per-entity fetch loop (sketch):**
1. Load `EntityRosterEntry` and any prior `EntityDossier`.
2. If prior dossier exists and `now - dossier_written_at < 90 days` and not `force_refresh` — return prior.
3. Otherwise, for each `seed_url` + discovered URLs (bounded by a per-entity fetch cap of 40):
   - BT12 pre-flight → FD broker → fetch → sha3_512 + content_hash record.
   - Parse per source-kind adapter (paper-parser, IRS-990-parser, website-parser, etc.). Each adapter returns a list of candidate claims with evidence_quote + URL + content_hash.
4. Deduplicate candidate claims by normalized claim_text.
5. **S11b: confidence tier assignment.**
   - For each claim, collect the set of registrable domains that independently support it.
   - `HIGH` iff |distinct registrable domains| ≥ 2. `MEDIUM` if exactly 1 registrable domain (regardless of subdomain count). `LOW` on source disagreement or ambiguity.
6. **S11a: per-org domain allowlist gate.** Load `SourceDomainAllowlist` for `session.slug`. Any claim whose `source_registrable_domain` is NOT in `allowlisted_registrable_domains` is marked `force_full_review = True` in an out-of-band metadata file; this overrides the tier-B spot-check default when the review queue is rendered to the operator.
7. Canonicalize the dossier as markdown → compute `dossier_content_hash = sha3_512(canonical_markdown)`.
8. `vault_write` the dossier body with `intent="dossier-body-write"`. Dossier is `UNSOURCED` until sign-off.

**Operator sign-off path (S11c):**

```python
def sign_off_dossier(
    session: Session, entity_slug: str,
    operator_confirmation_token: str,  # enforced by Section 1 record_admin_risk RED-tier retype
) -> DossierSignoff:
    """Atomically bind operator sign-off to (canonical_path, inode, content_hash) triple.

    Fails closed if:
      - Dossier body is absent at the expected path.
      - canonical_path(dossier_path) does not equal stored canonical path (symlink swap).
      - fstat(fd).st_ino does not equal inode recorded at dossier-write time.
      - sha3_512(body) does not equal dossier_content_hash.
      - Any of the above: F-SCOUT-D-01 DossierSignoffBindingFailed.
    """
    # A-03 / RT-v1-CRIT-03 closure: FD is HELD CONTINUOUSLY from open → hash → bind → vault_write.
    # _open_dossier_body_fd opens with O_RDONLY|O_NOFOLLOW, refuses symlinks, refuses FDs outside
    # within_org_root. The vault_write of the sign-off record happens INSIDE this with-block; a
    # final fstat is performed immediately before vault_write to catch an in-flight swap.
    dossier_path = _dossier_body_path(session.slug, entity_slug)
    with _open_dossier_body_fd(dossier_path) as fd:
        cpath = canonical_path(dossier_path)
        st = os.fstat(fd)
        inode = st.st_ino
        # A-v3-06 / RT-v2-HIGH-04 closure: size is decided from fstat BEFORE any read.
        # The v2 approach (read cap+1 bytes then compare len) had a race: a concurrent
        # truncate between open and read could yield a short body that passed the strict
        # > test even though the on-disk file had been oversized moments earlier. Using
        # st_size from the held FD removes that window — the file's size at the moment
        # the FD was opened is the authoritative value, and O_NOFOLLOW + the held FD
        # guarantee no attacker substitution between fstat and read.
        if st.st_size > _MAX_DOSSIER_BYTES:
            raise DossierSizeExceeded(
                f"F-SCOUT-D-02.fstat_size_gt_max: dossier body fstat st_size={st.st_size} "
                f"exceeds {_MAX_DOSSIER_BYTES}"
            )
        body_bytes = os.read(fd, _MAX_DOSSIER_BYTES)
        # Defence-in-depth: if the read returned fewer bytes than st_size, that implies
        # a concurrent truncation between fstat and read — fail closed.
        if len(body_bytes) != st.st_size:
            raise DossierSignoffBindingFailed(
                f"F-SCOUT-D-01e: read short — fstat st_size={st.st_size} read={len(body_bytes)}"
            )
        computed_hash = sha3_512(body_bytes)
        prior = _read_prior_dossier_meta(session.slug, entity_slug)
        if cpath != prior.expected_canonical_path:
            raise DossierSignoffBindingFailed("F-SCOUT-D-01a")
        if inode != prior.expected_inode:
            raise DossierSignoffBindingFailed("F-SCOUT-D-01b")
        if computed_hash != prior.expected_content_hash:
            raise DossierSignoffBindingFailed("F-SCOUT-D-01c")
        signoff_key_id = "tilth.dossier.signoff.hmac.v1"
        with resolve_keystore().retrieve(signoff_key_id) as k:
            binding_bytes = _canonical_json({
                "slug": session.slug,
                "entity_slug": entity_slug,
                "signed_canonical_path": str(cpath),
                "signed_inode": inode,
                "signed_content_hash": computed_hash.hex(),
                "signed_at_utc": _utc_now_iso(),
                "operator_id": session.operator_id,
            })
            signature = hmac_sha3_512(k.view(), binding_bytes)
        signoff = DossierSignoff(
            signed_at_utc=_utc_now_iso(),
            operator_id=session.operator_id,
            signed_canonical_path=str(cpath),
            signed_inode=inode,
            signed_content_hash=computed_hash,
            operator_signature=signature,
            expires_at_utc=_plus_90_days(prior.dossier_written_at_utc),
        )
        # Final TOCTOU closure: re-fstat the held FD and confirm the inode + canonical_path have
        # not drifted since the first reads. Still inside the with-block, so the FD still points at
        # the original file regardless of any parallel rename/bind-mount.
        final_inode = os.fstat(fd).st_ino
        final_cpath = canonical_path(dossier_path)
        if final_inode != inode or final_cpath != cpath:
            raise DossierSignoffBindingFailed("F-SCOUT-D-01d")  # sign-off aborted
        vault_write(
            path=_dossier_signoff_path(session.slug, entity_slug),
            bytes_=_canonical_json(signoff),
            intent="dossier-signoff-write",
            session_id=session.session_id,
            slug=session.slug,
        )
        return signoff
```

**Section 4 verifies the sign-off at cite time.** Section 3 does not enforce "the dossier claim I am about to cite is still sign-off-valid" — that is a draft-time PRE-gate Logician runs. Section 3 produces the binding; Section 4 checks it.

**Law 3 org isolation.** `run_entity_research` refuses to consult a dossier from another org. The dossier path is scoped to `orgs/{session.slug}/dossier/entities/{entity_slug}.md`; `within_org_root` forces this.

### 4.10 M7 health-tuple assembly + sign (`health_tuple.py`)

Assembles per-channel states and calls Section 1's signing primitive.

```python
# A-v3-10 / RT-v2-LOW-03 closure — _fresh_urandom hardens every os.urandom call-site
# in Scout against short-reads. On stock Linux/macOS short-reads are documented as
# impossible for /dev/urandom at sane byte lengths, but the OS contract is not
# universally guaranteed (exotic containerised environments, a future kernel bug,
# or a misbehaving seccomp profile could yield one) and the cost of defending is
# one check plus one retry. Failing closed here is cheaper than failing downstream
# in HMAC key derivation or a tiebreak seed.
def _fresh_urandom(n: int) -> bytes:
    b = os.urandom(n)
    if len(b) != n:
        b = os.urandom(n)           # one retry
        if len(b) != n:
            raise HealthTupleSchemaError(
                f"F-SCOUT-H-03.urandom_short_read: os.urandom({n}) returned {len(b)} bytes twice"
            )
    return b

def assemble_and_sign_health_tuple(
    session: Session,
    per_channel: dict[str, str],
    per_channel_a_endpoints: dict[str, str],
    run_wall_ns: int,
    run_tiebreak_seed: bytes,   # A-v3-01: seed captured at run_id time, carried here for audit
) -> SignedHealthTuple:
    for ch in ("A", "B", "C", "D", "E", "F"):
        if per_channel.get(ch) not in {"OK", "DEGRADED", "FAILED"}:
            raise HealthTupleSchemaError(f"F-SCOUT-H-01: channel {ch} missing or invalid")
    for ep in ("grants.gov", "sam.gov", "usaspending.gov"):
        if per_channel_a_endpoints.get(ep) not in {"OK", "DEGRADED", "FAILED"}:
            raise HealthTupleSchemaError(f"F-SCOUT-H-02: endpoint {ep} missing or invalid")
    backbone_failed = all(per_channel_a_endpoints[ep] == "FAILED" for ep in ("grants.gov", "sam.gov", "usaspending.gov"))
    if len(run_tiebreak_seed) != 16:
        raise HealthTupleSchemaError(
            f"F-SCOUT-V-06: run_tiebreak_seed length={len(run_tiebreak_seed)} (expected 16)"
        )
    # A-12 / RT-v1-MED-06 closure: run_id derivation includes monotonic clock AND 8 bytes of
    # os.urandom, so a backward wall-clock jump (NTP regression) cannot collide run_ids. urandom
    # is drawn inside the signing call via _fresh_urandom (A-v3-10), never reused.
    run_monotonic_ns = time.monotonic_ns()
    run_urandom = _fresh_urandom(8)
    run_id = sha3_512(
        f"{session.session_id}|{run_wall_ns}|{run_monotonic_ns}|".encode("utf-8") + run_urandom
    ).hexdigest()[:24]
    tuple_obj = HealthTuple(
        session_id=session.session_id,
        slug=session.slug,
        run_id=run_id,
        run_wall_ns=run_wall_ns,
        channel_a=per_channel["A"],
        channel_b=per_channel["B"],
        channel_c=per_channel["C"],
        channel_d=per_channel["D"],
        channel_e=per_channel["E"],
        channel_f=per_channel["F"],
        channel_a_endpoints=dict(per_channel_a_endpoints),
        backbone_failed=backbone_failed,
        # A-v3-01 / RT-v2-HIGH-01 closure: embed the per-run tiebreak seed in the health
        # tuple's run_entropy field so an auditor can replay VERIFY ordering post-hoc.
        # run_entropy is canonical-JSON stable (sorted keys, hex encoding).
        run_entropy={
            "run_urandom_hex": run_urandom.hex(),
            "run_monotonic_ns": run_monotonic_ns,
            "run_tiebreak_seed_hex": run_tiebreak_seed.hex(),
        },
    )
    canonical = _canonical_json(tuple_obj)  # sorted keys, no whitespace, NFC
    signature = sign_health_tuple(session, canonical)  # Section 1 primitive
    signed = SignedHealthTuple(
        tuple_canonical=canonical,
        hmac_sha3_512=signature,
        signed_at_utc=_utc_now_iso(),
        hmac_key_id=session.hmac_key_id,
    )
    vault_write(
        path=_run_log_health_path(session.slug, run_id),
        bytes_=_canonical_json(signed),
        intent="scout-run-log-write",
        session_id=session.session_id,
        slug=session.slug,
    )
    return signed
```

**Why canonicalize before signing.** Verifier canonicalization must be byte-identical to the signer's. Any re-ordering of keys, any UTF-8 normalization drift, any whitespace insertion invalidates the signature. Scout signs `canonical` bytes explicitly; Section 4's verifier reads `tuple_canonical` directly and does not re-serialize the `HealthTuple`.

**Scout does not self-attest.** `assemble_and_sign_health_tuple` does not emit an "OK" verdict for the overall tuple — it emits the per-channel states and the signature. The trust anchor is the verifier (Section 4 — Logician) per architecture line 270.

**Hard-abort decision is Logician's.** Architecture line 271: hard abort if all three Channel A endpoints FAILED OR ≥ 4/6 channel families FAILED. Scout records the facts; Logician decides the abort after verifying the signature. Scout does NOT short-circuit on backbone_failed — it still completes the signing and writes the run log, then Pipeline consults Logician.

### 4.11 Scout run orchestration (in `__init__.py`)

Parallel DISCOVER → union → VERIFY → sign health → REVIEW enqueue. Sketch of the entry point Pipeline invokes:

```python
def run_scout_discover_verify(session: Session) -> "ScoutRunResult":
    run_wall_ns = time.time_ns()
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futs = {
            "A": pool.submit(discover_channel_a, session),
            "B": pool.submit(discover_channel_b, session),
            "C": pool.submit(discover_channel_c, session),
            "D": pool.submit(discover_channel_d, session),
            "E": pool.submit(discover_channel_e, session),
            "F": pool.submit(discover_channel_f, session),
        }
        per_channel_states: dict[str, str] = {}
        per_channel_a_endpoints: dict[str, str] = {}
        candidates: list[Candidate] = []
        for ch, fut in futs.items():
            try:
                result = fut.result(timeout=120)
                candidates.extend(result.candidates)
                per_channel_states[ch] = result.channel_state
                if ch == "A":
                    per_channel_a_endpoints = result.per_endpoint_state
            except Exception as e:
                record_degradation(session, event_kind=f"channel_{ch}_exception",
                                   seat="scout", reason_code=f"F-SCOUT-{ch}-99",
                                   duration_seconds=None, authorization_id=None,
                                   expires_at=None)
                per_channel_states[ch] = "FAILED"
                if ch == "A":
                    per_channel_a_endpoints = {"grants.gov": "FAILED", "sam.gov": "FAILED", "usaspending.gov": "FAILED"}

    checkpoint(session, {"stage": "discover_complete", "n_candidates": len(candidates)})

    verdicts = verify_all(session, candidates)

    checkpoint(session, {"stage": "verify_complete", "n_verified_fit":
                         sum(1 for v in verdicts if v.verdict == "VERIFIED_FIT")})

    signed_health = assemble_and_sign_health_tuple(
        session, per_channel_states, per_channel_a_endpoints, run_wall_ns,
    )

    checkpoint(session, {"stage": "health_signed", "run_id": signed_health.hmac_key_id})

    for cand, verdict in zip(candidates, verdicts):
        if verdict.verdict == "VERIFIED_FIT":
            rationale = _build_fit_rationale(session, cand, verdict)  # bounded LLM call; see §9
            enqueue_for_review(session, cand, verdict, rationale)

    return ScoutRunResult(
        candidates=tuple(candidates), verdicts=tuple(verdicts),
        signed_health=signed_health,
    )
```

**Autonomy Rule 1 — save state always.** Every stage writes a checkpoint on success AND failure. The `checkpoint` calls above are on success; the `except` branches write `record_degradation` entries which are themselves audit-chained.

**Autonomy Rule 2 — test your own work.** `verify_all` is the Magic Step. A Candidate does not enter REVIEW without passing VERIFY. A dossier claim does not enter DOC_SOURCED trust-root without passing Section 4's cite-time verify (see §3.4 — Section 3 produces the binding, Section 4 checks it).

---

## 5. Blueprint-tracked implementations

### 5.1 BT12 — M11 Channel F domain pre-flight

Implemented in §4.6. Architecture row 749:

> Per-org research fetches consult the S11a allowlist *and* a per-org jurisdiction/sovereignty policy before dispatching. Fetches to disallowed jurisdictions are rejected pre-flight, not disclosed after-the-fact. Default policy: none; operator opts in.

**Realization:**
- `ChannelFJurisdictionPolicy` (§2.7) is the per-org policy file.
- `_preflight_channel_f(session, candidate_url)` (§4.6) runs before every outbound Channel F fetch; default-deny.
- `_jurisdiction_from_registrable_domain` consults a statically compiled eTLD+1 → ISO-3166-1 alpha-2 table shipped with the package; unknown → deny (F-BT12-03).
- Dossier research (§4.9) runs every fetch through the same pre-flight — S11a domain allowlist is a second gate on top of BT12, not a replacement.
- Rejections appear in the operator rails report as admin-risk entries at severity `LOW`. The count of rejections per run is the proxy metric for "how often the policy fires".

### 5.2 BT7 — Claim-evidence map (consumer note)

Scout does NOT build the claim-evidence map. Section 4 (Logician) builds it. Scout produces the raw `EntityClaim.evidence_quote` + `source_url` + `content_hash` triples that Section 4 rolls up into the map.

### 5.3 BT6 — M7 HMAC key lifecycle (consumer note)

Scout does NOT manage the session HMAC key. Section 1 `keys.py` + `session.py` own BT6. Scout calls `sign_health_tuple(session, canonical_bytes)` only — the key id is resolved internally.

### 5.4 BT11 — Cross-org dossier reference policy (consumer note)

Section 3 enforces org-scoping at dossier read/write. Cross-org manual reference is a Section 4 policy concern at draft time.

### 5.5 BT13 — Rails report + breach-flag signing (consumer note)

Scout emits structured inputs (channel state, Channel F disclosure rows, degradation events) that Section 4 aggregates into the rails report. Scout does not sign the rails report; Section 4 does.

### 5.6 S11a — Per-org source-domain allowlist

Implemented in §4.9 dossier research. `SourceDomainAllowlist` (§2.6) is consulted at dossier-write time; non-allowlisted sources force full operator review regardless of entity `kind`.

### 5.7 S11b — Cross-domain diversity for HIGH confidence

Implemented in §4.9 step 5. `EntityClaim.corroborating_claim_ids` carries the registrable-domain-diverse corroborations. `HIGH` requires ≥ 2 distinct registrable domains.

### 5.8 S11c — Dossier lock verification

Implemented in §4.9 `sign_off_dossier`. The binding is canonical_path + inode + content_hash, HMAC-SHA3-512 signed. Section 4 verifies at cite time.

### 5.9 L-001 — VERIFY gate precedent

Implemented in §4.7. Cached CRITICAL-fit does not elevate. Live synopsis elevation is mandatory and wins over DISCOVER (S6).

### 5.10 L-002 — Path references not content dumps (self-discipline)

Not a code path but a blueprint invariant: Scout's run log and audit entries record file paths + hashes, never full body dumps. `vault_write` body size is capped per §8.

### 5.11 L-003 — Cross-family review (self-discipline)

Scout's Channel F LLM calls (fit rationale builders, claim extractors) use the Scout-family primary (Ollama local) — any downstream audit of Scout's outputs routes to a non-matching family per router.yaml. Scout does not self-audit.

### 5.12 L-004 — API key separation (consumer note)

Scout resolves the KeyStore per session. Per-client BYOK is enforced by Section 1's `resolve_keystore`. Scout never reads provider keys from a global cache.

---

## 6. Failure modes + fail-closed recovery

All failure codes are Section-3-local namespace `F-SCOUT-*` and `F-BT12-*`. Propagated Section 2 codes retain their original namespace.

### 6.1 Channel-A-related (F-SCOUT-A-*)

- **F-SCOUT-A-01** — `grants.gov` fetchOpportunity returns malformed JSON. Recovery: mark endpoint DEGRADED, emit `record_degradation` entry, continue with next row. If ≥ 10% of fetches in this run produce F-SCOUT-A-01, flip endpoint to FAILED.
- **F-SCOUT-A-02** — search2 page paginator returned an overlapping-id page (API regression). Recovery: dedupe by `opp.id`; emit `record_degradation`; continue.
- **F-SCOUT-A-03** — nonce registry event. Reason-tag sub-codes extended in v2 (A-01 / RT-v1-CRIT-01): `F-SCOUT-A-03.duplicate` (duplicate reservation — hard-fail + admin-risk MEDIUM, no retry); `F-SCOUT-A-03.release-success` / `.release-timeout` / `.release-http-error` / `.release-exception` (audit-only release-path tags recorded by the outer `try/finally`). Every reserve has a matching release on every exit path. An un-released nonce is a hard bug (`F-SCOUT-A-03.orphan`, admin-risk HIGH).
- **F-SCOUT-A-04** — 429 rate limit. Recovery: DEGRADED for this endpoint; the 1/2/4 s backoff runs; after exhaustion FAILED; operator digest flags the rate-limit hit.
- **F-SCOUT-A-05** — TLS certificate verification failed. Recovery: FAILED for this endpoint; admin-risk HIGH.

### 6.2 Channel-B-related (F-SCOUT-B-*)

- **F-SCOUT-B-01** — malformed JSONL row in cache file. Recovery: skip row; record degradation.
- **F-SCOUT-B-02** — cache file watermark > 14 days old. Recovery: DEGRADED; row still usable; operator digest note.
- **F-SCOUT-B-03** — cache row carries an org identifier (S10a violation in cached data). Recovery: hard-fail this row (NOT the channel); admin-risk HIGH; emit into Section 4's rails report as a cross-org data leak.
- **F-SCOUT-B-04** — `vault_read` returned a non-matching or malformed `IdentityTuple` for a `vault_shared/cached_opportunities/*` read. Recovery (A-02 / RT-v1-CRIT-02 closure): hard-fail **the entire file** (no further rows consumed from that file), flip Channel B to **FAILED** for the run (not DEGRADED), admin-risk HIGH. Section 2's F-VAULT-* propagates up unwrapped.
- **F-SCOUT-B-05** — `> 10%` malformed rows in a single cache file (A-07 / RT-v1-MED-01 closure: threshold is inclusive `>=`). Recovery: Channel B DEGRADED; row count logged.

### 6.3 Channel-C-related (F-SCOUT-C-*)

- **F-SCOUT-C-01** — registered portal adapter raised. Recovery: mark adapter FAILED; continue with other adapters.
- **F-SCOUT-C-02** — portal returned HTML that did not parse into candidate rows. Recovery: adapter-specific; default DEGRADED + degradation log.
- **F-SCOUT-C-03** — `register_portal(slug)` called with a `canonical_slug(slug)` that is already registered (A-v3-09 / RT-v2-MED-05 closure). Recovery: **raise at registration time** (module import time, not run time); deployment is rejected with a clear error naming both the incoming `portal_slug` and the existing adapter's `__qualname__`. An operator typo that collapses two distinct portals into the same `canonical_slug` — which would previously have allowed either adapter to clobber the other's `feed_or_adapter_id = "portal:" + canonical_slug(slug)` namespace — is caught before any Scout run.

### 6.4 Channel-D-related (F-SCOUT-CHD-*) — program-page adapters

(The "D" channel failure codes live in the `F-SCOUT-CHD-*` namespace in v2 to avoid collision with dossier codes `F-SCOUT-D-*`.)

- **F-SCOUT-CHD-01** — program-page fetch failed. Recovery: DEGRADED; record_degradation; other pages continue.
- **F-SCOUT-CHD-02** — program-page parser reached `CHANNEL_D_MAX_CANDIDATES_PER_PAGE = 200` cap (A-04 / RT-v1-CRIT-04 closure). Recovery: truncate at cap; overflow count recorded; page flagged DEGRADED; admin-risk MEDIUM (suspicious page size).
- **F-SCOUT-CHD-03** — program-page adapter cumulative candidate count reached `CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER = 500` across all pages in this run (A-v3-05 / RT-v2-HIGH-03 closure). Recovery: further appends from this adapter short-circuit to DEGRADED; the adapter's remaining pages are skipped; other Channel D adapters continue. Admin-risk MEDIUM (the v2 per-page cap of 200 still holds per page — this is the per-adapter cumulative guard, which prevents an attacker serving 50 pages × 200 candidates from filling VERIFY's 1000-cap budget with one adapter's output).

### 6.5 Channel-E-related (F-SCOUT-E-*)

- **F-SCOUT-E-01** — malformed feed XML. Recovery: DEGRADED for feed; skip feed this run.
- **F-SCOUT-E-02** — feed TLS invalid. Recovery: FAILED for feed; admin-risk HIGH.
- **F-SCOUT-E-03** — feed iteration reached `CHANNEL_E_RUNAWAY_MAX = 100` entries (A-05 / RT-v1-CRIT-05 closure). Recovery: **break during iteration** before parsing the 101st entry into a `Candidate` (memory bounded at 100 × sizeof(Candidate)); feed flagged DEGRADED; admin-risk MEDIUM; emit `record_degradation`. Reason-tag sub-codes: `.streaming_break` (A-v3-08 — break fired mid-chunk), `.post_fetch_break` (A-v3-08 — entire body already buffered), `.buffer_drained` (A-v4-01 — always emitted alongside one of the above when the parser's internal buffer was zeroed post-break; absence on a truncation event is a hard bug), `.drain_api_missing` (B-v5-04 — feedparser exposes neither `raw_data` nor `reset()`; feed flips to FAILED, admin-risk MEDIUM, drain discipline cannot be honoured).

### 6.6 Channel-F-related (F-BT12-* and F-SCOUT-F-*)

- **F-BT12-01** — slug not opted into Channel F. Recovery: raise; this is expected default-deny behavior; admin-risk LOW.
- **F-BT12-02** — domain on per-org denylist. Recovery: raise; admin-risk LOW.
- **F-BT12-03** — domain jurisdiction unknown. Recovery: raise; admin-risk MEDIUM (blocked unknown domain).
- **F-BT12-04** — domain jurisdiction not in allowed_jurisdictions. Recovery: raise; admin-risk LOW.
- **F-SCOUT-F-01** — SearxNG unreachable. Recovery: Channel F FAILED; continue with the other five channels; Channel F results absent from DISCOVER union.
- **F-SCOUT-F-02** — Brave BYOK key missing when `opt_in=True`. Recovery: admin-risk HIGH (misconfiguration); Channel F FAILED.
- **F-SCOUT-F-03** — result URL's registrable domain differs from the URL's host SNI (DNS rebind or CDN quirk). Recovery: pre-flight re-runs on the resolved host; if still mismatched, reject + admin-risk MEDIUM.
- **F-SCOUT-F-04** — FD release path-tag (A-06 / RT-v1-CRIT-06 closure). Reason-tag sub-codes: `F-SCOUT-F-04.success`, `.fetch-error`, `.parse-error`, `.preflight-reject-after-acquire`, `.exception`. Every `fd_broker.request_fd` in Channel F has a matching `release_fd` on every exit path. Orphaned FDs are a hard bug (`F-SCOUT-F-04.orphan`, admin-risk HIGH).
- **F-BT12-05** — `_load_channel_f_policy` failed the `vault_read` identity-tuple check (A-08 / RT-v1-MED-02 closure). Recovery: pre-flight fails closed; Channel F remains OK-trivial for the run; admin-risk HIGH (policy file integrity event).
- **F-BT12-06** — URL host Punycode normalisation failed (A-14 / RT-v1-MED-08 closure). Recovery: default-deny (request rejected); admin-risk LOW (malformed host).
- **F-BT12-07** — `vault_read` returned an `IdentityTuple` whose `.intent` (NFC-normalised + `.strip()`ed) does not equal the expected intent constant (A-v3-04 / RT-v2-CRIT-02 + RT-v2-MED-01 closure). Recovery: hard-fail the caller; admin-risk HIGH (defence-in-depth against a hypothetical Section 2 regression that silently tolerated an intent mismatch). Scout declares every intent as a module-level `Final[str]` constant so static-name audit is trivial. Applies to every Scout `vault_read` call-site: `channel-f-policy-read`, `source-allowlist-read`, `entity-roster-read`, `cached-opportunity-read`, etc.

### 6.7 VERIFY-related (F-SCOUT-V-*)

- **F-SCOUT-V-01** — live endpoint URL resolution failed. Recovery: `VERIFICATION_FAILED` (not `UNVERIFIED`).
- **F-SCOUT-V-02** — live fetch timed out. Recovery: `VERIFICATION_FAILED`; no retry within this verdict (timeout == decision).
- **F-SCOUT-V-03** — live synopsis body did not parse into the expected schema. Recovery: `VERIFICATION_FAILED`; admin-risk LOW (channel-of-record schema drift).
- **F-SCOUT-V-04** — live synopsis content_hash differs from the hash captured ≤ 60 s ago (double-fetch stability check if enabled). Recovery: `VERIFICATION_FAILED`; admin-risk MEDIUM.
- **F-SCOUT-V-05** — candidate count exceeds `SCOUT_CANDIDATE_VERIFY_CAP = 1000` (A-09 / RT-v1-MED-03 closure). Recovery: truncate to top-1000 by `fit_score_cached` desc / per-run-seeded secondary tiebreak (see A-v3-01, §4.7); overflow count recorded; admin-risk MEDIUM (suspicious inflation — check Channel B or D for upstream poisoning). Reason-tag sub-codes (A-v3-01 / RT-v2-HIGH-01 closure): `.truncation_bounded` if `overflow ≤ SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO × cap` (VERIFY stage stays `OK`), `.truncation_degrades` if `overflow > ratio × cap` (VERIFY stage flipped to `DEGRADED`; rails report names the overflow ratio).
- **F-SCOUT-V-06** — tiebreak integrity event (A-v3-01 / RT-v2-HIGH-01 closure). Fires when `run_tiebreak_seed` is missing, not 16 bytes, or when `_canonical_json(candidate)` raises during secondary-key derivation. Recovery: hard-fail VERIFY stage; admin-risk HIGH (internal invariant violation — a bug, not a runtime condition). The seed itself is recorded in the SignedHealthTuple's `run_entropy.run_tiebreak_seed_hex` field so the ordering is replayable post-run.

### 6.8 REVIEW-related (F-SCOUT-R-*)

- **F-SCOUT-R-01** — enqueue invoked with a non-VERIFIED_FIT verdict. Recovery: raise; this is a caller bug; admin-risk HIGH (should never reach here).
- **F-SCOUT-R-02** — review-queue path outside org root. Recovery: raise; Section 2 F-VAULT-* gate catches this too.
- **F-SCOUT-R-03** — operator decision value invalid. Recovery: raise; no state change.
- **F-SCOUT-R-04** — operator decision already recorded. Recovery: raise; operator must use admin-risk UNDO path which is Section 4's. (A-10 / RT-v1-MED-04 closure: the per-(slug, candidate_id) lock serialises concurrent callers — the second to acquire sees the first decision's ACCEPT/REJECT and raises cleanly.)

### 6.9 Dossier-related (F-SCOUT-D-*)

- **F-SCOUT-D-01a** — canonical path mismatch at sign-off. Recovery: raise; sign-off refused.
- **F-SCOUT-D-01b** — inode mismatch at sign-off.
- **F-SCOUT-D-01c** — content-hash mismatch at sign-off.
- **F-SCOUT-D-01d** — final re-fstat inside the FD-holding block detected an inode/canonical-path drift between first-read and vault_write (A-03 / RT-v1-CRIT-03 closure — TOCTOU final gate). Recovery: sign-off aborted; admin-risk HIGH.
- **F-SCOUT-D-02** — dossier body strictly exceeds `_MAX_DOSSIER_BYTES` (A-13 / RT-v1-MED-07 closure: strict `>` enforcement; a body of exactly the cap is accepted, cap+1 is rejected). Recovery: hard-fail; admin-risk MEDIUM (runaway research). Reason-tag `.fstat_size_gt_max` (A-v3-06 / RT-v2-HIGH-04 closure) — size is decided from the held FD's `fstat.st_size` BEFORE any `os.read`, eliminating the v2 partial-read race in which a concurrent truncate between first-read and second-read could yield a short body that passed the strict `>` test erroneously.
- **F-SCOUT-D-03** — dossier write attempted for a roster entry whose `kind` is invalid. Recovery: raise; roster load validates kinds.

### 6.10 Health-tuple-related (F-SCOUT-H-*)

- **F-SCOUT-H-01** — channel state missing or invalid. Recovery: raise before signing; Pipeline aborts.
- **F-SCOUT-H-02** — Channel A endpoint missing or invalid. Recovery: same.
- **F-SCOUT-H-03** — run_id entropy source event (A-12 / RT-v1-MED-06 closure). Sub-codes: `.urandom-read-failed` (legacy alias retained for backward-compat); `.urandom_short_read` (A-v3-10 / RT-v2-LOW-03 closure — `_fresh_urandom(n)` wrapper asserts `len(result) == n`; on short read, retries once, then raises; every `os.urandom` call-site in Scout routes through this wrapper, so `.urandom_short_read` is the single unified tag for short-read events); `.monotonic-regression` (time.monotonic_ns() went backwards, which is a platform bug — admin-risk HIGH); `.collision-detected` (sha3_512 truncation collided with a prior run_id in the same session ledger — hard-fail, resign with fresh urandom).
- **F-SCOUT-H-04** — Section 1 `sign_health_tuple` raised. Recovery: propagate; emit `record_degradation` at seat=scout; Pipeline cannot proceed without a signed tuple.

### 6.11 Propagated Section 2 codes

- `F-VAULT-*`, `F-GATE-*`, `F-MIRROR-*`, `F-WRAPPER-*`, `F-UUID-*`, `F-FD-*`, `F-DIRECT-*`, `F-FREEZE-*`, `F-NS-*`, `F-SECCOMP-*`, `F-SANDBOX-*`, `F-CEDAR-*` — propagate unchanged. Scout does not mask or wrap these codes.

---

## 7. Test criteria

All tests live under `tests/scout/`. Must all pass before lock.

### 7.1 Unit — `channel_a_federal_apis`

- `test_search2_paginator_handles_empty_page` — zero-opportunity response returns empty list, not an exception.
- `test_search2_paginator_handles_overlapping_ids` — overlapping ids across pages dedupe to single Candidate; F-SCOUT-A-02 logged.
- `test_fetch_opportunity_timeout_returns_verification_failed` — 11 s live fetch → `VERIFICATION_FAILED` (F-SCOUT-V-02), not `UNVERIFIED`.
- `test_backbone_failed_iff_all_three_endpoints_failed` — 2 of 3 FAILED → DEGRADED, not backbone_failed; 3 of 3 → backbone_failed = True.
- `test_nonce_replay_rejected` — duplicate nonce → F-SCOUT-A-03; request not issued.
- `test_tls_cert_invalid_triggers_admin_risk_high` — presented self-signed cert → endpoint FAILED + admin-risk HIGH.

### 7.2 Unit — `channel_b_cache`

- `test_s10a_org_attribute_in_cache_row_fails_row_not_channel` — row with `slug` field → F-SCOUT-B-03; row skipped; channel state unaffected unless threshold hit.
- `test_s10a_defence_in_depth_row_currently_accepted` — polarity-inverted test for ARCH-02: a cache row carrying a forbidden org-identifier key is currently consumed by Scout (documents the Section 2 write-time locus decision). When ARCH-02 is resolved to move S10a into Scout read-time, this test flips polarity.
- `test_cache_watermark_over_14_days_degraded` — file with 15-day-old watermark → Channel B DEGRADED.
- `test_malformed_jsonl_row_skipped` — invalid JSON → row skipped; F-SCOUT-B-01.
- `test_identity_tuple_mismatch_hard_fails_entire_file_not_row` — fabricated IdentityTuple mismatch → F-SCOUT-B-04; **entire file** aborted (no further rows consumed); Channel B **FAILED** for the run (A-02 / RT-v1-CRIT-02 closure).
- `test_exactly_10pct_malformed_rows_triggers_degraded` — file with exactly 10% malformed rows → Channel B DEGRADED (A-07 / RT-v1-MED-01 closure: inclusive threshold).
- `test_nonce_released_on_every_exit_path` — for each of {success, timeout, 5xx, 4xx non-retriable, raised exception}, nonce_registry.release is called exactly once with the reserved nonce (A-01 / RT-v1-CRIT-01 closure).

### 7.3 Unit — `channel_c_portals`

- `test_duplicate_register_raises` — two adapters with same portal_slug → `ScoutConfigError`.
- `test_adapter_exception_fails_only_that_adapter` — one adapter raises; others run.
- `test_threshold_half_adapters_failed_flips_channel_failed` — 3 of 5 FAILED → Channel C FAILED.

### 7.4 Unit — `channel_d_program_pages`

- `test_aln_page_parser_extracts_multiple_opportunities` — multi-opportunity page → > 1 Candidate.
- `test_program_page_404_does_not_fail_channel` — one page 404 → DEGRADED.
- `test_per_page_candidate_cap_enforced` — program page crafted with 500 parseable rows → parser truncates at 200; F-SCOUT-CHD-02 logged; run-level candidates list grows by exactly 200 (A-04 / RT-v1-CRIT-04 closure).

### 7.5 Unit — `channel_e_rss`

- `test_feed_stale_60_days_not_failed_but_degraded` — feed with last entry > 60 days ago → DEGRADED, not FAILED.
- `test_runaway_feed_truncated_at_100_during_iteration` — feed returning 1500 entries → parser **stops iterating** at entry 100; entry 101..1500 are never constructed as Candidates (instrumented via Candidate __post_init__ counter). F-SCOUT-E-03 logged; admin-risk MEDIUM. (A-05 / RT-v1-CRIT-05 closure — memory bound, not post-hoc truncation.)
- `test_invalid_tls_fails_feed` — F-SCOUT-E-02.

### 7.6 Unit — `channel_f_websearch` + BT12 pre-flight

- `test_default_policy_is_opt_out` — freshly-created org has `opt_in=False`; every outbound call → F-BT12-01.
- `test_unknown_jurisdiction_rejected_even_when_opted_in` — domain with no jurisdiction mapping → F-BT12-03 regardless of policy.
- `test_per_org_denylist_overrides_allowed_jurisdictions` — allowed_jurisdictions includes `US`; denylist includes `example.com`; request to `example.com` → F-BT12-02.
- `test_dns_rebind_detection` — result URL resolves to a host whose SNI carries a different registrable domain → F-SCOUT-F-03.
- `test_click_through_url_requires_second_preflight` — SearxNG returns `N` results; each hydration pass runs pre-flight on the result URL; any single rejection does not abort the channel.
- `test_opt_out_short_circuit_produces_ok_health` — `opt_in=False` → channel state "OK" with zero requests attempted; no F-BT12-01 emitted for the short-circuit.
- `test_policy_file_loaded_via_vault_read_only` — AST assertion: `_load_channel_f_policy` contains exactly one call that resolves to `vault_read`, and no `open(` / `Path.read_text` / `builtins.__import__` (A-08 / RT-v1-MED-02 closure).
- `test_idn_homograph_rejected_at_preflight` — URL `https://pаypal.com` (Cyrillic а) → `_registrable_domain` normalises to Punycode `xn--pypal-ofa.com`; allowlist containing only `paypal.com` rejects the request with F-BT12-04 (A-14 / RT-v1-MED-08 closure).
- `test_malformed_idn_rejected_with_f_bt12_06` — URL with invalid UTF-8 in host → `idna.IDNAError` → F-BT12-06; default-deny.
- `test_fd_released_on_preflight_reject_after_acquire` — sequence: first result URL pre-flight passes → FD acquired → second result URL pre-flight fails → assert first FD already released before second pre-flight runs, and no FD is held at the time of rejection (A-06 / RT-v1-CRIT-06 closure).

### 7.7 Unit — `verify_stage`

- `test_verdict_matrix_all_four` — one fixture per verdict class; assert reason codes match.
- `test_cache_critical_fit_flipped_to_not_fit_when_live_disagrees` — S6 invariant.
- `test_timeout_maps_to_verification_failed_not_unverified` — L-001 corollary.
- `test_applicant_match_rejects_on_any_axis` — eligibility / scale / geography / timing each independently cause NOT_FIT.
- `test_verify_all_parallel_bounded_pool` — 100 candidates, pool max_workers=4; assert ≤ 4 concurrent live fetches at any instant (instrumentation hook).
- `test_verify_cap_truncates_at_1000` — 1500 candidates → pre-VERIFY truncation to top-1000 by fit_score_cached descending; F-SCOUT-V-05 logged with overflow=500; verify_all sees exactly 1000 candidates (A-09 / RT-v1-MED-03 closure).
- `test_verify_cap_ties_break_deterministically` — 1500 candidates all with fit_score_cached=50 → top-1000 selected in candidate_id ascending order; same run inputs produce same truncation set across repeats.

### 7.8 Unit — `review_stage`

- `test_only_verified_fit_enqueues` — F-SCOUT-R-01.
- `test_enqueue_path_outside_org_root_rejected` — forged path → F-SCOUT-R-02.
- `test_decision_lock_prevents_overwrite` — ACCEPT → attempt REJECT → F-SCOUT-R-04.
- `test_concurrent_operator_decisions_serialized` — two threads call `record_operator_decision` with ACCEPT and REJECT for the same candidate_id concurrently; assert exactly one succeeds, the other raises F-SCOUT-R-04 cleanly, and the final on-disk state matches the winner (A-10 / RT-v1-MED-04 closure — per-(slug, candidate_id) lock).
- `test_no_auto_file_path_exists` — module-level AST check: `operator_decision` field is only written inside `record_operator_decision` (enforced in §7.16 regression corpus).

### 7.9 Unit — `entity_research` + dossier hardening

- `test_s11a_nonallowlisted_domain_forces_full_review` — claim from `badnews.blog` with non-allowlisted domain → `force_full_review=True` metadata.
- `test_s11b_single_domain_cannot_reach_high` — 5 claims all from `psu.edu` subdomains → tier MEDIUM.
- `test_s11b_two_distinct_domains_reaches_high` — `psu.edu` + `nsf.gov` → tier HIGH.
- `test_s11c_canonical_path_mismatch_rejects_signoff` — symlink-swap fixture → F-SCOUT-D-01a.
- `test_s11c_inode_mismatch_rejects_signoff` — atomic swap → F-SCOUT-D-01b.
- `test_s11c_content_hash_mismatch_rejects_signoff` — body edited between write and signoff → F-SCOUT-D-01c.
- `test_s11c_fd_held_across_signoff` — FD captured inside `_open_dossier_body_fd` must remain open until after `vault_write` of the sign-off record completes. Instrumentation hook records `fstat(fd).st_ino` at both the start and end of the with-block and asserts equality AND asserts the FD is still in the process's open-fd list at the moment `vault_write` returns (A-03 / RT-v1-CRIT-03 closure).
- `test_s11c_final_fstat_catches_swap` — fixture: inside the with-block, after the first reads and before the final `vault_write`, an external rename swaps the file; assert sign-off aborts with F-SCOUT-D-01d.
- `test_dossier_size_strict_greater_than_enforced` — body of exactly `_MAX_DOSSIER_BYTES` (5 MB) succeeds; body of `_MAX_DOSSIER_BYTES + 1` bytes raises F-SCOUT-D-02 (A-13 / RT-v1-MED-07 closure).
- `test_law_3_refuses_cross_org_dossier_read` — run_entity_research in slug A cannot read dossier in slug B.

### 7.10 Unit — `health_tuple`

- `test_missing_channel_raises_h01` — per_channel missing "C" → F-SCOUT-H-01.
- `test_missing_endpoint_raises_h02` — per_channel_a_endpoints missing "sam.gov" → F-SCOUT-H-02.
- `test_canonicalization_stable_across_dict_insertion_order` — two HealthTuple inputs with differently-ordered channel_a_endpoints → identical `tuple_canonical` bytes.
- `test_signature_matches_section1_sign_health_tuple` — given a stub session + fixed canonical bytes, assert `signed.hmac_sha3_512` equals `hmac_sha3_512(key, tuple_canonical)` where key is drawn from KeyStore by session.hmac_key_id.
- `test_backbone_failed_computed_from_endpoints` — {all three FAILED} → True; any other combo → False.
- `test_run_id_unique_under_backward_clock_jump` — inject a backward jump of `run_wall_ns` (e.g., NTP regression simulation); assert two runs with identical `run_wall_ns` produce different `run_id` values because `time.monotonic_ns()` + `os.urandom(8)` differ (A-12 / RT-v1-MED-06 closure).
- `test_run_id_deterministic_given_identical_inputs_none` — property test: 1000 runs with varying wall/monotonic/urandom → all 1000 run_ids distinct (no collisions in 2^96 space).

### 7.11 Integration — full DISCOVER → VERIFY → health → REVIEW

- Six-channel fixture with: A partial success, B healthy, C all adapters OK, D healthy, E one feed TLS-invalid, F opt-in with 2 result URLs. Assert:
  - Per-channel states as expected.
  - `backbone_failed=False`.
  - `SignedHealthTuple.hmac_sha3_512` verifies against Section 1's key.
  - Exactly the set of Candidates that pass VERIFY FIT end up in the review queue.
  - `record_degradation` entries exist for the expected failures.

### 7.12 Integration — L-001 regression

EPA NEETP-26 fixture: cache row flagged `fit_score_cached=95`; live synopsis returns `eligibility=501c3_only`, applicant profile is LLC. Assert: `VERIFIED_NOT_FIT` + `reason_code="A-ELIG-01"` + NOT enqueued for review.

### 7.13 Integration — Autonomy Rule 1 save state

- Hard-kill Scout process mid-DISCOVER; restart; assert `detect_interrupted` sees the session; `resume_or_discard("discard")` drops the partial run; `resume_or_discard("resume")` re-runs only the channels that had not checkpointed success.

### 7.14 Property / fuzz

- `prop_canonical_json_round_trip` — random HealthTuple → canonicalize → parse → canonicalize → bytes equal.
- `prop_candidate_id_stable` — same channel + same source_key ⇒ same candidate_id.
- `prop_verdict_lattice` — for any (cache_verdict, live_verdict) pair, VERIFY output respects the S6 precedence.

### 7.15 Performance smoke (M1 8 GB dev target)

- 1500 Candidates through VERIFY with pool max_workers=4 and a 250 ms stub live-fetch: wall-time < 120 s; peak RSS < 400 MB.
- 50-entity dossier pass with 40 fetches per entity, 150 ms stub fetch: wall-time < 10 min; peak RSS < 600 MB.

### 7.16 Red-team regression corpus

Assertions that encode every Red Team finding we expect. Failing any corpus test blocks lock.

- **AST: no auto-file.** `ast.parse(review_stage.py)` — find every `Assign` targeting `operator_decision`. Assert every such node is inside a function whose name is `record_operator_decision`.
- **AST: no raw socket in Scout.** `ast.parse` every scout module; reject any `socket.socket(` call site outside an `fd_broker` helper.
- **AST: no direct `open()` on vault paths.** `ast.parse` every scout module; reject any `open(` call where the path literal contains `"vault_shared/"` or `"orgs/{slug}/vault/"` outside of `vault_read`/`vault_write` wrappers.
- **AST: no LLM call inside VERIFY.** `verify_stage.py` must not import any LLM provider module. Enforced by import-allowlist in the test.
- **AST: dossier signoff binding.** `sign_off_dossier` must read all three of (canonical_path, inode, content_hash) BEFORE writing the signoff record. Enforced via CFG analysis of the function body.
- **AST: BT12 pre-flight before FD broker.** In `channel_f_websearch.py`, every `fd_broker.request_fd` call must be dominated by a `_preflight_channel_f` call on the same path in the CFG.
- **AST: Channel A nonce release always.** In `channel_a_federal_apis.py`, every `nonce_registry.reserve(` call must be dominated by a matching `nonce_registry.release(` on EVERY CFG exit path (success, every exception class, early return). Enforced via CFG reachability analysis over the function containing the reserve call (A-01 closure, durable enforcement).
- **AST: Channel F FD release always.** In `channel_f_websearch.py`, every `fd_broker.request_fd(` must be matched by a `fd_broker.release_fd(` on every CFG exit path. Enforced identically to the nonce rule (A-06 closure, durable enforcement).
- **AST: policy file only via vault_read.** In `channel_f_websearch.py`, `_load_channel_f_policy` must contain exactly one call resolving to `vault_read` and zero calls to `open`, `Path.read_text`, `io.open`, `os.open`, or any other filesystem-access primitive (A-08 closure).
- **AST: dossier sign-off keeps FD held.** In `entity_research.py`, `sign_off_dossier` must have its `vault_write(..., intent="dossier-signoff-write", ...)` call contained inside the `with _open_dossier_body_fd(...) as fd:` scope (A-03 closure, durable enforcement).
- **AST: run_id derivation includes os.urandom + monotonic.** In `health_tuple.py`, `assemble_and_sign_health_tuple` must call `os.urandom(8)` AND `time.monotonic_ns()` within its body before computing `run_id` (A-12 closure).
- **AST: registrable_domain uses idna Punycode.** In `channel_f_websearch.py`, `_registrable_domain` must contain a call to `idna.encode` OR an equivalent Punycode normalisation before eTLD+1 extraction (A-14 closure).
- **Property: default-deny Channel F.** Randomly-generated `ChannelFJurisdictionPolicy` with `opt_in=False` → every outbound URL raises F-BT12-01.
- **Property: Scout never signs a self-attested OK tuple.** Instrumented sign path — assert the signer receives only raw `(A,B,C,D,E,F)` channel strings, never a derived "overall OK" bit.
- **Property: per-page cap upper bounds.** Generate random HTML containing `N ∈ [0, 1000]` parseable rows; assert Channel D parser emits `min(N, 200)` Candidates and logs F-SCOUT-CHD-02 iff `N > 200` (A-04 durable enforcement).
- **Property: RSS cap upper bounds.** Generate random RSS feed with `N ∈ [0, 1000]` entries; assert at most 100 Candidates are constructed, and assert Candidate `__post_init__` counter never exceeds 100 on any run (A-05 durable enforcement).
- **AST-NO-INDIRECT-VAULT-READ** (A-v3-03 / RT-v2-CRIT-01 closure; A-v4-03 / RT-v3-MED-03 refinement). `ast.parse` every `pipeline.scout.*` module; reject any of (a) `getattr(x, "__call__")` where the resolved symbol reference `x` is `vault_read` or `vault_write`; (b) `functools.partial(x, …)()` where `x` resolves to `vault_read` or `vault_write`; (c) any `ast.Attribute` load on the bare names `vault_read` / `vault_write` other than `.__name__` / `.__module__` for introspection-legal purposes (explicit whitelist). Static-name check: the rule rejects all attribute-access indirection on the symbol even if the attacker's later rebinding is dynamic, because the AST node itself is the evidence. **A-v4-03 / RT-v3-MED-03 refinement — alias tracking through ImportFrom and module-attribute rebinds.** The walker builds an alias table per module in a single pre-pass: (i) every `ImportFrom` whose module is `pipeline.section_02` (or any submodule thereof) and whose `names` list contains `vault_read` or `vault_write` — with or without `asname` — records the local name as an alias (e.g., `from pipeline.section_02 import vault_read as vr` → alias `vr`); (ii) every `Import` of `pipeline.section_02[.x]` followed by an `Assign` of the form `name = <imported_module>.vault_read` records `name` as an alias; (iii) every `Assign` of the form `name = vault_read` (direct rebinding) records `name` as an alias; (iv) alias resolution is transitive up to a fixed point within the module. The ban on indirect access and on bare-name `ast.Attribute` load is then enforced against **every name in the alias set**, not only the symbols `vault_read` / `vault_write`. Any call whose resolved symbol is `vault_read` or `vault_write` — regardless of the local spelling — is admitted only if it's a direct function call (`ast.Call` with `ast.Name` func node); every other access shape is rejected. Small static-analysis enhancement (≈ 10 lines added to the AST walker; single-pass alias resolution). **B-v5-02 / RT-v4-MED-01 refinement — alias-walker termination guard.** The fixed-point loop is bounded by `MAX_ALIAS_WALKER_STEPS = 1000` iterations. Every iteration increments a counter; if the fixed-point is not reached within the cap, the walker aborts with the reason-tag `ast_alias_walker_overflow` on the AST-rule failure path and the module is **rejected** (fail-closed — a module whose alias graph resists decidability within 1000 passes is, by policy, not admissible into Scout). The cap is three orders of magnitude above any plausible benign alias graph (Scout's current modules resolve in ≤ 8 steps); it exists purely to close the decidability attack surface. Documented blueprint invariant: the alias walker is decidable on every acceptable module. Narrow ≤ 3-line edit to the walker loop. No new failure code. **Defence-in-depth framing:** even without these refinements, the post-read `_assert_intent_matches` (A-v3-04) still catches any intent mismatch at runtime, so the alias-tracker is a compile-time hardening, not a load-bearing runtime guard. No new failure code.
- **AST-NO-SETATTR-OPERATOR-DECISION** (A-v3-03 / RT-v2-MED-06 closure). `ast.parse` every `pipeline.scout.*` module; reject `setattr(item, "operator_decision", …)` and `object.__setattr__(item, "operator_decision", …)` and any attribute-store whose attribute string is `"operator_decision"` anywhere **outside** the body of `record_operator_decision` in `review_stage.py`. Complements the existing `no auto-file` rule which only looks at `Assign` nodes.
- **AST-NO-EVAL-IN-SCOUT** (A-v3-03 / RT-v2-CRIT-01 closure). `ast.parse` every `pipeline.scout.*` module; reject any call to `eval`, `exec`, or `compile`. No exceptions; the Scout package never generates or executes runtime code.
- **AST-PREFLIGHT-DOMINATES-FD-REQUEST** (A-v3-07 / RT-v2-MED-03 closure; A-v4-02 / RT-v3-MED-02 refinement; B-v5-01 + B-v5-03 / RT-v4-HIGH-04 + RT-v4-MED-02 refinement). In `channel_f_websearch.py` and any module importing its public API, every `fd_broker.request_fd(kind="https", …)` whose call chain is rooted in Channel F (statically: whose enclosing function is reachable from `channel_f_discover`) must be CFG-dominated by a call to `_preflight_channel_f(...)` earlier in the same call chain. Custom adapter authors are forbidden from calling `fd_broker.request_fd` directly inside Channel F surface; they must delegate through the `channel_f` module's public API, which enforces the pre-flight. Documented in §5.channel_f.adapter-protocol. **A-v4-02 / RT-v3-MED-02 refinement — import-time-static conditional pre-flights accepted.** The dominance walker admits two additional dominance shapes without false-positive rejection: (a) the pre-flight call is inside an `if <STATIC_BOOL>:` block whose guard is a module-level `Final[bool]` or an `if ENABLE_PREFLIGHT:` constant assigned exactly once at module import and never reassigned (verified by AST static-single-assignment check on the module); (b) the pre-flight call is inside a function that is unconditionally invoked on the path to `fd_broker.request_fd` AND that function contains an `if <STATIC_BOOL>:` whose single branch performs `_preflight_channel_f(...)` and whose other branch raises `ChannelFJurisdictionReject`. Any non-static conditional guard (runtime variable, network state, attacker-controlled flag, `getattr`/`setattr`-resolved boolean) still fails the dominance check and the module is rejected. **B-v5-01 / RT-v4-HIGH-04 refinement — literal-only `Final[bool]` initializer.** The "`Final[bool]` module-level constant" shape from A-v4-02 is further restricted: the initializer `ast.AST` node must be (i) an `ast.Constant` with `value in (True, False)`, OR (ii) an `ast.BoolOp` / `ast.UnaryOp` / `ast.Compare` / `ast.IfExp` whose entire sub-tree contains zero `ast.Call` nodes, zero `ast.Attribute` loads, zero `ast.Subscript` loads, and whose every `ast.Name` leaf either (a) resolves to another module-level `Final[bool]` that itself satisfies the same literal-initializer rule (transitively), or (b) resolves to a builtin boolean literal. This explicitly **rejects** `Final[bool] = bool(os.environ.get("ENABLE_PREFLIGHT"))`, `Final[bool] = os.getenv("X") == "1"`, `Final[bool] = sys.platform == "linux"`, `Final[bool] = CONFIG["enabled"]`, and every other runtime-or-env-derived initializer — because each contains at least one `ast.Call`, `ast.Attribute`, or `ast.Subscript` in the initializer sub-tree. Only compile-time-fixed booleans are admitted. **B-v5-03 / RT-v4-MED-02 refinement — cross-module imported-`Final[bool]` resolution.** When the guard name is introduced via `from <mod> import <name>` (with or without `asname`) and `<name>` is declared `Final[bool]` in `<mod>`, the walker `ast.parse`s the originating module's source and re-applies the B-v5-01 literal-initializer rule there. The consuming module is admitted only if the originating module's binding satisfies the rule. Module lookups are bounded to the Scout package surface (`pipeline.scout.*`) plus Section 2's public import surface (`pipeline.section_02.*`); an import from any other module is treated as non-static and the guard is rejected. The walker caches parsed-module ASTs per-audit-run to avoid re-parsing on every rule invocation. Any non-static conditional guard, env-derived initializer, or cross-module mutable binding still fails the dominance check and the module is rejected. The guarantee is preserved and tightened: every Channel F `fd_broker.request_fd` is either unconditionally pre-flighted, or guarded by a compile-time-literal boolean whose initializer sub-tree contains no runtime evaluation — a crafted adapter cannot create an env-var or cross-module path that bypasses pre-flight. Narrow static-analysis extension in the CFG walker (≤ 5 lines for the literal-initializer predicate + ≤ 10 lines for cross-module resolution and cache); no new failure code.
- **Property: indirect vault_read evasion closed.** Three property-tests exercise each evasion vector: (1) a module that calls `getattr(vault_read,"__call__")(...)` — fuzz-runs the AST rule, asserts rejection; (2) a module that calls `functools.partial(vault_read, path=...)()` — same; (3) a module that calls `setattr(item, "operator_decision", "ACCEPT")` outside `record_operator_decision` — same (A-v3-03 durable enforcement).
- **Property: vault_read alias tracking (A-v4-03 durable enforcement).** Three additional property-tests exercise the alias-tracker: (1) a module with `from pipeline.section_02 import vault_read as vr; vr(path=...)` — alias walker records `vr` as alias, direct call admitted, but any `getattr(vr,"__call__")(...)` or `functools.partial(vr, ...)()` is rejected; (2) a module with `import pipeline.section_02 as sec; vr = sec.vault_read; getattr(vr,"__call__")(...)` — alias walker resolves `vr` transitively, AST-NO-INDIRECT-VAULT-READ fires; (3) a module with `vault_read_direct = vault_read; functools.partial(vault_read_direct, path=...)()` — alias-through-rebinding detected, rule fires. Every alias call-site is also subject to `_assert_intent_matches` at runtime — the property-tests confirm both layers.
- **Property: Channel E parser buffer drained (A-v4-01 durable enforcement).** Generate a random RSS feed with `N ∈ [101, 1000]` entries chunked across HTTP so entries 101..N straddle chunk boundaries; after Channel E returns, assert (a) `parser.raw_data` (or the implementation's equivalent internal buffer) has `len == 0`; (b) zero `Candidate` objects reference `content_hash` values derived from entries 101..N (checked via a pre-test-instrumented hash-set); (c) `F-SCOUT-E-03.buffer_drained` was emitted alongside `F-SCOUT-E-03.streaming_break` or `F-SCOUT-E-03.post_fetch_break` on every truncation event.
- **Property: AST-PREFLIGHT literal-only `Final[bool]` initializer (B-v5-01 durable enforcement).** Four adversarial modules: (1) `ENABLE_PREFLIGHT: Final[bool] = bool(os.environ.get("ENABLE_PREFLIGHT"))` — AST-PREFLIGHT-DOMINATES-FD-REQUEST rejects on the literal-initializer predicate (contains `ast.Call`); (2) `ENABLE_PREFLIGHT: Final[bool] = os.getenv("X") == "1"` — rejected (contains `ast.Call` + `ast.Attribute`); (3) `ENABLE_PREFLIGHT: Final[bool] = sys.platform == "linux"` — rejected (contains `ast.Attribute` load on `sys`); (4) `ENABLE_PREFLIGHT: Final[bool] = True` — accepted, dominance walker admits the guard. A fifth module `ENABLE_PREFLIGHT: Final[bool] = not False` — accepted (UnaryOp over literal, zero Call/Attribute/Subscript nodes).
- **Property: AST alias-walker termination under adversarial alias chains (B-v5-02 durable enforcement).** Three adversarial modules: (1) a module with a synthetic alias chain of length 999 (`v0 = vault_read; v1 = v0; ... v999 = v998; v999(...)`) — alias walker resolves within the cap, rejects the indirect-call (since `v999` is in the alias set); (2) a module with an alias chain of length 1500 — alias walker aborts at 1000 steps, module rejected with reason-tag `ast_alias_walker_overflow`; (3) a module with a self-referential alias pattern (`v0 = v1; v1 = v0; v0(...)`) — alias walker detects non-convergence, aborts at cap, module rejected. Assert that no test case causes the walker to hang longer than 2 seconds.
- **Property: AST-PREFLIGHT cross-module imported `Final[bool]` (B-v5-03 durable enforcement).** Four module pairs: (1) module M1 declares `ENABLE_PREFLIGHT: Final[bool] = True`; module M2 `from M1 import ENABLE_PREFLIGHT` and uses it as the guard — M2 admitted after the walker resolves M1's literal; (2) M1 declares `ENABLE_PREFLIGHT: Final[bool] = bool(os.environ.get("X"))`; M2 imports and uses it — M2 **rejected** because M1's binding fails B-v5-01 literal-initializer rule; (3) M1 declares `ENABLE_PREFLIGHT: Final[bool] = True`; M2 uses `from M1 import ENABLE_PREFLIGHT as EP` — walker resolves the asname alias, M2 admitted; (4) M3 outside the Scout/Section-2 import surface declares `ENABLE_PREFLIGHT: Final[bool] = True`; M2 imports from M3 — M2 **rejected** because M3 is outside the bounded lookup surface. Assert the per-audit-run AST cache resolves each originating module at most once.
- **Property: Channel E `_drain_parser_buffer` API-drift fallback (B-v5-04 durable enforcement).** Three parser stubs: (1) stub exposes `raw_data: bytearray` — drain replaces the bytearray, emits `.buffer_drained`, feed DEGRADED as before; (2) stub lacks `raw_data` but exposes `reset()` — drain calls `reset()`, emits `.buffer_drained`, feed DEGRADED; (3) stub lacks both — drain emits `.drain_api_missing`, feed flipped to FAILED (not DEGRADED), admin-risk MEDIUM logged on the health tuple. Assert the FD is released in every case via the enclosing `try/finally`.

---

## 8. Concrete numbers (pinned)

| Constant | Value | Rationale |
|---|---|---|
| Channel A per-endpoint connect timeout | 10 s | Matches M4 live-synopsis timeout; dominant failure mode is connect, not read. |
| Channel A per-endpoint read timeout | 30 s | Grants.gov search2 pages can take > 20 s at peak. |
| Channel A retry count | 3 | 1 s / 2 s / 4 s backoff; 7 s max added latency is tolerable. |
| VERIFY live-synopsis timeout | 10 s | Architecture M4 default; operator-configurable per-channel. |
| VERIFY pool max_workers | 4 | M1 8 GB dev node; 4 concurrent fetches leaves headroom for network + parse. |
| DISCOVER pool max_workers | 6 | One per channel family. Parallel primary. |
| DISCOVER per-channel hard timeout | 120 s | Long enough for a full cache sweep + slow portal; short enough to bound the tuple-sign step. |
| Cache watermark DEGRADED threshold | 14 days | Cache refresh cadence design target; stale-but-usable. |
| RSS stale-feed DEGRADED threshold | 60 days | Newsletters go dormant; not a failure. |
| `CHANNEL_E_RUNAWAY_MAX` | 100 entries | RSS runaway truncation — break iteration at entry 101 **before** Candidate construction (A-05 / F-SCOUT-E-03). |
| `CHANNEL_D_MAX_CANDIDATES_PER_PAGE` | 200 | Per-page cap on federal-program-page parser output **before** append to run-level list (A-04 / F-SCOUT-CHD-02). |
| `CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER` | 500 | Per-adapter cumulative cap across all pages in a single run (A-v3-05 / F-SCOUT-CHD-03). Bounds the 50-page × 200-candidate attack in which an attacker serving a single adapter fills VERIFY's 1000-cap budget. |
| `SCOUT_CANDIDATE_VERIFY_CAP` | 1000 | DISCOVER→VERIFY hand-off cap: truncate by `fit_score_cached` desc with per-run-seeded secondary tiebreak (A-v3-01), before `verify_all` (A-09 / F-SCOUT-V-05). |
| `SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO` | 0.25 | Overflow ratio threshold (A-v3-01 / F-SCOUT-V-05.truncation_degrades). If `overflow > ratio × cap` (here, > 250 overflow items), VERIFY stage flips to DEGRADED; rails report names the overflow ratio. |
| `SCOUT_REVIEW_LOCK_STRIPES` | 64 | Fixed-length striped lock array bounding `_REVIEW_DECISION_LOCKS` memory (A-v3-02 / F-SCOUT-R-04). Memory bound O(stripes), not O(candidates); hash collisions across distinct keys serialise unrelated decisions (correctness no-op). |
| Feed poll min interval | 15 min | Per-run cadence floor. |
| HMAC-SHA3-512 key length (session) | 64 bytes | < SHA-3-512's 72-byte block size; 512-bit entropy. |
| `candidate_id` prefix length | 24 hex chars | 96 bits; ample anti-collision; short enough for path + log. |
| `run_id` prefix length | 24 hex chars | same. |
| `claim_id` prefix length | 24 hex chars | same. |
| `_MAX_DOSSIER_BYTES` | 5 MB | Hard cap on a single dossier body. Strict `>` comparison: reading byte `_MAX_DOSSIER_BYTES + 1` triggers F-SCOUT-D-02 (A-13). |
| Dossier validity | 90 days | Architecture D.0 default. |
| Per-entity research fetch cap | 40 | Prevents runaway research passes. |
| HIGH-confidence distinct-domain requirement | 2 | S11b. |
| Channel F policy default | `opt_in=False`, empty allowed_jurisdictions | Default-deny per BT12. |
| Rotation grace window (BT6, reference only) | 5 s | Section 1 pins it; Scout does not change it. |

---

## 9. Scout run sequence (exact ordering, fail-closed at every step)

This is the canonical per-run ordering. Pipeline invokes this; Scout does not self-schedule.

1. Pipeline calls `start_session(envelope, rfa, project_context)` → `Session`. Section 1 step, not Scout.
2. Pipeline calls `run_scout_discover_verify(session)` (§4.11).
3. Scout records `run_wall_ns`, computes deterministic `run_id`.
4. Scout submits the six DISCOVER channel tasks to a bounded 6-worker pool.
5. As each channel returns, Scout records its state + candidates + per-endpoint state (Channel A).
6. On any channel future raising, Scout records degradation, assigns FAILED, and continues. No channel failure aborts the union.
7. Scout writes checkpoint `discover_complete` with candidate count.
8. Scout invokes `verify_all(session, candidates)` — bounded 4-worker pool, per-candidate live fetch with 10 s timeout.
9. Scout writes checkpoint `verify_complete` with verdict histogram.
10. Scout calls `assemble_and_sign_health_tuple(session, per_channel, per_channel_a_endpoints, run_wall_ns)`.
11. Scout writes checkpoint `health_signed` with run_id.
12. Scout writes the SignedHealthTuple JSON via `vault_write` to the per-run run-log.
13. For each `VERIFIED_FIT` verdict, Scout calls `_build_fit_rationale` (bounded LLM call — Scout's primary per router.yaml — local Ollama by default) and then `enqueue_for_review`.
14. Scout returns the `ScoutRunResult` to Pipeline.
15. Pipeline consults Section 4 (Logician) to verify the SignedHealthTuple and the candidate lattice. Any verification failure is Pipeline's hard abort, not Scout's.

**Operator-driven stages outside this sequence:**

- **Entity Research Pass.** Pipeline invokes `run_entity_research(session, roster, force_refresh=False)` at project init and on operator-triggered refresh. Independent of DISCOVER/VERIFY flow.
- **Operator sign-off.** Invoked directly by operator via `sign_off_dossier(session, entity_slug, confirmation_token)` through Section 1's `record_admin_risk` RED-tier retype ceremony.
- **REVIEW decision.** Operator calls `record_operator_decision(session, candidate_id, decision, reason)` after reading the queue. Each decision produces a vault_write with intent `review-queue-write`.

**LLM call boundaries (what Scout does and does not let an LLM touch):**

| Boundary | LLM allowed? | Why |
|---|---|---|
| DISCOVER (any channel) | **No** | Deterministic fetching + parsing; any LLM there is indeterministic and unauditable. |
| VERIFY | **No** | Deterministic matching. |
| REVIEW enqueue | **No** | The `fit_rationale` is produced *outside* the enqueue path; enqueue itself is deterministic. |
| `_build_fit_rationale` | **Yes, bounded** | Plain-text rationale pulled from VERIFY + Candidate fields; bounded to ≤ 800 tokens; no free-form web lookup. |
| Entity claim extraction (Channel F research fetch body → claim candidates) | **Yes, bounded** | Scout primary LLM; operator review gates acceptance into the dossier. |
| Dossier sign-off | **No** | Deterministic binding + HMAC. |
| Health-tuple sign | **No** | Deterministic; Section 1's HMAC. |

LLM calls are call-site-visible at code review time. The AST red-team regression (§7.16) enforces that LLM imports appear only in `_build_fit_rationale` and `entity_research.py`'s extraction functions.

---

## 10. Findings and open questions (for audit to confirm or refute)

### F-OQ-01 — Channel D adapter registry

Should Channel D share the Channel C adapter registry pattern, or keep its own `PROGRAM_PAGE_ADAPTERS` dict? v1 defaults to separate dicts for clarity (C = state/foundation, D = federal program pages). Audit: is the separation worth the duplication, or would a single `registered_portal_adapters` dict with a `kind` tag be cleaner?

### F-OQ-02 — `fit_score_cached` vs. eliminated

Given L-001 ("cache fit score ≠ elevation"), is `fit_score_cached` still useful as a VERIFY-workload filter, or should VERIFY always process every cached row and drop the heuristic entirely? v1 keeps it as a throughput gate; audit may prefer removing it.

### F-OQ-03 — `_build_fit_rationale` on Scout's local Ollama

Scout's primary per router.yaml is `ollama/mistral:7b` — which is a 7B model on an 8 GB M1. Is it realistic to run a per-VERIFIED_FIT rationale generation on Scout's dev hardware, or should the rationale be deferred to Pipeline after the run completes (allowing the 128 GB client node to handle it)? v1 calls it inline in §4.11; audit may push this to async.

### F-OQ-04 — Channel F "second pre-flight" on click-through

§4.6 requires pre-flight on every result URL. For a 10-result SearxNG query, that is 10 pre-flights + 10 fetches + 1 meta-search fetch. Is the bookkeeping cost worth the safety? v1 says yes — the attack surface is each click-through URL, not just the first query. Audit: agree?

### F-OQ-05 — Dossier `expires_at` enforcement

Is the 90-day expiry a Section 3 enforcement (dossier refuses to read after 90 days) or a Section 4 cite-time check? v1 records `expires_at_utc` in `DossierSignoff` but does NOT refuse Section-3-local reads — it lets Section 4 decide. Audit: is that split right, or should Section 3 also refuse?

### F-OQ-06 — Per-run nonce collision space

Scout uses `session.keys.nonce_registry.reserve(nonce_hex)` per outbound Channel A request. What is the reservation window? Section 1 owns the registry; Scout assumes per-session scope. Audit: confirm the window matches Scout's 24-hour-ish session lifetime expectation.

### F-OQ-07 — Brave BYOK jurisdiction pinning

`api.search.brave.com` is a US endpoint. Should `allowed_jurisdictions={"US"}` be a hard pin for the Brave path, or should operators be able to route Brave traffic through alternate regional endpoints? v1 pins to US.

### F-OQ-08 — SearxNG opt-out short-circuit emits "OK"

§4.6 says `channel_f="OK"` when `opt_in=False`, on the grounds that no work attempted = no failure. Is that the right semantic, or should it be a fourth state like `NOT_OPTED_IN`? v1 keeps it in the 3-state alphabet for Logician parity.

### F-OQ-09 — S11a allowlist warm-start

A new org has no `source_domains.yaml`. What is the default allowlist? v1 says empty — every claim force-routes through full operator review. Alternative: ship a sensible default (`grants.gov`, `nsf.gov`, `usda.gov`, `irs.gov`) to reduce first-project friction. Audit: is the zero-default worth the friction?

### F-OQ-10 — Architectural-finding triggers

Per Section 2 §10 F-OQ-08 pattern: an audit finding triggers an architecture revision only if it requires a new failure code, a new §8 constant, a new mechanism, or a new module. Red Team v1 findings that add to existing buckets without crossing this bar stay in Section 3 as minor fixes.

### F-OQ-11 — Channel F `OK` conflates "work succeeded" with "no work attempted" (ARCH-03 documented limitation)

v5-r8's M7 health-tuple admits three states — `OK`, `DEGRADED`, `FAILED`. Scout's opt-out short-circuit in §4.6 emits `channel_f="OK"` when the org's Channel F policy has `opt_in=False`, on the grounds that no work attempted = no failure. This conflates two semantically distinct conditions that a downstream human reader of a Section 4 rails report cannot disambiguate from the tuple alone:

- **OK (work attempted, work succeeded):** SearxNG/Brave requests completed and passed BT12 pre-flight.
- **OK (no work attempted, channel trivially healthy):** `opt_in=False` — Scout never contacted SearxNG/Brave.

Adding a fourth state `NOT_OPTED_IN` changes the M7 canonical JSON Section 3 signs and requires Section 4 to accept the new state in its hard-abort arithmetic ("≥ 4/6 channel families FAILED"). That is an **architectural** decision, not a blueprint edit — Section 3 cannot unilaterally grow the state alphabet.

Filed separately as `pipeline/validation/architecture_v0.1_findings_from_section_03/ARCH-03.md` against v5-r8. v2 retains the three-state schema; the Section 5 rails-report formatter disambiguates via the Channel F disclosure log — an empty `run_log/{run_id}.channel_f.jsonl` means "not opted in." This finding is documented here so a future architecture audit round can pick it up with full context.

Not a v2 Bucket-A mitigation.

---

## 11. What Section 3 deliberately does NOT implement

- **HMAC key generation + lifecycle.** Section 1 BT6.
- **Health-tuple signature verification.** Section 4 (Logician).
- **Cedar policy evaluation.** Section 4.
- **RFA re-verification at draft boundary.** Section 1 provides `reverify_rfa`; Section 4 invokes it.
- **Claim-evidence-map rollup.** Section 4 BT7.
- **Rails report generation + signing.** Section 4 BT13.
- **Draft generation.** Section 5 (Pipeline) calls Section 4 (Scribe) — Scout stops at `enqueue_for_review`.
- **Vault-layer I/O mechanics.** Section 2 M14 family + FD broker + PRE-gate.
- **Direct filesystem writes.** All writes go through `vault_write`. No `open()` on vault paths from Scout.
- **Non-sovereign network defaults.** Channel F defaults to SearxNG local; Brave BYOK is opt-in.
- **Any LLM call inside DISCOVER or VERIFY.** Enforced by AST regression (§7.16).

---

## 12. Dependencies

**Upstream (Section 3 consumes from):**
- Section 1 — Sovereignty Envelope (LOCKED v5, 2026-04-17). `Session`, `KeyStore`, `sign_health_tuple`, `hmac_sha3_512`, `canonical_slug`, `within_org_root`, `canonical_path`, `record_admin_risk`, `record_degradation`, `checkpoint`, `resolve_keystore`, `hmac_audit_writer`, `atomic_flush`, `nonce_registry.reserve`.
- Section 2 — Vault Topology + Enforcement Envelope (LOCKED v4, 2026-04-17). `vault_read`, `vault_write`, `research_db_read`, `fd_broker.request_fd/release_fd`, `IdentityTuple`, PRE-gate failure codes.
- Architecture v5-r8 (LOCKED 2026-04-17). D.0, D.1, M7, M11, BT12, S11a/b/c, L-001.

**Downstream (depends on Section 3):**
- Section 4 — Logician. Verifies `SignedHealthTuple`, gates candidate → draft on REVIEW accept, verifies dossier signoff at cite time.
- Section 5 — Pipeline. Orchestrates the run sequence (§9) and routes operator actions.

**External (outbound network):**
- `grants.gov` (Channel A, D — search2 + fetchOpportunity + program page fetch).
- `sam.gov` (Channel A).
- `usaspending.gov` (Channel A).
- Seeded state + foundation portals (Channel C) — per-org-configured.
- Federal program pages (Channel D) — per-org-configured ALNs.
- RSS / newsletter feeds (Channel E) — per-org-configured URLs.
- `127.0.0.1:searxng_port` (Channel F default, local).
- `api.search.brave.com` (Channel F fallback, BYOK opt-in).

---

## 13. Audit request (for the Thesis Team) — v5 round (operator-escalation)

Three-seat, cross-family, non-Anthropic (unchanged since v1):
- **Editor** = Llama 3.3 70B versatile (meta) — clarity, jargon, goals/outputs/outcomes/objectives sorting, replacement-option proposals.
- **Judge** = Qwen 3 32B (alibaba) — 10-dimension rubric scoring; mechanism coverage + blueprint-tracked coverage + v5-closure-map + v4-closures-preserved + v3-closures-preserved + v2-closures-preserved + deferral-faithfulness JSON maps. PASS ≥ 85/100.
- **Red Team** = GPT-OSS 120B (openai_oss), max_tokens=16000 — attack-surface regression: re-exercise the four legitimate v4 Bucket-B items triaged in `05_synthesis_v4.md` (RT-v4-HIGH-04, RT-v4-MED-01, RT-v4-MED-02, RT-v4-MED-03) to confirm v5 mitigations land, re-exercise the three v4 Bucket-A replays (A-v4-01..03) to confirm preservation, re-exercise the ten v3 Bucket-A replays and fourteen v2 Bucket-A replays to confirm preservation, and surface any residual or newly introduced weaknesses inside the v5-r8 envelope.

**PASS condition (STRICT v5 bar):** Editor `READY_TO_LOCK` ∧ Judge ≥ 85/100 ∧ Red Team ∈ {`READY_TO_LOCK`, `REQUIRES_MINOR_FIXES` with **Bucket-C only**, zero Bucket-B}. Zero Bucket-A items. Zero surviving v4 Bucket-B residuals. This is the operator-escalation round; the bar is tighter than v4.

**Lock policy (operator directive — Option B selected after v4 triage):** v4 PASSed Editor + Judge cleanly; Red Team's `REQUIRES_MAJOR_MITIGATIONS` verdict triaged to 4 legitimate Bucket-B + 3 Bucket-C. Operator selected Option B (spin v5 operator-escalation to close all four Bucket-B items before lock) because the "most stable secure efficient effective foundation" criterion outranks the 4-round budget heuristic. v5 is one more silent-revision round past the cap; per the operator's new policy ("one audit, one fix attempt, then discern with Opus 4.7"), v5 is the terminal audit round for Section 3. If v5 PASSes the STRICT bar, lock at v5 and promote `section_03_v5.md` → `pipeline/blueprint/v0.1/section_03_scout.md`. If v5 returns residuals, the result plus the Red Team output return to the operator + Opus 4.7 for a single synthesis pass — no silent v6.

**v5 is a narrow-edit revision of v4.** No architectural amendments; no new failure codes; the v5 fixes add one new reason-tag (`F-SCOUT-E-03.drain_api_missing`), two §7.16 AST-rule refinements (literal-only `Final[bool]` initializer in `AST-PREFLIGHT-DOMINATES-FD-REQUEST`; cross-module imported-`Final[bool]` resolution in the same rule; max-iteration cap in the alias walker under `AST-NO-INDIRECT-VAULT-READ`), two helper-path tightenings in `channel_e_rss.py` (`hasattr`-dispatch in `_drain_parser_buffer`), and four additional property-tests under §7.16. Reviewers should NOT re-litigate architectural items; ARCH-02 + ARCH-03 remain out of scope.

**v5 Bucket-B closure map (what to verify was applied):**

| ID | v4 Red Team finding | v5 location | What changed |
|----|---------------------|-------------|--------------|
| B-v5-01 | RT-v4-HIGH-04 env-var-derived `Final[bool]` admitted by AST-PREFLIGHT-DOMINATES-FD-REQUEST static-SSA check | §7.16 | Dominance walker requires the `Final[bool]` initializer to be a literal or a constant expression whose sub-tree contains zero `ast.Call`, zero `ast.Attribute` load, and zero `ast.Subscript` load. Rejects `bool(os.environ.get(...))` and all env-var / function-call / attribute-load derived initializers. Narrow ≤ 5-line edit to the CFG walker. No new failure code |
| B-v5-02 | RT-v4-MED-01 alias-walker non-termination on self-referential or adversarially long alias chains | §7.16 | Fixed-point loop gains `MAX_ALIAS_WALKER_STEPS = 1000` cap; if the cap is reached the walker aborts with reason-tag `ast_alias_walker_overflow` and the module is rejected (fail-closed). Narrow ≤ 3-line edit. No new failure code |
| B-v5-03 | RT-v4-MED-02 imported `Final[bool]` guard may be mutated in the originating module | §7.16 | Static-SSA check extends to resolve imported names to originating module's AST literal via bounded `ast.parse` (Scout + Section 2 surface only); per-audit-run cache. Narrow static-analysis enhancement. No new failure code |
| B-v5-04 | RT-v4-MED-03 `_drain_parser_buffer` assumes `parser.raw_data` attribute name | §4.5 + §6.5 + §7.16 | Helper now probes (i) `hasattr(parser, "raw_data")` → replace bytearray; (ii) `hasattr(parser, "reset")` → call `reset()`; (iii) else emit new reason-tag `F-SCOUT-E-03.drain_api_missing` and flip feed to FAILED (admin-risk MEDIUM). Narrow ≤ 5-line edit to `channel_e_rss.py`; adds one reason-tag sub-code |

**v4 Bucket-A preservation check (re-verify every v4 closure still stands):**

Every A-v4-01 … A-v4-03 closure from the v4 round MUST still be in place in v5 — no regressions. The v4 closure map is in `05_synthesis_v4.md`; v5 Editor and Red Team explicitly re-verify each entry.

**v3 Bucket-A preservation check (re-verify every v3 closure still stands):**

Every A-v3-01 … A-v3-10 closure from the v3 round MUST still be in place in v5 — no regressions. The v3 closure map is in `05_synthesis_v3.md`; v5 Editor and Red Team explicitly re-verify each entry.

**v2 Bucket-A preservation check (re-verify every v2 closure still stands):**

Every A-01 … A-14 closure from the v2 round MUST still be in place in v5 — no regressions. The v2 closure map is in `05_synthesis_v2.md`; v5 Editor and Red Team explicitly re-verify each entry.

**v5 Red Team scope hints (re-exercise v4 Bucket-B attacks + sweep for new residuals):**
- Re-run RT-v4-HIGH-04: write `ENABLE_PREFLIGHT: Final[bool] = bool(os.environ.get("ENABLE_PREFLIGHT"))` in a Channel F adapter — does AST-PREFLIGHT-DOMINATES-FD-REQUEST reject it (walker must see the `ast.Call` in the initializer sub-tree)? Now write `Final[bool] = True` — accepted? Now `Final[bool] = sys.platform == "linux"` — rejected (ast.Attribute load on `sys`)? Now `Final[bool] = CONFIG["on"]` — rejected (ast.Subscript)?
- Re-run RT-v4-MED-01: write a module with an alias chain of length 1500 (`v0 = vault_read; v1 = v0; ... v1499 = v1498`) — does the walker abort at step 1000 with `ast_alias_walker_overflow` and reject the module? Now write a self-referential alias (`v0 = v1; v1 = v0`) — does the walker detect non-convergence and reject at cap?
- Re-run RT-v4-MED-02: module M1 declares `ENABLE_PREFLIGHT: Final[bool] = True`; module M2 `from M1 import ENABLE_PREFLIGHT` — admitted? Module M1' declares `Final[bool] = bool(os.environ.get("X"))`; M2' imports it — rejected because M1' fails B-v5-01 at origin? Module M3 outside Scout/Section-2 surface declares `Final[bool] = True`; M2'' imports from M3 — rejected as out-of-bounded-surface?
- Re-run RT-v4-MED-03: feedparser stub exposing `raw_data` only — `.buffer_drained` emitted? Stub exposing `reset()` only — `.buffer_drained` emitted? Stub exposing neither — `.drain_api_missing` emitted, feed FAILED?
- Re-verify every A-v4-01 … A-v4-03: replay the v4 Red Team attack list; confirm each mitigation still lands.
- Re-verify every A-v3-01 … A-v3-10: replay the v3 Red Team attack list; confirm each mitigation still lands.
- Re-verify every A-01 … A-14: replay the v2 Red Team attack list; confirm each mitigation still lands.
- New residual vectors to hunt: (a) does B-v5-03's cross-module `ast.parse` introduce a new attack surface (e.g., parsing a pathologically large originating module causes memory pressure) — is the parse bounded by feed-size limits? (b) does the `hasattr` dispatch in B-v5-04 admit a TOCTOU where `hasattr` passes but the attribute is deleted before use — is the replace/call atomic from feedparser's perspective? (c) does the `ast_alias_walker_overflow` reason-tag surface cleanly through the failure path — is there an audit log entry?
- Out-of-scope this round: any finding that requires amending v5-r8 (S10a locus, NOT_OPTED_IN state) — already filed as ARCH-02 / ARCH-03. Re-reporting ARCH-03 (RT-v2/v3/v4-LOW-01 shape) is a protocol violation; skip. Same-uid hostile Python code (e.g., `importlib.reload`) is explicitly out-of-model per Section 1's trusted-operator threat model (RT-v4-HIGH-03 was correctly rejected in v4 triage); re-reporting is a protocol violation.

**STRICT PASS bar for v5 Red Team:** zero Bucket-A; zero re-surfaced v4 Bucket-B; zero new Bucket-B; `REQUIRES_MINOR_FIXES` acceptable only if residuals are Bucket-C (documentation-only). Any Bucket-A or Bucket-B surfaces return to operator + Opus 4.7 for synthesis (no silent v6 per the operator's new audit-fix policy).

---

**End of Section 3 v5 draft.**


