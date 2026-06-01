---
name: api-research-feeds
description: >
  Connects Mycologist to academic research APIs (PubMed, OpenAlex, CrossRef, Unpaywall, PubAg).
  Discovers peer-reviewed research across 10 default categories: Mushroom Science, Regenerative Ag,
  Biochar, Soil Biology, Soilless Growing, Vermiculture, Biodynamics, Food Systems & Policy,
  Land Remediation, Arts & Biodesign. Deduplicates on DOI. Saves results to pipeline/research/.
metadata:
  clawdis:
    emoji: "🔬"
    requires:
      bins: []
      env: []
---

# API Research Feeds

## Mission

Mycologist discovers peer-reviewed research across regenerative agriculture, mycology, remediation, and biodesign. Every paper is validated via DOI. Duplicates across APIs are merged. Output is JSON saved to `pipeline/research/`.

## Default Search Categories

Query all 10 categories on each run:

1. **Mushroom Science** — keywords: `mushroom cultivation`, `fungal biology`, `mycology research`, `fungal ecology`
2. **Regenerative Agriculture** — keywords: `regenerative farming`, `soil health`, `crop rotation`, `agroecology`
3. **Biochar** — keywords: `biochar`, `carbon sequestration`, `soil amendment`, `pyrolysis`
4. **Soil Biology** — keywords: `soil microbiome`, `mycorrhizal`, `soil fauna`, `microbial community`
5. **Soilless Growing** — keywords: `hydroponics`, `aquaponics`, `vertical farming`, `substrate media`
6. **Vermiculture** — keywords: `vermicompost`, `earthworm`, `worm composting`, `Eisenia`
7. **Biodynamics** — keywords: `biodynamic farming`, `biodynamic agriculture`, `anthroposophy farming`
8. **Food Systems & Policy** — keywords: `food security`, `food sovereignty`, `agricultural policy`, `farm bill`
9. **Land Remediation** — keywords: `mycoremediation`, `phytoremediation`, `contaminated soil`, `brownfield`
10. **Arts & Biodesign** — keywords: `mycelium design`, `biomaterial`, `bioart`, `speculative design`, `living materials`

## PubMed E-Utilities API

**Step 1: Search**

**Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`

**Parameters:**
- `db=pubmed`
- `term={query}` — from default categories
- `retmode=json`
- `retmax=25` — retrieve up to 25 results per search
- `sort=relevance`

**Response:** JSON with array of PubMed IDs (`idlist`)

**Rate Limit:** 3 requests per second. Add `&api_key=demo` if no NCBI API key is available (limited but functional).

**Step 2: Fetch Full Records**

**Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`

**Parameters:**
- `db=pubmed`
- `id={comma_separated_ids}` — from Step 1 results
- `rettype=abstract`
- `retmode=xml`

**Response:** XML. Parse each `<PubmedArticle>`:
- `<MedlineCitation><PMID>` — PubMed ID
- `<Article><ArticleTitle>` — Title
- `<Article><Journal><Title>` — Journal name
- `<Article><Journal><PubDate><Year>` — Publication year
- `<Article><ELocationID IdType="doi">` — DOI (if available)
- `<Article><Abstract><AbstractText>` — Abstract text (may be split across multiple `<AbstractText>` elements)
- `<Author><LastName>`, `<Author><Initials>` — Authors (repeating)

**Validation:**
- If DOI is present, store it for deduplication
- If DOI is absent, generate placeholder: `pubmed-{PMID}`
- Trim abstract to first 300 characters

## OpenAlex API

**Endpoint:** `https://api.openalex.org/works`

**Parameters:**
- `search={query}` — from default categories
- `filter=from_publication_date:2025-01-01` — published in 2025 or later
- `sort=publication_date:desc` — newest first
- `per_page=25`
- `email=josh@goldenquill.com` — Polite pool (add this to request header)

**Response:** JSON array under `results`. Parse each work:
- `id` — OpenAlex ID (e.g., `https://openalex.org/W2963961516`)
- `title` — Work title
- `publication_date` — ISO 8601 date
- `doi` — Full DOI string (e.g., `https://doi.org/10.1234/example`)
- `abstract_inverted_index` — Inverted index of abstract words (reconstruct to string)
- `cited_by_count` — Citation count
- `authorships` — Array with `author.display_name`
- `primary_location.source.display_name` — Journal/venue name

