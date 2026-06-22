"""
Z-Rig Config Module — Parse and validate run_config.json + task_description.json

Implements structural validation against the v5.5.3 root input schemas.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Mode(str, Enum):
    AUTO = "AUTO"
    MICRO = "MICRO"
    STANDARD = "STANDARD"
    FULL = "FULL"

    @property
    def rank(self) -> int:
        """Numeric rank for mode comparison: higher = more rigorous."""
        return {"AUTO": -1, "MICRO": 0, "STANDARD": 1, "FULL": 2}[self.value]


class StakesLevel(str, Enum):
    ROUTINE = "routine"
    ELEVATED = "elevated"
    CRITICAL = "critical"


class ScopeAmbiguity(str, Enum):
    NONE = "none"
    LOW = "low"
    HIGH = "high"


class DeploymentSideEffects(str, Enum):
    NONE = "none"
    LOCAL_ONLY = "local_only"
    REQUIRES_COORDINATION = "requires_coordination"
    IRREVERSIBLE = "irreversible"


class VerifierKind(str, Enum):
    FROZEN_TEST_SUITE = "frozen_test_suite"
    DETERMINISTIC_CHECKER = "deterministic_checker"
    SINGLE_INDEPENDENT_VERIFIER = "single_independent_verifier"
    NONE = "none"


# ---------------------------------------------------------------------------
# Validation errors
# ---------------------------------------------------------------------------

class ConfigValidationError(Exception):
    """Raised when run_config or task_description fails structural validation."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__(f"Config validation failed: {'; '.join(errors)}")


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class PipelineBounds:
    """Pipeline bounds — defaults from spec, overridable via custom_bounds."""
    max_w2_reruns: int = 2
    max_w3_challenger_retries: int = 1
    max_w5_reruns: int = 2
    max_w5_5_reruns: int = 1
    max_w6_remediation_cycles: int = 2
    max_w9_returns: int = 1
    max_micro_discards: int = 2
    max_failover_per_seat: int = 2
    max_failover_per_wave: int = 3
    total_pipeline_timeout_ms: int = 86_400_000  # 24h

    @classmethod
    def from_custom(cls, custom: dict[str, Any] | None = None) -> PipelineBounds:
        bounds = cls()
        if custom:
            for k, v in custom.items():
                if hasattr(bounds, k):
                    setattr(bounds, k, int(v))
        return bounds


@dataclass
class SecurityRelevance:
    is_security_relevant: bool = False
    is_safety_relevant: bool = False
    is_compliance_relevant: bool = False
    notes: str | None = None


@dataclass
class PublicInterfaceImpact:
    changes_public_surface: bool = False
    surface_types: list[str] = field(default_factory=lambda: ["none"])
    notes: str | None = None


@dataclass
class DeterministicVerifier:
    kind: str = "none"
    identifier: str = ""
    command_or_dispatch_key: str | None = None
    frozen_before_run: bool = False
    coverage_of_changed_scope: float | None = None
    verifier_bundle_hash: str | None = None


@dataclass
class Reversibility:
    fully_reversible: bool = True
    requires_migration: bool = False
    requires_cleanup: bool = False
    rollback_notes: str | None = None


