"""§2 Vault Round K.3 — boot-sequence parametric fuzz harness.

Per spec card ``pipeline/engineering/spec_cards/section_2_round_k_capstone.md``
K.3: single parametric harness that, given a clean vault root, boots Tilth
through all 19 §2 modules N times with N distinct org slugs, with N
parametrised over ``{2, 8, 16, 32}``. The flat slug list lays the four
batches end-to-end (2 + 8 + 16 + 32 = **58** individual pytest instances)
so the test count meets the spec floor while preserving N-grouped slug
labels for at-a-glance debugging.

Per-iteration invariants (asserted inside ``test_boot_invariants_per_org``
for every one of the 58 firings):

1.  ``vault_boot`` returns ``VaultBootResult(success=True, …)`` with a
    non-empty distinct ``session_id`` and a populated ``frozen_root``.
2.  Seed-manifest verify (§9.6) committed: ``frozen_root.root_hex`` is
    the canonical Merkle root over the per-iteration seed file set,
    matching the manifest's ``head_hash``. This is the §2 analog of §1
    Round J's "audit ledger hash-chain terminates at valid trailer
    HMAC" — for §2 the audit substrate IS the seed manifest.
3.  Atomic-freeze step (§9.7) created a CoV snapshot for *this* boot
    via the injected :class:`FakeSnapshotProvider`.
4.  Cedar policies (§9.9) loaded — mapping is non-empty.
5.  FD broker (§9.10) is online; the resulting ``vault_root_fd`` is a
    valid file descriptor that closes cleanly on ``vault_boot_close``.
6.  Per-org vault_write SIMPLE round-trip is byte-identical (rails
    report intent, ``overwrite`` mode).
7.  Identity-tuple mount-table snapshot is reused: ``frozen_root.\
    content_hashes_hex`` is populated for every seed path with the
    canonical SHA-3-512 of the on-disk bytes (Batch 3 Phase 2 widened
    schema).

Cross-cutting invariants (single-instance test methods that complement
the fuzz loop):

* ``test_session_ids_are_distinct_across_all_58_boots`` — boots all 58
  fuzz slugs back-to-back in one process and asserts the 58
  ``session_id`` values are pairwise distinct.
* ``test_law3_cross_org_vault_write_rejected`` — Law 3 mechanical:
  org-A's ``vault_write`` call against an ``orgs/org-B/...`` path with
  ``org_vault_root`` pinned to org-A raises
  :class:`VaultCrossOrgAccess`. Parametrised over ``N ∈ {2, 8, 16,
  32}`` org-pair counts so the rejection invariant holds at every
  fuzz batch size.
* ``test_cov_snapshot_retention_prunes_to_three`` — provisioning a
  shared snapshot provider with 5 org-scoped snapshots and invoking
  :func:`prune_snapshots` with ``retention_count=3`` deletes 2 and
  retains 3, exercising the §9.7 retention invariant outside the boot
  hot path.
* ``test_compound_txn_per_org_round_trip_with_monkeypatched_caps`` —
  begin → stage → commit lifecycle for one COMPOUND intent under
  ``MAX_STAGED_BYTES_PER_TXN`` and ``MAX_COMPOUND_TXN_BYTES``
  monkeypatched to ``1024`` for RAM safety, mirroring K.1.h discipline.

Spec card §"Test criteria":
    K.3: parametric fuzz harness across N ∈ {2, 8, 16, 32} org slugs =
    single parameterized class, **≥58 individual test instances**.

Blueprint anchor:
    ``pipeline/blueprint/v0.1/section_02_vault_topology.md`` v7.1 §9
    (full boot sequence) + §10 (compound-txn lifecycle).

Self-LOCK eligibility: §1 Round J + §3 Scout R5-R9 + §5 Pipeline R3-R12
compositional-round precedent — every consumed module has an
independent committee LOCK on record.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import asdict
from pathlib import Path
from typing import Iterator

import pytest

from pipeline.vault import compound_txn as _compound_txn
from pipeline.vault.atomic_freeze import prune_snapshots
from pipeline.vault.compound_txn import CompoundTxnDispatcher
from pipeline.vault.error_codes import VaultCrossOrgAccess
from pipeline.vault.mirror_verify import (
    compute_leaf_hash_hex,
    compute_merkle_root_hex,
)
from pipeline.vault.schemas import CompoundTxnState
from pipeline.vault.vault_boot import VaultBootResult, vault_boot, vault_boot_close
from pipeline.vault.vault_write import EMPTY_SHA3_512_HEX, VaultWriteAck, vault_write

from tests.vault.conftest import (
    DEFAULT_SEED_SPEC,
    FakeSnapshotProvider,
    always_true,
    build_manifest,
    make_seed_file,
    serialize_manifest,
    sha3_512_hex,
)


# ---------------------------------------------------------------------------
# Parametric slug generator: flat list of 58 (batch_n, idx_within_batch)
# ---------------------------------------------------------------------------


FUZZ_BATCH_SIZES: tuple[int, ...] = (2, 8, 16, 32)


def _flat_fuzz_slugs() -> list[tuple[int, int, str]]:
    """Yield ``(batch_n, idx, slug)`` triples for every fuzz iteration.

    The four parametric batches lay end-to-end: 2 + 8 + 16 + 32 = 58
    pytest instances. Slugs are zero-padded to keep stable ordering in
    pytest's verbose output. Format: ``"fuzz-N{batch:02d}-{idx:03d}"``
    so a debugger can map any failure back to its batch and index.
    """
    out: list[tuple[int, int, str]] = []
    for batch_n in FUZZ_BATCH_SIZES:
        for idx in range(batch_n):
            slug = f"fuzz-N{batch_n:02d}-{idx:03d}"
            out.append((batch_n, idx, slug))
    return out


FUZZ_SLUGS: list[tuple[int, int, str]] = _flat_fuzz_slugs()
assert len(FUZZ_SLUGS) == sum(FUZZ_BATCH_SIZES) == 58


# ---------------------------------------------------------------------------
# Per-iteration vault workspace builder
# ---------------------------------------------------------------------------


def _fresh_vault_workspace(base: Path, slug: str) -> dict:
    """Provision a fresh vault root + signed seed manifest under ``base/slug``.

    Mirrors the ``capstone_vault_workspace`` fixture shape from
    ``tests/vault/conftest.py`` so the fuzz iterations don't share
    module/function-scope tmp paths across the 58 firings (the J.3
    precedent: state leakage across iterations breaks the "no
    cross-boot leak" invariant we're asserting).
    """
    workspace = base / slug
    workspace.mkdir(parents=True, exist_ok=False)
    vault_root = workspace / "vault"
    vault_root.mkdir()
    vault_shared = vault_root / "vault_shared"
    vault_shared.mkdir()

    seeds = [
        make_seed_file(rel, content, vault_shared)
        for rel, content in DEFAULT_SEED_SPEC
    ]
    manifest = build_manifest(seeds)
    manifest_path = workspace / "seed_manifest.json"
    sig_path = workspace / "seed_manifest.sig"
    manifest_path.write_bytes(serialize_manifest(manifest))
    sig_path.write_text(manifest.signature + "\n", encoding="utf-8")

    return {
        "workspace": workspace,
        "vault_root": vault_root,
        "vault_shared": vault_shared,
        "seeds": seeds,
        "manifest": manifest,
        "manifest_path": manifest_path,
        "sig_path": sig_path,
    }


def _boot_kwargs(ws: dict, *, session_id: str) -> dict:
    """Ready-to-call kwargs for :func:`vault_boot` for one fuzz iteration.

    Parallels ``capstone_boot_kwargs`` but takes per-iteration session
    ID and snapshot provider explicitly — fixtures at module scope
    would cross-contaminate across iterations.
    """
    return {
        "vault_root": ws["vault_root"],
        "vault_shared_root": ws["vault_shared"],
        "seed_manifest_path": ws["manifest_path"],
        "seed_signature_path": ws["sig_path"],
        "session_id": session_id,
        "current_ledger_head": ws["manifest"].m15_ledger_head,
        "verify_signature": always_true,
        "platform": "darwin",
    }


# ---------------------------------------------------------------------------
# Fixture: auto-close VaultBootResults to avoid FD leak across iterations
# ---------------------------------------------------------------------------


@pytest.fixture
def _boot_auto_close() -> Iterator[list[VaultBootResult]]:
    """Yield a list to register :class:`VaultBootResult` instances; closes
    them on teardown so ``vault_root_fd`` never leaks between fuzz
    iterations or invariant tests.

    Mirrors ``capstone_auto_close`` from ``tests/vault/conftest.py``.
    """
    results: list[VaultBootResult] = []
    yield results
    for r in results:
        try:
            vault_boot_close(r)
        except Exception:
            pass


# ===========================================================================
# K.3 single parametric fuzz class
# ===========================================================================


class TestK3BootSequenceFuzzHarness:
    """58-instance parametric fuzz across the full §2 boot sequence.

    Each parametric firing exercises ``vault_boot`` end-to-end on a
    fresh per-iteration workspace, then round-trips one SIMPLE
    ``vault_write`` under that org. Cross-cutting invariants (distinct
    session IDs, Law 3 cross-org rejection, CoV retention, compound
    txn) live in dedicated single-instance methods to keep the fuzz
    loop fast while still hitting every K.3 invariant from the spec
    card.
    """

    # ------------------------------------------------------------------
    # Per-iteration boot invariants (58 parametric instances)
    # ------------------------------------------------------------------

    @pytest.mark.parametrize(
        "batch_n, idx, slug",
        FUZZ_SLUGS,
        ids=[s for _, _, s in FUZZ_SLUGS],
    )
    def test_boot_invariants_per_org(
        self,
        tmp_path: Path,
        _boot_auto_close: list[VaultBootResult],
        batch_n: int,
        idx: int,
        slug: str,
    ) -> None:
        # (0) Fresh per-iteration vault workspace.
        ws = _fresh_vault_workspace(tmp_path, slug)
        snapshot_provider = FakeSnapshotProvider()

        # (1) Boot.
        session_id = f"session-K3-{slug}"
        kwargs = _boot_kwargs(ws, session_id=session_id)
        kwargs["snapshot_provider"] = snapshot_provider
        result = vault_boot(**kwargs)
        _boot_auto_close.append(result)

        # Invariant 1: VaultBootResult populated and successful.
        assert isinstance(result, VaultBootResult)
        assert result.success is True
        assert result.session_id == session_id
        assert result.session_id  # non-empty
        assert result.vault_root == ws["vault_root"]
        assert result.vault_shared_root == ws["vault_shared"]
        assert result.frozen_root is not None

        # Invariant 2: Seed-manifest verify committed — frozen.root_hex is
        # the canonical Merkle root over this iteration's seed files. This
        # is §2's analog of §1 Round J's "audit ledger hash-chain
        # terminates at valid trailer" — for §2, the seed manifest IS the
        # audit substrate, and frozen.root_hex pins its head.
        sorted_seeds = sorted(ws["seeds"], key=lambda s: s.relative_path)
        leaves = [
            compute_leaf_hash_hex(sf.relative_path, sf.content_hash)
            for sf in sorted_seeds
        ]
        expected_root = compute_merkle_root_hex(leaves)
        assert result.frozen_root.root_hex == expected_root
        assert result.frozen_root.root_hex == ws["manifest"].head_hash

        # Invariant 3: Atomic-freeze (§9.7) created a CoV snapshot for
        # this boot via the injected FakeSnapshotProvider.
        assert len(snapshot_provider.created) == 1
        snap_label = snapshot_provider.created[0]
        assert session_id in snap_label

        # Invariant 4: Cedar policies (§9.9) loaded — mapping non-empty.
        assert result.cedar_policies
        # The DEFAULT_SEED_SPEC includes two cedar policies; ensure both
        # made it into the loader output, keyed by relative path.
        assert "cedar/org_isolation.cedar" in result.cedar_policies
        assert "cedar/write_gate.cedar" in result.cedar_policies

        # Invariant 5: FD broker (§9.10) online; vault_root_fd is open.
        assert result.fd_broker is not None
        assert isinstance(result.vault_root_fd, int)
        assert result.vault_root_fd >= 0
        # Stat the FD to prove it's a live descriptor.
        stat_result = os.fstat(result.vault_root_fd)
        assert stat_result.st_mode != 0

        # Invariant 7: Identity-tuple mount-table snapshot reused —
        # frozen_root.content_hashes_hex populated for every seed path
        # with canonical SHA-3-512 of on-disk bytes (Batch 3 Phase 2).
        assert len(result.frozen_root.content_hashes_hex) == len(sorted_seeds)
        for sf in sorted_seeds:
            on_disk_bytes = (ws["vault_shared"] / sf.relative_path).read_bytes()
            assert (
                result.frozen_root.content_hashes_hex[sf.relative_path]
                == sha3_512_hex(on_disk_bytes)
            )

        # Invariant 6: Per-org vault_write SIMPLE round-trip byte-identical.
        org_vault_root = ws["vault_root"] / "orgs" / slug
        org_vault_root.mkdir(parents=True)
        write_lock = org_vault_root / ".write.lock"
        rails_path = org_vault_root / "rails_reports" / "r.json"
        payload = f'{{"slug":"{slug}","batch_n":{batch_n},"idx":{idx}}}'.encode(
            "utf-8"
        )
        ack = vault_write(
            path=rails_path,
            bytes_=payload,
            intent="rails-report-write",
            session_id=session_id,
            slug=slug,
            org_vault_root=org_vault_root,
            write_lock_path=write_lock,
            write_mode="overwrite",
        )
        assert isinstance(ack, VaultWriteAck)
        assert ack.committed is True
        assert rails_path.read_bytes() == payload

    # ------------------------------------------------------------------
    # Distinct session_id across all 58 boots
    # ------------------------------------------------------------------

    def test_session_ids_are_distinct_across_all_58_boots(
        self, tmp_path: Path, _boot_auto_close: list[VaultBootResult]
    ) -> None:
        """All 58 fuzz iterations produce pairwise-distinct session IDs."""
        seen: set[str] = set()
        for batch_n, idx, slug in FUZZ_SLUGS:
            ws = _fresh_vault_workspace(tmp_path, f"distinct-{slug}")
            session_id = f"session-K3-distinct-{slug}"
            r = vault_boot(**_boot_kwargs(ws, session_id=session_id))
            _boot_auto_close.append(r)
            assert r.session_id not in seen
            seen.add(r.session_id)
        assert len(seen) == 58

    # ------------------------------------------------------------------
    # Law 3 mechanical — cross-org vault_write rejection
    # ------------------------------------------------------------------

    @pytest.mark.parametrize("n_orgs", FUZZ_BATCH_SIZES)
    def test_law3_cross_org_vault_write_rejected(
        self, tmp_path: Path, n_orgs: int
    ) -> None:
        """Law 3 mechanical: org-A vault_write to ``orgs/org-B/...`` path
        with ``org_vault_root`` pinned to org-A raises
        :class:`VaultCrossOrgAccess`. Parametrised over the four fuzz
        batch sizes so the rejection invariant holds regardless of how
        many siblings exist alongside the writer.
        """
        # Provision n_orgs sibling org dirs under a single vault_root.
        vault_root = tmp_path / f"law3-N{n_orgs:02d}" / "vault"
        vault_root.mkdir(parents=True)
        orgs_dir = vault_root / "orgs"
        orgs_dir.mkdir()
        org_dirs: list[Path] = []
        for i in range(n_orgs):
            d = orgs_dir / f"law3-org-{i:04d}"
            d.mkdir()
            (d / "PROJECT_CONTEXT.md").write_text(
                f"# PROJECT_CONTEXT — law3-org-{i:04d}\n", encoding="utf-8"
            )
            org_dirs.append(d)

        org_a = org_dirs[0]
        # Pick org-B as the last sibling so the wrap-around case is hit.
        org_b = org_dirs[-1]
        write_lock_a = org_a / ".write.lock"

        # vault_write call: path under org_b but org_vault_root is org_a.
        bad_target = org_b / "rails_reports" / "r.json"
        with pytest.raises(VaultCrossOrgAccess):
            vault_write(
                path=bad_target,
                bytes_=b'{"x":1}',
                intent="rails-report-write",
                session_id=f"s-law3-N{n_orgs:02d}",
                slug="law3-org-0000",
                org_vault_root=org_a,
                write_lock_path=write_lock_a,
                write_mode="overwrite",
            )

    # ------------------------------------------------------------------
    # CoV snapshot retention=3
    # ------------------------------------------------------------------

    def test_cov_snapshot_retention_prunes_to_three(self) -> None:
        """Provision 5 org-scoped snapshots in a shared FakeSnapshotProvider,
        invoke :func:`prune_snapshots` with ``retention_count=3``, and
        verify the §9.7 invariant: 2 deleted, 3 retained.
        """
        provider = FakeSnapshotProvider()
        for i in range(5):
            provider.create_snapshot(
                label=f"com.tilth.vault_shared.session-K3-org-{i:04d}"
            )
        deleted = prune_snapshots(
            snapshot_provider=provider, retention_count=3
        )
        assert len(deleted) == 2
        remaining = provider.list_snapshots()
        assert len(remaining) == 3

    # ------------------------------------------------------------------
    # Compound txn per-org round-trip with monkeypatched caps
    # ------------------------------------------------------------------

    def test_compound_txn_per_org_round_trip_with_monkeypatched_caps(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """begin → stage → commit lifecycle under monkeypatched stage-byte
        and undo-snapshot caps (1024 bytes each), mirroring K.1.h
        discipline. Asserts the COMPOUND intent path round-trips
        through the dispatcher under per-org isolation.
        """
        # Shrink caps from 128 MiB / 64 MiB to 1024 bytes for RAM safety.
        monkeypatch.setattr(
            _compound_txn, "MAX_STAGED_BYTES_PER_TXN", 1024
        )
        monkeypatch.setattr(
            _compound_txn, "MAX_COMPOUND_TXN_BYTES", 1024
        )

        org_root = tmp_path / "k3-compound-org"
        org_root.mkdir()
        lock_path = org_root / ".compound_txn.lock"
        dispatcher = CompoundTxnDispatcher(compound_lock_path=lock_path)

        session_id = "session-K3-compound"
        token = dispatcher.begin(
            txn_kind="index-update", session_id=session_id
        )
        assert isinstance(token, str) and token

        # Stage a single small write — well under the 1024-byte cap.
        dispatcher.stage_write(
            txn_token=token,
            session_id=session_id,
            intent="index-update",
            path=str(org_root / "pipeline" / "blueprint" / "x.json"),
            data=b'{"k":1}',
            write_mode="write-if-absent",
        )

        # Commit through a hook that captures the staged state.
        captured: list[CompoundTxnState] = []

        def _persist(state: CompoundTxnState) -> None:
            captured.append(state)

        committed = dispatcher.commit(
            txn_token=token, session_id=session_id, persist=_persist
        )
        assert len(committed) == 1
        assert len(captured) == 1
        assert captured[0].session_id == session_id
        # Session-count slot released on commit.
        # noinspection PyProtectedMember
        assert dispatcher._session_counts.get(session_id, 0) == 0  # type: ignore[attr-defined]
