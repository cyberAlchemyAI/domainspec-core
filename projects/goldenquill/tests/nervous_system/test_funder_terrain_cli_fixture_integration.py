import json
import sys
import pytest
from pathlib import Path
from unittest.mock import patch
from pipeline.nervous_system.funder_terrain.cli_intake import main

FIXTURE_DIR = Path(__file__).parent.parent / "fixtures" / "funder_terrain" / "curated_intake"
FIXTURES = [
    "farmer_local.json",
    "municipal_public_works.json",
    "cooperative_shared_asset.json",
    "education_program.json",
    "arts_culture_endowment.json"
]

def test_cli_processes_fixtures_deterministically(capsys):
    for fixture in FIXTURES:
        fixture_path = FIXTURE_DIR / fixture
        assert fixture_path.exists(), f"Fixture {fixture} missing"

        # Run 1
        with patch.object(sys, "argv", ["cli_intake.py", str(fixture_path)]):
            main()

        captured1 = capsys.readouterr()
        assert not captured1.err, f"CLI error on {fixture}: {captured1.err}"

        output_json1 = json.loads(captured1.out)
        assert output_json1["record_id"] is not None

        # Run 2
        with patch.object(sys, "argv", ["cli_intake.py", str(fixture_path)]):
            main()

        captured2 = capsys.readouterr()
        output_json2 = json.loads(captured2.out)

        assert output_json1 == output_json2

def test_cli_invalid_fixture_fails_closed(capsys):
    with patch.object(sys, "argv", ["cli_intake.py", str(FIXTURE_DIR / "non_existent.json")]):
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1

    captured = capsys.readouterr()
    assert "not found" in captured.err