@dataclass
class TaskDescription:
    """Parsed task_description.json per v5.5.3 schema."""
    task_id: str = ""
    summary: str = ""
    requested_change: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    artifact_type: str = ""
    artifact_domain_tags: list[str] = field(default_factory=list)
    stakes_level: StakesLevel = StakesLevel.ROUTINE
    scope_ambiguity: ScopeAmbiguity = ScopeAmbiguity.NONE
    target_files: list[str] = field(default_factory=list)
    public_interface_impact: PublicInterfaceImpact = field(default_factory=PublicInterfaceImpact)
    deterministic_verifier: DeterministicVerifier = field(default_factory=DeterministicVerifier)
    reversibility: Reversibility = field(default_factory=Reversibility)
    deployment_side_effects: DeploymentSideEffects = DeploymentSideEffects.NONE
    security_relevance: SecurityRelevance = field(default_factory=SecurityRelevance)
    predicted_diff: dict[str, int] | None = None
    references: list[str] = field(default_factory=list)

    # Raw data for mechanism access
    _raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TaskDescription:
        errors = _validate_task_description(data)
        if errors:
            raise ConfigValidationError(errors)

        sec = data.get("security_relevance", {})
        pub = data.get("public_interface_impact", {})
        det = data.get("deterministic_verifier", {})
        rev = data.get("reversibility", {})

        return cls(
            task_id=data["task_id"],
            summary=data["summary"],
            requested_change=data["requested_change"],
            acceptance_criteria=data["acceptance_criteria"],
            artifact_type=data["artifact_type"],
            artifact_domain_tags=data["artifact_domain_tags"],
            stakes_level=StakesLevel(data["stakes_level"]),
            scope_ambiguity=ScopeAmbiguity(data["scope_ambiguity"]),
            target_files=data["target_files"],
            public_interface_impact=PublicInterfaceImpact(
                changes_public_surface=pub.get("changes_public_surface", False),
                surface_types=pub.get("surface_types", ["none"]),
                notes=pub.get("notes"),
            ),
            deterministic_verifier=DeterministicVerifier(
                kind=det.get("kind", "none"),
                identifier=det.get("identifier", ""),
                command_or_dispatch_key=det.get("command_or_dispatch_key"),
                frozen_before_run=det.get("frozen_before_run", False),
                coverage_of_changed_scope=det.get("coverage_of_changed_scope"),
                verifier_bundle_hash=det.get("verifier_bundle_hash"),
            ),
            reversibility=Reversibility(
                fully_reversible=rev.get("fully_reversible", True),
                requires_migration=rev.get("requires_migration", False),
                requires_cleanup=rev.get("requires_cleanup", False),
                rollback_notes=rev.get("rollback_notes"),
            ),
            deployment_side_effects=DeploymentSideEffects(
                data.get("deployment_side_effects", "none")
            ),
            security_relevance=SecurityRelevance(
                is_security_relevant=sec.get("is_security_relevant", False),
                is_safety_relevant=sec.get("is_safety_relevant", False),
                is_compliance_relevant=sec.get("is_compliance_relevant", False),
                notes=sec.get("notes"),
            ),
            predicted_diff=data.get("predicted_diff"),
            references=data.get("references", []),
            _raw=data,
        )

    @classmethod
    def from_file(cls, path: str | Path) -> TaskDescription:
        with open(path) as f:
            return cls.from_dict(json.load(f))


@dataclass
class RunConfig:
    """Parsed run_config.json per v5.5.3 schema."""
    run_id: str = ""
    mode: Mode = Mode.STANDARD
    artifact_type: str = ""
    artifact_domain_tags: list[str] = field(default_factory=list)
    stakes_level: StakesLevel = StakesLevel.ROUTINE
    scope_ambiguity: ScopeAmbiguity = ScopeAmbiguity.NONE
    deterministic_metric_defined: bool = False
    deterministic_metric_id: str | None = None
    changed_files_predicted: int | None = None
    lines_changed_predicted: int | None = None
    no_new_public_interfaces: bool | None = None
    change_is_fully_reversible: bool | None = None
    verifier_kind: VerifierKind | None = None
    frozen_suite_qualifies: bool | None = None
    force_challenger: bool = False
    force_full: bool = False
    provider_list: list[str] = field(default_factory=list)
    w1_panel_size: int = 5
    w2_builder_count: int = 3
    w4_verifier_count: int = 3
    w5_squad_count: int = 2
    w9_panel_size: int = 5
    max_rework_cycles: int = 2
    human_escalation_timeout_ms: int = 86_400_000
    custom_timeouts: dict[str, Any] = field(default_factory=dict)
    custom_bounds: dict[str, Any] = field(default_factory=dict)
    deployment_config: dict[str, Any] = field(default_factory=dict)
    allowed_model_failover_map: dict[str, list[str]] = field(default_factory=dict)
    ignored_generated_files: list[str] = field(default_factory=list)
    operator_micro_override: bool = False
    include_quarantined_residue: bool = False
    halt_on_residue_tamper: bool = False

    # Computed
    bounds: PipelineBounds = field(default_factory=PipelineBounds)

    # Raw data
    _raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RunConfig:
        errors = _validate_run_config(data)
        if errors:
            raise ConfigValidationError(errors)

        vk = data.get("verifier_kind")
        verifier_kind = VerifierKind(vk) if vk else None

        rc = cls(
            run_id=data["run_id"],
            mode=Mode(data["mode"]),
            artifact_type=data["artifact_type"],
            artifact_domain_tags=data["artifact_domain_tags"],
            stakes_level=StakesLevel(data["stakes_level"]),
            scope_ambiguity=ScopeAmbiguity(data["scope_ambiguity"]),
            deterministic_metric_defined=data["deterministic_metric_defined"],
            deterministic_metric_id=data.get("deterministic_metric_id"),
            changed_files_predicted=data.get("changed_files_predicted"),
            lines_changed_predicted=data.get("lines_changed_predicted"),
            no_new_public_interfaces=data.get("no_new_public_interfaces"),
            change_is_fully_reversible=data.get("change_is_fully_reversible"),
            verifier_kind=verifier_kind,
            frozen_suite_qualifies=data.get("frozen_suite_qualifies"),
            force_challenger=data.get("force_challenger", False),
            force_full=data.get("force_full", False),
            provider_list=data["provider_list"],
            w1_panel_size=data["w1_panel_size"],
            w2_builder_count=data["w2_builder_count"],
            w4_verifier_count=data["w4_verifier_count"],
            w5_squad_count=data["w5_squad_count"],
            w9_panel_size=data["w9_panel_size"],
            max_rework_cycles=data["max_rework_cycles"],
            human_escalation_timeout_ms=data["human_escalation_timeout_ms"],
            custom_timeouts=data.get("custom_timeouts", {}),
            custom_bounds=data.get("custom_bounds", {}),
            deployment_config=data.get("deployment_config", {}),
            allowed_model_failover_map=data.get("allowed_model_failover_map", {}),
            ignored_generated_files=data.get("ignored_generated_files", []),
            operator_micro_override=data.get("operator_micro_override", False),
            include_quarantined_residue=data.get("include_quarantined_residue", False),
            halt_on_residue_tamper=data.get("halt_on_residue_tamper", False),
            bounds=PipelineBounds.from_custom(data.get("custom_bounds")),
            _raw=data,
        )
        return rc

    @classmethod
    def from_file(cls, path: str | Path) -> RunConfig:
        with open(path) as f:
            return cls.from_dict(json.load(f))


