# RWO–Eve Research Runtime Findings

## Artifact state

- Dispatch: `2026-08-13-rwo-eve-research-runtime-repair-002`
- Output contract: `schema:findings-artifact:v1`
- Decision: `SELECT_TOPOLOGY_DEFER_EXECUTION`
- State: findings candidate awaiting an exact audit; neither `AuditAcceptanceV1` nor `FinalApprovalV1` has been issued
- Evidence boundary: the evidence-closure-bound replacement blueprint and its two fresh independent reviews only

## Finding

The evidence supports selecting an authority-preserving RWO–Go–Eve topology as a blueprint and deferring execution.

DomainSpec and humans retain strategy, authorization, gates, and parent final approval. RWO remains the only semantic scheduler: it creates immutable commands, admits accepted events, and advances semantic cursors. A future durable Go coordinator may persist and physically deliver those already-created commands, manage attempts and fencing, correlate sessions, and perform recovery and reconciliation, but it may not invent commands. Eve is a bounded leaf executor: one generic root task session per admitted seat, with delegation and Workflow disabled, and with no ownership of the research graph or authority.

This separation is material. Moving semantic scheduling into Go or Eve would violate `A-SINGLE-SCHEDULER-01`; removing RWO is therefore a discriminating ablation, not a harmless implementation substitution.

## Closed blueprint obligations

| Obligation | Evidence-closed result | Boundary |
| --- | --- | --- |
| Canonical payload and identity | Eight action payloads, identity preimages, and unique command identities reproduce under `CanonicalJSONV1`. | Exact reviewed blueprint bytes; no command ran. |
| Per-action manifest, scope, output, and owner | Eight manifests and eight scope bindings reproduce; all 13 producer links are exact and acyclic. | Literal contracts and hashes only; dynamic output bytes bind later through `AcceptedEventV1.output_sha256`. |
| Discriminating crash cuts | Eight distinct cut points specify changed state, unchanged state, classification, and recovery. | Passes at blueprint level; no crash injection ran. |
| Missing and denied tool approval | Pending approval and explicit denial are distinct; both require zero tool invocation and zero tool effect. Exact approval permits one bounded noop invocation but is not seat completion. | Approval-control blueprint only; no tool ran. |
| Single semantic scheduler | Eight commands bind eight distinct authorization facts, and neither Go, Eve, final approval, nor closeout may create commands. | Passes at blueprint level; no runtime assertion ran. |
| Parent final approval | `FinalApprovalV1` is parent-owned, digest-bound, follows `AuditAcceptanceV1`, and is a separate zero-command transition. | Contract defined; approval not issued. |

All six evidence-closure rows pass. There are no unresolved or symbolic obligations inside this bounded writer gate.

## Deterministic construction

The blueprint defines `CanonicalJSONV1` as compact UTF-8 JSON with lexicographically ordered object keys, preserved array order, base-10 integers, and rejection of floats, duplicate keys, undefined values, and undeclared fields. It uses explicit domain separation for command identity, tool-request identity, and the composed candidate.

The declared eight-action graph is:

1. two independent exploration seats;
2. one synthesis seat over both admitted explorer outputs;
3. two independent review seats over the synthesis;
4. evidence closure over the synthesis and both review results;
5. findings writing over the evidence-closed inputs; and
6. audit over the findings and closure.

The two reviewers independently reproduced the construction over the same 67,521-byte synthesis:

- 8/8 payload digests, 8/8 input-manifest digests, 8/8 scope-binding digests, 8/8 identity-preimage digests, and 8/8 unique command identities passed;
- 13/13 producer links passed and were acyclic;
- 7/7 source selectors resolved;
- 10/10 component digests passed;
- the tool request reproduced as `toolreqv1:b0e0fa10076fa75e5a33ea8773f22e9d2799d32c46fdbf889daa7867bae5f1b0`, while missing-newline and wrong-version separator controls remained distinct; and
- the `RuntimeSynthesisCompositionV1\n` preimage was 7,554 bytes with SHA-256 `023c3cc12e8ca8dbb625195eb068403e2fe22fa2482eebb4734e783d972e8edb`, producing candidate SHA-256 `240acfe02fe8ac88a976b740cfc618e7f8835e7e5e5f7cb344fcbd65b133769e`.

