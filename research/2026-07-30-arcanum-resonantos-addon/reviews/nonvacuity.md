# Non-vacuity review

STATUS: pass  
VALIDATION: block  
BLOCKERS: [literal Strategy + Whisper route has no owner-backed execution witness; Subagent Strategy is absent from the consumer installation; installed Whisper is drifted and has no ResonantOS adapter; proposed manifest is not valid against the current SDK schema; no Arcanum bridge routes or capability-token map exist; no digest-bound proposal/approval implementation exists; no targeted child-clarification owner route exists; no reload/disable/rollback fixture exists; product checkout is seven commits behind cached origin/dev]  
ARTIFACTS: [reviews/nonvacuity.md]  
VERDICT: REVISE

## Witness verdict

KILL every present-tense or positive integration claim. Retain only the three-layer topology as an implementation candidate and the current owner seams as precedent.

The chain is unwitnessed from the first Arcanum-specific transition onward:

1. Explicit-command precedence is current-source supported at `browser-first/resonantos-side-panel-extension/src/lib/side-panel-command-router.js#createSidePanelCommandRouter/respondToCommand`.
2. The subsequent ordinary-language Arcanum classifier is absent.
3. `StrategyProposal` canonicalization, digesting, edit/decline behavior, exact approval, prelaunch revalidation, and replay protection are absent.
4. Bootstrap-installed package presence is not executable product authority. `../workspace-resonant/.agents/skills/subagent-strategy/` is absent. Whisper exists at `.agents/skills/whisper/SKILL.md` but is drifted and has no product adapter.
5. Add-on SDK owners exist, but the synthesis’s “Manifest candidate” is not an exact valid manifest. Current `src/core/contracts.ts#AddOnManifest` requires `name`, `version`, `author`, `description`, structured `surfaces`, `requestedCapabilities`, `providerRequirements`, `archiveIntegration`, `health`, `installHooks`, and `compatibility`. It expects `provenance` and `runtimeIsolation` objects, not scalar `provenance`/`isolation`; `category: orchestration` is not established as an accepted current enum value.
6. Current loopback delegation routes in `browser-first/host/addon-delegation-host-service.mjs#createAddonDelegationHostService` expose Hermes/OpenCode and generic delegation records. `executeDelegationRecord` in `addon-delegation-service.mjs` accepts only `hermes`, `opencode`, or `engineer`. No Strategy or Whisper owner operation, status route, clarification route, or artifact adapter exists.
7. Existing add-on/delegation cards and lifecycle helpers prove a projection seam, not the proposed two-child behavior, targeted clarification, parent continuity, owner-backed partial outcome, or reload reconciliation.
8. No accepted fixture proves separate open/attach/consume/intake actions.
9. Disable/revocation vocabulary exists, but no Arcanum run proves new-launch blocking, active-run reconciliation, or preserved owner state.
10. Rollback is prose only: no pinned prior adapter/profile artifact or observed restoration exists.

The branch basis is stale: `../workspace-resonant/2.0.0-alpha` is `dev@6f92af7b32b17d2eef66230d463eb8b6a21a98f7`, seven commits behind cached `origin/dev@3b07e635d596c18f9a047ef5921892acc7cba4ff`. Thus even precedent selectors require refresh before implementation.

## Exact bounded repairs

1. Refresh `dev`, record the new commit, and re-resolve every cited selector before freezing contracts.
2. Produce a complete JSON fixture, preferably `public/addons/arcanum.json` or an explicitly sideloaded fixture, matching `src/core/contracts.ts#AddOnManifest`; validate it through `src/sdk/addons/validation.ts#validateAddOnManifest` with `source: "sideload"`.
3. Separately obtain approval for a Bootstrap dry-run and exact selection refresh. Require current generated provenance for Subagent Strategy, Whisper, Orchestrate, runtime profile, and support bytes. Package presence must still report `Unavailable` until native owner operations exist.
4. Define one Arcanum bridge owner with exact paths, methods, request/response schemas, and scoped route-capability tokens for runtime status, proposal preview, approval, start, status, clarification, and artifact read.
5. Bind literal operations `subagent-strategy.execute` and `whisper.execute` to stable public native entrypoints. If either requires nested model CLI or lacks an owner operation, kill execution and expose preview/status only.
6. Add canonical proposal serialization and SHA-256 binding over every launch input. Prove preview, edit, decline, and stale approval produce zero registrations, owner calls, child records, processes, and writes.
7. Persist approval before exactly-once registration; bind `(proposalDigest, actionId)` and prove replay fails with zero additional starts.
8. Add child-scoped clarification using opaque owner handles. Prove an A-addressed message reaches A only and leaves parent/B unchanged.
9. Add owner-state reconciliation on reload; unreachable state must render `Unknown`, never cached success.
10. Implement independent result commands and prove `open != attach != consume != intake`.
11. Make disable independently block new launches, even if rollback fails. Rollback must restore pinned manifest, adapter, and runtime-profile hashes without rewriting owner records.

## Evidence-closure obligations

Required deterministic commands after implementation:

- Focused manifest tests under `src/sdk/addons/*.test.ts`
- Focused bridge capability-token and delegation tests
- Command-router, chat-session, child-isolation, lifecycle, reload, and consumption tests
- `npm run test:browser-first`
- `node scripts/security-pipeline/run-check.mjs`
- `npm run pre-release:scan`
- `npm run verify:alpha`

Required browser fixture:

- Enter the literal Strategy + Whisper request.
- Observe explicit-command fallthrough, `P1/D1`, two children, and “no actions started.”
- Edit to `D2`; prove approval of `D1` starts nothing.
- Approve current digest; observe approval persisted before two distinct owner correlation IDs.
- Keep parent chat responsive while children run.
- Send A-only clarification and prove no parent/B delivery.
- Observe owner-backed A `Blocked` with `blockerRef`, independent B `Succeeded` with `artifactHandle`, and a withheld dependent gate.
- Reload and observe identical reconciled owner truth.
- Open B without consumption; then explicitly consume only B; observe no sibling, lifecycle, or memory mutation.
- Disable and prove a new launch is blocked.
- Restore the pinned prior adapter/profile and rerun the fixture.
- Confirm screenshots, diagnostics, events, argv, and artifacts contain no tokens, credentials, private paths, or private-domain prose.

Until that closure exists, the correct claim is: owner seams and a bounded candidate topology are identified; no valid Arcanum add-on, execution route, or browser-valued two-child witness currently exists.
