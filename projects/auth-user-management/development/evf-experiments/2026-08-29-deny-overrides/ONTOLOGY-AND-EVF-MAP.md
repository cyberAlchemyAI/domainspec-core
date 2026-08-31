# Current Ontology And EVF Map

## Three Connected Views

The case crosses three views. They should connect, but they do not own the same
meaning.

### 1. Auth business ontology — what the product means

Already observed:

```text
AuthorizeRequest --has_rule--> AuthorizeRequest.R3
PermissionResolutionPolicy --governs--> AuthorizeRequest
AuthorizeRequest --produces--> AccessDenied
AuthorizeRequest.R3 --decided_by--> DEC-003
```

The same ontology records blocker `CON-04`: the declared authorization input is
a string list and cannot represent a DENY effect.

### 2. DomainSpec relationship projection — how the rule composes

Candidate normalization for the EVF vertical:

```text
AuthorizeRequest.R3 --enforces--> AuthorizeRequest
PermissionResolutionPolicy --applies--> AuthorizeRequest
AuthorizeRequest --reads--> PermissionGrant       # only if Path A is accepted
AuthorizeRequest --produces--> AccessDenied
```

`enforces` is the active DomainSpec Rule-to-Operation verb. `applies` is the
active Policy-to-Operation verb. The auth ontology currently uses `has_rule` and
`governs`, so this is a proposed bridge mapping, not a silent rewrite of its
canonical bytes.

### 3. Formal-claim/proof ontology — what is stated and what must be shown

The selected DomainSpec-v2 ontology candidate direction is:

```text
ProofObligation --derived_from--> FormalClaim --formalizes--> BusinessMeaning
```

For this case:

```text
PO-AUTH-R3-CARRIER-001 -----------+
                                   +--derived_from--> FormalClaim:principal-exact-deny-wins/v1
PO-AUTH-R3-PRECEDENCE-001 --------+

FormalClaim:principal-exact-deny-wins/v1
  --formalizes (bounded slice, declared loss)-->
BusinessMeaning:deny-overrides/v1
```

Current status:

- `BusinessMeaning` source: observed;
- `FormalClaim`: candidate, not admitted;
- `formalizes`: proposed, owner acceptances absent;
- `ProofObligation` records: planned, not derived;
- `derived_from`: not authored;
- implementation bindings: observed candidates, not admitted EVF bindings; and
- evidence/discharge: absent.

The direction has been selected in the DomainSpec-v2 architecture decision, but
its exact protected candidate contracts still await named owner admission. This
experiment reuses the direction as a candidate map; it does not promote it.

## EVF Architecture Walk

| EVF stage | This case now | What is needed next |
| --- | --- | --- |
| Source claim | R3, policy table, DEC-003 | settle the DENY carrier and first-slice fidelity |
| Normalized representation | candidate proposition in this package | owner review and exact semantic identity |
| FormalClaim | candidate only | formal-owner assertion plus business-owner fidelity acceptance |
| Executable projection | absent | one digest-bound DS-SFOL projection |
| Formal obligations | two planned R3 obligations | deterministic derivation from admitted claim/context |
| Implementation binding | code symbols identified | exact binding contract and executable identity |
| Positive checks | existing unit/E2E tests | generated or selected EVF checks with independent expected values |
| Negative checks | mutation ideas listed | isolated mutants and exact kill/survival results |
| Evaluator verdict | absent | selected runtime/provider execution |
| EVF evidence handle | absent | normalized/joined evidence with currentness |
| Independent consumer receipt | absent | separately authored consumer assessment |
| Obligation discharge | absent | separate owner decision; never inferred from PASS |

## Why This Decomposition Matters

There are two different questions:

1. **Precedence:** if a DENY is visible, does it beat ALLOW?
2. **Carrier:** does the operation see the DENY that the business says applies?

The current pure function and tests give strong starting evidence for precedence.
The ontology finding shows that the documented carrier remains unresolved. EVF
should preserve both facts. It should not let a green precedence test hide the
missing domain decision.

## Possible Paths

### Path A — meaning-first, operation reads grants (recommended experiment path)

Accept the current implementation responsibility as intended business meaning,
define the grant snapshot, then admit the operation-level claim and derive both
obligations. This gives the strongest trace from rule to operation with the
smallest code change.

### Path B — pure function first

Create a smaller claim only about `resolvePermissionDecision` and derive only
the precedence obligation. This can reach executable evidence sooner, but it
must be presented as an algorithm claim. It does not establish R3 at the
`AuthorizeRequest` boundary.

### Path C — redesign the carrier

Put typed grants in `AuthContext`, or resolve DENY before authorization. This may
produce a cleaner domain model, but it changes responsibilities, input types,
staleness rules, and implementation. It should be a later design decision, not
an invisible experiment assumption.

## Recommended Order

1. Decide Path A, B, or C.
2. Accept the bounded business meaning and declared loss.
3. Create the exact `FormalClaimSourcePayload/v2` and owner acceptance records.
4. Create one digest-bound DS-SFOL projection.
5. Derive the obligations.
6. Bind and run the EVF experiment.
7. Review the evidence and remaining domain questions.

This order protects the central DDD lesson: formal evidence is useful only when
the business meaning and its losses stay visible.
