# ScienceDirect corpus findings

## Scope and evidence boundary

This is a read-only synthesis of the local ScienceDirect *Computers and Education: Artificial Intelligence* snapshot: exactly 100 readable, unencrypted PDFs totaling 1,524 pages. Explorer partitions cover PDFs 001–034 (A), 035–067 (B), and 068–100 (C), reconciling as 34 + 33 + 33 = 100. The evidence surface is local PDF text and explorer-reported selectors; DOI, HTML, independent full-text, pooled-effect, causal, product, deployment, and human-acceptance verification were not performed. [dispatch-sheet.json#context; synthesis-revised.json#validation.coverage; synthesis-revised.json#validation.evidence_ceiling]

The manifest is a coverage map, not a quality or readiness claim. It records 100 total records, 99 trusted substantive records after governance exclusion, two corrigenda, and one retraction notice. [synthesis-revised.json#synthesis.manifest.counts]

## Corpus manifest and article-type governance

- The two corrigenda are retained as non-outcome records. The lab-assistant corrigendum repairs source-code URLs and identifies Mahidol University IRB/protocol metadata (PDF p1, Corrections 1–2); the *Face value* corrigendum repairs a Zenodo DOI and citation fields (PDF p1, Correction 1). They preserve provenance and ethics lineage; they do not add experiment outcomes. [synthesis-revised.json#synthesis.manifest.special_records.corrigendum_lineage; reviewer-precedent.json#validation.sample[0:2]]
- The retraction notice is retained for governance traceability and excluded from trusted substantive evidence. Its notice attributes retraction to consent/anonymization noncompliance and does not, by itself, establish that the underlying findings are scientifically false (PDF p1, Retraction/ethics statement). [synthesis-revised.json#synthesis.manifest.special_records[1]; reviewer-precedent.json#validation.sample[2]; reviewer-non-vacuity.json#validation.coverage_reconciliation]
- Reviews, scoping/umbrella reviews, frameworks, conceptual papers, primary experiments, surveys, qualitative studies, and computational benchmarks remain visibly distinct. Review/framework evidence maps constructs and gaps; primary studies provide bounded local signals; computational records establish task metrics under stated conditions only. [synthesis-revised.json#synthesis.method_map; reviewer-precedent.json#blockers[3]]

## Source-bound thematic synthesis

1. **Layered AI literacy, scaffolding, and reflective/ethical use.** Prompt-engineering and AI-literacy reviews/frameworks describe layered competencies, scaffolding, verification, and reflection; a bounded cross-sectional/educator signal is compatible with that framing. This is precedent and bridge work, not a corpus novelty claim. [explorer-a.json#papers[file=A-scoping-literature-review-of-prompt-engineerin_2026_Computers-and-Educatio.pdf].selectors=["PDF p1, Abstract","PDF p4, Search/eligibility"]; explorer-c.json#rows[id=90].selectors="pp.1-2 Abstract; pp.4-10 Synthesis"; explorer-b.json#articles[n=43].selectors=["Abstract p1","Quantitative/qualitative results pp7-10"]]
2. **Performance versus durable learning.** Controlled/comparative records report local gains in scores, code correctness, confidence, or immediate task performance, while limitations leave conceptual learning, delayed transfer, or higher-order reasoning unresolved. Performance must not be treated as synonymous with learning. [explorer-b.json#articles[n=35].selectors=["Results pp8-10","Conclusion and discussion pp11-12"]; explorer-b.json#articles[n=65].selectors=["Abstract pp1-2","RCT results pp10-15","Conclusion pp17-18"]; explorer-a.json#papers[file=A-systematic-review-of-the-impact-of-GenAI-on-learni_2026_Computers-and-Educ.pdf].selectors=["PDF p1, Abstract","PDF p4-5, Review method"]]
3. **Guidance, context, and oversight.** Guided versus unrestricted chatbot use, contextual prompting, hybrid feedback, and teacher-specific explanations provide promising local design signals; answer-giving, prompt injection, generic feedback, and untested transfer remain risks. [explorer-b.json#articles[n=36].selectors=["Results pp6-8","Conclusion p8"]; explorer-b.json#articles[n=48].selectors=["Abstract p1","Results pp7-10","Discussion/Conclusion pp11-12"]; explorer-c.json#rows[id=98].selectors="pp.1-2 Abstract; pp.4-12 Reliability/Accuracy"]
4. **Trust, credibility, identity, and governance.** Credibility, avatar identity, trust, privacy, consent, and governance constraints shape uptake or acceptance; perceived capability or agreement is not epistemic accuracy or equitable impact. [explorer-b.json#articles[n=40].selectors=["Abstract p1","Studies 1-2 pp6-13"]; explorer-b.json#articles[n=44].selectors=["Abstract p1","Validation pp11-16"]; explorer-c.json#rows[id=81].selectors="p.1 Retraction/ethics statement"]
5. **Equity and representation.** Disability, gender, race/ethnicity, socioeconomic status, language, and culture recur as moderators or bias sources. Average performance or balanced representation does not establish distributional fairness. [explorer-a.json#papers[file=Beyond-binary-outcomes--Evaluating-and-mitigatin_2026_Computers-and-Educatio.pdf].selectors=["PDF p1, Abstract"]; explorer-a.json#papers[file=Bias-and-representation-in-AI-generated-text-t_2026_Computers-and-Education-.pdf].selectors=["PDF p1, Abstract"]; explorer-b.json#articles[n=38].selectors=["User study pp9-12","Limitations and Conclusions pp13-14"]]
6. **Automated evaluation as aid, not high-stakes authority.** Benchmarks and validation studies show constrained agreement or efficiency, but stochastic variability, inferential weakness, drift, and disagreement limit autonomous or high-stakes use. [explorer-a.json#papers[file=A-framework-for-evaluation-of-large-language-model_2026_Computers-and-Educat.pdf].selectors=["PDF p1, Abstract","PDF p3, Methods"]; explorer-c.json#rows[id=98].selectors="pp.1-2 Abstract; pp.4-12 Reliability/Accuracy"; explorer-c.json#rows[id=72].selectors="pp.1-2 Abstract; pp.5-16 Experiment/Results"]

## Methods and populations

Observed method families include experiments/RCTs and field studies; surveys, SEM and instrument validation; systematic/scoping/umbrella/bibliometric/meta-analytic reviews; design-based and conceptual frameworks; NLP/ML benchmarks and reliability validation; and qualitative, participatory, Delphi, and mixed methods. Their outcomes and comparators are heterogeneous, so no pooled effect or common causal estimate is supported. [synthesis-revised.json#synthesis.method_map]

Settings span higher education, programming/STEM, L2/EFL, K–12/secondary and early childhood, teachers and preservice educators, families, deaf or hard-of-hearing learners, institutions, national corpora, benchmarks, and synthetic datasets. Samples range from 10 families and 16 DHH participants to large review or submission corpora; many are single-site, convenience, cross-sectional, short-course, or self-report. They are not representative of Living Archive users. [synthesis-revised.json#synthesis.population_map; explorer-a.json#papers[file=Conversational-AI-in-children-s-home-literacy-lear_2026_Computers-and-Educat.pdf].selectors=["PDF p1, Abstract"]; explorer-b.json#articles[n=38].selectors=["Highlights/Abstract pp1-2","User study pp9-12"]]

## Contradiction and evidence-quality map

| Tension | Local positive signal | Counter-signal / ceiling | Evidence |
|---|---|---|---|
| Task performance vs durable learning | Better scores, correctness, or immediate performance | Similar learning, reduced higher-order reasoning, or unmeasured transfer | B35, B61, B65 selectors in synthesis contradiction map |
| Automation efficiency vs reliability/oversight | Constrained alignment or workload reduction | Variability, drift, exploits, disagreement; human review required | B55, C98, B36 selectors in synthesis contradiction map |
| Adoption/usefulness vs critical/equitable use | Trust, self-efficacy, usefulness, reliance predict uptake | Privacy, fairness, anxiety, consent, and governance risks; uptake is not benefit | B41, C68, C81 selectors in synthesis contradiction map |

Within scope, stronger evidence is controlled or repeated-measures work with explicit samples and outcomes, but it remains local and often short-term. Quasi-experiments, surveys, mixed methods, and case studies support associations or feasibility. Reviews/frameworks support construct and gap mapping, not intervention efficacy. Benchmarks and automated evaluation support task metrics, not human learning or deployment safety. Corrigenda are provenance-only; the retraction is governance exclusion. [synthesis-revised.json#synthesis.evidence_quality_map; reviewer-non-vacuity.json#residue]

Cross-cutting limits are single-site/convenience samples, self-report and intention outcomes, short interventions without delayed transfer, model/version/prompt dependence, heterogeneous definitions, and no independent DOI/full-text verification. [synthesis-revised.json#synthesis.evidence_quality_map.cross-cutting_caveats]

## Verdict matrix

| Question | Verdict | Basis and ceiling |
|---|---|---|
| Was the 100-PDF snapshot covered? | **Observed: yes** | 34+33+33 manifest reconciliation; coverage is not quality/readiness. [synthesis-revised.json#validation.coverage] |
| Are article types and governance records separated? | **Observed: yes, with residue** | Two corrigenda remain provenance records; C81 remains traceability-only and is excluded from trusted substantive evidence. [synthesis-revised.json#synthesis.manifest] |
| Is there a coherent source-bound thematic map? | **Observed: yes** | Six themes have concrete selectors and explicit review/primary distinctions. [synthesis-revised.json#synthesis.theme_map] |
| Is a pooled causal or general educational effect established? | **Blocked/open: no** | Heterogeneous designs, populations, outcomes, and follow-up. [synthesis-revised.json#blockers] |
| Is there evidence for a Living Archive Memory Agent? | **Blocked: no direct test** | No paper tests its behavior, retention safety, usefulness, human acceptance, deployment, or production operation. [synthesis-revised.json#synthesis.living_archive_memory_agent_implications.explicit_non_claims] |

## Living Archive Memory Agent: bounded design hypotheses only

These are hypotheses for a separately authorized design/evidence work-pack, not requirements, implementation findings, or validation:

- A source-bound memory layer could retain article provenance, exact selector pointers, article type, population, method, limitations, and confidence rather than undifferentiated answers. [explorer-a.json#papers[file=A-systematic-review-of-the-impact-of-GenAI-on-learni_2026_Computers-and-Educ.pdf].selectors=["PDF p1, Abstract","PDF p4-5, Review method"]; explorer-b.json#articles[n=62].selectors=["Highlights/Abstract pp1-2","Synthesis pp7-12","Conclusion pp13-14"]; explorer-c.json#rows[id=81].selectors="p.1 Retraction/ethics statement"]
- Recall could expose evidence and counter-evidence together, preserving contradiction labels such as performance-versus-learning and automation-versus-oversight. [explorer-b.json#articles[n=35].selectors=["Results pp8-10","Conclusion and discussion pp11-12"]; explorer-b.json#articles[n=65].selectors=["Abstract pp1-2","RCT results pp10-15","Conclusion pp17-18"]; explorer-c.json#rows[id=98].selectors="pp.1-2 Abstract; pp.4-12 Reliability/Accuracy"]
- Adaptive or agentic behavior could be gated by uncertainty, human review, consent/privacy, and population/fairness checks rather than inferred from benchmark scores or adoption studies. [explorer-b.json#articles[n=44].selectors=["Abstract p1","Validation pp11-16"]; explorer-b.json#articles[n=40].selectors=["Abstract p1","Studies 1-2 pp6-13"]; explorer-c.json#rows[id=81].selectors="p.1 Retraction/ethics statement"]

No corpus evidence proves that a Memory Agent exists, works, is safe, benefits people, is human-accepted, or is ready for implementation, deployment, publication, or production. Any next step requires separate product-specific fixtures, runtime tests, privacy/consent review, and owner acceptance. [synthesis-revised.json#synthesis.living_archive_memory_agent_implications.explicit_non_claims; reviewer-non-vacuity.json#handoff_note]

## Residue and handoff

The writer artifact is source-bound and conditionally accepted for adjudication. Local PDF selectors may differ from HTML pagination; the reviewer-required repair is to keep the lab-assistant experiment selector to PDF pp.6–8 and cite its p.11 corrigendum only as metadata. Independent source verification and any product-context evidence remain open. [reviewer-non-vacuity.json#blockers[0]; synthesis-revised.json#residue]
