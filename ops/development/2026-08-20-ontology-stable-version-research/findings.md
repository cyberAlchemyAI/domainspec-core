# findings.md — the first stable ontology version and its runtime

Agent: Bourbaki, Nicolas · role writer · dispatch `2026-08-20-ontology-stable-version-and-runtime-research`
Sheet digest `cc788e4f3d615543cdc4de954cc0519a83f3f6aeac5e8e520735ca73a2599ddc`

Proof: `executed` = command run · `observed` = file read · `unverified` = declared, no falsifier.
Origins: **PF** prior-failure · **WA** working-artifact · **GOV** governance · **SY** synthesizer ·
**NV** non-vacuity skeptic · **AU** authority skeptic · **PV** parent-verified.

---

## 1. Direct answer — there is no first version

**There is no first version.** The synthesizer proposed `ontology-edge-law/v1` and withdrew it (SY,
`synthesis-revised.md` §0).

Executed reason: NV ran the prototype suite against 14 one-condition mutations from a 59/59 baseline.
**Seven left it 59/59 green** — including M11, which appended nonsense to the governed law file
`cyberAlchemy-v2/ontology/canonical-kinds/ALLOWED-EDGES.yaml` itself (NV, executed; restore
PV-verified, net change zero). A version of a law must be falsifiable against that law. This one is
not: nothing reads the YAML bytes. The pins at `src/evaluator/edge-grammar.mjs:1-6` are compared only
to the same hex strings retyped at `test/edge-grammar.test.mjs:103-110` (WA/SY, observed).

What exists instead, named exactly: **five executed falsifier results over one evaluator's
self-consistency, five declared properties with no falsifier, and one untested property.** That is an
evidence bundle — `kind.evidence`, owner route "source/inventory owner", forbidden collapse "Not
authority by itself" (`cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md:34`, PV; line 33 is
`kind.projection`). Not a version, not a spec, not a foundation.

**State: `blocked`.** The bundle declares no kind in the closed enumeration, and CAV2-D49
(`cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` §CAV2-D49, observed) says such an artifact
"defaults to **blocked** pending an owner decision". Not candidate, not eligible — eligibility is
decision-gate's judgment (`AUTHORITY-KINDS.md:28`). If a label is ever needed: `ontology-edge-law-v1`,
dash grammar (AU-O3, `OVS-GATE-004:138-141`). The stem is unowned: `ontology-edge-law-owner`
(`src/evaluator/policy-disposition.mjs:8`) has **zero** occurrences under `cyberAlchemy-v2/authority/`
or `cyberAlchemy-v2/ontology/` (PV, executed).

## 2. What is bound — five executed falsifier results

Source identity for all five: `cyberAlchemy-v2/implementation/ontology-candidate-graph-prototype`,
baseline `# tests 59 / # pass 59 / # fail 0` (WA, executed), governed files at pinned digests
`500851b1…0224b8` (ALLOWED-EDGES.yaml) and `f3ed1ed8…52e0d1` (EDGES.yaml) (WA/PV, executed).

| ID | Property | Selector | Mutation | Observed | Origin | Proof |
|---|---|---|---|---|---|---|
| B1 (S3a) | per-source cardinality **enforcement**, two `0..1` rows | `src/evaluator/edge-grammar.mjs`, `ALLOWED_TRIPLES` line 11 | M1: both finite rows → `Infinity` | 1 fail | NV | executed |
| B2 (S5) | session rule + triples the witness touches | same file, `SESSION_CLAIM_FORBIDDEN`, `SESSION_EVIDENCE_FORBIDDEN` | M9: removed `discovery\|contradicts\|discovery` | 16 fails | WA/NV | executed |
| B3 (S6) | `derives-from` acyclicity | `src/evaluator/grounding.mjs:13`, DFS cycle detection | M10: disabled `grounding.mjs` | 5 fails | WA/NV | executed |
| B4 (S7a) | `authority_effect === "none"` | `src/contracts/candidate-v1.mjs`, `validateAuthorityEffect`:109 | M13: neutered the guard | 24 fails | WA/NV | executed |
| B5 (S7b) | closed-field carrier | same file, `exactFields`:80 | M15: `exactFields` → no-op | 1 fail | WA/NV | executed |

Qualifications: B3 enforces a rule `EDGES.yaml` marks `acyclic-grounding status: UNENFORCED` —
evaluator law, **not governed law** (NV-O7). B5 is real but thin. B1 binds two rows; table
**membership** is unbound (D2).

## 3. Declared but unfalsifiable — the demoted properties

All `unverified`. Every mutation is NV, executed, against baseline 59/59.

