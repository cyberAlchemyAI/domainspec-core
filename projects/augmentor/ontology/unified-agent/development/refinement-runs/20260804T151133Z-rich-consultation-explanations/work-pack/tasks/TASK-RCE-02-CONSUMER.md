# TASK-RCE-02: Consumer And Answering Agent

## SWU-RCE-004

Extend the ResonantOS contract, loader, host service, and cache for atomic explanation bundles.

- Stage and verify projection, glossary, manifest, schemas, and combined digest before activation.
- Reject mixed, missing, stale, swapped, or drifted artifacts.
- Key cache by principal, policy, views, bundle digest, contract version, query, and effective limits.
- Preserve route-scoped access and fail-closed responses.

## SWU-RCE-005

Return optional explanation support selected by `brief`, `guided`, or `deep`.

- Absent selector preserves current response behavior.
- Profile selection never changes status, evidence, confidence, or answer policy.
- Apply global and profile caps by minimum.
- Drop only whole optional units and report `omittedSections`.
- Add instruction-shaped fixtures to every text field; assert data-only handling.
- Never emit a final prose field.

## SWU-RCE-006

Add answering-agent composition conformance and documentation.

- Compose all profiles from identical fixture evidence.
- Assert direct answer first, scoped state, process order, label/limit pairs, 2-5 used terms, source citations, and boundary.
- Verify clarify/abstain flows do not fabricate teaching material.
- Keep `consultationAnswerPolicy` deterministic and model-free.
