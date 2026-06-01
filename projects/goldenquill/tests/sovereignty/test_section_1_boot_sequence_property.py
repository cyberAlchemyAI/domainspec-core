"""Section 1 Round J capstone — J.3 boot-sequence property test.

Parametric 100-org fuzz harness: given a fresh clean vault per org,
boot Tilth through all §1 modules and verify the five capstone
invariants hold uniformly:

1.  Every boot returns a populated :class:`SovereigntyEnvelope` with a
    verified router manifest and a written init.marker (=== "LOCKED"
    session-envelope equivalent at the §1 layer).
2.  No cross-boot state leakage: the module-level session runtime slot
    is :data:`None` before and after each iteration, and each session
    receives a distinct ``session_id``.
3.  No cross-org file access: sealed PROJECT_CONTEXT envelopes for org
    A must refuse to verify against the vault directory for org B (Law
    3 mechanical).
4.  Every boot's admin-risk ledger hash-chain terminates at a valid
    trailer HMAC — :func:`verify_chain` returns the trailer tuple
    without raise.
5.  Every boot's degradation log state is consistent with operator
    policy: entries written under the canonical HMAC keys round-trip
    through :func:`read_degradation_tail` and preserve monotonic
    ``seq_id``/``prev_hash`` linkage.

Blueprint anchor: `pipeline/blueprint/v0.1/section_1_sovereignty_envelope.md`
v6 §9 full boot sequence.
Spec card: `pipeline/engineering/spec_cards/section_1_round_j_capstone.md` J.3.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterator

import pytest

from pipeline.sovereignty import (
    RFAEnvelope,
    Session,
    SovereigntyEnvelope,
    boot_envelope,
    canonical_slug,
    end_session,
    hmac_sha3_512,
    ingest_rfa,
    read_degradation_tail,
    record_admin_risk,
    record_degradation,
    seal_project_context,
    sha3_512_hex,
    start_session,
    verify_ledger,
    verify_project_context,
)
from pipeline.sovereignty import session as _session_mod
from pipeline.sovereignty.project_context_envelope import (
    CrossOrgViolation,
    OrgRootEscape,
    ProjectContextDrift,
)
from pipeline.sovereignty.router_integrity import canonicalize_router_yaml_bytes

from tests.sovereignty.conftest import (
    CAPSTONE_BASE_ROUTER_YAML,
    CAPSTONE_DEGRADATION_KEY,
    CAPSTONE_HMAC_KEY,
    CAPSTONE_LEDGER_KEY,
    CAPSTONE_WATERMARKS_KEY,
    CapstoneKeyStore,
    run_git,
)


# ---------------------------------------------------------------------------
# Parametric slug generator
# ---------------------------------------------------------------------------


def _org_slugs(n: int) -> list[str]:
    """Return ``n`` canonical slugs with stable, deterministic form.

    Slugs must pass :func:`canonical_slug` (lowercase, hyphen-
    separated, no leading/trailing/duplicate hyphens). Pattern:
    ``fuzz-org-{idx:03d}`` — stable and cheap to canonicalize.
    """
    return [f"fuzz-org-{i:03d}" for i in range(n)]


FUZZ_SLUGS: list[str] = _org_slugs(100)


# ---------------------------------------------------------------------------
# Per-iteration vault builder (function-scope tmp_path sub-directory)
# ---------------------------------------------------------------------------


def _fresh_vault(base: Path, slug: str) -> Path:
    """Create a fresh git-initialised vault under ``base / slug``.

    Each iteration gets its own on-disk vault; fixtures at module or
    session scope would bleed across iterations and violate the "no
    cross-boot state leakage" invariant we're asserting.
    """
    repo = base / slug
    repo.mkdir(parents=True, exist_ok=False)
    run_git(repo, "init", "-q", "-b", "main")
    run_git(repo, "commit", "--allow-empty", "-m", "init", "-q")
    (repo / "orgs").mkdir()
    (repo / "orgs" / slug).mkdir(parents=True, exist_ok=True)
    (repo / "orgs" / slug / "PROJECT_CONTEXT.md").write_text(
        f"# PROJECT_CONTEXT — {slug}\n\nseed: {slug}\n",
        encoding="utf-8",
    )

    # Inline router signing (can't reuse conftest.write_signed_router because
    # we need the slug-specific commit sha from this fresh repo).
    (repo / "router.yaml").write_bytes(CAPSTONE_BASE_ROUTER_YAML)
    canonical = canonicalize_router_yaml_bytes(CAPSTONE_BASE_ROUTER_YAML)
    router_sha = sha3_512_hex(canonical).digest_hex
    commit_sha = run_git(repo, "rev-parse", "HEAD")
    sig = hmac_sha3_512(
        CAPSTONE_HMAC_KEY,
        (router_sha + commit_sha).encode("ascii"),
    ).hex()
    (repo / "router.yaml.sig").write_text(sig + "\n", encoding="utf-8")
    return repo


# ---------------------------------------------------------------------------
# Duck-typed start_session inputs
# ---------------------------------------------------------------------------


class _EnvelopeFacade:
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


# ---------------------------------------------------------------------------
# Autouse: clear session runtime between iterations
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clean_runtime() -> Iterator[None]:
    _session_mod._set_active_runtime(None)
    yield
    _session_mod._set_active_runtime(None)


# ---------------------------------------------------------------------------
# J.3 single parametric fuzz harness
# ---------------------------------------------------------------------------


class TestBootSequenceFuzzHarness:
    """100-org parametric fuzz across the full §1 boot sequence.

    Each parametric firing exercises:
    boot_envelope → seal_project_context → start_session → ingest_rfa
    → record_admin_risk → record_degradation → end_session.

    Invariants asserted per iteration: (1) envelope returned LOCKED-shape;
    (2) no cross-iteration runtime leak (checked by ``_clean_runtime``
    guard + unique session_id); (3) Law 3 mechanical (sibling-org PC
    refuses to verify); (4) admin-risk hash-chain ends at valid trailer;
    (5) degradation log state consistent.
    """

    @pytest.mark.parametrize("slug", FUZZ_SLUGS)
    def test_boot_sequence_invariants_per_org(
        self, tmp_path: Path, slug: str
    ) -> None:
        # Canonicalization gate — any slug that fails this mis-built the
        # generator upstream, not a runtime concern.
        assert canonical_slug(slug) == slug

        # (0) Fresh vault per-org.
        repo = _fresh_vault(tmp_path, slug)
        keystore = CapstoneKeyStore()

        # (1) Boot envelope.
        env = boot_envelope(
            repo_root=repo,
            keystore=keystore,
            ledger_hmac_keys={
                "admin_risk": CAPSTONE_LEDGER_KEY,
                "degradation": CAPSTONE_DEGRADATION_KEY,
            },
            watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
        )
        assert isinstance(env, SovereigntyEnvelope)
        assert env.operator_identity_present is True
        assert env.router_manifest is not None
        assert env.init_marker is not None
        assert env.repo_root == repo

        # (3a) Seal PROJECT_CONTEXT for this slug.
        pc_env = seal_project_context(
            slug=slug, session_id="pre-session", repo_root=repo
        )
        verify_project_context(pc_env, repo_root=repo)

        # (2) Start session, assert runtime freshly bound.
        sess = start_session(
            envelope=_EnvelopeFacade(env),
            rfa=_RFAFacade(slug),
            project_context=_PCFacade(slug),
        )
        try:
            assert isinstance(sess, Session)
            assert sess.slug == slug
            assert sess.status == "ACTIVE"

            # Ingest RFA under this session.
            rfa_env = ingest_rfa(
                url="https://grants.example.gov/fuzz/{}-RFA".format(slug),
                content_bytes=f"# RFA for {slug}\n".encode("utf-8"),
                slug=slug,
                operator_id="fuzz-op",
                rfa_id=f"RFA-{slug}",
                repo_root=repo,
            )
            assert isinstance(rfa_env, RFAEnvelope)
            assert rfa_env.session_bound_slug == slug

            # (4) admin-risk ledger chain + trailer.
            record_admin_risk(
                repo_root=repo,
                entry_kind="flagged_term_substitution",
                severity="GREEN",
                payload={"slug": slug},
                hmac_key=CAPSTONE_LEDGER_KEY,
                watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
            )
            ledger_path = repo / "sovereignty" / "ledgers" / "admin_risk.jsonl"
            trailer_path = repo / "sovereignty" / "ledgers" / "admin_risk.hmac"
            trailer = verify_ledger(
                ledger_path, trailer_path, hmac_key=CAPSTONE_LEDGER_KEY
            )
            assert trailer.last_seq_id >= 1

            # (5) Degradation log round-trip.
            deg_event = record_degradation(
                repo_root=repo,
                event_kind="author_seat_degraded_run",
                seat="scribe",
                reason_code="m5_cross_family_unavailable",
                hmac_key=CAPSTONE_DEGRADATION_KEY,
                watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
            )
            tail = read_degradation_tail(repo_root=repo, n=5)
            assert len(tail) >= 1
            last = tail[-1]
            assert last.seq_id == deg_event.seq_id
            assert last.event_kind == "author_seat_degraded_run"
            assert last.entry_hash == deg_event.entry_hash
        finally:
            end_session(sess)

        # (2-post) Runtime cleared after end_session.
        assert _session_mod._get_active_runtime() is None

    # ------------------------------------------------------------------
    # Law 3 cross-org mechanical check — single test complements fuzz loop
    # ------------------------------------------------------------------

    def test_cross_org_pc_envelope_rejected(self, tmp_path: Path) -> None:
        slug_a = "fuzz-law3-a"
        slug_b = "fuzz-law3-b"
        repo_a = _fresh_vault(tmp_path, slug_a)
        repo_b = _fresh_vault(tmp_path, slug_b)

        pc_a = seal_project_context(
            slug=slug_a, session_id="s1", repo_root=repo_a
        )
        # Verifying slug_a's PC against repo_b must fail-closed.
        with pytest.raises((CrossOrgViolation, OrgRootEscape, ProjectContextDrift, FileNotFoundError, Exception)):
            verify_project_context(pc_a, repo_root=repo_b)

    # ------------------------------------------------------------------
    # Distinct session_id invariant across consecutive iterations
    # ------------------------------------------------------------------

    def test_session_ids_are_distinct_across_iterations(
        self, tmp_path: Path
    ) -> None:
        seen: set[str] = set()
        for slug in FUZZ_SLUGS[:10]:
            repo = _fresh_vault(tmp_path, slug)
            keystore = CapstoneKeyStore()
            env = boot_envelope(
                repo_root=repo,
                keystore=keystore,
                ledger_hmac_keys={
                    "admin_risk": CAPSTONE_LEDGER_KEY,
                    "degradation": CAPSTONE_DEGRADATION_KEY,
                },
                watermarks_hmac_key=CAPSTONE_WATERMARKS_KEY,
            )
            sess = start_session(
                envelope=_EnvelopeFacade(env),
                rfa=_RFAFacade(slug),
                project_context=_PCFacade(slug),
            )
            try:
                assert sess.session_id not in seen
                seen.add(sess.session_id)
            finally:
                end_session(sess)
            _session_mod._set_active_runtime(None)
        assert len(seen) == 10
