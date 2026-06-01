---
title: §15 Archivist v1 — Tilth external-review three-finding disposition packet
filed: 2026-05-10
operator: Josh
parent_locks:
  - pipeline/blueprint/v0.1/section_15_archivist.md  # §15 v1 SPEC LOCKED 2026-05-10 (compound-LOCK rows 191/192)
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md  # §0.5 v13 amendment (14 rows; range 291–304; runtime-live total 304)
parent_planning:
  - pipeline/planning/v0_2_dispatch_plan_2026-05-09.md  # WS-L is the next downstream consumer
  - pipeline/planning/v0_1_beta_readiness_2026-05-10.md
external_review_source: Tilth Cycle-1 Red Team output dispatched via `mcp__Control_your_Mac__osascript` → openclaw gateway against §15 v1 SCOPING DRAFT (pre-LOCK), 2026-05-10. Reviewer-family identity not pinned in operator-supplied output; treat as cross-family per the operator's intent ("Tilth gave this report through openclaw").
authority: Josh 2026-05-10 ("write that dispatch packet now").
status: DISPOSITIONED 2026-05-10 — lock_history row 195 (lock_class=`external_review_disposition`; verdict=`DISPOSITIONED`; parent_lock_row=192) + memory file at `.auto-memory/project_section_15_external_review_disposition_2026-05-10.md` + L-020 ERDP-PO discipline lesson appended to `pipeline/institutional_memory/lessons.json`. Two §3 NOW-actions adjusted after authoring: (1) #4 WS-L handoff update became a post-LOCK note + §4 v2.x.1 backlog packet because WS-L LOCKed 2026-05-10T20:45:00Z (rows 193/194) before disposition could ride; (2) #6 lessons.json entry filed as L-020 not L-020 because L-020 was already taken (reviewer-line-citation discipline, 2026-05-04). Tilth-RT-07 implementation has advanced beyond the packet — predicate body + acceptance test + §4 v2.x.1 SCOPING DRAFT all landed same day; awaits Cowork Thesis dispatch.
purpose: Route the seven Tilth-RT external-review findings against §15 v1 LOCKED text. Four FOLDED IN at LOCK (no further action). Three real gaps (one HIGH, one MED, one LOW) require routing — none reopens the §15 v1 LOCK. Disposition path is the row-170 transparent pattern matching v7.0.4-M1 + Cycle-2 §15 fold-ins: bound v0.1+v0.2 by v7 A1+A4, route the structural fix to its correct downstream consumer (WS-L §4 Logician v2.x for Tilth-RT-07; §15 v1.x amendment for Tilth-RT-02-indirect; v2 Section O.5 for Tilth-RT-04).
---

# 1. Why this packet exists

After §15 v1 SPEC LOCK 2026-05-10 (compound-LOCK rows 191/192), Josh dispatched a fresh Cycle-1 Red Team review through Tilth via the openclaw bridge, scoped to the §15 v1 SCOPING DRAFT. The review surfaced seven findings (Tilth-RT-01..07). Synthesis disposition against the LOCKED text — including the Cycle-1 + Cycle-2 closures already absorbed at LOCK — produced this routing map:

| Tilth-RT# | Severity | Disposition | Routing destination |
|---|---|---|---|
| RT-01 | HIGH/P0 | **FOLDED IN at LOCK** | none — closed by §15.9.3 sub-tags + Cedar `process_create` DENY + NF-05 v7-A1+A4 boundary |
| RT-02 | HIGH | **PARTIAL — literal slug folded in; indirect-reference subset open** | §15 v1.x amendment (when LLM-stage activates) |
| RT-03 | MED | **FOLDED IN at LOCK** with v7 A4 boundary | none — closed by NFKC + NER + regex three-layer + NF-04 disposition |
| RT-04 | MED | **NEW gap, bounded by v7 A1+A4 in v0.1+v0.2** | v2 multi-tenant amendment per Section O.5 |
| RT-05 | LOW | **FOLDED IN at LOCK** with v7 A1+A4 boundary | none — closed by Cycle-1 RT-04+12 closure |
| RT-06 | LOW | **FOLDED IN at LOCK** | none — closed by `test_f_archivist_cadence_drift_is_fail_closed_at_v1_x` |
| RT-07 | LOW | **PARTIAL — open-shim covers `open()`/`Path.write_*`; low-level rename primitives open** | WS-L §4 Logician v2.x (R-ARCHIVIST-NO-CANONICAL-MUTATE AST-lint enumeration extension) |

Full mapping evidence with file/line citations is appendixed at §6.

This packet does NOT reopen the §15 v1 LOCK. The dispositions ride into existing downstream consumers. No §15 v1.0.1 corrective amendment is required (the gaps are downstream-realization-shaped, not architecture-shaped — distinct from v7.0.4-M1 which surfaced architectural-layer gaps).

# 2. Disposition routes

## 2.1 Route 1 — FOLD INTO WS-L §4 Logician v2.x amendment

**Finding:** Tilth-RT-07 PARTIAL — the runtime open-shim in §15.9.3 wraps `open()` + `Path.write_text` + `Path.write_bytes`, and the AST-lint test `test_archivist_no_subprocess_canonical_cli` (§15.13.1 line 694) scans for subprocess + `os.system` + `os.popen` + `os.exec*` + `os.spawn*` + `pexpect.*` invocations. Neither layer enumerates **low-level rename primitives** that are commonly used as canonical-write atomic-tail operations: `os.replace`, `os.rename`, `shutil.move`, `shutil.copy*`, `os.link`. A contributor (or a model-authored module) could perform a canonical-substrate write by writing to a temp path inside an allowed prefix and then `os.replace`-ing the temp path over a forbidden canonical path — neither layer fires.

**Severity at LOCK:** LOW (v7 A4 operator-trusted boundary covers v0.1+v0.2 single-operator threat model; this is contributor-discipline + AST-lint enumeration, not an exploitable adversarial path under A1).

