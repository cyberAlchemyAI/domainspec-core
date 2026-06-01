# FID Sheet and Multi‑Agent Design for Key Grant Programs (FY2026)

**Document ID:** FID_CANONICAL_REFERENCE_2026-05-18
**Lifecycle:** canonical reference
**Authored:** 2026-05-18

---

## Overview

This document summarizes the key facts, eligibility rules and evaluation criteria for a set of funders and grant programs relevant to sustainable agriculture and rural development. It is the authoritative source-of-truth synthesis for every FID (Funder Intelligence Document) charter in `pipeline/funder_intelligence/pillar_1_charters/`. All FID charters must reconcile to this doc; variations require source-backed justification logged in the corresponding pass's improvements log.

Each funder profile follows a consistent structure: mission, eligibility, funding emphasis, cascading dependencies (between parent funder and its programs), common failure modes, and implications for the multi-agent FID design (Scout, Scribe, Judge, Red Team, Logician).

---

## USDA – Rural Development (USDA‑RD) – Funder Profile

### Mission / Strategic Emphasis

USDA Rural Development's mission is to improve the economy and quality of life in rural America by providing loans, grants and loan guarantees that support essential services such as housing, business creation, infrastructure, broadband, electric and community facilities【910421871630916†L60-L80】. RD works in partnership with local governments, cooperatives, tribal entities, nonprofits and rural businesses to build prosperous communities.

### Default Eligibility / Compliance Posture

| Field | Detail |
|---|---|
| Geography | "Rural" generally defined as places with ≤ 50,000 population (program-specific thresholds vary; Community Facilities uses ≤ 20,000). |
| Applicant types | Public bodies, federally recognized tribes, nonprofit organizations, cooperatives, agricultural producers, small/emerging businesses (varies by program). |
| Compliance baseline | SAM.gov registration, UEI, Davis-Bacon where construction is involved, environmental review (NEPA), Federal Funding Accountability/Transparency, audit thresholds per 2 CFR 200. |

### Funder-Wide Emphasis

* Distress-targeted: ReConnect, Rural Partners Network, persistent-poverty census-tract bonuses.
* Cooperative and producer-owned business models are explicitly favored across multiple programs (RCDG, VAPG, RBDG)【910421871630916†L60-L80】.
* Documented community benefit and long-term sustainability are recurring scoring themes.

### Cascading Dependencies

Programs inherit USDA-RD's geographic definition of "rural", SAM/UEI registration, environmental/NEPA framework, and audit thresholds. Program-specific eligibility narrows these defaults (e.g., CFP narrows population to ≤ 20,000; RCDG narrows applicant type to nonprofit incl. universities).

### Common Failure Modes

* Applicant misclassifies as "rural" using a non-RD definition.
* Project lacks documented coordination with state/tribal RD office before submission.
* Match or non-federal-funds commitments described but not evidenced with letters or board resolutions.
* Cooperative or community-benefit language present but not tied to specific governance or membership data.

### Implications for FID Design

* **Scout:** USDA-RD discovery channel must consult both grants.gov and state-office program pages; many program windows are state-office-published before the federal NOFA opens.
* **Scribe:** rural-place documentation, SAM/UEI, environmental review, and cooperative-governance language are recurring scaffolding sections; warrant a USDA-RD shared boilerplate registry.
* **Judge:** rubrics should cross-check community-benefit claims against any membership/governance evidence in the applicant's PROJECT_CONTEXT.
* **Red Team:** challenge rurality claims (does the project address line actually fall inside the RD-eligible polygon?); challenge non-federal-funds claims that lack documentary evidence.
* **Logician:** P0 gates for rural-place eligibility, SAM.gov active status, audit-threshold compliance.

---

## USDA‑RD – Rural Business Development Grants (RBDG)

### Purpose

RBDG provides grants for technical assistance, training and other activities that lead to the development or expansion of small and emerging private businesses in rural areas【603619300672499†L60-L88】.

### Eligibility

| Field | Detail |
|---|---|
| Applicant types | Rural towns, communities, state agencies, authorities, nonprofits, institutions of higher education, federally recognized tribes, rural cooperatives. |
| Place | Rural areas outside the urbanized periphery of any city with a population of 50,000+. |
| Beneficiary | Small and emerging private business enterprises (≤ 50 new employees, < $1M in projected gross revenues). |

