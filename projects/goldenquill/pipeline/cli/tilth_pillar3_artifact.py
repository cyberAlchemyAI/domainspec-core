"""``tilth pillar3 artifact`` — FID Pillar-3 structured-artifact CLI.

Authority
---------
Quality spec: ``docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md`` §3.
Planning authority:
``pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md``
§9.1 (Phase 1, weeks 4-5).

Scope
-----
This CLI scaffolds and signs the per-artifact YAML files Tilth's seats
read at runtime. It does **not** perform extraction (that's the LLM-driven
workflow the operator runs out-of-band under Local-Only-Sovereign posture
once Pillar-2 corpus is signed). The CLI's job:

* ``init`` — verify dependencies (signed Pillar-1 charter + signed
  Pillar-2 corpus), scaffold a YAML stub for the named artifact_id under
  the correct family directory.
* ``status`` — surface per-artifact lifecycle (stub / draft / audited /
  field_tested / validated), dependency state (charter signed? corpus
  signed?), file presence.
* ``sign`` — delegate to ``sign_artifact.py`` for the operator Ed25519
  ceremony.

NOT in this CLI (intentional, follow-up PR):

* ``validate`` — full Pydantic schema enforcement against §3.2 / §3.3 /
  §3.4 structures. Deferred until operator confirms schema details after
  the first Pillar-2 corpus is signed. The infrastructure is staged here
  so the follow-up has a clean home to land in.
* LLM extraction driver — operator runs extraction sessions via openclaw
  bridge under Local-Only-Sovereign posture; output is hand-curated into
  the artifact YAML.

Postures
--------
Local-Only-Sovereign only. No cloud routing. No frontier model calls.
No HTTP egress.

CC-007 / Law-5 boundary
-----------------------
Pure pathlib + yaml + delegation to sign_artifact. No HTTP libraries
imported. AST-lint ``R-NO-DIRECT-PROVIDER-HTTP`` rule covers this.

F-FID-* gates surfaced
-----------------------
* ``F-FID-ARTIFACT-UNSIGNED-CHARTER`` — ``init`` refuses if the named
  artifact's Pillar-1 charter is not signed.
* ``F-FID-ARTIFACT-UNSIGNED-CORPUS`` — ``init`` refuses if the named
  artifact's Pillar-2 corpus is not at ``_signed.yaml`` lifecycle.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys
from typing import Optional, Sequence

try:
    import yaml
except ImportError as e:  # pragma: no cover - imported by tests under venv
    print(f"ERROR: missing dep ({e}); install via `pip install pyyaml`.", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
FID_ROOT = REPO_ROOT / "pipeline" / "funder_intelligence"
CHARTERS_DIR = FID_ROOT / "pillar_1_charters"
P2_ROOT = FID_ROOT / "pillar_2_corpus"
FUNDERS_DIR = FID_ROOT / "funders"
PROGRAMS_DIR = FID_ROOT / "programs"
COMPLIANCE_DIR = FID_ROOT / "compliance_cascades"
PUBKEY_PATH = REPO_ROOT / "vault_shared" / "funder_intelligence" / "publisher_pubkey.signed.yaml"

# The 14 Phase-1 artifact IDs split by family.
PHASE_1_FUNDERS: tuple[str, ...] = (
    "USDA-RD",
    "USDA-NIFA",
    "USDA-AMS",
    "PA-DEPT-AG",
    "PA-DCED",
    "HEINZ-FOUNDATION",
    "NCBA-CLUSA",
    "RICHARD-KING-MELLON-FOUNDATION",
)
PHASE_1_PROGRAMS: tuple[str, ...] = (
    "USDA-AMS-VAPG-FY26",
    "USDA-RD-RBDG-FY26",
    "USDA-RD-RCDG-FY26",
    "USDA-NIFA-SARE-NE-FY26",
    "PA-DEPT-AG-AGINNOV-FY26",
    "USDA-RD-CFP-FY26",
)
PHASE_1_ALL: tuple[str, ...] = PHASE_1_FUNDERS + PHASE_1_PROGRAMS

# Lifecycle states surfaced in MANIFEST tables (per-family).
LIFECYCLE_STUB = "stub"
LIFECYCLE_DRAFT = "draft"
LIFECYCLE_AUDITED = "audited"
LIFECYCLE_FIELD_TESTED = "field_tested"
LIFECYCLE_VALIDATED = "validated"


def family_for(artifact_id: str) -> str:
    if artifact_id in PHASE_1_FUNDERS:
        return "funder"
    if artifact_id in PHASE_1_PROGRAMS:
        return "program"
    raise ValueError(
        f"artifact_id '{artifact_id}' not in Phase-1 roster (funders + programs)."
    )


def family_dir(family: str) -> pathlib.Path:
    return {
        "funder": FUNDERS_DIR,
        "program": PROGRAMS_DIR,
        "compliance_cascade": COMPLIANCE_DIR,
    }[family]


def artifact_yaml_path(artifact_id: str) -> pathlib.Path:
    return family_dir(family_for(artifact_id)) / f"{artifact_id}.yaml"


def signed_charter_path(artifact_id: str) -> pathlib.Path:
    return CHARTERS_DIR / f"{artifact_id}_charter_v1_SIGNED.md"


def signed_corpus_yaml(artifact_id: str) -> pathlib.Path:
    return P2_ROOT / artifact_id / "_signed.yaml"


# ─────────────────────────────────────────────────────────────────────
# Stub template (common header + family-specific scaffolding)
# ─────────────────────────────────────────────────────────────────────

def _common_header_stub(artifact_id: str, family: str) -> dict:
    """Per §3.1 of FID_ARTIFACT_OPTIMIZATION_PRINCIPLES."""
    return {
        "artifact_id": artifact_id,
        "artifact_family": family,
        "artifact_path": f"pipeline/funder_intelligence/{family_dir(family).name}/{artifact_id}.yaml",
        "schema_version": "1.0",
        "lifecycle_status": LIFECYCLE_STUB,
        "classification_default_tier": 1,
        "charter_pointer": f"pipeline/funder_intelligence/pillar_1_charters/{artifact_id}_charter_v1_SIGNED.md",
        "corpus_dir": f"pipeline/funder_intelligence/pillar_2_corpus/{artifact_id}/",
        "publisher_pubkey_path": "vault_shared/funder_intelligence/publisher_pubkey.signed.yaml",
        "publisher_pubkey_fingerprint": "<pending_operator_attestation>",
        "ed25519_signature": "<pending_operator_attestation>",
        "canonical_bytes_sha3_512": "<pending_operator_attestation>",
        "created_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        # The three §2 adversarial blocks — placeholders for operator + extractor.
        "runtime_consumer": {
            "scout": {"reads_fields": [], "stage": "not_applicable", "decision_changed": ""},
            "scribe": {"reads_fields": [], "stage": "not_applicable", "decision_changed": ""},
            "judge": {"reads_fields": [], "stage": "not_applicable", "decision_changed": ""},
            "red_team": {"reads_fields": [], "stage": "not_applicable", "decision_changed": ""},
            "logician": {"reads_fields": [], "stage": "not_applicable", "decision_changed": ""},
        },
        "artifact_must_not_contain": [
            "facts belonging to another artifact",
            "applicant-specific claims",
            "uncited generalizations",
        ],
        "strength_test": [
            "Name one concrete drafting decision this artifact changes.",
            "Name one proposal this artifact would reject or downgrade.",
            "Name one Red Team probe this artifact enables.",
        ],
    }


def _funder_body_stub() -> dict:
    """Per §3.2."""
    return {
        "mission_framing": {
            "one_paragraph_summary": "",
            "corpus_ref": "",
        },
        "program_roster": [],
        "compliance_cascade_defaults": [],
        "funder_dialect": {
            "register": "",
            "load_bearing_terms": [],
            "dialect_notes": "",
        },
        "funder_officer_relationship_notes": [],
        "historical_award_patterns_aggregate": {
            "total_award_volume_fy24": None,
            "total_award_volume_fy25": None,
            "award_count_fy24": None,
            "award_count_fy25": None,
            "geographic_distribution_fy24_25_pa_percent": None,
            "corpus_ref": "",
        },
        "geographic_eligibility": {
            "in_scope_geographies": [],
            "out_of_scope_geographies": [],
            "rural_pop_threshold_default": None,
        },
        "known_failure_modes_at_funder_level": [],
        "refresh_cadence": "annual",
        "last_refreshed_at": "",
        "next_refresh_due_at": "",
    }


def _program_body_stub() -> dict:
    """Per §3.3."""
    return {
        "funder_pointer": "",
        "program_summary_one_paragraph": "",
        "nofo": {
            "source_url": "",
            "source_pdf_sha256": "",
            "posted_date": "",
            "closing_date": "",
            "cycle_status": "",
            "corpus_ref": "",
        },
        "eligibility_gates": [],
        "disqualifiers": [],
        "match_requirements": {
            "required": False,
            "match_ratio": None,
            "match_cash_required_min_pct": None,
            "match_in_kind_allowable": True,
            "match_fund_authenticity_rules": [],
            "match_documentation_required": [],
        },
        "scoring_rubric": {
            "total_points": None,
            "criteria": [],
        },
        "review_stages": [],
        "required_application_elements": [],
        "scout_verify": {
            "live_check_url": "",
            "expected_response_indicator": "",
            "failure_action": "MARK_VERIFICATION_FAILED",
            "check_cadence": "",
        },
        "scribe_section_requirements": [],
        "judge_scoring_map": [],
        "logician_gates": [],
        "red_team_probes": [],
        "post_award_obligations": {
            "reporting_cadence": "",
            "reporting_deliverables": [],
            "beneficiary_metric_tracking_required": False,
            "data_collector_v0_2_inputs": [],
            "audit_obligations": "",
        },
        "known_failure_modes_from_prior_cycles": [],
        "historical_award_patterns": {
            "award_count_prior_cycle": None,
            "award_count_two_cycles_ago": None,
            "median_award_dollars": None,
            "award_size_range": [None, None],
            "pa_specific_award_count_recent": None,
            "corpus_ref": "",
        },
        "refresh_cadence": "per_cycle",
        "last_refreshed_at": "",
        "next_refresh_due_at": "",
    }


def build_artifact_stub(artifact_id: str) -> dict:
    family = family_for(artifact_id)
    stub = _common_header_stub(artifact_id, family)
    if family == "funder":
        stub.update(_funder_body_stub())
    elif family == "program":
        stub.update(_program_body_stub())
    return stub


# ─────────────────────────────────────────────────────────────────────
# Dependency gates
# ─────────────────────────────────────────────────────────────────────

def assert_charter_signed(artifact_id: str) -> pathlib.Path:
    p = signed_charter_path(artifact_id)
    if not p.exists():
        raise FileNotFoundError(
            f"F-FID-ARTIFACT-UNSIGNED-CHARTER: Pillar-1 charter not signed at {p}. "
            f"Run the Pillar-1 sign ceremony first."
        )
    return p


def assert_corpus_signed(artifact_id: str) -> pathlib.Path:
    p = signed_corpus_yaml(artifact_id)
    if not p.exists():
        raise FileNotFoundError(
            f"F-FID-ARTIFACT-UNSIGNED-CORPUS: Pillar-2 corpus not signed at {p}. "
            f"Run the Pillar-2 sign ceremony first."
        )
    return p


# ─────────────────────────────────────────────────────────────────────
# Subcommand handlers
# ─────────────────────────────────────────────────────────────────────

def cmd_init(args: argparse.Namespace) -> int:
    """Scaffold the YAML stub for the named artifact (requires signed deps)."""
    aid = args.artifact_id
    try:
        family = family_for(aid)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if not args.skip_dependency_check:
        try:
            assert_charter_signed(aid)
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        try:
            assert_corpus_signed(aid)
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1

    out_path = artifact_yaml_path(aid)
    if out_path.exists() and not args.force:
        print(
            f"ERROR: artifact YAML already exists at {out_path}. "
            f"Pass --force to overwrite.",
            file=sys.stderr,
        )
        return 1

    stub = build_artifact_stub(aid)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        yaml.safe_dump(stub, sort_keys=True, allow_unicode=True, default_flow_style=False)
    )
    print(f"INIT OK: {out_path}")
    print(f"  family: {family}")
    print(f"  lifecycle_status: {LIFECYCLE_STUB}")
    print(f"  next: operator authors body content from corpus, then run `sign`.")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Surface per-artifact lifecycle state + dependency state."""
    if args.artifact_id:
        targets = [args.artifact_id]
        if args.artifact_id not in PHASE_1_ALL:
            print(f"ERROR: artifact_id '{args.artifact_id}' not in Phase-1 roster.", file=sys.stderr)
            return 1
    else:
        targets = list(PHASE_1_ALL)

    print("=== FID Pillar-3 Artifact Status ===")
    for aid in targets:
        try:
            family = family_for(aid)
        except ValueError:
            print(f"  [SKIP] {aid}: unknown family")
            continue
        charter_ok = signed_charter_path(aid).exists()
        corpus_ok = signed_corpus_yaml(aid).exists()
        yaml_path = artifact_yaml_path(aid)
        if yaml_path.exists():
            try:
                data = yaml.safe_load(yaml_path.read_text()) or {}
                lifecycle = data.get("lifecycle_status", "<unknown>")
            except yaml.YAMLError:
                lifecycle = "<unparseable>"
        else:
            lifecycle = "<not_initialized>"
        c_mark = "C" if charter_ok else "-"
        co_mark = "K" if corpus_ok else "-"
        print(
            f"  {aid:36s}  family={family:8s}  "
            f"deps=[charter:{c_mark} corpus:{co_mark}]  lifecycle={lifecycle}"
        )
    print()
    print("Legend: C=charter SIGNED v1; K=corpus _signed.yaml; '-'=not yet")
    return 0


