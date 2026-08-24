"""Fail-closed admission for a Chapter Factory local voice compile handoff."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, cast

from .canonical import JsonValue, canonical_sha256
from .compiler_config import CompilerConfig, require_normalized_config


HANDOFF_SCHEMA = "lucifers-lights.voice-compiler-handoff/1.0.0"
AUTHOR_DECISION_SCHEMA = "lucifers-lights.author-decision/1.0.0"
SYNC_DISPOSITION_SCHEMA = "lucifers-lights.voice-sync-disposition/1.0.0"
_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


class FactoryHandoffError(ValueError):
    """Raised before compilation when the factory handoff does not bind exactly."""


@dataclass(frozen=True, slots=True)
class LocalCompileAdmission:
    """The bounded facts established by one successful local admission."""

    project_id: str
    chapter_id: str
    run_id: str
    chapter_run_digest: str
    handoff_sha256: str
    source_sha256: str
    compiler_config_sha256: str
    sync_disposition_sha256: str


def _duplicate_safe_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise FactoryHandoffError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_constant(token: str) -> None:
    raise FactoryHandoffError(f"non-finite JSON token is forbidden: {token}")


def _reject_float(token: str) -> None:
    raise FactoryHandoffError(f"floating-point JSON value is forbidden: {token}")


def _json_document(payload: bytes, label: str) -> dict[str, Any]:
    if type(payload) is not bytes:
        raise FactoryHandoffError(f"{label} must be exact bytes")
    try:
        value = json.loads(
            payload.decode("utf-8", errors="strict"),
            object_pairs_hook=_duplicate_safe_object,
            parse_constant=_reject_constant,
            parse_float=_reject_float,
        )
    except FactoryHandoffError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as error:
        raise FactoryHandoffError(f"{label} must be valid UTF-8 JSON") from error
    if type(value) is not dict:
        raise FactoryHandoffError(f"{label} must be an object")
    return cast(dict[str, Any], value)


def _closed(
    value: object,
    label: str,
    fields: set[str],
) -> dict[str, Any]:
    if type(value) is not dict:
        raise FactoryHandoffError(f"{label} must be an object")
    candidate = cast(dict[str, Any], value)
    missing = sorted(fields - set(candidate))
    unknown = sorted(set(candidate) - fields)
    if missing:
        raise FactoryHandoffError(f"{label} missing fields: {', '.join(missing)}")
    if unknown:
        raise FactoryHandoffError(f"{label} has unknown fields: {', '.join(unknown)}")
    return candidate


def _text(value: object, label: str) -> str:
    if type(value) is not str or not value or value.strip() != value:
        raise FactoryHandoffError(f"{label} must be non-empty trimmed text")
    return value


def _digest(value: object, label: str) -> str:
    digest = _text(value, label)
    if _SHA256_RE.fullmatch(digest) is None:
        raise FactoryHandoffError(f"{label} must be lowercase SHA-256")
    return digest


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _size(value: object, label: str) -> int:
    if type(value) is not int or value < 1:
        raise FactoryHandoffError(f"{label} must be a positive integer")
    return value


def _repository_root(value: Path) -> Path:
    root = value.resolve()
    if not root.is_dir():
        raise FactoryHandoffError(f"repository root is not a directory: {root}")
    return root


def _argument_locator(path: Path, root: Path, label: str) -> str:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError as error:
        raise FactoryHandoffError(f"{label} is outside the repository") from error
    if not resolved.is_file():
        raise FactoryHandoffError(f"{label} is not a file: {relative.as_posix()}")
    return relative.as_posix()


def _bound_repository_file(
    locator: object,
    root: Path,
    label: str,
) -> tuple[str, Path]:
    text = _text(locator, f"{label}.path")
    pure = PurePosixPath(text)
    if pure.is_absolute() or not pure.parts or any(part in {"", ".", ".."} for part in pure.parts):
        raise FactoryHandoffError(f"{label}.path must be a normalized repository-relative path")
    path = (root / Path(*pure.parts)).resolve()
    try:
        relative = path.relative_to(root).as_posix()
    except ValueError as error:
        raise FactoryHandoffError(f"{label}.path escapes the repository") from error
    if relative != text:
        raise FactoryHandoffError(f"{label}.path is not normalized")
    if not path.is_file():
        raise FactoryHandoffError(f"{label}.path is not a file: {text}")
    return relative, path


def _source_binding(
    value: object,
    *,
    root: Path,
    expected_locator: str,
    payload: bytes,
) -> dict[str, Any]:
    binding = _closed(
        value,
        "factory handoff voice_source",
        {"id", "path", "role", "sha256", "size_bytes"},
    )
    _text(binding["id"], "factory handoff voice_source.id")
    if binding["role"] != "audio-script-derivative":
        raise FactoryHandoffError("factory handoff voice source role is invalid")
    locator, _ = _bound_repository_file(
        binding["path"], root, "factory handoff voice_source"
    )
    if locator != expected_locator:
        raise FactoryHandoffError("factory handoff voice source path does not match CLI input")
    observed = _sha256(payload)
    if _digest(binding["sha256"], "factory handoff voice_source.sha256") != observed:
        raise FactoryHandoffError("factory handoff voice source digest does not match CLI bytes")
    if _size(binding["size_bytes"], "factory handoff voice_source.size_bytes") != len(payload):
        raise FactoryHandoffError("factory handoff voice source size does not match CLI bytes")
    return binding


def _config_binding(
    value: object,
    *,
    root: Path,
    expected_locator: str,
    payload: bytes,
    config: CompilerConfig,
) -> dict[str, Any]:
    binding = _closed(
        value,
        "factory handoff compiler_config",
        {
            "id",
            "path",
            "role",
            "sha256",
            "size_bytes",
            "schema_version",
            "production_id",
        },
    )
    _text(binding["id"], "factory handoff compiler_config.id")
    if binding["role"] != "voice-compiler-config":
        raise FactoryHandoffError("factory handoff compiler config role is invalid")
    locator, _ = _bound_repository_file(
        binding["path"], root, "factory handoff compiler_config"
    )
    if locator != expected_locator:
        raise FactoryHandoffError("factory handoff compiler config path does not match CLI input")
    observed = _sha256(payload)
    if _digest(binding["sha256"], "factory handoff compiler_config.sha256") != observed:
        raise FactoryHandoffError("factory handoff compiler config digest does not match CLI bytes")
    if _size(binding["size_bytes"], "factory handoff compiler_config.size_bytes") != len(payload):
        raise FactoryHandoffError("factory handoff compiler config size does not match CLI bytes")
    if binding["schema_version"] != config.schema_version:
        raise FactoryHandoffError("factory handoff compiler schema does not match parsed config")
    if binding["production_id"] != config.production_id:
        raise FactoryHandoffError("factory handoff production id does not match parsed config")
    return binding


def _sync_binding(
    value: object,
    *,
    root: Path,
    project_id: str,
    chapter_id: str,
    manuscript_sha256: str,
) -> tuple[dict[str, Any], str]:
    binding = _closed(
        value,
        "factory handoff sync_disposition",
        {"id", "path", "role", "sha256", "size_bytes"},
    )
    _text(binding["id"], "factory handoff sync_disposition.id")
    if binding["role"] != "derivative-sync-decision":
        raise FactoryHandoffError("factory handoff sync disposition role is invalid")
    _, path = _bound_repository_file(
        binding["path"], root, "factory handoff sync_disposition"
    )
    payload = path.read_bytes()
    observed = _sha256(payload)
    if _digest(binding["sha256"], "factory handoff sync_disposition.sha256") != observed:
        raise FactoryHandoffError("factory handoff sync disposition digest drift")
    if _size(binding["size_bytes"], "factory handoff sync_disposition.size_bytes") != len(payload):
        raise FactoryHandoffError("factory handoff sync disposition size drift")
    document = _json_document(payload, "voice sync disposition")
    if document.get("schema_version") != SYNC_DISPOSITION_SCHEMA:
        raise FactoryHandoffError("unsupported voice sync disposition schema")
    if document.get("project_id") != project_id or document.get("chapter_id") != chapter_id:
        raise FactoryHandoffError("voice sync disposition identity does not match handoff")
    if document.get("manuscript_sha256") != manuscript_sha256:
        raise FactoryHandoffError("voice sync disposition manuscript does not match handoff")
    authorization = document.get("authorization")
    if type(authorization) is not dict:
        raise FactoryHandoffError("voice sync disposition authorization must be an object")
    if authorization.get("scope") != "accepted-manuscript-to-local-performance-script":
        raise FactoryHandoffError("voice sync disposition scope is not local compilation")
    if authorization.get("external_effects_authorized") is not False:
        raise FactoryHandoffError("voice sync disposition authorizes external effects")
    return binding, observed


def _validate_chapter_run_and_decision(
    *,
    handoff_path: Path,
    root: Path,
    identity: dict[str, Any],
    manuscript_gate: dict[str, Any],
    voice_source: dict[str, Any],
    chapter_run_digest: str,
) -> None:
    chapter_run_path = handoff_path.resolve().parent / "chapter-run.json"
    if not chapter_run_path.is_file():
        raise FactoryHandoffError("factory handoff sibling chapter-run.json is missing")
    run_payload = chapter_run_path.read_bytes()
    run = _json_document(run_payload, "factory chapter run")
    try:
        observed_run_digest = canonical_sha256(cast(JsonValue, run))
    except (TypeError, ValueError) as error:
        raise FactoryHandoffError("factory chapter run is not canonicalizable") from error
    if observed_run_digest != chapter_run_digest:
        raise FactoryHandoffError("factory chapter run digest does not match handoff")
    if run.get("identity") != identity:
        raise FactoryHandoffError("factory chapter run identity does not match handoff")
    manuscript = run.get("manuscript")
    if type(manuscript) is not dict:
        raise FactoryHandoffError("factory chapter run manuscript must be an object")
    if manuscript.get("decision_state") != "accepted":
        raise FactoryHandoffError("factory chapter run manuscript is not author accepted")
    if manuscript.get("sha256") != manuscript_gate["expected_sha256"]:
        raise FactoryHandoffError("factory chapter run manuscript digest does not match handoff")
    if manuscript.get("decision_receipt_ref") != manuscript_gate["decision_receipt_ref"]:
        raise FactoryHandoffError("factory chapter run decision receipt does not match handoff")
    if run.get("effects") != {}:
        raise FactoryHandoffError("factory chapter run declares effects")
    derivatives = run.get("derivatives")
    derivative = (
        derivatives.get("motion-comic-voiceover")
        if type(derivatives) is dict
        else None
    )
    if type(derivative) is not dict or derivative.get("state") != "eligible":
        raise FactoryHandoffError("factory chapter run voice derivative is not eligible")
    binding = derivative.get("binding")
    if type(binding) is not dict or binding.get("source_id") != voice_source["id"]:
        raise FactoryHandoffError("factory chapter run voice source id does not match")
    if binding.get("source_digest") != voice_source["sha256"]:
        raise FactoryHandoffError("factory chapter run voice source digest does not match")

    _, decision_path = _bound_repository_file(
        manuscript_gate["decision_receipt_ref"], root, "factory author decision"
    )
    decision_payload = decision_path.read_bytes()
    decision = _json_document(decision_payload, "factory author decision")
    if decision.get("schema_version") != AUTHOR_DECISION_SCHEMA:
        raise FactoryHandoffError("unsupported factory author decision schema")
    if decision.get("decision_state") != "accepted":
        raise FactoryHandoffError("factory author decision is not accepted")
    for field in ("project_id", "chapter_id", "run_id"):
        if decision.get(field) != identity[field]:
            raise FactoryHandoffError(f"factory author decision {field} does not match")
    decision_manuscript = decision.get("manuscript")
    if type(decision_manuscript) is not dict or decision_manuscript.get("sha256") != manuscript_gate["expected_sha256"]:
        raise FactoryHandoffError("factory author decision manuscript does not match")
    authority = decision.get("authority")
    if type(authority) is not dict or authority.get("external_effects_authorized") is not False:
        raise FactoryHandoffError("factory author decision authorizes external effects")
    decision_id = _text(decision.get("decision_id"), "factory author decision.decision_id")
    receipts = run.get("receipts")
    expected_receipt = {
        "id": decision_id,
        "sha256": _sha256(decision_payload),
    }
    if type(receipts) is not list or expected_receipt not in receipts:
        raise FactoryHandoffError("factory chapter run does not bind the author decision bytes")


def validate_factory_handoff(
    handoff_bytes: bytes,
    *,
    handoff_path: Path,
    repository_root: Path,
    source_path: Path,
    source_bytes: bytes,
    compiler_config_path: Path,
    compiler_config_bytes: bytes,
    compiler_config: CompilerConfig,
) -> LocalCompileAdmission:
    """Validate one exact accepted-manuscript, local-compile-only admission."""

    config = require_normalized_config(compiler_config)
    root = _repository_root(repository_root)
    _argument_locator(handoff_path, root, "factory handoff")
    source_locator = _argument_locator(source_path, root, "voice source")
    config_locator = _argument_locator(
        compiler_config_path, root, "voice compiler config"
    )
    document = _json_document(handoff_bytes, "factory handoff")
    handoff = _closed(
        document,
        "factory handoff",
        {
            "schema_version",
            "identity",
            "chapter_run_digest",
            "manuscript_gate",
            "voice_source",
            "compiler_config",
            "sync_disposition",
            "derivative",
            "admission",
            "transport",
            "authority_effect",
            "external_effects",
        },
    )
    if handoff["schema_version"] != HANDOFF_SCHEMA:
        raise FactoryHandoffError("unsupported factory handoff schema")
    identity = _closed(
        handoff["identity"],
        "factory handoff identity",
        {"project_id", "chapter_id", "run_id"},
    )
    project_id = _text(identity["project_id"], "factory handoff identity.project_id")
    chapter_id = _text(identity["chapter_id"], "factory handoff identity.chapter_id")
    run_id = _text(identity["run_id"], "factory handoff identity.run_id")
    chapter_run_digest = _digest(
        handoff["chapter_run_digest"], "factory handoff chapter_run_digest"
    )
    manuscript_gate = _closed(
        handoff["manuscript_gate"],
        "factory handoff manuscript_gate",
        {"expected_sha256", "decision_state", "decision_receipt_ref"},
    )
    manuscript_sha256 = _digest(
        manuscript_gate["expected_sha256"],
        "factory handoff manuscript_gate.expected_sha256",
    )
    if manuscript_gate["decision_state"] != "accepted":
        raise FactoryHandoffError("factory handoff manuscript gate is not accepted")
    _text(
        manuscript_gate["decision_receipt_ref"],
        "factory handoff manuscript_gate.decision_receipt_ref",
    )
    voice_source = _source_binding(
        handoff["voice_source"],
        root=root,
        expected_locator=source_locator,
        payload=source_bytes,
    )
    _config_binding(
        handoff["compiler_config"],
        root=root,
        expected_locator=config_locator,
        payload=compiler_config_bytes,
        config=config,
    )
    if config.source_locator != source_locator:
        raise FactoryHandoffError("compiler config source locator does not match CLI input")
    if config.expected_source_sha256 != voice_source["sha256"]:
        raise FactoryHandoffError("compiler config source digest does not match handoff")
    _, sync_digest = _sync_binding(
        handoff["sync_disposition"],
        root=root,
        project_id=project_id,
        chapter_id=chapter_id,
        manuscript_sha256=manuscript_sha256,
    )
    derivative = _closed(
        handoff["derivative"],
        "factory handoff derivative",
        {"profile", "status"},
    )
    if derivative != {
        "profile": "motion-comic-voiceover",
        "status": "local-compile-ready",
    }:
        raise FactoryHandoffError("factory handoff derivative is not local-compile-ready")
    admission = _closed(
        handoff["admission"],
        "factory handoff admission",
        {"state", "scope", "reason"},
    )
    if admission != {
        "state": "eligible",
        "scope": "local-compile-only",
        "reason": "accepted_manuscript_and_synchronized_script",
    }:
        raise FactoryHandoffError("factory handoff does not grant local compile admission")
    if handoff["transport"] != "local-repository-data-only":
        raise FactoryHandoffError("factory handoff transport is not local-only")
    if handoff["authority_effect"] != "none":
        raise FactoryHandoffError("factory handoff claims an authority effect")
    effects = _closed(
        handoff["external_effects"],
        "factory handoff external_effects",
        {"network", "provider", "secret_access", "media_generation", "publication"},
    )
    if any(value is not False for value in effects.values()):
        raise FactoryHandoffError("factory handoff permits an external effect")
    _validate_chapter_run_and_decision(
        handoff_path=handoff_path,
        root=root,
        identity=identity,
        manuscript_gate=manuscript_gate,
        voice_source=voice_source,
        chapter_run_digest=chapter_run_digest,
    )
    return LocalCompileAdmission(
        project_id=project_id,
        chapter_id=chapter_id,
        run_id=run_id,
        chapter_run_digest=chapter_run_digest,
        handoff_sha256=_sha256(handoff_bytes),
        source_sha256=_sha256(source_bytes),
        compiler_config_sha256=_sha256(compiler_config_bytes),
        sync_disposition_sha256=sync_digest,
    )


__all__ = [
    "FactoryHandoffError",
    "HANDOFF_SCHEMA",
    "LocalCompileAdmission",
    "validate_factory_handoff",
]
