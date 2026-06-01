import re
import json
import hashlib
import yaml
from pathlib import Path
from typing import List, Optional, Tuple
from pydantic import BaseModel, field_validator

class FunderTerrainRule(BaseModel):
    rule_id: str
    target_field: str
    priority: int
    regex_patterns: List[str]
    output_value: str
    confidence: str
    review_required: bool
    rationale: str

    @field_validator('regex_patterns')
    @classmethod
    def validate_regex_patterns(cls, patterns: List[str]) -> List[str]:
        for pattern in patterns:
            # Reject suspicious ReDoS patterns
            if re.search(r'(\+|\*|\?|{\d+(,\d*)?})\s*\+', pattern) or re.search(r'\(\.\*\)\.\*', pattern) or re.search(r'\([^)]*(\+|\*|\?)\)\s*(\+|\*|\?)', pattern):
                raise ValueError(f"Suspicious/High-Risk regex pattern detected: {pattern}")
            try:
                re.compile(pattern)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{pattern}': {e}")
        return patterns

class FunderTerrainRuleset(BaseModel):
    rules: List[FunderTerrainRule]

def canonicalize_rules(rules: List[FunderTerrainRule]) -> str:
    rules_dicts = [r.model_dump() for r in rules]
    rules_dicts = sorted(rules_dicts, key=lambda x: x["rule_id"])
    return json.dumps(rules_dicts, sort_keys=True, separators=(',', ':'))

def hash_rules(rules: List[FunderTerrainRule]) -> str:
    canon = canonicalize_rules(rules)
    return hashlib.sha256(canon.encode('utf-8')).hexdigest()

def load_rules_from_yaml(filepath: Path) -> List[FunderTerrainRule]:
    if not filepath.exists():
        raise FileNotFoundError(f"Rule file missing: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or []
    return [FunderTerrainRule(**d) for d in data]

def check_rules(target_val: str, rules_list: List[FunderTerrainRule]) -> Optional[Tuple[FunderTerrainRule, str]]:
    best_match = None
    target_lower = target_val.lower()
    for rule in rules_list:
        matched_pattern = None
        for pat in rule.regex_patterns:
            if re.search(pat, target_lower):
                matched_pattern = pat
                break
        if matched_pattern:
            if not best_match or rule.priority > best_match[0].priority:
                best_match = (rule, matched_pattern)
    return best_match
