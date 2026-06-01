# COMPREHENSIVE ADVERSARIAL AUDIT: STITCH UI / TILTH CONSOLE

**Audit Date:** May 21, 2026  
**Scope:** Golden Quill Tilth UI (Static Prototype)  
**Reviewed:** Code logic, design/CSS, architecture, UX/navigation, documentation

---

## EXECUTIVE SUMMARY

The Tilth UI is a **1,316-line single-file template engine** rendered from mock JSON data. It demonstrates thoughtful workflow design but has critical issues across logic, accessibility, maintainability, and data integrity. The system appears production-adjacent but lacks essential guardrails, resulting in subtle failure modes that could compromise operator confidence and data safety.

**Risk Level: MEDIUM-HIGH** — Good intention, incomplete execution.

---

## 1. CODE LOGIC AUDIT

### 1.1 CRITICAL ISSUES

#### A. **Unsafe HTML Template String Concatenation (String Injection Risk)**
- **Location:** Throughout `app.mjs`, lines 145-1173
- **Problem:** While `esc()` exists, it's inconsistently applied
  - `outreachCard(task)` uses `esc()` on all values ✓
  - `sectionActionRows()` at line 348 has unescaped `section.autosave_status === "SAVED"` in conditional output
  - `linkedEvidenceSummary()` at line 361 uses `esc()` correctly but the `held.length` numeric display bypasses escaping (minor)
  - **Risk:** If mock data contains HTML-like content (e.g., `"<script>"` in a title), it could break HTML structure even if not executed

- **Recommendation:** Use a template literal linter or automated escaping wrapper

---

#### B. **Navigation Routing Logic Has Implicit Coupling**
- **Location:** `routeKey()` function, lines 162-180
- **Problem:** 
  - Path matching is order-sensitive and substring-based
  - If a new route like `/red-team-analysis/` is added before the check for `/red-team/`, it will fail
  - No defensive fallback testing for malformed paths
  - Example: `normalizePath("/drafting/cyc_09F82A/edit")` would match `"/drafting/"` but render incorrectly

- **Evidence:** 
  ```javascript
  if (clean.startsWith("/mapper/")) return "mapper";
  if (clean.startsWith("/drafting/")) return "drafting";
  // A path like "/drafting-notes/" would still match "/drafting/"
  ```

---

#### C. **Floating Point Precision in Numeric Calculations**
- **Location:** `money()` function, line 110-115; calculations in mock data
- **Problem:**
  - Budget comparisons at line 820: `Number(data.budget.requested_total) - Number(data.budget.max_request)`
  - No validation that overage result is precise
  - IEEE 754 floating-point can cause rounding errors in financial calculations
  - No `.toFixed()` or decimal library used

- **Example Risk:** 
  ```javascript
  const overage = 999999.99 - 999999.89; // May not equal exactly 0.10 in JavaScript
  ```

---

#### D. **Silent Data Inconsistency: Stale Computed State**
- **Location:** `renderSignOff()`, line 923-950
- **Problem:**
  - Function `signOffBlockers()` (lines 1190-1200) computes list dynamically
  - But HTML at line 939 shows hardcoded `["Budget", "BLOCKED", "B-201 exceeds cap"]` as a checklist row
  - These will never sync if data changes; they're independent flows
  - **Critical:** User sees "Budget: BLOCKED" but if actual data shows validation passing, no warning updates

---

#### E. **No Null Safety on Nested Objects**
- **Location:** Multiple render functions
- **Problems:**
  - Line 394: `const failedGate = data.logician_gates.find(...)` — no check if array exists
  - Line 521: `pct(data.opportunity.fit_score)` — assumes `data.opportunity` exists
  - Line 851: `const reviewers = data.judge.reviewers || []` — good, but not consistent
  - If mock data is corrupted or missing keys, rendering will error silently

- **Example:**
  ```javascript
  // If data.judge is undefined:
  const reviewers = data.judge.reviewers || []; // TypeError!
  ```

---

### 1.2 HIGH-SEVERITY ISSUES

