---
title: Blueprint §0.5 Interface Index — Amendment for Cedar policy primitive-kind split (2 new primitive_kind values + 2 paired-commit rows)
filed: 2026-04-20
operator: Josh
amendment_status: DRAFT — awaiting Thesis-round audit (Editor + Judge + Red Team) then LOCK as the next free §0.5 version slot after §0.5 v5 LOCKED 2026-04-19 and any pending sibling amendments (GPP `section_00_5_v5_amendment.md`, ARCH-04 `section_00_5_arch04_ast_lint_amendment.md`).
parent_lock: pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md  (§0.5 v5 LOCKED 2026-04-19, 101 rows)
supersedes_relationship: row-append + vocabulary extension. No existing row modified. §0.5.3.1 closed vocabulary extended from 13 values to 15 values; operator approval recorded in-amendment per §0.5.3.1 ("Vocabulary is closed in v1; v2 additions go through operator approval").
companion_code_files:
  - vault_shared/cedar/org_isolation.cedar                              # SKELETON — M15 signed-commit + M15.3 HIGH-severity admin-risk ledger entry required before load-bearing
  - pipeline/logician/cedar_policies/compound_commit.cedar              # SKELETON — Section 4 LOCK cycle + AST-lint-surface coverage required before load-bearing
companion_blueprint_anchors:
  - section_02_vault_topology.md §2.6 (Cedar entity shapes)              # v7.1 parent-backfill LOCKED 2026-04-19
  - section_02_vault_topology.md §3  (seed-file ledger)                  # v7.1 parent-backfill LOCKED 2026-04-19
  - section_02_vault_topology.md §4.10.5 (signed compound-kind registry) # v7.1 parent-backfill LOCKED 2026-04-19
  - section_04_logician.md §4.11 (compound-commit predicate + Cedar companion)  # v2.1 LOCKED 2026-04-19
  - section_04_logician.md §4.2.1 row #17 (PRE-gate compile check, M14)  # v2.1 LOCKED 2026-04-19
  - section_04_logician.md §4.2.1 row #4  (PRE-gate signature + ledger-head check) # v2.1 LOCKED 2026-04-19
parent_wins_discipline: row 1 points at §2 Vault Topology v7.1 (source of truth for seed-file ledger + Cedar entity shapes). Row 2 points at §4 Logician v2.1 (source of truth for the compound-commit predicate and the CedarEvaluator boot path). Both parents are LOCKED.
row_count: 2
vocabulary_extension: adds `cedar-policy-seed` and `cedar-policy-code` to §0.5.3.1 closed vocabulary. Rationale: the two .cedar-file classes have asymmetric lifecycles that consumers MUST distinguish (seed = M15 signed-commit + operator re-type on change; code = Section-4 LOCK cycle + AST-lint surface). Collapsing them into a single `cedar-policy` kind — or re-using existing `mechanism` — hides the lifecycle asymmetry from downstream tooling that needs to know which integrity path covers a given file.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; both rows must be present in the index or the commit fails closed.
version_wording_discipline: "LOCKED" refers to on-disk LOCKED state only; target-LOCK wording for forward-looking items.
---

# Amendment intent

This amendment is the paired-commit §0.5 counterpart for the two Cedar policy skeleton files authored 2026-04-20:

- `vault_shared/cedar/org_isolation.cedar` — the SHARED + SAME-ORG permit rules that, when signed under M15, supersede the Python fallback evaluator `pipeline/logician/cedar_eval.py::evaluate_org_isolation` as the authoritative decider for F-CEDAR-01.org_isolation_deny.
- `pipeline/logician/cedar_policies/compound_commit.cedar` — the Cedar companion policy for the Option-B compound-commit predicate defined in §4 v2.1 §4.11 (the fourth and final commit gate after required-intents multiset equality + stored hash-binding equality + session match).