# ---------------------------------------------------------------------------
# Family Registry
# ---------------------------------------------------------------------------

@dataclass
class FamilyRegistry:
    """The canonical family registry, locked at W0."""
    registry_version: str = __import__("zrig").__spec_version__
    families: dict[str, dict[str, Any]] = field(default_factory=dict)
    updated_at: str = ""
    _hash: str | None = field(default=None, repr=False)

    def family_of(self, model_id: str) -> str:
        """Resolve a model ID to its family name. UNKNOWN if unregistered."""
        for family_name, fam_def in self.families.items():
            if model_id in fam_def.get("models", []):
                return family_name
        return "UNKNOWN"

    def compute_hash(self) -> str:
        """MECH-002: REGISTRY_HASH — SHA-256 of canonical JSON."""
        import hashlib
        canonical = json.dumps(
            {"registry_version": self.registry_version,
             "families": self.families,
             "updated_at": self.updated_at},
            sort_keys=True, separators=(",", ":")
        )
        h = hashlib.sha256(canonical.encode()).hexdigest()
        self._hash = h
        return h

    @property
    def hash(self) -> str:
        if self._hash is None:
            return self.compute_hash()
        return self._hash

    @classmethod
    def default(cls) -> FamilyRegistry:
        """Build default registry from spec."""
        return cls(
            families={
                "anthropic": {"models": ["claude-opus-4", "claude-sonnet-4", "claude-haiku-4"], "organization": "Anthropic"},
                "openai": {"models": ["gpt-5.4", "gpt-4.1", "o3-pro", "o4-mini"], "organization": "OpenAI"},
                "google": {"models": ["gemini-2.5-pro", "gemini-2.5-flash"], "organization": "Google DeepMind"},
                "xai": {"models": ["grok-4", "grok-3"], "organization": "xAI"},
                "deepseek": {"models": ["deepseek-r1", "deepseek-v3"], "organization": "DeepSeek"},
                "meta-llama": {"models": ["llama-3.3-70b", "llama-4-maverick", "llama-4-scout"], "organization": "Meta"},
                "mistral": {"models": ["mistral-large", "mistral-medium", "codestral"], "organization": "Mistral AI"},
                "cohere": {"models": ["command-r-plus", "command-r", "command-a"], "organization": "Cohere"},
            },
            updated_at="2026-06-16T00:00:00+00:00",  # Fixed for deterministic hashing
        )

    @classmethod
    def from_file(cls, path: str | Path) -> FamilyRegistry:
        with open(path) as f:
            data = json.load(f)
        reg = cls(
            registry_version=data.get("registry_version", "5.5.3"),
            families=data.get("families", {}),
            updated_at=data.get("updated_at", ""),
        )
        return reg


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

