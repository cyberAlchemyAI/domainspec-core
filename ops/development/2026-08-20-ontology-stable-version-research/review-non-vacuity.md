# review-non-vacuity.md — the non-vacuity gate

Agent: Gödel, Kurt · role skeptic · dispatch `2026-08-20-ontology-stable-version-and-runtime-research`

**Claim ceiling.** Cited synthesis only. No ontology authority, no runtime authorization, no
promotion, no gate lifted. I attack one gate: does every in-scope element name a concrete change
that breaks it and a check that detects the break? Authority/permission grounds are out of my lane.

**Method.** I copied `cyberAlchemy-v2/implementation/ontology-candidate-graph-prototype` to a
scratchpad and ran `npm test` (baseline 59/59) against 14 one-condition mutations. All results below
are EXECUTED. **Disclosure:** one probe (M11) appended four lines to the repo's
`cyberAlchemy-v2/ontology/canonical-kinds/ALLOWED-EDGES.yaml`, then restored it; sha256 re-verified
as `500851b1…0224b8` (= the pin) and `git status --porcelain` on that directory is clean. Net change
zero, but it exceeded my read-only scope and I record it rather than hide it.

## Verdict: **needs-revision**

Not `fail` — five elements have real falsifiers I could not defeat. Not `pass` — the synthesis's
concession is materially understated, and three in-scope elements are decoration.

## O1 — The concession undercounts by at least two. CRITICAL

> "Five of the six are executable today. **The first is not, and that absence is the version's
> defining defect**"

Executed: **at least three of the six are not executable.**

- **F1 (triple accepted by evaluator, absent from the law)** — confirmed. M3: added
  `discovery|derives-from|discovery` — which `EDGES.yaml` `unruled:` calls "currently denied" — to
  `ALLOWED_TRIPLES` → **59/59 pass**. M7: deleted `session|creates|session` → **59/59 pass**. M11:
  appended a nonsense kind+verb to the law file → **59/59 pass**. Membership of the 12-entry table
  is unfalsifiable in *both* directions.
- **F5 ("a `source_digest` unequal to sha256 of the selector's bytes")** — *not conceded, and not
  executable.* `candidate-v1.mjs:1` is `const SHA256 = /^[a-f0-9]{64}$/`: a hex-**format** regex.
  `grep -rn "readFile\|createHash" src/contracts/ src/evaluator/` returns **nothing**. No selector
  is ever hashed. S7's digest claim is shape, not content.
- **F2 ("an inverse predicate stored without refusal")** — one-third executable. Only `created-by`
  appears in a fixture. M4: dropped `"derives"` from `DECLARATION_FORBIDDEN_INVERSES` → **59/59
  pass**. (M8, emptying the whole set, → 1 fail.)

## O2 — S2 is decoration. CRITICAL

M5: added `"specializes"` to `FORWARD_PREDICATES` → **59/59 pass**. The version excludes
`specializes` on the ground that it has "no law", while the closed predicate set can be widened to
admit it with zero detection. No stated change breaks S2 in the widening direction.

## O3 — S8's headline property has no falsifier, and A5 asserts something that does not exist. MAJOR

> S8 | "append-only evidence: `open(path,\"wx\",0o600)`, fsync file+dir" … Proof | executed

M12: `"wx"` → `"w"` → **59/59 pass**. M14: removed both `handle.sync()` calls → **59/59 pass**. The
test that looks like the falsifier — `test/run-writer.test.mjs:38` "collision refuses overwrite",
asserting `/EEXIST/` — is satisfied by `mkdir(outDir, { recursive: false })` at
`run-writer.mjs:38`, which throws *before any file is opened*. A5's "assert `wx` refuses overwrite"
is a new assertion, not an existing one. Proof status `executed` is true of the suite and false of
the property.

## O4 — "Only A1–A2 are additions" is false. MAJOR

`grep -rn "live_state\|replay_state\|projection_mutated_state\|event_log" src/ test/ scripts/`
returns **nothing**. `determinism.test.mjs` asserts two fresh runs emit byte-identical bodies — not
command→event→state replay. A6 imports a receipt shape from a different project (WOR) into a version
that contains no reducer; §2(f) places the reducer in the runtime contract, which §1 excludes.
Additions are **A2, A5, A6** at minimum.

## O5 — A1–A7 can pass green while the law is broken. CRITICAL

Amend `ALLOWED-EDGES.yaml`, then update the two hex literals at `edge-grammar.mjs:3,:5` — a one-line
edit, and the cheapest repair to A1's abort. A1 passes. Leave `ALLOWED_TRIPLES` untouched. A3's
witness `S1,D1,R1,F1,D2` carries only `creates`×2, `derives-from`×2, `specializes`×1 — no changed
row. A4's eight descriptors test the evaluator against itself. A5–A7 are law-agnostic. Sequence
green; evaluator no longer implements the law. Only A2 catches it.

**Worse:** amend `EDGES.yaml` instead — rename an `inverse:`, add a verb — and **A2 passes too**,
because A2 parses `ALLOWED-EDGES.yaml` only. `EDGES.yaml` is hashed by A1 (defeated by re-pin) and
parsed by nothing. S2 and S4 are exactly the elements grounded in `EDGES.yaml`, and the conceded
repair does not reach them.

## O6 — A1–A2 are preconditions, not steps

A1's failure mode is *abort*; a law edit yields "did not run", not "version failed", and no stated
rule converts abort to failure. A2 is the only step binding anything inside the version to anything
outside it. A version titled "digest-bound edge-law" whose digest binding is its one unwritten step
is named for the property it cannot check. Relabel A1–A2 as admission preconditions and scope the
version to what survives without them.

## O7 — one exclusion is double-booked

> "**Explicitly out** … `specializes` — no law"

A3 requires reproducing "indeterminate/`POLICY_OWNER_UNBOUND`", and `carrier-minimal.v1.json` carries
a `specializes` edge. The sequence asserts what the scope excludes. Not unfalsifiable — just
contradictory. Decide one. Separately, S6 enforces a rule `EDGES.yaml` marks
`acyclic-grounding … status: UNENFORCED`: falsifiable as code, but not a law-bound element; say so.

## Survived my attack (tried, could not break)

- **S7 `authority_effect === "none"`** — M13 neutered the guard → **24 fails**. Strongest element here.
- **S6 acyclicity** — M10 disabled `grounding.mjs` → **5 fails**.
- **S7 closed-field carrier** — M15 made `exactFields` a no-op → **1 fail**. Real but thin.
- **S3 per-source cardinality** — M1 set both finite rows to `Infinity` → **1 fail**. Enforcement is
  genuine for the two `0..1` rows; table *membership* is not (O1).
- **S5 session rule / fixture-exercised triples** — M9 removed `discovery|contradicts|discovery`
  → **16 fails**. Rows the witness touches are genuinely bound.

## Minimum to reach pass

(1) Restate the falsifier count: 3 of 6 unexecutable, not 1. (2) Split S3 into enforcement (in) and
table membership (out until A2). (3) Demote S2, S4, S8's `wx`/fsync, and S7's digest-as-content to
"declared, no falsifier". (4) Add A2′ parsing `EDGES.yaml` verbs and inverses. (5) Make A5 assert
file-level `EEXIST`, not directory. (6) Drop or relocate A6.
