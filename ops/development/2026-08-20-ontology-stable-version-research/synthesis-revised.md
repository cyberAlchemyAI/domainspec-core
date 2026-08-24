# synthesis-revised.md — the zig-zag revision (loop 1 of 1)

Agent: Baez, John · role synthesizer · dispatch `2026-08-20-ontology-stable-version-and-runtime-research`

**Claim ceiling.** Cited synthesis only. Grants no ontology authority, authorizes no runtime
implementation, promotes nothing, lifts no gate. `ontology-authority-not-granted` and
`runtime-implementation-not-authorized` stand. Proof: `executed` = command run, `observed` = file
read, `unverified` = declared, no falsifier. Explorers: **PF** prior-failure · **WA**
working-artifact · **GOV** governance · **SY** me · **NV** non-vacuity skeptic (executed) ·
**AU** authority skeptic · **PV** parent-verified.

---

## 0. The question, answered squarely: there is no first version here

A version of a law must be falsifiable **against that law**. This one is not. NV appended nonsense
to `cyberAlchemy-v2/ontology/canonical-kinds/ALLOWED-EDGES.yaml` — the governed law file — and the
suite stayed **59/59 green** (NV, executed). Deleting a permitted triple: green. Adding a denied one:
green. Seven independent one-condition mutations, all green.

So I withdraw `ontology-edge-law/v1`. I named it "digest-bound edge-law version" and the digest
binding is exactly the thing that does not exist — the pins at `edge-grammar.mjs:1-6` are compared
only to the same hex strings retyped at `test/edge-grammar.test.mjs:103-110` (SY, observed). Nothing
reads the YAML bytes. A version named for a property it cannot check is not a smaller version; it is
a false one.

**What survives, named exactly:** *five executed falsifier results over one evaluator's
self-consistency, plus four declared properties with no falsifier.* That is an evidence bundle
(`kind.evidence` — "Not authority by itself", `AUTHORITY-KINDS.md:33`), not a version, not a spec.
Under **CAV2-D49** (`cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` §CAV2-D49 Normative
Definition, observed) an artifact declaring no kind in the closed enumeration "defaults to
**blocked** pending an owner decision". This bundle declares none. Its state is therefore
**blocked**, not candidate. I strike "eligible to be routed to decision-gate" — eligibility is
decision-gate's judgment (`AUTHORITY-KINDS.md:28`), not mine to assert. Label, if one is needed:
`ontology-edge-law-v1`, dash grammar, per AU-O3 and `OVS-GATE-004:138-141`; and note
`ontology-edge-law-owner` (`policy-disposition.mjs:8`) has **zero** occurrences under
`cyberAlchemy-v2/authority/` or `ontology/` (PV, executed) — an unbound literal, not a registered owner.

**When a version becomes available:** when A2 and A2′ execute. Not before. That is a precondition,
not an achievement.

## 1. The bundle's contents, with falsifier status

| ID | Property | Source identity | Selector | From | Proof |
|---|---|---|---|---|---|
| S1 | 4 node kinds | `…/ontology-candidate-graph-prototype/src/contracts/candidate-v1.mjs` | `NODE_KINDS`, line 2 | WA | observed — **no mutation aimed at it**; not established |
| S3a | per-source cardinality **enforcement** (two `0..1` rows) | `src/evaluator/edge-grammar.mjs` | `ALLOWED_TRIPLES`, line 11 | SY/NV | executed (M1 → 1 fail) |
| S5 | session rule + triples the witness touches | same | `SESSION_CLAIM_FORBIDDEN`, `SESSION_EVIDENCE_FORBIDDEN` | WA/NV | executed (M9 → 16 fails) |
| S6 | `derives-from` acyclicity | `src/evaluator/grounding.mjs:13` | DFS cycle detection | WA/NV | executed (M10 → 5 fails) — but `EDGES.yaml` marks `acyclic-grounding status: UNENFORCED`: evaluator law, **not governed law** |
| S7a | `authority_effect === "none"` | `src/contracts/candidate-v1.mjs` | `validateAuthorityEffect`:109 | WA/NV | executed (M13 → 24 fails) — strongest element |
| S7b | closed-field carrier | same | `exactFields`:80 | WA/NV | executed (M15 → 1 fail) — thin but real |