**Routing destination:** WS-L §4 Logician v2.x amendment per `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §WS-L. The §15 v1 SPEC LOCK names the AST-lint rule `R-ARCHIVIST-NO-CANONICAL-MUTATE`; WS-L is the round that writes its predicate body. This is the cleanest place — the rule lives at §4, not §15.

**Specific edits to land at WS-L:**

1. **Extend `R-ARCHIVIST-NO-CANONICAL-MUTATE` AST-lint enumeration.** The §4 v2.x amendment text describing the rule must explicitly enumerate low-level rename primitives in the forbidden-call list:
   ```
   Forbidden direct-call patterns (additions per Tilth-RT-07 disposition):
     - os.replace(...)              → sub-tag .low_level_rename_replace
     - os.rename(...)               → sub-tag .low_level_rename_rename
     - shutil.move(...)             → sub-tag .low_level_rename_shutil_move
     - shutil.copy(...) / .copy2() / .copyfile() / .copytree()
                                    → sub-tag .low_level_rename_shutil_copy
     - os.link(...) / os.symlink(...)
                                    → sub-tag .low_level_rename_os_link
   ```
   These join the existing `subprocess` + `os.system` + `os.popen` + `os.exec*` + `os.spawn*` + `pexpect.*` enumeration in the §15.9.3 R-ARCHIVIST-NO-CANONICAL-MUTATE preflight.

2. **Add acceptance test** at WS-L:
   ```python
   def test_r_archivist_no_canonical_mutate_enumerates_low_level_rename_primitives():
       """Tilth-RT-07 PARTIAL closure: verify R-ARCHIVIST-NO-CANONICAL-MUTATE
       fires .low_level_rename_* sub-tags on each enumerated primitive."""
       for primitive, expected_sub_tag in [
           ("os.replace(tmp, '/vault_shared/funder_intelligence/register.yaml')",
            ".low_level_rename_replace"),
           ("os.rename(tmp, 'orgs/clientA/vault/kfr/register.yaml')",
            ".low_level_rename_rename"),
           ("shutil.move(tmp, 'orgs/clientA/vault/kfr/register.yaml')",
            ".low_level_rename_shutil_move"),
           ("shutil.copy(tmp, 'orgs/clientA/vault/kfr/register.yaml')",
            ".low_level_rename_shutil_copy"),
           ("os.link(canonical_path, tmp)",
            ".low_level_rename_os_link"),
       ]:
           result = ast_lint_archivist_seat_source(make_module_with(primitive))
           assert result.fired is True
           assert expected_sub_tag in result.sub_tags
           assert result.failure_code == "F-ARCHIVIST-AUTO-APPLY-ATTEMPTED"
   ```

3. **Runtime guard extension (defense-in-depth, non-load-bearing at v0.2 SPEC-ONLY).** When the runtime guard layer is realized at v1.x per §15.9.3 line 521, also wrap `os.replace` / `os.rename` / `shutil.move` with the same allowed-prefix-set check that the open-shim already applies. Document in the WS-L amendment that the runtime guard's wrapper set MUST mirror the AST-lint forbidden-call set.

**Why this routes to WS-L, not §15 v1.0.1:** The AST-lint rule is registered at §4, not §15. §15 v1 names the rule by reference; the rule definition lives in `R-ARCHIVIST-NO-CANONICAL-MUTATE` at the §4 v2.x predicate body. The author of WS-L is already pinning the AST-lint enumeration extension per memory line 26 ("extended R-ARCHIVIST-NO-CANONICAL-MUTATE AST-lint per RT-01/02/11 + Cycle 2 NF-01/02/05 closures"). This packet adds Tilth-RT-07 to that pin.

**WS-L handoff prompt addendum:** When WS-L opens, append the following to its handoff prompt in `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §WS-L:
```
Read pipeline/planning/section_15_external_review_disposition_2026-05-10.md §2.1 — the
R-ARCHIVIST-NO-CANONICAL-MUTATE AST-lint enumeration extension MUST include the five
low-level-rename-primitive sub-tags (.low_level_rename_replace, .low_level_rename_rename,
.low_level_rename_shutil_move, .low_level_rename_shutil_copy, .low_level_rename_os_link)
per Tilth-RT-07 PARTIAL disposition. Acceptance test
test_r_archivist_no_canonical_mutate_enumerates_low_level_rename_primitives must land
green before LOCK.
```

**TIMING-ADJUSTED ROUTING (2026-05-10).** This addendum could NOT ride the WS-L LOCK ceremony because WS-L §4 v2.x LOCKed at 2026-05-10T20:45:00Z (compound-LOCK rows 193/194) BEFORE this packet was authored and operator-approved. Disposition coordinator filed the §2.1 addendum text as the seed for a **§4 v2.x.1 corrective amendment** (narrow-corrective pattern mirroring v7.0.4-M1 row 190 precedent), with the backlog packet at `pipeline/planning/section_04_v2_x_1_tilth_rt_07_backlog_2026-05-10.md` and a brief post-LOCK note in `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §WS-L pointing to the backlog file.

**As-shipped (2026-05-10):** A Cowork code-phase session ran from the §4 v2.x.1 backlog packet and landed:
- **Predicate body:** `pipeline/linting/r_archivist_no_canonical_mutate.py` (~190 LOC) — `FORBIDDEN_PRIMITIVES` table maps 9 concrete `(module, attr)` call shapes to the 5 sub-tags. Resolves both `ast.Attribute(value=ast.Name('os'), attr='replace')` and `ast.Name('replace')` bound via `from os import replace`. `reason_tag` carries `archivist_auto_apply_attempted.<sub_tag>` (leading-dot preserved); diagnostic message body carries `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` for failure-code attribution.
- **Acceptance test:** `tests/linting/test_r_archivist_no_canonical_mutate.py` (~340 LOC; 11 test functions; 20 parametrized rows). Realizes the §3.2 stub against the real `lint_tree` API (the disposition-packet stub's `ast_lint_archivist_seat_source` / `make_module_with` helpers were notional; the actual test adapts to `lint_tree` + a `_write` fixture per `tests/linting/test_ast_lint.py` convention). Covers: §3.2 five-primitive parametrized acceptance + shutil.copy-family fan-out (4 primitives → 1 sub-tag) + os.link-family fan-out (2 primitives → 1 sub-tag) + module-import-alias resolution (`import os as o`) + from-import resolution (`from os import replace`) + from-import-with-asname resolution (`from shutil import move as m`) + scope discipline (modules outside `seats/archivist/` do not fire) + clean-module assertion + multi-primitive emission (5 forbidden calls → 5 distinct sub-tags) + FORBIDDEN_PRIMITIVES table introspection (5 sub-tags + 9 call shapes) + live-tree regression guard against the shipping Archivist seat package.
- **§4 v2.x.1 SCOPING DRAFT:** `pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md` (~190 lines + Appendix A). Mirrors the v7.0.4-M1 narrow-corrective-amendment frontmatter pattern (`amendment_status: SCOPING DRAFT`; `cowork_thesis_dispatch_status: NOT YET DISPATCHED`; `parent_lock_row=193`; `predecessor_disposition_packet=section_04_v2_x_1_tilth_rt_07_backlog_2026-05-10.md` row 195). Awaits Cowork Thesis dispatch + L-005 two-cycle + LOCK ceremony. Daily log at `daily_logs/2026-05-10.md` lines 540–547.

**Acceptance criterion (closes Tilth-RT-07):** §4 v2.x.1 LOCK ceremony asserts the five sub-tags above are registered in `R-ARCHIVIST-NO-CANONICAL-MUTATE` predicate body AND the acceptance test is green AND the §4 v2.x.1 amendment text enumerates them explicitly. Status as of 2026-05-10: predicate body LANDED + acceptance test LANDED + SCOPING DRAFT LANDED + tests-green VERIFIED + AST-lint clean VERIFIED. Awaits Thesis dispatch + LOCK.

## 2.2 Route 2 — DEFER to §15 v1.x amendment (LLM-stage activation)

**Finding:** Tilth-RT-02 indirect-reference subset — §15.9.1 POST-gate per Cycle-1 RT-06 closure scans `source_substrate_path` + `rationale` + `pattern_summary` for **literal** org_slug strings from `orgs/ORG_INDEX.md` (§15.9.1 line 459). Indirect references that don't include any literal slug — "the [ORG_NAME] client", "the client listed third in ORG_INDEX.md", "the nonprofit with $5M annual budget" — are NOT detected. The three-layer NER detection (NFKC + NER + regex) at §15.9.2 fires on `proposed_lesson_text` for the lesson-instance gate, not on workspace-aggregate digest fields for the cross-org-leak gate.

**Severity at LOCK:** MED but **not yet exploitable**. Archivist is SPEC-ONLY at v0.2 per dispatch packet decision 8d default; the LLM-generated digest narrative does not exist at v0.1+v0.2. The operator produces digests manually by walking substrates referencing the §15 templates. An operator producing a manual digest with an indirect reference to one of their own clients is bounded by v7 A4 (operator-trusted, applicant-brings-substance under Law 5). The threat model only activates at v1.x first ship when the LLM stage starts authoring digest content.

**Routing destination:** §15 v1.x amendment, opened per v7.0.4 §9.1 J-06 closure (operator-signed migration trigger required for slot-owner transition from `operator` → `archivist`). The v1.x amendment hasn't been authored yet — it's queued for post-v0.2.

**Specific text to land in v1.x amendment acceptance criteria:**

```
v1.x acceptance criterion (Tilth-RT-02 indirect-reference closure):

