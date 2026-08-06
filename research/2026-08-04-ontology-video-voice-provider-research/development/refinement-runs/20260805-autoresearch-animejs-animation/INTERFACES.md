# Interfaces

These are transport-neutral consumer contracts, not new public HTTP routes.

## `buildCandidate(sceneBeat, residue) -> AnimationHypothesisCandidate`

Pure and deterministic. It binds the frozen source snapshot, generates no runtime claim, and rejects missing contradiction, reduced-motion, or witness fields.

## `consultCandidate(candidate, hostContext) -> ConsultationReceipt`

Uses the existing `animejs-knowledge-consult-read` audience. Authorization, workspace, version context, and evidence scope come from the host. Only `ok` with current evidence may make a candidate tournament-eligible. `abstain`, `stale`, `denied`, `invalid_request`, and `temporary_failure` are preserved, not converted into empty success.

## `runSceneTournament(batch, policy) -> SceneSelectionReceipt`

First evaluates hard gates, then records independent criterion scores and dissent. The operator may select, reject, or defer. A score never authorizes implementation.

## `compileAnimationPlan(selected, runtimeManifest) -> AnimationPlan`

Produces local DOM/SVG layers, pinned Anime.js evidence/runtime identities, timeline states, reduced-motion states, and browser assertions. It performs no browser execution.

## Later `executeWitness(plan) -> BrowserWitness`

Owned by a selected Task Session SWU, not this refinement. It runs only local assets through the shared Playwright runtime, captures fixed viewport/time states, and returns pass/fail evidence.

## Later `appendWorkEpisode(command) -> EpisodeReceipt`

Uses the existing `animejs-work-episode-append` audience after a real attempt. The episode describes what happened and may feed residue. It changes no Task state and creates no Lesson or ontology authority.