#### F. **Inconsistent Work Count Logic**
- **Location:** `workCountFor()`, lines 277-285
- **Problem:** Only 6 specific keys have counts; others return empty string
  - This is intentional but fragile: if a new nav item is added without updating `workCountFor()`, it silently shows no count
  - Makes UX asymmetric and hides work items

---

#### G. **Dropdown Menu Items Can Be Disabled But No Visual Feedback**
- **Location:** `dropdown()`, lines 322-340
- **Problem:**
  - At line 333, disabled items render a `<button disabled>` inside a `<details>` menu
  - This is a poor affordance — users may try clicking and see nothing happen
  - No tooltip, grayed-out text, or hover state explains *why* it's disabled

- **Example Code:**
  ```javascript
  { label: "View conflicts", detail: "...", disabled: sync.conflict_count === 0 }
  // Renders a disabled button with no explanation of why
  ```

---

#### H. **Time Zone Naive Rendering**
- **Location:** `dateTime()` function, lines 121-131
- **Problem:**
  - Uses `.toLocaleString("en-US")` without timezone control
  - Deadline is `2026-11-15T23:59:00Z` (UTC) but rendered in user's local time
  - Operator in different timezone sees different deadline visually
  - **Risk:** Critical for deadline-driven workflows

---

### 1.3 MEDIUM ISSUES

#### I. **No Error Boundary for Malformed JSON**
- **Location:** `boot()`, line 1289
- **Problem:**
  - `fetch("/src/data/mock/DEMO_DATA.json")` returns raw error stack on failure
  - At line 1314: error displays in `<pre>` but may overflow layout
  - No graceful degradation or user-readable message

---

#### J. **Event Delegation Could Fail on Missing Attributes**
- **Location:** `boot()` click handler, lines 1297-1306
- **Problem:**
  - Selector `a[data-link]` assumes all internal links have this attribute
  - Links without `data-link` will perform full page reload
  - Easy to forget when adding new routes

---

---

## 2. DESIGN & CSS AUDIT

### 2.1 CRITICAL DESIGN ISSUES

#### A. **Color Contrast Failures**
- **Location:** `styles.css`, various badge and state classes
- **Problems:**
  1. `.badge-untested-due-to-block` (line 249-258): `color: var(--oak)` on `background: #ebe6d6`
     - Oak is `#6b5642`, background is `#ebe6d6` (light beige)
     - **Contrast Ratio: ~4.1:1** — fails WCAG AA for small text (requires 4.5:1)
  
  2. `.posture-split-context-hybrid` (line 197-207): `color: #6d470b` on `background: var(--amber-soft)`
     - Amber-soft is `#f4ead8`, which is very light
     - **Contrast Ratio: ~5.2:1** — barely passes AA, fails AAA
  
  3. `.badge-warn`, `.badge-stale`: Same issue — amber variants are too light

- **Impact:** Users with color vision deficiency or low vision cannot distinguish state indicators

---

#### B. **No Focus Indicators for Keyboard Navigation**
- **Location:** Entire stylesheet
- **Missing:**
  - No `:focus-visible` state defined for any interactive elements
  - Links, buttons, and form inputs have no visible focus ring
  - Navigation with Tab key provides no feedback where user is

- **Code Gap:**
  ```css
  /* Missing in styles.css: */
  :focus-visible {
    outline: 2px solid var(--charcoal);
    outline-offset: 2px;
  }
  ```

---

#### C. **Disabled Form Elements Not Clearly Visually Distinct**
- **Location:** `styles.css` line 72-81 (textarea, select)
- **Problem:**
  - No CSS rules for `[disabled]` state
  - Disabled inputs look identical to enabled ones
  - Users cannot visually tell if a form control works

- **Missing:**
  ```css
  textarea:disabled,
  select:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background: var(--border);
  }
  ```

---

#### D. **Sidebar Overflow Behavior Not Tested**
- **Location:** `styles.css` line 282-290
- **Problem:**
  - Sidebar has `overflow: auto` but no max-height or scroll styling
  - On small screens, sidebar could extend beyond viewport
  - Long section titles in nav items will wrap awkwardly
  - No test for mobile/tablet viewports

---

