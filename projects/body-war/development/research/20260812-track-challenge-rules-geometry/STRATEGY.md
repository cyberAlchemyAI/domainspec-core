# Body War Track Challenge Rules And Geometry Research Strategy

## Status

- Dispatch type: `research`
- Target schema: `0.8.0`
- State: confirmation-ready; not registered; not executed
- Evidence contract: `exact-binding`
- Final approver: `parent`
- Canonical product bytes changed: none
- Authority effect: none

## Design Hypothesis Under Test

The smallest coherent candidate is a `Track Challenge` over one versioned
`TrackGeometry` and one bounded `EventWindow`.

- Performance modes:
  - `Speed`: fixed route or lap count; lowest verified elapsed time wins.
  - `Distance`: fixed duration; greatest verified qualifying distance wins.
- Ladders:
  - `Open Record`: absolute performance on the exact course/version.
  - `Division Record`: peers grouped by a frozen, evidence-derived ability
    rating rather than self-selected labels.
  - `Personal Breakthrough`: improvement against a frozen personal baseline.
- Cadences: daily, weekly, and monthly windows use explicit templates rather
  than redefining what a record means.
- Record lifecycle: provisional result -> automated validation -> optional
  review/appeal -> final record -> settlement.
- Geometry: source identity, version/digest, centerline or corridor, start and
  finish gates, direction, lap semantics, route-match policy, tolerance,
  privacy, safety, and validation status are all explicit.
- Economy alternatives:
  1. original single-ledger paid-points rolling bounty;
  2. earned-only, non-purchasable, non-transferable capped bounty with a free
     attempt route;
  3. split ledger: gameplay attempt tokens are burned while fixed sponsor
     vouchers are pre-funded and never sourced from participant stakes.

The third option is the provisional safety preference, not an adopted rule.
The research must retain or overturn it with current evidence.

## P1 Trigger

Dispatch is required. The result needs synthesis across three independent
lenses—competition behavior, geospatial measurement, and economy/legal/safety
risk—whose source corpora and expected conclusions differ. The raw source and
simulation output would be substantially larger than the parent should carry,
and later skeptic lanes must independently attack the synthesis.

## Lanes And Subagents

### Explorers — parallel

- `Thaler, Richard` — empirical competition and behavioral-design lane. Returns
  candidate event, ladder, placement, record, and cadence rules plus worked
  participation and sandbagging examples.
- `Alexander, Christopher` — computational-geospatial lane. Returns
  `TrackGeometry Contract v0`, exact evidence status for Volta do Taquaral,
  deterministic fixtures, and anti-cheat/privacy/safety rules.
- `Sunstein, Cass` — adversarial economy and regulatory lane. Returns a
  comparison of the original pot, earned-only bounty, and split-ledger sponsor
  model, with current official-source risk and owner-decision matrices.

Anti-bias axis: composite methodology and source corpus. The group is expected
to disagree about how much motivational friction is acceptable, which geometry
can be measured honestly, and which reward mechanics remain safe and viable.

### Synthesis — sequential

`Simon, Herbert` reconciles the three returns into one rulebook candidate,
geometry contract, exact Taquaral evidence verdict, state/invariant model,
worked scenarios, risk register, ontology delta map, and
`adopt / decide / defer / kill` matrix.

### Review — parallel, then one bounded zig-zag

- `Rittel, Horst` — precedent and current-owner gate.
- `Popper, Karl` — non-vacuity, simulation, and deterministic-settlement gate.
- `Lakatos, Imre` — definitional and authority non-collapse gate.

Anti-bias axis: attack vector. Reviewers may return the synthesis for one
revision. Missing exact source evidence may route once to the relevant
explorer; writer revision cannot repair explorer-owned evidence gaps.

### Persistence And Approval — sequential

- The parent strategist appends verbatim explorer returns to `research.md`.
- `Shannon, Claude` writes `findings.md` only after exact-binding evidence
  closure returns `ready`.
