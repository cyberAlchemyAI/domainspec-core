#!/usr/bin/env python3
"""Owner-declared conformance validator.

Verifies conformance across >=3 owner dialects WITHOUT imposing any key.

Mechanism: a READ-SIDE alias table maps each owner's own spelling to a generic
concept. This is the executable form of ontology-vault SKILL.md Step 1 clauses
11-12 ("Translate local labels into generic Arcanum concepts" / "Preserve local
label names as aliases only when reporting ... Do not promote local labels into
canonical Arcanum vocabulary"). Owners are never asked to emit anything.

Falsifiable properties, checked per owner package:
  P1 single-spelling   : within a package, each concept has <=1 spelling.
  P2 id-denotes-one-shape: each dialect-id value denotes one record shape.
                         (Grammar uniformity is NOT required: a reader keyed on
                         the full dialect-id string never parses the grammar.)
  P3 no-homonym        : no single file carries two spellings of one concept.
  P4 resolvable        : the package's dialect is covered by the read table;
                         unresolved spellings are READER coverage gaps, not
                         owner defects.

If P1-P3 hold across >=3 dialects, cross-dialect reading is achievable by a
read-side table alone, and no imposed key is required. A package that fails
P1-P3 falsifies that claim for that package.
"""

import json
import os
import re
import sys
from collections import defaultdict

# READ-SIDE ONLY. Adding a row here changes the reader, never an owner's files.
# Aliases are PATH-aware: a concept may be carried flat ("authority_effect")
# or nested ("authority"."effect"). A flat-key-only reader miscounts nested
# carriers as absent and miscounts sibling concepts as rival spellings.
ALIASES = {
    "dialect_id":      ["schema_version", "schemaVersion", "schema"],
    "json_schema_ref": ["$schema"],
    "artifact_version": ["version"],
    "authority_effect": ["authority_effect", "authorityEffect",
                         "authority.effect"],
    "authority_class":  ["authorityClass", "authority_class",
                         "authority.class"],
    "owner_ref":       ["owner_route", "ownerRoute", "lifecycleOwner",
                        "lifecycle_owner", "owner_identity", "next_owner",
                        "ownerBoundaryResult"],
    "owner_table":     ["owner_routes", "ownership"],
}
SPELLING_TO_CONCEPT = {s: c for c, ss in ALIASES.items() for s in ss}

# Concepts whose disagreement would actually break a cross-dialect read.
INTEROP_CONCEPTS = ("dialect_id", "authority_effect", "owner_ref")

SKIP = re.compile(
    r"/(development|task-sessions|refinement-runs|invoke-runs|migrations|"
    r"history|staged|stage|outputs|materials|proofs|node_modules|\.git)/"
)


def grammar(value):
    """Classify a version value's grammar without ranking either as correct."""
    if not isinstance(value, str):
        return "non-string"
    if value.startswith("http") or value.startswith("urn:"):
        return "uri"
    if "@" in value:
        return "at"
    if "/" in value:
        return "slash"
    if "." in value:
        return "dot"
    return "bare"


def walk_keys(obj, out, depth=0, parent=""):
    """Collect key spellings path-aware, so nested carriers are visible."""
    if depth > 40:
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            dotted = f"{parent}.{k}" if parent else k
            # register both the bare key and the one-level-nested path
            out.append((k, v))
            if parent:
                out.append((dotted, v))
            walk_keys(v, out, depth + 1, k)
    elif isinstance(obj, list):
        for v in obj:
            walk_keys(v, out, depth + 1, parent)


