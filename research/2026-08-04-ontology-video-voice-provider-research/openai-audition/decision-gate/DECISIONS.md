# Decision Gate: OpenAI Stock-Voice Audition

- Target scope: OpenAI stock-voice audition through the first bounded provider render.
- Profile: pilot.
- Opened: 2026-08-04T18:10:13Z.
- Current result: `BLOCK` while blocker decisions remain unresolved.
- Current admissible routing: `gate`.
- Consequential mutation permitted: none.
- Provider call permitted: none.
- Override: not requested.

## Decision sequence

| ID | Decision | Class | Dependency | Status |
|---|---|---|---|---|
| OAIA-DG-001 | Intended use scope for the first test | blocker | none | resolved: private local audition |
| OAIA-DG-002 | Accent experiment posture | blocker for render | DG-001 | resolved: two-variant private A/B; Invoke revision pending |
| OAIA-DG-003 | Voice identity and clone route | blocker for render | DG-002 | own-voice clone selected; provider/method awaiting owner choice |
| OAIA-DG-004 | Named terminal production operator | blocker for render | DG-001 | pending |
| OAIA-DG-005 | Actual-account rights/data/retention/security admission path | blocker for render | DG-001, DG-004 | pending owner evidence |
| OAIA-DG-006 | Model, region/tier, token counter, and request binding | blocker for render; technical route | DG-002, DG-003, DG-005 | pending prefilter |
| OAIA-DG-007 | Audio normalization/alignment/fidelity toolchain | blocker for render under frozen protocol | DG-001 | pending |
| OAIA-DG-008 | Listener operations and unblinding-key custody | blocker for render under frozen protocol | DG-004 | pending |

## OAIA-DG-001 — Intended use scope

**Question:** What is the intended boundary of the first OpenAI voice test?

| Option | Kind | Benefit | Cost/risk | When to choose | Downstream impact |
|---|---|---|---|---|---|
| OAIA-SCOPE-PRIVATE-LOCAL | action | Smallest real voice-quality test; no publication step | Still sends owned text to a metered external provider and needs account/data gates | You want to hear the 237-word excerpt privately before considering release | Public-use/release stays deferred; accent, voice, operator, account data, tools, and listeners still need resolution |
| OAIA-SCOPE-PUBLIC-CANDIDATE | action | Tests the configuration intended for the final public educational video | Highest rights/disclosure/publication burden before rendering; still no guarantee of release | You want the audition manifest to be publication-oriented from the start | Actual public-use and disclosure owner gates become immediate blockers |
| OAIA-SCOPE-OFFLINE-ONLY | defer | Zero provider spend/upload; implements the safest L0 foundation | Produces no audible evidence | You want engineering readiness before any provider/account decision | SWU-OAIA-001 may later be selected; every render decision remains open |
| OAIA-SCOPE-STOP | stop | Ends spend, data, and implementation exposure | No OpenAI audition | You no longer want this provider route | Close Decision Gate as stopped |

- Selected option: `OAIA-SCOPE-PRIVATE-LOCAL`.
- Rationale: the user selected option 1, choosing the smallest real voice-quality test while keeping publication outside the first audition.
- Source of decision: direct user chat response `1`, recorded 2026-08-04T18:39:58Z.
- Admissibility request: `requests/OAIA-DG-001-use-scope.json`.
- Admissibility receipt: `receipts/OAIA-DG-001-use-scope.json`.
- Request digest: `31ffc1edb36e2a33a4f74775961908d5a9e719c7c8b6923d1bf7c194f141985f`.
- Prefilter result: four admissible options, zero rejected options, schema-valid `gate` route.

### Consequence

The first audition is private and local after provider generation. No public-video use, release, or publication is included. The selected route still sends the owned excerpt to a metered external provider, so accent, voice, named operator, actual-account data/retention/security gates, exact request binding, verification tools, and listening operations remain unresolved. This decision is not upload or spend authorization.

## OAIA-DG-002 — Accent and locale posture

**Question:** Which English accent posture should the exact stock voice follow for this private audition?

