# UI Prototyping Studio UX/UI Upgrade Research - Explorer Transcript

Dispatch: `2026-07-09-ui-prototyping-studio-ux-upgrade-research`

This file is the strategist-owned explorer transcript for the research dispatch. It records the four explorer returns and their robot-talks final positions. Synthesis, review, and recommendations belong in `findings.md`.

## Agent 1 - Turing, Alan - Runtime Archaeology

### Initial Return

Route: registered subagent dispatch, explorer Turing/Alan. Repo files not edited. Studio trials used only `/tmp` data. No preview processes left running (`pgrep -af "src/cli/studio.ts preview"` returned none). `git status --short projects/ui-prototyping-studio` returned clean.

Surfaces used:

- Source/test surfaces read: `backend/package.json`, `src/cli/studio.ts`, `e2e/helpers.ts`, `e2e/{auto-cycle,blind-naive-user,governance,human-loop,preview-accept,smoke}.spec.ts`, `e2e/fixtures/*`, `e2e/fixtures/corpus/CORPUS.md`.
- Validation:
  - `./node_modules/.bin/tsc -p tsconfig.json --noEmit` passed.
  - `./node_modules/.bin/tsx --test "src/**/*.test.ts"` passed `62/62`.
  - `pnpm run check` and `pnpm test` failed before project code: Corepack key-id signature mismatch.
  - Temp shim: `PATH=/tmp/ups-pnpm-shim-qWBwq2:$PATH ./node_modules/.bin/playwright test --output /tmp/ups-e2e-results-84C12Q --reporter=list` passed `13/13`. Output: `/tmp/ups-e2e-results-84C12Q/.last-run.json`.
- Manual CLI log: `/tmp/ups-live-troqar-SRqMWu/manual-cli.log`.
- Main direct command shape: `STUDIO_DATA=/tmp/ups-live-troqar-SRqMWu/studio.json STUDIO_ACTOR=explorer:turing ./node_modules/.bin/tsx src/cli/studio.ts <command>`.

TROQAR commands sampled:

- `session open --variants 3`
- `prompt submit ups-session-0001 "TROQAR login production architecture alternatives"`
- `variants register ups-session-0001 --from e2e/fixtures/corpus/troqar-login`
- `baseline select ups-session-0001 B`
- two `comment add` calls on `auth.connect.cta` and `login.hero`
- `pending`, `synthesize`, `watch`, `batch approve`
- `apply ups-session-0001 ups-batch-00001 --candidate-from e2e/fixtures/corpus/toy-game-theme/candidate-B-desaturated.html`
- `state`, `revisions`, `handoff export`, `accept`, `handoff export --confirm`, `revert`, `watch`

Browser/control evidence:

- `/tmp/ups-browser-controls-F3S4lU/controls.log`
- Screenshots:
  - `/tmp/ups-browser-controls-F3S4lU/discard-01-staged.png`
  - `/tmp/ups-browser-controls-F3S4lU/discard-02-after.png`
  - `/tmp/ups-browser-controls-F3S4lU/accept-01-staged.png`
  - `/tmp/ups-browser-controls-F3S4lU/accept-02-after-accept.png`
  - `/tmp/ups-browser-controls-F3S4lU/accept-03-after-revert.png`

Cycle evidence:

- `/tmp/ups-cycle-GLkcEB/cycle.log`
- `cycle exploit --objective "make cta clearer" --candidate continue.html:0.9 --candidate next.html:0.4` chose `0.9`, advanced head.
- `cycle exploit --objective tighten --candidate badge.html:0.8` rejected structural divergence.
- `cycle explore --objective "try badge" --candidate badge.html:0.8` admitted new `cta.badge`.

Guarantees that worked:

- Isolated `STUDIO_DATA` works; artifact roots land beside `/tmp/.../studio.json`.
- `variants register --from e2e/fixtures/corpus/troqar-login` registered A/B/C content-addressed artifacts.
- Baseline select set `revisionHeadId: rev-0000`; two-gate `apply` staged without advancing head; `revisions` stayed `[]` until accept.
- `handoff export` without `--confirm` refused with exit 3 and `HANDOFF_CONFIRMATION_REQUIRED`.
- `accept` advanced to `rev-0001`; `revert` appended `rev-0002`, did not rewind history.
- Browser annotate works: click component in `#annot`, submit form, `pending` shows one `web-ui` comment.
- Browser accept/discard/revert work when preview starts after staged state.
- Export remains absent as a browser button; terminal-only checkpoint is preserved.
- Exploit/explore distinction works: exploit rejects added `data-od-id`; explore admits it.