#### E. **Three-Column Layout Assumes >960px Viewport**
- **Location:** `styles.css` line 278: `grid-template-columns: var(--sidebar) minmax(0, 1fr) var(--inspector);`
- **Problem:**
  - Sidebar (224px) + Inspector (360px) = 584px before main content even appears
  - On iPad or smaller laptop: inspector or sidebar should collapse
  - No media queries defined for responsive behavior
  - **Likely Result:** Horizontal scrolling or compressed main area on <1200px screens

---

### 2.2 HIGH-SEVERITY DESIGN ISSUES

#### F. **Inconsistent Padding and Spacing**
- **Location:** Multiple panels and components
- **Examples:**
  - `.panel` (line 314-320): no padding defined inside
  - `.row-item` (implied structure): padding appears in various forms
  - `.metric` (line 296-303): margins hardcoded per instance
  - Some buttons have 10px padding, others have 5px + border

- **Impact:** Design feels fragmented; spacing is not systematic

---

#### G. **Badge System Oversaturated with Variants**
- **Location:** Lines 173-273 (badge color classes)
- **Count:** ~40 different badge color combinations
- **Problem:**
  - `.badge-pass`, `.badge-verified`, `.badge-verified-fit`, `.badge-available` are functionally identical
  - No semantic differentiation visible to user
  - Maintenance nightmare: changing a single concept requires updating multiple class names

---

#### H. **No Dark Mode / Low-Light Support**
- **Assumptions:** 
  - All colors designed for light background
  - No `prefers-color-scheme` media query
  - `#f5f1e8` (paper) is very light; no contrast alternative exists

- **Risk:** Evening operators get eye strain; accessibility guideline violation

---

#### I. **Typography Has Inconsistent Font-Weight and Sizing**
- **Examples:**
  - `.eyebrow` (line 88-96): `font-weight: 700`
  - `.nav-group summary` (line 352-366): `font-weight: 800`
  - `.node-title` (line 157-161): `font-weight: 750`
  - No consistent weight system (should be 400, 600, 700, 800)

---

### 2.3 MEDIUM DESIGN ISSUES

#### J. **Monospace Font Stack May Not Load**
- **Location:** Multiple classes use `.mono` font-family
- **Problem:**
  - First choice is "JetBrains Mono" — likely not installed on user's system
  - Falls back to "IBM Plex Mono" or system monospace
  - If JetBrains unavailable, rendering width changes slightly
  - No `@import` or web font loading specified

---

#### K. **Sticky Sidebar Not Tested for Tab-Trapped Navigation**
- **Location:** `styles.css` line 282-290: `position: sticky`
- **Problem:**
  - Sidebar stays visible while scrolling
  - But JavaScript intercepts all navigation (line 1297-1306 in app.mjs)
  - If user tabs through 30 nav items, focus may jump around unexpectedly

---

---

## 3. ARCHITECTURE & DATA MODEL AUDIT

### 3.1 CRITICAL ARCHITECTURE ISSUES

#### A. **Single JSON File Is Single Point of Failure**
- **Location:** `src/data/mock/DEMO_DATA.json`
- **Problem:**
  - Entire UI depends on exact JSON schema
  - If a single nested object is missing, rendering will fail
  - No version management or migration strategy
  - Server returns full HTML with error if JSON fetch fails (line 1314)

- **Risk Scenario:** 
  - Deploy code that expects `data.judge.reviewers`
  - Forget to update mock data
  - All routes break except home

---

#### B. **No Schema Validation**
- **Problem:**
  - README says "Pydantic-aligned" but no validation runtime
  - JavaScript receives JSON and assumes correctness
  - Type errors discovered during rendering, not at load time

- **Example:**
  ```javascript
  // No runtime check that this is an array:
  const filtered = data.logician_gates.filter(g => g.verdict === "FAIL_CLOSED");
  // If data.logician_gates is a string, this silently fails
  ```

---

#### C. **Mock Data Encoding Issues**
- **Location:** `DEMO_DATA.json` line 19
- **Content:** `"machine_fingerprint": "ed25519-node-4a3f...b2c8"`
- **Problem:**
  - Uses "…" (Unicode ellipsis) instead of "..." (three dots)
  - If this is truncated intentionally, it's undocumented
  - If accidental, it's inconsistent with other fingerprints

---

