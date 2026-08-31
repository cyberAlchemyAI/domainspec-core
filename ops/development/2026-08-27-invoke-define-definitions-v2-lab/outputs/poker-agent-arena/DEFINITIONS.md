# Poker Agent Arena Local CLI V0 Candidate Definitions

- Registry: `poker-agent-arena.definitions.v2`
- Status: `candidate`
- Owner route: `definitions-governance`
- Authority scope: `project:poker-agent-arena`
- Visibility: `private`
- Authority effect: `none`

## DEF-POKER-AGENT-ARENA-001: Legal action

- Status: `candidate`
- Version: `1`
- Aliases: none
- Source kinds: `local-inference`

### Normative Voice

An action explicitly admitted by the current game-state protocol.
### Formal Voice

Agents may choose only from legal actions supplied by the current protocol.
### Operational Voice

An action explicitly admitted by the current game-state protocol.
### Plain-Language Voice

An action explicitly admitted by the current game-state protocol.
### Domain-Context Voice

Define a bounded local poker-agent arena with constrained actions, hidden-information protection, deterministic fallback, replay, and diagnostics. Boundary: Local CLI V0 proof passed; no real-money, hosted, or calibrated-ranking claim.
### Boundary

#### Includes

- Define a bounded local poker-agent arena with constrained actions, hidden-information protection, deterministic fallback, replay, and diagnostics.

#### Excludes

- Local CLI V0 proof passed; no real-money, hosted, or calibrated-ranking claim.

#### Conditions

- Agents may choose only from legal actions supplied by the current protocol.
- Private transcripts support deterministic replay while public replay redacts hidden state.
- Ranking remains diagnostic and fixture-bounded.

### Sources

| Role | Path | Selector | SHA-256 | Size |
| --- | --- | --- | --- | ---: |
| evidence | `projects/poker-agent-arena/README.md` | line-span: `lines 1-63` | `b4d94391aed10270f884ac4673e53d6875fd0bf3782ba51e4e440b4c83c464a7` | 3477 |

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

## DEF-POKER-AGENT-ARENA-002: Public replay

- Status: `candidate`
- Version: `1`
- Aliases: none
- Source kinds: `local-inference`

### Normative Voice

A redacted replay projection that excludes hidden information.
### Formal Voice

Private transcripts support deterministic replay while public replay redacts hidden state.
### Operational Voice

A redacted replay projection that excludes hidden information.
### Plain-Language Voice

A redacted replay projection that excludes hidden information.
### Domain-Context Voice

Define a bounded local poker-agent arena with constrained actions, hidden-information protection, deterministic fallback, replay, and diagnostics. Boundary: Local CLI V0 proof passed; no real-money, hosted, or calibrated-ranking claim.
### Boundary

#### Includes

- Define a bounded local poker-agent arena with constrained actions, hidden-information protection, deterministic fallback, replay, and diagnostics.

#### Excludes

- Local CLI V0 proof passed; no real-money, hosted, or calibrated-ranking claim.

#### Conditions

- Agents may choose only from legal actions supplied by the current protocol.
- Private transcripts support deterministic replay while public replay redacts hidden state.
- Ranking remains diagnostic and fixture-bounded.

### Sources

| Role | Path | Selector | SHA-256 | Size |
| --- | --- | --- | --- | ---: |
| evidence | `projects/poker-agent-arena/README.md` | line-span: `lines 1-63` | `b4d94391aed10270f884ac4673e53d6875fd0bf3782ba51e4e440b4c83c464a7` | 3477 |

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
