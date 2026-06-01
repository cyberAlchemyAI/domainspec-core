# Spec card — pipeline.scout Round 10 (REVIEW stage + M11 Entity Research Pass + S11 dossier hardening)

**STATUS:** PRE-STAGED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_03_scout.md`
  - §2.4 `ReviewQueueItem` frozen kw-only dataclass (already defined Round 1? — **re-verify**)
  - §2.5 `EntityRosterEntry`, `EntityDossier`, `EntityClaim`, `DossierSignoff` dataclasses — **re-verify Round 1 exports**
  - §3.1 `pipeline.scout.__init__` public re-exports — extend with R10 surface
  - §3.5 Surfaces offered to Section 5 (Pipeline)
  - §4.8 REVIEW stage (`review_stage.py`) — **primary implementation target #1**
  - §4.9 M11 Entity Research Pass + S11a/b/c dossier hardening (`entity_research.py`) — **primary implementation target #2**
  - §6.8 F-SCOUT-R-* failure codes (R-01 only-VERIFIED_FIT-enqueues / R-02 path-outside-org-root / R-03 decision-invalid / R-04 decision-locked-use-admin-UNDO)
  - §6.9 F-SCOUT-D-* dossier failure codes (D-01 TOCTOU re-fstat-before-write / D-02 size-gt-max with `.fstat_size_gt_max` reason-tag / D-03+ per S11c lock verify)
  - §7 property tests — enqueue-only-VERIFIED_FIT invariant, decision idempotency under stripe-collision, TOCTOU-race property via parallel fuzz
  - §8 constants — `SCOUT_REVIEW_LOCK_STRIPES = 64`, `SCOUT_DOSSIER_MAX_BYTES = 5 * 1024 * 1024` (5 MB boundary per A-13)
  - `A-10` / `RT-v1-MED-04` — per-(slug, candidate_id) read-check-write serialisation via `threading.Lock()`
  - `A-v3-02` / `RT-v2-HIGH-02 + MED-07` — striped 64-slot lock array `_REVIEW_DECISION_LOCK_STRIPES`; memory O(stripes), not O(candidates)
  - `A-03` / `CRIT-03` — `sign_off_dossier` `vault_write` moved INSIDE the FD-holding `with` block; O_NOFOLLOW + re-fstat immediately before write (`F-SCOUT-D-01`)
  - `A-v3-06` / `RT-v2-HIGH-04` — dossier partial-read race at exact boundary: replace two-read with `os.fstat(fd).st_size` BEFORE `os.read` (`F-SCOUT-D-02` reason-tag `.fstat_size_gt_max`)
  - `A-13` / `MED-07` — 5 MB strict `>` boundary; §7 unit test at `5 MB + 1 byte`
  - `A-v3-04` / `RT-v2-CRIT-02 + MED-01` — NFC-normalised post-read intent equality check via `_assert_intent_matches` for `entity_research` intents (`source-allowlist-read`, `entity-roster-read`, `dossier-body-write`, `dossier-signoff-write`)
  - Architecture D.1 STAGE 3 (human gate) + D.0 (M11 Entity Research) + S11a/b/c (dossier writer + per-org domain allowlist + cross-domain diversity gate + operator sign-off)
  - Autonomy Rule 1 — `checkpoint(stage="review_enqueue_complete")` on success AND failure per enqueue; `checkpoint(stage="dossier_signoff_complete")` on sign-off; per-entity research checkpoints `entity_research_start` / `entity_research_complete`
- Section 1 consumed surface: `Session`, `checkpoint`, `record_degradation`, `within_org_root` — LOCKED.
- Section 2 consumed surface: `vault_write` (intents: `review-queue-write`, `dossier-body-write`, `dossier-signoff-write`), `vault_read` (intents: `review-queue-read`, `source-allowlist-read`, `entity-roster-read`, `dossier-body-read`, `dossier-signoff-read`), FD broker for O_NOFOLLOW + re-fstat — LOCKED.
- Round 1 consumed: `Candidate` + `VerificationVerdict` + (confirm) `ReviewQueueItem`/`DossierSignoff`/`EntityDossier`/`EntityClaim`/`EntityRosterEntry` frozen kw-only dataclasses — LOCKED.
- Round 4 consumed: `HTTPClient` + `FDBroker` + `NonceRegistry` Protocols — reused via E-017 ninth firing for entity-research live-domain fetches.
- Round 7 consumed: BT12 jurisdiction pre-flight pattern (idna UTS46 Punycode + eTLD→ISO-3166-1 default-deny table) — **candidate for reuse on per-org domain allowlist**. Re-evaluate at build-time; may not apply (allowlist is operator-curated, not jurisdiction-filtered).
- Round 9 consumed: `VerificationVerdict` surface — REVIEW enqueue only permits `verdict == "VERIFIED_FIT"` (F-SCOUT-R-01 enforcement).

**Blueprint hash-at-card:** `0a82d955f95b0fca` (sha3_512(section_03_scout.md)[:16]) — identical to Rounds 1–9. Re-verify at build-time before Step 1.

**Spec-card version:** v1 (pre-staged 2026-04-21 on Round 9 LOCK close)

**Round:** Scout R10 of 11. Consumes Round 9's `ScoutVerifyResult` and emits `ReviewQueueItem` records + per-entity `EntityDossier` + `DossierSignoff` records. **The Round 11 capstone-of-capstones `run_scout_discover_verify_review` composes Rounds 8/9/10 + bounded LLM `_build_fit_rationale(session, candidate, verdict)` and remains scope for the next round.**

---

## Summary

Land two modules:

1. **`pipeline/scout/review_stage.py`** — §4.8 REVIEW stage. `enqueue_for_review(session, candidate, verdict, fit_rationale) -> ReviewQueueItem` writes one canonical-JSON record per VERIFIED_FIT candidate to `{session.slug}/review_queue/{candidate_id}.json` via `vault_write` under intent `"review-queue-write"`. `record_operator_decision(session, candidate_id, decision, reason) -> ReviewQueueItem` reads-checks-writes under a per-(slug, candidate_id) striped lock (64 stripes); rejects ACCEPT/REJECT overwrite with `F-SCOUT-R-04` (operator must use admin-risk UNDO flow); `decision in {"ACCEPT","REJECT","HOLD"}` only (F-SCOUT-R-03 otherwise). **No auto-file invariant** — Scout's DISCOVER/VERIFY paths cannot reach `record_operator_decision`; only operator-initiated Pipeline actions can.

2. **`pipeline/scout/entity_research.py`** — §4.9 M11 Entity Research Pass. `run_entity_research(session, roster: tuple[EntityRosterEntry, ...]) -> tuple[EntityDossier, ...]` iterates the roster and writes one dossier per entity via `vault_write` under intent `"dossier-body-write"` into `orgs/{slug}/dossier/entities/{entity_slug}.md`. Per-org domain allowlist (`orgs/{slug}/dossier/source_domains.yaml`) read via `vault_read` under intent `"source-allowlist-read"` with NFC-normalised `_assert_intent_matches`. Cross-domain diversity gate enforces minimum domain-count per claim. `sign_off_dossier(session, entity_slug) -> DossierSignoff` performs the S11a/b/c three-part lock (path + inode + content_hash) under O_NOFOLLOW + re-fstat-immediately-before-write (A-03 closure); partial-read race closed via `os.fstat(fd).st_size` BEFORE `os.read` (A-v3-06). 5 MB strict `>` boundary (A-13). `read_entity_dossier(session, entity_slug) -> tuple[EntityDossier, DossierSignoff]` is Logician-facing; three-part lock re-verified at read time.

**Public surface additions (`pipeline/scout/__init__.py`):**

```python
# From review_stage:
enqueue_for_review, record_operator_decision, read_review_queue,
ReviewEnqueueRejected, ReviewDecisionInvalid, ReviewDecisionLocked,
F_SCOUT_R_01, F_SCOUT_R_02, F_SCOUT_R_03, F_SCOUT_R_04,

