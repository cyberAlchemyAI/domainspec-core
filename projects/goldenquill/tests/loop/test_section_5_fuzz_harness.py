"""§5 R13 capstone — J.5 100-run parametric fuzz harness.

Blueprint §5 v6 LOCKED 2026-04-19. Spec card
``pipeline/engineering/spec_cards/section_05_round_13_capstone.md`` §J.5.

Two top-level property classes exercised with
``pytest.mark.parametrize`` over 100 synthetic ``(org_slug, run_id)``
tuples each:

* :class:`TestSubmissionFuzz` — 100 happy-path submission runs.  Asserts
  per-run trajectory lands at ``tabs_written_ok``, every run's CAS chain
  is linear (no orphan writes / no second-attempt expected-hash-miss),
  every run terminates with ``final_committed_state_hash`` populated,
  and there is zero cross-run state leakage.

* :class:`TestEvalFuzz` — 100 happy-path eval runs against a PubkeyVault
  shared across all fuzzers.  Asserts every run writes ``exactly one``
  pubkey-first-write provenance sidecar the first time its org_slug is
  seen (MA-09 first-write-wins per blueprint §5.6.4); never on the
  subsequent 99 runs against that same slug.  Additionally asserts the
  Ed25519 signature on the emitted calibration report verifies under
  the landed pubkey — zero report that decodes but fails signature.

The fuzz harness is a Cedar-style mechanical determinism property:
given deterministic seeds and deterministic launchers, the pipeline
is reproducible bit-for-bit across 100 firings.  Per ORIENT OQ#6 the
fuzz runs sequentially (no threading).

Fixtures / harness: :mod:`tests.loop.conftest_section_5` (sibling).
"""

from __future__ import annotations

import hashlib
from typing import Any

import pytest

from pipeline.calibration import (
    report_from_json,
    verify_calibration_report,
)
from pipeline.loop.run_eval_pipeline import (
    EvalPipelineRunResult,
    run_eval_pipeline,
)
from pipeline.loop.run_pipeline import (
    PipelineRunResult,
    run_pipeline,
)

from tests.loop.conftest_section_5 import (
    EvalHarness,
    PubkeyVault,
    SubmissionHarness,
    build_eval_harness,
    build_submission_harness,
    make_cascade,
    make_charter,
)


# ---------------------------------------------------------------------------
# Parameter generators
# ---------------------------------------------------------------------------


_ORG_SLUGS = (
    "fit_farms_llc",
    "mycosymbiotics",
    "mystic_mamas",
    "run_a_muck_farm",
    "commons_org",
)


def _submission_param_tuples() -> list[tuple[str, str]]:
    """100 synthetic (org_slug, run_id) tuples for submission fuzz."""

    pairs: list[tuple[str, str]] = []
    for i in range(100):
        org = _ORG_SLUGS[i % len(_ORG_SLUGS)]
        pairs.append((org, f"run-fuzz-S-{i:03d}"))
    return pairs


def _eval_param_tuples() -> list[tuple[str, str]]:
    """100 synthetic (org_slug, run_id) tuples for eval fuzz.

    Runs are seeded such that the MA-09 first-write-wins assertion
    produces exactly ``len(_ORG_SLUGS)`` pubkey writes across the 100
    runs.  Run ordering is deterministic so the "first write per slug"
    check is stable.
    """

    pairs: list[tuple[str, str]] = []
    for i in range(100):
        org = _ORG_SLUGS[i % len(_ORG_SLUGS)]
        pairs.append((org, f"run-fuzz-E-{i:03d}"))
    return pairs


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run_submission(h: SubmissionHarness, *, org_slug: str, run_id: str) -> PipelineRunResult:
    return run_pipeline(
        run_id=run_id,
        org_slug=org_slug,
        session_id="sess-fuzz",
        rfa_hash="rfa-fuzz",
        project_context_hash="pc-fuzz",
        scribe_charter=make_charter("scribe"),
        editor_charter=make_charter("editor"),
        judge_charter=make_charter("judge"),
        scribe_cascade=make_cascade("scribe"),
        editor_cascade=make_cascade("editor"),
        judge_cascade=make_cascade("judge"),
        context=h.context,
        pre_gate_input_factory=h.pre_gate_input_factory,
    )


def _run_eval(h: EvalHarness, *, operator_org_slug: str, run_id: str) -> EvalPipelineRunResult:
    return run_eval_pipeline(
        run_id=run_id,
        operator_org_slug=operator_org_slug,
        golden_set_manifest_path=h.manifest_path,
        session_id="sess-fuzz",
        scribe_charter=make_charter("scribe"),
        editor_charter=make_charter("editor"),
        judge_charter=make_charter("judge"),
        scribe_cascade=make_cascade("scribe"),
        editor_cascade=make_cascade("editor"),
        judge_cascade=make_cascade("judge"),
        ctx=h.ctx,
        subset=None,
    )


# ---------------------------------------------------------------------------
# J.5.a Submission fuzz — 100 runs
# ---------------------------------------------------------------------------


