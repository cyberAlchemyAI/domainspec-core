#!/usr/bin/env python3
"""Render the human view of the ontology graph.

Usage:
    python3 docs/ontology/render.py [graph.json] [out.md]

The JSON graph is the source of truth. This markdown is a derived view and is
overwritten on every run — never edit it by hand.
"""
from __future__ import annotations

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "auth-domain-ontology.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "AUTH-DOMAIN-ONTOLOGY.md")

g = json.load(open(GRAPH))
nodes = {n["id"]: n for n in g["nodes"]}
by_role: dict[str, list] = collections.defaultdict(list)
for n in g["nodes"]:
    by_role[n["role"]].append(n)
edges_by_type: dict[str, list] = collections.defaultdict(list)
for e in g["edges"]:
    edges_by_type[e["type"]].append(e)

L: list[str] = []
w = L.append


def esc(s) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def ev(item) -> str:
    return " · ".join(f"`{e}`" for e in item.get("evidence", []))


run = g["run"]
w("---")
w(f"id: {g['ontology_id']}")
w("feature: auth-access-control")
w("title: Auth Access Control Business Domain Ontology")
w("summary: Human view of the business-domain ontology graph — concepts, typed relations, rules, "
  "confidence, and findings.")
w(f"status: {g['status']}")
w("pillar: platform")
w("domain: auth-access-control-ontology")
w("audience:")
w("  - developers")
w("  - operations")
w("priority: p1")
w("lang: en")
w("owners:")
w("  - platform-core")
w(f"updatedAt: {g['generated_at'][:10]}")
w("dependencies:")
w("  - ../auth-access-control/SPEC.md")
w("includes: []")
w("---")
w("")
w("# Auth Access Control — Business Domain Ontology")
w("")
w("> **GENERATED — DO NOT EDIT.**")
w(f"> Source of truth: [`{g['source_of_truth']}`]({os.path.basename(g['source_of_truth'])}) ")
w("> Regenerate with `python3 docs/ontology/render.py`; validate with "
  "`python3 docs/ontology/validate.py`.")
w("")
for note in g.get("notes", []):
    w(f"> {note}")
w("")

# ------------------------------------------------------------------- run
w("## Run")
w("")
w("| Field | Value |")
w("| ----- | ----- |")
w(f"| Ontology type | `{run['ontology_type']}` |")
w(f"| Selection source | {run['type_selection_source']} (confidence: {run.get('selection_confidence')}) |")
w(f"| Rejected candidates | {', '.join('`%s`' % c for c in run['ambiguity_candidates'] if c != run['ontology_type'])} |")
w(f"| Branch | `{run['branch']}` |")
w(f"| Mode | `{run['mode']}` |")
w(f"| Runtime | {run.get('runtime_mode')} (profile: {run.get('runtime_profile') or 'none'}) |")
w(f"| Knowledge inflection | **{run.get('knowledge_inflection')}** — {run.get('knowledge_inflection_rationale')} |")
w(f"| Graph size | {len(g['nodes'])} nodes · {len(g['edges'])} edges · {len(g['findings'])} findings |")
w("")

# ----------------------------------------------------------------- scope
w("## Scope")
w("")
w("**In scope (business branch):** " + ", ".join(g["scope"]["in_scope"]) + ".")
w("")
w("**Out of scope for this run:**")
w("")
for item in g["scope"]["out_of_scope"]:
    w(f"- {item['item']} — {item['reason']}.")
w("")
w("**Declared outside the domain** (the package disclaims these):")
w("")
w("| Concern | Evidence |")
w("| ------- | -------- |")
for item in g["scope"].get("out_of_domain", []):
    w(f"| {esc(item['concern'])} | `{item['evidence']}` |")
w("")

# --------------------------------------------------------------- sources
w("## Sources")
w("")
w("| Source | Branch | Read | Used for |")
w("| ------ | ------ | ---- | -------- |")
for s in g["sources"]:
    w(f"| `{s['path']}` | {s['branch']} | {s['read']} | {esc(s['used_for'])} |")
w("")
w("Not read as evidence: " + ", ".join(f"`{p}`" for p in g.get("sources_not_read", [])) + ".")
w("")