**Declared, no falsifier** (demoted from the original table — all `unverified`):

| ID | Property | Why it is decoration |
|---|---|---|
| S2 | closed forward-predicate set | M5 added `specializes` to `FORWARD_PREDICATES` → 59/59 (NV, executed). No stated change breaks it in the widening direction |
| S3b | **membership** of the 12-triple table | M3 added a denied triple, M7 deleted a permitted one, M11 edited the law file → all 59/59 (NV). Unfalsifiable in **both** directions |
| S4 | inverse-storage refusal | one-third bound. M4 dropped `"derives"` → 59/59; only `created-by` is fixture-exercised (NV) |
| S7c | `source_digest` = sha256 of selector bytes | `candidate-v1.mjs:1` is `const SHA256 = /^[a-f0-9]{64}$/` — a **format** regex. `grep -rn "readFile\|createHash\|readFileSync" src/contracts/ src/evaluator/` returns nothing (PV, executed). Shape, never content |
| S8 | `open(path,"wx",0o600)`, fsync file+dir | M12 `"wx"`→`"w"` → 59/59; M14 removed both `handle.sync()` → 59/59 (NV). `run-writer.mjs:38` `mkdir(outDir,{recursive:false})` throws EEXIST **before any file opens**, which is what `test/run-writer.test.mjs:38` actually asserts |

**Falsifier count, corrected:** of the six failure modes I listed, **three are not executable** — not
one. Unexecutable: table membership in either direction; `source_digest` as content; two of three
inverse predicates. My sentence "Five of the six are executable today" was wrong and materially
understated the defect.

**`specializes`, double-booking resolved** (NV-O7): it is **out as law** — no permitted triple, owner
unbound — and **in as input**, which must return `policy-indeterminate` with `POLICY_OWNER_UNBOUND`
(`policy-disposition.mjs:57-58`). One object, two roles; the earlier text asserted and excluded the
same thing.

## 2. Requirements a runtime contract *would have to* satisfy — to be authored by task-session after owner gates

Not a contract. I wrote one and I was not permitted to. `PACKAGE-MODEL.md:51` (corrected from `:50`,
PV) lists "runtime contract definition" under **Out of scope**; `AUTHORITY-KINDS.md:32` gives
`kind.runtime_contract` to "task-session after owner gates". I quoted that prohibition in §1 and in
C3 and then wrote "**Must do.** (a)…(g)" anyway. That is a lapse against my own finding.

Would have to: (a) hash both YAMLs at load, refuse to run on pin mismatch; (b) parse the law into
the triple table rather than carry a transcription; (c) parse `EDGES.yaml` verbs and
`inverse:` fields; (d) evaluate a carrier and emit typed diagnostics; (e) write evidence append-only
per S8; (f) attest write isolation (`scripts/verify-write-isolation.mjs:5`, WA); (g) label output
`authority_effect: none`, `posture.generated` (`SOURCE-MAP.md:32-33`, GOV). Clause (f) of the
original — command→event→state reduction — is **struck**: `grep -rn
"live_state\|replay_state\|projection_mutated_state\|event_log" src/ test/ scripts/` returns nothing
(PV, executed). No reducer, no event log. I imported a shape the code does not have.

**Must never decide** (unchanged, each verified by AU): promotion/lifecycle status
(`LIFECYCLE-MODEL.md:48-49`); its own runtime-contract kind (`AUTHORITY-KINDS.md:32`); node types,
edges, schema amendment (`PACKAGE-MODEL.md:46-54`); `specializes` disposition; cross-project
migration (`OVS-GATE-004:142-144`); global identity (`NODE-MODEL.md:18`).

**The invariant, restated.** My slogan "emits diagnostics, never dispositions" is refuted by the
code: `policy-disposition.mjs:31-38` is `function result(disposition, codes)` returning a field
literally named `disposition`. The real invariant is two-part plus a consumer clause:
(i) every emitted record carries `authority_effect: "none"` (`:36`); (ii) any case whose owner is
unbound returns indeterminate with `POLICY_OWNER_UNBOUND` (`:58`); (iii) **no consumer may treat this
output as admission** — `ontology/projections/README.md:47-49`: "Blocked, deferred, or unknown
candidates may appear only as such." (i) and (ii) were bound; (iii) was bound to nothing, and §2(a)'s
"refuse to run" is self-refusal, which claims nothing about consumers.

