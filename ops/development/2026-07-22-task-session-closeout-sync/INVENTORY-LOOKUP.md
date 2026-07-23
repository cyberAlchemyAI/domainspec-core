# Inventory Lookup — Task Session closeout synchronization

## Query

- Mode: `lookup`
- Machine source: `.arcanum/inventory/index.json`
- Terms: `task-session`, `continuation-router`, `invoke refresh`, `closeout`,
  `proposal-only`, `apply-approved`
- Authority: non-authority read model

## Matches

The machine index contains nearby execution, refresh, and closeout result
entries, but no entry that defines the Task Session-to-Invoke closeout seam.
Those nearby rows were excluded because they describe project results rather
than the reusable capability contract.

## Selected evidence

- `arcanum/arcana/task-session/SKILL.md`: Task Session contract and existing
  optional continuation behavior.
- `arcanum/arcana/continuation-router/SKILL.md`: exact one-hop authorization
  and owner-receipt join contract.
- `arcanum/spells/invoke/refresh.md`: proposal-only default and
  apply-approved mutation gate.
- `.arcanum/observability/signals/sigil-invocations.jsonl`: repeated Task
  Session completions that leave planning or status projections
  unsynchronized.
- `cyberAlchemy-v2/development/interactive-ontology-learning-map/refreshes/2026-07-22-iolm-ui-current-a1-a2-continuation/refresh-report.json`:
  current example where a passing SWU receipt still required a separate
  proposal-only Refresh and a second apply authorization.

## Exclusions

- Inventory result pages about individual project refreshes: useful as
  instances, but not authority for reusable Task Session behavior.
- Craft ledger state: target projection evidence, not capability authority.
- Historical execution receipts unrelated to post-run synchronization.

## Gap

Inventory does not yet describe a reusable closeout synchronization contract.
The authoritative seam must therefore be derived from the live Task Session,
Continuation Router, and Invoke Refresh contracts plus execution telemetry.

## Downstream obligation

Sigil Development may add a product-neutral, bounded `closeout-sync` contract
to Task Session. Inventory remains unchanged in this maintenance pass because
it is evidence input, not lifecycle authority.