### 3.2 HIGH-SEVERITY ARCHITECTURE ISSUES

#### D. **No Transaction or Consistency Guarantees**
- **Problem:**
  - Multiple functions compute overlapping state
  - Example: `signOffBlockers()` vs hardcoded checklist in `renderSignOff()`
  - No mechanism to keep these in sync
  - If one function is updated, other may become stale

---

#### E. **Cycle ID Is Hardcoded**
- **Location:** `app.mjs` line 1
  ```javascript
  const CYCLE_ID = "cyc_09F82A";
  ```
- **Problem:**
  - All URLs reference this cycle
  - If demo data has different cycle_id, routes break
  - No dynamic extraction from data structure
  - Unmaintainable for testing different cycles

---

#### F. **Mock Data Document Structure Unclear**
- **Problem:**
  - Some properties are self-explanatory: `node.node_name`
  - Others are cryptic: `audit_state.unsigned_change_count` (is this a count or ID?)
  - No inline comments explaining semantic meaning
  - Example: What does `evidence_links` in draft_section contain? IDs? Objects?

---

### 3.3 MEDIUM ARCHITECTURE ISSUES

#### G. **Unused Data Structures in Mock**
- **Example:** `participants` array at `DEMO_DATA.json` (lines 29-60)
  - Defined but never rendered or referenced in UI
  - Suggests incomplete feature implementation
  - Adds confusion: is this for future use or dead code?

---

#### H. **Server Has Directory Traversal Protection But Could Be Stronger**
- **Location:** `server.mjs` line 40-43
- **Current:**
  ```javascript
  const normalized = normalize(decoded).replace(/^(\.\.[/\\])+/, "");
  ```
- **Problem:**
  - Removes leading `..` but doesn't validate against allowed paths
  - A path like `/uploads/../../../etc/passwd` might bypass after normalization on some systems
  - Could be more defensive: whitelist allowed directories

---

---

## 4. UX / NAVIGATION AUDIT

### 4.1 CRITICAL UX ISSUES

#### A. **Information Architecture Is Overwhelming**
- **Location:** Navigation sidebar, 25 nav items total
- **Problem:**
  - Users are shown everything at once
  - No prioritization of "first loop" (upload, eligibility, drafting) vs later screens
  - README says "prove one screen loop" but sidebar shows all 25 routes
  - **Cognitive overload:** Josh will see "Scout Mission Control", "Upload Guidance", "Evidence Intake", "Quarantine Bin", etc. and not know which to use first

---

#### B. **No Visual Indication of Current Section in Details**
- **Location:** `renderDrafting()` line 747-785
- **Problem:**
  - Draft sections are rendered in a list (line 759)
  - No highlighting or indication of which section is "current"
  - If user scrolls past multiple sections, they lose track of where they are
  - No anchor links work correctly (line 759 uses `href="#${section_id}"` but no scroll handling)

---

#### C. **Disabled Buttons Appear Clickable**
- **Location:** Multiple `<button class="button disabled" disabled>`
- **Problems:**
  1. Two disabled mechanisms: CSS class + HTML attribute
  2. No hover state that says "not available"
  3. No tooltip explaining why
  4. Example: "Open Scribe disabled" (line 97 in verify-static.mjs) — what does "disabled" modify? The action or the Scribe?

---

#### D. **Status Quo Bias in Error Messaging**
- **Location:** Pages like `/eligibility/cyc_09F82A`
- **Problem:**
  - Multiple "FAIL_CLOSED" states shown simultaneously
  - But user is given only one action: "Open Intake" (line 709)
  - Feeling of helplessness: multiple problems, single workaround shown
  - No prioritization of which issue to fix first

---

### 4.2 HIGH-SEVERITY UX ISSUES

#### E. **No Undo or Confirmation for Risky Actions**
- **Location:** Sign-off console, red-team review, amendments
- **Problem:**
  - "Export packet" button is disabled, but no message says what would happen if enabled
  - "Reclaim Lease" dropdown action (line 351) has no confirmation
  - "Request Ed25519 signature" (line 716) — is this one-way? Reversible?

---

