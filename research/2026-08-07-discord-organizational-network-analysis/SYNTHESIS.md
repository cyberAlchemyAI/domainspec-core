# Discord API observability and limits on organizational network analysis

Status: repaired reviewer candidate, not final findings. The explorer corpus records documentation observations dated 2026-08-07; mutable pages are not immutable runtime proof, and no runtime or live-target verification occurred. No Discord server was accessed and no collector, study, or organizational inference was executed.

## Independent gates

Every candidate must pass these independently:

1. API observability
2. platform authorization
3. data quality and completeness
4. analytical and construct validity
5. privacy and ethics acceptability
6. organizational decision authority

Passing one gate never passes another.

## Six-gate verdict matrix

`PASS` means this candidate has evidence for this gate only. `BLOCK` stops the candidate. `OPEN` means evidence or an owner decision is absent. `N/A` means the gate does not apply to the bounded candidate. A Discord clarification can affect only platform authorization; it cannot clear data quality, validity, privacy, or decision authority.

| Candidate | API observability | Platform authorization | Data quality | Analytical validity | Privacy/ethics | Decision authority | Overall |
|---|---|---|---|---|---|---|---|
| Live person-linked Discord ONA | `OPEN`: fields are documented in principle; target state is unproved (`research.md`, A1 observability matrix, S1–S10) | `BLOCK`: Developer Policy rule 16 prohibits API-Data profiling of users/relationships and employment-eligibility use (`research.md`, A1 policy blocker and A3 decisive gate, S11/D1 §16) | `OPEN`: no installation, coverage, gaps, denominator, or replay proof | `OPEN`: no construct validation; mechanical graph values are not organizational qualities (A2 question ceiling and metric matrix) | `OPEN`: no acceptance decision; consent, pseudonyms, and admin approval do not cure rule 16 (A3 minimum controls) | `OPEN`: no scope-limited organizational-use authority; HR cannot override policy | **BLOCK** at platform gate |
| Non-relational channel/time aggregates | `OPEN`: counts are documented in principle, not verified on a target | `OPEN`: exact fields, transformations, purpose, and outputs require written Discord clarification (S11/D1 §§15–16) | `OPEN`: no target coverage or denominator evidence | `N/A` for ONA; descriptive event-count validity remains `OPEN` | `OPEN`: no privacy or disclosure determination | `OPEN`: no release or use owner | **HOLD**; Discord clarification is necessary, never sufficient |
| Fully synthetic Discord-shaped paper specification | `N/A`: no API access | `N/A`: no Discord API Data | `PASS` for declared fictional inputs; runtime transformation remains unexecuted | `OPEN`: manual arithmetic is reviewable, but no execution receipt exists | `PASS` only while identifiers and records remain irreversibly fictional | `N/A`: it grants no real organizational-use authority | **ADMIT for paper review only** |
| Voluntary, independently administered self-report ONA | `N/A` | `N/A` only if no Discord-derived data or identifiers enter | `OPEN`: nonresponse, recall, and boundary bias untested (A2 bias register) | `OPEN`: relation-specific construct validation absent | `OPEN`: voluntariness, labor, privacy, and nonparticipant effects undecided (A3 governance return) | `OPEN`: no release/use authority | **HOLD**; no readiness claim |
| Participatory team mapping | `N/A` | `N/A` only if independently created | `OPEN`: participation boundary and missing voices unresolved | `OPEN`: supports participant-authored maps only; protocol unclosed | `OPEN`: participant control and disclosure review undecided | `OPEN`: no release/use authority | **HOLD**; candidate human-governed alternative for owner evaluation |

The non-collapse chain is: `documented field -> analyst-defined graph projection -> graph-theoretic value -> externally tested organizational hypothesis -> separately authorized use`. No arrow is automatic.

## What Discord currently exposes

The current documentation describes REST snapshot or backfill where documented and Gateway forward events where documented for guild membership, roles, channels, messages, replies, mentions, reactions, threads, presence, voice state, audit logs, moderation events, bots, and webhooks. Not every surface has both. These are documented in principle; target-server fields, permissions, history, and coverage are separately unproved.

