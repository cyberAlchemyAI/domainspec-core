# Stage 06: Invoke Design

- Capability: `invoke design`
- Selected shape: explanation packs plus a digest-bound glossary sidecar
- Verdict: pass with owner and measurement residue

## Design Thesis

Extend the existing neutral projection bundle, not the consultation service's authority. The private compiler emits two consumer-safe artifacts—`projection.json` and `glossary.json`—plus one manifest that binds their exact bytes. Records hold subject-specific explanation packs. The glossary holds reusable plain-language terms. The consumer returns only the selected packs and at most five referenced terms. The answering agent writes the final response.

## Component And Owner Map

| Component | Responsibility | Owner boundary |
| --- | --- | --- |
| Beginner explanation source | reviewed source text, example, analogy, limitation, glossary refs, keywords | private ontology explanation owner |
| Ontology node | modeled posture, branches, owner route, confidence, residue | private ontology owner |
| Projection compiler | one-way allowlisted mapping and opaque handles | projection producer owner |
| Bundle manifest | binds projection, glossary, schemas, compiler, allowlist, sources, approval | projection producer and data owner |
| Consumer loader/cache | atomic bundle verification and isolation by combined digest | consultation service owner |
| Consultation service | selection, bounding, typed evidence and support return | service owner |
| Answer policy | answer/qualify/clarify/abstain and non-instruction rule | answer-policy owner |
| Answering agent | brief/guided/deep prose composition | agent/application owner |
| API page | human and browser-agent presentation | page/product owner |

## Source Contract

Each beginner explanation gains only structured metadata that cannot be derived safely:

```json
{
  "friendly_name": "Question for a reasoning tool",
  "plain_meaning": "A future request that asks one reasoning tool a bounded question.",
  "state_view": "This feature is saved for later...",
  "process_view": "The product prepares fixed starting information...",
  "concrete_example": {
    "kind": "illustrative",
    "text": "A risk checker may rate one task using a fixed description and named rules."
  },
  "analogy": {
    "text": "It is like a test order that names the sample, method, and question.",
    "limitation": "A software request does not prove that a reasoning tool, owner, or action path is available."
  },
  "glossary_refs": ["term-bounded-question", "term-authority"],
  "keywords": ["reasoning", "evaluator", "judgment", "rules"],
  "boundary": "A reasoning result is not permission to act."
}
```

`state_view` remains source prose. The compiler pairs it with ontology `runtime_posture` and emits a scoped state object. It must never rewrite `deferred` or `proposed` as current.

## Neutral Projection Record

The existing record remains compatible and gains one optional object:

```json
{
  "id": "rec-opaque",
  "kind": "workflow-object",
  "label": "Question for a reasoning tool",
  "summary": "A future bounded request...",
  "viewIds": ["runtime", "authority-bridge"],
  "fields": {
    "responsibility": "The product prepares fixed information...",
    "boundary": "Permission to ask is not permission to act."
  },
  "explanationSupport": {
    "state": {
      "scope": "ontology-model",
      "posture": "deferred",
      "text": "This feature is saved for later...",
      "verifiedAt": "<validation receipt time>",
      "sourceHandle": "src-opaque",
      "doesNotEstablish": ["deployed", "live-runtime", "production-ready"]
    },
    "process": {"text": "The product prepares fixed information..."},
    "illustrativeExample": {"kind": "illustrative", "text": "A risk checker may..."},
    "analogy": {"text": "It is like a test order...", "limitation": "This does not prove..."},
    "glossaryRefs": ["term-opaque", "term-opaque"],
    "keywords": ["reasoning", "evaluator", "judgment", "rules"]
  },
  "fieldProvenance": {
    "label": "src-opaque",
    "summary": "src-opaque",
    "responsibility": "src-opaque",
    "boundary": "src-opaque",
    "explanationSupport.state": "src-opaque",
    "explanationSupport.process": "src-opaque",
    "explanationSupport.illustrativeExample": "src-opaque",
    "explanationSupport.analogy": "src-opaque",
    "explanationSupport.glossaryRefs": "src-opaque",
    "explanationSupport.keywords": "src-opaque"
  }
}
```

