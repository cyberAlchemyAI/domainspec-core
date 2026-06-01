"""Section 1 Round J capstone — J.1 boot-sequence integration tests.

Cross-module lifecycle tests that exercise the full §1 public surface
as a single boot → session → ingest → seal → record loop. Each test
class targets ≥3 §1 modules per spec card.

Blueprint anchor: `pipeline/blueprint/v0.1/section_1_sovereignty_envelope.md`
v6 (LOCKED 2026-04-18). Round J scope per spec card J.1.
"""

from __future__ import annotations

import datetime as _dt
import json
import time
from pathlib import Path
from unittest import mock

import pytest

from pipeline.sovereignty import (
    DegradationEvent,
    LedgerState,
    OperatorNotProvisioned,
    RepoRootInvalid,
    RFADriftError,
    RFAEnvelope,
    RFAMissing,
    SEVERITY_LIMITS,
    Session,
    SovereigntyEnvelope,
    UnsupportedPlatform,
    bypass_is_active,
    boot_envelope,
    canonical_slug,
    canonicalize_router_yaml_bytes,
    end_session,
    ensure_slug_available,
    hmac_sha3_512,
    ingest_rfa,
    read_boot_clock_history,
    read_ledger_tail,
    record_admin_risk,
    record_degradation,
    reverify_rfa,
    seal_project_context,
    sha3_512_hex,
    sign_health_tuple,
    start_session,
    verify_chain,
    verify_project_context,
    verify_router_integrity,
)
from pipeline.sovereignty import session as _session_mod
from pipeline.sovereignty.admin_risk import RateLimitExceeded, OperatorConfirmationRequired
from pipeline.sovereignty.router_integrity import RouterHMACMismatch
from pipeline.sovereignty.org_slug import SlugCollisionError, InvalidSlug
from pipeline.sovereignty.project_context_envelope import ProjectContextDrift

from tests.sovereignty.conftest import (
    CAPSTONE_BASE_ROUTER_YAML,
    CAPSTONE_DEGRADATION_KEY,
    CAPSTONE_HMAC_KEY,
    CAPSTONE_LEDGER_KEY,
    CAPSTONE_WATERMARKS_KEY,
    CapstoneKeyStore,
    run_git,
    write_signed_router,
)


# ---------------------------------------------------------------------------
# Helpers local to integration
# ---------------------------------------------------------------------------


class _EnvelopeFacade:
    """Duck-typed envelope start_session accepts.

    Built from the SovereigntyEnvelope returned by boot_envelope. Carries
    ``router_manifest_sha``, ``keystore`` and ``repo_root``.
    """

    def __init__(self, env: SovereigntyEnvelope) -> None:
        self.router_manifest_sha = env.router_manifest.router_yaml_sha
        self.keystore = env.keystore
        self.repo_root = env.repo_root


class _RFAFacade:
    def __init__(self, slug: str) -> None:
        self.session_bound_slug = slug


class _PCFacade:
    def __init__(self, slug: str) -> None:
        self.slug = slug


@pytest.fixture(autouse=True)
def _ensure_clean_runtime():
    """Belt-and-braces: clear any prior session-runtime binding."""
    _session_mod._set_active_runtime(None)
    yield
    _session_mod._set_active_runtime(None)


def _boot_with_ledgers(
    repo: Path, keystore: CapstoneKeyStore
) -> SovereigntyEnvelope:
    """Boot the envelope wiring up both ledger verifiers.

    Ledgers are verified only when the on-disk files already exist.
    First boot always succeeds with the mapping supplied.
    """
    return boot_envelope(
        repo_root=repo,
        keystore=keystore,
        ledger_hmac_keys={
            "admin_risk": CAPSTONE_LEDGER_KEY,
            "degradation": CAPSTONE_DEGRADATION_KEY,
        },
        watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
    )


# ===========================================================================
# J.1.1 — Boot + Session lifecycle (boot.py + session.py + interrupted_state.py)
# ===========================================================================


