# BUILD-SPEC — Hardware & Golden Image (node: `hardware-golden-image`)

- Craft node: `hardware-golden-image` (`CTX-HGI-ROOT`)
- Source contract: `docs/golden-quill-task-role-breakdown-handoff.md` §1 (Workstream A — Hardware & Physical Node)
- Refine inputs: `docs/features/hardware-golden-image/.craft/ledger.yml`; `.../refinement-runs/2026-06-12-craft-pipeline-hydration/{RESEARCH-RESULT.md, REFINE-DISPATCH.json, INVOKE-FIRST-ARTIFACTS.md}`
- Canon: `router.yaml` (lines 17–48, signing/verify trust mechanism); `CLAUDE.md` Hardware section + Product Naming Chain + Sovereignty Promise; architecture v7.0.7 §6.1
- Status: implementation-ready spec for owning engineers (Vlad — backend; Koichi — AI/QA-field). Planning artifact only; no runtime executed.

## Guardrails (binding on every section)

- **Substrate LOCKED.** Pydantic AI + Logfire + curated Python parsing utils + Ollama/vLLM + DSPy/GEPA + Logician (Cedar). Frozen at Golden Image build, no marketplace access from the appliance (ADR-001, v7.0.3). Do not propose alternatives.
- **Law 3.** Evidence is Golden-Quill-project canon only. No `orgs/` data is read, embedded, or referenced by any procedure below. Per-unit verification operates on the image and the appliance, never on client vault contents.
- **No fabricated values.** Numeric burn-in thresholds and SKU datasheet figures are marked `[OPERATOR-INPUT]` / `[EXTERNAL-DEFERRED]`. This spec authors the *shape*; it does not invent the *numbers*.
- **Sovereignty Promise.** Customer owns the machine, the data, and the keys. Every backup/recovery/export procedure must keep custody local-by-default and exportable on customer terms.

## X-ray of the hardware → image chain (orientation)

```
[REFERENCE-SPEC]  → certified workstation baseline (128GB floor, approved SKUs)
       │
[PROCUREMENT]     → unit acquired (Josh; out of this node's authoring scope)
       │
[BURN-IN]         → per-unit acceptance: thermal / memory / storage / inference
       │
[OS BASELINE]     → hardened config, disk encryption, accounts, drivers, network
       │
[GOLDEN IMAGE]  ◄── assembled by tilth-runtime-build (signed installable artifact)
       │            INTERFACE: GAP-TRB-GOLDEN-IMAGE-HANDOFF
[IMAGE-VERIFY]    → repeatable write + per-unit verification (Ed25519 + boot-manifest)
       │
[BACKUP/RECOVERY] → local backup, customer-owned export, recovery posture
       │
[NODE ON DESK]    → white-glove delivery
```

The four gaps below cover REFERENCE-SPEC, BURN-IN, IMAGE-VERIFY, BACKUP/RECOVERY. PROCUREMENT and PERIPHERALS are Josh-owned and out of this node's authoring lane.

---

## GAP-HGI-IMAGE-VERIFY — repeatable write + per-unit verification

- **Owner:** Vlad (backend-engineer) · **Severity:** block · **Verdict:** refine-solvable (authorable from local canon)

### Define — what to build
A repeatable, scriptable procedure that writes the signed Golden Image onto a fresh unit and produces **per-unit verification evidence** that the written image is byte-faithful, signature-valid, and boot-manifest-valid. The signing/verification *trust mechanism* already exists in canon (`router.yaml` 17–48: publisher Ed25519 signing, white-glove-pinned publisher pubkey, `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` fail-closed, boot-time Golden Image manifest verification). What is missing is the **per-unit write+verify procedure that consumes it**.

### Design — components
1. **Image manifest** (consumed, produced by tilth-runtime-build): `golden_image_manifest.json` carrying image version, per-file SHA-256 digest set, total image digest, and the publisher Ed25519 signature over the manifest.
2. **Write step:** deterministic flash/clone of the signed image to the unit's encrypted target disk.
3. **Pre-write verification:** verify manifest Ed25519 signature against the white-glove-pinned publisher public key. Fail-closed on mismatch (reuse `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` discipline — admin-risk ledger HIGH on failure).
4. **Post-write verification:** re-hash the written volume's files, compare to manifest digest set; confirm total-image digest.
5. **Boot-time verification:** first boot runs the boot-manifest check (router.yaml line 48) — confirms heavy-Judge model and all frozen-substrate artifacts present and unmodified (no network fetch; ties to `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD` pre-load discipline).
6. **Per-unit verification receipt:** typed record `{ unit_serial, image_version, manifest_signature_status, prewrite_verify, postwrite_digest_match, boot_manifest_status, operator, timestamp, result: PASS|FAIL }`. Saved on BOTH success and failure (Autonomy Rule 1).

