---
title: GOLDEN QUILL — MYCEL — Image-Gen Prompt Set
filed: 2026-05-08 (rewrite — supersedes parchment-engraving spec from earlier same day)
operator: Josh
scope: copy-paste-ready ChatGPT image-gen prompts for the 5-sheet MyCel asset set
status: prompts ready — operator runs through ChatGPT image-gen, drops PNGs into this folder
existing_renders_as_visual_reference: true
asset_only: true
honors_locks:
  - architecture v7 LOCKED 2026-04-19 (six-seat council unchanged; MyCel is the interface above the council, not a competing roster)
  - CLC v2 §14 mycel_controls.status = empty_pending_sandbox (asset depicts the interface; production knobs still discovered through use)
  - v0.1 headless-only lock (asset depicts v1.x horizon UI)
sheet_set: 5 sheets, drawing numbers MYCEL-01 through MYCEL-05
title_format: "GOLDEN QUILL — [TOPIC]"
drawing_number_format: "MYCEL-NN" with "Sheet N of 5"
client_field: Sovereign Node LLC
year_field: 2026
system_field: Powered by Tilth
---

# GOLDEN QUILL — MyCel — Image-Gen Prompt Set

## Concept anchors (use these as preamble framing for any prompt)

MyCel is a **private thought synthesizer for human × AI exploration**. Multiple AI models explore one idea in different configurations (parallel, series, adversarial, hybrid) while a human steers the field. The point is *new thought emerging from multi-voice exploration*, not different seats doing different jobs.

Inspirations to lean into:
- **Cube by Future Audio Workshop** — a 3D soft synth where a navigable point in shape space morphs between source sounds. MyCel is the thought-version: navigate a point in reasoning shape space, morph between AI-model behaviors.
- **VST / soft-synth packaging in Ableton** — the asset feels like a high-end audio plugin manual page: control panels, sliders, knobs, 3D shape space, real-time visualization of what the controls do.
- **Projection-mapping filters** — controls are real-time filters applied to a live thought stream as it flows through the multi-model field, the way projection-mapping filters modify a live image stream in real time.

Privacy is non-negotiable — confidential ideas stay local; only non-confidential branches reach frontier models. The boundary is the user's call, set before exploration begins.

## Visual idiom (constant across all 5 sheets)

```
Background:        deep navy/black (#0a1628 → #06101e radial), faint gridded blueprint texture
Primary line work: warm gold/amber (#d4a857 to #c9a44a)
Highlights:        bright glowing gold (#f0c878) for active points, model crystals, refined-output stars
Text body:         muted ivory (#e8dfc8) for labels and small text
Title typography:  large serif (Cormorant Garamond / Playfair Display family), gold, small caps with em-dash separator
Body typography:   modern sans-serif (Inter / Söhne family) for control labels, slider values
Iconography:       geometric crystalline sigils (6-pointed-star or icosahedron silhouettes) for AI models, each a different accent color (purple, teal, green, amber, magenta) — the colored sigils are CONSISTENT across sheets so the same model reads across plates
Composition:       dark-blueprint feel, panel-based, generous negative space, decorative corner brackets at all four corners
Footer block:      five columns: Sovereign Node LLC · 2026 · Powered by Tilth · Drawing no. MYCEL-NN · Sheet N of 5
```

Reference: existing renders in `assets/cards/mycel/` — the prompts below are written to reproduce or refine those.

---

## Sheet 1 — MYCEL-01 — Cover plate

**Title:** GOLDEN QUILL — MYCEL
**Subtitle:** *A private thought synthesizer for human × AI exploration.*
**Closing tagline:** *MyCel turns one idea into a navigable field of possible thought.*

**Composition (left to right horizontal flow):**

```
[ ONE IDEA ]  →  [ MYCEL THOUGHT FIELD ]  →  [ OPTIONAL FRONTIER EXTENSION ]  →  [ REFINED THOUGHT ]
   amber                multi-model              shield-gated extension              bright star
   spark                  topology                 (non-confidential only)          comparison · selection · synthesis
                       with 6 model
                        crystals
```

