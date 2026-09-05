# Tink Go Conformance And Reward — Research Strategy

## Status And Claim Ceiling

This is a candidate research strategy under `CA2-ROUTE-DELEGATE`. It prepares a
read-only, source-first investigation; it does not launch agents, register a
dispatch, test a live service, contact maintainers, report a vulnerability,
submit for a reward, publish a finding, approve a product, or authorize code.

The target outcome is a decision-quality package, not a promised bounty. The
terminal research classifications are:

- `GO_PATCH`: a bounded upstream hardening patch is demonstrably useful and the
  current Patch Rewards rules plausibly cover it;
- `GO_PRIVATE_VRP`: a security vulnerability with a credible impact path must
  be handled privately under the current vulnerability-reporting rules;
- `RESEARCH_ONLY`: the work is useful conformance research but reward fit or
  security impact is not established; or
- `KILL`: no non-vacuous, definitionally sound, maintainer-compatible candidate
  survives.

No reward amount, eligibility, acceptance, merge, security impact, or marketing
claim is assumed in advance.

## P1 Trigger Decision

All four Principle-1 triggers apply, so the proposed type is `research`:

1. **Synthesis:** the answer joins current Google reward rules, Tink Go and
   cross-language implementation sources, cryptographic wire/keyset semantics,
   DomainSpec v2 obligations, CyberAlchemy-v2 claim governance, and EVF evidence.
2. **Context protection:** raw repositories, histories, specifications, program
   rules, test vectors, and competing hypotheses would overwhelm one parent pass.
3. **Isolation:** security hypotheses and reward theories must remain
   independently discardable and private until their status is known.
4. **Parallelism:** program eligibility, formal/conformance semantics, and
   implementation/patch feasibility can be researched independently before join.

## Objective

Determine whether one exact, current Tink Go keyset or wire-format validation
slice can support a credible Google Patch Rewards and/or OSS VRP path. Produce a
version-bound research package containing obligation definitions, adversarial
conformance and differential-test designs, security-impact gates, upstream patch
shapes, evidence requirements, and a marketing claim ceiling without
implementing, publishing, or submitting anything.

The working hypothesis is a **Tink Go Keyset And Wire-Format Conformance
Hardening** candidate. It is an attack target, not a selected product.

## Construction And Operations Separation

### Product-construction frontier

The present CAV2-D65 frontier is research and prototype definition: freeze the
actual program and source versions, select one exact candidate boundary, define
its obligations, and design discriminating current-product tests. No product
candidate has been tested or approved.

### Construction work runnable after confirmation

1. Freeze official program rules, Tink documentation, source tags/commits,
   contribution policy, security policy, and relevant language implementations.
2. Rank exact candidates and select one or kill all.
3. Derive typed obligations and explicit trusted boundaries.
4. Design finite positive/negative fixtures plus property and differential tests.
5. Determine the minimal maintainer-compatible patch or private-report shape.
6. Produce exact-bound findings and a claim ladder.

### Operational-support residue

| task | owner | affected stage | current effect |
| --- | --- | --- | --- |
| GitHub/Google account availability | human | later contribution/submission | no construction block |
| contributor/CLA requirements | upstream + human | later patch contribution | research must verify; no acceptance inferred |
| private-report channel | Google program + human | later vulnerability reporting | causal prerequisite only for `GO_PRIVATE_VRP` |
| KYC, tax, sanctions, payment eligibility | program + human | reward payment | outside product proof |
| disclosure coordination | maintainer/program + human | publication | publication remains forbidden now |
| Inventory index repair | Inventory owner | durable indexing | unrelated dirty bytes preserved; research may continue |

Operational tasks do not hide runnable prototype research. They become blockers
only when the exact candidate reaches the stage they control.

## Research Questions

### RQ1 — Current access and reward fit

- What current official rules distinguish proactive patch rewards from private
  vulnerability rewards?
- Is the exact Tink Go repository/component/version in scope, and under which
  route? Are duplicate or overlapping rewards excluded?
- What accounts, identity, contributor agreement, merge, disclosure, impact,
  originality, and timing conditions apply?
- Which facts are program discretion rather than researcher-provable predicates?

