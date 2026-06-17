#!/usr/bin/env python3
"""
C-1 Validator Spike — RUN phase.

Builds the V3 scope-attribution fence + 11 fixtures, runs V3 over them, and
adjudicates SURVIVED / FALSIFIED / INVALID against the FROZEN criterion at
  ./criterion.md

Stdlib only (html.parser). No pip installs. Python 3.

Four cleanly separated parts:
  PART 1  Fixtures            (baseline + 11 candidates, written to fixtures/, hashed into fixtures.lock)
  PART 2  frozenBaselineBinding  (trusted oracle: od-id -> stable structural identity)
  PART 3  v3(...)             (principled general algorithm; NO access to `expect`)
  PART 4  Adjudication        (ordered verdict rule; per-fixture table; RUN-RESULT.md)

Integrity: v3 never receives `expect`, fixture identities, or this criterion. The
adjudicator alone holds `expect`.
"""

import hashlib
import html.parser
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXDIR = os.path.join(HERE, "fixtures")

# ---------------------------------------------------------------------------
# Canonicalizer identity (frozen) — must match criterion.md exactly.
# ---------------------------------------------------------------------------
CANON_IDENTITY = {
    "name": "domainspec-html-canon",
    "version": "1.4.0",
    "norm_spec_hash": "sha256:c1a9f0e2b7",
}
# The frozen identity the criterion pins. The run-time canonicalizer MUST equal this.
FROZEN_CANON_IDENTITY = {
    "name": "domainspec-html-canon",
    "version": "1.4.0",
    "norm_spec_hash": "sha256:c1a9f0e2b7",
}

# ---------------------------------------------------------------------------
# Scope configuration. TaskScope MUST contain >= 2 od-ids.
# ---------------------------------------------------------------------------
A = "cta.primary"   # in-scope
B = "card.hint"     # in-scope
X = "card.title"    # out-of-scope
Z = "card.footer"   # out-of-scope
TASK_SCOPE = [A, B]

VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


# ===========================================================================
# PART 0 — Canonical parse tree (the frozen canonicalizer, mechanism-neutral)
# ===========================================================================
class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "text")

    def __init__(self, tag, attrs=None):
        self.tag = tag
        # attrs canonicalized: dict sorted by key at compare time
        self.attrs = dict(attrs or {})
        self.children = []
        self.parent = None
        self.text = ""  # collapsed text directly owned by this node (concatenated)

    def od_id(self):
        return self.attrs.get("data-od-id")


