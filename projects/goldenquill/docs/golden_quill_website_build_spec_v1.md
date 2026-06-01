# Golden Quill Website — Build Spec v1

**Status:** Draft for Josh's review
**Date:** 2026-05-09 (amended 2026-05-15 — sovereignty stat callout added to Home §7a + Founder Nodes hero proof strip; Gallup 70% local-data-center opposition is the load-bearing market evidence)
**Owner role:** FIT Farms LLC
**Scope:** V1 public marketing site — five pages, no auth, no app

---

## 1. Sitemap

| # | Page | URL | Job |
|---|---|---|---|
| 1 | Home | `/` | Surface the offer; route visitors to deeper pages and CTAs |
| 2 | Founder Nodes | `/founder-nodes` | Sell the hardware tiers + reservation flow |
| 3 | Why Tilth. Why Now. | `/why-tilth-why-now` | Strategic argument — why this matters now |
| 4 | Consulting | `/consulting` | Capture immediate-help inquiries; bridge to Founder Nodes |
| 5 | Contact | `/contact` | Single qualification form |

**Top nav (sticky, dark, minimal):** Golden Quill (logo, links to Home) · Founder Nodes · Why Tilth · Consulting · Contact · **Request a Consultation** (button)

**No blog. No About. No Resources. V1 stays tight.**

The About / Founder credibility (thousands of grants + collaboration with funding-area professionals) is folded into the Home page and the Why Tilth page rather than getting its own page in V1.

---

## 2. Brand framing — load-bearing decisions

- **Customer-facing entity:** FIT Farms LLC (only). No mention of Sovereign Node LLC anywhere on the site. Footer attribution: `© 2026 FIT Farms LLC. Golden Quill / Tilth.`
- **Naming chain:** Golden Quill = the hardware product. Tilth = the software intelligence inside it. The customer's relationship is primarily with Tilth; Golden Quill is the case it runs on.
- **Tier names:** Standard / Pro / Institutional. **NOT** "Base Founder Node / Professional Founder Node / Institutional Node" — those names from prior drafts are retired.
- **"Founders Node":** cohort badge for the first 12 buyers across all three tiers. Not a tier label. Visible on every tier card as a "11 of 12 Founders Node slots remaining" callout.
- **No CIC / CLC framework names on the site.** Audience tiles use plain English (Schools / Farms / Public Agencies / Arts & Culture / Co-ops / Intermediaries).
- **Hardware platform:** NVIDIA GB10 Grace Blackwell Superchip across the line. ASUS Ascent GX10 powers Standard; Dell Pro Max with GB10 powers Pro; Institutional configured to spec (Dell / Lenovo / HP).
- **Service area:** white-glove setup + in-house training included for deployments within a 50-mile radius of Pittsburgh, PA. Out-of-area = travel + per diem upcharge.
- **Hero brand line (Home + footer):** *The real work doesn't wait. Your funding shouldn't either. Stop renting intelligence. Own the system that helps you win.*

---

## 3. Page-by-page outline

### 3.1 Home (`/`)

**Job:** Get a visitor to feel both pains (deadline-survival, knowledge-loss) inside 10 seconds, name the offer, and route them deeper.

#### Section order

1. **Hero**
   - Headline: *The real work doesn't wait. Your funding shouldn't either.*
   - Sub-headline: *Stop renting intelligence. Own the system that helps you win.*
   - Body: *Golden Quill is a customer-owned desktop AI supercomputer powered by Tilth — the funding operating system for mission-driven organizations.*
   - Triplet line: *Your machine. Your files. Your funding intelligence.*
   - Primary CTA: **Reserve a Founders Node — $1** → `/founder-nodes#reserve`
   - Secondary CTA: **Request a Consultation** → `/contact`
   - Asset: composite of Dell Pro Max + 27" monitor + gold keyboard + gold mouse. (V1 fallback: clean product-grid layout if composite isn't producible without rendering risk.)

2. **Funding work needs infrastructure**
   - One-line headline + 3–4 sentence problem statement.
   - Lead: *Good organizations have the work, the relationships, the evidence, and the vision. What they lack is a reliable system for turning that knowledge into funder-ready proposals, reports, and renewal materials without burning out the people who know the work best.*
   - Close: *Golden Quill gives that work a place to live.*
   - Asset: none (let the words breathe). Optional editorial divider.