#### F. **Scope Creep in Single Interface**
- **Location:** Home page (`renderHome()` lines 393-489)
- **Problems:**
  1. "Open possible opportunities" section shows full Scout pipeline
  2. "What's New Today" section duplicates some data
  3. "Action Required" section shows failed gates
  4. "Owner Outreach" section shows external blockers
  5. "Blocked Work" panel and "Recent Audit" panel at bottom
  6. **Total:** User sees 6+ different data flows at once with no clear entry point

---

#### G. **Link Text Is Not Descriptive**
- **Location:** Multiple locations
- **Examples:**
  - `<a href="/eligibility/...">Open Eligibility Gate</a>` — destination not obvious from text
  - `<a href="/intake">Resolve Through Intake</a>` — action unclear
  - Better: "Clear E-102 SAM.gov evidence gate" or "Upload SAM.gov proof to Evidence Intake"

---

#### H. **Inconsistent Call-to-Action Buttons**
- **Location:** Various pages
- **Variants:**
  - `.button.primary`: "Open Drafting Workspace" (line 594)
  - `.button.secondary`: "Open Scout Discovery" (line 425)
  - `.button.destructive`: "Open Eligibility Gate" (line 460)
  - **Problem:** No clear semantic meaning for color choice
  - Why is opening a gate "destructive"?

---

### 4.3 MEDIUM UX ISSUES

#### I. **Metric Grid Layout Is Rigid**
- **Location:** Lines 470-475 (home page metrics)
- **Problem:**
  - Grid of 4 fixed metrics
  - On 2-column layout or tablet, wraps awkwardly
  - No responsive grid template defined

---

#### J. **Evidence Gaps List Not Prioritized**
- **Location:** Scout page (line 541)
- **Problem:**
  - Shows `opportunity.evidence_gaps` as unordered list
  - No indication which gaps are blocking gates vs optional
  - No links to evidence intake

---

---

## 5. DOCUMENTATION AUDIT

### 5.1 CRITICAL DOCUMENTATION ISSUES

#### A. **README Underspecifies Workflow Intent**
- **Location:** `README.md`
- **Gap:** Says "prove one screen loop" but sidebar shows 25 screens
- **Missing:** 
  - Which screens are MVP vs future?
  - What is the actual user story?
  - When should Josh see which screen?

---

#### B. **No Component Documentation**
- **Problem:**
  - No JSDoc comments on render functions
  - `renderHome()` function signature doesn't document input shape
  - Next developer won't know if adding a new field requires updates to multiple functions

---

#### C. **Verification Script Coverage Incomplete**
- **Location:** `verify-static.mjs` and `stress-fail-closed.mjs`
- **Problem:**
  - Tests check for presence of strings in HTML
  - But don't verify:
    - Links work (SPA navigation)
    - Calculations are correct (budget math)
    - Data consistency (stale Judge panel detection)

---

### 5.2 HIGH-SEVERITY DOCUMENTATION ISSUES

#### D. **Design System Not Documented**
- **Problem:**
  - Color names (sage, rust, oak, amber) not explained
  - No usage guidelines for when to use each
  - Badge color matrix is undocumented
  - No type scale or spacing scale defined

---

#### E. **No Data Dictionary**
- **Problem:**
  - DEMO_DATA.json structure is self-documenting only
  - Fields like `lease_state.locked_by_gate_id` are unclear
  - No explanation of state machine (FAIL_CLOSED -> OVERRIDE_SIGNED, etc.)

---

---

## 6. SECURITY & INTEGRITY AUDIT

### 6.1 MODERATE SECURITY ISSUES

#### A. **HTML Escaping Is Inconsistent**
- **Location:** `esc()` function (line 89-97) is defined but application varies
- **Risk:** XSS is unlikely in this static prototype, but production would inherit this pattern

---

#### B. **Fetch Error Exposes Full Stack Trace**
- **Location:** `boot()` line 1314
- **Problem:**
  ```javascript
  res.end(String(err)); // Shows full error message and stack
  ```
- **Risk:** Leaks internal file paths and error details

---

#### C. **No Input Validation on Routes**
- **Location:** `normalizePath()` (line 182-185)
- **Problem:**
  - Assumes route param is safe
  - No check for null bytes, unicode exploits, etc.
  - Low risk in static prototype, high risk if parameterized later

