# Distill Validate — OAVA-003 Work Pack

## Run profile

- Target: the runtime-admission slice between completed consultation and future scene construction.
- Mode: Validate.
- Proposal tracks: one Invoke Plan proposer and one true independent read-only Balancer helper.
- Recursive rounds: one critique and one reconciliation.
- Evidence ceiling: planning validation only; no implementation or runtime execution.

## Proposer claim

The manifest, pure verifier, and causal tests are the smallest coherent unit because the externally reviewable behavior is one fail-closed decision: either the exact local `animejs@4.5.0` runtime and MIT license match their approved provenance, bytes, paths, and static constraints, or admission returns one stable failure code. A manifest without enforcement is prose; a verifier without a closed manifest has no fixed identity; either without causal tests can fail open.

## Balancer objections and reconciliation

| Category | Objection | Decision |
| --- | --- | --- |
| atomicity | A receipt-only or manifest-only unit would be narrower. | reject split; neither establishes an executable admission decision. Retain exactly three collaborating files in one SWU. |
| source integrity | Runtime admission could accidentally rewrite or normalize vendor bytes. | accept; vendor files are read-only inputs and zero-delta evidence is acceptance-critical. |
| path safety | Relative-path checks alone miss traversal and symlink escape. | accept; require absolute, backslash, traversal, alternate-location, and resolved-path escape negatives before file use. |
| proof strength | Package metadata or a passing old receipt alone may be stale. | accept; bind receipt path, schema, size, hash, package identity, installed assets, required checks, and current live bytes. |
| execution leakage | Syntax validation might be confused with runtime execution or conformance. | accept; use static `node --check`, prohibit dynamic import and Anime.js calls, and retain the local-admission-only claim ceiling. |
| lifecycle | A passing test could expose the scene unit without owner synchronization. | accept; Task Session emits the terminal receipt and Invoke Refresh alone synchronizes closeout and exposes OAVA-004 with `successor_executed=false`. |

## Technique validation

- Abstraction-level guard: pass. The unit remains L1 dependency admission; it contains no scene, timeline, browser, voice, or episode behavior.
- Recomposition proof: pass. Completed consultation plus admitted local runtime supplies the two independent prerequisites for later OAVA-004 scene construction.
- Evolution profile: an Anime.js version, license, package, path, receipt schema, or semantic change invalidates this plan epoch instead of being hidden behind a generic provider abstraction.
- Boundary-object check: pass. The closed manifest and immutable verification result are the only consumer boundary objects; no executable runtime handle is returned on failure.
- Premortem: the likeliest failure is trusting a stale receipt or a path that escapes through a symlink. Ordered receipt, path-resolution, and live-byte gates make those causal failures.
- Frame expiry: any source identity, route digest, predecessor closeout, or validation-contract change requires re-planning or refresh before selection.
- Navigation: start at `WORK-PACK-OAVA-003.md`, proceed through Implementation Readiness, and execute only `work-pack/tasks/TASK-OAVA-RUNTIME-ADMISSION.md` after admission.

## Verdict

Pass. The independent Balancer found no blocker or open user decision after the above constraints were made explicit. OAVA-004 and all actual Anime.js execution remain outside the unit.