### Deadlines (FY 2026)

* **June 15, 2026** — Strikeforce/Economically Challenged Distress (SECD) areas.
* **June 30, 2026** — all other applications【603619300672499†L60-L88】.

### Funding

* Awards typically $10,000 to $500,000.
* **No match is required**, but committed non-federal funding contributes to the scoring profile【603619300672499†L60-L88】.

### Evaluation Criteria (FY 2026)

* Documented evidence of need.
* Project leverage (non-federal funds, partners, in-kind).
* Project economic impact (jobs created/retained, businesses started/expanded).
* Project quality (work plan, timeline, evaluation method).
* Project priority (alignment with state/regional priorities, distressed-area emphasis).

### Implications for FID Design

* **Scout:** key dates June 15 (SECD) and June 30 (general); SECD-area applicants must be detected and routed to the earlier deadline.
* **Scribe:** non-federal funding scoring is real even though no match is required — surface this to applicants as a competitive lever.
* **Judge:** distinct rubric weights for SECD vs general queues.
* **Red Team:** challenge inflated job-creation/retention numbers and ensure the small-and-emerging business definition (≤ 50 employees, < $1M revenue) is actually met.
* **Logician:** P0 gates on rural place, applicant type, beneficiary size class.

---

## USDA‑RD – Community Facilities Program (CFP)

### Purpose

CFP provides direct loans, loan guarantees and grants to develop essential community facilities (health care, public safety, public services, education, child care, food access infrastructure) in rural areas【442290906807144†L70-L120】.

### Eligibility

| Field | Detail |
|---|---|
| Applicant types | Public bodies, community-based nonprofit corporations, federally recognized tribes. |
| Place | Rural areas, towns and cities with population ≤ 20,000. |
| Use of funds | Acquire, construct, enlarge, improve essential community facilities for public use. |

### Grant Percentage Bands

The grant share of total project cost is determined by community population and Median Household Income (MHI) relative to the state non-metropolitan MHI:

| Population | MHI relative to state non-metro | Maximum grant share |
|---|---|---|
| ≤ 5,000 | ≤ 60% of state non-metro MHI | 75% |
| ≤ 12,000 | ≤ 70% of state non-metro MHI | 55% |
| ≤ 20,000 | ≤ 80% of state non-metro MHI | 35% |
| ≤ 20,000 | ≤ 90% of state non-metro MHI | 15% |

### Requirements

* Demonstrated significant community support.
* Documentation of inability to obtain credit at commercially reasonable rates.
* Environmental review (NEPA) and historic-preservation review.
* For construction, Davis-Bacon wage standards apply.

### Implications for FID Design

* **Scout:** the 20,000-population ceiling is a hard cliff; charters must encode it as a gate, not a guideline.
* **Scribe:** the grant-percentage band is determined by population × MHI; the draft must surface the band as a calculated field, not a narrative claim.
* **Judge:** essential-services framing, community-benefit framing, and inability-to-obtain-credit framing each merit their own rubric dimension.
* **Red Team:** challenge MHI claims — the state non-metropolitan MHI is the comparator, not statewide MHI, and applicants often confuse the two.
* **Logician:** P0 gates for population ≤ 20,000, MHI band classification, environmental review status.

---

## USDA‑RD – Rural Cooperative Development Grants (RCDG)

### Purpose

RCDG funds the establishment and operation of centers for rural cooperative development. The centers, in turn, provide technical assistance to individuals and entities forming or expanding cooperatives and mutually-owned businesses【762881089290126†L60-L130】.

### Eligibility

| Field | Detail |
|---|---|
| Applicant types | Nonprofit institutions, including institutions of higher education. The applicant does **not** need to already be a cooperative development center (CDC); the grant funds the establishment or operation of a center【762881089290126†L60-L130】. |
| Place | Centers must serve rural areas, defined per RD's standard threshold. |

### Funding

* Awards range from **$0 to $1,000,000** depending on appropriations and scoring.
* Matching funds typically required (program guidance specifies the rate; verify per NOFA).

### Closing Date

* **September 15, 2025** for FY 2025 NOFA【762881089290126†L60-L130】.

### Focus

