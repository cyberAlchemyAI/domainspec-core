# Context Pack: SWU-WFE-007B

Status: strict coverage pass

Mode: standard

Lifecycle route: private tooling plus Sigil Development, using the existing
Arcanum bootstrap for the portable core and a declared private adapter sync

## Task boundary

Classify the strategy surfaces as:

1. the public `subagent-strategy` canonical contract;
2. generated runtime metadata and the declared `Task` to `Agent` tool-name
   adaptation;
3. the private DomainSpec adapter overlay.

Prove semantic parity without requiring byte identity. Repair the stale Claude
adapter through its declared private sync mechanism. Keep the generated Codex
surface on the portable public package because the private installer explicitly
declares only a Claude adapter; do not invent a second private runtime target.
Do not move private paths or DomainSpec policy into public Arcanum.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| DSS2B-O1 | Public canonical strategy remains owned by Arcanum. | task scope; private/public boundary | covered |
| DSS2B-O2 | Codex and Claude public runtimes preserve canonical lifecycle semantics. | current bootstrap provenance and generated surfaces | covered |
| DSS2B-O3 | Runtime provenance and the `Task` to `Agent` tool-name mapping are allowed metadata/adaptation. | bootstrap generator behavior | covered |
| DSS2B-O4 | DomainSpec constitution, type owners, research-output split, paths, and publication restrictions remain a private overlay. | private adapter owner | covered |
| DSS2B-O5 | Private runtime adapters are generated from the private owner, never edited as independent authorities. | existing installer single-source declaration | covered |
| DSS2B-O6 | Codex uses the declared public package; Claude composes that package with the declared private adapter. | live installer target and runtime provenance | covered |
| DSS2B-O7 | Removal or addition of lifecycle semantics fails parity. | task negative acceptance | covered |
| DSS2B-O8 | Removal of local owner, research-output, or public/private semantics fails parity. | task negative acceptance | covered |
| DSS2B-O9 | Formatting and declared runtime metadata differences pass. | task positive acceptance | covered |
| DSS2B-O10 | Synchronization does not touch global hooks/settings or public canonical content. | bounded write scope | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `work-pack/tasks/TASK-WFE-007-DSS-SHEET-BINDING.md` | 007B behavior, acceptance, write scope | complete SWU contract | `901af3368396ad81c0351f949abb78151645118dcacd1eabb31ed6954e3d3ca8` |
| `DESIGN.md` | dispatch evidence binder; WFE-D06 | composition decision and boundary | `94bcee30991e0e4ef5975a71f3d5cbb884bb468918a7c6759a02dbffb39c0b19` |
| `arcanum/arcana/subagent-strategy/SKILL.md` | portable lifecycle and public/private ownership boundary | public canonical contract | `8808fc5aaa65844ccea6f75abf8a0cffac8978d080a0ca0d6480acb6fc6681a5` |
| `.agents/skills/subagent-strategy/SKILL.md` | generated Codex provenance and body | public Codex witness | `0f13a20aff783f841a46f13290e6dac2e055f082c7c39b30b00ef67bbfed8161` |
| `.claude/skills/subagent-strategy/SKILL.md` | generated Claude provenance, tool mapping, and body | public Claude witness | `4915675297614af53bb48d2a8026077047179e2a125ea5e27fe83aa1a19dc503` |
| `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md` | private adapter owner and local rules | declared local overlay | `d47c0f447960c8f139b61e1d5091025f383a2a40dce02e291577471958b4897f` |
| `implementation/domainspec/internal_tools/subagents-dispatch-hooks/install.cjs` | chain-skill single-source installation | existing adaptation mechanism | `4896d027c77c0bf8db83c7a5aa459248ec88f1fc22511b7d8908d0b8469b57ce` |
| `.claude/skills/domainspec-subagents-strategy/SKILL.md` | stale generated private copy | causal drift witness | `8bb979c83b875453cee73a1d3b467140ad0a004900c81bf1bf453a86a9919847` |

## Classified starting state

| Surface | Classification | Starting result |
| --- | --- | --- |
| `arcanum/arcana/subagent-strategy/SKILL.md` | canonical public contract | owner |
| `.agents/skills/subagent-strategy/SKILL.md` | generated Codex view plus provenance metadata | semantic match |
| `.claude/skills/subagent-strategy/SKILL.md` | generated Claude view plus provenance and `Task` to `Agent` mapping | semantic match |
| private owner `domainspec-subagents-strategy/SKILL.md` | declared DomainSpec overlay | owner |
| `.claude/skills/domainspec-subagents-strategy/SKILL.md` | undeclared/stale generated copy | semantic mismatch |
| `.agents/skills/domainspec-subagents-strategy/SKILL.md` | no declared private Codex target | intentionally absent |

## Validation surface

```bash
node implementation/domainspec/internal_tools/subagents-dispatch-hooks/tests/test-strategy-runtime-composition.cjs
node implementation/domainspec/internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs
git diff --check -- implementation/domainspec/internal_tools/subagents-dispatch-hooks .claude/skills/domainspec-subagents-strategy
```

## Context Builder result

- Files selected: 8
- Obligation coverage: 10/10
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none; execution is local and bounded
