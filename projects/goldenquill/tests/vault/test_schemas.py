"""Unit tests for pipeline.vault.schemas (§2.1–§2.10).

Round K. Every schema is a frozen, keyword-only dataclass; this suite verifies
frozen discipline, canonical JSON round-trip, and kw-only construction gates.
"""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError, asdict

import pytest

from pipeline.sovereignty.audit import canonical_json_bytes
from pipeline.vault.schemas import (
    CompoundTxnState,
    FDBrokerRequest,
    FDBrokerResponse,
    IdentityTuple,
    ProcessWrapperManifest,
    SandboxProfileManifest,
    SeccompFilterManifest,
    SectionLockMarker,
    SeedFile,
    StableUUIDFloor,
    StagedWrite,
    TrustRootMirrorManifest,
    VaultInitMarker,
    VaultSharedSeedManifest,
)


def _identity() -> IdentityTuple:
    return IdentityTuple(
        volume_uuid="a" * 32,
        fs_file_id="b" * 16,
        mount_id="c" * 8,
        fs_type="apfs",
        captured_at="2026-04-19T00:00:00Z",
    )


class TestFrozenDiscipline:
    def test_identity_tuple_frozen(self) -> None:
        tup = _identity()
        with pytest.raises(FrozenInstanceError):
            tup.fs_type = "ext4"  # type: ignore[misc]

    def test_staged_write_frozen(self) -> None:
        sw = StagedWrite(
            intent="index-update",
            path="orgs/x/vault/drafts/y.json",
            data=b"payload",
            data_sha3_512="0" * 128,
            data_len=7,
            expected_current_file_hash=None,
            write_mode="overwrite",
            staged_at_monotonic_ns=1,
        )
        with pytest.raises(FrozenInstanceError):
            sw.intent = "other"  # type: ignore[misc]

    def test_compound_txn_state_default_staged_writes_is_tuple(self) -> None:
        st = CompoundTxnState(
            txn_kind="index_amendment",
            txn_token="tok",
            session_id="s1",
            created_at_monotonic_ns=0,
        )
        assert isinstance(st.staged_writes, tuple)
        assert st.staged_writes == ()


class TestKWOnly:
    def test_identity_tuple_rejects_positional(self) -> None:
        with pytest.raises(TypeError):
            IdentityTuple("a" * 32, "b" * 16, "c", "apfs", "2026-04-19T00:00:00Z")  # type: ignore[misc]

    def test_init_marker_rejects_positional(self) -> None:
        with pytest.raises(TypeError):
            VaultInitMarker(  # type: ignore[misc]
                "org",
                "slug",
                "2026-04-19T00:00:00Z",
                "uuid",
                _identity(),
                "op",
                "0" * 128,
            )


class TestCanonicalJsonRoundTrip:
    def test_init_marker_canonical_json_deterministic(self) -> None:
        m = VaultInitMarker(
            scope="org",
            slug="mycosymbiotics",
            created_at="2026-04-19T00:00:00Z",
            created_under_uuid="d" * 32,
            identity_tuple=_identity(),
            operator_id="josh",
            section_lock_hash="e" * 128,
        )
        b1 = canonical_json_bytes(asdict(m))
        b2 = canonical_json_bytes(asdict(m))
        assert b1 == b2
        # separators must be tight
        assert b" " not in b1
        assert b"\n" not in b1
        decoded = json.loads(b1)
        assert decoded["scope"] == "org"
        assert decoded["identity_tuple"]["fs_type"] == "apfs"

    def test_seed_manifest_files_tuple_preserved_under_asdict(self) -> None:
        f = SeedFile(
            relative_path="cedar/org_isolation.cedar",
            content_hash="f" * 128,
            size_bytes=128,
            mode=0o440,
            identity_tuple=_identity(),
        )
        m = VaultSharedSeedManifest(
            head_hash="1" * 128,
            files=(f,),
            committed_at="2026-04-19T00:00:00Z",
            committed_by="josh",
            m15_ledger_head="2" * 128,
            signature="3" * 128,
        )
        as_dict = asdict(m)
        # asdict recurses over tuples preserving them as tuples (Python 3.14)
        assert len(as_dict["files"]) == 1
        assert as_dict["files"][0]["relative_path"] == "cedar/org_isolation.cedar"
        # canonical JSON serialises tuples as JSON arrays
        canonical = canonical_json_bytes(as_dict)
        decoded = json.loads(canonical)
        assert isinstance(decoded["files"], list)


