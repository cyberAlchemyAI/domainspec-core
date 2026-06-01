"""
Root test configuration.

Inserts the gpp/ source directory into sys.path *before* pytest begins
collecting test modules so that pytest-cov can instrument gpp_det,
gpp_council_dispatch, and gpp_manifest by their plain module names.
"""

from __future__ import annotations

import sys
from pathlib import Path

_GPP_DIR = (
    Path(__file__).resolve().parent.parent
    / "pipeline"
    / "validation"
    / "integration_scope_close_2026-04-19"
    / "gpp"
)

if _GPP_DIR.is_dir() and str(_GPP_DIR) not in sys.path:
    sys.path.insert(0, str(_GPP_DIR))

import pytest
from golden_quill_substrate.di import container
from golden_quill_substrate.archivist import ArchivistPipeline, MockArchivist
from golden_quill_substrate.model_boundary import MockModelBoundary
from golden_quill_substrate.memory import MockMemoryStore
from golden_quill_substrate.packet import MockPacketEngine
from golden_quill_substrate.contracts import StateMachineContext, IdentityContext, GateResult
from uuid import uuid4

@pytest.fixture
def di_container():
    archivist = MockArchivist()
    container.register("archivist", archivist)
    return container

@pytest.fixture
def mock_archivist_pipeline():
    return ArchivistPipeline()

@pytest.fixture
def mock_model_boundary():
    return MockModelBoundary()

@pytest.fixture
def mock_memory_store():
    return MockMemoryStore()

@pytest.fixture
def sm_context():
    return StateMachineContext(
        state_machine_run_id=uuid4(),
        request_id=uuid4(),
        correlation_id=uuid4(),
        identity_context=IdentityContext(
            principal_id=uuid4(),
            actor_type="STATE_MACHINE_RUNNER",
            auth_strength="SESSION",
            human_present=False,
            final_authorization_eligible=False,
            issued_at="2026-05-23T00:00:00Z",
            expires_at="2026-05-24T00:00:00Z",
            applied_as_entity_id=uuid4(),
            session_id=str(uuid4()),
            licensed_node_id=str(uuid4()),
            licensed_customer_entity_id=uuid4(),
            auth_token_id=str(uuid4()),
            actor_binding_hash=str(uuid4()) * 2,
            request_origin="INTERNAL_SERVICE"
        ),
        authorized_transition="REVIEW",
        pre_commit_gate_result=GateResult(
            request_id=uuid4(),
            correlation_id=uuid4(),
            stage="POST",
            passed=True,
            failures=[],
            evaluated_gate_ids=["test_gate"],
            policy_pack_version="1.0",
            completed_at="2026-05-23T00:00:00Z"
        )
    )

@pytest.fixture
def mock_packet_engine():
    return MockPacketEngine()

@pytest.fixture
def mock_archivist():
    archivist = MockArchivist()
    container.register("archivist", archivist)
    return archivist