3. **What Tilth helps you do**
   - Seven-card grid with icons:
     - **Discover** — aligned funding opportunities
     - **Decompose** — applications, requirements, review criteria
     - **Draft** — proposals, letters, budgets, narratives
     - **Review** — for evidence gaps, compliance, weak claims
     - **Capture** — photos, notes, invoices, outcomes
     - **Report** — to funders, boards, partners
     - **Remember** — what was pursued, won, delivered, learned
   - Footnote tag: *Capture, Report, and Remember are part of Tilth's roadmap and ship in stages — see Why Tilth · Why Now for the full sequence.* (Necessary disclosure since some agents are v0.2 / v1.x.)

4. **Choose your Founders Node** — preview, three cards
   - Standard $12,900 / Pro $19,900 / Institutional $24,900+
   - Each card: tier name, price, one-line descriptor, "Reserve for $1" PayPal CTA, "View full specs" link to `/founder-nodes`
   - Visible counter: *11 of 12 Founders Node slots remaining*
   - No spec dump on the homepage — this is a preview that drives to `/founder-nodes`.

5. **Built from working grant practice**
   - One paragraph anchored on credibility: *Tilth is being developed from thousands of funded proposals and active collaboration with grant professionals across food systems, education, public agency, arts, cooperative, and ecosystem-intermediary funding. The system is shaped by what actually happens when small organizations pursue funding under pressure.*
   - This is the About / Founder page in compressed form, on the Home page.

6. **Designed for mission-driven organizations**
   - Six tiles, plain-English audience doors:
     - Schools & youth programs
     - Farms & producers
     - Public agencies & municipal stewards
     - Arts & cultural organizations
     - Cooperatives & member networks
     - Ecosystem intermediaries & project builders
   - Closing line: *Especially those with serious projects, thin administrative capacity, and knowledge worth protecting.*
   - V1 click-through: each tile links to `/contact?audience=schools` (etc.) so the form pre-fills the audience field. No dedicated per-audience landing pages in V1.

7. **Funding intelligence becomes regenerative capacity** — cinematic motion section
   - Headline + one-paragraph copy: *Golden Quill turns the work your organization is already doing — projects, evidence, relationships, reports, and strategy — into reusable funding intelligence. Each proposal, report, and funding cycle strengthens the next.*
   - Asset: Gemini chip animation in a framed panel. Muted loop, dark/gold overlay, 60–70% opacity over a charcoal field. NOT full-screen, NOT hardware proof.

7a. **Sovereignty is the market** — stat callout
   - Headline: *Seven in ten Americans don't want an AI data center in their neighborhood.*
   - Sub-line: *Forty-eight percent are strongly opposed. (Gallup, 2026.)*
   - Body: *Golden Quill runs on one box at your desk. Your data never leaves. Your keys belong to you. If FIT Farms disappeared tomorrow, you would still have your machine, your data, your work.*
   - Visual: single large stat ("70%") in gold over charcoal field, with the secondary stat ("48% strongly opposed") in smaller weight beneath. No additional ornament.
   - This section sits between cinematic motion (§7) and consulting bridge (§8). One screen-height max. The job is to make the sovereignty thesis feel like a market fact, not an ideological position.

8. **Consulting bridge**
   - Two sentences: *Not ready to deploy a Founders Node? Golden Quill also offers grantwriting, fundraising strategy, and program-development consulting — immediate support for organizations preparing for their next funding cycle.*
   - CTA: **Learn About Consulting** → `/consulting`

9. **Final CTA**
   - Headline: *Own the work. Build the memory. Fund what matters.*
   - One-line close: *Golden Quill is built for organizations ready to own the process.*
   - CTA pair: **Reserve a Founders Node — $1** + **Request a Consultation**

10. **Footer** (shared across all pages — see § 5)

---

### 3.2 Founder Nodes (`/founder-nodes`)

**Job:** Make the offer feel like a real product. Convert serious visitors into a $1 reservation.

#### Section order

