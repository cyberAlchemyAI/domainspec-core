# Planned Witness Contracts

Status: Design-authored and unexecuted.

These witnesses define later implementation evidence. They are not current
Plan evidence, accessibility certification, human-study evidence, release
evidence, or implementation authorization.

## Fixture Matrix

| Fixture ID | Claim | Polarity | Input or violation | Expected result |
| --- | --- | --- | --- | --- |
| UPW-FIX-001 | absent staged identity has one canonical update representation | positive | render and poll each null-staged lifecycle state | shell version equals `/state.version`; no coercion mismatch |
| UPW-FIX-002 | unchanged desktop polling is inert | positive | two poll intervals in BaselineReady, CommentsCaptured, MutationDrafted, RevisionRecorded at 1440×900 | zero main-document navigations and zero region patches |
| UPW-FIX-003 | unchanged mobile polling preserves work | positive | select target, fill drafts, focus a control, set page/frame scroll at 390×844 | all named local context survives two poll intervals |
| UPW-FIX-004 | one browser Accept causes one intended update | positive | acknowledge and Accept one staged candidate | one new projection version applied once; head advances once; navigation counts separated |
| UPW-FIX-005 | duplicated transition observations are idempotent | negative | action refresh and poll both observe the same new version | the new version patches once, never twice |
| UPW-FIX-006 | stale local context is explicitly invalidated | negative | external head change makes selected target/revision identity stale | only bound context resets and a reason is perceivable |
| UPW-FIX-007 | comparison frames are distinguishable | positive | RevisionApplied staged review | distinct accessible names for before/current and after/candidate frames |
| UPW-FIX-008 | annotation feedback is announced only in its scope | positive | select a target and submit a comment | `cf-msg` emits atomic polite status updates |
| UPW-FIX-009 | action feedback is announced only in its state scope | positive | Accept/Discard in RevisionApplied and Revert in RevisionRecorded | `act-msg` or `act-msg2` announces the matching event |
| UPW-FIX-010 | unrelated content is not a live region | negative | inspect headings, diff, history, copy, and stable-poll events | no extra live scopes or unchanged-poll announcements |
| UPW-FIX-011 | light-surface normal text meets contrast floor | positive | calibrated computed-style/compositing fixture | sampled normal-size text is at least 4.5:1 |
| UPW-FIX-012 | outer workbench actions meet target-size floor | positive | calibrated desktop and mobile action matrix | at least 24×24 CSS pixels or a proven exception; primary target documented |
| UPW-FIX-013 | mobile task hierarchy remains operable | positive | all lifecycle states at 390×844 | no horizontal overflow; spine/action and active task precede collapsed history |
| UPW-FIX-014 | governance behavior does not regress | negative | missing/stale acknowledgment, staged/current identity, Revert, Export checks | existing gates reject illegal action; Revert appends; Export absent from browser |
| UPW-FIX-015 | malformed or failed projection refresh preserves work | negative | network error, invalid schema, or rejected action | current DOM and drafts remain; bounded error/recovery appears; no false state transition |
| UPW-FIX-016 | projection and compatibility fields come from one coherent read | negative | external CLI write interleaves between projection-input reads | torn read is retried or fails recoverably; no version represents mixed epochs |
| UPW-FIX-017 | renderer failure cannot leave mixed governed DOM | negative | changed region N throws after earlier regions prepared or committed | all changed mounts and local context roll back; prior whole/region versions remain applied |
| UPW-FIX-018 | action completion observes state after an older in-flight poll | negative | defer V0 poll, complete action to V1, then release V0 response | one trailing refresh fetches V1; V1 applies once; no reload or duplicate patch |
| UPW-FIX-019 | canonical whole/region digests bind exact objects | negative | golden vectors plus changed-object/unchanged-hash and changed-whole/unchanged-region mutants | server/contract validator rejects every mismatch; browser continues to treat digests as opaque |
| UPW-FIX-020 | action copy and CLI detail follow the state contract | positive | inspect every browser-action state and secondary CLI disclosure | state/copy matrix matches FR-14; CLI detail remains secondary and Export remains terminal-only |
| UPW-FIX-021 | keyboard and focus paths match pointer behavior | positive | complete annotation and governed actions by keyboard, including a removing transition | same handlers and receipts; visible focus persists or moves to the new task heading |
| UPW-FIX-022 | color and error urgency are not sole or overbroad signals | negative | remove color cues and trigger recoverable versus blocking failures | textual/state cues remain; polite scopes stay bounded; only the tested blocking error is assertive |
| UPW-FIX-023 | prototype frames retain the sandbox contract | negative | remove or weaken a required iframe sandbox attribute | security validator fails before admission |
| UPW-FIX-024 | projection routes remain in allowlisted local families | negative | inject an unknown or external route family | server/contract validator rejects the projection and the current workbench remains intact |

