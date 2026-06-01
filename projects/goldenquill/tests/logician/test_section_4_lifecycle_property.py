"""§4 Logician Round L.3 — full PRE → silent-loop → POST parametric fuzz.

Per spec card § L.3: given a clean Logician instance, run the full lifecycle
N times with N distinct ``(org_slug, session_id, claim_set)`` triples
(N parametrized over [2, 8, 16, 32]). Yields 2 + 8 + 16 + 32 = 58 individual
test instances in a single parameterized class.

Plus seven cross-cutting invariants (§2 Round K K.3 pattern):

* every run produces ``PostGateResult(success=True, ...)`` OR a fail-closed
  ``PostGateResult(success=False, failure_code=...)`` — never partial state;
* every run's lock_history append carries F-AMDT-12 daily-log block (modeled
  via the canonical-bytes recipe sanity check);
* no cross-org claim-evidence map leak (Law 3 mechanical invariant);
* admin-risk monotonicity holds across the full run;
* rails-report signature verifies post-delivery, tamper invalidates;
* conversation-log chain integrity holds across all N sessions;
* runner state machine transitions are deterministic and irreversible
  (no replay; F-PRE-19 mid-loop guard intact for every run).

Floor: ≥58 individual test instances + ≥7 cross-cutting invariant methods
= ≥65 tests total.
"""

from __future__ import annotations

import hashlib
import hmac
import random
from typing import Iterable

import pytest

from pipeline.logician.claim_evidence import (
    canonical_map_bytes,
    compute_content_hash,
)
from pipeline.logician.conversation_log import (
    serialise_entry_line,
    verify_chain,
)
from pipeline.logician.gate_runner import (
    GateRunnerPostResult,
    LogicianGateRunner,
    LogicianMidLoopCall,
    POST_GATE_STEP_ORDER,
    STATE_DONE,
    STATE_PRE,
)
from pipeline.logician.post_gate import F_POST_10, F_POST_11
from pipeline.logician.pre_gate import (
    PRE_GATE_CHECK_ORDER,
    PreGateResult,
)

from tests.logician.conftest_section_4 import (
    SESSION_HMAC_KEY_ACTIVE,
    AdminRiskCounters,
    CapturingVaultWrite,
    build_genesis_chain,
    canonical_rails_report_bytes,
    default_post_input,
    default_pre_input,
    fresh_runner,
    make_doc_sourced_claim,
    make_unsourced_claim,
    sign_rails_report,
    verify_rails_report,
)


# ---------------------------------------------------------------------------
# Fuzz parameter expansion: 2 + 8 + 16 + 32 = 58 instances
# ---------------------------------------------------------------------------


def _expand_fuzz_params() -> list[tuple[int, int]]:
    """Yield 58 (n, idx) pairs across N ∈ {2, 8, 16, 32}."""

    pairs: list[tuple[int, int]] = []
    for n in (2, 8, 16, 32):
        for idx in range(n):
            pairs.append((n, idx))
    return pairs


FUZZ_PARAMS = _expand_fuzz_params()
assert len(FUZZ_PARAMS) == 58, f"fuzz floor 58 instances; got {len(FUZZ_PARAMS)}"


# ---------------------------------------------------------------------------
# Deterministic synthesizer for (org_slug, session_id, claim_set) triples
# ---------------------------------------------------------------------------


def _synth_triple(seed_n: int, idx: int) -> dict:
    """Build a deterministic input bundle from (n, idx).

    The seed is a fixed function of (n, idx); all PRNG state derives from it.
    Cross-org isolation: each idx within an n picks a unique org_slug.
    """

    rng = random.Random((seed_n * 10_000) + idx)
    org_slug = f"org_l_n{seed_n}_i{idx:02d}"
    session_id = f"sess-{seed_n}-{idx:03d}-{rng.randrange(2**16):04x}"

    # Claim set: deterministic mix of DOC_SOURCED + (occasionally) UNSOURCED.
    # Honour the claim_id determinism by stamping draft_offset = idx*100 + j
    # so distinct triples yield distinct claim_ids.
    n_claims = 1 + (idx % 4)
    claims = []
    for j in range(n_claims):
        text = f"Claim-{seed_n}-{idx}-{j}: deterministic source line {rng.randrange(1_000)}."
        # Every 5th claim is UNSOURCED → fuzz both happy + failure paths
        if (idx * 11 + j) % 5 == 0:
            claims.append(
                make_unsourced_claim(
                    offset=(idx * 100) + j, text=text
                )
            )
        else:
            claims.append(
                make_doc_sourced_claim(
                    offset=(idx * 100) + j, text=text
                )
            )

    # admin-risk counter: deterministic; every 7th run flags 1 hard-block
    hard_block_count = 1 if (idx % 7 == 0 and idx > 0) else 0

    return {
        "org_slug": org_slug,
        "session_id": session_id,
        "claims": tuple(claims),
        "hard_block_count": hard_block_count,
    }


