---
title: Technical Backlog — the collaborator work queue
filed: 2026-05-17
audience: technical collaborator (Paul Norton, candidate engineer, paid reviewer)
companion_docs: docs/COLLABORATOR_HANDOFF.md · docs/AGENT_CONTEXT_INDEX.md · docs/LOCAL_DEVELOPMENT.md
front_door: PROJECT_STATUS.md (root)
maturity_vocabulary: RUNTIME_MATURITY_MATRIX.md (root, seven-state taxonomy)
canonical_cleanup_plan: docs/github_product_truth_cleanup_plan_v1_1_2026-05-17.md (Track 8)
---

# Technical Backlog

This is the collaborator queue. Read `docs/COLLABORATOR_HANDOFF.md`
first — it tells you what role you're playing. This doc tells you what to
pick up. The queue is not a plan of record; the operator can reprioritize
at any time. The queue is the surface where reprioritization is visible.

Sections, in priority order:

1. **Gate 1 blockers** — must complete before internal replay with Paul.
2. **Gate 2 blockers** — must complete before the first paid client.
3. **Safe first tasks** — the good-first-issue equivalent.
4. **Do-not-touch surfaces** — restated from the handoff doc so it lives
   in the queue too.
5. **Needs Josh decision** — work that is ready to start but waiting on
   an operator call.
6. **Needs architecture / LOCK process** — work that cannot land via
   ordinary PR; it requires a blueprint amendment and a ceremony.

## 1. Gate 1 blockers (internal replay with Paul)

Gate 1 is the internal-replay milestone: Josh and Paul reproduce a full
grant cycle end-to-end in a controlled environment using a real client's
data, with all five Laws enforced. Items in this subsection are the
runtime-or-content blockers that gate the replay; the cleanup /
advisories subsection below lists items that should land alongside but
do not themselves block the replay.

### 1a. Gate 1 runtime/content blockers

- **F-DIALECT-\* operator-content items still pending.** The 91-term
  apolitical-dialect audit needs operator-content edits before the
  F-DIALECT-* family is fully wired against the term registry. Cite:
  `docs/assessment_2026-05-16_72h_retrospective.md` + the F-DIALECT
  predicate-realization session on 2026-05-16T18:45:00Z. Specifically:
  the 91-term audit, the card-content rebinding for the four-axis enum
  retirement, and the Law 4 phrase-edit pass on existing card text.
  Operator-content — collaborator can stage the diff, cannot author.
- **Pre-existing capstone-hash drift** flagged by §4 v2.x.6 runtime
  companion landing on 2026-05-17. Three tests fail in
  `tests/seats/` against pinned capstone hashes in the `__init__` of
  the affected seats. Pre-existing WIP, not a regression — but a clean
  Gate 1 replay needs the failures reconciled (either rolled back, or
  the new hashes operator-pinned). Cite:
  `daily_logs/2026-05-17.md` §"§4 v2.x.6 runtime companion landed"
  point 4 (Verification).

### 1b. Gate 1 cleanup / advisories

- **198 `row: null` legacy lock_history rows (ledger hygiene).** The
  pre-`row`-field rollout left 198 rows in `lock_history.v1.jsonl`
  without a `row:` field. Open question: back-fill or keep audit-only.
  Cite: `docs/tilth_full_audit_prompt_v1_1.md` §"Failure mode (forward-
  looking)". Ledger-hygiene only — *not* a runtime gate-blocker — but
  Gate 1 replay should not surface "what are these rows" as a question,
  so resolving the back-fill-vs-audit-only call before the replay is
  preferable.
- **Phantom memory ref.** Mostly closed via the audit prompt v1.1
  systematic diagnosis pass. Cite the corresponding handoff for the
  final closure status; if any residual reference remains, surface it
  as a Gate 1 punch-list item.

## 2. Gate 2 blockers (first paid client)

Gate 2 is the first-paid-client milestone: a paying customer's first
deployment ships with the signed classification register, the runtime
card loader live, and the on-demand heavy Judge swap exercised. Per
`docs/tilth_full_audit_prompt_v1_1.md`, the canonical Gate 2 set is:
*CC-004 signed-asset-manifest · CC-007 finalization · CC-008 redaction
processor (v0.2) · CC-009 M13 end-to-end · Reflection Packet v0.2 first
wave · `R-NO-DIRECT-PROVIDER-HTTP` mature · LIVE/DORMANT gate-family
manifest.*

