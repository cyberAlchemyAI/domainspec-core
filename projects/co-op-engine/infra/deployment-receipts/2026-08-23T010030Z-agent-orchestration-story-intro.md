---
deployment_id: agent-orchestration-story-intro-20260823T010030Z
deployed_at: 2026-08-23T01:00:30Z
scope: agent-orchestration-guide
result: pass
authority_effect: bounded-public-route-update
---

# Agent Orchestration Story Introduction Deployment Receipt

## Outcome

The revised learner-facing guide is deployed at:

- `https://cyberalchemize.com/agent-orchestration`
- `https://cyberalchemize.com/agent-orchestration-guide`

Both routes returned HTTP 200 and the exact local HTML bytes:

- Source: `ops/development/2026-08-13-agent-orchestration-beginner-guide/guided-class.html`
- SHA-256: `904956c5e014f9e75f487a2d5bef95647b6388568ef42239dac5c770cd8745da`
- Size: 115906 bytes

The deployed copy replaces the generic sidebar safety warning with
`Meet Lantern and Priya`, introduces both story entities before Lesson 1,
and preserves the later command-context safety note.

## Control Drift And Route Selection

The repository's concurrent deployment controls changed before this release:

- Local deployment script: `24f37c6b61b525cea27f07b253f9535cba78a12081acc2e4470261a62ae3839f`.
- Local Nginx config: `7c2b419b6f75b4719173661e99fcdd990a83963cf283cdd1a8f8fc426d635594`.
- Local Compose config: `894d2e8d2b75251ab6dd5e54d4f9ec6192b1324f391c6f6ac2d831d25815627f`.

Those controls add a separate protected review route. Their simulated dry run
passed, but their live precondition gate stopped before upload because the
server does not yet contain that review artifact, credential file, or Compose
mount. No remote write occurred during that failed attempt.

The active server still matched the previously validated guide-only controls:

- Remote Nginx SHA-256: `62d842bf0052ad4020ea95ffa7cbce2a4da6ae8ebf7068969a673cc5360c6639`.
- Remote Compose SHA-256: `c3022b1cb3eddae1879d21b8b5e78143dbe7b6b5c1d8fe1e66056d1dbf6f1e07`.

The successful transaction was therefore pinned to those exact remote
controls and refused to change them. Its temporary guide-only script was
`3c0e046e5009e3f4458b017da1ca2a51789af117577fc5c6547bb98612aab66e`,
10781 bytes; shell syntax, whitespace, and ShellCheck validation passed. The
temporary script was removed after use.

## Deployment Validation

- Candidate contained one regular guide file with mode 0644 under a mode 0755 directory.
- Candidate guide digest matched the declared source digest.
- Every non-guide site byte compared equal before the switch.
- Existing remote Nginx syntax passed in an isolated networkless container.
- Existing remote Nginx and Compose digests were rechecked before and after the switch.
- An exact whole-site rollback snapshot was created as `/srv/co-op-engine/site.previous`.
- Existing static container was recreated without changing its image, Compose file, Nginx file, or Traefik labels.
- Container health and both in-container guide routes passed.
- Both public routes independently returned 115906 bytes with the exact source digest.
- Existing `/`, `/craft`, and `/bella` public bytes remained unchanged.
- Anonymous and wrong-credential `/domainspec/` requests remained HTTP 401.
- Public guide response retained its HTML content type, restrictive content security policy, `nosniff`, and frame denial.

## Public Browser Evidence

- Public response: HTTP 200 at the clean `/agent-orchestration` URL.
- Page title: `Agent orchestration: from prompt to proof`.
- Story heading: `Meet Lantern and Priya`.
- Story introduction matched the revised local copy.
- Removed `L0 static HTML/SVG.` text was absent.
- Seven lesson-navigation transitions each exposed exactly one active lesson.
- Eleven learner questions were present.
- Viewports: 390 by 844 and 1280 by 900.
- Every lesson had document width equal to viewport width at both viewports.
- Console errors: none. Page errors: none.
- Reload request inventory contained only `https://cyberalchemize.com/agent-orchestration`.

## Claim Ceiling

This receipt establishes exact-byte deployment, bounded preservation, and the
browser observations above. It does not establish human comprehension,
semantic truth, authorization for agent execution, canonical Arcanum
documentation status, or production readiness.

No commit or push was performed. The concurrent local deployment-control
changes were not deployed or modified by this release.