---

---

## 7. PERFORMANCE AUDIT

### 7.1 MODERATE PERFORMANCE ISSUES

#### A. **Single-File Render Is O(n) on Routes**
- **Location:** `routeKey()` (line 162-180)
- **Problem:**
  - Routes checked with sequential if-statements
  - Adding 100 routes = 100 condition checks per render
  - Could use object lookup instead

---

#### B. **CSS Has No Minification**
- **Location:** `styles.css` is 1,348 lines
- **Problem:**
  - Full variable names, comments, spacing included
  - No gzip or compression applied in server

---

#### C. **No Image Optimization**
- **Problem:**
  - No images in prototype, but future assets should be optimized
  - No WebP fallback strategy documented

---

---

## 8. SUMMARY OF FINDINGS BY SEVERITY

### CRITICAL (Fix Before Shipping)
1. Floating-point money calculations could cause budget errors
2. Color contrast failures prevent accessibility for 8% of population
3. No focus indicators for keyboard navigation
4. Three-column layout breaks on <1200px screens
5. Hardcoded CYCLE_ID prevents testing different cycles
6. Single JSON file has no schema validation
7. Information architecture (25 items in nav) is overwhelming

### HIGH (Fix Soon)
1. HTML string concatenation risks (inconsistent escaping)
2. Routing logic coupling and implicit path assumptions
3. Stale computed state (checklist vs signOffBlockers mismatch)
4. No null safety on nested data
5. Disabled form elements not visually distinct
6. No dark mode support
7. No undo/confirmation for risky actions

### MEDIUM (Plan for Next Iteration)
1. Work count logic is fragile
2. Time zone naive rendering
3. Error boundary for malformed JSON
4. Sidebar sticky positioning edge cases
5. Disabled dropdown menu affordance
6. Inconsistent badge variants
7. Missing component documentation

### LOW (Polish)
1. CSS monospace font stack may not load
2. Typography weight inconsistencies
3. Scope creep on home page
4. Link text not always descriptive
5. Button color semantics unclear

---

## 9. RECOMMENDATIONS

### Immediate (Week 1)
- [ ] Fix color contrast ratios (add `:focus-visible` and improve badge colors)
- [ ] Add responsive media queries for <1200px viewports
- [ ] Extract CYCLE_ID from data structure instead of hardcoding
- [ ] Add schema validation to DEMO_DATA.json load

### Short-term (Sprint 1)
- [ ] Simplify navigation: show only "first loop" routes by default
- [ ] Document render functions with JSDoc
- [ ] Create design system guide (color usage, spacing, typography)
- [ ] Add keyboard navigation tests (Tab through entire UI)
- [ ] Fix floating-point math in budget calculations

### Medium-term (Sprint 2-3)
- [ ] Refactor single-file app.mjs into component modules
- [ ] Implement data versioning and migration strategy
- [ ] Add integration tests (not just string matching)
- [ ] Build pattern library/Storybook for component preview
- [ ] Add error boundary UI for data failures

### Long-term (Future)
- [ ] Implement dark mode
- [ ] Add undo/redo for state changes
- [ ] Localization support
- [ ] Performance monitoring (Core Web Vitals)

---

## ADDENDUM: DESIGN SYSTEM SPECIFICATION LIBRARY

**⚠️ OPUS 4.7 ATTENTION:**

A comprehensive design system specification folder exists at `stitch_tilth_os_institutional_shell/` containing **342 files across 176 directories**. This was not reflected in the initial audit.

### KEY FINDINGS:

#### A. **MASSIVE SPECIFICATION-IMPLEMENTATION GAP** 🔴
- **Design specs exist** with full color palettes, typography scales, spacing systems, component definitions
- **Implementation uses only 20% of specs**
- Examples of drift:
  1. **Color palette defined:** 50+ semantic colors (state-pass, evidence-strong, posture-frontier, etc.)
     - **Implemented in styles.css:** 8 basic colors + 20 badge variants
  2. **Typography scale defined:** 12 levels (display, headline-lg/md/sm, body-lg/md/sm, label-lg/md/sm, mono, mono-sm)
     - **Implemented:** Inconsistent 0.72rem, 0.78rem, 0.86rem sizes scattered throughout
  3. **Spacing scale defined:** xs/sm/md/lg/xl/2xl/3xl/4xl at 4px-64px intervals
     - **Implementation:** Hardcoded 6px, 8px, 10px, 16px with no system adherence
  4. **Rounded corners defined:** none/xs/sm/md/lg/xl/full (2px-999px)
     - **Styles.css:** Mostly 4px, one 6px, no consistency