| Option | Kind | Benefit | Cost/risk | When to choose | Downstream impact |
|---|---|---|---|---|---|
| OAIA-ACCENT-CLEAR-INTERNATIONAL | action | Broad comprehension and restrained regional identity | “International” is prompt-interpreted rather than a standardized accent and must be judged by listening | The global educational audience matters more than a strong regional signature | Freeze an English instruction emphasizing clarity and minimal regional markers |
| OAIA-ACCENT-LIGHT-BRAZILIAN | action | Gives the narrator a closer connection to the creator's linguistic identity | Stock voices may render it inconsistently or stereotypically; requires careful listening | Personal identity and warmth matter more than maximum neutrality | Freeze a light, natural Brazilian-accent instruction; reject caricature or reduced clarity |
| OAIA-ACCENT-GENERAL-AMERICAN | action | Familiar, usually predictable English delivery for technology education | Less distinctive and potentially less aligned with the creator's identity | Predictability and broad North-American familiarity are preferred | Freeze `en-US`/General American delivery intent |
| OAIA-ACCENT-PROVIDER-NATIVE | action | Least prompt pressure and fastest voice evaluation | Weakest cross-candidate control; selected voice determines accent variation | You want to judge the stock voice as supplied before directing accent | Record explicit approval of provider-native variation and omit accent instruction |
| OAIA-ACCENT-DEFER | defer | Avoids premature creative commitment | Keeps every render blocked and produces no audible evidence | You want to listen to external demos or define the audience first | DG-003 and provider rendering remain blocked |
| OAIA-ACCENT-STOP | stop | Ends further work and provider exposure | No audition | You no longer want this provider route | Close Decision Gate as stopped |

- Selected option: `OAIA-EXPERIMENT-TWO-ACCENT-AB` through the explicit scope-revision route recorded below.
- Rationale: the user first answered `1 and 2`, then explicitly instructed `create the two variants`, resolving the ambiguity in favor of two separate accent candidates.
- Source of decision: direct user chat responses `1 and 2` and `create the two variants`, last recorded 2026-08-04T19:25:12Z.
- Admissibility request: `requests/OAIA-DG-002-accent-locale.json`.
- Admissibility receipt: `receipts/OAIA-DG-002-accent-locale.json`.
- Request digest: `ba7b888ab84a2ab2684f0140214e8fad8e07c168687d8afaacc395f5714ad16c`.
- Prefilter result: six admissible options, zero rejected options, schema-valid `gate` route.

### OAIA-DG-002A — Accent composition clarification

The combined interpretation is structurally admissible: one delivery instruction can ask for clear international English with a subtle, natural Brazilian accent, subject to human listening for clarity, naturalness, and stereotyping. Two separate accent variants are not admissible under the approved one-configuration protocol: `SPEC.md` admits exactly one stock voice/configuration, and `UX-PLAN.md` says the audition is not a preference carousel. Choosing two rendered variants would require an explicit scope revision through Invoke before this Decision Gate can continue.

| Option | Status | Consequence |
|---|---|---|
| OAIA-ACCENT-COMBINED-INTERNATIONAL-BRAZILIAN | admissible | Freeze one blended direction: clear international English with a subtle, natural Brazilian accent |
| OAIA-ACCENT-TWO-VARIANTS | rejected by prefilter | Requires a scoped protocol revision before separate variants can be compared |
| OAIA-ACCENT-CLEAR-INTERNATIONAL | admissible | Freeze clear international English only |
| OAIA-ACCENT-LIGHT-BRAZILIAN | admissible | Freeze a light, natural Brazilian accent only |
| OAIA-ACCENT-DEFER | admissible | Keep rendering blocked |
| OAIA-ACCENT-STOP | admissible | Close the OpenAI audition route |

- Clarification selected: two separate accent variants through a new Invoke scope revision. The historical rejection remains correct for the original one-configuration protocol; it is not being overridden in place.
- Admissibility request: `requests/OAIA-DG-002A-accent-composition.json`.
- Admissibility receipt: `receipts/OAIA-DG-002A-accent-composition.json`.
- Request digest: `b70ef4bc6e26bdd78fbd2b28dd392cf3aa79230594457d86880caa683806e842`.
- Prefilter result: five admissible options, one rejected option, schema-valid `gate` route.

### OAIA-DG-002B — Two-variant scope revision

