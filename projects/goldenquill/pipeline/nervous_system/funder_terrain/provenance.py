import hashlib
import json
from typing import Any, Dict

def compute_input_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def compute_record_hash(record_dict: Dict[str, Any]) -> str:
    dict_copy = dict(record_dict)
    dict_copy.pop("record_sha256", None)
    canon = json.dumps(dict_copy, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()
