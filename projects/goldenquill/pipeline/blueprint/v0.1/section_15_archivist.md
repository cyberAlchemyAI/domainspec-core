---
title: Blueprint §15 Archivist — between-cycle preservation surface (v1 SCOPING DRAFT → v2 post-Cycle-1)
filed: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 (v1 — L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor per WS-D v7.0.5 + WS-E §11 + WS-F §12 + WS-H §2 v7.2 + WS-G §5 v8 precedents — Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq). Cycle 1 surfaced 18 findings (2 HIGH + 5 MED + 11 LOW counting Editor + Judge + Red Team) including 2 HIGH from Red Team (RT-01 subprocess bypass + RT-02 custom file-write helper bypass; both silent-canonical-corruption attack vectors); all closures applied across §15.0/§15.1/§15.5.0/§15.6.0/§15.7/§15.9.1/§15.9.2/§15.9.3/§15.9.4/§15.10/§15.12/§15.13.1/§15.16. Cycle 2 verified all 18 closures CLOSED with zero new design concerns and zero new attack paths. Compound LOCK with `section_00_5_section_15_archivist_amendment.md` per §6.17 Option-B paired-commit pattern.
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                      # v7 LOCKED 2026-04-19 — A1-A12
  - pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md                  # v7.0.4 LOCKED 2026-05-09 row 178 — KFR + SP0 + F-LOGICIAN-FACT-DRIFT family + Intake module spec + Benchmarks Register; §9 reserves the curation slot for v1.x Archivist; §9.1 J-06 closure pins the slot transition discipline
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md               # v7.0.4-M1 LOCKED 2026-05-10 row 190 — narrow corrective; KFR canonical-JSON signing + AST whitelist + tag-mutation hash + audit-log timing-equalization + Decimal mandate + Logfire bootstrap (relevant to Archivist's read-mostly access through KFR substrate)
  - pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md                  # v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intelligence Database + Match Database + Scout channel G; §6 binds Funder Intel curation + Match DB lifecycle to the Archivist v1.x curation slot
  - pipeline/architecture/v0.1/architecture_v7_0_6_amendment.md                  # v7.0.6 SELF-LOCKED 2026-05-09 row 176 + verified row 177 — Archivist named as v1.x candidate seat (between-cycle preservation; KFR maintenance + Funder Intel curation + Match DB lessons-delta integration + lessons.json proposed diffs + Benchmarks Register freshness)
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                  # v7.0.7 LOCKED 2026-05-10 row 180 — Beta classification-driven routing; Archivist routing posture is "always-local, hard-coded, not operator-overridable" — Archivist reads classified-Confidential content (KFR with Confidential-default fields + Match DB narratives + post-fill drafts under reports/) and produces operator-facing digests
  - pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md                  # v7.0.8 LOCKED — CIC × CLC orthogonality; Archivist digest schemas + pattern-detection prompts must audit clean against the four detection layers at LOCK
  - pipeline/blueprint/v0.1/section_02_vault_topology.md                         # v7.1 LOCKED + v7.2 LOCKED 2026-05-10 row 186 — Archivist reads from §2 sub-kinds via Vault read intents; §2 v7.2 operational sub-kinds (metrics/financials/photos/narrative_entries/timeline_of_activities/beneficiary_records/attachments) are read-substrate for the quarterly review pass
  - pipeline/blueprint/v0.1/section_04_logician.md                               # v2.x in flight — Archivist gate family (4 codes) registered via §4 v2.x amendment (WS-L); §15 is the authority on gate codes and proposes-only discipline
  - pipeline/blueprint/v0.1/section_05_pipeline.md                               # v8 LOCKED 2026-05-10 row 188 — track-registry; Archivist runs OUTSIDE the §5 track dispatch (between-cycle, not inner-loop); does NOT register as a track
  - pipeline/blueprint/v0.1/section_11_intake.md                                 # §11 v1 LOCKED 2026-05-10 row 185 — Intake produces operator-confirmed KFR entries; Archivist proposes refresh prompts + expiry tracking against Intake-produced KFR (NEVER writes KFR canonical entries directly, mirrors Intake's discipline)
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md               # §0.5 v5 LOCKED + amendments v6-v12 (runtime-live 290 rows at 2026-05-10T07:00Z); Archivist primitives row-append at paired §0.5 §15 amendment companion-file
prerequisite_interlock: pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md §9 (curation-slot reservation; spec-text frozen at LOCK 2026-05-09 row 178 + cross-family-verified NEEDS-M1 row 181 + M1 LOCK row 190); pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md §6 (curation-slot binding; spec-text frozen at LOCK 2026-05-10 row 179). §15 is the seat-lifecycle wrapper around those two slot-reservation contracts; the slot-owner field stays `operator` for v0.1 + v0.2 and transitions to `archivist` only at v1.x rollout per v7.0.4 §9.1 J-06 closure discipline.
companion_module: pipeline/orchestrator/seats/archivist/__init__.py (skeleton authored at §15 v1 LOCK; mode dispatch SCAFFOLD-ONLY + dataclass schemas for the four digest types + four proposes-only gate predicate stubs raising NotImplementedError; full implementation deferred to v1.x per the spec-only-at-v0.2 disposition).
companion_amendment: pipeline/blueprint/v0.1/section_00_5_section_15_archivist_amendment.md (paired-commit at §15 v1 LOCK per §6.17 Option-B).
v0_2_implementation_disposition: SPEC-ONLY at v0.2. Operator-driven cadence in the interim — operator manually runs `tilth archivist weekly` and `tilth archivist quarterly` (CLI surface authored at v1.x). The §15 v1 LOCK is a SPEC LOCK not an implementation LOCK; downstream consumers (KFR + Funder Intel DB + Match DB + lessons.json + Benchmarks Register) reference §15 as the curation-slot binding contract while the curation work itself remains operator-owned. v1.x amendment lands when the operator-cadence-vs-Archivist-scheduled-cadence transition is operator-signed per v7.0.4 §9.1 + v7.0.5 §6.
downstream_siblings_out_of_scope: §13 Data Collector, §14 Report Generator (both v0.2 horizon — both share NO runtime path with Archivist; Data Collector writes operational-data sub-kinds that Archivist reads quarterly, Report Generator reads operator-promoted KFR + operational data, neither agent's prompt path or substrate is shared with Archivist).
ws_l_routing_dependency: WS-L §4 Logician v2.x amendment registers F-ARCHIVIST-* gate family as proposes-only Cedar policies. §15 v1 LOCK depends on §4 v2.x to materialize the gate-family Code-side; §15 v1 is the SPEC authority and §4 v2.x is the realization layer. AT v0.2 SPEC LOCK the gate predicates are skeleton stubs raising NotImplementedError (per v0.2 spec-only disposition); implementation lands at v1.x amendment.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent (lock_history row 179, 2026-05-10) + WS-E §11 + WS-F §12 + WS-H §2 v7.2 + WS-G §5 v8 blueprint-class precedents (rows 185 / 182 / 186 / 188 / 189). Editor=groq/llama-3.3-70b-versatile (Meta family) + Judge=google/gemini-2.5-pro (Google family) + Red Team=groq/openai/gpt-oss-120b (OpenAI-OSS family) dispatched via openclaw infer model run --gateway across both Cycle 1 and Cycle 2. Three distinct non-Anthropic families. L-003 satisfied. Bridge pattern: Cowork → openclaw via mcp__Control_your_Mac__osascript with timeout of 600 seconds for Gemini Pro thinking-mode runs. Dispatch shell scripts cribbed from pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh. Audit trail at pipeline/validation/blueprint_section_15_archivist_2026-05-10/.
cycle_1_changelog_2026_05_10:
  - "RT-01 (HIGH): §15.9.3 R-ARCHIVIST-NO-CANONICAL-MUTATE extended to forbid subprocess/os.system/os.popen/pexpect invocations whose argument list contains the literal token 'tilth' OR any canonical-write sub-command (kfr/funder-intel/match-db/lessons/benchmarks). Compound-token detection across f-strings, str.format(), str.join. Runtime guard at sandbox-level denies process creation unless target binary is the Archivist seat module entry point itself. Cedar policy archivist_proposes_only.cedar extends with explicit DENY of process_create capability for Archivist principal."
  - "RT-02 (HIGH): §15.9.3 module-level import-restriction added — any import from non-Archivist-package modules exposing file-write APIs (utils.file.atomic_write, tools.file_io.*, etc.) rejected at compile time. Runtime open()/Path.write_text/.write_bytes wrapped with shim injected at process start; shim validates target path against allowed-prefix set; PermissionError on violation; shim non-bypassable from Archivist code."
  - "RT-03 (MED): §15.9.3 Archivist seat MUST self-assert principal at startup by reading SN-LLC operator-signed token from /etc/tilth/seat_identity/archivist.signed.yaml; reject any request where incoming Cedar principal does not match expected archivist_seat identifier. Cedar policy adds attribute check principal.id == 'archivist_seat' && principal.signed_by == <SN_LLC_pinned_pubkey>; mismatch → DENY."
  - "RT-04 + RT-12 BUNDLED (MED + LOW): §15.4.1 + §15.7 + §15.10 add v0.2 + v1.x first-ship known-limitation acknowledgment for TTY-as-attack-surface model bounded by v7 LOCKED A1+A4 single-client + operator-trusted preflight assumptions; v2 multi-tenant mitigation track per Section O.5; admin-risk ledger entry per non-physical-TTY review event. TTY check itself strengthened: getsid(0)==getsid(1)==getsid(2) all stdio same session; controlling tty device is /dev/ttys* not PTY master. Hardware-token check is v2+ horizon. Mirrors v7.0.7 row 180 timing-side-channel disposition pattern."
  - "RT-05 (MED): §15.7 operator-signature requirement extended — each confirm action's signed payload MUST include confirmation_id: <opaque-uuid> field unique per (run_id, digest_entry_id) pair; verification step rejects any already-used confirmation_id (audit-ledger lookup at signature-verify time). Replay against different digest entry structurally prevented because confirmation_id is bound to specific entry."
  - "RT-06 (MED): §15.9.1 POST-gate sub-tag .aggregate_insufficient_orgs added — fires when workspace-level digest is generated for workspace containing fewer than N orgs (default N=3; operator-tunable per archivist_config.yaml with same Ed25519-signed config discipline as Intake's intake_config.yaml). Triggered → suppress per-org-derived statistics; replace with insufficient-orgs notice. POST-gate regex check extended to inspect rationale + pattern_summary fields for org_slug literals from orgs/ORG_INDEX.md; matches → fire .workspace_digest_per_org_content."
  - "RT-07 (MED): §15.9.2 regex-only approach replaced with two-layer detection — (1) Unicode NFKC normalization applied BEFORE detection; (2) named-entity recognizer (NER; xx-ent-wiki-sm spaCy or equivalent local model frozen at Golden Image build per ADR-001) flags org/funder/client identifier mentions regardless of wording; (3) regex check still runs as fast-path. Three layers union-of-fail. Common abbreviation expansion table at vault_shared/archivist_abbreviation_expansion.yaml (Ed25519-signed by operator)."
  - "RT-08 (LOW): §15.9.1 sub-tag .unconfirmed_substrate_read extended with runtime instrumentation requirement — ALL read helpers used by Archivist seat MUST emit gate-result with this tag when source path is under pending namespace, regardless of how helper is called. AST-lint extension flags any import of generic read_yaml/read_json/read_text utility from outside Archivist package."
  - "RT-09 (LOW): §15.5 + §15.7 + §15.13.1 explicit mandate — ALL YAML deserialization of Archivist digest files (including in operator review CLI) MUST use yaml.safe_load (or equivalent safe parser); ANY use of yaml.load is prohibited and detected by AST-lint extension at compile time. Skeleton test test_archivist_yaml_safe_load_only added to §15.13.1."
  - "RT-10 (LOW): §15.9.4 + §15.12 v1.x posture row explicit — at v1.x amendment F-ARCHIVIST-CADENCE-DRIFT.severity = HIGH and gate.action = FAIL_CLOSED MUST be set. §15.13.2 v1.x horizon test test_f_archivist_cadence_drift_is_fail_closed_at_v1_x parses gate definition and asserts fail_closed attribute is True."
  - "RT-11 (LOW): NEW failure code F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT (PRE-substrate-read) added as 5th owned gate at §15.9. Predicate: every substrate read attempt by Archivist MUST go through appropriate Vault read intent wrapper (vault_read_intent_kfr / vault_read_intent_funder_intel / vault_read_intent_match_db / vault_read_intent_lessons / vault_read_intent_benchmarks / vault_read_intent_archivist_state); reads via raw open() or generic file-read helpers fail-closed. Vault read intent is sole layer that performs SHA3-512 hash verification per v7.0.4-M1 §4 + v7.0.5 §5 F-FUNDER-CORPUS-INTEGRITY; bypass skips integrity verification."
  - "DC-01 (Judge LOW): §15.9.1 .unconfirmed_substrate_read sub-tag extended with explicit metadata-only read tool contract — contract MUST be specified as part of §15 v1.x implementation amendment, including non-negotiable test case in tests/seats/archivist/ that asserts ForbiddenContentReadError raised if any field other than documented metadata fields (extracted_at_utc, fact_id, queue_length) is accessed."
  - "E-01 (MED): §15.1 prepended with v0.2-vs-v1.x responsibilities summary block."
  - "E-02 (LOW): §15.6.0 cadence summary table cross-references §15.4 input contracts for trigger detail."
  - "E-03 (MED): §15.5.0.A subsection added explaining field-introduction pattern (Archivist-introduced fields conceptually carry archivist_* prefix; concrete name pattern matches §11/§12 precedent)."
  - "E-04 (LOW): §15.16 list extended with does-not-introduce-new-operator-key-types, does-not-introduce-new-vault-subtree-topology, does-not-introduce-new-admin-risk-severity-classes."
  - "E-05 (LOW): §15.0 cross-amendment composition map extended with explicit per-substrate contract reference dependency arrows."
  - "Final §15.9 gate roster: 5 codes (was 4). §0.5 §15 amendment row count: 14 rows (was 12). Range claim adjusts from 291-302 to 291-304."
cycle_2_changelog_2026_05_10:
  - "Cycle 2 verdicts: Editor READY_TO_LOCK (5/5 closed; zero new). Judge READY_TO_LOCK 100/100 (DC-01 closed; +1 from 99; zero regressions). Red Team REQUIRES_FIXES — 7 of 12 CLOSED + 4 PARTIAL (RT-01 / RT-02 / RT-05 / RT-08) + 5 NEW (NF-01 HIGH / NF-02 MED / NF-03 LOW / NF-04 LOW / NF-05 MED). Score 93/100."
  - "Cycle 2 disposition: row-170 transparent disposition pattern per WS-D v7.0.5 + WS-B v7.0.7 + WS-C-M1 v7.0.4-M1 precedents (lock_history rows 179 / 180 / 190). PARTIAL closures + NEW findings folded in at LOCK with explicit text-level mechanism specifications OR bounded-by-v7-LOCKED-A1+A4 dispositions; no third audit cycle, no silent revision."
  - "RT-01 PARTIAL (low-level execs via ctypes/os.execve through FFI) + NF-05 (ctypes-routed canonical-CLI launch) FOLD_IN at §15.9.3: AST-lint extended to forbid ctypes/cffi/FFI module imports; sub-tag .ffi_import_forbidden added; runtime FFI bypass via dynamic-loaded shared library bounded by v7 LOCKED A1+A4 (mirrors RT-04/12 + v7.0.7 row 180 timing-side-channel disposition); v2 multi-tenant amendment lands kernel-level sandbox interception per Section O.5."
  - "RT-02 PARTIAL (importlib.import_module bypass after shim install) + RT-08 PARTIAL FOLD_IN at §15.9.3: AST-lint extended to forbid importlib.import_module(...) AND __import__(...) calls in Archivist seat code; sub-tag .dynamic_import_forbidden added; runtime open-shim catches actual write attempt regardless of how helper got loaded — combined defense-in-depth closes the gap."
  - "RT-05 PARTIAL (confirmation ledger race) + NF-02 (concurrent confirmation race) FOLD_IN at §15.7: confirmation_id ledger discipline extended with explicit atomic check-then-write semantics — fcntl.flock(LOCK_EX) for entire lookup-then-append sequence; concurrent confirmation processes serialize at the lock; second process sees first's confirmation_id and rejects replay. Lock acquisition pattern mirrors v7.0.4-M1 §4 atomic-read fcntl.flock precedent. Lock-acquisition-timeout-30s → fail-closed."
  - "NF-01 (HIGH — Vault-read-intent wrapper runtime monkey-patching) FOLD_IN at §15.9.5: runtime-immutability self-check — function id(...) of resolved Vault read intent wrapper compared against import-time snapshot at every read call; mismatch → sub-tag .vault_intent_runtime_tampering; refuse read. Snapshot dict sealed via types.MappingProxyType. Sealed-module loading via importlib.util.LazyLoader with frozen-attribute discipline lands at v1.x amendment per §4 v2.x realization."
  - "NF-03 (LOW — SN-LLC signed token rotation requires Golden Image rebuild) FOLD_IN at §15.9.3 + §15.16: explicit acknowledgment that token rotation requires Golden Image rebuild at v0.2 + v1.x first ship; operator-driven rebuild cadence acceptable; advisory sub-tag .token_rotation_requires_golden_image_rebuild emitted at admin-risk ledger when token approaches rotation due-date; v2 amendment lands rolling-rotation mechanism per Section O.5."
  - "NF-04 (LOW — NER model adversarial evasion via Unicode homoglyph) FOLD_IN at §15.9.2: explicit disposition that NER is best-effort detection; adversarial robustness bounded by v7 LOCKED A4 (operator-trusted preflight) — operator is sole author of proposed_lesson_text; operator review surface §15.7 is the load-bearing trust boundary; adversarially-crafted instance-level lesson that evades all three detection layers AND survives operator review is outside the §15 v1 threat model. v2 amendment lands NER adversarial-robustness testing as part of §4 v2.x amendment."
  - "Cycle 2 NEW failure-code sub-tags added at this LOCK: .ffi_import_forbidden + .dynamic_import_forbidden + .token_rotation_requires_golden_image_rebuild + .vault_intent_runtime_tampering. No new top-level failure-code rows registered (sub-tags only); §0.5 §15 amendment row count UNCHANGED at 14 rows (range 291-304)."
  - "L-005 architecture-domain disagreement branch fired at Cycle 2 close: Editor READY_TO_LOCK + Judge READY_TO_LOCK 100/100 + Red Team REQUIRES_FIXES (PARTIAL+NEW). Operator-confirmation-precedent applied per WS-D v7.0.5 + WS-B v7.0.7 + WS-C-M1 v7.0.4-M1 row-170 transparent disposition pattern. Operator confirmation deferred to LOCK ceremony per implied confirmation pattern (operator dispatched WS-K with explicit cross-family-rigor instruction)."
---

# §15.0 Cross-amendment composition map

```
v7 LOCKED 2026-04-19 (A1-A12)
  ├─ v7.0.4 LOCKED 2026-05-09 row 178 + v7.0.4-M1 row 190 — KFR + SP0 + curation-slot reservation §9 + slot-transition-discipline §9.1 (J-06 closure)
  │    │
  │    └─→ §15 Archivist (THIS) — seat-lifecycle wrapper around v7.0.4 §9 + v7.0.5 §6 curation-slot bindings; owns proposes-only operator-facing digest discipline; F-ARCHIVIST-* family
  │
  ├─ v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intel DB + Match DB + Scout channel G; §6 binds Funder Intel curation + Match DB lifecycle to Archivist v1.x curation slot; the schema-level `curated_by: operator | archivist` slot-owner field per RT-08 closure stays `operator` at v0.1 + v0.2 and transitions to `archivist` at v1.x via operator-signed migration trigger
  ├─ v7.0.6 SELF-LOCKED 2026-05-09 row 176 — Archivist named as v1.x candidate seat (between-cycle preservation; long-running curation work)
  ├─ v7.0.7 LOCKED 2026-05-10 row 180 — classification routing; §15.10 always-local hard-coded (Archivist reads classified-Confidential content)
  └─ v7.0.8 LOCKED — CIC × CLC orthogonality; §15 schemas + pattern-detection prompt template audit clean at LOCK

§15 → companion edits at LOCK (compound paired-commit per §6.17 Option-B):
  ├─ §0.5 §15 amendment (14 rows; range 291-304; +2 rows from Cycle 1 RT-11 closure adding F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT failure-code + matching pre-gate-check)
  ├─ §4 v2.x amendment (registers F-ARCHIVIST-* gate family — 5 codes — as proposes-only Cedar policies — Code session per WS-L)
  ├─ orgs/_TEMPLATE/archivist_digests/ scaffold (per-org digest templates: KFR refresh + Match DB lessons-delta proposals)
  ├─ vault_shared/archivist_digests/ scaffold (workspace-level: quarterly Funder Intel curation digest template)
  ├─ pipeline/orchestrator/seats/archivist/__init__.py module skeleton (proposes-only; predicates raise NotImplementedError at v0.2)
  └─ tests/seats/archivist/skeleton_tests.py (NON-NEGOTIABLE: prevents future contributors from quietly turning the stub into auto-apply behavior)
```

**Per-substrate contract reference (per E-05 closure).** Archivist's read-only access to each substrate is bounded by the substrate's own LOCKED contract:

- **KFR canonical** — read-substrate per v7.0.4 §1 schema; Archivist reads `orgs/<slug>/vault/kfr/register.yaml` via `vault_read_intent_kfr` (per F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT §15.9.5 from RT-11 closure); SHA3-512 hash verification + canonical-JSON signing per v7.0.4-M1 §2 happens inside the read intent.
- **Funder Intelligence Database** — workspace-shared read-substrate per v7.0.5 §1 + §6 (curation slot binding); Archivist reads `vault_shared/funder_intelligence/register.yaml` via `vault_read_intent_funder_intel`; F-FUNDER-CORPUS-INTEGRITY per v7.0.5 §5.6 verification fires PRE-load AND POST-load.
- **Match Database** — per-org read-substrate per v7.0.5 §2 + §6 (curation slot binding); Archivist reads `orgs/<slug>/match_database/register.yaml` via `vault_read_intent_match_db`; F-MATCH-DB-CROSS-ORG per v7.0.5 §5.1 enforcement applies.
- **lessons.json** — workspace-shared read-substrate per institutional_memory convention; Archivist reads `pipeline/institutional_memory/lessons.json` via `vault_read_intent_lessons`; pattern-vs-instance discipline per F-ARCHIVIST-LESSON-INSTANCE-LEAK §15.9.2.
- **Benchmarks Register** — workspace-shared read-substrate per v7.0.4 §7; Archivist reads `vault_shared/benchmarks/register.yaml` via `vault_read_intent_benchmarks`; F-BENCHMARK-CONTAINS-PER-ORG-REF per v7.0.4-M1 §5 constant-time + audit-log verification fires.
- **Reports archive** — per-org per-grant read-substrate per v0.2 §14 Report Generator output; Archivist reads `orgs/<slug>/vault/grants/<grant_id>/reports/period_<n>/draft_<v>.md` (post-fill drafts) via the §2 Vault read intent (always-local routing per §15.10).

Each per-substrate read is wrapped by F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT (§15.9.5) — bypassing the Vault read intent skips the substrate-specific integrity verification.

# §15.1 Purpose and scope

## §15.1.0 v0.2 vs v1.x responsibilities at a glance (per E-01 closure)

**At v0.2 (this LOCK), the operator is responsible for:**
- Manually invoking `tilth archivist weekly --org <slug>` and `tilth archivist quarterly` cadences (no scheduled-task trigger; operator decides when).
- Manually walking the substrate paths referenced by the digest templates (`orgs/<slug>/archivist_digests/*.yaml` + `vault_shared/archivist_digests/*.yaml`) when the v1.x extraction LLM is not yet wired (operator follows the schema as a checklist).
- Reviewing produced digests via `tilth archivist review` and applying confirmed actions through the existing substrate write CLIs (`tilth kfr ...`, `tilth funder-intel ...`, `tilth match-db ...`, `tilth lessons ...`, `tilth benchmarks ...`).
- Curating `pending_facts.yaml → register.yaml` promotions per Intake §11 (Archivist proposes refresh prompts against the operator-confirmed canonical KFR; not against the pending queue).

**At v0.2 (this LOCK), Archivist itself does:**
- Validate the structural boundaries (proposes-only; org-isolation; pattern-vs-instance lessons; cadence-drift informational at v0.2) via the F-ARCHIVIST-* gate family registered at §4 v2.x amendment.
- Provide the §15.5 schema contracts for downstream consumers (KFR per v7.0.4 §9; Funder Intel + Match DB per v7.0.5 §6) that reference the curation slot.
- Provide the digest templates (`orgs/_TEMPLATE/archivist_digests/`, `vault_shared/archivist_digests/`) the operator references during manual cadence runs.
- Reserve the slot-owner field for operator-signed transition to `archivist` at v1.x rollout (per v7.0.4 §9.1 J-06 closure).

**At v1.x (forward-design — non-binding for v0.2), Archivist additionally does:**
- Run scheduled-task-driven cadences (Mondays 8:30 AM weekly cron; quarterly per 90-day cadence or operator-set calendar alignment) per the `schedule` skill precedent.
- Invoke a small local LLM (Mistral 7B class per §15.8) for pattern detection + digest narrative summarization across the substrates.
- Surface proactive curation proposals between cycles (operator no longer manually walks substrates; Archivist produces digests and operator only reviews + confirms).
- Run Cedar/Python predicate bodies for the F-ARCHIVIST-* gate family (currently skeleton stubs raising `NotImplementedError` at v0.2; live at v1.x via §4 v2.x amendment).

The v0.2 SPEC LOCK is a SPEC LOCK, not an implementation LOCK. v1.x is when Archivist transitions from operator-driven to scheduled-task-driven; the slot-owner field transitions from `operator` to `archivist` via operator-signed migration trigger at that boundary (per v7.0.4 §9.1).

## §15.1.1 Purpose

Archivist is the **between-cycle preservation** support agent of the Tilth pipeline. It runs OUTSIDE the §5 track dispatch — never as part of submission_mode, eval_mode, or report_mode inner loops — and tends the corpus the council has accumulated across cycles: stale Funder Intelligence Database documents, expiring KFR facts, Match Database outcome rollups, freshness drift in the Benchmarks Register, and pattern-level lessons proposed for `lessons.json`. **Archivist proposes; operator confirms every change.** Archivist NEVER auto-applies a single mutation to KFR, Funder Intel DB, Match DB, lessons.json, or Benchmarks Register canonical state — the autonomy boundary is structural and is enforced by `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` (PRE — fail-closed; §15.9.3).

**v0.2 scope (SPEC-ONLY).** Per dispatch packet decision 8d default + this blueprint's `v0_2_implementation_disposition` frontmatter, §15 v1 ships as a SPEC LOCK with skeleton module + digest templates + skeleton tests. **Implementation is deferred to v1.x.** During v0.2 the curation work remains operator-owned per v7.0.4 §9 + v7.0.5 §6 — the slot-owner field stays `operator`, the cadence is operator-driven (operator decides when to run the weekly tick or quarterly review), and the digests are produced by the operator referencing the templates in this spec. The §15 v1 SPEC LOCK is what downstream consumers (KFR substrate at v7.0.4 §9; Funder Intel DB + Match DB at v7.0.5 §6) reference as the curation-slot binding contract — without it, those substrates carry an unspec'd referenced slot, which is a design-debt flag for the Thesis Team.

**v1.x scope (forward-design — non-binding for v0.2).** The v1.x amendment fills the slot per v7.0.4 §9.1 + v7.0.5 §6: Archivist runs scheduled-task-driven cadences (per the existing `schedule` skill — Mondays 8:30 AM cron from the Monday fund-radar memory is the precedent pattern; Archivist runs on its own quarterly + weekly cadences); produces operator-facing digests proactively; the slot-owner field transitions from `operator` to `archivist` via operator-signed migration trigger; the proposes-only discipline is preserved unchanged.

**Out of scope for v0.2 (explicit non-goals).** Archivist does NOT auto-apply ANY change (per F-ARCHIVIST-AUTO-APPLY-ATTEMPTED, §15.9.3). Archivist does NOT generate proposal text (Scribe, §7). Archivist does NOT score, edit, or attack drafts (Judge, Editor, Red Team, §§9–10). Archivist does NOT write KFR canonical entries (Intake, §11 — Intake produces operator-confirmed candidates; Archivist proposes refresh prompts against Intake-produced KFR). Archivist does NOT submit (Uploader, §12). Archivist does NOT run grant cycles (§5 Pipeline). Archivist does NOT collect post-award outcome data (Data Collector, §13, v0.2). Archivist does NOT generate funder-ready reports (Report Generator, §14, v0.2). Archivist does NOT cross orgs in any operator-facing output (per F-ARCHIVIST-CROSS-ORG-LEAK, §15.9.1). Archivist does NOT propose instance-level lessons (per F-ARCHIVIST-LESSON-INSTANCE-LEAK, §15.9.2). Archivist does NOT silently revise the cadence (per F-ARCHIVIST-CADENCE-DRIFT, §15.9.4 — missed cadence is itself a signal surfaced to operator).

**Substance comes from the operator's substrate (Laws 1 + 5).** Every digest entry traces to a load-bearing read of an operator-confirmed substrate (KFR canonical entries, Funder Intel DB operator-curated docs, Match DB per-cycle rolled-up outcomes, lessons.json operator-confirmed entries, Benchmarks Register operator-curated baselines). Archivist proposes refreshes, rollups, lessons-delta integrations, and freshness flags — but the substance of every proposal traces to the operator-confirmed substrate it summarizes. Archivist fabricates nothing (Law 5 enforcement is structural — no extraction LLM at v0.2; pattern detection at v1.x is bounded to substrate reads only).

**Boundary with Editor (sharp; never collapse the seats).** Editor is in the **inner loop** (clarity review per draft, fires every cycle inside §5 track dispatch — submission_mode + eval_mode + report_mode). Archivist is in the **outer loop** (curation between cycles, fires on weekly + quarterly cadences scheduled OUTSIDE §5 track dispatch). Editor reads `SectionDraft` + `RubricCriterion`; Archivist reads `KFR.register.yaml` + `vault_shared/funder_intelligence/register.yaml` + `orgs/<slug>/match_database/register.yaml` + `pipeline/institutional_memory/lessons.json` + `vault_shared/benchmarks/register.yaml` + `orgs/<slug>/vault/grants/<grant_id>/reports/`. The seats share zero runtime path, zero substrate, zero prompt template. v0.2 spec MUST NOT collapse them; the seat-name distinction is structural and the v1.x amendment preserves it explicitly. Memory `project_archivist_v1x_candidate_seat.md` already documents this boundary; §15 codifies it at the spec level.

**Boundary with Logician (sharp).** Logician is deterministic Cedar + Python in the inner loop; zero token cost. Archivist runs an LLM (small + local at v1.x) for digest narrative + pattern detection in the outer loop. The work is different in kind: Logician decides PASS/FAIL on individual draft transactions; Archivist proposes operator-facing digest narratives across cycles. They share no concern. v0.2 spec MUST NOT propose Logician-side curation work — the F-ARCHIVIST-* family registered at §4 v2.x is itself enforced by Logician (Archivist's outputs are validated PRE/POST by Logician gates), but Logician does not perform curation on Archivist's behalf.

# §15.2 Five Operating Laws — enforcement mapping

Framework: per `pipeline/templates/component_analysis_template.md`

Each of the Five Laws is enforced by a combination of PRE-gates (Logician, before Archivist's digest is exposed to operator), in-seat discipline (Archivist's proposes-only contract + per-substrate read isolation), and POST-gates (Logician, after Archivist emits the digest but before operator-facing surface). Failure codes are enumerated in §15.9. Per the v0.2 spec-only disposition, the v0.2 enforcement is OPERATOR-DRIVEN (operator runs the weekly + quarterly cadence manually, references the digest templates, and applies the proposes-only discipline by hand); the gate predicates are skeleton stubs at v0.2 and become live Cedar/Python at v1.x via §4 v2.x amendment.

**Law 1 — RFA is the source of truth.**
- N/A direct path — Archivist runs between cycles, not against an active RFA. KFR refresh prompts surface for operator review at SP0 of the next active cycle (per v7.0.4 §3 SP0 KFR Freshness Review); the SP0 surface is where RFA-required-fields gating lives, NOT in Archivist's digest.
- In-seat: Archivist's quarterly digest may flag stale Funder Intelligence DB entries that prior grant cycles relied on (e.g., a USDA program page that has been updated since last citation). The flag is INFORMATIONAL — Archivist does NOT rewrite the cited material; operator decides whether to re-fetch and re-promote at next cycle's SP0.

**Law 2 — No boundary drift.**
- PRE-gate: Archivist's scope is mechanically bounded — weekly tick reads KFR expiry/pending-facts/Match DB delta/lessons append surfaces; quarterly review reads Funder Intel promotion-or-drop/Match DB outcome rollup/Benchmarks Register freshness/lessons.json proposed diffs. No web search, no cross-grant reasoning beyond the substrate's own cross-cycle structure (Match DB per (client × funder) cycle outcomes), no content generation beyond digest summarization.
- In-seat: Archivist's pattern-detection prompt is fixed per cadence (no operator-tunable prompt at v0.2 + v1.x first ship). The v1.x extraction LLM is bounded by the prompt to produce digest rows in the §15.5 schemas; structured-output validation rejects any output that doesn't match.
- POST-gate: Pydantic validation on every digest entry before it reaches the operator-facing surface. Schema violation → reject + audit trail under `pipeline/validation/archivist_rejects/<cadence>/<run_id>/`.

**Law 3 — Org isolation.**
- PRE-gate: Archivist's per-org digests (KFR refresh, Match DB lessons-delta) are SCOPED to exactly one `org_slug` per per-org-digest invocation. The CLI takes `--org <slug>` as a required argument for per-org cadences. Workspace-level digests (quarterly Funder Intel curation) explicitly carry no per-org content (Funder Intelligence DB is per-funder, not per-org). Cross-org aggregation in any operator-facing surface → fail-closed via `F-ARCHIVIST-CROSS-ORG-LEAK` (§15.9.1).
- In-seat: Per-org digests read from exactly one `orgs/<slug>/match_database/`, one `orgs/<slug>/vault/kfr/`, one `orgs/<slug>/vault/grants/<grant_id>/reports/` subtree. Workspace-level digests read only `vault_shared/funder_intelligence/` + `vault_shared/benchmarks/` + `pipeline/institutional_memory/lessons.json` (workspace-scoped substrates explicitly carry no per-org content).
- POST-gate: every digest write is path-resolve-normalized; any path that resolves outside the declared `org_slug` (or workspace) subtree → hard-block with `F-ARCHIVIST-CROSS-ORG-LEAK`. **Workspace-aggregate carve-out is explicit.** A workspace-aggregate digest like "across all your clients, X% of KFR facts are stale" is allowed because the aggregate is operator-only context (the operator IS the multi-org actor and operates above the org-isolation boundary by definition); the gate logic distinguishes (a) per-org content leakage from (b) workspace-aggregate statistics computed from per-org reads. Per-org content (specific KFR fact text, specific Match DB narratives, specific client names) MUST NOT cross orgs; aggregate statistics MAY cross orgs in the workspace-aggregate digest only.

**Law 4 — Apolitical sector language + admin-risk term scanning.**
- PRE-gate: Archivist's digest narrative is structurally bounded — per-cadence prompts produce structured digest rows (proposed_action + rationale + source_substrate_path), not free-form prose. The §7.11 admin-risk scanner (Scribe-side) does NOT fire on Archivist's structured outputs because there is no narrative-prose for it to scan.
- In-seat: lessons.json proposed diffs (the highest narrative-content surface in Archivist's outputs) carry verbatim quotes from operator-confirmed lessons.json entries when proposing pattern-level rollups; operator-authored lesson text is preserved without rewriting (Law 4 forbids silent rewriting of operator-authored material). The operator review surface displays the proposed lesson with its source-lesson references; if a proposed lesson contains an admin-risk-flagged term inherited from a source lesson, that's an operator review concern at promotion time, not an Archivist intervention at proposal time.
- v1.x horizon: when the v1.x extraction LLM produces digest narrative beyond structured rows (e.g., quarterly Funder Intel "narrative summary of corpus health"), the §7.11 admin-risk scanner could fire as an advisory POST-extract surface. NOT registered at v0.2 (no extraction LLM at v0.2); documented here as v1.x extension marker.

**Law 5 — Applicant brings the substance.**
- PRE-gate: Archivist reads ONLY operator-confirmed substrates (KFR with `validation.confirmed_by` populated; Funder Intel DB with `audit_chain` initialized; Match DB with `audit_chain` initialized; lessons.json with operator-confirmed entries; Benchmarks Register with operator-curated baselines). Archivist refuses to read non-operator-confirmed substrates (e.g., `pending_facts.yaml` from Intake; `proposal_commitments.yaml` with `status: PENDING_OPERATOR_REVIEW`); these are Intake's review surface, not Archivist's. Operator-confirmed-only read scope is enforced PRE (per `F-ARCHIVIST-CROSS-ORG-LEAK` sibling sub-tag `.unconfirmed_substrate_read` — see §15.9.1).
- In-seat: Archivist proposes refresh/rollup/lessons-delta operations; the proposals carry source_substrate_path + source_entry_id + rationale fields per §15.5 schemas. Operator-facing display shows the proposed operation side-by-side with its source-substrate justification.
- POST-pre-surface: F-ARCHIVIST-AUTO-APPLY-ATTEMPTED (§15.9.3) is the no-mutation structural enforcement — any code path where Archivist directly mutates KFR, Funder Intel DB, Match DB, lessons.json, or Benchmarks Register canonical state is rejected at gate time. Operator approval is the load-bearing transition from Archivist proposal to canonical mutation. Mirrors Intake's "produces queue → operator confirms → promotes to canonical" discipline (§11.1) but applied to *between-cycle curation* rather than *per-doc ingestion*.

# §15.3 Four Autonomy Rules — enforcement mapping

**Rule 1 — Save state always.** Archivist persists `ArchivistState` to `pipeline/institutional_memory/archivist_state/<run_id>.yaml` on every cadence invocation — both success and failure. State includes: invocation timestamp, cadence (`weekly` / `quarterly`), org_slug (per-org cadences) or `workspace` (workspace-level cadences), substrate paths read (with content_hash for tamper-detection cross-reference per v7.0.4-M1 §4), digest entries produced count, digest entries rejected pre-surface (with rejection reason), digest output path written, F-ARCHIVIST-* gate failures logged to `pipeline/validation/archivist_rejects/<cadence>/<run_id>/`, failure reason if applicable.

**PRE-gate failure persistence.** When Archivist is invoked but a PRE-gate (§15.9 PRE codes including org-isolation + auto-apply-attempt + cadence-drift) fails before digest production starts or mid-production, Archivist writes `archivist_state.yaml` with `cadence_completed=False, digest_entries_produced=0, failure_reason=<gate_code>, failure_detail=<predicate_message>`. No partial digest file is written; the operator-facing surface receives the gate-fail result with the same self-validation envelope as a successful run, just with `overall_status="cadence_failed"` and the failure code surfaced. This guarantees Rule 1 holds even when Archivist never reaches the operator-facing digest.

**Rule 2 — Test your own work.** Before marking the digest write "ready for operator review," Archivist runs the readiness check (§15.7) — a deterministic self-validation pass that confirms: every digest entry has source_substrate_path + source_entry_id + rationale populated, every entry's source path is under the declared org subtree (per-org cadence) or under workspace-shared substrates (workspace cadence), the digest file is Pydantic-schema-valid, the digest write succeeded under the §2 Vault write intent, the audit trail under `archivist_rejects/` is consistent with the digest count math (entries_emitted_by_cadence_pass = entries_in_digest + entries_rejected). The readiness result is persisted alongside `archivist_state.yaml`.

**Rule 3 — Be explicit.** Archivist's input contract (§15.4) declares exact substrate paths, cadences, and done-definitions per cadence. Archivist's output contract (§15.5) declares exact digest output paths per cadence (per-org KFR refresh digest at `orgs/<slug>/archivist_digests/kfr_refresh_<run_id>.yaml`; per-org Match DB lessons-delta at `orgs/<slug>/archivist_digests/match_db_lessons_delta_<run_id>.yaml`; workspace Funder Intel quarterly digest at `vault_shared/archivist_digests/funder_intel_quarterly_<run_id>.yaml`; lessons.json proposed-patches at `pipeline/institutional_memory/lessons_proposals/<run_id>.yaml`), schema, and operator-review surface format.

**Rule 4 — Clean output.** Digest files contain only structured digest-entry rows. No markdown fences, no LLM self-commentary, no Tilth-internal artifacts mixed into the operator-facing digest. Per-cadence digest schemas are Pydantic-validated before write. v1.x extraction LLM outputs go through structured-output discipline (Pydantic AI native pattern); raw LLM output never reaches the digest file.

# §15.4 Input contracts (per cadence)

Archivist fires at two distinct cadences; each cadence has its own input contract. Per the v0.2 spec-only disposition, the v0.2 invocation surface is **operator-explicit only** — operator manually runs `tilth archivist weekly --org <slug>` or `tilth archivist quarterly --workspace`. The scheduled-task-driven invocation lands at v1.x amendment.

## §15.4.1 Weekly tick input contract

Trigger: operator-explicit at v0.2 via `tilth archivist weekly --org <slug>`. (Scheduled-task-driven trigger lands at v1.x amendment — Mondays 8:30 AM cron pattern per Monday fund-radar memory.)

**Input bundle (`ArchivistWeeklyInput`, frozen, kw_only):**

- `run_id: str` — UUID assigned at CLI invocation; pins the run for state persistence.
- `org_slug: str` — client org slug for per-org substrate path resolution (required CLI arg). Workspace-level cadences use the `quarterly_workspace` invocation, NOT weekly.
- `kfr_register_path: str` — vault path to the org's KFR canonical register. Defaults to `orgs/<org_slug>/vault/kfr/register.yaml`. `Path.resolve()` is called at PRE-gate; the resolved path MUST sit under `orgs/<org_slug>/`. Symlink read is rejected.
- `match_database_path: str` — vault path to the org's Match Database register. Defaults to `orgs/<org_slug>/match_database/register.yaml`. `Path.resolve()` MUST sit under `orgs/<org_slug>/`.
- `lessons_json_path: str` — workspace-shared lessons audit trail. Defaults to `pipeline/institutional_memory/lessons.json`. `Path.resolve()` MUST sit under `pipeline/institutional_memory/`.
- `lookback_window_days: int` — operator-set lookback for delta detection; default `7` (one week tick). Out of range (`<= 0`) → reject at CLI parse time.
- `invoked_at_utc: datetime`.

**Bundle invariants (PRE-gate enforced).**
- `kfr_register_path` (after `Path.resolve()`) MUST sit under `orgs/<org_slug>/vault/kfr/`. Path-traversal-by-symlink → `F-ARCHIVIST-CROSS-ORG-LEAK` (sub-tag `.symlink_escape`).
- `match_database_path` (after `Path.resolve()`) MUST sit under `orgs/<org_slug>/match_database/`. Symlink → `F-ARCHIVIST-CROSS-ORG-LEAK.symlink_escape`.
- `lessons_json_path` (after `Path.resolve()`) MUST sit under `pipeline/institutional_memory/`. Symlink → `F-ARCHIVIST-CROSS-ORG-LEAK.symlink_escape`.
- `lookback_window_days` MUST be `>= 1`. Out of range → reject at CLI parse time (Pydantic input validation).
- **No `--yes` / `--auto-confirm` / `--force` flags** at v0.2 (or any v1.x first ship). Argparse-level rejection per §11.7 Layer 4 TTY-discipline precedent. Archivist proposes; operator confirms — the four-layer defense Intake established for autopromote-batch transfers to Archivist for the curation slot.
- **TTY check.** All `tilth archivist *` invocations MUST verify `sys.stdin.isatty()` at CLI parse time. Non-TTY invocation (piped from cron, script, or `yes |` pipeline) is rejected with a clear error message at v0.2 + v1.x first ship: "tilth archivist requires interactive TTY; cannot be scripted at v0.2 (operator-driven cadence) or v1.x first ship (proposes-only discipline; no autopromote path)." This closes the silent-auto-apply path where an attacker or careless automation could drive Archivist's CLI from a script and bypass operator scrutiny entirely.

## §15.4.2 Quarterly review input contract

Trigger: operator-explicit at v0.2 via `tilth archivist quarterly --workspace` (workspace-level Funder Intel curation pass) OR `tilth archivist quarterly --org <slug>` (per-org Match DB outcome rollup). Two sub-modes for the quarterly cadence; each has its own input bundle.

### §15.4.2.A Quarterly workspace input

`tilth archivist quarterly --workspace` — workspace-level Funder Intel + Benchmarks Register freshness pass.

**Input bundle (`ArchivistQuarterlyWorkspaceInput`, frozen, kw_only):**

- `run_id: str`.
- `funder_intel_register_path: str` — vault path to workspace-shared Funder Intel register. Defaults to `vault_shared/funder_intelligence/register.yaml`. `Path.resolve()` MUST sit under `vault_shared/funder_intelligence/`.
- `benchmarks_register_path: str` — vault path to workspace-shared Benchmarks Register. Defaults to `vault_shared/benchmarks/register.yaml`. `Path.resolve()` MUST sit under `vault_shared/benchmarks/`.
- `freshness_threshold_days: int` — operator-set freshness threshold; default `90` days (one quarter). A Funder Intel doc with `last_promoted_at_utc` older than `freshness_threshold_days` is flagged as "stale" in the digest.
- `invoked_at_utc: datetime`.

**Bundle invariants (PRE-gate enforced).**
- Both `_path` fields MUST resolve under their respective `vault_shared/` subtrees. Symlink → `F-ARCHIVIST-CROSS-ORG-LEAK.symlink_escape`.
- `freshness_threshold_days` MUST be `>= 1`. Out of range → reject.
- TTY check (per §15.4.1 invariant) applies.

### §15.4.2.B Quarterly per-org input

`tilth archivist quarterly --org <slug>` — per-org Match DB outcome rollup + KFR full-corpus refresh review.

**Input bundle (`ArchivistQuarterlyPerOrgInput`, frozen, kw_only):**

- `run_id: str`.
- `org_slug: str`.
- `kfr_register_path: str` — same as §15.4.1.
- `match_database_path: str` — same as §15.4.1.
- `reports_dir: str` — vault path to the org's completed-reports archive. Defaults to `orgs/<org_slug>/vault/grants/`. `Path.resolve()` MUST sit under `orgs/<org_slug>/vault/grants/`. Archivist walks the subtree to find `*/reports/` directories and rolls up per-grant per-period outcomes.
- `lookback_window_quarters: int` — operator-set lookback for outcome rollup; default `4` (one year of quarters). Out of range (`<= 0`) → reject.
- `invoked_at_utc: datetime`.

**Bundle invariants (PRE-gate enforced).**
- All `_path` fields MUST resolve under `orgs/<org_slug>/`. Symlink → `F-ARCHIVIST-CROSS-ORG-LEAK.symlink_escape`.
- `lookback_window_quarters` MUST be `>= 1`. Out of range → reject.
- TTY check applies.

# §15.5 Output contracts (per cadence)

## §15.5.0 Schema delta from upstream substrates

Archivist's digest schemas extend the upstream substrate schemas with proposes-only metadata. All upstream substrate fields are read-only references; Archivist's digest schemas add per-proposal metadata layered on top.

| Schema | Field | Type | Source | Purpose |
|---|---|---|---|---|
| `archivist_kfr_refresh_digest.v1` | `digest_id` | opaque-uuid | NEW (Archivist-introduced) | Per-digest identifier for audit trail and merge resolution at operator review |
| `archivist_kfr_refresh_digest.v1` | `archivist_run_id` | str | NEW (Archivist-introduced) | Pins the digest to the Archivist invocation that produced it |
| `archivist_kfr_refresh_digest.v1` | `cadence` | Literal["weekly","quarterly"] | NEW (Archivist-introduced) | Cadence selector; routes the operator-review surface |
| `archivist_kfr_refresh_digest.v1` | `proposed_at_utc` | datetime | NEW (Archivist-introduced) | When the proposal was emitted; distinct from any KFR `populated_at` (which fires only at canonical promotion) |
| `archivist_kfr_refresh_digest.v1` | `proposed_action` | Literal["mark_stale","mark_pending_refresh","propose_archive","propose_supersede"] | NEW (Archivist-introduced) | Categorical proposed action the operator may approve at SP0 of the next active grant cycle |
| `archivist_kfr_refresh_digest.v1` | `source_substrate_path` | str | NEW (Archivist-introduced) | Path to the KFR entry whose state motivated the proposal |
| `archivist_kfr_refresh_digest.v1` | `source_entry_id` | str | NEW (Archivist-introduced) | KFR fact `id` field — operator can navigate from digest to canonical entry |
| `archivist_kfr_refresh_digest.v1` | `rationale` | str | NEW (Archivist-introduced) | Verbatim-where-possible reason for the proposal (e.g., "when_expiry has passed: 2025-12-31"); the operator-facing surface displays this side-by-side with the source KFR entry |
| `archivist_match_db_lessons_delta.v1` | `proposed_action` | Literal["surface_pattern","propose_action_state_change","mark_for_review"] | NEW (Archivist-introduced) | Categorical proposed action against Match DB |
| `archivist_match_db_lessons_delta.v1` | `pattern_summary` | str | NEW (Archivist-introduced) | Pattern-level summary string (e.g., "this funder declined this client 3 cycles in a row") — instance-level details forbidden by F-ARCHIVIST-LESSON-INSTANCE-LEAK |
| `archivist_funder_intel_quarterly.v1` | `proposed_action` | Literal["mark_stale","propose_promotion","propose_drop","integrity_check_failed"] | NEW (Archivist-introduced) | Categorical proposed action against Funder Intel DB entry |
| `archivist_funder_intel_quarterly.v1` | `funder_id` | str | NEW (Archivist-introduced) | Funder identifier from `vault_shared/funder_intelligence/register.yaml` |
| `archivist_lessons_proposal.v1` | `proposed_lesson_text` | str | NEW (Archivist-introduced) | Pattern-level proposed lesson; instance-level forbidden |
| `archivist_lessons_proposal.v1` | `source_lesson_refs` | list[str] | NEW (Archivist-introduced) | List of source lessons.json entry IDs the proposed lesson aggregates |

Field names preserve §11 Intake / §12 Uploader conventions (snake_case with substrate prefix; UTC-suffixed timestamps; `_at_utc` for datetime fields; `_id` for opaque references). Pydantic schemas live in `pipeline/orchestrator/seats/archivist/__init__.py` per §15.15 module scaffold (skeleton only at v0.2; full implementation at v1.x).

## §15.5.0.A Field-introduction pattern (per E-03 closure)

All NEW fields introduced by Archivist's digest schemas conceptually carry an `archivist_*` semantic prefix when they originate at Archivist (the schema name itself carries the prefix — `archivist_kfr_refresh_digest.v1`, `archivist_match_db_lessons_delta.v1`, etc. — and the per-row metadata fields likewise carry Archivist provenance via `archivist_run_id`). The concrete field-name pattern matches §11 Intake's `pending_facts.v1` schema delta convention (per §11.5.0): `_id` suffix for opaque identifiers, `_at_utc` suffix for timestamps, snake_case for everything, no markdown fences anywhere.

**Composition with upstream substrate.** Each digest entry's `source_substrate_path` + `source_entry_id` fields point at the upstream substrate's existing schema (KFR fact `id`, Funder Intel doc `funder_id`, Match DB row `match_id`, lessons.json entry `lesson_id`, Benchmarks Register entry `benchmark_id`); the operator-review surface displays the proposed action side-by-side with the upstream substrate entry by following the path + id pair. Archivist's digest schemas do NOT re-encode the upstream substrate's content — they only carry pointers + the proposed_action + rationale. This decoupling preserves substrate-side schema evolution: if the upstream substrate's schema changes (e.g., v7.0.5 Match DB adds new fields at v7.0.5.1), Archivist's digest schema remains unchanged because it holds only pointers, not content.

**YAML safe-load mandate (per RT-09 closure).** ALL YAML deserialization of Archivist digest files (in the operator review CLI; in any downstream consumer) MUST use `yaml.safe_load` (or the equivalent `ruamel.yaml.YAML(typ='safe')`); ANY use of `yaml.load` in Archivist seat code or in the operator review CLI is prohibited and detected by the §4 v2.x amendment AST-lint extension at compile time. Skeleton test `test_archivist_yaml_safe_load_only` (per §15.13.1) scans `pipeline/orchestrator/seats/archivist/**` for `yaml.load` calls and asserts zero matches. Closes the malicious-YAML-injection path (`!!python/object/apply:os.system`) where an attacker writing a digest file by other means could embed an executable Python object that fires when the review CLI parses the file.

## §15.5.1 Weekly tick output

**Output files.** Two per-org digest files written per weekly tick run (only files with at least one digest entry are written; empty digests skip write per §15.7 readiness check):

1. `orgs/<slug>/archivist_digests/kfr_refresh_<run_id>.yaml` — Pydantic-validated against `archivist_kfr_refresh_digest.v1` schema (per §15.5.0). Contains digest entries for: KFR facts whose `when_expiry` has passed (proposed_action=`mark_stale`); KFR facts whose `when_expiry` is within `lookback_window_days` of expiry (proposed_action=`mark_pending_refresh`); pending_facts queue entries that have been pending operator review for `> 30` days (proposed_action=`mark_for_review`).
2. `orgs/<slug>/archivist_digests/match_db_lessons_delta_<run_id>.yaml` — Pydantic-validated against `archivist_match_db_lessons_delta.v1` schema. Contains delta entries for Match DB rows that changed `action_state` (e.g., `proposed → operator_actioned`) within the lookback_window_days; pattern-level rollups of cross-cycle outcomes (per F-ARCHIVIST-LESSON-INSTANCE-LEAK §15.9.2 — instance-level FORBIDDEN, only pattern-level allowed).

**State file (separate from digest).** `pipeline/institutional_memory/archivist_state/<run_id>.yaml` — per-run Tilth-internal artifact per Rule 1.

**Reject audit trail.** `pipeline/validation/archivist_rejects/weekly/<org_slug>/<run_id>/` — one `<reject_id>.yaml` per F-ARCHIVIST-* reject (or other PRE-pre-surface rejection). Each reject entry includes: `proposed_digest_payload`, `source_substrate_path`, `source_entry_id`, `rejected_at_utc`, `reject_reason_code` (the gate sub-tag), and the diff snippet showing what would have been emitted to the operator-facing surface had the gate not fired.

**Operator-review surface.** Operator runs `tilth archivist review --org <slug> --cadence weekly` to enter the review surface (CLI for v0.2 + v1.x first ship; UI deferred per overall v0.1+v0.2 headless posture). Surface displays per-cadence digest entries with side-by-side (`proposed_action / source_substrate_path / source_entry_id / rationale`) and offers per-entry actions: **confirm** (apply the proposed action — operator-signed mutation to KFR or Match DB canonical state via the appropriate Vault write intent), **defer** (carry the entry forward to next weekly tick; entry remains in queue), **reject** (drop with audit trail under `pipeline/validation/archivist_review_rejects/`), **edit-then-confirm** (operator modifies the proposed action — for example, an operator may downgrade a `propose_archive` action to `mark_stale` based on context only the operator knows). All confirm / edit-then-confirm actions require operator Ed25519 signature per the §11.7 operator-review-signature precedent.

**Resumability.** Per Rule 1, the review session is resumable. Partial-confirm state persists in `pipeline/institutional_memory/archivist_state/review_<session_id>.yaml`. Operator can exit mid-review and resume; previously-confirmed entries do NOT re-appear; previously-rejected entries do NOT re-appear; previously-deferred entries DO re-appear in the next review session AND in the next cadence's digest (the deferral is metadata-tagged, not an in-place re-emission).

## §15.5.2 Quarterly review output

**Quarterly workspace cadence output:**

1. `vault_shared/archivist_digests/funder_intel_quarterly_<run_id>.yaml` — Pydantic-validated against `archivist_funder_intel_quarterly.v1` schema. Contains: stale Funder Intel docs (per `freshness_threshold_days` invariant); Funder Intel docs since last quarterly review (proposed_action=`propose_promotion` for new docs that operator may want to formally promote into the active corpus); integrity-check results (proposed_action=`integrity_check_failed` if any Funder Intel doc fails F-FUNDER-CORPUS-INTEGRITY per v7.0.5 §5).
2. `vault_shared/archivist_digests/benchmarks_freshness_<run_id>.yaml` — Pydantic-validated against an `archivist_benchmarks_freshness.v1` schema (delegated to v1.x amendment for full schema detail; v0.2 spec lists the proposed shape: per-benchmark-entry `last_refreshed_at_utc` + age-in-days + proposed_action=`mark_stale` for entries past freshness threshold).
3. `pipeline/institutional_memory/lessons_proposals/<run_id>.yaml` — Pydantic-validated against `archivist_lessons_proposal.v1` schema. Contains pattern-level proposed lessons rolled up from the workspace's lessons.json + Match DB cross-cycle patterns. Mirrors Intake's `pending_facts.yaml → register.yaml` discipline applied to lessons curation: Archivist proposes; operator promotes via `tilth archivist lessons-promote --proposal <run_id>`.

**Quarterly per-org cadence output:**

1. `orgs/<slug>/archivist_digests/kfr_quarterly_<run_id>.yaml` — full-corpus refresh review (broader scope than weekly tick's `kfr_refresh_<run_id>.yaml`; covers all KFR entries regardless of expiry, surfacing facts that are technically un-expired but `when_as_of` is older than `lookback_window_quarters` for operator's discretionary refresh).
2. `orgs/<slug>/archivist_digests/match_db_outcome_rollup_<run_id>.yaml` — per-grant per-period outcome rollup over `lookback_window_quarters`; pattern-level summary per (client × funder) pairs with cross-cycle results.

**Operator-review surface.** Same shape as §15.5.1 weekly review surface, scoped to quarterly digests.

# §15.6 Two cadences specification

## §15.6.0 Cadence summary table

| Cadence | Trigger | Input | Output | Done definition |
|---|---|---|---|---|
| **Weekly tick** (light) | Operator-explicit at v0.2 (`tilth archivist weekly`) | `ArchivistWeeklyInput` over per-org KFR + Match DB + lessons.json | Per-org KFR refresh digest + per-org Match DB lessons-delta digest + per-run state file | Digests + state + audit trail consistent; F-ARCHIVIST-* gates verified on every PASS entry |
| **Quarterly review** (heavy) | Operator-explicit at v0.2 (`tilth archivist quarterly --workspace` OR `tilth archivist quarterly --org <slug>`) | `ArchivistQuarterlyWorkspaceInput` OR `ArchivistQuarterlyPerOrgInput` | Workspace: Funder Intel + Benchmarks freshness + lessons proposals. Per-org: KFR quarterly + Match DB outcome rollup. | Same as weekly, scoped to quarterly substrate |

**Trigger detail per cadence (per E-02 closure).** The trigger column above is the high-level fire condition; the input contracts at §15.4 carry the full dataclass definitions + Path.resolve() invariants + TTY-discipline + signed-config requirement specifications. Specifically:

- **Weekly tick trigger detail** — see §15.4.1 (`ArchivistWeeklyInput`). v0.2 trigger: operator-explicit only via `tilth archivist weekly --org <slug>`; no scheduled-task wiring at v0.2. v1.x trigger: scheduled-task-driven via the `schedule` skill (Mondays 8:30 AM cron precedent from `project_monday_fund_routine.md`); operator-explicit invocation always remains valid regardless of scheduled-task state.
- **Quarterly review trigger detail** — see §15.4.2.A (`ArchivistQuarterlyWorkspaceInput`) for workspace cadence; §15.4.2.B (`ArchivistQuarterlyPerOrgInput`) for per-org cadence. v0.2 trigger: operator-explicit only via `tilth archivist quarterly --workspace` OR `tilth archivist quarterly --org <slug>`; no scheduled-task wiring at v0.2. v1.x trigger: scheduled-task-driven on a quarterly cadence (every 90 days from prior quarterly review, OR operator-set calendar alignment per `archivist_config.yaml` — operator's choice).

## §15.6.1 Weekly tick cadence

**When:** operator-driven at v0.2 (operator decides when; recommended Mondays per Monday fund-radar memory pattern). v1.x: scheduled-task-driven via the existing `schedule` skill — Mondays 8:30 AM cron from the per-org Tilth instance (per Monday fund-radar memory entry `project_monday_fund_routine.md`).

**Input:** per-org KFR canonical register, per-org Match DB register, workspace-shared lessons.json. Read-only access (no canonical mutation).

**Process (v1.x — describes what implementation will do; v0.2 spec only):**

1. **Read substrates.** Read KFR `register.yaml` + `pending_facts.yaml` (latter for queue-age detection only — no mutation), Match DB `register.yaml`, lessons.json. All reads via the §2 Vault read intent (no raw `open()` on substrate files); content_hash recorded for tamper-detection cross-reference per v7.0.4-M1 §4.

2. **KFR expiry scan.** Walk the KFR `facts` list; for each entry, compare `when_expiry` against `invoked_at_utc`. If `when_expiry` < `invoked_at_utc`: emit a `mark_stale` digest entry. If `when_expiry` is within `lookback_window_days` of `invoked_at_utc`: emit a `mark_pending_refresh` digest entry.

3. **Pending facts queue scan.** Walk Intake's `pending_facts.yaml`; for each entry whose `extracted_at_utc` is older than 30 days: emit a `mark_for_review` digest entry (the entry has been pending operator review beyond the operator's typical review cadence; surface this as a hint that operator may want to allocate review time).

4. **Match DB delta scan.** Walk Match DB `register.yaml`; for each row whose `action_state` changed within `lookback_window_days`: emit a `surface_pattern` digest entry summarizing the state change. Cross-cycle pattern detection (per §15.9.2 pattern-level only, no instance-level) is in scope for v1.x; v0.2 spec defers the pattern-detection prompt template to the v1.x amendment but pins the schema fields here.

5. **Lessons.json append (v1.x only).** Walk lessons.json's recent appends (within `lookback_window_days`); detect any new lesson that pattern-aligns with existing lessons (e.g., a third lesson about the same funder's behavior pattern triggers a "pattern-level rollup" proposal). Emit a `propose_pattern_rollup` proposal entry to `lessons_proposals/<run_id>.yaml`. Pattern-detection logic is the v1.x extraction LLM's responsibility per §15.8 substrate.

6. **Self-validate.** Run §15.7 readiness check — every digest entry has source_substrate_path + source_entry_id + rationale; every entry's source path is under the declared org subtree (per-org cadence); the digest file is Pydantic-schema-valid.

7. **Write digests.** Write `kfr_refresh_<run_id>.yaml` + `match_db_lessons_delta_<run_id>.yaml` via §2 Vault write intents.

8. **State.** Write `archivist_state.yaml` with `cadence_completed=true, digest_entries_produced, digest_entries_rejected, per-substrate read content_hash`.

**Done definition:** digest files contain all proposes-only entries from this weekly tick; state file written; reject audit trail consistent; no partial state on disk.

**Operator-next-step:** `tilth archivist review --org <slug> --cadence weekly` to enter the per-cadence review surface.

## §15.6.2 Quarterly review cadence

**When:** operator-driven at v0.2 (operator decides; recommended quarterly aligned with calendar quarters or fiscal year quarters per operator's preference). v1.x: scheduled-task-driven on a quarterly cadence (every 90 days from the prior quarterly review, or operator-set calendar alignment).

**Input:** Per the §15.4.2 split — workspace-level quarterly OR per-org quarterly are distinct invocations with distinct input bundles.

**Process (v1.x — v0.2 spec only):**

For workspace quarterly:
1. **Read substrates.** Funder Intel `register.yaml` + Benchmarks `register.yaml` + lessons.json. All reads via §2 Vault read intent.
2. **Funder Intel freshness pass.** Walk Funder Intel `register.yaml`; for each doc, check `last_promoted_at_utc` against `invoked_at_utc`. Past `freshness_threshold_days` → emit `mark_stale`. Funder Intel docs added since last quarterly review with `status: pending_promotion` → emit `propose_promotion`.
3. **Funder Intel integrity check.** For each Funder Intel doc, run F-FUNDER-CORPUS-INTEGRITY check per v7.0.5 §5 (SHA3-512 verification on the cached doc bytes against the integrity manifest). FAIL → emit `integrity_check_failed` digest entry; operator surface flags this at HIGH severity (the corpus has been tampered with).
4. **Benchmarks freshness pass.** Walk Benchmarks `register.yaml`; for each entry, check `last_refreshed_at_utc` against `invoked_at_utc`. Past freshness threshold → emit `mark_stale` Benchmarks digest entry.
5. **Lessons proposals.** Walk lessons.json + Match DB cross-cycle patterns; propose pattern-level rollups (per §15.9.2 — instance-level FORBIDDEN); write to `lessons_proposals/<run_id>.yaml`.
6. **Self-validate + write digests + state.** Same as weekly tick steps 6-8.

For per-org quarterly:
1. **Read substrates.** Per-org KFR + Match DB + reports archive. All via §2 Vault read intent.
2. **KFR full-corpus refresh.** Walk every KFR entry (not just expiring ones); flag entries with `when_as_of` older than `lookback_window_quarters` for operator's discretionary refresh review.
3. **Match DB outcome rollup.** Walk Match DB `register.yaml`; aggregate per-grant per-period outcomes over `lookback_window_quarters`; emit pattern-level summary per (client × funder) pair.
4. **Reports archive cross-reference.** Walk `orgs/<slug>/vault/grants/*/reports/`; emit "completed-report" reference rows that the operator may want to archive or reference at next cycle's KFR refresh.
5. **Self-validate + write digests + state.** Same as weekly tick steps 6-8.

**Done definition:** quarterly digest files written; state file written; reject audit trail consistent.

**Operator-next-step:** `tilth archivist review --cadence quarterly` (workspace) OR `tilth archivist review --org <slug> --cadence quarterly` (per-org) to enter the quarterly review surface.

# §15.7 Operator review UX (proposes-only discipline)

The Archivist review surface is the load-bearing UX for proposes-only discipline. Unlike Intake's autopromote-batch surface (which has a confidence-threshold-driven batch-confirm view), Archivist has **no autopromote path at all**. Every digest entry requires per-entry operator review and operator-signed confirmation; this is structural per §15.4.1 invariant ("no `--yes` / `--auto-confirm` / `--force` flags at v0.2 or any v1.x first ship") + §15.9.3 (`F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` fail-closed).

**Surface entry.** `tilth archivist review --org <slug> --cadence <weekly|quarterly>` (per-org) OR `tilth archivist review --workspace --cadence quarterly` (workspace). Surface displays unreviewed digest entries grouped by cadence and digest type.

**Per-entry display.** Each entry shows side-by-side: `proposed_action` / `source_substrate_path` / `source_entry_id` / `rationale`. Operator can navigate from the digest entry directly to the source substrate (e.g., "open KFR fact `<fact_id>`") via the operator's preferred editor (Tilth does NOT auto-open; operator follows the path manually).

**Per-entry actions:**

- **Confirm.** Apply the proposed action with operator Ed25519 signature. The mutation to KFR / Match DB / Funder Intel DB / lessons.json / Benchmarks Register canonical state happens VIA THE EXISTING SUBSTRATE'S WRITE INTENT (Archivist itself does not perform the mutation — see §15.9.3). For example: operator confirms a `mark_stale` proposal on KFR fact `<fact_id>`; the actual KFR mutation is invoked via `tilth kfr mark-stale --fact-id <fact_id> --signed-by <operator_key_id>` which is the existing KFR write surface per v7.0.4. The digest entry's `proposed_action` becomes a directive that drives the existing substrate's write CLI; Archivist's role ends at producing the digest entry. This decoupling is the load-bearing structural enforcement of proposes-only.
- **Defer.** Carry the entry forward to the next cadence's digest. The entry is metadata-tagged in the next digest as "deferred from <prior_run_id>" so operator can see deferral history.
- **Reject.** Drop the entry from the operator-review queue; log to `pipeline/validation/archivist_review_rejects/<org_slug>/<run_id>/<reject_id>.yaml` for audit trail. Reject does NOT mutate the source substrate; the entry simply doesn't get acted on.
- **Edit-then-confirm.** Operator modifies the `proposed_action` (e.g., downgrade `propose_archive` to `mark_stale` based on operator-only context); Archivist re-validates the modified entry against the schema and the operator-modified entry then routes through the same confirm path (operator-signed mutation via the source substrate's write CLI).

**Operator key requirement.** All confirm + edit-then-confirm actions require operator Ed25519 signature per the §11.7 operator-review-signature precedent. Reject + defer actions do NOT require operator signature (rejecting / deferring is non-load-bearing for canonical state); the action is logged with operator key id for audit but no canonical mutation happens.

**Per-entry confirmation nonce (per RT-05 closure + Cycle 2 NF-02 atomic-ledger closure — replay protection).** Each confirm action's signed payload MUST include a `confirmation_id: <opaque-uuid>` field unique per `(run_id, digest_entry_id)` pair. **Atomic check-then-write ledger semantics (per RT-05 PARTIAL + NF-02 closure).** The audit-ledger lookup at `pipeline/institutional_memory/archivist_confirmations.ledger.jsonl` MUST use `fcntl.flock(LOCK_EX)` (or equivalent OS-level file lock) for the entire duration of the lookup-then-append sequence — concurrent confirmation processes serialize at the lock; the second process sees the first's `confirmation_id` already in the ledger and rejects the replay. Lock acquisition pattern mirrors v7.0.4-M1 §4 atomic-read fcntl.flock precedent. Failure to acquire the lock within 30 seconds → fail-closed; the operator-facing error message names the lock-contention condition explicitly. The signed payload schema is:

```yaml
confirmation_payload:
  run_id: <archivist_run_id producing the digest>
  digest_entry_id: <opaque-uuid of the specific digest row being confirmed>
  confirmation_id: <opaque-uuid generated at confirm-action time; unique per (run_id, digest_entry_id) pair>
  proposed_action: <Literal — copied from the digest entry>
  proposed_action_payload: <copied from the digest entry>
  confirmed_at_utc: <UTC datetime>
  operator_key_id: <key fingerprint>
signature: <Ed25519 signature of canonical-bytes serialization of confirmation_payload>
```

The verification step at the substrate's write CLI (e.g., `tilth kfr mark-stale --confirmation-id <uuid> --signed-payload <path>`) MUST: (a) verify the Ed25519 signature; (b) look up `confirmation_id` in the immutable audit ledger at `pipeline/institutional_memory/archivist_confirmations.ledger.jsonl`; (c) reject any already-used `confirmation_id` (replay attack); (d) write the new `confirmation_id` to the ledger atomically with the substrate mutation. Replay against a different digest entry is structurally prevented because `confirmation_id` is bound to `(run_id, digest_entry_id)` by construction; a captured signed payload cannot be replayed against a different `digest_entry_id` because the signature covers the pair.

**TTY check on every action — bounded threat model (per RT-04 + RT-12 bundled closure).** All `tilth archivist review` actions verify `sys.stdin.isatty()` per the §15.4.1 + §11.7 TTY-discipline precedent. The TTY check is strengthened to: (a) verify `os.getsid(0) == os.getsid(1) == os.getsid(2)` (all stdio streams attached to the same session); (b) verify the controlling terminal device is a real `/dev/ttys*` (not a PTY master allocated by `script` / `expect` / `pexpect`) via `os.ttyname(0).startswith("/dev/ttys")`. Non-TTY invocation OR PTY-allocated invocation rejects with the same v0.2 + v1.x first-ship message as the cadence-trigger CLI.

**v0.2 + v1.x first-ship known limitation — bounded by v7 LOCKED A1+A4.** A determined adversary with shell access to the operator's machine could allocate a PTY via low-level system calls (raw `pty.openpty()` invocation that satisfies `os.ttyname(...)` checks), feed pre-recorded Ed25519 signatures, and bypass operator presence — automating the review flow from a CI job. Under the v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight) assumptions that govern v0.1 + v0.2 + v1.x first-ship deployments, the operator IS the only actor and the operator-trusted preflight is the security model; an adversary with shell access to the operator's machine has already breached the security boundary v7 LOCKED assumes is enforced by external means (operator's OS + physical security + key custody). **Disposition (mirrors v7.0.7 row 180 timing-side-channel disposition pattern):** v0.2 + v1.x first-ship known limitation; v2 multi-tenant mitigation track per v7 LOCKED Section O.5 (hardware-token second-factor via TPM/YubiKey challenge-response, deferred to v2 amendment); admin-risk ledger entry per any review-CLI-invocation-with-non-physical-TTY event for forward audit. The hardware-token requirement is structurally aligned with Section O.5 multi-tenant + zero-trust posture; v0.1 + v0.2 + v1.x first-ship are intentionally single-tenant + operator-trusted.

**No autopromote-batch surface — emphasized.** Unlike Intake's autopromote-batch view (which still requires operator-confirmed-batch and is itself protected by four layers), Archivist has NO autopromote path. There is no confidence threshold; there is no batch-confirm-by-source-doc; there is no spot-check sample. Every entry requires per-entry operator-signed confirmation. Rationale: Archivist's outputs are between-cycle curation actions on operator-confirmed canonical substrates — the consequence of an erroneous auto-applied curation action is a silent corruption of the canonical substrate (e.g., silently archiving a KFR fact that was not actually stale). This consequence is materially different from Intake's autopromote-batch (which produces operator-confirmed *new* candidate facts in a queue, never canonical mutations); Intake's autopromote can be batch-confirmed because the worst case is operator wastes review time on a slightly-misconfidence-tagged candidate, whereas Archivist's worst case is silent canonical corruption. The seats' UX postures differ by their consequence asymmetry.

**Resumability.** Per Rule 1, the review session is resumable across CLI invocations. Partial state persists in `pipeline/institutional_memory/archivist_state/review_<session_id>.yaml`.

# §15.8 Substrate

**No extraction LLM at v0.2.** The v0.2 spec-only disposition explicitly excludes any LLM invocation on Archivist's part. Cadence-driven digest production at v0.2 is operator-driven (operator manually walks the substrates referencing the digest templates); the digest schemas are pinned at v0.2 SPEC LOCK and the v1.x extraction LLM produces digest entries against those schemas at v1.x amendment.

**v1.x substrate (forward-design — non-binding for v0.2).** Per `project_archivist_v1x_candidate_seat.md` memory entry + v7.0.4 §9 + v7.0.5 §6:

- **Local LLM.** Small local LLM, Mistral 7B class (per the v7 architecture envelope; same model family as Intake's extraction LLM per §11.8). Specific binding lives in `/router.yaml` per the SOLE-source-of-binding discipline; the §15 blueprint does NOT hardcode the model name.
- **Local vector store.** FAISS or Chroma — composes against existing per-org Intake embeddings + workspace-shared Funder Intel embeddings + Match DB structured vectors per v7.0.5 §1. Archivist does NOT introduce a new vector substrate; it reads from the existing local vector store with per-substrate namespace per v7.0.5 F-VECTOR-NS-MISMATCH discipline.
- **Embedding model.** bge-large-en-v1.5 (per v7.0.4 §5 substrate decision; same model family as Intake / Funder Intel DB indexing).
- **Orchestration.** Pydantic AI agent (per v7.0.3 substrate decision; same orchestration substrate as council seats + Intake / Uploader). Tool composition: substrate-read tools (KFR / Funder Intel DB / Match DB / lessons.json / Benchmarks Register read wrappers) wrapped as Pydantic AI tools with org_slug + workspace parameter validation; structured-output digest emission with v1 schemas as the output Pydantic models.
- **Always-local routing.** Per §15.10 (mirrors Intake §11.10). No cloud LLM at any cadence at any v1.x first ship.
- **Sealed embedding endpoint.** Same Golden-Image-baked discipline as Intake (per v7.0.4 §5 + Intake §11.10): `/etc/tilth/embedding_endpoint.yaml` validated against localhost-or-unix-socket allowlist. F-INTAKE-EMBEDDING-ENDPOINT-INVALID (§11.9.10) applies to Archivist's tool calls just as to Intake's; Archivist does NOT introduce its own endpoint config.

**No marketplace access from the appliance.** Per ADR-001, every dependency is frozen at Golden Image build. Archivist's v1.x substrate is exactly: FAISS or Chroma + bge-large-en-v1.5 + Mistral 7B class + Pydantic AI + the existing §2 Vault read/write intent wrappers. New substrate elements require a Golden Image rebuild + an ADR amendment.

**Composition with §11 Intake substrate.** Archivist composes against existing Intake embeddings (per-org KFR doc embeddings stored under `orgs/<slug>/vault/intake/embeddings/`); does NOT re-embed substrate at curation time. The compound-key embedding storage path (§11.9.8 RT-10 closure: `<org_slug>_<doc_hash>` directory naming) keeps Archivist reads namespace-isolated; F-INTAKE-EMBEDDING-NS-MISMATCH (§11.9.8) applies to Archivist's tool calls.

# §15.9 Logician gate family — F-ARCHIVIST-*

Archivist introduces a small focused gate family at v0.2 SPEC LOCK, all registered in the §4 Logician v2.x amendment (WS-L). All gates are deterministic (Python predicates + Cedar policies); zero token cost. Per the v0.2 spec-only disposition, the gate predicates are skeleton stubs at v0.2 (raise NotImplementedError) and become live Cedar/Python at v1.x via §4 v2.x amendment.

**v1 gate roster (5 codes — 1 new from Cycle 1 RT-11 closure: F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT):**

| # | Code | Position | Owner-§ | Notes |
|---|------|----------|---------|-------|
| 1 | F-ARCHIVIST-CROSS-ORG-LEAK | PRE + POST | §15.9.1 | Per-org digest aggregates content from foreign org subtree; OR substrate-read path resolves outside declared org subtree; OR workspace-aggregate digest leaks per-org content (vs aggregate statistics carve-out). Sub-tags `.symlink_escape`, `.path_outside_org`, `.unconfirmed_substrate_read`, `.workspace_digest_per_org_content`, `.aggregate_insufficient_orgs` (NEW per RT-06 closure — fires when workspace digest is generated for workspace with fewer than `N` orgs default `N=3`). |
| 2 | F-ARCHIVIST-LESSON-INSTANCE-LEAK | PRE | §15.9.2 | Proposed lessons.json patch carries instance-level details (specific funder name + specific client name + specific reason) instead of pattern-level abstraction. Sub-tags `.client_name_present`, `.funder_specific_with_client`, `.reason_attributable_to_specific_outcome`, `.ner_entity_match` (NEW per RT-07 closure — NER detection beyond regex), `.unicode_homoglyph` (NEW per RT-07 closure — pre-NFKC content matched a forbidden entity). Mirrors R.6 Telemetry Commons invariant. |
| 3 | F-ARCHIVIST-AUTO-APPLY-ATTEMPTED | PRE | §15.9.3 | Archivist code path attempts direct mutation of KFR / Funder Intel DB / Match DB / lessons.json / Benchmarks Register canonical state (vs producing a digest entry that operator approves to drive existing substrate's write CLI). Fail-closed at the gate; mutation never reaches canonical state. Sub-tags `.ast_lint_violation`, `.runtime_dispatcher_violation`, `.cedar_policy_denied`, `.subprocess_canonical_cli_invocation` (NEW per RT-01 closure — subprocess of `tilth <substrate-cli>` from within Archivist), `.foreign_file_write_helper_import` (NEW per RT-02 closure — imported module exposes file-write API outside Archivist package), `.principal_spoofing_detected` (NEW per RT-03 closure — Cedar principal does not match `archivist_seat` self-asserted identity). |
| 4 | F-ARCHIVIST-CADENCE-DRIFT | PRE | §15.9.4 | Scheduled cadence missed by `> 2x` interval (e.g., weekly tick not run for `> 14` days; quarterly not run for `> 180` days). Surface to operator (the absence of Archivist running is itself a signal). At v0.2 the cadence is operator-driven so this gate is informational-only; v1.x activates as fail-closed PRE-gate when scheduled-task wiring lands (RT-10 closure: `severity = HIGH` and `gate.action = FAIL_CLOSED` MUST be set at v1.x amendment). |
| 5 | **F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT** | PRE-substrate-read | §15.9.5 | NEW from Cycle 1 RT-11 closure. Every substrate read attempt by Archivist MUST go through the appropriate Vault read intent wrapper (`vault_read_intent_kfr` / `vault_read_intent_funder_intel` / `vault_read_intent_match_db` / `vault_read_intent_lessons` / `vault_read_intent_benchmarks` / `vault_read_intent_archivist_state`); reads via raw `open()` or generic file-read helpers fail-closed. The Vault read intent is the sole layer that performs SHA3-512 hash verification per v7.0.4-M1 §4 + v7.0.5 §5 F-FUNDER-CORPUS-INTEGRITY; bypassing it skips integrity verification. Sub-tags `.raw_open_call`, `.generic_helper_import`, `.vault_intent_signature_invalid`. |

## §15.9.1 F-ARCHIVIST-CROSS-ORG-LEAK (PRE + POST)

**Purpose.** Refuse Archivist invocation when any input substrate path resolves outside the declared `org_slug` subtree (PRE), AND refuse digest emission when any digest entry references content outside the declared scope (POST).

**Predicate (PRE — substrate-read path validation).** Per-cadence per-substrate per §15.4 invariants:

- **Weekly tick:** `Path.resolve(kfr_register_path)` MUST sit under `orgs/<org_slug>/vault/kfr/`. `Path.resolve(match_database_path)` MUST sit under `orgs/<org_slug>/match_database/`. `Path.resolve(lessons_json_path)` MUST sit under `pipeline/institutional_memory/`.
- **Quarterly workspace:** `Path.resolve(funder_intel_register_path)` MUST sit under `vault_shared/funder_intelligence/`. `Path.resolve(benchmarks_register_path)` MUST sit under `vault_shared/benchmarks/`.
- **Quarterly per-org:** `Path.resolve(kfr_register_path)`, `Path.resolve(match_database_path)`, `Path.resolve(reports_dir)` MUST all sit under `orgs/<org_slug>/`.

**Predicate (POST — digest content validation).** Each digest entry's `source_substrate_path` MUST resolve under the declared scope (org_slug subtree for per-org cadences, vault_shared for workspace cadences). Workspace-aggregate digests MUST contain only aggregate statistics (e.g., percentages, counts) — per-org content (specific KFR fact text, specific Match DB narratives, specific client names) MUST NOT appear in any workspace-aggregate digest entry. The post-gate detector is a regex + structured-field check: any `source_substrate_path` field in a workspace digest that matches `^orgs/[^/]+/` triggers `.workspace_digest_per_org_content`; any `pattern_summary` or `rationale` field in a workspace digest containing org_slug literals from the workspace's `orgs/ORG_INDEX.md` triggers the same sub-tag.

**Sub-tags.**
- `.symlink_escape` — `Path.resolve()` followed a symlink to a path outside the allowed subtree.
- `.path_outside_org` — substrate-read path resolves outside the declared org_slug subtree (per-org cadences) or outside vault_shared (workspace cadences).
- `.unconfirmed_substrate_read` — Archivist attempted to read a non-operator-confirmed substrate (e.g., `pending_facts.yaml` from Intake; `proposal_commitments.yaml` with `status: PENDING_OPERATOR_REVIEW`); Archivist may read these for queue-age detection only (per §15.6.1 step 3) and that read goes through a separate dedicated metadata-only read tool that explicitly DOES NOT extract content fields, only metadata (timestamps, queue length); any content extraction triggers the gate. **Metadata-only read tool contract (per Judge DC-01 closure + Cycle 1 RT-08 runtime-instrumentation closure).** The contract for this metadata-only read tool MUST be specified as part of the §15 v1.x implementation amendment, including a non-negotiable test case in `tests/seats/archivist/` that asserts a `ForbiddenContentReadError` is raised if any field other than the documented metadata fields (`extracted_at_utc`, `fact_id`, `queue_length`, `last_modified_at_utc`) is accessed. The tool is the SOLE permitted read path for unconfirmed substrates; ALL Archivist read helpers MUST be instrumented to emit a gate-result with this sub-tag when the source path is under a *pending* namespace, regardless of which helper or import path is used. AST-lint extension at the §4 v2.x amendment forbids any import of generic `read_yaml` / `read_json` / `read_text` utility from outside the Archivist package — Archivist seat code's read-helper imports are restricted to the explicit Vault read intent wrappers (per §15.9.5 RT-11 closure).
- `.workspace_digest_per_org_content` — workspace-aggregate digest contains per-org content (specific KFR fact text, specific narratives, specific client names) instead of aggregate statistics. POST-gate regex check inspects `source_substrate_path` field, `rationale` field, AND `pattern_summary` field for org_slug literals from `orgs/ORG_INDEX.md`; any literal match → fire.
- `.aggregate_insufficient_orgs` (NEW per RT-06 closure) — workspace-level digest is being generated for a workspace containing fewer than `N` orgs (default `N = 3`; operator-tunable per `archivist_config.yaml` Ed25519-signed config field with the same Ed25519-signed config discipline as Intake's `intake_config.yaml`). When triggered, the gate suppresses any per-org-derived statistics in the workspace digest (e.g., "100% of clients have stale KFR" when there is only 1 client → suppressed; replaced with `aggregate_insufficient_orgs: true` flag and an operator-facing notice "insufficient orgs to compute aggregate; per-org review recommended"). Closes the minimal-org-statistical-inference attack where a workspace summary trivially reveals per-org state. The default `N = 3` is the minimum where aggregate statistics are not trivially identifiable per-org; operators with workspaces below the threshold receive only structural counts (e.g., "you have 2 orgs; per-org review recommended") with no statistical aggregates.

**Position.** PRE (substrate-read validation, fires before any read); POST (digest content validation, fires before write to operator-facing surface).

**Severity.** P0 (Law 3 enforcement). Admin-risk ledger logged at HIGH severity (`LAW3_VIOLATION` ledger kind).

**Failure path.** Refuse Archivist invocation (PRE) or refuse digest emission (POST) + log to admin-risk ledger + write `archivist_state.yaml` with `cadence_completed=false, failure_reason="F-ARCHIVIST-CROSS-ORG-LEAK.<sub-tag>"` + clear operator-facing error message + exit non-zero. Operator must investigate the cross-org leak path manually.

**Composition with §11.9.8 F-INTAKE-EMBEDDING-NS-MISMATCH.** Archivist's local vector store reads route through the same Pydantic AI tool wrappers as Intake's; F-INTAKE-EMBEDDING-NS-MISMATCH applies. F-ARCHIVIST-CROSS-ORG-LEAK is the substrate-read-path-level enforcement; F-INTAKE-EMBEDDING-NS-MISMATCH is the vector-store-tool-call-level enforcement. Both gates are required; they catch different attack surfaces.

## §15.9.2 F-ARCHIVIST-LESSON-INSTANCE-LEAK (PRE)

**Purpose.** Refuse a proposed lessons.json patch that carries instance-level details (specific funder name + specific client name + specific reason) rather than pattern-level abstraction. Mirrors the R.6 Telemetry Commons invariant: lessons that propagate across the cooperative MUST be pattern-level (e.g., "Federal program officers in this category often decline in cycles where applicants undercount sub-awardees") not instance-level (e.g., "Funder X declined Client Y for reason Z"). The pattern-level discipline preserves Law 3 across the lessons surface and prepares the lessons substrate for Stage-5 cooperative-commons sharing without leaking per-org content.

**Predicate (three-layer detection per RT-07 closure — replaces regex-only).**

The detection is a three-layer union-of-fail (any layer fires → reject the proposed-lesson entry; other entries in the same run continue):

1. **Layer 1 — Unicode NFKC normalization step.** `proposed_lesson_text` is normalized via `unicodedata.normalize('NFKC', text)` BEFORE detection runs. Closes the Unicode-homoglyph evasion path (where attacker uses Cyrillic 'а' (U+0430) for Latin 'a' (U+0061) in client names to bypass detection). Pre-NFKC content that would have matched but post-NFKC normalized to a forbidden entity → also fires sub-tag `.unicode_homoglyph` for audit-trail clarity.
2. **Layer 2 — named-entity recognizer (NER).** A small local NER model (`xx-ent-wiki-sm` from spaCy or equivalent multilingual NER substrate; frozen at Golden Image build per ADR-001 — no marketplace access) extracts mentions of org names + funder IDs + client identifiers from the NFKC-normalized text. Any detection of a named entity that is in the workspace's `orgs/ORG_INDEX.md` (per-org client names) OR `vault_shared/funder_intelligence/register.yaml` (per-funder identifiers) → fires sub-tag `.ner_entity_match` (regardless of wording — paraphrased, abbreviated, or referenced by inferred attributes; NER catches what regex misses).
3. **Layer 3 — regex check.** The original hand-crafted regex set (literal name matches, funder+client combinations, instance-attribution language patterns) still runs as a fast-path for explicit literal matches. Sub-tags `.client_name_present`, `.funder_specific_with_client`, `.reason_attributable_to_specific_outcome` retained from the original predicate.

**Common abbreviation expansion.** Operator-curated table at `vault_shared/archivist_abbreviation_expansion.yaml` (Ed25519-signed by operator with the same signed-config discipline as `intake_config.yaml`); maps common abbreviations to their expanded forms (e.g., "SLOs" → "Service Level Objectives"; "LOIs" → "Letters of Intent"; client-specific abbreviations like "FFCoop" → "FIT Farms Cooperative"). Layer 2 (NER) processes both the raw and the expansion-applied text; either matching → fires.

**NER adversarial-robustness disposition (per Cycle 2 NF-04 closure — bounded by v7 LOCKED A4).** The local NER model (`xx-ent-wiki-sm` from spaCy) is best-effort detection; adversarial Unicode-homoglyph + crafted text could in principle cause the NER component to miss an entity even after NFKC normalization (Layer 1 catches most homoglyph variants, but novel adversarial constructions remain). **Disposition: bounded by v7 LOCKED A4 (operator-trusted preflight)** — the operator is the sole author of `proposed_lesson_text` (Archivist's pattern-detection LLM at v1.x produces the candidate; operator reviews + approves the proposal at the operator-review surface per §15.7 BEFORE it lands in `lessons_proposals/<run_id>.yaml`). The operator review surface is the load-bearing trust boundary; an adversarially-crafted instance-level lesson that evades all three detection layers AND survives operator review is outside the §15 v1 threat model. v2 amendment lands NER adversarial-robustness testing as part of §4 v2.x amendment (test corpus of known evasion attempts; per-deployment NER model upgrade cadence; Sovereign Node LLC ships NER model updates per the router-template-update precedent).

**Sub-tags.**
- `.client_name_present` — Layer 3 regex match: proposed_lesson_text contains a literal client name from `orgs/ORG_INDEX.md`.
- `.funder_specific_with_client` — Layer 3 regex match: proposed_lesson_text combines specific funder ID with specific client identifier.
- `.reason_attributable_to_specific_outcome` — Layer 3 regex match: proposed_lesson_text uses instance-attribution language.
- `.ner_entity_match` (NEW per RT-07) — Layer 2 NER detection: NER extracted a named entity matching the workspace's org/funder/client identifier set; instance-level smuggle attempt detected regardless of paraphrase / abbreviation.
- `.unicode_homoglyph` (NEW per RT-07) — Layer 1 NFKC normalization revealed forbidden entity that pre-normalization regex would have missed.

**Position.** PRE (fires BEFORE any proposed-lesson entry is written to `lessons_proposals/<run_id>.yaml`).

**Failure path.** Refuse the proposed-lesson entry (other entries in the same run continue) + log to admin-risk ledger at MEDIUM severity (`LAW3_PATTERN_VS_INSTANCE` ledger kind) + write reject to `pipeline/validation/archivist_rejects/lessons_instance_leak/<org_slug>/<run_id>/`. Operator-facing surface for that run flags the rejected entry separately from confirmed-pattern-level entries; operator can inspect the rejected entry's payload at the audit-trail path if curious.

**Severity.** MEDIUM. The leak is contained (the entry never reaches `lessons_proposals/<run_id>.yaml` or the workspace-shared lessons.json); the rejection is a structural prevention, not a remediation.

**Composition with R.6 Telemetry Commons.** The pattern-vs-instance distinction here is the same invariant R.6 enforces for cross-Tilth lessons sharing at Stage 5. v0.1 + v0.2 + v1.x first ship are single-Tilth (no cross-Tilth lessons sharing); F-ARCHIVIST-LESSON-INSTANCE-LEAK is the *upstream* enforcement that prepares the lessons substrate for safe Stage-5 propagation. If lessons.json contains only pattern-level entries at the time Stage-5 cooperative-commons goes live, no per-org content is at risk.

## §15.9.3 F-ARCHIVIST-AUTO-APPLY-ATTEMPTED (PRE)

**Purpose.** Refuse any code path where Archivist directly mutates KFR / Funder Intel DB / Match DB / lessons.json / Benchmarks Register canonical state. Archivist's only allowed substrate write is to `archivist_digests/` or `lessons_proposals/` (proposes-only digest output). Any attempt to call a canonical-state write CLI / tool / write intent from inside Archivist's process → fail-closed at the gate.

**Predicate (three-layer defense + Cycle 1 hardening per RT-01 + RT-02 + RT-03 closures).**

1. **AST-lint level (extended per RT-01 + RT-02 closures).** The §4 v2.x amendment registers an AST-lint rule **R-ARCHIVIST-NO-CANONICAL-MUTATE** that scans `pipeline/orchestrator/seats/archivist/**` source files at build time for forbidden patterns:
   - **Direct write-intent calls.** Any direct invocation of `kfr_write_intent(...)` / `funder_intel_write_intent(...)` / `match_db_write_intent(...)` / `lessons_json_write_intent(...)` / `benchmarks_write_intent(...)` from within Archivist seat code → fire `.ast_lint_violation`.
   - **Subprocess of canonical-write CLI (RT-01 closure).** Any `subprocess.*` / `os.system` / `os.popen` / `os.exec*` / `os.spawn*` / `pexpect.*` invocation whose argument list (or string concatenation thereof, including f-strings, `str.format()`, `str.join()`, `+` concatenation) contains the literal token `tilth` OR any of the canonical-write sub-commands (`kfr`, `funder-intel`, `match-db`, `lessons`, `benchmarks`) → fire `.subprocess_canonical_cli_invocation`. The compound-token detection inspects each f-string segment, each format-string template positional, each str.join element; the lint rule's regex set is the union of `r'\btilth\b'` plus the five sub-command literals.
   - **Foreign file-write helper imports (RT-02 closure).** Any `import` / `from ... import` statement that imports from a module outside the `pipeline.orchestrator.seats.archivist.*` package OR outside the explicit allowlist (`pipeline.vault.read_intents`, `pipeline.vault.write_intents.archivist_*` only) where the imported symbol exposes a file-write API (`atomic_write`, `write_file`, `safe_write`, `tempfile.NamedTemporaryFile` with `delete=False`, etc.) → fire `.foreign_file_write_helper_import`. The lint rule maintains an allowlist of approved Archivist write APIs (the explicit Vault write intents for `archivist_digests/` / `lessons_proposals/` / `archivist_state/` / `archivist_rejects/` paths).
   - **Raw write to non-allowed prefix.** Any `os.write` / `pathlib.Path.write_text` / `pathlib.Path.write_bytes` / `open(..., 'w')` / `open(..., 'a')` / `open(..., 'wb')` / `open(..., 'ab')` against any path NOT matching the allowed prefixes (`orgs/<slug>/archivist_digests/`, `vault_shared/archivist_digests/`, `pipeline/institutional_memory/lessons_proposals/`, `pipeline/institutional_memory/archivist_state/`, `pipeline/validation/archivist_rejects/`, `pipeline/validation/archivist_review_rejects/`).
   - **Unsafe YAML deserialization (RT-09 closure).** Any `yaml.load(...)` call → fire `.ast_lint_violation` sub-class `.unsafe_yaml_load`. Only `yaml.safe_load` (or `ruamel.yaml.YAML(typ='safe')`) is permitted.

2. **Runtime PRE-gate level (extended per RT-01 + RT-02 closures).**
   - **Vault write intent dispatcher (existing).** Every write operation Archivist attempts is wrapped by the §2 Vault write intent dispatcher; the dispatcher checks the requested write path against the Archivist allowed-prefix set; mismatch → fail-closed at the dispatcher BEFORE the write executes; fire `.runtime_dispatcher_violation`.
   - **Process-creation guard (RT-01 closure).** A runtime guard injected at Archivist seat module import time wraps `subprocess.Popen`, `subprocess.run`, `subprocess.call`, `subprocess.check_call`, `subprocess.check_output`, `os.system`, `os.popen`, `os.exec*`, `os.spawn*`, `pexpect.spawn`, and any other process-creation primitive. The guard rejects any process creation unless the spawned binary is in the Archivist process-creation allowlist (only the Archivist seat module's own re-entrant invocations for sub-cadence dispatch — NO shell, NO other tilth subcommand, NO `bash` / `sh` / `python` invocation). Mismatch → `PermissionError` raised; fire `.subprocess_canonical_cli_invocation` at the runtime guard layer (defense-in-depth on top of AST-lint).
   - **File-write shim (RT-02 closure).** A runtime shim injected at Archivist seat module import time wraps the built-in `open()` and `pathlib.Path.write_text` / `pathlib.Path.write_bytes`. The shim validates the target path against the allowed-prefix set per item 1; mismatch → `PermissionError` raised; fire `.foreign_file_write_helper_import` at the runtime shim layer (catches the case where a foreign helper bypassed AST-lint by being dynamically imported via `importlib`). The shim is part of the seat module and cannot be unloaded or bypassed at runtime by Archivist code (the shim install happens before any user-code import; subsequent attempts to restore the unwrapped builtins are themselves AST-lint-detected).

3. **Cedar policy level (extended per RT-01 + RT-03 closures).**
   - **Existing.** The §4 v2.x amendment registers a Cedar policy `archivist_proposes_only.cedar` that explicitly DENIES Archivist principal access to the canonical write intents (KFR / Funder Intel DB / Match DB / lessons.json / Benchmarks Register). The Cedar policy is defense-in-depth on top of the AST-lint + runtime checks.
   - **Process-create capability denial (RT-01 closure).** Cedar policy adds explicit DENY of the `process_create` capability for the Archivist principal; closes the policy-level path to subprocess invocation regardless of runtime-shim state.
   - **Principal binding (RT-03 closure).** The Archivist seat MUST self-assert its principal at startup by reading a Sovereign Node LLC operator-signed token embedded in the Golden Image at `/etc/tilth/seat_identity/archivist.signed.yaml`. The signed token includes `principal.id == "archivist_seat"` + `principal.signed_by == <SN_LLC_pinned_pubkey>` + a content-hash of the Archivist seat module bytes. The startup assertion: (a) reads the signed token; (b) verifies the SN-LLC Ed25519 signature against the Golden-Image-pinned SN-LLC public key (per A12 crypto-agility envelope); (c) verifies the content-hash matches the actually-loaded Archivist seat module bytes; (d) sets the Cedar principal context for all subsequent policy evaluations to the asserted identity. Cedar policy adds attribute check `principal.id == "archivist_seat" && principal.signed_by == <SN_LLC_pinned_pubkey>`; mismatch → DENY all canonical write intents, fire `.principal_spoofing_detected`. Closes the principal-spoofing path where an attacker sets `CEDAR_PRINCIPAL=operator` env var to bypass the proposes-only policy.

**Cycle 2 closures (RT-01 / RT-02 PARTIAL + NF-05 disposition).**

- **RT-01 PARTIAL (low-level execs via `ctypes` / `os.execve` through FFI) + NF-05 (`ctypes`-routed canonical-CLI launch):** EXTEND R-ARCHIVIST-NO-CANONICAL-MUTATE AST-lint to ALSO forbid imports of `ctypes` / `cffi` / any FFI module from Archivist seat code. Combined with the explicit `os.execve` / `os.execvp` etc. enumeration in the process-creation runtime guard list (already in §15.9.3 item 2), this catches the FFI-launch path at compile time. **Residual bypass via dynamic-loaded shared library that calls `execve` directly is bounded by v7 LOCKED A1 + A4 single-client + operator-trusted preflight assumptions** (mirrors RT-04/12 + v7.0.7 row 180 timing-side-channel disposition pattern); v2 multi-tenant amendment lands kernel-level sandbox interception per Section O.5.
- **RT-02 PARTIAL (importlib.import_module bypass after shim install) + RT-08 PARTIAL:** EXTEND R-ARCHIVIST-NO-CANONICAL-MUTATE AST-lint to ALSO forbid `importlib.import_module(...)` AND `__import__(...)` calls in Archivist seat code. These are dynamic-import primitives that can bypass the import-time AST-lint check. The static AST-lint catches the dynamic-import call at compile time; the runtime open-shim catches the actual write attempt regardless of how the helper got loaded. Combined defense-in-depth closes the gap.

**Sub-tags.**
- `.ast_lint_violation` — AST-lint detected forbidden write-intent call OR raw-write-to-non-allowed-prefix call in Archivist seat code at compile time.
- `.runtime_dispatcher_violation` — Vault write intent dispatcher caught a runtime attempt.
- `.cedar_policy_denied` — Cedar policy denied the write intent.
- `.subprocess_canonical_cli_invocation` (NEW per RT-01) — subprocess invocation of `tilth <substrate-cli>` from within Archivist (caught at AST-lint OR runtime guard layer).
- `.ffi_import_forbidden` (NEW per RT-01 PARTIAL + NF-05 closure) — Archivist seat code imports `ctypes` / `cffi` / FFI module (caught at AST-lint).
- `.dynamic_import_forbidden` (NEW per RT-02 PARTIAL + RT-08 PARTIAL closure) — Archivist seat code calls `importlib.import_module(...)` or `__import__(...)` (caught at AST-lint).
- `.foreign_file_write_helper_import` (NEW per RT-02) — imported module exposes file-write API outside the Archivist package allowlist (caught at AST-lint OR runtime shim layer).
- `.principal_spoofing_detected` (NEW per RT-03) — Cedar principal does not match `archivist_seat` self-asserted identity (caught at policy-eval layer).
- `.token_rotation_requires_golden_image_rebuild` (NEW per NF-03 disposition; advisory) — informational sub-tag emitted at admin-risk ledger surface when SN-LLC signed token approaches rotation due-date; rotation requires Golden Image rebuild at v0.2 + v1.x first ship; v2 amendment lands rolling-rotation mechanism per Section O.5.

**Position.** PRE (AST-lint at build time; runtime dispatcher at write-call time; Cedar at policy-eval time). All three layers are required; removing any one creates an auto-apply path.

**Failure path.** Refuse the write + log to admin-risk ledger at HIGH severity (`SEAT_BOUNDARY_VIOLATION` ledger kind) + write `archivist_state.yaml` with `cadence_completed=false, failure_reason="F-ARCHIVIST-AUTO-APPLY-ATTEMPTED.<sub-tag>"` + clear operator-facing error message naming the attempted write path + exit non-zero. AST-lint failures fail the build; the seat module never reaches a runnable state.

**Severity.** HIGH. The attempt indicates a structural seat-boundary violation; the consequence had it succeeded would be silent canonical-substrate corruption (the highest-severity class of substrate damage). Three-layer defense matches the §11.7 four-layer Intake autopromote-batch defense in pattern (defense-in-depth at multiple layers; removing any one creates the failure path).

**Composition with §11.9 Intake / §12 Uploader gate families.** Both Intake and Uploader have analogous fail-closed gates against their own boundary violations (Intake: F-EXTRACTOR-FABRICATION prevents fabricated facts; Uploader: F-UPLOADER-AUTOSUBMIT-ATTEMPTED prevents auto-submit). F-ARCHIVIST-AUTO-APPLY-ATTEMPTED is the Archivist-specific equivalent — the proposes-only contract is structural across all three support agents, with each agent having its own gate code for its own boundary.

## §15.9.4 F-ARCHIVIST-CADENCE-DRIFT (PRE)

**Purpose.** Surface to operator when the scheduled cadence has been missed by `> 2x` interval (e.g., weekly tick not run for `> 14` days; quarterly review not run for `> 180` days). The absence of Archivist running is itself a signal — operator may be over-loaded, the schedule may be misconfigured, the substrate may have grown to require manual intervention, etc.

**Predicate.**

1. At every Archivist cadence invocation (operator-explicit at v0.2; scheduled-task-fired at v1.x), locate the most recent prior `archivist_state.yaml` for the same cadence type (weekly tick OR quarterly workspace OR quarterly per-org) under `pipeline/institutional_memory/archivist_state/`.
2. Compute `time_since_last_run_days` from the prior state's `invoked_at_utc` to the current invocation's `invoked_at_utc`.
3. Compare against the cadence interval: `>2x` weekly interval = `> 14` days; `>2x` quarterly interval = `> 180` days.
4. If `>2x` interval AND v1.x scheduled-task wiring is live → fire as fail-closed PRE-gate (refuse the cadence run; require operator to acknowledge the drift and manually re-trigger).
5. If `>2x` interval AND v0.2 (operator-driven cadence; no scheduled-task wiring) → fire as INFORMATIONAL-only (do not refuse; surface to operator-facing log; the absence is operator's own decision).

**Sub-tags.**
- `.weekly_drift` — weekly tick missed by `> 14` days.
- `.quarterly_workspace_drift` — quarterly workspace cadence missed by `> 180` days.
- `.quarterly_per_org_drift` — quarterly per-org cadence missed by `> 180` days.

**Position.** PRE (fires at cadence invocation start, before any substrate read).

**Failure path (v1.x).** Refuse cadence + log to operator notification surface (per §15.7 surface conventions) + write `archivist_state.yaml` with `cadence_completed=false, failure_reason="F-ARCHIVIST-CADENCE-DRIFT.<sub-tag>"` + require operator to manually re-trigger with explicit `--acknowledge-drift` flag (which is the ONLY non-`--yes`-class flag allowed, because acknowledging cadence drift is itself an explicit operator decision rather than a silent bypass).

**Failure path (v0.2).** Informational only; log to operator notification surface; do not refuse cadence; cadence proceeds normally. The operator's prior decision to defer the cadence is respected.

**Severity.** LOW (v0.2 informational); HIGH (v1.x scheduled-task-driven, `OPERATIONAL_DRIFT` admin-risk-ledger kind — per RT-10 closure raised from MED to HIGH; missed cadence is a silent-drift exploit surface that must fail-closed at v1.x rollout).

**v0.2 vs v1.x posture.** This gate is the only F-ARCHIVIST-* gate whose enforcement posture differs between v0.2 and v1.x. The other four (CROSS-ORG-LEAK, LESSON-INSTANCE-LEAK, AUTO-APPLY-ATTEMPTED, READ-WITHOUT-VAULT-INTENT) are fail-closed at v0.2 (skeleton stubs raise NotImplementedError and the Cedar/Python realization at §4 v2.x is fail-closed) AND at v1.x. F-ARCHIVIST-CADENCE-DRIFT is informational at v0.2 because there's no scheduled cadence to drift from (operator decides when); at v1.x the scheduled cadence makes drift a meaningful signal worth fail-closing.

**v1.x severity-binding requirement (per RT-10 closure).** At the v1.x amendment LOCK, `F-ARCHIVIST-CADENCE-DRIFT.severity = HIGH` and `gate.action = FAIL_CLOSED` MUST be set explicitly in the Cedar/Python predicate registration. The §4 v2.x amendment realization at v0.2 ships the skeleton with the v0.2 informational-only severity; the v1.x amendment must explicitly toggle these attributes — leaving them as v0.2 defaults at v1.x rollout would silently allow missed cadences and let stale data persist. The §15.13.2 v1.x horizon test `test_f_archivist_cadence_drift_is_fail_closed_at_v1_x` parses the gate definition and asserts the `fail_closed` attribute is True; the §4 v2.x amendment LOCK ceremony at v1.x must include this test passing as a precondition.

## §15.9.5 F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT (PRE-substrate-read, NEW from RT-11 closure)

**Purpose.** Refuse Archivist substrate read when the read does not go through the appropriate Vault read intent wrapper. The Vault read intent is the SOLE layer that performs SHA3-512 hash verification + canonical-JSON signing-bytes integrity check (per v7.0.4-M1 §2 KFR canonical-JSON signing + §4 tag-mutation hash + v7.0.5 §5.6 F-FUNDER-CORPUS-INTEGRITY); bypassing it skips integrity verification and lets tampered content reach Archivist's pattern-detection LLM. Closes the silent-substrate-tampering attack path where an attacker who can write to canonical-state files directly (bypassing the existing substrate write CLIs) gets the tampered content into Archivist's outputs without any integrity flag.

**Predicate.**

1. The §4 v2.x amendment registers the AST-lint extension to R-ARCHIVIST-NO-CANONICAL-MUTATE that ALSO scans `pipeline/orchestrator/seats/archivist/**` for substrate-read patterns:
   - **Direct raw open.** `open(path, 'r')` / `open(path, 'rb')` / `pathlib.Path.read_text()` / `pathlib.Path.read_bytes()` against any path matching the canonical-substrate prefix set (`orgs/<slug>/vault/kfr/`, `vault_shared/funder_intelligence/`, `orgs/<slug>/match_database/`, `pipeline/institutional_memory/lessons.json`, `vault_shared/benchmarks/`, `orgs/<slug>/vault/grants/<grant_id>/reports/`) → fire `.raw_open_call`.
   - **Generic helper import.** Any `import` / `from ... import` of generic file-read utility (`yaml.safe_load(open(...))` directly without going through Vault read intent; `read_yaml(...)` from outside the Archivist allowlist; `requests.get(...)` against any URL — Archivist is always-local per §15.10 so HTTP fetch is forbidden regardless) → fire `.generic_helper_import`.
2. **Runtime PRE-gate.** Every substrate read attempt by Archivist MUST go through one of the appropriate Vault read intent wrappers:
   - `vault_read_intent_kfr(org_slug=...)` — reads `orgs/<slug>/vault/kfr/register.yaml` + verifies KFR canonical-JSON signing per v7.0.4-M1 §2.
   - `vault_read_intent_funder_intel()` — reads `vault_shared/funder_intelligence/register.yaml` + per-doc + verifies F-FUNDER-CORPUS-INTEGRITY per v7.0.5 §5.6.
   - `vault_read_intent_match_db(org_slug=...)` — reads `orgs/<slug>/match_database/register.yaml` + verifies F-MATCH-DB-CROSS-ORG per v7.0.5 §5.1.
   - `vault_read_intent_lessons()` — reads `pipeline/institutional_memory/lessons.json` + verifies operator-signature integrity.
   - `vault_read_intent_benchmarks()` — reads `vault_shared/benchmarks/register.yaml` + verifies F-BENCHMARK-CONTAINS-PER-ORG-REF per v7.0.4-M1 §5 constant-time + audit-log discipline.
   - `vault_read_intent_archivist_state(run_id=...)` — reads `pipeline/institutional_memory/archivist_state/<run_id>.yaml` (Tilth-internal artifact; lighter integrity discipline because Archivist owns the write path).
3. **Vault read intent signature integrity (per RT-11 closure + Cycle 2 NF-01 runtime-tampering closure).** Each Vault read intent wrapper itself MUST verify its own implementation has not been tampered (the wrapper is part of the Golden Image; tampering with the wrapper bytes would let an attacker insert a no-op verification). The startup self-check verifies the wrapper modules' SHA3-512 against a Golden-Image-pinned manifest; mismatch → fire sub-tag `.vault_intent_signature_invalid`. **Runtime-immutability self-check (per NF-01 closure — HIGH).** At every substrate read call, the runtime guard captures the function `id(...)` of the resolved Vault read intent wrapper AND compares against the snapshot taken at module import time. Re-binding attempts (e.g., `pipeline.vault.read_intents.vault_read_intent_kfr = malicious_fn` monkey-patching at runtime) cause the function id to differ from the snapshot → fire sub-tag `.vault_intent_runtime_tampering`; refuse the read. Closes the wrapper-tampering-after-import attack surface. The runtime guard's snapshot dict is itself sealed at import time via `types.MappingProxyType` (read-only mapping wrapper); attempts to mutate the snapshot also fire the same sub-tag. Sealed-module loading via `importlib.util.LazyLoader` with frozen-attribute discipline lands at v1.x amendment per the §4 v2.x realization.

**Sub-tags.**
- `.raw_open_call` — Archivist seat code attempted raw `open()` against canonical-substrate path (caught at AST-lint OR runtime guard layer).
- `.generic_helper_import` — Archivist imported a generic file-read utility outside the Vault-read-intent allowlist.
- `.vault_intent_signature_invalid` — Vault read intent wrapper module SHA3-512 does not match Golden-Image-pinned manifest; the wrapper itself has been tampered.
- `.vault_intent_runtime_tampering` (NEW per Cycle 2 NF-01 closure — HIGH) — Vault read intent wrapper function id at runtime does not match the import-time snapshot; monkey-patch attack detected.

**Position.** PRE-substrate-read (AST-lint at build time; runtime guard at read-call time; signature self-check at module import time). All three layers are required; removing any one creates a substrate-tampering bypass path.

**Failure path.** Refuse the read + log to admin-risk ledger at HIGH severity (`SUBSTRATE_INTEGRITY_BYPASS` ledger kind — substrate-tampering attempt, not operator-action-required) + write `archivist_state.yaml` with `cadence_completed=false, failure_reason="F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT.<sub-tag>"` + clear operator-facing error message naming the attempted read path + exit non-zero.

**Severity.** HIGH. The attempt indicates a structural substrate-integrity bypass; the consequence had it succeeded would be Archivist's pattern-detection LLM reading tampered content and producing operator-facing digests grounded in adversarially-crafted fake substrate state. Defense-in-depth at three layers matches the §15.9.3 three-layer auto-apply defense in pattern.

**Composition with v7.0.4-M1 + v7.0.5.** F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT is the *enforcement* of the existing integrity discipline on the *read path* — v7.0.4-M1 §2 + §4 + v7.0.5 §5.6 already specify the integrity-verification mechanisms; F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT prevents Archivist from bypassing those mechanisms by reading raw bytes. Same pattern as F-INTAKE-EMBEDDING-NS-MISMATCH (§11.9.8) which is the seat-side enforcement of the v7.0.5 vector-store namespace discipline.

# §15.10 Routing posture (per v7.0.7)

**Always-local. Hard-coded. Not operator-overridable at Classification Review.** Per v7.0.7 LOCKED 2026-05-10 row 180, Archivist's classification register entry is `archivist → always_local` with no operator override surface.

**Rationale.** Archivist reads classified-Confidential content by structural necessity:

- KFR canonical entries may carry Confidential-default fields (revenue figures, financial details, beneficiary counts, employee credentials) per v7.0.4 §1 schema + v7.0.7 classification register.
- Match DB narratives (`match_reasoning.narrative_summary` per v7.0.5 §2) may reference confidential client fields with default classification `shareable` and operator override available; Archivist's outcome rollup digests aggregate Match DB content and inherit the classification of the underlying entries.
- Per v7.0.5 §7 + v7.0.7 §1 routing rule: anything reading post-fill drafts (Reports archive at `orgs/<slug>/vault/grants/<grant_id>/reports/period_<n>/draft_<v>.md` per §14 Report Generator output) is local-routed structurally.
- Lessons.json may carry historical lessons whose pattern-level abstraction came from instance-level outcomes; the abstraction process itself happens locally.

No subset of Archivist's input is safely cloud-routable without per-substrate operator classification at curation time, and v0.2 + v1.x first ship have no per-substrate pre-classification UX for Archivist (operator already classified the substrate at its original ingestion time via Intake / Match DB write / Funder Intel curation).

**Local LLM call (v1.x only).** The pattern-detection LLM (Mistral 7B class per §15.8) runs locally on operator hardware. No cloud frontier model is invoked at any cadence at any v1.x first ship.

**Vector store.** Local FAISS or Chroma per §15.8 (composes against existing per-org Intake embeddings + workspace-shared Funder Intel embeddings + Match DB structured vectors per v7.0.5 §1). No cloud vector store. No third-party embedding service.

**Sealed embedding endpoint.** Per §11.10 + v7.0.4 §5 + Intake §11.9.10 (F-INTAKE-EMBEDDING-ENDPOINT-INVALID): `/etc/tilth/embedding_endpoint.yaml` validated against localhost-or-unix-socket allowlist. Archivist's tool calls inherit the same enforcement.

**Pre-tool guard on every vector-store call.** F-INTAKE-EMBEDDING-NS-MISMATCH (§11.9.8) is a PRE-tool-call gate: every Pydantic AI tool call against the local vector store is wrapped to assert the `org_slug` (and `workspace` for workspace cadences) tool arg matches the input dataclass field; mismatch fails closed. Archivist's tool calls inherit this enforcement; F-INTAKE-EMBEDDING-NS-MISMATCH applies regardless of which seat (Intake or Archivist) triggers the tool call.

**Token cost.** Bounded local. Per-cadence pattern-detection LLM call cost scales with substrate size; one Pydantic AI agent invocation per cadence; structured-output bounds the LLM to digest-entry rows. Logician gate predicates are deterministic Python; AST-lint is deterministic static analysis. No external API token cost at any point.

**v0.2 vs v1.x routing posture.** Identical at both — always-local. The v0.2 spec-only disposition does not invoke the LLM at all (operator-driven manual curation referencing the templates); v1.x activates the local LLM under the same always-local posture. There is no v0.1.x or v0.2.x posture that opens a cloud path for Archivist.

**TTY-as-attack-surface known limitation (per RT-04 + RT-12 closure cross-reference).** The TTY check on operator-review CLI invocations is bounded by the v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight) assumption set; an adversary with shell access to the operator's machine could allocate a real PTY via low-level system calls and bypass the operator-presence requirement (per §15.7 disposition). v2 multi-tenant mitigation track per v7 LOCKED Section O.5 lands hardware-token second-factor (TPM/YubiKey challenge-response). The Archivist routing posture is unaffected by the TTY-discipline disposition (always-local at v0.2 + v1.x first ship); the disposition concerns the operator-review surface, not the cadence-trigger or pattern-detection paths.

# §15.11 Pipeline placement (between-cycle, NOT in §5 track dispatch)

Per v7.0.4 §9 + v7.0.5 §6 curation-slot reservations + v7.0.6 Archivist v1.x candidate-seat naming:

```
GRANT CYCLE (per submission, eval, OR report — §5 track dispatch)
  Tracks dispatched: submission_mode → eval_mode → report_mode (per §5 v8 LOCKED 2026-05-10 row 188; v0.1 ships submission + eval; report ships v0.2)
  Inner-loop seats: Scout, Scribe, Editor, Judge, Red Team, Logician (per §3-§10 LOCKED blueprints)
  Support seats fire on cycle boundaries: Intake (§11) at SP0 KFR Freshness Review + at INCREMENTAL doc arrival; Uploader (§12) at end-of-cycle submission package assembly
  
BETWEEN CYCLES (Archivist runs HERE — never inside §5 track dispatch)
  Weekly tick (v0.2 operator-driven; v1.x scheduled): tilth archivist weekly --org <slug>
    → KFR refresh digest + Match DB lessons-delta digest + per-run state file
                                                       ↓
                                  (operator reviews via tilth archivist review at next available time)
  
  Quarterly review (v0.2 operator-driven; v1.x scheduled):
    tilth archivist quarterly --workspace
      → Funder Intel quarterly + Benchmarks freshness + lessons proposals
    tilth archivist quarterly --org <slug>
      → KFR quarterly + Match DB outcome rollup
                                                       ↓
                                  (operator reviews + per-entry confirms; mutations to canonical substrates happen via existing substrate write CLIs)
```

Archivist does NOT participate in the §5 inner revision loop. It does NOT fire on submission_mode, eval_mode, or report_mode runs. It does NOT register as a §5 track per the §5 v8 + §6 track-registry pattern (Archivist is a between-cycle seat, not a track-runnable workflow). Its triggers are: weekly cadence (v0.2 operator-explicit; v1.x scheduled), quarterly cadence (v0.2 operator-explicit; v1.x scheduled). Its writes are only to `archivist_digests/` + `lessons_proposals/` + `archivist_state/` + `archivist_rejects/` — never to canonical substrates. Operator confirmation drives the existing substrate write CLIs (`tilth kfr ...`, `tilth funder-intel ...`, `tilth match-db ...`, `tilth lessons ...`, `tilth benchmarks ...`); Archivist's role ends at producing the digest entry.

# §15.12 v0.2 vs v1.x posture summary

| Concern | v0.2 (this LOCK) | v1.x (forward-design) |
|---|---|---|
| Cadence trigger | Operator-explicit (`tilth archivist weekly` / `quarterly`) | Scheduled-task-driven (Mondays 8:30 AM cron for weekly; quarterly via 90-day cadence; per `schedule` skill) |
| Curation-slot owner | `operator` (per v7.0.4 §9 + v7.0.5 §6 v0.1+v0.2 default) | Transitions to `archivist` via operator-signed migration trigger (per v7.0.4 §9.1 J-06 closure) |
| LLM invocation | NONE (operator manually walks substrates referencing templates) | Local Mistral 7B class for pattern-detection + digest narrative |
| Module skeleton | EXISTS (this LOCK; predicates raise NotImplementedError) | Predicates implemented + LLM tool composition wired |
| Skeleton tests | PASS at v0.2 LOCK (validate proposes-only discipline at the structural level) | Extended with per-predicate behavior tests + integration tests |
| Operator-review surface | CLI for v0.2 first ship (operator manually invokes `tilth archivist review`) | Same CLI; possible UI consideration deferred to v1.x amendment |
| F-ARCHIVIST-CROSS-ORG-LEAK | Skeleton stub at v0.2; live Cedar/Python at v1.x via §4 v2.x | Live fail-closed |
| F-ARCHIVIST-LESSON-INSTANCE-LEAK | Skeleton stub at v0.2; live Cedar/Python at v1.x via §4 v2.x | Live fail-closed |
| F-ARCHIVIST-AUTO-APPLY-ATTEMPTED | AST-lint live at v0.2 (R-ARCHIVIST-NO-CANONICAL-MUTATE rule registered + enforced); runtime dispatcher + Cedar live at v1.x via §4 v2.x | All three layers live |
| F-ARCHIVIST-CADENCE-DRIFT | Informational-only at v0.2 (no scheduled cadence to drift from) | Fail-closed PRE-gate (per §15.9.4) |
| Routing posture | Always-local hard-coded | Same |
| Sub-curation cadences (e.g., per-funder, per-benchmark category) | NOT scoped at v0.2 | v1.x candidate (sub-cadence breakdown to land in v1.x amendment) |

The v0.2 SPEC LOCK is a SPEC LOCK, not an implementation LOCK. The skeleton tests + the AST-lint rule + the digest templates are the v0.2 deliverables; the live LLM + the live cadence + the live substrate-mutation-via-operator-confirm flow lands at v1.x.

# §15.13 Test matrix

Tests live at `tests/seats/archivist/`. Each test is a deterministic unit test — no LLM calls (Archivist's LLM is mocked in unit tests at v1.x; v0.2 has no LLM to mock), no network calls (enforced by `test_archivist_zero_network_egress`), no cross-org reads.

## §15.13.1 Skeleton tests (v0.2 LOCK ceremony — NON-NEGOTIABLE)

The skeleton tests are NON-NEGOTIABLE per the dispatch packet's explicit statement: "Skeleton tests are non-negotiable — they prevent any future contributor from quietly turning the stub into auto-apply behavior." Skeleton tests at v0.2 LOCK validate the structural discipline at the type-system + import-graph + AST-lint level; they do NOT test predicate behavior (predicates raise NotImplementedError at v0.2 by design).

- `test_two_cadences_register_in_dispatcher`: introspect the cadence dispatcher; assert exactly two cadences registered (`weekly` + `quarterly`); assert no third cadence silently leaked through type-checker holes; assert `quarterly` further routes to `quarterly_workspace` OR `quarterly_per_org` per the §15.4.2 split.
- `test_v1_gate_codes_resolve_to_predicates`: assert all 5 gate predicate stubs are importable + callable: `f_archivist_cross_org_leak`, `f_archivist_lesson_instance_leak`, `f_archivist_auto_apply_attempted`, `f_archivist_cadence_drift`, `f_archivist_read_without_vault_intent` (NEW from RT-11 closure).
- `test_gate_predicates_raise_not_implemented_at_v0_2`: invoke each predicate stub; assert `NotImplementedError` is raised with a "§15.9.<N> predicate scaffold" message naming the §15 LOCK as the spec authority and the §4 v2.x amendment as the realization layer.
- `test_archivist_proposes_only_no_canonical_write_intent_calls`: scan `pipeline/orchestrator/seats/archivist/**` source files (AST traversal); assert NO calls to `kfr_write_intent`, `funder_intel_write_intent`, `match_db_write_intent`, `lessons_json_write_intent`, `benchmarks_write_intent`, `tilth kfr promote` subprocess, etc. This is the AST-lint rule R-ARCHIVIST-NO-CANONICAL-MUTATE realized as a pytest assertion at v0.2 (the §4 v2.x amendment promotes this to a proper AST-lint rule at v1.x; the v0.2 pytest version is the bridge).
- `test_archivist_no_subprocess_canonical_cli` (NEW per RT-01 closure): scan source for `subprocess.*` / `os.system` / `os.popen` / `os.exec*` / `os.spawn*` / `pexpect.*` invocations; assert NONE contain literal token `tilth` or canonical-write sub-commands (`kfr` / `funder-intel` / `match-db` / `lessons` / `benchmarks`) anywhere in argument list, including f-strings + str.format() + str.join.
- `test_archivist_no_foreign_file_write_helper_imports` (NEW per RT-02 closure): scan source for imports; assert any imported module exposing file-write API (`atomic_write`, `write_file`, `safe_write`, etc.) is from the explicit Archivist write-intent allowlist (`pipeline.vault.write_intents.archivist_*`).
- `test_archivist_proposes_only_write_paths_only_to_allowed_prefixes`: scan `pipeline/orchestrator/seats/archivist/**` source files; assert any `open(..., 'w')` / `open(..., 'a')` / `pathlib.Path.write_text` calls (or their Pydantic AI tool wrappers) target only the allowed prefixes (`orgs/<slug>/archivist_digests/`, `vault_shared/archivist_digests/`, `pipeline/institutional_memory/lessons_proposals/`, `pipeline/institutional_memory/archivist_state/`, `pipeline/validation/archivist_rejects/`, `pipeline/validation/archivist_review_rejects/`). Mismatch → test fail (signals a future contributor introduced a forbidden write path; CI catches this before the change merges).
- `test_archivist_no_raw_open_on_canonical_substrate` (NEW per RT-11 closure): scan source for `open(...)` / `pathlib.Path.read_text()` / `pathlib.Path.read_bytes()` calls against any canonical-substrate path (`orgs/<slug>/vault/kfr/`, `vault_shared/funder_intelligence/`, etc.); assert ZERO matches. All canonical-substrate reads MUST go through Vault read intent wrappers per F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT.
- `test_archivist_yaml_safe_load_only` (NEW per RT-09 closure): scan source for `yaml.load(...)` calls; assert ZERO matches. Only `yaml.safe_load` is permitted. Scan extends to `pipeline/orchestrator/seats/archivist/**` AND to any operator-review CLI module that consumes Archivist digest files.
- `test_archivist_input_bundles_frozen_kw_only`: assert `ArchivistWeeklyInput`, `ArchivistQuarterlyWorkspaceInput`, `ArchivistQuarterlyPerOrgInput` are frozen + kw_only dataclasses per Tilth convention.
- `test_archivist_digest_schemas_frozen_kw_only`: assert `KfrRefreshDigestEntry`, `MatchDbLessonsDeltaEntry`, `FunderIntelQuarterlyEntry`, `BenchmarksFreshnessEntry`, `LessonsProposalEntry` (or whatever names the skeleton uses) are frozen + kw_only.
- `test_archivist_state_frozen_kw_only`: assert `ArchivistState` is frozen + kw_only per Rule 1.
- `test_gate_result_pass_factory` + `test_gate_result_fail_factory`: assert `GateResult.PASS()` returns `passed=True`; `GateResult.FAIL(code=..., sub_tag=..., detail=...)` returns `passed=False` with fields populated. Mirrors §11 Intake skeleton test pattern.
- `test_archivist_zero_network_egress`: full Archivist process invocation inside sandbox with all network egress blocked; assert run completes (or fails with NotImplementedError at v0.2 per the predicate stubs raising) with zero outbound connections — no phone-home, no cloud LLM, no third-party tool call.

## §15.13.2 v1.x horizon tests (NOT registered at v0.2)

The following tests land at §15 v1.x amendment alongside the corresponding feature additions:

- `test_f_archivist_cross_org_leak_pre_substrate_read_path`: per-org cadence with `kfr_register_path` resolving outside `orgs/<org_slug>/`; assert F-ARCHIVIST-CROSS-ORG-LEAK fires sub-tag `.path_outside_org`.
- `test_f_archivist_cross_org_leak_post_workspace_digest_per_org_content`: workspace cadence emits a digest entry containing per-org content (specific KFR fact text); assert F-ARCHIVIST-CROSS-ORG-LEAK fires sub-tag `.workspace_digest_per_org_content`.
- `test_f_archivist_lesson_instance_leak_client_name_in_proposal`: proposed-lesson with literal client name from `orgs/ORG_INDEX.md`; assert F-ARCHIVIST-LESSON-INSTANCE-LEAK fires sub-tag `.client_name_present`.
- `test_f_archivist_auto_apply_attempted_runtime_dispatcher`: Archivist code path attempts `kfr_write_intent(...)`; assert runtime dispatcher catches and fires F-ARCHIVIST-AUTO-APPLY-ATTEMPTED sub-tag `.runtime_dispatcher_violation`.
- `test_f_archivist_cadence_drift_weekly_14_days`: simulate weekly tick run after 15 days; assert F-ARCHIVIST-CADENCE-DRIFT fires sub-tag `.weekly_drift` at v1.x posture (informational at v0.2).
- `test_f_archivist_cadence_drift_is_fail_closed_at_v1_x` (NEW per RT-10 closure): parse F-ARCHIVIST-CADENCE-DRIFT gate definition at v1.x; assert `gate.severity == "HIGH"` AND `gate.action == "FAIL_CLOSED"`. Closes the silent-drift exploit path where v1.x amendment forgets to toggle the v0.2 informational defaults.
- `test_f_archivist_read_without_vault_intent_raw_open` (NEW per RT-11 closure): simulate Archivist seat code attempting `open("orgs/test/vault/kfr/register.yaml", "r")` (raw open against canonical-substrate path); assert F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT fires sub-tag `.raw_open_call`.
- `test_f_archivist_read_vault_intent_signature_invalid` (NEW per RT-11 closure): simulate tampered `vault_read_intent_kfr` module bytes (modify after Golden Image install); assert startup self-check fires sub-tag `.vault_intent_signature_invalid`; refuse Archivist initialization.
- `test_f_archivist_lesson_instance_leak_unicode_homoglyph` (NEW per RT-07 closure): proposed_lesson_text uses Cyrillic 'а' (U+0430) in client name; assert F-ARCHIVIST-LESSON-INSTANCE-LEAK fires sub-tag `.unicode_homoglyph` after NFKC normalization reveals the Latin equivalent.
- `test_f_archivist_lesson_instance_leak_ner_paraphrase` (NEW per RT-07 closure): proposed_lesson_text uses paraphrased reference ("the third client in our org index"); assert F-ARCHIVIST-LESSON-INSTANCE-LEAK fires sub-tag `.ner_entity_match` (NER detects the entity reference even though regex misses).
- `test_f_archivist_cross_org_leak_aggregate_insufficient_orgs` (NEW per RT-06 closure): workspace contains 2 orgs (below default N=3 threshold); workspace digest generation attempts to emit "100% of clients have stale KFR" entry; assert F-ARCHIVIST-CROSS-ORG-LEAK fires sub-tag `.aggregate_insufficient_orgs`; assert per-org-derived statistics suppressed; assert insufficient-orgs notice emitted.
- `test_f_archivist_auto_apply_subprocess_canonical_cli` (NEW per RT-01 closure): Archivist seat code attempts `subprocess.run(["tilth", "kfr", "mark-stale", "--fact-id", fid])`; assert F-ARCHIVIST-AUTO-APPLY-ATTEMPTED fires sub-tag `.subprocess_canonical_cli_invocation` at the AST-lint layer (build time) AND at the runtime guard layer (run time).
- `test_f_archivist_auto_apply_principal_spoofing` (NEW per RT-03 closure): set `CEDAR_PRINCIPAL=operator` env var; invoke Archivist; assert seat startup self-asserts principal as `archivist_seat` from signed token; Cedar policy denies any canonical write intent attempt; sub-tag `.principal_spoofing_detected` fires.
- `test_archivist_confirmation_id_replay_rejected` (NEW per RT-05 closure): operator confirms digest entry A with confirmation_id X; attacker captures the signed payload and replays against digest entry B; assert ledger lookup detects replay; reject the replayed payload with explicit "confirmation_id already used" error.
- `test_archivist_weekly_tick_end_to_end_seeded_org`: seeded test org with KFR + Match DB + lessons.json fixtures; invoke weekly tick; assert digests produced with expected entries; operator-confirm path mocked drives existing substrate write CLI; full round-trip operator review.
- `test_archivist_quarterly_workspace_end_to_end`: seeded workspace fixtures; invoke quarterly workspace cadence; assert Funder Intel quarterly + Benchmarks + lessons proposals digests produced.
- `test_archivist_quarterly_per_org_end_to_end`: seeded per-org fixtures; invoke quarterly per-org cadence; assert KFR quarterly + Match DB outcome rollup digests produced.
- `test_archivist_local_llm_pattern_detection`: mock the local LLM extraction step; assert Archivist invokes the LLM with the bounded pattern-detection prompt + structured-output schema; assert no cloud LLM invocation observed.

# §15.14 Open questions resolved and deferred

## §15.14.1 Resolved at v0.2

- **OQ-15-IMPLEMENTATION-DEGREE (per dispatch packet decision 8d).** RESOLVED at v0.2 with default per dispatch packet: spec-only at v0.2; implementation deferred to v1.x; operator-driven cadence in the interim. Per `v0_2_implementation_disposition` frontmatter + §15.1 + §15.12 posture summary.
- **OQ-15-SLOT-OWNER-TRANSITION (per v7.0.4 §9 + v7.0.5 §6).** RESOLVED at v0.2 with default per architecture: slot-owner field stays `operator` at v0.1 + v0.2; transitions to `archivist` at v1.x via operator-signed migration trigger per v7.0.4 §9.1 J-06 closure. §15 does not bake `curated_by: operator` permanently — it codifies the slot transition discipline at the seat-spec level.
- **OQ-15-EDITOR-BOUNDARY (per memory `project_archivist_v1x_candidate_seat.md`).** RESOLVED at v0.2 with default per memory: Editor stays Editor (clarity-during-drafting in §5 inner loop); Archivist stays Archivist (curation-between-cycles in outer loop). Sharp boundary preserved at §15.1.
- **OQ-15-LOGICIAN-BOUNDARY.** RESOLVED at v0.2: Logician enforces F-ARCHIVIST-* gates against Archivist's outputs PRE/POST; Logician does NOT perform curation on Archivist's behalf. Per §15.1 + §15.9.
- **OQ-15-LESSONS-JSON-APPEND-AUTHORITY (per `project_archivist_v1x_candidate_seat.md`).** RESOLVED at v0.2: operator-confirmed entries promote from `lessons_proposals/<run_id>.yaml` to `lessons.json` via existing `tilth lessons promote` CLI; Archivist drafts the proposal queue but does not mutate `lessons.json`. Per §15.5.2 + §15.7.
- **OQ-15-CROSS-CYCLE-MEMORY-MODEL (per `project_archivist_v1x_candidate_seat.md`).** PARTIALLY RESOLVED at v0.2: Archivist composes against existing Match DB + Funder Intel DB + Intake embeddings substrates; does NOT introduce a new substrate. Pattern detection at v1.x runs against the existing local vector store. Whether Archivist needs a graph database or expanded vector store for cross-cycle pattern detection is **deferred to v1.x amendment** when implementation evidence is in hand. Per §15.8 + §15.14.2.

## §15.14.2 Open questions for next-round attention

- **OQ-ARCHIVIST-CADENCE-WIRING (v1.x scope).** v0.2 is operator-driven cadence; v1.x activates the scheduled-task wiring via the existing `schedule` skill (Mondays 8:30 AM cron precedent from `project_monday_fund_routine.md`). Sub-questions: per-org weekly tick is per-org-watcher OR workspace-level scheduler with per-org dispatch loop? Quarterly cadence calendar-aligned (calendar quarters / fiscal-year quarters) or invocation-anchored (90 days from prior run)? Each requires a §15 v1.x amendment registering the schedule binding + the per-org/workspace dispatch wiring.
- **OQ-ARCHIVIST-PATTERN-DETECTION-PROMPT (v1.x scope).** v0.2 spec pins the digest schemas; v1.x amendment authors the LLM extraction prompt template for pattern detection. Operator-tunable per-org? Operator-tunable per-funder? Workspace-level only? Likely workspace-level + Sovereign Node LLC ships prompt template versions per quarterly review of pattern-detection effectiveness.
- **OQ-ARCHIVIST-CROSS-CYCLE-SUBSTRATE (v1.x evidence-driven).** Per OQ-15-CROSS-CYCLE-MEMORY-MODEL deferral. If v1.x first ship reveals that pattern detection across cycles requires a graph database or expanded vector store beyond the current local substrate envelope, that lands as a §15 v1.x amendment + an ADR amendment (per ADR-001 substrate-freeze discipline).
- **OQ-ARCHIVIST-FUNDER-INTEL-CURATION-CADENCE.** v7.0.5 §6 binds Funder Intel quarterly curation to the Archivist v1.x slot. v0.2 spec defaults to 90-day quarterly cadence (`freshness_threshold_days: 90`); operator may want to tune per-funder (some funders publish updates monthly, others annually). v1.x candidate: per-funder freshness threshold in `vault_shared/funder_intelligence/curation_config.yaml`.
- **OQ-ARCHIVIST-BENCHMARKS-FRESHNESS-SCHEMA.** v0.2 spec lists the proposed `archivist_benchmarks_freshness.v1` schema shape (per §15.5.2) but defers full schema detail to v1.x amendment. The Benchmarks Register itself (per v7.0.4 §7) is the authoritative substrate; Archivist's freshness digest defers to whatever schema the Benchmarks Register canonical form specifies at the time of v1.x.
- **OQ-ARCHIVIST-V1X-EXTRACTION-LLM-VERSIONING.** v1.x extraction LLM is Mistral 7B class per §15.8 substrate envelope. Future v1.x candidate: per-deployment LLM selection (some deployments may benefit from a domain-specific model). Defer until evidence of need from white-glove deployments.

# §15.15 Companion edits at LOCK

The following edits land in the same commit as §15 v1 LOCK (compound paired-commit per §6.17 Option-B):

1. **§0.5 §15 amendment** — `pipeline/blueprint/v0.1/section_00_5_section_15_archivist_amendment.md` — final inventory **14 rows at v1 post-Cycle-1 closures** (per the explode-pattern §10 / §11 / §12 precedent applied to F-ARCHIVIST-* failure-codes; +2 rows from RT-11 closure adding F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT failure-code + matching pre-gate-check):
   - 1 marker row (kind=`marker`): `blueprint.section_anchor.s15_archivist.v1`
   - 3 schema rows for input bundles: `archivist.weekly_input.v1`, `archivist.quarterly_workspace_input.v1`, `archivist.quarterly_per_org_input.v1`
   - 4 schema rows for digest schemas: `archivist.kfr_refresh_digest.v1`, `archivist.match_db_lessons_delta.v1`, `archivist.funder_intel_quarterly.v1`, `archivist.lessons_proposal.v1`
   - 5 failure-code rows (kind=`failure-code`): `archivist.failure_code.F-ARCHIVIST-CROSS-ORG-LEAK.v1`, `archivist.failure_code.F-ARCHIVIST-LESSON-INSTANCE-LEAK.v1`, `archivist.failure_code.F-ARCHIVIST-AUTO-APPLY-ATTEMPTED.v1`, `archivist.failure_code.F-ARCHIVIST-CADENCE-DRIFT.v1`, `archivist.failure_code.F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT.v1` (NEW per RT-11 closure)
   - 1 pre-gate-check row (kind=`pre-gate-check`): `archivist.pre_gate.proposes_only_three_layer.v1` (consolidates F-ARCHIVIST-AUTO-APPLY-ATTEMPTED + F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT — both share the AST-lint + runtime + Cedar three-layer pattern per §4 v2.2 consolidated-check pattern)

   **§0.5 row range note.** §15 LOCKs after §11 (rows 233-256), §12 (rows 212-232), §2 v7.2 (rows 257-278), and §5 v8 (rows 279-290). §15 amendment claims rows **291-304** (14 rows) at this LOCK. New runtime-live total: 290 + 14 = 304. (14-row count = 1 marker + 3 input-schema + 4 digest-schema + 5 failure-code + 1 pre-gate-check; if v1.x lands additional pre-gate-check / post-gate-check consolidation rows for the per-substrate Vault read intents, those land at the v1.x amendment's own row range.)

2. **§4 Logician v2.x amendment (WS-L)** — registers F-ARCHIVIST-CROSS-ORG-LEAK (with `.aggregate_insufficient_orgs` per RT-06) + F-ARCHIVIST-LESSON-INSTANCE-LEAK (with NER + Unicode NFKC discipline per RT-07) + F-ARCHIVIST-AUTO-APPLY-ATTEMPTED (with subprocess-canonical-CLI + foreign-file-write-helper-import + principal-spoofing extensions per RT-01/02/03) + F-ARCHIVIST-CADENCE-DRIFT (with v1.x severity-binding requirement per RT-10) + F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT (NEW per RT-11) at the Logician PRE/POST sequence + AST-lint rule R-ARCHIVIST-NO-CANONICAL-MUTATE extended for subprocess + foreign-helper-import + raw-canonical-substrate-read + yaml.load detection (Code session is authoring this in parallel; this blueprint is the authority on the gate codes + sub-tags + proposes-only semantics). Per the v0.2 spec-only disposition, the Cedar/Python predicate bodies are skeleton at v0.2 and become live at v1.x; the AST-lint rule R-ARCHIVIST-NO-CANONICAL-MUTATE is live at v0.2 (catches forbidden write-intent calls + subprocess + foreign-helper-import + raw-canonical-substrate-read + yaml.load in Archivist seat code at compile time).

3. **`orgs/_TEMPLATE/archivist_digests/` scaffold** — template directory for new client orgs:
   - `orgs/_TEMPLATE/archivist_digests/.gitkeep` (empty directory marker)
   - `orgs/_TEMPLATE/archivist_digests/kfr_refresh_template.yaml` (operator reference: per-row layout for v0.2 manual KFR refresh digest production; mirrors §15.5.0 schema delta + §15.5.1 output)
   - `orgs/_TEMPLATE/archivist_digests/match_db_lessons_delta_template.yaml` (operator reference: per-row layout for v0.2 manual Match DB lessons-delta digest production)
   - `orgs/_TEMPLATE/archivist_digests/kfr_quarterly_template.yaml` (operator reference: quarterly per-org KFR refresh digest layout)
   - `orgs/_TEMPLATE/archivist_digests/match_db_outcome_rollup_template.yaml` (operator reference: quarterly per-org Match DB outcome rollup layout)

4. **`vault_shared/archivist_digests/` scaffold** — workspace-level digest templates:
   - `vault_shared/archivist_digests/.gitkeep`
   - `vault_shared/archivist_digests/funder_intel_quarterly_template.yaml` (operator reference: workspace-level Funder Intel quarterly curation digest layout)
   - `vault_shared/archivist_digests/benchmarks_freshness_template.yaml` (operator reference: workspace-level Benchmarks Register freshness digest layout)

5. **`pipeline/institutional_memory/lessons_proposals/.gitkeep`** — new subdirectory for Archivist-proposed lessons.json patches; per-run YAML files land here at v1.x; operator promotes via `tilth lessons promote --proposal <run_id>` (CLI authored at v1.x; v0.2 operator manually applies).

6. **`pipeline/institutional_memory/archivist_state/.gitkeep`** — new subdirectory for Archivist per-run state files per Rule 1.

7. **Module skeleton** — `pipeline/orchestrator/seats/archivist/__init__.py`:
   - Frozen kw_only Pydantic dataclasses for `ArchivistWeeklyInput`, `ArchivistQuarterlyWorkspaceInput`, `ArchivistQuarterlyPerOrgInput`, `ArchivistState`, the four digest entry schemas, `GateResult`.
   - Cadence dispatcher with two cadences registered (`weekly`, `quarterly`); `quarterly` further routes to `quarterly_workspace` OR `quarterly_per_org` per the §15.4.2 split.
   - `f_archivist_cross_org_leak`, `f_archivist_lesson_instance_leak`, `f_archivist_auto_apply_attempted`, `f_archivist_cadence_drift` predicate stubs raising NotImplementedError with `§15.9.<N> predicate scaffold; v1.x amendment realizes` message.
   - Module-level docstring naming this as v0.2 SPEC LOCK (proposes-only; v1.x implementation deferred per v0.2 disposition); operator-driven cadence in v0.2 interim.
   - Module passes AST-lint clean (no `requests.post`, no `httpx`, no `socket`, no raw `subprocess` to non-allow-list targets, AND no canonical-substrate write-intent calls per R-ARCHIVIST-NO-CANONICAL-MUTATE).

8. **Test suite** — `tests/seats/archivist/skeleton_tests.py` per §15.13.1 — at LOCK ceremony, the skeleton tests validate the proposes-only structural discipline + the two cadences register in the dispatcher + the v1 gate codes resolve to imported predicate stubs + the AST-lint-equivalent pytest assertion catches forbidden write-intent calls. **Skeleton tests are non-negotiable per dispatch packet** — they are the structural defense against future contributors silently turning the stub into auto-apply behavior.

9. **Memory file** — `memory/project_blueprint_section_15_archivist_v1_locked.md` — written at LOCK ceremony per the standard memory pattern.

10. **MEMORY.md prepend** — index entry for the §15 LOCK.

11. **lock_history row** — appended to `pipeline/engineering/lock_history.v1.jsonl` with `lock_class=blueprint`, `module=pipeline.blueprint.v0_1.section_15_archivist`, `parent_lock_row=178` (v7.0.4 LOCK reserves the slot at §9) + `parent_lock_row_secondary=179` (v7.0.5 LOCK binds Funder Intel + Match DB curation to the slot at §6), `unblocks=["v1.x Archivist implementation amendment (slot transition + LLM wiring + scheduled-task cadences)", "WS-L §4 Logician v2.x (registers F-ARCHIVIST-* gate family + R-ARCHIVIST-NO-CANONICAL-MUTATE AST-lint)", "v0.2 production cut readiness checklist §15 SPEC LOCK box"]`.

12. **daily_log entry** — `daily_logs/2026-05-10.md` — per the standard daily_log pattern (LOCK ceremony summary + companion edits + unblocks).

# §15.16 What §15 v1 explicitly does NOT do

- Does NOT write canonical KFR / Funder Intel DB / Match DB / lessons.json / Benchmarks Register entries (per F-ARCHIVIST-AUTO-APPLY-ATTEMPTED).
- Does NOT register as a §5 track per the §5 v8 + §6 track-registry pattern (Archivist runs OUTSIDE §5 dispatch).
- Does NOT collapse with Editor (Editor stays inner-loop clarity review; Archivist stays outer-loop curation).
- Does NOT collapse with Logician (Logician enforces F-ARCHIVIST-* gates; Archivist produces digests subject to those gates).
- Does NOT introduce a new substrate (composes against existing KFR + Funder Intel DB + Match DB + lessons.json + Benchmarks Register substrates per v7.0.4 + v7.0.5).
- Does NOT introduce a new vector store (composes against existing local FAISS / Chroma per §11.10 + §15.10).
- Does NOT introduce a new embedding endpoint (composes against the sealed Golden-Image-baked endpoint per §11.10 + §15.10).
- Does NOT cross orgs in any operator-facing surface (per F-ARCHIVIST-CROSS-ORG-LEAK; workspace-aggregate carve-out for aggregate statistics only).
- Does NOT propose instance-level lessons (per F-ARCHIVIST-LESSON-INSTANCE-LEAK).
- Does NOT silently revise the cadence (per F-ARCHIVIST-CADENCE-DRIFT).
- Does NOT modify A1-A12 architectural lock.
- Does NOT modify the Five Operating Laws or the Four Autonomy Rules.
- Does NOT modify the v7.0.3 substrate decision (Pydantic AI substrate stands; FAISS/Chroma + bge-large-en-v1.5 + Mistral 7B class + per-substrate read intent wrappers align).
- Does NOT modify v7.0.4 KFR schema or fact validity model (KFR is the read-substrate; Archivist proposes refresh actions against KFR's existing schema without modifying it).
- Does NOT modify v7.0.5 Funder Intel DB or Match DB schemas (Archivist proposes curation actions against the existing schemas without modifying them; the `curated_by` slot-owner field per v7.0.5 §6 is the v1.x transition surface).
- Does NOT modify v7.0.7 classification register or routing pattern (Archivist routing posture is always-local hard-coded per §15.10; integrates with v7.0.7 routing rule via the always-local entry).
- Does NOT modify v7.0.8 CIC × CLC orthogonality discipline (Archivist schemas + prompt templates audit clean against the four detection layers at LOCK).
- Does NOT specify v1.x operator-cadence-vs-Archivist-scheduled-cadence transition mechanics beyond reserving the discipline at §15.12; v1.x amendment lands the transition CLI.
- Does NOT specify v1.x extraction LLM prompt template (per §15.14.2 OQ deferred).
- Does NOT specify cross-Tilth lessons sharing (Stage-5 R.6 Telemetry Commons; F-ARCHIVIST-LESSON-INSTANCE-LEAK is the upstream preparation but cross-Tilth wiring is out-of-scope-for-v0.2).
- Does NOT specify pricing-tier implications of Archivist functionality (biz-plan amendment territory; v1.x rollout when implementation horizon is closer).
- Does NOT introduce new operator key types (per E-04 closure — Archivist uses the existing operator Ed25519 key type per v7.0.4 §1 + §11.7 + §12 conventions; no new key class invented).
- Does NOT introduce new vault subtree topology beyond the four allowed digest-prefix paths (per E-04 closure — `orgs/<slug>/archivist_digests/`, `vault_shared/archivist_digests/`, `pipeline/institutional_memory/lessons_proposals/`, `pipeline/institutional_memory/archivist_state/`, `pipeline/validation/archivist_rejects/`, `pipeline/validation/archivist_review_rejects/` are the only Archivist write surfaces; no new vault subtree introduced beyond these).
- Does NOT modify the §6 track-registry schema (per E-04 closure — Archivist explicitly does NOT register as a track; the §5 v8 track-registry pattern is unaffected by §15).
- Does NOT introduce new admin-risk severity classes beyond `LAW3_VIOLATION` (CROSS-ORG-LEAK), `LAW3_PATTERN_VS_INSTANCE` (LESSON-INSTANCE-LEAK), `SEAT_BOUNDARY_VIOLATION` (AUTO-APPLY-ATTEMPTED), `OPERATIONAL_DRIFT` (CADENCE-DRIFT), `SUBSTRATE_INTEGRITY_BYPASS` (READ-WITHOUT-VAULT-INTENT) (per E-04 closure — five admin-risk-ledger kinds total across the F-ARCHIVIST-* family; no new severity class invented).
- Does NOT introduce a new local LLM substrate at v0.2 (no LLM invocation per the spec-only disposition); v1.x reuses the Mistral 7B class envelope per §15.8 + §11.8 + ADR-001.
- Does NOT introduce a hardware-token requirement at v0.2 + v1.x first ship (per RT-04 + RT-12 disposition — bounded by v7 LOCKED A1+A4; v2 multi-tenant amendment lands hardware-token via Section O.5).

# §15.17 Lock-history note + sequencing

- v0.2 SPEC DRAFT 2026-05-10 (this file): §15 Archivist seat-lifecycle wrapper + 4 owned Logician gate codes + 12 §0.5 primitive rows. SPEC LOCK target.
- Forward-pending:
  - §15 v1.x amendment (operator-cadence-vs-Archivist-scheduled-cadence transition + LLM wiring + per-cadence prompt templates + per-funder freshness threshold + per-org watcher + Cedar policy realization for fail-closed gates). Composes against v7.0.4 + v7.0.5 + v7.0.6 LOCKs (slot reservations + bindings already in place).

**Sequencing.** §15 v1 LOCK depends on:
- v7.0.4 LOCK (slot reservation at §9) — DONE 2026-05-09 row 178 + cross-family-verified row 181 + M1 LOCK row 190.
- v7.0.5 LOCK (slot binding at §6) — DONE 2026-05-10 row 179.
- v7.0.6 LOCK (Archivist named v1.x candidate seat) — DONE 2026-05-09 row 176 + verified row 177.
- v7.0.7 LOCK (always-local routing posture for Archivist) — DONE 2026-05-10 row 180.
- §2 v7.2 LOCK (operational sub-kinds Archivist reads at quarterly per-org cadence) — DONE 2026-05-10 row 186.
- §5 v8 LOCK (track-registry that Archivist EXPLICITLY does NOT register into) — DONE 2026-05-10 row 188.
- §11 v1 LOCK (Intake produces operator-confirmed KFR; Archivist proposes refreshes against Intake-produced KFR) — DONE 2026-05-10 row 185.
- §12 v1 LOCK (Uploader analogous proposes-and-stages discipline) — DONE 2026-05-10 row 182.

All prerequisites satisfied at §15 v1 LOCK time. Next-step downstream consumer: WS-L §4 Logician v2.x amendment (registers the F-ARCHIVIST-* gate family + R-ARCHIVIST-NO-CANONICAL-MUTATE AST-lint).

**Thesis-round priorities for §15 v1 LOCK:**

- Editor pass: clarity of v0.2 vs v1.x posture distinction; operator usability of digest templates for v0.2 manual cadence; cross-amendment composition map readability.
- Judge pass: rubric scoring against the architecture's stated goal (Archivist curates between cycles without auto-applying any change); does F-ARCHIVIST-AUTO-APPLY-ATTEMPTED structurally prevent canonical mutation? does the seat-boundary discipline with Editor + Logician hold under load?
- Red Team pass: adversarial — can Archivist's outputs leak per-org content into a workspace digest? can a proposed-lesson smuggle instance-level details past the pattern-vs-instance check? can a code path bypass the AST-lint + runtime-dispatcher + Cedar three-layer auto-apply defense? can cadence drift be silently masked? can Archivist read non-operator-confirmed substrates (pending_facts.yaml, PENDING proposal_commitments.yaml) to extract content?

The Red Team pass on §15 is critical because Archivist's failure modes are silent canonical corruption (the highest-severity class of substrate damage) and per-org content leakage across the workspace surface (Law 3 violation). Both paths are covered by the four owned gates with the three-layer auto-apply defense; Red Team verifies the layers are not removable and the gate predicates close all enumerated attack surfaces.

# §15.18 External-Review Disposition (post-LOCK audit-trail footer; not a content edit)

Filed 2026-05-10 as audit-trail pointer; LOCK row 191 stands historical. Packet at `pipeline/planning/section_15_external_review_disposition_2026-05-10.md` routes 7 Tilth Cycle-1 Red Team external-review findings dispatched via openclaw bridge against the §15 v1 SCOPING DRAFT pre-LOCK. Synthesis against this LOCKED text yields: 4 FOLDED IN at LOCK (Tilth-RT-01 / 03 / 05 / 06 — covered by existing §15.9.3 + §15.9.2 + §15.10 + §15.13.2 LOCKED text plus Cycle-1 + Cycle-2 closures); 3 routed to correct downstream consumers without reopening this LOCK (Tilth-RT-02 PARTIAL → §15 v1.x amendment for Layer 3 NER on workspace-aggregate digest fields; Tilth-RT-04 NEW → v2 multi-tenant amendment per Section O.5 for hard-link/bind-mount inode-integrity; Tilth-RT-07 PARTIAL → §4 v2.x.1 corrective-amendment backlog for `R-ARCHIVIST-NO-CANONICAL-MUTATE` AST-lint extension covering low-level rename primitives — adjusted from packet-stated WS-L routing because §4 v2.x LOCKed earlier same day rows 193/194). Disposition is row-170 transparent — bounded by v7 A1+A4 in v0.1+v0.2; structural fixes route to their natural downstream LOCK ceremonies. Disposition row appended to `pipeline/engineering/lock_history.v1.jsonl` row 195. Mirrors the v7.0.4 cross-family-verification footer pattern (row 181 disposition on row 178 LOCK).

# End of §15 v1 SCOPING DRAFT
