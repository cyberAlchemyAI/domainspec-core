# Context Pack: SWU-CAW-CONTENT-001

Task: create the Home page contract for the CyberAlchemy website content
package.

Mode: `lean`

Strict coverage: `pass`

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Resolve exactly one SWU and keep scope to the Home page contract. | Covered by `INVOKE-CONTENT-ROUTE.md:205-219`. |
| O2 | The contract must include reader job, role, source anchors, authority type, claim type, status labels, allowed and forbidden claims, public-boundary notes, explanation method, and CTA/next read. | Covered by `INVOKE-CONTENT-ROUTE.md:35-53` and `:181-203`. |
| O3 | Home must be an offer page, not an architecture page. | Covered by `INVOKE-CONTENT-ROUTE.md:57-82`, `findings.md:81-95`, and `whisper-presets/cyberalchemy-site-page.md:73-81`. |
| O4 | Public copy must not claim shipped runtime, universal product capability, security guarantee, or raw private/session/dispatch mechanics. | Covered by `findings.md:7-28`, `findings.md:191-202`, and `whisper-presets/cyberalchemy-site-page.md:202-236`. |
| O5 | Every future load-bearing claim must have authority type, claim type, and Built/Designed/Planned/Open status. | Covered by `findings.md:14-52` and `whisper-presets/cyberalchemy-site-page.md:10-26`. |
| O6 | Home claims should be anchored to canonical/public sources; analogy material may shape structure only. | Covered by `findings.md:58-60` and `projects/ontologize/PUBLIC-OFFERING.md:6-72`. |
| O7 | The contract must be ready for a `whisper` run using preset `cyberalchemy_site_page`. | Covered by `whisper-presets/cyberalchemy-site-page.md:1-81` and `:180-236`. |

## Selected Context

### Invoke Route

- `projects/cyberAlchemy-website/development/invoke-runs/20260618-content-production-route/INVOKE-CONTENT-ROUTE.md:35-53`
  - Requires page contracts before Whisper drafts.
  - Contract fields: reader job, page role, anchors, authority, claim type,
    status labels, allowed/forbidden claims, boundary notes, method, CTA.
- `INVOKE-CONTENT-ROUTE.md:57-82`
  - Home role: `home`.
  - Primary method: `public-offer`.
  - Core claim: capability-foundry method, with evidence and limits attached.
  - Forbidden: shipped universal runtime, security guarantee, raw private
    mechanics, ontology-heavy first-screen explanation.
- `INVOKE-CONTENT-ROUTE.md:205-219`
  - L0 proof task: create Home contract, draft Home with Whisper, review gates.

### Findings

- `projects/cyberAlchemy-website/research/2026-06-17-content-inventory/findings.md:7-28`
  - Editorial law: publish CyberAlchemy as method and trust discipline, not as
    shipped end-to-end runtime/security/universal product capability.
  - Every page must preserve authority type, claim type, anchors, boundary,
    proof/status, role, method, and transformation need.
- `findings.md:30-52`
  - Authority types and claim status labels.
  - `Built` requires owned evidence as implemented or operating; documentation
    alone is not enough.
- `findings.md:56-60`
  - Home offer page: publish after abstraction.
  - Authority: canonical source plus analogy pattern.
  - Method: `public-offer`.
  - Transformation: lead with problem, transformation, audience, proof hint, CTA.
- `findings.md:81-95`
  - Home purpose and allowed content.
  - Avoid internal concepts on the first screen.
- `findings.md:191-202`
  - Reject raw sessions, raw dispatch mechanics, broad shipped claims, security
    claims, runtime authority, and unaudited HTML/PDF factual claims.
- `findings.md:204-237`
  - Required Whisper inputs and gates.

### Whisper Preset

- `projects/cyberAlchemy-website/whisper-presets/cyberalchemy-site-page.md:10-26`
  - Required: page objective, target public, page role, primary method, evidence
    bundle, source anchors, authority type, claim type, status labels.
- `whisper-presets/cyberalchemy-site-page.md:56-62`
  - Required body parts: opening, orientation, evidence-backed body, boundary,
    next action.
- `whisper-presets/cyberalchemy-site-page.md:73-81`
  - Home pages are offer pages only.
  - Architecture belongs after offer, method, and trust.
- `whisper-presets/cyberalchemy-site-page.md:83-148`
  - Tone, target publics, authority mode, objections, and trajectory.
- `whisper-presets/cyberalchemy-site-page.md:150-178`
  - `public-offer` is the method for desire/offer pages with strict proof
    language.
- `whisper-presets/cyberalchemy-site-page.md:202-236`
  - Draft gate, flag conditions, and blockers.

### Canonical/Public Source Anchors

- `arcanum/framework/CYBERALCHEMY-METHOD.md:3-9`
  - Purpose: CyberAlchemy Method behind Arcanum; governed synthesis.
- `arcanum/framework/CYBERALCHEMY-METHOD.md:11-25`
  - Five anchors: objective, output artifact, discovery, tension, route.
- `arcanum/framework/CYBERALCHEMY-METHOD.md:27-43`
  - Core thesis: vague intent and discovered evidence become governed artifacts.
- `arcanum/framework/CYBERALCHEMY-METHOD.md:45-55`
  - Method loop: orient, discover, shape, stabilize, evolve.
- `arcanum/framework/CYBERALCHEMY-METHOD.md:96-123`
  - Synthesis pattern and successful handoff criteria.
- `arcanum/docs/index.html:440-450`
  - Public homepage language: ambitious ideas to named workflows, governed
    artifacts, validator-backed evidence, reusable tools.
- `arcanum/docs/index.html:455-477`
  - Method: name, shape, prove; keep evidence with the work.
- `arcanum/docs/index.html:482-495`
  - Loop: prompt, refine, invoke, route, execute, learn.

### Analogy Pattern

- `projects/ontologize/PUBLIC-OFFERING.md:6-10`
  - One-line offer structure.
- `projects/ontologize/PUBLIC-OFFERING.md:11-27`
  - Problem framing structure.
- `projects/ontologize/PUBLIC-OFFERING.md:29-39`
  - "What installs" structure.
- `projects/ontologize/PUBLIC-OFFERING.md:56-72`
  - Narrow pilot proof and anti-hype boundary structure.

This source is an analogy pattern only. It must not authorize CyberAlchemy
factual claims.

## Decisions

- Contract location: `projects/cyberAlchemy-website/content/page-contracts/home.md`.
  - Rationale: content artifact, not session evidence.
- Context pack location:
  `projects/cyberAlchemy-website/development/task-sessions/20260618-home-page-contract/CONTEXT-PACK.md`.
  - Rationale: execution evidence for this task-session run.
- Runtime: local.
  - Rationale: no `--via runtime` request and no need for handoff-pack JSON.

No blocker-level decisions remain.

## Gate Verdict

Proceed.

The task has sufficient source context, clear write scope, explicit validation
surface, and no unresolved blocker before mutation.