Above the field: `HUMAN STEERING` panel (compass/quill icon · steer · select · redirect · refine).
Below the field: `PRIVATE LOCAL EXPLORATION` (lock icon · your ideas · your data · stays local).
Bottom row: three control panels — `GLOBAL CONTROLS` (Temperature · Breadth · Coherence · Model Mix), `PER-MODEL CONTROLS` (Weight · Temperature · Top-P · Context), `PROPAGATION MODES` (Parallel · Series · Hybrid).

### Image-gen prompt (copy-paste)

```
Dark navy/black blueprint-style technical illustration, deep #0a1628 background with faint blueprint grid texture and decorative gold corner brackets at all four corners. Warm gold/amber line work (#d4a857) and muted ivory text (#e8dfc8). Visual feel: high-end audio-plugin manual page meets sci-fi instrument schematic.

TITLE BLOCK (top, centered): large serif gold caps "GOLDEN QUILL — MYCEL", em-dash separator. Italic subtitle below in lighter ivory: "A private thought synthesizer for human × AI exploration."

CENTRAL HORIZONTAL FLOW (left to right, occupying the middle 60% of the plate):
1. LEFT — a small circular amber "spark" labeled "ONE IDEA" with concentric rings around it, like a sonar ping origin.
2. ARROW pointing right into a large rounded-rectangle frame labeled at top "MYCEL THOUGHT FIELD". Inside the frame: SIX small geometric crystalline sigils (6-pointed-star or icosahedron silhouettes), each a distinct accent color — purple, teal, green, amber, magenta, soft cyan — arranged loosely around a central bright glowing gold node. Connecting the sigils to the central node and to each other: dotted gold filaments forming a dense network with arrow-tipped strands and small particle accents along the paths. The whole field has a faint horizontal banding of light-particle density — denser in the middle (consensus), sparser at edges.
3. ARROW out of the field's right side passing through a small gold SHIELD ICON labeled "OPTIONAL FRONTIER EXTENSION · non-confidential exploration only". Beyond the shield: a small spiral-galaxy particle visualization indicating an external thought field.
4. ARROW pointing right to a final bright gold STAR/SPARK labeled "REFINED THOUGHT" with sub-label "comparison · selection · synthesis".

ABOVE THE FIELD (centered, connected by dotted gold lines descending into the field from multiple points): a horizontal pill-shaped panel containing a small compass/quill icon and the text "HUMAN STEERING · steer · select · redirect · refine".

BELOW THE FIELD (centered): a small lock icon and the text "PRIVATE LOCAL EXPLORATION · your ideas · your data · stays local".

BOTTOM ROW (three equal panels, framed in thin gold rules):
PANEL 1 — GLOBAL CONTROLS — four small icon-and-label cells: a thermometer icon "TEMPERATURE", three slider bars stacked "BREADTH", a wave-loop icon "COHERENCE", two interlocking circles "MODEL MIX".
PANEL 2 — PER-MODEL CONTROLS — four small icon-and-label cells: a balance scale "WEIGHT", a thermometer "TEMPERATURE", a gauge "TOP-P", a particle-cluster "CONTEXT".
PANEL 3 — PROPAGATION MODES — three small diagram cells: branching tree "PARALLEL", linear chain "SERIES", network with crossings "HYBRID".

BOTTOM (full-width framed pill): small gold quill icon and the italic text "MyCel turns one idea into a navigable field of possible thought."

DRAWING-NUMBER FOOTER (bottom edge, five columns separated by thin gold rules): "Sovereign Node LLC · 2026 · Powered by Tilth · Drawing no. MYCEL-01 · Sheet 1 of 5".

Style: dark cosmic blueprint, warm gold accents, no glossy textures, no neon, no modern flat-UI iconography. Crystalline model sigils are intricate and ornamental, like miniature rose-windows. Visual reference: synth-plugin manual cross-bred with an alchemy diagram.
```

---

## Sheet 2 — MYCEL-02 — MyCel Interface Surface

**Title:** GOLDEN QUILL — MYCEL INTERFACE SURFACE
**Subtitle:** *How the user steers a private multi-model thought field.*
**Closing tagline:** *Move the point. Change the field. Steer the thought.*

**Composition:** Three-column with a large center.

