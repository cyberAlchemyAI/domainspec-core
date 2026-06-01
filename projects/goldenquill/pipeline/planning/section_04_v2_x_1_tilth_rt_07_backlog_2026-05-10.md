---
title: §4 v2.x.1 corrective amendment backlog — Tilth-RT-07 R-ARCHIVIST-NO-CANONICAL-MUTATE AST-lint enumeration extension
filed: 2026-05-10
operator: Josh
status: BACKLOG_QUEUED — seed text for a future §4 v2.x.1 corrective amendment; not yet dispatched.
parent_disposition_packet: pipeline/planning/section_15_external_review_disposition_2026-05-10.md  # §2.1 routes Tilth-RT-07 here
parent_locks:
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md  # §4 v2.x LOCKED 2026-05-10 rows 193/194 (compound-LOCK with §0.5 v14 amendment)
  - pipeline/blueprint/v0.1/section_15_archivist.md       # §15 v1 SPEC LOCKED 2026-05-10 rows 191/192 (compound-LOCK with §0.5 v13 amendment)
parent_lock_history_rows:
  - 195  # this disposition row (filed 2026-05-10T22:00:00Z; lock_class=external_review_disposition; verdict=DISPOSITIONED)
  - 193  # §4 v2.x LOCK
  - 194  # §0.5 v14 amendment (paired-commit with row 193)
  - 191  # §15 v1 SPEC LOCK
  - 192  # §0.5 v13 amendment (paired-commit with row 191)
authority: Josh 2026-05-10 ("write that dispatch packet now") + dispatch coordinator's WS-L LOCK timing adjustment.
purpose: Carry the Tilth-RT-07 PARTIAL closure forward as a backlog item for a future §4 v2.x.1 corrective amendment. The original disposition packet routed Tilth-RT-07 to the WS-L handoff prompt, but WS-L §4 v2.x LOCKed at 2026-05-10T20:45:00Z (rows 193/194) BEFORE this disposition packet could ride the LOCK ceremony. The addendum cannot retroactively edit the LOCKed text. Instead, this file holds the seed text for a future §4 v2.x.1 corrective amendment cycle.
disposition_class: backlog_seed_for_future_amendment
threat_severity_at_v0_1_v0_2: LOW — bounded by v7 LOCKED A4 (operator-trusted, contributor-discipline); not exploitable under single-operator Beta deployment threat model. Promotion to MED would require multi-contributor or v2 multi-tenant context.
---

# 1. Why this backlog file exists

§15 v1 SPEC LOCK 2026-05-10 (compound-LOCK rows 191/192) registered `R-ARCHIVIST-NO-CANONICAL-MUTATE` as the AST-lint rule preventing the Archivist seat from performing canonical-substrate mutations. The §15 SPEC names the rule by reference; the rule's predicate body lives at §4 Logician.

WS-L §4 Logician v2.x LOCK 2026-05-10 (compound-LOCK rows 193/194) registered the predicate body. The §4 v2.x amendment text already enumerates the standard subprocess + `os.system` + `os.popen` + `os.exec*` + `os.spawn*` + `pexpect.*` invocation patterns per §15.13.1 line 694 and Cycle-1 + Cycle-2 closures.

What §4 v2.x did NOT enumerate: **low-level rename primitives** that contributors could use to perform canonical-substrate writes by writing a temp file inside an allowed-prefix path and then atomically renaming it over a forbidden canonical path.

This backlog file carries the §2.1 addendum text from `pipeline/planning/section_15_external_review_disposition_2026-05-10.md` forward as the seed for a future §4 v2.x.1 corrective amendment.

# 2. Original disposition packet routing (for reference)

The disposition packet's §2.1 stated:

> Routing destination: WS-L §4 Logician v2.x amendment per `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §WS-L. The §15 v1 SPEC LOCK names the AST-lint rule `R-ARCHIVIST-NO-CANONICAL-MUTATE`; WS-L is the round that writes its predicate body. This is the cleanest place — the rule lives at §4, not §15.

WS-L closed at 2026-05-10T20:45:00Z (rows 193/194). The disposition packet was filed afterward, so the addendum could not ride the WS-L LOCK ceremony. The dispatch coordinator's adjusted routing: **§4 v2.x.1 corrective amendment backlog**, this file.

# 3. Seed text for §4 v2.x.1 corrective amendment

When a §4 v2.x.1 corrective amendment is dispatched, the following must land:

## 3.1 AST-lint enumeration extension (R-ARCHIVIST-NO-CANONICAL-MUTATE)

The §4 v2.x amendment text describing `R-ARCHIVIST-NO-CANONICAL-MUTATE` MUST be extended to explicitly enumerate the five low-level rename primitives in the forbidden-call list:

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

## 3.2 Acceptance test stub

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

Test file: `tests/logician/gates/test_r_archivist_no_canonical_mutate.py` (extends existing tests at WS-L LOCK).

## 3.3 Runtime guard wrapper extension (defense-in-depth, non-load-bearing at v0.2 SPEC-ONLY)

The runtime guard layer at §15.9.3 line 521 currently wraps `open()` + `Path.write_text` + `Path.write_bytes` with the allowed-prefix-set check. When the runtime guard is realized at v1.x per §15.9.3, that wrapper set MUST also extend to:

- `os.replace`
- `os.rename`
- `shutil.move`

Document in the §4 v2.x.1 amendment that the runtime guard's wrapper set MUST mirror the AST-lint forbidden-call set (single source of truth: §4 v2.x.1's forbidden-call enumeration drives both layers).

`shutil.copy*` and `os.link` / `os.symlink` are file-creation rather than file-overwrite primitives; the AST-lint sub-tag captures contributor-discipline at compile time. Runtime-guard wrapping for the link primitives is OPTIONAL at v1.x — track as a secondary defense-in-depth note for v1.x amendment author.

# 4. Acceptance criterion (closes Tilth-RT-07)

§4 v2.x.1 LOCK ceremony asserts:

1. The five sub-tags above (`.low_level_rename_replace`, `.low_level_rename_rename`, `.low_level_rename_shutil_move`, `.low_level_rename_shutil_copy`, `.low_level_rename_os_link`) are registered in the `R-ARCHIVIST-NO-CANONICAL-MUTATE` predicate body.
2. The new acceptance test `test_r_archivist_no_canonical_mutate_enumerates_low_level_rename_primitives` is green in the §4 LOCK suite.
3. The §4 v2.x.1 amendment text enumerates the five low-level rename primitives explicitly, with the sub-tag mapping shown verbatim.
4. The runtime-guard wrapper extension note for `os.replace` / `os.rename` / `shutil.move` is recorded in §15.9.3's v1.x amendment-realization checklist (cross-reference back to this backlog file).

# 5. Threat-model boundaries (interim posture)

- **v0.1 + v0.2 single-operator Beta deployment:** bounded by v7 LOCKED A4 (operator-trusted preflight). Operator is the only contributor; contributor-discipline gap is not exploitable. AST-lint enumeration extension is contributor-hygiene, not adversarial-defense.
- **v1.x first-ship:** bounded by v7 LOCKED A1 (single-client) + A4 (operator-trusted). Same boundary applies — gap remains contributor-discipline-shaped.
- **v2 multi-tenant:** if §4 v2.x.1 has not landed by the v2 amendment cycle, the gap promotes to MED severity (multi-contributor + multi-tenant context can exploit). Section O.5 v2 multi-tenant amendment author should verify §4 v2.x.1 LOCK before declaring §15 hardened for v2 deployment.

# 6. Dispatch readiness

This backlog packet is **dispatchable as-is** when bandwidth allows:

- Spec is fully derivable from §3 above without operator input.
- L-005 two-cycle cadence applies; cross-family rigor matches WS-L LOCK posture (Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq via openclaw bridge).
- Wall-time estimate: ~1 session (single-rule extension; existing test infrastructure in place; well-scoped).
- Cleanest dispatch trigger: ride into the next §4 amendment cycle (whatever opens next). Alternative: standalone §4 v2.x.1 corrective dispatch, modeled on v7.0.4-M1 (lock_history row 190) precedent for narrow-corrective amendment.

# 7. Cross-references

- Disposition packet: `pipeline/planning/section_15_external_review_disposition_2026-05-10.md` §2.1 (Tilth-RT-07 detailed analysis)
- §15 v1 LOCK: `pipeline/blueprint/v0.1/section_15_archivist.md` (§15.9.3 line 521 + §15.13.1 line 694)
- §4 v2.x LOCK: `pipeline/blueprint/v0.1/section_04_v2_x_amendment.md` (predicate body home)
- v7.0.4-M1 corrective-amendment precedent: `pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md` (lock_history row 190)
- WS-L dispatch handoff (closed): `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §WS-L (post-LOCK note added pointing here)
- Lock history row for this backlog filing: row 195 (lock_class=external_review_disposition)
