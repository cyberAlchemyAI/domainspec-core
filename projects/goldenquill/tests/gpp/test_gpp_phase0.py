"""
Phase 0 GPP Hardening — Unit Tests
====================================

Coverage targets (Da Vinci v2 §7, Phase 0 queue):
  - One test_det_check_<N>_* per DET check 1..10
  - Adversarial counterpart for each check (test_adv_*)
  - Bug-fix specific tests:
      test_det_family_taxonomy_skips_non_model_keys
      test_det_version_resolve_treats_target_wording_as_pending
      test_det_cite_skips_documented_template_globs
  - New tool tests:
      test_council_dispatch_emits_red_team_and_reasoner_unconditionally
      test_manifest_roundtrip_ed25519_and_ml_dsa_65

Coverage requirement: ≥ 95% on gpp_det.py.
Cross-family note: tests were authored by the Anthropic code_author seat;
Thesis Committee review (5 non-Anthropic families) gates merge.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pytest

# ---------------------------------------------------------------------------
# Import the tools under test — resolve the gpp/ directory path at import time
# so the test suite is portable regardless of working directory.
# ---------------------------------------------------------------------------

GPP_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "pipeline"
    / "validation"
    / "integration_scope_close_2026-04-19"
    / "gpp"
)
# pipeline/validation/* is gitignored; the gpp/ tree only exists in checkouts
# that have the historical Thesis-round dispatch artifacts. Skip this
# local-only suite on clean CI clones instead of failing collection.
if not GPP_DIR.is_dir():
    pytest.skip(
        f"gpp/ dispatch tree not present at {GPP_DIR}; local-only suite",
        allow_module_level=True,
    )
if str(GPP_DIR) not in sys.path:
    sys.path.insert(0, str(GPP_DIR))

import gpp_det  # noqa: E402
import gpp_council_dispatch  # noqa: E402
import gpp_manifest  # noqa: E402

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

REPO_ROOT = GPP_DIR.parent.parent.parent.parent  # …/GoldenQuill


@pytest.fixture
def plan_dir(tmp_path: Path) -> Path:
    """Empty temporary plan directory with a minimal router.yaml at repo root."""
    return tmp_path


@pytest.fixture
def plan_dir_with_router(tmp_path: Path) -> Path:
    """Temp dir that ALSO has a router.yaml sibling so find_repo_root succeeds."""
    (tmp_path / "router.yaml").write_text(
        "tilth:\n  red_team:\n    primary: groq/openai/gpt-oss-120b\n"
        "    fallback: anthropic/claude-haiku-4-5\n    role: Red Team\n"
        "  reasoner_review:\n    primary: google/gemini-2.5-pro\n"
        "    fallback: anthropic/claude-opus-4-6\n    role: Reasoner\n",
        encoding="utf-8",
    )
    return tmp_path


def _make_plan_doc(plan_dir: Path, name: str, content: str) -> Path:
    p = plan_dir / name
    p.write_text(content, encoding="utf-8")
    return p


def _make_router(plan_dir: Path, extra_seats: dict | None = None) -> Path:
    """Write a minimal router.yaml that satisfies FAMILY-TAXONOMY checks."""
    seats = extra_seats or {}
    base = {
        "tilth": {
            "scout":   {"primary": "ollama/mistral:7b", "fallback": "groq/llama-3.1-8b-instant"},
            "scribe":  {"primary": "anthropic/claude-sonnet-4-6", "fallback": "groq/qwen/qwen3-32b"},
            "editor":  {"primary": "groq/llama-3.3-70b-versatile", "fallback": "openai/gpt-4o-mini"},
            "judge":   {"primary": "groq/qwen/qwen3-32b", "fallback": "google/gemini-2.5-pro"},
            "red_team": {"primary": "groq/openai/gpt-oss-120b", "fallback": "anthropic/claude-haiku-4-5",
                         "role": "Red Team adversarial scan."},
            "reasoner_review": {"primary": "google/gemini-2.5-pro", "fallback": "anthropic/claude-opus-4-6",
                                "role": "Reasoning + prompt review."},
            "code_author": "anthropic/claude_code",
            "code_reviewer_1": {"primary": "openai/codex", "fallback": "openai/gpt-4o"},
            "code_reviewer_2": {"primary": "alibaba/qwen3-32b", "fallback": "alibaba/qwen2.5-72b"},
            "code_reviewer_3": {"primary": "meta/llama-3.3-70b", "fallback": "meta/llama-3.1-70b"},
            "code_reviewer_4": {"primary": "openai_oss/gpt-oss-120b", "fallback": "openai_oss/gpt-oss-20b"},
            "code_reviewer_5": {"primary": "moonshot/kimi-k2-instruct-0905",
                                "fallback": "google/gemini-2.5-pro"},
            # Non-model values — must NOT inflate family count (Bug-1 fix)
            "code_findings_path": "pipeline/validation/code_reviews/<round-id>/",
            "code_merge_rule": "all_pass",
            "code_retry_cap": 1,
            "code_dashboard_post": "batch",
            **seats,
        }
    }
    import yaml  # installed via pyyaml in Phase-0 pyproject.toml update

    p = plan_dir / "router.yaml"
    p.write_text(yaml.dump(base), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Check 1 — CITE-RESOLVE
# ---------------------------------------------------------------------------


def test_det_check_1_cite_resolve_passes_when_all_cites_exist(tmp_path: Path) -> None:
    """Check 1 PASS: every cited path exists on disk."""
    (tmp_path / "router.yaml").touch()
    # Create a target file
    (tmp_path / "pipeline").mkdir()
    (tmp_path / "pipeline" / "SESSION_BOOTSTRAP.md").write_text("# Bootstrap")
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "See pipeline/SESSION_BOOTSTRAP.md for orientation.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_cite_resolve(docs, tmp_path)
    assert result["status"] == "PASS", result["findings"]


def test_adv_check_1_cite_resolve_fails_for_missing_file(tmp_path: Path) -> None:
    """Adversarial Check 1: citing a non-existent file triggers FAIL."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "See pipeline/blueprint/v0.1/section_99_does_not_exist.md for details.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_cite_resolve(docs, tmp_path)
    assert result["status"] == "FAIL"
    assert any("section_99_does_not_exist" in f["cite"] for f in result["findings"])


# ---------------------------------------------------------------------------
# Check 2 — VERSION-RESOLVE
# ---------------------------------------------------------------------------


def test_det_check_2_version_resolve_passes_for_known_locked_version(tmp_path: Path) -> None:
    """Check 2 PASS: version claim matches first 120 lines of the target file."""
    (tmp_path / "router.yaml").touch()
    (tmp_path / "pipeline" / "blueprint" / "v0.1").mkdir(parents=True)
    sec4 = tmp_path / "pipeline" / "blueprint" / "v0.1" / "section_04_logician.md"
    sec4.write_text("# Section 4 Logician v2.1\n\nLOCKED 2026-04-18\n")
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "§4 v2.1 LOCKED is the current foundation.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_version_resolve(docs, tmp_path)
    assert result["status"] == "PASS", result["findings"]