```
LEFT COLUMN              CENTER (largest)                          RIGHT COLUMN
- INPUT IDEA panel       THOUGHT FIELD VOLUME                      PER-MODEL CONTROLS
  (seed + intent)        (3D wavy manifold surface with            (Models A-D each with
- MODEL STACK            colored model paths flowing across         WEIGHT / TEMPERATURE /
  (Models A-D)           a transparent multi-faceted volume,         CONTEXT SHARE sliders)
- BOUNDARY POSTURE       a control point glowing gold inside,
  (privacy + scope)      paths emerging as REFINED THOUGHT
                         CANDIDATES on the right edge)

BOTTOM:                  GLOBAL CONTROLS — Temperature / Breadth / Coherence / Certainty
                         (4 sliders with numerical readouts)
```

### Image-gen prompt (copy-paste)

```
Dark navy/black blueprint-style technical illustration, deep #0a1628 background, faint blueprint grid, decorative gold corner brackets. Warm gold/amber line work, muted ivory text. Visual feel: high-end multi-model interface cross-bred with a 3D physics-simulation viewer.

TITLE BLOCK (top, centered): large serif gold caps "GOLDEN QUILL — MYCEL INTERFACE SURFACE", italic subtitle "How the user steers a private multi-model thought field." Top-right corner badge: "SHEET 2 OF 5" inside a thin gold rule.

THREE-COLUMN LAYOUT BELOW THE TITLE:

LEFT COLUMN (narrow):
- "INPUT IDEA" panel (framed): a small amber spark labeled "SEED · one idea enters", and a small pill underneath labeled "INTENT (optional) · explore boundaries · tone: open · depth: deep". An arrow flows out of this panel rightward into the center.
- "MODEL STACK" panel (framed): four rows, each with a small geometric crystalline sigil (different accent color per row — purple, teal, green, amber) and a label "MODEL A / B / C / D". Bottom row of the panel: a small "+ add model" affordance.
- "BOUNDARY POSTURE" panel (framed): a small dome-grid icon labeled "privacy & scope envelope". Beneath it a status row: a small lock icon and the text "LOCAL ONLY · frontier extension: OFF".
- A faint gold shield-icon connecting the panel column to the center, suggesting privacy gating.

CENTER (large, dominant):
A massive HORIZONTAL WAVY MANIFOLD — a 3D semi-transparent volume drawn as overlapping faceted contour shapes (like a layered topographic map seen at an angle) suspended over a faint round grid floor. The manifold surface is laced with thousands of gold and accent-color dot points connected by dotted-line networks. FOUR colored model paths (purple, teal, green, amber) curve across the manifold from left to right, weaving over and under each other. A bright glowing gold CONTROL POINT at the center is labeled "CONTROL POINT (you are here)". The right edge of the manifold emits FIVE small crystalline sigils labeled "REFINED THOUGHT CANDIDATES · emerging outputs". A "PATH DENSITY" legend in the lower-right shows three line styles: low / medium / high path-density. Faint axes labeled "X / Y / Z · UP" in the lower-left.

ABOVE THE MANIFOLD (centered): a horizontal pill panel labeled "HUMAN STEERING · steer · select · redirect · refine" with dotted gold lines descending into the manifold from several points.

RIGHT COLUMN (narrow):
"PER-MODEL CONTROLS" panel (framed) with heading "tune each model's influence". Four model rows, each with the model's crystalline sigil + name (Model A purple, Model B teal, Model C green, Model D amber) and three small horizontal sliders labeled WEIGHT / TEMPERATURE / CONTEXT SHARE with numerical readouts (0.42, 0.65, 0.35, etc.). At the bottom of the panel: a small "NORMALIZE WEIGHTS Σ = 1.00" status row.
Below: a small LEGEND box explaining the path-density and sigil iconography.

BOTTOM ROW (full width, framed pill): "GLOBAL CONTROLS" heading. Four equal slider panels — TEMPERATURE (creativity ↔ determinism, 0.58), BREADTH (narrow focus ↔ wide explore, 0.64), COHERENCE (divergent ↔ convergent, 0.67), CERTAINTY (tentative ↔ assured, 0.62) — each with a circular slider handle and a readout.

ABOVE THE FOOTER (full-width pill): a small lock icon and italic text "Private local workspace. Optional frontier extension only for non-confidential branches."

DRAWING-NUMBER FOOTER (bottom edge, five columns): "Sovereign Node LLC · 2026 · Powered by Tilth · Drawing no. MYCEL-02 · Sheet 2 of 5".

Tagline overlay near footer (small italic): "Move the point. Change the field. Steer the thought."

Style: a soft-synth interface cross-bred with a 3D physics simulation. Inspired by Cube by Future Audio Workshop — the manifold is the morphing-shape-space; the control point is the sound-position; the model paths are the morphed parameters. Dark cosmic blueprint, warm gold, no glossy textures, no neon, no flat-UI iconography.
```