## Navigation And Update Accounting

Every continuity fixture records separately:

- main-document navigation count;
- annotation-frame navigation count;
- before/after-frame navigation count;
- applied whole-projection versions;
- applied region versions;
- projection read epochs or stable input identities;
- request and response sequence IDs;
- refresh caller reasons;
- queued trailing-refresh count and cause;
- region render attempts, commits, rollbacks, and failures;
- context invalidation identity and reason;
- action POST count; and
- resulting revision-head count.

“One intended update” means one application of one unseen projection version.
It does not mean that a head change can never legitimately navigate a child
frame whose bound content identity changed.

## Local Context Matrix

| Context | Preserve when | Invalidate when | Required feedback |
| --- | --- | --- | --- |
| selected annotation target | current-head identity and target still resolve | current head or target identity changes | target reset reason in `cf-msg` |
| intent and note drafts | annotation identity remains valid | their bound target becomes stale | drafts retained for recovery or explicit discard choice |
| focus | focused node remains present and enabled | state removes or disables the exact control | focus moves to state heading or relevant status |
| top-level scroll | active region remains | explicit operator navigation | none for unchanged poll |
| annotation-frame scroll | frame source identity remains | head identity changes | new frame loading/status context |
| open history/inspector state | same region remains available | lifecycle state removes the region | no silent whole-page reset |

## Validator Contracts

| Validator ID | Target | Pass condition | Required negative proof |
| --- | --- | --- | --- |
| UPW-VAL-VERSION | server projection identity | exact canonical digest recomputes, absent values are stable, and whole/region hashes bind their objects | nullable-coercion and digest-mismatch mutants fail |
| UPW-VAL-CONTINUITY | stable shell | unchanged polls are inert at both viewports | whole-document reload mutant fails |
| UPW-VAL-TRANSITION | refresh coordinator | one unseen version applies once and an action joining an older poll receives one trailing refresh | duplicate response and deferred old-poll/action mutants do not double patch or stay stale |
| UPW-VAL-CONTEXT | browser-local context | valid context survives; stale context resets with reason | identity-changing fixture invalidates bounded fields |
| UPW-VAL-RECOVERY | projection read and region commit | torn reads never emit a mixed epoch; failed commit restores prior governed surface | interleaved writer and renderer-N failure mutants fail closed |
| UPW-VAL-COPY | state/action language | browser action wording and secondary CLI disclosures match FR-14 | raw CLI-primary and browser-Export mutants fail |
| UPW-VAL-A11Y | frames, live regions, keyboard/focus, contrast, target size, color cues | exact bounded positive fixtures pass | unrelated live-scope, low-contrast, pointer-only, lost-focus, and color-only mutants fail |
| UPW-VAL-SECURITY | outer shell and frames | text uses safe DOM sinks; iframe sandbox/route allowlist persist | raw outer-shell HTML, sandbox-removal, and disallowed-route fixtures fail |
| UPW-VAL-GOVERNANCE | application gates and handoff | current invariants remain green | missing/stale ack and browser Export fail |
| UPW-VAL-RESPONSIVE | 390×844 workbench | no overflow and active task precedes history | forced chronology mutant fails |

## Human Evidence Contract

Only after automated and calibrated fixtures pass may a separately owned human
study measure:

- first-time orientation and next-action comprehension;
- task resumption after interruption;
- confidence in staged versus current identity;
- perceived control over Accept, Discard, and Revert;
- workload and comparison usability; and
- trust, safety, delight, and real-task success.

No automated result in this package can stand in for those outcomes.
