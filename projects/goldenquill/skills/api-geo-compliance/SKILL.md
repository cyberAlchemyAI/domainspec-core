---
name: api-geo-compliance
description: >
  Location intelligence and compliance verification for grant eligibility. Queries US Census,
  EPA EJScreen, USDA Food Access, ARC, and RUCA databases. Appends geo-compliance fields to
  PROJECT_CONTEXT.md. Auto-populates on address entry.
metadata:
  clawdis:
    emoji: "🗺️"
    requires:
      bins: []
      env: []
---

# API Geo Compliance

## Mission

Scout validates applicant location against federal grant eligibility geographies. Every org's address is geocoded and cross-checked against ARC, rural/urban status, food access, and environmental justice criteria. Results append directly to PROJECT_CONTEXT.md.

## Data Model: Geo Compliance Fields

**Append to PROJECT_CONTEXT.md `[organization]` section:**

```markdown
## Geospatial Compliance

census_tract: "1234.56"
county_fips: "42001"  # Pennsylvania = 42, Adams County = 001
state_fips: "42"
ej_score: 65  # 0–100, higher = greater EJ concern
food_desert_status: "low_food_access"  # low_food_access | food_apartheid | adequate_access
arc_status: "distressed"  # distressed | at-risk | competitive | non-appalachian
ruca_code: "1.0"  # 1.0 = metropolitan core, 2.0 = metro high commute, 10.5 = rural remote
rural_urban_code: "1"  # 1 = large metro, 2 = metro, 3 = micro, 4 = non-core
```

**Add explanations in comment lines** so Josh understands eligibility impact for each grant.

## US Census Geocoder API

**Endpoint:** `https://geocoding.geo.census.gov/geocoder/geographies/address`

**Method:** GET

**Parameters:**
- `street` — Street address (e.g., "1600 Pennsylvania Avenue")
- `city` — City
- `state` — Two-letter state code (PA, NY, CA, etc.)
- `benchmark=Public_AR_Current` — Current reference benchmark
- `vintage=Current_Current` — Current vintage
- `format=json`

**Example Request:**
```
https://geocoding.geo.census.gov/geocoder/geographies/address?street=123%20Main%20St&city=Philadelphia&state=PA&benchmark=Public_AR_Current&vintage=Current_Current&format=json
```

**Response:** JSON

```json
{
  "result": {
    "input": { ... },
    "addressMatches": [
      {
        "matchedAddress": "123 Main Street, Philadelphia, Pennsylvania, 42101 USA",
        "coordinates": {
          "x": -75.1234,
          "y": 39.5678
        },
        "tigerLine": { ... },
        "geographies": {
          "Counties": [
            {
              "COUNTY": "Philadelphia",
              "STATEFP": "42",
              "COUNTYFP": "101"
            }
          ],
          "Census Tracts": [
            {
              "TRACTCE": "1234.56",
              "STATEFP": "42",
              "COUNTYFP": "101"
            }
          ],
          "States": [
            {
              "STATE": "PA",
              "STATEFP": "42"
            }
          ]
        }
      }
    ]
  }
}
```

**Parse:**
- `geographies.Counties[0].COUNTYFP` → `county_fips` (e.g., "001")
- `geographies.Counties[0].STATEFP` → `state_fips` (e.g., "42")
- `geographies["Census Tracts"][0].TRACTCE` → `census_tract` (e.g., "1234.56")
- `coordinates.x, coordinates.y` → store as `lat`, `lon` for downstream lookups

**Rate Limit:** No published limit. 1 request per second (conservative).

## EPA EJScreen API

**Endpoint:** `https://ejscreen.epa.gov/mapper/ejscreenRESTbroker.aspx`

**Method:** GET

**Parameters:**
- `namestr` — Location name or address
- `geometry` — Optional: geometry object with coordinates (if using Census geocoded lat/lon)
- `distance` — Search radius in meters (9035 = ~5.6 miles)
- `unit` — `9035` (feet) or meters
- `yfirstagg` — Start year for environmental data (use current year)
- `ylastaggg` — End year (use current year)

**Alternative: Direct Coordinates**
```
https://ejscreen.epa.gov/mapper/ejscreenRESTbroker.aspx?geometry={"type":"Point","coordinates":[-75.1234,39.5678]}&distance=9035
```

**Response:** JSON with environmental justice indicators

```json
{
  "properties": {
    "EJIndex": 65,
    "P_EJIndex": 75,
    "PM25": 12.5,
    "OZONE": 75,
    "DSLPM": 567,
    "RMP": 0,
    "MINORPCT": 45,
    "LOWINCPCT": 38,
    "LINGISOPCT": 22,
    ...
  }
}
```

**Parse:**
- `properties.EJIndex` → `ej_score` (0–100, higher = greater EJ concern)
- If EJIndex > 70: qualify for Justice40 / Environmental Justice grants
- Store full properties object for downstream RFA analysis