_RUN_ID_PATTERN = re.compile(r"^HRR-[A-Za-z0-9._-]+$")
_VALID_MODES = {"AUTO", "MICRO", "STANDARD", "FULL"}
_VALID_STAKES = {"routine", "elevated", "critical"}
_VALID_AMBIGUITY = {"none", "low", "high"}
_VALID_PROVIDERS = {"anthropic", "openai", "google", "xai", "deepseek", "meta-llama", "mistral", "cohere"}

_RUN_CONFIG_REQUIRED = [
    "run_id", "mode", "artifact_type", "artifact_domain_tags", "stakes_level",
    "scope_ambiguity", "deterministic_metric_defined", "provider_list",
    "w1_panel_size", "w2_builder_count", "w4_verifier_count", "w5_squad_count",
    "w9_panel_size", "max_rework_cycles", "human_escalation_timeout_ms",
    "custom_timeouts", "custom_bounds", "deployment_config",
    "allowed_model_failover_map", "ignored_generated_files",
]

_TASK_REQUIRED = [
    "task_id", "summary", "requested_change", "acceptance_criteria",
    "artifact_type", "artifact_domain_tags", "stakes_level", "scope_ambiguity",
    "target_files", "public_interface_impact", "deterministic_verifier",
    "reversibility", "deployment_side_effects", "security_relevance",
]


def _validate_run_config(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in _RUN_CONFIG_REQUIRED:
        if key not in data:
            errors.append(f"Missing required field: {key}")
    if errors:
        return errors  # Can't validate further

    if not _RUN_ID_PATTERN.match(data.get("run_id", "")):
        errors.append(f"run_id must match ^HRR-[A-Za-z0-9._-]+$, got: {data.get('run_id')}")
    if data.get("mode") not in _VALID_MODES:
        errors.append(f"Invalid mode: {data.get('mode')}")
    if data.get("stakes_level") not in _VALID_STAKES:
        errors.append(f"Invalid stakes_level: {data.get('stakes_level')}")
    if data.get("scope_ambiguity") not in _VALID_AMBIGUITY:
        errors.append(f"Invalid scope_ambiguity: {data.get('scope_ambiguity')}")

    # Provider list
    providers = data.get("provider_list", [])
    if not providers:
        errors.append("provider_list must have at least 1 entry")
    for p in providers:
        if p not in _VALID_PROVIDERS:
            errors.append(f"Invalid provider: {p}")

    # Numeric bounds
    wpc = data.get("w1_panel_size", 0)
    if not (3 <= wpc <= 7):
        errors.append(f"w1_panel_size must be 3-7, got {wpc}")
    if data.get("w2_builder_count") not in (1, 3, 5):
        errors.append(f"w2_builder_count must be 1, 3, or 5")
    if not (1 <= data.get("w4_verifier_count", 0) <= 5):
        errors.append(f"w4_verifier_count must be 1-5")
    if not (1 <= data.get("w5_squad_count", 0) <= 3):
        errors.append(f"w5_squad_count must be 1-3")
    if not (3 <= data.get("w9_panel_size", 0) <= 7):
        errors.append(f"w9_panel_size must be 3-7")
    if not (0 <= data.get("max_rework_cycles", -1) <= 3):
        errors.append(f"max_rework_cycles must be 0-3")
    if data.get("human_escalation_timeout_ms", 0) < 60000:
        errors.append("human_escalation_timeout_ms must be >= 60000")

    # Conditional requirements for MICRO mode (not required for AUTO — will be evaluated dynamically)
    if data.get("mode") == "MICRO":
        micro_fields = [
            "changed_files_predicted", "lines_changed_predicted",
            "no_new_public_interfaces", "change_is_fully_reversible",
            "verifier_kind", "frozen_suite_qualifies",
        ]
        for mf in micro_fields:
            if mf not in data:
                errors.append(f"MICRO mode requires field: {mf}")

    return errors


def _validate_task_description(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in _TASK_REQUIRED:
        if key not in data:
            errors.append(f"Missing required field: {key}")
    if errors:
        return errors

    if not data.get("task_id"):
        errors.append("task_id must be non-empty")
    if not data.get("summary"):
        errors.append("summary must be non-empty")
    if not data.get("acceptance_criteria"):
        errors.append("acceptance_criteria must have at least 1 entry")
    if not data.get("target_files"):
        errors.append("target_files must have at least 1 entry")
    if data.get("stakes_level") not in _VALID_STAKES:
        errors.append(f"Invalid stakes_level: {data.get('stakes_level')}")
    if data.get("scope_ambiguity") not in _VALID_AMBIGUITY:
        errors.append(f"Invalid scope_ambiguity: {data.get('scope_ambiguity')}")

    return errors
