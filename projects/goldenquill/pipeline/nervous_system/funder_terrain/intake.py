"""
Funder Terrain: Curated Local Intake

Accepts human-provided local JSON or YAML files describing known funder observations
and normalizes them into deterministic FunderTerrainNormalizedRecord objects.

Hard boundaries (enforced by code structure and poison-pill tests):
- No live web/API fetch.
- No network imports (requests, httpx, urllib, aiohttp, playwright, selenium, etc.).
- No LLM/model imports or calls.
- No candidate sourcing.
- No partner alerts.
- No event bus writes.
- No Scout projection writes.
- No async/concurrency.
- No subprocess/shell calls.
- No export, draft, or submission logic.
"""

import json
import uuid
from pathlib import Path
from typing import Optional, Dict, List, Any

import yaml

from pipeline.nervous_system.funder_terrain.models import (
    FunderTerrainNormalizedRecord,
    FunderTerrainSourceRecord,
)
from pipeline.nervous_system.funder_terrain.rules import (
    FunderTerrainRule,
    load_rules_from_yaml,
    hash_rules,
)
from pipeline.nervous_system.funder_terrain.normalizer import normalize_record

# The single permitted source_type for this intake path.
CURATED_LOCAL_SOURCE_TYPE = "curated_local_file"

# Terms that are forbidden in source_id and source_type values supplied by the caller.
_FORBIDDEN_SOURCE_TERMS = frozenset([
    "http", "https", "api", "web", "url", "scrape", "crawler",
    "llm", "model", "candidate", "partner_alert",
])

# Path to the canonical rule pack shipped with the Funder Terrain module.
_RULES_DIR = Path(__file__).parent / "rules"

_RULE_FILES: Dict[str, str] = {
    "funder_family": "funder_family_rules.yaml",
    "document_type": "document_type_rules.yaml",
    "geography":     "geography_rules.yaml",
    "project":       "project_rules.yaml",
}


def _load_rules() -> Dict[str, List[FunderTerrainRule]]:
    """Load all canonical rule packs. Raises FileNotFoundError if any pack is missing."""
    rules_dict: Dict[str, List[FunderTerrainRule]] = {}
    for key, filename in _RULE_FILES.items():
        rules_dict[key] = load_rules_from_yaml(_RULES_DIR / filename)
    return rules_dict


def _compute_ruleset_sha256(rules_dict: Dict[str, List[FunderTerrainRule]]) -> str:
    """Compute a deterministic hash over all rule packs combined."""
    all_rules: List[FunderTerrainRule] = []
    for key in sorted(rules_dict.keys()):
        all_rules.extend(rules_dict[key])
    return hash_rules(all_rules)


def _validate_path(input_path: Any) -> Path:
    """Ensure input_path is a Path, exists, and is a local file."""
    if not isinstance(input_path, Path):
        raise TypeError(
            f"input_path must be a pathlib.Path, got {type(input_path).__name__!r}"
        )

    # Reject any path whose string representation starts with a URI scheme
    # BEFORE checking existence.
    path_str = str(input_path).lower()
    for term in ["http://", "https://", "http:/", "https:/", "://", "http:", "https:", "ftp:", "s3:", "gs:"]:
        if term in path_str:
            raise ValueError(f"Remote-looking path rejected: {input_path}")

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if not input_path.is_file():
        raise ValueError(f"input_path is not a regular file: {input_path}")

    return input_path


def _validate_source_id(source_id: Any) -> str:
    """Validate source_id: must be a non-empty str with no forbidden terms."""
    if not isinstance(source_id, str) or not source_id.strip():
        raise ValueError("source_id must be a non-empty string.")
    lower = source_id.lower()
    for term in _FORBIDDEN_SOURCE_TERMS:
        if term in lower:
            raise ValueError(
                f"Forbidden term {term!r} detected in source_id: {source_id!r}"
            )
    return source_id.strip()


def _parse_input_file(input_path: Path) -> Dict[str, Any]:
    """Parse a local JSON or YAML file. Returns the top-level dict."""
    suffix = input_path.suffix.lower()
    raw = input_path.read_text(encoding="utf-8")
    if suffix == ".json":
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Malformed JSON in {input_path}: {exc}") from exc
    elif suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(raw)
        except yaml.YAMLError as exc:
            raise ValueError(f"Malformed YAML in {input_path}: {exc}") from exc
    else:
        raise ValueError(
            f"Unsupported file extension {suffix!r}. Only .json and .yaml/.yml are accepted."
        )
    if not isinstance(data, dict):
        raise ValueError(
            f"Input file must deserialize to a JSON object / YAML mapping, got {type(data).__name__!r}"
        )
    return data