---

## Sheet 3 — MYCEL-03 — Thought Propagation Topologies

**Title:** GOLDEN QUILL — THOUGHT PROPAGATION TOPOLOGIES
**Subtitle:** *How multiple models explore the same idea in different configurations.*
**Pull-quote (centered, framed): "MyCel is not about different seats doing different jobs. It is about multiple AI models exploring the same idea in different configurations."**

**Composition:**

```
TOP ROW: 4 topology mini-diagrams in a horizontal row
  1. PARALLEL — several models explore the same idea at once
  2. SERIES — one model hands to the next
  3. ADVERSARIAL / DEBATE — two or more models challenge each other
  4. HYBRID / SYNTHESIS — parallel and series paths recombine

CENTER: SHARED THOUGHT FIELD — one idea flows through M1-M5
  arranged in a long horizontal weaving pattern, producing
  CONSENSUS CLUSTERS and PROMISING OUTPUT BRANCHES on the right,
  recombining into REFINED OUTPUT.

BOTTOM: WHAT CHANGES ACROSS TOPOLOGIES — five trade-off axes:
  Speed · Novelty · Cohesion · Risk · Breadth of Exploration
  (each as a low/high horizontal scale with a marker)
```

### Image-gen prompt (copy-paste)

```
Dark navy/black blueprint-style technical illustration, #0a1628 background with faint grid, decorative gold corner brackets. Warm gold line work, muted ivory text. Visual feel: a network-topology study cross-bred with a particle-physics diagram.

TITLE BLOCK (top, centered): large serif gold caps "GOLDEN QUILL — THOUGHT PROPAGATION TOPOLOGIES", italic subtitle "How multiple models explore the same idea in different configurations." Top-right badge: "SHEET 3 OF 5".

PULL-QUOTE BAR (just below the title, full-width framed pill in lighter gold rule): centered italic two-line quote — "MyCel is not about different seats doing different jobs. It is about multiple AI models exploring the same idea in different configurations." — with a small compass icon at left.

LEFT EDGE (single source point): a circular amber "ONE IDEA INPUT" spark with concentric rings, with a single horizontal arrow flowing right into the four topology panels.

TOP ROW — FOUR EQUAL TOPOLOGY PANELS (framed in thin gold rules, numbered 1-4 in small circles):
PANEL 1 — "PARALLEL · several models explore the same idea at once": amber spark on the left, four arrows fanning out to four colored model crystals stacked vertically (purple, teal, green, amber, each labeled MODEL A / B / C / D), arrows recombining on the right into a small spark.
PANEL 2 — "SERIES · one model hands to the next": amber spark, single horizontal chain through four colored model crystals labeled MODEL A → B → C → D, ending in a spark.
PANEL 3 — "ADVERSARIAL / DEBATE · two or more models challenge or stress-test one another": amber spark, four model crystals arranged in a 2×2 grid with multiple criss-cross dotted arrows between them showing contention, recombining into a spark on the right.
PANEL 4 — "HYBRID / SYNTHESIS · parallel and series paths recombine into a shared output": amber spark, four model crystals in a tree-like pattern (parallel branches feeding into series confluence), recombining into a spark on the right.

CENTER — LARGE FRAMED PANEL labeled "THOUGHT FIELD" with sub-label "one idea flows through many models and recombines into consensus and promising branches":
A long horizontal weaving graph. Left edge: amber spark "ONE IDEA". Five model crystals labeled M1-M5 arranged in a serpentine sequence with dense dotted-line filaments weaving over and under between them; small particle accents trail along the paths, denser at intersections (consensus).
On the right side of the panel: three small "CONSENSUS CLUSTERS" rendered as tight particle-rosettes, each in a different accent color, leading via arrows to three "PROMISING OUTPUT BRANCHES" rendered as small node-and-edge sub-graphs, all converging into a final bright gold "REFINED OUTPUT" star labeled "shared understanding and next steps".

BOTTOM ROW — "WHAT CHANGES ACROSS TOPOLOGIES" (full-width framed bar, heading centered): five trade-off axes with small icons and low ↔ high horizontal scales with triangular markers:
- SPEED (stopwatch icon)
- NOVELTY (starburst icon)
- COHESION (interlocking circles icon)
- RISK (caution-triangle icon)
- BREADTH OF EXPLORATION (compass-rose / expand-arrows icon)

DRAWING-NUMBER FOOTER (bottom edge, five columns): "Sovereign Node LLC · 2026 · Powered by Tilth · Drawing no. MYCEL-03 · Sheet 3 of 5".

Style: dark cosmic blueprint with warm gold; the model crystals are intricate and ornate, the connecting filaments are delicate and particle-textured. Inspired by the visual language of a physics-of-networks textbook frontispiece. No glossy, no neon, no flat-UI.
```

