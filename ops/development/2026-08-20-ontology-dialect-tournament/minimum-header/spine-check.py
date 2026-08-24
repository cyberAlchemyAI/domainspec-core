#!/usr/bin/env python3
"""spine-check: verify the 3-concept spine across N dialects WITHOUT renaming any file.

Design invariant (this is the whole argument):
  the sigil owns the three CONCEPTS; each owner owns its SPELLING and its VALUE SPACE.
  The alias table below is OWNER-DECLARED, not sigil-imposed. Adding a dialect is one
  table row, not a migration. That is why this validator can exist without collapsing
  owner authority.

Usage: python3 spine-check.py <root> [dialect ...]
"""
import json, os, re, sys, collections

# --- owner-declared dialect registry -------------------------------------------------
# Each owner declares, for each of the 3 concepts, which local key carries it.
# `None` = this owner does not carry that concept (a legitimate, reportable state).
DIALECTS = {
    "body-war": {
        "root": "projects/body-war/ontology",
        "type_id": ["schema_version"],
        "authority_effect": ["authority_effect"],
        "owner_route": ["owner_route"],
    },
    "augmentor": {
        "root": "projects/augmentor/ontology",
        "type_id": ["schema_version", "schemaVersion"],
        "authority_effect": ["authority_effect"],
        "owner_route": ["owner_route", "lifecycleOwner", "lifecycle_owner", "next_owner"],
    },
    "cav2": {
        "root": "cyberAlchemy-v2/ontology",
        "type_id": ["schema_version"],
        "authority_effect": ["authority_effect"],
        "owner_route": None,
    },
    "orchestrator": {
        "root": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/ontology",
        "type_id": ["schema_version"],
        "authority_effect": ["authority_effect"],
        "owner_route": ["owner_route", "owner_identity"],
    },
    "animejs": {
        "root": "projects/animejs/ontology",
        "type_id": ["schema_version"],
        "authority_effect": ["authority_effect"],
        "owner_route": None,
    },
}

# NOT aliases. Verified distinct value spaces; kept here so the validator can say so.
NOT_ALIASES = {
    "authorityClass": ("authority_effect", "values are {private} = a visibility class, "
                       "disjoint from authority_effect's effect vocabulary"),
    "authority_class": ("authority_effect", "same as authorityClass"),
    "ownerBoundaryResult": ("owner_route", "values are {pass,reject} = a check result, not an owner"),
}

BARE = re.compile(r"^\d+(?:\.\d+)*$")
# The typed grammars differ in ARITY as well as separator, so the normalizer needs both:
#   3-segment: ns<sep>name<sep>vN      e.g. rwo.current-state-evidence.v1
#   2-segment: name<sep>vN             e.g. rwo-architecture-property-ontology/v1
# Version tail may be v1, v0.1, or @1.0.0. Namespace is OPTIONAL -> normal form is
# (namespace|None, name, version).
TYPED3 = re.compile(r"^(?P<ns>[A-Za-z0-9_-]+)[./](?P<name>.+?)[./@]v?(?P<ver>\d+(?:\.\d+)*)$")
TYPED2 = re.compile(r"^(?P<name>[A-Za-z0-9_-]+)[./@]v?(?P<ver>\d+(?:\.\d+)*)$")


def classify_type_id(v):
    """-> (status, normalized_or_reason). Status in OK | HOMONYM | UNPARSED."""
    if not isinstance(v, str):
        return "UNPARSED", "non-string"
    if BARE.match(v):
        # Same key, different CONCEPT: a document version with no type identity.
        return "HOMONYM", v
    m = TYPED2.match(v)
    if m:  # 2-segment: no namespace declared
        return "OK", (None, m.group("name"), m.group("ver"))
    m = TYPED3.match(v)
    if m:
        return "OK", (m.group("ns"), m.group("name"), m.group("ver"))
    return "UNPARSED", v


def first_present(obj, keys):
    if not keys:
        return None, None
    for k in keys:
        if k in obj:
            return k, obj[k]
    return None, None


def scan(root, name, spec):
    base = os.path.join(root, spec["root"])
    r = collections.Counter()
    grammars = collections.Counter()
    misfiled = collections.Counter()
    for dp, _, fns in os.walk(base):
        for fn in fns:
            if not fn.endswith(".json"):
                continue
            p = os.path.join(dp, fn)
            try:
                o = json.load(open(p))
            except Exception:
                r["unparsable"] += 1
                continue
            if not isinstance(o, dict):
                continue
            r["records"] += 1

            k, v = first_present(o, spec["type_id"])
            if k is None:
                r["type_id.absent"] += 1
            else:
                st, norm = classify_type_id(v)
                r["type_id." + st] += 1
                if st == "OK":
                    sep = "slash" if "/" in v else ("@" if "@" in v else "dot")
                    arity = "3seg" if norm[0] else "2seg"
                    grammars["%s/%s/%s" % (norm[0] or "(no-ns)", sep, arity)] += 1

            for concept in ("authority_effect", "owner_route"):
                k2, _ = first_present(o, spec[concept] or [])
                if spec[concept] is None:
                    r[concept + ".not-declared"] += 1
                elif k2 is None:
                    r[concept + ".absent"] += 1
                else:
                    r[concept + ".present"] += 1

            for bad, (concept, why) in NOT_ALIASES.items():
                if bad in o:
                    misfiled[bad] += 1
    return r, grammars, misfiled


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    want = sys.argv[2:] or list(DIALECTS)
    total = collections.Counter()
    print("spine-check: 3 concepts (type_id, authority_effect, owner_route) over %d dialects\n" % len(want))
    for name in want:
        spec = DIALECTS[name]
        r, g, mis = scan(root, name, spec)
        for k, v in r.items():
            total[k] += v
        print("== %s  (%s)" % (name, spec["root"]))
        print("   records                 %d" % r["records"])
        print("   type_id  OK/HOMONYM/ABS %d / %d / %d"
              % (r["type_id.OK"], r["type_id.HOMONYM"], r["type_id.absent"]))
        if r["type_id.UNPARSED"]:
            print("   type_id  UNPARSED       %d" % r["type_id.UNPARSED"])
        for c in ("authority_effect", "owner_route"):
            if spec[c] is None:
                print("   %-16s NOT DECLARED by this owner (reported, not failed)" % c)
            else:
                print("   %-16s present %d / absent %d  via %s"
                      % (c, r[c + ".present"], r[c + ".absent"], "|".join(spec[c])))
        if g:
            print("   grammars normalized:  %s" % ", ".join(
                "%s x%d" % (k, v) for k, v in g.most_common(4)))
        if mis:
            for b, n in mis.items():
                print("   NOT-AN-ALIAS: %s x%d -> %s" % (b, n, NOT_ALIASES[b][1]))
        print()

    print("== TOTAL across %d dialects" % len(want))
    print("   records %d" % total["records"])
    ok, hom, absent = total["type_id.OK"], total["type_id.HOMONYM"], total["type_id.absent"]
    seen = ok + hom + total["type_id.UNPARSED"]
    print("   type_id carried by %d records; %d normalize under ONE function (%.0f%%),"
          % (seen, ok, 100.0 * ok / seen if seen else 0))
    print("   %d are the bare-semver HOMONYM (same key, different concept)" % hom)
    print("   %d records carry no type_id at all" % absent)
    # The verdict this validator is FOR: a countable conformance number per dialect.
    print("\n   VERDICT: conformance is computable across all %d dialects with zero file"
          % len(want))
    print("            rewrites, because aliasing lives in the reader's table, not in the record.")


if __name__ == "__main__":
    main()