Failures and surprises:

- Corepack currently blocks plain `pnpm`; e2e helpers depend on `pnpm exec tsx`, so cold e2e is fragile unless Corepack is healthy or a shim/direct path is used.
- Preview server does not observe external CLI writes after startup. Evidence: browser preview created comment, then separate CLI ran synthesize/approve/apply and returned `RevisionApplied`; running preview `/state` still reported `CommentsCaptured`, `stagedHash:null`. This contradicts the CLI source comment saying state is read fresh per request.
- TROQAR theme candidate reproduced the known honest-diff falsifier: `apply ... candidate-B-desaturated.html` returned `NOT_REJECT` but `diff.fragments: []`, `added/changed/removed: 0`, then accept recorded zero diff. Visible CSS/theme edits can look like "no changes."
- `watch` after synthesize returned `pendingComments:0` and `suggestion:"no pending comments; idle"` while state was `MutationDrafted`; it misses the next approval/apply action.
- Confirmed handoff sets `integration.uiPhaseBridgeReady/generateTestsUiReady/uiImplementReady: true` while `bundle.missingRefs` lists every default doc ref. That reads like readiness overclaim.
- Recorded screen after accept still renders the baseline variant card, not a current-head preview. Screenshot `accept-02-after-accept.png` shows `Go` while head is `rev-0001`.
- Annotation form is visible before target selection in screenshots, despite `hidden` in markup; `.cf { display:flex }` appears to defeat the hidden affordance. Submit before target would be confusing.
- Pending before/after iframes can appear blank in immediate screenshots unless tests wait inside frames; user-facing loading state is absent.

Upgrade candidates:

1. Make preview state coherent across CLI/server: reload file store per request, add a file version watcher, or move synthesize/apply into preview routes.
2. Add a global/style diff lane; never show zero-diff when raw HTML/CSS hash changed.
3. Add current-head preview after accept/revert, separate from baseline variant cards.
4. Fix annotate form hidden/disabled state; make severity a constrained control.
5. Make `watch` state-aware: drafted -> approve, approved -> apply, staged -> accept/discard.
6. Split handoff "export confirmed" from "implementation-ready" when `missingRefs` is nonempty.
7. Replace e2e helper `pnpm exec tsx` dependency with direct local `./node_modules/.bin/tsx` fallback.
8. Add iframe loaded indicators or wait-for-frame rendering before screenshot/export captures.

### Final Position

I keep my initial runtime claims: Studio's core gates are real, but the preview/control surface is not yet trustworthy enough for UX-upgrade claims. Own evidence: direct CLI TROQAR run at `/tmp/ups-live-troqar-SRqMWu/manual-cli.log`; browser/control run at `/tmp/ups-browser-controls-F3S4lU/controls.log`; unit `62/62`, shimmed e2e `13/13`.

Sibling evidence changes my priority order. Schon's accepted-head finding promotes "current head visibility" to the top: `/raw/baseline` may be correct, but cards/annotation showing the original variant is exactly the confidence break I saw in `accept-02-after-accept.png`. Beer also downgrades my "handoff readiness" concern from possible broken gate to governance/read-model drift: export refusal is solid, but readiness flags plus `missingRefs` need clearer semantics. Alexander changes the solution shape: borrow Open Design metadata/evidence structures, but keep Studio as admission harness.

I dissent from treating browser pass results as sufficient UX proof. The tests pass, but they scaffold around a live weakness: preview does not observe external CLI writes after startup, shown in `/tmp/ups-browser-clean-RCArgK/browser-clean.log`. I also dissent from any move toward subjective critique as a hard gate before calibration. CritiqueReview belongs in evidence/advisory, not admission.

Revised top upgrade ranking:

1. Current-head truth in preview: cards, annotation iframe, before/after, and recorded state must render the accepted/reverted head, not the original variant.
2. Preview state coherence: either reload file-backed state per request or clearly make preview the sole mutation surface while running.
3. Honest diff for global/style changes: CSS/theme edits must show a global/theme lane or explicit "not attributable per component," never zero-change confidence.
4. Decision framing for Accept/Revert/Discard: add consequence copy, staged summary, undo path, and maybe confirmation for durable accept/revert.
5. Annotation UX: component outlines/list, comment list, constrained severity, fix hidden-form bug.
6. Handoff/readiness semantics: export gate stays; readiness flags must not imply implementation-ready when `missingRefs` exists.
7. Harness reliability: remove `pnpm`/Corepack fragility from e2e helpers with direct local binary fallback.
8. OD borrowings: GeneratorProfile subset, DesignObjectiveBrief, CraftEvidencePack, seed/archetype library, and provenance fields as evidence, not bypasses.