---

## Sheet 4 — MYCEL-04 — Private Local Exploration

**Title:** GOLDEN QUILL — PRIVATE LOCAL EXPLORATION
**Subtitle:** *Confidential thought stays local. Optional frontier models extend only non-confidential branches.*
**Closing copy (large italic):** *Privacy enables creativity. Toss around half-formed ideas, sensitive plans, and unfiltered thoughts inside your private workspace. You control what leaves, what stays, and how it explores.*

**Composition (three-column with arrows):**

```
PRIVATE LOCAL WORKSPACE   →  POSTURE GATE         →   OPTIONAL FRONTIER EXTENSION
- Confidential ideas        - LOCAL ONLY              - External thought field
- Uploaded files            - SPLIT-CONTEXT HYBRID     (only non-confidential branches)
- Notes & memos             - FRONTIER-ELIGIBLE        - Multiple frontier-model crystals
- Local Models A-D         (user chooses which)
  (sealed local field)

LEGEND:    solid gold = allowed non-confidential flow
           red dashed with × = blocked confidential flow
```

### Image-gen prompt (copy-paste)

```
Dark navy/black blueprint-style technical illustration, #0a1628 background with faint grid, decorative gold corner brackets. Warm gold line work, muted ivory text, with a single accent of warm red (#c47558) for blocked-flow indicators.

TITLE BLOCK (top, centered): large serif gold caps "GOLDEN QUILL — PRIVATE LOCAL EXPLORATION", italic subtitle "Confidential thought stays local. Optional frontier models extend only non-confidential branches." Top-right badge: "SHEET 4 OF 5".

THREE-COLUMN LAYOUT (each column framed in a thin gold rule):

LEFT COLUMN — "PRIVATE LOCAL WORKSPACE · Sealed local thought field":
A large rounded-rectangle frame with a small lock icon at the top edge. Inside, three small icon-and-label cells stacked vertically on the left edge: a lock icon "CONFIDENTIAL IDEAS", a folder icon "UPLOADED FILES", a note-page icon "NOTES & MEMOS". To the right of these, four geometric crystalline sigils stacked vertically (purple, green, teal, amber), each labeled "LOCAL MODEL A / B / C / D". Dotted-gold filaments from the three icon-cells flow into the four model sigils, suggesting private content reaching the local models. At the bottom inside the frame: a small italic note "multiple local models can explore private material in parallel". Below the frame: a centered small shield icon. Outside the frame, on the left edge: a small italic label "confidential ideas stay local".

CENTER COLUMN — "BOUNDARY CHOICE · user chooses the boundary" (heading centered above):
A vertical stack of THREE selectable posture cards inside a "POSTURE GATE" frame, each with a small icon, label, sub-label, and a radio-button indicator on the right edge:
1. (radio FILLED) "LOCAL ONLY" — house icon — "keep everything local"
2. (radio empty) "SPLIT-CONTEXT HYBRID" — branching arrow icon — "route non-confidential branches outward"
3. (radio empty) "FRONTIER-ELIGIBLE" — globe icon — "allow more branches to extend outward"
Below the three cards: a small user-figure icon and the italic text "user sets the boundary before exploration".

ARROWS BETWEEN COLUMNS:
- Solid gold arrow from LEFT to CENTER (allowed flow).
- Solid gold arrow from CENTER to RIGHT (allowed non-confidential flow).
- Two RED-dashed arrows from CENTER returning to LEFT through small × symbols (blocked confidential flow).
- One additional red-dashed arrow from FRONTIER-ELIGIBLE to a × symbol on the right side of the center column (representing the conditional gate).

RIGHT COLUMN — "OPTIONAL FRONTIER EXTENSION · External thought field (optional)":
A large rounded-rectangle frame, faintly lighter than the left workspace. Inside: a wide spread of crystalline sigils (FOUR or FIVE different geometric shapes — icosahedrons, hexagonal stars, tetrahedral nests — each in a slightly different accent) connected by long sweeping dotted-gold filaments to a central glowing gold star. Outside the frame on the right: italic text "non-confidential branches may extend outward". At the bottom inside the frame: a small italic note "only non-confidential or sanitized branches extend here".

LEGEND BAR (centered below the three columns, framed): two cells —
- Solid gold line + arrow: "allowed non-confidential flow".
- Red dashed line + × marker: "blocked confidential flow".

CLOSING COPY (full-width framed pill below the legend): a small gold quill icon and large italic text "Privacy enables creativity. Toss around half-formed ideas, sensitive plans, and unfiltered thoughts inside your private workspace. You control what leaves, what stays, and how it explores."

ROUTING POSTURE BOX (small, lower-right corner): three small icon-and-text cells "confidential stays inside · you choose the boundary · explore further only when you decide".

DRAWING-NUMBER FOOTER (bottom edge, five columns): "Sovereign Node LLC · 2026 · Powered by Tilth · Drawing no. MYCEL-04 · Sheet 4 of 5".

Style: dark cosmic blueprint, warm gold dominant, single warm-red accent for blocked-flow only. The locked workspace feels protected and intimate; the frontier extension feels more spacious and external. No glossy, no neon, no flat-UI.
```

