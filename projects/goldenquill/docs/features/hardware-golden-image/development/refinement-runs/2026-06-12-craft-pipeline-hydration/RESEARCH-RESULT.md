# Research Result - Hardware and Golden Image

- Run ID: `2026-06-12-craft-pipeline-hydration`
- Dispatch: `gq-research-strategy-hardware-golden-image-2026-06-12`
- Execution mode: LOCAL-FIRST ONLY (external research permission-gated, NOT authorized this run)
- Role lenses exercised: local-evidence-reviewer, external-boundary-reviewer, claim-validation-reviewer
- Overall verdict: **PASS (local-first)** with two named external gaps DEFERRED for Josh's approval
- Owner boundary: planning evidence only; no canonical store or lifecycle artifact mutated; no `.craft/ledger.yml` edit

## Node

- Craft node: `hardware-golden-image` (`CTX-HGI-ROOT`)
- Title: Hardware and Golden Image
- Research lane: hardware and Golden Image research
- Owns: workbook Workstream A (Hardware & Physical Node) plus Golden Image packaging interfaces

## Core Research Question

What proof is needed for one approved hardware baseline and a repeatable signed Golden Image process?

## Findings (each with source path)

### F1 — The four active gaps and their owners are already named and severity-tiered in the node ledger.
- `GAP-HGI-REFERENCE-SPEC` (flag, ai-engineer), `GAP-HGI-BURN-IN` (flag, qa-field-tech), `GAP-HGI-IMAGE-VERIFY` (block, backend-engineer), `GAP-HGI-BACKUP-RECOVERY` (block, backend-engineer).
- Source: `docs/features/hardware-golden-image/.craft/ledger.yml` (gaps[0-3]).

### F2 — The eight Workstream-A tasks that constitute "node on the desk" are enumerated in the source contract, with role/effort-type binding.
- Reference workstation cert + one approved alternative (BUILD, AI Eng/Koichi); procurement (BUILD+PER-NODE, Josh); burn-in & acceptance per unit — thermal/memory/storage/inference benchmark (BUILD→PER-NODE, AI Eng→Field Tech); OS baseline — hardened config, disk encryption, accounts, drivers, network (BUILD, Backend/Vlad); imaging/cloning Golden Image with verification (BUILD→PER-NODE, Backend→Field Tech); peripherals/branded kit (BUILD+PER-NODE, Josh); backup & export posture — local backup, customer-owned export, recovery (BUILD, Backend/Vlad); update-and-signing mechanism (BUILD, Backend/Vlad).
- Source: `docs/golden-quill-task-role-breakdown-handoff.md` (§1 Node on the Desk, Workstream A rows).

### F3 — Golden Image assembly is a cross-node interface: "everything packaged as one installable, versioned, signed artifact."
- This binds the hardware node to Workstream B (software/Tilth build). The signed-artifact requirement is the proof anchor for `GAP-HGI-IMAGE-VERIFY`.
- Source: `docs/golden-quill-task-role-breakdown-handoff.md` (§1, Workstream B "Golden Image assembly" row, Vlad + Koichi).

### F4 — Golden Image manifest verification and router-template signing are already governed primitives in project config.
- `router.yaml` lines 17-23 (publisher Ed25519 signing / white-glove-pinned pubkey / `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` fail-closed / TOFU key rotation) and line 48 ("Golden Image manifest verification"). This means the *signing/verification trust mechanism* already exists in canon; what the node lacks is the per-unit *write+verify procedure* that consumes it.
- Source: `router.yaml` (lines 17-23, 48); cross-ref `CLAUDE.md` (v7.0.7 §6.1 router-template signing; boot-time manifest verification; F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD pre-load discipline).

### F5 — Canonical hardware reference SKUs and the 128 GB floor exist in project doctrine but NOT as a testable spec.
- M3 Ultra Mac Studio, AMD GX-10 class, NVIDIA Spark (DGX Spark / ASUS Ascent GX10); 128 GB canonical floor (earlier 32/64 GB references stale). Dev node M1 Mac Mini 8 GB; production 128 GB+.
- This is the load-bearing input for `GAP-HGI-REFERENCE-SPEC`: the SKUs are named in prose; the gap is that no acceptance-testable spec (thresholds, approved-alternative criteria) has been authored.
- Source: `CLAUDE.md` ("The Product Naming Chain" — Golden Quill hardware paragraph; "Hardware" section).

### F6 — The refine seed already selected the falsification overlay that the research must feed.
- `toy_game_for_low_cost_falsification` + `xray_for_hidden_structure` + `baseline_sequence`. The Invoke-first direction names the first deliverable: "x-ray the hardware-to-image chain and define the first low-cost acceptance test before install work is routable."
- Source: `.../REFINE-SEED-PROPOSAL.md` (Selected Technique Overlays); `.../INVOKE-FIRST-ARTIFACTS.md` (Next Direction).

