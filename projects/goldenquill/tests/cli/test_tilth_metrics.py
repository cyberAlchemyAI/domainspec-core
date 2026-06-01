"""Tests for ``tilth metrics cycle-cost`` CLI.

Covers:

* Happy path — synthetic cache-ledger with two rows tagged ``cycle_id=demo-1``,
  one ``scribe`` + one ``judge``; verify the report aggregates correctly,
  surfaces per-seat / per-card / per-model rollups, and degrades gracefully
  when the Coefficient Registry is the unsigned scaffold.
* Missing cycle_id — CLI exits 1 with a helpful stderr message when the
  requested cycle_id has zero matching rows.
* Invalid cycle_id grammar — CLI exits 1 with a path-traversal-defense
  error (mirrors ``CycleReceipt`` grammar).
* ``--json`` and ``--csv`` shape sanity.
* ``--include-unattributed`` includes rows with ``cycle_id: null``.
* ``--org`` restricts the scan.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path

import pytest

from pipeline.cli.tilth_metrics import (
    build_cycle_cost,
    format_csv,
    format_json,
    format_text,
    main as cli_main,
    read_registry_state,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def synth_repo(tmp_path: Path) -> Path:
    """Build a tiny synthetic repo with two orgs and a scaffold registry."""
    # pyproject so _resolve_repo_root finds the root.
    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname = 'synth'\nversion = '0.0.0'\n",
        encoding="utf-8",
    )

    # Coefficient registry — scaffold shape (canonical v0.1 Beta-launch state).
    reg = tmp_path / "vault_shared" / "wpfa" / "coefficient_registry"
    reg.mkdir(parents=True)
    (reg / "active.yaml").write_text(
        "\n".join(
            [
                'schema_version: "0.0.0-scaffold"',
                'quarter: "Q3-2026"',
                'published_at: "2026-05-11T00:00:00Z"',
                'sn_llc_signature_ed25519: ""',
                'sn_llc_signing_key_id: "scaffold"',
                'baseline_model_id: "scaffold"',
                "entries: []",
                'methodology_url: "https://example.invalid/scaffold"',
                "rollback_pointer: null",
            ]
        ),
        encoding="utf-8",
    )

    # session_log.jsonl — one row in the cycle window, one outside.
    sl = tmp_path / "pipeline" / "metrics"
    sl.mkdir(parents=True)
    (sl / "session_log.jsonl").write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "session_id": "in-window",
                        "date": "2026-05-18",
                        "agent": "test",
                        "turns": 4,
                    }
                ),
                json.dumps(
                    {
                        "session_id": "out-of-window",
                        "date": "2026-04-01",
                        "agent": "test",
                        "turns": 4,
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # acme-foo ledger — three rows: two tagged demo-1, one untagged legacy row.
    foo = tmp_path / "tilth" / "logs" / "acme-foo"
    foo.mkdir(parents=True)
    (foo / "cache-ledger.jsonl").write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "ts": "2026-05-18T12:00:00.000Z",
                        "org": "acme-foo",
                        "workflow": "scribe-draft",
                        "model": "claude-sonnet-4-6",
                        "cache_retention": "long",
                        "elapsed_ms": 1500,
                        "input_tokens": 100,
                        "output_tokens": 200,
                        "cache_read_input_tokens": 800,
                        "cache_creation_input_tokens": 0,
                        "paid_usd": 0.005,
                        "cached_savings_usd": 0.002,
                        "response_id": "msg_1",
                        "stop_reason": "end_turn",
                        "rates_fallback": False,
                        "cycle_id": "demo-1",
                        "seat": "scribe",
                        "card_id": "scribe.v1",
                    }
                ),
                json.dumps(
                    {
                        "ts": "2026-05-18T12:05:00.000Z",
                        "org": "acme-foo",
                        "workflow": "judge-score",
                        "model": "claude-opus-4-7",
                        "cache_retention": "long",
                        "elapsed_ms": 2200,
                        "input_tokens": 50,
                        "output_tokens": 80,
                        "cache_read_input_tokens": 0,
                        "cache_creation_input_tokens": 1000,
                        "paid_usd": 0.0123,
                        "cached_savings_usd": 0.0,
                        "response_id": "msg_2",
                        "stop_reason": "end_turn",
                        "rates_fallback": False,
                        "cycle_id": "demo-1",
                        "seat": "judge",
                        "card_id": "judge.vapg_fy26",
                    }
                ),
                # Legacy row — no cycle_id / seat / card_id stamping.
                json.dumps(
                    {
                        "ts": "2026-05-18T11:00:00.000Z",
                        "org": "acme-foo",
                        "workflow": "smoke-test",
                        "model": "claude-haiku-4-5",
                        "cache_retention": "long",
                        "elapsed_ms": 800,
                        "input_tokens": 10,
                        "output_tokens": 20,
                        "cache_read_input_tokens": 0,
                        "cache_creation_input_tokens": 0,
                        "paid_usd": 0.001,
                        "cached_savings_usd": 0.0,
                        "response_id": "msg_legacy",
                        "stop_reason": "end_turn",
                        "rates_fallback": False,
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # acme-bar ledger — one row, different cycle.
    bar = tmp_path / "tilth" / "logs" / "acme-bar"
    bar.mkdir(parents=True)
    (bar / "cache-ledger.jsonl").write_text(
        json.dumps(
            {
                "ts": "2026-05-18T13:00:00.000Z",
                "org": "acme-bar",
                "workflow": "scout",
                "model": "claude-sonnet-4-6",
                "cache_retention": "long",
                "elapsed_ms": 1000,
                "input_tokens": 75,
                "output_tokens": 25,
                "cache_read_input_tokens": 0,
                "cache_creation_input_tokens": 0,
                "paid_usd": 0.003,
                "cached_savings_usd": 0.0,
                "response_id": "msg_bar",
                "stop_reason": "end_turn",
                "rates_fallback": False,
                "cycle_id": "other-cycle",
                "seat": "scout",
                "card_id": "scout.channel_a",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    return tmp_path


# ---------------------------------------------------------------------------
# Library-level tests
# ---------------------------------------------------------------------------


def test_happy_path_build_cycle_cost(synth_repo: Path) -> None:
    report = build_cycle_cost(repo_root=synth_repo, cycle_id="demo-1")

    assert report.cycle_id == "demo-1"
    assert report.total.calls == 2
    assert report.total.input_tokens == 150
    assert report.total.output_tokens == 280
    assert report.total.cache_read_input_tokens == 800
    assert report.total.cache_creation_input_tokens == 1000
    assert report.total.paid_usd == pytest.approx(0.0173, abs=1e-6)
    assert report.total.cached_savings_usd == pytest.approx(0.002, abs=1e-6)

    # Per-seat breakdown — both seats present, no "unattributed".
    assert set(report.per_seat) == {"scribe", "judge"}
    assert report.per_seat["scribe"].paid_usd == pytest.approx(0.005, abs=1e-6)
    assert report.per_seat["judge"].paid_usd == pytest.approx(0.0123, abs=1e-6)

    # Per-card breakdown.
    assert set(report.per_card) == {"scribe.v1", "judge.vapg_fy26"}

    # Per-model breakdown.
    assert set(report.per_model) == {"claude-sonnet-4-6", "claude-opus-4-7"}

    # Registry state — scaffold per the synthetic fixture.
    assert report.registry_state == "unsigned-scaffold"
    assert report.registry_baseline_model == "scaffold"

    # Session-log join — one row matches the cycle window.
    assert report.session_log_matches == 1


def test_invalid_cycle_id_grammar(synth_repo: Path) -> None:
    with pytest.raises(ValueError, match="path-traversal defense"):
        build_cycle_cost(repo_root=synth_repo, cycle_id="../evil")


def test_org_filter_isolation(synth_repo: Path) -> None:
    # demo-1 only lives in acme-foo; --org acme-bar should find zero matches.
    report = build_cycle_cost(
        repo_root=synth_repo, cycle_id="demo-1", org_filter="acme-bar"
    )
    assert report.total.calls == 0

    # And --org acme-foo gets only acme-foo rows.
    report = build_cycle_cost(
        repo_root=synth_repo, cycle_id="demo-1", org_filter="acme-foo"
    )
    assert report.total.calls == 2
    assert report.orgs_seen == ["acme-foo"]


def test_include_unattributed_picks_up_legacy_row(synth_repo: Path) -> None:
    # The acme-foo ledger has one legacy row with no cycle_id; without the
    # flag it stays out; with the flag it folds into the unattributed bucket.
    report = build_cycle_cost(
        repo_root=synth_repo,
        cycle_id="demo-1",
        include_unattributed=True,
    )
    assert report.total.calls == 3
    assert "unattributed" in report.per_seat
    assert report.per_seat["unattributed"].calls == 1


def test_registry_state_signed_vs_scaffold(tmp_path: Path) -> None:
    # Missing.
    state, baseline = read_registry_state(repo_root=tmp_path)
    assert state == "missing"
    assert baseline is None

    # Signed-shaped (lightweight YAML-shape check — full crypto verify is
    # done by load_active at WPFA emit time, not by this CLI).
    reg = tmp_path / "vault_shared" / "wpfa" / "coefficient_registry"
    reg.mkdir(parents=True)
    (reg / "active.yaml").write_text(
        "\n".join(
            [
                'schema_version: "1.0.0"',
                'sn_llc_signature_ed25519: "' + ("a" * 128) + '"',
                'baseline_model_id: "claude-sonnet-4-6"',
            ]
        ),
        encoding="utf-8",
    )
    state, baseline = read_registry_state(repo_root=tmp_path)
    assert state == "signed"
    assert baseline == "claude-sonnet-4-6"


def test_format_json_shape(synth_repo: Path) -> None:
    report = build_cycle_cost(repo_root=synth_repo, cycle_id="demo-1")
    payload = json.loads(format_json(report))
    assert payload["cycle_id"] == "demo-1"
    assert payload["registry_state"] == "unsigned-scaffold"
    assert payload["total"]["calls"] == 2
    assert "scribe" in payload["per_seat"]


def test_format_csv_shape(synth_repo: Path) -> None:
    report = build_cycle_cost(repo_root=synth_repo, cycle_id="demo-1")
    rows = list(csv.reader(io.StringIO(format_csv(report))))
    header = rows[0]
    assert header[0] == "cycle_id"
    assert header[2] == "key"
    scopes = {r[1] for r in rows[1:]}
    assert scopes == {"total", "seat", "card", "model"}


def test_format_text_smoke(synth_repo: Path) -> None:
    report = build_cycle_cost(repo_root=synth_repo, cycle_id="demo-1")
    txt = format_text(report)
    assert "Cycle: demo-1" in txt
    assert "PER SEAT" in txt
    assert "scribe" in txt
    assert "counterfactual_usd : N/A" in txt
    assert "registry unsigned" not in txt or "registry state" in txt.lower()


# ---------------------------------------------------------------------------
# Entry-point tests
# ---------------------------------------------------------------------------


def test_cli_happy_path(synth_repo: Path, capsys: pytest.CaptureFixture) -> None:
    rc = cli_main(
        [
            "cycle-cost",
            "demo-1",
            "--repo-root",
            str(synth_repo),
            "--posture",
            "split-context-hybrid",
        ]
    )
    out = capsys.readouterr()
    assert rc == 0, out.err
    assert "Cycle: demo-1" in out.out
    assert "split-context-hybrid" in out.out
    assert "scribe" in out.out
    assert "judge" in out.out


def test_cli_missing_cycle_id(
    synth_repo: Path, capsys: pytest.CaptureFixture
) -> None:
    rc = cli_main(
        ["cycle-cost", "nonexistent-cycle", "--repo-root", str(synth_repo)]
    )
    out = capsys.readouterr()
    assert rc == 1
    assert "no ledger rows matched" in out.err
    assert "nonexistent-cycle" in out.err


def test_cli_invalid_cycle_id(
    synth_repo: Path, capsys: pytest.CaptureFixture
) -> None:
    rc = cli_main(
        ["cycle-cost", "../evil", "--repo-root", str(synth_repo)]
    )
    out = capsys.readouterr()
    assert rc == 1
    assert "path-traversal defense" in out.err


def test_cli_json_output(
    synth_repo: Path, capsys: pytest.CaptureFixture
) -> None:
    rc = cli_main(
        ["cycle-cost", "demo-1", "--json", "--repo-root", str(synth_repo)]
    )
    out = capsys.readouterr()
    assert rc == 0
    payload = json.loads(out.out)
    assert payload["cycle_id"] == "demo-1"
    assert payload["total"]["calls"] == 2


def test_cli_csv_output(
    synth_repo: Path, capsys: pytest.CaptureFixture
) -> None:
    rc = cli_main(
        ["cycle-cost", "demo-1", "--csv", "--repo-root", str(synth_repo)]
    )
    out = capsys.readouterr()
    assert rc == 0
    rows = list(csv.reader(io.StringIO(out.out)))
    assert rows[0][0] == "cycle_id"
    assert any(r[1] == "seat" for r in rows[1:])


def test_cli_include_unattributed(
    synth_repo: Path, capsys: pytest.CaptureFixture
) -> None:
    rc = cli_main(
        [
            "cycle-cost",
            "demo-1",
            "--include-unattributed",
            "--json",
            "--repo-root",
            str(synth_repo),
        ]
    )
    out = capsys.readouterr()
    assert rc == 0
    payload = json.loads(out.out)
    assert payload["total"]["calls"] == 3
    assert "unattributed" in payload["per_seat"]