### Acceptance criteria
- AC1: Running the procedure twice on two units of the same SKU yields two receipts with identical `image_version` and matching digest sets — repeatability proven.
- AC2: A tampered/unsigned manifest fails-closed at pre-write; no write proceeds; HIGH admin-risk ledger entry recorded.
- AC3: A single corrupted byte in the written volume is caught at post-write digest comparison → receipt `FAIL`.
- AC4: Boot-manifest check passes on a clean write and fails-closed if any frozen-substrate artifact is missing/modified.
- AC5: Every run produces a receipt regardless of outcome (no silent failures).

### Concrete first steps
1. Author `golden_image_manifest.json` schema as a Pydantic model (digest set + Ed25519 signature field); coordinate field names with tilth-runtime-build's assembly output (see Dependencies).
2. Write `scripts/image_verify.py` (or `.sh` wrapping Python) implementing pre-write signature verify → write → post-write re-hash → receipt emit. Reuse the existing pinned-pubkey verification path from the router-template signing code.
3. Define the per-unit receipt as a Pydantic model; pin its on-disk path (e.g. `deploy/unit_receipts/<unit_serial>.json`).
4. Toy-game falsification (per Refine seed): take a known-good image, flip one byte, confirm the procedure emits `FAIL` and refuses boot. This is the low-cost acceptance test the Invoke-first direction asks for before install work is routable.

### Dependencies / handoffs
- **Golden Image assembly interface → tilth-runtime-build** (`GAP-TRB-GOLDEN-IMAGE-HANDOFF`): tilth-runtime-build produces the signed, versioned installable artifact + its manifest; this node consumes them. **Interface contract to lock jointly:** manifest filename, digest algorithm (SHA-256), signature scheme (Ed25519 over manifest), version field format, and publisher-pubkey pinning ceremony. Neither side proceeds to LOCK until both agree the manifest schema byte-for-byte.
- Pinned publisher public key provisioned at white-glove (TOFU, audited rotation per router.yaml 22–23).

---

## GAP-HGI-BACKUP-RECOVERY — local backup, customer-owned export, recovery posture

- **Owner:** Vlad (backend-engineer) · **Severity:** block · **Verdict:** refine-solvable (authorable from local canon)

### Define — what to build
A tested procedure for (a) **local backup** of the appliance's mutable state, (b) **customer-owned export** of that state in a portable form, and (c) **recovery** of a node from the Golden Image + a backup. Must honor the Sovereignty Promise: if FIT Farms / any spin-off vanished, the customer still has their machine, data, keys, and grants — nothing held hostage.

### Design — components
1. **Backup scope definition.** Separate the two layers: (i) the **immutable Golden Image** (re-derivable from the signed artifact — does NOT need backing up, only re-writing) and (ii) the **mutable customer state** = the vault (org PROJECT_CONTEXT, classification registers, drafts, cycle receipts, audit log, keys). Only (ii) is backup-bearing.
2. **Local backup:** scheduled encrypted snapshot of the mutable-state volume to a customer-attached/local target. Disk encryption keys remain customer-held.
3. **Customer-owned export:** a one-command export producing a portable, decryptable-by-the-customer archive of their vault + a copy of their keys + a manifest of what's inside. Plain, open formats (no proprietary container that locks the customer out).
4. **Recovery posture:** documented path = re-write Golden Image (GAP-HGI-IMAGE-VERIFY) → restore mutable state from latest backup/export → re-verify. Recovery must NOT require any FIT Farms / publisher-side service to be reachable.
5. **Receipts:** backup receipt + recovery receipt (saved on success AND failure).

### Acceptance criteria
- AC1 (Sovereignty): a fully exported archive can be opened and read on a machine with no Golden-Quill software, using customer-held keys only. No call-home, no vendor dependency.
- AC2 (Round-trip): node wiped → Golden Image re-written → state restored from backup → vault contents and audit log are byte-identical to pre-wipe (verified by digest).
- AC3 (Custody): backup and export artifacts are encrypted with customer-held keys; no key material leaves the node to any FIT Farms/publisher endpoint.
- AC4 (Law 3): backup/export of one node never co-mingles another org's vault; export manifest is single-org scoped.
- AC5: every backup and recovery run emits a receipt regardless of outcome.

### Concrete first steps
1. Enumerate the mutable-state file set precisely (vault subtree, classification registers, keys, audit log, cycle receipts) vs. the immutable image set. Author this split as a manifest.
2. Write `scripts/backup_export.py` — encrypted snapshot + portable export with an inside-manifest; choose an open archive + open encryption format.
3. Write `scripts/recover.py` — orchestrates image re-write (calls GAP-HGI-IMAGE-VERIFY procedure) then state restore + digest re-verify.
4. Toy-game falsification: full wipe-and-recover on a scratch unit; assert AC2 round-trip digest match; assert AC1 by opening the export on a clean machine.

