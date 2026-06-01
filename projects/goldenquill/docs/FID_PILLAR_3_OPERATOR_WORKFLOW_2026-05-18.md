# FID Pillar-3 Operator Workflow

**Status:** Canonical operator-facing workflow doc for the Pillar-3 structured-artifact phase (FID Phase 1, weeks 4-5).
**Branch where infrastructure lands:** `fid-pillar-3-infrastructure-pre-stage-2026-05-18`.
**Companion artifacts:**
- Family-level MANIFESTs: `pipeline/funder_intelligence/funders/MANIFEST.md` + `pipeline/funder_intelligence/programs/MANIFEST.md`.
- CLI: `pipeline/cli/tilth_pillar3_artifact.py`.
- Signing helper: `pipeline/funder_intelligence/_methodology/sign_artifact.py`.
- Quality spec: `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §3 (per-family YAML schemas).
- Planning authority: `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §9.1.

---

## §0 — Prerequisites: signed Pillar-1 charter AND signed Pillar-2 corpus

Pillar-3 work for any of the 14 Phase-1 artifacts is **structurally blocked** until *both* of these are present for that artifact:

1. `pipeline/funder_intelligence/pillar_1_charters/<artifact_id>_charter_v1_SIGNED.md` (Pillar-1 sign ceremony, PR #33 + #40)
2. `pipeline/funder_intelligence/pillar_2_corpus/<artifact_id>/_signed.yaml` (Pillar-2 sign ceremony, PR #39)

The CLI fails closed at `init` with `F-FID-ARTIFACT-UNSIGNED-CHARTER` or `F-FID-ARTIFACT-UNSIGNED-CORPUS` until the corresponding signed file is on disk.

---

## §1 — Per-artifact workflow

### Step 1 — `init`

```bash
.venv/bin/python -m pipeline.cli.tilth_pillar3_artifact init \
    --artifact-id USDA-RD-RBDG-FY26
```

What it does:

- Confirms both dependency files exist (`_charter_v1_SIGNED.md` + corpus `_signed.yaml`).
- Determines family from the artifact_id (funder or program).
- Writes a YAML stub at the family directory (`funders/<id>.yaml` or `programs/<id>.yaml`) with the §3.1 common header, the §2 adversarial blocks (placeholders), and the family-specific body scaffolding per §3.2 or §3.3.
- Stamps `lifecycle_status: stub`.

### Step 2 — operator authoring (out-of-band LLM extraction)

This step is **fully operator-side** — Tilth's CLI doesn't drive extraction. The operator runs extraction sessions via openclaw bridge or other Local-Only-Sovereign tooling, using the signed Pillar-2 corpus as input, and hand-curates the structured-fact output into the artifact YAML body. The CLI's job is to scaffold and sign; the LLM extraction lives outside its boundary.

Authoring rules (the §2 adversarial fields):

- **`runtime_consumer:`** — must name, per seat, which fields the seat reads at what stage and what decision changes. At least one seat must be active (not `not_applicable`).
- **`artifact_must_not_contain:`** — keep the three canonical defaults verbatim; add artifact-specific exclusions as discovered.
- **`strength_test:`** — keep the three canonical questions; ensure the artifact body answers all three concretely (cross-reference the answers in `runtime_consumer.decision_changed` so the §A audit can verify alignment).

Authoring rules (corpus-traceability):

- Every substantive claim cites `corpus_ref` pointing at a `pillar_2_corpus/<id>/_signed.yaml`-registered file.
- No claim without a `corpus_ref`. F-FID-FACT-ORPHAN gate (validate subcommand, follow-up PR) will enforce this.

When body content is operator-complete, flip `lifecycle_status: draft` and commit.

### Step 3 — `status` (anytime)

```bash
# Single artifact
.venv/bin/python -m pipeline.cli.tilth_pillar3_artifact status \
    --artifact-id USDA-RD-RBDG-FY26

# Full 14-roster roll-up
.venv/bin/python -m pipeline.cli.tilth_pillar3_artifact status
```

Surfaces: family, dependency state (charter signed `C` / corpus signed `K` / neither `-`), and lifecycle.

### Step 4 — `sign` (operator Ed25519 ceremony)

```bash
# Dry-run: get canonical bytes + SHA3-512 hash
.venv/bin/python -m pipeline.cli.tilth_pillar3_artifact sign \
    --artifact-id USDA-RD-RBDG-FY26 \
    --dry-run

# Operator signs canonical bytes offline against FID publisher Ed25519 key.

# Apply signature
.venv/bin/python -m pipeline.cli.tilth_pillar3_artifact sign \
    --artifact-id USDA-RD-RBDG-FY26 \
    --signer-pubkey-fingerprint <hex> \
    --signature-hex <hex>
```

Behind the scenes (`sign_artifact.py`):

- Strips the four signature fields to placeholders → canonicalize YAML body (sort_keys=True, allow_unicode=True).
- SHA3-512 → `canonical_bytes_sha3_512`.
- Verifies operator signature against pinned FID publisher pubkey at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`.
- Writes signature back into the YAML; flips `lifecycle_status: draft → audited`.
- Regenerates the family MANIFEST row with the hash prefix.

Idempotent guard: re-running `sign` against a `lifecycle_status >= "audited"` artifact exits 4.

---

## §2 — What is NOT in this CLI (deferred)

* **`validate` subcommand** — full Pydantic-schema enforcement against §3.2 / §3.3 / §3.4 structures. Deferred until the operator confirms schema details after the first Pillar-2 corpus is signed. Until validate ships, schema discipline is honor-system (operator follows the §3 spec; spot-check audit by Codex external-validity reviewer).
* **LLM extraction driver** — operator runs extraction sessions out-of-band via openclaw bridge. The CLI does not invoke any LLM.
* **F-FID-* runtime gates** — the structural gates that fire when Tilth seats read artifact YAML at grant-cycle time. Those land with the §4 v2.x.y Logician follow-on amendment (see planning doc §10.2).

---

## §3 — Family taxonomy + per-artifact schemas

### Funder artifact (§3.2)

8 artifacts: USDA-RD, USDA-NIFA, USDA-AMS, PA-DEPT-AG, PA-DCED, HEINZ-FOUNDATION, NCBA-CLUSA, RICHARD-KING-MELLON-FOUNDATION.

Key body fields (operator authors from signed Pillar-2 corpus):

- `mission_framing` — one-paragraph plain-English summary + corpus_ref.
- `program_roster` — pointers to this funder's program artifacts (program_id + artifact_path).
- `compliance_cascade_defaults` — cascades that fire on this funder's awards (e.g., `2-CFR-200-UG`, `DAVIS-BACON-PREVAILING-WAGE` conditional).
- `funder_dialect` — register + load_bearing_terms + dialect_notes (Tier-2; Scribe reads).
- `geographic_eligibility` — Scout DISCOVER filter.
- `historical_award_patterns_aggregate` — Tier-1 public; Scout reads.
- `known_failure_modes_at_funder_level` — Red Team probe seeds.

### Program artifact (§3.3)

6 artifacts: USDA-RD-RBDG-FY26 (anchor), USDA-NIFA-SARE-NE-FY26, USDA-RD-CFP-FY26, USDA-RD-RCDG-FY26, USDA-AMS-VAPG-FY26 (FY26 cycle closed; preserved for FY27 pre-planning), PA-DEPT-AG-AGINNOV-FY26.

This is the densest artifact type — it carries machine-parseable structures that Logician, Judge, and Scribe all read at runtime:

- `eligibility_gates` — Logician PRE-gate predicates.
- `disqualifiers` — special class with `severity: P0` + `on_fail: REJECT_NO_DRAFT`.
- `match_requirements` — cash/in-kind rules + authenticity rules + documentation timing.
- `scoring_rubric` — total points + weighted criteria + sub-criteria; Judge reads.
- `review_stages` — screen / score / consensus (D3 enum vocab once locked).
- `required_application_elements` — narrative + SF-424 + match letter + section anchors.
- `scribe_section_requirements` — per-section drafting decisions with corpus refs.
- `judge_scoring_map` — Judge's per-criterion question + 0-5 score bands.
- `logician_gates` — PRE/POST predicates owned by this program.
- `red_team_probes` — per-probe question + score-impact + corpus ref.
- `post_award_obligations` — reporting cadence + Data Collector v0.2 input fields.

### Compliance cascade (§3.4)

Not in the Phase-1 Pillar-3 roster — cascade artifacts (`2-CFR-200-UG`, `DAVIS-BACON-PREVAILING-WAGE`, `NEPA-24-CFR-58`) land via the cross-cutting PRP trio per PR #20.

---

## §4 — Sign-off checklist per artifact

- [ ] Pillar-1 charter at `_charter_v1_SIGNED.md` (verify via `tilth pillar3 artifact status --artifact-id <id>`).
- [ ] Pillar-2 corpus at `pillar_2_corpus/<id>/_signed.yaml`.
- [ ] `init` ran cleanly; YAML stub at `funders/<id>.yaml` or `programs/<id>.yaml`.
- [ ] Operator authored body content from signed corpus; every claim has `corpus_ref`.
- [ ] `runtime_consumer:` populated for all five seats (or `not_applicable` documented); at least one seat active.
- [ ] `strength_test:` answered concretely in artifact body.
- [ ] Flipped `lifecycle_status: stub → draft`.
- [ ] `sign --dry-run` produced canonical bytes; operator Ed25519-signed those bytes offline.
- [ ] `sign --signature-hex ... --signer-pubkey-fingerprint ...` exited 0; lifecycle now `audited`.
- [ ] Family MANIFEST row updated with hash prefix.

When all 14 artifacts reach `audited`, FID Phase-1 closes. Weeks 6-7 = field-test calibration (a fresh cycle runs through the audited artifacts; Judge/Red Team scores compared; drift flagged for lifecycle promotion to `field_tested`).

---

## §5 — CC-007 / Law-5 boundary

The CLI uses pathlib + yaml only. It does not import `urllib`, `requests`, `httpx`, `aiohttp`, or any other HTTP library. AST-lint `R-NO-DIRECT-PROVIDER-HTTP` covers this. The signing helper uses `cryptography.hazmat.primitives.asymmetric.ed25519` — no provider calls.

LLM extraction (operator-side, out-of-band) runs under Local-Only-Sovereign posture per architecture v7.0.10 §1.
