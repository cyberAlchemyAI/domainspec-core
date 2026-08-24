#!/usr/bin/env python3
"""Conformance validator for the ontology-vault canonical record contract.

Two jobs:
  1. PROJECT: mechanically derive (record_kind, record_version) from any of the
     five schema_version dialects found on disk.  Lossless and reversible.
  2. VALIDATE: check a record against the canonical envelope.

Run:  python3 validate_canonical.py <repo-root>
Stdlib only.  Read-only.
"""
import json, os, re, sys, collections

# ---------- the canonical envelope ----------
REQUIRED = ("record_kind", "record_version", "authority_effect",
            "owner_route", "source_identities", "emitted_by")
# `visibility` is OPTIONAL and DISTINCT from authority_effect.  On disk the 127
# authorityClass/authority_class files all carry the single value "private" (a
# visibility class) and NONE of them also carries authority_effect (an effect).
# Merging them would destroy a visibility fact and fabricate an effect claim.
VISIBILITY_ENUM = {"private", "public"}
KIND_RE  = re.compile(r"^[a-z0-9]+(\.[a-z0-9]+(-[a-z0-9]+)*)+$")
VER_RE   = re.compile(r"^v[0-9]+(\.[0-9]+)*$")
# Closed enum, widened to the values actually observed in the corpus.  Two on-disk
# values are free text ("blocked", "review-dispatch-only; no product ...") and are
# exactly the drift a closed enum stops.
AUTHORITY_ENUM = {"none", "owner-decision", "protected-production-deployment",
                  "bounded-execution-intent-only", "refine-planning-only",
                  "planning-only"}

# ---------- dialect projection ----------
SEMVER = re.compile(r"^(?P<v>\d+\.\d+(\.\d+)?)$")            # 1.0.0
SLASH  = re.compile(r"^(?P<id>[^/]+)/(?P<v>v?\d[\w.\-]*)$")   # body-war-business-node/v1
AT     = re.compile(r"^(?P<id>[^@]+)@(?P<v>\d[\w.\-]*)$")     # augmentor.x@0.1.0
DOTV   = re.compile(r"^(?P<id>.+)\.(?P<v>v\d[\w.\-]*)$")      # animejs.x.v1

def project(sv, fallback_kind=None):
    """schema_version string -> (kind, version, form).  kind None => not derivable."""
    if not isinstance(sv, str) or not sv.strip():
        return (None, None, "absent")
    sv = sv.strip()
    if SEMVER.match(sv):                       # carries NO identity
        return (fallback_kind, "v" + SEMVER.match(sv).group("v"), "bare-semver")
    m = SLASH.match(sv)
    if m and "/" not in m.group("id"):
        v = m.group("v")
        form = "hybrid" if "." in m.group("id") else "slash"
        return (m.group("id"), v if v.startswith("v") else "v" + v, form)
    m = AT.match(sv)
    if m:
        return (m.group("id"), "v" + m.group("v"), "at-sign")
    m = DOTV.match(sv)
    if m:
        return (m.group("id"), m.group("v"), "dot")
    return (None, None, "unparseable")

def normalize_kind(k):
    """slash/hyphen identities -> dotted canonical kind."""
    return None if k is None else k.replace("/", ".").lower()

# ---------- validation ----------
def validate(rec):
    bad = []
    for f in REQUIRED:
        if f not in rec:
            bad.append(f"missing:{f}")
    if "record_kind" in rec and not KIND_RE.match(str(rec["record_kind"])):
        bad.append(f"record_kind-malformed:{rec['record_kind']}")
    if "record_version" in rec and not VER_RE.match(str(rec["record_version"])):
        bad.append(f"record_version-malformed:{rec['record_version']}")
    if rec.get("authority_effect") not in AUTHORITY_ENUM and "authority_effect" in rec:
        bad.append(f"authority_effect-not-in-enum:{rec['authority_effect']}")
    if "visibility" in rec and rec["visibility"] not in VISIBILITY_ENUM:
        bad.append(f"visibility-not-in-enum:{rec['visibility']}")
    if "authorityClass" in rec or "authority_class" in rec:
        bad.append("authorityClass-must-map-to-visibility-not-authority_effect")
    if "ownerBoundaryResult" in rec:
        bad.append("ownerBoundaryResult-is-a-check-result-not-an-owner")
    si = rec.get("source_identities")
    if "source_identities" in rec and (not isinstance(si, dict) or not si):
        bad.append("source_identities-empty-or-not-object")
    return bad

