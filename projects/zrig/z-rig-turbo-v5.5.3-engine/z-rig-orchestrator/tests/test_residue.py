#!/usr/bin/env python3
"""Tests for residue.py — Necronomicon Memory Loop + signing."""

import tempfile
from pathlib import Path
from zrig.residue import ResidueStore, PerWaveResidue


def test_write_and_load_residue_with_signature():
    with tempfile.TemporaryDirectory() as tmp:
        store_path = Path(tmp) / "residue_store.jsonl"
        store = ResidueStore(store_path, hmac_key=b"test-key")

        wave_res = PerWaveResidue(
            wave_id="Wα", run_id="HRR-004", rejected_alternatives=[{"alt": "micro-mode"}],
            dead_ends=[], minority_dissent=[], lessons=["Always verify signatures"],
            timestamp="2026-06-16T12:00:00Z"
        )
        rec = store.write_residue([wave_res], {"fatal_count": 0}, "registry-hash-abc123")

        assert rec.signature is not None
        assert len(rec.signature) == 64  # SHA-256 hex

        loaded = store.load_prior_residue("registry-hash-abc123")
        assert len(loaded) == 1
        assert loaded[0].registry_hash == "registry-hash-abc123"