## Agent 2 - Alexander, Christopher - Open Design Comparison

### Initial Return

Vendored snapshot only; I did not inspect live upstream. No files edited.

Studio baseline:

UI Prototyping Studio is not a generic design generator. Its spine is reversible, accountable UI exploration: generate 1-3 variants, pick/commit a baseline, annotate stable components, synthesize deterministic mutation batches, stage/apply/accept with lineage, then hand off evidence. The current model says control comes from reversibility plus an explicit human-confirmed export edge, not from blocking every agent action. Evidence: `projects/ui-prototyping-studio/README.md:3`, `projects/ui-prototyping-studio/SPEC.md:19`, `projects/ui-prototyping-studio/SPEC.md:95`, `projects/ui-prototyping-studio/ARCHITECTURE.md:95`.

Open Design mechanisms:

Open Design is organized around atomic `SKILL.md` capabilities plus optional `od:` metadata: preview type, design-system requirements, craft references, typed inputs, live parameters, outputs, and capability gates. This is a capability registry and artifact-production protocol, not an admission protocol. Evidence: `projects/ui-prototyping-studio/provenance/open-design-reference/skills-references/open-design/docs/skills-protocol.md:5`, `:57`, `:99`.

OD modes split artifact shapes: Prototype, Deck, Template, Design System. The mode controls skill picker, preview, export, and refinement affordances. Studio's HUMAN/AUTO explore/exploit modes are a different axis, so OD modes map better to "artifact profiles" than Studio operating modes. Evidence: `.../docs/modes.md:5`, `.../docs/modes.md:7`, `projects/ui-prototyping-studio/SPEC.md:100`.

OD's three-axis model is strong: artifact skill, brand `DESIGN.md`, universal `craft/` rules. Craft references are opt-in and can be auto-checked or guidance only. Evidence: `.../craft/README.md:16`, `:24`, `:52`.

Named skills show reusable production patterns: `web-prototype` uses seed templates, layout skeletons, `DESIGN.md`, self-checks, and `data-od-id`; `mobile-app` adds archetypes and mobile craft; `critique` outputs evidence-backed 5-dimension review; `tweaks` wraps artifacts in reversible knobs; `live-artifact` separates source template/data/provenance from derived preview; `design-brief` converts vague language into resolved design dimensions. Evidence: `.../skills/web-prototype/SKILL.md:29`, `.../skills/mobile-app/SKILL.md:27`, `.../skills/critique/SKILL.md:50`, `.../skills/tweaks/SKILL.md:36`, `.../skills/live-artifact/SKILL.md:75`, `.../skills/design-brief/SKILL.md:113`.

Maps cleanly into Studio:

- Stable component identity maps directly. OD's `data-od-id` rule on every section and major mobile region aligns with Studio's `AnnotationTarget.odId` survival requirement. Evidence: `web-prototype/SKILL.md:86`, `SPEC.md:41`, `SPEC.md:294`.
- Craft references map cleanly as candidate evidence packs: a11y, layout integrity, target size, contrast, state coverage, anti-slop checks. Studio already has L1/L2 acceptance surfaces and a deferred UX-constraint fitness layer; OD craft provides a pattern vocabulary and some lintable checks. Evidence: `SPEC.md:301`, `SPEC.md:309`, `anti-ai-slop.md:14`.
- Source/derived split from `live-artifact` maps very well to Studio handoff evidence: agent-authored source, compact data, provenance, derived preview, and all-or-nothing refresh/commit. Studio already cares about seen == recorded and append-only manifest entries. Evidence: `artifact-schema.md:5`, `refresh-contract.md:60`, `SPEC.md:84`.
- Structured brief parsing maps to objective capture, especially if defaults are disclosed and persisted as provenance. Evidence: `design-brief/SKILL.md:82`, `design-brief/SKILL.md:261`.

Inspires only:

- OD skill discovery and mode routing should inspire Studio generator profiles, not replace the Studio state machine. Studio's authoritative seam remains `studio variants register` plus admission validation.
- Critique scoring is useful as review evidence or AUTO self-critique input, but the scores are subjective. It should not become a hard gate until calibrated against fixtures. Evidence: `critique/SKILL.md:162`, `CRAFT.md:132`.
- Tweaks are excellent reversible exploration, but only durable if converted into comments/mutation batches or accepted staged revisions. LocalStorage-only deltas are not lineage. Evidence: `tweaks/SKILL.md:49`, `tweaks/SKILL.md:210`.
- VoltAgent `design-md` is a rich reference corpus, not Studio truth. It can seed design contexts, tokens, and examples, but not silently define product identity. Evidence: `open-design-reference/README.md:16`, `voltagent-design-md/PROVENANCE.md:14`.

