# DomainSpec v2 — First Production Release Roadmap

Status: **auditor-approved roadmap; not roadmap-ready for execution; production unauthorized**

Scope: private repository-local DomainSpec-v2 CLI, first target `0.1.0`

Witness: bounded Body War SuggestedTrack / Parque Taquaral scenario

Continuation authority: `projects/domainspec-v2/.craft/ledger.yml`

This is the canonical operational projection of the accepted product contract and the expanded-frontier research. It does not promote definitions, establish conformance, accept a pilot, or authorize a release. Detailed evidence, proof commands, exact target paths, dissent, and open questions remain in [findings.md](research/2026-07-12-expanded-capability-frontiers/findings.md). The old roadmap findings remain immutable history.

## Release claim

The first release must show that, for one exact supported profile and one exact candidate, DomainSpec-v2 can:

1. govern a finite business plane and map it into authoritative specification sources;
2. produce a complete typed specification projection;
3. enforce finite architecture and composable-pattern catalogs;
4. exhaustively explore declared finite formal bounds with no indeterminate result;
5. derive an independently owned nonempty obligation universe and generate executable verification for every obligation;
6. derive a structural implementation graph over frozen code roots;
7. adjudicate named directional conformance predicates across the contract planes;
8. reproduce one clean, supported, recoverable CLI candidate; and
9. pass a controlled `14/14` Body War pilot before separate claim acceptance and external authorization.

“Full coverage” means exact equality with the authority-owned profile obligation set, every required positive and negative outcome, zero skip/todo/orphan/unrunnable items, and a killed mutation for every obligation key. It does not mean runtime-path coverage or proof of undiscovered requirements.

“Equivalence” is restricted to the declared bounded `Sg→G→Sg_canonical` retraction. All other relations are directional traceability, preservation, realization, or conformance predicates. DomainSpec-v2 does not claim universal code/spec identity.

## Authority and evidence separation

```text
B = (BO, BK, provenance, authority receipt)
  → authoritative Spec
  → Sg typed projection
  ├─→ A_req architecture requirements ────────┐
  ├─→ F_struct / F_state proof artifacts ─────┤
  ├─→ O_spec → T_gen → E_run ─────────────────┤
  └─→ G internal IR → Sg_canonical retraction │
                                               ▼
frozen code roots → I_struct ───── cross_graph_conformance_vector
                                               │
                                               ▼
                                 implementation acceptance
                                               ▼
                                  independent verification
                                               ▼
                                  external release authorization
```

Contract planes are `B`, `Sg`, `A_req`, `O_spec`, `T_gen`, and `I_struct`. `G`, `F_struct`, `F_state`, and `E_run` are internal proof/evidence artifacts unless the supported product contract explicitly exposes them. Generated graphs are deterministic projections, never parallel semantic authority. Generated tests are programs, not execution evidence and not their own oracle.

## Ordered route

| Node | Outcome | Depends on | Execution lane | Current status |
|---|---|---|---|---|
| `FPR-00` | Accepted product decision | — | external owners | closed at decision altitude |
| `FPR-01` | One ratified non-contradictory authority baseline | `FPR-00` | authority | blocked/open |
| `FPR-02` | Machine product, profile, pilot, claim, negative, rollback, origin, and redaction contract | `FPR-01` | product/profile | blocked |
| `FPR-03` | Governed `BO`, `BK`, `B`, contradiction policy, and total `B→Spec` mapping | `FPR-02` | business semantics | blocked |
| `FPR-04` | Total `Spec→Sg` projection and independently checked bounded `Sg/G` retraction | `FPR-03` | semantic engine | blocked |
| `FPR-05` | Finite `A_req` catalogs and fail-closed architecture/pattern enforcement | `FPR-04` | architecture | partial; integration blocked |
| `FPR-06` | Pinned `F_struct/F_state` profile, exhaustive bounded results, replayable counterexamples | `FPR-04` | formal | research exists; integration blocked |
| `FPR-07` | Independent obligations, generated tests, executions, zero-gap checks, per-key mutation receipts | `FPR-04/05/06` | verification generation | partial/false-green |
| `FPR-08` | Frozen-root AST/symbol/import/call graph and complete tag reconciliation | `FPR-04/05` | implementation structure | partial/false-green |
| `FPR-09` | All required directional contract and internal-assurance predicates pass | `FPR-03..08` | conformance join | absent |
| `FPR-10` | Exact Body War auth/consent/redaction/origin/API journey | `FPR-02`, executable app | Body War behavior | current pack nonconformant |
| `FPR-11` | Self-contained, state-safe, security-bounded, operable, supportable CLI | `FPR-02` | release substrate | partial/absent |
| `FPR-12` | One clean reproducible candidate and seeded-red CI gate | `FPR-04..11` | release engineering | absent |
| `FPR-13` | Controlled Body War pilot, `14/14`, rollback/revocation/support/reproduction | `FPR-09/10/11/12` | pilot | absent |
| `FPR-14` | Craft expected-state equality and persistent reopen surface | seed before claims; close after `FPR-13` | continuation | seeded; equality not proved |
| `FPR-15` | Separate claim acceptance, external authorization, immutable private release | `FPR-13/14` | release authority | unauthorized |

