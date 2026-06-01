# Golden Quill — landing page

Single-file image-led interest page. Drop-in deployable to Cloudflare Pages.

## What's here

```
landing/
├── index.html                  ← the page (open this locally to preview)
├── images/                     ← slide images, ~2.5 MB total
│   ├── 01-hero-fallback.jpg    ← used as faint hero side-panels (slide 1 of deck)
│   ├── 02-problem.jpg          ← The Problem
│   ├── 03-physical-ai.jpg      ← Golden Quill is Physical AI
│   ├── 04-three-pillars.jpg    ← Physical AI / Vault / Funding OS
│   ├── 05-stack.jpg            ← Sovereign Compute / Frontier / Tilth OS
│   ├── 06-cycle.jpg            ← Scout → Draft → Score → Track → Report
│   ├── 07-how-tilth-enters.jpg ← Supplement / Substitute / Build
│   ├── 08-proof.jpg            ← $339K+ secured in 2026
│   └── 09-six-markets.jpg      ← Six Launch Markets
└── functions/
    └── api/
        └── submit.js           ← Cloudflare Pages Function for form handling
```

## Preview locally

Just open `index.html` in a browser. Form submissions will fail (no backend
locally) and the JS will gracefully fall back to a `mailto:` link.

## Deploy to Cloudflare Pages

1. **Cloudflare dashboard → Workers & Pages → Create → Pages → Upload assets**
2. Drag the entire `landing/` folder. Pages will auto-detect `functions/api/submit.js`.
3. **Settings → Custom domains** → add `yourgoldenquill.com` once registered.

The form will start working immediately — submissions land in **Pages → your
project → Functions → Logs** with prefix `INTEREST_SUBMISSION`. You can scroll
through logs to read every interest as it comes in.

## Wire up email delivery (optional but recommended)

To get every submission as an email:

1. Sign up at **https://resend.com** (free, no card, 3,000 emails/month)
2. **Resend → Domains** → add `yourgoldenquill.com` → add the DNS records
   it shows you (TXT for SPF, CNAMEs for DKIM)
3. **Resend → API Keys** → create one, copy the value
4. **Cloudflare Pages → your project → Settings → Environment variables →
   Production** → add `RESEND_API_KEY` with the value
5. Redeploy. Every submission now emails `tilth@yourgoldenquill.com`.

## Wire up KV storage (optional, additional belt-and-suspenders)

If you want every submission preserved as a record you can list later:

1. **Cloudflare → Workers & Pages → KV → Create namespace** named `golden_quill_submissions`
2. **Pages project → Settings → Functions → KV namespace bindings** →
   bind `SUBMISSIONS` to that namespace
3. Redeploy. Every submission writes a key like `2026-05-08T22:30:00Z_user@example.com`.

## Form fields

Required: `name`, `email`, `organization`.
Optional qualifying: `market[]` (multi), `role`, `scale`, `timeline`, `notes`.

## Editing copy

Hero tagline, section eyebrows/titles/subs, and the form lede are all in
`index.html` — search for the section's eyebrow text (e.g. "Six Launch Markets")
to find the spot.

## Updating slides

When the master deck changes, re-export PNGs/JPGs and replace the file at the
matching name in `images/`. Keep the filenames the same. Recommended export:
1500–2000 px wide, JPG quality 85.