Both files exist on disk as SKELETONS under explicit "NOT YET SIGNED" / "NOT YET DEPLOYED" headers. Neither is load-bearing at v0.1 runtime — the Python evaluator remains authoritative until M15 seals the seed file and Section 4 CedarEvaluator wires the code file. But both are already referenced by LOCKED blueprint sections (§2 v7.1 §3 seed-file ledger for the seed; §2 v7.1 §4.10.5 + §4 v2.1 §4.11 for the code), so both belong in the Index now — under `stability_tier = PENDING_PARENT_BACKFILL` with the backfill being the load-path activation (M15 signed-commit for row 1; Section 4 CedarEvaluator boot + AST-lint coverage for row 2), not a parent re-lock.

The amendment also extends §0.5.3.1's closed primitive_kind vocabulary by two values. The split is load-bearing: a consumer that wants to answer "which integrity path covers this .cedar file?" cannot answer correctly if both file classes carry the same `primitive_kind`. The M15 seed-manifest ledger walks only `vault_shared/cedar/*.cedar` at boot; the AST-lint + Section-4-blueprint-hash surface walks only `pipeline/logician/cedar_policies/*.cedar`. Collapsing the kinds into a single `cedar-policy` would force every downstream consumer to rediscover the asymmetry by string-matching the `defined_at` path prefix — a classic topology-drift hazard.

# Vocabulary extension (§0.5.3.1)

§0.5.3.1 currently enumerates 13 closed values:

> `mechanism`, `schema`, `failure-code`, `constant`, `allowlist-row`, `invariant`, `test`, `interface-contract`, `admin-risk-entry`, `pre-gate-check`, `post-gate-check`, `architecture-mechanism`, `marker`

This amendment adds two values, bringing the count to 15:

14. **`cedar-policy-seed`** — a Cedar policy text file stored under `vault_shared/cedar/*.cedar`. Loaded at boot (§2 v7.1 §9 step 9) by `pipeline/vault/m15_ledger.py::cedar_policy_loader_load_all`, re-hashed SHA-3-512 against the pinned `VaultSharedFrozenRoot.content_hashes_hex`, returned to the Section 4 CedarEvaluator. Lifecycle: M15 signed-commit + M15.3 HIGH-severity admin-risk ledger entry on every change. Drift at any PRE-gate boot → `CedarPolicyLoadFailed` (F-CEDAR-01) → hard abort. Governed by the M15 operator re-type discipline, NOT by a Section 4 LOCK cycle.

