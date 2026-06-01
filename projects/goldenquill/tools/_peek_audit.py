#!/usr/bin/env python3
import json, sys
p = "/Users/goldenquill/Downloads/GoldenQuill/pipeline/validation/bedrock_audit_2026-04-15/02_logician_audit.json"
d = json.load(open(p))

def hdr(s): print("\n=== " + s + " ===")

hdr("Summary")
print(json.dumps(d["summary"], indent=2))

hdr("routing_consistency")
print(json.dumps(d["checks"]["routing_consistency"], indent=2))

hdr("hardcoded_paths_in_tools (count + first 15)")
h = d["checks"]["hardcoded_paths_in_tools"]
print("count:", h["finding_count"])
for x in h["findings"][:15]:
    print(f"  {x['file']}:{x['line']} {x['text'][:110]}")

hdr("run_log_path_hygiene")
r = d["checks"]["run_log_path_hygiene"]
print("total_runs:", r.get("total_runs"),
      "stale:", r.get("stale_path_runs"),
      "canonical:", r.get("canonical_path_runs"))
for s in r.get("sample_stale", [])[:5]:
    print(f"  {s.get('run_id')}: {s.get('output')[:120]}")

hdr("topology_gate errors only")
t = d["checks"]["topology_gate"]
errs = [v for v in t.get("violations", []) if v.get("severity") == "ERROR"]
for e in errs:
    print(f"  [{e['rule']}] {e['path']}")
    print(f"    {e['detail']}")

hdr("recent_touches (first 20)")
rt = d["checks"]["recent_touches_fingerprint"]
print("touched_count:", rt["touched_count"])
for x in rt["touched"][:20]:
    print(f"  {x['mtime'][:19]}  {x['bytes']:>8}  {x['path']}")
