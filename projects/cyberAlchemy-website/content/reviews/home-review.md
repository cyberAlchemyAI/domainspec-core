# Home Draft Review

Review task: `SWU-CAW-CONTENT-003`

Target draft: `projects/cyberAlchemy-website/content/drafts/home.md`

Verdict: `flag`

Publication status: not accepted yet.

## Summary

The Home draft is source-safe enough to continue. It does not need to be blocked:
the core method claim is anchored, the authority/status map exists, forbidden
runtime/security/autonomy claims are avoided, and the public copy does not expose
private paths or project residue.

It should be revised before acceptance. The main issue is visitor clarity: the
draft is accurate, but a few examples still depend on internal artifact language
before a new reader has a concrete before/after picture.

## Gate Matrix

| Gate | Verdict | Evidence | Notes |
| --- | --- | --- | --- |
| Source anchors | `pass` | Draft claim map lines 47-56; method source lines 27-43 and 96-123 | Core method and offer claims have anchors. |
| Authority types | `pass` | Draft lines 49-56; Home contract lines 80-88 | Authority types are present and mostly conservative. |
| Status labels | `pass` | Draft lines 49-56; Home contract lines 97-108 | The draft uses `Designed`, `Planned`, and `Open`; no claim is promoted to operating implementation. |
| Claim <= proof | `pass-with-note` | Findings lines 7-28; draft lines 120-132 | Boundary section is explicit and conservative. Consider moving detailed status vocabulary to the Trust page later. |
| Public/private boundary | `pass` | Draft lines 58-144; review scan command in task report | Public body does not expose local paths, raw dispatch detail, token budgets, private project names, or owner handoffs. |
| HTML/PDF authority | `pass` | Findings lines 25-28 and 38-41; draft claim map lines 49-56 | No unaudited HTML/PDF factual authority is used. |
| Home role and explanation method | `pass` | Contract lines 20-34 and 144-170; draft lines 64-76 and 120-144 | It reads as a first-contact offer with method support. |
| Visitor clarity | `flag` | Draft lines 110-118; contract lines 172-181; preset lines 221-227 | Some examples are still internal-facing and may slow down a new reader. |
| CTA | `pass-with-note` | Draft lines 72-76 and 134-144; contract lines 163-170 | CTA labels match the contract. The pilot CTA needs one clarifying sentence before acceptance. |

## Block Findings

None.

## Flag Findings

### F1: Internal artifact vocabulary appears before a visitor-level example

Severity: `flag`

Location: `projects/cyberAlchemy-website/content/drafts/home.md:110`

The `What Changes` section lists page contracts, source-backed inventories,
bounded tasks, work-packs, review surfaces, validator plans, and reusable tools.
Those are accurate to the CyberAlchemy ecosystem, but they read like internal
artifact names before the visitor has seen one plain before/after example.

Why this matters:

- The Home contract warns that the draft may become too internal before
  explaining reader value.
- The Whisper preset flags copy that is true but too internal.
- The Home findings say the first page should lead with problem,
  transformation, audience, proof hint, and CTA.

Recommended revision:

Replace or precede the artifact list with visitor-facing outcomes, such as:

```markdown
A messy strategy folder can become a short decision map. A pile of research can
become a source-backed guide. A risky build idea can become a small, reviewable
next step. A complex system can become a plain explanation of what is known,
what is uncertain, and what should happen next.
```

Keep the precise artifact names for the Method, How It Works, or Examples pages.

### F2: Output examples introduce claims not fully mapped in the claim map

Severity: `flag`

Location: `projects/cyberAlchemy-website/content/drafts/home.md:110`

The claim map anchors the broad method and offer claims well, but the public
draft introduces specific output examples: page contract, source-backed
inventory, bounded task, work-pack, review surface, validator plan, reusable
tool. These are plausible method outputs, yet they are not individually mapped
to anchors/status labels in the review table.

Why this matters:

- The preset requires source anchors, authority type, claim type, and status for
  every load-bearing claim.
- The findings require every page to preserve authority type, claim type, source
  anchors, public-boundary status, and proof labels.

Recommended revision:

Either soften the examples into generic outcomes or add a second claim-map row
for "example output shapes" with `Designed` status, using the CyberAlchemy Method
synthesis and artifact-creation anchors.

### F3: The target audience could be named more plainly

Severity: `flag`

Location: `projects/cyberAlchemy-website/content/drafts/home.md:64`

The opening names situations: ambitious idea, tangled knowledge base, or a run of
agent work. It does not yet name the intended readers as plainly as the contract
does: curious builders, technical founders, research collaborators, and
buyers/adopters evaluating trust.

Why this matters:

- The Home findings say the page should include "who it helps."
- The contract's reader job includes deciding whether to continue into Method or
  How It Works, which is easier when the reader sees themselves early.

Recommended revision:

Add one short audience sentence after the opening, for example:

```markdown
It is for builders, founders, research teams, and careful adopters who have more
context than a chat transcript can safely carry.
```

### F4: The pilot CTA is allowed, but under-explained

Severity: `flag`

Location: `projects/cyberAlchemy-website/content/drafts/home.md:142`

The bounded pilot CTA is allowed by the Home contract as a planned offer. It
should still name what a bounded pilot would inspect or produce, so it does not
feel like a vague sales CTA.

Recommended revision:

Add one phrase to ground the offer:

```markdown
Start with a bounded pilot if you want one scattered body of content turned into
a source map, page contract, or reviewable first artifact.
```

Use this only if the page keeps the pilot as `Planned`, not as proof.

## Pass Findings

### P1: The core method promise is anchored and conservative

The hero and orientation claim that CyberAlchemy turns vague intent and evidence
into useful artifacts. This is supported by the canonical method source and kept
at `Designed` status.

### P2: The draft avoids forbidden broad capability claims

The public copy explicitly says CyberAlchemy is not presented as a shipped
end-to-end runtime, security guarantee, or autonomous replacement for decision
owners.

### P3: Public/private boundary is clean in the public body

The public body avoids local paths, private project names, raw dispatch detail,
token budgets, and owner handoffs.

### P4: CTA structure matches the Home role

`Read the Method` and `See How It Works` match the contract. The optional pilot
CTA is allowed if kept as a planned offer.

## Acceptance Recommendation

Do not publish this draft as-is.

Run a narrow revision task that:

1. Rewrites the `What Changes` examples into visitor-facing outcomes.
2. Adds one sentence naming who the page helps.
3. Grounds the bounded pilot CTA in one concrete deliverable.
4. Either softens specific output examples or adds claim-map coverage for them.

After those edits, rerun this review gate. The likely next verdict should be
`pass` unless the revision introduces a new overclaim.

## Next Route

Recommended next SWU: `SWU-CAW-CONTENT-003R`

Purpose: revise the Home draft using this review, without widening scope to
other pages or website implementation.
