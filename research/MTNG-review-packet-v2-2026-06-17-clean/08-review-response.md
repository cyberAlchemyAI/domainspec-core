# Response to Outside Reviews

This v2 packet incorporates the main recommendations from Analog 6, Raptor mini, and Gemini.

## Shared Review Signal

All reviews converged on the same boundary:

```text
MTNG is promising as an on-demand, audit-first, sidecar/schema/artifact pipeline.
MTNG is not ready to be a live runtime orchestration layer.
```

## Changes Made

### 1. V1 narrowed to Post-Hoc Issue Packager

The proposal now names the first pilot plainly: a CLI/sidecar process that turns selected logs, transcripts, diffs, and bug reports into issue packets, validator reports, memory candidates, contribution records, and OKF exports.

### 2. Runtime control deferred

Language that could imply live agent delegation or online orchestration has been constrained. Targeted live mode is explicitly deferred.

### 3. Branch pressure weights deferred

The original numeric scoring scheme is replaced with binary branch triggers for V1. Numeric scoring remains a future policy layer after empirical runs.

### 4. Tone simplified into Routing Signature

The poetic term "Tone" has been replaced in implementation sections by "Routing Signature" to reduce metaphor risk and make classifier behavior more concrete.

### 5. Lifecycle simplified

The V1 state model is now `proposed → processing → closed`, with `closed_result` preserving outcome details.

### 6. Reroute loops bounded

Misrouting recovery now has hard limits: one reroute, one validator failure per node, and stop-on-second-failure behavior.

### 7. V1 state ownership clarified

MTNG owns run-local state in its output directory for V1. ResonantOS may later ingest selected outputs through explicit review and authority gates.

### 8. Provider fabric and capabilities clarified

MTNG does not own provider routing in V1. Specialty tools must respect ResonantOS capability grants if run inside the app ecosystem.

### 9. OKF alignment strengthened

The spec now says OKF should be used for as much categorization/export as practical, while MTNG-native records preserve edge cases where OKF is insufficient.

## Remaining Questions for Maintainers

- Should V1 be CLI-only or include a minimal inspection panel?
- Where should output artifacts and audit logs live?
- Should MTNG output target Living Archive intake, GitHub issue creation, or both?
- What is the acceptable V1 failure mode: conservative missed branches or extra false-positive branches?
- What pilot dataset should be used to test the Post-Hoc Issue Packager?
