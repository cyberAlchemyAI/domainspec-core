# L0 — Corpus & Source Record

Date checked: 2026-06-16. All sources accessed via web search/summary; **none read in full**.
This is the source boundary: claims drawn from these are labeled `primary-source` /
`related-source` in `claim-ledger.md`; everything else is inference or operator-reading.

## Sources in the corpus

| # | Source | Kind | URL | What it grounds |
|---|---|---|---|---|
| S1 | TidalCycles | live-coding pattern language | https://tidalcycles.org/ · https://en.wikipedia.org/wiki/TidalCycles | Live-coding surface; mini-notation; pattern functions; SuperCollider/SuperDirt; OSC/MIDI; algorave use |
| S2 | Xenakis — Dynamic Stochastic Synthesis / GENDYN | algorithmic synthesis method | https://www.iannis-xenakis.org/en/stochastic-synthesis/ · https://hal.science/hal-02986346v1/document | "Stochastic synth": waveform as a polygon deformed by random walks; spectrum is *emergent*, not designed |
| S3 | Sethares — *Tuning, Timbre, Spectrum, Scale* | psychoacoustics / theory | https://sethares.engr.wisc.edu/ttss.html · https://en.wikipedia.org/wiki/William_Sethares | "Dissonance scale": sensory dissonance depends on timbre↔tuning alignment; computable dissonance curves (Plomp–Levelt) |
| S4 | NIME (New Interfaces for Musical Expression) | HCI / instrument design field | https://en.wikipedia.org/wiki/New_Interfaces_for_Musical_Expression | The DMI triad: controller → mapping → sound engine; ergonomics + gesture-sound mapping as a design discipline |
| S5 | Strasheela | declarative constraint composition | https://github.com/tanders/strasheela · http://www.algorithmic.net/system/strasheela | "Spec-driven music": user declares a music theory as a CSP; computer generates compliant music; outputs MIDI/Csound/Lilypond |
| S6 | AI music agents (Soundverse and similar) | contrast case (the approach to avoid) | https://www.soundverse.ai/blog/article/ai-music-agents-explained | Prompt→model→finished-audio agents; voice commands orchestrating generation. The *anti-pattern* for this project |

## Corpus boundary — what is NOT in scope here

- **Not read in full:** none of S1–S6 were read end-to-end; summaries only. Specific algorithm
  details (e.g. exact GENDYN random-walk bounds, Plomp–Levelt parameters) are `open-residue`.
- **Not covered:** Sonic Pi, SuperCollider internals, ChucK, Max/MSP, FoxDot, Gibber,
  Overtone — adjacent live-coding/synthesis systems that would deepen the survey but were not
  pulled. Listed as future work.
- **No empirical evidence** of whether a dissonance-curve objective actually produces perceived
  "strangeness" in listeners. That is an evidence-harness question, not a source-reading one
  (see `bridge-decisions.md` → evidence handoff).
- **The operator's design question itself** ("what communication processes could the studio
  have?") is not answered by any single source. The taxonomy in `findings.md` is synthesis
  (`local-inference` / `operator-reading`), grounded in but not stated by the corpus.