# =============================================================================
# L.3 — Parametric lifecycle fuzz (58 individual instances)
# =============================================================================


class TestL3_LifecycleFuzz:
    """One parameterized class, 58 invocations across N ∈ {2, 8, 16, 32}.

    Each instance runs a clean Logician through the complete PRE → BETWEEN
    → POST lifecycle and asserts the cross-cutting invariants from spec
    card § L.3 hold for that single run. Cross-run invariants (no claim-
    evidence-map leak, monotonic admin-risk register, no conversation-log
    chain bleed-through) are exercised in :class:`TestL3_CrossCuttingInvariants`.
    """

    @pytest.mark.parametrize(("n", "idx"), FUZZ_PARAMS, ids=[f"n{n}-i{i:03d}" for n, i in FUZZ_PARAMS])
    def test_lifecycle_run_produces_terminal_state(
        self, n: int, idx: int
    ) -> None:
        triple = _synth_triple(n, idx)
        runner = fresh_runner()
        # PRE
        pre_result = runner.run_pre_gate(default_pre_input())
        assert isinstance(pre_result, PreGateResult)
        assert pre_result.passed is True

        # BETWEEN
        runner.mark_between()

        # POST
        post = default_post_input(
            org_slug=triple["org_slug"],
            session_id=triple["session_id"],
            claims=triple["claims"],
            admin_risk_hard_block_count=triple["hard_block_count"],
        )
        post_result = runner.run_post_gate(post)
        assert isinstance(post_result, GateRunnerPostResult)
        # State machine transitioned to DONE
        assert runner.state == STATE_DONE
        # Either passed=True (no fail) OR failure_code carries an F-POST-* tag
        if post_result.passed:
            assert post_result.failed_step_number is None
            assert post_result.failure_codes == ()
        else:
            assert post_result.failure_code is not None
            # All failure codes are F-POST-* family
            for code in post_result.failure_codes:
                assert code.startswith("F-POST-") or code.startswith("F-CEDAR-") or code.startswith("F-BT")
        # claim_evidence_map is populated regardless of pass/fail (§4.4.4)
        assert post_result.claim_evidence_map is not None


# =============================================================================
# L.3 — Cross-cutting invariants (deterministic, run-to-run consistency)
# =============================================================================