### F7 — Local evidence is sufficient to author the SPEC SHAPE of all four gaps; it is NOT sufficient to fill the threshold VALUES for two of them.
- Reference spec (F5) and image-verify (F3/F4) can be shaped from internal canon alone. Burn-in thresholds (thermal/memory/storage/inference-benchmark numbers) and disk-encryption/imaging/signing reference *defaults* require external comparison data the workspace does not hold.
- Source: synthesis of F2 + F4 + F5 against `RESEARCH-STRATEGY.md` (External Evidence Classes list).

## Lane Map Per Gap

| Gap | Severity | Local-evidence sufficiency | Lane | External need |
| --- | --- | --- | --- | --- |
| GAP-HGI-REFERENCE-SPEC | flag | Spec shape: YES (SKUs in CLAUDE.md). Approved-alternative test criteria: PARTIAL. | local-first, author the spec; gap-triggered external only for current-SKU specs/pricing | DEFERRED: Apple Mac Studio / GX-10 / Spark current specs (EXT-HGI-1) |
| GAP-HGI-BURN-IN | flag | Procedure structure: YES (4 axes named). Numeric thresholds: NO. | local-first for procedure skeleton; gap-triggered external for threshold defaults | DEFERRED: burn-in / thermal-soak / inference-benchmark practice (EXT-HGI-2) |
| GAP-HGI-IMAGE-VERIFY | block | Trust primitive: YES (router.yaml signing + manifest verify). Per-unit write+verify procedure: authorable locally. | local-first, author per-unit verify procedure consuming existing signing chain | None required to author; EXT optional for imaging-tool reference patterns |
| GAP-HGI-BACKUP-RECOVERY | block | Posture intent: YES (local backup / customer-owned export / recovery, Sovereignty Promise). Tested procedure: authorable locally. | local-first, author tested procedure aligned to Sovereignty Promise | None required to author; EXT optional for encryption/export reference |

## External-Research Decision

**DEFERRED.** No web search, WebFetch, or external lookup was run (gate rg03 — not authorized this run). Two bounded external-research requests are named for Josh's explicit approval; the other two gaps are authorable from local evidence and need no external pass to begin.

Bounded request list (each requires Josh's go/no-go before any external execution):

- **EXT-HGI-1 — Current reference-SKU specifications.** Bounded to: Apple M3 Ultra Mac Studio, AMD GX-10 class, NVIDIA Spark (DGX Spark / ASUS Ascent GX10) — published spec sheets only (RAM ceilings, thermal envelope, port/peripheral fit, current availability). Triggering gap: `GAP-HGI-REFERENCE-SPEC`. Protected-context flag: NONE (public vendor specs; no applicant or client data leaves the node). Purpose: turn named SKUs into a testable acceptance spec with an approved-alternative rule.
- **EXT-HGI-2 — Burn-in / acceptance-test threshold references.** Bounded to: standard hardware burn-in practice (thermal soak, memory test, storage SMART/endurance) and local-inference benchmark conventions. Triggering gap: `GAP-HGI-BURN-IN`. Protected-context flag: NONE (general engineering practice). Purpose: source defensible numeric thresholds for the four burn-in axes.

Optional / not-yet-named-as-required: imaging-tool and disk-encryption/signing reference patterns for `GAP-HGI-IMAGE-VERIFY` and `GAP-HGI-BACKUP-RECOVERY` — these gaps are authorable from local canon (router.yaml signing chain + Sovereignty Promise), so external is enhancement-only, not blocking. Record but do not request approval unless the local authoring pass surfaces a concrete missing default.

## Residue

- R1: `GAP-HGI-IMAGE-VERIFY` and `GAP-HGI-BACKUP-RECOVERY` are `block` severity but newly assessed as **locally authorable** — the block reflects "procedure not yet written," not "evidence missing." This is a Refine-execution task, not a research blocker. Surface to Josh so the block severity is not misread as needing external input.
- R2: The "Sanitized" posture appears in the source workbook (§1, B "Posture system: Unrestricted / Hybrid / Sanitized / Sovereign") but is DEPRECATED in current canon (CLAUDE.md v7.0.10 three-posture model). Workbook is a 2026-06-12 extract; canon supersedes. Not this node's lane to fix — flag only.
- R3: router.yaml confirms the signing trust mechanism but holds no hardware SKU or burn-in data — confirming EXT-HGI-1/2 are genuine local gaps, not search-laziness.

## Next Move

Confirm with Josh: (a) approve EXT-HGI-1 + EXT-HGI-2 bounded external passes, OR keep deferred; and (b) authorize a local-first Refine execution pass to author the reference-spec, image-verify, and backup-recovery procedures (which need no external input) under the existing `REFINE-DISPATCH.json` route. The first concrete deliverable is the Invoke-first "x-ray the hardware-to-image chain + define the first low-cost acceptance test."
