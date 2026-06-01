import pytest
from pathlib import Path
import csv
import json
import yaml

from pipeline.cli.superscout_metro_expansion import expand_queries

def test_expand_queries():
    text = "Most Wanted Fine Art Gallery call for artists grant funding Pittsburgh"
    expanded, changed = expand_queries(text, "Philadelphia")
    assert changed
    assert expanded == "Most Wanted Fine Art Gallery call for artists grant funding Philadelphia"

    text2 = "Allegheny County sustainability grants"
    expanded2, changed2 = expand_queries(text2, "Washington DC")
    assert changed2
    assert expanded2 == "Washington DC sustainability grants"

    text3 = "Western Pennsylvania funding"
    expanded3, changed3 = expand_queries(text3, "Philadelphia")
    assert changed3
    assert expanded3 == "Philadelphia funding"

    text_no_change = "National arts funding"
    expanded_nc, changed_nc = expand_queries(text_no_change, "Philadelphia")
    assert not changed_nc
    assert expanded_nc == text_no_change

def test_deterministic_output(tmp_path):
    import sys
    from unittest.mock import patch
    from pipeline.cli.superscout_metro_expansion import main

    gold_dir = tmp_path / "gold"
    gold_dir.mkdir()
    
    seeds = [
        {"search_seed_id": "s1", "query": "Arts grant Pittsburgh", "category": "generated"},
        {"search_seed_id": "s2", "query": "Arts grant Western PA", "category": "program_cycle"},
    ]
    with (gold_dir / "search_seeds.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=seeds[0].keys())
        writer.writeheader()
        writer.writerows(seeds)

    funders = [
        {"funder_id": "f1", "name": "Pittsburgh Foundation", "funder_class": "private_foundation"},
    ]
    with (gold_dir / "funders.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=funders[0].keys())
        writer.writeheader()
        writer.writerows(funders)

    with (gold_dir / "broken_url_queue.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["source_id", "repair_candidate_query"])
        writer.writeheader()
        writer.writerow({"source_id": "b1", "repair_candidate_query": "Pittsburgh Foundation grants URL"})

    out_dir = tmp_path / "out"
    s_queue = tmp_path / "queue.jsonl"

    test_args = [
        "superscout_metro_expansion.py",
        "--gold-dir", str(gold_dir),
        "--output-dir", str(out_dir),
        "--target-metros", "Philadelphia",
        "--suggestion-queue", str(s_queue)
    ]
    
    with patch.object(sys, 'argv', test_args):
        main()

    philly_csv = out_dir / "philadelphia_queries.csv"
    assert philly_csv.exists()
    
    with philly_csv.open() as f:
        rows = list(csv.DictReader(f))
        assert len(rows) == 4
        # Sort order is by expansion_category, source_file, source_id, expanded_query
        # 1. broken-URL repair search queries (b1)
        # 2. funder-class analog queries (f1)
        # 3. funder-class analog queries (s1)
        # 4. program-cycle discovery queries (s2)
        assert rows[0]["original_query"] == "Pittsburgh Foundation grants URL"
        assert rows[0]["expanded_query"] == "Philadelphia Foundation grants URL"
        assert rows[0]["expansion_category"] == "broken-URL repair search queries"
        assert rows[0]["source_file"] == "broken_url_queue.csv"
        
        # Check YAML deterministic output
        philly_yaml = out_dir / "philadelphia_queries.yaml"
        assert philly_yaml.exists()
        with philly_yaml.open() as yf:
            data = yaml.safe_load(yf)
            assert len(data) == 4
            assert data[0]["created_by_cli_version"] == "0.1.0"
