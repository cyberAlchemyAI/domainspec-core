"""M6 atomic-flush + INTERRUPTED state writer/reader. [§3.9, §3.9.1, §4.5, §6]

Section 1 Round E. Owns:

* ``checkpoint(session, payload)`` — M6 atomic flush. Produces
  ``(payload_bytes, manifest_dict)`` and hands them to §2 v7 Vault via a
  registered ``VaultCommitHook``. If no hook is registered (Phase-0, before
  Section 2 Vault exists), falls back to ``_default_local_vault_commit``
  which performs a direct tmp+rename with the §4.5 v3 double-check
  ``st_dev`` cross-filesystem guard.
* ``detect_interrupted(repo_root)`` — scans ``sovereignty/sessions/`` for the
  newest ``INTERRUPTED`` session record.
* ``resume_or_discard(session, *, policy)`` — implements the three-policy
  post-crash decision (resume / discard / prompt).

``register_vault_commit_hook`` is the boundary that §2 v7 Vault will use
when it lands (Group 5). Until then, the default-local fallback keeps the
INTERRUPTED state path testable end-to-end.

Blueprint references:

* §2.4              Session schema (combined interrupted record)
* §2.8              on-disk layout
* §3.9              interrupted-state public API
* §3.9.1            M14 Vault-as-substrate clarifier
* §4.5 M6           atomic flush / signal plumbing / v3 double-check
* §6 (F-ADM-05/06), §6.7 (F-ISO-06 CrossFilesystemRename)

E-enforcement:

* E-001 arg-type validation before any I/O
* E-007 tests must monkey-patch ``_current_vault_commit_hook`` on THIS
  module, not on callers; Round E test file pins the convention.
"""

from __future__ import annotations

import datetime as _dt
import errno
import hashlib
import json
import os
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Protocol

from pipeline.sovereignty._types import HashDigest  # noqa: F401 (re-exported via pkg)
from pipeline.sovereignty.isolation import IsolationError as _IsolationError

__all__ = [
    "CrossFilesystemRename",
    "IntegrityError",
    "InterruptedStateInvalid",
    "OperatorDecisionRequired",
    "VaultCommitHook",
    "VaultCommitHookLocked",
    "checkpoint",
    "detect_interrupted",
    "lock_vault_commit_hook",
    "register_resume_validator",
    "register_vault_commit_hook",
    "resume_or_discard",
]

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": [
            "§2.4 Session (combined interrupted record)",
            "§3.9 interrupted_state public API",
            "§3.9.1 M14 Vault-as-substrate clarifier",
            "§4.5 M6 atomic flush + v3 st_dev double-check",
            "§6 F-ADM-05 integrity-error",
            "§6.7 F-ISO-06 cross-fs rename race",
        ],
        "hash_at_lock": "lock-round-E-v2-2026-04-19",
        "hash_source_version": "v6",
    },
}


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class IntegrityError(RuntimeError):
    """F-ADM-05. Payload integrity re-check failed before Vault hand-off.

    Raised when the payload bytes about to be committed to §2 Vault do not
    hash-match the canonical-JSON re-serialization. Fires on §1-internal
    buffer-integrity errors; NEVER on §2 Vault commit errors.
    """


class CrossFilesystemRename(_IsolationError):
    """F-ISO-06 (shared with isolation.py). tmp + final parents on diverged st_dev.

    Subclasses Round-D :class:`pipeline.sovereignty.isolation.IsolationError` —
    the shared F-ISO family parent — so ``except IsolationError`` catches this
    alongside PathEscape/InodeDrift/VolumeDrift. We sit beside PathEscape rather
    than under it because PathEscape uses kw-only init (path/root/reason),
    which would force callers to restructure their positional raise sites.
    Closes Round E committee v1 Gemini MED-1 taxonomy coherence finding.
    """


class VaultCommitHookLocked(RuntimeError):
    """Vault-commit hook registration rejected after boot-phase lock.

    Section 2 Vault calls :func:`lock_vault_commit_hook` once at boot after
    registering its hook; subsequent calls to :func:`register_vault_commit_hook`
    raise this error. Closes Round E committee v1 GPT-OSS HIGH-C boot-phase
    hardening finding.
    """


class InterruptedStateInvalid(RuntimeError):
    """resume policy selected a payload whose bound RFA/project_context hashes mismatch."""


class OperatorDecisionRequired(RuntimeError):
    """policy='prompt' — Section 5 CLI handles the decision; §1 raises."""


# ---------------------------------------------------------------------------
# VaultCommitHook protocol + registration
# ---------------------------------------------------------------------------


