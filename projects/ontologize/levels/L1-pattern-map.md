# L1 — Pattern Map

Seven reusable patterns extracted from GoldenQuill, each with its generic (company-agnostic)
form. These are the transferable assets of the CyberAlchemy product. Status: **reusable-pattern**
unless noted.

## P1 — Two-axis orthogonal ontology

**GoldenQuill:** CIC (who applies) × CLC (why funding flows), orthogonal, matched at runtime,
never coupled at design time (`F-CIC-CLC-COUPLING-VIOLATION`).
**Generic:** a _subject ontology_ (customer/segment) × a _mechanism ontology_ (revenue/deal/funding
route). Keep the axes independent; match per-opportunity at runtime. Each card carries card
primitives (search vocabulary, evidence schema, language register, reporting rhythm).
**Why it transfers:** any company that serves multiple segments through multiple value mechanisms
has this latent 2-axis structure; hardcoding the cross-product is the common, costly mistake.

## P2 — Signed classification register

**GoldenQuill:** per-org, operator-signed (Ed25519) field→authority-class map
(public / shareable / confidential / operator_flagged) with three-layer defaults.
**Generic:** a _data-governance register_ that gates which data may leave the building (cloud vs
local, internal vs shareable), operator-attested, hash-verified, fail-closed when indeterminate.

## P3 — Promotion record DAG (governed learning)

**GoldenQuill:** events → evidence → candidate → review gates → owner_decision → promoted/retired,
with an 11-rule deterministic validator and an execution DAG kept orthogonal to the ontology DAG.
**Generic:** turn operational runs into a _governed learning loop_: nothing becomes reusable
"truth" without source evidence, a contradiction path, a privacy/redaction check, and an explicit
owner decision. The eight primitives (source-truth; evidence≠candidate≠promotion; metric≠authority;
privacy-safe generalization; mandatory contradiction path; stage≠outcome≠validation; propose-vs-approve
uses; governance orthogonal to execution) are the core IP.

## P4 — Evidence-linked BI / anti-collapse metrics

**GoldenQuill:** KPI families where each metric carries a denominator definition, interpretation
limits, source events, and a promotion owner; receipts trace every claim to a span/coefficient.
**Generic:** _traceable BI_ — every KPI links to its evidence chain so it cannot silently drift;
replaces flat win-rate dashboards with auditable, multi-dimensional scorecards. Includes the
"actual vs counterfactual = delta, with proof" receipt pattern.

## P5 — Ontology-driven agent routing + deterministic gates

**GoldenQuill:** cards + classification register decide which seat runs and cloud-vs-local;
Logician (Python+Cedar, zero-token, fail-closed) enforces laws as PRE/POST gates; cross-family
rigor; Board Health remedy ladder; path-level org isolation.
**Generic:** route a company's _agent workforce_ by ontology, govern it with deterministic
(non-LLM) gates, and require per-agent self-validation ("test your own work") so silent partial
output is impossible.

## P6 — Self-validating agent discipline (Four Autonomy Rules)

**GoldenQuill:** Save State Always; Test Your Own Work (Rule 2, the "magic step"); Be Explicit
(typed handoffs); Clean Output.
**Generic:** a _minimum operating discipline_ for any autonomous agent before it is trusted in a
business workflow — reusable as a maturity checklist in consulting engagements.

## P7 — Governance-deliverable packaging

**GoldenQuill:** the client-sendable package separates value framing / implementation requirements /
reference, and closes with operator decisions that become the spec.
**Generic:** a repeatable _consulting deliverable template_ (README + MANIFEST + HTML overview +
executive brief + reference appendix + client decisions) and a 5-beat value-prop script.

## Cross-cutting insight

GoldenQuill is itself a worked **proof** of the CyberAlchemy thesis in one vertical (grant
intelligence): ontology (cards/registers) + DAG (promotion graph) measurably improved business
intelligence (evidence-linked KPIs) and agent work (governed, routed, self-validating council).
The product generalizes that proof to any company. **[reusable-pattern + proof-by-precedent]**