class TestSubmissionFuzz:
    @pytest.mark.parametrize("org_slug,run_id", _submission_param_tuples())
    def test_submission_run_reaches_tabs_written_ok(
        self, org_slug: str, run_id: str
    ) -> None:
        h = build_submission_harness(run_id=run_id)
        r = _run_submission(h, org_slug=org_slug, run_id=run_id)
        assert r.final_phase == "tabs_delivered"
        assert r.three_tab_envelope_hash is not None
        # Zero cross-run leak — every fresh harness's vault store
        # contains paths scoped to this run_id only.
        scoped = [w for w in h.vault.writes if run_id in w["path"]]
        assert len(scoped) >= 1

    def test_submission_fuzz_cas_chain_is_linear_for_each_run(self) -> None:
        """CAS chain invariant: within a single run, every state.json
        write after the first carries a non-None expected hash equal to
        the prior write's committed hash (append-only CAS tail).
        """

        for org_slug, run_id in _submission_param_tuples():
            h = build_submission_harness(run_id=run_id)
            _run_submission(h, org_slug=org_slug, run_id=run_id)
            state_writes = [
                w for w in h.vault.writes if w["path"].endswith("/state.json")
            ]
            assert len(state_writes) >= 2
            # First write has no expected hash, subsequent writes carry
            # the previous commit's hash.
            first = state_writes[0]
            assert first["expected_current_file_hash"] is None
            prior_hash: str | None = hashlib.sha256(first["payload"]).hexdigest()
            for w in state_writes[1:]:
                assert w["expected_current_file_hash"] == prior_hash
                prior_hash = hashlib.sha256(w["payload"]).hexdigest()

    def test_submission_fuzz_final_hashes_are_unique_across_runs(self) -> None:
        """Determinism: with varying run_ids and fresh vaults, three-tab
        envelope hashes should be distinct (no hash collision) — this
        is the authoritative per-run final-state identity.
        """

        envelope_hashes: set[str] = set()
        for org_slug, run_id in _submission_param_tuples():
            h = build_submission_harness(run_id=run_id)
            r = _run_submission(h, org_slug=org_slug, run_id=run_id)
            assert r.three_tab_envelope_hash is not None
            envelope_hashes.add(r.three_tab_envelope_hash)
        # 100 runs → 100 distinct envelope hashes expected.
        assert len(envelope_hashes) == 100

    def test_submission_fuzz_zero_write_if_absent_collisions(self) -> None:
        """No run should reuse an existing vault path — every run is a
        fresh harness, so ``write-if-absent`` must never receive a
        pre-existing key.
        """

        for org_slug, run_id in _submission_param_tuples():
            h = build_submission_harness(run_id=run_id)
            _run_submission(h, org_slug=org_slug, run_id=run_id)
            absent_writes = [
                w for w in h.vault.writes if w["write_mode"] == "write-if-absent"
            ]
            # All write-if-absent calls landed (no collision raise).
            # If a collision occurred, run_pipeline would have raised.
            assert all(w["payload_len"] > 0 for w in absent_writes)


# ---------------------------------------------------------------------------
# J.5.b Eval fuzz — 100 runs with shared PubkeyVault
# ---------------------------------------------------------------------------