def test_adv_check_2_version_resolve_fails_for_unknown_version(tmp_path: Path) -> None:
    """Adversarial Check 2: claiming v99.0 LOCKED when file has v2.1."""
    (tmp_path / "router.yaml").touch()
    (tmp_path / "pipeline" / "blueprint" / "v0.1").mkdir(parents=True)
    sec4 = tmp_path / "pipeline" / "blueprint" / "v0.1" / "section_04_logician.md"
    sec4.write_text("# Section 4 Logician v2.1\n\n")
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "§4 v99.0 LOCKED is the foundation.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_version_resolve(docs, tmp_path)
    assert result["status"] == "FAIL"
    assert any("v99.0" in f["claim"] for f in result["findings"])


# ---------------------------------------------------------------------------
# Check 3 — XDOC-REF
# ---------------------------------------------------------------------------


def test_det_check_3_xdoc_ref_passes_when_ref_exists(tmp_path: Path) -> None:
    """Check 3 PASS: cross-doc reference resolves to an existing file in plan dir."""
    (tmp_path / "router.yaml").touch()
    _make_plan_doc(tmp_path, "02_architecture.md", "# Architecture\n")
    plan_doc = _make_plan_doc(
        tmp_path, "01_scope.md",
        "See `02_architecture.md` for details.\n"
    )
    docs = {plan_doc: plan_doc.read_text(), tmp_path / "02_architecture.md": "# Architecture\n"}
    result = gpp_det.check_xdoc_ref(docs, tmp_path, tmp_path)
    assert result["status"] == "PASS", result["findings"]


def test_adv_check_3_xdoc_ref_fails_for_missing_file(tmp_path: Path) -> None:
    """Adversarial Check 3: referencing `99_missing.md` that is not in plan dir."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(
        tmp_path, "01_scope.md",
        "See `99_missing.md` for details.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_xdoc_ref(docs, tmp_path, tmp_path)
    assert result["status"] == "FAIL"
    assert any("99_missing.md" in f["ref"] for f in result["findings"])


# ---------------------------------------------------------------------------
# Check 4 — ROW-COUNT-ARITHMETIC
# ---------------------------------------------------------------------------


def test_det_check_4_row_count_arithmetic_passes_on_correct_count(tmp_path: Path) -> None:
    """Check 4 PASS: declared row count matches the table above it."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(tmp_path, "01_plan.md", (
        "| Col A | Col B |\n"
        "|---|---|\n"
        "| row 1a | row 1b |\n"
        "| row 2a | row 2b |\n"
        "| row 3a | row 3b |\n\n"
        "**Row count: 3.**\n"
    ))
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_row_count_arithmetic(docs, tmp_path)
    assert result["status"] == "PASS", result["findings"]


def test_adv_check_4_row_count_arithmetic_fails_for_wrong_count(tmp_path: Path) -> None:
    """Adversarial Check 4: claimed count of 5 but table only has 3 rows."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(tmp_path, "01_plan.md", (
        "| Col A | Col B |\n"
        "|---|---|\n"
        "| row 1a | row 1b |\n"
        "| row 2a | row 2b |\n"
        "| row 3a | row 3b |\n\n"
        "**Row count: 5.**\n"
    ))
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_row_count_arithmetic(docs, tmp_path)
    assert result["status"] == "FAIL"
    assert any(f["actual"] == 3 for f in result["findings"] if "actual" in f)


# ---------------------------------------------------------------------------
# Check 5 — HASH-PIN
# ---------------------------------------------------------------------------


def test_det_check_5_hash_pin_records_hashes(tmp_path: Path) -> None:
    """Check 5 always PASSes (records hashes); verify hashes are SHA-3-512."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(tmp_path, "01_plan.md", "Hello, GPP.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_hash_pin(docs, tmp_path)
    assert result["status"] == "PASS"
    rel_key = "01_plan.md"
    hashes = result["hashes"]
    assert any(k.endswith("01_plan.md") for k in hashes)
    # Verify the hash is a valid SHA-3-512 hex (128 hex chars)
    for h in hashes.values():
        assert len(h) == 128
        int(h, 16)  # must be valid hex


def test_adv_check_5_hash_pin_hash_is_deterministic(tmp_path: Path) -> None:
    """Adversarial Check 5: same file produces same hash across two calls."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(tmp_path, "01_plan.md", "Deterministic content.\n")
    docs = {plan_doc: plan_doc.read_text()}
    r1 = gpp_det.check_hash_pin(docs, tmp_path)
    r2 = gpp_det.check_hash_pin(docs, tmp_path)
    assert r1["hashes"] == r2["hashes"]


# ---------------------------------------------------------------------------
# Check 6 — INDEX-STALE-DRYRUN
# ---------------------------------------------------------------------------


def test_det_check_6_index_stale_dryrun_passes_for_non_0_5_docs(tmp_path: Path) -> None:
    """Check 6 PASS: doc with no §0.5 / Interface Index reference has no advisory."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(tmp_path, "01_plain.md", "Just a plan with no index references.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_index_stale_dryrun(docs, tmp_path)
    assert result["status"] == "PASS"
    assert result["advisories"] == []


def test_adv_check_6_index_stale_dryrun_flags_missing_fields_without_to_be_pinned(
    tmp_path: Path,
) -> None:
    """Adversarial Check 6: doc references §0.5 but omits required fields → advisory."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "This plan proposes new §0.5 Interface Index rows for the new mechanism.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_index_stale_dryrun(docs, tmp_path)
    assert result["status"] == "PASS"  # advisories are not failures
    assert len(result["advisories"]) >= 1
    adv = result["advisories"][0]
    assert "missing_fields" in adv


# ---------------------------------------------------------------------------
# Check 7 — FAMILY-TAXONOMY
# ---------------------------------------------------------------------------


def test_det_check_7_family_taxonomy_passes_when_claim_matches(tmp_path: Path) -> None:
    """Check 7 PASS: 'seven distinct families' claim matches router.yaml."""
    _make_router(tmp_path)
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "Family taxonomy is frozen at seven distinct provider families.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_family_taxonomy(docs, tmp_path)
    # Router above has 7 families (Anthropic, Google, OpenAI, OpenAI-OSS,
    # Alibaba, Meta, Moonshot) — 'seven' claim should match.
    assert result["status"] == "PASS", f"families={result['router_family_list']}, {result['findings']}"


def test_adv_check_7_family_taxonomy_fails_for_wrong_count(tmp_path: Path) -> None:
    """Adversarial Check 7: claiming 'eight distinct families' when router has 7.

    The FAMILY_CLAIM regex covers five|6|seven|8 etc.  We use 'eight' (8) so
    the regex matches and the actual family count (7) causes a FAIL.
    """
    _make_router(tmp_path)
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "The taxonomy has eight distinct provider families in the router.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_family_taxonomy(docs, tmp_path)
    assert result["status"] == "FAIL"
    assert any(f["claimed_families"] == 8 for f in result["findings"])


# ---------------------------------------------------------------------------
# Check 8 — SCOPE-FREEZE-BACKDOOR-FLAG
# ---------------------------------------------------------------------------


def test_det_check_8_scope_freeze_backdoor_flags_known_phrases(tmp_path: Path) -> None:
    """Check 8 FLAG: known backdoor phrases are flagged (not failed)."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "Item can proceed via pre-authorized reshape if operator signs.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_scope_freeze_backdoor(docs, tmp_path)
    assert result["status"] == "FLAG"
    assert len(result["flags"]) >= 1
    # DET tier does NOT fail; failure code is None
    assert result["failure_code"] is None


