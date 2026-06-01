import pytest
import ast
import os

SUBSTRATE_DIR = "golden_quill_substrate"

def test_guard_001_acceptance_tests_not_modified():
    # Prove acceptance tests were not weakened or skipped
    with open("tests/test_v03_acceptance_contract.py", "r") as f:
        tree = ast.parse(f.read())
    
    test_count = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_t"):
            test_count += 1
            # Ensure no @pytest.mark.skip is present
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Attribute) and decorator.attr == "skip":
                    pytest.fail(f"Test {node.name} is skipped!")
    
    assert test_count == 15, f"Expected 15 acceptance tests, found {test_count}"

def test_guard_002_contracts_not_relaxed():
    # Prove Pydantic contracts and enum constraints were not relaxed
    with open(f"{SUBSTRATE_DIR}/contracts.py", "r") as f:
        tree = ast.parse(f.read())
    
    found_route_mode = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "RouteMode":
                    # Check allowed values
                    if isinstance(node.value, ast.Subscript):
                        # Literal['LOCAL_ONLY', 'HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT', 'ALL_MODEL_ACCESS']
                        found_route_mode = True
                        slice_node = getattr(node.value, "slice", None)
                        if isinstance(slice_node, ast.Tuple):
                            allowed_values = [elt.value for elt in slice_node.elts if isinstance(elt, ast.Constant)]
                            assert "LOCAL_ONLY" in allowed_values
                            assert "HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT" in allowed_values
                            assert "ALL_MODEL_ACCESS" in allowed_values
                            assert "CLOUD_ONLY" not in allowed_values
                            assert "SANITIZED_CLOUD_ALLOWED" not in allowed_values
    
    assert found_route_mode, "RouteMode definition missing or altered in contracts.py"

def test_guard_003_no_sanitization_routing():
    # Do not introduce sanitization routing
    with open(f"{SUBSTRATE_DIR}/contracts.py", "r") as f:
        content = f.read()
    assert "SANITIZED" not in content
    assert "CLOUD_ONLY" not in content
    assert "CLOUD_PUBLIC_ONLY" not in content
    with open(f"{SUBSTRATE_DIR}/ingress.py", "r") as f:
        content = f.read()
    assert "SANITIZED" not in content
    assert "CLOUD_ONLY" not in content
    assert "CLOUD_PUBLIC_ONLY" not in content

def test_guard_004_no_directories_moved():
    assert os.path.isdir(SUBSTRATE_DIR)
    assert os.path.isfile(f"{SUBSTRATE_DIR}/contracts.py")

def test_guard_005_lightweight_di():
    # Use lightweight Python-native DI only
    with open(f"{SUBSTRATE_DIR}/di.py", "r") as f:
        tree = ast.parse(f.read())
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            module = getattr(node, "module", None)
            if module:
                assert "dependency_injector" not in module
            for alias in node.names:
                assert "dependency_injector" not in alias.name

def test_guard_006_brain_import_boundary():
    # Prove no DB, Memory repository, vector DB, or raw Gate Runner authority can be imported or resolved.
    with open(f"{SUBSTRATE_DIR}/di.py", "r") as f:
        tree = ast.parse(f.read())

    blocked_items = set()
    found_brain_check = False
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "resolve":
            for stmt in node.body:
                if isinstance(stmt, ast.Assign):
                    for target in stmt.targets:
                        if isinstance(target, ast.Name) and target.id == "forbidden_for_brain":
                            if isinstance(stmt.value, ast.List):
                                for elt in stmt.value.elts:
                                    if isinstance(elt, ast.Constant):
                                        blocked_items.add(elt.value)
                
                if isinstance(stmt, ast.If):
                    condition_str = ast.unparse(stmt.test)
                    if "context == 'brain'" in condition_str or 'context == "brain"' in condition_str:
                        found_brain_check = True

    assert found_brain_check, "Brain context boundary not found in DI container"
    assert "database_client" in blocked_items
    assert "memory_repository" in blocked_items
    assert "vector_db" in blocked_items
    assert "gate_runner_authority" in blocked_items

def test_guard_007_archivist_prefilter():
    # Prove vector search cannot execute before SQL applied_as_entity_id prefilter
    with open(f"{SUBSTRATE_DIR}/archivist.py", "r") as f:
        tree = ast.parse(f.read())
    
    found_expected = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "expected":
                    if isinstance(node.value, ast.List):
                        items = [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)]
                        sql_index = items.index("SQL_APPLIED_AS_PREFILTER")
                        vector_index = items.index("VECTOR_SEARCH")
                        assert sql_index < vector_index, "Vector search executes before SQL prefilter!"
                        found_expected = True
    assert found_expected

def test_guard_008_hybrid_egress_serialization():
    # Hybrid egress guard must prove non-public Vault canary data cannot serialize outward by type, hash, sensitivity label, and custody classification
    with open(f"{SUBSTRATE_DIR}/model_boundary.py", "r") as f:
        tree = ast.parse(f.read())
        
    found_custody_check = False
    found_sensitivity_check = False
    found_type_check = False
    found_hash_check = False
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            test_code = ast.unparse(node.test)
            if "custody_classification" in test_code:
                found_custody_check = True
            if "sensitivity_label" in test_code:
                found_sensitivity_check = True
            if "evidence_type" in test_code:
                found_type_check = True
            if "evidence_hash" in test_code:
                found_hash_check = True
                
    assert found_custody_check, "Missing custody_classification serialization check"
    assert found_sensitivity_check, "Missing sensitivity_label serialization check"
    assert found_type_check, "Missing evidence_type serialization check"
    assert found_hash_check, "Missing evidence_hash serialization check"

