#!/usr/bin/env python3
"""
HRR-004 Builder 3 — residue.py
Per-wave residue collection, Necronomicon Memory Loop (Wα-LOAD / Wα-WRITE), HMAC-SHA256 signing.
"""

from __future__ import annotations
import json
import hmac
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class PerWaveResidue:
    wave_id: str
    run_id: str
    rejected_alternatives: List[Dict]
    dead_ends: List[Dict]
    minority_dissent: List[Dict]
    lessons: List[str]
    timestamp: str


@dataclass
class ResidueRecord:
    record_id: str
    run_id: str
    wave_residues: List[PerWaveResidue]
    metrics_snapshot: Dict
    signature: str  # HMAC-SHA256
    registry_hash: str
    created_at: str


class ResidueStore:
    """residue_store.jsonl persistence + Necronomicon Memory Loop + signing (MECH-035/036)."""

    def __init__(self, store_path: Path = Path("residue_store.jsonl"), hmac_key: bytes = b"z-rig-secret-key"):
        self.store_path = store_path
        self.hmac_key = hmac_key
        self.records: List[ResidueRecord] = []

    def _sign(self, payload: Dict) -> str:
        """MECH-035: HMAC-SHA256 signing at Wα-WRITE."""
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hmac.new(self.hmac_key, canonical, hashlib.sha256).hexdigest()

    def write_residue(self, wave_residues: List[PerWaveResidue], metrics: Dict, registry_hash: str) -> ResidueRecord:
        """Wα-WRITE: archive current run residue with signature."""
        run_id = wave_residues[0].run_id if wave_residues else "unknown"
        payload = {
            "run_id": run_id,
            "wave_residues": [asdict(r) for r in wave_residues],
            "metrics_snapshot": metrics,
            "registry_hash": registry_hash,
            "created_at": datetime.now(timezone.utc).isoformat() + "Z",
        }
        signature = self._sign(payload)
        record = ResidueRecord(
            record_id=str(__import__("uuid").uuid4()),
            run_id=run_id,
            wave_residues=wave_residues,
            metrics_snapshot=metrics,
            signature=signature,
            registry_hash=registry_hash,
            created_at=payload["created_at"],
        )
        self.records.append(record)
        self._append_to_log(record)
        return record

    def _append_to_log(self, record: ResidueRecord):
        with open(self.store_path, "a") as f:
            f.write(json.dumps(asdict(record)) + "\n")

    def load_prior_residue(self, registry_hash: str) -> List[ResidueRecord]:
        """Wα-LOAD: verified prior-run residue (MECH-036)."""
        verified = []
        if not self.store_path.exists():
            return verified
        with open(self.store_path) as f:
            for line in f:
                try:
                    data = json.loads(line)
                    rec = ResidueRecord(**data)
                    # Verify signature
                    payload = {k: v for k, v in data.items() if k not in ("signature", "record_id")}
                    expected = self._sign(payload)
                    if rec.signature == expected and rec.registry_hash == registry_hash:
                        verified.append(rec)
                except Exception:
                    continue
        return verified
