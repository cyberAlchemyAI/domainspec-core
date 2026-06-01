# Spec card — pipeline.scout Round 1 (types + constants + package skeleton)

**STATUS:** LOCKED-backfilled

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_03_scout.md` §2.1–§2.8 (data schemas + on-disk layout, lines 106–328)
- §3.1 (package re-exports, lines 333–357)
- §8 (pinned numeric + policy constants, lines 1392–1422)
- §9 (LLM-call boundary table, lines 1451–1463) — documents which intents are deterministic vs bounded-LLM; shapes the intent constants
- §11 ("what Section 3 deliberately does NOT implement", lines 1524–1537) — confirms that Round 1 owns NO network, NO filesystem, NO signing logic

**Blueprint hash-at-card:** `0a82d955f95b0fca` (sha3_512(section_03_scout.md)[:16]).

**Spec-card version:** v1
**Round:** Scout R1 of 11 (§3 build stack). Dependency-free foundation; no sibling module depends on Round 1, but every subsequent Round imports from it.
**Futureproofing scope:** §4.1 public-API boundary via explicit `__all__`; §4.10 type hints 100%; §4.11 docstring blueprint anchors on every public symbol; §4.12 engineering-lessons accrual in the LOCK memory entry.

---

## Summary

Land the dependency-free substrate the rest of §3 Scout will compose against:

1. `pipeline/scout/_types.py` — eleven frozen, kw-only dataclasses mirroring §2.1–§2.7 exactly: `Candidate`, `VerificationVerdict`, `HealthTuple`, `SignedHealthTuple`, `ReviewQueueItem`, `EntityRosterEntry`, `EntityClaim`, `EntityDossier`, `DossierSignoff`, `SourceDomainAllowlist`, `ChannelFJurisdictionPolicy`.
2. `pipeline/scout/_constants.py` — §8 pinned numeric/timeout constants as `Final[int]` / `Final[float]` + §9/§3.3-derived intent strings + §2 enum strings (channel codes, verdicts, health states, funder kinds, entity kinds, confidence tiers, feed prefixes) as `Final[str]`.
3. `pipeline/scout/__init__.py` — package-level `__version__`, `__all__`, re-exports from `_types` and `_constants`. No module-level side effects at import. No network, no disk, no global state.
4. `pyproject.toml` — remove `pipeline.scout*` from the setuptools exclude list (currently line 52) so the package installs. Record the change in the LOCK entry's E-XXX lesson if surprising.

Nothing in this round reads files, opens sockets, calls Section 1 or Section 2, or produces `Violation`s against AST rules R1–R5 (all five rules' threat-surfaces are inactive on pure-data modules).

## Design decisions (operator-disposed 2026-04-20, reversible on request)

1. **Two modules instead of one.** `_types.py` and `_constants.py` split because (a) §2 schemas and §8 constants are audited separately; (b) later Rounds will import only the narrow slice they need; (c) a single 500-line module violates the Midas "one concern per file" norm the Section 2 build established (`schemas.py` + `error_codes.py` are split the same way).
2. **Private-underscore names.** `_types` and `_constants` carry the `_` prefix because Pipeline (§5) and Logician (§4) consume the **public** `pipeline.scout` surface via `__init__.py` re-exports, never the `pipeline.scout._types` path directly. The `_` is not a hard access barrier (Python); it is a convention pin that the AST-lint audit round (if extended) can enforce.
3. **`Final[str]` intent constants ship now, not in each channel round.** Rationale: every channel module's `vault_read`/`vault_write` call site names an intent string (`"read"`, `"channel-f-policy-read"`, `"review-queue-write"`, `"dossier-body-write"`, `"dossier-signoff-write"`, `"scout-run-log-write"`). Centralizing in Round 1 guarantees one source-of-truth and prevents string drift across six channels. Cost: ~15 lines. Benefit: zero risk of `"scout-run-log-write"` being typed `"scout-run-logs-write"` in channel_a vs channel_b.
4. **Enum-like `Final[str]` literals instead of `enum.StrEnum`.** Blueprint schemas use `str` fields, not `StrEnum` subclasses, so canonical JSON serialization is trivial (`json.dumps` over `str`). `Final[str]` constants give the same typo-safety without forcing every comparison through `Verdict.VERIFIED_FIT` syntax. This mirrors Section 2's `pipeline/vault/error_codes.py` pattern exactly.
5. **Canonical-bytes helper is imported from `pipeline.sovereignty.audit`.** `canonical_json_bytes(obj)` already exists; Round 1 does not re-implement. The per-type `canonical_bytes()` helpers this round adds use that function so verification-side canonicalization is bit-identical (§2.3 invariant: "Scout never signs raw `HealthTuple` bytes — only the canonicalized form, so verifier canonicalization is identical").
6. **No `_build_fit_rationale` stub.** Per router.yaml Scout primary is `ollama/mistral:7b` (local, sovereign). The rationale builder is a Round 11 concern (orchestration), not Round 1. Round 1 defines `ReviewQueueItem.fit_rationale: str` — the consumer surface — and that is the only commitment required for sibling Rounds to type-check.
7. **`feed_or_adapter_id` prefix constants ship as `Final[str]` without the `":"` suffix.** `FEED_PREFIX_API = "api"`, `FEED_PREFIX_CACHE = "cache"`, etc. Call sites compose `f"{FEED_PREFIX_API}:{endpoint_name}"`. Rationale: the colon is syntactic punctuation, not semantic content; including it in the constant invites accidental double-colons.
8. **One public symbol per blueprint §2.X subsection.** No consolidation, no convenience unions. If a future Round wants `SomeDossierView = EntityDossier | None`, it declares it locally.

## Public API (goes in `__init__.__all__`)

```python
__all__ = [
    # §2.1 — DISCOVER row
    "Candidate",
    # §2.2 — VERIFY verdict
    "VerificationVerdict",
    # §2.3 — health tuple + signed wrapper
    "HealthTuple",
    "SignedHealthTuple",
    # §2.4 — REVIEW queue
    "ReviewQueueItem",
    # §2.5 — entity research
    "EntityRosterEntry",
    "EntityClaim",
    "EntityDossier",
    "DossierSignoff",
    # §2.6 — S11a allowlist
    "SourceDomainAllowlist",
    # §2.7 — BT12 jurisdiction policy
    "ChannelFJurisdictionPolicy",
    # Enumerated string literals — §2 schema field domains
    "CHANNEL_A",
    "CHANNEL_B",
    "CHANNEL_C",
    "CHANNEL_D",
    "CHANNEL_E",
    "CHANNEL_F",
    "VERDICT_VERIFIED_FIT",
    "VERDICT_VERIFIED_NOT_FIT",
    "VERDICT_UNVERIFIED",
    "VERDICT_VERIFICATION_FAILED",
    "DECISION_ACCEPT",
    "DECISION_REJECT",
    "DECISION_HOLD",
    "HEALTH_OK",
    "HEALTH_DEGRADED",
    "HEALTH_FAILED",
    "FUNDER_FEDERAL",
    "FUNDER_STATE",
    "FUNDER_FOUNDATION",
    "FUNDER_INTERMEDIARY",
    "FUNDER_UNKNOWN",
    "ENTITY_KIND_PERSON_LEAD",
    "ENTITY_KIND_PERSON_PARTNER",
    "ENTITY_KIND_PERSON_REFERENCED",
    "ENTITY_KIND_ORG_APPLICANT",
    "ENTITY_KIND_ORG_PARTNER",
    "ENTITY_KIND_ORG_REFERENCED",
    "ENTITY_KIND_PRODUCT",
    "ENTITY_KIND_PUBLICATION",
    "CONFIDENCE_HIGH",
    "CONFIDENCE_MEDIUM",
    "CONFIDENCE_LOW",
    "ROSTER_ADDED_BY_OPERATOR",
    "ROSTER_ADDED_BY_SCOUT_PROPOSAL",
    "FEED_PREFIX_API",
    "FEED_PREFIX_CACHE",
    "FEED_PREFIX_PORTAL",
    "FEED_PREFIX_ALN",
    "FEED_PREFIX_RSS",
    "FEED_PREFIX_SEARXNG",
    "FEED_PREFIX_BRAVE",
    # §3.3 + §9 intent strings used with vault_read / vault_write
    "INTENT_READ",
    "INTENT_CHANNEL_F_POLICY_READ",
    "INTENT_REVIEW_QUEUE_WRITE",
    "INTENT_DOSSIER_BODY_WRITE",
    "INTENT_DOSSIER_SIGNOFF_WRITE",
    "INTENT_SCOUT_RUN_LOG_WRITE",
    # §8 pinned numeric constants
    "CHANNEL_A_CONNECT_TIMEOUT_S",
    "CHANNEL_A_READ_TIMEOUT_S",
    "CHANNEL_A_RETRY_COUNT",
    "VERIFY_LIVE_SYNOPSIS_TIMEOUT_S",
    "VERIFY_POOL_MAX_WORKERS",
    "DISCOVER_POOL_MAX_WORKERS",
    "DISCOVER_PER_CHANNEL_HARD_TIMEOUT_S",
    "CACHE_WATERMARK_DEGRADED_DAYS",
    "RSS_STALE_FEED_DEGRADED_DAYS",
    "CHANNEL_E_RUNAWAY_MAX",
    "CHANNEL_D_MAX_CANDIDATES_PER_PAGE",
    "CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER",
    "SCOUT_CANDIDATE_VERIFY_CAP",
    "SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO",
    "SCOUT_REVIEW_LOCK_STRIPES",
    "FEED_POLL_MIN_INTERVAL_MIN",
    "SESSION_HMAC_KEY_LEN_BYTES",
    "CANDIDATE_ID_HEX_LEN",
    "RUN_ID_HEX_LEN",
    "CLAIM_ID_HEX_LEN",
    "MAX_DOSSIER_BYTES",
    "DOSSIER_VALIDITY_DAYS",
    "PER_ENTITY_RESEARCH_FETCH_CAP",
    "HIGH_CONFIDENCE_DISTINCT_DOMAIN_REQUIREMENT",
    "ROTATION_GRACE_WINDOW_S",
    # Package meta
    "__version__",
]
```

`__version__ = "0.1.0-scout-r1"`.

## Data structures (exact field-for-field match with §2)

Every dataclass: `@dataclass(frozen=True, kw_only=True)`. Primitive fields only; nested dataclasses where §2 nests (`ReviewQueueItem.candidate_snapshot: Candidate`, `ReviewQueueItem.verification_snapshot: VerificationVerdict`, `EntityDossier.roster_entry: EntityRosterEntry`, `EntityDossier.claims: tuple[EntityClaim, ...]`, `EntityDossier.operator_signoff: DossierSignoff | None`). Tuple-valued fields use `tuple[X, ...]`; frozenset-valued fields (§2.6 `allowlisted_registrable_domains`, §2.7 `allowed_jurisdictions` + `disallowed_registrable_domains`) use `frozenset[str]`.

No `__post_init__` validators in Round 1 — validation is a channel-module concern (channel_a asserts `feed_or_adapter_id.startswith(f"{FEED_PREFIX_API}:")`, etc.). Round 1 ships the shape.

## Canonical-bytes surface

Four types sign / hash on-disk and therefore expose a `canonical_bytes()` module-level helper (free function, not method, to preserve frozen dataclass purity):

- `health_tuple_canonical_bytes(ht: HealthTuple) -> bytes`
- `candidate_canonical_bytes(c: Candidate) -> bytes`
- `entity_dossier_canonical_bytes(ed: EntityDossier) -> bytes`
- `dossier_signoff_canonical_bytes(ds: DossierSignoff) -> bytes`

Each delegates to `pipeline.sovereignty.audit.canonical_json_bytes` over `dataclasses.asdict(...)`. Tuples deserialize as lists in JSON — that is fine; the verifier canonicalizes identically. These helpers are NOT in Round 1's `__all__` beyond what the schemas require; sibling Rounds that need them import directly from `pipeline.scout._types`.

Actually revised — they ARE public, because `health_tuple.py` (Round 2) will call `health_tuple_canonical_bytes` and the public `__init__` should re-export. Adding to `__all__`:

```python
# Canonical bytes helpers (used by signing call-sites in later rounds)
"health_tuple_canonical_bytes",
"candidate_canonical_bytes",
"entity_dossier_canonical_bytes",
"dossier_signoff_canonical_bytes",
```

## Test surface (RED first, `tests/scout/test_round_1_types_constants.py`)

### Frozen discipline
- Each dataclass rejects attribute mutation (`FrozenInstanceError`).
- Each dataclass rejects positional construction (`TypeError` — kw_only).

### Field-completeness
- Each dataclass constructs from a valid example and round-trips through `dataclasses.asdict`.
- Each dataclass with a `tuple[..., ...]` field rejects `list` inputs at construction **type-check time**? No — dataclasses do not type-check. Test asserts isinstance of the tuple post-construction; no runtime rejection promised.
- Nested dataclass fields (`ReviewQueueItem.candidate_snapshot: Candidate`) type-hint-round-trip.
- Optional fields (`VerificationVerdict.live_synopsis_url: str | None`) accept `None` and a string.

### Canonical-bytes round-trip
- `health_tuple_canonical_bytes(ht)` is deterministic: same input → byte-identical output across 100 invocations.
- Keys are sorted: construct two `HealthTuple` instances with same fields in different declaration orders (impossible with kw-only — so this test asserts the dict produced by `asdict` is sorted by `canonical_json_bytes`).
- `json.loads(canonical_bytes(ht).decode("utf-8"))` returns a dict with string keys — serializer never emits non-string keys.
- Distinct instances produce distinct bytes (no hash collisions on common-field instances).
- `candidate_canonical_bytes`, `entity_dossier_canonical_bytes`, `dossier_signoff_canonical_bytes` — same four properties.
- Frozenset fields serialize stably (tested across invocations to confirm Python's `set` iteration order doesn't leak — `canonical_json_bytes` via `sort_keys=True` handles dict keys but frozenset values serialize as JSON arrays; our helper converts frozensets to **sorted tuples** before `asdict` → canonical JSON, ensuring determinism).

### Constants
- Every `Final[int]` / `Final[float]` constant matches blueprint §8 value (parametrized table test against a dict of `name → expected_value`).
- Every `Final[str]` enum literal is non-empty and ASCII-alphanumeric-plus-underscore-plus-dash.
- `CHANNEL_E_RUNAWAY_MAX == 100`; `CHANNEL_D_MAX_CANDIDATES_PER_PAGE == 200`; `CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER == 500`; `SCOUT_CANDIDATE_VERIFY_CAP == 1000`; `SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO == 0.25`; `SCOUT_REVIEW_LOCK_STRIPES == 64`; `MAX_DOSSIER_BYTES == 5 * 1024 * 1024`; `DOSSIER_VALIDITY_DAYS == 90`; `HIGH_CONFIDENCE_DISTINCT_DOMAIN_REQUIREMENT == 2`.
- Channel codes are uppercase single letters; verdict strings are UPPER_SNAKE; health-state strings are UPPER; feed prefixes are lowercase.
- All intent strings match §3.3 + §9 spellings exactly.

### `__all__` completeness
- Every public symbol exported; no private underscore symbol exported.
- `pipeline.scout.__version__` equals `"0.1.0-scout-r1"`.
- `import pipeline.scout` produces zero network activity (verified by absence of `socket.socket` mocks firing in a sandboxed test — NOT reliably testable at this layer, so instead assert that importing the module runs in < 100 ms wall-clock).

### AST-lint regression
- `lint_tree(Path("pipeline/scout"), DEFAULT_RULES)` returns an empty violations list — R1 N/A (scout is not logician), R2 N/A (no loop/ yet), R3 N/A (same), R4 passes trivially (no setattr), R5 passes trivially (no eval).

### No-side-effect import
- `importlib.import_module("pipeline.scout")` does not raise, does not open files, does not instantiate any dataclass at module load.

## Algorithms

None. Round 1 is declarative.

## Failure codes

None. Round 1 defines no failure codes; channel rounds will attach their `F-SCOUT-*` codes in their own `_constants.py`-style modules or pull from a future `pipeline/scout/error_codes.py` (deferred to Round 2 where `health_tuple.py` first raises).

## Coverage target

100% line + branch. Pure data types have no branches; one uncovered line is a bug.

## Dependencies added to pyproject.toml

None. Round 1 uses stdlib (`dataclasses`, `typing`, `json` via existing `pipeline.sovereignty.audit`). `pyyaml` + `cryptography` already present for later rounds. Later rounds will add `httpx`, `feedparser`, `idna` via §11 changelog at that round's commit — **not** here.

## pyproject.toml edit

`[tool.setuptools.packages.find] exclude` list currently contains `"pipeline.scout*"`. Remove that entry. The `pipeline.scout` package becomes part of the installed distribution. No other edit.

## Committee dispatch (post-GREEN)

Standard 5-reviewer Code Thesis Committee per `router.yaml` `code_reviewer_{1..5}`. Reviewers: Codex (openai), Qwen3-32B (alibaba), Llama 3.3 70B (meta), GPT-OSS 120B (openai-oss), Kimi K2 (moonshot with Gemini 2.5 Pro fallback). All-pass merge rule, 1 retry cap. Scope: §2 schema faithfulness, §8 constant fidelity, `__all__` completeness, frozen-discipline, canonical-bytes determinism.

Expected verdict: unanimous PASS (pure-data modules have minimal attack surface). If a reviewer flags anything HIGH, investigate; anything MED ships with inline fix per §8b narrow-edit carve-out if ≤ 5 lines.

## Done-definition

1. Spec card written (this file).
2. RED test module fails before implementation.
3. `_types.py`, `_constants.py`, `__init__.py` land; pyproject edit lands.
4. Full `scripts/run_tests.sh` green (prior 1733 + new Round-1 tests, no regressions elsewhere).
5. Coverage on `pipeline.scout._types` + `pipeline.scout._constants` + `pipeline.scout.__init__` = 100%.
6. `scripts/run_lint.sh` clean against `pipeline/scout/` (AST-lint regression).
7. 5-family Code Thesis Committee unanimous PASS (or PASS-with-inline-fixes).
8. LOCK entry written to `/Users/goldenquill/.claude/projects/-Users-goldenquill-Downloads-GoldenQuill/memory/project_impl_scout_round_1_locked.md`.
9. `MEMORY.md` index updated.
10. Round 2 pre-staged (spec card `scout_round_2_health_tuple.md` drafted) before sign-off.

---

**Lineage:** First Scout implementation round. Consumes nothing from sibling rounds. Exposed to: Round 2 (health_tuple.py), Round 3..7 (channel modules), Round 8 (verify_stage), Round 9 (review_stage), Round 10 (entity_research), Round 11 (orchestration).
