import json
import pytest
from pathlib import Path
from pipeline.nervous_system.funder_terrain.intake import intake_curated_funder_terrain_file

FIXTURE_DIR = Path(__file__).parent.parent / "fixtures" / "funder_terrain" / "curated_intake"
FIXTURES = [
    "farmer_local.json",
    "municipal_public_works.json",
    "cooperative_shared_asset.json",
    "education_program.json",
    "arts_culture_endowment.json"
]

def test_all_five_fixtures_exist():
    for f in FIXTURES:
        assert (FIXTURE_DIR / f).exists(), f"Fixture {f} is missing"

def test_all_fixtures_are_valid_json():
    for f in FIXTURES:
        content = (FIXTURE_DIR / f).read_text(encoding="utf-8")
        json.loads(content)

def test_no_forbidden_terms_in_fixtures():
    forbidden = ["http://", "https://", "api", "web", "url", "scrape", "crawler", "llm", "model", "candidate", "partner_alert"]
    for f in FIXTURES:
        content = (FIXTURE_DIR / f).read_text(encoding="utf-8").lower()
        for term in forbidden:
            assert term not in content, f"Forbidden term {term} found in {f}"

def test_intake_successfully():
    for f in FIXTURES:
        record = intake_curated_funder_terrain_file(FIXTURE_DIR / f)
        assert record is not None

def test_repeated_intake_deterministic():
    for f in FIXTURES:
        r1 = intake_curated_funder_terrain_file(FIXTURE_DIR / f)
        r2 = intake_curated_funder_terrain_file(FIXTURE_DIR / f)
        assert r1.record_sha256 == r2.record_sha256
        assert r1.normalization_input_sha256 == r2.normalization_input_sha256

def test_fixture_classification():
    for f in FIXTURES:
        record = intake_curated_funder_terrain_file(FIXTURE_DIR / f)
        assert record.review_status.human_review_required is True or record.program_status != "unknown"

def test_no_generation_script():
    assert not (FIXTURE_DIR / "generate.py").exists()
    assert not (FIXTURE_DIR / "generate.sh").exists()