1. **Hero**
   - Headline: *Choose your Golden Quill Founders Node.*
   - Sub-headline: *Compact desktop AI supercomputers configured for funding work.*
   - Body: *Golden Quill turns GB10-class desktop AI hardware into governed funding infrastructure for mission-driven organizations.*
   - Visible cohort counter: *11 of 12 Founders Node slots remaining*
   - Asset: Dell Pro Max product image (preferred) or ASUS Ascent GX10, on a dark gradient.

2. **Hardware proof strip** — five chips, single row on desktop, 2-row stack on mobile
   - **NVIDIA GB10 Grace Blackwell Superchip** — desktop AI supercomputing
   - **128 GB unified memory** — built for local model workflows
   - **1 petaFLOP FP4 class performance** — high-density AI compute on-site
   - **Local-first deployment** — your files stay where your work lives
   - **Tilth configured** — grant discovery, drafting, evidence, reporting, memory
   - Each chip is a small dark card with thin gold accent. No paragraphs.

2a. **Sovereignty stat strip** — one line under the chip row
   - Single line, italicized, smaller weight: *70% of Americans oppose AI data centers in their neighborhood (Gallup, 2026). Golden Quill runs on one box at your desk.*
   - Visual: same charcoal field as the chip row; gold rule above and below; no graphic — the stat carries the section.
   - The job is to anchor "local-first deployment" (chip 4) in a market fact before the visitor reaches the price comparison.

3. **Three-column package comparison**
   - Apple-style product grid. Each column: tier name, price, real product image, short descriptor, spec list, "Reserve for $1" CTA.
   - Pro column carries a "Recommended" badge in gold.

   | | **Standard** | **Pro** *(Recommended)* | **Institutional** |
   |---|---|---|---|
   | Price | **$12,900** | **$19,900** | **$24,900+** |
   | Image | ASUS Ascent GX10 | Dell Pro Max with GB10 | Quoted-config card |
   | Best for | First deployments, smaller organizations | Serious grant-active organizations | Multi-team, public-sector, school, consortium, institutional |
   | Hardware | ASUS Ascent GX10 (GB10 / DGX Spark) | Dell Pro Max with GB10 (NVIDIA DGX OS) | Dell / Lenovo / HP, configured |
   | Memory | 128 GB unified | 128 GB LPDDR5X unified | 128 GB+ / quoted |
   | Storage | 1 TB local SSD | 4 TB local M.2 SSD | Expanded storage available |
   | Display + input | Standard deployment kit | 27" monitor, gold anodized aluminum keyboard, gold wireless mouse | Team / department configuration |
   | Cooling / airflow | Standard setup | Airflow / cooling stand included | Quoted by environment |
   | Support | Standard Founders Node support | Dell ProSupport / ProSupport Plus + Node Care | Expanded support and governance |
   | Included services | Tilth configuration · white-glove setup · in-house training · 6 months Node Care | Tilth configuration · white-glove setup · in-house training · 6 months Node Care · premium accessory kit | Expanded onboarding · governance design · storage planning · staff training · support |
   | Service area | 50-mile radius from Pittsburgh, PA included | 50-mile radius from Pittsburgh, PA included | 50-mile radius from Pittsburgh, PA included |
   | CTA | **Reserve for $1** | **Reserve for $1** | **Reserve for $1** |

   *Internal margin numbers (~$5K Standard, ~$10.5–11.2K Pro hardware/accessory spend) are NOT on the public table.*

4. **Service-area note** — small, directly under the table
   - *White-glove setup and in-house training are included within a 50-mile radius of Pittsburgh, Pennsylvania. We deploy anywhere; out-of-area installs add travel and per diem.*

5. **Pro spotlight — "Recommended deployment"**
   - Side-by-side: Dell Pro Max product image on left, descriptive copy on right.
   - Copy: *Built around the Dell Pro Max with GB10 — NVIDIA DGX OS, 128 GB LPDDR5X memory, 4 TB local SSD, premium ProSupport. The Pro Founders Node is the recommended Golden Quill deployment for organizations that want the strongest standard configuration.*
   - Sub-block on Dell ProSupport / ProSupport Plus benefits (verified language pulled from the Dell PDF — see § 6 verification log).