**Rate Limit:** Polite pool; no explicit limit. 1 request per second (conservative).

**Deduplication:** Extract DOI from `doi` field. Match against existing records by DOI.

## CrossRef API

**Endpoint:** `https://api.crossref.org/works`

**Parameters:**
- `query={query}` — from default categories
- `filter=from-pub-date:2025-01-01` — published in 2025 or later
- `sort=published` — sort by publication date
- `order=desc` — newest first
- `rows=20`

**Response:** JSON with `message.items` array. Parse each item:
- `DOI` — Canonical DOI (may be uppercase)
- `title` — Array; use first element
- `URL` — Full record URL
- `published.date-parts` — `[[year, month, day]]`
- `container-title` — Journal name
- `abstract` — Abstract text (may be null or HTML)
- `author` — Array with `given`, `family` names
- `is-referenced-by-count` — Citation count

**Rate Limit:** None. 1 request per second (conservative).

**Deduplication:** Normalize DOI to lowercase. Match against existing records.

## Unpaywall API

**Endpoint:** `https://api.unpaywall.org/v2/{doi}`

**Parameters:**
- `{doi}` — Full DOI to check (replace slashes with forward slashes)
- `email=josh@goldenquill.com` — Required for API access

**Purpose:** Find open access PDF URLs for papers discovered via PubMed, OpenAlex, CrossRef.

**Response:** JSON. Parse:
- `doi` — Input DOI
- `title` — Paper title
- `oa_status` — `gold`, `hybrid`, `green`, `closed`
- `oa_location` — Object with `url` (direct PDF link) if available
- `is_oa` — Boolean

**Rate Limit:** 1 request per second per email.

**Logic:**
- Call Unpaywall AFTER discovering a paper from another API
- If `is_oa` is true and `oa_location.url` exists, store URL in output
- If no open access, omit `open_access_url` field (set to null)

## PubAg (USDA) API

**Endpoint:** `https://pubag.nal.usda.gov/pubag/rest/search/`

**Parameters:**
- `query={query}` — from default categories
- `page=1`
- `per_page=25`

**Response:** JSON with `results` array. Parse each record:
- `id` — PubAg record ID
- `title` — Paper title
- `authors` — Array of author names
- `journal` — Journal name
- `publicationYear` — Year (integer)
- `doi` — DOI if available
- `abstract` — Abstract text

**Rate Limit:** No published limit. 1 request per second (conservative).

## Semantic Scholar API

**Endpoint:** `https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=25&fields=title,authors,year,abstract,externalIds,openAccessPdf,citationCount`

**Parameters:**
- `query={query}` — from default categories
- `limit=25` — retrieve up to 25 results
- `fields` — request only necessary fields for efficiency

**Response:** JSON array under `data`. Parse each paper:
- `paperId` — Semantic Scholar paper ID
- `title` — Paper title
- `authors` — Array with `name` field
- `year` — Publication year (integer)
- `abstract` — Abstract text
- `externalIds` — Object with `DOI`, `PubMedId`, `ArxivId`
- `citationCount` — Citation count
- `openAccessPdf` — Object with `url` if open access available

**Rate Limit:** 100 requests per minute without API key.

**Use for:** Citation graph traversal, finding seminal papers, impact scoring. Especially valuable for tracking which papers cite foundational mycology/biochar/soil studies.

**Deduplication:** Extract DOI from `externalIds.DOI`. Match against existing records.

## CORE API

**Endpoint:** `https://api.core.ac.uk/v3/search/works?q={query}&limit=25`

**Method:** GET

**Headers:**
- `Authorization: Bearer {CORE_API_KEY}` — Register for free key at https://core.ac.uk

**Parameters:**
- `q={query}` — from default categories
- `limit=25` — retrieve up to 25 results

**Response:** JSON with `results` array. Parse each work:
- `id` — CORE work ID
- `title` — Paper title
- `authors` — Array with author names
- `publishedDate` — ISO 8601 date
- `abstract` — Abstract text
- `doi` — DOI if available
- `downloadUrl` — Direct PDF link if available

