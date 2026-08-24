# synthesis.md — one candidate account

Agent: Baez, John · role synthesizer · dispatch `2026-08-20-ontology-stable-version-and-runtime-research`

**Claim ceiling.** Cited synthesis only. Grants no ontology authority, authorizes no runtime
implementation, promotes nothing, lifts no decision gate. `ontology-authority-not-granted` and
`runtime-implementation-not-authorized` stand. Proof status: `executed` = a command was run,
`observed` = a file was read. Explorer keys: **PF** = prior-failure (Abramsky), **WA** =
working-artifact (Bénabou), **GOV** = governance (Banach), **SY** = verified by me today.

---

## 0. The three collisions, adjudicated

**C1 — machinery or tautology? Both, and the seam is exactly where the version boundary goes.**
The evaluators are real law; the *binding* is a constant compared to itself. `GRAMMAR_SOURCE_DIGESTS`
is a frozen literal at `src/evaluator/edge-grammar.mjs:1-6`, and the test named "binds the finite
table to the governed source digests" `deepEqual`s it against the same two hex strings written out
again in `test/edge-grammar.test.mjs:103-110` (SY, observed). `grep -rn "yaml" src/` returns only
those two key strings — no parser exists (SY, executed). So: **the predicate law is machinery, the
governed-source binding is a tautology.** Editing ALLOWED-EDGES.yaml breaks zero tests. Neither
explorer is corrected; they describe two different objects, and the first version must include the
first and exclude the claim carried by the second.

**C2 — "stable" is not a status, and the corpus is worse than GOV reported.** No enumeration
contains `stable` (GOV, observed). Two enumerations for the promoted state exist and they are
disjoint: `active` (`LIFECYCLE-MODEL.md:31`) and `promoted`
(`branch-aware-ontology-candidate.schema.yml` `$defs.lifecycle_status.enum`) — and
`LIFECYCLE-MODEL.md:36` says of its own states "These states are a candidate model. They do not bind
current artifact schemas" (SY, observed; not surfaced by any explorer). The only defined term,
`CAV2-D1 Stable Repository`, is repository-scoped (GOV). **What the goal should have asked:** not
"the first stable ontology version" but *"the first digest-bound edge-law version, carrying
`Status: candidate`, eligible to be routed to decision-gate."* "Stable" is an owner act reserved to
decision-gate and never performed for any schema (GOV, `AUTHORITY-MODEL.md:155-159`, **OPEN**).

**C3 — repaired precedent, absent owners: the method transfers, the authorization does not.**
The WOR repair is executed proof of a *shape*: closed enum, declared reduction rule for every
transition, `live_state_sha256 == replay_state_sha256` = `44dbb810…e1280c` (PF, executed receipt).
The runtime owner set — contract, implementation, registration, snapshot, run, retention, service —
is recorded absent (PF/GOV, `ORA/CLOSEOUT.json:/residue/0`), and `PACKAGE-MODEL.md:46-54` puts
"runtime contract definition" out of scope. **Permits:** adopting the digest-equality acceptance
shape as the terminator of any local fixture witness. **Forbids:** implementing, registering,
snapshotting, running, retaining, or serving anything under it. Precedent without owners licenses a
test, not a build.

---

## 1. Candidate first version — `ontology-edge-law/v1`, `Status: candidate`

Named this way because no `stable` value exists to carry (C2). The version is the pair
*(law text, evaluator)* bound by a digest that is checked, not transcribed.

| ID | In scope | Source identity | Selector | From | Proof |
|---|---|---|---|---|---|
| S1 | 4 Evidence node kinds | `…/ontology-candidate-graph-prototype/src/contracts/candidate-v1.mjs` | `NODE_KINDS`, line 2 | WA | executed (59/59) |
| S2 | 4 forward predicates | `src/evaluator/edge-grammar.mjs` | line 8 `FORWARD_PREDICATES` | SY | observed |
| S3 | 12 allowed triples + per-source cardinality | same | `ALLOWED_TRIPLES`, line 11; count 12 | SY | executed (`grep -c`) |
| S4 | inverse-storage refusal | same | `DECLARATION_FORBIDDEN_INVERSES`, line 9 | WA/SY | observed |
| S5 | session rule | same | `SESSION_CLAIM_FORBIDDEN`, `SESSION_EVIDENCE_FORBIDDEN` | WA | executed |
| S6 | `derives-from` acyclicity | `src/evaluator/grounding.mjs:13` | DFS cycle detection | WA | executed |
| S7 | closed-field carrier, SHA-256 `source_digest`, repo-relative selector, `authority_effect==="none"` | `src/contracts/candidate-v1.mjs` | `exactFields`:80, :150, :67, `validateAuthorityEffect`:109 | WA | executed |
| S8 | append-only evidence: `open(path,"wx",0o600)`, fsync file+dir, digest map, terminal receipt last | `src/evidence/run-writer.mjs` | :9, :27, :91 | WA | executed |

**Explicitly out** (each with the reason, not a hedge): `specializes` — no law; hardcoded
`policy-indeterminate` / `POLICY_OWNER_UNBOUND` at `policy-disposition.mjs:57` (WA). Every kind
beyond the four — `ALLOWED-EDGES.yaml:3` "Every other kind is deferred" (WA/SY, observed).
Mutation, revision, merge, node identity across edits — every writer is create-only (WA).
Query-by-predicate — `evaluatePokerTeamO13` (`cli.mjs:15`) takes no argv (WA). Production corpora
(e.g. body-war, 237 nodes, `validate.mjs` passes independently) — the prototype never touches them
(WA, executed). Cross-family `schema_version` reconciliation across ~12 production ontologies with
disjoint families (WA, observed). Promotion verdicts and runtime-contract definition
(`PACKAGE-MODEL.md:46-54`, GOV).

