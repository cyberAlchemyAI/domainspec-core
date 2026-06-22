"""Z-Rig deployment config schema validation."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .deploy_adapter import DeployConfig

# ---------------------------------------------------------------------------
# Schema constraints
# ---------------------------------------------------------------------------

_REQUIRED_FIELDS: list[str] = ["host", "app_path", "service_name"]

_FIELD_TYPES: dict[str, type | tuple[type, ...]] = {
    "host": str,
    "user": str,
    "app_path": str,
    "service_name": str,
    "venv_path": str,
    "health_url": str,
    "health_timeout_s": int,
    "git_branch": str,
    "pre_deploy_commands": list,
    "post_deploy_commands": list,
}


def validate_deploy_config(config: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate a deploy configuration dictionary against the schema.

    Checks:
        - All required fields (``host``, ``app_path``, ``service_name``) are
          present and non-empty.
        - Known fields have the correct type.
        - ``host`` is not blank whitespace.
        - ``health_timeout_s``, if present, is a positive integer.
        - List fields (``pre_deploy_commands``, ``post_deploy_commands``)
          contain only strings.

    Args:
        config: Raw config dictionary (e.g. parsed from JSON).

    Returns:
        Tuple of ``(valid, errors)`` where *errors* is a list of human-readable
        error strings.  An empty *errors* list means the config is valid.
    """
    errors: list[str] = []

    if not isinstance(config, dict):
        return False, ["Config must be a JSON object (dict)."]

    # Required fields -------------------------------------------------
    for fname in _REQUIRED_FIELDS:
        if fname not in config:
            errors.append(f"Missing required field: '{fname}'.")
        elif not isinstance(config[fname], str) or not config[fname].strip():
            errors.append(f"Field '{fname}' must be a non-empty string.")

    # Type checks -----------------------------------------------------
    for fname, expected in _FIELD_TYPES.items():
        if fname in config and not isinstance(config[fname], expected):
            errors.append(
                f"Field '{fname}' must be {expected.__name__ if isinstance(expected, type) else expected}, "
                f"got {type(config[fname]).__name__}."
            )

    # Semantic checks --------------------------------------------------
    if "health_timeout_s" in config:
        val = config["health_timeout_s"]
        if isinstance(val, int) and val <= 0:
            errors.append("Field 'health_timeout_s' must be a positive integer.")

    for list_field in ("pre_deploy_commands", "post_deploy_commands"):
        if list_field in config and isinstance(config[list_field], list):
            for idx, item in enumerate(config[list_field]):
                if not isinstance(item, str):
                    errors.append(
                        f"'{list_field}[{idx}]' must be a string, got {type(item).__name__}."
                    )

    return (len(errors) == 0), errors


def load_project_configs(config_dir: str | Path) -> dict[str, DeployConfig]:
    """Load all ``*_deploy_config.json`` / ``deploy_config*.json`` files from a directory.

    Each file is validated; files that fail validation are skipped with a
    warning printed to stderr.

    The returned dict is keyed by the stem of the filename (without the
    ``.json`` extension).

    Args:
        config_dir: Directory containing JSON config files.

    Returns:
        A mapping of ``{config_name: DeployConfig}``.

    Raises:
        FileNotFoundError: If *config_dir* does not exist.
    """
    import sys

    config_dir = Path(config_dir)
    if not config_dir.is_dir():
        raise FileNotFoundError(f"Config directory not found: {config_dir}")

    configs: dict[str, DeployConfig] = {}

    for json_file in sorted(config_dir.glob("*.json")):
        try:
            raw = json_file.read_text(encoding="utf-8")
            data = json.loads(raw)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"[warn] Skipping {json_file.name}: {exc}", file=sys.stderr)
            continue

        valid, errs = validate_deploy_config(data)
        if not valid:
            print(
                f"[warn] Skipping {json_file.name}: {'; '.join(errs)}",
                file=sys.stderr,
            )
            continue

        configs[json_file.stem] = DeployConfig.from_dict(data)

    return configs