The §15.9.1 F-ARCHIVIST-CROSS-ORG-LEAK POST-gate MUST be extended at v1.x first ship
to apply NER detection to digest fields `rationale` AND `pattern_summary` (in addition
to the existing literal-slug regex from Cycle-1 RT-06 closure):

  Layer 1 (existing v1): NFKC normalization of digest field text.
  Layer 2 (existing v1): literal org_slug regex from orgs/ORG_INDEX.md.
  Layer 3 (NEW v1.x):    NER extraction of any entity matching the workspace's
                         org/funder/client identifier set; sub-tag
                         .indirect_org_reference fires if the entity resolves to
                         a known per-org identifier through any path
                         (positional descriptor, template variable, paraphrase,
                         numeric clue, etc.).

The Layer 3 NER model is the same `xx-ent-wiki-sm`-class local model used at
§15.9.2 for the lesson-instance gate. NF-04 NER adversarial-robustness boundary
(per v7 A4) carries forward to this gate too — Layer 3 is best-effort within
operator-trusted threat model; Layer 2 literal-slug regex remains the structural
guarantee.

Acceptance test:
  test_f_archivist_cross_org_leak_indirect_reference_in_rationale (NEW per
  Tilth-RT-02 v1.x closure): workspace-aggregate digest entry rationale field
  contains "the third client in ORG_INDEX.md"; assert F-ARCHIVIST-CROSS-ORG-LEAK
  fires sub-tag .indirect_org_reference; literal-slug regex would have missed.

Acceptance test:
  test_f_archivist_cross_org_leak_template_variable_evasion (NEW per Tilth-RT-02
  v1.x closure): workspace-aggregate digest entry pattern_summary contains
  "the [ORG_NAME] client lost three cycles in a row"; assert
  F-ARCHIVIST-CROSS-ORG-LEAK fires sub-tag .indirect_org_reference (NER detects
  template-variable scaffolding as candidate-entity-marker).
```

**Why this routes to v1.x, not WS-L:** The threat surface (LLM-authored digest narrative) does not exist until v1.x first ship. The Layer 3 NER gate-extension reuses the §15.9.2 NER infrastructure; that infrastructure is realized when the slot-owner transitions from `operator` to `archivist` — i.e., at v1.x. Closing this gap at v0.2 would be premature realization (mirrors the v7.0.4 §9 / J-06 slot-transition discipline).

**Acceptance criterion (closes Tilth-RT-02 PARTIAL):** §15 v1.x amendment LOCK ceremony asserts the Layer 3 NER extension is registered in F-ARCHIVIST-CROSS-ORG-LEAK predicate body AND the two acceptance tests above are green.

**Interim posture (v0.1+v0.2):** No structural gate. Bounded by v7 A4 + Law 5 (applicant brings substance). Operator producing manual digests reads §15.7 operator-review surface every cycle; per-entry display shows `proposed_action` / `source_substrate_path` / `source_entry_id` / `rationale` side-by-side. Operator-eyes-on at confirmation-time is the v0.2 mitigation.

## 2.3 Route 3 — DEFER to v2 multi-tenant amendment per Section O.5

**Finding:** Tilth-RT-04 (NEW — surfaced in neither Cycle-1 nor Cycle-2) — `Path.resolve()` invariant in §15.4.1 + §15.4.2 input contracts ensures the resolved path is under the declared subtree but does NOT check `os.lstat().st_nlink > 1`, does NOT enforce `nosymfollow` / `nodev` mount options, does NOT scan for bind-mounts inside `orgs/` or `vault_shared/`. Threat model: an attacker with filesystem write access to an org subtree creates `orgs/clientA/vault/kfr/evil_link.yaml` as a hard-link or bind-mount targeting `vault_shared/funder_intelligence/secret.yaml`. `Path.resolve()` sees a file inside the per-org subtree and passes the gate; the read returns workspace-shared content. Law 3 isolation bypassed at the inode layer.

**Severity at LOCK:** MED in absolute terms; **bounded by v7 LOCKED A1 (single-client) + A4 (operator-trusted) at v0.1+v0.2** — the threat model assumes a non-operator filesystem-write party who lacks vault read but can write within an org subtree. In v0.1 Beta single-operator deployment, the operator has full filesystem access; there is no second party. The attacker has no foothold under A1.

**Routing destination:** v2 multi-tenant amendment per Section O.5 (the architecture's `tilth_architecture_locked.md` "Section O.5" v2-hardening targets section, NOT the numeric §0.5 Interface Index). Mirrors the disposition pattern for NF-05 (FFI execve bypass), Cycle-1 RT-04+12 (hardware-token), and §2 v7.2 RT-C1-01..04 raw-FS-write probes — all bounded by A1+A4 in v0.1, all routed to Section O.5 for v2 multi-tenant work.

**Specific text to add to Section O.5 (next-letter target):**

```
O.5.<next-letter> — Inode-integrity defense against hard-link / bind-mount
                    cross-org leakage on per-org Path.resolve()

(v2 multi-tenant hardening target; not required at v0.1 per A1+A4; surfaced
by Tilth-RT-04 external review 2026-05-10 against §15 Archivist v1 SPEC LOCK.
Disposition routed via pipeline/planning/section_15_external_review_disposition_2026-05-10.md
§2.3.)

Threat model (v2-only): mutually-adversarial multi-tenant deployment where
client A has filesystem write access to its own per-org subtree but not to
workspace-shared vaults. Client A creates a hard-link or bind-mount inside
orgs/<client-A>/vault/kfr/ that targets a file in vault_shared/. Path.resolve()
returns a path under orgs/<client-A>/, passing the per-org input contract.
The subsequent read returns workspace-shared content, bypassing Law 3.

Required v2 hardening (NOT required at v0.1+v0.2 per A1+A4):

1. Mount discipline: mount orgs/ and vault_shared/ with nosymfollow + nodev
   + noexec where the kernel supports it; reject any path resolution where
   a path component is a bind-mount source.

2. Inode check: every per-org input contract that resolves a path under
   orgs/<slug>/ MUST also call os.lstat() and reject if st_nlink > 1
   (multi-link inode = candidate hard-link to outside subtree).