These results establish internal reproducibility of the blueprint. They do not establish that the declared graph, commands, adapters, or recovery behavior exist in a runnable system.

## Failure, retry, and replay model

The eight blueprint cut points cover:

- failure before an accepted-event transaction;
- failure inside the journal/cursor/outbox transaction;
- failure after outbox commit but before acknowledgement;
- failure after attempt preparation but before POST;
- ambiguous delivery after Eve may receive a create request but before session mapping;
- failure after session persistence but before stream attachment;
- failure after raw terminal observation but before validation/admission; and
- failure after terminal admission but before worker acknowledgement.

The required residue is fail-closed: atomic rollback for partial transactions, inert replay for already committed events, same-attempt continuation before a first POST, reconciliation instead of blind repost after ambiguous delivery, reconnect to a known Eve session rather than creating another, and at-most-once admission of the same terminal bytes. These are specified controls, not observed crash-recovery results.

## Approval and closeout boundaries

Tool approval is request-specific and bound to the exact tool, arguments digest, command, session, and attempt. Missing, denied, stale, wrong-session, wrong-attempt, wrong-argument, and domain-separator-drift cases cannot authorize invocation. Even an exact approval authorizes only one invocation of the declared noop and cannot substitute for a valid terminal seat result.

Audit also cannot substitute for final approval. After an exact `AuditAcceptanceV1`, the state remains `await-parent-final-approval`. Only a separately issued, digest-bound parent `FinalApprovalV1` can make closeout eligible; that transition creates no command. A missing, stale, divergent, or wrong-owner approval leaves closeout absent.

## Review and repair disposition

The replacement synthesis incorporated the single authorized repair loop. Fresh round-002 reviewers then returned:

- non-vacuity review: `PASS`, with no findings or blockers; and
- authority review: `PASS` / `KEEP`, with no findings or blockers.

The closure joined both reviews over the identical synthesis digest and opened only the bounded findings-writer gate. It did not issue audit acceptance, parent final approval, or implementation authorization.

## Remaining gaps

- No Eve runtime was installed or executed.
- No compiler, durable Go coordinator, adapter, fixture, validator, or product behavior was implemented or executed.
- Eve compatibility, session behavior, delivery semantics, tool behavior, retry/replay behavior, and crash recovery remain unverified at runtime.
- Dynamic upstream output bytes remain future `AcceptedEventV1.output_sha256` bindings.
- Implementation readiness and lifecycle synchronization are not established.
- This findings artifact still requires an exact audit. Parent final approval remains a later, separate gate after an accepted audit.
- No authority or ontology promotion, credential use, external effect, Git commit or push, publication, deployment, or production release occurred.

## Bound evidence

| Artifact | SHA-256 | Bytes | Use |
| --- | --- | ---: | --- |
| `receipts/evidence-closure.json` | `79ff3103db6521c0bff211fac981075a36a9238a2d73555ece31f5989a5f6154` | 16,319 | Opens the writer gate only. |
| `receipts/runtime-synthesis.json` | `784756aa522d049134cbe304090c97472960d5e94edc339d4fe2ac911ddde7d7` | 67,521 | Exact repaired blueprint. |
| `receipts/reviewer-non-vacuity.json` | `a903d67f3ff52efed3e83f80d3942f565df9e6c56f119e8e2f93a5a9a593584e` | 4,993 | Fresh independent reproducibility and non-vacuity PASS. |
| `receipts/reviewer-authority.json` | `56652ec91f86ce932ff342bc8967546a2c1cb7ffd1e565ccdba671f0f8d02276` | 4,505 | Fresh independent authority PASS / KEEP. |

## Claim ceiling

This artifact reports an exact-bound, evidence-closed, independently reviewed blueprint and selects its topology for later consideration. It proves internal blueprint consistency and writer eligibility only. It does not prove executable Eve behavior, runtime compatibility, implementation or implementation readiness, audit acceptance, parent final approval, lifecycle completion or synchronization, authority or promotion, product behavior, publication, deployment, production readiness, commit, push, credentials, or any external effect.
