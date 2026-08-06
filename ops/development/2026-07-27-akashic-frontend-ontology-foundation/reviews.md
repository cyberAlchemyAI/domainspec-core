# Frontend and graph candidate reviews

## Rittel, Horst — precedent gate

action_id: `spawn-0005`  
status: `pass_with_repairs`  
validation: Read-only precedent-gate review completed against the dispatch sheet, synthesis receipt, `synthesis.md`, `research.md`, cited Akashic runtime contracts, private CyberAlchemy candidate precedent, and workspace UI precedent. No writes or external browsing occurred.

Precedent-gate verdict:

| Candidate/pattern | Gate label | Ownership finding |
|---|---|---|
| Candidate 1: reviewed principle explorer + bounded question panel | `build-from-owned` | Akashic owns the reviewed feed, Q1–Q6 implementation, closed request/result schemas, digests, and diagnostics. It does not own a deployed browser or HTTP adapter. |
| Candidate 2: static reader + server-rendered query pages | `build-from-owned` | Same Akashic-owned inputs; no deployed server/template surface was found. |
| Candidate 3: graph-first canvas | `searched precedent-clean` | No deployed Akashic graph canvas was found in the workspace-scoped search. Comparable graph/UI ideas do not supply Akashic ownership or justification. Precedent does not kill it; lack of a capability witness supports deferral. |
| Stable node identity | `already-deployed` | Akashic feed and runtime already expose authored record, entry, group/domain, evidence digest, and snapshot identities. |
| Source references | `already-deployed` | Akashic already owns authored origins and evidence source/selector/scope. |
| Confidence | `searched precedent-clean` | Private CyberAlchemy has candidate confidence fields; no executed Akashic confidence contract was found. Rejection from v1 is correct. |
| Challenge/residue | `build-from-owned` | Akashic owns gap, indeterminate, and structured diagnostic states; a broader challenge protocol is not owned and must not be imported. |
| Typed endpoints | `build-from-owned` | Existing Akashic relation tuples and query traversal support candidate endpoint signatures, but the proposed public graph profile is not deployed schema. |
| Direction | `already-deployed` for authored relations; `build-from-owned` for UI reverse labels | Runtime traversal preserves authored direction. Reverse labels remain a proposed view convention. |
| Evidence references | `already-deployed` | Evidence handles, digests, selectors, relations, and scope are Akashic-owned executed contracts. |
| `authority_effect:none` | `already-deployed` | It is present in the public-safe Akashic reviewed feed and schema; CyberAlchemy is not its owner here. |
| Cardinality | `build-from-owned` | Exact-one group membership is feed-grounded; other graph-profile cardinalities are candidate derivations and need schema-owner approval. |
| Default denial | `build-from-owned` | Closed Akashic schemas provide local precedent, but the proposed allowed-edge catalog is new. Private `ALLOWED-EDGES.yaml` is restricted to four CyberAlchemy Evidence kinds and cannot own or define Akashic edges. |
| Inverses as read views | `build-from-owned` | Sensible candidate convention, not an executed Akashic contract. |
| Cycle policy | `build-from-owned` | The endpoint-family argument is an architectural derivation. CyberAlchemy’s value-cycle guard remains private candidate precedent and cannot govern Akashic directly. |
| Projection separation | `already-deployed` | Authored records, generated Inventory, reviewed feed, and current pointer are concretely separate Akashic artifacts. |
| Stable `data-od-id` testing hooks | `already-deployed` only under UI Prototyping Studio ownership | Reusable workspace precedent, not Akashic deployment or usability proof. Akashic must own any selector namespace it adopts. |

Load-bearing verification:

- `graph-queries.mjs#SUPPORTED_OPERATIONS`, `#assertAuthoredState`, `#principleCoOccurrenceAndTensionStatus`, and `#executeGraphQuery` support six closed operations, exact authored-state binding, indeterminate tension status, canonical result digests, and structured failures.
- `example-feed.json#/` supports seven entries, stable identifiers, authored origins, scoped evidence handles, `authority_effect:"none"`, explicit forbidden actions, and claim ceilings.
- `query-contracts.schema.json#$defs/graph_query_request|graph_query_result` supports closed query unions.
- `cyberAlchemy-v2/ontology/README.md#Ontology` explicitly says the ontology is candidate-owned and cannot promote itself or redefine runtime/schema/public claims.
- `RELATION-MODEL.md#Relation Contract|Value-Cycle Guard|Endpoint Rule` is private candidate precedent only.
- `canonical-kinds/ALLOWED-EDGES.yaml` explicitly scopes its default denial to four private Evidence kinds; it is not reusable as an Akashic catalog.
- Workspace search found no Akashic browser app, HTTP adapter, frontend toolchain, or graph canvas. Existing Akashic HTML files are explanatory artifacts, not the proposed deployed frontend.

