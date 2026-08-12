"""Pure L1 static projection for the ElevenLabs direct-TTS request shape.

This module produces deterministic redacted request snapshots from a canonical
manifest and a caller-supplied pinned schema basis.  It has no transport,
credential, file, audio, or provider-client behavior.  A returned projection
is evidence of local request-shape mapping only; account and live-effect facts
remain explicitly unknown.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Callable, Mapping, cast

from .canonical import (
    JsonValue,
    canonical_bytes,
    canonical_clone,
    canonical_loads,
    canonical_sha256,
    require_valid_envelope,
)
from .contracts import MANIFEST_SCHEMA_ID
from .port import (
    FrozenEnvelope,
    PortContractError,
    build_capability_query,
    evaluate_capabilities,
    prepare_segment_plan,
)


STATIC_SCHEMA_BASIS_ID = "elevenlabs-direct-tts-static-schema/v1"
STATIC_ADAPTER_ID = "elevenlabs-direct-tts-static-projector"
STATIC_ADAPTER_VERSION = "1"
STATIC_TRANSPORT_MODE = "elevenlabs-direct-tts-static/v1"
STATIC_REQUEST_CAPABILITY = "documented-direct-tts-request-shape"
STATIC_SNAPSHOT_SCHEMA = "elevenlabs-direct-tts-static-snapshot/v1"
L2_UNKNOWN_REQUIREMENTS = (
    "account-entitlement",
    "live-account-evidence",
    "live-model-availability",
    "live-voice-binding-availability",
    "provider-submission",
    "provider-response",
    "audio-artifact",
    "cost-and-latency",
)


class StaticProjectionError(PortContractError):
    """Raised when a static-projection-only invariant is violated."""


@dataclass(frozen=True, slots=True)
class StaticProjection:
    """Immutable bindings for one redacted direct-TTS static projection."""

    query: FrozenEnvelope
    profile: FrozenEnvelope
    plan: FrozenEnvelope
    l2_prerequisite_query: FrozenEnvelope
    l2_prerequisite_profile: FrozenEnvelope
    schema_sha256: str
    redacted_snapshot_bytes: bytes
    l2_unknown_requirements: tuple[str, ...] = L2_UNKNOWN_REQUIREMENTS

    @property
    def redacted_snapshots(self) -> list[dict[str, JsonValue]]:
        """Return detached, redacted snapshot objects in manifest order."""

        parsed = canonical_loads(self.redacted_snapshot_bytes)
        if type(parsed) is not list:
            raise StaticProjectionError("redacted snapshots must be an array")
        snapshots: list[dict[str, JsonValue]] = []
        for item in parsed:
            if type(item) is not dict:
                raise StaticProjectionError("redacted snapshot must be an object")
            snapshots.append(cast(dict[str, JsonValue], canonical_clone(item)))
        return snapshots


def _text(value: object, label: str) -> str:
    if type(value) is not str or not value:
        raise StaticProjectionError(f"{label} must be non-empty text")
    return value


def _object(value: JsonValue, label: str) -> dict[str, JsonValue]:
    if type(value) is not dict:
        raise StaticProjectionError(f"{label} must be an object")
    return cast(dict[str, JsonValue], canonical_clone(value))


def _text_list(value: JsonValue, label: str) -> list[str]:
    if type(value) is not list or any(type(item) is not str for item in value):
        raise StaticProjectionError(f"{label} must be an array of text")
    return [cast(str, item) for item in value]


def _json_object_without_duplicate_keys(
    pairs: list[tuple[str, JsonValue]],
) -> dict[str, JsonValue]:
    result: dict[str, JsonValue] = {}
    for key, value in pairs:
        if key in result:
            raise StaticProjectionError(f"schema basis duplicates key {key!r}")
        result[key] = value
    return result


def load_pinned_schema_basis(schema_bytes: bytes) -> dict[str, JsonValue]:
    """Validate one canonical, local documentation-shape snapshot.

    The caller owns reading the bytes.  Keeping this loader byte-oriented makes
    the snapshot digest an exact, reviewable input and avoids a hidden file I/O
    dependency in the projector.
    """

    if type(schema_bytes) is not bytes:
        raise StaticProjectionError("schema basis must be exact bytes")
    try:
        decoded = schema_bytes.decode("utf-8", errors="strict")
        parsed = json.loads(
            decoded,
            object_pairs_hook=_json_object_without_duplicate_keys,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, StaticProjectionError) as exc:
        raise StaticProjectionError("schema basis must be valid UTF-8 JSON") from exc
    basis = _object(cast(JsonValue, parsed), "schema basis")
    if basis.get("basis_id") != STATIC_SCHEMA_BASIS_ID:
        raise StaticProjectionError("unexpected static schema basis id")
    if basis.get("claim_ceiling") != "static-request-shape-only":
        raise StaticProjectionError("schema basis must retain the static claim ceiling")
    _text(basis.get("provider"), "schema basis provider")
    _text(basis.get("snapshot_locator"), "schema basis snapshot_locator")

    source = _object(basis.get("source"), "schema basis source")
    _text(source.get("locator"), "schema basis source locator")
    _text(source.get("retrieved_on"), "schema basis retrieval date")

    request = _object(basis.get("request"), "schema basis request")
    if request.get("method") != "POST":
        raise StaticProjectionError("static schema method must be POST")
    if request.get("path_template") != "/v1/text-to-speech/{voice_id}":
        raise StaticProjectionError("static schema path template is unsupported")
    body = _object(request.get("body"), "schema basis request body")
    if _text_list(body.get("required_fields"), "required body fields") != ["text"]:
        raise StaticProjectionError("static schema must require exactly text")
    optional_fields = _text_list(body.get("optional_fields"), "optional body fields")
    if optional_fields != sorted(optional_fields):
        raise StaticProjectionError("optional body fields must be sorted")
    headers = _object(request.get("headers"), "schema basis request headers")
    if headers.get("content_type") != "application/json":
        raise StaticProjectionError("static schema content type is unsupported")
    return basis


def _selected_segments(
    manifest: Mapping[str, JsonValue], selected_segment_ids: list[str]
) -> list[dict[str, JsonValue]]:
    if type(manifest) is not dict:
        raise StaticProjectionError("manifest envelope must be an object")
    envelope = cast(dict[str, JsonValue], canonical_clone(dict(manifest)))
    require_valid_envelope(envelope)
    if envelope.get("schema_id") != MANIFEST_SCHEMA_ID:
        raise StaticProjectionError("static projection requires a manifest envelope")
    if type(selected_segment_ids) is not list or not selected_segment_ids:
        raise StaticProjectionError("selected segment ids must be non-empty")
    if any(type(item) is not str or not item for item in selected_segment_ids):
        raise StaticProjectionError("selected segment ids must be non-empty text")
    if len(set(selected_segment_ids)) != len(selected_segment_ids):
        raise StaticProjectionError("selected segment ids must be unique")

    value = _object(envelope.get("value"), "manifest value")
    raw_segments = value.get("segments")
    if type(raw_segments) is not list:
        raise StaticProjectionError("manifest segments must be an array")
    selected = set(selected_segment_ids)
    result: list[dict[str, JsonValue]] = []
    for raw in raw_segments:
        if type(raw) is not dict:
            raise StaticProjectionError("manifest segment must be an object")
        segment = cast(dict[str, JsonValue], canonical_clone(raw))
        segment_id = _text(segment.get("segment_id"), "manifest segment id")
        if segment_id in selected:
            result.append(segment)
    observed = {cast(str, segment["segment_id"]) for segment in result}
    missing = sorted(selected - observed)
    if missing:
        raise StaticProjectionError(f"selected segments are missing: {missing}")
    return result


def _binding_descriptor(
    segments: list[dict[str, JsonValue]], binding_refs: Mapping[str, str]
) -> tuple[dict[str, JsonValue], dict[str, str]]:
    if type(binding_refs) is not dict:
        raise StaticProjectionError("voice binding refs must be an object")
    required_speakers = sorted(
        {_text(segment.get("speaker"), "manifest speaker") for segment in segments}
    )
    provided_speakers = sorted(binding_refs)
    if provided_speakers != required_speakers:
        raise StaticProjectionError(
            "voice binding refs must cover exactly the selected speakers"
        )
    bindings = {
        speaker: _text(binding_refs[speaker], f"voice binding ref for {speaker}")
        for speaker in required_speakers
    }
    descriptor: dict[str, JsonValue] = {
        "binding_mode": "opaque-slot/v1",
        "binding_ref_sha256_by_speaker": {
            speaker: hashlib.sha256(bindings[speaker].encode("utf-8")).hexdigest()
            for speaker in required_speakers
        },
        "model_settings_state": "unbound",
        "live_account_state": "unknown",
    }
    return descriptor, bindings


def project_direct_tts_static(
    manifest: Mapping[str, JsonValue],
    *,
    selected_segment_ids: list[str],
    schema_basis_bytes: bytes,
    voice_binding_refs: Mapping[str, str],
    secret_resolver: Callable[..., object] | None = None,
) -> StaticProjection:
    """Build a no-effect direct-TTS request-shape projection.

    ``secret_resolver`` deliberately exists only as a boundary probe.  It is
    never invoked because credential resolution belongs to a separately gated
    L2 execution path.
    """

    _ = secret_resolver
    basis = load_pinned_schema_basis(schema_basis_bytes)
    schema_sha256 = hashlib.sha256(schema_basis_bytes).hexdigest()
    schema_locator = _text(basis.get("snapshot_locator"), "schema snapshot locator")
    request = _object(basis.get("request"), "schema basis request")
    body = _object(request.get("body"), "schema basis request body")
    segments = _selected_segments(manifest, selected_segment_ids)
    descriptor, bindings = _binding_descriptor(segments, voice_binding_refs)

    query = build_capability_query(
        manifest,
        selected_segment_ids=selected_segment_ids,
        required_capabilities=[STATIC_REQUEST_CAPABILITY],
        transport_mode=STATIC_TRANSPORT_MODE,
        adapter_id=STATIC_ADAPTER_ID,
        adapter_version=STATIC_ADAPTER_VERSION,
        schema_locator=schema_locator,
        schema_sha256=schema_sha256,
        binding_model_settings_descriptor=descriptor,
    )
    profile = evaluate_capabilities(
        query.as_envelope(),
        statuses={STATIC_REQUEST_CAPABILITY: "supported"},
        evidence_basis=[
            {
                "evidence_id": "documentation-schema-basis-001",
                "kind": "pinned-documentation-request-shape",
                "locator": _text(
                    _object(basis.get("source"), "schema basis source").get("locator"),
                    "schema basis source locator",
                ),
                "snapshot_locator": schema_locator,
                "sha256": schema_sha256,
                "live_account_evidence": False,
                "claim_ceiling": "static-request-shape-only",
            }
        ],
        output_granularity="segment",
    )
    l2_prerequisite_query = build_capability_query(
        manifest,
        selected_segment_ids=selected_segment_ids,
        required_capabilities=list(L2_UNKNOWN_REQUIREMENTS),
        transport_mode=STATIC_TRANSPORT_MODE,
        adapter_id=STATIC_ADAPTER_ID,
        adapter_version=STATIC_ADAPTER_VERSION,
        schema_locator=schema_locator,
        schema_sha256=schema_sha256,
        binding_model_settings_descriptor=descriptor,
    )
    l2_prerequisite_profile = evaluate_capabilities(
        l2_prerequisite_query.as_envelope(),
        statuses={requirement: "unknown" for requirement in L2_UNKNOWN_REQUIREMENTS},
        evidence_basis=[
            {
                "evidence_id": "l2-prerequisite-unproven-001",
                "kind": "static-unknowns-only",
                "locator": schema_locator,
                "sha256": schema_sha256,
                "live_account_evidence": False,
                "claim_ceiling": "no-live-provider-claim",
            }
        ],
        output_granularity="segment",
    )
    plan = prepare_segment_plan(
        manifest,
        query.as_envelope(),
        profile.as_envelope(),
        output_descriptor="elevenlabs-direct-tts-static-request/v1",
        secret_resolver=secret_resolver,
    )

    raw_operations = plan.value.get("operations")
    if type(raw_operations) is not list or len(raw_operations) != len(segments):
        raise StaticProjectionError("static plan operations do not match selection")
    snapshots: list[dict[str, JsonValue]] = []
    body_field_names = _text_list(body.get("required_fields"), "required body fields")
    for segment, raw_operation in zip(segments, raw_operations, strict=True):
        if type(raw_operation) is not dict:
            raise StaticProjectionError("static plan operation must be an object")
        operation = cast(dict[str, JsonValue], raw_operation)
        segment_id = _text(segment.get("segment_id"), "manifest segment id")
        speaker = _text(segment.get("speaker"), "manifest speaker")
        exact_text = _text(segment.get("exact_text"), "manifest exact text")
        binding_ref = bindings[speaker]
        native_request_material: dict[str, JsonValue] = {
            "body": {"text": exact_text},
            "method": _text(request.get("method"), "schema request method"),
            "path_template": _text(
                request.get("path_template"), "schema request path template"
            ),
            "voice_binding_ref": binding_ref,
        }
        snapshots.append(
            {
                "adapter_id": STATIC_ADAPTER_ID,
                "adapter_version": STATIC_ADAPTER_VERSION,
                "body_field_names": body_field_names,
                "exact_text_sha256": _text(
                    segment.get("exact_text_sha256"), "manifest exact text digest"
                ),
                "method": native_request_material["method"],
                "native_request_sha256": canonical_sha256(native_request_material),
                "path_template": native_request_material["path_template"],
                "plan_operation_fingerprint": _text(
                    operation.get("operation_fingerprint"), "plan operation fingerprint"
                ),
                "schema_locator": schema_locator,
                "schema_sha256": schema_sha256,
                "segment_id": segment_id,
                "snapshot_schema": STATIC_SNAPSHOT_SCHEMA,
                "speaker": speaker,
                "utf8_bytes": len(exact_text.encode("utf-8")),
                "voice_binding_ref_sha256": hashlib.sha256(
                    binding_ref.encode("utf-8")
                ).hexdigest(),
            }
        )
    return StaticProjection(
        query=query,
        profile=profile,
        plan=plan,
        l2_prerequisite_query=l2_prerequisite_query,
        l2_prerequisite_profile=l2_prerequisite_profile,
        schema_sha256=schema_sha256,
        redacted_snapshot_bytes=canonical_bytes(snapshots),
    )
