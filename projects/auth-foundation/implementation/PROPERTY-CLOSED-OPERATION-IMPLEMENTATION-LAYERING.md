---
title: Property-Closed Auth Operation Implementation Layering
status: planning-candidate
updatedAt: 2026-08-31
owner: Auth Foundation and DomainSpec v2 CLI
scope: capability
authority_effect: none
route: CA2-ROUTE-PLAN
---

# Property-Closed Auth Operation Implementation Layering

## Start here

The next implementation target is one standard DomainSpec v2 CLI command that
selects the Auth `authorize` Operation and produces a complete, compilable Rust
realization from ontology-bound DomainSpec source. Every relevant property and
rule must remain traceable through this chain:

```text
capability-local business ontology
  -> authored DomainSpec nodes and relationships
  -> deterministic property-and-rule closure IR
  -> Rust symbols and behavior
  -> structural, compilation, behavioral, and equivalence evidence
```

The smallest coherent unit is the **Ontology-bound Operation Closure**: the
selected Operation, all transitive property/type/rule dependencies needed to
execute it, one Rust realization, and an exact coverage receipt. A property
schema alone is too small because it does not prove executable translation. A
universal ontology compiler or complete Auth service is too large because it
adds unrelated meta-types, languages, integrations, and effects.

This is a planning candidate. It does not admit ontology bytes, authorize
implementation, establish conformance, or retire the existing Auth generator.

## Design review verdict

**FLAG — the outer design boundary is sound, but the current implementation
path is not property-closed.** The following gaps belong in L0 rather than in
later hardening:

| Closure break | Current evidence | Required repair |
| --- | --- | --- |
| Business-property identity | `business-ontology.json` gives nodes meanings but no structured property records. | Give each input, output, enum variant, and rule operand a stable ontology selector and language-neutral type. |
| Auth source versus standard CLI contract | Auth nodes use object-valued fields and Rule-specific members; the standard CLI expects string-array fields and a textual predicate. | Introduce a capability-neutral typed source contract while preserving existing untyped source compatibility. |
| Selected Operation | The Auth source has five Entities and one Rule, but no `authorize` Operation. | Author the Operation, its input and output contract, and legal `Rule --enforces--> Operation` and `Operation --reads--> Entity` relationships. |
| Dependency closure | Standard instantiation selects one node and its incident relationships, not recursive type/rule dependencies. | Calculate a deterministic, cycle-checked transitive closure rooted at the selected Operation. |
| Rust type fidelity | Entity output is `{ id: String, state: String }`; Operation state is `BTreeMap<String,String>`. | Lower ontology-bound property types into typed Rust records, enums, sets, optionals, references, and sums. |
| Rule execution | Rust Rule returns a caller-supplied Boolean and Operation accepts `guard: bool`. | Compile the bounded rule expression and call it inside the generated Operation. |
| Recomposition | Independently rendered files do not define module order, imports, collision handling, or a crate root. | Emit one deterministically ordered, compilable Rust unit or crate with no handwritten assembly. |
| Evidence meaning | Legal relationships or property-name coverage do not prove behavior or equivalence. | Keep structural coverage, compilation, behavioral conformance, and Lean/Rust equivalence as separate evidence classes. |

## L0 property denominator

“All properties” means the complete executable Auth contract, not only the
fields already present in the six minted nodes. Before implementation, create
an immutable denominator manifest covering:

- record fields for `Permission`, `Session`, `Role`, `AuthorizationRequest`,
  and `EvaluationContext`;
- variants and payloads for `SessionStatus`, `DenyReason`, and
  `AuthorizationDecision`;
- the `authorize` input and result types;
- the eight business rules and every property selector referenced by their
  expressions;
- collection element types, uniqueness/cardinality, optionality, identity,
  and named-type references;
- the distinction between normative decision data and non-normative
  diagnostics.

The current Rust comparison oracle contains at least 22 record fields and 15
enum/sum variants. Those counts are discovery evidence, not the final
denominator: the denominator is complete only when every executable input,
output, and rule operand is either mapped to a stable business-ontology
property selector or explicitly classified as implementation-only with a
reason.

### Minimum language-neutral type algebra

L0 supports only the variety exercised by Auth:

- scalars: `String`, `Bool`, and `UInt64`;
- named references to ontology-bound records and enums;
- `Set<T>` with explicit uniqueness semantics;
- `List<T>` where resolver-row multiplicity must remain observable;
- `Optional<T>`;
- discriminated sums with optional variant payloads;
- record properties with stable property ID, name, type, cardinality,
  identity role, meaning, and source selector.

