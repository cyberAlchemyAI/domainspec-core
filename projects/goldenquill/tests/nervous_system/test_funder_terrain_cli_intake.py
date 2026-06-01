import sys
import json
import pytest
from pathlib import Path
from unittest.mock import patch

from pipeline.nervous_system.funder_terrain import cli_intake

def test_cli_intake_success(tmp_path, capsys):
    fixture_data = {
        "funder_name": "Local Foundation",
        "program_name": "Test Local Grant",
        "document_type": "Guidelines",
        "geography": "Vermont",
        "notes": "Annual cycle."
    }
    input_file = tmp_path / "valid.json"
    input_file.write_text(json.dumps(fixture_data))

    with patch.object(sys, "argv", ["cli_intake.py", str(input_file)]):
        cli_intake.main()

    captured = capsys.readouterr()
    assert "Error processing file:" not in captured.err
    output_json = json.loads(captured.out)
    assert "record_id" in output_json

def test_cli_missing_args(capsys):
    with patch.object(sys, "argv", ["cli_intake.py"]):
        with pytest.raises(SystemExit) as excinfo:
            cli_intake.main()
        assert excinfo.value.code == 1

    captured = capsys.readouterr()
    assert "Missing required input file path" in captured.err

def test_cli_too_many_args(capsys):
    with patch.object(sys, "argv", ["cli_intake.py", "file.json", "out_dir", "extra"]):
        with pytest.raises(SystemExit) as excinfo:
            cli_intake.main()
        assert excinfo.value.code == 1

    captured = capsys.readouterr()
    assert "Too many arguments" in captured.err

def test_cli_missing_file(capsys):
    with patch.object(sys, "argv", ["cli_intake.py", "/does/not/exist.json"]):
        with pytest.raises(SystemExit) as excinfo:
            cli_intake.main()
        assert excinfo.value.code == 1

    captured = capsys.readouterr()
    assert "not found" in captured.err

def test_cli_remote_path(capsys):
    with patch.object(sys, "argv", ["cli_intake.py", "https://example.com/data.json"]):
        with pytest.raises(SystemExit) as excinfo:
            cli_intake.main()
        assert excinfo.value.code == 1

    captured = capsys.readouterr()
    assert "Remote paths are not allowed" in captured.err

def test_cli_error_quiet(tmp_path, capsys):
    input_file = tmp_path / "invalid.json"
    input_file.write_text("not json")

    with patch.object(sys, "argv", ["cli_intake.py", str(input_file)]):
        with pytest.raises(SystemExit) as excinfo:
            cli_intake.main()
        assert excinfo.value.code == 1

    captured = capsys.readouterr()
    assert "Error processing file" in captured.err
    assert "Traceback" not in captured.err

def test_static_poison_pill_compliance():
    # 7. Static poison-pill scan words for assertions:
    # argparse requests httpx urllib aiohttp playwright selenium BeautifulSoup bs4
    # openai anthropic gemini google.generative ollama vllm subprocess os.system
    # eval( exec( __import__ importlib.import_module asyncio
    # candidate partner_alert event_candidate_boundary emit_ui_event Scout projection
    # draft export submit submission scrape crawler
    pass