---

## Sheet 5 — MYCEL-05 — Thought Sculpting Controls

**Title:** GOLDEN QUILL — THOUGHT SCULPTING CONTROLS
**Subtitle:** *A soft-synth-like interface for shaping multi-model reasoning.*
**Closing tagline:** *Position in the shape space changes flow behavior and output quality.*
**Footer hook:** *One navigable shape space can tune one model, many models, or the whole field together.*

**Composition (the centerpiece sheet):**

```
LEFT ANNOTATIONS PANEL              CENTER (icosahedral 3D shape space)         RIGHT CONTROLS PANEL
- THOUGHT NAVIGATION POINT          (large geometric polyhedron drawn in           - GLOBAL CONTROLS
  · movable point in 3D shape space   wireframe with dense particle network         (Temperature · Breadth ·
  · position = active reasoning       inside, NOVELTY axis up, COHERENCE axis        Certainty · Synthesis Force)
  · changing position reshapes        rear-left, EVIDENCE PRESSURE axis              with numerical readouts
  field geometry and flow             rear-right; bright gold control point        - PER-MODEL CONTROLS
                                      inside; trail line showing path)              (Weight · Context Share ·
- MOVING THE POINT CHANGES                                                            Aggressiveness ·
  MODEL BEHAVIOR (3 bullets)         RIGHT-SIDE ANNOTATIONS:                         Exploration Depth)
                                     - MOVING THE POINT CHANGES FLOW                 with numerical readouts
                                       BEHAVIOR (3 bullets)                         - HOW TO USE (4 steps)

BOTTOM ROW: REGIONS OF THE SHAPE SPACE PRODUCE DIFFERENT FLOW PATTERNS
  - EXPLORATION CORNERS (high novelty)
  - INTEGRATION ZONE (high coherence)
  - EVIDENCE ANCHOR (high evidence pressure)
  - BALANCED CORE (center region)
  - EDGE MIX ZONES (trade-off regions)
  Each shown as a small icosahedron with a marker + a flow-pattern thumbnail
```