3. Audit-trail: attempted hard-link / bind-mount detection logs at HIGH severity
   to admin-risk ledger as SUBSTRATE_INTEGRITY_BYPASS (mirrors §15.9.5
   F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT failure-path discipline).

Cross-references: Tilth-RT-04 disposition; v0.2 production cut readiness
checklist in pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §6 already
gates v0.2 cut on A1+A4 single-client posture; v2 amendment opens the
multi-tenant threat model as a new architectural round.
```

**Why this routes to Section O.5, not §15 v1.0.1:** The fix is not §15-specific. Every per-org input contract across the Tilth substrate (KFR + Funder Intel + Match DB + lessons + Benchmarks + every future v0.2 sub-kind from §2 v7.2) shares the same `Path.resolve()` pattern. Closing it at §15 alone would leave the same gap at every other read site. Section O.5 is the right architectural layer because it's where v2 multi-tenant hardening targets aggregate. See §2.3.1 immediately below for the cross-section blast-radius sweep.

**Acceptance criterion (closes Tilth-RT-04):** v2 multi-tenant amendment LOCK includes O.5.<next-letter> entry above + at least three acceptance tests covering the three v2 hardening mechanisms (mount discipline / inode check / audit-trail discipline) + the cross-section binding from §2.3.1.

**Interim posture (v0.1+v0.2):** No structural gate. Bounded by v7 A1+A4. Document this disposition in §15 v1's audit trail (this packet) so that future-rounds don't re-flag it as a new finding.

## 2.3.1 Cross-section blast-radius sweep for Tilth-RT-04

The hard-link / bind-mount inode attack is not a §15-local property. Every Tilth read site that resolves a path under a per-org or workspace-shared subtree using `Path.resolve()` *without* an inode-link check shares the same gap. If Section O.5.<next-letter> protects only the §15 site, every other site remains exposed at v2; if it protects the pattern, all sites get the mitigation in one mechanism.

**Candidate sites (preliminary enumeration — needs operator-confirmed sweep before v2 amendment opens):**

| Section | LOCK state | Read substrate | Path.resolve() use | Inode check today? |
|---|---|---|---|---|
| §2 v7.2 | LOCKED row 186 | 7 operational-data sub-kinds (metrics, financials, photos, narrative_entries, timeline, beneficiary_records, attachments) | Every per-org write/read intent uses path-prefix invariant | No — same `Path.resolve()` discipline as §15 |
| §9 KFR (v7.0.4 + M1) | LOCKED rows 178/181/190 | `orgs/<slug>/vault/kfr/register.yaml` | Read intent enforces path-prefix; canonical-JSON signing per M1 | No — signing covers content tampering, not inode redirection |
| §11 Intake v1 | LOCKED row 185 | BULK_INGEST file readers + INCREMENTAL + AWARD_INGEST | TOCTOU-hardened watcher per RT-04 closure; per-org subtree confined | No — TOCTOU covers race; not link-redirection |
| v7.0.5 §1 Funder Intel DB | LOCKED row 179 | `vault_shared/funder_intelligence/register.yaml` + per-doc | Workspace-shared scope; `vault_shared/` prefix invariant | No |
| v7.0.5 §2 Match DB | LOCKED row 179 | `orgs/<slug>/match_database/register.yaml` | Per-org subtree | No |
| Benchmarks Register (v7.0.4 §7) | LOCKED rows 178/190 | `vault_shared/benchmarks/register.yaml` | Workspace-shared | No — M1 added constant-time + audit-log; not inode-link |
| `lessons.json` (institutional_memory) | Existing convention | `pipeline/institutional_memory/lessons.json` | Workspace-shared; operator-signature integrity | No |
| §13 Data Collector v0.2 | NOT YET LOCKED (WS-I queued) | Inbound/outbound channel substrate per §2 sub-kinds | TBD at WS-I author time | TBD — sweep applies prospectively |
| §14 Report Generator v0.2 | NOT YET LOCKED (WS-J queued) | KFR + operational data + proposal_commitments + report drafts | TBD at WS-J author time | TBD — sweep applies prospectively |
| §15 Archivist v1 | LOCKED rows 191/192 | All five substrates above (read-only) | Per-substrate Vault read intent + Path.resolve() | No — Tilth-RT-04 finding |

**Recommended sweep:**

1. **Pre-v2 audit (one session, Cowork or Code).** Walk each LOCKED section above. For each per-org and workspace-shared read site, classify: (a) does the site call `os.lstat()` and check `st_nlink > 1`? (b) does the site rely on mount-option discipline (`nosymfollow` / `nodev`)? (c) does the site rely on Path.resolve() alone? Log results in `pipeline/validation/section_o5_inode_sweep_<date>/findings.md`.

2. **Verdict expected:** every site falls into class (c) — Path.resolve() alone — because the inode-link attack vector wasn't part of the LOCKED threat model under v7 A1+A4. The sweep is confirmation, not investigation.

3. **Section O.5.<next-letter> binding extension.** Rewrite the O.5 entry text from §2.3 to bind explicitly across the enumerated sites. Replace the §15-scoped framing with: "Every per-org and workspace-shared read site enumerated in `pipeline/planning/section_15_external_review_disposition_2026-05-10.md` §2.3.1 MUST adopt the v2 hardening (mount discipline + inode check + audit-trail discipline). Single shared mitigation; not N point-fixes."

4. **Prospective binding for §13/§14.** When WS-I (Data Collector) and WS-J (Report Generator) blueprint rounds open, the §2.3.1 sweep entry rides into their handoff prompts as a v2 acceptance criterion. The sites added at v0.2 inherit the pattern automatically.

**Why the sweep happens BEFORE v2 amendment opens, not at v2 amendment author-time:**

If the sweep waits, the v2 amendment author has to enumerate sites themselves and may miss some (especially v0.2 sites added between this packet and v2 author-time). If the sweep happens now, the enumeration is frozen at the §2.3.1 table (with prospective rows for §13/§14), the v2 amendment cites this packet by path, and the operator-driven sweep documents the pre-v2 reality. The session cost is ~30 minutes (no LOCK ceremony — just an audit walk).

**Acceptance criterion (closes the cross-section binding):** Section O.5.<next-letter> at v2 amendment LOCK references this packet's §2.3.1 site enumeration and binds the v2 hardening across all enumerated sites — not only §15. Sweep findings file exists at `pipeline/validation/section_o5_inode_sweep_<date>/findings.md`.

**This is a NOW-action only insofar as the sweep wants to happen before v2 amendment opens.** It does not block v0.2 production cut. It does not block WS-L. It does not block any v0.1+v0.2 LOCK. It is a v2-readiness pre-stage.

# 3. NOW-actions (before WS-L opens)

These actions land before WS-L opens, regardless of WS-L scheduling:

1. **Append disposition row to lock_history.v1.jsonl.** Use `lock_class="external_review_disposition"`, `parent_lock_row=192` (the §15 v1 SPEC LOCK row), `verdict="DISPOSITIONED"`. Mirror the row-181 cross-family-verification pattern from v7.0.4. The row references this packet path. (Operator-driven; not auto-applied.)

2. **Memory file.** Write `memory/project_section_15_external_review_disposition_2026-05-10.md` summarizing the seven findings + four FOLDED IN + three routed dispositions. Prepend a one-line entry to `MEMORY.md` (under-150-char hook). This packet's disposition becomes part of the workspace's institutional memory; future external reviews shouldn't re-surface findings already routed.

3. **Update §15 v1 LOCKED text audit trail.** Append a "External-Review Disposition" footer paragraph to `pipeline/blueprint/v0.1/section_15_archivist.md` (NOT a content edit to the LOCK; just the audit-trail footer that points to this packet). Match the pattern from v7.0.4 cross-family-verification footer.

4. **Update WS-L handoff prompt.** Append the addendum from §2.1 above to `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §WS-L handoff prompt. Operator-driven; not auto-applied.

