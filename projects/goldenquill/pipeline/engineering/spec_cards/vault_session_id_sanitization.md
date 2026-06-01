# Spec card — pipeline.vault.vault_write (session_id filename sanitization)

**STATUS:** PRE-STAGED 2026-05-10
**Round:** Defense-in-depth filename safety — surfaced by 2026-05-10 review (finding #9).
**Canonical home:** `pipeline/vault/vault_write.py`

**Framework:** per `pipeline/templates/component_analysis_template.md`.

---

## 1. Blueprint anchors

- `pipeline/blueprint/v0.1/section_02_v7_2_locked.md` — vault write discipline + path-traversal defense.
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 §A4 — operator-trusted preflight assumption (defense-in-depth still required).
- `pipeline/architecture/v0.1/architecture_v7_0_4_M1_locked.md` §5 — write-before-compare audit-log discipline + symlink rejection.

**Spec-card version:** v1

---

## 2. Current state (drift)

`pipeline/vault/vault_write.py` line 517:

```python
tmp_path = tmp_dir / f"{intent}.{os.getpid()}.{session_id}.part"
```

**Problem:** `session_id` is interpolated directly into a filename. Upstream callers are expected to pass ULID-ish values (per §2 KFR ingestion), but the vault layer should still enforce filename-safe input as defense-in-depth. A malformed `session_id` containing `/`, `..`, NUL, or shell metacharacters could:
- Cause the temp file to land outside `tmp_dir` (path traversal).
- Collide with a sibling vault's `.tmp` namespace (org isolation, Law 3).
- Survive long enough to trigger F-VAULT-* gates downstream that assume well-formed paths.

This is not currently exploitable in production code paths (Intake mints ULIDs), but A4's "operator-trusted preflight" does NOT extend to the vault write layer — the vault is the last fail-closed gate.

---

## 3. Scope

### 3.1 In scope

- New helper `pipeline/vault/_session_id.py`:
  ```python
  _SESSION_ID_RE = re.compile(r"^[A-Z0-9]{26}$")  # ULID canonical form
  def assert_session_id_safe(value: str) -> None: ...
  ```
  Raises `F-VAULT-SESSION-ID-UNSAFE` if value does not match the ULID regex.
- Call `assert_session_id_safe(session_id)` at the top of `vault_write()` BEFORE any path construction.
- New failure code `F-VAULT-SESSION-ID-UNSAFE` registered in `pipeline/logician/failure_codes.py` (or wherever the F-VAULT-* family is enumerated). Severity: BLOCKING. Reason-tag: `"session_id {value!r} fails ULID canonical-form check at vault write gate"`.
- Update `BLUEPRINT_DEPS` on `vault_write.py` to reference §2 v7.2 and v7.0.4-M1 §5.

### 3.2 Out of scope

- Replacing the entire `session_id`-as-filename pattern. The pgid + session_id construction is intentional for crash-recovery / orphan-tmp detection. This card hardens the input check, not the structural pattern.
- Validation of `intent`. `intent` is enum-bounded upstream and not user-controlled at this layer.
- Symlink/path-traversal on `tmp_dir` itself. Covered by §5 v7.0.4-M1 NEW symlink rejection — already wired.

---

## 4. Failure codes touched

- **NEW:** `F-VAULT-SESSION-ID-UNSAFE` (BLOCKING, fail-closed). Triggers BEFORE any disk I/O.
- No existing F-VAULT-* codes change semantics.

---

## 5. Test surface

### 5.1 Property tests
- Valid ULID (26 char Crockford Base32 uppercase) passes.
- Empty string fails.
- String with `/` fails.
- String with `..` fails.
- String with NUL byte fails.
- String with shell metacharacter (`;`, `$`, `` ` ``, newline) fails.
- Lowercase ULID fails (canonical form is uppercase).
- 25-char string fails (length).
- 27-char string fails (length).
- Non-Base32 character (`I`, `L`, `O`, `U` excluded from Crockford) fails.

### 5.2 Failure-code tests
- `F-VAULT-SESSION-ID-UNSAFE` fires with exact reason-tag.
- Failure is raised BEFORE any `mkdir`/`open` call (test via `mock.patch` on `Path.mkdir` — must not be invoked).

### 5.3 Integration test
- `vault_write(..., session_id="../../etc/passwd")` raises `F-VAULT-SESSION-ID-UNSAFE`; no file is created anywhere.

### 5.4 Regression
- Every existing vault test that constructs a session_id must use a valid ULID. If any test passes a placeholder like `"test-session"` or `"abc123"`, it will fail under this card and need to be updated. Sweep needed.

---

## 6. Done definition

- `pytest pipeline/vault/tests/` green.
- `F-VAULT-SESSION-ID-UNSAFE` registered in failure-code enumeration with documented severity.
- Zero callers of `vault_write` pass non-ULID session_ids in the test corpus.
- `BLUEPRINT_DEPS` updated.

---

## 7. Risks / open questions

- **Q1.** Is `session_id` ever set to a non-ULID value in legitimate paths? E.g., `_assert_runstate_schema_current` may use a different identifier scheme. Grep `session_id=` across `pipeline/loop/`, `pipeline/seats/`, and `pipeline/intake/` before locking the regex.
- **Q2.** Does any test currently exercise the `.part` tmp-file path with a hand-rolled session_id? If yes, the regex needs to be looser OR those tests need ULID minting.
- **Q3.** Should we generalize to a `safe_filename_component()` helper used at other vault paths? Possibly — but scope expansion. Note for follow-up card.

---

## 8. Suggested executor

Codex (Claude Code) authoring → cross-family two-audit committee per L-005. Red Team should specifically probe path-traversal escapes.
