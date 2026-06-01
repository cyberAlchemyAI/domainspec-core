---
title: §4 v2.x.y.1 — F-PACKET-* predicate bodies LIVE flip + META-gate strengthening
filed: 2026-05-15
operator: Josh Inklovich
status: LOCKED 2026-05-15 — compound paired-commit (sibling 3/5) with §16 v1.1 + §2 v7.x + §15 v2.x + §0.5 v24 at same `lock_timestamp_utc`. L-005 strict two-cycle Thesis CLOSED with FULL LIVE CROSS-FAMILY rigor.
parent_locks:
  - pipeline/blueprint/v0.1/section_04_v2_x_y_packet_amendment.md                        # §4 v2.x.y LOCKED 2026-05-15 row 217 (predecessor; 18 NotImplementedError predicates land LIVE here)
  - pipeline/blueprint/v0.1/section_04_v2_x_z_wpfa_amendment.md                          # §4 v2.x.z row 207 — LIVE bodies pattern mirrored byte-for-byte
  - pipeline/blueprint/v0.1/section_04_logician_v2_x_2_amendment.md                      # §4 v2.x.2 row 203 — F-REFLECTION-* sibling at producer-side
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md                       # v7.0.4-M1 row 190 — A12 Decimal mandate + canonical-JSON Ed25519 mirrored
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                          # v7.0.7 row 180 — producer-pubkey pinning mirrored at F-PACKET-SIGNATURE-INVALID
companion_amendments:
  - pipeline/blueprint/v0.1/section_16_v1_1_amendment.md                                  # sibling 1/5
  - pipeline/blueprint/v0.1/section_02_v7_x_reflection_packet_subkind_amendment.md        # sibling 2/5
  - pipeline/blueprint/v0.1/section_15_v2_x_archivist_reflection_amendment.md             # sibling 4/5
  - pipeline/blueprint/v0.1/section_00_5_section_16_v1_1_amendment.md                     # sibling 5/5
compound_lock_with: section_16_v1_1_amendment.md + section_02_v7_x_reflection_packet_subkind_amendment.md + section_15_v2_x_archivist_reflection_amendment.md + section_00_5_section_16_v1_1_amendment.md
amendment_class: predicate-body-realization (18 NotImplementedError → LIVE; META-gate body strengthened)
target_lock_row: 223
ws_dispatch: WS-Reflection Packet v0.2 first wave compound LOCK
review_discipline: L-005 strict two-cycle; FULL live cross-family
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out)
session_metrics: pipeline/metrics/session_log.jsonl
---

# §4 v2.x.y.1 — F-PACKET-* predicate bodies LIVE at v0.2 first wave

## §4.v2.x.y.1.0 Amendment intent

This amendment realizes 18 BINDING F-PACKET-* predicate bodies from NotImplementedError to LIVE at the v0.2 first wave. The 19th predicate (F-PACKET-COVERAGE-INCOMPLETE META-gate) was LIVE at v0.1 hook and STRENGTHENS at this LOCK per Cycle 1 RT-01 fold-in contract 7 (dry-run probe each BINDING predicate + reject NotImplementedError).

**Path-B naming invariants preserved.** F-PACKET-* still owns the artifact-validity layer; F-REFLECTION-* still owns producer behavior (§4 v2.x.2); F-ARCHIVIST-* still owns substrate write (§15 v1); F-WPFA-* still owns the sibling artifact (§4 v2.x.z). Zero cross-family imports — AST-lint regression at `pipeline/linting/ast_lint.py` enforces unchanged.

## §4.v2.x.y.1.1 Live body specifications (18 predicates)

The 18 BINDING predicates flip from NotImplementedError to live bodies per §16 v1 §16.8 + the v1.x amendment-realization checklist contracts 1-8 in §4 v2.x.y §9. Module bodies live at `pipeline/logician/gates/f_packet_*.py`.

### §4.v2.x.y.1.1.1 F-PACKET-INSTANCE-LEAK (contract 1)

Three-layer detection per §15.9.2 RT-07 precedent:

- **Layer 1 — NFKC normalization.** `unicodedata.normalize("NFKC", text)` applied to pattern_summary + proposed_rule fields before any subsequent check. Closes homoglyph + ZWJ + RTL-override class at the canonicalization step.
- **Layer 2 — NER scan.** Surface-level NER over NFKC-normalized text. v0.2 uses `re` regex over the operator-signed entity-name blocklist at `vault_shared/reflection_packet/instance_blocklist.signed.yaml` (deterministic; no LLM at v0.2; v1.x may upgrade to spaCy or local NER model). Operator-signed blocklist mirror of router-template pubkey pinning byte-for-byte; SHA3-512 over canonical YAML.
- **Layer 3 — Regex.** Static regex closed-set scan for known instance-level patterns (`r"\b\d{3}-\d{2}-\d{4}\b"` US-SSN guard; `r"\$\d+(?:,\d{3})*(?:\.\d{2})?"` award-specific dollar amounts; client-name regex per operator-signed list).

