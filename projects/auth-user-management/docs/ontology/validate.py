#!/usr/bin/env python3
"""Validate the ontology graph: schema, referential integrity, evidence, branch discipline.

Usage:
    python3 docs/ontology/validate.py [graph.json]

Run from the project root (projects/auth-user-management). Exits non-zero on error.
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
GRAPH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "auth-domain-ontology.json")
SCHEMA = os.path.join(HERE, "ontology.schema.json")

# Edge types that require evidence from both the business and system branches.
BRIDGE_EDGE_TYPES = {"realized_by", "tested_by", "observed_by", "drifts_from", "traced_to",
                     "depends_on", "constrained_by"}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


g = json.load(open(GRAPH))

# ---------------------------------------------------------------- 1. schema
try:
    import jsonschema

    schema = json.load(open(SCHEMA))
    validator = jsonschema.Draft202012Validator(schema)
    for e in sorted(validator.iter_errors(g), key=lambda x: list(x.path)):
        err(f"schema: {'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}")
except ImportError:  # pragma: no cover
    warn("schema: jsonschema not installed; structural checks only")

# ------------------------------------------------------- 2. node/edge identity
node_ids: set[str] = set()
for nd in g["nodes"]:
    if nd["id"] in node_ids:
        err(f"nodes: duplicate id {nd['id']}")
    node_ids.add(nd["id"])

edge_ids: set[str] = set()
for ed in g["edges"]:
    if ed["id"] in edge_ids:
        err(f"edges: duplicate id {ed['id']}")
    edge_ids.add(ed["id"])

role_ids = {r["id"] for r in g["node_roles"]}
for nd in g["nodes"]:
    if nd["role"] not in role_ids:
        err(f"nodes: {nd['id']} has undeclared role '{nd['role']}'")

# -------------------------------------------- 3. edge integrity and role rules
edge_types = {t["id"]: t for t in g["edge_types"]}
roles_of = {nd["id"]: nd["role"] for nd in g["nodes"]}

for ed in g["edges"]:
    if ed["type"] not in edge_types:
        err(f"edges: {ed['id']} uses undeclared type '{ed['type']}'")
        continue
    spec = edge_types[ed["type"]]
    for side, key in (("from", "from_roles"), ("to", "to_roles")):
        target = ed[side]
        if target not in node_ids:
            err(f"edges: {ed['id']} {side} '{target}' does not resolve to a node")
            continue
        allowed = spec[key]
        if "*" not in allowed and roles_of[target] not in allowed:
            err(f"edges: {ed['id']} {side} role '{roles_of[target]}' not allowed by "
                f"edge type '{ed['type']}' (allows {allowed})")

# ----------------------------------------------------- 4. finding cross-links
finding_ids = {f["id"] for f in g["findings"]}
for f in g["findings"]:
    for s in f["subjects"]:
        if s not in node_ids:
            err(f"findings: {f['id']} subject '{s}' does not resolve to a node")

for holder, items in (("nodes", g["nodes"]), ("edges", g["edges"])):
    for item in items:
        ref = item.get("finding_ref")
        if ref and ref not in finding_ids:
            err(f"{holder}: {item['id']} finding_ref '{ref}' does not resolve to a finding")

for cluster in g["confidence_clusters"]:
    for m in cluster["members"]:
        if m not in node_ids:
            err(f"confidence_clusters: {cluster['id']} member '{m}' does not resolve to a node")
    for fid in cluster.get("findings", []):
        if fid not in finding_ids:
            err(f"confidence_clusters: {cluster['id']} finding '{fid}' does not resolve")

for asym in g.get("intentional_asymmetries", []):
    for s in asym["subjects"]:
        if s not in node_ids:
            err(f"intentional_asymmetries: {asym['id']} subject '{s}' does not resolve to a node")

for pid in g.get("promotion_policy", {}).get("promotions_recommended", []):
    if pid not in {c["id"] for c in g["confidence_clusters"]}:
        err(f"promotion_policy: '{pid}' does not resolve to a confidence cluster")

# --------------------------------------------------- 5. evidence paths on disk
def evidence_paths(obj) -> list[str]:
    ev = obj.get("evidence", [])
    return ev if isinstance(ev, list) else [ev]


missing_evidence: collections.Counter = collections.Counter()
for group in ("nodes", "edges", "findings"):
    for item in g[group]:
        for ref in evidence_paths(item):
            path = ref.split("#", 1)[0]
            if not path:
                continue
            full = os.path.join(ROOT, path)
            if not (os.path.isfile(full) or os.path.isdir(full)):
                missing_evidence[path] += 1
                err(f"{group}: {item['id']} evidence path does not exist: {path}")
for src in g["sources"]:
    if not os.path.exists(os.path.join(ROOT, src["path"])):
        err(f"sources: {src['id']} path does not exist: {src['path']}")

# --------------------------------------------------------- 6. orphan detection
connected = {ed["from"] for ed in g["edges"]} | {ed["to"] for ed in g["edges"]}
orphans = sorted(nid for nid in node_ids if nid not in connected)
# Decisions and deferred scope legitimately stand alone until something cites them.
orphans = [o for o in orphans if roles_of[o] != "decision"]
for o in orphans:
    warn(f"orphan: {o} ({roles_of[o]}) has no incoming or outgoing edge")

# ------------------------------------------------------- 7. branch discipline
branch = g["run"]["branch"]
if branch == "business":
    for ed in g["edges"]:
        if ed["type"] in BRIDGE_EDGE_TYPES:
            err(f"branch: bridge edge type '{ed['type']}' present on a business-branch ontology "
                f"({ed['id']}); bridge claims need evidence from both branches")
    for src in g["sources"]:
        if src["branch"] == "system" and src["read"] != "none":
            err(f"branch: system-branch source '{src['id']}' was read on a business-branch run")
if g["indexes"]["counts"].get("bridge_edges", 0) != sum(
        1 for ed in g["edges"] if ed["type"] in BRIDGE_EDGE_TYPES):
    err("branch: indexes.counts.bridge_edges disagrees with the graph")

# ------------------------------- 8. spec_registered must match the SPEC registry
spec_md = os.path.join(ROOT, "docs/auth-access-control/SPEC.md")
registry: set[str] = set()
if os.path.isfile(spec_md):
    text = open(spec_md).read()
    m = re.search(r"^## Concept Registry\s*$(.*?)^## ", text, re.M | re.S)
    if m:
        for row in m.group(1).splitlines():
            cells = [c.strip() for c in row.split("|")]
            for c in cells:
                if re.fullmatch(r"auth-access-control\.[A-Za-z][A-Za-z0-9]*", c):
                    registry.add(c)
    else:
        warn("spec: could not locate '## Concept Registry' section in SPEC.md")
else:
    warn("spec: SPEC.md not found; skipping registry cross-check")

if registry:
    for nd in g["nodes"]:
        if nd.get("spec_registered") is True and nd["id"] not in registry:
            err(f"spec: {nd['id']} claims spec_registered but is absent from SPEC.md Concept Registry")
        if nd.get("spec_registered") is False and nd["id"] in registry:
            err(f"spec: {nd['id']} claims not spec_registered but IS in SPEC.md Concept Registry")
    modeled = {nd["id"] for nd in g["nodes"]}
    for rid in sorted(registry - modeled):
        warn(f"coverage: SPEC registry concept '{rid}' is not modeled as a node "
             f"(expected for system-branch concepts; confirm it is deliberate)")

# ------------------------------------------------------- 9. index freshness
by_role = collections.defaultdict(list)
for nd in g["nodes"]:
    by_role[nd["role"]].append(nd["id"])
expected_counts = {
    "nodes": len(g["nodes"]),
    "edges": len(g["edges"]),
    "findings": len(g["findings"]),
    "blockers": sum(1 for f in g["findings"] if f["severity"] == "blocker"),
    "flags": sum(1 for f in g["findings"] if f["severity"] == "flag"),
    "notes": sum(1 for f in g["findings"] if f["severity"] == "note"),
}
for k, v in expected_counts.items():
    if g["indexes"]["counts"].get(k) != v:
        err(f"indexes: counts.{k} is {g['indexes']['counts'].get(k)}, recomputed {v} — regenerate indexes")
for role, ids in by_role.items():
    if g["indexes"]["nodes_by_role"].get(role) != sorted(ids):
        err(f"indexes: nodes_by_role.{role} is stale — regenerate indexes")

# ------------------------------------------------- 10. authority non-collapse
if g["authority_effect"] != "none":
    err("authority: an ontology graph must declare authority_effect 'none'")
if g.get("promotion_policy", {}).get("executes_promotion") is not False:
    err("authority: an ontology map must not execute promotions")

# ------------------------------------------------------------------- report
print(f"graph:    {os.path.relpath(GRAPH, ROOT)}")
print(f"nodes:    {len(g['nodes'])}  edges: {len(g['edges'])}  findings: {len(g['findings'])}")
print(f"roles:    {len(role_ids)}  edge types: {len(edge_types)}")
print(f"branch:   {branch}  bridge edges: {sum(1 for e in g['edges'] if e['type'] in BRIDGE_EDGE_TYPES)}")
print()
for w in warnings:
    print(f"WARN  {w}")
if warnings:
    print()
for e in errors:
    print(f"ERROR {e}")
print()
print(f"result: {'FAIL' if errors else 'PASS'}  ({len(errors)} errors, {len(warnings)} warnings)")
sys.exit(1 if errors else 0)