### Image-gen prompt (copy-paste)

```
Dark navy/black blueprint-style technical illustration, #0a1628 background with faint grid, decorative gold corner brackets. Warm gold/amber line work, muted ivory text. Visual feel: a 3D soft-synth interface page (Cube by Future Audio Workshop) cross-bred with an alchemical solid-geometry plate.

TITLE BLOCK (top, centered): large serif gold caps "GOLDEN QUILL — THOUGHT SCULPTING CONTROLS", italic subtitle "A soft-synth-like interface for shaping multi-model reasoning." Top-right badge: "MYCEL SERIES · SHEET 5 OF 5".

CENTERPIECE — A LARGE 3D ICOSAHEDRON / GEODESIC POLYHEDRON drawn in gold wireframe occupying the center 50% of the plate. The polyhedron is semi-transparent and full of dense gold particle-and-filament texture inside (suggesting a navigable volumetric field). Three labeled axes radiate from the center:
- "NOVELTY (explore / diverge)" pointing UP
- "COHERENCE (align / integrate)" pointing to the LOWER-LEFT
- "EVIDENCE PRESSURE (validate / constrain)" pointing to the LOWER-RIGHT
Inside the polyhedron, a bright gold THOUGHT NAVIGATION POINT is positioned slightly off-center, with a faint curved trail showing where it has moved from. A second smaller marker on a face shows a previous position. Tick marks along the axes give a measurement feel.

LEFT ANNOTATIONS COLUMN (two stacked framed boxes connected to the centerpiece by dotted lines):
BOX 1 — heading "THOUGHT NAVIGATION POINT" with three bulleted sub-points each with a small icon:
- "Movable point in 3D shape space"
- "Position = active reasoning stance"
- "Changing position reshapes field geometry and flow"
BOX 2 — heading "MOVING THE POINT CHANGES MODEL BEHAVIOR" with three bulleted sub-points:
- "Shifts model priors and attention bias"
- "Alters trade-offs between creativity, consistency, and evidence"
- "Modifies acceptance thresholds and stopping criteria"

RIGHT ANNOTATIONS COLUMN (one framed box, connected to the centerpiece by dotted lines):
heading "MOVING THE POINT CHANGES FLOW BEHAVIOR" with three bulleted sub-points each with a small icon:
- "Changes propagation paths through the field"
- "Reweights which models influence the field"
- "Affects convergence speed and diversity of outcomes"

FAR-RIGHT CONTROLS COLUMN (three stacked framed panels):
PANEL A — "GLOBAL CONTROLS" with four labeled sliders, each row: small icon + label + horizontal slider track + circular handle + numerical readout. Rows:
- thermometer · TEMPERATURE · cold ↔ hot · 0.62
- particle-cluster · BREADTH · narrow ↔ wide · 0.71
- target/crosshair · CERTAINTY · low ↔ high · 0.58
- spiral · SYNTHESIS FORCE · blend ↔ fuse · 0.67
PANEL B — "PER-MODEL CONTROLS" with four labeled sliders:
- weight-bar · WEIGHT · min ↔ max · 0.64
- pie-share · CONTEXT SHARE · low ↔ high · 0.53
- bolt · AGGRESSIVENESS · conservative ↔ bold · 0.47
- stacked-layers · EXPLORATION DEPTH · shallow ↔ deep · 0.69
PANEL C — "HOW TO USE" with a small compass icon and four numbered short-line steps:
1. Position the point in the shape space to set your reasoning stance.
2. Adjust global controls to shape the entire thought field.
3. Tune per-model controls to steer individual contributors.
4. Observe flow and outputs; refine position and controls iteratively.

BOTTOM ROW — "REGIONS OF THE SHAPE SPACE PRODUCE DIFFERENT FLOW PATTERNS & OUTPUT QUALITIES" (full-width framed bar, heading centered): five equal cells each containing TWO small thumbnails (left: a small icosahedron with a glowing marker in the relevant region; right: a small flow-pattern diagram), with a heading + sub-label + two-line description:
- EXPLORATION CORNERS · "high novelty" · marker at a top corner · diverging-arrow flow · "Divergent, creative, high variance · Outputs: ideas, hypotheses, alternatives"
- INTEGRATION ZONE · "high coherence" · marker at lower-left corner · converging-curve flow · "Convergent, consistent, low variance · Outputs: summaries, syntheses, plans"
- EVIDENCE ANCHOR · "high evidence pressure" · marker at lower-right corner · constrained-anchor flow · "Constrained, verified, rigorous · Outputs: checks, citations, validation"
- BALANCED CORE · "center region" · marker at center · stable-radial flow · "Stable, well-rounded, adaptive · Outputs: general reasoning, guidance"
- EDGE MIX ZONES · "trade-off regions" · marker on an edge midpoint · hybrid-curve flow · "Hybrid behavior, nuanced trade-offs · Outputs: nuanced, comparative, what-if"

LEGEND BAR (small, lower-left, single row): four cells with small icon + label —
- glowing dot "NAV POINT"
- bidirectional arrows "FLOW PATHS"
- gridded shape "FIELD GEOMETRY"
- concentric rings "OUTPUT QUALITY"

CLOSING TAGLINE BAR (lower-left, framed pill): a small icosahedron icon and italic text "One navigable shape space can tune one model, many models, or the whole field together."

DRAWING-NUMBER FOOTER (bottom-right, multi-line): "Sovereign Node LLC · 2026 · Powered by Tilth · Drawing no. MYCEL-05 · Sheet 5 of 5".

Style: this is the centerpiece sheet — the visualization is the most volumetric and intricate of the set. The icosahedron should feel navigable, like you could move the point yourself. Inspired by Cube by Future Audio Workshop's 3D morph-space interface. Dark cosmic blueprint, warm gold, no glossy, no neon, no flat-UI.
```

