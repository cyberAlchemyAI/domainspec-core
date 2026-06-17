# Claim Ledger

Every load-bearing claim with its source kind. Labels: `primary-source` (stated by the named
source), `related-source`, `local-inference` (reasoned from sourced material), `analogy` (Arcanum/
design mapping, not source meaning), `operator-reading` (design interpretation for the operator),
`open-residue` (unresolved).

## Source-grounded claims

| ID | Claim | Source kind | From |
|---|---|---|---|
| C1 | TidalCycles is a live-coding DSL (embedded in Haskell) for improvising/composing music via terse "mini-notation" patterns and a library of pattern-transform functions; sound via SuperCollider/SuperDirt; controls other synths via OSC/MIDI; used at algoraves. | primary-source | S1 |
| C2 | Xenakis's dynamic stochastic synthesis (GENDYN) treats the waveform as a polygon of breakpoints deformed over time by random walks; **spectral/frequency attributes are emergent** from the probabilistic process, not designed in the frequency domain. | primary-source | S2 |
| C3 | Sensory consonance/dissonance is **not fixed to intervals** — it depends on alignment between a sound's timbre/spectrum and the tuning; dissonance curves (Plomp–Levelt) make it **computable** for a given spectrum, so scales can be chosen to hit target dissonance. | primary-source | S3 |
| C4 | A digital musical instrument decomposes into **controller → mapping → sound engine**; the *mapping* (how gesture connects to sound) is a primary design discipline, and ergonomics + gesture-sound mapping drive expressivity. | primary-source | S4 |
| C5 | Strasheela lets a user **declaratively state a music theory as a constraint-satisfaction problem**; the system deterministically generates compliant music and outputs MIDI/Csound/Lilypond. Spec-driven composition is a proven, pre-LLM technique. | primary-source | S5 |
| C6 | Current "AI music agents" accept voice/text commands and orchestrate **generative models** to produce/modify finished audio (stems, extend, master). | related-source | S6 |

## Design claims (the operator's question lives here — labeled honestly)

| ID | Claim | Source kind | Basis |
|---|---|---|---|
| C7 | The operator's example decomposes into **intent→spec→deterministic-realization** plus **objective-driven search**, with no generative model producing sound. | local-inference | C2+C3+C5 + the example text |
| C8 | A generative model, if present, belongs only as a **front-end parser** of intent into a governed, artisan-editable spec vocabulary (a compiler front-end), never as the sound producer — this is what preserves craft and reproducibility. | local-inference | contrast C6 vs C5; operator's "not relying on models" |
| C9 | "Bring strangeness to the listener" is a **perceptual objective** that can be partially operationalized as a computable target (e.g. target dissonance/roughness/tension), letting the agent search engine parameters toward it. | local-inference | C3 (+ unverified that the metric matches felt "strangeness" → O1) |
| C10 | Every interface surface (voice, live-code, gesture, annotation, dialogue) can be modeled as an **editor of one shared, reproducible spec** — the spec is the lingua franca that unifies modalities. | operator-reading | C5 + DomainSpec design stance |
| C11 | "Interface as communication process" is best taxonomized by **speech-act + who-leads-when**, a layer above raw modality; ten such processes are identified (`findings.md`). | operator-reading | C4 framing + synthesis |
| C12 | A reverse channel — **agent → human perceptual feedback** (showing what it perceives: spectrum, dissonance meter, predicted listener effect) — is the ergonomic keystone of human-agent symbiosis in the studio. | operator-reading | ergonomics-first principle + C3 |

## Open residue (claims we cannot make yet)

| ID | Open question | Why unresolved |
|---|---|---|
| O1 | Does a Sethares/Plomp–Levelt dissonance target actually predict perceived "strangeness"? | needs listener evidence → evidence-harness, not source-reading |
| O2 | Can natural-language timbre adjectives ("dark", "violin", "strange") be reliably compiled to spectral-feature specs with a *governed* (non-model) vocabulary? | unverified; depends on building the vocabulary |
| O3 | What latency/ergonomics budget does voice control need to feel like an instrument rather than a remote? | NIME-adjacent (C4) but unmeasured here |
| O4 | How do adjacent systems (Sonic Pi, ChucK, Max/MSP, FoxDot) change the surface taxonomy? | corpus boundary — not pulled |