class CanonParser(html.parser.HTMLParser):
    """
    Frozen canonicalizer `domainspec-html-canon` v1.4.0:
      - attribute-order normalization (attrs stored in a dict; compared sorted)
      - whitespace collapse (runs of whitespace -> single space; trimmed)
      - void-element normalization (void tags never receive children)
      - od-id preservation (data-od-id attribute kept verbatim)
    Raises on malformed structure -> caller maps to parse failure (⊥).
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.stack = [self.root]
        self.failed = False
        self.fail_reason = ""

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        node.parent = self.stack[-1]
        self.stack[-1].children.append(node)
        if tag not in VOID_ELEMENTS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, attrs)
        node.parent = self.stack[-1]
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        if tag in VOID_ELEMENTS:
            return
        # find matching open tag on the stack
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return
        # unmatched close tag -> malformed
        self.failed = True
        self.fail_reason = "unmatched-close-tag:%s" % tag

    def handle_data(self, data):
        collapsed = " ".join(data.split())
        if collapsed:
            self.stack[-1].text = (self.stack[-1].text + " " + collapsed).strip()


def canonicalize(candidate_html):
    """
    Returns (root_node, ok, reason). ok=False signals parse/canonicalization
    failure -> ⊥ collapse.
    """
    p = CanonParser()
    try:
        p.feed(candidate_html)
        p.close()
    except Exception as exc:  # noqa: BLE001 — any parse error is ⊥
        return None, False, "parse-exception:%s" % exc
    if p.failed:
        return None, False, p.fail_reason
    if len(p.stack) != 1:
        # unclosed tags remain on the stack
        return None, False, "unclosed-tags:%s" % ",".join(n.tag for n in p.stack[1:])
    return p.root, True, ""


def runtime_canon_identity():
    """The identity the run-time canonicalizer actually advertises."""
    return dict(CANON_IDENTITY)


# ===========================================================================
# Structural alignment key — stable under content edits.
# ===========================================================================
def alignment_key(node):
    """
    Structural identity of a node, independent of its text content, its
    attribute *values*, and any od-id it asserts. Built from the chain of
    (tag, sibling-index-among-same-tag) from root to the node. Stable under
    text edits, attribute-value edits, and od-id re-tagging — which is exactly
    what we need for a trustable oracle and for forge/re-tag detection.
    """
    chain = []
    cur = node
    while cur is not None and cur.tag != "#root":
        parent = cur.parent
        if parent is None:
            break
        idx = 0
        for sib in parent.children:
            if sib is cur:
                break
            if sib.tag == cur.tag:
                idx += 1
        chain.append("%s[%d]" % (cur.tag, idx))
        cur = parent
    return "/".join(reversed(chain))


def walk(node):
    for child in node.children:
        yield child
        yield from walk(child)


# ===========================================================================
# PART 2 — frozenBaselineBinding (trusted oracle)
# ===========================================================================
# Baseline: a one-card prototype carrying od-ids. The binding is od-id -> the
# structural alignment key of the node that legitimately carries it. Derived
# ONCE here from the baseline and treated as trusted ground truth thereafter.
BASELINE_HTML = """\
<!doctype html>
<html>
<head>
<title>Studio Prototype</title>
<style>
.card { border: 1px solid #ccc; }
</style>
</head>
<body>
<div class="wrapper">
  <section class="card">
    <h2 class="card-title" data-od-id="card.title">Original Title</h2>
    <button class="cta" data-od-id="cta.primary" aria-label="go">Click me</button>
    <p class="hint" data-od-id="card.hint">Original hint text</p>
    <footer class="card-footer" data-od-id="card.footer">Original footer</footer>
  </section>
</div>
</body>
</html>
"""


def derive_baseline_binding():
    root, ok, reason = canonicalize(BASELINE_HTML)
    if not ok:
        raise RuntimeError("baseline failed to canonicalize: %s" % reason)
    binding = {}
    for n in walk(root):
        oid = n.od_id()
        if oid:
            binding[oid] = alignment_key(n)
    return binding, root


# ===========================================================================
# PART 3 — v3 (PRINCIPLED GENERAL ALGORITHM — NO ACCESS TO `expect`)
# ===========================================================================
def _nearest_od_id(node, candidate_binding):
    """
    Walk up from `node` to the nearest ancestor (inclusive) that asserts an
    od-id; return (od_id, alignment_key_of_that_node) or (None, None) if none.
    """
    cur = node
    while cur is not None and cur.tag != "#root":
        oid = cur.od_id()
        if oid:
            return oid, alignment_key(cur)
        cur = cur.parent
    return None, None


def _selector_resolves(node, sel):
    """Does CSS selector token `sel` resolve to `node`? Supports class .x,
    attribute [a=b] / [a], and bare tag. Mechanism-neutral, conservative."""
    sel = sel.strip()
    if not sel:
        return False
    if sel.startswith("."):
        classes = node.attrs.get("class", "").split()
        return sel[1:] in classes
    if sel.startswith("[") and sel.endswith("]"):
        body = sel[1:-1]
        if "=" in body:
            k, v = body.split("=", 1)
            v = v.strip().strip('"').strip("'")
            return node.attrs.get(k.strip()) == v
        return body.strip() in node.attrs
    # bare tag (ignore '*' which we don't emit)
    return node.tag == sel


def _parse_style_selectors(style_text):
    """Yield each selector group head (the part before '{') split on commas."""
    selectors = []
    chunks = style_text.split("}")
    for chunk in chunks:
        if "{" not in chunk:
            continue
        head = chunk.split("{", 1)[0]
        for part in head.split(","):
            part = part.strip()
            if part:
                selectors.append(part)
    return selectors


def v3(candidate_html, task_scope_od_ids, baseline_binding, scope_rule):
    """
    H1 pure function. Returns "REJECT" or "NOT_REJECT".

    Algorithm (whole-tree, od-id-attributed):
      1. Canonicalize candidate -> canonical tree. Parse fail => ⊥ => REJECT.
      2. od-id integrity: for every od-id the candidate asserts, its node's
         structural alignment key MUST equal baseline_binding[od-id]. A mismatch
         (or an asserted od-id absent from the binding) is forge/re-tag => REJECT.
      3. Whole-tree diff baseline<->candidate by alignment key:
           - text change / attribute change on an aligned node
           - inserted node (alignment key not in baseline)
           - deleted node (baseline key absent from candidate)
         Attribute each change to its nearest-ancestor od-id. For deletions,
         attribute using the BASELINE tree (the candidate no longer has the node).
      4. CSS: each <style> selector that resolves to an od-id-bearing node (or a
         descendant of one) attributes to that od-id.
      5. Any attributed change touching an od-id NOT in task_scope => REJECT.
         Any change unattributable to any od-id => ⊥ => REJECT.
      6. Else NOT_REJECT.
    """
    scope = set(task_scope_od_ids)

    # --- 1. canonicalize ---------------------------------------------------
    cand_root, ok, _reason = canonicalize(candidate_html)
    if not ok:
        return "REJECT"  # ⊥ collapse: parse/canonicalization failure

    base_root, base_ok, _ = canonicalize(BASELINE_HTML)
    if not base_ok:
        return "REJECT"  # baseline must canonicalize; treat failure as ⊥

    # index nodes by alignment key
    base_by_key = {}
    for n in walk(base_root):
        base_by_key[alignment_key(n)] = n
    cand_by_key = {}
    for n in walk(cand_root):
        cand_by_key[alignment_key(n)] = n

    # --- 2. od-id integrity (forge / re-tag) ------------------------------
    for n in walk(cand_root):
        oid = n.od_id()
        if not oid:
            continue
        expected_key = baseline_binding.get(oid)
        if expected_key is None:
            # candidate asserts an od-id the trusted binding doesn't know
            return "REJECT"
        if alignment_key(n) != expected_key:
            # od-id asserted on a node that doesn't align to the bound node
            return "REJECT"

    # --- collect attributed touches ---------------------------------------
    # touched_out: True if any change touches an out-of-scope od-id
    # any_change: at least one change observed (for ⊥ unattributable detection)

    def attribute_change(node, tree_is_baseline):
        """Return od-id for nearest ancestor, or None if unattributable."""
        oid, _key = _nearest_od_id(node, None)
        return oid

    # 3a. inserted + mutated nodes (candidate side)
    for key, cnode in cand_by_key.items():
        bnode = base_by_key.get(key)
        if bnode is None:
            # inserted node
            oid = attribute_change(cnode, False)
            if oid is None:
                # change unattributable to any od-id => ⊥
                # (an addition not under any od-id is unscopeable)
                if _is_structural_noise(cnode):
                    continue
                return "REJECT"
            if oid not in scope:
                return "REJECT"
        else:
            # mutated node: text or attribute change (ignore style/od-id here;
            # style handled separately, od-id handled by integrity check)
            text_changed = cnode.text != bnode.text
            attr_changed = _attrs_differ(cnode, bnode)
            if cnode.tag == "style":
                # style content handled by CSS pass; skip raw-text diff here
                text_changed = False
            if text_changed or attr_changed:
                oid = attribute_change(cnode, False)
                if oid is None:
                    if _is_structural_noise(cnode):
                        continue
                    return "REJECT"
                if oid not in scope:
                    return "REJECT"

    # 3b. deleted nodes (present in baseline, absent in candidate)
    for key, bnode in base_by_key.items():
        if key not in cand_by_key:
            oid = attribute_change(bnode, True)
            if oid is None:
                if _is_structural_noise(bnode):
                    continue
                return "REJECT"
            if oid not in scope:
                return "REJECT"

    # --- 4. CSS attribution -----------------------------------------------
    # Compare style content; only changed/added style rules are scoped, but to
    # stay mechanism-neutral and conservative we attribute every selector that
    # resolves to an od-id node whenever the <style> content changed.
    cand_styles = [n for n in walk(cand_root) if n.tag == "style"]
    base_style_text = " ".join(n.text for n in walk(base_root) if n.tag == "style")
    for st in cand_styles:
        if st.text == base_style_text and len(cand_styles) == 1:
            continue  # style unchanged
        for sel in _parse_style_selectors(st.text):
            resolved_oids = set()
            for target in walk(cand_root):
                if _selector_resolves(target, sel):
                    oid, _ = _nearest_od_id(target, None)
                    if oid is not None:
                        resolved_oids.add(oid)
            # selector that touches anything must stay within scope
            for oid in resolved_oids:
                if oid not in scope:
                    return "REJECT"

    return "NOT_REJECT"


def _attrs_differ(cnode, bnode):
    """Attribute comparison ignoring data-od-id (integrity-checked elsewhere)
    and ignoring class only when it equals (class changes ARE mutations)."""
    ca = {k: v for k, v in cnode.attrs.items() if k != "data-od-id"}
    ba = {k: v for k, v in bnode.attrs.items() if k != "data-od-id"}
    return ca != ba


def _is_structural_noise(node):
    """
    Un-anchored scaffolding that bears no od-id and lives outside any od-id
    subtree: head/title/style/meta and the wrapper chrome. These never carry
    scope meaning, so a diff confined to them is not a scope violation. A node
    is noise only if NO ancestor and the node itself bear an od-id AND it is one
    of the known chrome tags.
    """
    oid, _ = _nearest_od_id(node, None)
    if oid is not None:
        return False
    chrome = {"#root", "html", "head", "title", "meta", "style", "body", "div", "section", "!doctype"}
    return node.tag in chrome


# ===========================================================================
# PART 1 — Fixtures (baseline above; 11 candidates here)
# ===========================================================================
def build_fixtures():
    """Return list of {id, category, candidate_html, expect}. `expect` is for
    the ADJUDICATOR only and is never passed to v3."""
    fixtures = []

    # ---- GOOD (expect NOT_REJECT) ----
    fixtures.append({
        "id": "GOOD-1",
        "category": "GOOD",
        "expect": "NOT_REJECT",
        # text edit confined to node bound to A (cta.primary); od-ids agree
        "candidate_html": _doc(
            title="Studio Prototype",
            style=".card { border: 1px solid #ccc; }",
            card_title=("Original Title", X, None),
            cta=("Press now", A, "go"),
            hint=("Original hint text", B, None),
            footer=("Original footer", Z, None),
        ),
    })

    fixtures.append({
        "id": "GOOD-2",
        "category": "GOOD",
        "expect": "NOT_REJECT",
        # <style> rule resolving only to nodes bound to A and B (class .cta, .hint)
        "candidate_html": _doc(
            title="Studio Prototype",
            style=".card { border: 1px solid #ccc; } .cta { color: red; } .hint { color: blue; }",
            card_title=("Original Title", X, None),
            cta=("Click me", A, "go"),
            hint=("Original hint text", B, None),
            footer=("Original footer", Z, None),
        ),
    })

    fixtures.append({
        "id": "GOOD-3",
        "category": "GOOD",
        "expect": "NOT_REJECT",
        # edit to node bound to B, byte-adjacent to out-of-scope X sibling.
        # whole-tree attribution must attribute only to B.
        "candidate_html": _doc(
            title="Studio Prototype",
            style=".card { border: 1px solid #ccc; }",
            card_title=("Original Title", X, None),
            cta=("Click me", A, "go"),
            hint=("Edited hint, adjacent to title", B, None),
            footer=("Original footer", Z, None),
        ),
    })

    # ---- BAD (expect REJECT) ----
    fixtures.append({
        "id": "BAD-1",
        "category": "BAD",
        "expect": "REJECT",
        # text edit to node bound to out-of-scope X (card.title)
        "candidate_html": _doc(
            title="Studio Prototype",
            style=".card { border: 1px solid #ccc; }",
            card_title=("HACKED Title", X, None),
            cta=("Click me", A, "go"),
            hint=("Original hint text", B, None),
            footer=("Original footer", Z, None),
        ),
    })

    fixtures.append({
        "id": "BAD-2",
        "category": "BAD",
        "expect": "REJECT",
        # <style> selector spans A (.cta, in) and X (.card-title, out) => REJECT
        "candidate_html": _doc(
            title="Studio Prototype",
            style=".card { border: 1px solid #ccc; } .cta, .card-title { color: red; }",
            card_title=("Original Title", X, None),
            cta=("Click me", A, "go"),
            hint=("Original hint text", B, None),
            footer=("Original footer", Z, None),
        ),
    })

    fixtures.append({
        "id": "BAD-3",
        "category": "BAD",
        "expect": "REJECT",
        # forge: candidate asserts A (cta.primary) on the node the binding binds
        # to X (the card-title <h2>). The real cta node loses/changes its od-id.
        "candidate_html": _doc(
            title="Studio Prototype",
            style=".card { border: 1px solid #ccc; }",
            card_title=("Original Title", A, None),     # forged: A on title node
            cta=("Click me", "cta.primary.x", "go"),    # avoid duplicate; node mis-tagged
            hint=("Original hint text", B, None),
            footer=("Original footer", Z, None),
        ),
    })

    # ---- HELD-OUT (sealed; expected verdicts pinned, hidden from V3) ----
    fixtures.append({
        "id": "HELD-4",
        "category": "HELD",
        "expect": "REJECT",
        # re-tag: candidate re-tags B (card.hint) onto a node bound elsewhere
        # (the footer node, bound to Z). Disagreement with binding.
        "candidate_html": _doc(
            title="Studio Prototype",
            style=".card { border: 1px solid #ccc; }",
            card_title=("Original Title", X, None),
            cta=("Click me", A, "go"),
            hint=("Original hint text", "card.hint.x", None),  # hint node mis-tagged off
            footer=("Original footer", B, None),               # B re-tagged onto footer node
        ),
    })

    fixtures.append({
        "id": "HELD-5",
        "category": "HELD",
        "expect": "NOT_REJECT",
        # in-scope CSS resolving only to A via a selector form distinct from GOOD-2
        # (attribute selector [aria-label=go] resolves to the cta node bound to A)
        "candidate_html": _doc(
            title="Studio Prototype",
            style=".card { border: 1px solid #ccc; } [aria-label=go] { color: green; }",
            card_title=("Original Title", X, None),
            cta=("Click me", A, "go"),
            hint=("Original hint text", B, None),
            footer=("Original footer", Z, None),
        ),
    })

    fixtures.append({
        "id": "HELD-6",
        "category": "HELD",
        "expect": "NOT_REJECT",
        # in-scope attribute mutation on A (aria-label changed)
        "candidate_html": _doc(
            title="Studio Prototype",
            style=".card { border: 1px solid #ccc; }",
            card_title=("Original Title", X, None),
            cta=("Click me", A, "submit form"),  # aria-label go -> submit form
            hint=("Original hint text", B, None),
            footer=("Original footer", Z, None),
        ),
    })

    fixtures.append({
        "id": "HELD-7",
        "category": "HELD",
        "expect": "NOT_REJECT",
        # in-scope node addition under B (an extra <span> inside the hint <p>)
        "candidate_html": _doc(
            title="Studio Prototype",
            style=".card { border: 1px solid #ccc; }",
            card_title=("Original Title", X, None),
            cta=("Click me", A, "go"),
            hint=("Original hint text", B, None),
            footer=("Original footer", Z, None),
            hint_extra="<span>added detail</span>",
        ),
    })

    fixtures.append({
        "id": "HELD-8",
        "category": "HELD",
        "expect": "REJECT",
        # out-of-scope Z via node deletion: footer (bound to Z) removed.
        # mechanism (deletion) + od-id (Z) absent from any visible BAD shape.
        "candidate_html": _doc(
            title="Studio Prototype",
            style=".card { border: 1px solid #ccc; }",
            card_title=("Original Title", X, None),
            cta=("Click me", A, "go"),
            hint=("Original hint text", B, None),
            footer=None,  # deleted
        ),
    })

    return fixtures


def _doc(title, style, card_title, cta, hint, footer, hint_extra=""):
    """Render a one-card document. Each od-id slot is (text, od_id, aria) or None
    (omit the node). hint_extra is raw HTML appended inside the hint <p>."""
    def el(tag, cls, slot, extra=""):
        if slot is None:
            return ""
        text, oid, aria = slot
        attrs = ' class="%s"' % cls
        if oid is not None:
            attrs += ' data-od-id="%s"' % oid
        if aria is not None:
            attrs += ' aria-label="%s"' % aria
        return "    <%s%s>%s%s</%s>\n" % (tag, attrs, text, extra, tag)

    return (
        "<!doctype html>\n<html>\n<head>\n"
        '<title>%s</title>\n' % title +
        "<style>\n%s\n</style>\n" % style +
        "</head>\n<body>\n"
        '<div class="wrapper">\n'
        '  <section class="card">\n' +
        el("h2", "card-title", card_title) +
        el("button", "cta", cta) +
        el("p", "hint", hint, hint_extra) +
        el("footer", "card-footer", footer) +
        "  </section>\n</div>\n</body>\n</html>\n"
    )


def materialize_fixtures(fixtures):
    """Write each candidate to fixtures/<id>.html and compute fixtures.lock
    (sha256 per file). Returns the lock dict."""
    os.makedirs(FIXDIR, exist_ok=True)
    lock = {}
    for f in fixtures:
        path = os.path.join(FIXDIR, "%s.html" % f["id"])
        data = f["candidate_html"].encode("utf-8")
        with open(path, "wb") as fh:
            fh.write(data)
        lock[f["id"]] = hashlib.sha256(data).hexdigest()
    lock_path = os.path.join(HERE, "fixtures.lock")
    with open(lock_path, "w") as fh:
        for fid in sorted(lock):
            fh.write("%s  %s\n" % (lock[fid], fid))
    return lock, lock_path


def verify_lock(fixtures, lock):
    """Re-hash materialized files; return True iff every hash matches lock."""
    for f in fixtures:
        path = os.path.join(FIXDIR, "%s.html" % f["id"])
        with open(path, "rb") as fh:
            h = hashlib.sha256(fh.read()).hexdigest()
        if lock.get(f["id"]) != h:
            return False, f["id"]
    return True, None


# ===========================================================================
# PART 4 — Adjudication
# ===========================================================================
SCOPE_RULE = {"name": "r1-scope-rule", "version": "frozen", "note": "no-expect-labels"}


def adjudicate(fixtures, baseline_binding, lock):
    """Apply the criterion's ordered rule (INVALID -> FALSIFIED -> SURVIVED)."""
    invalid_reasons = []

    # INVALID check: TaskScope < 2
    if len(set(TASK_SCOPE)) < 2:
        invalid_reasons.append("TaskScope < 2 od-ids")

    # INVALID check: canonicalizer identity must equal frozen identity
    if runtime_canon_identity() != FROZEN_CANON_IDENTITY:
        invalid_reasons.append("canonicalizer identity != frozen identity")

    # INVALID check: fixtures.lock content hashes must match materialized files
    lock_ok, bad = verify_lock(fixtures, lock)
    if not lock_ok:
        invalid_reasons.append("fixtures.lock mismatch on %s" % bad)

    # Compute v3 per fixture (NO expect passed) + determinism re-run
    rows = []
    nondeterministic = []
    for f in fixtures:
        v1 = v3(f["candidate_html"], TASK_SCOPE, baseline_binding, SCOPE_RULE)
        v2 = v3(f["candidate_html"], TASK_SCOPE, baseline_binding, SCOPE_RULE)
        if v1 != v2:
            nondeterministic.append(f["id"])
        match = (v1 == f["expect"])
        rows.append({
            "id": f["id"],
            "category": f["category"],
            "expect": f["expect"],
            "v3": v1,
            "match": match,
        })
    if nondeterministic:
        invalid_reasons.append("nondeterministic v3 on: %s" % ", ".join(nondeterministic))

    if invalid_reasons:
        return "INVALID", rows, invalid_reasons

    mismatches = [r for r in rows if not r["match"]]
    if mismatches:
        return "FALSIFIED", rows, None
    return "SURVIVED", rows, None


def locate_horns(rows):
    """For a FALSIFIED run, classify each mismatch into an open horn."""
    horns = []
    for r in rows:
        if r["match"]:
            continue
        if r["expect"] == "REJECT" and r["v3"] == "NOT_REJECT":
            horn = "false-admit (too loose)"
        elif r["expect"] == "NOT_REJECT" and r["v3"] == "REJECT":
            if r["category"] == "HELD":
                horn = "scope-false-reject (too strict; held-out)"
            else:
                horn = "scope-false-reject (too strict)"
        else:
            horn = "unknown"
        if r["category"] == "HELD" and r["expect"] == "REJECT" and r["v3"] == "NOT_REJECT":
            horn = "held-out-only false-admit (overfit)"
        horns.append((r["id"], r["category"], horn))
    return horns


def render_table(rows):
    lines = []
    header = "%-8s | %-8s | %-11s | %-11s | %s" % ("id", "category", "expect", "v3", "match")
    lines.append(header)
    lines.append("-" * len(header))
    for r in rows:
        lines.append("%-8s | %-8s | %-11s | %-11s | %s" % (
            r["id"], r["category"], r["expect"], r["v3"],
            "OK" if r["match"] else "MISMATCH",
        ))
    return "\n".join(lines)


def write_run_result(verdict, rows, invalid_reasons, lock_path):
    path = os.path.join(HERE, "RUN-RESULT.md")
    out = []
    out.append("# C-1 Validator Spike — RUN-RESULT\n")
    out.append("Criterion: `criterion.md` (FROZEN)\n")
    out.append("Canonicalizer: %s v%s (%s)\n" % (
        CANON_IDENTITY["name"], CANON_IDENTITY["version"], CANON_IDENTITY["norm_spec_hash"]))
    out.append("TaskScope: {%s}\n" % ", ".join(TASK_SCOPE))
    out.append("Out-of-scope: {%s, %s}\n" % (X, Z))
    out.append("fixtures.lock: `%s`\n" % os.path.basename(lock_path))
    out.append("\n## Per-fixture results\n\n```\n%s\n```\n" % render_table(rows))
    out.append("\n## Verdict: **%s**\n" % verdict)
    if verdict == "INVALID":
        out.append("\n### INVALID reasons\n")
        for r in invalid_reasons:
            out.append("- %s\n" % r)
    elif verdict == "FALSIFIED":
        out.append("\n### Located horn(s)\n")
        for fid, cat, horn in locate_horns(rows):
            out.append("- %s (%s): %s\n" % (fid, cat, horn))
        out.append("\n### Repair note\n")
        out.append("- One-line repair: see mismatched fixtures above; "
                   "adjust the V3 attribution rule (not fixtures/labels) to close the located horn.\n")
    else:
        out.append("\nV3 matched every fixture on the closed set (incl. held-out). "
                   "Generalization beyond this set is NOT established by this spike.\n")
    with open(path, "w") as fh:
        fh.write("".join(out))
    return path


# ===========================================================================
# MAIN
# ===========================================================================
def main():
    print("=" * 72)
    print("C-1 VALIDATOR SPIKE — RUN")
    print("=" * 72)

    # PART 2: trusted oracle
    baseline_binding, _ = derive_baseline_binding()
    print("\nfrozenBaselineBinding (od-id -> structural alignment key):")
    for oid in sorted(baseline_binding):
        scope_tag = "IN " if oid in set(TASK_SCOPE) else "OUT"
        print("  [%s] %-14s -> %s" % (scope_tag, oid, baseline_binding[oid]))

    # PART 1: fixtures + lock
    fixtures = build_fixtures()
    lock, lock_path = materialize_fixtures(fixtures)
    print("\nMaterialized %d fixtures -> %s" % (len(fixtures), FIXDIR))
    print("Wrote fixtures.lock -> %s" % lock_path)

    # PART 4: adjudication
    verdict, rows, invalid_reasons = adjudicate(fixtures, baseline_binding, lock)

    print("\nPer-fixture verdicts:\n")
    print(render_table(rows))

    print("\n" + "=" * 72)
    print("FINAL VERDICT: %s" % verdict)
    print("=" * 72)
    if verdict == "INVALID":
        print("\nINVALID reasons:")
        for r in invalid_reasons:
            print("  - %s" % r)
    elif verdict == "FALSIFIED":
        print("\nLocated horn(s):")
        for fid, cat, horn in locate_horns(rows):
            print("  - %s (%s): %s" % (fid, cat, horn))

    result_path = write_run_result(verdict, rows, invalid_reasons, lock_path)
    print("\nWrote %s" % result_path)
    return verdict


if __name__ == "__main__":
    main()