class TestWrapperManifest:
    def test_mode_field_preserves_octal(self) -> None:
        w = ProcessWrapperManifest(
            platform="macos-launchd",
            wrapper_path="vault_shared/process_wrappers/macos-launchd/com.tilth.seat.plist",
            content_hash="4" * 128,
            identity_tuple=_identity(),
            m15_ledger_head="5" * 128,
            mode=0o550,
        )
        assert w.mode == 0o550


class TestFDBrokerRoundTrip:
    def test_request_and_response_compose(self) -> None:
        req = FDBrokerRequest(
            requester_skill="vault-query",
            requester_pid=1234,
            requester_session_id="s1",
            requester_org_slug="mycosymbiotics",
            requested_path="orgs/mycosymbiotics/vault/drafts/x.json",
            intent="read",
            nonce_hex="00" * 32,
        )
        resp = FDBrokerResponse(
            granted=True,
            denial_reason="",
            fd_count=1,
            issued_at="2026-04-19T00:00:01Z",
            identity_tuple=_identity(),
            cedar_decision_id="dec-1",
        )
        assert req.intent == "read"
        assert resp.granted is True


class TestManifests:
    def test_seccomp_and_sandbox_manifest_shapes(self) -> None:
        s = SeccompFilterManifest(
            platform="linux",
            filter_bpf_hash="6" * 128,
            denied_syscalls=("io_uring_setup", "bpf", "perf_event_open"),
            m15_ledger_head="7" * 128,
            operator_signature="8" * 128,
        )
        sb = SandboxProfileManifest(
            platform="macos",
            profile_text_hash="9" * 128,
            denied_primitives=("task_for_pid", "clonefile"),
            m15_ledger_head="a" * 128,
            operator_signature="b" * 128,
        )
        assert s.denied_syscalls[0] == "io_uring_setup"
        assert sb.denied_primitives[1] == "clonefile"

    def test_trust_root_mirror_manifest(self) -> None:
        m = TrustRootMirrorManifest(
            mirror_path="/home/josh/.tilth/logician_trust_root/router.yaml",
            content_hash="c" * 128,
            identity_tuple=_identity(),
            m15_ledger_head="d" * 128,
            operator_signature="e" * 128,
            signed_at="2026-04-19T00:00:00Z",
            immutability_flag_set=True,
        )
        assert m.immutability_flag_set is True


class TestSectionLockMarker:
    def test_default_section_id(self) -> None:
        m = SectionLockMarker(
            version="v1",
            locked_at="2026-04-19T00:00:00Z",
            locked_by="josh",
            architecture_head_hash="f" * 128,
            blueprint_content_hash="0" * 128,
            m15_ledger_head="1" * 128,
            operator_signature="2" * 128,
        )
        assert m.section == "02-vault-topology"


class TestStableUUIDFloor:
    def test_rejection_reason_empty_on_accept(self) -> None:
        fl = StableUUIDFloor(
            fs_type="apfs",
            volume_uuid="a" * 32,
            accepted=True,
            rejection_reason="",
            evaluated_at="2026-04-19T00:00:00Z",
        )
        assert fl.accepted is True
        assert fl.rejection_reason == ""

# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS pin — drift-detection guard (§4.6 engineering_process_v0.1.md)
# ---------------------------------------------------------------------------


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        from pipeline.vault import schemas as _mod

        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
