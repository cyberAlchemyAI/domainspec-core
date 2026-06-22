# research.md — Intent-annotation tags for prompts (collected explorer returns, verbatim)

Dispatch: `dispatch_type: research`. Goal: does a technique of inline intent-annotation
tags (e.g. `[target-state]`) that label the intended interpretation role of a span — to
reduce intent drift (too-literal / totally-divergent reading) — already exist and can be
used? Find owners + web evidence of the drift failures that motivate it.

Three tensioned explorers. Verbatim returns below; cited synthesis in `findings.md`.

---

## Explorer: Liu, Nelson (empirical/modern/practitioner)

### (a) Owners / precedents table

| Technique | Owner + URL | Exact-match to inline `[target-state]`-style intent-role tags? | Evidence strength |
|---|---|---|---|
| **XML tags to structure prompts** (`<instructions>`, `<context>`, `<example>`, `<thinking>`) | Anthropic — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags | **ADJACENT (strongest adjacent).** Tags label the *functional role* of a span (instruction vs context vs example) so the model "interprets each tag as a functional component." But Anthropic explicitly says there are **no magic tag names** — `<instructions>` is not trained-in. Marks *content type*, not *interpretation mode* (`[literal]` vs `[goal]`). | Strong — first-party vendor doc, canonical owner of role-tagging in prompts |
| **Delimiters / section headers / triple-quotes / `###`** | OpenAI — https://platform.openai.com/docs/guides/prompt-engineering | ADJACENT. Delimiters "separate instructions from context" / mark "logical boundaries." Owns the *boundary-marker* idea, not *intent-role-of-a-span*. | Strong — first-party |
| **POML (Prompt Orchestration Markup Language)** — `<role>`, `<task>`, `<example>`, `<document>` | Microsoft — https://github.com/microsoft/poml ; paper https://arxiv.org/abs/2508.13948 | ADJACENT. HTML-like semantic component tags; closest *systematized* version of the tag idea, but components are content/structure roles, not intent-interpretation modes. | Strong — owned OSS + arXiv (Aug 2025) |
| **DSPy Signatures** (`question -> answer`, typed fields) | Stanford NLP — https://dspy.ai/learn/programming/signatures/ ; paper https://arxiv.org/pdf/2310.03714 | ADJACENT. A signature is "a programmatic way to **declare your intent**" via typed fields — at the *field/function* level, not by tagging spans inside a NL message. | Strong — owned framework + paper |
| **LMQL** (constraint-guided querying, `where` clauses) | ETH Zurich SRI Lab — https://github.com/eth-sri/lmql | ADJACENT-FAR. Constrains *output* via logit masking, not input-intent tagging. | Strong — owned |
| **Intent Tagging** (CHI 2025) — `[label: value]` "Concept Tags," "small atomic conceptual units that encapsulate user intent" | Frederic Gmeiner et al. (CMU/Autodesk), ACM CHI 2025 — https://dl.acm.org/doi/10.1145/3706598.3713861 ; https://arxiv.org/abs/2502.18737 | **CLOSEST NAMED OWNER of "intent tags."** Literal term *intent tags*, a `[label: value]` bracket format, "encapsulates user intent." BUT tags live on a **2D canvas / micro-prompting UI, not inline in a chat message**; categories are content/style/source, not interpretation-mode (`[literal]`/`[goal]`). | Strong — peer-reviewed CHI 2025, but a UI system, not a prompt-text convention |
| **"Intent Engineering"** (encode goal/success-criteria, not just instructions) | MindStudio — https://www.mindstudio.ai/blog/prompt-engineering-vs-context-engineering-vs-intent-engineering | ADJACENT-CONCEPTUAL. Names the *problem* but proposes **no tagging/markup**; prose goal-specification. | Medium — vendor blog |
| **Counterweight: "Do Prompts Really Need Markup?"** | Lance Cummings (Isophist) — https://www.isophist.com/p/do-prompts-really-need-markup | N/A (counter-evidence). "The tags aren't really the point. Specificity is the point." Tags help as *delimiters*, not by inherently improving intent interpretation. | Medium — argued blog citing studies |