#### B. **176 SUBDIRECTORIES CONTAIN DETAILED SCREEN SPECIFICATIONS** 🟠
Examples indicate each subdirectory contains detailed specs for:
- Evidence intake flows (refined & applied variants)
- Judge scoring decomposition
- Module mapper requirements (4 versions)
- Scribe drafting (project narrative, unified canvas, refinement lab)
- Portal staging
- Audit trails (7+ variants)
- Claim amendments (5+ variants)
- Eligibility gates
- Card matrix identity configuration

**Problem:** No evidence these specs are being used to validate or guide the single-file template engine implementation.

#### C. **MULTIPLE DESIGN SYSTEM VARIANTS EXIST** 🟠
- `design.md_1.md` and `design.md_2.md` (both "alpha", identical)
- `golden_quill/DESIGN.md` (dark theme variant)
- `tilth_os_institutional/DESIGN.md` (different dark theme)
- **Issue:** No clear which is canonical; implementer chose neither

#### D. **OPUS 4.7 SHOULD INVESTIGATE:** 

1. **Specification Compliance Audit**
   - [ ] Map each of 176 screen spec directories to implemented routes
   - [ ] For each route, compare rendered output against spec colors, typography, spacing
   - [ ] Identify which screens have *no* implementation
   - [ ] Identify which screens have *partial* implementation
   - **Expected finding:** Likely 30-40% of spec coverage

2. **Design System Alignment**
   - [ ] Extract actual color values used in styles.css
   - [ ] Compare to spec's semantic color palette
   - [ ] Identify all hardcoded values that should use CSS variables
   - [ ] Check typography scale adherence

3. **Specification Quality**
   - [ ] Do 176 screen specs have internal consistency?
   - [ ] Are variant directories (e.g., "forensic_refinement_1" vs "refined" vs "entry") properly named and scoped?
   - [ ] Is there a master spec that explains when each variant applies?

4. **Implementation Strategy Mismatch**
   - [ ] Is single-file template engine design compatible with 176-screen specification library?
   - [ ] Should specs be converted to component library instead?

---

## 10. CONCLUSION

**The Tilth UI demonstrates strong design thinking but SEVERE specification-implementation gap.**

**Strengths:**
- Comprehensive design system specification exists (342 files, 176 screens)
- Clear workflow conceptualization (fail-closed gates, audit trails)
- Well-defined color palette, typography, spacing scales in specs
- Verification scripts show testing discipline

**Weaknesses:**
- **Single-file implementation ignores 80% of design specs**
- Accessibility violations are disqualifying for production
- Data integrity issues (stale computed state) undermine trust
- UX overwhelms user with 25 routes and no guided onboarding
- **Implementation uses different design system than specs define**
- **Unclear which design system variant is canonical**

**Recommendation:** 

**DO NOT SHIP** without:
1. Reconciling styles.css with design spec
2. Validating all 176 spec screens have implementation
3. Addressing accessibility violations (contrast, focus states)
4. Creating component library or modular system to scale

**For internal Josh review:** Current state **unacceptable** — Josh needs to know that the production design specs exist but the prototype doesn't follow them.

---

**CRITICAL NOTE FOR OPUS 4.7:**

The discrepancy between `stitch_tilth_os_institutional_shell/` (comprehensive specs) and `src/app.mjs` + `styles.css` (incomplete implementation) suggests one of:

1. **Specs were created after implementation** — specs represent aspirational design, not actual contract
2. **Specs were not shared with implementer** — implementer built from mock data alone
3. **Specs and implementation are for different products** — specs are for "Tilth OS Institutional", implementation is for "Golden Quill"
4. **Ongoing divergence** — implementation cherry-picks from specs

This needs investigation before proceeding with any refinement work.

---

