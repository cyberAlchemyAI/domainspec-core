import dataclasses
import hashlib
import json
import os
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping, Optional, Sequence


class SnapshotAlreadyExistsError(Exception):
    pass


@dataclasses.dataclass(frozen=True)
class ReadModelExportResult:
    run_id: str
    snapshot_dir: str
    latest_dir: str
    full_jsonl_path: str
    index_jsonl_path: str
    manifest_path: str
    latest_full_jsonl_path: str
    latest_index_jsonl_path: str
    latest_manifest_path: str
    full_record_count: int
    index_record_count: int
    matched_count: int
    missing_aln_count: int
    malformed_aln_count: int
    unmatched_count: int
    ambiguous_count: int
    full_jsonl_sha256: str
    index_jsonl_sha256: str
    manifest_sha256: str


def _robust_serialize(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, Path):
        return str(obj)
    if dataclasses.is_dataclass(obj):
        if not isinstance(obj, type):
            d = dataclasses.asdict(obj)
            return {k: _robust_serialize(v) for k, v in d.items()}
    if isinstance(obj, SimpleNamespace):
        return {k: _robust_serialize(v) for k, v in obj.__dict__.items()}
    if isinstance(obj, Mapping):
        return {k: _robust_serialize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_robust_serialize(item) for item in obj]
    if hasattr(obj, "__dict__"):
        return {k: _robust_serialize(v) for k, v in obj.__dict__.items() if not k.startswith("_")}
    return str(obj)