5. **Daily log entry.** Append disposition to `daily_logs/2026-05-10.md` with the three routing decisions and the four FOLDED IN findings.

6. **Append lesson to `pipeline/institutional_memory/lessons.json`.** [LANDED 2026-05-10 as **L-020**, NOT L-020 — L-020 already taken by 2026-05-04 reviewer-line-citation discipline.] First time a post-LOCK external review has surfaced real gaps that L-005 two-cycle PASS missed (Tilth-RT-04 NEW + Tilth-RT-07 PARTIAL). The lesson — names the discipline, names the routing rule, names the no-LOCK-reopen default. Skeleton (filed shape — use L-020 not L-020):
   ```json
   {
     "id": "L-020",
     "title": "Post-LOCK external review can surface real gaps even after L-005 two-cycle PASS with FULL cross-family rigor",
     "filed": "2026-05-10",
     "filed_by_session": "<this session id>",
     "frequency": 1,
     "severity": "MED",
     "rule": "When an external review (Tilth-via-openclaw, partner audit, or operator-driven fresh-eyes pass) surfaces findings against a LOCKED section, route via row-170 transparent-disposition pattern: bound interim posture under v7 A1+A4, route the structural fix to its correct downstream consumer (next blueprint round / next architectural amendment / Section O.5 v2-hardening). Do NOT reopen the LOCK unless the gap is architectural-layer (v7.0.4-M1 precedent: 5 HIGH/P0 architectural-layer findings warranted a corrective amendment). Downstream-realization gaps ride into next consumer; architectural-layer gaps ride into a corrective amendment.",
     "evidence": [
       "pipeline/planning/section_15_external_review_disposition_2026-05-10.md (this packet)",
       "pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md (architectural-layer corrective precedent, lock_history row 190)",
       "pipeline/blueprint/v0.1/section_15_archivist.md (downstream-realization disposition precedent, lock_history rows 191/192)"
     ],
     "applies_to": ["all v0.1 + v0.2 + v1.x sections post-LOCK"],
     "first_observed": "2026-05-10 §15 Archivist v1 LOCK + same-day Tilth Cycle-1 external review",
     "discipline_name": "ERDP-PO (external-review disposition packet, post-LOCK opportunistic) — see §10 of evidence packet"
   }
   ```
   Frequency increases on subsequent ERDP-PO packets. If the pattern recurs (e.g., at §13 / §14 / v1.x amendment LOCK ceremonies), the lesson's frequency + severity weight grows; at frequency≥3 and MED+ severity it would graduate to a mandatory pre-LOCK check ("verify there is no pending external review before declaring LOCK").

   **As-shipped (2026-05-10):** L-020 landed in lessons.json with the actual ID, expanded `sibling_to` cross-references (L-006 / L-017 / L-018), explicit `evidence` array (5 paths), `applies_to` scope, `graduation_threshold` field, and origin paragraph naming the §4 v2.x WS-L timing pre-emption that forced the corrective-amendment-backlog fallback path. `last_updated` field of lessons.json updated to "2026-05-10 (L-020 appended — ERDP-PO discipline naming from §15 external-review disposition)".

7. **Recursive-self-review meta-note in memory file.** When writing `memory/project_section_15_external_review_disposition_2026-05-10.md` per NOW-action #2, include a one-paragraph footer naming the recursive sovereignty pattern observed: *Tilth — the agentic software running on Golden Quill — reviewed the §15 spec for its own Archivist seat via the openclaw bridge. This is the council reviewing its own substrate. The Sovereign Node arc points at exactly this kind of recursive sovereignty — the system surfaces gaps in its own design and routes them through its own LOCK discipline. Not load-bearing for this packet; worth a note because it's a small piece of evidence the architecture is doing what the architecture says it should do.* This is a one-paragraph addition, not a new memory file.

The four FOLDED IN findings (Tilth-RT-01, RT-03, RT-05, RT-06) require no further action — they're closed by existing §15 v1 LOCKED text. The audit trail footer (action 3 above) names them so future reviewers see they were considered and resolved. Live test-verification evidence at §6.8 below confirms the AST-lint subset of the FOLDED IN closures runs green on current main.

# 4. Acceptance criteria summary

