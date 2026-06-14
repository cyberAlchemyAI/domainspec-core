# Build-All DomainSpec Specs — Result

- Dispatch: `gq-domainspec-build-all-specs-2026-06-13` (route `DISPATCH-BUILD-ALL-SPECS.json`, validated pass)
- Mode: fanout, 5 spec-builder subagents, parent synthesis
- Adoption: DomainSpec tooling wired at `./.domainspec` → `../domainspec-core/implementation/domainspec` (gitignored, **not committed** to GoldenQuill)
- Validator: `python3 .domainspec/scripts/audit_richness.py <spec-dir>` (stdlib)

## Verdicts (parent re-run, authoritative)

| Domain | Action | Concepts | Edges | Test rows | Severity | Verdict |
|---|---|---|---|---|---|---|
| goldenquill-promotion-governance | validate + complete | 88 | 79 | 80 | 11 | MODERATELY UNDER-SPECIFIED (named residue) |
| capital-logic-library | author net-new | 29 | 17 | 71 | **5** | **RICH IN STRUCTURE w/ gaps** (best) |
| hardware-golden-image | author net-new | 44 | 33 | 67 | 10 | MODERATELY UNDER-SPECIFIED |
| tilth-runtime-build | author net-new (bounded) | 29 | 28 | 97 | 8 | MODERATELY UNDER-SPECIFIED |
| quality-security-proof | author net-new | 35 | 25 | 0 | 14 | UNDER-SPECIFIED (TEST-SPEC deferred to L2/Victor) |

Calibration: the shipped reference `examples/order-management` audits at **severity 19** — every spec here is richer (lower severity) except QSP, whose severity is entirely TEST-SPEC-deferred (injectivity + faithfulness are green).

## What each produced (all under `docs/features/<domain>/`)

- **promotion-governance** — drove the pre-existing 14-file spec from severity 23→11: registered 34 orphan aspect H2s as concepts (34→0 orphans), resolved both original collapse clusters (PromotionCandidate≢OwnerDecision; ProjectEventToDag≢PublishApprovedReusePacket), fixed TEST-SPEC ID format so 80 rows parse (was 0), reconciled prose 47→44 KPIs + named the 9-ingestion/13-op-output event axes. **No canonical enum mutated.**
- **capital-logic-library** — 8 files (SPEC + domain/operations/queries/interfaces/events/states/TEST-SPEC). 29 concepts; faithfulness 106%; **no CIC→CLC coupling** (AntiCouplingRule ACR-INV-1..4, closed sets 8 CLC / 6 CIC).
- **hardware-golden-image** — 10 files. 44 concepts; 0 unwitnessed edges; SKU values (EXT-HGI-1) + burn-in thresholds (EXT-HGI-2) marked operator-input, not invented; Sovereignty Promise modeled (customer-held keys, no call-home, round-trip digest).
- **quality-security-proof** — 3 files (SPEC/domain/operations). 35 concepts; injectivity + faithfulness green; TEST-SPEC + guardrail-test-matrix.yaml deferred to Victor (L2 work per BUILD-SPEC). Cross-feature deps modeled (claims→sales/COF, instrumentation→WGD Day-60).
- **tilth-runtime-build** — 7 files. 29 concepts (six council seats as operations + GrantCyclePipeline workflow). PostureEnforcement + SplitContextComposition marked decision-gated on DEC-BC-POSTURE-VOCAB; OperatorConsoleProjection gated on DEC-BC-UI-BOUNDARY (read-only/deferred only, never interactive v0.1 UI). Three-posture canon; no "Sanitized"; no [SLOT_*]; no CIC→CLC coupling.

## Gates held (all builders)
No CLAUDE.md / locked-architecture / canonical-enum mutation; Law 3 (no `orgs/`); no CIC→CLC coupling; v0.1 headless; three-posture canon; writes confined to each `docs/features/<domain>/`; `.domainspec` symlink stays gitignored.

## Residue / next
- **Common residue:** M6 / collapse "clusters" reported by the audit are mostly **parser-dialect artifacts** — the audit credits distinguishing structure to H2-header concepts, so H3-authored entities/rules/events read as collapsed despite distinct content; and inline paired-rule guards (the canonical order-management pattern) trip M6. Documented per-spec in each SPEC's residue section.
- **quality-security-proof** needs its TEST-SPEC.md authored to clear fullness (Victor / L2).
- **Excluded by design:** the business-strategy Craft nodes (sales, staffing, finance, roadmap, white-glove, after-acceleration, boundary-and-canon, node-on-desk-readiness) — not domain-modelable software contracts.
- **Decision-gated, unresolved:** DEC-BC-POSTURE-VOCAB (tilth posture), DEC-BC-UI-BOUNDARY (console), DEC-OQ4 (promotion L1).