**Decision:** Revise the private pilot to create exactly two A/B candidates with one provider render each. Both use the same frozen excerpt, model, stock voice, output format, and shared delivery constraints. The sole intended semantic difference is the accent instruction:

- Candidate A: clear international English.
- Candidate B: English with a light, natural Brazilian accent; no caricature and no reduction in intelligibility.

- Selected option: `OAIA-EXPERIMENT-TWO-ACCENT-AB`.
- Rationale: the user explicitly requested creation of the two variants after being told that this requires a new Invoke scope.
- Source of decision: direct user chat instruction `create the two variants`, recorded 2026-08-04T19:25:12Z.
- Admissibility request: `requests/OAIA-DG-002B-two-variant-scope.json`.
- Admissibility receipt: `receipts/OAIA-DG-002B-two-variant-scope.json`.
- Request digest: `fad43cfc1493c9f0b93895d0accd44ca2dd84f8f48dc6a37527460958febfc50`.
- Prefilter result: three admissible options, zero rejected options, schema-valid `gate` route.
- Consequence: the prior Define/Design/Plan artifacts are stale where they require one configuration and two identical-setting repetitions. Invoke must revise those artifacts before implementation or rendering.

## OAIA-DG-003 — Exact shared stock voice

**Question:** Which single OpenAI stock voice should both accent variants use so accent remains the intended A/B difference?

| Option | Kind | Benefit | Cost/risk | When to choose | Downstream impact |
|---|---|---|---|---|---|
| OAIA-VOICE-MARIN | action | Current official quality recommendation; keeps the comparison controlled | Official docs do not establish reflective-tone fit | You prefer a fast, reversible first audition with one of OpenAI's recommended voices | Freeze `voice: marin` in both request manifests |
| OAIA-VOICE-CEDAR | action | Current official quality recommendation; keeps the comparison controlled | Official docs do not establish reflective-tone fit | You prefer cedar after hearing its official demo | Freeze `voice: cedar` in both request manifests |
| OAIA-VOICE-DEFER-FOR-DEMO | defer | Lets tone and accent remain a listening decision rather than a textual guess | Delays rendering | Voice identity matters enough to hear official demos first | Keep provider rendering blocked; choose after OpenAI.fm listening |
| OAIA-VOICE-STOP | stop | Ends provider exposure and work | No audition | You no longer want the OpenAI route | Close Decision Gate as stopped |

- Selected option: `OAIA-VOICE-DEFER-FOR-DEMO`.
- Rationale: the user selected option 3 so the voice choice is informed by official audio rather than textual quality guidance. This is an explicit defer, not a selection of `marin` or `cedar`.
- Source of decision: direct user chat response `3`, recorded 2026-08-04T19:30:41Z.
- Admissibility request: `requests/OAIA-DG-003-shared-stock-voice.json`.
- Admissibility receipt: `receipts/OAIA-DG-003-shared-stock-voice.json`.
- Request digest: `622f99dd5d296ec1b87a3cbdffaf031bf285638e64baf4ce209cdf4f64f41434`.
- Prefilter result: four admissible options, zero rejected options, schema-valid `gate` route.

### Deferred consequence

The official-demo defer ended when the owner judged the tested stock voices too mechanical and selected an own-voice clone. No stock voice was accepted.

### OAIA-DG-003B — Voice identity strategy

**Decision:** Replace the stock-voice direction with a private clone of the owner's own voice.

| Option | Kind | Benefit | Cost/risk | When to choose | Downstream impact |
|---|---|---|---|---|---|
| OAIA-VOICE-OWN-CLONE | action | Preserves the creator's identity, accent, and characteristic cadence | Uploads sensitive voice material; synthesis can still sound mechanical; consent, retention, deletion, and misuse controls become hard gates | Identity and natural accent matter more than minimizing biometric exposure | Supersede the stock-voice design and open a clone-provider/method gate |
| OAIA-VOICE-SELF-RECORDED | action | Maximum authentic timing and emotion with no provider voice model | Requires recording, editing, cleanup, and possibly retakes | Natural performance matters more than automation | Route to human recording production rather than cloning |
| OAIA-VOICE-KEEP-STOCK | action | Lowest biometric exposure and smallest existing plan change | Owner has already found the tested voices too mechanical | The stock audition remains acceptable after further prompting | Resume the prior stock-voice gate |
| OAIA-VOICE-IDENTITY-DEFER | defer | Avoids biometric commitment | Produces no narration | More privacy or quality evaluation is needed | Keep every render blocked |
| OAIA-VOICE-IDENTITY-STOP | stop | Ends provider and biometric exposure | No generated narration | The route should end | Close the narration-provider gate |