def scan_package(pkg_dir):
    """Derive one owner's dialect from that owner's own files."""
    spellings = defaultdict(set)       # concept -> spellings used
    grammars = defaultdict(set)        # concept -> value grammars used
    examples = defaultdict(set)        # grammar -> example values
    shapes = defaultdict(set)          # dialect_id value -> top-level keysets
    homonyms = []                      # files carrying 2 spellings of 1 concept
    unresolved = defaultdict(int)      # reader coverage gaps
    files = 0

    for root, dirs, names in os.walk(pkg_dir):
        if SKIP.search(root + "/"):
            dirs[:] = []
            continue
        for name in names:
            if not name.endswith(".json") or name.endswith(".schema.json"):
                continue
            path = os.path.join(root, name)
            try:
                with open(path, encoding="utf-8") as fh:
                    doc = json.load(fh)
            except Exception:
                continue
            files += 1
            if isinstance(doc, dict):
                did = (doc.get("schema_version") or doc.get("schema")
                       or doc.get("schemaVersion"))
                if isinstance(did, str):
                    shapes[did].add(",".join(sorted(doc.keys())))
            pairs = []
            walk_keys(doc, pairs)
            per_file = defaultdict(set)
            for key, value in pairs:
                concept = SPELLING_TO_CONCEPT.get(key)
                if concept is None:
                    meta = ("." in key or ":" in key
                            or key in ("const", "enum", "type", "minLength",
                                       "items", "properties"))
                    if not meta and re.fullmatch(
                            r"(owner|authority|schema|version)[_A-Za-z]*",
                            key, re.I):
                        unresolved[key] += 1
                    continue
                spellings[concept].add(key)
                per_file[concept].add(key)
                if concept == "dialect_id":
                    g = grammar(value)
                    if g not in ("non-string", "uri"):
                        grammars[concept].add(g)
                        if len(examples[g]) < 3:
                            examples[g].add(value)
            for concept, used in per_file.items():
                if len(used) > 1:
                    homonyms.append((path, concept, sorted(used)))

    return {
        "dir": pkg_dir,
        "files": files,
        "spellings": {c: sorted(s) for c, s in spellings.items()},
        "grammars": {c: sorted(g) for c, g in grammars.items()},
        "homonyms": homonyms,
        "unresolved": dict(unresolved),
        "examples": {g: sorted(v) for g, v in examples.items()},
        "shapes": {k: v for k, v in shapes.items()},
    }


def main(packages):
    results = [scan_package(p) for p in packages]
    dialect_sigs = set()
    verdicts = []

    for r in results:
        p1 = all(len(r["spellings"].get(c, [])) <= 1
                 for c in INTEROP_CONCEPTS)
        ambiguous = {k: v for k, v in r["shapes"].items() if len(v) > 1}
        p2 = not ambiguous
        p3 = not [h for h in r["homonyms"] if h[1] in INTEROP_CONCEPTS]
        p4 = not r["unresolved"]
        sig = json.dumps({c: r["spellings"].get(c, [])
                           for c in INTEROP_CONCEPTS}, sort_keys=True)
        dialect_sigs.add(sig)
        verdicts.append((r, p1, p2, p3, p4))

        print(f"\n=== {r['dir']}  ({r['files']} json) ===")
        for concept in INTEROP_CONCEPTS:
            sp = r["spellings"].get(concept, [])
            print(f"  {concept:16s} spelling(s): {sp or ['<absent>']}")
        print(f"  version value grammar(s): "
              f"{r['grammars'].get('dialect_id', []) or ['<none>']}")
        for g, vals in sorted(r["examples"].items()):
            print(f"      {g:6s} e.g. {vals[:2]}")
        print(f"  P1 single-spelling   : {'PASS' if p1 else 'FAIL'}")
        print(f"  distinct dialect-ids    : {len(r['shapes'])}")
        print(f"  P2 id-denotes-one-shape: {'PASS' if p2 else 'FAIL'} "
              f"{sorted(ambiguous)[:2] if ambiguous else ''}")
        print(f"  P3 no-homonym        : {'PASS' if p3 else 'FAIL'} "
              f"({len([h for h in r['homonyms'] if h[1] in INTEROP_CONCEPTS])}"
              f" file(s))")
        print(f"  P4 reader-resolvable : {'PASS' if p4 else 'GAP'} "
              f"{sorted(r['unresolved']) if r['unresolved'] else ''}")

    print("\n" + "=" * 62)
    print(f"distinct dialects observed : {len(dialect_sigs)}")
    core_ok = all(p1 and p3 for _, p1, _, p3, _ in verdicts)
    print(f"packages scanned           : {len(results)}")
    print(f"P1+P3 hold in every package: {core_ok}")
    if len(dialect_sigs) >= 3 and core_ok:
        print("VERDICT: >=3 dialects read correctly with ZERO imposed keys.")
        print("         Read-side aliasing is sufficient; imposition is not "
              "required for conformance checking.")
        return 0
    print("VERDICT: claim falsified or dialect count insufficient.")
    return 1


if __name__ == "__main__":
    root = "/home/vrondelli/projects/domainspec-core"
    # The five canonical owner packages cited in receipt.md. cyberAlchemy-v2
    # /ontology is deliberately absent: it holds ZERO json outside
    # development/ -- its ontology surface is markdown, not record-per-file.
    default = [
        f"{root}/projects/body-war/ontology/business",
        f"{root}/projects/body-war/ontology/whole-system",
        f"{root}/projects/augmentor/ontology/unified-agent",
        f"{root}/projects/animejs/ontology/agent-knowledge-vault",
        f"{root}/projects/cyberalchemy-orchestrator/docs/features/"
        f"recursive-work-orchestrator/ontology",
    ]
    sys.exit(main(sys.argv[1:] or default))