**Rate Limit:** No published limit. 1 request per 2 seconds (conservative).

## USDA Food Access Research Atlas

**Endpoint:** `https://www.ers.usda.gov/webdocs/DataFiles/{dataset_id}/` (static data files)

**Alternative: Proxy via Census data**

Use Census tract and cross-reference USDA food access tier:
1. Obtain Census tract from Census Geocoder
2. Query local USDA office food access database (manual lookup for v0.1)
3. Classify as: `low_food_access`, `food_apartheid`, or `adequate_access`

**Food Access Categories:**
- **Low Food Access:** Tract is >1 mile (urban) or >10 miles (rural) from nearest supermarket
- **Food Apartheid:** Low food access + Low income + Low car access
- **Adequate Access:** <1 mile (urban) or <10 miles (rural)

**Data Source for v0.1:**
- Download USDA Food Access Atlas data: `https://www.ers.usda.gov/webdocs/DataFiles/48714/FoodAccessResearchAtlas_12.17.19.xlsx`
- Load into local database (on first run)
- Lookup by Census tract FIPS code

**Parse:**
- If `LowAccessTracts2010` = 1 and `PovertyRate` > 20: `food_apartheid`
- If `LowAccessTracts2010` = 1: `low_food_access`
- Else: `adequate_access`

## ARC County Status Lookup

**Endpoint:** Manual lookup via ARC website or local CSV

**Data Source:** ARC maintains list of distressed counties
- Download: `https://www.arc.gov/research/ResearchTopicDetails.asp?TOPICID=42` (manual export)
- CSV format: county_fips, state, designation (distressed|at-risk|competitive|non-appalachian)

**For v0.1:**
- Maintain local CSV file: `pipeline/data/arc_county_designations.csv`
- Lookup by `state_fips + county_fips`

**Designations:**
- **Distressed:** Economic indicators in bottom quintile (highest eligibility for ARC grants)
- **At-Risk:** Indicators trending downward
- **Competitive:** Median performance
- **Non-Appalachian:** Outside ARC's 13-state region

**Parse:**
- Match `county_fips` to ARC CSV
- If not found, set to `non-appalachian`

## USDA RUCA Codes

**Endpoint:** Census RUCA database (static)

**Data Source:** USDA NASS
- Download: `https://www.ers.usda.gov/webdocs/DataFiles/53251/RUCA2010_Rural_Urban_Commuting_Area_Codes.csv`
- Store locally: `pipeline/data/ruca_codes.csv`
- Columns: Census tract code, RUCA code, description

**RUCA Code Scale:**
- **1.0** — Metropolitan core (urban, high density, commuting to metro)
- **2.0** — Metropolitan high commute (commutes to metro, <10% non-commuting workers)
- **3.0** — Metropolitan low commute (commutes to metro, ≥10% non-commuting)
- **4.0** — Micropolitan core (small-city high density)
- **5.0** — Micropolitan commute (commutes to small city)
- **6.0** — Small town (isolated small town)
- **7.0** — Rural (isolated rural)
- **10.0–10.5** — Remote rural (least accessible)

**Parse:**
- Match Census tract to RUCA codes CSV
- Extract RUCA code (e.g., "1.0", "10.5")
- Store as `ruca_code`

**Eligibility Impact:**
- USDA VAPG: Bonus points for RUCA > 4 (non-metro)
- USDA Rural grants: Require RUCA ≥ 4 (non-metropolitan)

## USDA Web Soil Survey (SSURGO) API

**Endpoint:** `https://SDMDataAccess.sc.egov.usda.gov/Tabular/post.rest`

**Method:** POST with SQL query in request body

**Query Example:**
```
SELECT * FROM mapunit WHERE muname LIKE '%silt loam%'
```

**Alternative: WMS Endpoint** — `https://SDMDataAccess.sc.egov.usda.gov/Spatial/SDMWMS.ashx`

**Parameters:**
- Request body: SQL WHERE clause filtering by soil type, map unit name, or spatial bounds
- `returnGeometry=true` — Include geographic boundaries

**Response:** JSON with soil unit records. Parse:
- `muname` — Map unit name (e.g., "Butler silt loam, 0 to 2% slopes")
- `drainage_class` — Drainage classification (well drained, somewhat poorly drained, etc.)
- `farmland_classification` — Prime farmland status
- `hydro_group` — Hydrologic soil group (A, B, C, D)

**Rate Limit:** No published limit. 1 request per second (conservative).

**Use for:** Soil type data by location. Essential for any agriculture/remediation grant claiming specific soil conditions. Output: add `soil_type`, `drainage_class`, `farmland_classification` to PROJECT_CONTEXT.

## SoilGrids API

