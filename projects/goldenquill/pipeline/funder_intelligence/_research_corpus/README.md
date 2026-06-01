# _research_corpus/

**Pillar 2 of 4** per planning doc §3.2. Primary-source corpus that grounds every FID artifact's facts.

> **No fact in any FID artifact exists without a `corpus_ref` pointing here.** `F-FID-FACT-ORPHAN` PRE-gate fails closed on any orphan fact.

---

## Directory layout

```
_research_corpus/
├── README.md                          ← this file
└── <artifact_id>/
    ├── charter.signed.yaml            ← Pillar 1 Depth Charter (operator-Ed25519-signed)
    ├── manifest.yaml                  ← per-file provenance (URL + access_date + SHA256 + content_type)
    ├── nofos/                         ← NOFO / RFA / FOA PDFs + HTML snapshots
    │   ├── <doc_id>.pdf
    │   ├── <doc_id>.html
    │   └── <doc_id>.txt               ← extracted text for citation
    ├── rubrics/                       ← scoring sheets where FOIA-available or publicly published
    ├── awards/                        ← public award database extracts
    ├── interviews/                    ← operator + collaborator interview transcripts (Tier-2 default)
    └── guidance/                      ← federal-register interpretive notices ONLY when cited by NOFO (Tier-1)
```

---

## Five non-negotiable discipline rules

### 1. URL + access date + SHA256 hash per file

Every file in any artifact's corpus has a `manifest.yaml` entry recording where it came from and when. No exceptions.

`manifest.yaml` schema:

```yaml
artifact_id: USDA-RD-RBDG-FY26
charter_path: charter.signed.yaml
populated_at: 2026-05-XXTXX:XX:XXZ
files:
  - file_path: nofos/USDA-RD-RBDG-FY26.pdf
    source_url: https://www.rd.usda.gov/...
    access_date: 2026-05-XX
    content_type: application/pdf
    sha256: <64-hex-char hash>
    bytes_size: <int>
    pages: <int or null>
    ocr_processed: false
    classification_tier: 1
    classification_rationale: "Public NOFO from Grants.gov"
  - file_path: nofos/USDA-RD-RBDG-FY26.html
    source_url: https://www.grants.gov/...
    access_date: 2026-05-XX
    content_type: text/html
    sha256: <64-hex-char hash>
    bytes_size: <int>
    classification_tier: 1
  - file_path: interviews/2026-05-XX_rbdg_program_officer_anon.md
    source_url: null
    access_date: 2026-05-XX
    content_type: text/markdown
    sha256: <64-hex-char hash>
    classification_tier: 2
    classification_rationale: "Operator-network outreach interview; consent for anonymized internal use only"
    interview_consent_recorded: true
    interview_consent_path: interviews/2026-05-XX_consent_record.txt
```

`F-FID-CORPUS-HASH-MISMATCH` PRE-gate fails closed when on-disk SHA256 ≠ manifest entry.

### 2. ≤2-sentence verbatim quote per fact extraction

Every fact extracted into a FID artifact (`funders/<id>.yaml`, `programs/<id>.yaml`, etc.) carries:

- `corpus_ref: <artifact_id>:<filename>:<page_or_line>`
- `verbatim_quote: "..."` — **≤2 sentences**, copied bit-exact from the corpus source

This inherits the OQ-4 discipline from Wave-1+2 card content. Longer quotes get split across multiple facts each with their own ≤2-sentence quote. No paraphrasing in the quote field — paraphrasing belongs in adjacent `analysis` fields, never in `verbatim_quote`.

### 3. Primary sources only

In scope:

- NOFO / RFA / FOA PDFs and HTML
- Agency program pages (public)
- Public 990-PF tax filings
- FOIA-returned scoring sheets, rubric documents, debrief letters
- USAspending.gov / Grants.gov award database extracts
- Federal Register interpretive notices **only when cited by a NOFO and the notice materially changes applicant framing**
- Operator + collaborator interview transcripts (Tier-2 default; consent recorded)

Out of scope (do not put here):

- Secondhand summaries (blog posts, news articles, "what we heard about X")
- Case law interpretation (compliance-officer territory)
- AI-generated paraphrase or summary of any source (extracts only)
- Per-applicant data from past grant cycles (lives in `orgs/<slug>/`)

### 4. Tier classification at file granularity

Per architecture v7.0.10 + planning doc §1.5:

- **Tier 1 (commons-readable at Stage 5):** public NOFO, public 990-PF, public USAspending.gov data, FOIA-returned public rubrics.
- **Tier 2 (operator-derived + opt-in shareable):** interview transcripts, operator-derived analyses, funder-officer-relationship summaries.
- **Tier 3 (my-eyes-only forever):** personal communications, individual relationships, anything that would break trust if leaked.

Classification recorded per file in `manifest.yaml`. Mixed-tier corpus is fine; classification flows up to FID artifact field-by-field per the Depth Charter §3.

`F-FID-CLASSIFICATION-LEAK` PRE-gate fails closed on any Tier-2 or Tier-3 corpus content routed to a cloud frontier model under Frontier-Eligible posture (mirrors `F-CLASS-*` family).

### 5. Anti-fabrication and reviewer-heuristic provenance

Reviewer heuristics carry a stricter rule per `F-FID-REVIEWER-HEURISTIC-FABRICATION`:

- Every reviewer-heuristics entry MUST cite either:
  - operator-verified interview source (with consent record), OR
  - documented public reviewer-debrief source (FOIA-returned debrief letter, public conference panel transcript, published reviewer-perspective article)
- LLM-generated reviewer heuristics WITHOUT a real source = fail-closed at Pillar 3.

---

## Per-artifact corpus lifecycle

1. **Charter signed** (Pillar 1) → `<artifact_id>/charter.signed.yaml` lands.
2. **Corpus assembly** (Pillar 2 — this directory) → files fetched, hashed, classified, manifest populated.
3. **Operator spot-check** on Pillar-1-flagged-uncertainty sources before extraction begins.
4. **Pillar 3 extraction** → FID artifact draft populated with facts each pointing back here.
5. **Single-cycle L-005 audit** verifies provenance chain (every `corpus_ref` resolves; every `verbatim_quote` matches the cited file's bytes; every quote ≤2 sentences).
6. **Pillar 4 field-test** runs against the calibrated CIC × CLC pair.

---

## Phase 1 corpus envelope (weeks 2-3)

Per planning doc §9.1:

- LLM-bulk fetching across 21 exemplar-pair artifacts.
- Operator spot-check at flagged-uncertainty files.
- Manifest signing per-artifact at Pillar 2 closure.
- Estimated corpus volume: ~80-150 files total across 21 artifacts (4-10 files each).

---

## What is NOT here

- Structured FID artifacts (live in `pipeline/funder_intelligence/funders/`, `programs/`, etc.)
- Per-client KFR substrate (lives in `orgs/<slug>/vault/kfr/`)
- Scout's per-doc corpus storage (lives in `vault_shared/funder_intelligence/docs/` — different layer; the v7.0.5 system)
- Card content (lives in `pipeline/cards/`)