def _extract_text_window(data: Dict[str, Any]) -> str:
    """
    Build a deterministic text window from the input record for rule matching.

    The text window concatenates the values of well-known text fields in a
    stable, sorted order so that repeated calls produce identical hashes.
    """
    text_fields = [
        "funder_name", "funder_family", "program_name", "document_type",
        "geography", "notes", "description", "title", "summary",
    ]
    parts = []
    for field in text_fields:
        val = data.get(field)
        if isinstance(val, str) and val.strip():
            parts.append(val.strip())
    # Also include any remaining string values not in the known list,
    # sorted by key for determinism.
    for key in sorted(data.keys()):
        if key not in text_fields:
            val = data[key]
            if isinstance(val, str) and val.strip():
                parts.append(val.strip())
    return " ".join(parts)


def intake_curated_funder_terrain_file(
    input_path: Path,
    output_dir: Optional[Path] = None,
    source_id: Optional[str] = None,
) -> FunderTerrainNormalizedRecord:
    """
    Normalize a single human-provided local file into a FunderTerrainNormalizedRecord.

    Parameters
    ----------
    input_path : Path
        Absolute or relative path to a local .json or .yaml/.yml file
        containing a curated funder observation.
    output_dir : Path | None
        If provided, the normalized record is written as deterministic JSON
        to ``output_dir / <record_id>.json``. The directory must already exist.
        No existing ledgers or production fixtures are mutated.
    source_id : str | None
        Caller-supplied source identifier string. Must not be empty and must
        not contain forbidden terms (http, https, api, web, url, scrape,
        crawler, llm, model, candidate, partner_alert). If None, a stable
        UUID derived from the input path is used.

    Returns
    -------
    FunderTerrainNormalizedRecord
        Fully normalized record with deterministic provenance hashes.
        Records with unresolved metadata gaps have ``review_status.human_review_required``
        set to True.

    Raises
    ------
    TypeError
        If input_path is not a pathlib.Path.
    FileNotFoundError
        If input_path does not exist.
    ValueError
        If input_path points to a remote URI, the file is malformed,
        source_id contains forbidden terms, or source_type validation fails.
    """
    # --- Input validation ---
    validated_path = _validate_path(input_path)

    if source_id is None:
        # Derive a stable, deterministic source_id from the canonical path.
        source_id = str(uuid.uuid5(uuid.NAMESPACE_URL, validated_path.resolve().as_posix()))
    else:
        source_id = _validate_source_id(source_id)

    # --- Parse file ---
    data = _parse_input_file(validated_path)

    # --- Build source provenance ---
    source_record = FunderTerrainSourceRecord(
        source_id=source_id,
        source_type=CURATED_LOCAL_SOURCE_TYPE,
        url_or_local_path=str(validated_path.resolve()),
    )

    # --- Load rules and compute ruleset hash ---
    rules_dict = _load_rules()
    ruleset_sha256 = _compute_ruleset_sha256(rules_dict)

    # --- Build text window for rule matching ---
    text_window = _extract_text_window(data)

    # --- Derive record_id from source_id + path for determinism ---
    record_id = str(uuid.uuid5(
        uuid.NAMESPACE_URL,
        f"{source_id}::{validated_path.resolve().as_posix()}"
    ))

    # --- Normalize through existing Funder Terrain logic ---
    normalized = normalize_record(
        record_id=record_id,
        filename=validated_path.name,
        original_path=str(validated_path.resolve()),
        text_window=text_window,
        source_record=source_record,
        rules_dict=rules_dict,
        ruleset_sha256=ruleset_sha256,
    )

    # --- Optional deterministic output write ---
    if output_dir is not None:
        if not isinstance(output_dir, Path):
            raise TypeError(f"output_dir must be a pathlib.Path, got {type(output_dir).__name__!r}")
        if not output_dir.is_dir():
            raise FileNotFoundError(f"output_dir does not exist or is not a directory: {output_dir}")
        out_path = output_dir / f"{normalized.record_id}.json"
        out_data = normalized.model_dump()
        out_json = json.dumps(out_data, sort_keys=True, default=str)
        out_path.write_text(out_json, encoding="utf-8")

    return normalized