Only official Google, Tink, and repository-owner sources may carry these claims.

### RQ2 — Exact source and semantic boundary

- Which current release tag and immutable commit define the baseline?
- Which files own keyset validity, protobuf parsing, key material/type URLs,
  key status, primary-key selection, output-prefix encoding/routing, primitive
  parameter validation, and error behavior?
- Which behavior is specified, which is implementation convention, and which is
  intentionally unspecified?
- Which Go, Java, and C++ versions are comparable without mixing release epochs?

### RQ3 — Candidate matrix

At minimum evaluate:

1. keyset validity and primary/status invariants;
2. key material/type URL agreement;
3. output-prefix encoding, parsing, and primitive routing;
4. malformed/truncated/duplicated/unknown protobuf-field handling;
5. primitive parameter domain validation;
6. cross-language acceptance/rejection parity; and
7. bounded resource behavior for untrusted serialized inputs.

Score each by exact source ownership, security relevance, reproducibility,
formalizability, negative-fixture discriminability, patch boundedness,
maintainer fit, program fit, and public/private handling risk. The synthesizer
must select one exact candidate or return a typed blocker.

### RQ4 — Proof obligations and trusted boundary

The candidate obligation set must test, where the frozen source supports it:

- total, typed rejection of malformed untrusted serialized input without panic;
- exactly one valid primary among enabled keys when the operation requires one;
- unique key IDs and valid status/material/type combinations;
- specified output-prefix construction and correct primitive routing;
- valid parameter domains before primitive construction;
- specified serialization round-trip or canonical behavior only where promised;
- version-matched cross-language equivalence for shared semantics; and
- explicit resource bounds or defended limits for parsing/validation paths.

Cryptographic primitive security, protobuf correctness, compiler correctness,
and language runtime correctness remain trusted or separately sourced. The
research must not relabel conformance proof as a proof of cryptographic security.

### RQ5 — Experimental and patch design

- Build a finite fixture taxonomy with positive controls and discriminating
  malformed, ambiguous, stale-version, and cross-language negative cases.
- Specify offline unit/property/fuzz/differential harnesses only; no live target,
  production key, user data, or third-party system is in scope.
- Define oracle rules that avoid treating one implementation as truth merely
  because it is older or more popular.
- Separate a minimal hardening patch with tests from a private vulnerability
  report. An actual vulnerability switches the work to coordinated private
  handling; it is not published as marketing material first.

### RQ6 — DomainSpec v2, CyberAlchemy-v2, and EVF use

- DomainSpec v2 supplies typed candidate, obligation, selector, fixture,
  evaluator, and claim schemas.
- CyberAlchemy-v2/CAV2-D65 keeps prototype, product test, product approval, and
  later authority/publication decisions separate.
- EVF binds immutable source identities, executions, observations, negative
  controls, and receipts. It can show what ran against which bytes; it cannot by
  itself establish semantic truth, vulnerability impact, reward eligibility, or
  upstream acceptance.

### RQ7 — Marketing claim ladder

The research must produce a claim matrix with evidence prerequisites. A safe
upper-bound candidate, only after the corresponding work exists, is:

> We derived a version-bound validation model for a security-critical
> cryptographic interface, generated adversarial conformance cases, and
> contributed an independently reproducible hardening result.

Forbidden without stronger independent evidence: “Tink is formally verified,”
“Tink is secure,” “we proved the cryptography,” “Google approved our method,”
“bounty guaranteed,” “certified,” or market-first/unique claims.

## Source Policy And Exact-Binding Contract

Every load-bearing row must contain:

- claim, rule, obligation, fixture, or candidate ID;
- immutable source identity (commit, release artifact digest, or dated official
  program page snapshot identity);
- exact file/heading/anchor/line-range or structured pointer;
- explorer-return reference;
- evidence scope;
- proof status: `observed`, `executed`, or `unverified`; and
- explicit version compatibility where two implementations are compared.

Mutable web pages require capture date and content digest or an equivalent
immutable repository revision. Search results, snippets, Inventory summaries,
and secondary articles are discovery leads only.

## Stop Conditions

Stop and classify rather than forcing a bounty narrative when any applies:

- exact Tink Go/component coverage cannot be confirmed from current official rules;
- no bounded security-relevant validation slice survives;
- the issue is known, already fixed, stale, duplicate, or based on mixed versions;
- only a theoretical difference exists with no discriminating impact witness;
- no maintainer-compatible patch or private-report shape exists;
- required source, selector, version, license, or contribution terms are ambiguous;
- meaningful validation would require live systems, real secrets, user data, or
  unauthorized access; or
- the public/private disclosure boundary is unresolved.

## Research Topology

Three explorers run in parallel:

- `Grothendieck, Alexander`: formal specification and cross-language semantic
  obligations;
- `Turing, Alan`: computational implementation, fixtures, fuzzing, differential
  tests, and patch feasibility;
- `Ashby, W. Ross`: adversarial program eligibility, impact, disclosure, and
  contribution-route analysis.

`Simon, Herbert` synthesizes and selects one candidate or a typed blocker.
`Popper, Karl`, `Taleb, Nassim Nicholas`, and `Quine, Willard Van Orman` attack
precedent, non-vacuity, and definitional soundness. `Noether, Emmy` writes only
`findings.md` after exact-binding closure. `Brandenburg, Martin` audits only the
findings. The parent remains final approver.

```text
three explorers in parallel
  -> synthesizer
  <-> three skeptics in parallel (maximum two exchanges)
  -> exact-binding evidence closure
  -> writer
  -> auditor
  -> parent decision
```

One synthesis-to-explorer repair and one auditor-to-writer revision are
declared. Missing exact evidence may not be repaired by prose at the writer stage.

## Required Outputs

- `research.md`: verbatim explorer returns, mechanically assembled by the parent;
- `findings.md`: evidence-closed synthesis with candidate verdict matrix;
- exact source/version denominator and program-rules matrix;
- candidate scorecard and one selected candidate or typed blocker;
- obligation and trusted-boundary model;
- fixture/differential/fuzz plan and reproducibility protocol;
- minimal patch/private-report decision tree;
- reward-fit and operational-readiness matrix;
- marketing claim ladder and explicit non-claims;
- dependency-ordered, non-executed next Work Pack.

## Inventory Preflight

The root `index.json` parses and passes identity, existence, derived-map,
human-view, and freshness checks, but lookup readiness is `blocked`: source
coverage reports six errors and uncontrolled tags report 182 warnings. The
Inventory is therefore a flagged discovery view, not ready evidence.

Selected seeds cover proof-obligation substrate design, EVF exact evidence and
claim boundaries, three-layer conformance, validation-moat positioning, and AI
assurance vocabulary. No Tink or Google reward corpus was found. That no-match
does not establish novelty; it requires a real current external precedent sweep.

The Inventory files already contain unrelated modifications. This setup does
not edit them; durable Inventory result registration remains operational residue
for the Inventory owner or a later exact-scope pass.

## Gate And Ledger State

- Candidate sheet schema: `0.10.0`
- Evidence contract: `exact-binding`
- Deterministic confirmation readiness: `PASS`
- Candidate sheet SHA-256: `4b2952edcd642ad98f0c5c06a0501110b6550583e3f24873bff3ed9fa5239fa8`
- Material projection schema: `domainspec.material-strategy.v3`
- Material strategy SHA-256: `6e1e62c14496b2e20038946eb72252c95b44c4347ce7dcf1b9d2221d039449ee`
- Material projection file SHA-256: `b9bc55e2fd4735048c8d9f00041264cf30567a98e4841921182bb965c606b745`
- Check-tension: not run; subject groups require two independent digest-bound verdicts
- Preconfirmation closure: not evaluable until tension evidence exists
- Human confirmation: not requested
- Dispatch registration: none
- Agents spawned: zero
- Ledger mutation: none
- Research execution: not started
- Product approval, authority, publication, release, deployment: none

## Next Human Gate

After deterministic readiness passes, the next permissible action is approval
to run only the two read-only tension-gate helpers against the exact sheet
digest. That is not confirmation of the research dispatch. Human `confirmed`
becomes meaningful only after both tension verdicts and preconfirmation closure
pass on unchanged bytes.