6. **What every Founders Node includes**
   - Six-icon row: Tilth configuration · white-glove setup · in-house training · 6 months Node Care · grant workflow configuration · file / evidence intake.
   - One paragraph closer: *The hardware is not the whole product. The product is the configured system: local AI compute, Tilth workflows, grant logic, evidence capture, review patterns, setup, training, and human authority.*

7. **Reservation FAQ** — short, three Q&As
   - **What does $1 reserve?** *A $1 reservation holds one of the remaining Founders Node slots. It is a reservation of the opportunity to purchase, not a deposit toward purchase. Final purchase happens at launch contingent on qualification.*
   - **What is qualification?** *We talk with you about your organization, your funding work, your readiness, and your fit for a white-glove deployment. The Founders cohort is small; we want each install to succeed.*
   - **What if I don't qualify, or change my mind?** *We refund the $1. No further obligation.*

8. **Final CTA**
   - Headline: *11 of 12 Founders Nodes remaining.*
   - CTA: **Reserve for $1**
   - Secondary CTA: **Talk to us about Institutional deployment** → `/contact?interest=institutional`

9. **Footer**

---

### 3.3 Why Tilth. Why Now. (`/why-tilth-why-now`)

**Job:** Make the strategic case. Hardware finally exists; generic AI is a liability; competitive applications need governed intelligence.

#### Section order

1. **Hero**
   - Headline: *Why Tilth. Why now.*
   - Sub-headline: *Funding work is changing. The hardware finally exists to keep up.*
   - One paragraph framing the moment.

2. **The hardware finally exists**
   - GB10 Grace Blackwell Superchip explanation in plain language. Why the form factor matters (compact desktop, not data-center). Why 128 GB unified memory is a threshold.
   - Visual: GB-10 abundance chip image OR a clean technical close-up.

3. **Generic grant software helps — but it's not enough**
   - Acknowledge what SaaS / grant databases / AI writing tools do well. Then name what they don't do (preserve memory, hold sensitive context, govern proposals, defend against generic-AI flagging).

4. **Generic AI language is becoming a liability**
   - Trend-as-pain framing: funders increasingly flag inflated, ungrounded, automation-flavored prose. The pain isn't AI use — it's the tell.

5. **The most competitive applications come from governed intelligence**
   - List of what makes a proposal believable: real work, credible partners, specific evidence, fundable design, accurate budgets, funder-aware language, compliance discipline, human editorial authority. Tilth supports each.

6. **Tilth is built for human-led funding work**
   - Tilth doesn't write grants on its own. The human carries judgment; Tilth carries the mechanical and analytical burden.

7. **Local control changes the economics of knowledge**
   - Where institutional memory normally goes to die (consultant turnover, departed staff, stale spreadsheets, locked grant portals). How local custody compounds instead.

8. **Why now**
   - Five-line summary: hardware powerful enough · generic AI losing its advantage · funders more sensitive · small/mid-size orgs need capacity without surrendering knowledge · the competitive edge is governed intelligence.

9. **CTA**
   - **Reserve a Founders Node — $1** + **Request a Consultation**

10. **Footer**

---

### 3.4 Consulting (`/consulting`)

**Job:** Capture buyers who need help now and aren't ready for a Founders Node. Bridge to the deployment offer.

#### Section order

1. **Hero**
   - Headline: *Grantwriting and fundraising consulting.*
   - Sub-headline: *Immediate support before adopting a full Golden Quill deployment.*

2. **What we help with**
   - Six bullets, plain English: fundable project clarification · opportunity identification · narrative development · program design · proposal materials · funding systems setup.

3. **Who it's for**
   - Same six audience tiles as Home § 6 — schools, farms, public agencies, arts, cooperatives, ecosystem intermediaries.

4. **From consulting to Founders Node**
   - One paragraph: *Many consulting clients eventually deploy a Founders Node. The intake work, document organization, and project framing we do together becomes the substrate Tilth runs on. Consulting is often the first step.*

5. **Final CTA**
   - **Request a Consultation**

6. **Footer**

**No pricing on this page in V1.** The advisory service ladder ($500 onboarding, $250 alert setup, $9/mo radar email, $750+ drafts, etc.) discussed in the ChatGPT thread stays internal until you decide to surface a service menu.

---

### 3.5 Contact (`/contact`)