**Endpoint:** `https://rest.isric.org/soilgrids/v2.0/properties/query?lon={lon}&lat={lat}&property={property}&depth={depth}&value=mean`

**Method:** GET

**Parameters:**
- `lon`, `lat` — Decimal coordinates (from Census Geocoder)
- `property` — Soil property code: `phh2o` (pH), `soc` (soil organic carbon), `nitrogen`, `clay`, `sand`, `silt`, `bdod` (bulk density)
- `depth` — Soil depth: `0-5cm`, `5-15cm`, `15-30cm`, `30-60cm`, `60-100cm`, `100-200cm`
- `value=mean` — Return mean value for property

**Response:** JSON with predicted soil properties:
```json
{
  "properties": {
    "phh2o": {
      "mean": 6.8,
      "std": 0.3
    },
    "soc": {
      "mean": 2.5,
      "std": 0.8
    }
  }
}
```

**Parse:**
- Extract property mean values
- Store as quantitative data for grant narratives
- Example: "Baseline soil pH at site is 6.8, organic carbon 2.5% (0-5cm depth)"

**Rate Limit:** No published limit. 1 request per second (conservative).

**Use for:** Global soil property predictions — pH, organic carbon, nitrogen, texture at any coordinate. Key strength: Gives quantitative soil data to back up narrative claims with hard numbers.

## EPA ECHO API

**Endpoint:** `https://echo.epa.gov/tools/web-services/facility-lookups/cwa-lookup?output=JSON&p_st={state}&p_zip={zip}`

**Alternative: Effluent Charts** — `https://echo.epa.gov/tools/web-services/effluent-charts?p_id={facility_id}`

**Method:** GET

**Parameters (Facility Lookup):**
- `p_st={state}` — Two-letter state code
- `p_zip={zip}` — Five-digit ZIP code
- `output=JSON` — JSON response format

**Response:** JSON with facility array. Parse each facility:
- `PermitID` — EPA permit identifier
- `FacilityName` — Facility name
- `Street`, `City`, `State`, `Zip` — Address
- `LatitudeMeasure`, `LongitudeMeasure` — Coordinates
- `ComplianceStatus` — Compliant, noncompliant, etc.

**Use for:** Environmental compliance data near project sites. Identifies brownfields, Superfund sites, contaminated areas, and polluting facilities.

**Critical for:** Remediation and environmental justice grants. Proof of contamination/pollution justifies mycoremediation or phytoremediation focus.

## NASA EarthData / MODIS API

**Endpoint:** `https://modis.ornl.gov/rst/api/v1/{product}/subset?latitude={lat}&longitude={lon}&startDate={start}&endDate={end}`

**Method:** GET

**Parameters:**
- `{product}` — MODIS product code: `MOD13Q1` (vegetation indices), `MOD11A2` (land surface temperature), `MOD17A2H` (net primary productivity)
- `latitude`, `longitude` — Decimal coordinates
- `startDate={YYYY-MM-DD}`, `endDate={YYYY-MM-DD}` — Date range
- Requires registration at https://earthdata.nasa.gov (free, username/password in request)

**Response:** ASCII/JSON with time-series MODIS data. Parse:
- `NDVI` (Normalized Difference Vegetation Index) — Vegetation health (0–10000 scale, higher = healthier)
- `LSTD` — Land surface temperature (Kelvin)
- `NPP` — Net primary productivity (grams carbon per m²)

**Use for:** NDVI (vegetation health), land use change, crop health monitoring via satellite imagery.

**Grant narrative value:** "Satellite NDVI data (2024-2026) confirms degraded land conditions at project site (NDVI = {value}), supporting remediation/restoration focus."

## USDA Food Access Research Atlas API

**Endpoint:** Data download via USDA ERS — `https://www.ers.usda.gov/data-products/food-access-research-atlas/`

**Method:** Static CSV/Excel download (updated annually)

**Data Source:**
- Download: `https://www.ers.usda.gov/webdocs/DataFiles/` + latest dataset ID
- Store locally: `pipeline/data/food_access_atlas.csv`

**Fields to extract:**
- `CensusTract` — Census tract FIPS code
- `LowAccessTracts2010` — Binary (1 = low access, 0 = adequate)
- `LowIncomeTracts` — Binary (1 = low income, 0 = not)
- `PovertyRate` — Poverty percentage
- `VehicleAccessRate` — Percentage without vehicle

**Classification Logic:**
- If `LowAccessTracts2010 = 1` AND `PovertyRate > 20%` AND `VehicleAccessRate > 20%` → `food_apartheid`
- If `LowAccessTracts2010 = 1` → `low_food_access`
- Else → `adequate_access`

**Grant eligibility:** USDA nutrition/food access grants give priority to food apartheid and low-food-access areas.

## ARC Distressed Counties API