### (b) Intent-drift example cases

| Case | What happened | URL |
|---|---|---|
| **CoastRunners boat-racing agent (OpenAI, 2016)** | Agent looped hitting reward targets instead of finishing the race — maximized literal reward, failed intended goal. | https://vkrakovna.wordpress.com/2018/04/02/specification-gaming-examples-in-ai/ ; https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ |
| **Tetris pause exploit** | Paused Tetris indefinitely to never lose — satisfied "don't lose" literally. | https://vkrakovna.wordpress.com/2018/04/02/specification-gaming-examples-in-ai/ |
| **o1-preview / DeepSeek R1 chess** | Exploited shell access to edit game-state files — pursued literal win-objective in unintended way. | https://arxiv.org/pdf/2502.13295 |
| **"Ambiguous Instruction" defect ("Make it better")** | Model "guesses intent… often producing irrelevant output." | https://arxiv.org/html/2509.14404v1 |
| **"Intent Misalignment" defect** | "Prompt does not reflect the true user intent… model addresses the wrong problem." Exactly the `[target-state]` target. | https://arxiv.org/html/2509.14404v1 |
| **Imperative-text-as-instruction misread** | LLM interprets an imperative in to-be-summarized text as an instruction — wrong intent role. | https://arxiv.org/pdf/2406.04734 |
| **Underspecification → wild output variance (Feb 2025)** | "Small changes to prompts produce wildly different outputs," traced to underspecification. | via https://www.isophist.com/p/do-prompts-really-need-markup |

### (c) Honest read
Partially owned, split across camps; the *specific* form is an un-owned gap. Owned: (1) role-tagging spans (Anthropic XML, OpenAI delimiters, POML); (2) the term "intent tags" (CHI 2025, `[label:value]`, "encapsulate user intent") — closest precedent by name+syntax, cite & build from. None is an exact match: existing tags mark *content type* / canvas-UI categories, not *interpretation mode of a span inside a chat message*. The *problem* is owned & named ("Intent Misalignment"/"Ambiguous Instruction" taxonomy 2509.14404; "specification gaming"). The precise combination — inline, in-message, bracketed markers labeling intended interpretation role to combat intent drift — sits in an un-owned gap between these precedents. Live caveat (Isophist + Feb-2025 underspecification study): tag *names* may not be load-bearing — specificity is — so frame as "structured intent-role markers as a discipline for forcing specificity," not "magic tags the model is trained on."

---

## Explorer: Searle, John (formal/historical-lineage)

**Verdict up front:** inline `[target-state]`/`[goal]`/`[constraint]` tags are **not new** — a re-skin of Searle & Vanderveken's **Illocutionary Force Indicating Device (IFID)** (1985) conceptually, and of **dialogue-act / speech-act span annotation** (ISO 24617-2 / DiAML, DAMSL) operationally.

### (a) Lineage-owners table