* Improving the economic condition of rural areas through cooperative development.
* Strengthening producer/community ownership models.
* Building the capacity of CDCs to provide ongoing TA.

### Implications for FID Design

* **Scout:** RCDG is annual; the publication window is mid-summer with a mid-September deadline — track on a dedicated calendar.
* **Scribe:** the "we are establishing or operating a center" framing is load-bearing; an applicant who frames the grant as direct-to-cooperative misreads the program.
* **Judge:** evaluate CDC theory of change, ongoing-TA model, and rural-cooperative impact pathway as distinct dimensions.
* **Red Team:** common misreading is that the applicant must already be a CDC; clarify that nonprofit institutions including universities are eligible to *establish* a center.
* **Logician:** P0 gates on nonprofit status, rural-service-area definition, match commitment.

---

## USDA – National Institute of Food and Agriculture (USDA‑NIFA) – Funder Profile

### Mission

NIFA invests in and advances agricultural research, education, and extension to solve societal challenges. It funds competitive grants, capacity grants, and special research initiatives focused on food, agriculture, natural resources, and human-science issues【455099064093608†L60-L100】.

### Default Eligibility / Compliance Posture

| Field | Detail |
|---|---|
| Applicant types | Universities, colleges (1862, 1890, 1994 land-grant institutions and others), nonprofits, federally recognized tribes, state and local agencies, individuals depending on program. |
| Compliance baseline | SAM.gov, UEI, Federal cost principles (2 CFR 200), Responsible Conduct of Research (where applicable), data management plans, project director CV/biosketch standards. |

### Funder-Wide Emphasis

* Scientific rigor, peer review, and reproducibility.
* Education and extension are co-equal with research in NIFA's mission.
* Workforce development and integrated projects (research + education + extension) receive priority across many NIFA programs.

### Implications for FID Design

* **Scout:** NIFA programs publish RFAs on a predictable annual cadence; track each program (AFRI, SARE, BFRDP, OREI, others) on a dedicated calendar.
* **Scribe:** NIFA's voice is academic and scientific — code-switch to peer-reviewed-grant register, even for community-facing projects.
* **Judge:** distinct rubric dimensions for scientific rigor, education plan, extension plan, integration.
* **Red Team:** challenge weak literature review, weak evaluation design, and missing integration claims.
* **Logician:** P0 gates on PI eligibility, institution type, data-management-plan presence.

---

## USDA‑NIFA – SARE Northeast (FY 2026)

### Purpose

The Northeast Sustainable Agriculture Research and Education (SARE NE) program funds applied agricultural research and education projects that promote profitable, environmentally sound, and community-supportive farming in the Northeast region (CT, DE, MA, MD, ME, NH, NJ, NY, PA, RI, VT, WV, and DC)【317528590989824†L60-L130】.

### Grant Types (FY 2026)

| Grant type | Typical award | Lead applicant |
|---|---|---|
| Research & Education (R&E) | up to $250,000 | researcher or educator with cooperator farmers |
| Research for Novel Approaches | up to $30,000 (preproposal) | researcher exploring early-stage idea |
| Partnership | up to $30,000 | researcher or extension working directly with farmers |
| Farmer Grant | up to $30,000 | farmer (with technical advisor) |
| Professional Development | up to $150,000 | educator/agency training other educators |
| Graduate Student | up to $15,000 | grad student with faculty advisor |

### Eligibility

* Lead applicant must reside or operate in the SARE Northeast region.
* Farmer grants require farmers to derive a meaningful portion of income from farming and to identify a technical advisor.
* Research grants require an institutional appointment or equivalent.

### Funding / Match

* Match is **not** universally required across all SARE grant types; verify per call. Cost-share is encouraged for larger R&E projects.

### Evaluation Criteria

* Importance of the problem and project rationale.
* Project design and methods (scientific or educational rigor).
* Outreach plan (transfer of learning to farmers and the broader community).
* Qualifications of the project team.
* Budget reasonableness.

### Implications for FID Design

* **Scout:** SARE grant types have different deadlines, different awards, and different eligibility — Scout must classify *which* SARE grant the opportunity is before routing.
* **Scribe:** Farmer Grant voice is plain-language operator narrative; R&E voice is academic; Scribe must code-switch by grant type.
* **Judge:** outreach plan is a distinct rubric dimension and is often where applicants underperform.
* **Red Team:** challenge novelty claims (Research for Novel Approaches is specifically for early-stage ideas) and challenge farmer-income claims for Farmer Grants.
* **Logician:** P0 gates on region (12 states + DC), applicant type per grant type, advisor presence for Farmer Grants.

