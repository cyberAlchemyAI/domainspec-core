---
module: openai-stock-voice-audition
version: current
status: draft
updatedAt: 2026-08-04
docType: implementation-layering
---

# Implementation Layering: OpenAI Stock-Voice Audition

## Target and scope

- Target: candidate-local OpenAI stock-voice audition runner and evidence workflow.
- Scope: local process plus one later metered external render route.
- Current state: defined and designed; no runner or audio exists.

## Boundary rule

Each layer answers one decision and leaves later claims deferred.

| Layer | Decision question | Minimum working unit | Included | Deferred | Exit evidence | Promotion decision |
|---|---|---|---|---|---|---|
| L0 — offline trust | After this layer, we know whether the manifest and admission boundary fail closed before credentials or network. | Exact excerpt lock, manifest schema, admission evaluator, redacted request preview, causal negative fixtures, transport spy | Node 22.12.0 built-ins; no SDK/package root; no network | Voice selection, account gates, audio, verification, listening | Deterministic tests showing stale/missing/secret/unsupported inputs block and network count is zero | Continue to owner decisions or repair L0 |
| L1 — bounded render | After this layer, we know whether one admitted OpenAI configuration can produce two immutable raw WAV attempts without secret leakage or overwrite. | One exact manifest, two explicit repetitions, append-only attempt receipts | Built-in HTTPS/fetch transport, exact snapshot/voice/request, raw bytes/hashes | Normalization, alignment, blind ranking, full narration | Two raw hashes, identical request digest, safe metadata, observed native format and actual cost/latency fields where returned | Continue to verification, reject route, or stop |
| L2 — fidelity and fit | After this layer, we know whether the candidate is technically faithful and can be evaluated without identity/order bias. | Pinned audio inspection/normalization, independent fidelity checks, key-phrase review, blinded two-repetition listening with three listeners | Verification, derivative provenance, score sheets, unblinding | Full-script continuity and public video | Passing technical/fidelity receipt, locked scores, listener spread, protected/unblinded mapping | Decide, run longer tie-break, or reject |
| L3 — audition decision | After this layer, we know whether the named operator approves, rejects, or defers this configuration for a separate production route. | Hash-bound terminal decision and disclosure-aware production handoff | Decision receipt and bounded next-route inputs | Full narration, animation, mix, captions, release, deployment | Dated owner decision citing governing hashes and all unresolved production gates | Route separately to production planning or stop |

## Non-regression guardrails

- L1 cannot weaken L0 preflight, secret, no-network-on-block, or request-key guarantees.
- L2 cannot replace raw bytes or merge alignment with independent word-fidelity evidence.
- L3 cannot turn a score or audition approval into public-use, release, or deployment authority.
- A changed model, voice, instruction, excerpt, account gate, provider contract, or tool manifest creates a new candidate identity.
- No later layer may silently add a custom voice, pronunciation workaround, retry, or unsupported request control.

## Nested-layer policy

Each wave completes its own layer question before the next opens. Tool selection for L2 is a decision gate, not something L0 or L1 may guess. The current active layer is L0; L1–L3 are conditionally planned and blocked on named decisions.

## Recommended next layer

- Next layer: L0.
- First unit: `SWU-OAIA-001`, exact excerpt and manifest-schema validator.
- Selection: none; Invoke planning does not authorize execution.
- Major deferred scope: all provider calls and audio evidence.
