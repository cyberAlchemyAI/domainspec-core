import pytest
from fastapi import HTTPException
from pipeline.nervous_system.models import IdentityContext
from pipeline.nervous_system.governance import require_human_reauth

def test_require_human_reauth_missing_origin_defaults_to_system_and_fails():
    # 1. missing origin defaults to system and cannot authorize final packet
    identity = IdentityContext(
        user_id="demo_operator",
        applied_as="tilth_admin",
        is_human=True
    )
    assert identity.origin == "system"
    with pytest.raises(HTTPException) as excinfo:
        require_human_reauth(identity)
    assert excinfo.value.status_code == 403
    assert "origin: human_direct" in excinfo.value.detail

def test_require_human_reauth_conversation_agent_fails():
    # 2. conversation_agent + is_human true still cannot authorize final packet
    identity = IdentityContext(
        user_id="demo_operator",
        applied_as="tilth_admin",
        is_human=True,
        origin="conversation_agent"
    )
    with pytest.raises(HTTPException) as excinfo:
        require_human_reauth(identity)
    assert excinfo.value.status_code == 403
    assert "origin: human_direct" in excinfo.value.detail

def test_require_human_reauth_scheduled_fails():
    # 3. scheduled + is_human true cannot authorize final packet
    identity = IdentityContext(
        user_id="demo_operator",
        applied_as="tilth_admin",
        is_human=True,
        origin="scheduled"
    )
    with pytest.raises(HTTPException) as excinfo:
        require_human_reauth(identity)
    assert excinfo.value.status_code == 403
    assert "origin: human_direct" in excinfo.value.detail

def test_require_human_reauth_system_fails():
    # 4. system + is_human true cannot authorize final packet
    identity = IdentityContext(
        user_id="demo_operator",
        applied_as="tilth_admin",
        is_human=True,
        origin="system"
    )
    with pytest.raises(HTTPException) as excinfo:
        require_human_reauth(identity)
    assert excinfo.value.status_code == 403
    assert "origin: human_direct" in excinfo.value.detail

def test_require_human_reauth_human_direct_but_not_human_fails():
    # 5. human_direct + is_human false cannot authorize final packet
    identity = IdentityContext(
        user_id="demo_operator",
        applied_as="tilth_admin",
        is_human=False,
        origin="human_direct"
    )
    with pytest.raises(HTTPException) as excinfo:
        require_human_reauth(identity)
    assert excinfo.value.status_code == 403
    assert "requires human re-auth" in excinfo.value.detail

def test_require_human_reauth_human_direct_and_human_passes():
    # 6. human_direct + is_human true can authorize the allowed human-required action
    identity = IdentityContext(
        user_id="demo_operator",
        applied_as="tilth_admin",
        is_human=True,
        origin="human_direct"
    )
    # Should not raise
    require_human_reauth(identity)