### Dependencies / handoffs
- Consumes the GAP-HGI-IMAGE-VERIFY write procedure as the image-restore half of recovery.
- The mutable-state file set must agree with the vault layout owned by tilth-runtime-build (vault/classification paths). Cross-check, do not duplicate, those path definitions.

---

## GAP-HGI-BURN-IN — burn-in & acceptance test procedure (per unit)

- **Owner:** Koichi (qa-field-tech; BUILD → PER-NODE → Field Tech) · **Severity:** flag · **Verdict:** operator-input (procedure refine-solvable; numeric thresholds external-deferred)

### Define — what to build
A per-unit burn-in & acceptance **procedure** across four axes — thermal, memory, storage, inference-benchmark — that emits a pass/fail acceptance receipt before a unit proceeds to OS baseline / imaging. This spec authors the procedure and the **metrics to capture**; the numeric pass/fail **thresholds are `[OPERATOR-INPUT / EXTERNAL-DEFERRED]`** pending bounded external request **EXT-HGI-2** (burn-in / thermal-soak / inference-benchmark practice) — approve or keep deferred.

### Design — the four axes (capture-shape; thresholds deferred)
| Axis | Procedure step | Metrics to capture | Pass/fail threshold |
| --- | --- | --- | --- |
| Thermal | Sustained-load thermal soak for a fixed duration | peak core/package temp, throttle events, ambient, fan curve | `[OPERATOR-INPUT]` max temp / zero-throttle window |
| Memory | Full-coverage memory test pass(es) | errors detected, addressable RAM confirmed vs 128GB floor | `[OPERATOR-INPUT]` zero-error pass count |
| Storage | SMART read + endurance/IO sample | SMART health attrs, reallocated sectors, read/write throughput | `[OPERATOR-INPUT]` SMART-clean + min throughput |
| Inference benchmark | Run a fixed local-model prompt set on the frozen substrate (Ollama/vLLM) | tokens/sec, time-to-first-token, completion correctness on a canned set | `[OPERATOR-INPUT]` min tok/s, max TTFT |

### Acceptance criteria
- AC1: procedure runs unattended end-to-end on one unit and emits one acceptance receipt `{ unit_serial, sku, thermal{...}, memory{...}, storage{...}, inference{...}, result, operator, timestamp }`.
- AC2: each axis captures its named metrics even when that axis fails (no early-abort that drops later-axis data; save-state-always).
- AC3: result computed mechanically once thresholds are supplied — the threshold table is a config input, not hardcoded.
- AC4: receipt is the gate artifact for proceeding to imaging; a `FAIL` blocks the unit.
- AC5: PER-NODE repeatable from a checklist by a Field Tech who didn't author it (ties to Workstream C internal-deployment-test discipline).

### Concrete first steps
1. Author `burn_in.py` orchestrating the four axes and emitting the acceptance receipt; thresholds read from `burn_in_thresholds.yaml` (values left `[OPERATOR-INPUT]`).
2. Select the canned inference prompt set (fixed, Golden-Quill-project content only — Law 3) and a correctness oracle for it.
3. Write the Field-Tech checklist wrapper (human-runnable, references the script).
4. Surface EXT-HGI-2 go/no-go to Josh: without it, the threshold cells stay `[OPERATOR-INPUT]` and acceptance cannot compute a final PASS.

### Dependencies / handoffs
- Inference-benchmark axis depends on the frozen substrate being present — runs AFTER a verified image write OR against a reference build. Sequence note: full per-unit burn-in incl. inference benchmark sits post-image; bare-hardware axes (thermal/memory/storage) can run pre-image.
- Threshold values gated on EXT-HGI-2 (operator decision).

---

## GAP-HGI-REFERENCE-SPEC — reference-workstation spec template + acceptance fields

- **Owner:** Koichi (ai-engineer) · **Severity:** flag · **Verdict:** operator-input (spec shape refine-solvable; SKU values external-deferred)

### Define — what to build
A **testable reference-workstation specification template** plus an **approved-alternative acceptance rule**, turning the named SKUs (currently prose in `CLAUDE.md`) into a spec a unit can be checked against. 128GB is the canonical floor (32/64GB references are stale). Reference SKUs: **Apple M3 Ultra Mac Studio**, **AMD GX-10 class**, **NVIDIA Spark (DGX Spark / ASUS Ascent GX10)**. This spec authors the **shape + acceptance fields**; exact SKU datasheet **values are `[OPERATOR-INPUT / EXTERNAL-DEFERRED]`** pending bounded external request **EXT-HGI-1** (current reference-SKU spec sheets — public vendor specs only, no protected context).