---

## USDA – Agricultural Marketing Service (USDA‑AMS) – Funder Profile

### Mission

AMS facilitates the competitive and efficient marketing of agricultural products. It administers grant programs that support local and regional food systems, specialty crops, organic standards, and producer-owned market development【204986117928478†L60-L120】.

### Default Applicant Types

* State departments of agriculture (SCBGP).
* Local governments, agricultural cooperatives, nonprofits, producer networks, schools, and tribal entities (FMPP, LFPP).
* Producers and producer-owned ventures (VAPG).

### Cost Share

* **FMPP and LFPP require a 25% match** (cash or in-kind from non-federal sources)【204986117928478†L60-L120】. This is a competitive scoring lever and a hard eligibility threshold.
* SCBGP does not require match but state agency leverage is scored.
* VAPG match requirement varies by award type (planning vs working-capital); see VAPG charter for current cycle.

### Common Programs

* **FMPP** (Farmers Market Promotion Program) — direct-to-consumer market development.
* **LFPP** (Local Food Promotion Program) — intermediated market development (hubs, processors, distribution).
* **SCBGP** (Specialty Crop Block Grant) — state-administered specialty crop competitiveness.
* **VAPG** (Value-Added Producer Grant) — producer-owned value-added business development.
* **LAMP** umbrella program structures FMPP/LFPP and related local-food work.

### Evaluation Themes

* Market viability and demand evidence.
* Producer benefit (price, access, scale).
* Project sustainability beyond grant period.
* Diversity of customer base and supply base.
* Partnership and leverage.

### Implications for FID Design

* **Scout:** AMS programs cluster around spring NOFAs; track LAMP umbrella publication date as the leading indicator.
* **Scribe:** market-viability narrative and producer-benefit narrative are mandatory; thin demand evidence is the most common reason for low scores.
* **Judge:** match-source documentation must score independently — undocumented match is a fatal flaw.
* **Red Team:** challenge demand claims (letters of support are not market evidence); challenge sustainability claims (what happens at month 37?).
* **Logician:** P0 gates on match documentation, applicant type per program, project-period limits.

---

## Pennsylvania Department of Agriculture – Funder Profile

### Mission

PA Dept of Ag promotes the viability and competitiveness of Pennsylvania agriculture through regulatory programs, market development, food safety, animal health, and grant programs that support farms, food businesses, and rural communities【659826293196942†L60-L120】.

### Default Eligibility

| Field | Detail |
|---|---|
| Geography | Pennsylvania only. |
| Applicant types | PA-based farms, food businesses, cooperatives, nonprofits, local governments, school districts, processors. |
| Compliance baseline | Pennsylvania state vendor registration, applicable PA Dept of Ag licensing where relevant (food safety, dairy, meat processing), federal compliance where federal pass-through is involved. |

### Implications for FID Design

* **Scout:** PA Dept of Ag grants are state-published; subscribe to PA Bulletin and PDA news releases as primary Scout signals.
* **Scribe:** state-aligned language ("Pennsylvania-grown", "PA Preferred", "PA producer-owned") is scored even when not required.
* **Judge:** state-priority alignment is a distinct rubric dimension on most PDA programs.
* **Red Team:** challenge geography (PA-only includes business location, not just project location).
* **Logician:** P0 gates on PA registration, applicable PDA licensing, project geography.

---

## PA Dept of Ag – Agricultural Innovation Grant Program (FY 2025–26)

### Purpose

The PA Agricultural Innovation Grant supports projects that introduce or expand innovative agricultural practices, technologies, products, business models, or supply chain solutions in Pennsylvania【728192937017942†L60-L150】.

### Eligibility

* PA-based farms, agricultural cooperatives, nonprofits, agricultural businesses, processors, and partnerships.
* Project work must occur in Pennsylvania.

### Grant Types

| Grant type | Award range | Non-state match |
|---|---|---|
| Planning | $7,500 – $50,000 | 30% non-state |
| On-site | $5,000 – $200,000 | 50% non-state |
| Regional impact | $100,000 – $2,000,000 | 50% non-state |