Would violate Studio governance:

- Directly emitting OD `<artifact>` output as final product without `variants register`, baseline selection/commit, staging, manifest append, and export evidence would bypass Studio.
- Hard-blocking durable changes on subjective taste checks would overclaim. Studio admission can prove bounded/well-formed/reversible; it explicitly does not machine-check full acceptance intent. Evidence: `SPEC.md:299`.
- Silent craft fallback is acceptable in OD but risky in Studio. If a generator profile declares a required craft reference and it is missing, Studio should mark evidence incomplete rather than silently drop it. OD's silent-fallback rule is documented at `skills-protocol.md:246`.
- Connector-backed live artifacts should not be imported wholesale. Studio has no OD daemon/connector runtime; connector data, credentials, and raw provider envelopes are outside its current boundary. Evidence: `connector-policy.md:91`.

Upgrade candidates:

1. Add `GeneratorProfile` metadata: a Studio-owned subset of OD `od:` fields: `platform`, `preview`, `designContext.sections`, `craft.requires`, `inputs`, `parameters`, `outputs`. Persist profile id/version in variant provenance. This keeps OD skill shape as generator context, not authority.
2. Add `DesignObjectiveBrief`: structured objective intake with explicit defaults, unresolved dimensions, and constraints. Use the design-brief pattern, but persist default provenance and require user confirmation before it becomes export evidence.
3. Add `CraftEvidencePack`: per-candidate checks for `data-od-id`, raw hex, accent budget, contrast, target size, focus/label basics, state coverage. Split `required_gate`, `advisory`, and `subjective_review`.
4. Add seed/archetype generator libraries for web and mobile. Use OD's section/screen archetypes to improve generated variants, while preserving Studio's 1-3 variant loop and `data-od-id` survival rule.
5. Add `CritiqueReview` as candidate evidence: five dimension scores, evidence paragraphs, Keep/Fix/Quick-wins. Good for compare/selection and AUTO scoring; not a hard admission gate.
6. Add reversible tweak sessions: curated knobs for accent, type scale, density, mode, motion. Store knob changes as temporary candidate deltas; make them durable only through staged accept/revision manifest.
7. Strengthen handoff bundle with source/derived/provenance separation: authored HTML/source, normalized design context, candidate hash, validator results, critique summary, and export confirmation. This is the most Studio-native Open Design import.

### Final Position

Tension axis: import Open Design's pattern language only where it strengthens Studio's reversible governance and handoff evidence. Runtime trust defects now outrank new design-pattern imports.

Keep from initial return:

- Keep the core claim: Studio is an admission, lineage, and handoff harness, not a generic design generator. Its identity is accountable UI exploration with reversible durable changes and explicit export/handoff evidence (`SPEC.md:19`, `SPEC.md:95`).
- Keep the clean Open Design borrowings, but as Studio-owned evidence/profile layers: `GeneratorProfile`, `DesignObjectiveBrief`, `CraftEvidencePack`, seed/archetype libraries, `CritiqueReview`, reversible tweak sessions, and source/derived handoff packaging. OD's useful model is skill + design-system + craft context (`skills-protocol.md:57`, `craft/README.md:16`).
- Keep the warning: critique/taste scores are advisory evidence, not hard gates. OD itself requires evidence-backed scoring but it remains reviewer judgment (`critique/SKILL.md:162`).

Sibling evidence changes:

- The preview/head mismatch changes the priority order. If `/raw/baseline` has the accepted head but preview cards and annotation still show the original variant, Studio's control contract is visibly lying. Fixing head truth beats adding richer OD pattern context.
- The "visible CSS/theme edit with zero honest diff" finding makes honest diff integrity a top governance issue. My earlier source/derived handoff idea still stands, but it now needs a stronger visible-change/diff bridge before it can be trusted.
- Beer's finding changes the export-gate ranking: core export confirmation is no longer the top governance hole if tests now exist. The new need is docs/test-count sync plus regression evidence for `missingRefs` and TROQAR-style selector/copy obligations.
- Schon's walkthrough sharpens the UX layer: Accept/Revert can stay one-click only if framed as reversible durable actions with visible current-head state, loading, selected/hover outlines, comment list, severity controls, and human-readable next steps.