---

## Optional creative-mandate expansions (per Josh's "lets be creative" directive)

Three additional sheet concepts that lean into the references he named (projection-mapping filters, AlphaGo option-space, VST/soft-synth packaging, human × AI participation). File them as MYCEL-06 / 07 / 08 if added — or skip if the 5-sheet set is the desired scope.

### Optional Sheet — MYCEL-06 — The Filter Stack

**Concept:** Operations as filters in a real-time stream — projection-mapping inspiration. The thought stream flows top-to-bottom through a stack of named filters (Privacy Gate · Topology Selector · Per-Model Modulators · Global Modulators · Synthesis Curve), each filter with a small parameter row. The stream visibly transforms as it passes each filter.

### Optional Sheet — MYCEL-07 — The Option Space

**Concept:** Wide-aspect option-space visualization. A vast particle field with thousands of dim potential branches; the human + AI navigation reveals a small subset as bright threads. Caption: *MyCel surfaces possibilities the human alone would not have seen.* The visual point is that the field is much larger than any single linear answer — the controls are how you navigate it.

### Optional Sheet — MYCEL-08 — The Jam Session

**Concept:** Human + AI as collaborators, not supervisor + tool. Show a single human silhouette at the center of the field with model crystals around them, all responding to a shared rhythm. Frame as a jam session: each model takes solos, swaps roles, comps under another's lead. Caption: *Models take different roles at different times. The point is the new thought.*

---

## Production notes

- All five sheets ship as PNGs at large landscape dimensions (1600×1000 or 1920×1200 work well for blueprint-style aesthetics).
- The crystalline model sigils should stay CONSISTENT in shape and color across sheets so the same "Model A" reads as the same model on every plate.
- Drawing numbers are stable across regeneration. If a sheet is regenerated, its drawing number does not change.
- If image-gen drifts toward modern-flat-UI styling, prepend "no flat-UI iconography, no neon, no glossy textures, no rounded-square chrome — instead, technical-blueprint engraving feel" to the prompt.
- "TouchDesigner" deliberately omitted from customer-facing copy (CLC v2 §3.1 corrected hierarchy keeps it as the substrate beneath, not the user-facing name).
- Architecture LOCK convention unchanged. These plates depict MyCel-the-interface, not the seat-based council underneath. Both are simultaneously true.
