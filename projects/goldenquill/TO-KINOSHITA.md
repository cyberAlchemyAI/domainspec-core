# TO-KINOSHITA (Koichi) — AI Engineer (full-stack)

**Role:** Local inference, multi-model routing, ingestion/OCR, Scout, Grant Module Mapper, section drafting workflow, ensemble review, operator console, evidence capture, hardware spec + burn-in.
**Source:** [docs/strategy/development/node-on-desk-readiness/DISPATCH-VALIDATION.md](docs/strategy/development/node-on-desk-readiness/DISPATCH-VALIDATION.md) · workbook role map [docs/golden-quill-task-role-breakdown-handoff.md](docs/golden-quill-task-role-breakdown-handoff.md)

These are **refine-solvable and specced** — start now. Specs carry Define→Design→Plan, acceptance criteria, and first steps.

## Agent execution contract — run this first

When Koichi asks an agent to "read the artifacts" or start the AI/hardware lane,
the agent should treat this handoff as an executable Craft interface.

1. Read `pipeline/SESSION_BOOTSTRAP.md` for project orientation.
2. Read this handoff and linked artifacts by path.
3. Run `$craft state` for the Koichi-facing ledgers below.
4. Use `$interrogation` for Koichi-owned technical choices: inference/routing
   lane order, ingestion evidence shape, burn-in metric capture, reference-spec
   fields, or AI-side Golden Image handoff details. Ask one question at a time.
5. Do not implement or plan an interactive v0.1 UI. If the console row appears,
   route it to `TO-JOSH.md` until `DEC-BC-UI-BOUNDARY` is closed.
6. Do not fabricate SKU datasheet values or burn-in thresholds. Bracket them or
   route them to Josh/external-research approval.
7. After each answer or implementation receipt, update the relevant Craft ledger
   with evidence, residue, and next move.

### Koichi-facing Craft scope

| Scope | Ledger | Koichi interface |
| --- | --- | --- |
| Tilth runtime | `docs/features/tilth-runtime-build/.craft/ledger.yml` | AI lane work-packs: inference, routing, ingestion/OCR, Scout, Mapper, drafting, ensemble, evidence capture. |
| hardware image | `docs/features/hardware-golden-image/.craft/ledger.yml` | Reference workstation spec, burn-in procedure, inference benchmark, manifest producer/consumer boundary. |
| quality/security/proof | `docs/features/quality-security-proof/.craft/ledger.yml` | Provide AI/routing outputs that Victor can test and cite. |
| node readiness | `docs/strategy/development/node-on-desk-readiness/.craft/ledger.yml` | Child receipts eventually feed parent RG-2, RG-3, and RG-4. |

### Interrogation interface for Koichi

Use `$interrogation` for one technical choice at a time, for example:

```text
$interrogation docs/features/tilth-runtime-build --mode technical-interface
```

Good Koichi questions ask for one implementation-shaping answer: model route
input/output shape, parser boundary, benchmark prompt set, metric capture field,
or handoff contract with Vlad. Every answer should update the relevant spec,
work-pack, or Craft ledger.

## Build now (specs ready)

1. **Tilth runtime work-packs — AI lane** — `GAP-TRB-WORK-PACKS` (block)
   → [docs/features/tilth-runtime-build/BUILD-SPEC.md](docs/features/tilth-runtime-build/BUILD-SPEC.md)
   Your packs: local inference layer, multi-model routing, ingestion/OCR/evidence-extraction, Scout (manifest, governed fetch, fetch ledger, opportunity DB, reality report), Grant Module Mapper, section drafting workflow, ensemble review, evidence capture. Follow the sequenced dependency edges; coordinate Scout + ensemble with Vlad (shared packs).
   **Guardrails:** substrate LOCKED (Pydantic AI + Logfire + Ollama/vLLM + DSPy/GEPA + Logician) — no alternatives; no `[SLOT_*]` on the normal path; no CIC→CLC coupling.

2. **Reference-workstation spec template** — `GAP-HGI-REFERENCE-SPEC`
   → [docs/features/hardware-golden-image/BUILD-SPEC.md](docs/features/hardware-golden-image/BUILD-SPEC.md)
   Author the spec template + 128 GB floor + approved-alternative rule (SKUs: M3 Ultra Mac Studio / AMD GX-10 / NVIDIA Spark). **SKU datasheet values are operator-input/external-deferred (EXT-HGI-1)** — leave them bracketed, don't fabricate.

3. **Burn-in / acceptance procedure** — `GAP-HGI-BURN-IN`
   → same spec. Author the four-axis procedure (thermal / memory / storage / inference-benchmark) + which metrics to capture + the acceptance receipt. **Numeric pass/fail thresholds are operator-input (EXT-HGI-2)** — bracketed, not invented.

4. **Golden Image handoff (with Vlad)** — `GAP-TRB-GOLDEN-IMAGE-HANDOFF`
   Jointly fix the manifest/signature schema with **Vlad** before assembly.

## Blocked — do not start until ratified
- **Operator console** (`GAP-TRB-UI-PHASE`, WP-12) — blocked on **DEC-BC-UI-BOUNDARY** (Josh). v0.1 is **headless-only (locked)**. Console may only be a **read-only projection** over the real backend or a **deferred later-phase** surface — **never an interactive v0.1 UI**. Build only after Josh picks the phase.

## Coordinate with
- **Vlad** — Golden Image manifest/signature schema (joint lock); Scout + ensemble-review shared packs; routing vs. posture-enforcement boundary.
- **Victor** — your Scout/drafting/routing outputs feed his demo standard, claims register, and instrumentation.