# From entity_research:
run_entity_research, read_entity_dossier, sign_off_dossier,
EntityResearchResult, DossierSignoffVerifyFailure,
F_SCOUT_D_01, F_SCOUT_D_02, F_SCOUT_D_03,  # + S11c sub-codes
```

Bump `__version__` to `0.1.0-scout-r10`. No breaking change to Rounds 1–9 surface.

**Scope delimiter:** Round 10 does NOT dispatch `_build_fit_rationale` LLM calls (that's Round 11 §4.11 capstone-of-capstones). Round 10 does NOT orchestrate DISCOVER + VERIFY + REVIEW end-to-end (that's Round 11). Round 10 lands the two modules individually — Round 11 composes them.

---

## Design decisions (operator-disposed 2026-04-21, reversible — pre-staged)

### review_stage.py

1. **`F-SCOUT-R-01` enforcement at top of `enqueue_for_review`** — reject any verdict whose `.verdict != "VERIFIED_FIT"` before path computation. Law 5 (Applicant Brings the Substance) compliance: UNVERIFIED + VERIFICATION_FAILED + VERIFIED_NOT_FIT all refused.
2. **`F-SCOUT-R-02` path-outside-org-root check** — call `within_org_root(...)` from Section 1 on the computed queue path before `vault_write`. Defense-in-depth even though Section 2 also validates.
3. **Striped lock array `_REVIEW_DECISION_LOCK_STRIPES`** — `list[threading.Lock]` of length `SCOUT_REVIEW_LOCK_STRIPES = 64`. Memory is O(stripes), not O(candidates). Hash collisions serialise unrelated decisions — cheap trade given decisions are idempotent once linearised. `hash((slug, candidate_id)) % 64` — intra-run stability only (PYTHONHASHSEED salt is fine; we do not need cross-process stability).
4. **Read-check-write inside `with _review_lock(...)` block** — `_read_queue_item` → check `existing.operator_decision in {"ACCEPT","REJECT"}` → raise `ReviewDecisionLocked(F_SCOUT_R_04)` if locked → `replace(existing, operator_decision=decision, ...)` → `vault_write`.
5. **`decision in {"ACCEPT","REJECT","HOLD"}` validation** — anything else raises `ReviewDecisionInvalid(F_SCOUT_R_03)` BEFORE lock acquisition (fast-fail, no lock contention for garbage inputs).
6. **`read_review_queue(session) -> tuple[ReviewQueueItem, ...]`** — Logician-facing read; enumerates all `review_queue/*.json` under the org root via `vault_read` under intent `"review-queue-read"` with NFC-normalised `_assert_intent_matches`. Returns sorted tuple by `candidate_id` for determinism.
7. **E-017 injected Protocols** — reuse `SessionLike` / `CheckpointWriter` from Round 9. New Protocol: `ReviewQueueReader` wrapping Section 2 `vault_read` for the enumerate path (enables test fakes without filesystem). NO new Protocol for `vault_write` — already available via injected `VaultWriter` from Round 8.

### entity_research.py

8. **`EntityRosterEntry` schema** — re-verify Round 1 export. Assumed fields: `entity_slug: str`, `canonical_name: str`, `aliases: tuple[str, ...]`, `primary_domain: str`, `jurisdiction_hint: Optional[str]`. Materialised from `orgs/{slug}/dossier/entity_roster.yaml` read at pass entry under intent `"entity-roster-read"`.
9. **Per-org domain allowlist** — `orgs/{slug}/dossier/source_domains.yaml` read under intent `"source-allowlist-read"`. Dossier body claims MUST cite only allowlisted domains; violations emit `F-SCOUT-D-03.domain_not_allowlisted` and the claim is dropped (not the entire dossier — graceful degradation).
10. **Cross-domain diversity gate** — each top-level dossier claim must be evidenced by citations from ≥ 2 distinct domains (per §4.9). Single-domain claims emit `F-SCOUT-D-03.insufficient_domain_diversity` and are flagged `unverified=True` on the EntityClaim record — not dropped.
11. **S11a path-lock**: dossier body written to `orgs/{slug}/dossier/entities/{entity_slug}.md` via `vault_write` under intent `"dossier-body-write"`. Path canonicalised + `within_org_root` check before write.
12. **S11b inode-lock**: after body write, `os.stat(path).st_ino` captured and stored in the `DossierSignoff` record. Re-verified at `read_entity_dossier` time; drift raises `F-SCOUT-D-03.inode_drift`.
13. **S11c content-hash lock**: sha3_512 of dossier body bytes stored in `DossierSignoff.content_hash`. Re-verified at read time; drift raises `F-SCOUT-D-03.content_hash_drift`.
14. **`sign_off_dossier` A-03 closure**: the `vault_write` of the sign-off record is moved INSIDE the FD-holding `with` block. O_NOFOLLOW on open; re-`os.fstat(fd).st_ino` immediately before `vault_write` to detect symlink-swap between body write and signoff write. Drift raises `F-SCOUT-D-01.toctou_inode_drift`.
15. **A-v3-06 partial-read race closure**: `read_entity_dossier` replaces the "read → check size → re-read" pattern with `os.fstat(fd).st_size` BEFORE `os.read`. If size > `SCOUT_DOSSIER_MAX_BYTES = 5 * 1024 * 1024`, raise `F-SCOUT-D-02.fstat_size_gt_max` WITHOUT reading. Strict `>` (A-13): `5 MB` exact passes, `5 MB + 1 byte` fails. §7 unit test pins the boundary.
16. **NFC-normalised post-read intent checks** — call `_assert_intent_matches(identity, expected)` immediately after every `vault_read` in this module. New intents: `source-allowlist-read`, `entity-roster-read`, `dossier-body-read`, `dossier-signoff-read`. Deviation raises `F-SCOUT-D-03.intent_mismatch_post_read` (matches Round 7's Channel F `F-BT12-07` pattern).
17. **No LLM calls in Round 10** — entity research collects factual claims (name/aliases/jurisdiction/primary funders) from allowlisted domains only. LLM-based dossier narrative is Round 11 scope. Round 10's dossier body is template-assembled from `EntityClaim` records.
18. **E-017 injected Protocols** — eight+ seams; reuse from Rounds 4/7/8/9 where possible. New Protocol: `DomainAllowlistReader` (wraps Section 2 `vault_read` under `source-allowlist-read` intent with YAML parse + NFC intent assertion). New Protocol: `EntityRosterReader` (likewise under `entity-roster-read`). The live-domain fetcher for entity claims is a NEW Protocol `EntityClaimFetcher` wrapping Round 4's HTTPClient + FDBroker + nonce registry — **candidate for unification with Round 9's SynopsisFetcher in Round 11 if the surface convergence is worth the refactor**; keep separate for Round 10.

### Cross-cutting

19. **Zero direct filesystem / vault calls** — all persistence through injected Protocols. AST-lint R1/R3 clean.
20. **Zero `eval` / `exec` / `setattr` on operator decisions** — R4/R5 clean.
21. **Public re-exports via `pipeline/scout/__init__.py`** — see Summary block above. Bump `__version__` to `0.1.0-scout-r10`.
22. **Autonomy Rule 1 checkpoint landmarks** — `review_enqueue_start` / `review_enqueue_complete` (both paths) / `operator_decision_complete` (both paths) / `entity_research_start` / `entity_research_complete` / `dossier_signoff_complete`.
23. **Seed-consumption boundary** — Round 10 does NOT consume `run_tiebreak_seed`. The seed's role ends at Round 9 VERIFY truncation.

---

## Failure codes (REVIEW + dossier)

| Code | Raised when | State effect |
|------|-------------|--------------|
| F-SCOUT-R-01 | Verdict != VERIFIED_FIT presented to `enqueue_for_review` | `ReviewEnqueueRejected` raised; no queue write |
| F-SCOUT-R-02 | Computed queue path fails `within_org_root` | `ReviewEnqueueRejected` raised; no queue write |
| F-SCOUT-R-03 | `decision not in {"ACCEPT","REJECT","HOLD"}` | `ReviewDecisionInvalid` raised; no lock held |
| F-SCOUT-R-04 | Existing `ACCEPT`/`REJECT` decision being overwritten | `ReviewDecisionLocked` raised inside the striped lock |
| F-SCOUT-D-01 | TOCTOU inode drift between dossier body write and signoff write | Signoff aborted; `.toctou_inode_drift` sub-tag |
| F-SCOUT-D-02 | Dossier body size > `SCOUT_DOSSIER_MAX_BYTES` via `fstat` pre-read | Read aborted; `.fstat_size_gt_max` sub-tag |
| F-SCOUT-D-03 | Dossier sign-off verify failure (inode / content_hash / path / domain / diversity / intent drift) | `DossierSignoffVerifyFailure` raised with sub-tag |

---

## Constants to pin

Re-verify at build time against §8:
- `SCOUT_REVIEW_LOCK_STRIPES = 64`
- `SCOUT_DOSSIER_MAX_BYTES = 5 * 1024 * 1024` (5 MB, strict `>` boundary)
- Per-intent inline-literal strings — module-scope `Final[str]` in `_constants.py`: `INTENT_REVIEW_QUEUE_WRITE`, `INTENT_REVIEW_QUEUE_READ`, `INTENT_SOURCE_ALLOWLIST_READ`, `INTENT_ENTITY_ROSTER_READ`, `INTENT_DOSSIER_BODY_WRITE`, `INTENT_DOSSIER_BODY_READ`, `INTENT_DOSSIER_SIGNOFF_WRITE`, `INTENT_DOSSIER_SIGNOFF_READ`. Declare once; import at call sites; rebind-resistant.

---

## Minimum test surface (floor ≥ 80; expect ~150 given E-024 8th-firing 2.03× multiplier)

### review_stage.py

1. `TestEnqueueForReviewHappyPath` — VERIFIED_FIT + valid path → queue item written, returned.
2. `TestEnqueueRejectsVerifiedNotFit` — `verdict == "VERIFIED_NOT_FIT"` → `ReviewEnqueueRejected(F_SCOUT_R_01)`.
3. `TestEnqueueRejectsUnverified` — same taxonomy, different verdict.
4. `TestEnqueueRejectsVerificationFailed` — same.
5. `TestEnqueueRejectsPathOutsideOrgRoot` — mock `within_org_root` → False → `F_SCOUT_R_02`.
6. `TestEnqueueIsIdempotent` — enqueue same candidate twice → second call overwrites first (clarify vs RaceOverwrite); open-Q pre-flight.
7. `TestRecordOperatorDecisionAccept` — ACCEPT with empty existing decision → written, returned.
8. `TestRecordOperatorDecisionReject` / `Hold` — same.
9. `TestRecordOperatorDecisionInvalidRaisesR03` — decision="MAYBE" → `ReviewDecisionInvalid(F_SCOUT_R_03)` BEFORE lock.
10. `TestRecordOperatorDecisionLockedRaisesR04` — existing ACCEPT + new REJECT → `ReviewDecisionLocked(F_SCOUT_R_04)` inside lock.
11. `TestRecordOperatorDecisionStripedLockContention` — many (slug, candidate_id) pairs that hash-collide to same stripe → serialisation correctness.
12. `TestRecordOperatorDecisionParallelStress` — N threads issuing decisions on same candidate_id → exactly one ACCEPT, others see F-SCOUT-R-04.
13. `TestReadReviewQueueSortsByCandidateId` — 10 items → returned tuple sorted ascending.
14. `TestReadReviewQueueEmpty` — no queue dir → empty tuple.
15. `TestReadReviewQueueIntentCheckPostRead` — NFC-drifted intent → F_SCOUT_D_03-adjacent or module-specific intent mismatch code.
16. `TestAutonomyRule1CheckpointEnqueueSuccess` / `Failure` — both paths write `review_enqueue_complete`.
17. `TestAutonomyRule1CheckpointOperatorDecision` — both paths write `operator_decision_complete`.

### entity_research.py

18. `TestRunEntityResearchHappyPath` — 3-entity roster → 3 dossiers written, returned in roster order.
19. `TestEntityRosterReadIntentCheck` — NFC-drifted intent → F_SCOUT_D_03 `.intent_mismatch_post_read`.
20. `TestSourceAllowlistReadIntentCheck` — same for allowlist read.
21. `TestDomainNotAllowlistedDropsClaim` — claim citing non-allowlisted domain → dropped, rest of dossier intact, F_SCOUT_D_03 `.domain_not_allowlisted` event emitted.
22. `TestInsufficientDomainDiversityFlagsUnverified` — claim with 1-domain evidence → `EntityClaim.unverified=True`, F_SCOUT_D_03 `.insufficient_domain_diversity` event.
23. `TestSignOffDossierHappyPath` — body written + signoff → three-part lock recorded (path canonicalised, inode captured, content_hash computed).
24. `TestSignOffDossierA03InodeDrift` — mid-sequence symlink swap → `F_SCOUT_D_01.toctou_inode_drift`.
25. `TestReadEntityDossierA_v3_06FstatBoundary` — body of size exactly 5 MB → passes.
26. `TestReadEntityDossierA_v3_06FstatBoundaryPlus1` — body of size 5 MB + 1 byte → `F_SCOUT_D_02.fstat_size_gt_max`, NO bytes read.
27. `TestReadEntityDossierInodeDriftRaisesD03` — inode at read time ≠ signoff inode → `F_SCOUT_D_03.inode_drift`.
28. `TestReadEntityDossierContentHashDriftRaisesD03` — body bytes modified post-signoff → `F_SCOUT_D_03.content_hash_drift`.
29. `TestReadEntityDossierPathDriftRaisesD03` — canonical path mismatch → `F_SCOUT_D_03.path_drift`.
30. `TestNoLLMImports` — module does not import `anthropic` / `openai` / `llm_*`.
31. `TestInjectedProtocols` — all R10 seams (ReviewQueueReader, DomainAllowlistReader, EntityRosterReader, EntityClaimFetcher, CheckpointWriter, VaultWriter, ClockFn, SessionLike) honoured via fakes.
32. `TestKWOnly` — positional calls to R10 public entries rejected.
33. `TestPublicSurface` — `__version__` range-check `rN ≥ 10` (E-025); all new public names reachable via `pipeline.scout`.
34. `TestNoDirectVault` — AST-lint DEFAULT_RULES clean on both modules.
35. `TestAutonomyRule1CheckpointEntityResearch` — `entity_research_start` / `entity_research_complete` land on both success and mid-pass exception.
36. `TestAutonomyRule1CheckpointDossierSignoff` — `dossier_signoff_complete` lands on both paths.

**Adversarial (≥ 6 per E-024 8th-firing precedent):**

- `TestAdv_StripedLockHashCollisionCorrectness` — force `hash((slug, cid1)) % 64 == hash((slug, cid2)) % 64`; parallel decisions on cid1 and cid2 must each serialise correctly (no cross-contamination of stored decision).
- `TestAdv_SignOffDossierSymlinkSwapMidWrite` — symlink-swap orchestrated between body write and signoff write; `F_SCOUT_D_01.toctou_inode_drift` MUST fire before signoff is persisted.
- `TestAdv_ReadEntityDossierFstatRaceDuringRead` — fstat returns ≤ 5 MB, then another process truncates/extends the file; `os.read` path must not panic.
- `TestAdv_EnqueueWithCorruptedVerificationVerdict` — VerificationVerdict with tampered verdict field → F_SCOUT_R_01 fires on the string compare; no downstream write.
- `TestAdv_RecordOperatorDecisionStressFuzz` — 1000 random (slug, candidate_id, decision) triples across 16 threads → no lost updates, no spurious lock-held-forever.
- `TestAdv_EntityResearchAllowlistYamlMalformed` — YAML parse raises → `F_SCOUT_D_03.allowlist_parse_error`; pass aborts cleanly with checkpoint write.
- `TestAdv_DossierBodyWriteRaceWithSignoff` — signoff_write racing a second body_write on the same path; either body write wins or signoff wins, but no half-state (invariant pinned by re-fstat).
- `TestAdv_DossierMaxBytesBoundaryExact` / `Plus1` — already in nominal (#25/26); adversarial variant uses an actual 5 MB byte-literal body for end-to-end read-path exercise.

---

## Engineering risks to pre-flight

- **`ReviewQueueItem` / `DossierSignoff` / `EntityRosterEntry` / `EntityDossier` / `EntityClaim` schemas** — blueprint §2.4–§2.5 cites these dataclasses; re-verify Round 1's `_types.py` exports before build. If any are missing, file a Round-1 v1.1 spec-card deviation (add to types, no canonical-bytes change) and land the types in a pre-R10 micro-amend.
- **`within_org_root` availability** — Section 1 surface; confirm Round 10 can call it directly without a new Protocol seam. If not, add to the existing SessionLike Protocol.
- **`SCOUT_REVIEW_LOCK_STRIPES = 64` vs `SCOUT_MAX_WORKERS = 6`** — lock count is independent of pool sizing; confirm both pins live in `_constants.py` with distinct names.
- **E-017 9th firing** — `ReviewQueueReader` / `DomainAllowlistReader` / `EntityRosterReader` / `EntityClaimFetcher`. Evaluate at build-time whether the four Reader Protocols should collapse into a single `IntentedVaultReader(intent: str)` Protocol. Current recommendation: keep per-intent Protocols for intent-specific validation wiring.
- **E-024 8th firing 2.03× multiplier** — Round 9 landed 142 tests against floor ≥ 70. Round 10 projects 150+ against floor ≥ 80; two-module round so test count is additive (review_stage ~60, entity_research ~90, shared cross-cutting ~10).
- **E-026 6th firing** — tests patching module state use `__globals__` direct-dict dispatch or `__module__` lineage checks; not `sys.modules` identity.
- **E-028 3rd firing (if needed)** — any contract-unreachable branch (e.g. striped-lock array always 64, `os.fstat` after successful `open`) gets `# pragma: no cover` + docstring rationale.
- **L-001 enforcement** — the spec card's failure-code taxonomy MUST match blueprint §6.8 / §6.9 verbatim at build time. If the spec card diverges from the blueprint, blueprint wins and the deviation is documented in-module (Round 9 pattern: four deviations logged).
- **BT12 Round 7 jurisdiction pre-flight** — do NOT reuse for per-org domain allowlist. Allowlist is operator-curated; BT12 is jurisdiction-filtered against a frozen eTLD table. Different threat model.
- **No REVIEW ordering semantics** — Round 10 does NOT impose a read order on the review queue beyond `sorted(candidate_id)`. Priority ordering is a Pipeline concern (Section 5), not a Scout concern.

---

## Lessons-applied-from-start

- **E-017** (injected-Protocol pattern) — 9th Scout firing. ≥8 seams across the two modules: 4-5 new (ReviewQueueReader, DomainAllowlistReader, EntityRosterReader, EntityClaimFetcher, DossierSignoffWriter?) + 4+ reused (SessionLike, CheckpointWriter, DegradationWriter, VaultWriter, HTTPClient/FDBroker/NonceRegistry).
- **E-024** (2.03× multiplier) — spec-card floor ≥80 tests, expect ~150 given two-module scope. Adversarial count ≥ 6.
- **E-025** (range-check version pin) — `test_version_pin_rN_ge_10` via tuple comparison. **Applied from start.**
- **E-026** (sys.modules-reload fragility) — import-hygiene tests inspect `__dict__` lineage or use `__globals__` direct-dict patch, not `sys.modules`. **Applied from start (6th firing candidate).**
- **E-027** (lint_tree directory vs single-file) — AST-lint regression tests always pass a directory root.
- **E-028** (pragma: no cover doctrine) — formally promoted at Round 9 2nd firing; applied to any contract-unreachable defensive branch.

---

## Round 11 roadmap (NOT this round's scope — for continuity)

**Round 11:** `run_scout_discover_verify_review(session) -> ScoutRunResult` (§4.11 capstone-of-capstones) — composes Round 8 DISCOVER + Round 9 VERIFY + Round 10 REVIEW + bounded LLM `_build_fit_rationale(session, candidate, verdict) -> str`. §3.5 Pipeline-facing entry. 5-family Code Thesis Committee dispatch recommended for R11 given composition surface (4 stages + LLM fan-out). Scout build COMPLETE at Round 11 LOCK.

---

## Spec-card version history

- **v1 (2026-04-21)** — pre-staged on Round 9 LOCK close. Operator-disposed decisions 1–23 above. Blueprint hash pinned `0a82d955f95b0fca`. Re-verify Round 1 exports of `ReviewQueueItem` / `DossierSignoff` / `EntityRosterEntry` / `EntityDossier` / `EntityClaim` at build-time Step 0.
