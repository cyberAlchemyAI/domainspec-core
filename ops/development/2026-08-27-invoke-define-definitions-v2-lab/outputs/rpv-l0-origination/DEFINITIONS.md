# RPV L0 Source-Neutral Origination Prototype Candidate Definitions

- Registry: `rpv-l0-origination.definitions.v2`
- Status: `candidate`
- Owner route: `definitions-governance`
- Authority scope: `project:rpv-l0-origination`
- Visibility: `private`
- Authority effect: `none`

## DEF-RPV-L0-ORIGINATION-001: Secret gate

- Status: `candidate`
- Version: `1`
- Aliases: none
- Source kinds: `local-inference`

### Normative Voice

A pre-persistence check that rejects prohibited secret-bearing input.
### Formal Voice

Secret detection precedes parsing and persistence.
### Operational Voice

A pre-persistence check that rejects prohibited secret-bearing input.
### Plain-Language Voice

A pre-persistence check that rejects prohibited secret-bearing input.
### Domain-Context Voice

Define the proven synthetic mechanics of a secret-gated, transactional, replay-safe origination pipeline. Boundary: Synthetic candidate-local verification passed; no real-source, legal, or production claim.
### Boundary

#### Includes

- Define the proven synthetic mechanics of a secret-gated, transactional, replay-safe origination pipeline.

#### Excludes

- Synthetic candidate-local verification passed; no real-source, legal, or production claim.

#### Conditions

- Secret detection precedes parsing and persistence.
- Accepted synthetic fixtures reconcile to terminal outcomes and replay without database growth.
- The aggregate result is redacted and semantically validated before it is reported.

### Sources

| Role | Path | Selector | SHA-256 | Size |
| --- | --- | --- | --- | ---: |
| evidence | `projects/rpv-origination/phase-0/prototype/README.md` | line-span: `lines 1-109` | `750e2230378e169095cdb225447b0f363189a03490c75dfa931bccf00d0aad16` | 4406 |

### Primary Consumers

- `DEFINITIONS.md`
- `GLOSSARY.md`
- `SPEC.md`

### Use Carefully

Treat this as a human-curated project projection, not extraction proof.

### Misuse Warning

Candidate packaging grants no semantic or operational authority.

### Promotion Boundary

Candidate only; definitions-governance owns any later review and promotion.

### Drift Route

`definitions-governance`

## DEF-RPV-L0-ORIGINATION-002: Idempotent replay

- Status: `candidate`
- Version: `1`
- Aliases: none
- Source kinds: `local-inference`

### Normative Voice

Repeated execution that preserves the accepted result without record growth.
### Formal Voice

Accepted synthetic fixtures reconcile to terminal outcomes and replay without database growth.
### Operational Voice

Repeated execution that preserves the accepted result without record growth.
### Plain-Language Voice

Repeated execution that preserves the accepted result without record growth.
### Domain-Context Voice

Define the proven synthetic mechanics of a secret-gated, transactional, replay-safe origination pipeline. Boundary: Synthetic candidate-local verification passed; no real-source, legal, or production claim.
### Boundary

#### Includes

- Define the proven synthetic mechanics of a secret-gated, transactional, replay-safe origination pipeline.

#### Excludes

- Synthetic candidate-local verification passed; no real-source, legal, or production claim.

#### Conditions

- Secret detection precedes parsing and persistence.
- Accepted synthetic fixtures reconcile to terminal outcomes and replay without database growth.
- The aggregate result is redacted and semantically validated before it is reported.

### Sources

| Role | Path | Selector | SHA-256 | Size |
| --- | --- | --- | --- | ---: |
| evidence | `projects/rpv-origination/phase-0/prototype/README.md` | line-span: `lines 1-109` | `750e2230378e169095cdb225447b0f363189a03490c75dfa931bccf00d0aad16` | 4406 |

### Primary Consumers

- `DEFINITIONS.md`
- `GLOSSARY.md`
- `SPEC.md`

### Use Carefully

Treat this as a human-curated project projection, not extraction proof.

### Misuse Warning

Candidate packaging grants no semantic or operational authority.

### Promotion Boundary

Candidate only; definitions-governance owns any later review and promotion.

### Drift Route

`definitions-governance`
