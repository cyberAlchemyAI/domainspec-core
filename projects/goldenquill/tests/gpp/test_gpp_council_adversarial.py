"""
Phase 0 GPP Hardening — Tier 2 COUNCIL adversarial tests
=========================================================

Complements tests/gpp/test_gpp_phase0.py with hostile-input probes
per pipeline/validation/gpp_phase0_adversarial_test_specs.md §Tier 2.

Scope note: the current gpp_council_dispatch.py implements the PLAN-LAYER
Tier 2 council — exactly two seats (red_team + reasoner_review), UNCONDITIONAL
dispatch per gpp_spec_v1.md §3.2.

The 5-family Code Thesis Committee (CTC) is a DIFFERENT mechanism, not yet
wired into this module; CTC-specific probes from the adversarial spec are
marked xfail with a pointer to the Phase-1 CTC dispatch work item.

Attack classes:
  ADV-COUNCIL-01  family-collision at dispatch
  ADV-COUNCIL-02  quorum-gaming (payload count invariants)
  ADV-COUNCIL-03  verdict-injection (payload-shape contracts)
  ADV-COUNCIL-04  timeout-evasion (dry-run-mode determinism)
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml as pyyaml

GPP_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "pipeline"
    / "validation"
    / "integration_scope_close_2026-04-19"
    / "gpp"
)
# pipeline/validation/* is gitignored; see test_gpp_phase0.py for why this
# local-only suite skips clean CI clones without historical dispatch artifacts.
if not GPP_DIR.is_dir():
    pytest.skip(
        f"gpp/ dispatch tree not present at {GPP_DIR}; local-only suite",
        allow_module_level=True,
    )
if str(GPP_DIR) not in sys.path:
    sys.path.insert(0, str(GPP_DIR))

import gpp_council_dispatch  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _write_router(
    plan_dir: Path,
    *,
    red_team_model: str = "groq/openai/gpt-oss-120b",
    reasoner_model: str = "google/gemini-2.5-pro",
    include_red_team: bool = True,
    include_reasoner: bool = True,
) -> Path:
    """Write a router.yaml into plan_dir for repo-root discovery."""
    tilth: dict[str, Any] = {}
    if include_red_team:
        tilth["red_team"] = {
            "primary": red_team_model,
            "fallback": "anthropic/claude-haiku-4-5",
            "role": "Red Team adversarial scan.",
        }
    if include_reasoner:
        tilth["reasoner_review"] = {
            "primary": reasoner_model,
            "fallback": "anthropic/claude-opus-4-6",
            "role": "Reasoning + prompt review.",
        }
    data = {"tilth": tilth}
    router = plan_dir / "router.yaml"
    router.write_text(pyyaml.dump(data), encoding="utf-8")
    return router


@pytest.fixture
def plan_dir(tmp_path: Path) -> Path:
    _write_router(tmp_path)
    (tmp_path / "01_scope.md").write_text("Scope pin.\n", encoding="utf-8")
    return tmp_path


def _minimal_det_report(plan_doc: str = "01_scope.md") -> dict[str, Any]:
    return {
        "tier_1_overall_status": "PASS",
        "plan_sub_docs": [plan_doc],
        "checks": [
            {"check_id": "SCOPE-FREEZE-BACKDOOR-FLAG", "status": "PASS", "flags": []},
        ],
    }


# ===========================================================================
# ADV-COUNCIL-01 — family-collision at dispatch
# ===========================================================================


def test_adv_reviewer_family_equal_to_author_family_is_router_responsibility(
    plan_dir: Path,
) -> None:
    """The plan-layer Tier 2 enforces cross-family at the ROUTER level
    (router.yaml binds the two seats to non-Anthropic providers by design).

    If the router were mis-configured to bind red_team to an Anthropic model,
    this module does NOT currently detect the collision at dispatch time —
    it honors whatever router.yaml says.  This is a documented boundary:
    cross-family enforcement is the router's job.  Probe confirms the boundary.
    """
    # Re-write router with red_team on Anthropic (adversarial config)
    _write_router(
        plan_dir,
        red_team_model="anthropic/claude-sonnet-4-6",  # SAME family as author
    )
    router = gpp_council_dispatch.load_router(plan_dir)
    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], _minimal_det_report(), router
    )
    # Module passes through the router binding — cross-family enforcement
    # must happen upstream (router audit / admin-risk check).
    rt = next(p for p in payloads if p["seat"] == "red_team")
    assert rt["model_primary"].startswith("anthropic/"), (
        "Module currently honors router; cross-family enforcement is upstream"
    )


def test_adv_missing_red_team_binding_returns_error_payload(plan_dir: Path) -> None:
    """If router.yaml is missing tilth.red_team entirely, build_council_payloads
    still returns 2 payload slots but red_team has model_primary='UNKNOWN'."""
    _write_router(plan_dir, include_red_team=False)
    router = gpp_council_dispatch.load_router(plan_dir)
    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], _minimal_det_report(), router
    )
    assert len(payloads) == 2
    rt = next(p for p in payloads if p["seat"] == "red_team")
    assert rt["model_primary"] == "UNKNOWN", (
        "Missing binding should yield UNKNOWN placeholder, not a real model"
    )


def test_adv_missing_reasoner_binding_returns_error_payload(plan_dir: Path) -> None:
    """Symmetric check for missing reasoner_review."""
    _write_router(plan_dir, include_reasoner=False)
    router = gpp_council_dispatch.load_router(plan_dir)
    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], _minimal_det_report(), router
    )
    rr = next(p for p in payloads if p["seat"] == "reasoner_review")
    assert rr["model_primary"] == "UNKNOWN"


def test_adv_malformed_router_yaml_returns_error_dict(tmp_path: Path) -> None:
    """load_router returns {'error': ...} instead of raising on malformed YAML."""
    bad = tmp_path / "router.yaml"
    bad.write_text("tilth:\n  red_team: [broken\n", encoding="utf-8")  # invalid YAML
    result = gpp_council_dispatch.load_router(tmp_path)
    assert "error" in result
    assert "parse" in result["error"].lower()


def test_adv_missing_router_yaml_returns_error(tmp_path: Path) -> None:
    """load_router returns error dict when router.yaml is absent."""
    result = gpp_council_dispatch.load_router(tmp_path)
    assert "error" in result
    assert "not found" in result["error"]


# ===========================================================================
# ADV-COUNCIL-02 — quorum-gaming (payload count invariants)
# ===========================================================================


def test_adv_payload_count_always_exactly_two(plan_dir: Path) -> None:
    """Plan-layer Tier 2: build_council_payloads returns EXACTLY 2 payloads.
    Not 1, not 3 — always the (red_team, reasoner_review) pair."""
    router = gpp_council_dispatch.load_router(plan_dir)
    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], _minimal_det_report(), router
    )
    assert len(payloads) == 2


def test_adv_payload_seats_are_distinct(plan_dir: Path) -> None:
    """The two payloads must be for distinct seats — never two red_team."""
    router = gpp_council_dispatch.load_router(plan_dir)
    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], _minimal_det_report(), router
    )
    seats = [p["seat"] for p in payloads]
    assert len(set(seats)) == 2
    assert set(seats) == {"red_team", "reasoner_review"}


def test_adv_payload_order_is_stable(plan_dir: Path) -> None:
    """Payload order is documented as [red_team, reasoner_review]. Stable
    ordering matters for downstream manifests that index by position."""
    router = gpp_council_dispatch.load_router(plan_dir)
    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], _minimal_det_report(), router
    )
    assert payloads[0]["seat"] == "red_team"
    assert payloads[1]["seat"] == "reasoner_review"


@pytest.mark.xfail(
    reason="5-family Code Thesis Committee dispatch is a Phase-1 work item; "
    "this probe from the adversarial spec targets CTC, not plan-layer Tier 2.",
    strict=False,
)
def test_adv_fewer_than_5_reviewers_rejected() -> None:
    """CTC-specific — not implemented in gpp_council_dispatch yet.
    Kept as xfail to surface the gap in Phase-1 planning."""
    raise NotImplementedError("CTC 5-family dispatch not wired yet")


# ===========================================================================
# ADV-COUNCIL-03 — verdict-injection / payload-shape contracts
# ===========================================================================


def test_adv_payload_exposes_only_path_references_not_content(plan_dir: Path) -> None:
    """Per L-002 (path references, not content dumps): the payload's
    shared_context carries plan_sub_docs as paths, NOT the file contents."""
    router = gpp_council_dispatch.load_router(plan_dir)
    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], _minimal_det_report(), router
    )
    for p in payloads:
        ctx = p["context"]
        assert "plan_sub_docs" in ctx
        # plan_sub_docs is a list of strings (paths), not opened file contents
        assert all(isinstance(d, str) for d in ctx["plan_sub_docs"])


def test_adv_payload_role_excerpt_truncated_to_200_chars(plan_dir: Path) -> None:
    """role_excerpt is truncated to 200 chars to bound context size."""
    # Re-write router with a huge role string
    big_role = "X" * 10_000
    data = {
        "tilth": {
            "red_team": {"primary": "groq/openai/gpt-oss-120b", "role": big_role},
            "reasoner_review": {"primary": "google/gemini-2.5-pro", "role": big_role},
        }
    }
    (plan_dir / "router.yaml").write_text(pyyaml.dump(data), encoding="utf-8")
    router = gpp_council_dispatch.load_router(plan_dir)
    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], _minimal_det_report(), router
    )
    for p in payloads:
        assert len(p["role_excerpt"]) <= 200, (
            "role_excerpt must be truncated to bound context size"
        )


def test_adv_scope_freeze_flags_truncated_to_10(plan_dir: Path) -> None:
    """shared_context.scope_freeze_flags is truncated to first 10 items
    to bound context size — full list is on disk."""
    det = {
        "tier_1_overall_status": "PASS",
        "plan_sub_docs": ["01_scope.md"],
        "checks": [
            {
                "check_id": "SCOPE-FREEZE-BACKDOOR-FLAG",
                "status": "FLAG",
                "flags": [
                    {"phrase": f"adversarial flag {i}", "severity": "FLAG"}
                    for i in range(50)
                ],
            }
        ],
    }
    router = gpp_council_dispatch.load_router(plan_dir)
    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], det, router
    )
    for p in payloads:
        flags_in_ctx = p["context"]["scope_freeze_flags"]
        assert len(flags_in_ctx) == 10
        # The count of all flags is still reported accurately
        assert p["context"]["scope_freeze_flag_count"] == 50


def test_adv_stub_findings_marked_with_stub_true(plan_dir: Path) -> None:
    """Dry-run stub findings MUST carry stub:True so the manifest signer can
    reject them as non-real council output."""
    gpp_dir = plan_dir / "gpp"
    gpp_dir.mkdir()
    date_stamp = datetime.date.today().isoformat()
    (gpp_dir / f"gpp_det_report_{date_stamp}.json").write_text(
        json.dumps(_minimal_det_report()), encoding="utf-8"
    )
    result = gpp_council_dispatch.run_council_dispatch(plan_dir, dry_run=True)
    assert result.get("exit_code") == 0
    # Load the written findings and verify stub markers
    findings_path = plan_dir / "gpp" / f"council_findings_{date_stamp}.json"
    assert findings_path.is_file()
    data = json.loads(findings_path.read_text())
    assert data["dispatch_mode"] == "dry_run"
    for f in data["findings"]:
        assert f.get("stub") is True, (
            "All dry-run findings must be marked stub:True"
        )


# ===========================================================================
# ADV-COUNCIL-04 — timeout-evasion / offline-mode determinism
# ===========================================================================


def test_adv_dry_run_deterministic_across_invocations(plan_dir: Path) -> None:
    """Dry-run mode is deterministic: same inputs → same payload shape."""
    router = gpp_council_dispatch.load_router(plan_dir)
    p1 = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], _minimal_det_report(), router
    )
    p2 = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], _minimal_det_report(), router
    )
    # Compare non-timestamp fields
    for a, b in zip(p1, p2):
        assert a["seat"] == b["seat"]
        assert a["model_primary"] == b["model_primary"]
        assert a["prompt"] == b["prompt"]


def test_adv_offline_mode_never_requires_keys(plan_dir: Path) -> None:
    """Dry-run mode works without any BYOK keys present — no key lookup
    should be required.  Sanity check: execute_dispatch(dry_run=True) returns
    stubs regardless of env state."""
    router = gpp_council_dispatch.load_router(plan_dir)
    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], _minimal_det_report(), router
    )
    findings, mode = gpp_council_dispatch.execute_dispatch(
        payloads, env={}, dry_run=True
    )
    assert mode == "dry_run"
    assert len(findings) == 2  # one stub per seat
    assert all(f.get("stub") for f in findings)


def test_adv_no_keys_mode_also_produces_stubs(plan_dir: Path) -> None:
    """When dry_run=False but no keys are present, execute_dispatch falls back
    to stub mode labeled stub_no_keys — does NOT make real HTTP calls."""
    router = gpp_council_dispatch.load_router(plan_dir)
    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir, ["01_scope.md"], _minimal_det_report(), router
    )
    findings, mode = gpp_council_dispatch.execute_dispatch(
        payloads, env={}, dry_run=False
    )
    # Either stub_no_keys or stub_http_unavailable — both acceptable stub modes
    assert mode in ("stub_no_keys", "stub_http_unavailable")
    assert len(findings) == 2
    assert all(f.get("stub") for f in findings)


def test_adv_run_council_dispatch_fails_fast_without_det_report(tmp_path: Path) -> None:
    """run_council_dispatch returns an error dict (exit_code=1) when no
    DET report is available — no silent PASS."""
    _write_router(tmp_path)
    # No gpp_det_report_*.json written
    result = gpp_council_dispatch.run_council_dispatch(tmp_path, dry_run=True)
    assert "error" in result
    assert result["exit_code"] == 1


def test_adv_run_council_dispatch_rejects_malformed_det_report(tmp_path: Path) -> None:
    """If gpp_det_report_*.json exists but is malformed, dispatch errors out."""
    _write_router(tmp_path)
    gpp_dir = tmp_path / "gpp"
    gpp_dir.mkdir()
    (gpp_dir / "gpp_det_report_2026-04-19.json").write_text(
        "{ invalid json", encoding="utf-8"
    )
    result = gpp_council_dispatch.run_council_dispatch(tmp_path, dry_run=True)
    assert "error" in result
