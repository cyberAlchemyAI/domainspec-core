# Whisper writing-framework integration research substrate

This file is a mechanical collation of the verbatim structured explorer returns. It contains no synthesizer, reviewer, writer, or auditor content.

## writer-science-pdf-explorer

Source: `runtime/run-001/raw-results/explorers/spawn-0001.json`
SHA-256: `c5a72ad826e682eda0835afe3b254e02376e44fd1d2d666cbc7960c1c12a4dc0`

```json
{
  "task_status": "completed",
  "evidence_gate_status": "ready",
  "artifacts": [
    {
      "artifact_type": "exact_bound_pdf_extraction",
      "source_id": "writer-science-anatomy-great-essay-v1",
      "source_title": "Anatomy of a Great Essay: A Visual Guide to Expert Writing",
      "source_digest_sha256": "fddbb4ea730acb73475683d3472d4ce2abaf62a8c3a1a82abc8ed4dd2fc468b4",
      "page_count_observed": 4,
      "authority": "user-supplied source; not canonical Whisper authority",
      "claim_classes": {
        "explicit_source_claim": "A rule, definition, or benefit stated directly by the PDF.",
        "example": "Quoted third-party prose used to illustrate a pattern; it does not independently prove the rule or benefit.",
        "marketing_assertion": "A broad effectiveness, reader-response, naturalness, or value claim supplied without evidence in the PDF.",
        "inferred_lineage": "Terminology suggests an intellectual tradition, but the PDF does not attribute it.",
        "interpretation": "This explorer's bounded mapping or limitation, not a PDF claim."
      },
      "component_rows": [
        {
          "component_id": "WS-TITLE-01",
          "page": 1,
          "local_anchor": "A GOOD TITLE",
          "unit_level": "title",
          "component": "Clear title with one of four curiosity triggers: question or puzzle, unresolved sequence, expectation violation, or knowledge asymmetry.",
          "problem": "Cryptic titles and inside jokes do not establish a useful reason to read.",
          "preconditions": "A title is needed and the subject can honestly sustain the selected curiosity trigger.",
          "claimed_benefit": "Clarity plus curiosity.",
          "counterexample_or_limitation": "No evidence is supplied that these four triggers are exhaustive or appropriate for every transport; curiosity can conflict with exact technical or legal naming.",
          "likely_whisper_owner_surface": "transport or preset contract; possibly reusable title technique",
          "proof_status": "explicit prescription; claimed benefit is unverified marketing assertion"
        },
        {
          "component_id": "WS-WHOLE-01",
          "page": 1,
          "local_anchor": "INVERT YOUR POINT / BE FAIR / BUT... / STATE THE COST / MAKE YOUR POINT",
          "unit_level": "whole essay",
          "component": "Reader movement from Status Quo to Point through fair concession, instability, and perceived cost or benefit.",
          "problem": "A central claim has little value if it does not displace a belief that matters to the intended reader.",
          "preconditions": "A specific reader, a sincere articulable Status Quo, a defensible Point, an instability, and a reader-relevant cost or benefit.",
          "claimed_benefit": "The Point gains value from the distance it moves the reader from the prior belief; fair concession earns trust.",
          "counterexample_or_limitation": "Not every essay overturns a reader belief; descriptive, exploratory, procedural, commemorative, or genuinely uncertain writing may lack a single invertible Point. The trust and value claims are not evidenced.",
          "likely_whisper_owner_surface": "trajectory_core plus composition_plan; fair-concession technique",
          "proof_status": "explicit framework rule; reader-value and trust effects are unverified marketing assertions"
        },
        {
          "component_id": "WS-INTRO-01",
          "page": 1,
          "local_anchor": "LEVEL 2 — THE INTRODUCTION: COMMON GROUND / PROBLEM / SOLUTION",
          "unit_level": "introduction",
          "component": "Open with taken-for-granted common ground, establish a costly problem, then promise a solution fulfilled by the body.",
          "problem": "Readers may not perceive the subject as a problem worth solving.",
          "preconditions": "Problem-solution writing, identifiable shared context, reader-relevant stakes, and a body capable of fulfilling the promised resolution.",
          "claimed_benefit": "Motivates the reader to take the problem seriously and establishes the value of the Point.",
          "counterexample_or_limitation": "Poor fit for genres whose job is not problem resolution. The PDF supplies no method for audiences lacking common ground or for multiple competing problems.",
          "likely_whisper_owner_surface": "composition pattern governed by trajectory_core; transport-specific applicability",
          "proof_status": "explicit structure; motivational benefit unverified"
        },
        {
          "component_id": "WS-INTRO-02",
          "page": 1,
          "local_anchor": "MAKE READERS CARE",
          "unit_level": "introduction",
          "component": "Reject Background→Thesis, General→Specific, and Gap→Niche introduction patterns; frame the text as a solution and the introduction as the problem statement.",
          "problem": "Introductions that merely supply context may fail to make the reader care.",
          "preconditions": "The document can coherently be framed as solving a reader-relevant problem.",
          "claimed_benefit": "An introduction that does not repel and makes the relevance of the text legible.",
          "counterexample_or_limitation": "The prohibition is categorical but unsupported. The PDF's own Common Ground opening can function as background or general context, and Problem→Solution can overlap a gap-and-niche move.",
          "likely_whisper_owner_surface": "experiment-only candidate or transport-specific composition pattern; not a base gate",
          "proof_status": "explicit polemical prescription; universal rejection is unsupported and internally tensioned"
        },
        {
          "component_id": "WS-INTRO-03",
          "page": 1,
          "local_anchor": "HOOKS DON'T WORK",
          "unit_level": "opening",
          "component": "A catchy opening has value only when it vividly establishes a relevant problem; startling facts, quotations, and stories are not independently valuable.",
          "problem": "Attention devices can be detached from reader relevance.",
          "preconditions": "A relevant problem exists and the hook directly sets it up.",
          "claimed_benefit": "Relevance rather than superficial catchiness.",
          "counterexample_or_limitation": "The heading's categorical claim is immediately qualified in the body. No evidence establishes what readers value or that problem setup is the only valid function of an opening.",
          "likely_whisper_owner_surface": "relevance_core plus optional opening technique and human editorial check",
          "proof_status": "explicit qualified prescription; reader-preference assertion unverified"
        },
        {
          "component_id": "WS-WHOLE-02",
          "page": 1,
          "local_anchor": "THE PROBLEM, SOLVED",
          "unit_level": "conclusion",
          "component": "Return to the opening problem, show it settled, and link its resolution to a broader question.",
          "problem": "The body may not visibly fulfill the introduction's promise or leave forward significance.",
          "preconditions": "The opening established a problem and the essay can legitimately claim some degree of resolution.",
          "claimed_benefit": "Promise fulfillment and broader relevance.",
          "counterexample_or_limitation": "The source does not accommodate intentionally unresolved inquiry, partial results, or findings that invalidate the original problem framing.",
          "likely_whisper_owner_surface": "composition_plan or trajectory_core; conclusion technique",
          "proof_status": "explicit prescription; benefit unverified"
        },
        {
          "component_id": "WS-IDX-01",
          "page": 1,
          "local_anchor": "SET READER EXPECTATIONS / KEEP THE PROMISE",
          "unit_level": "every discourse unit",
          "component": "Each unit opens with an Index that announces what the unit is doing; the remainder develops that announced idea.",
          "problem": "Readers may not know how to interpret a unit or what development to expect.",
          "preconditions": "A unit has a coherent controlling purpose that can be announced before its development.",
          "claimed_benefit": "Readers can identify the unit's function and interpret what follows.",
          "counterexample_or_limitation": "The universal 'every unit' scope is unsupported and may not fit delayed-reveal, narrative, lyric, dialogic, or intentionally inductive structures.",
          "likely_whisper_owner_surface": "reusable composition pattern plus human structural check",
          "proof_status": "explicit universal claim; reader effect unverified"
        },
        {
          "component_id": "WS-IDX-02",
          "page": 2,
          "local_anchor": "LEVEL 3 — INDEX & DISCUSSION: SIZE VARIES / 1–3 SENTENCES",
          "unit_level": "paragraph or larger discourse unit",
          "component": "Index length varies with the complexity of the problem: one sentence inside a paragraph, two to three for complexity, opposition, or a question, and potentially a few paragraphs for larger units.",
          "problem": "A fixed-length setup may under-specify a complex unit or overburden a simple one.",
          "preconditions": "The writer can identify the unit boundary and the problem being set up.",
          "claimed_benefit": "Proportional expectation-setting.",
          "counterexample_or_limitation": "Page 1 defines an Index as 1–3 sentences, while page 2 permits a few paragraphs; scope-sensitive reconciliation is plausible but not stated.",
          "likely_whisper_owner_surface": "composition-pattern guidance, not conservative executable lint",
          "proof_status": "explicit guidance with unresolved internal scope inconsistency"
        },
        {
          "component_id": "WS-IDX-03",
          "page": 2,
          "local_anchor": "KEY TERMS",
          "unit_level": "Index–Discussion unit",
          "component": "The Index often closes with words naming the unit's core concepts, which are developed in the Discussion.",
          "problem": "The unit's conceptual center and cohesion may be unclear.",
          "preconditions": "The unit has stable core concepts that can recur without distortion or awkward repetition.",
          "claimed_benefit": "Readers expect and can track conceptual development.",
          "counterexample_or_limitation": "The modal 'often' conflicts with stronger page 1 and page 3 language implying Key Terms in every unit and every Discussion sentence. No threshold distinguishes useful recurrence from redundancy.",
          "likely_whisper_owner_surface": "cohesion technique and human readability check",
          "proof_status": "explicit qualified rule; reader-expectation benefit unverified"
        },
        {
          "component_id": "WS-IDX-04",
          "page": 2,
          "local_anchor": "FIXED STRUCTURE",
          "unit_level": "all discourse units",
          "component": "Index–Discussion is asserted to be a fixed, intuitive structure analogous to Subject–Verb–Object; readers use the Index to interpret the Discussion regardless of authorial intent.",
          "problem": "Unsignalled or uncontrolled interpretation of development.",
          "preconditions": "The discourse actually contains an identifiable initial orienting segment.",
          "claimed_benefit": "Alignment with an allegedly intuitive reader-processing structure.",
          "counterexample_or_limitation": "The analogy crosses grammatical and discourse levels without argument. Languages and genres vary, and the PDF supplies no evidence that all discourse is perceived this way.",
          "likely_whisper_owner_surface": "experiment-only theoretical candidate; reject as universal executable rule",
          "proof_status": "explicit universality and cognition claims; unsupported marketing assertion"
        },
        {
          "component_id": "WS-FRACTAL-01",
          "page": 2,
          "local_anchor": "LEVEL 4 — WRITING IN FRACTALS / EVERY PART REPEATS THE ANATOMY",
          "unit_level": "essay, section, paragraph",
          "component": "Index–Point–Discussion–Conclusion recurs across nested levels; a section is a small essay whose Point controls its paragraphs and supports the parent essay's Point.",
          "problem": "Nested units may lack local control or fail to contribute to the parent claim.",
          "preconditions": "Hierarchical expository or argumentative composition with identifiable parent and child Points.",
          "claimed_benefit": "Local unity plus upward support across levels.",
          "counterexample_or_limitation": "The diagram demonstrates a proposed template, not actual recursion in all writing. Paragraph-level conclusions are not separately explained, and non-hierarchical or multi-voiced structures may resist the model.",
          "likely_whisper_owner_surface": "composition_plan pattern with hierarchical support relation; human semantic review",
          "proof_status": "explicit framework claim; universality and benefit unverified"
        },
        {
          "component_id": "WS-POINT-01",
          "page": 3,
          "local_anchor": "POINT FIRST",
          "unit_level": "section or Index–Discussion unit",
          "component": "For maximal apparent clarity, place the Point early, at the end of the Index.",
          "problem": "Readers may not know the controlling claim soon enough.",
          "preconditions": "Direct exposition is desired and early disclosure does not undermine the transport.",
          "claimed_benefit": "Writing seems clearest.",
          "counterexample_or_limitation": "The wording 'at the end of the beginning' is imprecise; clarity is asserted without evidence and may not be the dominant goal.",
          "likely_whisper_owner_surface": "point-placement technique selected by transport and trajectory",
          "proof_status": "explicit preference; clarity claim unverified"
        },
        {
          "component_id": "WS-POINT-02",
          "page": 3,
          "local_anchor": "POINT LAST / POINT ONCE, NOT TWICE",
          "unit_level": "section or Index–Discussion unit",
          "component": "When the Point is not stated up front, use the Index to prepare it and place it at the end of the Discussion; state it at either beginning or end, not both, and never bury it in the middle.",
          "problem": "A delayed Point may be missed or duplicated.",
          "preconditions": "The unit benefits from inductive or delayed disclosure and the Index can orient readers without stating the Point.",
          "claimed_benefit": "Preserves visibility while allowing delayed revelation.",
          "counterexample_or_limitation": "The absolute prohibition on restating a Point excludes summaries, pedagogical repetition, long-form recall support, and conclusion restatement. No evidence supports 'readers will miss it' in all cases.",
          "likely_whisper_owner_surface": "optional point-placement technique plus human editorial check",
          "proof_status": "explicit rule; universal memory/visibility claim unsupported"
        },
        {
          "component_id": "WS-KEY-01",
          "page": 3,
          "local_anchor": "LEVEL 6 — KEY TERMS / THEMATIC STRINGS",
          "unit_level": "sentence sequence within a Discussion",
          "component": "Key Terms announced by the Index recur through repetition, synonyms, and pronouns, forming thematic strings across sentences.",
          "problem": "Successive sentences may lack visible lexical or referential continuity.",
          "preconditions": "Stable referents or concepts, resolvable pronouns, and variation that preserves meaning.",
          "claimed_benefit": "Readers experience the lexical thread as coherence.",
          "counterexample_or_limitation": "The two excerpts are examples, not tests of causality. Several displayed strings use associative or hierarchical relations rather than strict repetition, synonymy, or pronominal reference. Forced threading can create monotony or semantic drift.",
          "likely_whisper_owner_surface": "cohesion technique and human readability check; at most conservative lint for missing/ambiguous recurrence",
          "proof_status": "explicit technique and reader-effect claim; examples illustrate but do not prove benefit"
        },
        {
          "component_id": "WS-PARA-01",
          "page": 4,
          "local_anchor": "CONSTANT THEME",
          "unit_level": "clause sequence or paragraph",
          "component": "Repeat the same Topic across successive clauses while each Comment adds new information.",
          "problem": "A paragraph may wander away from its controlling Key Term.",
          "preconditions": "A single stable discourse Topic can appropriately anchor the sequence.",
          "claimed_benefit": "Maintains focus while elaborating different aspects.",
          "counterexample_or_limitation": "Poor fit where progression, contrast, multiple actors, or causal sequence requires Topic change. The cited Happiness passage is illustrative only.",
          "likely_whisper_owner_surface": "paragraph information-flow technique and human readability check",
          "proof_status": "explicit pattern and benefit claim; example-only support"
        },
        {
          "component_id": "WS-PARA-02",
          "page": 4,
          "local_anchor": "LINKING PATTERN Old → New",
          "unit_level": "clause sequence or paragraph",
          "component": "New information in one clause's Comment becomes old information in the next clause's Topic, creating a chain.",
          "problem": "Transitions between propositions may be abrupt or unmotivated.",
          "preconditions": "Each step introduces an entity or concept suitable to become the next clause's Topic.",
          "claimed_benefit": "Backward and forward linkage across clauses.",
          "counterexample_or_limitation": "The PDF describes the chain but does not specify when it should stop, how to handle branching, or how distant lexical inference can be before linkage fails. The Lorenz excerpt is illustrative only.",
          "likely_whisper_owner_surface": "paragraph information-flow technique and human flow review",
          "proof_status": "explicit pattern; benefit is plausible but untested in source"
        },
        {
          "component_id": "WS-PARA-03",
          "page": 4,
          "local_anchor": "SUPER THEME",
          "unit_level": "Index plus Discussion clauses",
          "component": "The Index Comment introduces a category; subsequent Discussion Topics name its parts.",
          "problem": "A paragraph enumerating related parts may lack a visible organizing category.",
          "preconditions": "A genuine category-to-member or whole-to-part relation exists.",
          "claimed_benefit": "Organized elaboration under one higher-order theme.",
          "counterexample_or_limitation": "The parenthetical terminology is reversed: the category is called a 'hyponym' and its parts 'hypernyms', contrary to standard lexical relation usage. The source's structural intent remains visible, but the labels must be flagged rather than silently repaired.",
          "likely_whisper_owner_surface": "composition/cohesion technique with human semantic review",
          "proof_status": "explicit pattern; internally inconsistent terminology; cited brain passage is example-only"
        },
        {
          "component_id": "WS-PARA-04",
          "page": 4,
          "local_anchor": "THEME PREVIEW",
          "unit_level": "Index plus Discussion clauses",
          "component": "The Index Comment previews Key Terms; Discussion Topics pick them up and Comments develop them across successive clauses.",
          "problem": "A multi-part Discussion may not signal its planned conceptual coverage.",
          "preconditions": "The writer can name the upcoming parts accurately and the Discussion follows that preview.",
          "claimed_benefit": "Expectation-setting and coherent development of multiple Key Terms.",
          "counterexample_or_limitation": "Can become mechanical, spoil deliberate discovery, or mislead when the Discussion evolves. The morality passage illustrates one clean enumeration but does not establish general efficacy.",
          "likely_whisper_owner_surface": "composition pattern plus cohesion technique and human promise-fulfilment check",
          "proof_status": "explicit pattern; example-only support"
        }
      ],
      "examples_and_attribution": [
        {
          "page": 3,
          "use": "Key Terms and thematic strings",
          "credited_sources": ["James Frazer, The Golden Bough", "David Deutsch, The Beginning of Infinity"],
          "proof_status": "illustrative excerpts only"
        },
        {
          "page": 4,
          "use": "paragraph information-flow patterns",
          "credited_sources": ["Mihaly Csikszentmihalyi, Flow: The Psychology of Optimal Experience", "James Gleick, Chaos: Making a New Science", "Steven Pinker, The Language Instinct", "Jonathan Haidt, The Righteous Mind: Why Good People are Divided by Politics and Religion"],
          "proof_status": "illustrative excerpts only"
        }
      ],
      "inferred_lineage": [
        {"terms": "Topic, Comment, theme, old and new information", "inference": "The vocabulary resembles theme-rheme and information-structure traditions.", "status": "inferred only; the PDF provides no theory citation or lineage claim"},
        {"terms": "hyponym, hypernym", "inference": "The vocabulary invokes lexical-semantic taxonomy.", "status": "inferred only; the PDF provides no source and appears to reverse the terms"},
        {"terms": "Common Ground, Problem, Solution and Status Quo, Cost, Point", "inference": "The sequence may overlap established problem-framing and rhetorical-movement families.", "status": "comparison forbidden on this lane; no lineage assigned"}
      ],
      "internal_inconsistencies": [
        {"pages": [1, 2], "issue": "Page 1 defines every Index as 1–3 sentences; page 2 says an Index may extend to a few paragraphs.", "disposition": "Flagged; not repaired. A level-sensitive interpretation is possible but unstated."},
        {"pages": [1, 2, 3], "issue": "Key Terms are said on page 1 to thread through every sentence, page 2 says the Index only 'often' closes with Key Terms, and page 3 again says Key Terms are threaded through every Discussion sentence.", "disposition": "Flagged; exact requirement remains ambiguous."},
        {"pages": [1], "issue": "The heading 'HOOKS DON'T WORK' is contradicted in absolute form by its own statement that catchy openings work when they vividly establish the problem.", "disposition": "Treated as a qualified anti-hook rule, while retaining the headline/body tension."},
        {"pages": [1], "issue": "The PDF rejects Background→Thesis, General→Specific, and Gap→Niche, yet its Common Ground can function as background/general context and its Problem→Solution movement can overlap gap-and-niche structure.", "disposition": "Flagged as conceptual overlap; no external comparison or repair performed."},
        {"pages": [2], "issue": "Index–Discussion is declared fixed and universal while Index size and form are variable and no criteria establish a recognizable Index in every genre.", "disposition": "Flagged as unsupported universality rather than normalized into a softer rule."},
        {"pages": [3], "issue": "Point-Once prohibits stating the Point both early and late, while page 2's fractal diagram includes Point labels near both the start and conclusion bars, creating at least a visual ambiguity about restatement.", "disposition": "Flagged; the diagram may mean structural closure rather than repeated wording, but the PDF does not explain it."},
        {"pages": [4], "issue": "SUPER THEME calls the category a hyponym and its parts hypernyms, reversing the standard direction of those lexical relations.", "disposition": "Flagged verbatim; not silently corrected."}
      ],
      "bounded_owner_summary": [
        {"responsibility": "Status Quo→Cost→Point and Common Ground→Problem→Solution movement", "likely_surface": "trajectory_core and composition_plan", "certainty": "candidate mapping only; current Whisper internals were outside this lane"},
        {"responsibility": "Index–Discussion, fractal nesting, Point-first/Point-last, and conclusion return", "likely_surface": "reusable composition patterns selected by transport and trajectory", "certainty": "candidate mapping only"},
        {"responsibility": "Key Terms, thematic strings, and paragraph Topic–Comment patterns", "likely_surface": "technique_stack plus human readability or semantic checks", "certainty": "candidate mapping only"},
        {"responsibility": "Claims about reader trust, clarity, value, intuitive processing, or coherence", "likely_surface": "experiment-only evidence residue; not executable semantic validation", "certainty": "source provides no outcome evidence"}
      ]
    }
  ],
  "validation": {
    "declared_inputs_read": [
      "ops/development/2026-08-25-whisper-writing-frameworks-research/dispatch-sheet.json",
      "ops/development/2026-08-25-whisper-writing-frameworks-research/source-manifest.json",
      "ops/development/2026-08-25-whisper-writing-frameworks-research/strategy-inventory-packet.json"
    ],
    "manifest_bound_source_read": true,
    "digest_check": {
      "expected": "fddbb4ea730acb73475683d3472d4ce2abaf62a8c3a1a82abc8ed4dd2fc468b4",
      "observed": "fddbb4ea730acb73475683d3472d4ce2abaf62a8c3a1a82abc8ed4dd2fc468b4",
      "result": "pass"
    },
    "page_count_check": {"expected": 4, "observed": 4, "result": "pass"},
    "comparative_web_browsing_performed": false,
    "repository_writes_performed": false,
    "canonical_selection_performed": false,
    "briefing_digest_received": "1761440281a4f20051baa2a346a330db1c0342a71b6336f5bdc26f3163f9cf80"
  },
  "blockers": [],
  "residue": [
    "The PDF gives no empirical evidence for its reader-effect, universality, clarity, trust, value, or coherence claims.",
    "The source does not identify the origins of Index–Discussion, Topic–Comment, old-to-new flow, thematic strings, or the introduction movements.",
    "The four cited prose examples illustrate selected patterns but do not prove causality, completeness, or transport independence.",
    "Likely Whisper owner surfaces are bounded interpretations derived from the dispatch packet, not verified internal ownership findings.",
    "No adoption, schema change, validator rule, promotion, publication, or reader-outcome claim is authorized by this receipt."
  ]
}
```

