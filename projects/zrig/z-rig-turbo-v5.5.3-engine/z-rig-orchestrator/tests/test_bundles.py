#!/usr/bin/env python3
"""
HRR-004 Builder 2 — tests/test_bundles.py
Tests for bundles.py: BUNDLE_ASSEMBLY_INVARIANT, strip lists, include lists,
hash computation, multi-agent fan-out, manifest recording.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from zrig.bundles import (
    BundleAssembler,
    BundleAssemblyError,
    MissingOutputError,
    TransitionSpec,
    UnknownTransitionError,
    STANDARD_TRANSITIONS,
    ArtifactStore,
    _nested_get,
    _nested_delete,
    _MISSING,
)


# ---------------------------------------------------------------------------
# Test data helpers
# ---------------------------------------------------------------------------

def w1_output_sample() -> dict:
    """Sample W1 blueprint output."""
    return {
        "requirements": {
            "functional": [{"id": "REQ-001", "priority": "MUST", "description": "Build works"}],
            "non_functional": [],
        },
        "failure_modes": [{"fm_id": "FM-001", "description": "No network", "recovery": "retry"}],
        "rubric": [{"criterion_id": "RC-001", "weight": 1.0, "pass_condition": "ok", "fail_condition": "nok"}],
        "build_directives": {"language": "python"},
        "mechanism_registry": {"MECH-001": "DIVERSITY_CHECK"},
        "residue": {
            "minority_dissent": [{"seat": "panel_safety", "position": "needs more tests"}],
            "open_items": [],
        },
        "w1_synthesizer_attribution": "panel_correctness",
        "w1_deliberation_transcripts": ["Round 1...", "Round 2..."],
        "user_journeys": [{"journey_id": "UJ-001", "description": "User builds artifact"}],
        "panel_consensus": {"agreement_level": "majority", "vote_counts": {"agree": 4, "disagree": 1}},
        "w1_synthesis_confidence": 0.85,
        "architecture_overview": "Layered architecture",
    }


def w2_output_sample() -> dict:
    """Sample W2 builder output."""
    return {
        "agent_id": "builder_1_abc123",
        "model_actual": "claude-opus-4",
        "family_actual": "anthropic",
        "implementation": {
            "files": [{"path": "main.py", "content": "print('hello')", "language": "python"}],
            "test_suite": {"files": [{"path": "test_main.py", "content": "def test_noop(): pass"}]},
        },
        "test_suites": [],
        "requirements_coverage": {"MUST_satisfied": 1, "MUST_total": 1, "coverage_rate": 1.0},
        "build_self_assessment": {"confidence": 0.9, "known_gaps": [], "synthesis_strategy_per_file": {}},
        "build_status": "SUCCESS",
        "build_log": "Build completed in 5s",
        "residue": {"rejected_alternatives": [], "open_items": []},
        "requirements": {"functional": [{"id": "REQ-001", "priority": "MUST"}]},
    }


def w3_output_sample() -> dict:
    """Sample W3 synthesis output."""
    return {
        "canonical_implementation": {
            "files": [{"path": "main.py", "content": "print('canonical')", "source_agents": ["builder_1"]}]
        },
        "requirements_matrix": [{"requirement_id": "REQ-001", "satisfied": True, "evidence": "main.py"}],
        "synthesis_rationale": "Builder 1 had the cleanest implementation",
        "conflict_resolutions": ["Resolved: use type annotations"],
        "source_agent": "builder_1",
        "w2_self_assessments": {"builder_1": {"confidence": 0.9}},
        "confidence_narratives": ["Primary synthesizer was confident"],
        "synthesis_confidence": 0.80,
        "synthesis_log": ["Step 1: compare", "Step 2: merge"],
        "verification_scope": {"scope": "full"},
        "mechanism_registry": {"MECH-001": "DIVERSITY_CHECK"},
        "residue": {"conflict_resolutions": ["use type annotations"]},
    }


# ---------------------------------------------------------------------------
# BUNDLE_ASSEMBLY_INVARIANT tests
# ---------------------------------------------------------------------------

class TestBundleAssemblyInvariant:

    def test_w1_to_w2_strips_minority_dissent(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        bundle = assembler.assemble("W1→W2", source)
        # minority_dissent must be stripped
        residue = bundle.payload.get("residue", {})
        assert "minority_dissent" not in residue, (
            "W1→W2: minority_dissent should be stripped (builders build, don't deliberate)"
        )

    def test_w1_to_w2_strips_synthesizer_attribution(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        bundle = assembler.assemble("W1→W2", source)
        assert "w1_synthesizer_attribution" not in bundle.payload

    def test_w1_to_w2_strips_deliberation_transcripts(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        bundle = assembler.assemble("W1→W2", source)
        assert "w1_deliberation_transcripts" not in bundle.payload

    def test_w1_to_w2_includes_requirements(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        bundle = assembler.assemble("W1→W2", source)
        assert bundle.payload.get("requirements") is not None, (
            "requirements must be in W2 bundle"
        )

    def test_w1_to_w2_includes_mechanism_registry(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        bundle = assembler.assemble("W1→W2", source)
        assert bundle.payload.get("mechanism_registry") is not None

    def test_w2_to_w3_strips_agent_id(self):
        """BLIND_SYNTHESIS invariant: synthesizer selects on merit, not family trust."""
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w2_output_sample()
        bundle = assembler.assemble("W2→W3", source)
        assert "agent_id" not in bundle.payload

    def test_w2_to_w3_strips_model_actual(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w2_output_sample()
        bundle = assembler.assemble("W2→W3", source)
        assert "model_actual" not in bundle.payload

    def test_w2_to_w3_strips_family_actual(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w2_output_sample()
        bundle = assembler.assemble("W2→W3", source)
        assert "family_actual" not in bundle.payload

    def test_w2_to_w3_strips_build_log(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w2_output_sample()
        bundle = assembler.assemble("W2→W3", source)
        assert "build_log" not in bundle.payload

    def test_w3_to_w4_strips_synthesis_rationale(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w3_output_sample()
        bundle = assembler.assemble("W3→W4", source)
        assert "synthesis_rationale" not in bundle.payload

    def test_w3_to_w4_strips_conflict_resolutions(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w3_output_sample()
        bundle = assembler.assemble("W3→W4", source)
        assert "conflict_resolutions" not in bundle.payload

    def test_w3_to_w4_strips_synthesis_log(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w3_output_sample()
        bundle = assembler.assemble("W3→W4", source)
        assert "synthesis_log" not in bundle.payload

    def test_w3_to_w4_includes_canonical_implementation(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w3_output_sample()
        bundle = assembler.assemble("W3→W4", source)
        assert bundle.payload.get("canonical_implementation") is not None

    def test_w3_to_w4_includes_mechanism_registry(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w3_output_sample()
        bundle = assembler.assemble("W3→W4", source)
        assert bundle.payload.get("mechanism_registry") is not None


# ---------------------------------------------------------------------------
# Include list enforcement
# ---------------------------------------------------------------------------

class TestIncludeListEnforcement:

    def test_missing_include_field_raises(self):
        """Assembly fails with FM-SPEC if include field is missing."""
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        # Remove a required include field
        del source["requirements"]

        with pytest.raises(BundleAssemblyError, match="FM-SPEC"):
            assembler.assemble("W1→W2", source)

    def test_null_include_field_raises(self):
        """Assembly fails with FM-SPEC if include field is null."""
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        source["requirements"] = None

        with pytest.raises(BundleAssemblyError, match="FM-SPEC"):
            assembler.assemble("W1→W2", source)

    def test_null_and_missing_both_caught(self):
        """Error message includes both NULL and MISSING fields."""
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        source["requirements"] = None
        del source["failure_modes"]

        with pytest.raises(BundleAssemblyError) as exc_info:
            assembler.assemble("W1→W2", source)
        err = str(exc_info.value)
        assert "NULL" in err or "MISSING" in err


# ---------------------------------------------------------------------------
# Hash computation
# ---------------------------------------------------------------------------

class TestBundleHashing:

    def test_bundle_has_non_empty_hash(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        bundle = assembler.assemble("W1→W2", source)
        assert bundle.bundle_hash
        assert len(bundle.bundle_hash) == 64  # SHA-256 hex

    def test_bundle_hash_is_deterministic(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        b1 = assembler.assemble("W1→W2", source)
        b2 = assembler.assemble("W1→W2", source)
        assert b1.bundle_hash == b2.bundle_hash

    def test_different_payloads_produce_different_hashes(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        s1 = w1_output_sample()
        s2 = w1_output_sample()
        s2["architecture_overview"] = "Different architecture"
        b1 = assembler.assemble("W1→W2", s1)
        b2 = assembler.assemble("W1→W2", s2)
        assert b1.bundle_hash != b2.bundle_hash

    def test_input_hashes_recorded(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        bundle = assembler.assemble("W1→W2", source)
        assert isinstance(bundle.input_hashes, dict)
        for key, val in bundle.input_hashes.items():
            assert val.startswith("sha256:")


# ---------------------------------------------------------------------------
# Multi-agent fan-out
# ---------------------------------------------------------------------------

class TestMultiAgentFanOut:

    def test_assemble_for_agents_returns_n_bundles(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        bundles = assembler.assemble_for_agents("W1→W2", source, agent_count=3)
        assert len(bundles) == 3

    def test_each_agent_gets_unique_isolation_id(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        bundles = assembler.assemble_for_agents("W1→W2", source, agent_count=3)
        ids = [b.agent_isolation_id for b in bundles]
        assert len(set(ids)) == 3, "Each agent must have a unique isolation ID"

    def test_each_agent_gets_unique_bundle_id(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        bundles = assembler.assemble_for_agents("W1→W2", source, agent_count=3)
        bids = [b.bundle_id for b in bundles]
        assert len(set(bids)) == 3

    def test_fan_out_payloads_are_equal(self):
        """All agents in same wave get the same payload content."""
        assembler = BundleAssembler(run_id="HRR-TEST")
        source = w1_output_sample()
        bundles = assembler.assemble_for_agents("W1→W2", source, agent_count=3)
        payloads = [json.dumps(b.payload, sort_keys=True) for b in bundles]
        assert len(set(payloads)) == 1, "All agents in same wave should get identical payload"


# ---------------------------------------------------------------------------
# Manifest recording
# ---------------------------------------------------------------------------

class TestManifestRecording:

    def test_manifest_records_grow_per_assembly(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        assembler.assemble("W1→W2", w1_output_sample())
        # W2→W3 needs different source
        assembler.assemble("W2→W3", w2_output_sample())
        assert len(assembler.manifest_records) == 2

    def test_manifest_records_strip_list(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        assembler.assemble("W1→W2", w1_output_sample())
        record = assembler.manifest_records[0]
        assert "residue.minority_dissent" in record.strip_list_applied

    def test_manifest_records_include_bundle_hash(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        bundle = assembler.assemble("W1→W2", w1_output_sample())
        record = assembler.manifest_records[0]
        assert record.bundle_hash == bundle.bundle_hash

    def test_manifest_include_check_passed(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        assembler.assemble("W1→W2", w1_output_sample())
        record = assembler.manifest_records[0]
        assert record.include_check_passed is True

    def test_manifest_strip_check_passed(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        assembler.assemble("W1→W2", w1_output_sample())
        record = assembler.manifest_records[0]
        assert record.strip_check_passed is True

    def test_dump_manifest_returns_dicts(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        assembler.assemble("W1→W2", w1_output_sample())
        manifests = assembler.dump_manifest()
        assert isinstance(manifests, list)
        assert isinstance(manifests[0], dict)
        assert "bundle_hash" in manifests[0]


# ---------------------------------------------------------------------------
# Unknown transition
# ---------------------------------------------------------------------------

class TestUnknownTransition:

    def test_unknown_transition_raises(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        with pytest.raises(UnknownTransitionError):
            assembler.assemble("W99→W100", {})


# ---------------------------------------------------------------------------
# Filesystem namespace isolation
# ---------------------------------------------------------------------------

class TestFilesystemNamespace:

    def test_write_to_namespace_creates_file(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        bundle = assembler.assemble("W1→W2", w1_output_sample())
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            path = BundleAssembler.write_to_namespace(
                "HRR-TEST",
                bundle.agent_isolation_id,
                bundle,
                base,
            )
            assert path.exists()
            content = json.loads(path.read_text())
            assert content["bundle_id"] == bundle.bundle_id

    def test_write_to_same_namespace_twice_raises(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        bundle = assembler.assemble("W1→W2", w1_output_sample())
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            # First write
            BundleAssembler.write_to_namespace(
                "HRR-TEST", bundle.agent_isolation_id, bundle, base
            )
            # Second write to same namespace → should raise (or overwrite)
            # Spec mandates unique namespaces per agent invocation;
            # FileExistsError signals collision
            with pytest.raises(FileExistsError):
                BundleAssembler.write_to_namespace(
                    "HRR-TEST", bundle.agent_isolation_id, bundle, base
                )


# ---------------------------------------------------------------------------
# ArtifactStore
# ---------------------------------------------------------------------------

class TestArtifactStore:

    def test_store_and_load_artifact(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ArtifactStore(Path(tmpdir))
            artifact = {"data": "hello", "number": 42}
            aid = store.store(artifact, wave="W2", agent_isolation_id="agent_001")
            loaded = store.load(aid)
            assert loaded == artifact

    def test_artifact_hash_verification(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ArtifactStore(Path(tmpdir))
            artifact = {"data": "integrity test"}
            aid = store.store(artifact, wave="W2", agent_isolation_id="agent_001")
            assert store.verify_hash(aid) is True

    def test_load_unknown_artifact_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ArtifactStore(Path(tmpdir))
            with pytest.raises(KeyError):
                store.load("nonexistent-artifact-id")


# ---------------------------------------------------------------------------
# Task description rendering
# ---------------------------------------------------------------------------

class TestTaskDescriptionRendering:

    def test_bundle_to_task_description_is_valid_json(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        bundle = assembler.assemble("W1→W2", w1_output_sample())
        task_desc = bundle.to_task_description()
        parsed = json.loads(task_desc)
        assert "bundle_id" in parsed
        assert "wave" in parsed
        assert "payload" in parsed

    def test_bundle_to_dict_excludes_payload(self):
        assembler = BundleAssembler(run_id="HRR-TEST")
        bundle = assembler.assemble("W1→W2", w1_output_sample())
        d = bundle.to_dict()
        assert "payload" not in d, "Manifest records should not include full payload (too large)"
        assert "bundle_hash" in d


# ---------------------------------------------------------------------------
# Helper function tests
# ---------------------------------------------------------------------------

class TestHelpers:

    def test_nested_get_dotted_key(self):
        obj = {"a": {"b": {"c": "found"}}}
        val = _nested_get(obj, "a.b.c")
        assert val == "found"

    def test_nested_get_missing_key(self):
        obj = {"a": {"b": {}}}
        val = _nested_get(obj, "a.b.c")
        assert isinstance(val, type(_MISSING))

    def test_nested_delete_dotted_key(self):
        obj = {"a": {"b": {"c": "will_be_deleted"}}}
        deleted = _nested_delete(obj, "a.b.c")
        assert deleted is True
        assert "c" not in obj["a"]["b"]

    def test_nested_delete_missing_key_returns_false(self):
        obj = {"a": {}}
        deleted = _nested_delete(obj, "a.b.c")
        assert deleted is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