15. **`cedar-policy-code`** — a Cedar policy text file stored under `pipeline/logician/cedar_policies/*.cedar` (or a per-Section analogue that the Section's blueprint explicitly declares). Loaded at Section 4 module boot by the CedarEvaluator. Covered by the code-tree integrity surface: AST-lint harness (ARCH-04 `pipeline/linting/ast_lint.py`) walks the `.py` siblings of the policy file; the signed blueprint-hash covering the parent Section file (e.g., `section_04_logician.md` v2.1) pins the policy's authoring window. Lifecycle: changes require a new parent-Section LOCK cycle, NOT an M15 operator re-type. Drift between the on-disk bytes and the Section's referenced expected bytes → Section 4 lock-audit failure surface.

Both new kinds are Tier 1 stable in their semantics; the instance files are skeletons.

The vocabulary is still closed after this extension: no consumer may introduce a 16th value without a further amendment + operator approval.

# Proposed 2 new §0.5 rows

Each row carries the §0.5 v5 schema: `primitive_id`, `defined_at`, `parent_lock_version`, `parent_lock_commit_hash` (`TO_BE_PINNED_AT_COMMIT`), `primitive_kind`, `description`, `introduced_in_index_version`, `stability_tier`.

## Group — Cedar policy seed (1 row)

| # | primitive_id | defined_at | parent_lock | kind | stability |
|---|---|---|---|---|---|
| 102 | `vault.cedar_policy.org_isolation_seed` | `section_02_vault_topology.md` §3 (seed-file ledger) + §2.6 (Cedar entity shapes); on-disk instance `vault_shared/cedar/org_isolation.cedar` (SKELETON as of 2026-04-20) | §2 v7.1 | cedar-policy-seed | PENDING_PARENT_BACKFILL (load-path activation — M15 signed-commit + M15.3 HIGH-severity ledger entry; on activation → STABLE) |

**Description:** Cedar policy seed carrying two `permit` rules: (1) SHARED vault access — any resource flagged `is_shared` permits read+write to any session principal; (2) SAME-ORG access — a session bound to `org_slug` S may read+write any VaultPath whose `org_slug_hint` is S. Cedar default-deny covers everything else → F-CEDAR-01.org_isolation_deny. Python fallback evaluator at `pipeline/logician/cedar_eval.py::evaluate_org_isolation` authoritative at v0.1 until M15-sealed. File integrity is belt-and-suspenders: (a) the M15 seed manifest pins the file's SHA-3-512 hash; (b) `cedar_policy_loader_load_all` re-hashes at every boot; (c) Section 2 canonical_path-vs-org_root filesystem check gives a second enforcement layer independent of Cedar.

## Group — Cedar policy code (1 row)

| # | primitive_id | defined_at | parent_lock | kind | stability |
|---|---|---|---|---|---|
| 103 | `logician.cedar_policy.compound_commit` | `section_04_logician.md` §4.11 (compound-commit predicate + Cedar companion) + `section_02_vault_topology.md` §4.10.5 (signed compound-kind registry); on-disk instance `pipeline/logician/cedar_policies/compound_commit.cedar` (SKELETON as of 2026-04-20) | §4 v2.1 + §2 v7.1 | cedar-policy-code | PENDING_PARENT_BACKFILL (load-path activation — Section 4 CedarEvaluator boot + AST-lint surface coverage + `pipeline/logician/compound_commit.py` target module ship per spec card `pipeline/engineering/spec_cards/compound_commit.md`; on activation → STABLE) |

**Description:** Cedar policy covering the fourth commit gate of the Option-B compound-transaction enforcement. Principal: `Seat::"Dispatcher"` (Section 2 vault dispatcher — the only seat permitted to commit a compound transaction). Action: `VaultAction::"commit_compound_txn"` (the §4.10.7 entry point). Resource: the enumerated `CompoundTxnKind` set; v0.1 = exactly `{index_amendment}`. Permit condition: the three context booleans `required_intents_present`, `hash_bindings_valid`, `session_matches` — each the stored outcome of one of the first three predicate phases in §4.11 (§9.8.2 / §9.8.3 / §9.8.4 test vectors). Cedar does not re-derive them; it affirmatively signs off as the final commit gate. Adding a new compound kind (e.g., eventual report-submission, content-vertical publish) requires a Section 4 LOCK cycle to add a new permit rule — the v0.1 enumeration is a lock, not a default.

# Row-count reconciliation

Adding 2 rows. Current §0.5 v5 LOCKED row count = 101. If this amendment LOCKs before any pending sibling amendment (GPP v5 draft, ARCH-04 ast_lint v1 draft), new count = 103. If siblings LOCK first, this amendment rebases its row numbers at merge time; the `primitive_id` values are insensitive to row-number drift (they are identity, not position).

The F-INDEX-STALE PRE-gate checks that the declared row count matches the actual row count at commit time — there is no arithmetic hazard introduced by this amendment because the row count update is mechanical (101 + 2 = 103, or the corresponding sum if siblings land first).

# Parent_lock_commit_hash population

At commit time, each row's `parent_lock_commit_hash` is populated with the SHA-3-512 canonical-bytes hash of the parent section file at the moment of commit. Row 102 points at §2 v7.1 (one hash). Row 103 points at both §4 v2.1 and §2 v7.1 (two hashes; the `parent_lock_commit_hash` field canonicalizes the primary parent — §4 v2.1 — and the secondary parent hash is recorded in a follow-on `binds_to = IDX:v{N}:vault.compound_txn_registry` row added by a later amendment when §2 v7.1's compound-kind registry grows its own Index row).

