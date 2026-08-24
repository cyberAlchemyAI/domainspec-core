# Explorer return — working artifact (what builds and passes today)

Agent: Bénabou, Jean · role explorer · dispatch `2026-08-20-ontology-stable-version-and-runtime-research`

**Claim ceiling.** Cited synthesis only. No ontology authority granted, no runtime
implementation authorized, nothing promoted, no decision gate lifted. Residue
`ontology-authority-not-granted` and `runtime-implementation-not-authorized` stand.
Every result below marked EXECUTED was run by me today; OBSERVED means read, not run.

---

## 1. Executable machinery and exactly what it verifies

### A. `cyberAlchemy-v2/implementation/ontology-candidate-graph-prototype`
EXECUTED `npm test` (= `node --test test/*.test.mjs`, `package.json:10`):
`# tests 59 / # pass 59 / # fail 0 / # skipped 0`.
Per-file (each run separately): candidate-v1 8, determinism 2, edge-grammar 10,
grounding 5, policy-disposition 12, research-lineage 5, run-writer 4,
terminal-receipt 8, write-isolation 5.

What it actually verifies:
- **Carrier shape** (`src/contracts/candidate-v1.mjs:286`): exact-field closure
  (`exactFields`, line 80), 4 node kinds only (`NODE_KINDS`, line 2), SHA-256
  `source_digest` (line 150), repository-relative selector (line 67), duplicate ids
  (line 268), unresolved endpoints (line 231), and `authority_effect === "none"`
  everywhere (`validateAuthorityEffect`, line 109).
- **Edge grammar** (`src/evaluator/edge-grammar.mjs:38`): a 12-entry hardcoded
  `ALLOWED_TRIPLES` Map (line 11), inverse-storage refusal (line 48-56 region,
  `INVERSE_EDGE_DECLARATION`), the session rule (`SESSION_CLAIM_FORBIDDEN`,
  `SESSION_EVIDENCE_FORBIDDEN`), and per-source cardinality.
- **Grounding** (`src/evaluator/grounding.mjs:13`): DFS cycle detection on
  `derives-from` only; root/path closure.
- **Evidence** (`src/evidence/run-writer.mjs:27`): `open(path,"wx",0o600)` refuses
  overwrite (line 9), fsync of file and directory, digest-map binding inputs →
  evaluators → outputs, terminal receipt written last (line 91).
- **Write isolation** (`scripts/verify-write-isolation.mjs:5`): hashes a protected
  selector set (EDGES.yaml, ALLOWED-EDGES.yaml, `cyberAlchemy-v2/authority/**`,
  `arcanum/**`, …) before/after and attests no mutation.

EXECUTED `sha256sum cyberAlchemy-v2/ontology/canonical-kinds/{EDGES,ALLOWED-EDGES}.yaml`
→ `f3ed1ed8…52e0d1` and `500851b1…0224b8`, which match the pinned constants at
`src/evaluator/edge-grammar.mjs:3` and `:5`. They agree **today**.

### B. `arcanum/arcana/ontology-vault/development/schema-validation-plan/tests/`
EXECUTED `python3 tests/validate_branch_schema.py` → `branch-schema-fixtures: PASS`
(exit 0). EXECUTED `python3 tests/validate_branch_json_schema.py` →
`branch-json-schema-fixtures: PASS` (exit 0). Scope: 11 valid + 9 invalid fixtures
under `fixtures/`, checked against `schema/branch-aware-ontology-candidate.schema.yml`
via `jsonschema.Draft202012Validator`. Its own docstring (line 3-4) says it is
"development-only … not a canonical Ontology Vault runtime contract."

### C. `cyberAlchemy-v2/implementation/ontology-evidence-workbench`
Everything I ran builds. EXECUTED, all exit 0:
`./node_modules/.bin/tsc -b --pretty false`; `vitest run` → `Test Files 26 passed (26) /
Tests 35 passed (35)`; `vite build` → `dist/assets/index-GH1VXHVj.js 403.60 kB … built
in 721ms`; `node scripts/validate-standalone-oew.mjs` →
`{"result":"pass","journeys":10,"errors":0}`; `node scripts/audit-active-frontend.mjs`
→ `{"result":"pass","findings":0,"migration":"51/51","historical_unchanged":true}`;
the `test:legacy` command → `# tests 212 / # pass 211 / # skipped 1`. The two
`historical:` suites I probed also pass (`test/upstream-lock.test.mjs` 6/6,
`test/l1-toolchain-bootstrap.test.mjs` 6/6). **Nothing here is broken.**