**Job:** Qualify a serious lead in one form, route them.

#### Form fields

**Required (5):**
- Name
- Organization
- Email
- What are you trying to fund? (textarea, ~3 lines)
- Interest: Consulting / Founders Node deployment / Both *(radio)*

**Optional (5):**
- Phone
- Location (city, state)
- Audience: Schools / Farms / Public Agencies / Arts & Culture / Cooperatives / Ecosystem Intermediaries / Other *(dropdown — pre-fills from Home audience tiles)*
- Current grant or fundraising activity? *(textarea)*
- Anything else we should know? *(textarea)*

**Submit:** "Request a Consultation" button.

**Submission target:** `/api/submit` (Cloudflare function or static-form handler — see § 7 build notes). Graceful fallback: `mailto:` link in case the function fails.

**Below the form:** *Golden Quill is currently developed and operated by FIT Farms LLC. Pittsburgh, Pennsylvania.*

#### Confirmation page

After submit, redirect to `/contact/thank-you` (or replace form with inline confirmation): *Thanks. We'll follow up within 2 business days.* Plus a "View Founders Node options" CTA back to `/founder-nodes` for buyers who haven't reserved yet.

---

## 4. Asset placement map

| Section | Asset | File | Notes |
|---|---|---|---|
| Home § 1 hero | Composite product shot OR product grid | Dell Pro Max + 27" monitor + GT80 Gold keyboard + Satechi M1 mouse | If composite, mark as concept; V1 fallback = product grid |
| Home § 7 motion | Gemini chip animation | `Let's_animate_this_around_the.mp4` | Muted loop, dark/gold overlay, framed panel |
| Founder Nodes § 1 hero | Dell Pro Max product image | `Dell Workstation.png` or extract from Dell PDF | Real product imagery |
| Founder Nodes § 3 — Standard column | ASUS Ascent GX10 | `Asus Ascent GX10.png` (or 2.png) | Real product imagery |
| Founder Nodes § 3 — Pro column | Dell Pro Max with GB10 | `Dell Workstation.png` | Real product imagery |
| Founder Nodes § 3 — Institutional column | Quoted-config placeholder card | (none — render a neutral workstation silhouette) | No fake hardware |
| Founder Nodes § 5 Pro spotlight | Dell Pro Max + ProSupport visual cue | Extract from Dell PDF | Real product imagery |
| Why Tilth § 2 hardware-finally-exists | GB-10 abundance still | `GB-10 abundance chip.jpg` | Cinematic atmosphere only |
| All pages footer | Wordmark + favicon | (need to commission/design) | Open item |

**Brand assets still needed:**
- Golden Quill wordmark (primary)
- Golden Quill icon / quill mark (secondary)
- Favicon (16/32/180/192/512)
- Social preview image (1200×630)
- 27" monitor product shot (need OEM image once monitor model is picked — propose Dell U2725QE)

---

## 5. Footer (shared, all pages)

```
GOLDEN QUILL
powered by Tilth
A customer-owned funding workbench for mission-driven organizations.

© 2026 FIT Farms LLC.   Pittsburgh, Pennsylvania.

[Privacy]  [Terms]
```

No social icons in V1 unless you want them.

---

## 6. Verification log (run before public launch)

| Claim | Source | Status |
|---|---|---|
| NVIDIA GB10 Grace Blackwell Superchip on ASUS Ascent GX10 | `Asus Ascent GX10.png` ASUS marketing | ✅ confirmed |
| NVIDIA GB10 Grace Blackwell Superchip on Dell Pro Max with GB10 | `Dell Pro Max Desktop with Nvidia Blackwell.pdf` | TODO — extract from PDF |
| 1 petaFLOP FP4 class performance | ASUS marketing + NVIDIA spec | TODO — confirm exact wording |
| 128 GB unified memory class — both SKUs | ASUS + Dell pages | TODO |
| 4 TB M.2 SSD configuration on Dell Pro Max | Dell PDF | TODO — confirm SKU availability |
| 200B-parameter local capacity | NVIDIA + ASUS marketing | TODO |
| Dell ProSupport / ProSupport Plus terms | Dell PDF | TODO — pull exact warranty/support copy |
| FIT Farms LLC ownership language | internal | ✅ confirmed |
| Pittsburgh, PA service area | internal | ✅ confirmed |
| 50-mile radius white-glove inclusion | internal | ✅ confirmed |

