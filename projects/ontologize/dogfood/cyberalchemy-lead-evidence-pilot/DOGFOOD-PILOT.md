# CyberAlchemy Lead Evidence Dogfood Pilot

Date: 2026-06-18
Status: planned internal validation lane
Parent product: Ontologize
Pilot type: dogfood, not external offer

## Purpose

Validate whether Ontologize, `projects/autoads/`, and `../maestro-trama` can compose into a useful future product for improving lead-generation decisions.

This pilot uses CyberAlchemy as the first proving ground. The goal is not to sell a new service yet. The goal is to improve CyberAlchemy's own page and lead funnel while checking whether the combined substrate can produce reusable evidence, not just better copy.

## Product Boundary

- **Ontologize** is the parent trust and metric-governance product.
- **CyberAlchemy Lead Evidence Dogfood Pilot** is a validation lane inside Ontologize.
- **autoads** remains an internal ad/creative experiment-loop seed, not the buyer-facing product name.
- **Maestro-Trama** remains an internal creative-performance and retrieval substrate.

Do not rename `projects/autoads/` based on this pilot. Do not spin out a separate product until repeated pilots prove the loop beyond CyberAlchemy.

## Validation Question

Can the combined substrate help CyberAlchemy make better lead-funnel decisions by linking one offer, one conversion action, one channel path, one response window, and one owner-reviewed scorecard?

## Starting Hypothesis

The future product is likely **Ontologize Lead Evidence** or **Ontologize Decision Scorecard**, not `autoads`.

It becomes product-worthy only if the dogfood pilot produces:

- a clearer CyberAlchemy offer page;
- a measurable lead or conversion event;
- 3-6 message, page, or creative variants;
- a scorecard tied to source evidence;
- one real owner decision;
- reusable templates for later external pilots.

## Scope

In scope:

- CyberAlchemy primary page and lead pages;
- one CyberAlchemy offer;
- one primary conversion event;
- one primary channel execution path;
- optional second-channel readiness brief;
- manually reviewed evidence bundle.

Out of scope:

- selling the offer to SMBs now;
- autonomous media buying;
- guaranteed lead, CPA, ROAS, ranking, or revenue claims;
- live ad-account integration without a separate readiness decision;
- broad multi-channel orchestration.

## Source Context

Primary source synthesis:

- `projects/ontologize/research/2026-06-18-autoads-maestro-smb-marketing-offer/findings.md`
- `projects/ontologize/research/2026-06-18-autoads-maestro-smb-marketing-offer/research.md`
- `projects/autoads/README.md`
- `projects/autoads/DEFINE.md`
- `implementation/domainspec/development/COMMERCIALIZATION-SYNTHESIS.md`
- `cyberAlchemy/README.md`
- `cyberAlchemy/main.html`

## Pass Criteria

The pilot passes if it yields a useful owner-reviewed scorecard and a real decision about what CyberAlchemy should keep, revise, pause, retest, or mark inconclusive.

The pilot does not need to prove scalable lead economics. It only needs to prove that the evidence loop improves the quality of CyberAlchemy's GTM decisions.

## Flag Criteria

Flag the pilot if:

- the CyberAlchemy offer cannot be named clearly;
- the conversion event is not measurable;
- lead quality cannot be judged;
- channel data is too thin;
- the result is only improved prose, not reusable evidence discipline;
- the output cannot be turned into templates for a later pilot.

## Next Work

1. Complete `OFFER-MAP.md`.
2. Select one primary channel in `CHANNEL-BRIEFS.md`.
3. Define the scorecard fields in `SCORECARD-SPEC.md`.
4. Run the first manual pass against CyberAlchemy page and lead surfaces.
5. Record observations and owner decision in `RESULTS.md`.