class TestBootSessionLifecycle:
    def test_boot_then_start_session_happy(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
        capstone_slug: str,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        sess = start_session(
            envelope=_EnvelopeFacade(env),
            rfa=_RFAFacade(capstone_slug),
            project_context=_PCFacade(capstone_slug),
        )
        try:
            assert isinstance(sess, Session)
            assert sess.slug == capstone_slug
            assert sess.status == "ACTIVE"
            assert sess.router_manifest_sha == env.router_manifest.router_yaml_sha
            # .active.lock file must exist under repo_root.
            assert (capstone_repo / "sovereignty" / "sessions" / ".active.lock").is_file()
        finally:
            end_session(sess)

    def test_session_end_releases_active_lock(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
        capstone_slug: str,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        sess = start_session(
            envelope=_EnvelopeFacade(env),
            rfa=_RFAFacade(capstone_slug),
            project_context=_PCFacade(capstone_slug),
        )
        end_session(sess)
        # Second start_session must succeed (lock released).
        sess2 = start_session(
            envelope=_EnvelopeFacade(env),
            rfa=_RFAFacade(capstone_slug),
            project_context=_PCFacade(capstone_slug),
        )
        try:
            assert sess2.session_id != sess.session_id
        finally:
            end_session(sess2)

    def test_session_sign_health_tuple_roundtrip(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
        capstone_slug: str,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        sess = start_session(
            envelope=_EnvelopeFacade(env),
            rfa=_RFAFacade(capstone_slug),
            project_context=_PCFacade(capstone_slug),
        )
        try:
            mac = sign_health_tuple(sess, b"health-tuple-bytes")
            assert isinstance(mac, bytes)
            assert len(mac) == 64  # SHA3-512
        finally:
            end_session(sess)

    def test_adv_boot_with_missing_operator_identity_rejected(
        self, capstone_repo: Path
    ) -> None:
        ks = CapstoneKeyStore(operator_present=False)
        with pytest.raises(OperatorNotProvisioned):
            _boot_with_ledgers(capstone_repo, ks)

    def test_adv_boot_with_tampered_router_rejected(
        self, capstone_repo: Path, capstone_keystore: CapstoneKeyStore
    ) -> None:
        (capstone_repo / "router.yaml").write_bytes(
            CAPSTONE_BASE_ROUTER_YAML.replace(b"mistral:7b", b"claude-4-opus")
        )
        # Signature not refreshed.
        with pytest.raises(Exception):
            _boot_with_ledgers(capstone_repo, capstone_keystore)

    def test_adv_boot_unsupported_platform_rejected(
        self, capstone_repo: Path, capstone_keystore: CapstoneKeyStore
    ) -> None:
        with mock.patch(
            "pipeline.sovereignty.boot._platform_mod.system",
            return_value="Windows",
        ):
            with pytest.raises(UnsupportedPlatform):
                _boot_with_ledgers(capstone_repo, capstone_keystore)

    def test_adv_start_session_rejects_slug_mismatch(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        with pytest.raises(_session_mod.SessionSlugMismatch):
            start_session(
                envelope=_EnvelopeFacade(env),
                rfa=_RFAFacade("slug-a"),
                project_context=_PCFacade("slug-b"),
            )


# ===========================================================================
# J.1.2 — Boot + RFA ingest + reverify (boot.py + rfa_envelope.py + crypto_primitives)
# ===========================================================================


class TestBootRFAIngest:
    def test_boot_then_ingest_and_reverify(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
        capstone_slug: str,
        capstone_rfa_bytes: bytes,
        capstone_rfa_url: str,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        envelope = ingest_rfa(
            url=capstone_rfa_url,
            content_bytes=capstone_rfa_bytes,
            slug=capstone_slug,
            operator_id="josh",
            rfa_id="rfa-0001",
            repo_root=env.repo_root,
        )
        assert isinstance(envelope, RFAEnvelope)
        reverify_rfa(envelope)  # must not raise

    def test_two_ingests_same_url_distinct_content_hashes(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
        capstone_slug: str,
        capstone_rfa_bytes: bytes,
        capstone_rfa_url: str,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        e1 = ingest_rfa(
            url=capstone_rfa_url,
            content_bytes=capstone_rfa_bytes,
            slug=capstone_slug,
            operator_id="josh",
            rfa_id="rfa-a",
            repo_root=env.repo_root,
        )
        e2 = ingest_rfa(
            url=capstone_rfa_url,
            content_bytes=capstone_rfa_bytes,
            slug=capstone_slug,
            operator_id="josh",
            rfa_id="rfa-b",
            repo_root=env.repo_root,
        )
        # BT1: distinct nonce ⇒ distinct content_hash even for identical bytes.
        assert e1.hashes.content_hash != e2.hashes.content_hash
        assert e1.hashes.nonce_hex != e2.hashes.nonce_hex
        # URL hash is stable (no nonce by §2.1 invariant).
        assert e1.hashes.url_hash == e2.hashes.url_hash

    def test_adv_reverify_detects_content_mutation(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
        capstone_slug: str,
        capstone_rfa_bytes: bytes,
        capstone_rfa_url: str,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        envelope = ingest_rfa(
            url=capstone_rfa_url,
            content_bytes=capstone_rfa_bytes,
            slug=capstone_slug,
            operator_id="josh",
            rfa_id="rfa-mutate",
            repo_root=env.repo_root,
        )
        # Overwrite raw file with different content — size drifts first,
        # reverify fails fast on the stat-based size check.
        Path(envelope.canonical_path).write_bytes(
            capstone_rfa_bytes + b"TRAILING-DRIFT"
        )
        with pytest.raises(RFADriftError):
            reverify_rfa(envelope)

    def test_adv_reverify_detects_deleted_file(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
        capstone_slug: str,
        capstone_rfa_bytes: bytes,
        capstone_rfa_url: str,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        envelope = ingest_rfa(
            url=capstone_rfa_url,
            content_bytes=capstone_rfa_bytes,
            slug=capstone_slug,
            operator_id="josh",
            rfa_id="rfa-del",
            repo_root=env.repo_root,
        )
        Path(envelope.canonical_path).unlink()
        with pytest.raises(RFAMissing):
            reverify_rfa(envelope)

    def test_adv_reverify_detects_url_hash_drift(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
        capstone_slug: str,
        capstone_rfa_bytes: bytes,
        capstone_rfa_url: str,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        envelope = ingest_rfa(
            url=capstone_rfa_url,
            content_bytes=capstone_rfa_bytes,
            slug=capstone_slug,
            operator_id="josh",
            rfa_id="rfa-url",
            repo_root=env.repo_root,
        )
        # Build a tampered envelope with a different url_at_ingest.
        from dataclasses import replace
        tampered = replace(envelope, url_at_ingest=capstone_rfa_url + "?x=1")
        with pytest.raises(RFADriftError):
            reverify_rfa(tampered)


# ===========================================================================
# J.1.3 — Boot + PROJECT_CONTEXT seal + verify (boot + project_context + isolation)
# ===========================================================================


class TestBootProjectContext:
    def test_boot_then_seal_and_verify(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
        capstone_slug: str,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        envelope = seal_project_context(
            slug=capstone_slug,
            session_id="sess-001",
            repo_root=env.repo_root,
        )
        assert envelope.slug == capstone_slug
        assert envelope.bound_session_id == "sess-001"
        verify_project_context(envelope, repo_root=env.repo_root)

    def test_adv_verify_rejects_mutated_pc(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
        capstone_slug: str,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        envelope = seal_project_context(
            slug=capstone_slug,
            session_id="sess-002",
            repo_root=env.repo_root,
        )
        pc_path = capstone_org_dir / "PROJECT_CONTEXT.md"
        pc_path.write_text(pc_path.read_text() + "\nTAMPERED\n", encoding="utf-8")
        with pytest.raises(ProjectContextDrift):
            verify_project_context(envelope, repo_root=env.repo_root)

    def test_adv_seal_missing_pc_rejected(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_slug: str,
    ) -> None:
        _boot_with_ledgers(capstone_repo, capstone_keystore)
        # No org_dir fixture → no PROJECT_CONTEXT.md.
        (capstone_repo / "orgs" / capstone_slug).mkdir(parents=True, exist_ok=True)
        with pytest.raises(FileNotFoundError):
            seal_project_context(
                slug=capstone_slug,
                session_id="sess-miss",
                repo_root=capstone_repo,
            )

    def test_adv_seal_rejects_non_canonical_slug_type(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
    ) -> None:
        _boot_with_ledgers(capstone_repo, capstone_keystore)
        with pytest.raises(TypeError):
            seal_project_context(
                slug=123,  # type: ignore[arg-type]
                session_id="x",
                repo_root=capstone_repo,
            )


# ===========================================================================
# J.1.4 — Boot + admin_risk ledger (boot + admin_risk + audit)
# ===========================================================================


class TestBootAdminRisk:
    def test_boot_then_record_green_entry(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        entry = record_admin_risk(
            repo_root=env.repo_root,
            entry_kind="flagged_term_substitution",
            severity="GREEN",
            payload={"term": "equity", "accepted": True},
            hmac_key=CAPSTONE_LEDGER_KEY,
            watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
        )
        assert entry.severity == "GREEN"
        assert entry.seq_id == 1
        tail = read_ledger_tail(repo_root=env.repo_root, n=5)
        assert len(tail) == 1
        assert tail[0].entry_hash == entry.entry_hash

    def test_red_requires_operator_retype(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        with pytest.raises(OperatorConfirmationRequired):
            record_admin_risk(
                repo_root=env.repo_root,
                entry_kind="flagged_term_substitution",
                severity="RED",
                payload={"term": "illegal"},
                hmac_key=CAPSTONE_LEDGER_KEY,
                watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
            )

    def test_adv_rate_limit_red_cap_enforced(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        limit = SEVERITY_LIMITS["RED"]
        # Fill the daily window — RED limit is 10.
        for i in range(limit):
            record_admin_risk(
                repo_root=env.repo_root,
                entry_kind="flagged_term_substitution",
                severity="RED",
                payload={"term": f"t{i}"},
                operator_retype_confirmation=f"retype-{i}",
                hmac_key=CAPSTONE_LEDGER_KEY,
                watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
            )
        with pytest.raises(RateLimitExceeded):
            record_admin_risk(
                repo_root=env.repo_root,
                entry_kind="flagged_term_substitution",
                severity="RED",
                payload={"term": "overflow"},
                operator_retype_confirmation="retype-overflow",
                hmac_key=CAPSTONE_LEDGER_KEY,
                watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
            )

    def test_adv_boot_after_append_idempotent_init_marker(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env1 = _boot_with_ledgers(capstone_repo, capstone_keystore)
        record_admin_risk(
            repo_root=env1.repo_root,
            entry_kind="flagged_term_substitution",
            severity="YELLOW",
            payload={"t": "a"},
            hmac_key=CAPSTONE_LEDGER_KEY,
            watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
        )
        # Re-boot — should accept existing ledger state and NOT rewrite marker.
        env2 = _boot_with_ledgers(capstone_repo, capstone_keystore)
        assert env2.init_marker.init_version == env1.init_marker.init_version


# ===========================================================================
# J.1.5 — Boot + degradation log (boot + degradation_log + admin_risk.bypass)
# ===========================================================================


class TestBootDegradationLog:
    def test_boot_then_record_degraded_run(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        event = record_degradation(
            repo_root=env.repo_root,
            event_kind="author_seat_degraded_run",
            seat="scribe",
            reason_code="timeout",
            hmac_key=CAPSTONE_DEGRADATION_KEY,
            watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
            duration_seconds=45,
        )
        assert isinstance(event, DegradationEvent)
        assert event.seat == "scribe"
        verify_chain(repo_root=env.repo_root, hmac_key=CAPSTONE_DEGRADATION_KEY)

    def test_bypass_requires_operator_signature(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        with pytest.raises(ValueError):
            record_degradation(
                repo_root=env.repo_root,
                event_kind="review_seat_bypass_active",
                seat="red_team",
                reason_code="operator_override",
                hmac_key=CAPSTONE_DEGRADATION_KEY,
                watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
                signed_by_operator=False,
            )

    def test_bypass_is_active_lifecycle_happy(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        now = _dt.datetime.now(_dt.timezone.utc)
        expires_at = (now + _dt.timedelta(hours=1)).isoformat().replace(
            "+00:00", "Z"
        )
        mono_now = time.monotonic_ns()
        history = read_boot_clock_history(env.repo_root)
        event = record_degradation(
            repo_root=env.repo_root,
            event_kind="review_seat_bypass_active",
            seat="red_team",
            reason_code="operator_override",
            hmac_key=CAPSTONE_DEGRADATION_KEY,
            watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
            expires_at=expires_at,
            expires_monotonic_ns=mono_now + 10**12,
            boot_epoch_ns_at_issuance=env.boot_epoch_ns,
            signed_by_operator=True,
        )
        assert bypass_is_active(
            event,
            now_utc=now,
            now_mono_ns=mono_now,
            boot_clock_history=history,
        ) is True

    def test_adv_bypass_expired_when_wall_past(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        past = (
            _dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(hours=1)
        ).isoformat().replace("+00:00", "Z")
        now = _dt.datetime.now(_dt.timezone.utc)
        mono_now = time.monotonic_ns()
        history = read_boot_clock_history(env.repo_root)
        event = record_degradation(
            repo_root=env.repo_root,
            event_kind="review_seat_bypass_active",
            seat="red_team",
            reason_code="expired_slot",
            hmac_key=CAPSTONE_DEGRADATION_KEY,
            watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
            expires_at=past,
            expires_monotonic_ns=mono_now - 10**9,
            boot_epoch_ns_at_issuance=env.boot_epoch_ns,
            signed_by_operator=True,
        )
        assert bypass_is_active(
            event,
            now_utc=now,
            now_mono_ns=mono_now,
            boot_clock_history=history,
        ) is False

    def test_adv_degradation_rejects_unknown_seat(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        with pytest.raises(ValueError):
            record_degradation(
                repo_root=env.repo_root,
                event_kind="author_seat_degraded_run",
                seat="nonexistent_seat",
                reason_code="x",
                hmac_key=CAPSTONE_DEGRADATION_KEY,
                watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
            )


# ===========================================================================
# J.1.6 — Boot + org slug + isolation (boot + org_slug + isolation)
# ===========================================================================


class TestBootOrgIsolation:
    def test_boot_with_slug_arg_canonicalized(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env = boot_envelope(
            repo_root=capstone_repo,
            keystore=capstone_keystore,
            slug_arg="  MyCo Symbiotics  ",
        )
        assert env.slug == "myco-symbiotics"

    def test_boot_rejects_collision_slug(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_slug: str,
    ) -> None:
        (capstone_repo / "orgs" / capstone_slug).mkdir(parents=True, exist_ok=True)
        with pytest.raises(SlugCollisionError):
            boot_envelope(
                repo_root=capstone_repo,
                keystore=capstone_keystore,
                slug_arg=capstone_slug,
            )

    def test_adv_invalid_slug_type(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        with pytest.raises(TypeError):
            boot_envelope(
                repo_root=capstone_repo,
                keystore=capstone_keystore,
                slug_arg=3.14,  # type: ignore[arg-type]
            )

    def test_adv_slug_reserved_name_rejected(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        with pytest.raises((InvalidSlug, Exception)):
            boot_envelope(
                repo_root=capstone_repo,
                keystore=capstone_keystore,
                slug_arg=".git",
            )


# ===========================================================================
# J.1.7 — Repo-root sanity (boot + lockfile)
# ===========================================================================


class TestBootRepoSanity:
    def test_adv_missing_router_yaml(
        self, capstone_keystore: CapstoneKeyStore, tmp_path: Path
    ) -> None:
        run_git(tmp_path, "init", "-q", "-b", "main")
        run_git(tmp_path, "commit", "--allow-empty", "-m", "init", "-q")
        (tmp_path / "orgs").mkdir()
        # No router.yaml.
        with pytest.raises(RepoRootInvalid):
            boot_envelope(repo_root=tmp_path, keystore=capstone_keystore)

    def test_adv_missing_orgs_dir(
        self, capstone_keystore: CapstoneKeyStore, tmp_path: Path
    ) -> None:
        run_git(tmp_path, "init", "-q", "-b", "main")
        run_git(tmp_path, "commit", "--allow-empty", "-m", "init", "-q")
        write_signed_router(tmp_path)
        with pytest.raises(RepoRootInvalid):
            boot_envelope(repo_root=tmp_path, keystore=capstone_keystore)

    def test_adv_repo_root_is_file(
        self, capstone_keystore: CapstoneKeyStore, tmp_path: Path
    ) -> None:
        f = tmp_path / "repo-file"
        f.write_bytes(b"x")
        with pytest.raises(RepoRootInvalid):
            boot_envelope(repo_root=f, keystore=capstone_keystore)

    def test_adv_repo_root_nonexistent(
        self, capstone_keystore: CapstoneKeyStore, tmp_path: Path
    ) -> None:
        with pytest.raises(RepoRootInvalid):
            boot_envelope(
                repo_root=tmp_path / "no-such-path",
                keystore=capstone_keystore,
            )


# ===========================================================================
# J.1.8 — Full end-to-end lifecycle cross-check
# ===========================================================================


class TestFullLifecycle:
    def test_boot_to_session_to_rfa_to_pc_to_ledger(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
        capstone_slug: str,
        capstone_rfa_bytes: bytes,
        capstone_rfa_url: str,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        # Seal PROJECT_CONTEXT before the session binds.
        pc = seal_project_context(
            slug=capstone_slug,
            session_id="sess-full",
            repo_root=env.repo_root,
        )
        # Start session.
        sess = start_session(
            envelope=_EnvelopeFacade(env),
            rfa=_RFAFacade(capstone_slug),
            project_context=_PCFacade(capstone_slug),
        )
        try:
            # Ingest RFA under the session's slug.
            rfa = ingest_rfa(
                url=capstone_rfa_url,
                content_bytes=capstone_rfa_bytes,
                slug=capstone_slug,
                operator_id="josh",
                rfa_id="rfa-full",
                repo_root=env.repo_root,
            )
            # Record an admin-risk flag.
            entry = record_admin_risk(
                repo_root=env.repo_root,
                entry_kind="flagged_term_substitution",
                severity="YELLOW",
                payload={"rfa_id": rfa.rfa_id, "term": "marginalized"},
                hmac_key=CAPSTONE_LEDGER_KEY,
                watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
            )
            assert entry.severity == "YELLOW"
            # Re-verify both envelopes without raising.
            reverify_rfa(rfa)
            verify_project_context(pc, repo_root=env.repo_root)
            # Sign a health tuple (M7 end-to-end).
            mac = sign_health_tuple(sess, b"health")
            assert len(mac) == 64
        finally:
            end_session(sess)

    def test_second_boot_is_idempotent_post_full_cycle(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
        capstone_org_dir: Path,
        capstone_slug: str,
        capstone_rfa_bytes: bytes,
        capstone_rfa_url: str,
    ) -> None:
        env1 = _boot_with_ledgers(capstone_repo, capstone_keystore)
        # One round of writes so the second boot must verify persisted state.
        ingest_rfa(
            url=capstone_rfa_url,
            content_bytes=capstone_rfa_bytes,
            slug=capstone_slug,
            operator_id="josh",
            rfa_id="rfa-persist",
            repo_root=env1.repo_root,
        )
        record_admin_risk(
            repo_root=env1.repo_root,
            entry_kind="flagged_term_substitution",
            severity="GREEN",
            payload={"t": "ok"},
            hmac_key=CAPSTONE_LEDGER_KEY,
            watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
        )
        env2 = _boot_with_ledgers(capstone_repo, capstone_keystore)
        assert env2.init_marker.init_version == env1.init_marker.init_version
        history = read_boot_clock_history(env2.repo_root)
        # Two distinct boots → two history entries when boot_epoch_ns differs.
        # On a single test run the kernel epoch is stable, so idempotent
        # append may leave history at 1. Both outcomes are legitimate.
        assert len(history) in (1, 2)

    def test_adv_tampered_ledger_rejects_second_boot(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        record_admin_risk(
            repo_root=env.repo_root,
            entry_kind="flagged_term_substitution",
            severity="GREEN",
            payload={"t": "a"},
            hmac_key=CAPSTONE_LEDGER_KEY,
            watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
        )
        ledger = env.repo_root / "sovereignty" / "ledgers" / "admin_risk.jsonl"
        raw = ledger.read_bytes()
        # Mutate the severity field in the line's entry_hash — any byte-flip
        # invalidates the trailer HMAC.
        assert b'"severity":"GREEN"' in raw
        ledger.write_bytes(raw.replace(b'"severity":"GREEN"', b'"severity":"RED"  '))
        # Second boot verifies trailers; must fail-closed.
        with pytest.raises(Exception):
            _boot_with_ledgers(capstone_repo, capstone_keystore)

    def test_adv_tampered_watermarks_rejects_second_boot(
        self,
        capstone_repo: Path,
        capstone_keystore: CapstoneKeyStore,
    ) -> None:
        env = _boot_with_ledgers(capstone_repo, capstone_keystore)
        record_admin_risk(
            repo_root=env.repo_root,
            entry_kind="flagged_term_substitution",
            severity="GREEN",
            payload={"t": "a"},
            hmac_key=CAPSTONE_LEDGER_KEY,
            watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
        )
        watermarks_body = (
            env.repo_root
            / "sovereignty"
            / "watermarks"
            / "ledger_watermarks.json"
        )
        raw = watermarks_body.read_bytes()
        watermarks_body.write_bytes(raw.replace(b'"last_seq_id":1', b'"last_seq_id":9'))
        with pytest.raises(Exception):
            _boot_with_ledgers(capstone_repo, capstone_keystore)
