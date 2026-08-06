# TASK-OAIA-PREFLIGHT — Offline trust boundary

## Objective

Implement the L0 manifest and admission boundary so every invalid, stale, unresolved, secret-bearing, or undocumented candidate stops before credential access, network activity, or attempt output.

## Mapping

- Slice: S-PREFLIGHT
- Layer: L0
- Wave: W1
- Sources: `../../SPEC.md`, `../../DESIGN.md`, `../../IMPLEMENTATION-DETAILS.md#preflight-algorithm`, `../../VALIDATION-CONTRACTS.md`
- Dependencies: W0 baseline; no provider/account/voice decision required for fixture-only implementation.
- Current gate: ready for one explicit SWU selection; none selected.

## SWU-OAIA-001 — Exact source and manifest validator

- Primary behavior: accept only structurally valid, source-bound candidate input.
- Independent boundary: tests can prove exact/stale/escaping/unknown-field behavior without admission logic.
- Split analysis: canonical JSON and schema validation are helper concerns of the same accepted-manifest behavior.
- Write scope: `.gitignore`; `runtime/schemas/audition-manifest.schema.json`; `runtime/lib/canonical-json.mjs`; `runtime/lib/validate-manifest.mjs`; `runtime/test/manifest.test.mjs`.
- Done criteria: schema closed; relative paths stay in-root; excerpt digest/1,487-byte/1,473-code-point/237-word checks exact; model is dated; stock/custom enum enforced; unsupported fields rejected; fixtures are causal.
- Acceptance evidence: passing positive fixture and one-cause failures for punctuation drift, traversal, alias-only model, custom voice, unknown field, and stale digest.
- Validation: `node --test runtime/test/manifest.test.mjs`.
- Execution owner: local-fallback.
- Handoff: read only shared context and named source anchors; return the standard worker receipt; do not implement admission or network.

## SWU-OAIA-002 — Admission decision and safe request preview

- Primary behavior: deterministically decide `admitted|not_ready` and emit a redacted preview only on complete inputs.
- Independent boundary: can pass with injected fake transport/probe and no provider credential.
- Split analysis: gate evaluation and preview projection form one observable decision contract; transport remains SWU-003.
- Dependencies: SWU-OAIA-001.
- Write scope: `runtime/lib/evaluate-admission.mjs`; `runtime/lib/request-preview.mjs`; `runtime/bin/audition.mjs`; `runtime/test/admission.test.mjs`.
- Done criteria: all owner/account/tool/route gates explicit; allowlisted request keys only; secret-shaped fields rejected/redacted; no environment access; fake transport invocation count zero on every block; canonical receipt stable.
- Acceptance evidence: positive complete fixture plus one-cause failures for every blocker class, extra request keys, secret material, and stale provider/source digest.
- Validation: `node --test runtime/test/admission.test.mjs` and scoped source scan.
- Execution owner: local-fallback.
- Handoff: do not add real fetch, read credentials, resolve owner decisions, or call the provider.

## Synchronization

SWU-001 closes before 002 can be selected. Both close through their exact `WORK-PACK.md#task-session-closeout-sync-contract` rows. L0 completion changes no audition admission and does not open W2 automatically.

## Completion evidence

L0 is complete when both SWU receipts pass, the full runtime tests remain offline, and an independent transport spy proves every incomplete-manifest path invokes the network zero times.