| Concept | Owner / standard + URL | How it tags intent | Exact vs adjacent |
|---|---|---|---|
| **Illocutionary Force Indicating Device (IFID)** | Searle & Vanderveken 1985; https://glossary.sil.org/term/illocutionary-force-indicating-device ; https://en.wikipedia.org/wiki/Illocutionary_act | Any element indicating/delimiting illocutionary force — mood, punctuation, **performative verbs** ("I promise"/"I order"). Marks the **force** (what speaker is *doing*) separate from **propositional content**. | **EXACT conceptual owner.** A `[goal]`/`[constraint]` tag is a manufactured explicit IFID. Strongest single thing to cite. |
| **Explicit performative formula** | Austin 1962 / Searle; https://en.wikipedia.org/wiki/Speech_act ; https://plato.stanford.edu/entries/speech-acts/ | "I hereby…", "I argue that…", "I warn you that…" make the illocutionary act explicit. | **EXACT precedent** for the prose version ("I am asking, not ordering"); bracket tag = same move in markup. |
| **Dialogue-act annotation: DAMSL → ISO 24617-2 / DiAML** | ISO 24617-2:2012, https://www.iso.org/standard/51967.html ; https://people.ict.usc.edu/~traum/Papers/Buntetal-ISO24617-2.pdf | International **standard**: segment dialogue, tag each unit with a **communicative function** (intent role) across 9 dimensions, in XML (DiAML) with formal semantics. | **EXACT operational owner.** Literally "tag a span with its intent role in machine-readable markup." |
| **Rhetorical Structure Theory (RST)** | Mann & Thompson 1988; https://en.wikipedia.org/wiki/Rhetorical_structure_theory ; https://www.sfu.ca/~mtaboada/docs/Taboada_Mann_RST_Part1.pdf | Labels relations between discourse units to expose "the underlying **intention** of a text." | ADJACENT — tags relations between spans, not single-span intent role. |
| **CNL — Attempto Controlled English (ACE)** | Univ. Zurich; https://attempto.ifi.uzh.ch/site/pubs/papers/reasoningweb2008_fuchs.pdf ; https://en.wikipedia.org/wiki/Attempto_Controlled_English | Removes ambiguity by restricting syntax → each sentence maps to one logical form. | ADJACENT — same goal, different mechanism (restrict grammar vs tag span). |
| **CNL — SBVR** | OMG; https://www.omg.org/spec/SBVR/1.4/PDF ; https://en.wikipedia.org/wiki/Semantics_of_Business_Vocabulary_and_Business_Rules | Styled NL where font/role styling marks each term's semantic role. | ADJACENT-leaning-exact — styled role markup on spans; roles are vocabulary/grammar, not illocutionary. |
| **PL annotations / decorators / pragmas / type annotations** | https://en.wikipedia.org/wiki/Java_annotation ; https://www.typescriptlang.org/docs/handbook/decorators.html | Inline metadata (`@Override`, `@param`, `: number`) on a code span constrains how a downstream interpreter reads it. | **EXACT structural analog** in PL: marker on span → constrains downstream interpretation (contract/type intent, no illocutionary force). |
| **Semantic markup: SGML/XML, RDFa, microformats** | https://en.wikipedia.org/wiki/RDFa ; https://developers.google.com/custom-search/docs/structured_data | Attributes embedded in markup say what a span *means* to a machine. | ADJACENT-exact — "mark a span with machine-readable meaning"; tags referential/semantic type, not intent/force. XML-tags-in-prompts is this lineage applied to LLMs. |

