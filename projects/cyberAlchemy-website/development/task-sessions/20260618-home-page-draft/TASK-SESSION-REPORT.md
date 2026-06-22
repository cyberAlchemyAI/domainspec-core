# Task Session Report: SWU-CAW-CONTENT-002 Home Page Draft

Task session: `20260618-home-page-draft`

SWU: `SWU-CAW-CONTENT-002`

Capability: `task-session` using `whisper` preset
`cyberalchemy_site_page`

Status: `completed`

## Objective

Draft the CyberAlchemy Home page from the accepted Home page contract, preserving
source anchors, authority types, claim types, proof/status labels, public/private
boundaries, and first-page visitor clarity.

## Artifacts Created

- `projects/cyberAlchemy-website/development/task-sessions/20260618-home-page-draft/CONTEXT-PACK.md`
- `projects/cyberAlchemy-website/content/drafts/home.md`

## Source Boundary

The task used:

- `projects/cyberAlchemy-website/content/page-contracts/home.md`
- `projects/cyberAlchemy-website/whisper-presets/cyberalchemy-site-page.md`
- `projects/cyberAlchemy-website/research/2026-06-17-content-inventory/findings.md`
- `projects/cyberAlchemy-website/development/invoke-runs/20260618-content-production-route/INVOKE-CONTENT-ROUTE.md`
- `arcanum/framework/CYBERALCHEMY-METHOD.md`
- `arcanum/docs/index.html`
- `projects/ontologize/PUBLIC-OFFERING.md` as analogy pattern only

No public `arcanum` file was changed.

## Result

The Home draft is a first review draft, not accepted website copy.

It includes:

- a `Whisper Result` block
- a composition plan
- a claim map with source anchors, authority types, claim types, and status
  labels
- public-facing Home copy
- review notes and next route

The public copy is 592 words, within the preset's short-page range. It leads
with the reader problem, names CyberAlchemy as a capability-foundry method,
explains the transformation, states proof/status boundaries, and routes readers
to `Read the Method`, `See How It Works`, or a bounded pilot offer.

## Trade-Offs

- Kept the Home page short and offer-led instead of explaining the full
  architecture.
- Used `capability-foundry method` but immediately scoped it as a method, not a
  product/system claim.
- Included a planned pilot CTA, but marked it as offer language rather than
  proof of broad operating capability.
- Avoided the words and concepts most likely to make the first page too
  internal: route, ontology, substrate, residue, promotion, dispatch, token
  budgets, local paths, and private project names.

## Validation

Commands run from `/home/vrondelli/projects/domainspec-core`:

```bash
awk '/^## Public Draft/{flag=1; next} /^## Review Notes/{flag=0} flag' projects/cyberAlchemy-website/content/drafts/home.md | rg -n "route|ontology|substrate|residue|promotion|dispatch|token|/home|projects/|arcanum/|DomainSpec|GoldenQuill|Ontologize" || true
```

Result: no matches.

```bash
awk -F'|' '/^\| .* \|/{ if ($5 ~ /Built/) print NR ":" $0 }' projects/cyberAlchemy-website/content/drafts/home.md || true
```

Result: no claim-map status uses `Built`.

```bash
awk '/[[:blank:]]+$/{print FILENAME ":" FNR ": trailing whitespace"}' projects/cyberAlchemy-website/content/drafts/home.md projects/cyberAlchemy-website/development/task-sessions/20260618-home-page-draft/CONTEXT-PACK.md
```

Result: no trailing whitespace.

```bash
for p in "## Whisper Result" "## Composition Plan" "## Claim Map" "## Public Draft" "### When Good Work Keeps Disappearing" "### A Capability-Foundry Method" "### What Changes" "### Why The Method Is Trustworthy" "### Start Here"; do rg -q "^$p" projects/cyberAlchemy-website/content/drafts/home.md || echo "missing $p"; done
```

Result: no missing sections.

```bash
awk '/^## Public Draft/{flag=1; next} /^## Review Notes/{flag=0} flag' projects/cyberAlchemy-website/content/drafts/home.md | wc -w
```

Result: `592`.

## Completion Check

- Context pack created: pass
- Home draft created: pass
- Required body parts present: pass
- Claim map includes anchors, authority types, claim types, and statuses: pass
- Public copy has no local path/private residue from validation scan: pass
- No claim-map status uses `Built`: pass
- Website implementation deferred: pass
- Review deferred to `SWU-CAW-CONTENT-003`: pass

## Next Route

Run `SWU-CAW-CONTENT-003`: review the Home draft against source anchors,
authority types, public/private boundary, claim <= proof, visitor clarity, tone,
and CTA strength. The expected result is `pass`, `flag`, or `block` with reasons.
