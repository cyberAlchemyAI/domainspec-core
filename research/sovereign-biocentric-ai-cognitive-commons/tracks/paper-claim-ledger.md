# Source Claim Ledger

Target: `Sovereign Biocentric AI and Cognitive Commons corpus`

Checked: `2026-08-03`

“Accepted” means accepted within the stated evidence ceiling. It never means
canonical promotion.

| ID | Claim | Voice | Source kind | Evidence | Local reading | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | AI should support human creativity and action rather than absorb meaningful agency. | Human prompt, S06 | `primary-source` | [`../sources/source-map.md`](../sources/source-map.md) | Durable design intent | `accepted-as-intent` |
| C2 | AI and Romantic literature both shape perception through logic and emotion. | Assistant, S01 | `analogy` | Corpus S01; Green/Brock; Romanticism sources | Useful opening comparison only | `qualified` |
| C3 | Romantic literature is a manipulation framework that bypasses critical thought. | Assistant, S01-S02 | `primary-source` | Corpus; checked literary sources | Reductive and unsupported as a period-wide claim | `blocked` |
| C4 | Narrative transportation can affect story-consistent beliefs. | Tower synthesis | `related-source` | Green and Brock, DOI `10.1037/0022-3514.79.5.701` | General narrative mechanism, not Romanticism-specific | `accepted-qualified` |
| C5 | Adaptive digital systems can influence thinking and decision-making. | Assistant, S01-S04 | `related-source` | UNESCO AI Ethics Recommendation | A socio-technical risk requiring lifecycle governance | `accepted-qualified` |
| C6 | Empathetic neural systems can eliminate burnout and reliably create flow. | Assistant, S03 | `primary-source` | Corpus; WHO/ILO/GAO boundaries | Desired outcome, not established effect | `blocked` |
| C7 | Intrusive monitoring and loss of autonomy can increase psychosocial risk. | Assistant, S04 | `related-source` | ILO 2026 working paper; WHO; Ravid et al.; GAO | Supported as bounded/mixed population evidence | `accepted-qualified` |
| C8 | Local processing can reduce sensitive-data disclosure. | Assistant, S04/S07 | `local-inference` | UNESCO neurotechnology; privacy guidance | Useful architecture option when verified | `accepted-qualified` |
| C9 | Local processing and aggregation guarantee anonymity, corporate blindness, and safety. | Assistant, S04/S07 | `primary-source` | Corpus; W3C/ICO privacy guidance | Aggregates can identify people; implementation and power matter | `blocked` |
| C10 | Data Sanctuary + Creative Dissonance + Agency Sovereignty necessarily produces wellbeing and innovation. | Assistant, S04-S07 | `operator-reading` | Corpus | Candidate design hypothesis requiring measures | `future-work` |
| C11 | Every Cognitive Act has inherent scientific, legal, and economic ownership. | Assistant, S07 | `primary-source` | Corpus; US Copyright Office AI Report Part 2 | Contribution, expression, rights, and value are distinct | `blocked` |
| C12 | A timestamp, exact location, digest, and DID together prove source authorship. | Assistant, S07-S08 | `primary-source` | DID Core; VC Data Model 2.0 | Can support an issuer assertion and integrity evidence, not truth or legal authorship | `blocked` |
| C13 | W3C VCs can carry tamper-evident issuer claims. | Assistant, S08 | `related-source` | W3C VC Data Model 2.0 and Data Integrity 1.0 | Borrow for provenance assertions with verifier policy | `accepted-qualified` |
| C14 | The corpus Python creates a digital signature. | Assistant, S08 | `primary-source` | Hard-coded placeholder `jws`; no key/sign operation | Demonstration-shaped JSON only | `false-blocked` |
| C15 | `"ipfs://Qm" + truncated SHA-256 hex` is a valid IPFS CID. | Assistant, S08 | `primary-source` | IPFS CID docs and CID specification | CIDv0 is base58btc multihash; CID construction includes codec/format | `false-blocked` |
| C16 | IPFS provides eternal availability. | Assistant, S08 | `primary-source` | IPFS persistence documentation | Content addressing does not guarantee storage or retrieval | `false-blocked` |
| C17 | Arweave mathematically guarantees availability for centuries. | Assistant, S08 | `primary-source` | Arweave protocol and legal policies | An incentive/economic design with assumptions, not unconditional certainty | `blocked` |
| C18 | ERC-7007 forces models to cite and reward training-data contributors. | Assistant, S08-S09 | `primary-source` | ERC-7007 Final specification | Verifies configured AIGC model/input/output relations; not weight provenance | `false-blocked` |
| C19 | ERC-7857 establishes human prompt authorship and payment. | Assistant, S09 | `primary-source` | ERC-7857 Final specification | Governs private metadata transfer for AI-agent NFTs | `false-blocked` |
| C20 | A ZKP can prove a system did not manipulate a person. | Assistant, S07-S08 | `primary-source` | ZKP scope in cited standards | Only proves the encoded relation; behavioral non-manipulation requires a threat model and evidence | `false-blocked` |
| C21 | CAS is an enforceable open-source license. | Assistant, S07 | `primary-source` | OSI OSD and rejection guidance | Behavioral, royalty, processing, and technology restrictions conflict with OSD | `false-blocked` |
| C22 | Human prompting automatically makes the prompter author of AI output. | Assistant implication, S07-S08 | `related-source` | U.S. Copyright Office AI Report Part 2 | Not the general U.S. rule; prompt expression and edited arrangements require separate analysis | `blocked-jurisdiction-bound` |
| C23 | Immutable time/location/biometric attribution is privacy-preserving. | Assistant, S07-S08 | `primary-source` | W3C privacy considerations; LGPD/GDPR; UNESCO | Creates correlation, safety, consent, and erasure conflicts | `blocked` |
| C24 | A governed commons can attribute contributions and return value. | Human prompt and assistant, S10 | `local-inference` | Corpus | Plausible design objective; allocation and legitimacy remain open | `future-work` |
| C25 | Historical harms should be retained as learning evidence. | Human prompt, S11 | `primary-source` | Corpus | Borrow as minimized, consented Negative Outcome Records | `accepted-qualified` |
| C26 | Because AI lacks moral agency, all harm is the end user's responsibility. | Assistant, S11 | `primary-source` | UNESCO AI Ethics; NIST AI RMF | Ultimate responsibility belongs to people/legal entities across lifecycle roles, not only one user | `blocked-as-oversimplified` |

## Source-Kind Rules

- `primary-source`: stated by the main corpus; this label does not certify truth.
- `related-source`: stated by a directly checked external authority or study.
- `local-inference`: inferred from source-backed material.
- `analogy`: useful comparison, not source equivalence.
- `operator-reading`: practical design interpretation.
- `open-residue`: unresolved question or future task.

## Open Claim Residue

| ID | Question | Blocking artifact | Next route |
| --- | --- | --- | --- |
| R1 | Exact turn-level human/model provenance | Original conversation export | Source recovery |
| R5 | CAS enforceability and covered asset | Jurisdiction and legal review | Legal counsel/decision gate |
| R7 | Human-outcome and contribution metrics | Measured protocol | `research-evidence-harness` |
| R9 | Fair collective allocation | Community-approved governance | Decision gate plus evidence harness |