def export_enriched_opportunities_read_model(
    enriched_records: Sequence[object],
    *,
    output_root: Path | str,
    run_id: str,
    generated_at_utc: str,
    source_grants_gov_file: str,
    source_sam_gov_file: str,
    source_grants_gov_hash: str,
    source_sam_gov_hash: str,
    schema_version: str = "1.0",
    read_model_version: str = "scout_enriched_opportunities_v1",
    overwrite_snapshot: bool = False,
) -> ReadModelExportResult:

    output_root_path = Path(output_root)
    snapshots_dir = output_root_path / "snapshots"
    latest_dir = output_root_path / "latest"

    run_snapshot_dir = snapshots_dir / run_id

    if run_snapshot_dir.exists():
        if not overwrite_snapshot:
            raise SnapshotAlreadyExistsError(f"Snapshot directory already exists: {run_snapshot_dir}")
        else:
            shutil.rmtree(run_snapshot_dir)

    run_snapshot_dir.mkdir(parents=True, exist_ok=True)
    latest_dir.mkdir(parents=True, exist_ok=True)

    full_path = run_snapshot_dir / "enriched_opportunities_full.jsonl"
    index_path = run_snapshot_dir / "enriched_opportunities_index.jsonl"
    manifest_path = run_snapshot_dir / "manifest.json"

    # Sort records deterministically by opportunity_id if available
    def _get_opp_id(r: object) -> str:
        opp = getattr(r, "opportunity", None)
        return str(getattr(opp, "id", "") or getattr(opp, "opportunity_id", "") or "")

    try:
        sorted_records = sorted(enriched_records, key=_get_opp_id)
    except Exception:
        sorted_records = list(enriched_records)

    counts = {
        "matched": 0,
        "missing_aln": 0,
        "malformed_aln": 0,
        "unmatched": 0,
        "ambiguous": 0,
    }

    join_version = "unknown"
    if sorted_records:
        join_version = getattr(sorted_records[0], "enrichment_version", "unknown")

    full_lines = []
    index_lines = []

    for r in sorted_records:
        status = getattr(r, "enrichment_status", "unmatched")
        if status in counts:
            counts[status] += 1

        opp = getattr(r, "opportunity", None)
        listing = getattr(r, "assistance_listing", None)

        opp_id = _get_opp_id(r)
        title = str(getattr(opp, "title", getattr(opp, "opportunity_title", "")))
        agency = str(getattr(opp, "agency", getattr(opp, "agency_code", getattr(opp, "funder", ""))))
        norm_aln = getattr(r, "assistance_listing_number_normalized", None)

        joined_at = getattr(r, "joined_at_utc", None)
        reason = getattr(r, "enrichment_reason", "")

        lineage_block = {
            "source_grants_gov_file": source_grants_gov_file,
            "source_sam_gov_file": source_sam_gov_file,
            "source_grants_gov_hash": source_grants_gov_hash,
            "source_sam_gov_hash": source_sam_gov_hash,
            "joined_at_utc": joined_at,
            "generated_at_utc": generated_at_utc,
            "join_version": join_version,
            "read_model_version": read_model_version,
            "run_id": run_id
        }

        full_record = {
            "schema_version": schema_version,
            "record_type": "enriched_opportunity_full",
            "read_model_version": read_model_version,
            "opportunity_id": opp_id,
            "title": title,
            "agency": agency,
            "assistance_listing_number_normalized": norm_aln,
            "enrichment_status": status,
            "enrichment_reason": reason,
            "capital_efficiency_signals": _robust_serialize(getattr(r, "capital_efficiency_signals", [])),
            "grants_gov": _robust_serialize(opp),
            "sam_gov": _robust_serialize(listing),
            "lineage": lineage_block
        }

        posted_date = str(getattr(opp, "posted_date", getattr(opp, "post_date", "")))
        close_date = str(getattr(opp, "close_date", ""))

        signals = getattr(r, "capital_efficiency_signals", [])
        index_record = {
            "schema_version": schema_version,
            "record_type": "enriched_opportunity_index",
            "read_model_version": read_model_version,
            "opportunity_id": opp_id,
            "title": title,
            "agency": agency,
            "assistance_listing_number_normalized": norm_aln,
            "enrichment_status": status,
            "capital_efficiency_signals_count": len(signals),
            "capital_efficiency_signal_types": [s.signal_type.value for s in signals],
            "capital_efficiency_review_required": any(getattr(s, "review_required", True) for s in signals),
            "capital_efficiency_review_owners": list({s.professional_review_owner for s in signals}),
            "posted_date": posted_date,
            "close_date": close_date,
            "full_record_ref": f"{run_id}/enriched_opportunities_full.jsonl#{opp_id}",
            "lineage_ref": run_id
        }

        full_lines.append(json.dumps(full_record, sort_keys=True, separators=(",", ":")))
        index_lines.append(json.dumps(index_record, sort_keys=True, separators=(",", ":")))

    full_content = ("\n".join(full_lines) + "\n").encode("utf-8") if full_lines else b""
    index_content = ("\n".join(index_lines) + "\n").encode("utf-8") if index_lines else b""

    full_path.write_bytes(full_content)
    index_path.write_bytes(index_content)

    full_sha256 = hashlib.sha256(full_content).hexdigest()
    index_sha256 = hashlib.sha256(index_content).hexdigest()

    manifest = {
        "schema_version": schema_version,
        "read_model_version": read_model_version,
        "run_id": run_id,
        "generated_at_utc": generated_at_utc,
        "source_grants_gov_file": source_grants_gov_file,
        "source_sam_gov_file": source_sam_gov_file,
        "source_grants_gov_hash": source_grants_gov_hash,
        "source_sam_gov_hash": source_sam_gov_hash,
        "join_version": join_version,
        "full_record_count": len(full_lines),
        "index_record_count": len(index_lines),
        "matched_count": counts.get("matched", 0),
        "missing_aln_count": counts.get("missing_aln", 0),
        "malformed_aln_count": counts.get("malformed_aln", 0),
        "unmatched_count": counts.get("unmatched", 0),
        "ambiguous_count": counts.get("ambiguous", 0),
        "full_jsonl_sha256": full_sha256,
        "index_jsonl_sha256": index_sha256
    }

    manifest_content = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode("utf-8")
    manifest_path.write_bytes(manifest_content)
    manifest_sha256 = hashlib.sha256(manifest_content).hexdigest()

    latest_full = latest_dir / "enriched_opportunities_full.jsonl"
    latest_index = latest_dir / "enriched_opportunities_index.jsonl"
    latest_manifest = latest_dir / "manifest.json"

    shutil.copy2(full_path, latest_full)
    shutil.copy2(index_path, latest_index)
    shutil.copy2(manifest_path, latest_manifest)

    return ReadModelExportResult(
        run_id=run_id,
        snapshot_dir=str(run_snapshot_dir.absolute()),
        latest_dir=str(latest_dir.absolute()),
        full_jsonl_path=str(full_path.absolute()),
        index_jsonl_path=str(index_path.absolute()),
        manifest_path=str(manifest_path.absolute()),
        latest_full_jsonl_path=str(latest_full.absolute()),
        latest_index_jsonl_path=str(latest_index.absolute()),
        latest_manifest_path=str(latest_manifest.absolute()),
        full_record_count=len(full_lines),
        index_record_count=len(index_lines),
        matched_count=counts.get("matched", 0),
        missing_aln_count=counts.get("missing_aln", 0),
        malformed_aln_count=counts.get("malformed_aln", 0),
        unmatched_count=counts.get("unmatched", 0),
        ambiguous_count=counts.get("ambiguous", 0),
        full_jsonl_sha256=full_sha256,
        index_jsonl_sha256=index_sha256,
        manifest_sha256=manifest_sha256
    )