Sub-tags: `.client_name_present`, `.funder_specific_with_client`, `.ner_entity_match`, `.unicode_homoglyph`, `.zwj_obfuscation`.

Fail-closed iff any layer surfaces a match. Detail field names the layer + sub-tag.

### §4.v2.x.y.1.1.2 F-PACKET-CROSS-ORG-LEAK (contract 2)

Two-axis defense mirroring `check_f_wpfa_cross_org_leak` byte-for-byte:

- **Axis (a) — path-slug match.** `target_write_path` normalized via `PurePosixPath`; matched against `r"(?:^|/)orgs/(?P<slug>[^/]+)/vault/operational/reflection_packets/"` regex; extracted slug compared against `packet.org_slug`. Mismatch → fail-closed `.path_outside_org` or `.symlink_escape` sub-tag.
- **Axis (b) — span_org_slug match per RT-09 fold-in.** Every span_id in `packet.span_provenance.per_claim_span_ids` cross-checked against Logfire export's `span.attributes["org_slug"]`. Mismatch → fail-closed `.span_org_slug_mismatch` sub-tag.

M13 NOT bypassable (Law 3 structural gate).

### §4.v2.x.y.1.1.3 F-PACKET-FABRICATION (contract 3)

Aggregated counts in `packet.gate_pass_counts` + `packet.score_signals` + `packet.outcome` cross-checked against Logfire span-tree aggregates for the cycle:

- `gate_pass_counts.f_class_pass + .f_class_fail` ≤ count of F-CLASS-* span events in cycle's trace tree.
- `score_signals.judge_score` matches the most-recent Judge span's recorded score.
- `outcome.award_amount_minor_units` matches the KFR funder-outcome ledger entry's amount field iff present (Packet 2 BACKFILL only).

POST-emission + POST-load replay. Detail names the divergent count/score.

### §4.v2.x.y.1.1.4 F-PACKET-CLASS-SLOT-LEAK (contract 4)

Mirror of `F-CLASS-SLOT-ID-NON-OPAQUE` from v7.0.7 §5.1 byte-for-byte. Semantic-slot regex `r"\[SLOT_[^\]]*\]"` (broadened per v7.0.10) applied to the canonical-JSON bytes of any cloud-routable field of the packet. Always-local routing at v0.2 (per §16 v1.1 §16.v1.1.1) means this predicate should never fire in normal-path operation — firing indicates a routing bug or attack vector.

PRE-emission. Defense-in-depth alongside v7.0.7 routing.

### §4.v2.x.y.1.1.5 F-PACKET-CLASS-MISLABEL (contract 5)

`packet.classification_register_version` (128-hex SHA3-512) MUST match the operator-signed classification register's hash at cycle start. Mid-cycle relabeling attack (MINJA-shaped) closed at this predicate.

`pipeline.vault.classification.register.load_register_at_cycle_start(cycle_id, org_slug)` returns the canonical bytes hash for cross-check; the predicate compares packet field byte-for-byte against the load.

### §4.v2.x.y.1.1.6 F-PACKET-EVAL-ONLY-GROUNDED (contract 6)

`packet.grounding_signal_classes` MUST contain at least one of the six non-eval-only classes: `external_funder_outcome`, `operator_approval`, `logician_gate_outcome`, `kfr_drift_event`, `admin_risk_event`, `match_db_outcome`. Already enforced at schema layer per `ReflectionPacket.__post_init__` invariant 11; predicate body provides the Logician PRE-emission failure-code path for the same check (test-surface parity).

Sibling to F-REFLECTION-EVAL-ONLY-GROUNDED at producer-side (§4 v2.x.2).

### §4.v2.x.y.1.1.7 F-PACKET-PREMATURE-GENERALIZATION (contract 7)

For every `ProposedLesson` in `packet.lessons_proposed`:

- `frequency == 1` REQUIRES `severity == "HIGH"`.
- Operator SP0 override surface: per-grant SP0 may relax this rule with HIGH-severity admin-risk ledger entry. Predicate body reads operator SP0 ledger; if SP0 grant active for the cycle_id, fail-closed → pass with admin-risk YELLOW elevation.

Schema-layer invariant 10 enforces the same check at construction; predicate body is the runtime failure-code surface.