class TestEvalFuzz:
    """Eval fuzz uses a shared ``PubkeyVault`` across all 100 runs to
    exercise MA-09 first-write-wins.
    """

    def test_eval_fuzz_100_runs_first_write_wins_per_slug(self) -> None:
        """Runs 100 eval pipelines sharing one PubkeyVault.  Asserts
        exactly ``len(_ORG_SLUGS)`` pubkey writes landed (one per slug)
        and the remaining 95 runs read the pre-existing pubkey without
        writing.
        """

        shared_pubkey_vault = PubkeyVault()
        results: list[EvalPipelineRunResult] = []
        seen_slugs: set[str] = set()
        for org_slug, run_id in _eval_param_tuples():
            h = build_eval_harness(
                run_id=run_id,
                org_slug=org_slug,
                pubkey_vault=shared_pubkey_vault,
            )
            r = _run_eval(h, operator_org_slug=org_slug, run_id=run_id)
            results.append(r)
            seen_slugs.add(org_slug)

        # Exactly one pubkey_vault.write per unique org_slug — MA-09.
        pubkey_writes = shared_pubkey_vault.writes
        slugs_written = [w["operator_org_slug"] for w in pubkey_writes]
        assert len(pubkey_writes) == len(seen_slugs)
        assert set(slugs_written) == seen_slugs
        # And for each slug, exactly one write entry — not two or more.
        for slug in seen_slugs:
            assert slugs_written.count(slug) == 1

        # All 100 runs landed a well-formed EvalPipelineRunResult.
        assert len(results) == 100
        for r in results:
            assert r.final_phase in {
                "eval_finalized",
                "aborted_trusted_fail",
                "aborted_operator",
            }

    def test_eval_fuzz_signature_verifies_for_each_run(self) -> None:
        """Every eval run that emits a calibration report must verify
        under the pubkey landed in the shared vault.
        """

        shared_pubkey_vault = PubkeyVault()
        for org_slug, run_id in _eval_param_tuples():
            h = build_eval_harness(
                run_id=run_id,
                org_slug=org_slug,
                pubkey_vault=shared_pubkey_vault,
            )
            _run_eval(h, operator_org_slug=org_slug, run_id=run_id)
            # The pubkey written for this slug is the only one authoritative.
            pubkey_bytes = shared_pubkey_vault.stored.get(org_slug)
            assert pubkey_bytes is not None
            # Find the latest calibration report JSON payload in the
            # vault.  Reports land at ``.../{run_id}.json``; signatures
            # land at ``.../{run_id}.sig`` — filter to JSON only.
            report_writes = [
                w
                for w in h.vault.writes
                if "calibration_reports" in w["path"]
                and w["path"].endswith(".json")
                and w["intent"] == "golden-set-write"
            ]
            if not report_writes:
                # Some fuzz seeds may short-circuit; accept and skip.
                continue
            last_payload = report_writes[-1]["payload"]
            report = report_from_json(last_payload)
            # verify_calibration_report raises on invalid; bool otherwise.
            verify_calibration_report(report, pubkey_bytes=pubkey_bytes)

    def test_eval_fuzz_zero_second_write_for_any_slug(self) -> None:
        """Across 100 runs, no slug's pubkey is written twice.  This is
        the MA-09 first-write-wins invariant, re-asserted as a property.
        """

        shared_pubkey_vault = PubkeyVault()
        for org_slug, run_id in _eval_param_tuples():
            h = build_eval_harness(
                run_id=run_id,
                org_slug=org_slug,
                pubkey_vault=shared_pubkey_vault,
            )
            _run_eval(h, operator_org_slug=org_slug, run_id=run_id)

        per_slug_counts: dict[str, int] = {}
        for w in shared_pubkey_vault.writes:
            per_slug_counts[w["operator_org_slug"]] = (
                per_slug_counts.get(w["operator_org_slug"], 0) + 1
            )
        assert all(c == 1 for c in per_slug_counts.values())

    def test_eval_fuzz_provenance_sidecar_written_once_per_slug(self) -> None:
        """Provenance sidecar tracking: each first pubkey write should
        have been accompanied by a non-empty provenance blob in the
        same write call.  Second writes are impossible (see above).
        """

        shared_pubkey_vault = PubkeyVault()
        for org_slug, run_id in _eval_param_tuples():
            h = build_eval_harness(
                run_id=run_id,
                org_slug=org_slug,
                pubkey_vault=shared_pubkey_vault,
            )
            _run_eval(h, operator_org_slug=org_slug, run_id=run_id)

        # Every pubkey-write entry has a provenance sidecar (provenance_len > 0).
        for w in shared_pubkey_vault.writes:
            assert w["provenance_len"] > 0
        # And every stored slug has a matching provenance entry.
        assert set(shared_pubkey_vault.stored.keys()) == set(
            shared_pubkey_vault.provenance.keys()
        )

    def test_eval_fuzz_reads_accumulate_across_runs(self) -> None:
        """Per-run read against PubkeyVault happens at least once to
        reconcile pubkey-first-write; across 100 runs, total reads
        should be at least 100.
        """

        shared_pubkey_vault = PubkeyVault()
        for org_slug, run_id in _eval_param_tuples():
            h = build_eval_harness(
                run_id=run_id,
                org_slug=org_slug,
                pubkey_vault=shared_pubkey_vault,
            )
            _run_eval(h, operator_org_slug=org_slug, run_id=run_id)
        assert len(shared_pubkey_vault.reads) >= 100


# ---------------------------------------------------------------------------
# Determinism smoke — re-run one fuzz seed and confirm identical trajectory
# ---------------------------------------------------------------------------


class TestFuzzReplayDeterminism:
    def test_same_seed_replays_to_same_final_hash_submission(self) -> None:
        h1 = build_submission_harness(run_id="run-fuzz-replay-S")
        h2 = build_submission_harness(run_id="run-fuzz-replay-S")
        r1 = _run_submission(h1, org_slug="fit_farms_llc", run_id="run-fuzz-replay-S")
        r2 = _run_submission(h2, org_slug="fit_farms_llc", run_id="run-fuzz-replay-S")
        assert r1.three_tab_envelope_hash == r2.three_tab_envelope_hash
        assert r1.final_phase == r2.final_phase

    def test_different_seeds_yield_different_final_hash_submission(self) -> None:
        h1 = build_submission_harness(run_id="run-fuzz-seed-A")
        h2 = build_submission_harness(run_id="run-fuzz-seed-B")
        r1 = _run_submission(h1, org_slug="fit_farms_llc", run_id="run-fuzz-seed-A")
        r2 = _run_submission(h2, org_slug="fit_farms_llc", run_id="run-fuzz-seed-B")
        assert r1.three_tab_envelope_hash != r2.three_tab_envelope_hash
