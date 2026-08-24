# Distill Plan Validation - SWU-RWO-CX-003R

- Verdict: pass
- Target: WP-RWO-CODEX-APP-SERVER-REPAIR-001
- Unit count: 1
- Task-shaped units: 0
- Recomposition: pass
- Hidden acceptance-critical gaps: 0
- Mutation authority: none

## Smallest Coherent Unit

The retained unit owns one behavior: select and execute the public app-server adapter through the generic runtime boundary while returning raw evidence to Task Session. Registration, driver, fake process, parity validator, and documentation are not independent product behaviors. Splitting them would permit a registered adapter without an executable driver, a driver without fail-closed validation, or public claims without installed-schema evidence.

## Split Analysis

Candidate children considered:

1. adapter registration;
2. stdio driver;
3. fake-stdio tests;
4. installed-schema parity;
5. documentation.

Each child can be mechanically authored alone, but none can satisfy or safely expose the behavior alone. Their acceptance closes only as one reversible repository-local change set. The unit does not bundle later provider-neutral physical records, private capsule integration, model execution, network transport, or lifecycle promotion.

## Recomposition Proof

The unit repairs exactly the three codes in the immutable CX003 finding:

- LIVE_APP_SERVER_ADAPTER_UNAVAILABLE -> registration plus driver and fake execution;
- CX002_CAPSULE_BRIDGE_UNSPECIFIED -> generic seven-method boundary without copying private bytes;
- INSTALLED_BINARY_PARITY_UNVERIFIED -> regenerated installed-schema parity evidence.

A fresh CX003 audit then recomputes sufficiency. CX004 remains unreachable from this Work Pack.

## Narrowness And Boundaries

- One unit and one parent task.
- Ten exact public material paths.
- Eight exact private execution outputs.
- No Git, Inventory, ledger, telemetry, credential, network, model, provider, daemon, publication, or deployment effect.
- Failure creates no terminal and exposes no successor.

## Result

The candidate is minimally executable and not overbuilt. Canonical validators, v2 readiness, and post-audit candidate inventory are complete; exact human owner acceptance remains outstanding.
