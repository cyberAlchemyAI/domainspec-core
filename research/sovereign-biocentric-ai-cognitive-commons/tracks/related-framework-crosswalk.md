# Related Framework Crosswalk

Target: `Sovereign Biocentric AI and Cognitive Commons`

Checked: `2026-08-03`

Only sources that close named residue or prevent a dangerous analogy are
included. The corpus's remaining unverified links are not silently inherited.

| Framework or source | Why included | Source kind | Closes residue | Boundary |
| --- | --- | --- | --- | --- |
| [W3C DID Core 1.0](https://www.w3.org/TR/did-core/) — Recommendation, 19 July 2022 | Defines DID syntax, documents, controllers, verification methods, and privacy risks | `related-source` | R4, R6 | `borrow-carefully`: identifier/control evidence, not legal identity or ownership |
| [W3C VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/) — Recommendation, 15 May 2025 | Separates verification of issuer statements from truth of claims | `related-source` | R4, R6 | `borrow-carefully`: assertions plus verifier policy |
| [W3C VC Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/) | Defines actual data-integrity proof structures | `related-source` | R4 | `borrow-carefully`: corpus placeholder is not a proof |
| [IPFS CID documentation](https://docs.ipfs.tech/concepts/content-addressing/) and [persistence](https://docs.ipfs.tech/concepts/persistence/) | Corrects hash/CID construction and availability claims | `related-source` | R4, R11 | `borrow-carefully`: integrity/addressing, not persistence or ownership |
| [Arweave protocol documentation](https://docs.arweave.org/developers/development/protocol) and [legal policies](https://www.arweave.org/legal-policies) | Identifies incentive assumptions and deletion/privacy warning | `related-source` | R6, R11 | `block` as default for raw personal or exact-location records |
| [ERC-7007](https://eips.ethereum.org/EIPS/eip-7007) — Final | Defines AIGC NFT model/input/output verification interface | `related-source` | R4 | `block` for training attribution or mandatory rewards |
| [ERC-7857](https://eips.ethereum.org/EIPS/eip-7857) — Final | Defines private-metadata transfer for AI-agent NFTs | `related-source` | R4 | `block` for prompt authorship or cognitive ownership |
| [OSI Open Source Definition](https://opensource.org/osd) and [rejection guidance](https://opensource.org/licenses/common-reasons-for-rejection-of-licenses) | Tests the “open-source CAS License” label | `related-source` | R5 | `block`: current CAS clauses are not OSI-open-source compatible |
| [U.S. Copyright Office AI Report Part 2](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf) | Provides one jurisdiction's human-authorship boundary | `related-source` | R5 | `borrow-carefully`: U.S.-specific; prompts alone ordinarily do not confer output authorship |
| [Brazil LGPD data-subject rights](https://www.gov.br/mcti/pt-br/acesso-a-informacao/lei-geral-de-protecao-de-dados-pessoais-lgpd/direito-dos-titulares) | Grounds access, correction, blocking, deletion, and consent withdrawal concerns | `related-source` | R6 | `borrow-carefully`: applicability and exceptions require legal analysis |
| [UNESCO Ethics of Neurotechnology Recommendation](https://www.unesco.org/en/legal-affairs/recommendation-ethics-neurotechnology) — adopted 11 Nov 2025 | Covers mental-state inference, consent, privacy, manipulation, and oversight | `related-source` | R6, R10 | `borrow-carefully`: normative recommendation, not a self-executing treaty or license |
| [UNESCO Ethics of AI Recommendation](https://www.unesco.org/en/legal-affairs/recommendation-ethics-artificial-intelligence) — adopted 23 Nov 2021 | Places responsibility across lifecycle actors and preserves human oversight | `related-source` | R12 | `borrow-carefully`: governance baseline, not proof of system compliance |
| [NIST AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10) | Provides lifecycle roles and continuous govern/map/measure/manage framing | `related-source` | R12 | `borrow-carefully`: voluntary framework; current 1.0 is being revised |
| [ILO Working Paper 170](https://www.ilo.org/publications/ai-systems-work-changing-psychosocial-work-environment) — 30 Apr 2026 | Bounds AI workplace surveillance, autonomy, and psychosocial risk | `related-source` | R10 | `borrow-carefully`: risks vary by system and context |
| [WHO psychosocial risks and mental health](https://www.who.int/tools/occupational-hazards-in-health-sector/psycho-social-risks-mental-health) | Connects lack of control, work organization, stress, fatigue, and burnout | `related-source` | R10 | `borrow-carefully`: not proof of the corpus's deterministic disease claims |
| [Ravid et al. meta-analysis](https://doi.org/10.1111/peps.12514) and [GAO-25-107126](https://www.gao.gov/products/gao-25-107126) | Supplies a mixed evidence ceiling for electronic monitoring | `related-source` | R10 | `borrow-carefully`: association and heterogeneous effects |
| [Green and Brock](https://doi.org/10.1037/0022-3514.79.5.701) and [narrative-persuasion meta-analysis](https://doi.org/10.1080/03637751.2015.1128555) | Supports a general narrative-influence mechanism | `related-source` | R2 | `analogy-only`: not Romanticism-specific and not a dopamine equivalence |
| [Poetry Foundation introduction to British Romanticism](https://www.poetryfoundation.org/collections/152982/an-introduction-to-british-romanticism) and [Cambridge Romanticism and the Emotions](https://www.cambridge.org/core/books/romanticism-and-the-emotions/4E8D76CEB39EB8E46D61D884748969B1) | Prevents reduction of a diverse historical movement to manipulation | `related-source` | R2 | `analogy-only`: emotion, imagination, skepticism, dissent, and varied forms |

## Bridge Decisions

| Concept | Decision | Rationale | Follow-up |
| --- | --- | --- | --- |
| Provenance assertion | `borrow-carefully` | Standards can make issuer claims tamper-evident | Define trust and verifier policy |
| Content addressing | `borrow-carefully` | Useful byte integrity/addressing | Specify real CID generation and persistence separately |
| Immutable personal record | `block` | Correlation, consent, erasure, and safety risk | Privacy threat model |
| Tokenized training attribution | `block` | ERCs do not establish the claimed relation | Empirical lineage design if pursued |
| CAS open-source license | `block` | OSD conflicts and missing jurisdiction | Legal route |
| Narrative/AI equivalence | `analogy-only` | Different mechanisms and evidence bases | Select a concrete literary corpus for future study |
| Wellbeing-aware AI | `future-work` | Plausible objective without validated effects | Evidence harness |