| ID | Property | Mutation that left the suite green |
|---|---|---|
| D1 (S2) | closed forward-predicate set (`FORWARD_PREDICATES`) | M5 added `specializes` → 59/59. No stated change breaks it in the widening direction |
| D2 (S3b) | **membership** of the 12-entry `ALLOWED_TRIPLES` table | M3 added denied `discovery\|derives-from\|discovery`; M7 deleted permitted `session\|creates\|session`; M11 edited the law file — all → 59/59. Unfalsifiable in **both** directions |
| D3 (S4) | inverse-storage refusal (`DECLARATION_FORBIDDEN_INVERSES`) | M4 dropped `"derives"` → 59/59. One-third bound: only `created-by` is fixture-exercised (M8, emptying the set → 1 fail) |
| D4 (S7c) | `source_digest` = sha256 of selector bytes | No mutation needed — the property is absent. `candidate-v1.mjs:1` is `const SHA256 = /^[a-f0-9]{64}$/`, a **format** regex; `grep -rn "readFile\|createHash\|readFileSync" src/contracts/ src/evaluator/` returns nothing (PV, executed) |
| D5 (S8) | append-only evidence: `open(path,"wx",0o600)`, fsync file + dir | M12 `"wx"`→`"w"` → 59/59; M14 removed both `handle.sync()` → 59/59. The apparent falsifier (`test/run-writer.test.mjs:38`, asserting `/EEXIST/`) is satisfied by `mkdir(outDir,{recursive:false})` at `run-writer.mjs:38`, which throws **before any file opens** |

Falsifier count of record: **three** of the six failure modes originally listed are not executable —
not one (NV-O1).

## 4. What a runtime would have to satisfy — requirements only

Not a contract; this record may not author one. `cyberAlchemy-v2/ontology/PACKAGE-MODEL.md:51` (PV,
not `:50`) lists "runtime contract definition" under **Out of scope**; `AUTHORITY-KINDS.md:32` assigns
`kind.runtime_contract` to "task-session after owner gates".

Would have to: (a) hash both YAMLs at load and refuse to run on pin mismatch; (b) parse the law into
the triple table rather than carry a transcription; (c) parse `EDGES.yaml` `verbs:` and `inverse:`
fields; (d) evaluate a carrier and emit typed diagnostics; (e) write evidence append-only in the shape
D5 declares — a shape currently unfalsified; (f) attest write isolation
(`scripts/verify-write-isolation.mjs:5`, WA); (g) label output `authority_effect: none`,
`posture.generated` (`cyberAlchemy-v2/SOURCE-MAP.md:32-33`, GOV).

Struck: command→event→state reduction. `grep -rn
"live_state\|replay_state\|projection_mutated_state\|event_log" src/ test/ scripts/` returns nothing
(PV, executed) — no reducer, no event log (NV-O4).

**Must never decide** (each re-verified by AU): promotion/lifecycle status
(`LIFECYCLE-MODEL.md:48-49`); its own runtime-contract kind (`AUTHORITY-KINDS.md:32`); node types,
edges, schema amendment (`PACKAGE-MODEL.md:46-54`); the `specializes` disposition; cross-project
migration (`OVS-GATE-004:142-144`); global identity (`NODE-MODEL.md:18`).

**The invariant.** "Emits diagnostics, never dispositions" is refuted by the code:
`policy-disposition.mjs:31-38` returns a field named `disposition` (AU-O4). What holds is three-part:
(i) every emitted record carries `authority_effect: "none"` (`:36`); (ii) a case whose owner is
unbound returns indeterminate with `POLICY_OWNER_UNBOUND` (`:58`); (iii) no consumer may treat this
output as admission (`ontology/projections/README.md:47-49`). (i) and (ii) are bound in code;
**(iii) is bound to nothing.** `specializes` is out as law (no permitted triple, owner unbound) and in
as input — the evaluator returns `policy-indeterminate` with `POLICY_OWNER_UNBOUND` (`:57-58`).

## 5. What would establish a version

**A1, A2, A2′ are admission preconditions, not steps** (NV-O6). A1's failure mode is *abort* — "did
not run", not "version failed" — and no rule converts abort to failure. Everything below is
law-agnostic: amend the law, re-pin the two hex literals at `edge-grammar.mjs:3,:5`, and A1 and A3–A7
pass green while the evaluator no longer implements the law. Only A2 + A2′ catch that.

| Step | Content | Owner | Origin |
|---|---|---|---|
| A1 *(precondition)* | Hash both YAMLs; compare to pin; abort on mismatch | runtime-contract owner (**unregistered**) | OEWL step 1 (PF) |
| A2 *(precondition)* | Parse `ALLOWED-EDGES.yaml`; assert parsed table ≡ the 12-entry table | same | WA §4.1, "single largest gap" |
| A2′ *(precondition)* | Parse `EDGES.yaml` `verbs:` and each `inverse:`; assert ≡ `FORWARD_PREDICATES` and `DECLARATION_FORBIDDEN_INVERSES` | same | NV-O5 |
| A3 | Minimum Finite Witness `S1,D1,R1,F1,D2`; reproduce policy-pass, 7 fail classes, indeterminate/`POLICY_OWNER_UNBOUND` | same | PF §3 |
| A4 | 8 mutation descriptors + 1 additive, each failing with its declared code | same | WA |
| A5 | Assert **file-level** `EEXIST` from `open(path,"wx")` on a pre-existing file — not directory `EEXIST` | same | NV-O3 (new assertion; does not exist) |
| A7 | Write-isolation before/after over the protected selector set | same | WA |

