# §5 v6 STR + Telemetry Schema Additions — Draft

**Filed:** 2026-04-19
**Intended parent:** `pipeline/blueprint/v0.1/section_05_pipeline.md` (v5 LOCKED → v6 in-flight)
**Round:** §5 v6 re-lock Thesis round (active)
**Carries:** Item 2 (STR column) per scope-close pin

This is a draft for folding into the §5 v6 re-lock. Not a LOCK. Thesis round audits this text plus the rest of the v6 surface.

---

## New subsection — §5.X Per-Invocation Telemetry Record Schema (pinned)

Every seat invocation emits exactly one telemetry record at invocation-end. Schema:

```
{
  "run_id":                 <string>,       // session run identifier (§5 run-lifecycle)
  "seat":                   <enum>,         // scout|scribe|editor|judge|red_team|reasoner_review|code_author|code_reviewer_{1..5}
  "timestamp":              <iso8601>,      // invocation-end, UTC, millisecond precision
  "model_family_resolved":  <enum>,         // router.yaml family taxonomy, post-fallback (anthropic|openai|openai_oss|alibaba|meta|moonshot|google)
  "model_id_resolved":      <string>,       // concrete model string after fallback resolution
  "token_count_input":      <int>,          // prompt + system tokens as reported by provider
  "token_count_output":     <int>,          // completion tokens as reported by provider
  "latency_ms":             <int>,          // invocation wall-clock; excludes queue time
  "success_flag":           <bool>,         // seat-specific outcome predicate (§4.7 claim-evidence map + §5 POST-gate family)
  "failure_code":           <string|null>,  // if success_flag=false, one F-* code from §6 registry
  "invocation_id":          <string>        // globally-unique per invocation (UUIDv4 acceptable)
}
```

Field discipline:
- All fields are REQUIRED. No optional fields at v6 pin.
- `success_flag` is a seat-specific outcome predicate, not a generic "no-error" flag. Judge success = rubric scored on all dimensions with evidence strings present. Scribe success = draft complete with no KGIE preflight failures. Scout success = VERIFY stage returned a non-VERIFICATION_FAILED status.
- `failure_code` MUST be non-null when `success_flag=false`. This is a §6 registry-membership gate.
- `model_family_resolved` captures post-fallback family, enabling the Canary family-collision check (§4.15) and Runtime Integrity drift detection (§4.16 4a).

### Emission path

Records are emitted to the org's telemetry sink per §4.10.4 (`claim-evidence-write` SIMPLE target, under `vault/telemetry/<run_id>/`). Per-record emission is append-only; batch flush at run-end is §5's responsibility, not the seat's.

## New subsection — §5.Y Success-to-Token Ratio (STR) Derivation

STR is a derived metric, not a substrate. The §5 v6 schema above provides the ingredients; STR derivation is defined here so downstream consumers (A11 R.6 Telemetry Commons, Item 3 Canary harness) have a single canonical definition.

### Per-invocation STR

```
STR_per_invocation = 1 / (token_count_input + token_count_output)   if success_flag=true
                   = 0                                               if success_flag=false
```

Per-invocation STR is a raw value retained only inside the run-local telemetry store. It never exits a client's Golden Quill as a raw point.

### Per-seat rolling distribution

Per seat `s`, over a rolling window `W` (default `W = 30 days`) with minimum denominator `k = 5` invocations (A11 R.6 k-anonymity floor):

```
STR_distribution(s, W) = { quantile: value }
  where quantile ∈ { 0.10, 0.25, 0.50, 0.75, 0.90 }
  computed over the set of per-invocation STR values for seat s within window W
```

Distributions are ONLY emitted when `count(invocations(s, W)) ≥ k`. If the count is below `k`, the distribution is suppressed for that window and seat — fail-closed per A11 R.6 k-anonymity discipline.

### Export shape

STR distributions export as the quantile envelope above. Never as per-invocation raw points. The Canary harness (§4.15) is the sole consumer authorized to read per-invocation raw STR values, and only within the same Golden Quill's local run-context — never in cross-client export.

## §5 run-lifecycle addition — Privacy Router call-site placeholder

Per §3 blueprint-amendment-plan: §5 v6 adds a placeholder paragraph naming the Privacy Router PRE-gate (Item 1) call-site between seat selection and model invocation. The concrete gate spec lands in §4 v2.3; §5 v6 describes the orchestrator position.

Placeholder paragraph:
> Between seat resolution (the output of §5 seat-selection logic) and model invocation (the HTTP or local-LLM call), the orchestrator invokes the Privacy Router PRE-gate (§4.14, landing at §4 v2.3). The gate returns one of LOCAL-ONLY / CLOUD-ELIGIBLE / CLASSIFIER-ERROR per §4.14 semantics. LOCAL-ONLY and CLASSIFIER-ERROR both force local seat resolution regardless of default binding or BYOK key presence. No invocation dispatches to a cloud endpoint prior to this gate.

## Paired §0.5 row additions (2 rows — per 03_blueprint_amendment_plan.md)

| Primitive ID | Kind | Source | Description |
|---|---|---|---|
| `per_invocation_telemetry_record_schema` | schema | §5 v6 §5.X | See full schema above. Parent-lock: §5 v6. |
| `str_derivation_and_aggregation` | mechanism | §5 v6 §5.Y | Per-invocation + per-seat rolling quantile distribution with k=5 W=30d floor. Parent-lock: §5 v6. |

Parent-wins discipline: both rows point at §5 v6 as parent_lock_version. F-INDEX-STALE must see both at commit time.

## Thesis round cross-check list

Audit pass 1 (Editor + Judge):
- Editor: schema field naming consistency; k/W default values justified; "success_flag" predicate clarity per seat
- Judge: rubric fit vs §5 v5 LOCK style; A11 R.6 k-anonymity compliance; no new substrate introduced

Audit pass 2 (Red Team + Reasoner):
- Red Team: what if a seat emits a malformed record? what if clock drift makes `W` computation wrong? what if provider token counts are wrong? what if `success_flag` predicate is adversarially tuned?
- Reasoner: decision journal — was additive-aggregation considered vs distribution? was `k=5 W=30d` justified or arbitrary? was rolling window vs tumbling window debated?

## Open questions for Josh

- Default quantile set `{0.10, 0.25, 0.50, 0.75, 0.90}` — acceptable, or tighter (e.g., `{0.05, 0.50, 0.95}`) preferred?
- `W = 30 days` default — appropriate for grant-writing cadence?
- Should `failure_code=null` when `success_flag=true` be the only null-allowed case, or should we pin ALL fields non-null at v6?
