# Context Pack: SWU-WFE-008A

Status: strict coverage pass

Mode: standard

Lifecycle route: Spellcraft for Whisper plus the public Arcanum runtime-overlay
validator owner

## Task boundary

Create the generic manifest schema, deterministic admission validator, and
causal fixtures for runtime overlays. Create the private Whisper manifest and
migrate the existing `product_research_blueprint` preset into private payload
source. Do not change the bootstrap generator or generated Whisper packages in
this unit.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| WH1A-O1 | Manifest binds the live canonical source and SHA-256. | task manifest fields; WH-1 | covered |
| WH1A-O2 | Runtime targets and allowed runtime metadata are explicit. | generated Codex/Claude provenance | covered |
| WH1A-O3 | Local preset IDs and every payload digest are declared. | current product preset files | covered |
| WH1A-O4 | Additions occur only at exact declared extension anchors. | WFE-D06; task boundary | covered |
| WH1A-O5 | Copied-file destinations remain inside the runtime package. | task copied-file destinations | covered |
| WH1A-O6 | Protected canonical controls and gates cannot be removed. | `surface_map`, `language_audition`, `intent_state`, human gate, status ceiling | covered |
| WH1A-O7 | Missing/stale base, missing control, undeclared preset, unsafe destination, or digest mismatch fails. | task negative acceptance | covered |
| WH1A-O8 | Declared metadata and declared additive preset pass. | task positive acceptance | covered |
| WH1A-O9 | Generic code and fixtures contain no private preset content. | public/private boundary | covered |
| WH1A-O10 | `business_plan` and `live_presentation` remain canonical; only `product_research_blueprint` migrates to private source. | task explicit ownership split | covered |
| WH1A-O11 | Generator integration remains deferred to SWU-WFE-008B. | task split and dirty bootstrap overlap | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `work-pack/tasks/TASK-WFE-008-WHISPER-RUNTIME-COMPOSITION.md` | 008A scope and manifest fields | complete SWU contract | `21a31cedd0d7d592cd6f87e675ab2286cf5b20494b844b5920670377ce4bdf74` |
| `../2026-07-22-most-used-skills-efficiency-review/findings.md` | WH-1 | accepted source defect | current accepted review |
| `arcanum/spells/whisper/README.md` | shared state, gates, preset catalog, output status | canonical base | `20d430873a07ebc9ec02b89e77c94982168827755dced06f46685e70bea88f13` |
| `arcanum/tools/bootstrap_arcanum.sh` | current generation path | read-only integration boundary for 008B | `eed93902a1941cb40eb0560de40e2361ad969cdc72388c0c471009a317f9d257` |
| `.agents/skills/whisper/SKILL.md` | current controls and local preset additions | migration witness | `8de00e31a1aa75223eba40ab8351b14de5dd5bfa6cacaa110c0200ce0c2da202` |
| `.claude/skills/whisper/SKILL.md` | missing current canonical controls | stale-runtime witness | `d6b22c3f4543f30661e39c8cb007dd04bff2ddefc3139fb0d53938da361e3245` |
| `.agents/skills/whisper/presets/product-research-blueprint/` | README, preset, template | exact private payload source to migrate | `dfd0609a...`, `30579eb8...`, `e6ad0766...` |
| `work-pack/session-evidence/SWU-WFE-007B/receipt.json` | W1 closure | serial dependency | `60a18a7a959b982c813b415ab5b6fa25d0339fe5c7555e3267626668cebb40ac` |

## Dirty-overlap decision

`arcanum/tools/bootstrap_arcanum.sh` already contains unrelated Orchestrate
generation changes. SWU-WFE-008A reads but does not mutate that file. The
Whisper hook is deferred to 008B, where the live diff must be preserved.

## Validation surface

```bash
python3 arcanum/runtime/overlays/tests/test_runtime_overlay.py
python3 arcanum/runtime/overlays/scripts/validate_runtime_overlay.py \
  --manifest .arcanum/runtime/overlays/whisper/manifest.json \
  --target whisper
git diff --check -- arcanum/runtime/overlays .arcanum/runtime/overlays/whisper
```

## Context Builder result

- Files selected: 8
- Obligation coverage: 11/11
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none; implementation is deterministic and bounded