- **CC-008 Logfire disable-by-default end-to-end verification.**
  Logfire is disabled-by-default at v0.1; the AST-lint rule
  `R-INTAKE-NO-LOGFIRE-IMPORT-BEFORE-ENV` catches the static case.
  End-to-end runtime verification (boot the pipeline, confirm zero
  Logfire HTTP egress without an explicit operator opt-in, confirm the
  fail-closed posture on misconfiguration) is the Gate 2 close. Cite:
  audit prompt v1.1 §"Acceptance question" for data egress.
- **CC-009 M13 end-to-end.** M13 is the audited bypass mechanism for
  the Logician fail-closed posture; Gate 2 requires the full
  audit-trail-and-decision path exercised against a real grant cycle.
- **Reflection Packet v0.2 first wave activation.** The Reflection
  Packet is DORMANT at v0.1; the v0.2 first wave handoffs at
  `pipeline/handoffs/ws_reflection_packet_v0_2_first_wave_handoff_2026-05-15.md`
  + `ws_reflection_v0_1_hook_handoff_2026-05-10.md` are the spec
  surface. The Gate 2 close is "Reflection Packet writes activate,
  reflection_agent fires on a real cycle, the Archivist v1.x stub
  remains DORMANT but the v0.2 hook is LIVE."
- **`R-NO-DIRECT-PROVIDER-HTTP` maturation.** The §4 v2.x.6 amendment
  extended the rule's `direct_provider_call_without_wrapper` sub-tag;
  Gate 2 maturation is full-tree coverage (not just the router) plus
  the test surface that proves no path bypasses `provider_boundary.py`.
  Cite: `daily_logs/2026-05-17.md` point 2.
- **LIVE/DORMANT gate-family manifest formalization.** Currently the
  state of each F-* family (LIVE, scaffold, dormant, NotImplementedError-
  pending) is inferable from the predicate bodies on disk; Gate 2
  requires a single canonical manifest the operator signs. Cite: audit
  prompt v1.1 §"LIVE/DORMANT gate-family manifest."

## 3. Safe first tasks (good-first-issue equivalent)

Pick from this section for your first few PRs. Each item is bounded,
non-LOCKed, and visible — landing it gives you a clean PR cycle to
calibrate the workflow.

- **README polish and `docs/LOCAL_DEVELOPMENT.md` improvements** as you
  discover gaps. The cleanup plan v1.1 lists these as "single-day quick
  wins" (P0 items from the form/function analysis — pyproject readme
  flip, README deleted-sentence-restore, README contact-handle revert).
- **AST-lint rule additions** for known patterns. The §4 v2.x.6
  amendment extended `R-NO-DIRECT-PROVIDER-HTTP` with a new sub-tag;
  similar narrow extensions for known footguns are welcome. Cite:
  `pipeline/linting/` + the rule pattern in
  `r_no_direct_provider_http.py`.
- **Test coverage on dormant gate families.** F-CARDS-* and several
  F-PACKET-* primitives are NotImplementedError-pending; a coverage
  pass that adds parametrized "the gate exists, errors as expected, and
  the import path is correct" tests is bounded work that strengthens
  the runtime once the bodies graduate.
- **CI workflow hardening.** Matrix expansion (e.g., add 3.13 ahead of
  the 3.14 local pin closing the gap), dependency caching tweaks, an
  additional smoke job for the wheel-import path with the spaCy model
  pre-installed. Cite: `.github/workflows/ci.yml`.
- **`docs/TEST_VERIFICATION_MATRIX.md`** first draft. Per cleanup plan
  v1.1 Track 7 item 3: a one-page map of subsystem → tests that
  exercise it → F-* gate codes the tests guard. The discipline already
  exists in the operator's head; the doc surfaces it.

## 4. Do-not-touch surfaces

Restated from `docs/COLLABORATOR_HANDOFF.md` so it lives in the queue
too:

- Any LOCKed amendment file under `pipeline/blueprint/v0.1/` or
  `pipeline/architecture/v0.1/` (cosmetic edits also prohibited; the
  canonical bytes are pinned).
