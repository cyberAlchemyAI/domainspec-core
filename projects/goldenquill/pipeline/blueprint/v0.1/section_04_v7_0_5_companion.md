---
title: §4 Logician — v7.0.5 companion delta (7 new gate families with deterministic enforcement specs)
filed: 2026-05-10
parent_section: pipeline/blueprint/v0.1/section_04_logician.md
parent_amendment: pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md
status: COMPANION — v7.0.5 LOCKED 2026-05-10 (lock_history row 179)
---

# §4 Logician v7.0.5 companion delta — 7 new failure codes

This companion catalogs the §4 Logician gate families registered by architecture amendment v7.0.5. Full enforcement spec and Cedar policy paths live in the amendment §5 — this file pins the §4 gate-registry binding.

## Failure code registry — v7.0.5 additions

| Code | Phase | Type | Severity | Cycle |
|---|---|---|---|---|
| `F-MATCH-DB-CROSS-ORG` | PRE | path-validation | P0 (Law 3) | Cycle 1 RT-01 |
| `F-VECTOR-NS-MISMATCH` | PRE | tool-arg-validation | P0 (Law 3) | Cycle 1 RT-04 |
| `F-CHANNEL-G-CROSS-ORG-LEAK` | POST-extract | regex + decode-rescan | P0 (Law 3) | Cycle 1 RT-06 |
| `F-CHANNEL-G-SANITIZATION-BYPASS` | advisory | downstream-transform | P1 | Cycle 2 Probe B |
| `F-MATCH-DB-CONSENT-TIER-VIOLATION` | PRE-write + Stage-5-read | audit_chain signature | P1 (Law 4 + sovereignty) | Cycle 1 RT-05 |
| `F-FUNDER-CORPUS-STALE` | POST-cite | per-funder-type defaults | P2 (RFA-truth) | Cycle 1 RT-07 |
| `F-FUNDER-CORPUS-INTEGRITY` | PRE-load + POST-load | SHA3-512 per-read | P0 (Law 5 — fabrication via tamper) | Cycle 1 RT-03 |

## §4.v7-0-5 Enforcement specs (from amendment §5)

### F-MATCH-DB-CROSS-ORG (Logician PRE-check #17 extension)

1. PRE-check parses session-bound `org_slug` from PROJECT_CONTEXT.md at session start.
2. Every Match DB read intercepted at I/O wrapper. Wrapper calls `logician.assert_path_session_scoped(path, session_slug)` BEFORE opening the file.
3. Path validated against `^orgs/<session_slug>/match_database/[^/]+\.(yaml|yml|json)$` (exact slug match; no `..` traversal; no symlink follow).
4. Cedar policy at `pipeline/vault/policies/match_db_session_scoped.cedar`.
5. Mismatch → raises and aborts I/O. Audit-chain event emitted on every PRE-check pass AND fail.
6. Fail-closed semantics: failure code RAISES and ABORTS; does not log-and-continue.

### F-VECTOR-NS-MISMATCH (Logician PRE-check #18 — NEW)

1. Pydantic AI tool definition for `vector_store.search()` declares `org_slug: str` REQUIRED, no default.
2. Tool invocation passes through PRE-check #18; validates `org_slug` against session context.
3. Workspace-scoped namespaces (`funder_intel/`) skip slug check; per-org namespaces (`kfr_facts/<org_slug>/` and forward `match_db/<org_slug>/`) enforce strict match.
4. Mismatch or missing → raises and aborts tool call.

### F-CHANNEL-G-CROSS-ORG-LEAK (POST-Channel-G-extract)

1. Channel G extraction pipeline runs decode-then-rescan cascade (base-64 / hex / URL-encoding) BEFORE regex.
2. POST-extraction Logician scans sanitized output for `match_[a-f0-9]{32}` patterns.
3. Any cross-org `match_id` remaining → raises and rejects content from Scout candidate roster.

### F-CHANNEL-G-SANITIZATION-BYPASS (advisory)

1. Downstream components that transform extracted text MUST invoke sanitization wrapper as POST-transform check.
2. Bypass detected → emits advisory at next REVIEW gate (does not block; flagged for operator).

### F-MATCH-DB-CONSENT-TIER-VIOLATION (PRE-write + Stage-5-read)

**Trigger A (forward-design — Stage-5 only):** commons-side query reads Match DB beyond consent tier.
**Trigger B (v0.1-active):** consent_tier mutation lacks `operator_signature_per_consent_tier_change` row in audit_chain with fresh UTC timestamp.

1. Match DB write wrapper validates audit_chain append on every consent_tier change.
2. Missing signature → raises; write rejected.
3. No silent upgrade path — `my_eyes_only → composable_with_others` requires operator-signed write even by operator's own admin privileges.

### F-FUNDER-CORPUS-STALE (POST-cite)

Per-funder-type defaults: federal_agency 365d / regional_authority 365d / state_agency 365d / private_foundation 180d / community_foundation 180d / corporate_giving 90d / cdfi 180d / county/city 365d.

1. POST-check after Scout match reasoning composition AND after Scribe KGIE preflight.
2. Stale doc cited → raises; flagged for operator REVIEW; downstream draft held.

### F-FUNDER-CORPUS-INTEGRITY (PRE-load + POST-load — per-read, not just ingestion)

1. **At ingestion:** SHA3-512 hash computed and stored as `content_hash`.
2. **At every load:** read pipeline wrapper recomputes SHA3-512 of on-disk bytes and compares against `content_hash` BEFORE bytes reach the seat.
3. Mismatch → raises; doc excluded from seat working set; quarantined to `vault_shared/funder_intelligence/_quarantine/<doc_hash>.<ext>`.
4. **Process-scope BYTE caching FORBIDDEN** (Cycle 2 Probe C closure): per-`load()` re-hash regardless of prior verification. Parsed-content caching permitted post-verification within single agent invocation.
5. Audit row emitted on every PRE-load and POST-load check.

## Composition with v7.0.4 KFR family

KFR family (F-LOGICIAN-FACT-DRIFT-* — 9 codes per v7.0.4) and v7.0.5 family (7 codes) operate on orthogonal substrates:
- KFR family validates per-org factual claims about THIS client.
- v7.0.5 family validates per-funder corpus integrity AND per-org Scout reasoning trail isolation.

Both fire as POST-gates after Scribe; both fire as PRE-gates before Scout / Scribe / Editor / Judge / Red Team reads.

## Composition with v7.0.7 classification routing (forward-pending)

When v7.0.7 LOCKs (currently SCOPING DRAFT, parallel to v7.0.5):
- Match DB `narrative_summary_classification` per-entry interacts with classification-aware split-context routing.
- F-MATCH-DB-CONSENT-TIER-VIOLATION + classification routing co-enforce that Confidential narrative content stays local-routed regardless of consent tier.

Full enforcement specs at `pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md` §5.