I'll close out the TODOs against the OEM PDFs as part of the build pass — this just establishes the discipline that no spec claim ships without source.

---

## 7. Build notes

**Stack:** static site, single repo, deploy to Cloudflare Pages.

- Plain HTML + CSS + minimal JS. No React unless we genuinely need it (Founder Nodes table interactivity is the closest to needing it).
- Tailwind via CDN OR a tiny custom CSS file — either is fine. Avoid heavy build chains.
- Form handler: Cloudflare Functions endpoint at `/api/submit` posting to a forwarding email or to a Google Sheet via the Sheets API. Mailto fallback if JS fails.
- PayPal $1 reservation: hosted PayPal button per tier OR a single PayPal product with a "tier" custom field. Josh sets up the PayPal product; we wire the link.
- Image optimization: serve WebP with PNG fallback; Cloudflare Images can do this automatically.
- Mobile-first. Test on iPhone SE width (375 px).
- Accessibility: real `<button>` and `<a>` tags, proper `<label>` on form fields, alt text on every image, color contrast against the dark theme verified.
- No localStorage for V1. No external icon fonts (use inline SVG icons).
- Privacy / Terms pages stub out at minimum.

**Visual direction:**
- Dark theme: deep charcoal background (~#0F0E0C), warm off-white text (~#F4ECDC), aged-gold accent (~#C9A24A), restrained green only where useful (audience tiles).
- Typography: serif for hero/section headlines (Source Serif 4 or similar), sans for body (Inter or system stack).
- Whitespace generous. Big type. Short copy.
- Section rhythm: text → image → text → comparison grid → motion → text → form.
- Real hardware photography first, custom Golden Quill atmosphere second.

**Out of scope for V1 (declared):**
- AR / 3D model viewer
- Tilth UI screenshots
- Per-audience landing pages (Schools / Farms / etc. each get a tile, not a page)
- Blog
- About page (folded into Home § 5)
- Pricing on the Consulting page
- "LocalGuard" or any new productized security feature name
- Custom-anodized gold keyboard (factory GT80 Gold colorway sufficient)
- Single-cable USB-C / 6K video claim on Pro tier (unverified for Dell)

---

## 8. What ships with V1

- 5 pages (HTML + CSS + minimal JS)
- 1 form endpoint
- 3 PayPal reservation links (one per tier) wired into the Founder Nodes table
- Asset folder organized: `/img/hardware/`, `/img/atmosphere/`, `/img/brand/`, `/video/`
- Sitemap.xml + robots.txt
- Privacy + Terms stubs
- OG / favicon / social preview
- Verification log closed out against OEM sources

---

## 9. What's deferred to V1.x (post-launch)

- Per-audience landing pages (one each for Schools / Farms / Public Agencies / Arts / Co-ops / Intermediaries)
- About / Founder page (Josh's bio + collaborators)
- Proof / Results page (case studies of the three 2026 grant wins, if shareable)
- Blog or newsletter
- Service-menu pricing on Consulting (advisory ladder: $500 onboarding, $250 alert setup, $9/mo radar email, $750+ drafts)
- AR / 3D product viewer
- Tilth UI screenshots once shippable
- Six Worlds detailed pages

---

## 10. Open items requiring Josh's decision before code

1. **Composite hero or product grid?** (Home § 1 — composite needs digital compositing risk; product grid is safer and ChatGPT-warned-against renders are avoided.)
2. **27" monitor model** — Dell U2725QE, or a different choice?
3. **PayPal product setup** — Josh creates the $1 PayPal product on his account and sends the link; I wire it in.
4. **Audience-tile click-through behavior** — pre-fill `/contact?audience=X` (proposed) or stay on Home with no nav (alternative)?
5. **Domain** — `yourgoldenquill.com` (per memory) or a different one?
6. **Privacy / Terms text** — V1 stubs that say "TBD pending counsel review," or skip until v1.x?

---

*End of Build Spec v1. Mark it up directly, send corrections, or tell me what to lock and what to revise.*
