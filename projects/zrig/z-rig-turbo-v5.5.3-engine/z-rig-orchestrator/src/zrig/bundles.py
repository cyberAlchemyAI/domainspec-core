#!/usr/bin/env python3
"""
HRR-004 Builder 2 — bundles.py
Bundle Assembly, Strip List Enforcement, Hash Recording.

Implements the Bundle Engine (Part 5 §5.2, A.13.5):
  - Per-transition strip and include lists (B.5 Bundle Transition Matrix)
  - BUNDLE_ASSEMBLY_INVARIANT enforcement
  - SHA-256 bundle hashing + manifest recording
  - Agent isolation ID assignment

Spec refs: A.13.5, A.13.6, A.13.7, B.5, 5.2, INV-009
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Strip-list field access helpers
# ---------------------------------------------------------------------------

def _nested_get(obj: Any, dotted_key: str) -> Any:
    """Access obj["a"]["b"]["c"] from dotted_key 'a.b.c'. Returns _MISSING on miss."""
    parts = dotted_key.split(".")
    current = obj
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return _MISSING
    return current


def _nested_delete(obj: Any, dotted_key: str) -> bool:
    """Remove a nested key (supports dotted notation). Returns True if deleted."""
    parts = dotted_key.split(".")
    current = obj
    for part in parts[:-1]:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False
    if isinstance(current, dict) and parts[-1] in current:
        del current[parts[-1]]
        return True
    return False


class _Missing:
    def __repr__(self):
        return "<MISSING>"


_MISSING = _Missing()


# ---------------------------------------------------------------------------
# B.5 — Bundle Transition Matrix (Standard Mode)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TransitionSpec:
    """Defines strip/include rules for a single wave-to-wave transition."""
    transition_id: str      # e.g. "W1→W2"
    src_wave: str
    dst_wave: str
    # strip_list: field paths to REMOVE from assembled bundle (dotted notation or prefix match)
    strip_list: Tuple[str, ...] = ()
    # include_list: field paths that MUST be present and non-null in bundle
    include_list: Tuple[str, ...] = ()
    # residue_class_strip: strip entire residue classes (e.g. "residue_class:security")
    residue_class_strip: Tuple[str, ...] = ()


# Standard Mode Bundle Transition Matrix (spec B.5)
STANDARD_TRANSITIONS: Dict[str, TransitionSpec] = {
    "W0→W1": TransitionSpec(
        transition_id="W0→W1",
        src_wave="W0",
        dst_wave="W1",
        strip_list=(),  # W1 receives clean task input — no stripping
        include_list=(
            "probe_report.summary",
            "task_description",
            "run_config.mode",
            "necronomicon_context",
        ),
    ),
    "Wα-LOAD→W1": TransitionSpec(
        transition_id="Wα-LOAD→W1",
        src_wave="Wα-LOAD",
        dst_wave="W1",
        strip_list=(),
        include_list=(
            "probe_report.summary",
            "task_description",
            "run_config.mode",
            "necronomicon_context",
        ),
    ),
    "W1→W2": TransitionSpec(
        transition_id="W1→W2",
        src_wave="W1",
        dst_wave="W2",
        strip_list=(
            # BLIND_SYNTHESIS invariant: builders build, don't deliberate
            "residue.minority_dissent",
            "w1_synthesizer_attribution",
            "w1_deliberation_transcripts",
        ),
        include_list=(
            "requirements",
            "failure_modes",
            "rubric",
            "build_directives",
            "mechanism_registry",
        ),
    ),
    "W2→W3": TransitionSpec(
        transition_id="W2→W3",
        src_wave="W2",
        dst_wave="W3",
        strip_list=(
            # BLIND_SYNTHESIS invariant: synthesizer selects on merit, not family trust
            "agent_id",
            "model_actual",
            "family_actual",
            "build_self_assessment.confidence",
            "build_log",
        ),
        include_list=(
            "implementation.files",
            "implementation.test_suite.files",
            "requirements",
        ),
    ),
    "W3→W4": TransitionSpec(
        transition_id="W3→W4",
        src_wave="W3",
        dst_wave="W4",
        strip_list=(
            "synthesis_rationale",
            "conflict_resolutions",
            "source_agent",
            "w2_self_assessments",
            "confidence_narratives",
            "residue.conflict_resolutions",
            "synthesis_log",
        ),
        include_list=(
            "canonical_implementation",
            "requirements_matrix",
            "verification_scope",
            "mechanism_registry",
        ),
    ),
    "W4→W5": TransitionSpec(
        transition_id="W4→W5",
        src_wave="W4",
        dst_wave="W5",
        strip_list=(
            # Per B.5: individual W4 verifier reports (detail), verifier rationale,
            # builder identities, synthesis rationale
            "individual_w4_verifier_reports",
            "verifier_rationale",
            "builder_identities",
            "synthesis_rationale",
        ),
        include_list=(
            "canonical_implementation",
            "verification_summary",
            "squad_assignment",
        ),
    ),
    "W5→W5.5": TransitionSpec(
        transition_id="W5→W5.5",
        src_wave="W5",
        dst_wave="W5.5",
        strip_list=(),  # No stripping for W5.5 remediation bundle
        include_list=(
            "canonical_implementation",
            "w5_attack_reports",
            "w4_findings",
            "requirements",
            "issues_to_address",
        ),
    ),
    "W8→W8.5": TransitionSpec(
        transition_id="W8→W8.5",
        src_wave="W8",
        dst_wave="W8.5",
        strip_list=(
            "builder_rationale",
            "w4_verifier_internals",
            "w5_reasoning",
        ),
        include_list=(
            "phase1_fdl",
            "w8_user_testing_report",
            "pipeline_clean_run",
        ),
    ),
    "W8.5→W9": TransitionSpec(
        transition_id="W8.5→W9",
        src_wave="W8.5",
        dst_wave="W9",
        strip_list=(),  # W9 needs broad view — minimal stripping
        include_list=(
            "original_blueprint",
            "canonical_implementation",
            "pipeline_summary",
            "independence_exceptions",
        ),
    ),
    "W8→W9": TransitionSpec(
        transition_id="W8→W9",
        src_wave="W8",
        dst_wave="W9",
        strip_list=(),
        include_list=(
            "original_blueprint",
            "canonical_implementation",
            "pipeline_summary",
        ),
    ),
    "W9→W10": TransitionSpec(
        transition_id="W9→W10",
        src_wave="W9",
        dst_wave="W10",
        strip_list=(
            "panel_deliberation_transcripts",
            "individual_vote_rationale",
        ),
        include_list=(
            "artifact",
            "deployment_config",
            "approval_proof",
        ),
    ),
    "W10→W11": TransitionSpec(
        transition_id="W10→W11",
        src_wave="W10",
        dst_wave="W11",
        strip_list=("deployment_internals",),
        include_list=(
            "deployment_record",
            "requirements",
            "residual_risks",
            "alert_policy",
        ),
    ),
}

# Micro Mode transitions
MICRO_TRANSITIONS: Dict[str, TransitionSpec] = {
    "M0→M1": TransitionSpec(
        transition_id="M0→M1",
        src_wave="M0",
        dst_wave="M1",
        strip_list=(),
        include_list=(
            "task_description",
            "target_file",
            "verifier_config",
        ),
    ),
    "M1→M2": TransitionSpec(
        transition_id="M1→M2",
        src_wave="M1",
        dst_wave="M2",
        strip_list=(),
        include_list=(
            "candidate_artifact",
            "build_status",
        ),
    ),
}

ALL_TRANSITIONS: Dict[str, TransitionSpec] = {
    **STANDARD_TRANSITIONS,
    **MICRO_TRANSITIONS,
}


# ---------------------------------------------------------------------------
# Bundle dataclass
# ---------------------------------------------------------------------------

@dataclass
class Bundle:
    """
    Self-contained, hashed package of inputs authorized for one agent invocation.
    Spec §5.2.2.
    """
    bundle_id: str
    run_id: str
    wave: str
    created_at: str
    input_hashes: Dict[str, str]      # artifact_id → sha256 hash
    strip_list: List[str]
    residue_class_strip: List[str]
    agent_isolation_id: str
    payload: Dict[str, Any]           # actual content delivered to agent
    bundle_hash: str = ""             # set by BundleAssembler.seal()

    def to_dict(self) -> Dict:
        d = asdict(self)
        # Remove payload from manifest record (too large) — recorded separately
        d.pop("payload", None)
        return d

    def to_task_description(self) -> str:
        """
        Render bundle as a structured task description string for agent delivery.
        Agents receive this as their input; they never receive raw manifests.
        """
        return json.dumps(
            {
                "bundle_id": self.bundle_id,
                "run_id": self.run_id,
                "wave": self.wave,
                "agent_isolation_id": self.agent_isolation_id,
                "payload": self.payload,
            },
            indent=2,
        )


@dataclass
class BundleManifestRecord:
    """Recorded in run manifest after every bundle assembly."""
    transition_id: str
    bundle_id: str
    bundle_hash: str
    wave: str
    strip_list_applied: List[str]
    residue_class_strip_applied: List[str]
    include_list_verified: List[str]
    agent_isolation_id: str
    created_at: str
    include_check_passed: bool
    strip_check_passed: bool


# ---------------------------------------------------------------------------
# BundleAssembler
# ---------------------------------------------------------------------------

class BundleAssembler:
    """
    Implements BUNDLE_ASSEMBLY_INVARIANT (A.13.5 + 5.2):

    For each wave transition T from W_src → W_dst:
      1. Read output artifacts from W_src.
      2. Strip fields listed in T.strip_list.
      3. Include — verify all fields in T.include_list are present and non-null.
      4. Compute bundle hash: SHA-256(canonical_json(assembled_bundle)).
      5. Record transition in manifest.
      6. Dispatch bundle to W_dst agents.

    Invariant:
      ∀ transition T:
        ∀ field F in T.include_list: F EXISTS in bundle ∧ F IS non-null
        ∀ field F in T.strip_list:  F NOT IN bundle
        bundle_hash = SHA-256(canonical_json(bundle))
        bundle_hash IS recorded in manifest
    """

    def __init__(self, run_id: str, transitions: Optional[Dict[str, TransitionSpec]] = None):
        self.run_id = run_id
        self.transitions = transitions or ALL_TRANSITIONS
        self._manifest_records: List[BundleManifestRecord] = []

    # ------------------------------------------------------------------ #
    # Primary assembly method                                             #
    # ------------------------------------------------------------------ #

    def assemble(
        self,
        transition_id: str,
        source_artifacts: Dict[str, Any],
        agent_isolation_id: Optional[str] = None,
    ) -> "Bundle":
        """
        Assemble a bundle for the given transition.

        Args:
            transition_id: Key into self.transitions (e.g. "W1→W2")
            source_artifacts: Merged dict of all W_src output artifacts
            agent_isolation_id: Pre-assigned isolation ID, or auto-generated

        Returns:
            Bundle ready for delivery to agent.

        Raises:
            BundleAssemblyError: if strip or include invariant is violated.
            UnknownTransitionError: if transition_id not in registry.
        """
        spec = self._resolve_transition(transition_id)
        isolation_id = agent_isolation_id or f"agent_{uuid.uuid4()}"

        # Deep-copy the source to avoid mutating caller data
        payload = _deep_copy(source_artifacts)

        # Step 2: Apply strip list
        stripped_fields: List[str] = []
        for field_path in spec.strip_list:
            if _nested_delete(payload, field_path):
                stripped_fields.append(field_path)

        # Strip by residue class
        stripped_classes: List[str] = []
        for residue_class in spec.residue_class_strip:
            removed = self._strip_residue_class(payload, residue_class)
            if removed:
                stripped_classes.append(residue_class)

        # Step 3: Verify include list
        missing_fields: List[str] = []
        null_fields: List[str] = []
        verified_fields: List[str] = []
        for include_field in spec.include_list:
            val = _nested_get(payload, include_field)
            if isinstance(val, _Missing):
                missing_fields.append(include_field)
            elif val is None:
                null_fields.append(include_field)
            else:
                verified_fields.append(include_field)

        include_ok = len(missing_fields) == 0 and len(null_fields) == 0

        if not include_ok:
            problems = []
            if missing_fields:
                problems.append(f"MISSING: {missing_fields}")
            if null_fields:
                problems.append(f"NULL: {null_fields}")
            raise BundleAssemblyError(
                f"FM-SPEC: BUNDLE_ASSEMBLY_INVARIANT violation for {transition_id}. "
                f"Include list check failed — {'; '.join(problems)}"
            )

        # Verify strip was effective for critical fields
        strip_ok = True
        strip_violations: List[str] = []
        for field_path in spec.strip_list:
            val = _nested_get(payload, field_path)
            if not isinstance(val, _Missing):
                strip_ok = False
                strip_violations.append(field_path)
        if not strip_ok:
            raise BundleAssemblyError(
                f"FM-SPEC: Strip enforcement failure for {transition_id}. "
                f"Fields still present after strip: {strip_violations}"
            )

        # Step 4: Compute bundle hash
        input_hashes = self._compute_artifact_hashes(source_artifacts)
        now = datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + "Z"

        bundle = Bundle(
            bundle_id=f"bndl_{uuid.uuid4()}",
            run_id=self.run_id,
            wave=spec.dst_wave,
            created_at=now,
            input_hashes=input_hashes,
            strip_list=list(spec.strip_list) + list(stripped_fields),
            residue_class_strip=list(spec.residue_class_strip) + stripped_classes,
            agent_isolation_id=isolation_id,
            payload=payload,
            bundle_hash="",
        )
        bundle.bundle_hash = self._hash_bundle(bundle)

        # Step 5: Record manifest entry
        record = BundleManifestRecord(
            transition_id=transition_id,
            bundle_id=bundle.bundle_id,
            bundle_hash=bundle.bundle_hash,
            wave=spec.dst_wave,
            strip_list_applied=list(spec.strip_list),
            residue_class_strip_applied=stripped_classes,
            include_list_verified=verified_fields,
            agent_isolation_id=isolation_id,
            created_at=now,
            include_check_passed=include_ok,
            strip_check_passed=strip_ok,
        )
        self._manifest_records.append(record)

        return bundle

    # ------------------------------------------------------------------ #
    # Multi-agent fan-out (one bundle per agent in same wave)             #
    # ------------------------------------------------------------------ #

    def assemble_for_agents(
        self,
        transition_id: str,
        source_artifacts: Dict[str, Any],
        agent_count: int,
    ) -> List[Bundle]:
        """
        Assemble N independent bundles for parallel agent execution.
        Each agent receives a unique agent_isolation_id (A.13.6 namespace isolation).
        """
        bundles = []
        for _ in range(agent_count):
            isolation_id = f"agent_{uuid.uuid4()}"
            b = self.assemble(transition_id, source_artifacts, agent_isolation_id=isolation_id)
            bundles.append(b)
        return bundles

    # ------------------------------------------------------------------ #
    # Manifest access                                                     #
    # ------------------------------------------------------------------ #

    @property
    def manifest_records(self) -> List[BundleManifestRecord]:
        return list(self._manifest_records)

    def dump_manifest(self) -> List[Dict]:
        return [asdict(r) for r in self._manifest_records]

    # ------------------------------------------------------------------ #
    # Filesystem namespace isolation (A.13.6)                             #
    # ------------------------------------------------------------------ #

    @staticmethod
    def write_to_namespace(
        run_id: str,
        agent_isolation_id: str,
        bundle: Bundle,
        base_dir: Path,
    ) -> Path:
        """
        Write bundle payload to the agent's isolated namespace directory.
        workspace/<run_id>/agents/<agent_isolation_id>/bundle.json

        Raises FileExistsError if namespace already occupied (prevents re-use).
        """
        namespace = base_dir / run_id / "agents" / agent_isolation_id
        namespace.mkdir(parents=True, exist_ok=False)
        bundle_path = namespace / "bundle.json"
        bundle_path.write_text(
            json.dumps({"bundle_id": bundle.bundle_id, "payload": bundle.payload}, indent=2),
            encoding="utf-8",
        )
        return bundle_path

    @staticmethod
    def read_output_from_namespace(
        run_id: str,
        agent_isolation_id: str,
        base_dir: Path,
    ) -> Dict:
        """
        Collect agent output from its isolated namespace.
        workspace/<run_id>/agents/<agent_isolation_id>/output.json
        """
        output_path = base_dir / run_id / "agents" / agent_isolation_id / "output.json"
        if not output_path.exists():
            raise MissingOutputError(
                f"Agent {agent_isolation_id} has no output at {output_path}"
            )
        return json.loads(output_path.read_text(encoding="utf-8"))

    # ------------------------------------------------------------------ #
    # Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _resolve_transition(self, transition_id: str) -> TransitionSpec:
        spec = self.transitions.get(transition_id)
        if spec is None:
            available = sorted(self.transitions.keys())
            raise UnknownTransitionError(
                f"Unknown transition {transition_id!r}. "
                f"Available: {available}"
            )
        return spec

    @staticmethod
    def _compute_artifact_hashes(artifacts: Dict[str, Any]) -> Dict[str, str]:
        """Compute SHA-256 for each top-level artifact value."""
        hashes: Dict[str, str] = {}
        for key, val in artifacts.items():
            serialized = json.dumps(val, sort_keys=True, separators=(",", ":"))
            digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
            hashes[key] = f"sha256:{digest}"
        return hashes

    @staticmethod
    def _hash_bundle(bundle: Bundle) -> str:
        """
        SHA-256(canonical_json(assembled_bundle)) — Step 4 of BUNDLE_ASSEMBLY_INVARIANT.
        The payload is the canonical content; metadata is not included in the hash.
        """
        canonical = json.dumps(
            bundle.payload,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @staticmethod
    def _strip_residue_class(payload: Dict, residue_class: str) -> bool:
        """
        Strip a residue class (e.g. "residue_class:security").
        Looks for payload["residue"][<class_name>] and removes it.
        """
        class_name = residue_class.replace("residue_class:", "")
        residue = payload.get("residue", {})
        if isinstance(residue, dict) and class_name in residue:
            del residue[class_name]
            return True
        return False


# ---------------------------------------------------------------------------
# Artifact store (simple JSON-on-disk)
# ---------------------------------------------------------------------------

class ArtifactStore:
    """
    Lightweight artifact storage for Z-Rig runs.
    Stores artifacts under HRR-NNN/waveN/<artifact_id>.json

    Spec A.13.7: artifact_id = UUID-v4()
    """

    def __init__(self, run_dir: Path):
        self.run_dir = run_dir
        self._inventory: Dict[str, Dict] = {}  # artifact_id → metadata

    def store(
        self,
        artifact: Dict,
        wave: str,
        agent_isolation_id: str,
    ) -> str:
        """Store artifact, return artifact_id."""
        artifact_id = str(uuid.uuid4())
        wave_dir = self.run_dir / f"wave{wave.lstrip('W')}"
        wave_dir.mkdir(parents=True, exist_ok=True)
        path = wave_dir / f"{artifact_id}.json"
        path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

        artifact_hash = hashlib.sha256(
            json.dumps(artifact, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

        self._inventory[artifact_id] = {
            "artifact_id": artifact_id,
            "wave": wave,
            "agent_isolation_id": agent_isolation_id,
            "file_path": str(path),
            "hash": artifact_hash,
        }
        return artifact_id

    def load(self, artifact_id: str) -> Dict:
        """Load artifact by ID."""
        meta = self._inventory.get(artifact_id)
        if meta is None:
            raise KeyError(f"Artifact {artifact_id!r} not found in store.")
        return json.loads(Path(meta["file_path"]).read_text(encoding="utf-8"))

    def verify_hash(self, artifact_id: str) -> bool:
        """Recompute and compare stored hash."""
        meta = self._inventory.get(artifact_id)
        if meta is None:
            return False
        artifact = json.loads(Path(meta["file_path"]).read_text(encoding="utf-8"))
        actual = hashlib.sha256(
            json.dumps(artifact, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        return actual == meta["hash"]

    @property
    def inventory(self) -> Dict[str, Dict]:
        return dict(self._inventory)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class BundleAssemblyError(RuntimeError):
    """Raised when BUNDLE_ASSEMBLY_INVARIANT is violated (FM-SPEC)."""


class UnknownTransitionError(RuntimeError):
    """Raised when transition_id is not in the registry."""


class MissingOutputError(RuntimeError):
    """Raised when an agent has not written output to its namespace."""


# ---------------------------------------------------------------------------
# Utility: deep copy without stdlib copy module
# ---------------------------------------------------------------------------

def _deep_copy(obj: Any) -> Any:
    """Simple deep copy via JSON round-trip (works for JSON-serializable data)."""
    return json.loads(json.dumps(obj))
