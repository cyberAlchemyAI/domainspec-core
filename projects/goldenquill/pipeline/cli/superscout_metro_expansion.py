#!/usr/bin/env python3
"""SuperScout Metro Expansion Engine

Generates metro-specific search query packs from normalized funder atlas.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
import yaml

CLI_VERSION = "0.1.0"

ANALOG_TERMS = [
    r"\bpittsburgh\b",
    r"\ballegheny county\b",
    r"\ballegheny\b",
    r"\bwestern pennsylvania\b",
    r"\bwestern pa\b",
    r"\bswpa\b",
]

ANALOG_REGEX = re.compile("|".join(ANALOG_TERMS), re.IGNORECASE)

@dataclass(frozen=True)
class MetroQuery:
    source_file: str
    source_id: str
    source_category: str
    original_query: str
    target_metro: str
    replacement_rule_id: str
    expanded_query: str
    expansion_category: str
    requires_model_review: bool
    created_by_cli_version: str

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold-dir", default="pipeline/funder_intelligence/_staging/gold")
    parser.add_argument("--output-dir", default="pipeline/funder_intelligence/_staging/metro_expansion_query_packs")
    parser.add_argument("--target-metros", default="Philadelphia,Washington DC")
    parser.add_argument("--suggestion-queue", default="pipeline/funder_intelligence/_staging/model_suggestions_queue.jsonl")
    return parser.parse_args()

def expand_queries(text: str, metro: str) -> tuple[str, bool]:
    """Replace analog terms with the target metro. Return expanded text and whether replacement occurred."""
    if not text:
        return text, False
    expanded, count = ANALOG_REGEX.subn(metro, text)
    return expanded, count > 0

def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    args = parse_args()
    gold_dir = Path(args.gold_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    metros = [m.strip() for m in args.target_metros.split(",")]
    
    seeds = load_csv(gold_dir / "search_seeds.csv")
    funders = load_csv(gold_dir / "funders.csv")
    broken_urls = load_csv(gold_dir / "broken_url_queue.csv")

    seen_suggestions = set()
    suggestions = []
    
    for metro in metros:
        queries = []
        
        # 1. Search Seeds Expansion
        for row in seeds:
            q = row.get("query", "")
            expanded_q, changed = expand_queries(q, metro)
            if changed:
                expansion_category = "program-cycle discovery queries" if "cycle" in row.get("category", "") else "prior-grantee mining queries" if "grantee" in row.get("category", "") else "funder-class analog queries"
                queries.append(MetroQuery(
                    source_file="search_seeds.csv",
                    source_id=row.get("search_seed_id", ""),
                    source_category=row.get("category", ""),
                    original_query=q,
                    target_metro=metro,
                    replacement_rule_id="regex_analog_term",
                    expanded_query=expanded_q,
                    expansion_category=expansion_category,
                    requires_model_review=False,
                    created_by_cli_version=CLI_VERSION,
                ))

        # 2. Funder Name Expansion
        for row in funders:
            name = row.get("name", "")
            expanded_name, changed = expand_queries(name, metro)
            if changed:
                queries.append(MetroQuery(
                    source_file="funders.csv",
                    source_id=row.get("funder_id", ""),
                    source_category=row.get("funder_class", ""),
                    original_query=name,
                    target_metro=metro,
                    replacement_rule_id="regex_analog_term",
                    expanded_query=expanded_name,
                    expansion_category="funder-class analog queries",
                    requires_model_review=False,
                    created_by_cli_version=CLI_VERSION,
                ))

        # 3. Broken URL Repair Queries
        for row in broken_urls:
            repair = row.get("repair_candidate_query", "")
            expanded_repair, changed = expand_queries(repair, metro)
            if changed:
                queries.append(MetroQuery(
                    source_file="broken_url_queue.csv",
                    source_id=row.get("source_id", ""),
                    source_category="broken_url",
                    original_query=repair,
                    target_metro=metro,
                    replacement_rule_id="regex_analog_term",
                    expanded_query=expanded_repair,
                    expansion_category="broken-URL repair search queries",
                    requires_model_review=False,
                    created_by_cli_version=CLI_VERSION,
                ))
            elif "pittsburgh" in repair.lower():
                 # ambiguous, queue it
                 s_id = row.get("source_id", "")
                 if s_id not in seen_suggestions:
                     seen_suggestions.add(s_id)
                     suggestions.append({
                         "reason": "ambiguous_metro_expansion",
                         "source_file": "broken_url_queue.csv",
                         "source_id": s_id,
                         "text": repair
                     })

        # Write out
        pack_name = metro.replace(" ", "_").lower()
        csv_path = out_dir / f"{pack_name}_queries.csv"
        yaml_path = out_dir / f"{pack_name}_queries.yaml"
        
        # Sort by expansion_category, source_file, source_id, expanded_query to keep deterministic
        q_dicts = [asdict(q) for q in sorted(queries, key=lambda x: (x.expansion_category, x.source_file, x.source_id, x.expanded_query))]
        
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            if q_dicts:
                writer = csv.DictWriter(f, fieldnames=list(q_dicts[0].keys()))
                writer.writeheader()
                writer.writerows(q_dicts)
                
        with yaml_path.open("w", encoding="utf-8") as f:
            yaml.dump(q_dicts, f, sort_keys=True)
            
    if suggestions:
        s_path = Path(args.suggestion_queue)
        with s_path.open("a", encoding="utf-8") as f:
            for s in suggestions:
                f.write(json.dumps(s) + "\n")

if __name__ == "__main__":
    main()