Exact repair requests:

1. Replace “reuse structurally” for Akashic evidence handles, `authority_effect:none`, and projection separation with “already deployed in Akashic; private precedent independently asks similar questions.” This prevents false CyberAlchemy ownership.
2. Add a `precedent_status` column to every frontend and graph-pattern table using exactly `build-from-owned`, `already-deployed`, or `searched precedent-clean`, alongside the separate `reuse/adapt/reject` decision.
3. Qualify `searched precedent-clean` as “workspace-scoped; external precedent search was forbidden in this action.” Do not claim global novelty.
4. Change “all authored edge families are acyclic” to “cycles are structurally unavailable under the current proposed endpoint-kind partition; this is candidate reasoning, not a validated Akashic cycle contract.”
5. Change `EvidenceHandle` “content-addressed by evidence_digest plus source/selector/scope” to an explicit candidate composite identity rule, or keep it as a nested evidence value. Current contracts expose those fields but do not establish a graph-node identity schema.
6. Split `Principle or illustration relation -> EvidenceHandle` into separately typed candidate edges. “Principle or relation” collapses node and relation ownership and leaves the source endpoint ambiguous.
7. Do not state `grouped_in exactly 1 for feed Principle` as a general graph invariant. Scope it to the reviewed-feed projection unless the Akashic schema owner promotes it.
8. Keep `co_occurs_with` explicitly non-persisted and derived from shared-paper witnesses. Do not call it an allowed declarable edge.
9. State that stable `data-od-id` hooks are UI Prototyping Studio-owned workspace precedent with shimmed-e2e caveat; adoption creates new Akashic-owned selectors and proves only deterministic correspondence.
10. Preserve all three frontend candidates. Precedent does not kill Candidate 3; its v1 deferral rests on missing Akashic capability evidence, complexity, and semantic risk.

artifacts:

- `ref receipts/reviewer-precedent.json` — not written, returned here for parent normalization.
- Consulted: dispatch sheet, `receipts/frontend-graph-synthesis.json`, `synthesis.md`, `research.md`, cited Akashic feed/schema/query/CLI sources, four permitted private ontology sources, and cited UI Studio findings.

blockers:

- External primary-source precedent search was explicitly forbidden, so `searched precedent-clean` is workspace-scoped only.
- No approved public Akashic graph schema, browser adapter, frontend deployment, usability evidence, or accessibility-conformance evidence exists.

## Russell, Bertrand — non-vacuity gate

Non-vacuity review result: `pass`. No candidate is killed; each admits a concrete screen-level witness. Candidate 3 remains unsuitable for v1 on complexity and semantic-risk grounds, but non-vacuity alone cannot kill it.

### Witness matrix