- Selected option: `OAIA-VOICE-OWN-CLONE`.
- Rationale: after listening, the owner judged the stock voices too mechanical and stated that the project should use a voice clone.
- Source of decision: direct user chat statement `i think we need to go with voice clone, this voices are too mechanical`, recorded 2026-08-04T19:44:12Z.
- Admissibility request: `requests/OAIA-DG-003B-voice-identity.json`.
- Admissibility receipt: `receipts/OAIA-DG-003B-voice-identity.json`.
- Request digest: `8e875236e34132daed4e4703dab70f74825074d8e1be047f857c53634f8f42f5`.
- Prefilter result: five admissible options, zero rejected options, schema-valid `gate` route.
- Consequence: the current OpenAI stock-voice Define/Design/Plan package is superseded for execution. Its explicit clone prohibition remains historically correct and must be replaced through a new Invoke scope, not silently edited away.

### OAIA-DG-003C — Clone provider and method

**Question:** Which bounded clone route should be prepared before any biometric recording is uploaded?

| Option | Kind | Benefit | Cost/risk | When to choose | Downstream impact |
|---|---|---|---|---|---|
| OAIA-CLONE-ELEVENLABS-PVC | action | Highest documented fidelity to cadence, pauses, tone, and accent; dedicated model | Creator plan or above; approximately 30–180 minutes of clean single-speaker audio; verification and training; vendor lock-in; biometric privacy/data gates | Voice identity and natural performance are the priority | New Invoke package for PVC recording, verification, deletion, data-use, audition, and disclosure controls |
| OAIA-CLONE-ELEVENLABS-IVC | action | Fast, reversible pilot from roughly 1–2 minutes of clean audio | Uses few-shot conditioning rather than a dedicated model; may struggle with distinctive accents and may remain synthetic; same biometric gate | You want the smallest audible clone experiment before committing to PVC | New Invoke package for a private IVC pilot with a strict stop/go result |
| OAIA-CLONE-OPENAI-ELIGIBILITY-CHECK | defer | Keeps the existing provider family and needs two short recordings if access exists | Custom voices are limited to eligible customers; entitlement is unknown; same TTS pipeline may retain mechanical prosody | You want to verify account access before selecting another provider | No upload; check entitlement, supplemental agreement, and retention first |
| OAIA-CLONE-DEFER | defer | Avoids immediate biometric/provider commitment | No clone or narration | You need more time | Keep rendering blocked |
| OAIA-CLONE-STOP | stop | Ends cloning exposure | No cloned narration | Cloning is no longer desired | Close this route |

- Recommendation: `OAIA-CLONE-ELEVENLABS-PVC` when fidelity to the owner's accent and cadence is the decisive requirement; `OAIA-CLONE-ELEVENLABS-IVC` only as a smaller experiment.
- Selected option: pending.
- Rationale: pending owner response. Selection prepares a governed route; it does not authorize account creation, agreement acceptance, recording, upload, spend, training, or synthesis.
- Source of decision: pending owner response.
- Admissibility request: `requests/OAIA-DG-003C-clone-provider-method.json`.
- Admissibility receipt: `receipts/OAIA-DG-003C-clone-provider-method.json`.
- Request digest: `8a1f65994aac574a21cac100fa7de046959974b3145160d31c47e851d065e27d`.
- Prefilter result: five admissible options, zero rejected options, schema-valid `gate` route.

## Remaining blockers

Six decision fronts remain unresolved. They will be asked one at a time. Technical decisions with only one admissible route will be recorded as `direct` without manufacturing consent or execution authorization.

## Assumptions

- The target is the OpenAI audition package created by the immediately preceding Invoke run.
- The user is the audition owner for creative choices unless they name another owner.
- No account, publication, legal, data, or production-owner authority is inferred from chat context.
