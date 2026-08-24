#!/usr/bin/env python3
"""Derive one no-overwrite Halo WAV master from a live audition receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "projects/voice-production"))

from voice_production.canonical import (  # noqa: E402
    JsonValue,
    canonical_bytes,
    canonical_loads,
    make_envelope,
    require_valid_envelope,
)


PROFILE_SCHEMA = "voice-production.mastering-profile/v1"
PROFILE_SCHEMAS = frozenset(
    {
        PROFILE_SCHEMA,
        "voice-production.mastering-profile/v2",
        "voice-production.mastering-profile/v3",
    }
)
RECEIPT_SCHEMA = "voice-production.mastering-receipt"
SOURCE_RECEIPT_SCHEMA = "voice-production.elevenlabs-live-audition-receipt"
DEFAULT_NODE = Path("/home/vrondelli/.nvm/versions/node/v22.12.0/bin/node")
DEFAULT_PLAYWRIGHT_MODULE = Path(
    "/home/vrondelli/.nvm/versions/node/v22.12.0/lib/node_modules/playwright"
)
DEFAULT_CHROMIUM = Path(
    "/home/vrondelli/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
)
RENDER_SCRIPT = Path(__file__).with_name("render_halo_master.js")


class MasteringError(ValueError):
    pass


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _closed(value: object, label: str, fields: set[str]) -> dict[str, Any]:
    if type(value) is not dict:
        raise MasteringError(f"{label} must be an object")
    result = cast(dict[str, Any], value)
    missing = sorted(fields - set(result))
    unknown = sorted(set(result) - fields)
    if missing or unknown:
        raise MasteringError(
            f"{label} field mismatch; missing={missing}, unknown={unknown}"
        )
    return result


def _text(value: object, label: str) -> str:
    if type(value) is not str or not value or value.strip() != value:
        raise MasteringError(f"{label} must be non-empty trimmed text")
    return value


def _number(
    value: object,
    label: str,
    *,
    minimum: float,
    maximum: float,
) -> float:
    if type(value) not in (int, float):
        raise MasteringError(f"{label} must be a number")
    number = float(value)
    if not minimum <= number <= maximum:
        raise MasteringError(f"{label} must be from {minimum} to {maximum}")
    return number


def _positive_integer(value: object, label: str) -> int:
    if type(value) is not int or value < 1:
        raise MasteringError(f"{label} must be a positive integer")
    return value


def _relative_path(root: Path, value: object, label: str) -> Path:
    relative = Path(_text(value, label))
    if relative.is_absolute() or ".." in relative.parts:
        raise MasteringError(f"{label} must be a repository-relative path")
    resolved = (root / relative).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise MasteringError(f"{label} escapes the repository") from error
    return resolved


def _load_json(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
    try:
        payload = path.read_bytes()
        value = json.loads(payload.decode("utf-8", errors="strict"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise MasteringError(f"cannot load {label}: {path}") from error
    if type(value) is not dict:
        raise MasteringError(f"{label} must be an object")
    return cast(dict[str, Any], value), payload


def load_mastering_profile(path: Path) -> tuple[dict[str, Any], bytes]:
    profile, payload = _load_json(path, "mastering profile")
    profile_fields = {
        "authority",
        "cleanup",
        "dynamics",
        "identity",
        "render",
        "reverb",
        "schema_version",
    }
    if profile.get("schema_version") == "voice-production.mastering-profile/v3":
        profile_fields.update({"performance", "tone"})
    profile = _closed(
        profile,
        "mastering profile",
        profile_fields,
    )
    if profile["schema_version"] not in PROFILE_SCHEMAS:
        raise MasteringError("unsupported mastering profile schema")
    identity = _closed(profile["identity"], "identity", {"name", "profile_id"})
    _text(identity["name"], "profile name")
    _text(identity["profile_id"], "profile id")

    authority = _closed(
        profile["authority"],
        "authority",
        {
            "canonical_acceptance_effect",
            "canonical_cast_effect",
            "publication",
            "purpose",
        },
    )
    if authority != {
        "canonical_acceptance_effect": "none",
        "canonical_cast_effect": "none",
        "publication": False,
        "purpose": "local-quality-audition",
    }:
        raise MasteringError("mastering authority must remain local and non-canonical")

    render = _closed(
        profile["render"],
        "render",
        {"channels", "pcm_bits", "sample_rate_hz", "tail_seconds"},
    )
    if render["channels"] != 2 or render["pcm_bits"] != 24:
        raise MasteringError("render must remain 24-bit stereo PCM")
    if render["sample_rate_hz"] not in {44_100, 48_000}:
        raise MasteringError("render sample_rate_hz must be 44100 or 48000")
    _number(render["tail_seconds"], "tail_seconds", minimum=0.5, maximum=3.0)

    cleanup = _closed(profile["cleanup"], "cleanup", {"dry_highpass_hz"})
    _number(cleanup["dry_highpass_hz"], "dry_highpass_hz", minimum=20, maximum=160)

    dynamics_fields = {
        "attack_ms",
        "knee_db",
        "ratio",
        "release_ms",
        "target_peak_dbfs",
        "threshold_db",
    }
    if profile["schema_version"] in {
        "voice-production.mastering-profile/v2",
        "voice-production.mastering-profile/v3",
    }:
        dynamics_fields.update({"max_makeup_db", "target_rms_dbfs"})
    dynamics = _closed(
        profile["dynamics"],
        "dynamics",
        dynamics_fields,
    )
    _number(dynamics["threshold_db"], "threshold_db", minimum=-40, maximum=-3)
    _number(dynamics["knee_db"], "knee_db", minimum=0, maximum=20)
    _number(dynamics["ratio"], "ratio", minimum=1, maximum=4)
    _number(dynamics["attack_ms"], "attack_ms", minimum=1, maximum=100)
    _number(dynamics["release_ms"], "release_ms", minimum=20, maximum=500)
    _number(
        dynamics["target_peak_dbfs"],
        "target_peak_dbfs",
        minimum=-6,
        maximum=-0.5,
    )
    if profile["schema_version"] in {
        "voice-production.mastering-profile/v2",
        "voice-production.mastering-profile/v3",
    }:
        _number(
            dynamics["target_rms_dbfs"],
            "target_rms_dbfs",
            minimum=-30,
            maximum=-10,
        )
        _number(
            dynamics["max_makeup_db"],
            "max_makeup_db",
            minimum=0,
            maximum=6,
        )

    if profile["schema_version"] == "voice-production.mastering-profile/v3":
        performance = _closed(
            profile["performance"], "performance", {"playback_rate"}
        )
        _number(
            performance["playback_rate"],
            "playback_rate",
            minimum=0.90,
            maximum=1.00,
        )
        tone = _closed(
            profile["tone"],
            "tone",
            {
                "high_shelf_frequency_hz",
                "high_shelf_gain_db",
            },
        )
        _number(
            tone["high_shelf_frequency_hz"],
            "high_shelf_frequency_hz",
            minimum=2500,
            maximum=5000,
        )
        _number(
            tone["high_shelf_gain_db"],
            "high_shelf_gain_db",
            minimum=-2,
            maximum=0,
        )

    reverb = _closed(
        profile["reverb"],
        "reverb",
        {
            "early_reflections_ms",
            "input_highpass_hz",
            "input_lowpass_hz",
            "pre_delay_ms",
            "rt60_seconds",
            "seed_left",
            "seed_right",
            "type",
            "wet_db",
        },
    )
    if reverb["type"] != "deterministic-dark-plate":
        raise MasteringError("unsupported reverb type")
    _number(reverb["pre_delay_ms"], "pre_delay_ms", minimum=0, maximum=100)
    _number(reverb["rt60_seconds"], "rt60_seconds", minimum=0.3, maximum=2.5)
    _number(reverb["wet_db"], "wet_db", minimum=-30, maximum=-10)
    highpass = _number(
        reverb["input_highpass_hz"],
        "input_highpass_hz",
        minimum=20,
        maximum=1000,
    )
    lowpass = _number(
        reverb["input_lowpass_hz"],
        "input_lowpass_hz",
        minimum=2000,
        maximum=18_000,
    )
    if highpass >= lowpass:
        raise MasteringError("reverb input filter frequencies are inverted")
    reflections = reverb["early_reflections_ms"]
    if type(reflections) is not list or len(reflections) != 3:
        raise MasteringError("early_reflections_ms must contain exactly three taps")
    reflection_values = [
        _number(item, "early reflection", minimum=1, maximum=200)
        for item in reflections
    ]
    if reflection_values != sorted(reflection_values) or len(set(reflection_values)) != 3:
        raise MasteringError("early reflections must be unique and ascending")
    for key in ("seed_left", "seed_right"):
        seed = _positive_integer(reverb[key], key)
        if seed > 4_294_967_295:
            raise MasteringError(f"{key} exceeds uint32")
    if reverb["seed_left"] == reverb["seed_right"]:
        raise MasteringError("stereo reverb seeds must differ")
    return profile, payload


def _write_once(path: Path, payload: bytes, *, mode: int = 0o600) -> None:
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


def _load_source_receipt(
    path: Path,
    root: Path,
) -> tuple[dict[str, JsonValue], dict[str, JsonValue], Path, bytes]:
    try:
        payload = path.read_bytes()
        parsed = canonical_loads(payload)
    except Exception as error:
        raise MasteringError("source receipt is not canonical valid JSON") from error
    if type(parsed) is not dict:
        raise MasteringError("source receipt must be an envelope")
    envelope = cast(dict[str, JsonValue], parsed)
    require_valid_envelope(envelope)
    if (
        envelope["schema_id"] != SOURCE_RECEIPT_SCHEMA
        or envelope["schema_version"] != "1"
    ):
        raise MasteringError("source receipt schema is not a live audition receipt")
    value = envelope["value"]
    if type(value) is not dict:
        raise MasteringError("source receipt value must be an object")
    receipt_value = cast(dict[str, JsonValue], value)
    if receipt_value.get("status") != "generated-awaiting-human-listen":
        raise MasteringError("source audition is not awaiting human listening")
    artifact = receipt_value.get("artifact")
    if type(artifact) is not dict:
        raise MasteringError("source receipt artifact is missing")
    artifact_value = cast(dict[str, JsonValue], artifact)
    if artifact_value.get("media_type") not in {"audio/mpeg", "audio/mp3"}:
        raise MasteringError("source artifact is not MP3 audio")
    source_path = _relative_path(root, artifact_value.get("path"), "source artifact path")
    source_bytes = source_path.read_bytes()
    if _sha256(source_bytes) != artifact_value.get("sha256"):
        raise MasteringError("source audio digest does not match its receipt")
    if len(source_bytes) != artifact_value.get("size_bytes"):
        raise MasteringError("source audio size does not match its receipt")
    if not (
        source_bytes.startswith(b"ID3")
        or (len(source_bytes) > 1 and source_bytes[0] == 0xFF and source_bytes[1] & 0xE0 == 0xE0)
    ):
        raise MasteringError("source artifact does not have an MP3 signature")
    return envelope, receipt_value, source_path, source_bytes


def _require_wav(payload: bytes, profile: dict[str, Any]) -> None:
    if len(payload) < 44 or payload[:4] != b"RIFF" or payload[8:12] != b"WAVE":
        raise MasteringError("renderer did not produce a RIFF/WAVE artifact")
    audio_format, channels, sample_rate = struct.unpack_from("<HHI", payload, 20)
    bits_per_sample = struct.unpack_from("<H", payload, 34)[0]
    data_size = struct.unpack_from("<I", payload, 40)[0]
    render = cast(dict[str, Any], profile["render"])
    if (
        audio_format != 1
        or channels != render["channels"]
        or sample_rate != render["sample_rate_hz"]
        or bits_per_sample != render["pcm_bits"]
        or data_size != len(payload) - 44
    ):
        raise MasteringError("renderer WAV structure does not match the profile")


def build_master_receipt_artifact(
    value: dict[str, JsonValue],
) -> tuple[dict[str, JsonValue], bytes]:
    receipt = make_envelope(RECEIPT_SCHEMA, value, schema_version="1")
    return receipt, canonical_bytes(receipt)


def _runtime_info(node: Path, playwright_module: Path, chromium: Path) -> dict[str, JsonValue]:
    for label, path in (
        ("node", node),
        ("Playwright module", playwright_module),
        ("Chromium", chromium),
        ("render script", RENDER_SCRIPT),
    ):
        if not path.exists():
            raise MasteringError(f"{label} runtime path is missing: {path}")
    node_version = subprocess.run(
        [str(node), "--version"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    package, _ = _load_json(playwright_module / "package.json", "Playwright package")
    return {
        "chromium_executable": str(chromium),
        "chromium_executable_sha256": _file_sha256(chromium),
        "node_executable": str(node),
        "node_executable_sha256": _file_sha256(node),
        "node_version": node_version,
        "playwright_module": str(playwright_module),
        "playwright_version": _text(package.get("version"), "Playwright version"),
        "render_script_sha256": _file_sha256(RENDER_SCRIPT),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_receipt", type=Path)
    parser.add_argument("profile", type=Path)
    parser.add_argument("output_audio", type=Path)
    parser.add_argument("output_receipt", type=Path)
    parser.add_argument("--repo-root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--node", type=Path, default=DEFAULT_NODE)
    parser.add_argument("--playwright-module", type=Path, default=DEFAULT_PLAYWRIGHT_MODULE)
    parser.add_argument("--chromium", type=Path, default=DEFAULT_CHROMIUM)
    parser.add_argument("--execute", action="store_true")
    arguments = parser.parse_args(argv)

    root = arguments.repo_root.resolve()
    source_receipt = arguments.source_receipt
    if not source_receipt.is_absolute():
        source_receipt = (root / source_receipt).resolve()
    profile_path = arguments.profile
    if not profile_path.is_absolute():
        profile_path = (root / profile_path).resolve()
    output_audio = _relative_path(root, str(arguments.output_audio), "output_audio")
    output_receipt = _relative_path(root, str(arguments.output_receipt), "output_receipt")
    if output_audio.suffix != ".wav" or output_receipt.suffix != ".json":
        raise MasteringError("master outputs must use .wav and .json")
    if output_audio.exists() or output_receipt.exists():
        raise FileExistsError("master outputs already exist; refusing overwrite")

    profile, profile_bytes = load_mastering_profile(profile_path)
    source_envelope, source_value, source_path, source_bytes = _load_source_receipt(
        source_receipt, root
    )
    runtime = _runtime_info(
        arguments.node.resolve(),
        arguments.playwright_module.resolve(),
        arguments.chromium.resolve(),
    )
    if not arguments.execute:
        print(
            json.dumps(
                {
                    "mode": "check",
                    "network": False,
                    "output_audio": str(output_audio.relative_to(root)),
                    "profile_sha256": _sha256(profile_bytes),
                    "provider_requests": 0,
                    "source_audio_sha256": _sha256(source_bytes),
                    "status": "ready",
                },
                sort_keys=True,
            )
        )
        return 0

    output_audio.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output_audio.name}.render.", dir=output_audio.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    temporary.unlink()
    try:
        completed = subprocess.run(
            [
                str(arguments.node.resolve()),
                str(RENDER_SCRIPT),
                str(source_path),
                str(temporary),
                str(profile_path),
                str(arguments.playwright_module.resolve()),
                str(arguments.chromium.resolve()),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if completed.returncode != 0:
            safe_error = completed.stderr.strip().splitlines()[-1:]
            suffix = f": {safe_error[0]}" if safe_error else ""
            raise MasteringError(f"offline renderer failed{suffix}")
        try:
            renderer = json.loads(completed.stdout)
        except json.JSONDecodeError as error:
            raise MasteringError("offline renderer returned invalid metadata") from error
        if type(renderer) is not dict or renderer.get("status") != "rendered":
            raise MasteringError("offline renderer did not report rendered status")
        master_bytes = temporary.read_bytes()
    finally:
        temporary.unlink(missing_ok=True)

    _require_wav(master_bytes, profile)
    if renderer.get("output_size_bytes") != len(master_bytes):
        raise MasteringError("renderer output size metadata mismatch")
    metrics = renderer.get("metrics")
    if type(metrics) is not dict:
        raise MasteringError("renderer metrics are missing")
    runtime["browser_version"] = _text(renderer.get("browser_version"), "browser version")
    source_identity = source_value.get("identity")
    if type(source_identity) is not dict:
        raise MasteringError("source receipt identity is missing")
    identity = cast(dict[str, JsonValue], source_identity)
    master_sha256 = _sha256(master_bytes)
    observed_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
    value: dict[str, JsonValue] = {
        "artifact": {
            "channels": 2,
            "encoding": "pcm_s24le",
            "media_type": "audio/wav",
            "path": str(output_audio.relative_to(root)),
            "sample_rate_hz": cast(dict[str, Any], profile["render"])["sample_rate_hz"],
            "sha256": master_sha256,
            "size_bytes": len(master_bytes),
        },
        "authority": cast(dict[str, JsonValue], profile["authority"]),
        "external_effects": {
            "audio_derived": True,
            "network": False,
            "provider_requests": 0,
            "publication": False,
            "secret_access": False,
        },
        "identity": {
            "chapter_id": identity.get("chapter_id"),
            "profile_id": cast(dict[str, JsonValue], profile["identity"])["profile_id"],
            "project_id": identity.get("project_id"),
            "source_run_id": identity.get("run_id"),
        },
        "metrics": cast(dict[str, JsonValue], metrics),
        "observed_at": observed_at,
        "processor": runtime,
        "profile": {
            "path": str(profile_path.relative_to(root)),
            "sha256": _sha256(profile_bytes),
        },
        "source": {
            "artifact_path": str(source_path.relative_to(root)),
            "artifact_sha256": _sha256(source_bytes),
            "receipt_digest": source_envelope["digest"],
            "receipt_path": str(source_receipt.relative_to(root)),
        },
        "status": "mastered-awaiting-human-listen",
    }
    receipt, receipt_bytes = build_master_receipt_artifact(value)
    _write_once(output_audio, master_bytes)
    _write_once(output_receipt, receipt_bytes)
    print(
        json.dumps(
            {
                "audio_path": str(output_audio.relative_to(root)),
                "audio_sha256": master_sha256,
                "audio_size_bytes": len(master_bytes),
                "network": False,
                "provider_requests": 0,
                "receipt_digest": receipt["digest"],
                "receipt_path": str(output_receipt.relative_to(root)),
                "status": "mastered-awaiting-human-listen",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