**A6 dropped** (replay / `live_state_sha256`): no replay machinery exists here (PV, executed). Its
method stays citable from `WOR/receipts/state-contract-validation.json` (PF); it is not a step.

Ceiling if all seven executed: one local fixture witness of evaluator self-consistency — **not**
ontology correctness, corpus validity, or promotion.

## 6. Verdict matrix

| Claim | Verdict |
|---|---|
| S3a cardinality enforcement (two `0..1` rows) | **bound** (M1 → 1 fail) |
| S5 session rule + witness-touched triples | **bound** (M9 → 16) |
| S6 `derives-from` acyclicity as evaluator law | **bound** (M10 → 5); as governed law: **unresolved** (`EDGES.yaml`: UNENFORCED) |
| S7a `authority_effect === "none"` | **bound** (M13 → 24) |
| S7b closed-field carrier | **bound** (M15 → 1) |
| S2 closed forward-predicate set | declared-no-falsifier (M5) |
| S3b 12-triple table membership | declared-no-falsifier, both directions (M3/M7/M11) |
| S4 inverse-storage refusal | declared-no-falsifier for 2 of 3 predicates (M4) |
| S7c `source_digest` as content | declared-no-falsifier — property absent from code (PV) |
| S8 `wx` + fsync | declared-no-falsifier (M12/M14) |
| S1 four node kinds (`candidate-v1.mjs`, `NODE_KINDS` line 2) | **untested** — no mutation aimed at it (NV-O1) |
| Digest binding of pins to governed YAML bytes | declared-no-falsifier — constant compared to constant |
| "stable" as a status | **unresolved** — absent from every enumeration checked (GOV) |
| Promoted-state enum | **unresolved** — `active` (`LIFECYCLE-MODEL.md:31`) vs `promoted` (schema `properties.lifecycle_status`, line 44, PV); twelve values, none `stable`; `LIFECYCLE-MODEL.md:36` disclaims its own binding force |
| Runtime contract | **untested** — none exists; owner unregistered |
| Cross-corpus coherence | **untested** — no tool checks any production ontology against `canonical-kinds/` (WA) |

## 7. Unresolved rows, with owners

OQ-1 / OQ-2 **OPEN**, no validator decision (`AUTHORITY-MODEL.md:155-165`) → authority route ·
CR-1 / CR-2 **CRITICAL**, unactioned (route 3 mis-points: `CLAUDE.md:67`, `AGENTS.md:176`; no
definition card for `authority kind` / `canonical kind`) → definitions-governance · OVS-GATE-003, no
gate file in `decision-gates/` (`GOVERNED-CANDIDATE-BUNDLE.md:154`) → DomainSpec handoff route ·
cross-project ontology migration (`OVS-GATE-004:142-144`) → unassigned · authority-ledger validator
absent (`LIFECYCLE-MODEL.md:58-62`) → unassigned · `specializes` law, owner unbound → unassigned ·
**X4**, whether the four `SNAPSHOT_CONTRACT_BINDING_MISMATCH` failures reproduce → whoever executes
the Node suite at `ontology-working-prototype-gap…:87, :130-131` · **X5**, Inventory read model vs
working folder as dispatch-state truth → parent.

Writer-observed row: `synthesis-revised.md` §0 says "**four** declared properties with no falsifier"
while its own §1 table lists **five** (S2, S3b, S4, S7c, S8). Recorded here as five; flagged, not
repaired.

**Excluded, not unresolved:** anything resting on `attacks.md` — CR-9 records three fabricated quotes
and states that file "must not be cited as independent confirmation". No row above draws on it.

## 8. Preserved objections — unrepaired

- **NV-O5 / NV-O6** stand as findings, not repairs: the green-while-broken path exists until A2 and
  A2′ are written, and neither is written.
- **NV-O1 on S1**: no mutation was aimed at `NODE_KINDS`, so its enforcement is *untested* — a third
  status, collapsible into neither bound nor declared-with-a-known-green-mutation.
- **AU-O2**: repaired only in direction. The state is stated as **blocked** and `kind.evidence` is
  proposed, but no owner accepted that routing, and CAV2-D49 makes accepting a kind owner-gated.
  Blocked remains blocked.
- **AU-O3, second point**: `ontology-edge-law-owner` is unregistered anywhere in the authority spine
  (PV, executed). Any label on that stem names an owner that does not exist.

## 9. Claim ceiling

Cited synthesis only. Grants no ontology authority, authorizes no runtime implementation, promotes
nothing, lifts no decision gate. `ontology-authority-not-granted` and
`runtime-implementation-not-authorized` stand. Nothing here is an owner act — not the `kind.evidence`
proposal, not the label, not the A-steps. The bundle is `blocked` under CAV2-D49; only an owner
decision moves it.

Process findings of record (PV): five selector defects this run, all one shape — a true claim carried
by a pointer that does not resolve — none caught by the producing stage, all five by parent
re-dereferencing; and the read-only constraint on a skeptic was instruction only, enforced by no
mechanism, while `verify-write-isolation.mjs` existed and was not applied (D3).

Private paths appear above; this working folder is private. No content here may be copied into
`arcanum/` (public).