### §4.v2.x.y.1.1.8 F-PACKET-SPAN-PROVENANCE-MISSING (contract 8)

**RESOLVES §17 v1 §6.5 forward-reference.** Body mirrors `check_f_wpfa_span_provenance_missing` byte-for-byte:

- `_REQUIRED_CLAIM_KEYS_V0_2` closed set: `{"gate_pass_counts.f_packet_pass", "gate_pass_counts.f_packet_fail", "gate_pass_counts.f_logician_total_pass", "gate_pass_counts.f_logician_total_fail", "score_signals.judge_score", "score_signals.red_team_score", "outcome.status"}`. Every claim key MUST map to ≥1 resolvable span_id in `packet.span_provenance.per_claim_span_ids`.
- Sub-tag `.no_trace_id` (empty span_id tuple), `.trace_id_unresolvable_in_logfire` (span_id not in resolvable_span_ids set), `.claim_key_unmapped` (required key absent from mapping), `.span_id_from_different_cycle` (span_id's parent cycle_id ≠ packet.cycle_id per RT-08 fold-in).

Extended sub-tag check: for each span_id in `per_claim_span_ids`, resolve to Logfire export, extract parent cycle_id attribute, compare against `packet.cycle_id`. Mismatch fires `.span_id_from_different_cycle` (RT-08 closure).

### §4.v2.x.y.1.1.9 F-PACKET-RETRIEVAL-CORRUPTION (contract 9; Consumer C)

PRE-load defense for Consumer C (v1.x scheduled-cadence Archivist). At v0.2 first wave the predicate body is LIVE but Consumer C runtime is deferred to v1.x — the predicate fires when invoked but no v0.2 consumer invokes it. Schema is forward-compatible.

Detection:

- **High-entropy burst** — Shannon entropy of `packet.pattern_observations[i].pattern_summary` > 7.5 bits/byte over a 200-byte rolling window. Burst suggests cryptographic-payload smuggling.
- **Optimized-trigger fingerprint** — substring scan against `vault_shared/reflection_packet/known_trigger_fingerprints.signed.yaml` (operator-signed; AgentPoison + PoisonedRAG defense; updates via white-glove). Empty list at v0.2 first wave; populated as the field surfaces real triggers.

AgentPoison / PoisonedRAG class defense; v1.x may extend with adversarial-perturbation detection.

### §4.v2.x.y.1.1.10 F-PACKET-MEMORY-INJECTION (contract 10)

Three-layer detection:

- **Layer 1 — Regex.** Closed-set static regex for known MINJA shapes: `r"(?im)\bSYSTEM\s*:\s*"`, `r"(?im)<\|im_(start|end)\|>"`, `r"(?im)\[INST\]"`, `r"(?im)assistant\s*:"`, etc.
- **Layer 2 — NFKC-normalized regex.** Layer 1 patterns applied to `unicodedata.normalize("NFKC", text)`. Closes Unicode-obfuscated injection.
- **Layer 3 — Small classifier (optional at v0.2).** Logistic-regression-shaped classifier over n-gram features; default disabled at v0.2 (operator opts in via SP0). v1.x may default-enable.

Scope: `packet.pattern_observations[i].pattern_summary` + `packet.lessons_proposed[i].pattern_summary` + `packet.lessons_proposed[i].proposed_rule`. MINJA-shaped substrings fail-closed with sub-tag `.regex_match` / `.nfkc_regex_match` / `.classifier_match`.

### §4.v2.x.y.1.1.11 F-PACKET-SCHEMA-DRIFT (contract 11)

OQ-5a tolerant-reader pattern at v0.2 first wave: predicate body returns ADVISORY (GateOutcome.PASS with `detail` field carrying advisory message) when `packet.schema_version` major exceeds consumer's known max. v1.x flips to fail-closed.

`consumer_known_max` provided as call argument; current v0.2 max is `"1.1.0"` (this amendment's bump).

### §4.v2.x.y.1.1.12 F-PACKET-CADENCE-VIOLATION (contract 12)

Two-axis defense:

- **Axis A — cycle-close-marker resolution.** `packet.cycle_close_marker_span_id` MUST resolve to an existing span in Logfire export AND the span MUST have `attribute.event_type == "cycle_close_marker"` AND the span MUST belong to `cycle_id == packet.cycle_id`. Mid-cycle emission fail-closes.
- **Axis B — packet_id collision per RT-13 fold-in.** Pre-write check uses **atomic POSIX `os.open(path, O_CREAT | O_EXCL | O_WRONLY)`** per operator-resolved OQ-3 2026-05-15. The kernel enforces the collision check atomically — no pre-check-then-write race window. On EEXIST, the predicate fail-closes with sub-tag `.packet_id_collision` carrying the existing path. Mirrors §15 v1 RT-09 file-handle-chain + §17 RT-C2-05 path-traversal-class fix-in-place precedent byte-for-byte.

### §4.v2.x.y.1.1.13 F-PACKET-SIGNATURE-INVALID (contract 13)

Producer-pubkey resolution from `vault_shared/reflection_packet/producer_pubkey.signed.yaml` (NOT from packet's `emitted_by_seat` field per RT-10 fold-in; circular-trust closed). Mirrors v7.0.4-M1 §2 KFR canonical-signature-invalid byte-for-byte:

1. Load producer pubkey from white-glove-pinned signed-asset registry (Trust-On-First-Use rotation supported).
2. Compute `to_canonical_bytes(packet)` (signature fields excluded; mirrors KFR canonicalization).
3. Compute SHA3-512 over canonical bytes; compare against `packet.canonical_bytes_hash`. Mismatch → `.canonical_json_mismatch` sub-tag.
4. Verify Ed25519 signature `packet.producer_signature_ed25519` against `(producer_pubkey, canonical_bytes)`. Verification failure → `.signature_bytes_invalid` sub-tag.

M13 NOT bypassable for buyer-attested artifacts (not applicable — Reflection Packet is Tilth-internal; bypass permitted with HIGH-severity admin-risk ledger entry).

### §4.v2.x.y.1.1.14 F-PACKET-OPERATOR-SIGNATURE-MISSING (contract 14)

`packet.outcome.status != "PENDING"` REQUIRES `packet.operator_signature_ed25519 is not None`. Schema-layer invariant 16 enforces at construction; predicate body is the runtime failure-code surface.

Sub-tag `.signature_present_for_pending` per Cycle 2 RT-C2-02 fold-in: `packet.outcome.status == "PENDING"` REQUIRES `packet.operator_signature_ed25519 is None`. Defensive symmetry; schema enforces at construction.

### §4.v2.x.y.1.1.15 F-PACKET-OPERATOR-SIGNATURE-INVALID (contract 15)

Operator-pubkey resolution from v7.0.7 §6.1 classification-register operator signature mechanism (already pinned at white-glove). Same verify procedure as F-PACKET-SIGNATURE-INVALID, applied to `packet.operator_signature_ed25519` when non-None.

### §4.v2.x.y.1.1.16 F-PACKET-CYCLE-ID-UNRESOLVABLE (contract 16)

`packet.cycle_id` MUST resolve to a cycle in Logfire export. Resolution = at least one span in the cycle's trace tree carries `attribute.cycle_id == packet.cycle_id`. Fail-closed on unresolvable.

Composition with F-PACKET-CADENCE-VIOLATION: this predicate fires PRE-emission; CADENCE-VIOLATION fires PRE-write. Both must pass for emission.

### §4.v2.x.y.1.1.17 F-PACKET-OUTCOME-EVIDENCE-MISSING (contract 17)

`packet.outcome.status != "PENDING"` REQUIRES `packet.outcome.outcome_evidence_span_ids` non-empty AND every span_id resolvable in Logfire export. Schema-layer invariant covers the non-empty case; predicate body adds the resolvability check + cross-cycle check (span_id's parent cycle_id matches packet.cycle_id; mismatch → sub-tag `.evidence_span_from_different_cycle` per RT-08 mirror).

### §4.v2.x.y.1.1.18 F-PACKET-PRODUCER-UNAUTHORIZED (contract 18)

Closed-set membership check. v0.2 producer registry = `frozenset({"archivist.reflection_submode"})`. Schema-layer invariant 7 enforces at construction; predicate body is the runtime failure-code surface.

Forward-extension marker: if v1.x adds new producers (Cultivator Stage 2 et al.), the registry extends additively here.

## §4.v2.x.y.1.2 META-gate strengthening — F-PACKET-COVERAGE-INCOMPLETE (contract 7 RT-01 fold-in)

`f_packet_coverage_incomplete.py::check_f_packet_coverage_incomplete()` body strengthens to dry-run-probe semantic per §16 v1.1 §16.v1.1.7:

**`_SENTINEL_PROBES_V0_2`** Final-constant maps each of 18 BINDING codes to a minimal sentinel `(args, kwargs)` payload that exercises the predicate's signature without triggering substantive content. Probe execution catches `NotImplementedError`; if raised, the predicate is reported as un-realized in `CoverageIncompleteResult.missing_bodies`.

Sentinel payloads:

- `F-PACKET-INSTANCE-LEAK`: `({"pattern_summary": "ok", "proposed_rule": "ok"},)` — passes if body reaches the "no instance leak detected" return.
- `F-PACKET-CROSS-ORG-LEAK`: `({"target_write_path": "orgs/x/vault/operational/reflection_packets/p.json", "packet_org_slug": "x", "span_provenance_org_slugs": frozenset({"x"})},)` — passes on match.
- ... (per-predicate sentinel payloads listed in `_SENTINEL_PROBES_V0_2` source; AST-lint regression `R-PACKET-SENTINEL-COVERAGE` verifies 18-code completeness)

Probe runs at PRE-cycle once per cycle invocation. Performance budget: < 50ms cold; < 5ms warm. Tested at `tests/logician/gates/test_f_packet_coverage_incomplete_meta_gate.py::test_dry_run_probe_perf_budget`.

**Any v0.2 first wave deployment with a partially-flipped registry (e.g., 17 of 18 LIVE) fail-closes at META-gate PRE-cycle.** Names the un-realized code(s) in `CoverageIncompleteResult.missing_bodies` for operator triage.

## §4.v2.x.y.1.3 AST-lint rule extensions

Two new AST-lint rules ship with this amendment:

1. **`R-PACKET-NO-NOTIMPLEMENTEDERROR`** — bans `raise NotImplementedError(...)` in any `pipeline/logician/gates/f_packet_*.py` module EXCEPT `f_packet_coverage_incomplete.py` (which uses sentinel-probe catch semantic, not raise). Module: `pipeline/linting/r_packet_no_notimplementederror.py`. Defense against partial-flip regressions during code review.
2. **`R-PACKET-SENTINEL-COVERAGE`** — verifies `_SENTINEL_PROBES_V0_2` in `f_packet_coverage_incomplete.py` covers all 18 BINDING codes from `_BINDING_F_PACKET_CODES`. Module: `pipeline/linting/r_packet_sentinel_coverage.py`. Prevents META-gate drift from BINDING-codes registry.

## §4.v2.x.y.1.4 Test surface (v0.2 first wave scope)

- **18 LIVE-body test files** `tests/logician/gates/test_f_packet_<code>.py`: each ≥ 6 tests covering happy path + fail-closed cases + sub-tag coverage + grammar boundary cases + cross-family-import regression.
- **META-gate test file** `test_f_packet_coverage_incomplete_meta_gate.py`: dry-run probe semantic + 18-code coverage + perf budget + NotImplementedError catch + LIVE/PARTIAL-FLIP scenarios.
- **AST-lint regression**: `scripts/run_lint.sh pipeline` exits 0 with R-PACKET-NO-NOTIMPLEMENTEDERROR + R-PACKET-SENTINEL-COVERAGE active.
- **Schema-layer regression** `tests/vault/sub_kinds/test_reflection_packets.py` already LIVE per §16 v1 — no change at this amendment.

## §4.v2.x.y.1.5 Cycle 1 + Cycle 2 disposition log

See `pipeline/validation/reflection_packet_v0_2_first_wave_thesis_2026-05-15/` for the actual Cycle 1 + Cycle 2 audit-trail; this amendment inherits the same dispositions as the four sibling amendments per compound-paired-commit discipline.

## §4.v2.x.y.1.6 v1.x amendment-realization checklist (forward-binding contracts)

1. **Consumer B (KFR cross-check)** runtime wiring at v1.x — F-LOGICIAN-FACT-DRIFT composition over BACKFILL packets.
2. **Consumer C (Archivist scheduled-cadence)** runtime wiring at v1.x — full PRE-load gate composition including F-PACKET-RETRIEVAL-CORRUPTION + F-PACKET-MEMORY-INJECTION (both LIVE at v0.2 but no consumer invokes).
3. **Cedar full enforcement** of remaining 18 BINDING rules at v1.x (OQ-2 minimal at v0.2 keeps only META-gate enforcing).
4. **Tolerant-reader flip** for F-PACKET-SCHEMA-DRIFT (ADVISORY at v0.2 → fail-closed at major-version drift at v1.x per OQ-5a).
5. **Heavy-Reflection swap analog** (optional, operator-demand-driven; not promised; v1.x scope marker).
6. **NER upgrade** for F-PACKET-INSTANCE-LEAK Layer 2 (regex+blocklist → spaCy or local NER model at v1.x; SP0 opt-in surface).

## §4.v2.x.y.1.7 Audit trail

See `pipeline/validation/reflection_packet_v0_2_first_wave_thesis_2026-05-15/`.

---

**Filed:** 2026-05-15. LOCKED via L-005 strict two-cycle Thesis with FULL LIVE CROSS-FAMILY rigor. Compound paired-commit sibling 3/5.