**Rate Limit:** No published limit. 1 request per second (conservative).

**Use for:** Open access papers that PubMed and OpenAlex miss. Especially theses, dissertations, and conference proceedings. Key strength: European agricultural research and gray literature.

## iNaturalist API

**Endpoint:** `https://api.inaturalist.org/v1/observations?taxon_name={species}&place_id=1&per_page=25&order=desc&order_by=created_at`

**Method:** GET

**Parameters:**
- `taxon_name={species}` — scientific name (e.g., "Pleurotus ostreatus")
- `iconic_taxa=Fungi` — filter for fungi only
- `per_page=25` — retrieve up to 25 results
- `order_by=created_at` — newest observations first

**Response:** JSON with `results` array. Parse each observation:
- `id` — Observation ID
- `time_observed_at` — ISO 8601 datetime
- `place_guess` — Location text
- `latitude`, `longitude` — Coordinates
- `species_guess` — Identified species name
- `photos` — Array with photo URLs
- `user.name` — Observer name

**Rate Limit:** Respectful use, no hard limit published.

**Use for:** Citizen science fungal observations and species distribution data. Especially useful for grant narratives: "X fungal species has been documented at Y locations in {state/region}".

## GBIF API

**Endpoint:** `https://api.gbif.org/v1/occurrence/search?scientificName={species}&country=US&limit=25`

**Alternative: Species Search** — `https://api.gbif.org/v1/species/search?q={query}&rank=SPECIES&limit=10`

**Method:** GET

**Parameters:**
- `scientificName={species}` — Full species name
- `country=US` — Filter for US records
- `limit=25` — retrieve up to 25 results

**Response:** JSON with `results` array. Parse each occurrence:
- `gbifID` — GBIF record ID
- `scientificName` — Species name
- `eventDate` — ISO 8601 date
- `decimalLatitude`, `decimalLongitude` — Coordinates
- `institutionCode` — Museum/herbarium code
- `catalogNumber` — Specimen reference number

**Rate Limit:** No published limit. 1 request per second (conservative).

**Use for:** Global biodiversity occurrence data backed by museum and herbarium specimen records. Key strength: Historical distribution data going back decades, providing proof of species presence at specific locations over time.

## MycoBank API

**Endpoint:** `https://www.mycobank.org/Services/Generic/SearchService.svc/rest/xml?layout=14682616000000161&filter={species}`

**Method:** GET

**Parameters:**
- `filter={species}` — Scientific name (e.g., "Pleurotus ostreatus")

**Response:** XML with fungal nomenclature records. Parse:
- `Name` — Current accepted name
- `Synonyms` — Previous names
- `TaxonomicStatus` — accepted, synonym, doubtful, etc.
- `YearOfName` — Publication year
- `Authors` — Authority citation

**Rate Limit:** No published limit. 1 request per second (conservative).

**Use for:** Authoritative fungal nomenclature. Verify species names, get taxonomic classification, find accepted names for synonyms. Critical for any grant that names specific fungal species — wrong nomenclature causes credibility damage.

## MushroomObserver API

**Endpoint:** `https://mushroomobserver.org/api2/observations?name={species}&format=json&detail=high`

**Method:** GET

**Parameters:**
- `name={species}` — Species name or partial name
- `detail=high` — Return full observation details
- `format=json` — JSON response format

**Response:** JSON with `observations` array. Parse each observation:
- `id` — Observation ID
- `name` — Identified species name
- `location` — Location text
- `latitude`, `longitude` — Coordinates
- `when` — ISO 8601 date
- `images` — Array with image URLs
- `notes` — Observer notes

**Rate Limit:** No published limit. 1 request per second (conservative).

**Use for:** Community mushroom identification data, location records, and seasonal patterns. Complements iNaturalist (different user base, more mycology-focused community).

## Index Fungorum

**Endpoint:** `http://www.indexfungorum.org/ixfwebservice/fungus.asmx/NameSearch?SearchText={species}&AnywhereInText=true&MaxNumber=25`

**Method:** GET

**Parameters:**
- `SearchText={species}` — Scientific name
- `AnywhereInText=true` — Search partial matches
- `MaxNumber=25` — Return up to 25 results