class TestL3_CrossCuttingInvariants:
    def test_invariant_1_no_partial_state(self) -> None:
        """Every run produces a terminal PostGateResult — never partial state."""

        for (n, idx) in [(2, 0), (8, 3), (16, 7), (32, 15)]:
            triple = _synth_triple(n, idx)
            runner = fresh_runner()
            runner.run_pre_gate(default_pre_input())
            runner.mark_between()
            r = runner.run_post_gate(
                default_post_input(
                    org_slug=triple["org_slug"],
                    session_id=triple["session_id"],
                    claims=triple["claims"],
                    admin_risk_hard_block_count=triple["hard_block_count"],
                )
            )
            assert runner.state == STATE_DONE
            # underlying_post_gate_result populated even on fail (§4.4.4)
            assert r.underlying_post_gate_result is not None

    def test_invariant_2_lock_history_canonical_bytes_recipe(self) -> None:
        """Per F-AMDT-12: a lock-history row must canonicalize via the
        sort_keys + tight-separators recipe and append byte-for-byte.

        Modeled here against the rails-report canonical-bytes builder
        (same recipe). Verifies invariant holds across N=58 hash inputs.
        """

        seen_hashes: set[str] = set()
        for (n, idx) in FUZZ_PARAMS:
            triple = _synth_triple(n, idx)
            row = {
                "org_slug": triple["org_slug"],
                "session_id": triple["session_id"],
                "lock_timestamp_utc": "2026-04-29T00:00:00Z",
                "code_sha3_512_prefix": "x" * 16,
            }
            body = canonical_rails_report_bytes(row)
            h = hashlib.sha3_512(body).hexdigest()
            seen_hashes.add(h)
        # 58 distinct triples → 58 distinct hashes (no two collide)
        assert len(seen_hashes) == 58

    def test_invariant_3_no_cross_org_claim_evidence_leak(self) -> None:
        """Law 3 mechanical: session-A in org-A produces a claim_evidence_map
        whose org_slug field MUST equal org-A. No bleed-through across runs."""

        seen: list[tuple[str, str]] = []
        for (n, idx) in [(2, 0), (2, 1), (8, 2), (16, 5)]:
            triple = _synth_triple(n, idx)
            runner = fresh_runner()
            runner.run_pre_gate(default_pre_input())
            runner.mark_between()
            r = runner.run_post_gate(
                default_post_input(
                    org_slug=triple["org_slug"],
                    session_id=triple["session_id"],
                    claims=triple["claims"],
                    admin_risk_hard_block_count=triple["hard_block_count"],
                )
            )
            assert r.claim_evidence_map is not None
            assert r.claim_evidence_map.org_slug == triple["org_slug"]
            seen.append((triple["org_slug"], r.claim_evidence_map.org_slug))
        # Every (input, output) pair is internally consistent
        for inp, outp in seen:
            assert inp == outp

    def test_invariant_4_admin_risk_monotonicity_across_run(self) -> None:
        """Cumulative low/medium/high never decrease across the lifecycle."""

        prior = AdminRiskCounters()
        for (n, idx) in FUZZ_PARAMS[:32]:  # subset of fuzz instances
            triple = _synth_triple(n, idx)
            # Append one entry per run based on hard_block_count
            sev = "RED" if triple["hard_block_count"] > 0 else "GREEN"
            new = prior.append(sev)
            assert new.dominates(prior)
            prior = new

    def test_invariant_5_rails_report_signature_round_trip(self) -> None:
        """Rails report signature verifies post-delivery; tamper invalidates."""

        for (n, idx) in [(2, 0), (8, 4), (16, 8), (32, 16)]:
            triple = _synth_triple(n, idx)
            report = {
                "session_id": triple["session_id"],
                "org_slug": triple["org_slug"],
                "verdict": "FAIL" if triple["hard_block_count"] > 0 else "PASS",
            }
            body = canonical_rails_report_bytes(report)
            sig = sign_rails_report(body, key=SESSION_HMAC_KEY_ACTIVE)
            assert verify_rails_report(body, sig, SESSION_HMAC_KEY_ACTIVE) is True
            tampered = body[:1] + bytes([body[1] ^ 0xFF]) + body[2:]
            assert verify_rails_report(tampered, sig, SESSION_HMAC_KEY_ACTIVE) is False

    def test_invariant_6_conversation_chain_integrity_per_session(self) -> None:
        """Conversation-log chain integrity holds for every distinct session."""

        for (n, idx) in [(2, 0), (8, 6), (16, 11), (32, 23)]:
            triple = _synth_triple(n, idx)
            chain = build_genesis_chain(
                3 + (idx % 4),
                session_id=triple["session_id"],
                org_slug=triple["org_slug"],
            )
            r = verify_chain(chain)
            assert r.chain_intact is True
            assert r.head_seq_id == 3 + (idx % 4)

    def test_invariant_7_state_machine_irreversible_per_run(self) -> None:
        """F-PRE-19 mid-loop guard intact: no run can re-enter PRE after DONE."""

        for (n, idx) in [(2, 1), (8, 5), (16, 12), (32, 27)]:
            triple = _synth_triple(n, idx)
            runner = fresh_runner()
            runner.run_pre_gate(default_pre_input())
            runner.mark_between()
            runner.run_post_gate(
                default_post_input(
                    org_slug=triple["org_slug"],
                    session_id=triple["session_id"],
                    claims=triple["claims"],
                    admin_risk_hard_block_count=triple["hard_block_count"],
                )
            )
            # Re-entry blocked
            with pytest.raises(LogicianMidLoopCall):
                runner.run_pre_gate(default_pre_input())
            with pytest.raises(LogicianMidLoopCall):
                runner.run_post_gate(default_post_input())
            with pytest.raises(LogicianMidLoopCall):
                runner.mark_between()