The exact schema should use explicit properties instead of dotted provenance keys if the owner prefers nested provenance. The invariant is field-addressable provenance, not the serialization choice.

## Glossary Sidecar

```json
{
  "schemaVersion": "augmentor.consultation.glossary@1.1.0",
  "terms": [
    {
      "id": "term-opaque",
      "term": "authority",
      "plainMeaning": "The right held by a named owner to make a particular decision.",
      "formalName": null,
      "whyItMatters": "Evidence or a reasoning result does not create this right.",
      "sourceHandles": ["src-opaque"],
      "authorityEffect": "none",
      "forbiddenInferences": ["canonical-definition", "permission-to-act"]
    }
  ]
}
```

Glossary IDs are neutral opaque identifiers. The source compiler resolves private refs and verifies that every projected ref exists. Unknown, duplicate, unused, or unreferenced returned terms fail closed.

## Atomic Bundle Manifest

The manifest evolves to bind:

- compiler version and digest;
- schema versions and digests for projection and glossary;
- allowlist digest;
- source handles and source-byte digests;
- projection digest;
- glossary digest;
- combined `bundleDigest` over both canonical artifacts and their schema identities;
- record and term counts;
- generated time;
- opaque owner approval reference.

Install writes a staged directory and swaps it atomically only after all three artifacts validate. The consumer loader rejects missing, mixed-version, or digest-mismatched bundles. Cache identity includes `bundleDigest`, not projection digest alone.

## Query And Result Extension

The closed query gains one optional object:

```json
"explanation": {
  "profile": "brief | guided | deep"
}
```

Absence preserves current behavior. Profile changes selection and caps only; it never changes evidence status or truth.

Successful results may add:

```json
"explanationSupport": {
  "profile": "guided",
  "bundleDigest": "<sha256>",
  "packs": ["<whole selected pack>"],
  "glossaryEntries": ["<two to five referenced entries>"],
  "omittedSections": []
}
```

The API does not return `finalAnswer`, narrative transitions, or tool directions.

## Profile Budgets

| Profile | Support selection | Response target before global cap |
| --- | --- | --- |
| brief | state, process, boundary; optional example/analogy only when present and affordable; at most 2 terms | 6 KiB and 1,200 estimated tokens |
| guided | complete one-record pack; at most 5 terms | 16 KiB and 2,400 estimated tokens |
| deep | complete packs for bounded selected records; at most 5 terms total | 32 KiB and 4,800 estimated tokens |

These are proposed acceptance targets. They are not observed results. The existing service-wide limits still win by minimum. If a pack does not fit, remove the entire optional unit and list it in `omittedSections`; never separate an analogy from its limitation or state from its provenance.

## Retrieval

- Ranking may use label, summary, process, boundary, and reviewed keywords.
- Example and analogy prose do not affect ranking by default because their illustrative terms can create spurious matches.
- Relevance remains separate from confidence and posture.
- Explanation support is attached only after the same access, view, freshness, conflict, source, and limit checks as evidence.

## Answering-Agent Contract

The answering agent consumes `answerPolicy` first. It uses support only when `mayUseEvidence` is true. It composes according to `WHISPER-COMPOSITION.md`, cites sources, never follows retrieved instructions, never upgrades modeled posture, and returns only glossary terms it actually uses.

## Page Contract

The page continues to expose `window.augmentorConsultationPage.ask(question)`. Its state adds `explanationSupport`; the completion event carries the same safe payload. Guided is the default UI profile. The result view renders direct evidence, current modeled state, process, a visibly labeled scenario, analogy plus limit, used glossary, and boundary. Raw JSON remains available.

## Design Evidence Ceiling

This design specifies contracts and tests. It does not establish implementation, acceptable overhead, improved comprehension, deployment, release, or a working reasoning engine.