## comparative-framework-explorer

Source: `runtime/run-001/raw-results/explorers/spawn-0002.json`
SHA-256: `8e8daaf71d17726556693c3ef082c489994480df44a095cce959f766dd6dd558`

```json
{
  "task_status": "completed",
  "evidence_gate_status": "passed",
  "artifacts": [
    {
      "artifact_id": "receipts/explorer-comparative-frameworks.json",
      "artifact_kind": "inline-read-only-receipt",
      "briefing_digest": "944cfd882b342847455fe3809a37972f13944b44c207b5b03faf954bad9253a1",
      "portfolio": [
        {
          "candidate_id": "toulmin-argument",
          "responsibility": "argument and evidence",
          "source": {
            "identity": "Purdue OWL, Toulmin Argument; attributes method to Stephen E. Toulmin and points to The Uses of Argument",
            "url": "https://owl.purdue.edu/owl/general_writing/academic_writing/historical_perspectives_on_argumentation/toulmin_argument.html",
            "date_or_version": "page undated; original method attributed to Toulmin",
            "selectors": ["What is the Toulmin Method?", "lines 28-35", "lines 46-52"]
          },
          "unit_level": "claim or argument cluster",
          "objective": "Expose the inferential bridge between evidence and claim and qualify the claim against exceptions.",
          "mandatory_parts": ["claim", "grounds", "warrant"],
          "conditional_parts": ["backing", "qualifier", "rebuttal"],
          "evidence_and_limitations": "The university guide calls only claim, grounds, and warrant fundamental; the remaining elements may be added as necessary. It is an argument-analysis heuristic, not evidence that every genre or paragraph should instantiate six slots.",
          "attribution_or_license": "Attribute Toulmin. Purdue states all rights reserved and prohibits republication or rewriting without permission; cite and paraphrase, do not reproduce its diagrams or prose.",
          "pdf_overlap": "Partial: both address a point and supporting discussion, but Toulmin distinctly models the warrant, qualification, and rebuttal that the manifest's PDF topic summary does not name.",
          "shortlist": true,
          "shortlist_reason": "Adds inferential accountability rather than another movement or cohesion pattern."
        },
        {
          "candidate_id": "minto-scq",
          "responsibility": "problem framing",
          "source": {
            "identity": "Barbara Minto / Minto Books International, official originator site",
            "url": "https://www.barbaraminto.com/",
            "date_or_version": "site copyright 2007-2026; identifies the 1996 textbook edition",
            "selectors": ["Concept, lines 21-23", "Course, lines 30-32", "Textbook, lines 35-37"]
          },
          "unit_level": "introduction or briefing setup",
          "objective": "Use Situation, Complication, and Question to identify the question in the reader's mind.",
          "mandatory_parts": ["situation", "complication", "question"],
          "evidence_and_limitations": "The official page supports SCQ and its question-identification purpose, but does not publish enough method detail to justify common internet expansions, sequencing rules, or efficacy claims.",
          "attribution_or_license": "Use the marks Minto Pyramid Principle® and SCQ Framework™ accurately. Site says all rights reserved; do not copy course or textbook expression.",
          "pdf_overlap": "High: the manifest says the PDF introduction uses common-ground/problem/solution and whole-essay status-quo/cost/problem/solution movement.",
          "shortlist": false,
          "shortlist_reason": "No non-duplicative responsibility against the supplied PDF; retain as origin/precedent evidence for attribution and conflict analysis."
        },
        {
          "candidate_id": "minto-pyramid",
          "responsibility": "executive structure",
          "source": {
            "identity": "Barbara Minto / Minto Books International, official originator site",
            "url": "https://www.barbaraminto.com/",
            "date_or_version": "site copyright 2007-2026; identifies the 1996 textbook edition",
            "selectors": ["Concept, lines 21-23", "Textbook, lines 35-37"]
          },
          "unit_level": "whole document and recursively grouped supporting ideas",
          "objective": "Present ideas as a pyramid under one governing point.",
          "mandatory_parts": ["single governing point", "supporting ideas organized beneath it"],
          "evidence_and_limitations": "The public originator page supports only this high-level shape. It does not expose sufficient rules to claim MECE, answer-first ordering, or a complete operational method from this source alone.",
          "attribution_or_license": "Attribute Minto and preserve registered/trademark status. All rights reserved; describe the concept without copying proprietary instructional material.",
          "pdf_overlap": "Moderate: overlaps point placement and fractal organization, but adds an executive hierarchy of grouped support under one governing point.",
          "shortlist": true,
          "shortlist_reason": "Distinct responsibility is executive prioritization/hierarchy; shortlist only this narrowly sourced concept, not an inferred full template."
        },
        {
          "candidate_id": "swales-cars",
          "responsibility": "academic and genre movement",
          "source": {
            "identity": "University of Waterloo Writing and Communication Centre, adapted from John Swales and Christine Feak",
            "url": "https://uwaterloo.ca/writing-and-communication-centre/creating-research-space-cars-model",
            "date_or_version": "adaptation cites Academic Writing for Graduate Students, 2013",
            "selectors": [
              "Move 1: Establish a Research Territory, lines 47-58",
              "Move 2: Establish a Niche, lines 59-80",
              "Move 3: Occupying a Niche, lines 81-93",
              "adaptation notice, line 101"
            ]
          },
          "unit_level": "research introduction",
          "objective": "Position a research contribution relative to an existing scholarly territory and an identified niche.",
          "mandatory_parts": ["establish research territory", "establish niche", "occupy niche"],
          "evidence_and_limitations": "Waterloo says it is especially useful in STEM and frames it as help for introductions. The listed niche and occupation strategies are alternatives, not universally mandatory steps. It is genre-bound and should not be universalized to all essays.",
          "attribution_or_license": "Attribute Swales/Feak and the university adaptation. No reuse license was established in this search; cite and paraphrase conservatively.",
          "pdf_overlap": "High surface overlap with common-ground/problem/solution, but CARS distinctly binds those moves to prior scholarship, a research gap or continuation, and the present study.",
          "shortlist": true,
          "shortlist_reason": "Adds genre-specific participation in a scholarly conversation; must remain conditional on a research-introduction transport."
        },
        {
          "candidate_id": "labov-narrative",
          "responsibility": "narrative movement",
          "source": {
            "identity": "William Labov, University of Pennsylvania, Narrative Theory",
            "url": "https://www.ling.upenn.edu/~wlabov/sfs.html",
            "date_or_version": "originator retrospective page; discusses Labov and Waletzky 1967 and later refinements",
            "selectors": [
              "3. Structural types of narrative clauses",
              "Definition 3.1 Abstract",
              "Definition 3.2 Orientation",
              "Definition 3.3 Complicating action",
              "Definition 3.4 Coda",
              "discussion of evaluation and resolution"
            ]
          },
          "unit_level": "personal-experience narrative, from clauses to whole story",
          "objective": "Account for temporal event movement and how a narrative establishes its point or significance.",
          "mandatory_parts": ["sequential complicating action for a minimal narrative"],
          "conditional_parts": ["abstract", "orientation", "evaluation", "resolution", "coda"],
          "evidence_and_limitations": "The originator page says complicating-action clauses are sequential, defines abstract/orientation/coda, and explicitly describes earlier treatment of resolution as imprecise and the framework as incomplete without evaluation. It arose from oral personal-experience narrative and is not a universal prose outline.",
          "attribution_or_license": "Attribute Labov and Waletzky. No explicit reuse license was established; cite definitions and paraphrase rather than copying examples.",
          "pdf_overlap": "Partial at whole-text movement and a story's point; distinct in temporal junctions, reportability, evaluation, and return to speaking time.",
          "shortlist": true,
          "shortlist_reason": "Adds narrative-event responsibility absent from an expository essay movement model, provided it is transport-conditional."
        },
        {
          "candidate_id": "rst",
          "responsibility": "rhetorical relation",
          "source": {
            "identity": "William C. Mann and Sandra A. Thompson, Rhetorical Structure Theory; originator site maintained by Maite Taboada",
            "url": "https://www.sfu.ca/rst/01intro/intro.html",
            "primary_paper_url": "https://www.sfu.ca/rst/05bibliographies/bibs/Mann_Thompson_1988.pdf",
            "date_or_version": "Mann and Thompson 1988, Text 8(3), pp. 243-281",
            "selectors": [
              "Texts, Coherence and Structure, lines 35-40",
              "Nucleus::Satellite Relations, lines 39-45",
              "More Relations, lines 51-82",
              "Observers and Definitions, lines 82-94",
              "primary paper section 2, Definitions for relations, schemas and structures"
            ]
          },
          "unit_level": "related non-overlapping text spans, recursively composed to text structure",
          "objective": "Make the intended functional relation between spans explicit, including which span is nuclear or whether the relation is multinuclear.",
          "mandatory_parts": ["two non-overlapping spans", "a defined relation", "observer plausibility judgment", "nuclearity where the relation is nucleus-satellite"],
          "evidence_and_limitations": "RST describes text rather than the processes of creating or reading it. The relation set is open; analyses can be ambiguous or multiple; relation assignment rests on plausibility judgments about author intent. It therefore cannot serve as deterministic semantic lint.",
          "attribution_or_license": "Attribute Mann and Thompson 1988; originator site is copyright William C. Mann and Maite Taboada, all rights reserved. Cite relation names/definitions and avoid copying tables or diagrams wholesale.",
          "pdf_overlap": "Moderate with Index-Discussion units and fractal recurrence; distinct because it types relations such as Evidence, Elaboration, Condition, Contrast, and Solutionhood rather than prescribing one recurring pair.",
          "shortlist": true,
          "shortlist_reason": "Adds relation semantics between spans; its subjectivity requires human analysis rather than automatic correctness claims."
        },
        {
          "candidate_id": "gmu-cohesion",
          "responsibility": "lexical and referential cohesion",
          "source": {
            "identity": "George Mason University Writing Center, Cohesion and Coherence",
            "url": "https://writingcenter.gmu.edu/writing-resources/general-writing-practices/cohesion-and-coherence",
            "date_or_version": "page undated; footer copyright 2026",
            "selectors": [
              "Repetition of key terms/concepts/phrases, lines 33-36",
              "Synonyms, lines 37-41",
              "Sentence Patterns, lines 42-46",
              "Pronouns, lines 47-51",
              "Familiar information first, new information last, lines 52-56"
            ]
          },
          "unit_level": "sentence, paragraph, and cross-paragraph thread",
          "objective": "Maintain recognizable conceptual threads using lexical repetition, reference, patterning, and familiar-to-new ordering.",
          "mandatory_parts": [],
          "evidence_and_limitations": "The source offers optional techniques, not a closed framework or universal checklist. Synonym substitution can alter meaning; pronouns require clear referents; repetition can conflict with stylistic variety.",
          "attribution_or_license": "George Mason University states all rights reserved. Cite and paraphrase; do not reproduce its examples or guide.",
          "pdf_overlap": "Very high with the PDF's key terms, thematic strings, and old-to-new flow.",
          "shortlist": false,
          "shortlist_reason": "Useful independent precedent, but it duplicates responsibilities already explicit in the PDF."
        },
        {
          "candidate_id": "theme-rheme-progression",
          "responsibility": "theme-rheme and information progression",
          "source": {
            "identity": "Monash University Student Academic Success, Organise your ideas",
            "url": "https://www.monash.edu/student-academic-success/improve-your-academic-english/strategies-for-writing-academic-english/organise-your-ideas",
            "date_or_version": "page undated; references Halliday, Oshima and Hogue, and related academic sources",
            "selectors": [
              "Theme-rheme relation, lines 204-220",
              "thematic progress pattern, lines 220-228",
              "cohesion/coherence distinction, lines 240-243",
              "References, lines 252-265"
            ]
          },
          "unit_level": "clause and sentence sequence",
          "objective": "Control the point of departure of successive clauses through constant-theme or rheme-to-next-theme progression.",
          "mandatory_parts": ["identify theme as clause/sentence starting information", "identify rheme as the remaining added information"],
          "conditional_patterns": ["constant theme", "rheme becomes the next theme"],
          "evidence_and_limitations": "Monash calls these two common patterns, not exhaustive or mandatory laws. Its page adapts textbook examples and simplifies the wider systemic-functional and Prague School literature; application is language- and genre-sensitive.",
          "attribution_or_license": "Attribute the selected university resource and its cited lineage when concepts are retained. No permissive reuse license was established; paraphrase and create original examples.",
          "pdf_overlap": "Direct: the manifest identifies constant theme, old-to-new linking, super theme, and theme preview on PDF page 4.",
          "shortlist": false,
          "shortlist_reason": "Essential precedent and attribution evidence, but not a distinct responsibility beyond the supplied PDF."
        }
      ],
      "responsibility_matrix": [
        {"responsibility": "argument/evidence inference", "best_bound_candidate": "toulmin-argument", "distinct_from_pdf": true},
        {"responsibility": "problem framing", "best_bound_candidate": "minto-scq", "distinct_from_pdf": false},
        {"responsibility": "academic genre movement", "best_bound_candidate": "swales-cars", "distinct_from_pdf": "conditionally, through scholarship/niche/contribution binding"},
        {"responsibility": "executive hierarchy", "best_bound_candidate": "minto-pyramid", "distinct_from_pdf": "narrowly"},
        {"responsibility": "narrative temporal movement", "best_bound_candidate": "labov-narrative", "distinct_from_pdf": true},
        {"responsibility": "functional relations between spans", "best_bound_candidate": "rst", "distinct_from_pdf": true},
        {"responsibility": "lexical/referential cohesion", "best_bound_candidate": "gmu-cohesion", "distinct_from_pdf": false},
        {"responsibility": "theme-rheme information progression", "best_bound_candidate": "theme-rheme-progression", "distinct_from_pdf": false}
      ],
      "bounded_shortlist": ["toulmin-argument", "minto-pyramid", "swales-cars", "labov-narrative", "rst"],
      "shortlist_boundary": "This is a comparative evidence shortlist, not canonical selection or an integration recommendation. SCQ, cohesion, and theme-rheme remain important attribution/overlap evidence but add no non-duplicative responsibility against the manifest-bound PDF."
    }
  ],
  "validation": {
    "declared_inputs_read": [
      "ops/development/2026-08-25-whisper-writing-frameworks-research/dispatch-sheet.json",
      "ops/development/2026-08-25-whisper-writing-frameworks-research/source-manifest.json",
      "ops/development/2026-08-25-whisper-writing-frameworks-research/strategy-inventory-packet.json"
    ],
    "external_search_performed": true,
    "source_quality_check": "Each retained entry is bound to an originator, university, or primary-paper source. Search-result-only popular summaries were excluded.",
    "selector_check": "Every candidate includes a heading, line selector, paper section, or definition locator.",
    "coverage_check": {
      "argument_evidence": true,
      "problem_framing": true,
      "academic_or_genre_movement": true,
      "executive_structure": true,
      "narrative_movement": true,
      "rhetorical_relation": true,
      "cohesion": true,
      "theme_rheme_information_progression": true
    },
    "scope_check": "No repository files were written; Whisper internals were not inspected; no canonical framework or implementation mechanics were selected."
  },
  "blockers": [],
  "residue": [
    "The Writer Science overlap judgments are limited to the exact source-manifest topic inventory; this lane did not inspect or reinterpret the PDF.",
    "The public Minto page is sufficient for provenance and a narrow concept statement, but insufficient for reconstructing a full Pyramid or SCQ method.",
    "CARS varies by genre, discipline, and introduction length; synthesis must preserve its conditional scope.",
    "Labov's framework originated in oral personal-experience narratives and must not be generalized to all narrative transports without further evidence.",
    "RST analysis is observer-dependent and descriptive; relation assignment cannot be presented as deterministic semantic validation.",
    "No source in this portfolio proves reader-outcome improvement.",
    "No permissive reuse license was established for the instructional sources; public derivatives should cite, paraphrase, and use original examples."
  ]
}
```