Key operational limits include privileged `GUILD_MEMBERS`, `GUILD_PRESENCES`, and `MESSAGE_CONTENT` intents; REST message pages of 1–100; member pages of 1–1000; audit-log pages of 1–100 with exactly 45 days retention; dynamic rate-limit buckets; a documented global bot ceiling of 50 requests per second; 10,000 invalid requests per 10 minutes; and a Gateway send limit of 120 events per 60 seconds. These current documentation claims are provisional design inputs, not collection authorization or completeness proof (`research.md`, A1 permissions/rates/history, S1/S4/S8/S10).

Known loss and ambiguity include inaccessible channels, deleted or inaccessible historic messages, edits, unresolved reply targets, forward-only Gateway gaps, departed members, bot/webhook activity, off-platform communication, lack of a native reaction timestamp in Gateway reaction events and REST current reaction state, lack of durable presence history, and lack of native voice speaking turns. Extant accessible messages may be REST-backfilled; that does not reconstruct deleted, inaccessible, or forward-only state (`research.md`, A1 REST versus Gateway and per-surface matrix).

## Candidate event-to-graph bindings

These mappings are mechanically specified for fully synthetic data, or may be investigated over independently collected non-Discord data whose provenance, relation semantics, voluntariness, privacy, and governance are separately established. Governance alone does not establish validity or authority. Every live Discord person-linked binding remains blocked.

| Observation | Candidate graph | Claim ceiling |
|---|---|---|
| Reply | directed author-to-referenced-author edge | authored message referencing another authored message; intent, reading, quality, collaboration, and knowledge flow are unproved (`research.md`, A1 Replies, S3 Message Reference; A2 Reply binding) |
| Mention | directed author-to-mentioned-human edge; no broadcast expansion | explicit mention token; attention, receipt, and relationship are unproved (`research.md`, A1 Mentions, S3 Message Object; A2 Mention binding) |
| Authorship | user-channel bipartite graph, retained as the primary two-mode form | in-scope authorship-event footprint, not engagement or workload (A2 User-channel; Latapy et al. 2008 selector) |
| Role assignment | temporal user-role bipartite affiliation | observed Discord role assignment with unverified organizational and effective-permission meaning. Team analysis requires a separate authoritative, time-bounded roster and construct validation, which still grants no use authority (A1 Roles, S4/S5; A2 User-role) |
| Reaction | tripartite reactor-to-message-from-author structure; self-reactions separate | recorded linkage; acknowledgment, endorsement, polarity, and social meaning are unproved (A1/A2 Reactions, S2/S3) |
| Thread participation | primary user-thread bipartite construction; an explicit derived hyperedge or projection is optional | users authored in-scope events in one thread; exposure and collaboration are unproved (A1 Threads, S2/S6; A2 Thread) |
| Time-ordered projected events | within one declared layer unless an explicit cross-layer coupling is separately specified | order and recurrence, not transmission or causation (A2 Temporal sequence; Holme and Saramäki 2012 §§2–3) |

Layers remain separate by default. A coupling rule and sensitivity analysis are necessary but insufficient for a cross-layer construct; it also requires independent validation and authority. There is no default “social graph.”

## Metric ceilings

Degree, strength, reciprocity, betweenness, PageRank/eigenvector centrality, k-core, brokerage, modularity, assortativity, density, centralization, and temporal stability return graph-theoretic values for one declared partial graph, boundary, layer, and window. They do not describe organizational qualities and cannot be promoted to productivity, performance, importance, leadership, influence, indispensability, trust, cohesion, silos, health, hierarchy, resilience, actual information transfer, misconduct, promotion potential, retention risk, or employment eligibility (A2 metric matrix and abstention rules).

An unavailable population denominator permits, at most, explicitly partial-graph calculations; it blocks population comparisons, rankings, and organizational-community claims. Discord roles are not teams. A team hypothesis requires separately sourced, temporally valid boundary records under a named authoritative owner and discriminating construct evidence; those records remain fallible and grant no use authority.

## Validation and abstention contract

A synthetic arithmetic test requires exact fictional inputs, deterministic projection rules, expected outputs, mutants, and an execution receipt. A real non-Discord study would separately require, at minimum:

- relation-specific surveys whose voluntariness is independently established; surveys are evidence, not gold truth, consent for another data source, or decision authority;
- comparison with separately sourced, temporally valid boundary records under a named authoritative owner;
- blinded coding only under a separately approved purpose, access, privacy/ethics basis, participant protections, and release scope;
- temporal holdout against sender, receiver, channel, and recency baselines;
- stratified missingness simulations;
- predeclared, discriminating negative controls appropriate to the exact relation and sampling design;
- preregistered windows, inclusion rules, metrics, sensitivities, and stop rules.

Failed validation returns `ABSTAIN`; it does not degrade into a weaker organizational claim.

## Privacy and governance boundary

Minimum controls for any materially narrower design, and only after platform clearance, include purpose and field locks, exclusion of DMs, private/restricted channels, message bodies, attachments, voice/video, deleted content, minors, guests, and nonparticipants; predeclared finite retention; cascading deletion; separated identity keys; no cross-server linkage; RBAC; analyst/manager firewall; two-person export review; disclosure testing; low-count and differencing suppression; participant notice; no-detriment choice; auditability; and named incident/release owners. These are necessary but insufficient: every remaining applicable gate still requires its own evidence or decision.

These controls do not make relationship ONA permissible under Discord policy. Stable hashes are pseudonyms, not anonymity. A provisional `k >= 5` release floor is a test fixture, not a safe harbor.

Red lines include live Discord relationship graphs, individual ranks, employment scoring, scraping or self-bots, covert collection, DMs, private/restricted channels, message bodies, attachments, voice/video, deleted content, re-identification, sparse network release, secondary use, and indefinite retention.

## Uncleared non-relational aggregate candidate

Only after the exact design passes API observability, platform authorization, data quality, descriptive-count validity, privacy/ethics, and decision-authority gates could a non-ONA dashboard contain coarse channel/time event totals, bot/webhook share, observed edit/delete counts, a coverage-and-gaps panel, and a retention/review panel. Failure of any applicable gate blocks release. It must not contain node-link diagrams, ego networks, centrality tables, inferred silos, named small groups, sentiment, individual alerts, downloadable microdata, or HR outputs.

## Finite synthetic fixture

All identifiers are invented, content is absent, `synthetic=true`, and every human record has `is_bot=false` and `is_webhook=false` unless stated. This is a manually recomputable paper specification, not a runtime witness.

### Frozen projection configuration

| Field | Value |
|---|---|
| `guild_id` | `g-syn` |
| `window` | `[2026-01-01T09:00:00Z, 2026-01-01T09:15:00Z)` |
| fixed human vertex universe | `{u1,u2,u3,u4,u5,u6}`, including isolates in directed density |
| directed density | simple binary directed arcs, no self-loops, denominator `n*(n-1)` |
| layer policy | reply, mention, reaction, role, channel, and thread layers remain separate |
| channel policy | thread-authored messages roll up to `parent_channel_id` for the user-channel layer |
| thread policy | user-thread bipartite graph is primary; optional projection weight is `1/(n_t-1)` per pair |
| reaction time | `event_time=null`; `observed_at` is collector receipt time and never reaction event time |
| role interval | `[2026-01-01T09:00:00Z, 2026-01-01T09:15:00Z)`; `owner_validated_team=false` |
| suppression fixture | distinct participating humans per parent channel per window; provisional `k=5`; no claim of safe harbor |
| mutation policy | every mutant applies independently to the baseline, then all normalized, graph, aggregate, cache, and export outputs are recomputed |

### Exact normalized baseline records

Empty list fields are `[]`; nulls are explicit.

