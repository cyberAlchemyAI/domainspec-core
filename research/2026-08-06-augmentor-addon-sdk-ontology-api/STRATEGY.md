# Augmentor Ontology Add-on SDK/API Research Strategy

Status: `confirmation-ready`

Authority effect: `none`

## Direct strategy

Research the smallest owner-preserving way to expose the existing Augmentor
ontology consultation capability through the ResonantOS Add-on SDK.

This is not a greenfield ontology API study. Current source already contains:

- a private candidate ontology and neutral consumer-projection compiler;
- closed projection, glossary, query, result, and evidence contracts;
- leakage, version, freshness, budget, cache-isolation, and instruction-shaped
  text tests;
- an implemented `POST /augmentor/consultation` host route;
- route-scoped access, the `augmentor-consultation-read` bridge capability,
  answer policy, and local plus remote boundary tests; and
- Add-on SDK v0.1.0 manifest, registry, capability, tool, connector,
  `augmentorSkills`, and `memoryAccess` owners.

The exact gap is that Add-on SDK v0.1.0 does not model ontology consultation,
and its public `Capability` union does not contain the host route's
`augmentor-consultation-read` capability. The research must decide whether
the right seam is an additive manifest contract, a capability addition, a
generic tool or connector declaration, host-derived runtime discovery, a
hybrid of those, or no SDK change.

The study must not treat `augmentorSkills` as ontology data, `memoryAccess` as
ontology access, a manifest declaration as a grant, or consultation evidence
as instructions, approval, routing, memory writes, ontology writes, authority,
or permission to act.

## P1 trigger decision

Dispatch is required by all four Principle-1 triggers:

- **Synthesis:** current SDK/runtime bytes, private ontology/projection
  contracts, security/lifecycle boundaries, and external API precedents must
  be reconciled.
- **Context protection:** the exact source and test corpus is much larger than
  the parent should carry verbatim.
- **Isolation:** ontology semantics, SDK ergonomics, and threat analysis need
  independent methods before synthesis.
- **Parallelism:** three independent explorer lanes fit the active
  three-child runtime ceiling and can run together.

The live dispatch type is `research`; the admitted sheet uses schema `0.8.0`.

## Lanes, groups, and subagents

### Explorers — three parallel lanes

1. `Simon, Herbert` — **SDK, runtime, and comparative API lane**
   (`explorer`, 4,800-token target). Traces current Add-on SDK types,
   validation, registry, manifests, grants, bridge capability tokens,
   consultation route/client/service, reference API, and focused tests. It
   also checks current official API patterns for capability discovery,
   negotiation, versioning, read-only queries, and developer ergonomics.
   Expected output: current-versus-absent matrix, owner map, fit/non-fit
   precedent matrix, candidate TypeScript/JSON shapes, compatibility and
   lifecycle rules, and positive/negative fixtures.

2. `Ashby, W. Ross` — **ontology and neutral-projection lane**
   (`explorer`, 4,800-token target). Traces the private ontology, source
   digests, nodes, relations, views, residue, neutral compiler, schema closure,
   opaque source handles, structured conflicts, explanation support, and
   consultation query/result semantics. Expected output: public-safe metadata
   boundary, contract/version invariants, projection approval and installation
   owners, candidate static/service/hybrid shapes, and leakage plus semantic
   collapse reject tests.

3. `Turing, Alan` — **security and lifecycle lane**
   (`explorer`, 4,600-token target). Threat-models a malicious add-on, stale or
   mixed bundles, injection-shaped records, overbroad views, cache cross-talk,
   credential or path leakage, insecure remote access, downgrade, disable,
   revoke, uninstall, and attempts to turn evidence into authority or effects.
   Expected output: host-derived versus manifest-trusted fields, capability and
   grant decision, threat/control matrix, deterministic negative tests, and
   the exact degraded-mode behavior.

The explorer anti-bias axis is a composite of methodology and source corpus:
empirical current-byte tracing plus official API precedent, formal ontology
modeling, and adversarial security analysis. All three pairwise disagreements
are embedded in the admitted sheet.

### Synthesis, rejection gates, writing, and audit

- `Shannon, Claude` (`synthesizer`) joins the three explorer receipts into one
  exact current-versus-target decision package and selects or kills each
  integration option.
- Three reviewers run in parallel:
  - `Lakatos, Imre` attacks precedent and duplicate ownership.
  - `Gödel, Kurt` attacks non-vacuity and requires a finite
    manifest-to-grant-to-bridge witness plus discriminating failures.
  - `Quine, Willard Van Orman` attacks definitional and authority collapse.
- The parent performs exact-binding evidence closure.
- `van Lamsweerde, Axel` (`writer`) may write only `findings.md` after closure.
- `Brandenburg, Martin` (`auditor`) audits the result; the parent remains the
  final approver.

Nine pooled research agents are declared. The two earlier check-tension
helpers were gate infrastructure, not members of this dispatch.

## Dependency flow

```text
three explorers in parallel
  -> synthesizer
  <-> three reviewers in parallel
  -> exact-binding evidence closure
  -> writer
  -> auditor
  -> parent final approval
```

- One bounded synthesizer-to-explorer feedback edge may repair missing source
  bindings.
