# Dependency and Interface Map

## Ownership

| Boundary | Producer owner | Consumer owner | Contract owner | Validation owner |
| --- | --- | --- | --- | --- |
| project source → admitted record | individual project owner | portfolio owner | `vrondelli` | record validator |
| admitted record → projection | record compiler | browser UI | `vrondelli` | projection validator |
| visibility policy → view model | privacy owner (`vrondelli`) | every rendered surface | privacy owner | independent privacy auditor |
| route/history → projection state | browser user | projection router | application owner | black-box UI owner |
| offer draft → transition command | participant | state machine | workflow owner | state validator |
| transition command → gateway | state machine | collaboration gateway | interface owner | integration validator |
| gateway → receipt ledger | gateway | project owner and participant | persistence owner | receipt validator |
| saved version → Sites deployment | application owner | restricted audience | release owner | deployment validator |
| public-release request → access change | publication owner | public audience | publication owner | privacy and naming reviewers |

## Field Projection Matrix

| Field family | Public | Meeting | Assigned collaborator | Participant private | Owner private |
| --- | --- | --- | --- | --- | --- |
| display name, domain, problem, bounded witness | yes | yes | yes | yes | yes |
| limitation, claim ceiling, public source label | yes | yes | yes | yes | yes |
| contribution options, effort ceiling, stop rule | yes | yes | yes | yes | yes |
| facilitator timing and clinic cue | no | no | no | no | yes |
| participant identity and availability | no | no | yes | yes | yes |
| unsubmitted offer draft | no | no | no | yes | no |
| candidate-pair negotiation | no | no | yes | yes | yes |
| permitted terminal receipt summary | no by default | no by default | yes | yes | yes |
| source-local forbidden wording and private notes | no | no | no | no | yes |
| unclassified field | block | block | block | block | block |

“No” means absent before serialization and rendering, not present with CSS,
ARIA, clipping, collapsed controls, source maps, logs, or hidden attributes.

## Adapter Contracts

### Project source adapter

Input:

- owner identity and verification date;
- exact source selector and digest;
- project display name and domain;
- problem, witness, limitation, and claim ceiling;
- forbidden claims;
- experiment ask, effort, stop rule, expected witness;
- field visibility and policy version.

Output: candidate `ProjectRecord`. Admission is a separate decision.

### Projection adapter

Input: admitted record, actor visibility, mode, and current date.

Output: immutable mode-specific view model with:

- `truth_digest`;
- exact eligibility and freshness label;
- permitted content fields;
- semantic actions;
- no raw-record escape hatch.

### Collaboration gateway

Input: command ID, expected revision, permitted participant payload, transition
event, appointment/receipt terms, and policy version.

Output:

- accepted acknowledgement with revision;
- typed validation refusal;
- typed conflict;
- timeout/unknown outcome with safe retry instructions.

No response may be interpreted as success without an acknowledgement.

### Sites boundary

Input: opaque Sites project identity from checked-in
`projects/co-op-engine/.openai/hosting.json`, exact pushed source state, saved
version, and access policy.

Output: production deployment identity and access state.

Rules:

- never invent or derive opaque Sites IDs;
- create a site no more than once;
- push the exact source state before saving a version;
- deploy only a saved version;
- all first-proof deployments remain access-restricted;
- public access requires separate D-005 and audit evidence.

## Version Compatibility

| Contract | Incompatible change | Response |
| --- | --- | --- |
| project record | required field removal, state/visibility meaning change | new major version and migration/adapter decision |
| view model | disclosure broadening or semantic action change | new major version and black-box/privacy revalidation |
| transition event | precondition, terminality, or reciprocity change | new major version and state-fixture replay |
| receipt | outcome meaning or policy binding change | new major version; preserve old receipt interpretation |
| gateway | acknowledgement/idempotency/revision behavior change | explicit protocol negotiation or block |
| route | existing direct-link meaning changes | redirect or compatibility parser with regression fixture |

## Dependency Policy

- Runtime dependencies must not be used to smuggle record truth or visibility
  policy into components.
- The browser bundle contains no secret or private raw source corpus.
- Build and test tooling may consume synthetic sentinel fixtures.
- A dependency that observes DOM, network, storage, screenshot, or traces is
  inside the privacy audit denominator.
- Version selection and supply-chain checks belong to Plan.