Anything outside this algebra is rejected as unsupported. L0 does not add a
universal type system.

### Minimum rule-expression algebra

Use a structured, capability-neutral Rule expression rather than executable
Rust or free text. L0 admits only operators required by the Auth rules:

- literals and property paths;
- `all`, `any`, and `not`;
- equality and strict less-than;
- exact cardinality and uniqueness;
- set equality and membership;
- existential match over a collection;
- enum/sum variant checks.

Unsupported operators, unresolved paths, type mismatches, and cycles fail
closed before generation.

## Layer boundary

Each layer ends when it changes what can responsibly be decided next.

| Layer | Decision question | Minimum working unit | Operator outcome | Primary risk reduced | Promotion |
| --- | --- | --- | --- | --- | --- |
| L0 — Auth vertical | After this layer, we know whether the standard CLI can translate one complete ontology-bound Auth Operation into tested Rust without handwritten semantic glue. | One `instantiate --node auth-exact-permission:authorize --language rust` clean-target run plus exact closure and coverage receipts. | A generated Rust Auth kernel that compiles and matches the current behavioral oracle. | Meaning and type loss across ontology, DomainSpec, IR, and Rust. | Continue only if every denominator row is covered and all four evidence classes are reported separately. |
| L1 — capability neutrality | After this layer, we know whether the mechanism is a reusable DomainSpec capability rather than Auth logic hidden in the CLI. | A second small non-Auth fixture using the same property, closure, Rule, and Rust paths. | The same command shape generates two independent Operations. | Auth overfitting and fixed-name generation. | Harden only when no compiler or renderer branch refers to Auth identifiers. |
| L2 — fail-closed hardening | After this layer, we know whether malformed, incomplete, cyclic, or semantically unsupported source is rejected deterministically and equivalence evidence is credible. | Mutation suite, two-run determinism, negative closure tests, and Lean/Rust characterization checks. | Predictable diagnostics and bounded trust in the generated kernel. | Silent omission, accidental defaults, semantic drift, and false evidence inflation. | Package only after negative cases and equivalence obligations have terminal results. |
| L3 — migration and packaging | After this layer, we know whether the standard path can replace the specialized Auth generator without losing a guarantee. | Clean migration, comparison report, documentation, and removal of the specialized generator in a separate reviewed change. | One supported standard instantiation path. | Dual-path drift and maintenance burden. | Retire the old path only after parity and non-regression evidence are bound to unchanged bytes. |

## Capability progression

| Area | L0 | L1 | L2 | L3 |
| --- | --- | --- | --- | --- |
| Ontology | Full Auth denominator and stable selectors | Reused by a second capability | Mutation and unsupported-form rejection | Versioned package contract |
| DomainSpec | Typed Auth nodes, Rule, Operation, and relationships | Capability-neutral fixture | Graph/closure failure coverage | Migration documentation |
| Compiler | Selected-Operation transitive closure and typed IR | No Auth-specific branches | Cycle, ambiguity, collision, and determinism checks | Stable CLI surface |
| Rust | Typed Auth crate and internal Rule evaluation | Second generated crate | Behavior and equivalence hardening | Specialized generator removed |
| Evidence | Exact coverage plus compile and behavior results | Cross-capability reuse evidence | Negative and formal evidence | Final comparison and migration receipt |

## L0 — minimum working unit

### Goal

Prove one useful end-to-end claim: the standard CLI can derive a property-
complete, typed, pure Rust `authorize` Operation from the selected ontology-
bound DomainSpec closure, with no caller-supplied guard and no handwritten
post-generation edits.

### Included

- A versioned property denominator manifest and stable ontology property IDs.
- Structured business-ontology property and Rule records for the Auth kernel.
- Typed DomainSpec source for the required records, enums/sums, Rule, and
  `authorize` Operation.
- Explicit legal relationships from the Rule and read Entities to the
  Operation, plus named type references used by properties.
- A deterministic closure algorithm rooted at the selected Operation.
- A typed intermediate representation retaining property identity, type,
  cardinality, input/output role, Rule use, and source selector.
- Rust crate composition, typed lowering, internal Rule evaluation, and
  deterministic naming/import ordering.
- One coverage row for every denominator property, variant, and Rule:

```text
business ontology selector
  -> DomainSpec selector
  -> compiled IR selector
  -> Rust symbol and type
  -> conformance check
```

### Explicitly deferred