**Endpoint:** ARC County Economic Status database — `https://www.arc.gov/county-economic-status-and-distressed-areas/`

**Method:** Static CSV download (updated annually)

**Data Source:**
- Download: `https://www.arc.gov/` (manual export to CSV)
- Store locally: `pipeline/data/arc_county_designations.csv`
- Columns: `state_fips`, `county_fips`, `county_name`, `designation`

**Designations:**
- **Distressed** — Economic indicators in bottom quintile (highest eligibility for ARC grants, highest match reduction)
- **At-Risk** — Indicators trending downward
- **Transitional** — Improving performance
- **Competitive** — Median performance
- **Attainment** — Top quartile (lowest ARC eligibility)
- **Non-Appalachian** — Outside ARC's 13-state region

**Parse:**
- Match `state_fips + county_fips` to CSV
- Extract `designation`
- If not found, set to `non-appalachian`

**Grant eligibility:** ARC grants strongly prefer Distressed and At-Risk counties. Distressed counties are eligible for higher award ceilings and 50% federal match (vs. typical 80/20).

## Workflow: Auto-Populate on Address Entry

**Trigger:** When Josh enters or updates address in PROJECT_CONTEXT.md

**Sequence:**

1. **Parse address** from PROJECT_CONTEXT.md `organization > address` field
2. **Census Geocode** → get census_tract, county_fips, state_fips, lat/lon
3. **EPA EJScreen** → get ej_score (use lat/lon from Census)
4. **Food Access Lookup** → census_tract to food_desert_status
5. **ARC Lookup** → state_fips + county_fips to arc_status
6. **RUCA Lookup** → census_tract to ruca_code
7. **Append all fields** to PROJECT_CONTEXT.md under `## Geospatial Compliance` section
8. **Add comment lines** explaining each field's grant eligibility impact

## Output Example

**Appended to PROJECT_CONTEXT.md:**

```markdown
## Geospatial Compliance

**Census Tract:** 1234.56
- Identifies specific neighborhood for hyperlocal data lookups

**County FIPS:** 42-101 (Philadelphia, PA)
- Used for county-specific grant eligibility (ARC, rural/urban classifications)

**EJ Score:** 78/100
- High environmental justice concern. Qualifies for Justice40 grants.
- Recommend highlighting environmental remediation focus in USDA/EPA proposals.

**Food Desert Status:** food_apartheid
- Census tract is >1 mile from supermarket AND has >20% poverty rate.
- Strong eligibility for USDA nutrition/food access grants.
- Mention community food security in applications.

**ARC Status:** distressed
- Appalachian Regional Commission designates this county as distressed.
- ARC grants offer higher award ceilings and match rates (50% federal match).

**RUCA Code:** 7.0 (Rural, isolated)
- This is isolated rural. Qualifies for all USDA rural development grants.
- Recommend USDA Sustainable Agriculture grants (VAPG) with rural focus.

**Recommendations:**
- Align applications with food apartheid + environmental remediation priorities.
- Emphasize rural isolation and ARC distressed status in federal proposals.
```

## Validation Rules

1. **Address Validation:** Confirm Census Geocoder returns exactly 1 match. If 0 or >1, ask Josh for clarification.
2. **FIPS Codes:** All FIPS codes must be valid (state + county combo exists).
3. **EJ Score Range:** 0–100. If outside range, set to `null` and flag warning.
4. **RUCA Code Match:** If Census tract not found in RUCA CSV, default to `null` and flag warning.
5. **ARC Lookup:** If county not in ARC region, set `arc_status` to `non-appalachian` (not error).

## Operating Law Compliance

- **Rule 2 (Test Your Own Work):** Validate Census Geocoder match quality. Log warnings for ambiguous results.
- **Rule 3 (Org Isolation):** Each org's geo data stored separately in its own PROJECT_CONTEXT.md.

## Error Handling

**Census Geocoder fails:**
- Halt workflow. Ask Josh to provide exact address or county FIPS code manually.

**EJScreen API unreachable:**
- Log error. Continue with other lookups. Set `ej_score: null` with note.

**RUCA/ARC CSV files missing:**
- Fail-closed: Do not populate those fields. Alert Josh to download data files.

## Scheduling & Triggers

- **On-demand:** Josh enters/updates address in PROJECT_CONTEXT.md
- **Auto:** Scout can trigger geo-lookup before RFA matching (ensures geospatial filters are applied)
- **Batch:** Weekly refresh of all client org geographies (update if address changed)

## Local Data Files Required

Create/maintain these in `pipeline/data/`:

1. **arc_county_designations.csv** — ARC distressed/at-risk county list
2. **ruca_codes.csv** — Census tract to RUCA code mapping (USDA NASS download)
3. **food_access_atlas.csv** — USDA food access by Census tract (ERS download)

All three are static, annual updates. Download on setup and refresh yearly.