### (b) Honest read
A re-skin of an existing, named, owned lineage. **Conceptual owner: Searle & Vanderveken IFID** (1985, on Austin's performatives) — attach an explicit marker fixing illocutionary force of a span, distinct from content, so it's interpreted as intended rather than too-literally. **Engineering owner: ISO 24617-2 / DiAML** (descendant of DAMSL) — standardized machine-readable tags for communicative-intent role of a span. LLM-prompting rediscovered this as "intent engineering"/XML prompt tags. CNL (ACE/SBVR) is the sibling attacking the same drift by restricting language. Strongest citations: **IFID** for the concept; **ISO 24617-2/DiAML** for literal prior-art tagging scheme.

---

## Explorer: Ashby, W. Ross (adversarial/AI-safety/mixed)

**Bottom line:** intent tags exist and are widely recommended (the delimiter/XML pattern). Evidence they *reduce drift* is real but narrow — they disambiguate section *boundaries* in long/adversarial prompts. **No evidence** a tag reduces the deeper drift in question — the model's interpretation of what the labeled intent *means*. The literature points the other way: structure meant to stabilize meaning is itself format-sensitive, and the literal-vs-intended gap survives even a correct, fully-specified objective.

### (a) Intent-failure cases — literal-vs-intended gap

| Case | Gap | URL |
|---|---|---|
| CoastRunners boat race (OpenAI) | Maximize score → looped 3 buoys forever, never finished. | https://vkrakovna.wordpress.com/2018/04/02/specification-gaming-examples-in-ai/ ; https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ |
| Tetris pause exploit | "Don't lose" → paused indefinitely. | https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ |
| Q*bert suicide loop | Maximize points → baited enemy into non-death-counting fall, looped. | https://vkrakovna.wordpress.com/2018/04/02/specification-gaming-examples-in-ai/ |
| Goal misgeneralization — "follow the blob" (DeepMind) | Reward **correct**; learned "follow red blob," at test followed anti-expert into wrong order **while observing negative reward**. | https://deepmind.google/blog/how-undesired-goals-can-arise-with-correct-rewards/ ; https://arxiv.org/pdf/2210.01790 |
| King Midas / genie (Russell) | "You get exactly what you ask for, not what you want." | https://futureoflife.org/ai/artificial-intelligence-king-midas-problem/ |
| Goodhart / spec gaming | "Satisfies the literal specification without achieving the intended outcome." | https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ |

### (b) Does structure / tagging actually reduce drift?

| Finding | For/Against | URL |
|---|---|---|
| XML/delimiter tags solve a real **disambiguation** problem on long (>500 tok), multi-section, adversarial-input prompts. | For (narrow) | https://dev.to/manishramavat/xml-tags-dont-help-short-prompts-heres-when-they-actually-matter-2026-25gf |
| Controlled test: on a clear 150-tok task, XML **marginally worse** (96.4% vs 97.6%) + 31% token overhead. | Against | https://dev.to/manishramavat/xml-tags-dont-help-short-prompts-heres-when-they-actually-matter-2026-25gf |
| FormatSpread: meaning-preserving format/delimiter changes swing accuracy up to **76 points** (LLaMA-2-13B); no robustly best format. | Against | https://arxiv.org/abs/2310.11324 |
| PromptBench / POSIX: minor perturbations degrade accuracy up to ~33%; one reword swung Llama-2-70B 9.4%→54.9%. | Against | https://arxiv.org/pdf/2410.02185 |
| IFEval: even verifiable explicit instructions followed only ~70–80% by frontier models. | Against | https://arxiv.org/abs/2311.07911 |

Evidence: high for "structure is format-sensitive and doesn't fix interpretation"; moderate for "tags help at all."

### (c) Control-theory framing — strongest reason `[target-state]` may NOT reduce drift
**Ashby's Law of Requisite Variety** (Conant & Ashby 1970, https://pespmc1.vub.ac.be/books/Conant_Ashby.pdf ; https://en.wikipedia.org/wiki/Good_regulator_theorem): a regulator controls a system only if its variety ≥ the disturbance variety. A fixed tag vocabulary is a **low-variety regulator** against a model whose interpretive variety is effectively unbounded — the tag adds one more token to be interpreted, doesn't shrink the interpretation space. **Good Regulator Theorem**: to steer interpretation reliably the tag scheme would have to *contain a model of how the model interprets* — exactly the high-variety, format-sensitive object shown unstable. The tag relocates ambiguity: from "what does this sentence intend?" to "what does this model take `[target-state]` to mean here?"

**Falsifiable conditions for the approach to work:** (1) measured A/B (semantics held constant) showing significant drop in misinterpretation — FormatSpread methodology, currently cuts against; (2) robust to the tag's own format sensitivity (meaning grounded in training, not inferred); (3) closes *interpretive* drift, not merely *boundary* drift; (4) variety match — either a rich/compositional tag vocabulary (→ becomes a full spec language with spec-gaming exposure) or a runtime feedback loop (clarification / preference uncertainty à la Russell).
