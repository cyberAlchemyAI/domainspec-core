# Handoff Notice: Admit the OEW focus-scene A/B test before Task Session execution

- Code: `HN-75D3CBED57D2`
- Status: `blocked`
- Type: `session-handoff`
- To: Invoke Refresh owner for the OEW focus-scene Work Pack (`owner-route`)
- From: Codex Task Session preflight (`agent`)
- Project scope: `cyberAlchemy-v2/development/ontology-evidence-workbench-focus-scene`
- Created: `2026-07-30T20:30:46.473656Z`
- Digest: `75d3cbed57d2f1221ed85eb1cb0e3d9111c422b2a428b286672061e0bb892163`
- Remote availability: `unverified`

## Why Now

The user approved an A/B prototype test for the Body War focus scene, but Task Session stopped before writing artifacts because SWU-OEW-FOCUS-TEST-001 is not present or selected in the live Work Pack and the current browser validator cannot emit the planned three-scene evidence set without a bounded runner change.

## Key Points

- The accepted prototype baseline is 237 nodes and 231 edges; the first focus scene is four exact context nodes, zero internal edges, and six labeled portals.
- FOCUS-001 and FOCUS-002 are completed, selected_swu is null, and implementation_authorized and mutation_runtime_ready are false.
- The existing browser validator produces one final browser witness; a repeatable A/B test needs a separately owned runner plus baseline.png, focus-scene.png, portal-pivot.png, and result.json.
- Automation may prove structure, portal semantics, pointer and keyboard interaction, Back restoration, isolation, errors, requests, and cleanup. It cannot prove improved comprehension or discoverability.
- The proposed three-person novice test is a separate prototype signal with gates of at least 7 of 9 correct answers, at least 30 percent faster median answers in the focus condition, and 3 of 3 participants finding focus within 10 seconds.

## Open Calls

- [blocked] Invoke Refresh owner: Will the Work Pack admit and select SWU-OEW-FOCUS-TEST-001 with one bounded A/B runner as a material write and the declared browser artifacts as execution outputs?

## Boundaries

- This notice is communication evidence only and grants no implementation, mutation, dispatch, promotion, publication, or release authority.
- Do not mutate the Body War ontology, accepted focus-scene product source, or completed FOCUS-001 and FOCUS-002 evidence while defining the test SWU.
- Do not classify the new runner as an execution output; it is a material tooling change that requires an explicit owner and validation contract.
- Do not claim human comprehension, accessibility conformance, ontology promotion, release, deployment, or production readiness from automated structural evidence.
- Preserve the existing live viewer and accepted immutable build/browser receipts; run the A/B harness in a fresh isolated Chromium context.

## Next Actions

- Invoke Refresh owner: Add and select SWU-OEW-FOCUS-TEST-001 in the focus-scene Work Pack and manifest, with dependencies on the passing FOCUS-002 receipt.
- Invoke Refresh owner: Declare scripts/validate-body-war-focus-ab.mjs as the bounded material tooling target and declare the four A/B browser artifacts plus terminal Task Session evidence as execution outputs.
- Invoke Refresh owner: Bind acceptance to the same immutable build and viewport, exact baseline and focus counts, literal owns-to-related portal evidence, pointer and keyboard pivot, Back restoration, zero outbound failures or browser errors, cleanup, and protected-tree equality.
- Task Session owner: After a passing Invoke Refresh receipt selects the SWU, execute exactly SWU-OEW-FOCUS-TEST-001 and publish automated evidence plus the still-pending novice-test protocol.

## Source References

- `cyberAlchemy-v2/development/ontology-evidence-workbench-focus-scene/planning/WORK-PACK.md` — Accepted focus-scene outcome, completed SWUs, exact structural baseline, and claim ceiling
- `cyberAlchemy-v2/development/ontology-evidence-workbench-focus-scene/planning/work-pack/swu-manifest.json` — Live selected-SWU and mutation-authorization state
- `cyberAlchemy-v2/development/ontology-evidence-workbench-focus-scene/planning/work-pack/session-evidence/SWU-OEW-FOCUS-002/receipt.json` — Passing terminal preview receipt that the proposed test SWU must consume
- `cyberAlchemy-v2/implementation/ontology-evidence-workbench/scripts/validate-body-war-browser.mjs` — Current browser validator whose single-witness output does not cover the proposed A/B artifact contract

## Suggested Next Route

- Capability: `invoke`
- Mode: `refresh`
- Target: `WP-OEW-FOCUS-001 / SWU-OEW-FOCUS-TEST-001`
- Authorization: `not-granted`

## Terminal Receipt

- `cyberAlchemy-v2/development/ontology-evidence-workbench-focus-scene/planning/work-pack/session-evidence/SWU-OEW-FOCUS-002/receipt.json`

## Authority Boundary

This notice is communication evidence only. The notice and locator grant no permission, authenticate no actor, resolve no open call, select no task, and authorize no mutation, dispatch, Git publication, or external delivery.