- The synthesizer/reviewer zig-zag has a loop cap of two.
- One auditor-to-writer feedback edge may repair presentation when evidence
  already exists.
- Every spawned agent must be joined and closed before success is reported.
- The parent mechanically assembles `research.md` from verbatim explorer
  returns; the writer never authors or rewrites that source record.

## Inventory preflight

The owner machine index passed lookup readiness with zero failures and 146
inherited uncontrolled-tag warnings. The target ResonantOS checkout has no
repository-local Inventory, so target claims must be verified directly from
current product bytes.

Selected owner evidence:

- verified Arcanum-to-ResonantOS add-on research for the retained installer,
  manifest, capability, bridge, host, state, and Augmentor projection owners;
- verified Augmentor unified-agent architecture for the three-plane and
  no-second-owner boundaries; and
- verified Augmentor user-graph/reasoning research only where source-bound,
  disposable projection semantics are relevant.

Excluded:

- routing/session research, because it is outside this API seam unless a
  proposal wrongly expands consultation into live route state;
- the earlier unified-agent strategy, because its completed result supersedes
  it; and
- target Inventory evidence, because no target index exists.

The concrete design consequence is that research begins from the existing
neutral-projection and `POST /augmentor/consultation` owners. It must not
invent another ontology service, registry, graph store, grant owner, or
authority path. Inventory remains a discovery read model, not proof or
dispatch authority.

## Required research output

The final findings must contain:

1. current-state contract and owner map;
2. exact SDK/runtime mismatch and other gaps;
3. option and kill matrix for no change, `augmentorSkills`, generic tool or
   connector, additive `ontologyConsultation`, a capability addition, and
   host-derived or hybrid discovery;
4. selected TypeScript and JSON contract examples;
5. version and compatibility negotiation;
6. registry, validation, grant, UI, projection-installation, query,
   answer-policy, cache, audit, revoke, disable, upgrade, rollback, and
   uninstall flows;
7. public/private packaging boundary and host-derived facts;
8. threat model and fail-closed status vocabulary;
9. dependency-ordered implementation slices without implementation authority;
10. exact positive and negative test matrix;
11. one local executable witness; and
12. unresolved owner decisions and claim ceiling.

Every load-bearing row must bind an explorer receipt to immutable source
identity, an exact source-local selector, evidence scope, and proof status:
`observed`, `executed`, `designed`, `absent`, or `blocked`.

## Executable witness requirement

The selected contract must support one finite local witness:

```text
concrete add-on manifest
  -> SDK validation
  -> visible capability request
  -> explicit reviewed grant
  -> host-derived consultation availability
  -> closed query
  -> POST /augmentor/consultation
  -> bounded source-backed result + answer policy
  -> revoke or disable
  -> honest degraded behavior
```

Negative fixtures must cover at least: undeclared or ungranted capability,
disallowed view, stale or malformed projection, mixed contract versions,
leakage, instruction-shaped ontology text, cache isolation, and any direct
write or authority inference.

A new manifest field without this route, or a working route that bypasses SDK
validation and grant owners, is not an acceptance witness.

## Gate and ledger state

- Confirmation readiness: `PASS`
- Live schema: `0.8.0`
- Final sheet SHA-256:
  `77915e0aa286b94d587746426f221b5a31236357c1ccff27d3bb56c85b6c57e3`
- Material-strategy SHA-256:
  `6206745262170f9798df45c0f2b045c7e5f94bee873ff8ef14218568ccfa9895`
- Ledger mutation during readiness validation: `none`
- Dispatch Spec: `PASS`
- Tension checker:
  `check-tension-checker-5d4b9e17-6ad2-4a48-b51e-5a19b64e46ef = PASS`
- Tension reviewer: `CT-REV2-77915E0A-6F2C91 = PASS`
- Prior four-explorer digest and verdicts: retired before confirmation because
  they exceeded the active three-child runtime ceiling
- Human confirmation: `pending`
- Registration: not appended
- Research execution: not started
- Findings: not produced
- Expected closeout after an authorized run: exactly one dispatch row, every
  agent joined and closed, and one paired close row

## Mutation and claim boundary

This strategy wrote only its research proposal artifacts. It did not modify:

- the private Augmentor ontology or neutral projection;
- the ResonantOS checkout or Add-on SDK;
- projection installation or access grants;
- the append-only dispatch ledger;
- authority, promotion, deployment, release, or production state; or
- the unrelated dirty Mint and OAVA work already present in the parent tree.

Even a successful research run would produce an evidence-closed candidate
contract, not implementation authorization, an approved projection, a
capability grant, deployment, release, or production readiness.

## Post-result Inventory hook

The installed Inventory baseline remains ready with zero failures and 146
inherited warnings. Its deterministic append dry-run classified the new
strategy entry as `added` but returned `candidate-not-ready`: the updater
cannot currently stage a new entry page atomically with both projections.

The candidate page and record remain under `.arcanum/inventory/tmp/`. The
human and machine indexes were not changed, no manual bypass was used, and the
exact fail-closed receipt is stored beside this strategy. This read-model
residue has no effect on dispatch readiness, tension, or the human gate.

## Next human action

Reply exactly `confirmed` to authorize registration and execution of the
frozen material strategy, request a revision, or decline.