def test_adv_check_8_scope_freeze_backdoor_passes_for_clean_plan(tmp_path: Path) -> None:
    """Adversarial Check 8: a clean plan with no backdoor phrases → PASS."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "The scope is fixed per 01_scope_pin.md.  No reshape clauses.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_scope_freeze_backdoor(docs, tmp_path)
    assert result["status"] == "PASS"
    assert result["flags"] == []


# ---------------------------------------------------------------------------
# Check 9 — VERSION-SKEW-DISCLOSURE
# ---------------------------------------------------------------------------


def test_det_check_9_version_skew_disclosure_passes_without_skew(tmp_path: Path) -> None:
    """Check 9 PASS: doc references only v7 (no v6-r2 proximity) → no disclosure needed."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "All amendments target v7 architecture.  No v6 references.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_version_skew_disclosure(docs, tmp_path)
    assert result["status"] == "PASS"


def test_adv_check_9_version_skew_disclosure_fails_without_heading(tmp_path: Path) -> None:
    """Adversarial Check 9: doc has v6-r2 + v7 proximity but no disclosure heading."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "Prior work used v6-r2 architecture.  Now we target v7 LOCKED.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_version_skew_disclosure(docs, tmp_path)
    assert result["status"] == "FAIL"
    assert result["failure_code"] == "F-GPP-VERSION-SKEW-UNDISCLOSED"


# ---------------------------------------------------------------------------
# Check 10 — BLOCKER-CARRY-CHECK
# ---------------------------------------------------------------------------


def test_det_check_10_blocker_carry_passes_with_no_predecessors(tmp_path: Path) -> None:
    """Check 10 PASS: no predecessor existence audits → nothing to carry."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(tmp_path, "01_plan.md", "Fresh plan with no predecessors.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_blocker_carry(docs, tmp_path, tmp_path)
    assert result["status"] == "PASS"
    assert "no predecessor" in result.get("note", "")


def test_adv_check_10_blocker_carry_fails_for_uncarried_blocker(tmp_path: Path) -> None:
    """Adversarial Check 10: predecessor audit has a blocker absent from current plan.

    The check skips audits inside plan_dir itself, so plan_dir must be a
    subdirectory of the repo root — NOT the root itself.
    """
    # repo_root has router.yaml; plan_dir is a subdirectory
    repo_root = tmp_path
    (repo_root / "router.yaml").touch()

    # Predecessor plan dir with an existence_audit naming a blocker
    pred_dir = repo_root / "pipeline" / "validation" / "predecessor_2026-04-01"
    pred_dir.mkdir(parents=True)
    (pred_dir / "existence_audit.md").write_text(
        "| missing_module_xyz | PROPOSED-NOT-EXISTS | Needed for feature Q |\n"
    )

    # Current plan dir is a DIFFERENT subdir (not an ancestor of predecessor)
    current_dir = repo_root / "pipeline" / "validation" / "current_2026-04-19"
    current_dir.mkdir(parents=True)
    current_plan = _make_plan_doc(
        current_dir, "01_current_plan.md",
        "This plan does not mention the predecessor blocker at all.\n"
    )
    docs = {current_plan: current_plan.read_text()}
    result = gpp_det.check_blocker_carry(docs, current_dir, repo_root)
    assert result["status"] == "FAIL", (
        f"Expected FAIL (uncarried blocker 'missing_module_xyz'); got: {result}"
    )
    assert result["failure_code"] == "F-GPP-BLOCKER-UNCARRIED"


# ===========================================================================
# Bug-fix specific tests (Phase 0 named tests)
# ===========================================================================

# ---------------------------------------------------------------------------
# Bug 1 — FAMILY-TAXONOMY: skip non-model-shaped strings in router.yaml walk
# ---------------------------------------------------------------------------


