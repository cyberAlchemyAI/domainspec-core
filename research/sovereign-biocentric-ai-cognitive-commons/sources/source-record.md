# Source Record

Checked: `2026-08-03`

Status: `pass-with-boundaries`

## Primary Corpus

- Format: Microsoft Word DOCX.
- Supplied path: `/mnt/c/Users/vlad_/OneDrive/Documentos/Artificial intelligence frameworks and romantic literature both frameworks  shape human sense and beliefs by targeting logic and emotion.docx`
- Size: `150366` bytes.
- SHA-256: `3153a4ced4a268294e9695e75618448f75737ac101a06534e31544ad8b7e8c54`.
- Package content: `856` Word paragraph elements, `2` table elements, one
  embedded PNG, no substantive footnotes or endnotes.
- Link relationships: `102` external relationships and `71` unique targets.
- Word application metadata: `13318` words, `178` application paragraphs.
- Core metadata creator and last modifier: `Estela Claudia Bilbao Love`.
- Core metadata created: `2026-07-28T21:16:00Z`.
- Core metadata modified: `2026-07-31T06:22:00Z`.
- Revision: `3`.

The hash identifies the exact checked bytes. Metadata records what the DOCX
declares; it does not independently prove sole authorship, originality, or legal
ownership.

## Corpus Classification

The document is a captured human-AI dialogue followed by generated summaries
and suggested questions. It is not a conventional research paper: it has no
stable bibliography, the numeric references restart across responses, links
often point only to domains, prose and example code are duplicated, and source
quality ranges from standards and peer-reviewed work to social media and vendor
pages.

## Voice Rule

| Voice | Source treatment | Truth treatment |
| --- | --- | --- |
| Human prompt | `primary-source` for the creator's questions, values, and intended direction | Does not prove external facts |
| Assistant response | `primary-source` only for what the captured dialogue says | Unverified until a related source supports it |
| Generated closing summary | `primary-source` for corpus structure | Not independent corroboration |
| External link | Candidate `related-source` | Must be opened, identified, and matched to the exact claim |
| Tower synthesis | `local-inference` or `operator-reading` | Must cite the corpus and/or a checked related source |

## Reproducibility Commands

```bash
sha256sum '<supplied-docx-path>'
unzip -l '<supplied-docx-path>'
unzip -p '<supplied-docx-path>' docProps/core.xml
unzip -p '<supplied-docx-path>' docProps/app.xml
unzip -p '<supplied-docx-path>' word/document.xml
unzip -p '<supplied-docx-path>' word/_rels/document.xml.rels
```

These commands inspect the OOXML package. They do not validate any claim inside
the document.

## Source Boundary

- The DOCX remains external to the repository; this tower records its digest
  and does not duplicate the full text.
- The embedded image is part of the primary corpus, not independent evidence.
- Location and biometric examples inside the corpus are design examples, not
  evidence that those data should be permanently recorded.
- High-risk claims are adjudicated in
  [`../tracks/paper-claim-ledger.md`](../tracks/paper-claim-ledger.md).