**What would break it** (non-vacuity — the version names its own falsifiers): a triple the evaluator
accepts that the parsed YAML does not list, or the reverse; an inverse predicate stored without
refusal; an admitted `derives-from` cycle; an admitted session claim/evidence edge; a carrier with an
extra field or a `source_digest` unequal to sha256 of the selector's bytes; any evaluator output with
`authority_effect != "none"`. Five of the six are executable today. **The first is not, and that
absence is the version's defining defect** — it is what step A2 below exists to fix.

## 2. Candidate runtime contract

**Must do.** (a) Read `EDGES.yaml` and `ALLOWED-EDGES.yaml` at load, hash the bytes, refuse to run
on mismatch with the pin. (b) Parse the law into the triple table rather than carrying a
transcription. (c) Evaluate a submitted carrier and emit typed diagnostics. (d) Write evidence
append-only per S8. (e) Attest write isolation over the protected selector set before/after
(`scripts/verify-write-isolation.mjs:5`, WA). (f) Reduce command→event→state under a closed enum with
a declared rule for *every* transition and prove live/replay digest equality (C3 method). (g) Label
all output `authority_effect: none`, posture `posture.generated`, pointing back to canonical sources
(`SOURCE-MAP.md:32-33`, GOV).

**Must never decide** (authority non-collapse — each belongs to a named owner): promotion or
lifecycle status — "must not fill the verdict hole" (`LIFECYCLE-MODEL.md:48-49`); its own runtime
contract kind — `kind.runtime_contract` is owned by "task-session after owner gates"
(`AUTHORITY-KINDS.md:32`); node types, edges, or schema amendment (`PACKAGE-MODEL.md:46-54`);
`specializes` disposition — owner unbound, must remain indeterminate; cross-project migration — no
owner route exists (`OVS-GATE-004:142-144`); global identity — `concept_id`/`relation_id` are "Local
stable identifier" (`NODE-MODEL.md:18`); finality of the JSON Schema candidate (`OVS-GATE-001:240-247`).
The contract emits **diagnostics**, never **dispositions**.

## 3. Smallest acceptance sequence (assembled, not invented)

| Step | Content | Origin |
|---|---|---|
| A1 | Hash both YAMLs on disk; compare to the pin; abort on mismatch | OEWL step 1 (PF) |
| A2 | Parse ALLOWED-EDGES.yaml; assert parsed table ≡ the 12-entry table | WA §4.1 "single largest gap" |
| A3 | Minimum Finite Witness `S1,D1,R1,F1,D2`: closure exactly `F1→R1→D1`, `D2 contradicts D1` outside it; reproduce policy-pass, 7 policy-fail classes, indeterminate/`POLICY_OWNER_UNBOUND` | PF §3 |
| A4 | The 8 one-condition mutation descriptors + 1 additive in `fixtures/cases/`, each failing with its declared code | WA |
| A5 | Write the run through `run-writer`; assert `wx` refuses overwrite, terminal receipt last, digest map binds inputs→evaluators→outputs | WA |
| A6 | Replay the event log; assert `live_state_sha256 == replay_state_sha256`, `projection_mutated_state: false` | WOR receipt (PF) |
| A7 | Write-isolation before/after; no protected selector changed | WA |

Only A1–A2 are additions; both are named as the largest gap by WA. Ceiling: one local fixture
witness of edge law and evidence determinism — **not** ontology correctness, corpus validity, or
promotion. No browser step: the OEWL sequence's serving steps 4–5 are dropped as out of scope here.

## 4. Preserved disagreements

| ID | Disagreement | Settling evidence |
|---|---|---|
| X1 | Prototype is working machinery (WA §3 load-bearing) vs. a tautology wearing a suite (WA §2.2). Unresolvable by wording | A2 executed. Until it runs, the version may claim *predicate law*, never *governed binding* |
| X2 | Promoted state is `active` (LIFECYCLE) vs `promoted` (schema enum); LIFECYCLE:36 disclaims its own binding force | A decision-gate record naming one enum as binding for ontology versions. Owner: decision-gate + definitions-governance |
| X3 | WOR precedent repaired (PF, executed receipts) vs seven runtime owners absent (GOV/PF) | An owner registration for `kind.runtime_contract` from task-session after owner gates |
| X4 | Whether the four `SNAPSHOT_CONTRACT_BINDING_MISMATCH` failures still reproduce — PF states it executed nothing; WA ran other suites, not this one | Execute the Node suite named in `ontology-working-prototype-gap…` entry `:87`, `:130-131` |
| X5 | Inventory read model vs working folder as dispatch-state truth — the stale entry produced this dispatch's own false premise (CONTEXT-CORRECTION) | The owed completion entry. Owner: parent, post-result hook |

## 5. Unresolved rows

| Row | Missing evidence | Owner |
|---|---|---|
| OQ-1, OQ-2 | Both **OPEN**; no validator decision (`AUTHORITY-MODEL.md:155-165`) | authority route |
| CR-1, CR-2 **CRITICAL** | Unactioned: route 3 mis-points (`CLAUDE.md:67`, `AGENTS.md:176`); no definition card for `authority kind` / `canonical kind` | definitions-governance |
| OVS-GATE-003 | No gate file exists in `decision-gates/` | DomainSpec handoff route |
| Cross-project migration | No owner route (`OVS-GATE-004:142-144`) | unassigned |
| Authority-ledger validator | Absent (`LIFECYCLE-MODEL.md:58-62`) | unassigned |
| `specializes` law | Owner unbound | unassigned |
| Anything resting on `attacks.md` | CR-9: three fabricated quotes; "must not be cited as independent confirmation" | excluded from this synthesis |
