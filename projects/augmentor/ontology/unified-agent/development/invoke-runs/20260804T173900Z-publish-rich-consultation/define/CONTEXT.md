# Define Context

## Objective

Publish the locally validated rich Augmentor consultation page, API document,
and API contract family `1.1.0` through the existing protected production
route.

## Bounded evidence set

| Obligation | Selector | What it establishes |
| --- | --- | --- |
| Existing production route | `deployment/DEPLOYMENT-RECEIPT.md:30-137` | The protected page, API route, private API container, atomic release directory, rollback generation, and older deployed byte set exist. |
| Release mechanism | `deployment/deploy-static-vps.sh:80-200` | The current script builds, uploads, switches, checks, and rolls back a release. |
| Rich local implementation | `refinement-runs/.../implementation/TERMINAL-EVIDENCE.md:1-53` | Contract `1.1.0`, the new page, glossary, explanation profiles, and local validation pass. |
| Rich bundle closure | `generated/consumer/projection-manifest.json` | Projection, glossary, manifest, and four schema versions/digests form one bundle. |
| Consumer load contract | `augmentor-consultation-contract.mjs:383-417` | The service requires projection, glossary, manifest, and four schema files at startup. |
| Human and agent page | `ontology-visualization.html#agent-api` | The page asks questions, selects explanation depth, renders structured support, and exposes a browser-agent controller. |
| Agent-facing reference | `docs/reference/AUGMENTOR_CONSULTATION_API.md` | External agents receive the `1.1.0` request and answer-use contract. |

Inventory lookup readiness passed. Inventory was used only to locate candidate
evidence; the selectors above are the direct evidence.

## Structured interview gap check

- Mode: release-definition gap check
- Questions asked: 0
- Reason: the operator fixed the site, page, API, and publication objective;
  repository evidence exposes one production route and one rollback model.
- Remaining blocker ambiguity: none for Define, Design, or Plan.
- Deferred execution input: an authorized operator session able to run the
  existing SSH release route. No credential belongs in this package.
- Verdict: pass

## Current truth

The old page and consultation API were deployed on 2026-08-04. The richer local
page and API family are newer bytes. They are not yet deployment evidence. The
release packager still copies only the old two-file projection closure, while
the `1.1.0` loader requires seven bundle files. That mismatch is a blocking
precondition for publication and is the first implementation target.

