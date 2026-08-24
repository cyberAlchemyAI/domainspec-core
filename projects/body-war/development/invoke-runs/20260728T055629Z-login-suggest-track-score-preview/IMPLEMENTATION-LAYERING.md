---
module: body-war-login-suggest-track-score-preview
version: current
status: planned
updatedAt: 2026-07-28
docType: implementation-layering
---

# Implementation Layering

## W0 — Owner Decisions

Not an implementation layer. It closes DEC-JSP-001 through DEC-JSP-003:

- complete ScorePolicy V0, including window/timezone, eligibility,
  aggregation, bootstrap self-sample, missing-history, and history-consent
  rules;
- private geometry filter, retention, and deletion;
- first real-provider OAuth scope.

No numeric score or participant geometry persistence may proceed by guessing
these values.

DEC-JSP-001 and DEC-JSP-002 admit L0. DEC-JSP-003 is deferred until L2 and
does not block fixture implementation or moderated local testing.

## L0 — Local Working Prototype

Smallest end-to-end proof:

- fake OAuth/session;
- deterministic Strava-shaped activity summary, geometry streams, and
  complete-window derived history;
- exact non-first SuggestedTrack binding;
- unchecked affirmative consent;
- ownership-before-evidence and idempotent confirmation;
- private GeometryCandidate;
- canonical ScoreInputSnapshot;
- ratified ScorePolicy V0;
- deterministic ScorePreview;
- responsive web score card and explanation;
- memory and Postgres-backed tests.

External evidence:

- one browser journey that shows a numeric preview;
- a receipt proving `provider_mode: fixture`,
  `geometry_authority: candidate_from_activity`,
  `score_authority: preview_only`;
- negative controls for consent, binding, geometry, policy, duplicates, and
  authority inflation;
- raw-stream canaries across every active L0 sink.

What L0 does not prove: live Strava, hosted fit, participant comprehension,
score fairness, source-backed geometry, or production readiness.

## L1 — Moderated Local Prototype

After L0 passes, three supervised fake-provider sessions at assigned 320px and
390px widths plus short-height, 200% text, long-content, and orientation
stressors.

External evidence:

- completion or failure for login, non-first track Help, activity selection,
  consent, and score explanation;
- participant interpretation of candidate geometry and preliminary score;
- observed friction/residue.

L1 is formative UX evidence only.

## L2 — Real-Provider Gateway Evidence

- server-only token retrieval/decryption/refresh;
- required accepted-scope validation and race-safe token rotation;
- official summary, detail, and stream calls;
- policy-eligible history derivation and canonical snapshot input;
- least-privilege OAuth scope;
- raw stream exclusion;

L2 proves the controlled real-provider code boundary only. It does not admit a
hosted environment or a participant.

## L3 — Hosted Supervised Real-Provider Witness

- hosted admission;
- explicit parent admit/reject gate;
- one participant, one activity, one track, one attempt;
- redacted real-provider geometry and score receipt.

L3 proves one supervised real-provider path only.

## L4 — Repeat-Safe and Promotion-Ready Evolution

Outside the first prototype:

- broader retries and repeat/unmoderated use;
- deletion/self-service privacy lifecycle hardening;
- multiple-activity route aggregation and map matching;
- operator review and source-backed promotion;
- public geometry, control, rankings, fairness/balancing studies;
- production SLOs and release admission.

## Promotion Matrix

| From | To | Required evidence |
| --- | --- | --- |
| W0 | L0 | DEC-JSP-001 and DEC-JSP-002 recorded |
| L0 | L1 | code/browser/no-leak gates pass |
| L1 | L2 | formative residue disposition, DEC-JSP-003, plus real-gateway selection |
| L2 | L3 | controlled provider-gateway receipt plus HOST-01 admission and explicit parent admit |
| L3 | L4 | new bounded plan and owner authorization |