### Application Period (FY 2025–26)

* **Closed April 18, 2026**【728192937017942†L60-L150】. Next cycle TBD; Scout should track PDA announcements for FY 2026–27 publication.

### Evaluation Principles

* Relevant — addresses a documented PA agricultural challenge or opportunity.
* Practical — implementable with the proposed budget and timeline.
* Accessible — outcomes shareable with other PA producers.
* Scalable — model can grow beyond the initial project.
* Triple-bottom-line — economic, environmental, and social benefit.

### Implications for FID Design

* **Scout:** track PDA Innovation Grant on annual cadence; current cycle is closed.
* **Scribe:** triple-bottom-line framing is mandatory; applicants who write only an economic narrative score below threshold.
* **Judge:** five evaluation principles map to five rubric dimensions; weight scalability and accessibility heavily.
* **Red Team:** challenge "innovation" claims that are actually adoption of existing practice; challenge scalability claims that lack a replication pathway.
* **Logician:** P0 gates on PA project location, applicant type, match band per grant type.

---

## Heinz Endowments

### Mission / Geography

The Heinz Endowments funds work primarily in Southwestern Pennsylvania (SWPA), with a focus on creative learning, sustainable communities, and a just economy. Grants are made only to organizations that are tax-exempt under IRC §501(c)(3) or to public agencies【281097117836681†L60-L120】.

### Eligibility

* SWPA-based or SWPA-serving 501(c)(3) nonprofits and public agencies.
* National or regional organizations are eligible only when work demonstrably benefits SWPA.

### Process

* Rolling Letter of Inquiry (LOI). Decision typically within **60–90 days** of LOI submission【281097117836681†L60-L120】.
* Invited proposals follow LOI acceptance.

### Funder Emphasis

* Clear theory of change.
* Sustained impact beyond the grant period.
* Alignment with Heinz program areas (Creativity, Learning, Sustainability).
* Demonstrated organizational capacity.

### Implications for FID Design

* **Scout:** Heinz is rolling, not deadline-driven — Scout's job is to surface fit, not to time submission.
* **Scribe:** LOI format is its own document type with specific structural conventions; Scribe must distinguish LOI voice from full-proposal voice.
* **Judge:** theory-of-change clarity is the most-scored dimension.
* **Red Team:** challenge geography (SWPA is a defined region — verify the project actually serves it); challenge 501(c)(3) status.
* **Logician:** P0 gates on tax-exempt status, geographic eligibility.

---

## Richard King Mellon Foundation

### Mission / Geography

The Richard King Mellon Foundation funds work primarily in Southwestern Pennsylvania and in Western Pennsylvania conservation habitats, with strategic interests in conservation, economic development, and social impact【903441299371880†L60-L150】.

### Six Program Areas

1. **Conservation** — land conservation, habitat protection, watershed health.
2. **Economic Development** — regional competitiveness, workforce, sector growth.
3. **Economic Mobility** — pathways out of poverty, workforce development, education-to-career.
4. **Health & Well-Being** — health systems, access, mental health.
5. **Organizational Effectiveness** — capacity building for grantee organizations.
6. **Social-Impact Investments** — PRI and MRI vehicles in addition to grants.

### Eligibility

* Nonprofits (501(c)(3)).
* Public agencies.
* Mission-driven for-profits (for social-impact investments specifically).

### Funder Emphasis

* **Scale** — projects that move the needle at regional level, not pilot-only work.
* **Permanence** — durable institutional or land-conservation outcomes.
* Strong leadership and governance.
* Measurable, time-bounded outcomes.

### Implications for FID Design

* **Scout:** RK Mellon is invitation-oriented; the LOI process is a relationship gate. Track relationship readiness as a separate signal class.
* **Scribe:** scale and permanence framing must be primary; "pilot" or "proof of concept" language is often penalized.
* **Judge:** distinct rubric dimensions for scale potential, durability, and measurable outcomes.
* **Red Team:** challenge scale claims that lack a credible pathway; challenge permanence claims that rely on continued philanthropic subsidy.
* **Logician:** P0 gates on eligibility (note that for-profits are eligible only for social-impact-investment program).

---

## NCBA CLUSA – Cooperative Authenticity Layer