- `Brandenburg, Martin` audits only `findings.md`; one writer revision is
  available.
- The parent verifies the result and remains final approver.

## Dependency Flow

```text
explorers -> synthesizer <-> reviewers -> exact-binding closure -> writer -> auditor
                 |                                                   |
                 +-> explorer feedback (1)                           +-> writer revision (1)
```

- Whole-dispatch ceiling: two loops.
- Every dependent wave waits for joined, closed receipts and the named
  type-owner gate.
- Partial or failed agents remain visible to every downstream role.

## Expected Result

The result is a decision-ready candidate, not an adopted or implemented game:

1. complete playable rules for speed and distance across daily, weekly, and
   monthly windows;
2. open, ability-division, and personal-improvement competition paths;
3. deterministic attempt, verification, record, tie, appeal, settlement,
   rollover/reset, and reward rules;
4. a source/provenance-safe geometry model and explicit Taquaral evidence
   verdict;
5. comparison and recommendation for the points/bounty/sponsor economy;
6. safety, privacy, fraud, consumer, legal, and sponsor risk decisions;
7. worked simulations and kill conditions;
8. a map to current Body War concepts and the smallest next decision/spec route.

## Mutation And Authority Boundary

The strategy may create only its proposal, run-local research, findings, and
receipt artifacts inside this folder. It may not edit:

- current Body War game, geometry, score, SuggestedTrack, or deployment specs;
- `projects/body-war/.craft/ledger.yml` or `CRAFT.md`;
- Body War ontology or application bytes;
- `.arcanum/inventory/` or dispatch telemetry during proposal/execution work,
  except the mandatory append-only dispatch and close rows after confirmation;
- the public OEW dataset or its generated assets;
- any external account, sponsor system, deployment, payment, or reward catalog.

Research cannot provide legal advice, approve sponsor terms, certify geometry,
promote ontology, set score/controller authority, or authorize implementation,
participant testing, release, deployment, or production.

## Inventory Preflight

- Lookup readiness: `ready`; machine validation passed with zero failures and
  153 tag warnings.
- Selected: current SuggestedTrack prototype result, login/geometry/score plan
  review result, and relationship-coverage authority guardrail.
- Excluded: Mint convergence, OEW UI/comprehension, and general DomainSpec v2
  consumer proof as non-load-bearing.
- Design effect: source-backed geometry and score authority receive explicit
  gates; Inventory and the generated OEW dataset cannot decide them.
- Full packet: `STRATEGY-INVENTORY-PACKET.md`.

## Gate And Ledger State

- Confirmation-readiness: `ready` for the exact material strategy bound to
  sheet SHA-256
  `a4f386bcdbcdbdb3cebeeb4b6c5820346e556a25066f2fff02a8bf83e5ab10d1`.
- Sheet form validation: `PASS`; capability-bound route validation: `PASS`.
- Material strategy projection: `same`; SHA-256
  `12095fa9368c230ad426daeb93c83c4ed22431291df5fd197b1524b985902721`.
- Check-tension: independent checker `PASS` plus independent reviewer `PASS`;
  exact receipt in `CHECK-TENSION.md`.
- Human confirmation: pending.
- Registration: not appended.
- Agents: none spawned for research execution.
- Closeout expectation: exactly one dispatch append and one close append after
  a confirmed run, with all nine agents joined and closed or explicit residue.
- Inventory post-result hook: deferred while shared Inventory index/log files
  contain unrelated concurrent changes; this proposal records the residue and
  does not overwrite them.

## Next Human Action

Reply exactly `confirmed` to authorize registration and execution of the exact
material strategy bound above. Discussion or approval to revise is not
confirmation. A jurisdiction change from the assumed Brazil/Campinas baseline
or any change to the agents, lanes, economy alternatives, boundaries, or
expected result creates a revised strategy and requires a new tension gate.
