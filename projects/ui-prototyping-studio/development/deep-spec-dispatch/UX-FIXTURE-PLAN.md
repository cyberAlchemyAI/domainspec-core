# UX-FIXTURE-PLAN.md

Fixture corpus for the studio ux-evidence-validator run (s6). Dispatch ui-prototyping-studio-deep-spec-001.

- UX-FIXTURE-PLAN.md (fixture corpus for the ui-prototyping-studio UX validator). RULE: no hard gate is promoted until its known-good fixture passes, its known-bad fixture fires, and the false-positive traps stay silent. Domain tag = authoring/data-tool (NOT ecommerce -> Baymard pack OFF). Viewport matrix = desktop/tablet/mobile with stable fonts, frozen mock data, disabled motion.
- === KNOWN-GOOD FIXTURES (gates must PASS / stay silent) ===
- FX-KG-01 (full compliant studio): all 7 panels mount, every control has accessible name+role, tab order = reading order, governance keyboard-operable, no overflow at 3 viewports, happy-path cycle completes via getByRole. Calibrates: smoke.1, a11y.1/2/3/6, layout.1/3, flow.1/2, dom.1. Expected: ALL PASS, no L4 flag.
- FX-KG-02 (compliant failure/recovery): each D5 state (GenerationFailed/SynthesisTimedOut/SourceStale/ApplyConflicted) shown with prompt+comments+draft preserved, GateState=blocked reason text, exactly one safe recovery control, no auto-apply/auto-discard. Calibrates flow.3. Expected PASS.
- FX-KG-04 (compliant apply dialog): ApplyApprovedBatch opens role=dialog/aria-modal, focus moves in, Tab cycles within, Escape closes, focus returns to trigger. Calibrates a11y.4. Expected PASS. (Currently UNBUILDABLE against impl -> this fixture is the acceptance target for closing the a11y.4 gap.)
- FX-KG-05 (gate with associated reason): a disabled governance button with aria-describedby pointing at its gate-reason note. Calibrates a11y.5. Expected PASS.
- FX-KG-06 (compliant targets): all governance buttons >= WCAG 2.2 SC 2.5.8 24x24 CSS px on touch viewport. Calibrates layout.2. Expected PASS.
- === KNOWN-BAD (DETERMINISTIC) FIXTURES (the matching hard gate must FIRE) ===
- FX-KB-01 (broken asset): a variant htmlArtifactRef 404s / a panel asset fails. smoke.1/2 must FIRE (block/high).
- FX-KB-02 (unnamed icon-only button): Apply rendered as an icon button with no accessible name. a11y.1 must FIRE (block) + axe button-name violation.
- FX-KB-03 (tab-order scramble): positive tabindex values reorder focus away from reading order. a11y.2 must FIRE (high).
- FX-KB-04 (untrapped modal): an apply dialog that does NOT trap focus / does not return focus on close. a11y.4 must FIRE (high).
- FX-KB-05 (overflow): a fixed-width panel causes horizontal scroll / clipped task text at mobile. layout.1 must FIRE (high).
- FX-KB-06 (sub-24px apply): the irreversible Apply button rendered at 18x18px. layout.2 must FIRE (medium).
- FX-KB-07 (gate bypass): Apply enabled before human approval (applyEnabled true with draftStatus!=approved). flow.2 must FIRE (block) -- proves the agent cannot take an unaccountable irreversible action.
- FX-KB-08 (work loss): a failure path that silently drops the comment stream / draft batch. flow.3 must FIRE (high) -- never lose the human's work.
- === SOFT-FLAG FIXTURES (proxy SHOULD flag, must NEVER block) ===
- FX-SF-01 (unassociated reason): disabled-reason text present near the control but no aria-describedby. a11y.5 soft_flag.
- FX-SF-02 (off-screen state change): governance state changes only in a region outside viewport. flow.4 soft_flag (change-blindness proxy).
- FX-SF-03 (ungrouped density): ONE decision region with 12 ungrouped sibling buttons. cog.1 soft_flag -- contrast with FX-FP-01 to prove it flags ungrouping, not total count.
- FX-SF-04 (override asymmetry): override placed behind an extra confirm step while ratify is one click. cog.2 soft_flag (D-S1 override-symmetry violation).
- FX-SF-05 (false-trust chip): a TypedReference-pending field shown with a confident green 'held' chip. cog.3 soft_flag (D-S2 honesty violation).
- FX-SF-06 (hidden prior selection): committed baseline badge hidden after synthesize. cog.4 soft_flag (working-memory proxy).
- FX-SF-07 (disabled drops name): a button that loses its accessible name in disabled state. dom.2 soft_flag.
- FX-SF-08 (renamed components): same UIElementIdentity rendered under a new name each cycle. dom.3 soft_flag (recognition-over-recall).
- === SCREENSHOT-REVIEW FIXTURES (human inspects; never a gate) ===
- FX-SR-01 (apply less salient than promo): irreversible Apply gate visually quieter than a decorative/secondary region. cog.5 reviewer prompt.
- FX-SR-02 (indistinct failure badge): failure state badge same color as the running badge. cog.6 reviewer prompt.
- === FALSE-POSITIVE TRAPS (the load-bearing proof: density/salience checks must NOT block an expert tool) ===
- FX-FP-01 (legitimate dense expert studio): the REAL seven-panel workbench with all controls visible and correctly GROUPED into labelled panels (variant grid, annotation form, mutation list, etc.). EXPECTED: cog.1 density proxy stays SILENT, cog.2 info-only, NO hard gate fires. This is the proof that high control-count in a grouped expert authoring tool is not a defect -- if cog.1 fires here, the threshold is mis-calibrated and the gate is rejected. Directly enforces claim-map note 'expert, search, and comparison workflows intentionally expose many options.'
- FX-FP-02 (compact secondary toolbar): an expert toolbar with intentionally compact, low-risk SECONDARY controls (e.g., zoom/density toggles) below the WCAG floor where alternate input exists. EXPECTED: layout.2 target-size hard gate fires ONLY on the irreversible/primary governance targets, NOT on these low-risk secondary controls -- proving the target-size gate uses product context and does not apply one universal threshold to every control.
- === CALIBRATION EXIT CRITERIA === A hard gate is promotable only when: (1) it PASSES on its FX-KG fixture, (2) it FIRES on its FX-KB fixture at the stated severity, (3) it stays SILENT on FX-FP-01 and respects context on FX-FP-02, (4) the finding output carries source_cards + proxy_limit. L4/L5 proxies remain non-blocking regardless. L6 claims are never automated -- supporting evidence (traces/timing/screenshots from FX-KG-01) is handed to the s8 naive-user study.