Dissent:

- Do not treat Corepack/pnpm failure as product evidence. It is an evidence-production blocker and should be fixed, but direct `tsx`/shim passing means the product claim should not be rejected solely on package-manager friction.
- Do not promote OD's `tweaks` model directly. LocalStorage knobs are exploration only unless captured as staged candidate deltas and committed through Studio lineage (`tweaks/SKILL.md:36`).
- Do not import OD live-artifact connector assumptions. The useful part is source/derived/provenance separation, not OD's daemon/connector runtime (`artifact-schema.md:5`).

Revised top upgrade ranking:

1. Head-truth and preview integrity: accepted head must drive preview cards, annotation, current state labels, and before/after surfaces.
2. Honest visible diff: CSS/theme/layout-visible edits must produce diff evidence; zero-diff visible mutations are governance regressions.
3. Control-confidence UX: framed Accept/Revert, loading states, current-head language, mobile before/after width, annotation hover/selected outlines, component/comment lists, severity controls.
4. Evidence harness repair: Corepack/pnpm path or shim e2e standardization, stale docs/test-count sync, `watch` state fix, preview external-write observation.
5. Handoff correctness: fail integration-ready on `missingRefs`; preserve Body War/TROQAR as selector/copy-to-test obligation evidence, not production-HTML proof.
6. OD-derived craft layer: `CraftEvidencePack` for a11y/layout/anti-slop checks, clearly split into hard gates, advisory checks, and subjective review.
7. OD-derived generation layer: `GeneratorProfile`, `DesignObjectiveBrief`, and seed/archetype libraries after runtime trust is fixed.

## Agent 3 - Schon, Donald - UX Walkthrough

### Initial Return

Read prior expectations: `TEST-PROTOCOL.md:3` frames the test as governance/control, not visual polish; `blind-naive-user.spec.ts:6` expects cold-start orientation, visible annotation success, visible before/after, in-browser Accept/Discard, and no Export button. Used only `/tmp` copies/sessions; no repo edits. Preview servers were stopped and leftover preview PIDs killed.

Evidence commands/surfaces:

- `STUDIO_DATA=/tmp/ups-walkthrough-bodywar/studio.json ./node_modules/.bin/tsx src/cli/studio.ts preview ups-session-0001 --port 0`
- `STUDIO_DATA=/tmp/ups-walkthrough-staged*/studio.json ./node_modules/.bin/tsx src/cli/studio.ts ...`
- Screens:
  - `/tmp/ups-bodywar-desktop.png`
  - `/tmp/ups-bodywar-mobile.png`
  - `/tmp/ups-staged-desktop.png`
  - `/tmp/ups-staged-mobile-before.png`
  - `/tmp/ups-staged-desktop-after-accept.png`
  - `/tmp/ups-staged-desktop-after-revert.png`

What held:

- The staged state says the important thing: `RevisionApplied` plus "STAGED (head not advanced)" is visible in the header.
- The pending panel shows a human-readable diff line and before/after panes.
- Export stays terminal-only with `--confirm`, matching the blind test expectation.
- Annotation can succeed: clicking a Body War copied preview target opened the form and submission returned `captured`.

Ranked friction:

1. Critical: after Accept, the preview no longer shows the accepted head as the main inspectable artifact. Observed on synthetic staged session: before Accept, `/raw/baseline` was `Go` and `/raw/staged` was `Continue`; clicking Accept changed `/state` to `RevisionRecorded`, head `rev-0001`. But the visible card and annotation iframe still rendered `/raw/variant/A` with `Go`, while `/raw/baseline` correctly returned `Continue`. Source shape explains it: preview cards come from variants in `studio.ts:204`, annotation uses `/annotate/variant/${baseline.label}` at `studio.ts:230`, but current head is only exposed via `/raw/baseline` at `studio.ts:334`. Upgrade: after `RevisionRecorded`, show a primary "Current accepted revision" iframe sourced from `/raw/baseline`; make annotation target the current head, not the original variant. Keep original variants collapsed as history/reference.
2. High: Accept/Revert are one-click durable controls with weak decision framing. On the Body War copy, a recorded accepted session immediately showed `Revert last change`. On staged synthetic, `Accept this change` immediately advanced head; after Accept, `Revert last change` immediately advanced head again to `rev-0002`. No confirmation, no "you are about to commit/revert X", no diff recap at click time. Routes wire direct POSTs at `studio.ts:304`. Upgrade: add a lightweight confirmation sheet for Accept/Revert with current head, candidate hash/revision id, diff summary, and "I inspected this change" checkbox. Revert should preview the target state before committing.
3. High: mobile staged before/after is technically responsive but not inspectable. At 390px, no horizontal overflow, but before/after panes were about 143px wide each. Screenshot `/tmp/ups-staged-mobile-before.png`: the panes read as narrow blank columns, not a meaningful comparison. Upgrade: stack before/after vertically on mobile; add a segmented control "Before / After / Diff"; put the changed component excerpt above the iframes.
4. Medium-high: annotation target selection is discoverable only after trial. Initial form shows `Target:` blank, severity/input fields visible, and no target outline. In Body War copy, 22 `data-od-id` targets existed; clicking inside the preview produced target `login.hero` and `captured`, but the user gets no hover affordance, no component list, no comment list, and severity is a free text field. On mobile, the annotate iframe looked blank/low-information in screenshot `/tmp/ups-bodywar-mobile.png`. Upgrade: hide form until selection; add hover/selected outlines; show component label + od-id; use severity select/buttons; show "1 comment captured" and pending comments.
5. Medium: next-step language is CLI-shaped, not user-shaped. Headers say things like `studio accept <sid>` and `studio handoff export <sid>`; on mobile the session id wraps awkwardly. This matches implementation state sentences in `studio.ts:188`. Upgrade: replace placeholder CLI text with contextual actions: "Next: review the staged change, then Accept or Discard." Keep exact CLI in a collapsed details row.
6. Medium: variant preview cards crop or appear blank on mobile. Body War mobile stacked cards correctly, but variant C's iframe captured as blank while frame text existed. The fixed 340px iframe height and no load/status affordance make this feel unreliable. Upgrade: add iframe load/error indicators, "open full preview" buttons, and responsive thumbnail scaling.

Bottom line:

The preview now proves the governance loop exists, but the user's control confidence breaks right after the most important moment: Accept changes state, while the visible artifact still looks like the pre-accept variant. Fix current-head visibility first, then mobile staged comparison, then annotation affordances. Those three upgrades would make the blind-naive-user contract much closer to true from a human perspective, not just from tests.

### Final Position

I keep my core finding: the preview's biggest UX failure is that after Accept, the visible artifact does not become the accepted head. I observed `/raw/baseline` change to `Continue` while the visible variant/annotation iframe still showed `Go`; the code path supports that split because cards render variant refs and annotation uses `/annotate/variant/...`, not current head (`studio.ts:204`, `studio.ts:230`, `studio.ts:334`). I also keep mobile before/after as non-inspectable evidence: screenshot `/tmp/ups-staged-mobile-before.png`.

Sibling evidence changes: Turing's runtime evidence sharpens my UX finding into a state-truth problem, not merely presentation. If the preview may miss external CLI writes after startup, and CSS/theme edits can produce visible changes with zero honest diff, the user cannot reliably infer "what changed" from either page state or diff summary. Beer also changes priority: before claiming the loop is usable, docs/test counts, direct/shim e2e, L1/L2 proof, and human-control evidence must be synced. Alexander adds a useful design direction: borrow Open Design metadata/critique/evidence-pack structure, but only as evidence and authoring scaffolding, never as a bypass around register/baseline/stage/manifest.

I dissent from treating Open Design "taste" or critique as a gate. It can enrich objective briefs, seeds, archetypes, and review packets, but it cannot decide acceptance. I also dissent from calling the Body War/TROQAR handoff production UI proof; it proves a selector/copy-to-app-test bridge and a useful session artifact, not deployable HTML. Finally, a "shim e2e passes" result does not erase the UX risk if the human-facing preview can still show stale or misleading state.

Revised top upgrade ranking:

1. Current-head truth surface: after Accept/Revert/external CLI writes, the primary preview and annotation surface must render current head, not original variant. Include explicit state invalidation/reload.
2. Diff trust repair: honest diff must catch visible CSS/theme deltas or disclose "visual-only/style changes not represented." Zero diff with visible edit is control poison.
3. Durable gate framing: Accept/Revert need confirmation with candidate/revision id, human-readable diff recap, and "I inspected this" friction. My one-click Accept/Revert concern stands; route is direct POST today (`studio.ts:304`).
4. Mobile staged comparison: stack before/after or use a Before/After/Diff segmented view; current side-by-side mobile panes are too narrow to judge.
5. Annotation usability: fix hidden/form state, add hover/selection outlines, component labels, comment list, severity controls, and iframe loading/error states.
6. Evidence/docs sync: direct/shim e2e command path, stale docs/test counts, L1/L2 proof, human-study/control packet, and TROQAR regression bridge before stronger ergonomics claims.

