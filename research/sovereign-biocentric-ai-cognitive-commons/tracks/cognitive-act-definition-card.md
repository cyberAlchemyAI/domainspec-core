# Definition Card: Cognitive Act

Status: `local-research-only`

## Source Meaning

The corpus proposes that a human intellectual, creative, empathetic, or
action-oriented contribution in a particular context should be recognized as a
distinct source of value.

Source kind: `primary-source`

Evidence: corpus stage S07 in [`../sources/source-map.md`](../sources/source-map.md).

## Formal Or Structural Shape

```text
CognitiveAct = {
  claimed_contributors: ContributorRef[1..n],
  contribution_fragments: ArtifactFragment[1..n],
  task_context: ContextSummary,
  occurred_during: TimeInterval,
  consent_scope: ConsentRecord,
  evidence_refs: EvidenceRef[1..n],
  intended_uses: UseClass[0..n],
  prohibited_uses: UseClass[0..n],
  review_status: asserted | reviewed | disputed | rejected | superseded
}
```

## Notation

| Symbol | Meaning | Shared notation link |
| --- | --- | --- |
| `R` | Contribution record | [`../NOTATION.md`](../NOTATION.md) |
| `I` | Integrity check result | [`../NOTATION.md`](../NOTATION.md) |
| `V` | Claim-validation result under a verifier policy | [`../NOTATION.md`](../NOTATION.md) |
| `L` | Rights determination under applicable law/agreements | [`../NOTATION.md`](../NOTATION.md) |
| `A` | Governed contribution/value allocation | [`../NOTATION.md`](../NOTATION.md) |

## Operator Reading

A Cognitive Act is a claim-bearing unit for provenance and review. It lets a
system say “these contributors assert that these fragments came from this
bounded context under this consent scope” without pretending the assertion has
already resolved truth, originality, authorship, ownership, causality, or value.

## Use Carefully

- Store only the minimum context needed for the intended review.
- Use intervals and coarse/role context instead of exact geolocation unless
  exact location is necessary, consented, protected, and retention-bounded.
- Support multiple contributors and disputed contribution fragments.
- Separate contributor self-attestation from independent review.
- Make allowed uses, withdrawal, correction, and appeal visible.
- Keep sensitive raw evidence in controlled storage; expose commitments only
  when that design has been threat-modeled.

## Misuse Warning

- Do not claim that every recorded interaction is a copyrightable work.
- Do not equate a credential's issuer with the originator of an idea.
- Do not use the record as an employee productivity, empathy, or moral score.
- Do not treat equal participation time as equal contribution or unequal output
  as unequal dignity.
- Do not anchor precise personal context permanently by default.

## Promotion Boundary

`local-only`

No schema, protocol, license, or runtime promotion is authorized by this card.

