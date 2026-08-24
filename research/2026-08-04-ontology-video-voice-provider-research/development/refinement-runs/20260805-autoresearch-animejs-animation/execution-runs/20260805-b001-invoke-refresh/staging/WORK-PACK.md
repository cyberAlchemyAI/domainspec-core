# WORK-PACK — Ontology Video Anime.js Prototype

## Control

| Field | Value |
|---|---|
| gate status | pass for L0; B-001 resolved; L1 remains sequenced after OAVA-002 |
| complexity | medium |
| output mode | split |
| active layer | L0 |
| selected SWU | none |
| prototype target | Sequence 6, `04:29–04:39` |
| readiness profile | candidate-local browser prototype |
| execution evidence | B-001 acquisition validated; SWU execution pending |

## SWU handoff table

| SWU | Behavior | Dependencies | Future write scope under this run | Done criteria | Validation |
|---|---|---|---|---|---|
| OAVA-001 | validate exact source snapshot and candidate structure | none | `prototype/contracts/*`, `prototype/fixtures/*`, `prototype/lib/validate-candidate.mjs`, `prototype/test/candidate.test.mjs` | positive fixture passes; one-cause source/schema/proof/reduced-motion mutants fail | `node --test prototype/test/candidate.test.mjs` |
| OAVA-002 | build candidate and consult existing vault fail-closed | 001 | `prototype/lib/build-candidate.mjs`, `prototype/lib/consult-animejs.mjs`, `prototype/lib/evaluate-eligibility.mjs`, `prototype/test/consultation.test.mjs` | exact evidence ids returned; all non-`ok`/stale paths block; no canonical vault writes | `node --test prototype/test/consultation.test.mjs` plus vault byte-delta check |
| OAVA-003 | admit one local Anime.js runtime asset | 002 + B-001 resolved | `prototype/vendor/anime.esm.js`, `prototype/runtime-manifest.json`, `prototype/lib/validate-runtime.mjs`, `prototype/test/runtime.test.mjs` | version/origin/license/path/hash exact; no CDN or runtime network; mismatch blocks | `node --test prototype/test/runtime.test.mjs` and network-string scan |
| OAVA-004 | build static S6 DOM/SVG semantic scene | 003 | `prototype/index.html`, `prototype/styles.css`, `prototype/src/scene-s6.mjs`, `prototype/test/scene.test.mjs` | typed objects, edge, arrow, label, captions surface, and terminal states are addressable; PNG untouched | `node --test prototype/test/scene.test.mjs` |
| OAVA-005 | animate the ten-second S6 edge witness | 004 | `prototype/src/timeline-s6.mjs`, `prototype/src/runtime.mjs`, `prototype/test/timeline.test.mjs` | standard and reduced timelines reach identical semantic endpoints; direction never reverses | `node --test prototype/test/timeline.test.mjs` |
| OAVA-006 | capture deterministic browser evidence | 005 | `prototype/browser/verify.mjs`, `prototype/test/browser.test.mjs`, `prototype/evidence/<run-id>/*` | fixed viewport/time assertions pass in standard/reduced modes; source/vault zero delta; screenshots and state JSON hash-bound | pinned shared Playwright command plus `node --test prototype/test/browser.test.mjs` |
| OAVA-007 | record bounded owner disposition | 006 | `prototype/reviews/<run-id>.json` | named reviewer chooses `accept|revise|retire` with evidence hashes and rationale | schema/hash review; no auto-continuation |
| OAVA-008 | append WorkEpisode and prepare next-route residue | 007 | `prototype/episodes/<run-id>.json`, `prototype/handoffs/s7-owner-gate.md` | one idempotent episode receipt; projection shows attempt; Lesson eligibility false; S7 is a non-executed handoff only | operational API tests plus receipt/project read |

## Blockers

| ID | Status | Scope | Condition | Owner | Resolution |
|---|---|---|---|---|---|
| B-001 | resolved | OAVA-003+ | Anime.js v4.5.0 runtime and license are vendored locally. | dependency owner | Acquisition and validation evidence: `execution-runs/20260805-b001-animejs-runtime/acquisition-receipt.json` and `validation-receipt.json`. OAVA-003 remains ordered after OAVA-002 and requires explicit Task Session selection. |
| B-002 | open | OAVA-006 | The shared Playwright binary is not on the active shell PATH, though the verified `1.59.1` absolute runtime and Chromium 1217 exist. | Task Session | Re-discover and pin exact executable, package, browser, and hashes at preflight; do not add a package root for Playwright. |
| B-003 | open | OAVA-007 | Named animation/source reviewer is not recorded. | video owner | Name reviewer before subjective disposition. |

## Atomicity and continuation

Each SWU produces one independently reviewable behavior. A terminal closeout may point to the unique dependency-ready successor, so design/readiness is not rerun when the source and plan digests are unchanged. It may not silently start the successor, acquire a dependency, or cross an unresolved external-effect gate. B-001 was separately acquired and is resolved; B-002 and B-003 remain open.

## Task Session closeout sync

Every mutation-capable SWU captures exact target baselines as SHA-256 or `absent`, permits only its declared paths, runs its exact validation, checks zero delta in the source video, AutoAds, and canonical Anime.js vault, and writes `work-pack/closeouts/SWU-OAVA-00N.json`. The terminal receipt must include the next unique successor or blocker and must not claim that successor started.

No execution is selected by this Work Pack.