# ------------------------------------------------------- local vocabulary
if g.get("local_aliases"):
    w("## Local Label → Generic Concept")
    w("")
    w(f"{g.get('alias_policy', '')}")
    w("")
    w("| Local label | Generic concept |")
    w("| ----------- | --------------- |")
    for a in g["local_aliases"]:
        w(f"| {esc(a['local'])} | `{a['generic']}` |")
    w("")

# ------------------------------------------------------------ role catalog
w("## Node Roles")
w("")
w("| Role | Count | Meaning |")
w("| ---- | ----- | ------- |")
for r in g["node_roles"]:
    w(f"| `{r['id']}` | {len(by_role.get(r['id'], []))} | {esc(r['description'])} |")
w("")

# ------------------------------------------------------------ node inventory
ROLE_ORDER = ["actor", "capability", "entity", "value_object", "enumeration", "error_code",
              "permission_key", "behavior", "read_model", "lifecycle", "lifecycle_state",
              "domain_event", "decision_policy", "orchestration", "constraint", "business_rule",
              "derivation_rule", "guarantee", "acceptance_claim", "decision", "boundary_concept"]

w("## Concept Inventory")
w("")
w("Concept IDs reuse the existing `auth-access-control.*` registry namespace. "
  "`spec` marks membership in `SPEC.md#concept-registry`; this ontology invents no competing "
  "authority namespace.")
w("")
for role in ROLE_ORDER:
    items = sorted(by_role.get(role, []), key=lambda n: n["id"])
    if not items:
        continue
    w(f"### {role.replace('_', ' ').title()} ({len(items)})")
    w("")
    w("| ID | Label | Summary | Flags | Evidence |")
    w("| -- | ----- | ------- | ----- | -------- |")
    for n in items:
        flags = []
        if n.get("spec_registered") is True:
            flags.append("spec")
        if n.get("status") == "referenced-undefined":
            flags.append("**referenced-undefined**")
        if n.get("status") == "unregistered":
            flags.append("**unregistered**")
        if n.get("terminal"):
            flags.append("terminal")
        if n.get("enumerated") is False:
            flags.append("**out-of-enum**")
        if n.get("in_domain") is False:
            flags.append("**disclaimed**")
        if n.get("commitment"):
            flags.append(n["commitment"])
        if n.get("finding_ref"):
            flags.append(f"[{n['finding_ref']}](#{n['finding_ref'].lower()})")
        summary = esc(n["summary"])
        if n.get("formal"):
            summary += f" — `{esc(n['formal'])}`"
        w(f"| `{n['id']}` | {esc(n['label'])} | {summary} | {' · '.join(flags)} | {ev(n)} |")
    w("")

    # Field tables for structural concepts.
    for n in items:
        if n.get("fields"):
            w(f"**`{n['id']}` fields** (identity: {n.get('identity', 'n/a')})")
            w("")
            w("| Field | Type | Required | Domain / constraint | Note |")
            w("| ----- | ---- | -------- | ------------------- | ---- |")
            for f in n["fields"]:
                dom = f.get("domain") or f.get("constraint") or ""
                if isinstance(dom, list):
                    dom = ", ".join(f"`{d}`" for d in dom)
                req = {True: "yes", False: "no"}.get(f.get("required"), "—")
                w(f"| `{f['name']}` | `{f.get('type','')}` | {req} | {esc(dom)} | {esc(f.get('note',''))} |")
            w("")

# ------------------------------------------------------------ relation catalog
w("## Typed Relations")
w("")
bridge = g["indexes"]["counts"].get("bridge_edges", 0)
w(f"Bridge edges present: **{bridge}**. "
  "Realization, coverage, observation, and drift edges require system-branch evidence, "
  "which this run did not read.")
w("")
w("| Edge type | Count | From roles | To roles | Meaning |")
w("| --------- | ----- | ---------- | -------- | ------- |")
for t in g["edge_types"]:
    w(f"| `{t['id']}` | {len(edges_by_type.get(t['id'], []))} | "
      f"{', '.join(t['from_roles'])} | {', '.join(t['to_roles'])} | {esc(t['description'])} |")
w("")