- `pipeline/engineering/lock_history.v1.jsonl` (operator-write-only).
- Signed cards under `pipeline/cards/` (embedded
  `_research_metadata.ed25519_signature`).
- Classification register signatures under
  `orgs/<slug>/vault/classification/`.
- Root wake-up files: `SOUL.md`, `USER.md`, `MEMORY.md`, `AGENTS.md`,
  `CLAUDE.md`, plus `IDENTITY.md`, `SKELETON.md`, `HEARTBEAT.md`,
  `TOOLS.md`, `lessons.md`. Many bootstrap chains hard-code these paths.
- `data/` and `orgs/` (per `.gitignore`; client truth, Law 3 isolation).
  The `orgs/_TEMPLATE/` subtree is the one operator-blessed shape to
  copy from.

If you have to touch any of these, surface the need in a PR description
or daily-log entry and wait for operator coordination.

## 5. Needs Josh decision

Items that are ready to start but blocked on an operator call. Pulling
from this section means "I'm waiting on a decision," not "I'm working."

- **cedarpy v0.2 substrate-addition** — the Rust wheel candidate for the
  Golden Image build. Decision points: which Cedar implementation, what
  build-time discipline ships the wheel, what the F-* coverage looks
  like over the new Cedar boundary, whether it ships at v0.1 or waits
  for v0.2.
- **§4 v2.x.7 RT-01 / RT-05 / RT-09 follow-on items.** Surfaced by the
  §4 v2.x.6 runtime companion landing on 2026-05-17 as v2.x.7 follow-on
  candidates. Specifically: (RT-01) the AST-lint
  `R-NO-CLOUD-LIKE-LOCAL-PROVIDER` rule per §12.1 RT-01 PARTIAL closure;
  (RT-05) `_coerce_to_provider_boundary_context` runtime per-field
  validation per §12.3 RT-05 deferral; (RT-09) post-fill-draft check
  moved into wrapper PRE (closes the documented deviation). Each is a
  bounded engineering ticket but the order in which they land is an
  operator call.
- **FID publisher pubkey generation timing.** Day-2-Tuesday anchor at
  2026-05-19 per the FID Phase 1 dispatch. Decision: pre-generate the
  pubkey ahead of the Tuesday anchor or land the ceremony Tuesday
  morning.

## 6. Needs architecture / LOCK process

Items that cannot land via ordinary PR — they require a blueprint
amendment, a paired §0.5 commit, and a LOCK ceremony. A collaborator
who notices "this would be useful" should propose, not unilaterally
implement.

- **Any new `§-blueprint amendment`.** Cite the example chain at
  `pipeline/blueprint/v0.1/section_04_v2_x_*_amendment.md` — every
  amendment lands as a paired commit with its `section_00_5_…`
  interface-index sibling and a `lock_history` row.
- **Any new F-\* failure-code family addition.** F-CLASS-*, F-CARDS-*,
  F-DIALECT-*, F-PACKET-*, F-WPFA-*, F-INTAKE-*, F-UPLOADER-*, F-REPORT-*,
  F-FG-*, F-CIC-CLC-*, F-GPP-*, F-AMDT-* are the registered families
  as of 2026-05-16; adding a new family requires the architecture
  amendment chain.
- **Any policy / Cedar update.** Cedar policies sit under the
  `pipeline/logician/` umbrella and the outbound boundary at
  `outbound_boundary.cedar`. Policy edits change the security posture
  and are LOCK-tracked.
- **Any new Ed25519 signing-role addition.** The cards-publisher
  pubkey at `vault_shared/cards/publisher_pubkey.signed.yaml` is the
  current canonical signer. A new signing role (e.g., a separate
  router-template publisher per architecture v7.0.7 §6.1) is an
  architecture-level decision.

---

When you land work from any section, update the relevant front-door doc
(`PROJECT_STATUS.md` for state changes; `RUNTIME_MATURITY_MATRIX.md` for
maturity label changes; this file for queue shifts). Lightweight matrix
corrections do not need a `lock_history` row per the cleanup plan v1.1
Track 3 "promotion requires dated evidence" softening — but governance-
bound transitions still do, and the operator runs those.

Cite the artifact you're working from in the PR description. If you're
not sure whether something belongs in Gate 1 or Gate 2, default to Gate
2 and ask in the PR — the operator will reroute if needed.