def cmd_sign(args: argparse.Namespace) -> int:
    """Delegate to sign_artifact helper. Forwards exit code."""
    from pipeline.funder_intelligence._methodology import sign_artifact  # noqa: WPS433
    aid = args.artifact_id
    try:
        family_for(aid)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    yaml_path = artifact_yaml_path(aid)
    if not yaml_path.exists():
        print(
            f"ERROR: artifact YAML not at {yaml_path}. Run `init` first.",
            file=sys.stderr,
        )
        return 1

    forward = [str(yaml_path)]
    if args.dry_run:
        forward.append("--dry-run")
    else:
        if args.signer_pubkey_fingerprint:
            forward += ["--signer-pubkey-fingerprint", args.signer_pubkey_fingerprint]
        if args.signature_hex:
            forward += ["--signature-hex", args.signature_hex]
        if args.signed_at:
            forward += ["--signed-at", args.signed_at]
        if args.allow_missing_pubkey_yaml:
            forward.append("--allow-missing-pubkey-yaml")
    return sign_artifact.main(forward)


# ─────────────────────────────────────────────────────────────────────
# Argparse wiring
# ─────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tilth pillar3 artifact",
        description=(
            "FID Pillar-3 structured-artifact CLI "
            "(Local-Only-Sovereign; init / status / sign; validate deferred)."
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Scaffold a Pillar-3 artifact YAML stub.")
    p_init.add_argument("--artifact-id", required=True)
    p_init.add_argument("--force", action="store_true",
                        help="Overwrite existing YAML.")
    p_init.add_argument("--skip-dependency-check", action="store_true",
                        help="(Debug.) Skip Pillar-1 + Pillar-2 signed-state checks.")
    p_init.set_defaults(func=cmd_init)

    p_status = sub.add_parser("status", help="Per-artifact lifecycle + dependency state.")
    p_status.add_argument("--artifact-id", default=None,
                          help="If omitted, reports the full 14-artifact roster.")
    p_status.set_defaults(func=cmd_status)

    p_sign = sub.add_parser("sign", help="Delegate to sign_artifact helper.")
    p_sign.add_argument("--artifact-id", required=True)
    p_sign.add_argument("--dry-run", action="store_true",
                        help="Print canonical bytes + hash; do not modify files.")
    p_sign.add_argument("--signer-pubkey-fingerprint", default=None)
    p_sign.add_argument("--signature-hex", default=None)
    p_sign.add_argument("--signed-at", default=None)
    p_sign.add_argument("--allow-missing-pubkey-yaml", action="store_true",
                        help="(Testing.) Skip pinned-pubkey verification.")
    p_sign.set_defaults(func=cmd_sign)

    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
