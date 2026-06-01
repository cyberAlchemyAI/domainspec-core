# Golden Quill landing — brief for the next generator

This is an interest-form landing page (no pricing). One prior attempt is in
`/landing/` — read it for what's been tried, then ignore the design. We need
something less boring.

## Source material to feed in

| Folder | What's there |
|---|---|
| `/tilth_v2.pptx` | **Most authoritative content & visual idiom.** 18-slide deck. Pull copy, color palette, illustration style. |
| `/assets/Tilth BluePrint/` | 12 architectural plates + Golden Quill Index plate. Parchment-on-dark idiom. |
| `/assets/cards/customer_identification/` | 6 Customer Identity Cards (Educator, Farm & Food Systems, Municipal Steward, Arts & Culture, Cooperative Lead, Regenerative Systems Supplier). |
| `/assets/cards/capital_logic/` | 8 Capital Logic Cards. |
| `/assets/Decks/GoldenQuillPitch.pptx` | Older deck — reference only. tilth_v2 supersedes. |
| `/site_images/` | 2 SVG diagrams (house, data flow). |
| `/landing/` | Prior attempt. Code, images, Cloudflare Pages Function. Reject the visuals; the structure & copy are mostly locked. |

## What's locked

**Brand**
- Product: **Golden Quill** — the hardware (gold-cased desktop AI node)
- Software inside: **Tilth** — the funding operating system (six-seat AI council)
- Legal entity: **Sovereign Node LLC**, Pittsburgh, PA
- "Sovereign Node" (no LLC) is internal, never customer-facing
- Email: `tilth@yourgoldenquill.com`
- Domain target: `yourgoldenquill.com`

**Hero copy (locked verbatim by operator)**
> # GOLDEN QUILL
> ### Datacenter-class AI compute, *finally affordable for the rest of us.*
> NVIDIA Grace Blackwell — the chip behind the world's largest AI systems — in a desktop your organization can own. Running Tilth, the funding operating system. Your grants, your files, your office.

Spec strip: `NVIDIA Grace Blackwell · 1 PFLOP AI compute · 128 GB unified memory · Tilth OS`

**Cost-class proof block (must be on the page)**
Three-way comparison:
- Datacenter GPU server (DGX H100 / B200 class) — **$200K–$500K+** capex one-time, requires datacenter & IT staff, out of reach for SMBs
- Cloud rental (AWS p5 / Azure ND, equivalent compute) — **$100K+/year** recurring forever, files leave your office
- Golden Quill — **a fraction** of any other capable hardware, on a desk in your office, files stay

Closing line: **"The first cost-effective path for SMBs to own datacenter-class AI."** *(operator's chosen punchline — this line lands the section)*

**Six launch markets — concrete scenarios, not card grids.** Each is a recognition paragraph: *"You run a charter school. The PACSP RFA just dropped. Tilth reads the RFA, drafts your sections from your own enrollment data, scores against the rubric…"* Full text is in `/landing/index.html` — search for `class="scenarios"`.

**Plain-English outcomes, not architecture words.** No "Sovereign Compute," no "Vault-Governed Privacy," no "Funding Operating System" stack diagrams. Translations:
- "Your files never leave your office."
- "Every grant you write becomes memory."
- "You stay the author. Tilth does the labor."
- "One machine. Your whole organization."

**Proof of method.** $339K+ secured in 2026, with named grants:
- $100K Carnegie Mellon University Pathways Fellowship + $3,700/mo stipend
- $125K Robotics Factory Scale + Phantom (residency, grant, match, in-kind)
- $60K SARE Farmer-Led Research — 2 awards, 85% rejection rate
- $50K Braiding Seeds Fellowship — 97% rejection rate
- $4K NJ Career Accelerator Internship Grant, Summer 2026

**Form fields**
- Required: name, email, organization
- Optional qualifying: 10 markets as multi-select checkboxes (the 6 above + Inventor/Scientist/Researcher, Workforce Developer, Conservationist, Tribal/First Nations), role, annual grant volume (Under $50K / $50K–$250K / $250K–$1M / $1M–$5M / $5M+ / None yet), timeline (Ready now / Next 3 / 6 / 6–12 mo / Just exploring), free-text notes
- Action target: `/api/submit` (Cloudflare Pages Function — handler exists at `/landing/functions/api/submit.js`)
- Mailto fallback: `tilth@yourgoldenquill.com`

## What's been ruled out

- Pricing (no Golden Quill price on the page)
- "Regenerative grant intelligence" as the brand line
- A founder note / signed letter
- Slide images of architecture diagrams (Sovereign Compute / Frontier / Tilth OS stack, the Scout-Draft-Score-Track-Report cycle, the Three Pillars) — these are investor-pitch material, not first-buyer
- The "Six Launch Markets" card grid from the deck (we want scenarios, not cards)
- Anything that names "Sovereign Node" customer-facing (Stage-5 only)
- A pure dark/scribal aesthetic (felt heavy, not regenerative)

## Aesthetic direction (open — try something different)

The prior attempt was light cream/walnut/sage/gold editorial. Operator said
boring. Reach further. Possible moves:

- Photography (real images of farms, schools, public buildings, market stalls, art studios) — bring the six worlds to life as people and places, not abstract icons
- Movement: subtle parallax, ink type-on, mycelium-growth, particles
- Dimensional layering: paper textures, layered shadows, depth instead of flat editorial
- Hardware imagery: render or photo of the gold-cased Golden Quill on a real desk — make the machine itself a hero element
- Asymmetric / broken-grid layouts
- A bigger typographic moment for the locked headline
- Color drama: the parchment+gold idiom is the deck's, but the website doesn't have to inherit it 1:1 — try other warm palettes that match "regenerative" + "premium hardware"

## Audience

First buyers, not investors. Four personas to keep in mind:
1. Charter school administrator preparing a state grant
2. Small-farm operator chasing USDA programs
3. Borough manager / municipal grant lead
4. Arts nonprofit director

They are time-poor, AI-skeptical, burned by software promises, live in their grant cycle. They want to know "will this help me with my next grant?"

## Operator notes

- Pittsburgh, PA — locality is part of the brand, real
- Operator does not code. Hand back a deployable artifact (HTML or framework export), not a Figma file. Cloudflare Pages target.
- Form must work or fall back gracefully to mailto.
