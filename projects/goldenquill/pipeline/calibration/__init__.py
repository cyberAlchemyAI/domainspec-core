"""pipeline.calibration — §4.15 eval-mode calibration primitives (R12.A).

Blueprint §5 v6 LOCKED 2026-04-19 (section_05_pipeline.md):
- §4.15 step 1 path hardening + §5.6 GoldenSetItem (golden_set.py)
- §5.6 CalibrationReport + §5.6.4 canonical-bytes + §4.15 step 7 assemble (report.py)
- §4.15 step 10 Ed25519 sign + verify + freshness + first-write-wins pubkey (signing.py)

R12.A ships the three sub-modules as the standalone primitive surface the
§4.15 eval-mode capstone (R12.B) will compose. All three are
committee-level quality: inline-literal RHS comparisons (V1 discipline),
module-load integrity asserts, E-017 Protocol seams for every external
dependency, Autonomy-Rule-1 save-state-always semantics at every write
surface.

Spec card: ``pipeline/engineering/spec_cards/section_05_round_12_run_eval_pipeline.md``
(R12.A split per ORIENT 2026-04-21).
"""

from __future__ import annotations

from pipeline.calibration.golden_set import (
    BLUEPRINT_DEPS as GOLDEN_SET_BLUEPRINT_DEPS,
)
from pipeline.calibration.golden_set import (
    GOLDEN_SET_SCHEMA_VERSION,
    GOLDEN_SET_VAULT_PREFIX_TMPL,
    GoldenSetItem,
    GoldenSetVaultRead,
    IsSymlinkCallable,
    RealpathCallable,
    _deserialize_manifest,
    _resolve_golden_set_path,
    _vault_prefix_for,
    assert_manifest_org_matches,
    golden_set_iter,
)
from pipeline.calibration.report import (
    BLUEPRINT_DEPS as REPORT_BLUEPRINT_DEPS,
)
from pipeline.calibration.report import (
    AssembleInputs,
    CalibrationReport,
    CalibrationReportItem,
    assemble_from_run,
    calibration_report_field_set,
    calibration_report_item_field_set,
    canonical_bytes,
    canonical_bytes_exclusions,
    compute_canonical_sha256,
    report_from_json,
    report_to_json,
)
from pipeline.calibration.signing import (
    BLUEPRINT_DEPS as SIGNING_BLUEPRINT_DEPS,
)
from pipeline.calibration.signing import (
    CALIBRATION_KEY_PATH_TMPL,
    CALIBRATION_PUBKEY_PROVENANCE_PATH_TMPL,
    CalibrationSignerProtocol,
    ClockNowUTC,
    Ed25519ReferenceSigner,
    PubkeyVaultReader,
    PubkeyVaultWriter,
    _build_provenance_bytes,
    _parse_signed_at,
    _pubkey_key_path,
    _pubkey_provenance_path,
    reconcile_operator_pubkey,
    sign_report,
    verify_calibration_report,
)

__all__ = [
    # golden_set
    "GOLDEN_SET_BLUEPRINT_DEPS",
    "GOLDEN_SET_SCHEMA_VERSION",
    "GOLDEN_SET_VAULT_PREFIX_TMPL",
    "GoldenSetItem",
    "GoldenSetVaultRead",
    "IsSymlinkCallable",
    "RealpathCallable",
    "_deserialize_manifest",
    "_resolve_golden_set_path",
    "_vault_prefix_for",
    "assert_manifest_org_matches",
    "golden_set_iter",
    # report
    "REPORT_BLUEPRINT_DEPS",
    "AssembleInputs",
    "CalibrationReport",
    "CalibrationReportItem",
    "assemble_from_run",
    "calibration_report_field_set",
    "calibration_report_item_field_set",
    "canonical_bytes",
    "canonical_bytes_exclusions",
    "compute_canonical_sha256",
    "report_from_json",
    "report_to_json",
    # signing
    "SIGNING_BLUEPRINT_DEPS",
    "CALIBRATION_KEY_PATH_TMPL",
    "CALIBRATION_PUBKEY_PROVENANCE_PATH_TMPL",
    "CalibrationSignerProtocol",
    "ClockNowUTC",
    "Ed25519ReferenceSigner",
    "PubkeyVaultReader",
    "PubkeyVaultWriter",
    "_build_provenance_bytes",
    "_parse_signed_at",
    "_pubkey_key_path",
    "_pubkey_provenance_path",
    "reconcile_operator_pubkey",
    "sign_report",
    "verify_calibration_report",
]