# §0.5 front-matter updates at LOCK

- `version` → next free slot after §0.5 v5 LOCKED 2026-04-19 and any sibling amendments that LOCK ahead of this one.
- `parent_relationships` → add `v7.1 blueprint §2 Vault Topology + v2.1 blueprint §4 Logician` as the parent lock set for the 2 new rows.
- `row_count` → previous row count + 2.
- `discipline_version` → unchanged (parent-wins paired commit).
- `§0.5.3.1 closed vocabulary` → extended from 13 values to 15 values; `cedar-policy-seed` and `cedar-policy-code` added with full definitional prose per this amendment's "Vocabulary extension" section.

# Non-goals for this amendment

- Does not modify any v5 (or earlier) row.
- Does not touch F-INDEX-STALE semantics.
- Does not wire either .cedar file into a runtime load path — both remain SKELETON until their respective load-path-activation backfills (M15 signed-commit for row 102; Section 4 CedarEvaluator boot + AST-lint coverage + `compound_commit.py` target-module ship for row 103).
- Does not retroactively re-kind any existing Index row. Prior rows that could arguably have carried `cedar-policy-*` kinds (there are none in v5) remain unaffected.
- Does not author the `pipeline/logician/compound_commit.py` module — that ships via its spec card at `pipeline/engineering/spec_cards/compound_commit.md` (filed same session, 2026-04-20).
- Does not modify the GPP draft amendment's row count. The GPP amendment and this amendment are siblings in the §0.5ThesisRound queue; whichever LOCKs first takes the lower version slot, the other rebases its row numbering at merge time.

# Paired-commit reminder

This amendment commits atomically with the two Cedar policy skeleton files at their canonical on-disk locations:

- `vault_shared/cedar/org_isolation.cedar`       (SHA-3-512 hash `TO_BE_PINNED_AT_COMMIT`)
- `pipeline/logician/cedar_policies/compound_commit.cedar`  (SHA-3-512 hash `TO_BE_PINNED_AT_COMMIT`)

F-INDEX-STALE PRE-gate in §0.5 v5 fails-closed if the 2 rows are not in the index at the moment of commit. The on-disk files remain SKELETONS under their respective explicit-status headers until the load-path-activation backfills land.

# Thesis round expectations

- **Audit pass 1 (Editor + Judge):** Editor audits primitive_id naming consistency with existing §0.5 row naming conventions (dotted segments, parent-section short tag as first segment); parent_lock_version cross-references (§2 v7.1 + §4 v2.1 both LOCKED); description grounding against the two parent subsections cited; vocabulary-extension prose clean and non-overlapping with existing 13 kinds. Judge scores against §0.5 v5 discipline rubric (parent-wins, same-commit landing, F-INDEX-STALE clean, vocabulary-extension rigor).
- **Audit pass 2 (Red Team + Reasoner):** Red Team adversarial on: does the two-kind split actually carry load-bearing information, or could `cedar-policy` (one kind) + `defined_at` prefix suffice? Does `stability_tier = PENDING_PARENT_BACKFILL` correctly describe load-path activation (the skeleton-to-live transition), or should a new tier be introduced for "file exists on disk as skeleton but is not yet in a runtime load path"? Can a stale M15 seed-manifest entry (e.g., operator re-types after editing row 102's .cedar bytes but forgets to regenerate the seed manifest) produce a false-green PRE-gate? Reasoner audits decision journal for: was `mechanism` explicitly considered and rejected as the kind? was the single-kind `cedar-policy` alternative considered and rejected? was operator approval for the vocabulary extension recorded in-line?
- **Synthesis:** operator + Opus 4.7 emits LOCK commit atomically with the two skeleton files at their canonical paths.

# End of amendment