class VaultCommitHook(Protocol):
    """§3.9.1. Shape §2 v7 Vault will satisfy when it lands (Group 5)."""

    def __call__(
        self,
        *,
        org_slug: str,
        sub_path: str,
        payload_bytes: bytes,
        manifest: dict[str, Any],
    ) -> Path:
        ...


_vault_commit_hook: VaultCommitHook | None = None
_vault_commit_hook_locked: bool = False


def register_vault_commit_hook(hook: VaultCommitHook | None) -> VaultCommitHook | None:
    """Install or clear the §2 Vault commit hook. Returns prior hook for restore.

    Phase-0 contract: when no hook is registered, ``checkpoint`` routes to
    ``_default_local_vault_commit`` which performs a direct tmp+rename to
    ``sovereignty/sessions/{session_id}.json``. When §2 v7 lands, it will
    register its real ``vault_commit`` at boot, then call
    :func:`lock_vault_commit_hook` to freeze the registration against
    further changes.

    :raises VaultCommitHookLocked: if :func:`lock_vault_commit_hook` has been
        called on this process. Boot-phase locking closes the Round E v1
        GPT-OSS HIGH-C hostile-injection window — code paths loaded after
        Section 2 boot cannot swap the hook.
    """
    global _vault_commit_hook
    if _vault_commit_hook_locked:
        raise VaultCommitHookLocked(
            "vault_commit hook is locked; register_vault_commit_hook rejected"
        )
    prior = _vault_commit_hook
    _vault_commit_hook = hook
    return prior


def lock_vault_commit_hook() -> None:
    """Freeze vault_commit hook registration. Idempotent; once True stays True.

    Called by Section 2 Vault at boot after its own registration. Tests
    that need to install/uninstall hooks do NOT call this — it locks for
    process lifetime. Unit tests exercise the locked path via
    :func:`_unlock_vault_commit_hook_for_tests` in test scaffolding only.
    """
    global _vault_commit_hook_locked
    _vault_commit_hook_locked = True


def _unlock_vault_commit_hook_for_tests() -> None:
    """TEST-ONLY: release the lock so the next test starts fresh.

    Not in ``__all__``; not a public API. Exists so the test suite can
    exercise the lock-reject path without leaking locked state across tests.
    """
    global _vault_commit_hook_locked
    _vault_commit_hook_locked = False


def _current_vault_commit_hook() -> VaultCommitHook:
    if _vault_commit_hook is not None:
        return _vault_commit_hook
    return _default_local_vault_commit


# ---------------------------------------------------------------------------
# Canonical JSON + SHA3-512 helpers
# ---------------------------------------------------------------------------