| id | type | actor | parent channel | thread | message | reply ref | mentions | reaction target/token | event_time | observed_at | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `m1` | `MESSAGE_CREATE` | `u1` | `c-public` | `t1` | `m1` | null | `[]` | null | `09:00Z` | `09:00Z` | human |
| `m2` | `MESSAGE_CREATE` | `u2` | `c-public` | `t1` | `m2` | `m1` | `[]` | null | `09:02Z` | `09:02Z` | human |
| `m3` | `MESSAGE_CREATE` | `u3` | `c-public` | null | `m3` | null | `[u4]` | null | `09:03Z` | `09:03Z` | human |
| `m4` | `MESSAGE_CREATE` | `u4` | `c-public` | null | `m4` | null | `[]` | null | `09:05Z` | `09:05Z` | human |
| `m5` | `MESSAGE_CREATE` | `u5` | `c-public` | `t1` | `m5` | `m2` | `[]` | null | `09:06Z` | `09:06Z` | human |
| `m6` | `MESSAGE_CREATE` | `u1` | `c-small` | null | `m6` | null | `[u6]` | null | `09:07Z` | `09:07Z` | human |
| `m7` | `MESSAGE_CREATE` | `u6` | `c-small` | null | `m7` | `m6` | `[]` | null | `09:08Z` | `09:08Z` | human |
| `x1` | `REACTION_ADD` | `u3` | `c-public` | `t1` | null | null | `[]` | `m1/check` | null | `09:09Z` | human |
| `x2` | `REACTION_ADD` | `u1` | `c-public` | `t1` | null | null | `[]` | `m1/check` | null | `09:10Z` | human, self-reaction control |
| `b1` | `MESSAGE_CREATE` | `bot1` | `c-public` | null | `b1` | null | `[]` | null | `09:11Z` | `09:11Z` | `is_bot=true`; excluded from every human projection |
| `bc1` | `MESSAGE_CREATE` | `u2` | `c-public` | null | `bc1` | null | `[]` | null | `09:12Z` | `09:12Z` | `mention_everyone=true`; adds no mention edge |

Six role records `rs1`–`rs6` use the frozen role interval: `u1,u2,u6 -> role-x` and `u3,u4,u5 -> role-y`. They are exact affiliation records, not validated teams.

The baseline coverage manifest declares both parent channels included for the full window, no known gaps, the fixed six-human population, and complete fictional records by construction. It does not model real sampling completeness.

### Deterministic baseline expectations

| Projection/test | Exact expectation |
|---|---|
| Reply | arcs `{u2->u1,u5->u2,u6->u1}`; out-degree `u2=u5=u6=1`; in-degree `u1=2,u2=1`; reciprocity `0`; density `3/30=0.10` |
| Mention | arcs `{u3->u4,u1->u6}`; broadcast `bc1` adds none; density `2/30=0.0667` |
| User-channel | seven human edges; `c-public={u1,u2,u3,u4,u5}`, `c-small={u1,u6}`; `degree(u1)=2`, others `1`; bot excluded |
| Roles | six user-role edges; each user degree `1`; both role degrees `3`; any team or group-mixing claim is `ABSTAIN(TEAM_BOUNDARY_UNVALIDATED)` |
| Reactions | raw receipts `2`; non-self projected arc `{u3->u1}` weight `1`; self-control `{u1->u1}` count `1`; no latency |
| Thread | bipartite edges `{u1-t1,u2-t1,u5-t1}`; optional projected pairs `{u1,u2},{u1,u5},{u2,u5}` each weight `0.5`, each user strength `1`, total projected weight `1.5` |
| Reply-reference delay | `[2m,4m,1m]`, sorted `[1m,2m,4m]`, median `2m`, mean `7/3m`; it is not human response-time evidence |
| Cross-layer chronology | The 09:02 reply and 09:07 mention are merely chronological events in distinct layers; no temporal path or coupled construct is asserted |
| Suppression | `c-public n=5` may display only the declared coarse count under the fixture rule; `c-small n=2` suppresses; this does not test differencing or complementary suppression |
| Bot/broadcast controls | `b1` is absent from human graphs; `bc1` adds authorship in an already occupied user-channel cell and adds no mention edge |

### Independent deterministic mutants