## whisper-owner-explorer

Source: `runtime/run-001/raw-results/explorers/spawn-0003.json`
SHA-256: `2b96c1e55a7ff2956fd0f7cc8059e637219a249720f4364f5af3a7955d8a0462`

```json
{
  "task_status": "completed",
  "evidence_gate_status": "ready",
  "artifacts": {
    "owner_map": [
      {
        "responsibility": "resonance_core",
        "owner": "Whisper base contract",
        "placement_boundary": "felt meaning only: tone, voice, register, emotional residue, value signal, forbidden feels",
        "evidence": ["arcanum/spells/whisper/README.md:113-123", "arcanum/spells/whisper/schemas/text-intent-substrate.schema.yaml:65-75"]
      },
      {
        "responsibility": "relevance_core",
        "owner": "Whisper base contract",
        "placement_boundary": "audience/domain fit: target public, reader state, authority mode, assumed knowledge, objections, reward",
        "evidence": ["arcanum/spells/whisper/README.md:113-123", "arcanum/spells/whisper/schemas/text-intent-substrate.schema.yaml:76-87"]
      },
      {
        "responsibility": "trajectory_core",
        "owner": "Whisper base contract",
        "placement_boundary": "whole-text movement: anchor, transport, introduction, body parts, ending, must include/avoid",
        "evidence": ["arcanum/spells/whisper/README.md:113-123", "arcanum/spells/whisper/schemas/text-intent-substrate.schema.yaml:88-99"]
      },
      {
        "responsibility": "technique_stack",
        "owner": "Whisper candidate/selection surface",
        "placement_boundary": "reusable local moves combined with all three cores; optional field family, but required in each advanced Pareto candidate",
        "evidence": ["arcanum/spells/whisper/schemas/text-intent-substrate.schema.yaml:24-33", "arcanum/spells/whisper/tools/validate-whisper-draft.py:21-32", "arcanum/spells/whisper/development/DESIGN.md:209-213"]
      },
      {
        "responsibility": "composition_plan",
        "owner": "Whisper base planning contract",
        "placement_boundary": "ordered construction plan; body parts, sequence, anchor, examples, checklist, delivery-flow map; must bind selected candidate when Pareto present",
        "evidence": ["arcanum/spells/whisper/README.md:65-78", "arcanum/spells/whisper/schemas/text-intent-substrate.schema.yaml:129-144", "arcanum/spells/whisper/tools/validate-whisper-draft.py:354-368"]
      },
      {
        "responsibility": "transport_or_preset_profile",
        "owner": "transport_schema plus preset package",
        "placement_boundary": "transport-specific body parts, constraints, checks, publication expectations; preset should be structured contract + scaffold + bounded README",
        "evidence": ["arcanum/spells/whisper/README.md:125-137", "arcanum/spells/whisper/development/DESIGN.md:207-216", "arcanum/spells/whisper/presets/README.md:1-18"]
      },
      {
        "responsibility": "readability_dynamics",
        "owner": "optional Whisper extension",
        "placement_boundary": "density/scan/grounding plus delivery_flow; reader_movement is conditional candidate inside it, not parallel base gate",
        "evidence": ["arcanum/spells/whisper/README.md:149-170", "arcanum/spells/whisper/schemas/text-intent-substrate.schema.yaml:172-190"]
      },
      {
        "responsibility": "human_editorial_review",
        "owner": "human editorial judgment through plan/review/validation",
        "placement_boundary": "semantic repetition, sequence, specificity, earned progression, load-bearing relations, terminology timing, transformed ending, example preservation",
        "evidence": ["arcanum/spells/whisper/README.md:172-209", "arcanum/spells/whisper/schemas/examples/reader-movement.yaml:21-37"]
      },
      {
        "responsibility": "executable_lint",
        "owner": "validate-whisper-draft.py",
        "placement_boundary": "contract shape, Pareto consistency, mechanical density/pattern/duplicate checks; never semantic reader outcome",
        "evidence": ["arcanum/spells/whisper/tools/validate-whisper-draft.py:197-281", "arcanum/spells/whisper/tools/validate-whisper-draft.py:471-680"]
      },
      {
        "responsibility": "learning_residue",
        "owner": "Whisper validation/reflection",
        "placement_boundary": "observed lessons, technique results, unresolved gaps; not canonical voice/transport truth",
        "evidence": ["arcanum/spells/whisper/README.md:77-80", "arcanum/spells/whisper/README.md:101-111", "arcanum/spells/whisper/schemas/text-intent-substrate.schema.yaml:159-166"]
      },
      {
        "responsibility": "promotion",
        "owner": "inventory/glossary maintainers after Whisper evidence",
        "placement_boundary": "broad promotion requires experiment harness; base additions need repeated examples or executable support and separation from article-specific context",
        "evidence": ["arcanum/spells/whisper/README.md:30-38", "arcanum/spells/whisper/README.md:111-111", "arcanum/spells/whisper/schemas/text-intent-substrate.schema.yaml:218-225"]
      }
    ],
    "placement_classes": [
      {
        "framework_responsibility": "whole-essay status-quo/cost/point movement; narrative or executive macro-arc",
        "placement": "existing trajectory_core value plus composition pattern",
        "condition": "express as transport/audience-conditioned candidate, not universal law"
      },
      {
        "framework_responsibility": "common-ground/problem/solution or CARS/SCQA introduction movement",
        "placement": "composition pattern; transport/preset contract only when mandatory for that transport",
        "condition": "must not become a base opening gate without cross-transport evidence"
      },
      {
        "framework_responsibility": "Index-Discussion section units and point placement",
        "placement": "composition_plan/composition_parts pattern",
        "condition": "must produce an ordered part-level witness and preserve selected global candidate binding"
      },
      {
        "framework_responsibility": "fractal recurrence across essay/section/paragraph",
        "placement": "experiment-only candidate initially",
        "condition": "prove level-specific non-vacuity; do not collapse levels into one recursive slogan"
      },
      {
        "framework_responsibility": "key-term cohesion/thematic strings",
        "placement": "reusable technique plus human review check",
        "condition": "executable lint may check only configured lexical presence/duplication, never conceptual cohesion"
      },
      {
        "framework_responsibility": "paragraph information flow or theme-rheme progression",
        "placement": "reusable technique and conditional reader_movement human review; experiment-only if proposed as general policy",
        "condition": "mechanical checks cannot infer given/new information or reader comprehension"
      },
      {
        "framework_responsibility": "argument/evidence relations (e.g. Toulmin/RST-like jobs)",
        "placement": "composition pattern plus transport-specific human review check",
        "condition": "only introduce a new structured contract if a concrete witness cannot be represented by parts, validation checks, and existing cores"
      },
      {
        "framework_responsibility": "tone/voice/style supplied by a named framework",
        "placement": "existing resonance_core values",
        "condition": "reject any duplicate framework field"
      },
      {
        "framework_responsibility": "audience assumptions, objections, authority relation",
        "placement": "existing relevance_core values",
        "condition": "reject duplicate audience/profile owner"
      },
      {
        "framework_responsibility": "claimed retention, comprehension, persuasion, or model update",
        "placement": "experiment-only candidate or reject",
        "condition": "validator and editorial review cannot prove reader outcomes"
      }
    ],
    "overlap_and_gaps": {
      "overlap": "Most likely framework content already decomposes into trajectory values, technique_stack, composition plan/parts, transport contract, or readability human checks. A generic framework_profile is not presently necessary on current evidence.",
      "missing_responsibilities": [
        "No canonical machine-readable framework/profile identity, provenance, attribution, applicability/preconditions, or level-of-operation field exists.",
        "No generic registry ties named framework components to techniques/composition patterns while preserving source/version/selectors.",
        "No explicit level vocabulary distinguishes whole essay, section, paragraph, and clause responsibilities."
      ],
      "extension_preconditions": [
        "Demonstrate a concrete composition decision that existing owners cannot express without loss.",
        "Bind source identity/version/selectors and attribution/licensing duty.",
        "Name unit level, applicability, counterexample, and transport interaction.",
        "Add positive and negative fixtures across relevant transports.",
        "Keep semantic review human-owned and executable checks conservative.",
        "Keep new field optional/candidate until repeated evidence; broad promotion needs experiments."
      ]
    },
    "preset_shape_defects": [
      "presets/README.md:7-18 indexes only business_plan and live_presentation, omitting veritasium despite veritasium.md claiming Preset ID and L0 proof status.",
      "veritasium.md is prose-only, while the preset index requires a machine-readable or structured contract, scaffold/template, and bounded README.",
      "veritasium conflates transport profile (explanatory_deep_dive), frozen SCU values, technique set, composition arc, validation checklist, and claimed reader-effect evidence in one file.",
      "veritasium.md:73-78 asserts far higher model-update and retention and a failed core gate; current validator authority supports neither reader outcome nor that new base/core gate.",
      "veritasium.md:90-96 points to one proof artifact/residue but does not expose a reproducible structured fixture or evidence binding in the audited preset package. Treat as precedent/problem statement, not proven preset contract."
    ]
  },
  "validation": {
    "method": "read-only exact-selector audit of all declared inputs plus delivery-flow and reader-movement fixtures within allowed scope",
    "result": "pass",
    "checks": [
      "Owner fields reconciled across README, DESIGN, schema, validator, fixtures, and preset docs.",
      "Task completion kept separate from evidence gate.",
      "No repository bytes changed."
    ]
  },
  "blockers": [],
  "residue": [
    "Synthesis should default to decomposition into existing owners; require a non-collapsing witness before proposing framework_profile.",
    "The Veritasium preset is the strongest live warning: its useful content is separable, but its packaging and efficacy/core-gate claims exceed current structured and executable evidence.",
    "If a future framework_profile survives, it should be a provenance/applicability binding over existing values/patterns/checks, not a fourth SCU core or parallel readability/validation owner."
  ]
}
```
