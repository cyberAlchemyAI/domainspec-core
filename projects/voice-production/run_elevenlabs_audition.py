#!/usr/bin/env python3
"""Validate or execute one explicitly bounded ElevenLabs audition request."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, cast
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "projects/voice-production"))

from voice_production.canonical import (  # noqa: E402
    JsonValue,
    canonical_bytes,
    make_envelope,
)
from voice_production.compiler import compile_manifest  # noqa: E402
from voice_production.compiler_config import (  # noqa: E402
    compiler_config_from_json_bytes,
)
from voice_production.elevenlabs_live import (  # noqa: E402
    DirectTtsRequest,
    synthesize_direct_tts,
)


CONFIG_SCHEMA = "voice-production.elevenlabs-live-audition/v1"
CONFIG_SCHEMAS = frozenset(
    {CONFIG_SCHEMA, "voice-production.elevenlabs-live-audition/v2"}
)
RECEIPT_SCHEMA = "voice-production.elevenlabs-live-audition-receipt"


class AuditionConfigError(ValueError):
    pass


def _closed(value: object, label: str, fields: set[str]) -> dict[str, Any]:
    if type(value) is not dict:
        raise AuditionConfigError(f"{label} must be an object")
    result = cast(dict[str, Any], value)
    missing = sorted(fields - set(result))
    unknown = sorted(set(result) - fields)
    if missing or unknown:
        raise AuditionConfigError(
            f"{label} field mismatch; missing={missing}, unknown={unknown}"
        )
    return result


def _closed_optional(
    value: object,
    label: str,
    required: set[str],
    optional: set[str],
) -> dict[str, Any]:
    if type(value) is not dict:
        raise AuditionConfigError(f"{label} must be an object")
    result = cast(dict[str, Any], value)
    missing = sorted(required - set(result))
    unknown = sorted(set(result) - required - optional)
    if missing or unknown:
        raise AuditionConfigError(
            f"{label} field mismatch; missing={missing}, unknown={unknown}"
        )
    return result


def _text(value: object, label: str) -> str:
    if type(value) is not str or not value or value.strip() != value:
        raise AuditionConfigError(f"{label} must be non-empty trimmed text")
    return value


def _integer(value: object, label: str) -> int:
    if type(value) is not int or value < 1:
        raise AuditionConfigError(f"{label} must be a positive integer")
    return value


def _require_current_authorization_date(
    authorized_on: object,
    timezone_name: object,
    *,
    now_utc: datetime | None = None,
) -> None:
    authorized_text = _text(authorized_on, "authorized_on")
    timezone_text = _text(timezone_name, "authorization timezone")
    try:
        authorized_date = datetime.strptime(authorized_text, "%Y-%m-%d").date()
    except ValueError as error:
        raise AuditionConfigError("authorized_on must use YYYY-MM-DD") from error
    try:
        authorization_zone = ZoneInfo(timezone_text)
    except ZoneInfoNotFoundError as error:
        raise AuditionConfigError("authorization timezone is unknown") from error
    instant = datetime.now(UTC) if now_utc is None else now_utc
    if instant.tzinfo is None:
        raise AuditionConfigError("authorization clock must be timezone-aware")
    current_date = instant.astimezone(authorization_zone).date()
    if authorized_date != current_date:
        raise AuditionConfigError("paid audition authorization is not current")


def _relative_path(root: Path, value: object, label: str) -> Path:
    text = _text(value, label)
    relative = Path(text)
    if relative.is_absolute() or ".." in relative.parts:
        raise AuditionConfigError(f"{label} must be a repository-relative path")
    resolved = (root / relative).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise AuditionConfigError(f"{label} escapes the repository") from error
    return resolved


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _write_once(path: Path, payload: bytes, *, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes().decode("utf-8", errors="strict"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditionConfigError(f"cannot load audition config: {path}") from error
    if type(value) is not dict:
        raise AuditionConfigError("audition config must be an object")
    return cast(dict[str, Any], value)


def build_receipt_artifact(
    value: dict[str, JsonValue],
) -> tuple[dict[str, JsonValue], bytes]:
    """Return a canonical receipt envelope and its exact no-suffix bytes."""

    receipt = make_envelope(RECEIPT_SCHEMA, value, schema_version="1")
    return receipt, canonical_bytes(receipt)


def _prepare(config_path: Path, repository_root: Path) -> tuple[
    dict[str, Any], DirectTtsRequest, Path, Path, str
]:
    config_bytes = config_path.read_bytes()
    config_digest = _sha256(config_bytes)
    config = _closed(
        _load_json(config_path),
        "audition config",
        {
            "authorization",
            "identity",
            "output",
            "provider",
            "schema_version",
            "secret",
            "selection",
            "source",
        },
    )
    if config["schema_version"] not in CONFIG_SCHEMAS:
        raise AuditionConfigError("unsupported audition config schema")

    identity = _closed(
        config["identity"],
        "identity",
        {"chapter_id", "project_id", "purpose", "run_id"},
    )
    if identity["purpose"] not in {
        "connectivity-only-not-cast",
        "quality-audition-not-cast",
    }:
        raise AuditionConfigError("identity purpose must remain non-canonical")

    source = _closed(
        config["source"],
        "source",
        {
            "compiler_config_path",
            "compiler_config_sha256",
            "csv_path",
            "csv_sha256",
            "manifest_digest",
        },
    )
    csv_path = _relative_path(repository_root, source["csv_path"], "source csv_path")
    compiler_path = _relative_path(
        repository_root,
        source["compiler_config_path"],
        "source compiler_config_path",
    )
    csv_bytes = csv_path.read_bytes()
    compiler_bytes = compiler_path.read_bytes()
    if _sha256(csv_bytes) != source["csv_sha256"]:
        raise AuditionConfigError("source CSV digest mismatch")
    if _sha256(compiler_bytes) != source["compiler_config_sha256"]:
        raise AuditionConfigError("compiler config digest mismatch")
    manifest = compile_manifest(
        csv_bytes,
        config=compiler_config_from_json_bytes(compiler_bytes),
    )
    if manifest.digest != source["manifest_digest"]:
        raise AuditionConfigError("compiled manifest digest mismatch")

    selection = _closed(
        config["selection"],
        "selection",
        {"exact_text_sha256", "max_characters", "segment_id", "speaker"},
    )
    selected = [
        item
        for item in manifest.value["segments"]
        if item["segment_id"] == selection["segment_id"]
    ]
    if len(selected) != 1:
        raise AuditionConfigError("selected segment is missing or ambiguous")
    segment = cast(dict[str, JsonValue], selected[0])
    if segment["speaker"] != selection["speaker"]:
        raise AuditionConfigError("selected speaker mismatch")
    if segment["exact_text_sha256"] != selection["exact_text_sha256"]:
        raise AuditionConfigError("selected text digest mismatch")
    exact_text = _text(segment["exact_text"], "selected exact text")
    if len(exact_text) > _integer(selection["max_characters"], "max_characters"):
        raise AuditionConfigError("selected text exceeds the authorized character cap")

    provider = _closed_optional(
        config["provider"],
        "provider",
        {
            "language_code",
            "model_id",
            "output_format",
            "voice_binding_state",
            "voice_id",
            "voice_label",
            "voice_settings",
        },
        {"context", "seed"},
    )
    if provider["voice_binding_state"] not in {
        "non-canonical-connectivity-only",
        "non-canonical-quality-audition",
    }:
        raise AuditionConfigError("provider voice must remain non-canonical")
    settings = _closed_optional(
        provider["voice_settings"],
        "provider voice_settings",
        {"similarity_boost", "stability", "style", "use_speaker_boost"},
        {"speed"},
    )
    previous_text: str | None = None
    next_text: str | None = None
    context_binding: dict[str, JsonValue] | None = None
    if "context" in provider:
        context = _closed(
            provider["context"],
            "provider context",
            {"next_segment_id", "previous_segment_id"},
        )
        segments = cast(list[dict[str, JsonValue]], manifest.value["segments"])
        segment_indexes = {
            item["segment_id"]: index for index, item in enumerate(segments)
        }
        previous_id = _text(context["previous_segment_id"], "previous segment id")
        next_id = _text(context["next_segment_id"], "next segment id")
        selected_index = segment_indexes.get(selection["segment_id"])
        previous_index = segment_indexes.get(previous_id)
        next_index = segment_indexes.get(next_id)
        if (
            selected_index is None
            or previous_index is None
            or next_index is None
            or not previous_index < selected_index < next_index
        ):
            raise AuditionConfigError(
                "context segments must exist and surround the selected segment"
            )
        previous_segment = segments[previous_index]
        next_segment = segments[next_index]
        previous_text = _text(previous_segment["exact_text"], "previous exact text")
        next_text = _text(next_segment["exact_text"], "next exact text")
        context_binding = {
            "next_segment_id": next_id,
            "next_text_sha256": _text(
                next_segment["exact_text_sha256"], "next text digest"
            ),
            "previous_segment_id": previous_id,
            "previous_text_sha256": _text(
                previous_segment["exact_text_sha256"], "previous text digest"
            ),
        }

    language_code = provider["language_code"]
    if language_code is not None:
        language_code = _text(language_code, "language code")
    request = DirectTtsRequest(
        segment_id=_text(segment["segment_id"], "segment id"),
        speaker=_text(segment["speaker"], "speaker"),
        exact_text=exact_text,
        exact_text_sha256=_text(segment["exact_text_sha256"], "text digest"),
        voice_id=_text(provider["voice_id"], "voice id"),
        voice_label=_text(provider["voice_label"], "voice label"),
        model_id=_text(provider["model_id"], "model id"),
        output_format=_text(provider["output_format"], "output format"),
        language_code=language_code,
        stability=settings["stability"],
        similarity_boost=settings["similarity_boost"],
        style=settings["style"],
        use_speaker_boost=settings["use_speaker_boost"],
        speed=settings.get("speed"),
        seed=provider.get("seed"),
        previous_text=previous_text,
        next_text=next_text,
    )

    authorization_fields = {
        "authorized_on",
        "canonical_acceptance_effect",
        "canonical_cast_effect",
        "max_provider_requests",
        "mode",
        "publication",
    }
    if config["schema_version"] == "voice-production.elevenlabs-live-audition/v2":
        authorization_fields.add("timezone")
    authorization = _closed(
        config["authorization"],
        "authorization",
        authorization_fields,
    )
    expected_authorization = {
        "canonical_acceptance_effect": "none",
        "canonical_cast_effect": "none",
        "max_provider_requests": 1,
        "mode": "single-segment-paid-audition",
        "publication": False,
    }
    if {
        key: value
        for key, value in authorization.items()
        if key not in {"authorized_on", "timezone"}
    } != expected_authorization:
        raise AuditionConfigError("authorization must remain the exact one-request audition")
    timezone_name = authorization.get("timezone", "UTC")
    _require_current_authorization_date(
        authorization["authorized_on"], timezone_name
    )

    secret = _closed(config["secret"], "secret", {"logical_name"})
    if secret["logical_name"] != "elevenlabs/api-key":
        raise AuditionConfigError("unexpected secret logical name")
    output = _closed(config["output"], "output", {"audio_path", "receipt_path"})
    audio_path = _relative_path(repository_root, output["audio_path"], "audio_path")
    receipt_path = _relative_path(
        repository_root, output["receipt_path"], "receipt_path"
    )
    if audio_path.suffix != ".mp3" or receipt_path.suffix != ".json":
        raise AuditionConfigError("output extensions must be .mp3 and .json")
    if audio_path.exists() or receipt_path.exists():
        raise FileExistsError("audition outputs already exist; refusing provider retry")
    if context_binding is not None:
        config["_resolved_context_binding"] = context_binding
    return config, request, audio_path, receipt_path, config_digest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("--repo-root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--execute", action="store_true")
    arguments = parser.parse_args(argv)

    root = arguments.repo_root.resolve()
    config_path = arguments.config
    if not config_path.is_absolute():
        config_path = (root / config_path).resolve()
    config, request, audio_path, receipt_path, config_digest = _prepare(
        config_path, root
    )
    if not arguments.execute:
        print(
            json.dumps(
                {
                    "audio_path": str(audio_path.relative_to(root)),
                    "character_count": len(request.exact_text),
                    "config_sha256": config_digest,
                    "context_bound": request.previous_text is not None,
                    "mode": "check",
                    "provider_requests": 0,
                    "request_digest": request.request_digest,
                    "segment_id": request.segment_id,
                    "speed": request.speed,
                    "status": "ready",
                },
                sort_keys=True,
            )
        )
        return 0

    sys.path.insert(0, str(root / "projects/secret-management"))
    from secret_management import SopsAgeStore

    secret_name = cast(dict[str, Any], config["secret"])["logical_name"]
    store = SopsAgeStore()

    def consume_secret(
        request_digest: str, callback: Callable[[memoryview], None]
    ) -> dict[str, JsonValue]:
        return store.consume(
            secret_name,
            callback,
            consumer_id=f"co_{secrets.token_hex(16)}",
            request_digest=request_digest,
        )

    result = synthesize_direct_tts(request, secret_consumer=consume_secret)
    observed_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
    value: dict[str, JsonValue] = {
        "artifact": {
            "media_type": result.content_type,
            "path": str(audio_path.relative_to(root)),
            "sha256": result.audio_sha256,
            "size_bytes": len(result.audio_bytes),
        },
        "authorization": cast(dict[str, JsonValue], config["authorization"]),
        "config_sha256": config_digest,
        "external_effects": {
            "audio_generated": True,
            "network": True,
            "provider_requests": 1,
            "publication": False,
            "secret_access": True,
        },
        "identity": cast(dict[str, JsonValue], config["identity"]),
        "observed_at": observed_at,
        "provider": {
            "model_id": request.model_id,
            "output_format": request.output_format,
            "voice_binding_state": cast(dict[str, Any], config["provider"])[
                "voice_binding_state"
            ],
            "voice_id": request.voice_id,
            "voice_label": request.voice_label,
            "voice_settings": {
                "similarity_boost": request.similarity_boost,
                "speed": request.speed,
                "stability": request.stability,
                "style": request.style,
                "use_speaker_boost": request.use_speaker_boost,
            },
        },
        "provider_observation": result.safe_summary(),
        "selection": {
            "character_count": len(request.exact_text),
            "exact_text_sha256": request.exact_text_sha256,
            "segment_id": request.segment_id,
            "speaker": request.speaker,
        },
        "status": "generated-awaiting-human-listen",
    }
    context_binding = config.get("_resolved_context_binding")
    if type(context_binding) is dict:
        value["context"] = cast(dict[str, JsonValue], context_binding)
    receipt, receipt_bytes = build_receipt_artifact(value)
    _write_once(audio_path, result.audio_bytes, mode=0o600)
    _write_once(receipt_path, receipt_bytes, mode=0o600)
    print(
        json.dumps(
            {
                "audio_path": str(audio_path.relative_to(root)),
                "audio_sha256": result.audio_sha256,
                "audio_size_bytes": len(result.audio_bytes),
                "provider_requests": 1,
                "receipt_digest": receipt["digest"],
                "receipt_path": str(receipt_path.relative_to(root)),
                "status": "generated-awaiting-human-listen",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
