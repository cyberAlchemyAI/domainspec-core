# Glossary

Quick reference. Each entry: source kind · local meaning · (warning where misuse is likely).
Governed, load-bearing terms are expanded in `definitions.md`.

| Term | Source kind | Local meaning |
|---|---|---|
| **Agentic music studio** | operator-reading | A studio whose intelligence is deterministic engineering + objective-driven search over a shared spec — *not* prompt-to-audio generation. The human supplies intent and aesthetic judgment; the agent engineers toward it. |
| **Spec (musical spec)** | operator-reading | A reproducible, version-controllable document declaring musical intent and constraints. The lingua franca every interface edits. ⚠ Not a model prompt — a deterministic source artifact. |
| **Stochastic synthesis** | primary-source (S2) | Xenakis/GENDYN: build the waveform as a polygon deformed by random walks; spectrum is *emergent* from the process. "Dark violin stochastic synth" names an engine of this class with a violin-like, dark spectral target. |
| **Dissonance curve / dissonance scale** | primary-source (S3) | Sethares: sensory dissonance computed from a timbre's spectrum; a scale chosen so its intervals hit target dissonance values. The deterministic means behind "bring strangeness." ⚠ Computable dissonance ≠ guaranteed felt "strangeness" (O1). |
| **Timbre target** | local-inference | A spectral specification ("dark" = low centroid; "violin" = match violin partials) the engine is searched to satisfy. |
| **Objective-function steering** | local-inference | The human names a perceptual goal ("strangeness", "more bite"); the agent optimizes engine parameters against a computable metric. The heart of "agentic engineering." |
| **Communication process** | operator-reading | The *kind of message* between human and studio (command / declaration / goal / example / critique / rule-authoring …) plus *who leads when* — a layer above modality (voice/text/gesture). |
| **Modality** | reference | The surface a message rides on: voice, typed code, gesture/controller, on-timeline annotation, visual graph. One process can use several. |
| **Mapping** | primary-source (S4) | NIME: the rule connecting a controller gesture to sound-engine behavior. Where ergonomics is won or lost. |
| **Live coding** | primary-source (S1) | Writing/mutating code (e.g. TidalCycles patterns) live to make music; the artisan steers the *statistics* of output, not each note. |
| **Declarative / constraint composition** | primary-source (S5) | Strasheela: state a music theory as constraints; the system deterministically yields compliant music. |
| **Front-end parser (intent compiler)** | analogy | A model (if used) that only translates natural-language intent into governed spec fields — never produces sound. Compiler front-end, not composer. |
| **Reverse channel / perceptual feedback** | operator-reading | Agent→human surfacing of what it perceives (spectrum, dissonance meter, predicted listener effect) so human and agent share a model of the listener. |
| **Who-leads-when** | reference (ergonomics principle) | For each process: who holds initiative at each moment (human leads / agent leads / shared). An ergonomic property, not a feature. |