- Type and Rule operators not required by Auth.
- Languages other than Rust and unrelated DomainSpec meta-types.
- HTTP, persistence, session/role resolution, tokens, audit transport,
  deployment, performance optimization, and service orchestration.
- General-purpose expression evaluation at runtime.
- Acceptance, publication, release, or external-effect authority.
- Removal of the existing specialized Auth generator.

### Exit evidence

L0 exits only when all of these results exist for one immutable source digest:

1. **Structural coverage:** zero missing, duplicate, incompatible, or
   implementation-only-unexplained denominator rows.
2. **Compilation:** a clean target generated by the standard CLI passes
   `cargo check` and `cargo test` without manual edits.
3. **Behavioral conformance:** permitted, no-grant, invalid session, expiry,
   stale revision, untrusted scope, incomplete/duplicate/mismatched roles, and
   resource/action/scope mismatch cases agree with the current Rust oracle.
4. **Equivalence state:** Lean/Rust characterization is reported independently
   as pass, fail, or not-evaluable with causal blockers; structural or test
   success cannot substitute for it.
5. **Determinism:** two clean-target runs produce identical source and receipt
   digests.

### Promotion decision

- Continue to L1 when all L0 structural, compilation, behavior, and
  determinism checks pass and formal status is explicitly bounded.
- Pivot when a required Auth form cannot be represented without adding a
  capability-neutral extension to the denominator, source contract, or IR.
- Stop when any semantic behavior still depends on a handwritten template,
  caller-supplied Boolean, or untracked property mapping.

## Implementation wave backbone

The first five waves together form L0; none alone proves the L0 claim.

| Wave | Layer | Work | Primary artifacts | Verification |
| --- | --- | --- | --- | --- |
| W0.1 — denominator | L0 | Freeze the complete Auth property/variant/Rule denominator and define the minimal type and Rule-expression algebra. | Versioned ontology schema changes, denominator manifest, property records, schema fixtures. | Collect-all validator reports every current runtime symbol as mapped or explicitly classified; malformed types and expressions fail. |
| W0.2 — authored closure | L0 | Remint property-complete Auth source, add `authorize`, and add legal dependency relationships. | Typed nodes for records/enums/sums/Rule/Operation; rebuilt graph and system ontology candidates. | Source validator and relationship validation pass; selected Operation closure is non-empty and contains every required selector. |
| W0.3 — closure compiler | L0 | Extend standard CLI selection to compute dependency closure and compile it to typed IR. | Closure resolver, typed IR, deterministic ordering, precise diagnostics, unit/fixture tests. | Missing refs, ambiguous refs, cycles, type mismatch, unsupported forms, and naming collisions fail closed; two IR runs are byte-identical. |
| W0.4 — Rust realization | L0 | Lower the IR to one typed Rust crate and evaluate the compiled Rule inside `authorize`. | Rust renderer/profile changes, crate assembler, generated Auth candidate. | Clean `cargo check`; generated API contains every required symbol/type; no Auth identifiers occur in generic compiler branches. |
| W0.5 — conformance | L0 | Bind source-to-symbol coverage and compare behavior with the current specialized kernel. | Coverage receipt, compile receipt, behavioral comparison, determinism receipt, equivalence status. | Exact-row closure, Auth case suite, mutation tests, and two-run digest comparison. |
| W1 — second vertical | L1 | Run the same pipeline on one small non-Auth Operation. | Capability-neutral fixture and generated crate. | Same CLI path succeeds with no Auth-specific conditionals or templates. |
| W2 — hardening | L2 | Expand negative, degraded, and formal checks without widening the feature surface. | Mutation matrix, diagnostics contract, Lean/Rust bridge evidence. | Collect-all results distinguish pass, fail, and not-evaluable. |
| W3 — migration | L3 | Compare and retire the specialized Auth generator. | Migration report, docs, deletion candidate. | All prior guarantees remain green against immutable bytes before removal. |

## Required file-impact discipline for implementation

Before each wave mutates files, name an exact allowlist. The expected ownership
zones are:

- Auth meaning/source: `projects/auth-foundation/implementation/`;
- generic CLI contracts, closure compiler, Rust renderer, and tests:
  `projects/domainspec-v2/impl/cli/`;
- generated Auth output: a clean target under the Auth implementation package.

Do not edit the current generated Rust comparison oracle by hand. Do not delete
the specialized generator in L0. Preserve unrelated dirty bytes and treat each
wave as a separately reviewable semantic change.

## Non-regression guardrails

