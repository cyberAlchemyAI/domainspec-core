# SFOL Test Closure Capability

Status: implementation-directed candidate
Owner: DomainSpec v2 owner
Visibility: private
Authority effect: none

This package carries the capability-local D65 construction chain for bounded
SFOL test closure. It keeps product meaning, business semantics, authored
DomainSpec source, generated graph/system projections, implementation binding,
and conformance evidence distinct.

The package does not change the existing Lean claim, rewrite historical Auth
v1 evidence, admit its own definitions or ontology, or grant publication,
release, deployment, or production authority.

Run the deterministic compiler from the repository root with the TDE package's
installed `tsx` runtime:

```text
tsx projects/domainspec-v2/capabilities/sfol-test-closure/scripts/build.ts
```

Run the bounded conformance gate, including two complete SFOL test runs, two
compiles, CLI smoke validation, the 21-property denominator, and immutable
Lean/Auth-v1 digest checks:

```text
tsx projects/domainspec-v2/capabilities/sfol-test-closure/scripts/validate.ts
```

The capability-local development profile is necessary because the canonical
minted-profile registry currently binds an older meta-type digest. It grants
no release admission; the generated graph and system ontology remain
candidates.