### Note

NCBA CLUSA is **not** a standalone funder. It is the National Cooperative Business Association / Cooperative League of the USA — a federation of cooperatives that anchors the seven cooperative principles in U.S. policy and practice.

### Cooperative Principles (relevant to grant scoring)

The Rochdale principles, as adapted and promulgated by the International Co-operative Alliance and reinforced by NCBA CLUSA, include:

1. Voluntary and open membership.
2. **Democratic member control — one member, one vote.**
3. Member economic participation — **patronage** distributions in proportion to use.
4. Autonomy and independence.
5. Education, training, and information.
6. Cooperation among cooperatives.
7. Concern for community.

### Use in Grants

Multiple USDA programs (RCDG, VAPG, RBDG) and many foundation funders explicitly favor or require cooperative governance. The two principles that scoring routinely tests are **one-member-one-vote** and **patronage**【204986117928478†L60-L120】.

### Implications for FID Design

* NCBA CLUSA is a **reusable overlay**, not a per-funder charter. Encode the cooperative-authenticity check as a cross-funder validator that any FID can compose into its rubric.
* **Scribe:** when the applicant is a cooperative, draft language must reflect one-member-one-vote and patronage explicitly; vague "member-driven" language scores lower than specific governance citation.
* **Judge:** cooperative-authenticity is a binary signal — either the bylaws confirm one-vote and patronage or they don't.
* **Red Team:** challenge cooperative claims by checking actual bylaws, not marketing materials.
* **Logician:** cooperative-authenticity gate may be HIGH-warning when the funder favors cooperatives, or P0 when the funder requires them (e.g., VAPG producer-owned definition).

---

## Designing Specialised Agents Across Sections

### Architecture

Every funder profile and every program profile in this canonical reference exposes five orthogonal dimensions that map to the five council seats:

| Seat | Reads from FID | Output |
|---|---|---|
| **Scout** | discovery channels, deadline cadence, fit signals | candidates surfaced with verified live endpoint |
| **Scribe** | scaffold sections, voice/register, mandatory framings | draft sections per grant type |
| **Judge** | rubric dimensions, scoring weights, evaluation themes | scored draft with dimension-by-dimension breakdown |
| **Red Team** | failure modes, common misreadings, claim-vs-evidence gaps | adversarial challenges + rebuttal expectations |
| **Logician** | P0 gates, HIGH/MED warnings, cost-share thresholds | deterministic pass/fail before draft leaves the cycle |

### Benefits

* Each seat operates on the slice of the FID it needs and ignores the rest — reduces context bleed and routing complexity.
* New funders are added by authoring one FID charter; the council automatically inherits the right rubric, gates, and warnings.
* The same FID drives Scout fit scoring at discovery time and Judge rubric scoring at draft time — single source of truth.

### When Per-Sheet Agents

Most funders are served by the shared seat configuration described above. Per-sheet specialist agents are warranted when:

* A program's rubric has a dimension that no other program shares (e.g., NIFA scientific rigor at the level of peer-review standards).
* A funder's relationship dynamics dominate the application path (e.g., RK Mellon relationship-readiness signal).
* A funder's compliance regime is uniquely complex (e.g., USDA-RD Davis-Bacon construction work).

In those cases, the per-sheet specialist composes the shared seat as its base and adds program-specific behavior — never the reverse.

---

## Footer

**Status:** canonical reference. All FID charters must reconcile to this doc. Variations require source-backed justification.

**Authored:** 2026-05-18 from operator-supplied synthesis.

**Cross-references:**

* Pillar-1 charter set: [PR #33 — FID Pillar-1 charters](https://github.com/FIT-Farms/GoldenQuill/pull/33)
* Methodology: [`docs/FID_REFINEMENT_METHODOLOGY_2026-05-18.md`](./FID_REFINEMENT_METHODOLOGY_2026-05-18.md)
* Charter directory: `pipeline/funder_intelligence/pillar_1_charters/`
* Charter template: `pipeline/funder_intelligence/_templates/depth_charter_template.md`

**Citation notation:** The 【XXX†L#-L#】 markers indicate source-document IDs and line ranges from the operator's source-anchored synthesis. They are preserved verbatim as evidence anchors and must not be stripped or paraphrased during downstream charter authoring.