- The command remains the standard `instantiate` command; Auth does not gain a
  hidden alternate product command.
- Existing untyped node fixtures remain compatible or receive an explicit,
  tested version migration.
- Every supported property type is capability-neutral and used through the
  typed IR; generic compiler code contains no Auth field names or Rule IDs.
- The generated Operation evaluates its Rule; callers cannot inject the
  authorization result as a Boolean.
- Unsupported or missing ontology dependencies fail closed and identify the
  exact selector.
- Generated output is clean-target reproducible and requires no manual edits.
- Structural, compilation, behavioral, and formal evidence remain separate.
- A candidate receipt grants no admission, conformance, publication, release,
  deployment, or external-effect authority.

## Distill review trace

### Run frame

- Mode: Standard, assumed because no budget was selected.
- Proposal tracks: one.
- Recursive rounds: two, followed by one reconciliation.
- Optimization goal: the smallest layer that proves full property translation
  for a real Operation while preserving a reusable DomainSpec boundary.

### Role conversation

| Round | Proposer claim | Balancer objection category | Reconciliation |
| --- | --- | --- | --- |
| 1 | Select an Operation and generate its Rust implementation plus a property receipt. | Hidden glue; brittle minimalism; recomposition failure. | Expand the unit to include a typed denominator, transitive closure IR, internal Rule evaluation, and deterministic crate composition. |
| 2 | Build the generic closure path for Auth, then remove the specialized generator. | Overbuilding/overfit; unsupported knowledge; migration risk. | Bound the algebra to Auth-required capability-neutral forms, prove a second vertical in L1, separate evidence classes, and defer generator retirement to L3. |

Balancer closure verdict: **FLAG for planning closure**. The candidate becomes
navigable and implementable as a plan only with the mandatory L0 contracts
named above. This verdict is not implementation readiness or authority.

### Technique trace

| Technique | Result | Outcome |
| --- | --- | --- |
| Abstraction-Level Guard | The outer unit is a capability; its child responsibilities are ontology artifact, authored source, compiler operation, Rust artifact, and evidence artifact. | pass |
| Recomposition Proof | Property IDs and selectors flow through one typed closure IR into deterministic Rust symbols and receipt rows; no unnamed adapter is allowed. | pass with the IR boundary made mandatory |
| Evolution Profile | Concrete pressure is new capabilities and Rule growth; the smallest extension boundary is a capability-neutral type/Rule algebra, while other languages and universal semantics remain deferred. | pass |
| Cognitive Load Check | Five L0 waves are retained because each names a distinct evidence-bearing responsibility; the four decision layers prevent those waves from becoming separate product abstractions. | pass |
| Requisite Variety Check | The algebra matches known Auth scalars, collections, optionals, references, sums, and Rule forms; everything else fails closed. | pass |
| Boundary-Object Check | Stable shared meaning is the property selector plus typed IR row; ontology authors, DomainSpec compiler owners, Rust profile owners, and evidence reviewers may use local representations behind that boundary. | pass |
| Concept-vs-Knowledge Status | Current renderer limitations and missing source are code-backed; the final denominator count and formal equivalence remain unresolved evidence, not assumed facts. | pass |
| Premortem | Most likely failure: a coverage receipt proves names while behavior remains in handwritten glue. Guardrail: generated Rule evaluation, clean-target crate assembly, mutation tests, and separate behavioral/equivalence results. | pass with guardrail |
| Frame-Expiry Note | Re-run this layering if Auth requires a new type/operator, a second language becomes current scope, or the standard CLI source/relationship contract changes. The first deferred complexity to revisit is the type/Rule algebra. | pass |
| Navigable Result Check | Start at W0.1, promote only on layer exit evidence, and keep unresolved formal status visible. | pass |

## Open decisions at implementation entry

These are local design choices for W0.1, not reasons to broaden L0:

1. Version the typed node body alongside the current body contract or migrate
   the current contract in place. Compatibility evidence is mandatory either
   way.
2. Represent `AuthorizationDecision` as a discriminated sum directly or as a
   record constrained by a Rule. Choose the smaller representation that
   preserves the current Rust behavior and exact diagnostic optionality.
3. Choose one stable selector syntax for ontology properties and Rule property
   paths. It must survive reminting and appear unchanged in the coverage row.

## Next action

Execute **W0.1 only**: produce the denominator and the minimal typed
property/Rule contracts with positive and negative schema fixtures. Review its
exact property list and source compatibility before authoring the Operation or
changing Rust generation.
