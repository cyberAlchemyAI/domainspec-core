# Educational Video Voiceover v2 Validation

Validated: `2026-08-05`

Transport: `educational_video_candidate`

Result: `pass` as a full narration draft, with recording and synchronization residue

## Artifact boundary

| Artifact | SHA-256 | State |
|---|---|---|
| `educational-video-voiceover-v2.md` | `94dc3b54fea0562e1e6c28feea79dce9e66ca43be0609b5bdb8e125a379d69c9` | Conversational full-draft candidate |
| `educational-video-voiceover.md` | `c658410ed6a595533f50b1eb274400af01862b6e092c5b33415bef1ad617a41a` | Existing synchronized voiceover; unchanged |
| `educational-video-production-script.md` | `ee5a3d5b2eae53cc712d2904971164a52d4e7ca248881ab2d1490cece7610784` | Existing production score; unchanged |
| `educational-video-captions.vtt` | `aea66578bc3a192fa8c34f94088acee3880515d1f5dd416a31a38aee5c530358` | Existing captions; unchanged |

The new draft does not silently replace the synchronized package. Captions, picture timing, screen text, transitions, teleprompter surfaces, and HTML must be regenerated only after the wording is accepted.

## Timing validation

| Start | Section | Words | Effective WPM to next boundary |
|---:|---|---:|---:|
| 00:00 | A bounded model of a world | 114 | 120.0 |
| 00:57 | The same idea in different contexts | 119 | 123.1 |
| 01:55 | A genuine approval | 145 | 120.8 |
| 03:07 | Time, confidence, and authority | 128 | 120.0 |
| 04:11 | Putting the world around the record | 106 | 122.3 |
| 05:03 | The meaning carried by relationships | 114 | 126.7 |
| 05:57 | Confidence is not commitment | 89 | 121.4 |
| 06:41 | From evidence to an authority gate | 117 | 121.0 |
| 07:39 | Building useful context for an agent | 150 | 120.0 |
| 08:54 | The Augmentor bridge | 189 | 121.9 |
| 10:27 | The complete movement | 124 | 122.0 |
| 11:28 | What should survive | 126 | 121.9 |

- Sections: 12
- Total spoken words: 1,521
- Target duration: 12:30
- Average pace: approximately 121.7 WPM
- Pace band: pass — every section remains within the requested 120–130 WPM range

The timecodes remain editorial targets. The final captions and cuts must follow the recorded waveform.

## Intent and delivery checks

| Check | Result |
|---|---|
| Opens with a definition rather than a dramatic case | pass |
| Defines ontology as a knowledge space and bounded world model | pass |
| Names types, classes, definitions, interactions, time, confidence, provenance, lifecycle, ownership, and use conditions | pass |
| Establishes multiple contexts before selecting one case | pass — healthcare, organizations, and agents |
| Keeps the organizational example concrete | pass — citywide grants program versus prior two-neighborhood pilot |
| Avoids software-engineer framing | pass — no software-engineer or graph-engineering setup |
| Avoids cinematic science-video hooks | pass — no “everyone is talking,” “let me show,” “imagine,” or “look closely” construction |
| Reads as explanation rather than keynote copy | pass — three-moment conversational audition approved; full recording evidence pending |
| Uses conversational cues to guide conceptual turns | pass — questions, short answers, callbacks, and transitions are present without prefixing every paragraph |
| Uses each section for one primary job | pass |
| Ends once, without restating the full model twice | pass |

## Meaning and authority checks

| Check | Result |
|---|---|
| Earlier approval remains genuine | pass |
| Old approval is not treated as current permission | pass |
| Time, confidence, and authority remain independent | pass |
| Glossary, taxonomy, and ontology remain distinct | pass |
| DomainSpec relation meaning does not imply runtime conformance | pass |
| Body War availability does not imply promotion or commitment | pass |
| Source, evidence, candidate, owner gate, and governed meaning remain separate | pass |
| Memory, context builder, ontology, owner, and runtime remain separate roles | pass |
| Context packet remains a task view, not a new source of truth | pass |
| Augmentor request stops at the owner gate | pass |
| Augmentor retains `authority_effect: none` | pass |
| Ontology package is not claimed as proof of runtime features or release | pass |

The healthcare context is illustrative and does not claim a specific medical ontology, clinical recommendation, or treatment rule.

## Distill trace

### Round 1

- **Proposer claim:** add spoken signposts at conceptual transitions and turn dense exposition into short question-and-answer movements.
- **Evidence/assumption:** the operator approved the conversational opening, approval tension, and owner-gate reveal.
- **Balancer objection — performance-density risk:** adding a cue to every paragraph would sound scripted, slow the narration, and replace one mechanical rhythm with another.
- **Reconciliation:** use one cue per conceptual turn, retain uncued explanatory paragraphs, and compress repeated setup language until every section returns to the target pace band.

### Round 2

- **Proposer claim:** return to the approval example as a conversational callback instead of restarting the explanation in each section.
- **Evidence/assumption:** the example already carries time, confidence, authority, relationships, context selection, and the owner gate.
- **Balancer objection — semantic-boundary risk:** conversational compression could blur evidence, candidate interpretation, governed meaning, authority, and runtime proof.
- **Reconciliation:** shorten syntax while preserving the independent questions, explicit owner gate, `authority effect: none`, and the distinction between a model and runtime evidence.

## Smallest coherent unit and recomposition

The conceptual anchor remains the approved two-level definition:

> Ontologies are knowledge spaces. They describe a part of the world we want to understand.
>
> More precisely, they are world models: types, classes, and definitions name the things in that world, while relationships describe how those things interact and what those interactions mean.

The selected delivery unit is one conversational turn: an entry cue, one idea, and either its consequence or the next question. It recomposes into the narration without changing the conceptual anchor:

1. “So what does that look like?” moves from definition to contexts;
2. “Let’s make this concrete” introduces the approval case;
3. “So what’s missing?” separates time, confidence, and authority;
4. callbacks to the approval explain relationships and the authority gate;
5. “So where does memory fit?” connects the model to agent context;
6. “And that brings us to Augmentor” introduces the proposed bridge;
7. the closing takeaway returns to the approved owner-boundary reveal.

## Open residue

- The operator approved the three-moment conversational voice direction; the resulting full draft has not yet been approved sentence by sentence.
- No voice recording or read-aloud performance has been evaluated.
- No listener-comprehension evidence exists.
- The existing WebVTT captions do not match v2.
- The production picture score and transition inventory still follow v1 timing and sequence order.
- The presentation HTML and any teleprompter derivative have not been regenerated.
- No audio has been processed through OBS, Auphonic, or another enhancement route.

## Verdict

The v2 narration passes its text-level structure, duration, conversational-flow, and authority checks. It carries the approved voice direction through all twelve sections and is ready for operator wording review and a short full-script recording audition. It is not yet a synchronized production package, accepted waveform, rendered video, or audience-proven explanation.