| Candidate | Smallest exact screen witness | Typed graph result | Distinct failure | Honest ceiling | Verdict |
|---|---|---|---|---|---|
| 1. Reviewed Principle Explorer | Browse exactly `At, Co, Cr, Ft, Gr, Is, Mo`; select `At` / `entry:claim:at`; show authored origin, two evidence handles, and entry ceiling; invoke Q4 and display its typed evidence groups. The same closed panel exposes Q1–Q5, with Q6 isolated behind base/target snapshot inputs. | Exact `graph_query_result` union: operation, `authored_input_digest` or snapshot IDs, typed `results`, and `result_digest`. Q5 shows witnessed co-occurrences plus `tensions: []` and `tension_status: indeterminate`. | Diagnostic view replaces or marks stale the prior result for `source_state_mismatch`; separately labels `invalid_input`, `unsupported_expression`, empty result, indeterminate Q5, and missing Q6 prerequisites. | Persistent feed/entry ceiling: reviewed read-only projection, not truth, authority, promotion, publication, freshness, deployment, or usability evidence. | PASS |
| 2. Static reader plus server-rendered query pages | One semantic page renders the same seven exact entries. The `At` section expands its two evidence handles and posts an `EvidenceForPrinciple` form; result page carries operation, bound digest, typed evidence groups, result digest, and return context. Six closed forms cover Q1–Q6. | Same closed result union rendered server-side; no loss of operation-specific types is necessary. | Dedicated HTTP-rendered diagnostic template, distinct from an empty-results template and Q5 indeterminate state; Q6 missing inputs remain prerequisite failure. | Same explicit ceiling and snapshot label; static generation must not be called live or fresh. | PASS |
| 3. Graph-first canvas | Render `At` as `Principle claim:at`, its `grouped_in → Group reliability`, and two `evidenced_by → EvidenceHandle` inspector rows. Selecting `At` and Q4 opens the exact typed evidence result; Q5 adds only derived `co_occurs_with` views witnessed by paper IDs and an inspector stating `tension_status: indeterminate`. Q1–Q6 remain closed overlays, with Q6 as a non-persisted two-snapshot comparison. | Possible through the same typed result union; canvas marks are projections of results, never arbitrary traversal or persisted inferred edges. | A non-canvas diagnostic region must replace/disable the overlay on mismatch or invalid input; empty, indeterminate, and prerequisite states remain separate. | Visible statement that nodes/edges are read-only projections with `authority_effect:none`; no completeness, truth, persisted relation, authority, or arbitrary traversal claim. | PASS, not recommended for v1 |

### Exact repairs requested

1. Candidate 1: name the literal typed result fields in its component contract: `operation`, `authored_input_digest` or `base_snapshot_id`/`target_snapshot_id`, operation-specific `results`, and `result_digest`.
2. Candidate 1: do not call the seven-entry reviewed feed the query RecordSet. Their provenance bindings are related but distinct; the adapter must expose which source backs each view.
3. Candidate 2: specify that static build identity is displayed independently from query-time authored-input binding, preventing a stale page from appearing current.
4. Candidate 2: require failure templates to invalidate prior-success presentation, not merely append an error banner.
5. Candidate 3: provide a mandatory semantic list/table equivalent for every canvas result and keyboard traversal.
6. Candidate 3: prohibit inferred `tensions_with` and arbitrary edges; permit only authored typed edges and derived, paper-witnessed `co_occurs_with`.
7. All candidates: Q3 requires exactly two distinct closed domain IDs; Q6 requires two explicit snapshot IDs plus its impact index and server-loaded snapshots.
8. All candidates: preserve the exact Q5 distinction: empty `tensions` with `tension_status: indeterminate` is not “no tension.”
9. All candidates: display `source_state_mismatch`, `invalid_input`, `unsupported_expression`, empty result, Q5 indeterminate, and missing-Q6-input states as distinct outcomes.
10. All candidates: retain the ceiling that this is candidate architecture without HTTP, browser-security, accessibility/usability, publication, deployment, live transport, agent-execution, or ontology-promotion evidence.

```json
{
  "output_ref": "ops/development/2026-07-27-akashic-frontend-ontology-foundation/receipts/reviewer-non-vacuity.json",
  "written": false,
  "action_id": "spawn-0006",
  "status": "pass",
  "validation": "pass: read-only exact-source review; seven feed entries, Q1-Q6 request/result unions, digest binding, structured diagnostics, Q5 indeterminate semantics, Q6 prerequisites, and claim ceilings verified",
  "artifacts": [
    "ops/development/2026-07-27-akashic-frontend-ontology-foundation/dispatch-sheet.json",
    "ops/development/2026-07-27-akashic-frontend-ontology-foundation/receipts/frontend-graph-synthesis.json",
    "ops/development/2026-07-27-akashic-frontend-ontology-foundation/synthesis.md",
    "ops/development/2026-07-27-akashic-frontend-ontology-foundation/research.md",
    "projects/akashic-records/agent-pool/reviewed-content/example-feed.json",
    "projects/akashic-records/src/graph-queries.mjs",
    "projects/akashic-records/schema/query-contracts.schema.json",
    "projects/akashic-records/src/cli.mjs"
  ],
  "blockers": []
}
```