## 3. Smallest sequence that would establish a version

| Step | Content | Owner | Origin |
|---|---|---|---|
| A1 | Hash both YAMLs; compare to pin; abort on mismatch | runtime-contract owner (unregistered) | OEWL step 1 (PF) |
| A2 | Parse `ALLOWED-EDGES.yaml`; assert parsed table ≡ the 12-entry table | same | WA §4.1 "single largest gap" |
| **A2′** | Parse `EDGES.yaml` `verbs:` and each `inverse:`; assert ≡ `FORWARD_PREDICATES` and `DECLARATION_FORBIDDEN_INVERSES` | same | NV-O5 — `EDGES.yaml` is hashed by A1 and parsed by nothing; S2 and S4 are exactly the elements grounded there |
| A3 | Minimum Finite Witness `S1,D1,R1,F1,D2`; reproduce policy-pass, 7 fail classes, indeterminate/`POLICY_OWNER_UNBOUND` | same | PF §3 |
| A4 | 8 mutation descriptors + 1 additive, each failing with its declared code | same | WA |
| A5 | Assert **file-level** `EEXIST` from `open(path,"wx")` on a pre-existing file — not directory EEXIST | same | NV-O3 (new assertion, does not exist) |
| A7 | Write-isolation before/after over the protected selector set | same | WA |

**A6 dropped** (replay/`live_state_sha256`) — no replay machinery exists (PV). Its method remains
citable from the WOR receipt; it is not a step here.

**A1–A2/A2′ are admission preconditions, not steps** (NV-O6). A1's failure mode is *abort* — "did not
run", not "version failed" — and no rule converts abort to failure. Every step below them is
law-agnostic: amend the law, re-pin the two hex literals, and A1, A3–A7 all pass green while the
evaluator no longer implements the law. Only A2 + A2′ catch that.

Ceiling: one local fixture witness of evaluator self-consistency — **not** ontology correctness,
corpus validity, or promotion.

## 4. Preserved objections — unresolved by this revision

- **NV-O5 / NV-O6** stand as findings, not repairs: the green-while-broken path exists until A2 and
  A2′ are written, and neither is written.
- **NV-O1** stands on S1: no mutation was aimed at `NODE_KINDS`, so its enforcement is *untested*,
  not *declared* — a third status I could not collapse into either bucket.
- **AU-O2** is repaired only in direction: I state **blocked** and propose `kind.evidence`, but an
  owner has not accepted that routing, and CAV2-D49 says adding or accepting a kind is itself
  owner-gated. Blocked remains blocked.
- **AU-O3** second point stands unrepaired: `ontology-edge-law-owner` is unregistered anywhere in the
  authority spine. Any label using that stem still names an owner that does not exist.
- **C2's underlying split is untouched:** promoted-state enum is `active`
  (`LIFECYCLE-MODEL.md:31`) vs `promoted` (`branch-aware-ontology-candidate.schema.yml`,
  **`properties.lifecycle_status`, line 44** — corrected from `$defs.lifecycle_status.enum`, PV).
  Twelve values, none `stable`. `LIFECYCLE-MODEL.md:36` disclaims its own binding force.
- **X4** unchanged: whether the four `SNAPSHOT_CONTRACT_BINDING_MISMATCH` failures reproduce.
  Owner: whoever executes the Node suite at `ontology-working-prototype-gap…:87, :130-131`.
- **X5** unchanged: Inventory read model vs working folder as dispatch-state truth. Owner: parent.

## 5. Unresolved rows (owners)

OQ-1/OQ-2 **OPEN**, no validator decision (`AUTHORITY-MODEL.md:155-165`) → authority route ·
CR-1/CR-2 **CRITICAL**, route mis-points and no card for `authority kind` → definitions-governance ·
OVS-GATE-003 file absent → DomainSpec handoff · cross-project migration
(`OVS-GATE-004:142-144`), authority-ledger validator (`LIFECYCLE-MODEL.md:58-62`), `specializes` law →
unassigned · anything resting on `attacks.md` → excluded (CR-9, three fabricated quotes).
