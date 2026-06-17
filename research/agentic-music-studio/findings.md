# Findings — The Communication-Process Taxonomy

This is the direct answer to the operator's question: *what types of interfaces, as communication
processes, could this studio have?*

A **communication process** = `(speech-act, who-leads-when)` — a layer above modality (voice / text /
gesture / annotation / graph). The same modality (e.g. voice) can carry several processes. Design
the *processes* first; assign modalities second.

Every process below edits the **one shared spec** (D1). That is what lets them coexist: voice, code,
a knob, and a timeline scribble are all editors of the same reproducible document.

Source labels: most processes are `operator-reading`/`local-inference` syntheses grounded in the
named source. The taxonomy is design, not a source result (C11).

---

## The ten processes

Threaded through with the operator's example: **"create some dark violin stochastic synth, then use
some dissonance scale to bring a strangeness to the listener."**

### 1. Imperative / command — *"do this now"*
- **Speech-act:** direct instruction. **Leads:** human leads, agent executes.
- **Modalities:** voice ("mute the bass"), typed eval (TidalCycles `d1 $ ...`), a button/knob.
- **In the example:** "create … synth" — the trigger that spins up an engine.
- **Ergonomics:** lowest cognitive load for *known* atomic actions; high friction for complex
  intent (you'd be dictating a paragraph). Best as the fast path for small, reversible moves.
- **Grounding:** TidalCycles live-eval (S1, C1).

### 2. Declarative / spec — *"this should be true"*
- **Speech-act:** declare a constraint/intent that persists. **Leads:** human declares, agent keeps
  it satisfied continuously.
- **Modalities:** the spec document itself; a constraint editor; voice ("the bass must never clash
  with the kick's fundamental").
- **In the example:** "dark", "violin-like", "stochastic" become persistent spec fields the engine
  must keep satisfying.
- **Ergonomics:** highest leverage per word; the constraint holds even as everything else changes.
  This is the studio's **backbone** — every other process ultimately writes here.
- **Grounding:** Strasheela declarative CSP (S5, C5).

### 3. Intent / semantic naming — *"a dark violin stochastic synth"*
- **Speech-act:** name an aesthetic target in natural language. **Leads:** human names, agent
  *compiles* the name into spec fields via a **governed, artisan-editable vocabulary** (timbre
  adjectives → spectral features) — a front-end parser, never a sound generator (C8, D2).
- **Modalities:** voice or text.
- **In the example:** the whole phrase "dark violin stochastic synth" is one intent utterance.
- **Ergonomics:** the most natural entry point; the friction is *vocabulary drift* — "dark" must
  resolve to a defined spectral target the artisan can inspect and edit, or it becomes a black box.
- **Grounding:** contrast S6 (which sends the same phrase to a model) vs. the compiler-front-end
  stance (C8). Open: O2 (can the vocabulary be governed, not learned?).

### 4. Objective / goal steering — *"bring a strangeness to the listener"*
- **Speech-act:** name a perceptual *target effect*; let the agent search toward it. **Leads:**
  human sets the goal + judges; **agent leads the search**.
- **Modalities:** voice/text to set the target; a slider for target dissonance/roughness/tension.
- **In the example:** "bring strangeness" → agent computes a dissonance curve for the chosen timbre
  (S3) and searches scales/tunings that land on the target (D3, D5).
- **Ergonomics:** the operator's key idea made literal — you state the *what*, the agent finds the
  *how*. Friction risk: the metric is a proxy (O1); the studio must show *which* objective it's
  optimizing and let you correct it.
- **Grounding:** Sethares (S3, C3, C9).

### 5. Demonstrative / by-example — *"like this"*
- **Speech-act:** point at a reference (a clip, a past take, an audio region) and say "match this."
  **Leads:** human points, agent analyzes + fits parameters (analysis/retrieval — **no generation**).
- **Modalities:** drag a file, select a region, hum a phrase (analyzed for contour, not generated
  from).
- **In the example:** "make the strangeness *like* that Penderecki passage" → extract its dissonance
  profile, set it as the target for #4.
- **Ergonomics:** powerful when intent is easier to *show* than to *name*; keeps craft because the
  example seeds an editable spec, not a copy.

### 6. Conversational / negotiated refinement — *propose → critique → adjust*
- **Speech-act:** turn-taking dialogue. **Leads:** shared; agent proposes candidates within the
  spec, human critiques, agent adjusts.
- **Modalities:** voice fits naturally (hands busy); also chat. Agent **narrates what it changed**
  ("widened the random-walk bounds; centroid dropped").
- **In the example:** "too muddy" → "more bite" → "yes, keep that" while shaping the synth.
- **Ergonomics:** matches how producers actually work; the risk is the agent over-driving (becoming
  the composer). Guardrail: every accepted change writes to the spec, visibly.

### 7. Corrective / annotation — *mark the artifact*
- **Speech-act:** annotate a timeline/score in place: "here, more tension; here, resolve." **Leads:**
  human annotates, agent satisfies the annotations.
- **Modalities:** drawing on a timeline/piano-roll/spectrogram; spatial+temporal pointing.
- **In the example:** scribble "strangeness peaks here" on bar 12; the dissonance objective (#4)
  becomes time-varying.
- **Ergonomics:** unbeatable for *where/when* intent; pairs with #4 to give objectives a shape over
  time.

### 8. Generative-grammar / rule authoring — *write the process, not the notes*
- **Speech-act:** author/edit the rules and stochastic processes themselves (patterns, random-walk
  bounds, L-systems, constraints). **Leads:** human leads; this is where **craft concentrates**.
- **Modalities:** live-coding text (TidalCycles), constraint code (Strasheela), GENDYN parameter
  bounds.
- **In the example:** hand-tune the random walks of the stochastic synth; write the pattern that
  sequences the dissonant scale.
- **Ergonomics:** highest ceiling, steepest learning; the artisan controls the *statistics* of
  output. The studio's job is to make this *legible and reversible*, not to hide it.
- **Grounding:** TidalCycles (S1, C1) + GENDYN (S2, C2).

### 9. Gestural / continuous performance — *play it*
- **Speech-act:** real-time continuous expressive control. **Leads:** human leads, agent maps and
  reacts within the spec's bounds.
- **Modalities:** knobs, MIDI, sensors, breath, motion (NIME). The **mapping** (D7) is the design
  object.
- **In the example:** ride a fader that sweeps the synth's "darkness" (spectral centroid) live.
- **Ergonomics:** for the body-in-the-loop, expressive shaping; ergonomics is *won or lost in the
  mapping*, not the controller.
- **Grounding:** NIME controller→mapping→engine (S4, C4).

### 10. Ambient / perceptual feedback (agent → human) — *the reverse channel*
- **Speech-act:** the agent reports what it perceives. **Leads:** agent volunteers; human consumes.
- **Modalities:** live spectrogram, dissonance/roughness meter, "predicted listener effect: high
  strangeness", diff of what changed in the spec.
- **In the example:** as you steer toward strangeness, a meter shows the dissonance you're actually
  hitting and *where on the scale* it sits.
- **Ergonomics:** the **keystone**. Symbiosis needs a *shared model of the listener* (C12). Without
  this channel the human steers blind and the studio decays into trial-and-error. Every other
  process is improved by pairing it with #10.

---

## How the processes compose (who-leads-when matrix)

| # | Process | Human leads | Agent leads | Best modality | Craft locus |
|---|---|---|---|---|---|
| 1 | Imperative | ✔ initiative | execute | voice / eval | low |
| 2 | Declarative | ✔ declare | maintain | spec doc | medium |
| 3 | Intent naming | ✔ name | compile | voice / text | medium |
| 4 | Objective steering | set goal + judge | ✔ search | slider / voice | medium |
| 5 | By-example | ✔ point | analyze + fit | drag / hum | medium |
| 6 | Conversational | shared | shared | voice | medium |
| 7 | Annotation | ✔ mark | satisfy | timeline | medium |
| 8 | Rule authoring | ✔✔ author | assist | live-code | **high** |
| 9 | Gestural | ✔ perform | map | controller | high |
| 10 | Perceptual feedback | consume | ✔ report | meters / spectrogram | — (enables all) |

**The unifying architecture:** processes 1–9 are *write* paths into the one spec (D1, C10);
process 10 is the *read* path back. The spec is the lingua franca; modalities are interchangeable
editors; the deterministic engine + objective search (D2, D3) is the shared core. The operator's
example uses #3 (name) → #1 (create) → #4 (objective) → #8 (tune the process) → #10 (verify by ear
*and* meter) — five processes over one spec, no generative model anywhere in the sound path.