| Mutant | Exact expected post-state |
|---|---|
| `DELETE_m1` | Purge-derived semantics for this fixture: `m1` becomes a non-attributable tombstone; reply `{u5->u2,u6->u1}`, density `2/30`; reply delays `[4m,1m]`, median `2.5m`; reactions empty; `c-public={u2,u3,u4,u5}`; thread `t1={u2,u5}` with projected pair weight `1`; mentions and roles unchanged; all `m1`-dependent caches/exports invalidated. No author or deleter is inferred from the delete event. |
| `ERASE_u1` | Population becomes `{u2,u3,u4,u5,u6}`; reply `{u5->u2}`, density `1/20`; mention `{u3->u4}`, density `1/20`; reactions empty; `c-public={u2,u3,u4,u5}`, `c-small={u6}`; thread `{u2,u5}` weight `1`; reply median `4m`; roles `role-x={u2,u6}`, `role-y={u3,u4,u5}`; all attributable raw/normalized records, incident edges, aggregates, caches, and exports recomputed. |
| `GAP_c-small` | Remove all `c-small` observations and add coverage record `{channel:c-small,gap_kind:permission,whole_window:true}`; reply `{u2->u1,u5->u2}`, density `2/30`; mention `{u3->u4}`, density `1/30`; reply delays `[2m,4m]`, median `3m`; any cross-channel comparison or ranking returns `ABSTAIN(KNOWN_PERMISSION_GAP)`. Explicit within-`c-public` partial-graph arithmetic may remain labeled partial. |
| `NULL_REPLY_m2` | Set `m2.reply_ref=null`; reply arcs become `{u5->u2,u6->u1}`, density `2/30`; this exact frozen mutation tests that projections do not manufacture a target. It is not called a permutation test. |
| `SUPPRESS_after_ERASE_u1` | Under the provisional fixture rule, `c-public n=4` and `c-small n=1`; both suppress. |

Deterministic query outcomes are `ABSTAIN(TEAM_BOUNDARY_UNVALIDATED)` for “which role is the silo?”, `ABSTAIN(REACTION_SEMANTICS_UNVALIDATED)` for whether `check` means endorsement, and `BLOCK(PROHIBITED_PERSON_RANKING)` for any contributor ranking. No target-permutation, timestamp-shuffle, role-label-permutation, differencing-safety, or stratified-loss claim is made by this finite fixture; those would require separate discriminating fixtures and frozen expected statistics.

Manual reviewer recomputation found the baseline headline arithmetic internally consistent under this now-explicit configuration. No code, collector, Discord data, or validation runtime was executed. Synthetic execution can test internal transformation, arithmetic, and control behavior only; it can never prove a real Discord or organizational study.

## Open candidate decision and review routes

- Discord: written clarification on the exact non-relational fields, transformations, purpose, and outputs; this can reopen only the platform-authorization gate.
- Sponsor/data controller: organization-specific purpose, population, expiry, output, and stop rule.
- Data/coverage owner: population, accessible surfaces, history, gaps, denominators, and quality thresholds.
- Method owner: event constructs, validation thresholds, negative controls, and abstention behavior.
- Ethics/IRB and worker representatives: separate review category, voluntariness, consultation, and nonparticipant-effect determinations.
- DPO/privacy, labor counsel, and jurisdiction-dependent counsel: separate advisory or accountable determinations; one does not substitute for another.
- Security and disclosure-control owners: separate architecture, access, deletion, incident-response, suppression, and release decisions.
- Organizational-use authority: a narrow scope-limited descriptive use after all other gates pass. Executive/HR may acknowledge enforceable non-use but cannot authorize Discord-prohibited employment use.

No such decision is evidenced in this run.

## Evidence closure candidate

| Proposition | Closure |
|---|---|
| Current Discord interfaces and limits exist as documented | Closed for documentation claims only; no live proof |
| Developer Policy rule 16 prohibits API-Data relationship profiling and employment-eligibility use | Closed as the current platform gate; two explorers independently reviewed the same first-party policy source, so this is one authoritative source, not two independent sources |
| Live person-linked Discord ONA falls inside that boundary | Closed candidate: blocked. Discord clarification could reopen only the platform gate; every other gate remains independently unresolved |
| Non-relational aggregates are permitted | Open; written Discord clarification required |
| A target server authorizes access and has complete data | Open; no server access or permission evidence |
| The declared graph bindings are mechanically specified | Candidate-ready for synthetic review only; unexecuted and not organizationally validated |
| Metrics establish organizational constructs | Closed negative: reject or abstain |
| Privacy controls make live relationship ONA acceptable | Closed negative |
| The synthetic fixture proves a real study | Closed negative: synthetic execution can never prove a real Discord or organizational study |
| Any candidate output has organizational decision authority | Closed negative for this run. A permitted non-employment use would need scope-limited authority only after every other gate passes; organizational authority cannot override Discord policy |

Source identities and exact selectors are preserved in `research.md`. This synthesis is a bounded interpretation of that explorer corpus, not a new evidence source.