The machine-readable node/edge/frontier projection is [expected-node-edge-manifest.yml](craft/expected-node-edge-manifest.yml). Its target paths are proposals until the owning node creates them.

## Dependency and parallelism policy

```text
FPR-00 → 01 → 02 → 03 → 04
                         ├─→ 05 ─┐
                         ├─→ 06 ─┤
                         ├─→ 08 ─┤
                         └─→ 07* ┤
                                  ├─→ 09 ─┐
FPR-02 → 10 ──────────────────────────────┤
FPR-02 → 11 ──────────────────────────────┤
                                          ▼
                                  12 → 13 → 14 → 15
```

`FPR-05`, `FPR-06`, `FPR-08`, `FPR-10`, and `FPR-11` are the main parallel lanes after their named inputs stabilize. Generic `FPR-07` machinery may begin after `FPR-04`, but it cannot close before architecture and formal obligation classes arrive. `FPR-09` is the technical join; `FPR-13` is the runtime/human join. Work before `FPR-02/FPR-04` must not mint competing denominators or graph schemas.

## First execution frontier

The next move is `FPR-01`, not implementation:

- reconcile 13/14 backend-type, 24/25 candidate-type, and 30/31 relationship-signature projections;
- decide how the active contract→authoring ontology lens relates to the accepted business-plane→spec chain;
- identify stale projections without choosing the favorable count;
- produce `authority-baseline.yml` and an owner-ratification receipt; and
- prove one deliberate authority-count/reference mutation is rejected.

Only then may `FPR-02` enumerate the exact supported profile, claims, roots, languages, obligation kinds, callback/origin route, redaction allowlist, and release roles.

## Persistent frontiers

The Craft context `CTX-DSV2-FIRST-PRODUCTION-RELEASE` owns continuation. Stable unresolved frontiers are:

- `FR-FPR-ONTOLOGY-DIRECTION` — authority direction and supersession semantics;
- `FR-FPR-SOLVER-PROFILE` — formal languages, solver versions, bounds, timeout, and fairness/liveness policy;
- `FR-FPR-BW-ORIGIN-ROUTE` — real-provider callback/deployment/origin and redaction allowlist;
- `FR-FPR-I-ROOT-DISPOSITIONS` — complete Body War root and non-code disposition set; and
- `FR-FPR-APE-SELF-CONTAINMENT` — v2-only catalogs or a promoted shared-method dependency.

Lifecycle:

```text
observed → triaged → researching | proposed | rejected | deferred
researching → proposed | rejected | deferred
proposed → accepted → scheduled → verified → closed
rejected | deferred | verified | closed → triaged on an explicit trigger
```

Evidence expires when the candidate SHA, supported profile, authoritative `B/Spec`, mapping, toolchain, solver bounds, source roots, normalization policy, or relevant implementation changes. New research dispatches require a material dependency, the subagent trigger, a tensioned sheet, explicit human confirmation, registration, and closeout.

## Body War acceptance boundary

The witness is the SuggestedTrack / Parque Taquaral slice, not the whole TROQAR system. The critical-step denominator is exactly `CP-01` through `CP-14` in the approved findings: candidate identity, profile, business/spec mapping, architecture, formal, obligations, generated engine, implementation structure, cross-graph predicates, auth/consent/redaction, create-track, attach-evidence, rollback/revocation, and independent operation/support.

Pass requires `14/14`; no step can be waived. The accepted transition is only `needs_evidence→evidence_submitted`. The pilot must reject unsupported promotion to `source_backed`, verified geometry, scoring, leaderboard, accepted/rejected, or pilot-ready status.

## Binding exclusions

Do not add DomainSpec UI, hosted DomainSpec service, public distribution/SDK, multi-language support, automatic Saturn actuation, arbitrary application generation, universal program proof, proof of undeclared requirements, generic APE mint/inheritance/cross-project propagation, or automatic promotion/release authorization.

Hermetic builds, SBOM/SLSA, broad attestation, tabletop exercises, and central dashboards stay trigger-bound to the recorded threat/distribution model. Candidate identity, deterministic normalized output, private-boundary checks, state safety, rollback, support, and external authorization are not optional hardening.

## Release rule

No SemVer label, green component suite, generated test file, formal example, digest match, owner judgment, or pilot result independently establishes production. A release exists only when `FPR-00..14` applicable gates pass for one exact candidate, a claim owner accepts only the proved claims, an independent verifier reproduces the evidence, external owners authorize the exact bits and boundaries, and the release operator records the immutable private release under `projects/domainspec-v2/releases/RELEASE-ID/`.

## Sources

- Accepted scope: [product-release contract](decisions/2026-07-12-product-release-contract.md)
- Frozen evidence: [research.md](research/2026-07-12-expanded-capability-frontiers/research.md)
- Auditor-approved synthesis: [findings.md](research/2026-07-12-expanded-capability-frontiers/findings.md)
- Machine continuation projection: [expected-node-edge-manifest.yml](craft/expected-node-edge-manifest.yml)
- Craft authority: `projects/domainspec-v2/.craft/ledger.yml`