**Response:** XML with fungal name records. Parse:
- `NameIndex` — Name record ID
- `Name` — Current name
- `Authors` — Author citation
- `YearOfPub` — Publication year
- `Comments` — Taxonomic notes

**Rate Limit:** No published limit. 1 request per second (conservative).

**Use for:** Cross-reference with MycoBank for nomenclatural verification. Provides independent validation of fungal species names and taxonomic authority.

## Europe PMC API

**Endpoint:** `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={query}&format=json&pageSize=25&sort=DATE desc`

**Method:** GET

**Parameters:**
- `query={query}` — from default categories
- `format=json` — JSON response
- `pageSize=25` — retrieve up to 25 results
- `sort=DATE desc` — newest first

**Response:** JSON with `hitCount` and `resultList` array. Parse each result:
- `id` — Europe PMC ID
- `title` — Article title
- `authorString` — Authors (semicolon-separated)
- `pubYear` — Publication year
- `abstractText` — Abstract
- `doi` — DOI if available
- `isOpenAccess` — Boolean

**Rate Limit:** No published limit. 1 request per second (conservative).

**Use for:** European biomedical and life sciences literature. Fills gaps in PubMed coverage, especially for EU-funded mushroom, soil, and remediation research.

## Output Format: JSON

Save all discoveries to `pipeline/research/{category}_{timestamp}.json`:

```json
{
  "category": "Mushroom Science|Regenerative Ag|Biochar|...",
  "query_terms": ["mushroom cultivation", "fungal biology"],
  "papers": [
    {
      "doi": "https://doi.org/10.1234/example",
      "title": "Full Paper Title",
      "authors": [
        {"name": "First Author", "first": "F", "last": "Author"},
        {"name": "Second Author", "first": "S", "last": "Author"}
      ],
      "journal": "Journal Name",
      "publication_date": "2026-03-15",
      "abstract_snippet": "First 300 characters of abstract...",
      "open_access_url": "https://example.com/paper.pdf",
      "citation_count": 42,
      "relevance_category": "Mushroom Science",
      "source_apis": ["pubmed", "openalex"],
      "fetched_at": "2026-04-12T14:32:18Z"
    }
  ],
  "deduplication_notes": {
    "duplicate_dois_merged": 3,
    "unique_papers": 45
  },
  "validation_passed": true
}
```

## Deduplication Logic

1. **Within one API response:** Check title similarity (>90% match) and DOI. Keep first occurrence, log duplicates.
2. **Across APIs:** Match on DOI first (canonical source of truth). If same paper found in multiple APIs:
   - Merge metadata: prefer OpenAlex title if longer/clearer
   - Keep all source_apis listed
   - Use highest citation_count from any source
   - Prefer open_access_url from Unpaywall if available
   - Remove duplicate record, keep one merged record

3. **Against historical records:** Check `pipeline/research/` for papers already fetched. If DOI exists in prior runs, skip (unless explicitly refreshing).

## Validation Rules (Pre-Output)

1. **DOI Validation:** All DOIs must start with `https://doi.org/` or be convertible. Normalize to full URL.
2. **Date Validation:** publication_date must be ISO 8601 and before today().
3. **Abstract Check:** Trim to 300 characters. If >1000 characters, likely HTML-encoded—strip tags.
4. **Citation Count:** Integer, non-negative. If null, set to 0.
5. **Author Count:** If >50 authors, likely a consortium paper—log warning, keep all names.

## Operating Law Compliance

- **Rule 1 (RFA is Truth):** This skill discovers research context only. Scribe synthesizes findings into grant narratives.
- **Rule 2 (Test Your Own Work):** All DOIs are validated. Deduplication is logged. Output includes validation_passed flag.
- **Rule 4 (Admin-Risk Scanning):** Output does not interpret findings. Logician reviews for policy/sectoral flags.

## Error Handling

If an API is unreachable:
- Log error with timestamp
- Continue with remaining APIs
- Save partial results to `pipeline/research/`
- Return non-zero exit if 3+ APIs failed

## Scheduling & Triggers

- Run on demand by Mycologist operator
- Optionally scheduled: 2x per week to catch new publications
- After each run, validate output before handing to institutional memory
