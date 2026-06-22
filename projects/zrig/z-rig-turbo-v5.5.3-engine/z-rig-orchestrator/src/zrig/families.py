#!/usr/bin/env python3
"""
HRR-004 Builder 2 — families.py
Family Registry, Model Lookup, and Diversity Enforcement.

Implements:
  MECH-001: DIVERSITY_CHECK — verify |distinct_families| >= min_families
  MECH-002: REGISTRY_HASH  — SHA-256 of canonical (sorted, minified) JSON
  RULE-R6:  Hash locked at W0, re-verified at every gate pre-check.

Spec refs: A.2, A.2.1, A.2.2, A.2.3, A.2.4, A.2.5
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List, Optional, Set

# ---------------------------------------------------------------------------
# Canonical family registry (spec A.2.1)
# Operators may extend but MUST NOT modify once W0 is complete (RULE-R6).
# ---------------------------------------------------------------------------

DEFAULT_FAMILY_REGISTRY: Dict = {
    "registry_version": "5.5.2",
    "families": {
        "anthropic": {
            "models": ["claude-opus-4", "claude-sonnet-4", "claude-haiku-4"],
            "organization": "Anthropic",
            "known_limitations": [],
        },
        "openai": {
            "models": ["gpt-5.4", "gpt-4.1", "o3-pro", "o4-mini"],
            "organization": "OpenAI",
            "known_limitations": [],
        },
        "google": {
            "models": ["gemini-2.5-pro", "gemini-2.5-flash"],
            "organization": "Google DeepMind",
            "known_limitations": [],
        },
        "xai": {
            "models": ["grok-4", "grok-3"],
            "organization": "xAI",
            "known_limitations": [],
        },
        "deepseek": {
            "models": ["deepseek-r1", "deepseek-v3"],
            "organization": "DeepSeek",
            "known_limitations": [],
        },
        "meta-llama": {
            "models": ["llama-3.3-70b", "llama-4-maverick", "llama-4-scout"],
            "organization": "Meta",
            "known_limitations": [],
        },
        "mistral": {
            "models": ["mistral-large", "mistral-medium", "codestral"],
            "organization": "Mistral AI",
            "known_limitations": [],
        },
        "cohere": {
            "models": ["command-r-plus", "command-r", "command-a"],
            "organization": "Cohere",
            "known_limitations": [],
        },
    },
    "updated_at": "2026-06-16T00:00:00Z",
}

UNKNOWN_FAMILY = "UNKNOWN"


# ---------------------------------------------------------------------------
# MECH-002: REGISTRY_HASH
# ---------------------------------------------------------------------------

def compute_registry_hash(registry: Dict) -> str:
    """
    MECH-002: REGISTRY_HASH
    canonical = JSON.stringify(registry, keys sorted lexicographically, minified)
    RETURN SHA-256(canonical)

    Returns hex string (64 chars).
    """
    canonical_json = json.dumps(registry, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Family registry class
# ---------------------------------------------------------------------------

@dataclass
class FamilyRegistry:
    """
    Canonical family registry with MECH-001 / MECH-002 enforcement.

    Usage:
        registry = FamilyRegistry.from_dict(DEFAULT_FAMILY_REGISTRY)
        registry.lock()               # W0: compute and store hash
        family = registry.family_of("claude-opus-4")  # → "anthropic"
        ok = registry.diversity_check(models, min_families=3)
        registry.verify_hash()        # gate pre-check (RULE-R6)
    """

    data: Dict
    _locked_hash: Optional[str] = field(default=None, repr=False)

    # ------------------------------------------------------------------ #
    # Construction helpers                                                 #
    # ------------------------------------------------------------------ #

    @classmethod
    def from_dict(cls, registry_dict: Dict) -> "FamilyRegistry":
        return cls(data=registry_dict)

    @classmethod
    def default(cls) -> "FamilyRegistry":
        return cls.from_dict(DEFAULT_FAMILY_REGISTRY)

    # ------------------------------------------------------------------ #
    # MECH-002: hash lock + verification                                   #
    # ------------------------------------------------------------------ #

    def lock(self) -> str:
        """
        W0: compute registry_hash and store it.
        Subsequent verify_hash() calls compare against this value.
        Returns the hash string for recording in the manifest.
        """
        self._locked_hash = compute_registry_hash(self.data)
        return self._locked_hash

    @property
    def locked_hash(self) -> Optional[str]:
        return self._locked_hash

    def verify_hash(self) -> bool:
        """
        RULE-R6 gate pre-check: recompute and compare to locked value.
        Returns True if integrity holds.
        Raises RegistryTamperError if locked but mismatched.
        Raises RuntimeError if not yet locked.
        """
        if self._locked_hash is None:
            raise RuntimeError(
                "Registry has not been locked yet. Call lock() at W0 before verifying."
            )
        current_hash = compute_registry_hash(self.data)
        if current_hash != self._locked_hash:
            raise RegistryTamperError(
                f"FM-REGISTRY-TAMPER: registry hash mismatch. "
                f"Expected {self._locked_hash!r}, got {current_hash!r}"
            )
        return True

    # ------------------------------------------------------------------ #
    # A.2.3: Family resolution                                            #
    # ------------------------------------------------------------------ #

    def family_of(self, model_id: str) -> str:
        """
        A.2.3 familyOf(model_id)
        Returns the family name, or UNKNOWN_FAMILY if not registered.
        UNKNOWN is treated as a unique family for diversity purposes.
        """
        for family_name, family_def in self.data.get("families", {}).items():
            if model_id in family_def.get("models", []):
                return family_name
        return UNKNOWN_FAMILY

    def all_models_for_family(self, family_name: str) -> List[str]:
        """Return all models registered under a family."""
        fam = self.data.get("families", {}).get(family_name, {})
        return list(fam.get("models", []))

    def all_families(self) -> List[str]:
        return list(self.data.get("families", {}).keys())

    # ------------------------------------------------------------------ #
    # MECH-001: DIVERSITY_CHECK                                           #
    # ------------------------------------------------------------------ #

    def diversity_check(
        self,
        model_ids: List[str],
        min_families: int = 3,
    ) -> "DiversityResult":
        """
        MECH-001: DIVERSITY_CHECK
        families = {familyOf(a.model_actual) for a in agents}
        RETURN |families| >= min_families

        Returns a DiversityResult with .ok, .families, .count.
        """
        families: Set[str] = {self.family_of(m) for m in model_ids}
        count = len(families)
        return DiversityResult(
            ok=count >= min_families,
            families=frozenset(families),
            count=count,
            min_required=min_families,
        )

    # ------------------------------------------------------------------ #
    # Full Mode partition feasibility (A.2.4)                             #
    # ------------------------------------------------------------------ #

    def full_mode_partition_feasible(
        self,
        available_families: List[str],
        execution_pool_size: int = 5,
        adversarial_pool_size: int = 3,
    ) -> bool:
        """
        A.2.4: Before Full Mode dispatch, verify a valid disjoint family partition.
        execution_pool ∩ adversarial_pool = ∅
        |execution_pool| = execution_pool_size
        |adversarial_pool| = adversarial_pool_size
        """
        total_needed = execution_pool_size + adversarial_pool_size
        return len(set(available_families)) >= total_needed

    # ------------------------------------------------------------------ #
    # Cross-assignment helpers                                            #
    # ------------------------------------------------------------------ #

    def assert_cross_assignment(
        self,
        assigned_agents: List[str],
        excluded_families: Set[str],
        wave_label: str = "unknown",
    ) -> None:
        """
        Raise CrossAssignmentError if any agent family is in excluded_families.
        Used for W4 (exclude W3 synthesizer family) and W5 (exclude W2+W3 families).
        """
        for model_id in assigned_agents:
            fam = self.family_of(model_id)
            if fam in excluded_families and fam != UNKNOWN_FAMILY:
                raise CrossAssignmentError(
                    f"FM-INDEPENDENCE: model {model_id!r} (family {fam!r}) "
                    f"violates cross-assignment rule for {wave_label}. "
                    f"Excluded families: {sorted(excluded_families)}"
                )


# ---------------------------------------------------------------------------
# Result + error types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DiversityResult:
    """Result of MECH-001 DIVERSITY_CHECK."""
    ok: bool
    families: FrozenSet[str]
    count: int
    min_required: int

    def __str__(self) -> str:
        status = "PASS" if self.ok else "FAIL"
        return (
            f"DIVERSITY_CHECK {status}: {self.count}/{self.min_required} families "
            f"({sorted(self.families)})"
        )


class RegistryTamperError(RuntimeError):
    """FM-REGISTRY-TAMPER: registry hash mismatch detected."""


class CrossAssignmentError(RuntimeError):
    """FM-INDEPENDENCE: model family violates cross-assignment rule."""


class DiversityViolationError(RuntimeError):
    """FM-DIVERSITY: family count below minimum after all failovers."""