def _canonical_json_bytes(obj: dict[str, Any]) -> bytes:
    """Sorted keys, ASCII-safe, no whitespace. Matches §2.8 canon rules."""
    return json.dumps(
        obj,
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha3_512_hex(data: bytes) -> str:
    return hashlib.sha3_512(data).hexdigest()


# ---------------------------------------------------------------------------
# Atomic write (M6 v3 double-check)
# ---------------------------------------------------------------------------


def _atomic_write_with_st_dev_double_check(
    final_path: Path, data: bytes
) -> Path:
    """Tmp+rename with pre AND post st_dev check. [§4.5 M6 v3]

    Check A (pre-creation): ``os.stat(tmp_parent).st_dev ==
    os.stat(final_parent).st_dev``. Check B (post-creation, pre-rename):
    ``os.fstat(fd).st_dev == os.stat(final_parent).st_dev``. Divergence at
    either check raises :class:`CrossFilesystemRename` (F-ISO-06).
    """
    final_parent = final_path.parent
    final_parent.mkdir(parents=True, exist_ok=True)
    tmp_parent = final_parent  # per §4.5 we co-locate
    # Check A — pre-creation.
    if os.stat(tmp_parent).st_dev != os.stat(final_parent).st_dev:
        raise CrossFilesystemRename(
            f"F-ISO-06 pre-creation st_dev mismatch on {final_path}"
        )
    suffix = secrets.token_hex(8)
    tmp_path = tmp_parent / f"{final_path.name}.tmp.{suffix}"
    fd = os.open(
        str(tmp_path), os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600
    )
    try:
        written = os.write(fd, data)
        if written != len(data):
            raise IntegrityError(
                f"short write: {written}/{len(data)} bytes for {final_path}"
            )
        os.fsync(fd)
        # Check B — post-creation, pre-rename.
        tmp_st_dev = os.fstat(fd).st_dev
        final_st_dev = os.stat(final_parent).st_dev
        if tmp_st_dev != final_st_dev:
            raise CrossFilesystemRename(
                f"F-ISO-06 post-creation st_dev mismatch on {final_path}"
            )
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        try:
            os.unlink(str(tmp_path))
        except OSError:
            pass
        raise
    else:
        os.close(fd)
    os.rename(str(tmp_path), str(final_path))
    return final_path


# ---------------------------------------------------------------------------
# Default local Vault-commit (Phase-0 fallback)
# ---------------------------------------------------------------------------


def _default_local_vault_commit(
    *,
    org_slug: str,
    sub_path: str,
    payload_bytes: bytes,
    manifest: dict[str, Any],
) -> Path:
    """Phase-0 fallback: write combined session record directly. [§3.9.1]

    Derives ``sovereignty/sessions/{session_id}.json`` from the manifest
    ``repo_root`` + ``session_id`` and performs the M6 v3 atomic write. §2
    Vault will replace this with a CAS commit under M14.1 gate-and-open when
    Group 5 lands.
    """
    repo_root = Path(manifest["repo_root"])
    session_id = manifest["session_id"]
    sessions_dir = repo_root / "sovereignty" / "sessions"
    final_path = sessions_dir / f"{session_id}.json"
    return _atomic_write_with_st_dev_double_check(final_path, payload_bytes)


# ---------------------------------------------------------------------------
# checkpoint
# ---------------------------------------------------------------------------


def checkpoint(session: Any, payload: dict[str, Any]) -> Path:
    """Write a combined ``{session, interrupted_payload}`` record. [§4.5 M6]

    Steps:

    1. Build combined dict from ``session`` fields + status ``INTERRUPTED``
       + ``interrupted_at`` UTC + canonical ``interrupted_payload``.
    2. Serialize canonical JSON to ``payload_bytes``.
    3. Re-hash and re-serialize; mismatch raises :class:`IntegrityError`
       (F-ADM-05) BEFORE Vault hand-off, per §3.9.1.
    4. Build ``manifest_dict`` with kind + session_id + slug + sha3-512 +
       repo_root.
    5. Call the registered :class:`VaultCommitHook` (or the Phase-0 fallback).
    6. Return the Path yielded by the hook (read-only telemetry handle).

    :param session: sovereignty Session dataclass (duck-typed — must expose
        ``session_id``, ``slug``, ``started_at``, ``hmac_key_id``,
        ``router_manifest_sha``, ``pid``, ``repo_root`` access via the
        session ``_repo_root`` attribute set by :func:`start_session`).
    :param payload: seat-emitted state to persist. Must be JSON-serializable.
    """
    if not isinstance(payload, dict):
        raise TypeError(
            f"payload must be dict; got {type(payload).__name__}"
        )

    # Step 1 — combined dict.
    interrupted_at = _dt.datetime.now(_dt.timezone.utc).isoformat(
        timespec="microseconds"
    )
    combined = {
        "session_id": session.session_id,
        "slug": session.slug,
        "started_at": session.started_at,
        "hmac_key_id": session.hmac_key_id,
        "router_manifest_sha": session.router_manifest_sha,
        "pid": session.pid,
        "status": "INTERRUPTED",
        "interrupted_at": interrupted_at,
        "interrupted_payload": payload,
    }

    # Step 2 — serialize.
    payload_bytes = _canonical_json_bytes(combined)

    # Step 3 — integrity re-check. Re-hash and re-serialize; divergence =
    # F-ADM-05. The re-serialize catches a subtly non-canonical input dict
    # that JSON happens to serialize deterministically but whose re-parse
    # + re-dump yields different bytes.
    expected_hash = _sha3_512_hex(payload_bytes)
    reparsed = json.loads(payload_bytes.decode("utf-8"))
    reserialized = _canonical_json_bytes(reparsed)
    if _sha3_512_hex(reserialized) != expected_hash:
        raise IntegrityError(
            "F-ADM-05 payload re-serialize diverged; refusing Vault hand-off"
        )

    # Step 4 — manifest.
    # repo_root is resolved via the session's attached runtime; callers that
    # construct a bare Session for testing can set `_repo_root` directly.
    repo_root = getattr(session, "_repo_root", None)
    if repo_root is None:
        raise IntegrityError(
            "F-ADM-05 session has no _repo_root binding; cannot route to Vault"
        )
    manifest_dict = {
        "kind": "session_interrupted",
        "session_id": session.session_id,
        "slug": session.slug,
        "sha3_512": expected_hash,
        "repo_root": str(Path(repo_root)),
    }

    # Step 5 — route.
    hook = _current_vault_commit_hook()
    written_path = hook(
        org_slug=session.slug,
        sub_path=f"runs/{session.session_id}/interrupted/",
        payload_bytes=payload_bytes,
        manifest=manifest_dict,
    )
    if not isinstance(written_path, Path):
        raise IntegrityError(
            f"VaultCommitHook must return Path; got {type(written_path).__name__}"
        )
    return written_path


# ---------------------------------------------------------------------------
# detect_interrupted
# ---------------------------------------------------------------------------


def detect_interrupted(repo_root: Path) -> dict[str, Any] | None:
    """Return the newest INTERRUPTED session record, as a dict. [§3.9]

    Returns a plain dict (not the frozen :class:`Session` dataclass) because
    the dataclass lives in :mod:`pipeline.sovereignty.session` and would
    create a circular import. Callers in Section 5 materialize the dataclass
    via ``Session(**record_dict)`` at the policy boundary.
    """
    if not isinstance(repo_root, Path):
        raise TypeError(
            f"repo_root must be Path; got {type(repo_root).__name__}"
        )
    sessions_dir = repo_root / "sovereignty" / "sessions"
    if not sessions_dir.is_dir():
        return None
    candidates: list[dict[str, Any]] = []
    for p in sessions_dir.glob("*.json"):
        if p.name.startswith("."):
            continue
        try:
            record = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(record, dict):
            continue
        if record.get("status") == "INTERRUPTED":
            candidates.append(record)
    if not candidates:
        return None
    candidates.sort(key=lambda r: r.get("started_at", ""), reverse=True)
    return candidates[0]


# ---------------------------------------------------------------------------
# resume_or_discard
# ---------------------------------------------------------------------------


_RESUME_VALIDATORS: dict[str, Callable[[dict[str, Any]], None]] = {}


def register_resume_validator(
    name: str, validator: Callable[[dict[str, Any]], None]
) -> Callable[[dict[str, Any]], None] | None:
    """Boundary for Section 5 to inject RFA + PROJECT_CONTEXT hash re-check.

    §1 does not know the concrete :mod:`rfa_envelope` / :mod:`project_context_envelope`
    interfaces yet (those are Rounds F/G). The caller injects a validator;
    when none is registered, the ``resume`` policy only re-reads the record
    without cross-envelope validation. Unit tests install a validator to
    exercise the :class:`InterruptedStateInvalid` path.
    """
    prior = _RESUME_VALIDATORS.get(name)
    _RESUME_VALIDATORS[name] = validator
    return prior


def _clear_resume_validators() -> None:
    _RESUME_VALIDATORS.clear()


def resume_or_discard(
    session: Any, *, policy: str, repo_root: Path | None = None
) -> dict[str, Any] | None:
    """Resume, discard, or prompt the operator. [§3.9 / §4.5 policies]

    :param session: Session dataclass instance.
    :param policy: ``"resume"`` | ``"discard"`` | ``"prompt"``.
    :param repo_root: override for the session's ``_repo_root`` binding.
    """
    if policy not in {"resume", "discard", "prompt"}:
        raise ValueError(
            f"policy must be 'resume'|'discard'|'prompt'; got {policy!r}"
        )
    if policy == "prompt":
        raise OperatorDecisionRequired(
            "policy='prompt' — Section 5 CLI must resolve the decision."
        )
    effective_repo_root = (
        repo_root if repo_root is not None else getattr(session, "_repo_root", None)
    )
    if effective_repo_root is None:
        raise IntegrityError(
            "resume_or_discard: repo_root must be provided via kwarg or session._repo_root"
        )
    record_path = (
        Path(effective_repo_root)
        / "sovereignty"
        / "sessions"
        / f"{session.session_id}.json"
    )
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise InterruptedStateInvalid(
            f"cannot read session record {record_path}: {e}"
        ) from e

    if policy == "resume":
        payload = record.get("interrupted_payload")
        if payload is None:
            raise InterruptedStateInvalid(
                "resume: record has no interrupted_payload"
            )
        for name, validator in _RESUME_VALIDATORS.items():
            try:
                validator(record)
            except Exception as e:
                raise InterruptedStateInvalid(
                    f"resume validator {name!r} rejected record: {e}"
                ) from e
        return payload

    # discard — rewrite status=ENDED_CLEAN + drop payload.
    cleaned = {
        "session_id": record["session_id"],
        "slug": record["slug"],
        "started_at": record["started_at"],
        "hmac_key_id": record["hmac_key_id"],
        "router_manifest_sha": record["router_manifest_sha"],
        "pid": record["pid"],
        "status": "ENDED_CLEAN",
    }
    cleaned_bytes = _canonical_json_bytes(cleaned)
    _atomic_write_with_st_dev_double_check(record_path, cleaned_bytes)
    return None