# ---------- corpus sweep ----------
DIRS = ["projects/augmentor/ontology", "projects/body-war/ontology",
        "cyberAlchemy-v2/ontology", "projects/animejs/ontology",
        "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/ontology"]

def main(root):
    forms = collections.Counter()
    per   = collections.defaultdict(collections.Counter)
    undecidable = collections.defaultdict(list)
    for d in DIRS:
        base = os.path.join(root, d)
        if not os.path.isdir(base):
            print(f"!! missing {d}"); continue
        for dp, _, fn in os.walk(base):
            for f in fn:
                if not f.endswith(".json"): continue
                try: rec = json.load(open(os.path.join(dp, f)))
                except Exception: continue
                if not isinstance(rec, dict): continue
                per[d]["records"] += 1
                sv = rec.get("schema_version")
                kind, ver, form = project(sv)
                forms[form] += 1; per[d][form] += 1
                if form in ("absent", "bare-semver", "unparseable"):
                    per[d]["needs-authoring"] += 1
                    if len(undecidable[d]) < 2:
                        undecidable[d].append(os.path.relpath(os.path.join(dp, f), root))
                else:
                    ck = normalize_kind(kind)
                    if ck and KIND_RE.match(ck) and VER_RE.match(ver):
                        per[d]["auto-derivable"] += 1
                    else:
                        per[d]["derived-but-malformed"] += 1

    print("== dialect projection over 5 directories ==")
    print("forms:", dict(forms))
    for d in DIRS:
        c = per[d]
        print(f"\n{d}\n  records={c['records']} auto-derivable={c['auto-derivable']} "
              f"needs-authoring={c['needs-authoring']} malformed={c['derived-but-malformed']}")
        if undecidable[d]: print("   e.g. undecidable:", undecidable[d][0])

    # --- unit checks: one real value from each of the 5 grammars ---
    print("\n== projection unit checks (real on-disk values) ==")
    cases = [
        ("body-war-business-node/v1",                    "body-war-business-node", "v1",   "slash"),
        ("animejs.agent-knowledge-vault.nodes.v1",       "animejs.agent-knowledge-vault.nodes", "v1", "dot"),
        ("arcanum.background-helper-receipt/v1",         "arcanum.background-helper-receipt", "v1", "hybrid"),
        ("augmentor.consultation.task-context@0.1.0",    "augmentor.consultation.task-context", "v0.1.0", "at-sign"),
        ("1.0.0",                                        None, "v1.0.0", "bare-semver"),
        ("domainspec.ontology-vault.validation.v1",      "domainspec.ontology-vault.validation", "v1", "dot"),
    ]
    ok = True
    for sv, ek, ev, ef in cases:
        k, v, f = project(sv)
        good = (k == ek and v == ev and f == ef)
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {sv!r:52} -> ({k!r}, {v!r}, {f})")

    # --- envelope checks ---
    print("\n== envelope validation ==")
    conforming = {"record_kind": "domainspec.ontology-vault.validation",
                  "record_version": "v1", "authority_effect": "none",
                  "owner_route": "projects/cyberalchemy-orchestrator/docs/.../ontology",
                  "source_identities": {"target_git_head": "b42228fc"},
                  "emitted_by": "arcanum/arcana/ontology-vault"}
    print("  conforming record ->", validate(conforming) or "PASS (no violations)")
    for label, mut in [("slash left in kind", {"record_kind": "body-war-business-node/v1"}),
                       ("authority outside enum", {"authority_effect": "promotes"}),
                       ("free-text authority", {"authority_effect": "review-dispatch-only; no product"}),
                       ("empty source_identities", {"source_identities": {}}),
                       ("bare semver version", {"record_version": "1.0.0"}),
                       ("authorityClass merged in", {"authorityClass": "private"}),
                       ("ownerBoundaryResult as owner", {"ownerBoundaryResult": "pass"})]:
        r = dict(conforming); r.update(mut)
        v = validate(r)
        print(f"  {label:24} -> {'REJECTED ' + str(v) if v else 'ACCEPTED (BUG)'}")
        ok &= bool(v)
    print("\nRESULT:", "ALL CHECKS PASS" if ok else "FAILURES PRESENT")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