### Design — spec template fields (shape; values deferred)
```yaml
reference_workstation_spec:
  sku_name:            # e.g. "Apple M3 Ultra Mac Studio"   [OPERATOR-INPUT]
  status:              # certified | approved-alternative | candidate
  unified_memory_gb:   # MUST be >= 128 (canonical floor)    [OPERATOR-INPUT exact]
  compute:             # chip/accelerator id                 [EXTERNAL-DEFERRED]
  storage_min_gb:      #                                      [OPERATOR-INPUT]
  thermal_envelope:    # sustained-load rating               [EXTERNAL-DEFERRED]
  ports_peripheral_fit:#                                      [EXTERNAL-DEFERRED]
  availability:        # current procurement availability    [EXTERNAL-DEFERRED]
  substrate_compat:    # runs frozen substrate (Ollama/vLLM) — bool
acceptance_fields:
  meets_memory_floor:  # unified_memory_gb >= 128
  runs_substrate:      # substrate_compat == true
  passes_burn_in:      # links to GAP-HGI-BURN-IN receipt
approved_alternative_rule:
  # a non-certified SKU is an APPROVED ALTERNATIVE iff:
  #  (1) meets_memory_floor, AND
  #  (2) runs_substrate, AND
  #  (3) passes_burn_in against the same threshold table,
  #  AND (4) operator sign-off recorded.
```

### Acceptance criteria
- AC1: the template instantiates cleanly for each of the three named SKUs (cells filled `[OPERATOR-INPUT]`/`[EXTERNAL-DEFERRED]` until EXT-HGI-1 lands — never fabricated).
- AC2: `meets_memory_floor` mechanically rejects any spec with `unified_memory_gb < 128`.
- AC3: the approved-alternative rule is evaluable: a candidate SKU either satisfies all four conditions (→ approved) or not (→ rejected), with operator sign-off as the final gate.
- AC4: spec is the input the burn-in threshold table and procurement key off — one source of truth for "what counts as a Golden Quill unit."

### Concrete first steps
1. Write `reference_workstation_spec.yaml` (template + three SKU stubs with deferred cells) and a tiny validator asserting AC2/AC3 against the closed-set fields.
2. Encode the approved-alternative rule as a checkable function (4 conditions + sign-off).
3. Surface EXT-HGI-1 go/no-go to Josh: without it, the datasheet cells stay deferred; the SHAPE and the floor/rule logic are complete now regardless.

### Dependencies / handoffs
- Feeds GAP-HGI-BURN-IN (per-SKU threshold table) and procurement (Josh, out of authoring lane).
- SKU values gated on EXT-HGI-1 (operator decision).

---

## Residue carried from research (surface to Josh)

- **R1:** IMAGE-VERIFY and BACKUP-RECOVERY are `block` severity but **locally authorable** — the block means "procedure not yet written," not "evidence missing." Both are refine-solvable now; do not misread the block as needing external input.
- **R2:** The source workbook's "Sanitized" posture (§1, B) is **DEPRECATED** in current canon (CLAUDE.md v7.0.10 three-posture model). Not this node's lane to fix — flagged only; do not propagate "Sanitized" into any procedure here.
- **R3:** `router.yaml` confirms the signing/verify trust mechanism but holds **no** hardware SKU or burn-in numbers — confirming EXT-HGI-1/EXT-HGI-2 are genuine local gaps, not search-laziness.

## Per-gap verdict summary

| Gap | Owner | Verdict | What the owner must do |
| --- | --- | --- | --- |
| GAP-HGI-IMAGE-VERIFY | Vlad | refine-solvable | Build per-unit write+verify procedure consuming the existing Ed25519 signing chain; lock manifest schema with tilth-runtime-build; toy-game the byte-flip failure case. |
| GAP-HGI-BACKUP-RECOVERY | Vlad | refine-solvable | Build local-backup + customer-owned-export + recovery procedure honoring Sovereignty Promise; prove wipe→recover round-trip digest match. |
| GAP-HGI-BURN-IN | Koichi | operator-input | Author the four-axis procedure + receipt now; thresholds stay `[OPERATOR-INPUT]` pending EXT-HGI-2 go/no-go from Josh. |
| GAP-HGI-REFERENCE-SPEC | Koichi | operator-input | Author the spec template + 128GB-floor + approved-alternative rule now; SKU datasheet values stay `[EXTERNAL-DEFERRED]` pending EXT-HGI-1 go/no-go from Josh. |