def test_guard_009_all_model_access_requires_auth():
    # ALL_MODEL_ACCESS must require explicit authorization
    with open(f"{SUBSTRATE_DIR}/ingress.py", "r") as f:
        tree = ast.parse(f.read())
    
    found_check = False
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            test_code = ast.unparse(node.test)
            if "ALL_MODEL_ACCESS" in test_code:
                body_code = ast.unparse(node.body)
                if "explicit_customer_authorization" in body_code:
                    found_check = True
                    
    assert found_check, "Missing explicit customer authorization check for ALL_MODEL_ACCESS"

def test_guard_010_final_packet_authorization():
    # Final Packet Authorization guard must prove human actor + human reauth + human presence + eligibility + Applied-As match
    with open(f"{SUBSTRATE_DIR}/logician.py", "r") as f:
        tree = ast.parse(f.read())
        
    found_packet_auth_check = False
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            test_code = ast.unparse(node.test)
            if "packet.authorize_final" in test_code:
                found_packet_auth_check = True
                body_code = ast.unparse(node.body)
                assert "actor_type != 'HUMAN'" in body_code or "actor_type != \"HUMAN\"" in body_code
                assert "is_human_final_authorization_capable" in body_code
                assert "applied_as_entity_id !=" in body_code or "applied_as_entity_id !=" in test_code
                
        # Also ensure that an exception is raised when applied_as doesn't match
        if isinstance(node, ast.If):
            test_code = ast.unparse(node.test)
            if "applied_as_entity_id !=" in test_code:
                body_code = ast.unparse(node.body)
                assert "_raise_security_failure" in body_code or "raise " in body_code
    
    assert found_packet_auth_check, "Missing Final Packet Authorization gate logic"

def test_guard_011_behavioral_applied_as_mismatch_blocked():
    from golden_quill_substrate.contracts import RequestEnvelope, IdentityContext
    from golden_quill_substrate.logician import run_pre_gates
    from golden_quill_substrate.errors import SubstrateError
    from uuid import uuid4

    # 2. Add a runtime guard test that actually constructs an envelope with:
    #    * `operation_type == "packet.authorize_final"`
    #    * `identity_context.actor_type == "HUMAN"`
    #    * valid human final authorization capability
    #    * mismatched `identity_context.applied_as_entity_id` vs payload target entity
    #    The test must assert that the operation is blocked. Do not merely AST-check that a comparison exists.

    valid_applied_as = uuid4()
    envelope = RequestEnvelope(
        request_id=uuid4(),
        operation_type="packet.authorize_final",
        correlation_id=uuid4(),
        target={"resource_type": "PACKET", "applied_as_entity_id": valid_applied_as},
        declared_purpose="Test final authorization",
        requested_route_mode="LOCAL_ONLY",
        identity_context=IdentityContext(
            principal_id=uuid4(),
            actor_type="HUMAN",
            auth_strength="HUMAN_REAUTH",
            human_present=True,
            final_authorization_eligible=True,
            issued_at="2026-05-23T00:00:00Z",
            expires_at="2026-05-24T00:00:00Z",
            applied_as_entity_id=valid_applied_as,
            session_id=str(uuid4()),
            licensed_node_id=str(uuid4()),
            licensed_customer_entity_id=uuid4(),
            auth_token_id=str(uuid4()),
            actor_binding_hash=str(uuid4()) * 2,
            request_origin="INTERNAL_SERVICE"
        ),
        payload={"target_entity_id": uuid4()} # Mismatched payload target
    )

    with pytest.raises(SubstrateError) as exc:
        run_pre_gates(envelope)

    # Must return/block with 403 AUTHORIZATION.APPLIED_AS_MISMATCH and GateFailure.failure_type == SECURITY_FAILURE
    assert exc.value.status_code == 403
    assert exc.value.error.code == "AUTHORIZATION.APPLIED_AS_MISMATCH"
    assert len(exc.value.error.gate_failures) > 0
    assert exc.value.error.gate_failures[0].failure_type == "SECURITY_FAILURE"


@pytest.mark.asyncio
async def test_guard_012_behavioral_hybrid_egress_blocked():
    from golden_quill_substrate.model_boundary import MockModelBoundary
    
    boundary = MockModelBoundary()
    
    # 1. Test evidence_type block
    response1 = await boundary.invoke(
        route_mode="HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT",
        outbound_payload={"some_key": {"evidence_type": "INTERNAL_MEMORY"}},
        known_non_public_canaries=["secret_hash_123"]
    )
    assert response1.status_code == 403
    assert response1.error.code == "MODEL_BOUNDARY.HYBRID_VAULT_EGRESS_ATTEMPT"
    
    # 2. Test evidence_hash block
    response2 = await boundary.invoke(
        route_mode="HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT",
        outbound_payload={"some_key": {"evidence_hash": "secret_hash_123"}},
        known_non_public_canaries=["secret_hash_123"]
    )
    assert response2.status_code == 403
    assert response2.error.code == "MODEL_BOUNDARY.HYBRID_VAULT_EGRESS_ATTEMPT"