## Agent 4 - Beer, Stafford - Governance Viability

### Initial Return

Current governance facts:

Studio is best read as a governance harness, not a UI generator identity. The live architecture says Claude Code generates/mutates HTML through the `studio` CLI seam, while the orchestration core owns gates, state, synthesis, stores, and invariants. Evidence: `SPEC.md:30`, `ARCHITECTURE.md:46`.

The current control model is reversibility, not human-vs-agent identity gating. The agent may drive reversible in-Studio actions, including auto-cycle and accept, but export is the one irreversible downstream edge and requires explicit confirmation. Evidence: `SPEC.md:90`, `ARCHITECTURE.md:132`.

The export boundary now has real code support, not just docs. `exportDesignHandoff` requires a non-empty `confirmedBy`; the HTTP route passes `confirm` into that core gate; the HTTP export-gate tests cover both refused and confirmed paths. Evidence: `export-design-handoff.ts:21`, `http-routes.ts:362`, `http-export-gate.test.ts:19`.

Prototype Gate is a reusable evidence interface between DomainSpec UI docs and a target app task-session. It explicitly does not promote Studio HTML into production or canonical specs. Evidence: `PROTOTYPE-GATE.md:7`, `PROTOTYPE-GATE.md:69`.

Verification I ran:

- TypeScript check passed via local binary.
- Unit/slice tests passed `62/62`.
- Playwright e2e did not reach product assertions here because checked-in e2e helpers call `pnpm exec tsx`, and Corepack fails before CLI JSON is produced.
- Direct CLI smoke via `./node_modules/.bin/tsx src/cli/studio.ts session open --variants 1` works.

Contradictions / stale areas:

- The human-facing `CRAFT.md:18` is stale at the top: it still says extraction/decision-gate approval is the next move. The ledger has newer state saying `PLAN-NEXT` N1-N11 are done, unit/e2e green at that time, and commit/republication pending. Evidence: `.craft/ledger.yml:169`, `.craft/ledger.yml:744`.
- `PLAN-NEXT.md:13` is internally split: header says the work pack executed, but later still says "Non-executed." That should be treated as stale planning residue, not live state.
- Test-count claims drift: `SPEC.md:115` says `53 unit + 12 e2e`; `PLAN-NEXT.md:13` says `61 + 13`; current unit/slice reality is `62/62`. Fresh e2e cannot be claimed green until the Corepack/pnpm harness issue is resolved or bypassed in checked-in test tooling.
- SPEC still has a stale invariant row saying comments are escaped before persistence and render, while its own correction says raw text is persisted and escaped at render. Evidence: `SPEC.md:119`, `SPEC.md:266`.
- ARCH still contains old "preview read-only" wording, while live tests and docs show preview now annotates and provides accept/discard/revert controls. Evidence: `ARCHITECTURE.md:58`, `blind-naive-user.spec.ts:70`, `preview-accept.spec.ts:5`.

Body War / TROQAR handoff implications:

- The TROQAR handoff is real consumption evidence. It records an accepted Studio prototype gate, accepted revision, baseline variant B, candidate hash, no missing refs, and stable `data-od-id` obligations. Evidence: `STUDIO-PROTOTYPE-HANDOFF.md:3`, `HANDOFF-BUNDLE.json:30`.
- Consumption appears to have crossed into Body War production surfaces and tests: the handoff names `static/index.html`, `static/app.js`, Body War e2e, `UI-SPEC.md`, and `TEST-SPEC.md`; targeted search found those selectors and assertions in the named files. Evidence: `STUDIO-PROTOTYPE-HANDOFF.md:51`, `ui.spec.ts:24`, `UI-SPEC.md:122`.
- The Body War handoff is especially strong as evidence that Studio can translate reviewed selectors/copy obligations into a real app test contract. It is not proof that Studio HTML is production-ready, and the handoff says that explicitly. Evidence: `STUDIO-PROTOTYPE-HANDOFF.md:61`.
- The accepted changes preserve claim <= proof: token privacy explicit, public Strava link framed as display data, route geometry outside proof, CTA avoids verified scoring language. Evidence: `STUDIO-PROTOTYPE-HANDOFF.md:30`.

Viable upgrade taxonomy:

- Docs first: reconcile `CRAFT.md`, `PLAN-NEXT.md`, SPEC invariant rows, ARCH preview wording, and test counts. This is the highest leverage governance upgrade because stale claims now create more risk than missing code.
- Test/tooling: fix e2e helpers so they do not depend on ambient `pnpm exec` under Corepack. Either call repo-local `./node_modules/.bin/tsx`/`process.execPath` deterministically or pin package manager intentionally. Until then, "13/13 e2e" is not fresh proof in this environment.
- UX/research: the browser loop can complete accept/revert, but cold-start still needs terminal scaffolding and the ergonomics claim remains human-study-gated. Use `TEST-PROTOCOL.md:1` for control/understanding evidence, not visual taste.
- Tests next: add L1/L2 accessibility and layout proof if claiming release readiness. Current `package.json` has Playwright but no `@axe-core/playwright`; L1/L2 acceptance is specified, not fully evidenced by current dependencies. Evidence: `SPEC.md:301`, `package.json:20`.
- Code later: identity/UIIdentityIndex, richer component registry, L4/L5 scoring, and UX-constraint exploit/explore fitness should wait behind fixtures/calibration. They are valid upgrades, but not needed to close the immediate governance viability gap.

Non-goals:

- Do not treat Open Design borrowing as identity replacement. In this corpus it is reference/guideline/provenance, not Studio's canonical identity.
- Do not promote Studio HTML into Body War production.
- Do not claim trust-meter, saw-the-diff proxy, import-integrity, or soft-score calibration are solved.
- Do not reintroduce human-vs-agent identity gating unless DEC-026 is reopened.

Ranking hints:

1. Docs/governance sync: urgent, low risk, directly reduces stale-claim damage.
2. E2E harness fix: urgent, because fresh e2e proof is currently blocked by tooling, not product logic.
3. Human-study/control evidence: needed before stronger ergonomics claims.
4. L1/L2 accessibility/layout proof: needed before "release floor" claims.
5. TROQAR regression bridge: preserve Body War handoff as a live selector/copy contract.
6. L4/L5 code upgrades: valuable, but only after fixtures and calibration.

No repo edits were retained from this inspection.

### Final Position

I keep my core viability read: Studio's governance spine is real enough to build on. The irreversible export edge is core-enforced, not merely CLI theater: `exportDesignHandoff` requires `confirmedBy`, and HTTP passes `confirm` into that use case (`export-design-handoff.ts:21`, `http-routes.ts:362`). I also keep the Body War finding: TROQAR proves selector/copy obligations can move from accepted Studio evidence into real app specs/tests without promoting prototype HTML into production (`STUDIO-PROTOTYPE-HANDOFF.md:51`, `STUDIO-PROTOTYPE-HANDOFF.md:61`).

Sibling evidence changes the center of gravity: the next risk is not "is there a governance model?" but "does the visible operator loop truthfully reflect the governed state?" Turing + Schon both point to the same serious UX/runtime split: accepted head can be correct at `/raw/baseline` while preview cards/annotation still show the original variant. That directly undermines the control-confidence claim. Turing's CSS/theme zero-honest-diff finding also upgrades diff integrity from "future polish" to governance-critical, because a visible change with no honest diff weakens the saw-the-change boundary.

I dissent from treating those preview defects as proof the irreversible export boundary failed. They are confidence and state-projection failures around reversible work, not evidence that handoff export bypasses confirmation. I also dissent from any Open Design path that turns taste into a hard gate or replaces Studio identity. Alexander's usable contribution is the safe subset: OD metadata/profile/objective/evidence-pack/provenance as structured inputs, never as an authority bypass or identity transplant.

I keep stale-doc/test-count drift as live governance debt: `CRAFT.md:18` and `PLAN-NEXT.md:13` still mix old and executed states. The e2e harness risk is also real: helpers shell through `pnpm exec`, which was the Corepack failure path in my run (`helpers.ts:22`, `helpers.ts:74`).

Revised top upgrade ranking:

1. Fix preview/head projection after accept: cards, annotation target, visible current head.
2. Fix honest-diff coverage for CSS/theme/style changes.
3. Fix e2e harness to avoid ambient Corepack/pnpm fragility.
4. Frame one-click Accept/Revert and improve mobile before/after layout.
5. Reconcile stale docs/test counts and live Craft state.
6. Harden handoff readiness semantics around `missingRefs`.
7. Improve annotation UX: hover/selected outlines, component list, comment list, severity controls.
8. Add L1/L2 accessibility/layout proof before stronger release claims (`SPEC.md:301`).
9. Add OD-derived structured profile/evidence inputs only behind existing register/baseline/stage/manifest gates.