### D. Production corpus — the one validator over real data
EXECUTED `node projects/body-war/ontology/business/scripts/validate.mjs` →
`{"counts":{"lifecycle_policies":11,"nodes":237,"relations":231,"residue_items":6,
"sources":34},"receipt":"projects/body-war/ontology/business/receipts/
validation-receipt.json","status":"pass"}`. Its 16 diagnostic codes
(`scripts/validate.mjs:6-21`) include `BWO_SOURCE_DIGEST_MISMATCH`, and it really
hashes files on disk (`sha256File`, line 216; call site line 550). EXECUTED
`node --test tests/business-ontology.test.mjs tests/business-views.test.mjs` →
`# tests 15 / # pass 15`.

---

## 2. What none of it verifies

1. **No code parses the governed YAML.** `grep -rn "EDGES.yaml"` over the prototype's
   `src/`, `test/`, `scripts/` returns only digest constants and protected-path
   strings. `ALLOWED_TRIPLES` (12 entries) is a **hand transcription** of
   `ALLOWED-EDGES.yaml:16-48`. I compared them by eye — faithful today.
2. **The digest pin is not checked against the file.** Test 19, "binds the finite
   table to the governed source digests" (`test/edge-grammar.test.mjs:103-110`),
   asserts the constant equals a *literal*. It never reads the YAML. Editing
   EDGES.yaml breaks nothing in the suite. The only file-hashing guard is
   write-isolation, which proves the file *didn't change* — the opposite obligation.
3. **Scope is 4 kinds and 4 predicates.** `ALLOWED-EDGES.yaml:3`: "Every other kind
   is deferred." `specializes` has no law — `policy-disposition.mjs:57` hardcodes
   `policy-indeterminate` / `POLICY_OWNER_UNBOUND`.
4. **The prototype never touches the production corpus.** Its universe is one
   5-node/4-edge carrier plus 8 one-condition mutation descriptors and 1 additive
   descriptor (`fixtures/cases/`).
5. **No cross-package coherence anywhere.** OBSERVED: 76 directories named
   `ontology` (find, excluding node_modules/.git); ~12 are non-staged production
   ones. Their `schema_version` families are disjoint — `body-war-business-node/v1`
   (237) and `body-war-whole-system-relation/v1` (301); `animejs.agent-knowledge-vault.*`;
   `ontology.graph.v0.1` (auth-user-management); `rwo-*` (orchestrator); bare
   semver `1.0.0`/`2.0.0` (augmentor). No tool checks any of them against
   `cyberAlchemy-v2/ontology/canonical-kinds/`.
6. **No query, no update, no identity over time.** Every writer is create-only
   (`open(...,"wx")`); there is no merge, revision, or read-by-predicate path.

---

## 3. Load-bearing vs scaffolding

**Load-bearing** (real, reusable law): `candidate-v1.mjs` (closed-field contract);
`edge-grammar.mjs` (the session rule + inverse refusal are the sharpest rules in the
repo); `grounding.mjs`; `canonical-json.mjs` + `run-writer.mjs` (append-only,
digest-bound evidence); `verify-write-isolation.mjs`; **`body-war/.../validate.mjs`
— the only executable ontology check that runs over a 237-node real corpus and
verifies source digests.**

**Scaffolding**: `policy-disposition.mjs` — `POLICY_DIGEST` (line 1) and `EXPECTED`
(line 4) are both literals in the same file, so "rejects stale policy digest"
verifies a constant against itself; the only genuine branch is `specializes` →
indeterminate. `projection/research-lineage.mjs` and `cli.mjs` are single-fixture:
`evaluatePokerTeamO13` (`cli.mjs:15`) takes no argv and hardcodes one case.
The workbench's `historical:*` scripts, `upstream/` (620K) and `generated/` (55M)
are the README's own "historical evidence only" — dead weight that still passes.

---

## 4. What a runtime would have to add

1. **Read the law instead of transcribing it** — parse ALLOWED-EDGES.yaml, and hash
   it at test time. This is the single largest gap and it is small work.
2. **Ingest the real corpus.** Nothing today evaluates a production ontology
   directory through the candidate grammar.
3. **Kind and predicate coverage** past the 4 Evidence kinds, plus an owner binding
   so `specializes` resolves instead of returning indeterminate forever.
4. **Mutation semantics** — revise, supersede, merge. Every current writer is
   create-once; a runtime needs node identity that survives an edit.
5. **A parameterized read surface.** `projectResearchLineage` is one hardcoded view;
   a runtime needs query-by-request.
6. **Cross-family resolution** across the disjoint `schema_version` vocabularies
   above — or an explicit decision that they stay separate.