| Disposition | Closes when | Evidence path |
|---|---|---|
| Tilth-RT-01, 03, 05, 06 | §15 v1 LOCKED text already covers — no further action; AST-lint subset live-verified at §6.8 | `pipeline/blueprint/v0.1/section_15_archivist.md` §15.9.3 + §15.9.2 + §15.10 + §15.13.2 + §6.8 below |
| Tilth-RT-07 PARTIAL | WS-L LOCK with 5 sub-tags + new acceptance test green | `pipeline/blueprint/v0.1/section_04_v2_x_consolidated_amendment.md` (when authored) |
| Tilth-RT-02 PARTIAL | §15 v1.x amendment LOCK with Layer 3 NER + 2 acceptance tests | `pipeline/blueprint/v0.1/section_15_archivist_v1_x_amendment.md` (when authored) |
| Tilth-RT-04 NEW (single-site) | v2 multi-tenant amendment LOCK with O.5.<letter> + 3 acceptance tests | `pipeline/architecture/v0.1/architecture_v2_multi_tenant_amendment.md` (when authored) |
| Tilth-RT-04 NEW (cross-section binding per §2.3.1) | Pre-v2 inode sweep findings file exists + Section O.5.<letter> at v2 LOCK references §2.3.1 site enumeration + every enumerated site adopts the v2 hardening | `pipeline/validation/section_o5_inode_sweep_<date>/findings.md` + v2 amendment LOCK ceremony |
| L-020 lessons.json append (this packet's discipline) | `lessons.json` contains entry per §3 NOW-action #6 with ERDP-PO discipline naming | `pipeline/institutional_memory/lessons.json` |

# 5. Why no §15 v1.0.1 corrective amendment

v7.0.4-M1 (lock_history row 190) was the precedent for "narrow corrective amendment" — but the M1 conditions are different in kind:

- v7.0.4-M1 surfaced 5 HIGH/P0 + 2 RECOMMENDED + 4 OPTIONAL paths through cross-family verification of the LOCKED text. The findings were architectural-layer (KFR canonicalization, AST whitelist enumeration, atomic-read fcntl.flock, Decimal mandate). A corrective amendment was the right shape because the architecture itself had gaps.

- This packet's findings are downstream-realization-shaped. Tilth-RT-07 lives at §4 Logician predicate-body realization, not at the §15 SPEC. Tilth-RT-02-indirect lives at the v1.x LLM-stage realization, not at the v0.2 SPEC. Tilth-RT-04 lives at v2 multi-tenant architectural extension, not at the §15 per-org input contract.

A §15 v1.0.1 corrective amendment would either:
(a) reopen §15 to add text that belongs at §4 / v1.x / v2 (architectural-layer-confusion); or
(b) redundantly state the dispositions already documented in this packet (process noise without LOCK consequence).

The row-170 transparent-disposition pattern is the correct primitive: surface the gap, route it to its correct downstream consumer, document the bounded interim posture under v7 A1+A4, close the loop at the consumer's LOCK ceremony.

# 6. Appendix — full mapping evidence per finding

Citations are line/§ from `pipeline/blueprint/v0.1/section_15_archivist.md` (§15 v1 LOCKED) + `pipeline/validation/blueprint_section_15_archivist_2026-05-10/audit_v{1,2}_red_team.md` (Cycle-1 + Cycle-2 audits) + memory file `memory/project_blueprint_section_15_archivist_v1_locked.md`.

## 6.1 Tilth-RT-01 (HIGH/P0) — Dynamic subprocess + indirect importlib + os.replace + signed-CLI bypass

**Three sub-attacks bundled in the finding:**

(a) `importlib.import_module(...)` indirect call to `kfr_write_intent` →
**FOLDED IN** at LOCK via Cycle-2 RT-02 PARTIAL closure: §15.9.3 sub-tag `.dynamic_import_forbidden` (memory line 16, blueprint §15.9.3 line 535). AST-lint forbids any `importlib.import_module(...)` or `__import__(...)` call in `pipeline/orchestrator/seats/archivist/**`.

(b) `os.replace(tmp_file, "/vault_shared/...")` →
**FOLDED IN partially** at LOCK via Cycle-1 RT-02 closure (runtime open-shim wraps `open()`/`Path.write_text`/`.write_bytes`, audit_v1_red_team.md RT-02 closure column). `os.replace` itself NOT explicitly enumerated — see Tilth-RT-07 disposition for the gap.

(c) Subprocess invokes `tilth kfr mark-stale --signed-by operator --signature <sig>` via forged operator key →
**FOLDED IN structurally**: §15.9.3 line 521 — "Cedar policy adds explicit DENY of the `process_create` capability for the Archivist principal; closes the policy-level path to subprocess invocation regardless of runtime-shim state." Forged-operator-signature premise rejected: LOCKED §15 does not assume operator private keys are readable by the archivist process — `archivist` runtime has read-access only to its own signed token at `/etc/tilth/seat_identity/archivist.signed.yaml` per Cycle-1 RT-03 closure.

ctypes/execve through FFI = NF-05 from Cycle-2 audit, FOLDED IN bounded by v7 A1+A4 per memory line 12 + Cycle-2 closure table.

**Final disposition: FOLDED IN at LOCK** — no further action beyond Tilth-RT-07 enumeration extension at WS-L.

## 6.2 Tilth-RT-02 (HIGH) — Free-text leakage via `rationale` / `pattern_summary`

**Literal-slug subset:** FOLDED IN at LOCK via Cycle-1 RT-06 closure — §15.9.1 line 459 POST-gate regex extended to scan `source_substrate_path` AND `rationale` AND `pattern_summary` for org_slug literals from `orgs/ORG_INDEX.md`. Sub-tag `.workspace_digest_per_org_content`. Plus `.aggregate_insufficient_orgs` N=3 threshold from Cycle-1 RT-06 + Cycle-2 closure CLOSED.

**Indirect-reference subset (positional descriptors / template variables / numeric clues / paraphrase):** PARTIAL — not covered by literal-slug regex; F-ARCHIVIST-LESSON-INSTANCE-LEAK §15.9.2 NER detection is scoped to `proposed_lesson_text`, not to workspace-aggregate digest fields. Real gap.

**Final disposition: PARTIAL — DEFER to §15 v1.x amendment** per §2.2 above.

## 6.3 Tilth-RT-03 (MED) — NER paraphrase / Unicode-homoglyph evasion (lesson gate)

FOLDED IN at LOCK via Cycle-1 RT-07 closure — §15.9.2 three-layer (NFKC + NER + regex), blueprint lines 478, 490–491 + tests 717–718. Cycle-2 NF-04 surfaced "frozen `xx-ent-wiki-sm` adversarial weakness" → dispositioned at LOCK as bounded by v7 A4 (memory line 15: "NF-04 NER adversarial-robustness bounded by v7 LOCKED A4"). Mirrors row-170 transparent-disposition pattern.

**Final disposition: FOLDED IN at LOCK with v7 A4 boundary explicit** — no further action.

## 6.4 Tilth-RT-04 (MED) — Hard-link / bind-mount inode attack on `Path.resolve()`

**NEW finding** — not surfaced in either Cycle-1 or Cycle-2 of the §15 v1 audit. LOCKED §15 input contracts (§15.4.1 + §15.4.2) validate `Path.resolve()` resolves to a path under the declared subtree but do NOT check `os.lstat().st_nlink > 1`, do NOT enforce mount-option discipline, do NOT scan for bind-mounts.

Bounded by v7 A1 (single-client) + A4 (operator-trusted) in v0.1+v0.2 — only the operator has filesystem access to the Golden Quill in single-operator Beta deployment; the threat model has no foothold. Not exploitable at v0.1+v0.2 single-operator-trust posture.

**Final disposition: NEW gap, bounded v0.1+v0.2 by v7 A1+A4 — DEFER to v2 multi-tenant amendment per Section O.5** per §2.3 above.

## 6.5 Tilth-RT-05 (LOW) — PTY-based automation of TTY check

FOLDED IN at LOCK via Cycle-1 RT-04+RT-12 closure — TTY check now verifies `getsid()` consistency + controlling terminal is real `/dev/ttys*` (not PTY master). LOCKED §15.10 line 824 explicit boundary: "Does NOT introduce a hardware-token requirement at v0.2 + v1.x first ship (per RT-04+RT-12 disposition — bounded by v7 LOCKED A1+A4; v2 multi-tenant amendment lands hardware-token via Section O.5)." `/proc/$$/loginuid` proposal partially adopted via `getsid()` mechanism; OTP/YubiKey deferred to v2.

**Final disposition: FOLDED IN at LOCK with v7 A1+A4 boundary explicit** — no further action.

## 6.6 Tilth-RT-06 (LOW) — Persistence of informational mode into v1.x

FOLDED IN at LOCK via Cycle-1 RT-10 closure — `test_f_archivist_cadence_drift_is_fail_closed_at_v1_x` (§15.13.2 line 714) parses gate definition at v1.x, asserts `gate.severity == "HIGH"` AND `gate.action == "FAIL_CLOSED"`. User's "compile-time hard-code" variant not adopted; runtime gate definition + asserting test is structurally equivalent (the test fails the v1.x release if the toggle was missed; build-gate enforces).

**Final disposition: FOLDED IN at LOCK** — no further action.

## 6.7 Tilth-RT-07 (LOW, truncated in operator-supplied output) — Missing test for indirect file writes

LOCKED `test_archivist_no_subprocess_canonical_cli` (§15.13.1 line 694) scans for subprocess + `os.system` + `os.popen` + `os.exec*` + `os.spawn*` + `pexpect.*` invocations — but NOT `os.replace` / `os.rename` / `shutil.move` / `shutil.copy*` / `os.link`. `test_archivist_no_foreign_file_write_helper_imports` (line 695) scans imports, not direct calls. Runtime open-shim per Cycle-1 RT-02 closure wraps `open()` + `Path.write_text` + `Path.write_bytes` — but does NOT wrap `os.replace`. Real enumeration gap at the AST-lint layer.

Routes to WS-L because R-ARCHIVIST-NO-CANONICAL-MUTATE predicate body lives at §4, not §15 (memory line 26: "WS-L §4 Logician v2.x amendment registers F-ARCHIVIST-* family + extended R-ARCHIVIST-NO-CANONICAL-MUTATE AST-lint per RT-01/02/11 + Cycle 2 NF-01/02/05 closures" — this packet adds Tilth-RT-07 to that pin).

**Final disposition: PARTIAL — FOLD INTO WS-L §4 Logician v2.x amendment** per §2.1 above.

## 6.8 Live test-verification evidence (run 2026-05-10)

Per operator instruction (#4 of the five-additions queue), the AST-lint subset of the FOLDED IN findings was test-verified on current main rather than relying solely on line-citation. The pinned interpreter `.venv/bin/python3 → python3.14` is operator-side and unavailable in this session's sandbox; the sandbox runs Python 3.10.12, which is below the `pyproject.toml` minimum `>=3.11` but above the `@dataclass(frozen=True, kw_only=True)` collection floor (3.10+). Collection succeeded; the 27 skeleton tests + the 6 targeted AST-lint tests both ran green. Operator MUST re-run on the pinned 3.14 venv before treating this evidence as canonical.

**Run 1 — full skeleton suite:**
```
$ cd /Users/goldenquill/Downloads/GoldenQuill && python3 -m pytest tests/seats/archivist/skeleton_tests.py
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/goldenquill/Downloads/GoldenQuill
configfile: pyproject.toml
collected 27 items

tests/seats/archivist/skeleton_tests.py ...........................      [100%]

============================== 27 passed in 0.12s ==============================
```

**Run 2 — targeted AST-lint subset (FOLDED IN closures):**
```
$ python3 -m pytest tests/seats/archivist/skeleton_tests.py -v -k "no_subprocess or no_raw_open or yaml_safe_load or no_canonical_write_intent or v1_gate_codes or gate_predicates_raise"
============================= test session starts ==============================
collected 27 items / 21 deselected / 6 selected

test_v1_gate_codes_resolve_to_predicates                        PASSED [ 16%]
test_gate_predicates_raise_not_implemented_at_v0_2              PASSED [ 33%]
test_archivist_proposes_only_no_canonical_write_intent_calls    PASSED [ 50%]
test_archivist_no_subprocess_canonical_cli                      PASSED [ 66%]
test_archivist_no_raw_open_on_canonical_substrate               PASSED [ 83%]
test_archivist_yaml_safe_load_only                              PASSED [100%]

======================= 6 passed, 21 deselected in 0.11s =======================
```

**Per-test mapping to FOLDED IN findings:**

| Test | Closes Tilth-RT# | Verdict |
|---|---|---|
| `test_archivist_no_subprocess_canonical_cli` | RT-01 sub-attack (a) — subprocess invocation | PASS |
| `test_archivist_proposes_only_no_canonical_write_intent_calls` | RT-01 sub-attack (b) — direct write-intent calls | PASS |
| `test_archivist_no_raw_open_on_canonical_substrate` | Cycle-1 RT-11 closure (F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT, related to Tilth-RT-07 enumeration gap) | PASS |
| `test_archivist_yaml_safe_load_only` | Cycle-1 RT-09 closure (yaml.safe_load mandate) | PASS |
| `test_v1_gate_codes_resolve_to_predicates` | All five gate codes register | PASS |
| `test_gate_predicates_raise_not_implemented_at_v0_2` | v0.2 SPEC-ONLY discipline holds (predicates intentionally raise NotImplementedError) | PASS |

**LOCK manifest SHA verification (sha3-512 prefix):**

| File | Expected (memory line 22) | Live | Match |
|---|---|---|---|
| `pipeline/orchestrator/seats/archivist/__init__.py` | `7fb04e0199fa355a` | `7fb04e0199fa355a` | ✓ |
| `tests/seats/archivist/skeleton_tests.py` | `2702ff30bc984547` | `2702ff30bc984547` | ✓ |

Both LOCK-manifest SHAs match — the §15 v1 LOCK state is intact and matches the lock-time record. Live verification = stronger evidence path than line-citation alone.

**Tests NOT run (v1.x horizon, intentionally NotImplementedError at v0.2):**

The §15.13.2 v1.x horizon tests (Tilth-RT-03 NER paraphrase + RT-05 TTY check + RT-06 cadence-drift fail-closed + RT-02 indirect-reference + confirmation-id replay + principal-spoofing) are NOT runnable today because the predicate bodies live in §4 v2.x predicate realization (WS-L) + §15 v1.x amendment. `test_gate_predicates_raise_not_implemented_at_v0_2` PASS confirms the v0.2 SPEC-ONLY discipline — the predicates intentionally raise NotImplementedError per skeleton-tests pattern. Test-pass evidence for those will land at WS-L LOCK + §15 v1.x amendment LOCK.

**Caveat (operator action recommended):** the sandbox interpreter (3.10.12) is below `pyproject.toml` `>=3.11`. The 27 skeleton tests collect and pass on 3.10.12 because they don't exercise 3.11+ features, but full-suite green on the pinned `.venv/bin/python3 → python3.14` is the canonical evidence path per CLAUDE.md "Running tests — PINNED INTERPRETER." Re-run on operator-side venv before promoting this evidence to "canonical."

# 7. Cross-references

- §15 v1 SPEC LOCKED: `pipeline/blueprint/v0.1/section_15_archivist.md` (compound-LOCK rows 191/192)
- §0.5 v13 amendment: `pipeline/blueprint/v0.1/section_00_5_section_15_archivist_amendment.md` (14 rows; range 291–304)
- Cycle-1 + Cycle-2 audits: `pipeline/validation/blueprint_section_15_archivist_2026-05-10/audit_v{1,2}_{editor,judge,red_team}.md` + synthesis files
- WS-L §4 Logician v2.x packet: `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §WS-L (§4 v2.x amendment for new gate families)
- v0.1 Beta readiness: `pipeline/planning/v0_1_beta_readiness_2026-05-10.md`
- Section O.5 v2 hardening targets: `pipeline/architecture/v0.1/tilth_architecture_locked.md` Section O.5 (uppercase-O — v2-hardening; distinct from numeric §0.5 Interface Index)
- v7.0.4-M1 (corrective-amendment precedent): `pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md` (lock_history row 190)
- Row-170 transparent-disposition precedent: WS-D + WS-B + WS-C-M1 + Cycle-2 §15 fold-ins (memory lines 12, 15)
- §15 memory file: `memory/project_blueprint_section_15_archivist_v1_locked.md`

# 8. Done definition for this packet

This packet is "done" when:

1. NOW-actions §3 items 1–7 land (lock_history row + memory file + audit-trail footer + WS-L addendum + daily_log entry + lessons.json L-020 append + recursive-self-review meta-note in memory file).
2. WS-L acceptance criterion §2.1 is registered in the WS-L handoff (already covered by NOW-action 4).
3. §15 v1.x amendment author backlog includes the §2.2 acceptance criterion (operator-driven; happens when v1.x amendment opens, post-v0.2).
4. v2 multi-tenant amendment author backlog includes the §2.3 Section O.5 entry + the §2.3.1 cross-section binding (operator-driven; happens when v2 amendment opens).
5. Pre-v2 inode sweep walk per §2.3.1 happens in a separate operator-driven session before v2 amendment opens; findings file lands at `pipeline/validation/section_o5_inode_sweep_<date>/findings.md` (~30-min Cowork session).
6. ERDP-PO discipline §10 is referenced by future post-LOCK external-review packets (when they happen) rather than being re-derived.

This packet itself does NOT need a Thesis round — it's a routing document, not a new authored mechanism. Operator review + sign-off is sufficient.

# 9. Open questions for operator (if any)

- **Q1: Should the lock_history disposition row reference parent_lock_row=192 (§0.5 §15 amendment LOCK) or row=191 (§15 v1 SPEC LOCK)?** Default: 192, because the disposition is about the §15 v1 LOCK as a whole, and 192 is the compound-paired-commit terminal row. Override to 191 if the convention prefers the spec-row-not-amendment-row.

- **Q2: Should the audit-trail footer in `section_15_archivist.md` be appended in this session or in a follow-up?** Default: follow-up (so the LOCK-time SHA stays clean for downstream consumers); this packet's existence + the lock_history row + memory file are sufficient to surface the disposition without modifying the LOCKED file.

- **Q3: Should this packet itself ride a row-170 transparent disposition for the four FOLDED IN findings, or only for the three routed ones?** Default: only the three routed dispositions get row-170 treatment; the four FOLDED IN findings are documented in this packet's appendix (§6) but don't require their own disposition rows because the LOCK already covered them.

If Q1/Q2/Q3 defaults are acceptable, no operator response required — proceed with NOW-actions §3.

# 10. ERDP-PO — External-Review Disposition Packet (Post-LOCK Opportunistic) discipline

This section names the discipline this packet exemplifies, so future post-LOCK external-review responses have a precedent to point at rather than re-inventing the routing rules.

## 10.1 Definition

**ERDP-PO** = External-Review Disposition Packet, Post-LOCK Opportunistic. A planning-layer document that:

1. Receives external-review findings (Tilth-via-openclaw, partner audit, operator-driven fresh-eyes pass, third-party reviewer) against an already-LOCKED section or amendment.
2. Synthesizes each finding against the LOCKED text + its Cycle-1 + Cycle-2 closures, classifying each as FOLDED IN / PARTIAL / NEW.
3. Routes the open findings (PARTIAL + NEW) to their correct downstream consumer per the row-170 transparent-disposition pattern.
4. Documents the bounded interim posture for unlanded fixes under v7 A1+A4 (or whatever upstream-lock posture applies).
5. Does NOT reopen the LOCK unless the gap is architectural-layer (v7.0.4-M1 precedent).

**"Post-LOCK"** distinguishes from pre-LOCK Thesis Team rounds (L-005 two-cycle is the standard pre-LOCK discipline; ERDP-PO is what happens after a section LOCKs and a new review surfaces).

**"Opportunistic"** distinguishes from scheduled cross-family verification rounds (v7.0.4 row 181 was scheduled; this packet's parent review was unscheduled — Tilth ran a fresh Cycle-1 against the SCOPING DRAFT through the openclaw bridge without prompting from the blueprint process).

## 10.2 When to use ERDP-PO

- An external review surfaces ≥1 finding against a LOCKED section.
- The findings are MIX of FOLDED IN / PARTIAL / NEW (if all are FOLDED IN, a memory note + daily_log are sufficient — no packet needed).
- At least one finding routes to a downstream consumer that does not yet exist as a planned packet (e.g., needs a v1.x amendment criterion + a v2 Section O.5 entry + a WS-L acceptance test all at once).

If the findings only route to a single downstream consumer that already exists (e.g., "extend the WS-L handoff prompt by one line"), an inline edit to that consumer's handoff is sufficient — no full packet.

## 10.3 Packet structure (canonical sections)

The structure this packet uses is the canonical ERDP-PO template:

1. Why this packet exists + per-finding disposition table
2. Disposition routes (one §2.<n> per route; sub-section §2.<n>.<m> for cross-section blast-radius if applicable)
3. NOW-actions (lock_history row + memory file + audit-trail footer + downstream-consumer addenda + daily_log + lessons.json append + recursive-self-review meta-note where relevant)
4. Acceptance criteria summary table
5. Why no §-V-corrective amendment (architectural-layer vs. downstream-realization distinction; cite v7.0.4-M1 as the architectural-layer precedent)
6. Per-finding mapping evidence appendix (line/§ citations + live test-verification evidence where the LOCK includes runnable tests)
7. Cross-references
8. Done definition
9. Open questions for operator (if any)
10. (this section) ERDP-PO discipline naming — only the FIRST ERDP-PO packet writes this section; subsequent packets cite this packet's §10 by path

## 10.4 Distinction from architectural-layer corrective amendment (v7.0.4-M1 precedent)

| Property | ERDP-PO (this packet) | Corrective amendment (v7.0.4-M1) |
|---|---|---|
| Trigger | Post-LOCK external review surfaces gaps | Cross-family verification surfaces architectural-layer gaps |
| Scope of findings | Mix of FOLDED IN + downstream-realization PARTIAL + NEW gaps bounded by upstream lock | Architectural-layer gaps (KFR canonicalization, AST whitelist enumeration, atomic-read primitives) |
| Reopens parent LOCK? | No | Yes — narrow corrective amendment with new lock_history row |
| Routing destination | Downstream consumers (next blueprint round / next architectural amendment / Section O.5) | New corrective amendment file (e.g., `architecture_v7_0_4_M1_amendment.md`) |
| LOCK ceremony required? | No (operator review + sign-off sufficient) | Yes (full L-005 two-cycle Thesis round on the corrective amendment) |
| Memory file class | `project_section_<NN>_external_review_disposition_<date>.md` | `project_architecture_v<X>_<Y>_<Z>_M<n>_locked.md` |
| Lessons.json frequency increment | L-020 (this packet's lesson) | L-006 dormant-binding activation pattern (v7.0.4-M1's lesson) |

**Decision rule:** if the external-review findings would require text edits to the LOCKED architectural-layer file (the architecture amendment itself), it's a corrective amendment. If the findings route to downstream consumers without modifying the LOCKED text, it's an ERDP-PO.

## 10.5 Recursive sovereignty observation (informational)

The first ERDP-PO packet (this one) was triggered by Tilth — the agentic software that this packet's parent LOCK governs — running a fresh Cycle-1 review of the §15 SCOPING DRAFT through the openclaw bridge. This is the council reviewing its own substrate. It is the kind of recursive self-review pattern the Sovereign Node arc points at — the system surfacing gaps in its own design and routing them through its own LOCK discipline.

The ERDP-PO discipline named here is NOT specific to recursive-self-review; partner audits and operator-driven fresh-eyes passes route the same way. But the first instance is recursive, and worth noting because it's a small piece of evidence the architecture is doing what the architecture says it should do.
