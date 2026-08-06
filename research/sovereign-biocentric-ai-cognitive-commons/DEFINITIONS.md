# Governed Local Definitions

Authority: this research tower only.

Promotion status: `local-research-only`

## D1 — Cognitive Act

Source kind: `local-inference` from a `primary-source` proposal.

A Cognitive Act is a bounded human contribution for which the tower can name:

```text
(actor assertion, contribution content, task context, time interval,
 consent scope, evidence references, intended use)
```

Intuition: preserve the person's contextual contribution without claiming that
every interaction is original, valuable, or legally ownable.

Anti-misuse: do not infer authorship, ownership, truth, value, or causal impact
from the presence of a prompt, timestamp, location, or signature alone.

## D2 — Contribution Record

Source kind: `operator-reading`.

```text
R = {
  artifact_digest,
  contributor_assertions[],
  contribution_fragments[],
  context,
  consent_scope,
  evidence_refs[],
  disclosure_policy,
  dispute_status
}
```

Intuition: the record makes an inspectable claim about contribution. It is not
the contribution, the person, or a legal judgment.

Anti-misuse: do not put raw biometrics, private exact location, secrets, or
irreversible personal identifiers into a public immutable layer.

## D3 — Integrity/Truth/Rights Separation

Source kind: `related-source` plus `operator-reading`.

```text
signature verifies issuer control for an assertion
digest verifies byte relationship under an algorithm
verifier policy evaluates whether claims are fit for use
law and agreement determine rights and remedies
governance determines contribution recognition and allocation
```

Intuition: a system can verify that a statement was signed without knowing that
the statement is true. W3C VC Data Model 2.0 explicitly preserves this
distinction.

Anti-misuse: never translate “cryptographically verifiable” into “ethically
owned,” “scientifically validated,” or “eternally rewarded.”

## D4 — Sovereign Support Boundary

Source kind: `local-inference` from the Sovereign Biocentric proposal.

An AI support arrangement satisfies the local boundary only when:

1. the human can understand the relevant role of the system;
2. sensitive collection is minimized and purpose-bound;
3. meaningful override or refusal exists without hidden penalty;
4. responsibility remains attributable across the lifecycle;
5. consequential outputs admit review, correction, and remedy;
6. claimed wellbeing or productivity effects are measured rather than assumed.

Anti-misuse: “human in the loop” is insufficient if the person merely ratifies a
system decision or lacks time, information, authority, or a safe opt-out.

## D5 — Creative Dissonance

Source kind: `operator-reading` from a `primary-source` metaphor.

Creative Dissonance is protected capacity for exploration, dissent, uncertainty,
rest, and non-optimized activity within a safe and consented environment.

Intuition: optimization should not collapse every ambiguous path into the most
predictable one.

Anti-misuse: do not manufacture crisis, burnout, disorder, or insecurity in the
name of creativity. Evidence that narratives influence beliefs does not show
that all emotional intensity improves insight.

## D6 — Negative Outcome Record

Source kind: `local-inference`.

```text
N = (event boundary, affected parties, precursor evidence, observed impact,
 response, uncertainty, safeguards, retention rule, access rule, remedy)
```

Intuition: a failure record should help later actors recognize harm patterns.

Anti-misuse: preserve the minimum evidence needed for learning; do not create a
permanent blame ledger, infer moral character, or expose victims and vulnerable
contributors.

## D7 — Cognitive Commons

Source kind: `local-inference` from a `primary-source` proposal.

A Cognitive Commons is a governed contribution and retrieval system with:

```text
membership + contribution policy + provenance assertions + access control
+ consent/withdrawal + review/appeal + attribution + benefit allocation
+ harm reporting + retention/deletion policy
```

Intuition: collective learning depends on governance and remedy as much as
storage and search.

Anti-misuse: no technical substrate—DAO, blockchain, vector database, VC, or
local model—creates a legitimate commons by itself.

## D8 — Romanticism Analogy

Source kind: `analogy`.

The Romanticism analogy observes that literary language can engage emotion,
imagination, attention, and beliefs, while AI-mediated systems can shape
information environments and respond to behavior.

Intuition: both can influence perception, but their mechanisms, temporality,
institutions, and agency differ.

Anti-misuse: do not describe Romantic literature as a unified manipulation
framework or equate a fixed literary work with adaptive recommender control.