for t in g["edge_types"]:
    items = edges_by_type.get(t["id"], [])
    if not items:
        continue
    w(f"### `{t['id']}` ({len(items)})")
    w("")
    w("| From | To | Detail | Evidence |")
    w("| ---- | -- | ------ | -------- |")
    for e in sorted(items, key=lambda x: (x["from"], x["to"])):
        detail = []
        for k in ("trigger", "guard", "effect", "reason", "note"):
            if e.get(k):
                detail.append(f"{k}: {esc(e[k])}")
        if e.get("finding_ref"):
            detail.append(f"[{e['finding_ref']}](#{e['finding_ref'].lower()})")
        w(f"| `{e['from']}` | `{e['to']}` | {' · '.join(detail)} | {ev(e)} |")
    w("")

# --------------------------------------------------------------- findings
w("## Findings")
w("")
counts = g["indexes"]["counts"]
def plural(count: int, word: str) -> str:
    return f"{count} {word}{'' if count == 1 else 's'}"


w(f"**{plural(counts['blockers'], 'blocker')} · {plural(counts['flags'], 'flag')} · "
  f"{plural(counts['notes'], 'note')}.** "
  "Every finding is a defect **between documents** on the business branch. None asserts anything "
  "about the implementation.")
w("")
w("| ID | Severity | Summary | Action | Owner route |")
w("| -- | -------- | ------- | ------ | ----------- |")
for f in g["findings"]:
    w(f"| [{f['id']}](#{f['id'].lower()}) | **{f['severity']}** | {esc(f['summary'])} | "
      f"`{f['recommended_action']}` | {f.get('owner_route', '—')} |")
w("")
for f in g["findings"]:
    w(f"### {f['id']}")
    w("")
    w(f"**{f['severity'].upper()} · {f['kind']} · {f['status']}** — {f['summary']}")
    w("")
    w(f["detail"])
    w("")
    if f["subjects"]:
        w("**Subjects:** " + ", ".join(f"`{s}`" for s in f["subjects"]))
        w("")
    w("**Evidence:** " + ev(f))
    w("")
    w(f"**Consequence:** {f['consequence']}")
    w("")
    w(f"**Recommended action:** `{f['recommended_action']}`"
      + (f" → owner route `{f['owner_route']}`" if f.get("owner_route") else ""))
    w("")
    if f.get("note"):
        w(f"**Note:** {f['note']}")
        w("")

if g.get("intentional_asymmetries"):
    w("## Intentional Asymmetries")
    w("")
    w("Recorded so a later pass does not re-open them as defects.")
    w("")
    for a in g["intentional_asymmetries"]:
        w(f"- **{a['id']}** — {a['summary']} *Rationale:* {a['rationale']} ({ev(a)})")
    w("")

# ------------------------------------------------------------- confidence
w("## Confidence")
w("")
w("Evidence confidence and commitment confidence are tracked separately. "
  f"This document executes no promotion (`executes_promotion: "
  f"{str(g['promotion_policy']['executes_promotion']).lower()}`).")
w("")
w("| Cluster | Evidence | Commitment | Action | Rationale | Findings |")
w("| ------- | -------- | ---------- | ------ | --------- | -------- |")
for c in g["confidence_clusters"]:
    fnd = ", ".join(f"[{x}](#{x.lower()})" for x in c.get("findings", []))
    w(f"| {esc(c['label'])} | {c['evidence_confidence']} | {c['commitment_confidence']} | "
      f"`{c['action']}` | {esc(c['rationale'])} | {fnd} |")
w("")
pp = g["promotion_policy"]
w(f"**Promotions recommended:** {len(pp.get('promotions_recommended', []))} "
  f"({', '.join(pp.get('promotions_recommended', [])) or 'none'}). "
  f"**Demotions recommended:** {len(pp.get('demotions_recommended', []))}.")
w("")
if pp.get("note"):
    w(pp["note"])
    w("")

# --------------------------------------------------------------- boundaries
w("## What This Ontology Does Not Establish")
w("")
for item in g.get("does_not_establish", []):
    w(f"- {item}")
w("")

open(OUT, "w").write("\n".join(L) + "\n")
print(f"rendered {OUT} ({len(L)} lines) from {os.path.basename(GRAPH)}")