def test_det_family_taxonomy_skips_non_model_keys(tmp_path: Path) -> None:
    """Bug-1 regression test: code_findings_path does NOT produce UNCLASSIFIED row.

    router.yaml has:
      code_findings_path: pipeline/validation/code_reviews/<round-id>/
      code_merge_rule: all_pass
      code_dashboard_post: batch

    After the fix these must NOT appear in the family list — only real
    provider/model-name strings should be classified.
    """
    _make_router(tmp_path)  # includes code_findings_path + code_merge_rule
    plan_doc = _make_plan_doc(tmp_path, "01_plan.md", "No families claim here.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_family_taxonomy(docs, tmp_path)
    family_list = result.get("router_family_list", [])
    # No UNCLASSIFIED entry — every string must be from FAMILY_MAP_RULES
    unclassified = [f for f in family_list if "UNCLASSIFIED" in str(f)]
    assert unclassified == [], f"Unexpected UNCLASSIFIED entries: {unclassified}"
    # Must be exactly the 7 canonical families
    assert len(family_list) == 7, f"Expected 7 families, got {len(family_list)}: {family_list}"


def test_det_family_taxonomy_is_model_shaped_helper() -> None:
    """Unit-test the _is_model_shaped helper directly."""
    assert gpp_det._is_model_shaped("anthropic/claude-sonnet-4-6") is True
    assert gpp_det._is_model_shaped("groq/qwen/qwen3-32b") is True
    assert gpp_det._is_model_shaped("google/gemini-2.5-pro") is True
    assert gpp_det._is_model_shaped("meta/llama-3.3-70b") is True
    assert gpp_det._is_model_shaped("pipeline/validation/code_reviews/<round-id>/") is False
    assert gpp_det._is_model_shaped("all_pass") is False
    assert gpp_det._is_model_shaped("batch") is False
    assert gpp_det._is_model_shaped("openai/<placeholder>") is False  # has <>


# ---------------------------------------------------------------------------
# Bug 2 — VERSION-RESOLVE: treat TARGET-LOCK wording as pending
# ---------------------------------------------------------------------------


def test_det_version_resolve_treats_target_wording_as_pending(tmp_path: Path) -> None:
    """Bug-2 regression test: TARGET-LOCK context causes LOCKED claim to be skipped.

    A plan that says:
      'amendment_v2.3 TARGET-LOCK: 2026-04-25 is the goal for §4 v2.3 LOCKED
       at round close'
    must PASS VERSION-RESOLVE even when §4 v2.3 is not yet on disk.
    """
    (tmp_path / "router.yaml").touch()
    (tmp_path / "pipeline" / "blueprint" / "v0.1").mkdir(parents=True)
    sec4 = tmp_path / "pipeline" / "blueprint" / "v0.1" / "section_04_logician.md"
    # v2.1 is LOCKED — v2.3 is NOT on disk yet
    sec4.write_text("# Section 4 Logician v2.1\n\nLOCKED 2026-04-18\n")

    plan_doc = _make_plan_doc(
        tmp_path, "04_dispatch_plan.md",
        # TARGET-LOCK context is within 150 chars of 'LOCKED'
        "Round goal: amendment_v2.3 TARGET-LOCK: 2026-04-25.\n"
        "Output on LOCK: §4 v2.3 LOCKED manifest + paired §0.5 commit.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_version_resolve(docs, tmp_path)
    assert result["status"] == "PASS", (
        f"Expected PASS but got FAIL: {result['findings']}"
    )


def test_det_version_resolve_version_wording_discipline_in_front_matter(tmp_path: Path) -> None:
    """Bug-2 regression: front-matter version_wording_discipline causes ALL claims to be skipped."""
    (tmp_path / "router.yaml").touch()
    (tmp_path / "pipeline" / "blueprint" / "v0.1").mkdir(parents=True)
    sec4 = tmp_path / "pipeline" / "blueprint" / "v0.1" / "section_04_logician.md"
    sec4.write_text("# Section 4 Logician v2.1\n\nLOCKED 2026-04-18\n")

    plan_doc = _make_plan_doc(
        tmp_path, "03_amendment_plan.md",
        "---\n"
        "version_wording_discipline: LOCKED = output of round, not current state.\n"
        "---\n\n"
        "§4 v2.3 LOCKED is what the round produces.\n"
        "§4 v2.5 LOCKED is the runtime-integrity target.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_version_resolve(docs, tmp_path)
    assert result["status"] == "PASS", result["findings"]


def test_adv_version_resolve_current_state_claim_still_validated(tmp_path: Path) -> None:
    """Adversarial Bug-2: a plain 'LOCKED' claim with no TARGET context IS validated."""
    (tmp_path / "router.yaml").touch()
    (tmp_path / "pipeline" / "blueprint" / "v0.1").mkdir(parents=True)
    sec4 = tmp_path / "pipeline" / "blueprint" / "v0.1" / "section_04_logician.md"
    sec4.write_text("# Section 4 Logician v2.1\n\nLOCKED 2026-04-18\n")

    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "We depend on §4 v99.0 LOCKED as the current foundation.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_version_resolve(docs, tmp_path)
    # v99.0 not in sec4's first 120 lines; should FAIL
    assert result["status"] == "FAIL"


# ---------------------------------------------------------------------------
# Bug 3 — CITE-RESOLVE: skip documented template glob patterns
# ---------------------------------------------------------------------------


def test_det_cite_skips_documented_template_globs(tmp_path: Path) -> None:
    """Bug-3 regression test: pipeline/<...>.yaml references in CITE_EXCLUDE_PATTERNS
    are ignored by CITE-RESOLVE.

    The spec text uses `pipeline/...md` and `pipeline/...yaml` as documentation
    examples in §3.  These must not trigger F-GPP-CITATION-UNRESOLVED.
    """
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(
        tmp_path, "gpp_spec_v1.md",
        "## §3 — Check descriptions\n\n"
        "Check 1 verifies every `pipeline/...md` or `pipeline/...yaml` path.\n"
        "Use `pipeline/<plan-dir>/gpp_det.py` as the entrypoint.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_cite_resolve(docs, tmp_path)
    assert result["status"] == "PASS", (
        f"Expected PASS but found: {result['findings']}"
    )


def test_det_cite_exclude_patterns_ellipsis() -> None:
    """Unit-test CITE_EXCLUDE_PATTERNS rejects ellipsis-placeholder paths."""
    has_ellipsis = any(p.search("pipeline/...md") for p in gpp_det.CITE_EXCLUDE_PATTERNS)
    assert has_ellipsis, "CITE_EXCLUDE_PATTERNS must reject 'pipeline/...md'"

    has_yaml = any(p.search("pipeline/...yaml") for p in gpp_det.CITE_EXCLUDE_PATTERNS)
    assert has_yaml, "CITE_EXCLUDE_PATTERNS must reject 'pipeline/...yaml'"


def test_det_cite_future_lock_citations_from_front_matter_are_excluded(tmp_path: Path) -> None:
    """Bug-3 regression: future_lock_citations in front-matter suppresses CITE failure."""
    (tmp_path / "router.yaml").touch()
    # section_04a_canary_harness.md is intentionally not on disk
    plan_doc = _make_plan_doc(
        tmp_path, "03_amendment_plan.md",
        "---\n"
        "future_lock_citations:\n"
        "  - pipeline/blueprint/v0.1/section_04a_canary_harness.md\n"
        "---\n\n"
        "The new harness will live at "
        "pipeline/blueprint/v0.1/section_04a_canary_harness.md\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_cite_resolve(docs, tmp_path)
    # The future citation should be suppressed — no findings for that path
    missing = [
        f for f in result.get("findings", [])
        if "section_04a_canary_harness" in f["cite"]
    ]
    assert missing == [], f"Future-lock cite should be suppressed: {missing}"


def test_adv_cite_resolve_still_catches_genuinely_missing_file(tmp_path: Path) -> None:
    """Adversarial Bug-3: a real citation to a missing file still fails."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "Depends on pipeline/blueprint/v0.1/section_99_missing.md.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_cite_resolve(docs, tmp_path)
    assert result["status"] == "FAIL"
    assert any("section_99_missing" in f["cite"] for f in result["findings"])


# ===========================================================================
# New tool tests
# ===========================================================================

# ---------------------------------------------------------------------------
# test_council_dispatch_emits_red_team_and_reasoner_unconditionally
# ---------------------------------------------------------------------------


def test_council_dispatch_emits_red_team_and_reasoner_unconditionally(
    plan_dir_with_router: Path,
) -> None:
    """Tier 2 is unconditional: BOTH red_team and reasoner_review are always dispatched.

    This test covers the case where Check 8 has ZERO flags (no scope-freeze
    backdoor phrases) — Tier 2 still dispatches both seats.

    gpp_spec_v1.md §3.2: 'A plan with zero Check 8 flags still requires
    Tier 2 invocation.'
    """
    plan_dir = plan_dir_with_router
    # Create a clean plan doc with NO Check 8 flags
    plan_doc = _make_plan_doc(
        plan_dir, "01_scope.md",
        "Clean plan.  No scope-widening language.  Families: seven.\n"
    )
    # Minimal DET report (no Check 8 flags, Tier 1 PASS)
    det_report: dict[str, Any] = {
        "tier_1_overall_status": "PASS",
        "plan_sub_docs": [str(plan_doc)],
        "checks": [
            {"check_id": "SCOPE-FREEZE-BACKDOOR-FLAG", "status": "PASS", "flags": []},
        ],
    }

    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir,
        [str(plan_doc)],
        det_report,
        gpp_council_dispatch.load_router(plan_dir),
    )

    assert len(payloads) == 2, (
        f"Expected exactly 2 payloads (red_team + reasoner_review), got {len(payloads)}"
    )
    seats = {p["seat"] for p in payloads}
    assert "red_team" in seats, "red_team payload missing"
    assert "reasoner_review" in seats, "reasoner_review payload missing"


def test_council_dispatch_unconditional_even_with_check8_flags(
    plan_dir_with_router: Path,
) -> None:
    """Tier 2 dispatches ALSO when Check 8 has flags — not just when clean."""
    plan_dir = plan_dir_with_router
    plan_doc = _make_plan_doc(plan_dir, "01_scope.md", "Uses pre-authorized reshape.\n")
    det_report: dict[str, Any] = {
        "tier_1_overall_status": "PASS",
        "plan_sub_docs": [str(plan_doc)],
        "checks": [
            {
                "check_id": "SCOPE-FREEZE-BACKDOOR-FLAG",
                "status": "FLAG",
                "flags": [{"phrase": "pre-authorized reshape", "severity": "FLAG"}],
            },
        ],
    }
    payloads = gpp_council_dispatch.build_council_payloads(
        plan_dir,
        [str(plan_doc)],
        det_report,
        gpp_council_dispatch.load_router(plan_dir),
    )
    assert len(payloads) == 2
    seats = {p["seat"] for p in payloads}
    assert seats == {"red_team", "reasoner_review"}


def test_council_dispatch_dry_run_writes_stub_output(
    plan_dir_with_router: Path,
) -> None:
    """run_council_dispatch in dry_run mode writes council_findings_*.json."""
    plan_dir = plan_dir_with_router
    _make_plan_doc(plan_dir, "01_scope.md", "Scope pin.\n")
    # Write a minimal DET report so run_council_dispatch finds it
    gpp_dir = plan_dir / "gpp"
    gpp_dir.mkdir(exist_ok=True)
    det_report = {
        "tier_1_overall_status": "PASS",
        "plan_sub_docs": ["01_scope.md"],
        "checks": [],
    }
    import datetime as dt
    date_stamp = dt.date.today().isoformat()
    (gpp_dir / f"gpp_det_report_{date_stamp}.json").write_text(
        json.dumps(det_report), encoding="utf-8"
    )
    result = gpp_council_dispatch.run_council_dispatch(plan_dir, dry_run=True)
    assert result.get("exit_code") == 0, result
    assert result["dispatch_mode"] in ("dry_run",)
    assert len(result["payloads_dispatched"]) == 2


# ---------------------------------------------------------------------------
# test_manifest_roundtrip_ed25519_and_ml_dsa_65
# ---------------------------------------------------------------------------


def test_manifest_roundtrip_ed25519_and_ml_dsa_65(tmp_path: Path) -> None:
    """Tier 3 signed manifest verifies under BOTH Ed25519 AND ML-DSA-65.

    Phase-0 ML-DSA-65 uses HMAC-SHA3-512 stub (oqs not yet installed).
    Both primitives must round-trip: sign → verify → True.
    """
    keypair = gpp_manifest.GPPKeypair.generate()

    manifest_data = gpp_manifest.build_manifest(
        plan_artifact_paths=[],  # no actual files needed for unit test
        repo_root=tmp_path,
        det_report={"tier_1_overall_status": "PASS", "checks": []},
        council_findings=[],
        tier_3_dispositions=[],
    )
    signed = gpp_manifest.sign_manifest(manifest_data, keypair)
    result = gpp_manifest.verify_manifest(signed)

    assert result["ed25519_valid"], f"Ed25519 verification failed: {result['errors']}"
    assert result["ml_dsa_65_valid"], f"ML-DSA-65 verification failed: {result['errors']}"
    assert result["both_valid"], f"Both-valid check failed: {result}"
    assert result["freshness_ok"], "Freshness check failed on a just-signed manifest"


def test_manifest_ed25519_detects_tampered_content(tmp_path: Path) -> None:
    """Adversarial: altering manifest body after signing invalidates Ed25519."""
    keypair = gpp_manifest.GPPKeypair.generate()
    manifest_data = gpp_manifest.build_manifest(
        plan_artifact_paths=[], repo_root=tmp_path,
        det_report={"tier_1_overall_status": "PASS", "checks": []},
        council_findings=[], tier_3_dispositions=[],
    )
    signed = gpp_manifest.sign_manifest(manifest_data, keypair)
    # Tamper
    tampered = dict(signed)
    tampered["tier_1_det_results"] = {"FAKE_CHECK": "PASS"}
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ed25519_valid"], "Ed25519 should fail on tampered manifest"


def test_manifest_ml_dsa_65_detects_tampered_content(tmp_path: Path) -> None:
    """Adversarial: altering manifest body after signing invalidates ML-DSA-65."""
    keypair = gpp_manifest.GPPKeypair.generate()
    manifest_data = gpp_manifest.build_manifest(
        plan_artifact_paths=[], repo_root=tmp_path,
        det_report={"tier_1_overall_status": "PASS", "checks": []},
        council_findings=[], tier_3_dispositions=[],
    )
    signed = gpp_manifest.sign_manifest(manifest_data, keypair)
    tampered = dict(signed)
    tampered["gpp_spec_version"] = "v99"
    result = gpp_manifest.verify_manifest(tampered)
    assert not result["ml_dsa_65_valid"], "ML-DSA-65 should fail on tampered manifest"


def test_manifest_freshness_check_fails_for_old_manifest(tmp_path: Path) -> None:
    """Freshness criterion 5: signed_at > 90 days ago → freshness_ok=False."""
    keypair = gpp_manifest.GPPKeypair.generate()
    manifest_data = gpp_manifest.build_manifest(
        plan_artifact_paths=[], repo_root=tmp_path,
        det_report={"tier_1_overall_status": "PASS", "checks": []},
        council_findings=[], tier_3_dispositions=[],
    )
    signed = gpp_manifest.sign_manifest(manifest_data, keypair)
    # Back-date signed_at by 100 days
    import datetime as dt
    old_ts = (
        dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=100)
    ).isoformat()
    signed["signed_at"] = old_ts
    result = gpp_manifest.verify_manifest(signed)
    assert not result["freshness_ok"]


# ---------------------------------------------------------------------------
# Full orchestrator smoke test (uses real plan dir)
# ---------------------------------------------------------------------------


def test_run_gpp_det_on_real_plan_dir_passes() -> None:
    """Integration: run the full 10-check suite on the live scope-close plan dir.

    This test asserts the fixed gpp_det.py produces an overall PASS on the
    integration_scope_close_2026-04-19 plan directory (the bootstrap run).
    The 12 SCOPE-FREEZE-BACKDOOR FLAGs are expected and do not cause FAIL.
    """
    plan_dir = (
        Path(__file__).resolve().parent.parent.parent
        / "pipeline"
        / "validation"
        / "integration_scope_close_2026-04-19"
    )
    assert plan_dir.is_dir(), f"Plan dir not found: {plan_dir}"
    report = gpp_det.run_gpp_det(plan_dir)
    assert "error" not in report, report.get("error")
    assert report["tier_1_overall_status"] == "PASS", (
        "Expected PASS on real plan dir; failing checks: "
        + str([c for c in report["checks"] if c["status"] == "FAIL"])
    )


# ===========================================================================
# Coverage gap closers — Phase 0 supplement (targeting ≥95% on gpp_det.py)
# ===========================================================================

# ---------------------------------------------------------------------------
# find_repo_root — RuntimeError branch (line 80)
# ---------------------------------------------------------------------------


def test_find_repo_root_raises_when_no_router_yaml(tmp_path: Path) -> None:
    """find_repo_root raises RuntimeError when no router.yaml exists above start."""
    subdir = tmp_path / "a" / "b" / "c"
    subdir.mkdir(parents=True)
    with pytest.raises(RuntimeError, match="router.yaml"):
        gpp_det.find_repo_root(subdir)


# ---------------------------------------------------------------------------
# classify_family — UNCLASSIFIED branch (line 583)
# ---------------------------------------------------------------------------


def test_classify_family_returns_unclassified_for_unknown_provider() -> None:
    """classify_family returns UNCLASSIFIED(...) for a model string matching no rule."""
    result = gpp_det.classify_family("unknownprovider/model-xyz")
    assert result.startswith("UNCLASSIFIED"), f"Expected UNCLASSIFIED prefix, got: {result}"
    assert "unknownprovider/model-xyz" in result


# ---------------------------------------------------------------------------
# classify_family — regression: OpenAI direct-API gpt-N slug coverage
# (2026-04-20 classifier drift patch: `openai/gpt-5.1` escalation slug
# was added to router.yaml but the classifier regex `gpt-4|gpt-3` did
# not match, inflating FAMILY-TAXONOMY count from 7 to 8.)
# ---------------------------------------------------------------------------


def test_classify_family_matches_openai_gpt_5_1() -> None:
    """Red test: `openai/gpt-5.1` must classify as OpenAI, not UNCLASSIFIED.

    Root cause before fix: regex `^openai/(codex|gpt-4|gpt-3|o\\d)` did not
    cover gpt-5 / gpt-N for N>=5. Fix generalizes to `gpt-\\d` so current
    and future direct-API gpt-N slugs (5, 5.1, 6, …) all match OpenAI.
    """
    assert gpp_det.classify_family("openai/gpt-5.1") == "OpenAI"
    # Future-proofing: any gpt-N for N in 3..9 should also match.
    for slug in ("openai/gpt-3.5", "openai/gpt-4", "openai/gpt-5", "openai/gpt-6"):
        assert gpp_det.classify_family(slug) == "OpenAI", slug
    # Existing coverage preserved.
    assert gpp_det.classify_family("openai/codex") == "OpenAI"
    assert gpp_det.classify_family("openai/o1") == "OpenAI"
    assert gpp_det.classify_family("openai/o3") == "OpenAI"


def test_adv_openai_oss_still_wins_over_openai_rule() -> None:
    """Adversarial: generalized `openai/gpt-\\d` must NOT cannibalize OpenAI-OSS.

    `groq/openai/gpt-oss-120b` is routed through Groq and must classify as
    OpenAI-OSS (line 563 rule matches substring `gpt-oss` or `openai_oss`).
    The OpenAI rule is anchored with `^openai/` so a `groq/openai/…` prefix
    cannot match it — but this test guards the anchor against future drift.
    """
    assert gpp_det.classify_family("groq/openai/gpt-oss-120b") == "OpenAI-OSS"
    assert gpp_det.classify_family("groq/openai/gpt-oss-20b") == "OpenAI-OSS"
    assert gpp_det.classify_family("openai_oss/gpt-oss-120b") == "OpenAI-OSS"
    # Direct openai/ hosted gpt-oss (hypothetical) — gpt-oss substring wins
    # because FAMILY_MAP_RULES evaluates the OpenAI rule first but the OpenAI
    # rule's alternation is `codex|gpt-\\d|o\\d`, and `gpt-oss` has no digit
    # after `gpt-`, so it falls through to the OpenAI-OSS rule.
    assert gpp_det.classify_family("openai/gpt-oss-experimental") == "OpenAI-OSS"


# ---------------------------------------------------------------------------
# load_router_families — error branches (lines 589, 591)
# ---------------------------------------------------------------------------


def test_load_router_families_missing_router_yaml(tmp_path: Path) -> None:
    """load_router_families returns error dict when router.yaml is absent."""
    result = gpp_det.load_router_families(tmp_path)  # no router.yaml
    assert "error" in result
    assert "router.yaml not found" in result["error"]


def test_load_router_families_yaml_none_monkeypatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """load_router_families returns error dict when yaml module is None (PyYAML absent)."""
    (tmp_path / "router.yaml").write_text("tilth:\n  scout:\n    primary: anthropic/claude\n")
    monkeypatch.setattr(gpp_det, "yaml", None)
    result = gpp_det.load_router_families(tmp_path)
    assert "error" in result
    assert "PyYAML" in result["error"]


# ---------------------------------------------------------------------------
# load_router_families — walk() list branch (lines 609-610)
# ---------------------------------------------------------------------------


def test_load_router_families_walks_list_values(tmp_path: Path) -> None:
    """walk() correctly descends into list values in router.yaml."""
    import yaml as pyyaml

    data = {
        "tilth": {
            "scout": {"primary": "anthropic/claude-sonnet-4-6"},
            # A list nested inside router data
            "some_list": [
                {"primary": "google/gemini-2.5-pro"},
                {"primary": "openai/gpt-4o"},
            ],
        }
    }
    (tmp_path / "router.yaml").write_text(pyyaml.dump(data))
    result = gpp_det.load_router_families(tmp_path)
    assert "error" not in result
    # All three providers should appear
    assert any("anthropic" in m for m in result["models"])
    assert any("google" in m for m in result["models"])
    assert any("openai" in m for m in result["models"])


# ---------------------------------------------------------------------------
# check_family_taxonomy — error-path branch (lines 618-624)
# ---------------------------------------------------------------------------


def test_check_family_taxonomy_fails_when_router_missing(tmp_path: Path) -> None:
    """check_family_taxonomy returns FAIL with F-GPP-FAMILY-TAXONOMY-MISMATCH
    when router.yaml is absent — error from load_router_families propagates."""
    plan_doc = _make_plan_doc(tmp_path, "01_plan.md", "Seven distinct families.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_family_taxonomy(docs, tmp_path)
    assert result["status"] == "FAIL"
    assert result["failure_code"] == "F-GPP-FAMILY-TAXONOMY-MISMATCH"
    assert any("router.yaml" in f["reason"] for f in result["findings"])


# ---------------------------------------------------------------------------
# check_version_resolve — architecture-file branches (lines 295-310)
# ---------------------------------------------------------------------------


def test_version_resolve_section_target_file_missing_fails(tmp_path: Path) -> None:
    """VERSION-RESOLVE FAILs (lines 303-310) when the mapped target file is absent.

    §4 v2.1 LOCKED is claimed, but section_04_logician.md does not exist on disk.
    VERSION_CLAIM regex captures group(1)='§4', group(2)='2.1'.
    SECTION_FILE_MAP routes to section_04_logician.md → not a file → findings.append.
    """
    (tmp_path / "router.yaml").touch()
    # Do NOT create section_04_logician.md — it must be absent to trigger the branch
    (tmp_path / "pipeline" / "blueprint" / "v0.1").mkdir(parents=True)
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "§4 v2.1 LOCKED is the current foundation.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_version_resolve(docs, tmp_path)
    assert result["status"] == "FAIL", f"Expected FAIL (target file missing): {result}"
    assert any("2.1" in f["claim"] for f in result["findings"]), result["findings"]
    assert any("missing" in f["reason"] for f in result["findings"]), result["findings"]


def test_version_resolve_section_file_exists_but_version_absent_fails(tmp_path: Path) -> None:
    """VERSION-RESOLVE FAILs when the target file exists but lacks the claimed version.

    §4 v99.9 LOCKED is claimed; section_04_logician.md only has v2.1.
    Exercises the 'v{version} not found in target's first 120 lines' branch.
    """
    (tmp_path / "router.yaml").touch()
    bp = tmp_path / "pipeline" / "blueprint" / "v0.1"
    bp.mkdir(parents=True)
    (bp / "section_04_logician.md").write_text("# Section 4 Logician v2.1\nLOCKED.\n")
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "§4 v99.9 LOCKED is the current foundation.\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_version_resolve(docs, tmp_path)
    assert result["status"] == "FAIL"
    assert any("99.9" in f["claim"] for f in result["findings"]), result["findings"]


# ---------------------------------------------------------------------------
# check_row_count_arithmetic — no-table branch (lines 391, 424)
# and blank-row skip (line 401)
# ---------------------------------------------------------------------------


def test_row_count_fails_when_no_preceding_table(tmp_path: Path) -> None:
    """ROW-COUNT-ARITHMETIC FAILs when no table exists above the row-count claim."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        "Introduction paragraph.\n\n**Row count: 5.**\n"
    )
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_row_count_arithmetic(docs, tmp_path)
    assert result["status"] == "FAIL"
    assert any("no preceding table" in f["reason"] for f in result["findings"])


def test_count_preceding_table_rows_blank_data_row_skipped() -> None:
    """count_preceding_table_rows skips blank data rows (stripped to empty string)."""
    text = (
        "| Col A | Col B |\n"
        "|---|---|\n"
        "| data 1 | data 1b |\n"
        "|  |  |\n"          # blank row — should be skipped
        "| data 2 | data 2b |\n\n"
        "**Row count: 2.**\n"
    )
    pos = text.index("**Row count")
    actual = gpp_det.count_preceding_table_rows(text, pos)
    # 2 real data rows + 1 blank (skipped) + 1 header (not counted) = 2
    assert actual == 2


def test_count_preceding_table_rows_returns_none_when_no_table() -> None:
    """count_preceding_table_rows returns None when no Markdown table precedes pos."""
    text = "Just text here.\n\n**Row count: 3.**\n"
    pos = text.index("**Row count")
    result = gpp_det.count_preceding_table_rows(text, pos)
    assert result is None


# ---------------------------------------------------------------------------
# collect_plan_docs — council_findings skip (line 860)
# ---------------------------------------------------------------------------


def test_collect_plan_docs_excludes_council_findings(tmp_path: Path) -> None:
    """collect_plan_docs excludes council_findings_*.md from the gpp/ subdir."""
    (tmp_path / "router.yaml").touch()
    gpp_dir = tmp_path / "gpp"
    gpp_dir.mkdir()
    council = gpp_dir / "council_findings_2026-04-19.md"
    council.write_text("# Council Findings\nSeven distinct families.\n")
    spec = gpp_dir / "gpp_spec_v1.md"
    spec.write_text("# GPP Spec\nActual plan content.\n")
    docs = gpp_det.collect_plan_docs(tmp_path)
    assert council not in docs, "council_findings must be excluded from plan docs"
    assert spec in docs, "gpp_spec_v1.md should be included"


# ---------------------------------------------------------------------------
# run_gpp_det — empty-dir error (line 869) and FAIL propagation (lines 889-890)
# ---------------------------------------------------------------------------


def test_run_gpp_det_returns_error_for_empty_plan_dir(tmp_path: Path) -> None:
    """run_gpp_det returns error dict when no .md files exist under plan_dir."""
    (tmp_path / "router.yaml").touch()
    result = gpp_det.run_gpp_det(tmp_path)
    assert "error" in result, f"Expected error key; got: {result}"


def test_run_gpp_det_overall_fail_propagates_from_any_check(tmp_path: Path) -> None:
    """run_gpp_det sets tier_1_overall_status=FAIL when any check returns FAIL."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        # Cite a non-existent file → CITE-RESOLVE FAIL
        "See pipeline/blueprint/v0.1/section_99_nonexistent_xyz.md for details.\n"
    )
    result = gpp_det.run_gpp_det(tmp_path)
    assert result["tier_1_overall_status"] == "FAIL", (
        "Expected overall FAIL because a non-existent file is cited"
    )
    fail_checks = [c for c in result["checks"] if c["status"] == "FAIL"]
    assert fail_checks, "At least one check must be FAIL"


# ---------------------------------------------------------------------------
# render_markdown — full coverage (lines 905-953)
# ---------------------------------------------------------------------------


def test_render_markdown_covers_all_sections(tmp_path: Path) -> None:
    """render_markdown produces a well-formed markdown report with all check sections."""
    (tmp_path / "router.yaml").touch()
    _make_router(tmp_path)
    plan_doc = _make_plan_doc(tmp_path, "01_plan.md", "Clean plan.\n")
    report = gpp_det.run_gpp_det(tmp_path)
    md = gpp_det.render_markdown(report)
    # Title
    assert "# GPP-DET Report" in md
    # Metadata fields
    assert "Tool version:" in md
    assert "Spec version:" in md
    assert "Run at (UTC):" in md
    assert "Tier 1 overall status:" in md
    # All 10 check IDs should appear
    for check_id in (
        "CITE-RESOLVE",
        "VERSION-RESOLVE",
        "XDOC-REF",
        "ROW-COUNT-ARITHMETIC",
        "HASH-PIN",
        "INDEX-STALE-DRYRUN",
        "FAMILY-TAXONOMY",
        "SCOPE-FREEZE-BACKDOOR",
        "VERSION-SKEW-DISCLOSURE",
        "BLOCKER-CARRY-CHECK",
    ):
        assert check_id in md, f"Missing check section: {check_id}"


def test_render_markdown_includes_findings_and_flags(tmp_path: Path) -> None:
    """render_markdown includes Findings and Flags subsections when they are non-empty."""
    (tmp_path / "router.yaml").touch()
    plan_doc = _make_plan_doc(
        tmp_path, "01_plan.md",
        # Trigger Check 1 FAIL (missing cite) + Check 8 FLAG (backdoor phrase)
        "See pipeline/blueprint/v0.1/totally_missing.md.\n"
        "Option can proceed via pre-authorized reshape if approved.\n"
    )
    report = gpp_det.run_gpp_det(tmp_path)
    md = gpp_det.render_markdown(report)
    assert "### Findings" in md
    assert "### Flags" in md


def test_render_markdown_extra_diagnostics_appear(tmp_path: Path) -> None:
    """render_markdown emits extra diagnostic keys (hashes, router_family_list, etc.)."""
    (tmp_path / "router.yaml").touch()
    _make_router(tmp_path)
    plan_doc = _make_plan_doc(tmp_path, "01_plan.md", "Clean plan.\n")
    report = gpp_det.run_gpp_det(tmp_path)
    md = gpp_det.render_markdown(report)
    # hashes appear in HASH-PIN section; router_family_list in FAMILY-TAXONOMY
    assert "hashes" in md
    assert "router_family_list" in md


# ---------------------------------------------------------------------------
# main() — entry-point coverage (lines 957-978)
# ---------------------------------------------------------------------------


def test_main_creates_report_files_and_returns_0_for_pass(tmp_path: Path) -> None:
    """main() writes gpp_det_report_*.json + *.md and exits 0 when overall PASS."""
    (tmp_path / "router.yaml").touch()
    _make_router(tmp_path)
    _make_plan_doc(tmp_path, "01_plan.md", "Clean plan with no problematic citations.\n")
    ret = gpp_det.main(["gpp_det.py", str(tmp_path)])
    assert ret == 0
    gpp_subdir = tmp_path / "gpp"
    assert gpp_subdir.is_dir()
    assert any(gpp_subdir.glob("gpp_det_report_*.json")), "JSON report missing"
    assert any(gpp_subdir.glob("gpp_det_report_*.md")), "Markdown report missing"


def test_main_returns_1_for_overall_fail(tmp_path: Path) -> None:
    """main() returns 1 when the DET run produces overall FAIL."""
    (tmp_path / "router.yaml").touch()
    _make_plan_doc(
        tmp_path, "01_plan.md",
        "Depends on pipeline/blueprint/v0.1/totally_missing_file_xyz.md.\n"
    )
    ret = gpp_det.main(["gpp_det.py", str(tmp_path)])
    assert ret == 1


def test_main_returns_2_for_no_arguments() -> None:
    """main() returns 2 (usage error) when called with no plan-dir argument."""
    ret = gpp_det.main(["gpp_det.py"])
    assert ret == 2


def test_main_returns_2_for_nonexistent_directory() -> None:
    """main() returns 2 when the provided path is not a directory."""
    ret = gpp_det.main(["gpp_det.py", "/no/such/path/exists/abc123"])
    assert ret == 2


def test_main_returns_2_for_empty_dir_no_md_files(tmp_path: Path) -> None:
    """main() returns 2 when plan_dir exists but has no .md files (error in report)."""
    (tmp_path / "router.yaml").touch()
    # No .md files → run_gpp_det returns {"error": ...}
    ret = gpp_det.main(["gpp_det.py", str(tmp_path)])
    assert ret == 2


# ---------------------------------------------------------------------------
# BLOCKER-CARRY-CHECK edge cases (lines 764, 767, 769, 776, 814, 818)
# ---------------------------------------------------------------------------


def test_blocker_carry_skips_audit_inside_plan_dir(tmp_path: Path) -> None:
    """existence_audit.md that lives inside plan_dir is excluded from predecessors."""
    repo_root = tmp_path
    (repo_root / "router.yaml").touch()
    plan_dir = repo_root / "pipeline" / "validation" / "current_2026-04-19"
    plan_dir.mkdir(parents=True)
    gpp_sub = plan_dir / "gpp"
    gpp_sub.mkdir()
    # Blocker audit INSIDE plan_dir — must be ignored
    (gpp_sub / "existence_audit.md").write_text(
        "| unique_blocker_abc | PROPOSED-NOT-EXISTS | needed |\n"
    )
    plan_doc = plan_dir / "01_plan.md"
    plan_doc.write_text("This plan does not mention unique_blocker_abc.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_blocker_carry(docs, plan_dir, repo_root)
    # Audit skipped → no predecessors → PASS
    assert result["status"] == "PASS"
    assert "no predecessor" in result.get("note", "")


def test_blocker_carry_skips_audit_with_no_date_in_path(tmp_path: Path) -> None:
    """existence_audit.md in a dir without a date stamp is skipped (line 767 continue)."""
    repo_root = tmp_path
    (repo_root / "router.yaml").touch()
    pred_dir = repo_root / "pipeline" / "validation" / "no_date_here"
    pred_dir.mkdir(parents=True)
    (pred_dir / "existence_audit.md").write_text(
        "| blocker_no_date | PROPOSED-NOT-EXISTS | needed |\n"
    )
    plan_dir = repo_root / "pipeline" / "validation" / "current_2026-04-19"
    plan_dir.mkdir(parents=True)
    plan_doc = plan_dir / "01_plan.md"
    plan_doc.write_text("Nothing relevant here.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_blocker_carry(docs, plan_dir, repo_root)
    assert result["status"] == "PASS"


def test_blocker_carry_skips_audit_with_future_date(tmp_path: Path) -> None:
    """existence_audit.md with date AFTER plan_date is skipped (line 769 continue)."""
    repo_root = tmp_path
    (repo_root / "router.yaml").touch()
    pred_dir = repo_root / "pipeline" / "validation" / "future_2026-12-31"
    pred_dir.mkdir(parents=True)
    (pred_dir / "existence_audit.md").write_text(
        "| future_blocker_xyz | PROPOSED-NOT-EXISTS | tbd |\n"
    )
    plan_dir = repo_root / "pipeline" / "validation" / "current_2026-04-19"
    plan_dir.mkdir(parents=True)
    plan_doc = plan_dir / "01_plan.md"
    plan_doc.write_text("Nothing relevant here.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_blocker_carry(docs, plan_dir, repo_root)
    assert result["status"] == "PASS"


def test_blocker_carry_skips_preflight_audit_inside_plan_dir(tmp_path: Path) -> None:
    """05_preflight_existence_audit.md inside plan_dir is skipped (line 776 continue)."""
    repo_root = tmp_path
    (repo_root / "router.yaml").touch()
    plan_dir = repo_root / "pipeline" / "validation" / "current_2026-04-19"
    plan_dir.mkdir(parents=True)
    # Preflight audit is INSIDE plan_dir — must be excluded
    (plan_dir / "05_preflight_existence_audit.md").write_text(
        "| inside_blocker | PROPOSED-NOT-EXISTS | inside plan |\n"
    )
    plan_doc = plan_dir / "01_plan.md"
    plan_doc.write_text("Does not mention inside_blocker.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_blocker_carry(docs, plan_dir, repo_root)
    assert result["status"] == "PASS"


def test_blocker_carry_skips_blocker_with_only_stopwords(tmp_path: Path) -> None:
    """Blocker mechanism that consists only of stop-words is skipped (lines 814, 818)."""
    repo_root = tmp_path
    (repo_root / "router.yaml").touch()
    pred_dir = repo_root / "pipeline" / "validation" / "pred_2026-04-01"
    pred_dir.mkdir(parents=True)
    # "the or in" — all three words are stop-words in the filter
    (pred_dir / "existence_audit.md").write_text(
        "| the or in | PROPOSED-NOT-EXISTS | generic |\n"
    )
    plan_dir = repo_root / "pipeline" / "validation" / "current_2026-04-19"
    plan_dir.mkdir(parents=True)
    plan_doc = plan_dir / "01_plan.md"
    plan_doc.write_text("Fresh plan with no specific mechanism references.\n")
    docs = {plan_doc: plan_doc.read_text()}
    result = gpp_det.check_blocker_carry(docs, plan_dir, repo_root)
    # All keywords filtered out → blocker skipped → PASS
    assert result["status"] == "PASS"
